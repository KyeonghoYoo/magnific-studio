---
name: storyboard-director
description: |
  콘티(스토리보드) 스테이지 디렉터. Use when: (1) /ms-storyboard 실행, (2) 숏 리스트/카메라 설계/콘티 작업, (3) storyboard.json을 만들거나 수정할 때. 산출물: storyboard.json.
---

# Storyboard Director — 콘티

먼저 `magnific-studio-core` 스킬을 읽었는지 확인한다. 입력: 승인된 `project_brief.json` + `characters.json`.

## 숏 구조 (schemas/storyboard.schema.json)

숏마다 카메라를 **구조화된 필드**로 기술한다 — 자유 텍스트에 묻지 않는다:

- `camera.shot_size`: extreme_wide | wide | full | medium | medium_close_up | close_up | extreme_close_up
- `camera.angle`: eye_level | high | low | overhead | dutch
- `camera.movement`: static | pan_left | pan_right | tilt_up | tilt_down | dolly_in | dolly_out | slow_push_in | pull_back | handheld | orbit | crane
- `camera.lens`: 예 "24mm", "50mm", "85mm"
- `camera.position_id`: 같은 물리적 카메라 포지션을 공유하는 숏들의 그룹 키

그리고 렌더 경계를 만드는 3분해:

- `first_frame_desc` — 첫 프레임의 **정적 스냅샷**
- `last_frame_desc` — 마지막 프레임의 정적 스냅샷 (variation_type이 small이면 null)
- `motion_desc` — 그 사이의 카메라 무브먼트 + 인물 동작

## 작법 하드 룰

1. **정적 스냅샷 규칙**: 프레임 묘사에 진행형·예정 동작 금지. "그가 일어서려 한다" ❌ → "그가 의자에 앉아 상체를 약간 앞으로 기울이고 있다" ✅
2. **motion_desc에서 캐릭터는 이름이 아닌 외형 특징으로 지칭**한다 — 비디오 모델은 이름을 모른다. "Alice가 걷는다" ❌ → "짧은 머리에 초록 원피스를 입은 여성이 걷는다" ✅ (외형은 characters.json의 static/dynamic features에서 가져온다)
3. **첫 숏은 씬 환경을 확립하는 최대한 넓은 숏**으로 시작한다.
4. **카메라 포지션 재사용 우선**: 새 숏을 설계할 때 기존 position_id로 찍을 수 있는지 먼저 검토하고, 사이즈·앵글·포커스가 크게 다를 때만 새 포지션을 만든다. 큰 무브먼트를 겪은 포지션은 이후 재사용하지 않는다.
5. **단계적 숏 사이즈 전환**: wide → medium → close-up 순의 이웃 전환만. long shot에서 close-up으로 직접 점프 금지.
5-1. **감정 비트는 medium 이상으로 당겨 찍는다.** 표정이 서사를 나르는 숏(반전·설렘·해소)을 고정 카메라 풀샷 원테이크로 잡으면 증명사진처럼 죽는다(실증). 인물이 프레임을 크게 채울수록 비디오 모델의 모션 품질과 감정 전달이 모두 좋아진다. 잠금 프레이밍으로 워핑을 막을 때는 slow_push_in 같은 최소 무브먼트를 남겨 생동감을 보존한다.
6. **대사는 dialogue 배열에 구조화** (speaker, emotion, line). 효과음·환경음은 sound 배열에.
6-0. **비율 파생은 크롭이 아니라 재구도다.** 9:16 세로 파생 시 가로 구도를 그대로 옮기지 말 것 — 측면 병주 투샷은 좁은 세로 프레임에서 반복적으로 마주보는 구도로 붕괴한다(실증 2회). 세로 대체 문법: 병주 투샷 → 후방 추적(뒤에서 나란히 멀어지는), 로우앵글 와이드 → 강변 측면 수평띠 구도(하단 피사체/중단 수면/상단 스카이라인). 랜드마크는 실물 구조 특징(잠수교=낮고 평평한 거더교, 타워·케이블 없음)을 명시해 재해석 왜곡을 막는다. 공유 모션 프롬프트가 새 구도와 어긋나면 비율 전용 모션 텍스트로 분리한다.
6-1. **복수 이동체(차량·바이크·인물 다수)가 함께 이동하는 숏은 공유 진행 방향을 화면 기준으로 명시**한다 ("both traveling left to right, seen in side profile, parallel, never facing each other, never oncoming"). 이미지 모델은 "side by side" + "smiling at each other"류 표현을 마주보고 교차하는 구도로 해석하는 경향이 있다(실증: 투샷 2컷 연속 교차 생성). 씬 내 스크린 디렉션(180도 규칙)도 이때 함께 고정한다.
7. 민감 요소는 대체물 치환 (피 → 케첩 등).
8. **씬 전환마다 연결 비트를 검사한다.** 장소가 바뀌는 컷은 이동/도착/원인 중 하나로 이어야 한다 — "채비 → (컷) → 이미 도착해 있음"처럼 비트가 빠지면 점프로 느껴진다(실증). 전환 브리지 패턴: (a) 도착 컷 — 주체가 프레임 밖에서 새 장소로 진입, (b) 매치컷 — 앞 숏이 시선/동작으로 끝나고 뒷 숏 첫 프레임에 그 대상(접근하는 헤드라이트 등)이 존재, (c) 인서트 경유. 등장 대기 컷(빈 장소에 주체의 소유물이 먼저 있는 구도)은 연속성 모순을 만들기 쉬우니 피한다.

## variation_type — 렌더 비용을 결정하는 라벨

숏 안에서 화면 변화량을 3단계로 라벨링한다. 이 라벨이 4단계(/ms-produce)에서 키프레임 장수와 비디오 모드를 결정한다:

| 라벨 | 기준 | 렌더 방식 |
|---|---|---|
| `small` | 표정·미세 자세 변화 수준 | 첫 프레임 1장 → image-to-video |
| `medium` | 인물 등장/퇴장, 몸 돌리기 | 첫+끝 프레임 2장 → first+last-frame video |
| `large` | 구도·포커스 대변화 (와이드→클로즈업 등) | 첫+끝 프레임 2장 → first+last-frame video |

숏 길이는 대상 비디오 모델의 클립 한도(보통 5~10초) 이내로. 넘으면 숏을 분할한다.

## 절차

1. project_brief의 씬 개요를 씬별 숏 리스트로 전개한다 (위 규칙 적용).
2. `storyboard.json` 초안 작성, 스키마 검증.
3. (선택, 사용자 동의 시) 씬당 대표 숏 1~2개의 first_frame을 저비용 이미지 모델로 러프 생성해 콘티 보드로 보여준다 — 스타일 방향 확인용. 비용 게이트 적용.
4. 사용자 승인 후 `approved_by_user: true`. 수정 요청 시 해당 숏만 고치고 하류 stale 전파를 확인한다.
