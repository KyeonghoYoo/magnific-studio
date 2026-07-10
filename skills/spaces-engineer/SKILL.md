---
name: spaces-engineer
description: |
  Magnific Spaces 그래프 구축·검증·실행 전문 스킬. Use when: (1) spaces_create/spaces_edit/spaces_run 계열 툴을 호출하기 전, (2) 콘티를 Space 노드 그래프로 번역할 때, (3) Space 실행이 실패해 부분 재실행이 필요할 때.
---

# Spaces Engineer — Space 구축과 실행

## 핵심 이해

`spaces_edit`는 노드 JSON을 직접 쓰는 API가 아니라 **자연어 편집 쿼리**를 받는 헤드리스 API다. 따라서 이 스킬의 본질은 "구조화된 콘티 → 정확하고 검증 가능한 편집 쿼리 시퀀스"로의 번역이다.

## 편집-검증 루프 (필수)

1. `spaces_edit(spaceId, query)` — 한 번에 **하나의 논리적 변경**만 요청한다 (노드 몇 개 + 연결). 거대한 쿼리 하나로 그래프 전체를 만들려 하지 않는다.
2. `spaces_edit_status`를 allTerminal까지 폴링.
3. **`spaces_state`(또는 변경 부위만 `spaces_get_nodes`)로 결과 그래프를 읽어 의도와 대조한다.** 노드 타입, 프롬프트 내용, 연결 방향을 확인.
4. 불일치하면 수정 쿼리를 발행한다 — 이때 `selectedElementIds`/`anchorElementId`로 대상을 명시해 모호성을 줄인다.
   - **다중 노드 일괄 편집(find-replace 등)은 부분 반영될 수 있다** (실증: 참조 3개 중 1개만 끊기고 텍스트 교체 누락). 성공 응답이라도 대상 노드 전수를 `spaces_get_nodes`로 재확인하고, 누락분만 노드를 명시해 재시도한다.
   - **prompt 필드 오염 검증(필수)**: 편집 에이전트가 생성/복제한 image·video 노드는 nodeData의 `prompt` 키에 `"Create image-generator"` 같은 지시문 잔재가 남아 **실제 생성 프롬프트에 접두사로 새어 들어간다**(실증: 복제 브랜치 전 노드에서 발견, creations metadata의 prompt에 그대로 노출). 노드 생성 직후 `spaces_get_nodes`로 `prompt` 키를 확인하고, 텍스트 노드 배선 외의 잔재가 있으면 제거 쿼리를 발행한다.
   - **연결 삭제+추가를 한 쿼리에 섞으면 오배선 위험**(실증: prompt 교체 요청에서 last-frame이 삭제됨). 삭제와 추가는 별도 항목으로 명시하고, 완료 후 해당 노드의 연결 전체(prompt/first-frame/last-frame/reference)를 재검증한다.
5. 검증을 통과한 노드 id를 `production_manifest.json`에 기록한다.

검증 없이 다음 편집이나 실행으로 넘어가지 않는다.

## 편집 쿼리 작성 요령

- 노드를 만들 때 프롬프트 전문을 쿼리 안에 그대로 담는다: 「image 노드를 만들어줘. 프롬프트: "..."」
- 위치 지시는 anchor 기반으로: 「<노드>의 오른쪽에 image-to-video 노드를 추가하고 연결해줘」 (`anchorElementId` + `anchorDirection` 병용).
- 캐릭터 참조가 필요한 노드에는 Library 자산/기존 creation을 참조로 연결한다. 기존 creation은 `spaces_add_creations`로 image 노드로 먼저 올린 뒤 와이어로 연결하는 편이 확실하다.
- 모델 지정이 필요하면 쿼리에 명시하고, 검증 단계에서 실제 반영됐는지 확인한다. 반영 불가면 강등 금지 규칙에 따라 blocker 보고.

## 실행 2모드 — 과금 경로에 따라 역할을 나눈다

`account_balance`와 1노드 실측으로 과금 경로를 확정한 뒤 모드를 정한다:

- **agent-run**: MCP 실행도 무제한/저비용이면 에이전트가 `spaces_run`으로 전량 실행.
- **user-run (프롬프트-온리)**: GUI 재생만 무제한이면 **에이전트 = 노드·프롬프트·배선 구축과 검증, 사용자 = GUI 재생 버튼**으로 역할 분담. 이때 에이전트는 (1) 실행 순서를 의존성 기준으로 안내(참조 소스 먼저, 하위 나중), (2) 사용자 실행 후 `spaces_get_nodes`로 `currentCreationIdentifier` 변경을 확인해 결과를 검수, (3) 재생성이 필요한 노드만 콕 집어 다시 안내한다. 한 세션에서 수십 회 반복되는 표준 루프다.

  **실행 카드 형식(정형)**: user-run 안내는 매번 아래 카드로 발행한다 —
  ① 실행할 노드 이름 목록(의존성 순서·단계 구분), ② 각 노드의 기대 산출(무엇이 바뀌어야 하는가), ③ "완료" 신호 후 에이전트가 확인할 것(`currentCreationIdentifier` 변경 + 심사 축). 실행 전 `currentCreationIdentifier` 스냅샷을 기록해 두고, 완료 보고 시 스냅샷과 대조해 **미실행 노드를 자동 검출**한다(실증: 15개 중 1개 누락을 식별자 대조로 발견).

모델 선정 시 무제한 포함 모델 간 비교는 **요구 매트릭스**(duration 지원값 × 시작/끝 키프레임 × 해상도 × 참조 지원)로 한다 — 이름/등급이 아니라 그래프 요구와의 정합으로 결정한다 (실증: 4초+끝프레임+1080p를 동시 충족하는 무제한 모델은 1개뿐이었다).

## 그래프 설계 규약 (콘티 → Space)

- 기본은 **씬당 Space 1개**, 이름은 `<project-slug>/s01 <씬 제목>` 형식. 단, **공용 참조가 많고 user-run 모드면 단일 Space + 영역 분할**이 낫다(바이블 참조를 직접 배선, GUI 실행 동선 단일화). 어느 쪽이든 decision_log에 기록.
- 단일 Space 레이아웃 규약: 캔버스를 열 단위로 — 바이블(캐릭터/프롭/무드) 좌측 → 키프레임 클러스터(씬별 행) 중앙 → 클립 노드 우측. 텍스트 노드는 항상 대응 이미지/비디오 노드의 왼쪽에.
- 숏당 서브그래프: `[캐릭터/키프레임 참조] → image 노드(first_frame) [→ image 노드(last_frame)] → image-to-video 노드`.
- variation_type이 small이면 first_frame만, medium/large면 first+last 두 키프레임을 비디오 노드에 연결한다.
- 공용 참조(캐릭터 3뷰, 씬 앵커 프레임)는 Space 상단에 한 번만 올리고 여러 숏에서 와이어로 재사용한다.

## 실행 규칙

0. **무제한 플랜을 믿지 마라.** 사용자가 "무제한 모델"이라고 해도 GUI와 MCP의 과금 경로가 다를 수 있다 (실증 사례: nano-banana-2-flash 1k가 GUI 재생 버튼 = 0크레딧, MCP `spaces_run` = 75크레딧/장). 반드시 `simulate_spaces` 견적 + 저비용 노드 1개 실측(잔액 전후 비교)으로 검증하고, MCP 경로가 과금이면 "에이전트는 프롬프트·배선만 구축하고 실행은 사용자가 GUI에서" 하는 프롬프트-온리 모드로 전환을 제안한다.
1. **실행 전 `simulate_spaces`로 견적** (같은 startNodeId·mode). 예산 게이트 통과 후에만 실행.
2. `spaces_run`은 기본 `mode: "downstream"` — 성공한 상류를 재과금하지 않는다.
3. 단일 노드 재시도는 `mode: "singular"`.
4. `mode: "connected"`는 성공분까지 다시 돌리는 파괴적 전체 재실행 — 사용자가 명시적으로 전체 재실행을 요청할 때만.
5. `spaces_run_status`로 폴링 (long-poll timeoutSeconds 활용). 터미널 상태에서 산출물은 `creations_show`로 사용자에게 보여주고, identifier를 manifest에 기록.
6. 실패 노드는 원인(프롬프트 문제/모델 문제/일시 오류)을 구분해 프롬프트 수정 후 singular 재실행.
7. **합성(`video_concatenate`)은 크레딧 0 실측** — 자유롭게 반복하되, 1회 최대 10클립이므로 초과분은 파트 분할 후 파트끼리 재합성한다. 배선 수정과 사용자 실행이 동시에 일어나면 레이스가 생긴다 — 배선 변경 후에는 반드시 "지금 재생해도 된다"고 명시하고, 실행 결과의 생성 시각을 배선 완료 시각과 대조한다.

## 참조 이미지 선택 휴리스틱 (키프레임 생성 시)

캐릭터가 등장하는 키프레임은 후보를 **해당 캐릭터 `reference_bank.citation_ids`에서** 고른다(캐릭터 일관성 계약 — core 규칙 5). `enforce_citation=true`면 최소 `min_citations`개를 반드시 배선하고 `primary_ref`를 포함한다. 후보가 많을 때 우선순위:

- 시간순으로 **최근 프레임 우선** (직전 숏의 프레임이 가장 강한 연속성 근거)
- **같은 camera.position_id의 앵커 프레임 우선**(`reference_bank.anchor_frames`) (구도 연속성)
- 캐릭터 3뷰 중에서는 해당 숏의 카메라 방향과 맞는 뷰 **1개만**
- 중복 정보를 주는 참조는 배제, 총 참조 수는 모델 한도 이내(보통 최대 8장)
- 프롬프트에 참조 역할을 명시: "인물의 얼굴은 참조 1을, 배경은 참조 2를 따른다"
- 배선한 참조 id를 manifest의 숏 `references_used`에 기록한다(프로버넌스).
