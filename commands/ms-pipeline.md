---
description: "전체 파이프라인 일괄 실행 — 기획→캐릭터→콘티→영상→후반 (각 단계 승인 게이트는 유지)"
argument-hint: "[영상 아이디어]"
---

Magnific Studio 파이프라인 전체를 순서대로 실행한다: 기획 → 캐릭터 → 콘티 → 영상 → 후반.

1. `magnific-studio-core` 스킬을 읽는다.
2. 사용자 아이디어: $ARGUMENTS
3. 각 스테이지마다 해당 디렉터 스킬(`planning-director` → `character-director` → `storyboard-director` → `spaces-engineer`+`production-director` → `post-production-director`)을 읽고 절차를 따른다.
4. **일괄 실행이어도 승인 게이트는 생략하지 않는다** — 각 정본 아티팩트마다 사용자 승인을 받고 다음 단계로 넘어간다. 비용 게이트도 동일하게 적용한다.
5. 기존 프로젝트가 있으면 완료된 스테이지는 건너뛰고 첫 미완료 스테이지부터 재개한다.
