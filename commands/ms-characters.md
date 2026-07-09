---
description: "2단계 캐릭터 — 캐릭터 시트 확정, 3뷰 생성, Magnific Library 등록"
argument-hint: "[프로젝트 슬러그 (생략 시 자동 탐색)]"
---

Magnific Studio 파이프라인의 **캐릭터 생성** 스테이지를 실행한다.

1. `magnific-studio-core` 스킬을 읽는다.
2. 대상 프로젝트: $ARGUMENTS (생략 시 `.studio/`에서 탐색, 복수면 사용자에게 확인)
3. **게이트 확인**: `project_brief.json`의 `approved_by_user`가 true가 아니면 중단하고 /ms-plan부터 안내한다.
4. `character-director` 스킬을 읽고 그 절차를 따른다.

산출물: `.studio/<project>/characters.json` + Magnific Library 캐릭터 자산 (사용자 승인 필수).
