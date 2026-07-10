#!/usr/bin/env python3
"""render_edit_plan.py — edit_plan.json의 결정적 ffmpeg 실행기.

Magnific Studio /ms-post의 렌더 계층. 에이전트는 창작 결정을 edit_plan.json(EDL)에
기술하고, 이 스크립트가 동일 입력 → 동일 출력(프레임 결정적)을 보증한다.

사용:
  python3 render_edit_plan.py <edit_plan.json> --renders-dir <clips dir> --out <output.mp4>
  옵션: --skip-loudness  --qc-dir <dir>  --deliverable <name>

구현 규약 (post-production-director SKILL Step 3):
  정규화 → 트림(+freeze_tail) → 경계 xfade 블렌드 → concat → 자막 번인 →
  음악 믹스/페이드 → 1차 렌더 → ebur128 실측 → volume 보정 → QC 프레임 추출.
  전환 'dissolve'는 노이즈 디더라 금지 — 'fade'로 강제 치환한다.

전환 구현 노트: SKILL 3c의 누적 오프셋 산식(offset_k = Σd − k·t)과 이 스크립트의
"경계 블렌드 세그먼트 + concat" 방식은 수학적으로 동치다(각 경계에서 앞 t초+뒤 t초를
xfade한 조각을 삽입하고 원 조각에서 t초씩 제거 → 총 길이 Σd − Σt 동일).
블렌드 방식은 하드컷 다수 + 소수 디졸브 구성에서 단일 filter_complex보다 견고하다.
"""
import argparse, json, math, os, re, shlex, subprocess, sys, tempfile

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-4000:] + "\n")
        raise SystemExit(f"[render] 명령 실패: {' '.join(map(shlex.quote, cmd[:8]))} ...")
    return r

def probe_dur(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(r.stdout.strip())

def enc_args(render):
    return ["-r", str(render.get("fps", 24)), "-pix_fmt", render.get("pix_fmt", "yuv420p"),
            "-c:v", render.get("video_codec", "libx264"), "-preset", render.get("preset", "veryfast"),
            "-crf", str(render.get("crf", 19))]

def norm_filter(render):
    w, h = render.get("width", 1080), render.get("height", 1920)
    fps = render.get("fps", 24)
    return (f"fps={fps},scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,format={render.get('pix_fmt','yuv420p')}")

def find_source(entry, renders_dir, plan):
    """timeline.clip_id → 로컬 파일. source.clips[].file 매핑 우선, 없으면 clip_id로 추정."""
    for c in plan.get("source", {}).get("clips", []):
        if c.get("clip_id") == entry["clip_id"] and c.get("file"):
            p = os.path.join(renders_dir, c["file"])
            if os.path.exists(p):
                return p
    for cand in (entry["clip_id"], entry.get("shot_id", "")):
        for ext in (".mp4", ".mov"):
            p = os.path.join(renders_dir, str(cand) + ext)
            if os.path.exists(p):
                return p
    raise SystemExit(f"[render] 소스 없음: {entry['clip_id']} (renders_dir={renders_dir})")

def fingerprint_guard(plan, renders_dir):
    warn = []
    for c in plan.get("source", {}).get("clips", []):
        f = c.get("file")
        if not f:
            continue
        p = os.path.join(renders_dir, f)
        if not os.path.exists(p):
            warn.append(f"missing:{f}")
            continue
        if c.get("size_bytes") and os.path.getsize(p) != c["size_bytes"]:
            warn.append(f"size-mismatch:{f}")
    if warn:
        sys.stderr.write("[render][stale 경고] 소스 지문 불일치 — " + ", ".join(warn) + "\n")
    return warn

def build_pieces(plan, renders_dir, work, render):
    """트림·freeze_tail·경계 xfade 블렌드 → concat 조각 목록과 타임라인 길이 반환."""
    tl = plan["timeline"]
    enc = enc_args(render)
    nf = norm_filter(render)
    lens, srcs = [], []
    for i, e in enumerate(tl):
        src = find_source(e, renders_dir, plan)
        seg = os.path.join(work, f"t{i:02d}.mp4")
        vf = nf
        dur = round(e["out"] - e["in"], 3)
        if e.get("speed") and e["speed"] != 1.0:
            vf += f",setpts=PTS/{e['speed']}"
            dur = round(dur / e["speed"], 3)
        if e.get("freeze_tail"):
            vf += f",tpad=stop_mode=clone:stop_duration={e['freeze_tail']}"
            dur = round(dur + e["freeze_tail"], 3)
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(e["in"]), "-to", str(e["out"]),
             "-i", src, "-an", "-vf", vf] + enc + [seg])
        lens.append(dur); srcs.append(seg)
    # 경계 전환: transition_in이 있는 인덱스 앞 경계를 xfade 블렌드로
    pieces, total = [], 0.0
    i = 0
    head_cut = [0.0] * len(tl)
    tail_cut = [0.0] * len(tl)
    for i, e in enumerate(tl):
        tr = e.get("transition_in") or {}
        ttype = tr.get("type", "cut")
        if ttype == "dissolve":
            ttype = "fade"  # 하드 룰: dissolve 금지 → fade 치환
        if i > 0 and ttype != "cut" and tr.get("duration"):
            D = float(tr["duration"])
            blend = os.path.join(work, f"x{i:02d}.mp4")
            la = lens[i - 1]
            run(["ffmpeg", "-v", "error", "-y", "-i", srcs[i - 1], "-i", srcs[i], "-filter_complex",
                 f"[0:v]trim=start={la - D},setpts=PTS-STARTPTS[a];[1:v]trim=end={D},setpts=PTS-STARTPTS[b];"
                 f"[a][b]xfade=transition={ttype if ttype != 'fade' else 'fade'}:duration={D}:offset=0[v]",
                 "-map", "[v]"] + enc + [blend])
            tail_cut[i - 1] = D
            head_cut[i] = D
            pieces.append(("blend", blend, 0.0, D))
    # 순서 재구성: 각 트림 조각(머리/꼬리 컷 반영) 사이에 블렌드 삽입
    ordered = []
    blend_at = {int(re.search(r"x(\d+)", p[1]).group(1)): p for p in pieces}
    t = 0.0
    for i, e in enumerate(tl):
        a, b = head_cut[i], lens[i] - tail_cut[i]
        cut = os.path.join(work, f"p{i:02d}.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", srcs[i]] + enc + [cut])
        ordered.append(cut); t += b - a
        if (i + 1) in blend_at:
            ordered.append(blend_at[i + 1][1]); t += blend_at[i + 1][3]
    listfile = os.path.join(work, "list.txt")
    with open(listfile, "w") as f:
        for p in ordered:
            f.write(f"file '{os.path.abspath(p)}'\n")
    return listfile, round(t, 3)

def drawtext_chain(plan, total):
    caps = plan.get("captions", [])
    st = plan.get("caption_style", {})
    if not caps or st.get("engine", "drawtext") == "ass":
        return None  # ASS는 별도 파일 경로(captions_file)로 subtitles= 필터 사용 권장
    font = st.get("fontfile", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
    h_margin = st.get("margin_v", 300)
    parts = []
    for c in caps:
        txt = c["text"].replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")
        a, b = c["start"], c["end"]
        alpha = f"clip((t-{a})/0.3,0,1)*clip(({b}-t)/0.3,0,1)"
        parts.append(
            f"drawtext=fontfile={font}:text='{txt}':fontcolor=white:fontsize={st.get('fontsize', 54)}:"
            f"shadowcolor=black@0.6:shadowx=2:shadowy=2:x=(w-text_w)/2:y=h-{h_margin}:"
            f"alpha='{alpha}':enable='between(t,{a},{b})'")
    return ",".join(parts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--renders-dir", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--skip-loudness", action="store_true")
    ap.add_argument("--qc-dir", default=None)
    args = ap.parse_args()

    plan = json.load(open(args.plan))
    render = plan.get("render", {})
    renders_dir = args.renders_dir or plan.get("source", {}).get("renders_dir") or "."
    out = args.out or (plan.get("deliverables") or [{}])[0].get("name", "output.mp4")

    fingerprint_guard(plan, renders_dir)

    with tempfile.TemporaryDirectory(prefix="msrender_") as work:
        listfile, total = build_pieces(plan, renders_dir, work, render)

        # 오디오: 음악 베드 (sync_offset 음수 = 음악 in점을 |offset|초로)
        music = plan.get("audio", {}).get("music", {})
        msrc = music.get("source", "")
        if msrc and not os.path.isabs(msrc) and not os.path.exists(msrc):
            cand = os.path.join(renders_dir, msrc)
            msrc = cand if os.path.exists(cand) else msrc
        have_music = bool(msrc) and os.path.exists(msrc)
        m_in = abs(min(0.0, float(music.get("sync_offset", 0))))
        fade_in = float(music.get("fade_in", 0.5))
        fade_out = float(music.get("fade_out", 1.5))
        gain = float(music.get("gain_db", 0))

        vf = [norm_filter(render)]  # concat 출력 재정규화(안전)
        dt = drawtext_chain(plan, total)
        if dt:
            vf.append(dt)
        vf.append(f"fade=t=in:st=0:d=0.5,fade=t=out:st={max(0, total - 1.0):.3f}:d=1.0")
        fc = f"[0:v]{','.join(vf)}[v]"
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", listfile]
        maps = ["-map", "[v]"]
        if have_music:
            cmd += ["-i", msrc]
            fc += (f";[1:a]atrim=start={m_in}:end={m_in + total:.3f},asetpts=PTS-STARTPTS,"
                   f"afade=t=in:st=0:d={fade_in},afade=t=out:st={max(0, total - fade_out):.3f}:d={fade_out},"
                   f"volume={gain}dB[a]")
            maps += ["-map", "[a]", "-c:a", render.get("audio_codec", "aac"), "-b:a", render.get("audio_bitrate", "192k")]
        pre = out + ".pre.mp4" if (have_music and not args.skip_loudness) else out
        run(cmd + ["-filter_complex", fc] + maps + enc_args(render) +
            (["-movflags", "+faststart"] if render.get("faststart", True) else []) + [pre])

        # 라우드니스 2-pass: 실측 → volume 보정 (비디오 copy)
        if have_music and not args.skip_loudness:
            target = float(plan.get("audio", {}).get("loudness_lufs", -14))
            r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", pre, "-af", "ebur128", "-f", "null", "-"],
                               capture_output=True, text=True)
            m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
            if m:
                measured = float(m[-1])
                delta = round(target - measured, 1)
                run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-c:v", "copy",
                     "-af", f"volume={delta}dB", "-c:a", render.get("audio_codec", "aac"),
                     "-b:a", render.get("audio_bitrate", "192k"), out])
                os.remove(pre)
                print(f"[render] loudness {measured} → {target} LUFS (volume {delta}dB)")
            else:
                os.rename(pre, out)

    dur = probe_dur(out)
    print(f"[render] 완료: {out} ({dur:.2f}s, 계획 {total:.2f}s)")
    if abs(dur - total) > 0.5:
        sys.stderr.write(f"[render][QC 경고] 길이 편차 {abs(dur - total):.2f}s\n")

    # QC 프레임 4지점
    qc_dir = args.qc_dir
    if qc_dir:
        os.makedirs(qc_dir, exist_ok=True)
        for pct in (0.0, 0.33, 0.66, 0.95):
            t = max(0.1, dur * pct)
            run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", out, "-frames:v", "1",
                 os.path.join(qc_dir, f"qc_{int(pct * 100):02d}.jpg")])
        print(f"[render] QC 프레임 4장 → {qc_dir} (육안 점검 필수)")

if __name__ == "__main__":
    main()
