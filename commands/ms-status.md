---
description: "프로젝트 진행 상황 보고 — 스테이지 상태, 비용, 다음 할 일"
argument-hint: "[프로젝트 슬러그 (생략 시 전체)]"
---

Magnific Studio 프로젝트 상태를 보고한다. **읽기 전용 — 아무것도 생성하거나 수정하지 않는다.**

1. `magnific-studio-core` 스킬을 읽는다.
2. 대상: $ARGUMENTS (생략 시 `.studio/` 아래 모든 프로젝트)
3. 각 프로젝트에 대해 보고한다:
   - 스테이지별 상태 (draft / awaiting_approval / approved / stale) 와 정본 아티팩트 존재 여부
   - production_manifest가 있으면: 숏별 진행 상황 (succeeded/running/failed/pending 집계), 실패 숏과 사유
   - 비용: 견적 대비 지출 (`cost` 필드), 필요 시 `account_balance`로 잔액 확인
   - decision_log의 최근 주요 결정 3~5건
   - **다음 할 일**: 어느 커맨드로 무엇을 하면 되는지 한 줄 안내
4. Space가 있으면 각 Space의 webUrl을 함께 제공한다.
