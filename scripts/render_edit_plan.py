#!/usr/bin/env python3
"""render_edit_plan.py — edit_plan.json의 결정적 ffmpeg 실행기.

Magnific Studio /ms-post의 렌더 계층. 에이전트는 창작 결정을 edit_plan.json(EDL)에
기술하고, 이 스크립트가 동일 입력 → 동일 출력(프레임 결정적)을 보증한다.

사용:
  python3 render_edit_plan.py <edit_plan.json> --renders-dir <clips dir> --out <output.mp4>
  옵션: --skip-loudness  --qc-dir <dir>  --deliverable <name>

구현 규약 (post-production-director SKILL Step 3):
  정규화 → 트림(+freeze_tail) → 경계 xfade 블렌드 → concat → (show LUT) → 자막 번인 →
  오디오 믹스/페이드 → 1차 렌더 → ebur128 실측 → volume 보정 → QC 프레임 추출.

v2 (filmcraft): 전환은 편집실 어휘(soft_cut/dissolve/fade_through_black/dip_to_white/...)로
  기술하고 TRANSITION_MAP이 ffmpeg xfade로 번역한다. v1 이름은 경고 후 수용.
  ffmpeg의 'dissolve'(노이즈 디더)는 어떤 경로로도 노출하지 않는다.
  duration_ms(정본, ms) 우선 — 구 duration(초)도 수용.
  audio.music_cues/sfx/ambience가 있으면 다중 요소 amix 그래프(ffmpeg ≥4.4 — amix
  normalize=0 필요), 없으면 v1 단일 음악 베드 경로를 그대로 사용(결정성 보존).
  licensed 큐는 license 미기재 시 렌더 차단. color.show_lut은 lut3d로 균일 적용.
  render.opening_fade_ms/end_fade_ms로 머리/꼬리 페이드 설정(기본 500/1000ms).

전환 구현 노트: SKILL 3c의 누적 오프셋 산식(offset_k = Σd − k·t)과 이 스크립트의
"경계 블렌드 세그먼트 + concat" 방식은 수학적으로 동치다(각 경계에서 앞 t초+뒤 t초를
xfade한 조각을 삽입하고 원 조각에서 t초씩 제거 → 총 길이 Σd − Σt 동일).
블렌드 방식은 하드컷 다수 + 소수 디졸브 구성에서 단일 filter_complex보다 견고하다.
"""
import argparse, json, math, os, re, shlex, subprocess, sys, tempfile

# ── 전환 어휘(v2): 스키마는 편집실 언어, 렌더러가 ffmpeg로 번역한다 ──────────────
# ffmpeg xfade의 'dissolve'(노이즈 디더)는 생성 클립에서 지지직거려 어떤 경로로도 노출하지 않는다.
TRANSITION_MAP = {
    "cut": None,
    "soft_cut": "fade",            # 200–400ms 기술적 보정(첫 프레임 톤 팝) — 시간 의미 없음
    "dissolve": "fade",            # 크로스디졸브 = 시간 경과
    "fade_through_black": "fadeblack",
    "dip_to_white": "fadewhite",
    "wipe_left": "wipeleft", "wipe_right": "wiperight",
    "slide_up": "slideup", "slide_down": "slidedown",
    "iris_open": "circleopen", "iris_close": "circleclose", "clock_wipe": "radial",
}
LEGACY_TRANSITIONS = {  # v1 이름 → v2 이름 (경고 후 수용)
    "fade": "dissolve", "fadeblack": "fade_through_black", "fadewhite": "dip_to_white",
    "wipeleft": "wipe_left", "wiperight": "wipe_right",
    "slideup": "slide_up", "slidedown": "slide_down",
    "circleopen": "iris_open", "radial": "clock_wipe",
}

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
    trims = (plan.get("color") or {}).get("scene_trims") or []

    def trim_filters(shot_id):
        """shot_id에 매칭되는 scene_trims → eq/colorbalance 필터 문자열 목록(선언 순서 유지)."""
        parts = []
        for t_ in trims:
            if shot_id and shot_id in (t_.get("shot_ids") or []):
                eq = t_.get("eq") or {}
                if eq:
                    parts.append("eq=" + ":".join(f"{k}={eq[k]}" for k in eq))
                cb = t_.get("colorbalance") or {}
                if cb:
                    parts.append("colorbalance=" + ":".join(f"{k}={cb[k]}" for k in cb))
        return parts

    lens, srcs = [], []
    for i, e in enumerate(tl):
        src = find_source(e, renders_dir, plan)
        seg = os.path.join(work, f"t{i:02d}.mp4")
        vf = nf
        for tf in trim_filters(e.get("shot_id")):
            vf += "," + tf  # 정규화 직후·xfade 이전 — 블렌드 조각에도 자동 반영
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
        if ttype in LEGACY_TRANSITIONS:
            mapped = LEGACY_TRANSITIONS[ttype]
            sys.stderr.write(f"[render][v1 호환] transition '{ttype}' → '{mapped}'\n")
            ttype = mapped
        if ttype not in TRANSITION_MAP:
            sys.stderr.write(f"[render][경고] 미지원 전환 '{ttype}' → cut 처리\n")
        xf = TRANSITION_MAP.get(ttype)
        dur_ms = tr.get("duration_ms")
        D = float(dur_ms) / 1000.0 if dur_ms is not None else float(tr.get("duration") or 0)
        if i > 0 and xf and D > 0:
            blend = os.path.join(work, f"x{i:02d}.mp4")
            la = lens[i - 1]
            run(["ffmpeg", "-v", "error", "-y", "-i", srcs[i - 1], "-i", srcs[i], "-filter_complex",
                 f"[0:v]trim=start={la - D},setpts=PTS-STARTPTS[a];[1:v]trim=end={D},setpts=PTS-STARTPTS[b];"
                 f"[a][b]xfade=transition={xf}:duration={D}:offset=0[v]",
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
        lut = (plan.get("color") or {}).get("show_lut")
        if lut:
            lp = lut if os.path.isabs(lut) or os.path.exists(lut) else os.path.join(renders_dir, lut)
            if os.path.exists(lp):
                vf.append(f"lut3d=file={lp}")  # 그레이드(균일 show LUT) → 자막 번인 순서
            else:
                sys.stderr.write(f"[render][경고] show_lut 파일 없음: {lut} — 미적용\n")
        dt = drawtext_chain(plan, total)
        if dt:
            vf.append(dt)
        ofade = float(render.get("opening_fade_ms", 500)) / 1000.0
        efade = float(render.get("end_fade_ms", 1000)) / 1000.0
        fparts = []
        if ofade > 0:
            fparts.append(f"fade=t=in:st=0:d={ofade}")
        if efade > 0:
            fparts.append(f"fade=t=out:st={max(0, total - efade):.3f}:d={efade}")
        if fparts:
            vf.append(",".join(fparts))
        fc = f"[0:v]{','.join(vf)}[v]"
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", listfile]
        maps = ["-map", "[v]"]

        # ── 오디오 그래프(v2): music_cues/sfx/ambience가 있으면 다중 요소 amix(ffmpeg ≥5),
        #    아니면 v1 단일 음악 베드 경로를 그대로 사용(기존 렌더 결정성 보존) ──
        audio_cfg = plan.get("audio", {})
        cues = list(audio_cfg.get("music_cues") or [])
        sfx_list = list(audio_cfg.get("sfx") or [])
        amb_list = list(audio_cfg.get("ambience") or [])
        for c in cues:
            if c.get("provenance") == "licensed" and not c.get("license"):
                raise SystemExit(f"[render] licensed 큐에 license 미기재: {c.get('cue_id', '?')} — 납품 차단")

        def _resolve(p):
            if p and not os.path.isabs(p) and not os.path.exists(p):
                q = os.path.join(renders_dir, p)
                return q if os.path.exists(q) else p
            return p

        vo = audio_cfg.get("voiceover") or {}
        vsrc = _resolve(vo.get("source", ""))
        have_vo = bool(vsrc) and os.path.exists(vsrc)
        if vo.get("source") and not have_vo:
            sys.stderr.write(f"[render][경고] VO 소스 없음: {vo.get('source')} — 미믹스\n")

        use_mix = bool(cues or sfx_list or amb_list or have_vo)
        have_audio = False
        if use_mix:
            if have_music and not cues:  # legacy 단일 베드 → M1 승격
                cues = [{"cue_id": "M1", "source": msrc, "in": 0.0, "out": None, "source_in": m_in,
                         "gain_db": gain, "fade_in": fade_in, "fade_out": fade_out}]
            elems, idx = [], 1
            bed_labels, sfx_labels = [], []  # bed(music+ambience)만 VO 사이드체인 덕킹 대상, SFX 제외
            for c in cues:
                src = _resolve(c.get("source", ""))
                if not src or not os.path.exists(src):
                    sys.stderr.write(f"[render][경고] 큐 소스 없음: {c.get('cue_id', '?')} — 건너뜀\n")
                    continue
                t_in = float(c.get("in", 0))
                t_out = c.get("out")
                t_out = float(t_out) if t_out is not None else total
                seg = max(0.1, t_out - t_in)
                s_in = float(c.get("source_in", 0))
                fi, fo = float(c.get("fade_in", 0.5)), float(c.get("fade_out", 1.5))
                g = float(c.get("gain_db", 0))
                ch = (f"[{idx}:a]atrim=start={s_in}:end={s_in + seg:.3f},asetpts=PTS-STARTPTS,"
                      f"afade=t=in:st=0:d={fi},afade=t=out:st={max(0, seg - fo):.3f}:d={fo},"
                      f"volume={g}dB,adelay={int(t_in * 1000)}:all=1[m{idx}]")
                cmd += ["-i", src]
                elems.append((f"[m{idx}]", ch)); bed_labels.append(f"[m{idx}]"); idx += 1
            for a_ in amb_list:
                src = _resolve(a_.get("source", ""))
                if not src or not os.path.exists(src):
                    sys.stderr.write("[render][경고] 앰비언스 소스 없음 — 건너뜀\n")
                    continue
                t_in = float(a_.get("in", 0))
                t_out = a_.get("out")
                t_out = float(t_out) if t_out is not None else total
                seg = max(0.1, t_out - t_in)
                fi, fo = float(a_.get("fade_in", 0.5)), float(a_.get("fade_out", 0.5))
                g = float(a_.get("gain_db", -18))
                ch = (f"[{idx}:a]atrim=start=0:end={seg:.3f},asetpts=PTS-STARTPTS,"
                      f"afade=t=in:st=0:d={fi},afade=t=out:st={max(0, seg - fo):.3f}:d={fo},"
                      f"volume={g}dB,adelay={int(t_in * 1000)}:all=1[m{idx}]")
                cmd += ["-i", src]
                elems.append((f"[m{idx}]", ch)); bed_labels.append(f"[m{idx}]"); idx += 1
            for s_ in sfx_list:
                src = _resolve(s_.get("source", ""))
                if not src or not os.path.exists(src):
                    sys.stderr.write(f"[render][경고] SFX 소스 없음: {s_.get('id', '?')} — 건너뜀\n")
                    continue
                at = float(s_.get("at_sec", 0))
                g = float(s_.get("gain_db", 0))
                ch = f"[{idx}:a]asetpts=PTS-STARTPTS,volume={g}dB,adelay={int(at * 1000)}:all=1[m{idx}]"
                cmd += ["-i", src]
                elems.append((f"[m{idx}]", ch)); sfx_labels.append(f"[m{idx}]"); idx += 1
            duck = have_vo and bool(vo.get("duck", True)) and bool(bed_labels)
            if have_vo:
                v_start = float(vo.get("start_sec", 0))
                v_gain = float(vo.get("gain_db", 0))
                tail = ",asplit=2[vok0][vomix]" if duck else "[vomix]"
                ch = f"[{idx}:a]asetpts=PTS-STARTPTS,volume={v_gain}dB,adelay={int(v_start * 1000)}:all=1{tail}"
                if duck:
                    # 사이드체인 키를 타임라인 길이로 무음 패딩 — 안 하면 VO가 끝나는 지점에서
                    # sidechaincompress가 bed 출력을 함께 끊어 음악이 조기 종료된다
                    ch += f";[vok0]apad=whole_dur={total:.3f}[vok]"
                cmd += ["-i", vsrc]
                elems.append(("[vomix]", ch)); idx += 1
            if elems:
                fc += ";" + ";".join(ch for _, ch in elems)
                if duck:
                    # bed(음악+앰비언스) 서브믹스 → VO 키로 사이드체인 덕킹(하우스 레시피, post SKILL 3d) → SFX·VO와 최종 amix
                    if len(bed_labels) > 1:
                        fc += (";" + "".join(bed_labels) +
                               f"amix=inputs={len(bed_labels)}:duration=longest:dropout_transition=0:normalize=0[bed]")
                    else:
                        fc += f";{bed_labels[0]}anull[bed]"
                    fc += ";[bed][vok]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[bedduck]"
                    final = ["[bedduck]"] + sfx_labels + ["[vomix]"]
                else:
                    final = [lbl for lbl, _ in elems]  # VO 부재 시 기존 그래프와 byte-identical (결정성 보존)
                fc += (";" + "".join(final) +
                       f"amix=inputs={len(final)}:duration=longest:dropout_transition=0:normalize=0,"
                       f"atrim=end={total:.3f}[a]")
                maps += ["-map", "[a]", "-c:a", render.get("audio_codec", "aac"), "-b:a", render.get("audio_bitrate", "192k")]
                have_audio = True
        elif have_music:
            cmd += ["-i", msrc]
            fc += (f";[1:a]atrim=start={m_in}:end={m_in + total:.3f},asetpts=PTS-STARTPTS,"
                   f"afade=t=in:st=0:d={fade_in},afade=t=out:st={max(0, total - fade_out):.3f}:d={fade_out},"
                   f"volume={gain}dB[a]")
            maps += ["-map", "[a]", "-c:a", render.get("audio_codec", "aac"), "-b:a", render.get("audio_bitrate", "192k")]
            have_audio = True
        pre = out + ".pre.mp4" if (have_audio and not args.skip_loudness) else out
        run(cmd + ["-filter_complex", fc] + maps + enc_args(render) +
            (["-movflags", "+faststart"] if render.get("faststart", True) else []) + [pre])

        # 라우드니스 2-pass: 실측 → volume 보정 (비디오 copy)
        if have_audio and not args.skip_loudness:
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
