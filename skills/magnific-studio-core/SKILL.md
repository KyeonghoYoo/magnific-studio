---
name: magnific-studio-core
description: |
  Magnific Studio 파이프라인의 횡단 규칙과 워크스페이스 규약. Use when: (1) /ms-* 커맨드가 실행될 때 — 모든 디렉터 스킬보다 먼저 읽는다, (2) .studio/ 프로젝트 워크스페이스를 읽거나 쓸 때, (3) Magnific MCP로 비용이 발생하는 생성을 실행하기 직전.
---

# Magnific Studio — Core 계약

이 스킬은 모든 스테이지에 적용되는 불변 규칙이다. 디렉터 스킬과 충돌하면 이 스킬이 우선한다.

## 파이프라인

```
기획(/ms-plan) → 캐릭터(/ms-characters) → 콘티(/ms-storyboard) → 영상(/ms-produce) → 후반(/ms-post)
       ↑ 교차 계층: format-director(포맷 규칙 주입) · quality-reviewer(증거 기반 심사) · spaces-engineer(그래프 실행)
```

포맷 규칙과 영화 문법이 충돌하면 **포맷 규칙이 우선**한다(format-director). 모든 생성 호출의 모델·프롬프트(리라이트 전후)·시드·비용은 manifest에 직렬화한다 — 어떤 산출물도 단독 재현 가능해야 한다(ComfyUI 재현성 철학).

## filmcraft — 기법 사전 (v1.1)

`skills/filmcraft/`는 전 부서 영화 기법의 **정본 사전**이다. 매 스테이지는 추론 대신 사전을 참조한다:

| 스테이지 | 먼저 읽는 레퍼런스 |
|---|---|
| 기획 | story-structure, emotion-recipes (+ production-design, color-grading의 world/palette 절) |
| 캐릭터 | production-design(의상·실루엣), lenses-optics(포트레이트) |
| 콘티 | shot-grammar, camera-movement, lighting, directing-mise-en-scene, emotion-recipes |
| 영상 | prompting(프롬프트 프로젝션 — 필수), camera-movement, lighting, animation-motion, vfx-compositing(하이브리드), model-matrix(캠페인마다 재검증) |
| 후반 | editing-grammar, sound-music, color-grading |
| 심사 | 해당 부서 파일의 QA 열 + prompting의 pre-flight lint |

**횡단 하드 룰(사전에서 승격):**
1. **통제 어휘** — 아티팩트의 카메라·조명·전환 필드는 filmcraft canonical 값만. 금지 별칭(push_in, slow_push_in, tracking, orbit, steadicam…)은 저장 전에 해소한다.
2. **프롬프트 프로젝션** — 프롬프트 문자열은 아티팩트에 저장하지 않는다. produce 시점에 prompting.md의 결정적 테이블로 아티팩트에서 렌더한다(아티팩트=모델-프리, 모델 사실=capability 플래그+model-matrix).
3. **빈 토큰 차단(pre-flight lint, 생성 전 0원)** — masterpiece/8k/highly detailed/artstation/award-winning/octane render 등 금지. "cinematic"은 구체 기술 명사(필름스톡·기종·mm·f값·조명 패턴·비율) 동반 시만. 부정 구문(no/without/avoid+명사) 금지 — 긍정 재구성.
4. **씬 조명 잠금** — 씬 lighting 구조체에서 렌더된 조명 문장을 그 씬 모든 키프레임 프롬프트에 byte-identical 주입. 숏 오버라이드는 사유 기록.
5. **진실 표기** — 스티치드 원테이크를 "single take"로 표기 금지("연속 테이크로 설계"). 좌우 반전(flop)으로 방향 오류를 고치지 않는다(재생성 또는 뉴트럴 인서트).

각 스테이지는 정확히 하나의 정본 아티팩트를 산출한다. 다음 스테이지는 정본 아티팩트만 신뢰하고, 대화 기억에 의존하지 않는다.

| 스테이지 | 정본 아티팩트 | 스키마 |
|---|---|---|
| 기획 | `project_brief.json` | `schemas/project_brief.schema.json` |
| 캐릭터 | `characters.json` | `schemas/characters.schema.json` |
| 콘티 | `storyboard.json` | `schemas/storyboard.schema.json` |
| 영상 | `production_manifest.json` | `schemas/production_manifest.schema.json` |
| 후반 | `edit_plan.json` + 최종 납품 파일(들) + manifest 갱신 | `schemas/edit_plan.schema.json` |

## Magnific 자산 계층 — Library-first 원칙 (횡단 하드 룰)

Magnific의 재사용 자산 표면을 전 스테이지가 인덱싱하고 활용한다. **재사용 시각 정체성은 creation이 아니라 Library 자산이 정본**이다.

| Library 카테고리 | 무엇 | 등록 시점 | 생성 참조 타입 | 소유 스킬 |
|---|---|---|---|---|
| `character` | 인물·동물 정체성 (3뷰 시트 포함) | /ms-characters | `references{type:character}` | character-director |
| `product`(element) | 제품·소품·차량·바이크 | /ms-characters(동반 프롭) · /ms-plan(브랜드 제품) | `type:product` | character-director |
| `locations` | 반복 등장 장소 플레이트 | /ms-storyboard에서 식별 → /ms-produce에서 등록 | `type:locations` | production-director |
| `style` | 룩 LoRA / 스타일 포토 | /ms-plan에서 `visual_grammar.look` 잠금 시 검토 | `type:style` | planning-director |
| `color` | 팔레트 자산 (`visual_grammar.palette` 공유·재사용) | /ms-plan | (Seedance video: `type:color`) | planning-director |
| `template`·brandKit | 온-브랜드 생성 (`images_generate`의 `brandKitId`/`templateSlug`) | 브랜드 캠페인 반복 시 | 파라미터 | planning-director |
| flows (`flows_list/run/wait`) | 저장된 그래프 재실행 — 반복 파이프라인 | 동일 구조 재생산 시 검토 | — | spaces-engineer |
| `agent`·`context` | 생성 보조 프리셋 | 현재 활용 규칙 없음 — 인덱스만 | — | — |

**하드 룰:**
1. **인벤토리 우선**: 각 스테이지 시작 시 `library_list`(type 지정)로 기존 자산을 확인한다 — 있는 자산을 재생성하지 않는다(중복 `library_create` 금지, 수정은 `library_edit`).
2. **배선은 Library id로**: 캐릭터·제품·장소가 등장하는 생성 노드의 정체성 참조는 **반드시 Library 자산 id**로 배선한다. raw creation 참조가 허용되는 경우는 정확히 둘 — ①키프레임 간 **구도 연속성 앵커**(Library에 없는 정보), ②일회성 참조. (실증: 파일럿 1에서 front 시트 creation만 와이어 → Library의 3뷰가 정체성 계산에 미기여하는 결함.)
3. **중복 참조 금지**: Library 자산에 이미 포함된 이미지를 creation으로 병행 배선하지 않는다 — 같은 정보의 이중 가중은 특정 뷰 편향을 만든다(실증: front 이중 가중).
4. brandKitId 대응 list 도구는 현재 MCP 표면에 없다 — 브랜드 정합은 Library `color`/`template` + 실물 로고 합성으로 달성하고, sqid를 이미 알 때만 `brandKitId`를 쓴다.

## 워크스페이스 규약

프로젝트 루트는 현재 작업 디렉토리의 `.studio/<project-slug>/`이다. slug는 소문자-하이픈.

```
.studio/<project-slug>/
├── project_brief.json
├── characters.json
├── storyboard.json
├── production_manifest.json
├── edit_plan.json            # 5단계(후반) 정본 — edit-as-data EDL
├── decision_log.jsonl        # append-only
└── renders/                  # 다운로드 산출물 (후반 소재, 원본 보존)
```

- 커맨드 시작 시 항상 워크스페이스를 먼저 읽어 현재 상태를 파악한다. 아티팩트가 이미 있으면 재생성하지 않고 이어서 작업한다 (idempotent resume).
- 모든 정본 아티팩트는 공통 헤더를 가진다: `{"project": slug, "stage_status": "draft"|"awaiting_approval"|"approved", "approved_by_user": bool, "stale": bool, "updated_at": ISO8601}`.
- 쓰기 전에 해당 스키마 파일과 대조해 필수 필드를 검증한다. 검증 실패 상태로 저장하지 않는다 (fail-fast).

## 게이트 규칙 (하드 룰)

1. **승인 게이트(증거 기반)**: 이전 스테이지 아티팩트의 `approved_by_user`가 `true`가 아니면 다음 스테이지를 시작하지 않는다. 승인은 사용자에게 아티팩트 요약을 보여주고 명시적으로 받는다 (AskUserQuestion 가능 환경이면 사용). **생성 산출물(키프레임·클립·최종 렌더)의 승인은 `quality-reviewer`의 자동 자기검수(`review`)를 먼저 붙여 증거와 함께 제시한다** — review 없이 승인 게이트를 올리지 않는다. verdict가 pass인 것만 승인 후보.
2. **비용 게이트**: 크레딧이 소모되는 실행(`spaces_run`, `images_generate`, `video_generate`, `audio_*` 등) 전에 반드시 `simulate_spaces` 또는 `simulate_cost`로 견적을 내고, `project_brief.budget_cap_credits`와 비교해 사용자 승인을 받는다. 견적 없는 실행 금지. 러프 콘티용 저비용 이미지 1장 수준의 미세 비용도 최초 1회는 고지한다. 견적과 별개로 **과금 경로는 실측**한다 — 같은 모델도 GUI/MCP 경로에 따라 0크레딧과 과금으로 갈린다(spaces-engineer의 실행 2모드 참조). `account_balance`의 `unlimitedAppliesHere` 필드와 1노드 실행 전후 잔액 비교가 근거다.
3. **증거 원칙**: 툴 결과나 파일 상태가 증명하지 않는 한 기획·생성·렌더가 완료되었다고 주장하지 않는다.
4. **강등 금지**: 모션(영상) 요청을 정지 이미지로, 사용자가 확정한 모델을 다른 모델로 조용히 대체하지 않는다. 불가능하면 blocker로 보고하고 결정을 요청한다.
5. **캐릭터 일관성 계약**: `characters.json`의 `consistency_policy.enforce_citation=true`이면, 캐릭터가 등장하는 모든 키프레임 생성은 해당 캐릭터 `reference_bank`의 참조 id를 최소 `min_citations`개 인용(배선)해야 한다. 텍스트 프롬프트만으로 정체성을 지어내는 생성 금지. 인용 id는 manifest `references_used`에, 일관성 심사는 `consistency_check`에 기록한다(character-director / production-director).

## Decision Log

유의미한 선택(모델, 보이스, Space 구조, 컨셉 채택, 예산 트레이드오프)은 `decision_log.jsonl`에 한 줄씩 append:

```json
{"ts": "...", "stage": "produce", "category": "video_model", "subject": "s01_sh03", "options_considered": [{"option": "...", "rejected_because": "..."}], "selected": "...", "reason": "..."}
```

같은 결정이 번복되면 삭제하지 말고 같은 `(category, subject)`로 새 엔트리를 append한다. 최신 엔트리가 현재 결정이다.

## Stale 전파

상류 아티팩트가 수정되면 하류 아티팩트 전부에 `stale: true`를 마킹하고, 무엇을 재실행해야 하는지 사용자에게 보고한다. stale한 아티팩트를 입력으로 렌더를 실행하지 않는다.

## 식별자 위생

creation/space/run identifier는 아티팩트 파일에만 기록한다. 사용자 대화에는 이름, 제목, `webUrl`만 노출한다.

## 실패 처리

- 장시간 job은 polling 툴(`spaces_run_status`, `creation_status`)로 추적하고, 진행 상황을 `production_manifest.json`에 기록한다.
- 부분 실패 시 성공분은 보존하고 실패 노드만 재실행한다. 전체 재실행(connected 모드)은 사용자가 명시적으로 요청할 때만.
- API 오류 메시지를 사용자에게 전달할 때 키·토큰류 문자열은 마스킹한다.
