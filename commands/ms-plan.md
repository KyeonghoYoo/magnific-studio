---
description: "1단계 기획 — 아이디어를 project_brief.json으로 확정"
argument-hint: "[영상 아이디어]"
---

Magnific Studio 파이프라인의 **기획** 스테이지를 실행한다.

1. `magnific-studio-core` 스킬을 읽는다 (워크스페이스·게이트 규칙).
2. `planning-director` 스킬을 읽고 그 절차를 따른다.
3. 사용자 아이디어: $ARGUMENTS (비어 있으면 아이디어를 먼저 물어본다)

기존 `.studio/` 프로젝트가 있으면 이어서 작업할지 새 프로젝트인지 확인한다.
산출물: `.studio/<project>/project_brief.json` (사용자 승인 필수).
