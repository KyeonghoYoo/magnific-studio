#!/usr/bin/env python3
"""Build Claude Desktop-ready skill .zip packages from the plugin's skills/.

Claude Desktop (claude.ai upload path) caps the SKILL.md `description` at 200
characters, while the Claude Code plugin uses longer descriptions. This script
copies each skill, rewrites only the frontmatter `description` to a <=200-char
Desktop variant, and zips each folder (folder as archive root) into dist/.

Change detection: a content hash of each skill's files is compared against the
previous build (desktop/.build-manifest.json). The summary marks each zip as
NEW / CHANGED / unchanged so you only re-upload what actually changed at
https://claude.ai/customize/skills.

Run:  python3 desktop/build.py
Output: desktop/dist/<skill>.zip
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
SRC_EXTRA = os.path.join(ROOT, "desktop", "skills-src")
STAGE = os.path.join(ROOT, "desktop", "_stage")
DIST = os.path.join(ROOT, "desktop", "dist")
MANIFEST = os.path.join(ROOT, "desktop", ".build-manifest.json")

# Desktop-ready descriptions (<=200 chars). Verified: no "claude"/"anthropic",
# lowercase-hyphen names, single-line values.
DESKTOP_DESCRIPTIONS = {
    "magnific-studio-core": "Magnific Studio 파이프라인 횡단 규칙·워크스페이스 규약. Use when: 모든 ms 디렉터 스킬 실행 전 최우선으로, .studio/ 워크스페이스를 읽거나 쓸 때, Magnific 유료 생성 직전.",
    "planning-director": "기획 스테이지 디렉터. Use when: 영상 아이디어로 기획/컨셉을 잡을 때, project_brief.json을 만들거나 수정할 때. 산출물: project_brief.json.",
    "character-director": "캐릭터 생성 스테이지 디렉터. Use when: 캐릭터 시트·외모 확정·Library 자산 등록, characters.json 작성/수정. 산출물: characters.json + Magnific Library 캐릭터 자산.",
    "storyboard-director": "콘티(스토리보드) 스테이지 디렉터. Use when: 숏 리스트·카메라 설계·콘티 작업, storyboard.json을 만들거나 수정할 때. 산출물: storyboard.json.",
    "production-director": "영상 제작 스테이지 디렉터. Use when: 키프레임/클립 생성·합성·오디오, production_manifest.json 작성/갱신. spaces-engineer와 함께 사용. 산출물: production_manifest.json + 영상.",
    "spaces-engineer": "Magnific Spaces 그래프 구축·검증·실행 전문. Use when: spaces_create/edit/run 호출 전, 콘티를 Space 노드 그래프로 번역할 때, Space 실행 실패로 부분 재실행이 필요할 때.",
    "quality-reviewer": "생성 산출물 자동 자기검수(QA) 교차 스킬. Use when: 키프레임/클립/최종 렌더를 승인 게이트에 올리기 직전, 증거 기반 승인이 필요할 때. 산출물: 축별 review(점수+verdict+issues).",
    "post-production-director": "후반 편집 디렉터 — edit_plan.json 계획 수립. Use when: 컷/트랜지션/음악/자막/파생본을 설계할 때. 주의: 실제 ffmpeg 렌더는 Claude Code 전용, Desktop은 계획까지만.",
    # New Desktop-only entrypoint skill (source in desktop/skills-src/)
    "magnific-studio-quickstart": None,  # keep its own frontmatter as-authored
}

DESKTOP_NOTE = (
    "> **Claude Desktop 제약**: 이 스킬의 실제 렌더링(ffmpeg·librosa·WhisperX·libass)은 "
    "Desktop 코드 실행 환경에서 사용할 수 없다. Desktop에서는 `edit_plan.json` 계획 수립까지만 "
    "수행하고, 최종 렌더는 **Claude Code**에서 실행한다.\n\n"
)


def rewrite_description(skill_md_path, new_desc):
    with open(skill_md_path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---"):
        raise SystemExit(f"No frontmatter: {skill_md_path}")
    # Split into ['', frontmatter, body] on the '---' fences.
    _, _frontmatter, body = text.split("---", 2)
    body = body.lstrip("\n")
    esc = new_desc.replace('"', '\\"')
    name = os.path.basename(os.path.dirname(skill_md_path))
    return f'---\nname: {name}\ndescription: "{esc}"\n---\n\n{body}'


def content_hash(skill_dir):
    """Stable hash over all files in a staged skill dir (path + bytes)."""
    h = hashlib.sha256()
    for dirpath, _dirs, files in os.walk(skill_dir):
        for fn in sorted(files):
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, skill_dir)
            h.update(rel.encode("utf-8"))
            with open(fp, "rb") as f:
                h.update(f.read())
    return h.hexdigest()


def main():
    prev = {}
    if os.path.isfile(MANIFEST):
        try:
            with open(MANIFEST, encoding="utf-8") as f:
                prev = json.load(f)
        except (json.JSONDecodeError, OSError):
            prev = {}

    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(STAGE)
    os.makedirs(DIST, exist_ok=True)

    manifest = {}
    statuses = []  # (name, status)
    for name, desc in DESKTOP_DESCRIPTIONS.items():
        src = os.path.join(SKILLS, name) if desc is not None else os.path.join(SRC_EXTRA, name)
        if not os.path.isdir(src):
            print(f"skip (missing): {name}")
            continue
        stage_dir = os.path.join(STAGE, name)
        shutil.copytree(src, stage_dir)
        skill_md = os.path.join(stage_dir, "SKILL.md")

        if desc is not None:
            new_text = rewrite_description(skill_md, desc)
            # Inject the ffmpeg limitation note for post-production.
            if name == "post-production-director":
                head, sep, rest = new_text.partition("\n\n")
                new_text = head + sep + DESKTOP_NOTE + rest
            with open(skill_md, "w", encoding="utf-8") as f:
                f.write(new_text)

        # Validate description length (<=200) from the staged file.
        with open(skill_md, encoding="utf-8") as f:
            fm = f.read().split("---", 2)[1]
        for line in fm.splitlines():
            if line.startswith("description:"):
                val = line[len("description:"):].strip().strip('"')
                if len(val) > 200:
                    raise SystemExit(f"{name}: description {len(val)} > 200 chars")

        digest = content_hash(stage_dir)
        manifest[name] = digest
        zip_path = os.path.join(DIST, f"{name}.zip")
        if name not in prev:
            status = "NEW"
        elif prev[name] != digest:
            status = "CHANGED"
        else:
            status = "unchanged"
        statuses.append((name, status))

        # Always (re)write the zip so dist/ is complete; the status tells the
        # user which ones actually need re-uploading.
        if os.path.exists(zip_path):
            os.remove(zip_path)
        subprocess.run(["zip", "-rq", zip_path, name], cwd=STAGE, check=True)

    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2, sort_keys=True)
    shutil.rmtree(STAGE)

    changed = [n for n, s in statuses if s in ("NEW", "CHANGED")]
    print("빌드 결과 (desktop/dist/):")
    for name, status in statuses:
        mark = {"NEW": "🆕", "CHANGED": "✏️ ", "unchanged": "  "}[status]
        label = "" if status == "unchanged" else f"  <- {status}"
        print(f"  {mark} {name}.zip{label}")

    print()
    if changed:
        print(f"재업로드 필요 ({len(changed)}개) — claude.ai/customize/skills에서 교체:")
        for n in changed:
            print(f"  - {n}.zip")
    else:
        print("변경 없음 — Desktop 재업로드 불필요.")


if __name__ == "__main__":
    sys.exit(main())
