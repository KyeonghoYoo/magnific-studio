---
description: "4단계 영상 제작 — Spaces 구축, 키프레임/클립 생성, 합성 (비용 견적 게이트 포함)"
argument-hint: "[프로젝트 슬러그 (생략 시 자동 탐색)]"
---

Magnific Studio 파이프라인의 **영상 제작** 스테이지를 실행한다.

1. `magnific-studio-core` 스킬을 읽는다.
2. 대상 프로젝트: $ARGUMENTS (생략 시 `.studio/`에서 탐색)
3. **게이트 확인**: `project_brief.json`, `characters.json`, `storyboard.json` 모두 `approved_by_user: true`이고 `stale`이 아니어야 한다. 아니면 중단하고 필요한 단계를 안내한다.
4. `spaces-engineer`·`production-director`·`quality-reviewer` 스킬을 읽고 production-director의 절차를 따른다.
5. **하드 룰**: 크레딧이 소모되는 모든 실행 전에 simulate 계열 툴로 견적을 내고 사용자 승인을 받는다. 키프레임·클립은 `quality-reviewer` 자동 자기검수(`review`) 후 증거와 함께 승인 게이트에 올린다. 캐릭터 등장 생성은 `reference_bank` 인용 필수(core 규칙 5).

산출물: `.studio/<project>/production_manifest.json` + 최종 영상.
