---
name: storyboard-director
description: |
  콘티(스토리보드) 스테이지 디렉터. Use when: (1) /ms-storyboard 실행, (2) 숏 리스트/카메라 설계/콘티 작업, (3) storyboard.json을 만들거나 수정할 때. 산출물: storyboard.json.
---

# Storyboard Director — 콘티

먼저 `magnific-studio-core` 스킬을 읽었는지 확인한다. 입력: 승인된 `project_brief.json` + `characters.json`.

## 시작 전 — filmcraft 라우팅

콘티 설계 전에 `filmcraft/references/`의 **shot-grammar, camera-movement, lighting, directing-mise-en-scene, emotion-recipes**를 읽는다. 감정/목표가 정해진 씬은 emotion-recipes의 부서 합의 레시피에서 출발한다. 모든 필드 값은 filmcraft canonical 어휘만 사용한다.

## 씬 구조 (schemas/storyboard.schema.json v2 — scenes[])

숏보다 먼저 **씬 계약**을 쓴다. 조명 플롯·180° 축은 씬에 한 번 쓰고 숏이 상속한다(숏별 재기술 = 패러프레이즈 = #1 AI 실패):

- `scenes[].lighting` — time_of_day, key_direction, key_quality, **ratio**(flat_1_1…extreme_16_1), **contrast_proxy**(lighting.md 정본 테이블에서 그대로 — 창작 금지), color_temp_k+gloss, pattern, motivation, exposure_bias. 이 구조체에서 렌더된 조명 문장이 씬 전 키프레임 프롬프트에 **byte-identical** 주입된다. 숏 오버라이드는 사유 기록.
- `scenes[].axis` — 지오그래피/마스터 숏이 180° 축을 그린다(a/b 캐릭터, a_side). 축 교차는 4가지 합법 경로만(뉴트럴 숏 경유가 파이프라인 기본).
- `scenes[].type` — normal | montage_sequence(시간압축, 1–3s 숏, 음악 주도). `cut_sync`는 hype/comedy만 beat_grid.

## 장소 자산 마킹 — 환경 플레이트 독트린 (Library-first, 필수)

**씬 환경은 캐릭터와 동급의 정체성이다.** 조명 문장은 빛·시간대·날씨를, 로케이션 팔레트는 색을 잠그지만, **형태(도로 곡률·차선·수종·지형·계절)는 참조 이미지 없이는 잠기지 않는다**(실증: 파일럿 1 — 같은 조명 문장의 씬 키프레임 4장이 계곡 도로→가드레일 산길→가을 들판으로 발산, 계절까지 이탈).

- 한 장소에 **2개 이상 숏**이 있으면 그 씬은 **환경 마스터 플레이트**가 필요하다 — 콘티에 마킹(`scenes[].palette_note`에 "환경 플레이트 필수").
- produce 절차: 씬의 첫 키프레임(또는 전용 빈 환경 플레이트)을 먼저 생성·채택 → `library_create(type: locations)` 등록 → **그 씬 나머지 모든 키프레임에 참조 배선** + 프롬프트에 "the same [환경] as the reference location" 지시.
- **3중 잠금**: 조명 문장(빛·시간·날씨) + location_palettes(색) + locations 플레이트(형태).

## 숏 구조

숏마다 카메라를 **구조화된 필드**로 기술한다 — 자유 텍스트에 묻지 않는다:

- `camera.shot_size`: extreme_wide | wide | full | **medium_full**(허벅지 중간 — cowboy/american은 별칭) | medium | medium_close_up | close_up | extreme_close_up — 컷라인 정의는 shot-grammar.md. 씬 내 2단 초과 점프는 플래그.
- `camera.angle`: eye_level | low | high | overhead(90° 직하·근접) | underneath(90° 직상) | bird_eye(고도 부감) | worm_eye(지면 앙각) — 기하 정의. `dutch_deg`(0–45)는 별도 롤 필드(로우앵글+더치 동시 표현 가능).
- `camera.framing`: single | two_shot(정확히 2인) | group | empty_frame | ots | pov(+`pov_of` 필수) + `dirty`(bool). `camera.function`: establishing | master | insert | cutaway | reaction | transition — **편집 역할**(프레임만 봐선 판별 불가). establishing/insert/cutaway는 기본 stock 후보.
- `camera.movement`: **객체 — 숏당 정확히 1개(1무브 법칙)**: `{base, direction, speed, support, subject_relation, arc_degrees, foreground_anchor}`. base 13종·유효 방향·리스크 티어(green/amber/red — red는 포스트 폴백 선기록)는 camera-movement.md. **dolly/truck은 `foreground_anchor` 필수**(없으면 모델이 줌으로 렌더 — 시차 부재); pedestal/crane/arc는 강력 권장 — 개방/공중 프레임처럼 전경면이 없으면 `parallax_note`(배경면 전단)로 대체. 금지 별칭(push_in/pull_back/slow_push_in/tracking/orbit/steadicam/gimbal)은 저장 전 해소.
- `camera.lens_mm`: 정수, **풀프레임 환산**(전역 규칙). `camera.dof`: shallow|medium|deep (ots/dirty는 shallow 자동).
- `camera.composition_tags`: ≤3개 (rule_of_thirds ⊕ centered_symmetry 상호배타).
- `screen_direction` + `gaze_target`: 이동·시선이 있는 숏 필수 — 180° 축 기계 검증의 원료. 시선은 각도 수치가 아니라 타깃으로("to_camera", "at:alice", "off_left").
- `camera.position_id`: 같은 물리적 카메라 포지션 그룹 키

그리고 렌더 경계를 만드는 3분해:

- `first_frame_desc` — 첫 프레임의 **정적 스냅샷** (조명 문장은 쓰지 않는다 — 씬 lighting에서 주입)
- `last_frame_desc` — 마지막 프레임의 정적 스냅샷 (variation_type이 small이면 null)
- `motion_desc` — 그 사이의 카메라 무브먼트 + 인물 동작

## 작법 하드 룰

1. **정적 스냅샷 규칙**: 프레임 묘사에 진행형·예정 동작 금지. "그가 일어서려 한다" ❌ → "그가 의자에 앉아 상체를 약간 앞으로 기울이고 있다" ✅
2. **캐릭터 지칭은 포크된다(식별자 핸들 규칙).** 콘티에는 안정 플레이스홀더 `{{char:key}}` + appearance_phrase만 저장한다(모델-프리). 해소는 produce의 프롬프트 프로젝션: ①참조가 배선되고 모델이 명명 태그를 지원하면(@name·<<<name>>>·@Image N — capability 플래그) **모델 네이티브 태그**, ②태그 미지원이면 appearance_phrase+참조 이미지. **`motion_desc`는 항상 외형 문구다** — 프레임에 2인 이상일 때 비디오 모델은 누가 움직이는지 외형으로만 구분한다. "Alice가 걷는다" ❌ → "짧은 머리에 초록 원피스를 입은 여성이 걷는다" ✅ (외형 문구는 characters.json에서 **verbatim** — 패러프레이즈 금지)
3. **첫 숏은 씬 환경을 확립하는 최대한 넓은 숏**으로 시작한다 — 단 ①숏폼은 포맷 규칙이 이긴다(훅 우선, 설정 숏 생략 — format-director), ②설정 숏이 필요하면 `function: establishing`으로 표기하고 **기본 stock 후보**로 처리한다(모델은 와이드 다요소 지오그래피에 가장 약하고, 설정 숏은 정의상 캐릭터·브랜드 식별자가 없다 — 생성 예산을 쓰지 않는 것이 기본).
4. **카메라 포지션 재사용 우선**: 새 숏을 설계할 때 기존 position_id로 찍을 수 있는지 먼저 검토하고, 사이즈·앵글·포커스가 크게 다를 때만 새 포지션을 만든다. 큰 무브먼트를 겪은 포지션은 이후 재사용하지 않는다.
5. **단계적 숏 사이즈 전환**: wide → medium → close-up 순의 이웃 전환만. long shot에서 close-up으로 직접 점프 금지.
5-1. **감정 비트 = MCU 이상 + 플레이어블 액션(병합 규칙).** 표정이 서사를 나르는 숏(반전·설렘·해소)은 medium_close_up 이상으로 당겨 찍되, **반드시 기술된 신체 동작(타동사)을 함께 준다** — "she clutches the letter to her chest" ✅, "she is sad" ❌. 생성 모델의 미세 표정은 **어떤 사이즈에서도** 신뢰 불가하므로 감정의 1차 운반체는 몸·실루엣이다(실루엣 테스트: 검은 윤곽만으로 감정이 읽히는가). 잠금 프레이밍으로 워핑을 막을 때는 `{base: dolly, direction: in, speed: slow}` 같은 최소 무브먼트 + moving hold(미세 지속동작)를 남겨 생동감을 보존한다.
6. **대사는 dialogue 배열에 구조화** (speaker, emotion, line). 효과음·환경음은 sound 배열에.
6-0. **비율 파생은 크롭이 아니라 재구도다.** 9:16 세로 파생 시 가로 구도를 그대로 옮기지 말 것 — 측면 병주 투샷은 좁은 세로 프레임에서 반복적으로 마주보는 구도로 붕괴한다(실증 2회). 세로 대체 문법: 병주 투샷 → 후방 추적(뒤에서 나란히 멀어지는), 로우앵글 와이드 → 강변 측면 수평띠 구도(하단 피사체/중단 수면/상단 스카이라인). 랜드마크는 실물 구조 특징(잠수교=낮고 평평한 거더교, 타워·케이블 없음)을 명시해 재해석 왜곡을 막는다. 공유 모션 프롬프트가 새 구도와 어긋나면 비율 전용 모션 텍스트로 분리한다.
6-1. **복수 이동체(차량·바이크·인물 다수)가 함께 이동하는 숏은 공유 진행 방향을 화면 기준으로 명시**한다. 관용구는 **관계 유형별로 정반대**다 — 잘못 빌려 쓰면 정확히 반대 구도가 나온다(실증 2건):
   - **동행(나란히)**: "both traveling left to right, seen in side profile, parallel, never facing each other, never oncoming" — 마주보기·교차 방지.
   - **교차(oncoming)**: "riding in the OPPOSITE direction, coming toward the camera, the front of the vehicle and its headlight facing the viewer, in the opposite lane" — **정면·헤드라이트의 시각 신호를 명시**해야 한다. "approaching ... ahead"는 '앞서 가는 동방향'으로, 동행용 "never facing each other"를 교차 신에 쓰면 **등돌림**으로 해석된다(실증: 파일럿 1 — oncoming 3키프레임 전부 동방향 주행으로 생성).
   씬 내 스크린 디렉션(180도 규칙)도 이때 함께 고정한다.
7. 민감 요소는 대체물 치환 (피 → 케첩 등).
8. **씬 전환마다 연결 비트를 검사한다.** 장소가 바뀌는 컷은 이동/도착/원인 중 하나로 이어야 한다 — "채비 → (컷) → 이미 도착해 있음"처럼 비트가 빠지면 점프로 느껴진다(실증). 전환 브리지 패턴: (a) 도착 컷 — 주체가 프레임 밖에서 새 장소로 진입, (b) 매치컷 — 앞 숏이 시선/동작으로 끝나고 뒷 숏 첫 프레임에 그 대상(접근하는 헤드라이트 등)이 존재, (c) 인서트 경유. 등장 대기 컷(빈 장소에 주체의 소유물이 먼저 있는 구도)은 연속성 모순을 만들기 쉬우니 피한다.

## 편집 문법 부록 (정전 기반 — 위반은 차단이 아니라 플래그. 전체 컷 유형학·전환 의미론은 filmcraft/editing-grammar.md)

- **컷 판단 가중(Murch Rule of Six)**: 컷/트림/전환을 결정할 때 감정(51%) > 스토리 진전(23%) > 리듬(10%) > 시선 유도(7%) > 화면 문법(5%) > 공간 연속(4%) 순으로 판단한다. 하위 규칙(180° 등)과 감정·스토리가 충돌하면 상위를 따르되 decision_log에 남긴다.
- **180° 축**: 신마다 액션 축을 정하고 모든 숏의 카메라를 한쪽 반원에 배치한다. 축을 넘어야 하면 중립 숏(축 위/이동 숏)을 삽입한다. 복수 이동체 방향 규칙(6-1)은 이 축의 특수형이다.
- **30° 규칙**: 같은 피사체를 잇는 인접 숏은 앵글 30° 이상 또는 숏 사이즈 2단계 이상 차이 — 아니면 점프컷 플래그.
- **eye-trace**: 앞 숏에서 관객 시선이 머문 화면 좌표 근처에 다음 숏의 관심 대상을 배치한다(실전: 시선→헤드라이트 매치컷).
- **데쿠파주 vs 커버리지(용어 정확)**: 클립 상한(5–10s)이 강제하는 것은 **데쿠파주**(숏 분해 — 필수)이지 커버리지가 아니다. **커버리지**(마스터+싱글+인서트의 중복 대안 확보 = 편집 보험)는 생성 비용이 드는 **히어로 신 전용 지출**이다. 브릿지 신은 단일 designed 숏으로 족하다. 검증: 3숏 이상 씬은 insert/cutaway/reaction 중 ≥1개 포함(솔기 은폐 + 편집 유연성 — 대개 캐릭터가 없어 stock으로 해결).
- **신 가치전환(McKee)**: 각 씬은 가치값을 +→− 또는 −→+로 뒤집어야 한다. 시작·끝 가치가 같은 씬은 '비사건'으로 플래그하고 삭제/병합을 검토한다. 전환 방식(action|revelation)을 씬 요약에 명시한다.
- **ASL·리듬**: 목표 평균 숏 길이는 format_profile이 정한다(format-director 표). 숏 길이를 균일하게 두지 말고 긴장 구간은 짧게 군집, 이완 구간은 길게(1/f 리듬 — Cutting).
- **포맷 우선**: 위 영화 문법이 format-director의 포맷 규칙(예: 숏폼 훅 우선 — 설정 숏 생략)과 충돌하면 **포맷 규칙이 이긴다**.

## variation_type — 렌더 비용 라벨 (연출 라벨 아님)

숏 안의 **피사체 변화량**을 3단계로 라벨링한다(감정·연출 판단은 shot_size/function으로 — 비용 라벨에 연출 의미를 싣지 않는다). 이 라벨이 4단계에서 키프레임 장수와 비디오 모드를 결정한다:

| 라벨 | 기준 | 렌더 방식 |
|---|---|---|
| `small` | 표정·미세 자세 변화 | 첫 프레임 1장 → image-to-video |
| `medium` | 인물 등장/퇴장, 몸 돌리기 (동일 카메라 포지션) | 첫+끝 프레임 → FLF2V |
| `large` | 피사체 대변화 — **단 동일 카메라 포지션 내에서** | 첫+끝 프레임 → FLF2V |

**FLF 합법 조건(하드):** FF와 LF는 **같은 카메라 포지션**(shot_size·angle·lens_mm·dof 동일)이어야 한다. 와이드↔클로즈업, 팬포커스↔보케 페어는 모델이 의도치 않은 카메라 무브·포커스 애니메이션을 발명한다(워핑 실증 2건). **구도·포커스가 바뀌는 변화는 FLF가 아니라 ①두 숏으로 분할 또는 ②FF-only + 카메라 무브**로 표현한다.

**길이 산술(핸들):** `duration_sec`는 **타임라인 의도 길이**다. 생성 길이는 핸들 포함 — 후반이 헤드 ~0.5초(도입 색전환 트림)·테일 ~0.3초(말단 열화 트림)를 먹고 디졸브가 전환당 길이를 당긴다. 비트 검증은 타임라인 길이 합산으로 하고, produce에서 `gen_duration ≥ duration_sec + 0.8s`의 모델 합법 길이를 고른다(model_profile.legal_durations — 이산적: 예 4/6/8s). 숏 길이는 모델 클립 한도 이내로, 넘으면 분할.

## 숏 생성 전략 — generative / stock / hybrid (비용 절감)

숏마다 `generation_strategy`를 정한다. 모든 숏을 생성(generative)하지 말고, 히어로가 아닌 숏은 Magnific 스톡으로 대체해 비용·시간을 아낀다(비용 게이트 서사 강화):

| 전략 | 언제 | 방식 |
|---|---|---|
| **generative**(기본) | **히어로 숏** — 캐릭터 등장·감정 비트·제품/로고. 캐릭터 일관성 계약이 걸리는 숏 | 키프레임 생성 → I2V |
| **stock** | **캐릭터·브랜드 식별자가 없는** 설정 롱숏·추상 B롤·인서트(하늘·강물·도심 야경·질감 등) | `stock_search`→`stock_to_creation`으로 스톡 클립/사진을 소재로. **캐릭터가 있으면 금지.** |
| **hybrid** | 스톡 환경/플레이트 + 생성 전경(캐릭터) | 스톡을 배경/참조로 배선하고 전경만 생성 |

- 판단 기준: "이 숏이 **캐릭터 정체성이나 브랜드 특정 요소**를 나르는가?" → 예면 generative(또는 hybrid), 아니면 stock 후보.
- stock 숏은 `stock.query`(검색어)·`orientation`·`media`를 콘티에 적고, 확정 후 `stock.creation_identifier`를 기록한다.
- 전략과 근거(특히 비용 트레이드오프)를 decision_log에 남기고, 4단계 비용 견적은 stock 숏을 제외해 산정한다(스톡은 생성 과금이 없거나 낮음 — 실측).

## 절차

1. project_brief의 씬 개요를 씬별 숏 리스트로 전개한다 (위 규칙 적용). 숏마다 generation_strategy를 배정한다.
2. `storyboard.json` 초안 작성, 스키마 검증.
3. (선택, 사용자 동의 시) 씬당 대표 숏 1~2개의 first_frame을 저비용 이미지 모델로 러프 생성해 콘티 보드로 보여준다 — 스타일 방향 확인용. 비용 게이트 적용.
4. 사용자 승인 후 `approved_by_user: true`. 수정 요청 시 해당 숏만 고치고 하류 stale 전파를 확인한다.
