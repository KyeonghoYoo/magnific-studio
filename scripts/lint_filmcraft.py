#!/usr/bin/env python3
"""lint_filmcraft.py — filmcraft 통제 어휘 정합성 린트 (결정적).

검사:
  1. 스키마 enum ⊆ 사전 — filmcraft 소유 enum 값이 references/*.md 어딘가에 등장하는가
  2. 금지 별칭이 스키마 enum에 없음 (push_in, slow_push_in, tracking, orbit, steadicam, gimbal, cowboy, fade, dissolve-as-v1…)
  3. 레퍼런스 파일 ≤500줄 (파일 규율)
  4. KR gloss 존재 (레퍼런스마다 한국어 포함)
  5. 디렉터 스킬이 참조하는 filmcraft 파일이 실제 존재
  6. 빈 토큰이 프롬프트 권장 문구로 쓰이지 않음 (blocklist 문맥 밖 등장 탐지 — prompting.md 제외)

사용: python3 scripts/lint_filmcraft.py   (repo 루트에서)
종료코드: 0=전체 통과, 1=실패 존재
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "skills", "filmcraft", "references")
FAILS, WARNS = [], []

def fail(msg): FAILS.append(msg)
def warn(msg): WARNS.append(msg)

# ── 레퍼런스 코퍼스 로드 ──────────────────────────────────────────────
ref_files = sorted(glob.glob(os.path.join(REF, "*.md")))
corpus = {}
for p in ref_files:
    corpus[os.path.basename(p)] = open(p, encoding="utf-8").read()
all_text = "\n".join(corpus.values()).lower()
if not ref_files:
    fail("references/*.md 없음")

# ── 1. 스키마 enum ⊆ 사전 ────────────────────────────────────────────
def collect_enums(node, path=""):
    out = []
    if isinstance(node, dict):
        if "enum" in node and isinstance(node["enum"], list):
            out.append((path, [v for v in node["enum"] if isinstance(v, str)]))
        for k, v in node.items():
            out += collect_enums(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out += collect_enums(v, path)
    return out

# filmcraft 소유 enum 경로 화이트리스트(부분 문자열 매치)
OWNED = ["shot_size", "angle", "movement", "framing", "function", "composition_tags",
         "lighting", "transition_in", "diegesis", "film_stock", "lens_character",
         "grain", "diffusion", "harmony", "pattern", "ratio", "key_direction",
         "key_quality", "time_of_day", "exposure_bias", "screen_direction",
         "beat_snap", "support", "subject_relation", "dof"]
# 파이프라인 상태/운영 enum은 사전 검사 제외
SKIP_VALUES = {"pass", "fail", "na", "warn", "revise", "pending", "draft", "awaiting_approval",
               "approved", "left", "right", "up", "down", "in", "out", "cw", "ccw",
               "none", "null", "true", "false", "photo", "video", "generated", "licensed",
               "snap", "offset", "off", "native", "blur_pad", "pad", "center_crop",
               "auto_reframe", "action", "revelation", "brand", "activation", "keep",
               "strip", "sfx_only", "ass", "drawtext", "agent", "user", "normal",
               "motivated", "stylized", "score", "source"}

for schema_name in ("storyboard", "project_brief", "edit_plan"):
    sp = os.path.join(ROOT, "schemas", f"{schema_name}.schema.json")
    schema = json.load(open(sp, encoding="utf-8"))
    for path, values in collect_enums(schema):
        if not any(k in path.lower() for k in OWNED):
            continue
        for v in values:
            if v in SKIP_VALUES or len(v) <= 2 or ":" in v:
                continue
            token = v.lower()
            # snake_case 값은 그대로 또는 공백/하이픈 변형으로 사전에 존재해야 한다
            variants = [token, token.replace("_", " "), token.replace("_", "-")]
            if not any(t in all_text for t in variants):
                fail(f"[enum⊆사전] {schema_name}:{path} 값 '{v}' — references/*.md에 없음")

# ── 2. 금지 별칭이 enum에 없음 ────────────────────────────────────────
BANNED_ENUM = {"push_in", "pull_back", "slow_push_in", "tracking", "orbit", "steadicam",
               "gimbal", "cowboy", "american_shot", "dutch", "fade", "fadeblack",
               "fadewhite", "wipeleft", "wiperight", "slideup", "slidedown",
               "circleopen", "radial", "j_cut", "l_cut", "soundtrack", "magic_hour",
               "day_for_night", "golden_ratio", "camera_height", "recruitment"}
for schema_name in ("storyboard", "project_brief", "edit_plan"):
    sp = os.path.join(ROOT, "schemas", f"{schema_name}.schema.json")
    schema = json.load(open(sp, encoding="utf-8"))
    for path, values in collect_enums(schema):
        for v in values:
            if isinstance(v, str) and v.lower() in BANNED_ENUM:
                fail(f"[금지 별칭] {schema_name}:{path} 에 금지 값 '{v}'")

# ── 3. 파일 규율 ≤500줄 ──────────────────────────────────────────────
for name, text in corpus.items():
    n = text.count("\n") + 1
    if n > 500:
        fail(f"[파일 규율] {name} {n}줄 > 500")
    elif n > 460:
        warn(f"[파일 규율] {name} {n}줄 (500 임박)")

# ── 4. KR gloss 존재 ─────────────────────────────────────────────────
hangul = re.compile(r"[가-힣]")
for name, text in corpus.items():
    if name == "model-matrix.md":
        continue  # 데이터 부록은 면제
    if not hangul.search(text):
        fail(f"[KR gloss] {name} 에 한국어 gloss 없음")

# ── 5. 스킬 참조 무결성 ──────────────────────────────────────────────
skill_files = glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))
ref_pat = re.compile(r"filmcraft/references/([a-z0-9\-]+\.md)")
for sf in skill_files:
    text = open(sf, encoding="utf-8").read()
    for m in set(ref_pat.findall(text)):
        if not os.path.exists(os.path.join(REF, m)):
            fail(f"[참조 무결성] {os.path.relpath(sf, ROOT)} → 없는 파일 {m}")
# SKILL.md 인벤토리와 실제 파일 대조
skill_md = os.path.join(ROOT, "skills", "filmcraft", "SKILL.md")
if os.path.exists(skill_md):
    inv = set(re.findall(r"([a-z0-9\-]+\.md)", open(skill_md, encoding="utf-8").read()))
    actual = {os.path.basename(p) for p in ref_files}
    for m in inv - actual - {"SKILL.md"}:
        fail(f"[인벤토리] SKILL.md가 없는 파일 참조: {m}")
    for m in actual - inv:
        warn(f"[인벤토리] SKILL.md 인덱스 누락: {m}")

# ── 6. 빈 토큰이 권장 문구로 쓰이지 않음 ─────────────────────────────
EMPTY_TOKENS = ["masterpiece", "best quality", "trending on artstation", "octane render",
                "unreal engine 5", "score_9", "highly detailed"]
for name, text in corpus.items():
    if name in ("prompting.md",):
        continue  # 블록리스트 정의 파일은 면제
    low = text.lower()
    for tok in EMPTY_TOKENS:
        for m in re.finditer(re.escape(tok), low):
            ctx = low[max(0, m.start() - 120):m.end() + 120]
            if not any(k in ctx for k in ("ban", "blocklist", "placebo", "금지", "empty", "avoid", "never", "reject")):
                fail(f"[빈 토큰] {name}: '{tok}' 이 금지 문맥 밖에서 등장")

# ── 결과 ─────────────────────────────────────────────────────────────
print(f"filmcraft lint — refs {len(ref_files)}개, 실패 {len(FAILS)}, 경고 {len(WARNS)}")
for f in FAILS:
    print("FAIL", f)
for w in WARNS:
    print("WARN", w)
sys.exit(1 if FAILS else 0)
