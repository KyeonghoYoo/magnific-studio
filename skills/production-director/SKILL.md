---
name: production-director
description: |
  영상 제작 스테이지 디렉터. Use when: (1) /ms-produce 실행, (2) 키프레임/클립 생성·합성·오디오 작업, (3) production_manifest.json을 만들거나 갱신할 때. spaces-engineer 스킬과 함께 사용한다. 산출물: production_manifest.json + 최종 영상.
---

# Production Director — 영상 제작

먼저 `magnific-studio-core`·`spaces-engineer`·`quality-reviewer` 스킬을 읽었는지 확인한다.
입력: 승인된 `project_brief.json` + `characters.json` + `storyboard.json` (stale 아닌 것).

## 절차

### Step 0 — 재개 확인

`production_manifest.json`이 있으면 읽고, 이미 완료된 항목(status: succeeded)은 건너뛴다. 파이프라인은 어느 지점에서든 재개 가능해야 한다.

### Step 1 — 모델 선정

`video_models_list`/`images_models_list`로 후보를 확인하고, 씬 스타일·클립 길이·키프레임 지원 여부(FF2V/FLF2V)·비용 기준으로 선정한다. 선정 근거와 기각 사유를 decision_log에 기록한다. project_brief에서 사용자가 모델을 지정했다면 그것을 따른다.

### Step 2 — Space 구축 (spaces-engineer 규약)

씬당 Space를 만들고 콘티의 숏 서브그래프를 구축한다. 편집-검증 루프 필수. 구축된 space/node id를 manifest에 기록한다.

### Step 3 — 키프레임 생성 + 품질 심사 루프

**숏 생성 전략 분기(먼저 확인).** 숏의 `generation_strategy`가 `stock`이면 키프레임을 생성하지 않고 `stock_search`→(`stock_show` 확인)→`stock_to_creation`으로 스톡 소재를 소싱해 클립 노드에 배선한다(캐릭터 없음 확인 — 있으면 콘티 결함). `hybrid`면 스톡을 배경/플레이트로 두고 전경(캐릭터)만 생성한다. `stock.creation_identifier`를 manifest에 기록하고, **비용 견적에서 stock 숏은 제외**한다. 아래 절차는 `generative`(및 hybrid의 생성 전경)에 적용된다:

1. **캐릭터 일관성 계약 강제(하드).** 숏의 `characters[]`가 비어있지 않고 `consistency_policy.enforce_citation=true`면, 각 캐릭터의 `reference_bank`에서 `reference_selection` 휴리스틱으로 참조를 골라 키프레임 노드에 **반드시 배선**한다(최소 `min_citations`개, `primary_ref` 포함). 인용 없이는 생성하지 않는다 — 텍스트 프롬프트만으로 정체성을 지어내면 드리프트한다. 배선한 참조 id는 manifest의 해당 숏 `references_used`에 기록한다.
2. **variation 2~3장 생성** 후 `quality-reviewer`로 자동 심사해 최선을 채택하고, 결과를 manifest 숏 `review.keyframe`(축·verdict·cause_layer·issues)에 기록한다(`consistency_check`는 character_consistency 축 요약):
   - **character_consistency** — 이목구비·체형·헤어가 characters.json 시트 및 reference_bank와 일치
   - **spatial_continuity** — 인물 배치(좌/우), 배경 구도가 인접 숏과 모순 없음
   - **prompt_adherence** — first_frame_desc의 내용이 실제로 구현됨 (+ brand_fit·technical)
   character_consistency가 fail이면 `drift_action`(앵커+Library 참조 강화 재생성)을 적용한다. 채택 후보는 승인 게이트에서 review 요약과 함께 제시한다.
3. 채택 프레임의 creation identifier를 manifest에 기록. 탈락 사유는 decision_log에.
4. 같은 camera.position_id의 첫 채택 프레임은 그 포지션의 **앵커 프레임**으로 지정 — manifest `spaces[].anchor_frames`와 **해당 캐릭터 `reference_bank.anchor_frames`에 누적**하고, 이후 같은 포지션 숏의 참조 풀에 항상 포함한다(뱅크가 프로덕션과 함께 성장).
5. **키프레임에 없는 주체를 비디오 모델이 만들게 하지 마라.** 첫 프레임이 빈 장면이면 등장 인물·차량의 정체성을 텍스트만으로 지어내 캐릭터 일관성이 깨진다(실증: 빈 주차장 진입 클립에서 헬멧·인물·복장·바이크 전부 붕괴). "프레임 밖에서 진입" 연출이 필요하면 주체가 **가장자리를 막 통과하는 순간**을 첫 프레임으로 잡아 픽셀 정체성을 프레임 안에 심는다.
6. **FLF(첫+끝 프레임) 페어는 카메라 일치 검증 후에만 사용한다.** LF를 채택하기 전에 FF와 나란히 놓고 카메라 위치·프레이밍·배경 요소가 일치하는지 육안 대조한다. 이미지 모델은 "same camera position as the reference"류 지시를 안정적으로 지키지 못하므로(실증: 배경 워핑 클립 2건), 불일치하면 LF 재생성을 반복하지 말고 **FF-only + 잠금 카메라 모션 프롬프트("locked framing, only the subject moves")로 강등**하는 편이 결과가 좋다. 액션 과적도 워핑을 유발한다 — 클립 길이당 동작 1~2개로 제한하고 필요하면 duration을 늘린다.

### Step 4 — 비용 게이트 (하드)

전체 클립 생성 전에 `simulate_spaces`(또는 `simulate_cost`)로 총 견적을 산출하고, `budget_cap_credits`와 비교해 사용자 승인을 받는다. 초과 시 실행하지 않고 옵션(숏 수 축소, 저비용 모델, 해상도 하향)을 제시한다.

### Step 5 — 클립 생성

variation_type에 따라:

- `small` → first_frame 1장을 키프레임으로 image-to-video
- `medium`/`large` → first+last 프레임을 키프레임으로 first+last-frame video

motion_desc를 비디오 프롬프트로 사용한다 (캐릭터는 외형 특징으로 지칭되어 있어야 함 — 아니면 storyboard 결함이므로 수정 후 진행). `spaces_run`(downstream)으로 실행하고 폴링, 결과를 manifest에 기록. 실패 숏은 singular 재실행.

### Step 5.5 — 클립 검수 (비평-수정 루프)

클립 심사는 `quality-reviewer`로 자동 자기검수한다(재생 없이): `creations_get`이 반환하는 **preview-grid**(50여 프레임 시트)와 start/end frame으로 프레임 단위 판정. 축: ① 모션 자연스러움(워핑·텔레포트·배경 유동=technical), ② 캐릭터/차량 정체성 유지(character_consistency), ③ 카메라 지시 준수(prompt_adherence), ④ 시작/끝 프레임이 키프레임과 일치. 결과를 manifest의 숏 `review.clip`(축·verdict·cause_layer·issues)에 기록하고, **승인 게이트에서 요약을 제시**한다(증거 기반 승인). FilmAgent의 비평-수정 패턴처럼 **revise/fail 클립은 원인 층위를 분류**(keyframe/prompt/model/edit)해 해당 층에서 고친다 — 키프레임 결함을 프롬프트·모델 승급으로 때우면 반복 실패한다. 원인과 조치는 decision_log에.

재생성으로 고칠 수 없는 **생성 클립 고유 특성**(첫 0.3~0.5초 색감 전환, 엔드카드 로고가 클립 끝에서 정착, 클립에 베이크된 텍스트)은 결함이 아니라 후반에서 트림·홀드로 처리할 사항이다 — 검수 시 이런 클립은 표시해 post-production-director로 넘긴다(후반 Step 3b).

### Step 6 — 오디오 (콘티에 대사/음악이 있을 때)

- 대사: `audio_voices_list`로 캐릭터별 보이스 선정(decision_log 기록) → `audio_tts`. 립싱크 지원 모델이면 `video_speak` 우선.
- 배경음악: `audio_music_generate` (분위기·길이 지정).

### Step 7 — 합성과 시사

1. 숏 클립을 씬 순서대로 `video_concatenate` (크레딧 0 실측, 1회 10클립 한도 — 초과 시 파트 분할 후 파트끼리 재합성).
2. 결과를 `creations_show`로 사용자에게 **시사**시키고 피드백을 받는다 — Full Cut을 봐야만 보이는 결함(전환 어색함, 리듬)이 반드시 나온다. 수정 숏만 재생성 → 해당 파트만 재합성하는 vN 루프를 돌린다.
3. manifest의 모든 항목이 터미널 상태인지 확인 후 `stage_status: "approved"` 처리. 최종 영상 webUrl과 함께 완료 보고.
4. 트리밍·트랜지션·음악·자막·업스케일·파생본은 다음 스테이지(/ms-post, post-production-director)로 — 합성 단계에서 해결하려 하지 않는다.

## UI 화면 정합 (앱/웹 화면이 등장하는 숏)

생성 모델은 UI를 "다시 그리기" 때문에 실제 화면과 픽셀 일치가 불가능하다. 폰/모니터 화면이 식별 가능하게 등장하는 키프레임은 **실제 스크린샷을 원근 워핑으로 합성**한다: 첫 프레임에서 화면 쿼드 4점을 추정 → 스크린샷을 perspective transform으로 워핑 → 라운드 코너 마스크로 합성 → 업로드해 키프레임으로 배선. 첫 프레임 위에 직접 합성하면 FLF 페어의 카메라 일치가 자동 보장된다(실증: 지하철 폰 화면 전환 숏).

## 실패·드리프트 대응

- 캐릭터 드리프트 발견 시: 해당 숏 키프레임을 앵커 프레임 + Library 참조를 강화한 프롬프트로 재생성. 반복 실패 시 characters.json의 특징 기술을 보강한다.
- 클립이 motion_desc와 다르게 나오면: 프롬프트를 "카메라 지시 먼저, 인물 동작 다음" 순으로 재구성해 1회 재시도, 그래도 실패면 사용자에게 보고.
