---
description: "3단계 콘티 — 구조화된 숏 리스트(storyboard.json) 작성"
argument-hint: "[프로젝트 슬러그 (생략 시 자동 탐색)]"
---

Magnific Studio 파이프라인의 **콘티(스토리보드)** 스테이지를 실행한다.

1. `magnific-studio-core` 스킬을 읽는다.
2. 대상 프로젝트: $ARGUMENTS (생략 시 `.studio/`에서 탐색)
3. **게이트 확인**: `project_brief.json`과 `characters.json` 모두 `approved_by_user: true`여야 한다. 아니면 중단하고 이전 단계를 안내한다.
4. `storyboard-director` 스킬을 읽고 그 절차를 따른다.

산출물: `.studio/<project>/storyboard.json` (사용자 승인 필수).
