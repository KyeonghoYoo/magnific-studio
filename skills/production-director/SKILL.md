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

**model_profile(capability 플래그)을 manifest에 기록한다** — 모델명이 아니라 능력치로: `{negative_prompt, max_moves_per_shot, named_tag_syntax, flf_support, camera_param_object, legal_durations[], text_render_ok, native_audio}`. 현재 값은 `video_models_list`/`video_models_show` + `filmcraft/references/model-matrix.md`(**날짜 있는 부록 — 캠페인마다 재검증**)로 채운다. 규칙은 플래그만 참조한다(예: "1무브 법칙은 항상 저작, `max_moves_per_shot≥2`면 produce에서 인접 동일 포지션 숏 병합 가능").

**프롬프트는 아티팩트에서 렌더한다(프로젝션).** `filmcraft/references/prompting.md`의 결정적 테이블을 따른다: **키프레임(T2I)은 피사체 선행**([이미지 타입/숏 사이즈]→[피사체+식별자 핸들]→[정적 포즈]→[환경]→[구도]→[씬 조명 문장 byte-identical]→[렌즈/광학]→[스톡/스타일]), **클립(I2V)은 카메라 선행**([무브+속도]→[외형 문구]→[액션 1개]→[환경 큐]→[settle 절]). 식별자 핸들: 참조 배선+태그 지원 모델 → 모델 네이티브 태그, 아니면 외형 문구+참조. 리라이트 발생 시 **원문과 리라이트본을 모두 로그**(디버깅 가능성). 생성 전 **pre-flight lint**(빈 토큰·부정 구문·hex/비율 숫자·foreground_anchor 부재·조명 문장 불일치) — 0크레딧에 잡는다.

### Step 2 — Space 구축 (spaces-engineer 규약)

씬당 Space를 만들고 콘티의 숏 서브그래프를 구축한다. 편집-검증 루프 필수. 구축된 space/node id를 manifest에 기록한다.

### Step 3 — 키프레임 생성 + 품질 심사 루프

**숏 생성 전략 분기(먼저 확인).** 숏의 `generation_strategy`가 `stock`이면 키프레임을 생성하지 않고 `stock_search`→(`stock_show` 확인)→`stock_to_creation`으로 스톡 소재를 소싱해 클립 노드에 배선한다(캐릭터 없음 확인 — 있으면 콘티 결함). `hybrid`면 스톡을 배경/플레이트로 두고 전경(캐릭터)만 생성한다. `stock.creation_identifier`를 manifest에 기록하고, **비용 견적에서 stock 숏은 제외**한다. 아래 절차는 `generative`(및 hybrid의 생성 전경)에 적용된다:

1. **캐릭터 일관성 계약 강제(하드) + 참조 배선 우선순위.** 숏의 `characters[]`가 비어있지 않고 `consistency_policy.enforce_citation=true`면, 각 캐릭터의 `reference_bank`에서 참조를 골라 키프레임 노드에 **반드시 배선**한다(최소 `min_citations`개, `primary_ref` 포함). 배선 우선순위(core 자산 계층): **① Library 자산(character/product/locations/style — 정체성·환경) ② 키프레임 앵커(구도 연속성 — Library에 없는 정보) ③ raw creation(일회성만)**. `primary_ref`가 Library 자산이면 반드시 Library id로 배선한다 — front 시트 creation만 와이어하면 3뷰가 정체성 계산에 미기여한다(파일럿 1 실증). Library에 든 이미지의 creation 병행 배선 금지(이중 가중). 인용 없이는 생성하지 않는다. 배선한 참조 id는 manifest의 해당 숏 `references_used`에 기록한다.
1-0. **동일 포지션 연속 컷은 단일 클립으로 생성한다(하드).** 같은 position_id의 인접 숏들(예: POV 접근 컷 + POV 스침 컷)을 각각 FLF 클립으로 만들면 **클립 경계 = 컷 지점에서 카메라 리그 불일치가 반드시 노출**된다(실증: 파일럿 1 — 중간 키프레임 리그 이탈로 컷 점프). 대신 **구간 전체를 하나의 클립**(모델 합법 길이 내, Seedance 4–15s)으로 생성하고 — FLF는 구간의 첫/끝 프레임, 중간 비트는 프롬프트의 구간 서술("First half: … Second half: …") — **콘티의 컷은 후반에서 그 클립을 트림해 재현**한다. 클립 내부는 카메라가 물리적으로 연속이라 튈 수 없다. 구간이 모델 한도를 넘을 때만 분할하고, 분할 경계는 리그 대조 검수를 통과해야 한다. (멀티숏 기능 지원 모델이면 multishot이 대안 — Step 3.5)
1-1. **환경 플레이트 먼저(씬 단위).** 한 장소에 2개 이상 숏이 있는 씬은 캐릭터 키프레임보다 먼저 **환경 마스터**를 확정한다: 씬 첫 키프레임(또는 빈 환경 플레이트)을 생성·심사·채택 → `library_create(type: locations)` → 씬 나머지 키프레임 전부에 참조 배선 + 프롬프트에 "the same [환경] as the reference location". 조명 문장·팔레트만으로는 형태(도로·차선·수종·지형·계절)가 잠기지 않는다(파일럿 1 실증 — storyboard-director 환경 플레이트 독트린).
2. **N-후보는 차등 배분한다(실전 표준).** 기본은 **단발 생성 → quality-reviewer 심사 → 원인 층위 분류 재시도**. variation 2~3장 비교 선택은 **히어로 숏에만** 쓴다(캐릭터 기준 이미지, 감정 클라이맥스, 엔드카드 — AniMaker의 중요도 차등 탐색, 상업 사례 채택률 ~4%의 교훈은 '선별'이지 '전 숏 N배 생성'이 아니다). 같은 씬의 키프레임들은 **같은 참조 세트로 연속 생성**해 배치 일관성을 얻는다(StoryDiffusion 원리의 운영 모사). 심사 결과는 manifest 숏 `review.keyframe`(축·verdict·cause_layer·issues)에 기록한다(`consistency_check`는 character_consistency 축 요약):
   - **character_consistency** — 이목구비·체형·헤어가 characters.json 시트 및 reference_bank와 일치
   - **spatial_continuity** — 인물 배치(좌/우), 배경 구도가 인접 숏과 모순 없음
   - **prompt_adherence** — first_frame_desc의 내용이 실제로 구현됨 (+ brand_fit·technical)
   character_consistency가 fail이면 `drift_action`(앵커+Library 참조 강화 재생성)을 적용한다. 채택 후보는 승인 게이트에서 review 요약과 함께 제시한다.
3. 채택 프레임의 creation identifier를 manifest에 기록. 탈락 사유는 decision_log에.
4. **포지션 락(앵커 파생) — 같은 position_id는 독립 T2I 금지(하드).** 같은 camera.position_id의 첫 채택 프레임을 그 포지션의 **앵커 프레임**으로 지정하고(manifest `spaces[].anchor_frames` + 캐릭터 `reference_bank.anchor_frames`에 누적), **이후 같은 포지션의 모든 키프레임은 앵커를 참조로 강배선 + 프롬프트 서두에 "Keep the EXACT same camera position, framing, [전경 리그 요소 열거] as the reference frame — only the described change differs:" 지시로 편집 파생**한다. 각 키프레임을 독립 T2I로 만들면 같은 포지션인데 핸들바 높이·계기판·미러 위치가 매번 미세 발산해 컷이 뚝뚝 튄다(실증: 파일럿 1 POV 4키프레임). 항상 승인 원본에서 파생하므로 conform_from_source와 정합 — 클립 끝프레임 체이닝과 혼동 금지.
5. **키프레임에 없는 주체를 비디오 모델이 만들게 하지 마라.** 첫 프레임이 빈 장면이면 등장 인물·차량의 정체성을 텍스트만으로 지어내 캐릭터 일관성이 깨진다(실증: 빈 주차장 진입 클립에서 헬멧·인물·복장·바이크 전부 붕괴). "프레임 밖에서 진입" 연출이 필요하면 주체가 **가장자리를 막 통과하는 순간**을 첫 프레임으로 잡아 픽셀 정체성을 프레임 안에 심는다.
6. **FLF(첫+끝 프레임) 페어의 합법 조건 = 동일 카메라 포지션(하드).** FF와 LF는 shot_size·angle·lens_mm·dof가 같아야 한다(스키마 v2 variation_type 정의와 일치). 채택 전 나란히 놓고 육안 대조 — 와이드↔클로즈업 쌍은 의도치 않은 카메라 무브를, 보케↔팬포커스 쌍은 원치 않는 포커스 애니메이션을 모델이 발명한다(실증 워핑 2건). 불일치하면 LF 재생성을 반복하지 말고 **FF-only + 잠금 카메라 모션 프롬프트("locked framing, only the subject moves")로 강등**한다. 액션 과적도 워핑 유발 — 클립당 동작 1~2개(gesture economy). **렌더 후 flf_adherence 기계 검사**: 클립 마지막 프레임을 공급한 LF와 SSIM/pHash 대조 — 임계 미달이면 서빙 경로가 LF를 무시한 것(실재하는 장애 유형)이므로 review 축 `flf_adherence`에 기록하고 경로/모델을 재검토한다.
7. **conform_from_source — 원본에서 컨폼한다(체이닝 금지).** 클립 끝 프레임을 다음 클립의 **소스 키프레임**으로 잇는 체이닝은 세대마다 드리프트한다(dub-of-a-dub). 연속 씬은 항상 **원본 키프레임/앵커 프레임에서 재출발**. 예외는 정확히 1세대 — 업스케일+색 정규화 후, decision_log 기록, 재체이닝 금지. 단, 끝 프레임을 **비권위 참조 인용**(reference_used에 추가 배선)으로 쓰는 것은 허용 — 권위는 항상 원본 앵커에 있다. 벤더 3사 공통 독트린("항상 원본 참조 팩에 재고정")과 일치.

### Step 3.5 — 멀티숏 단일 실행·프롬프트 컨센서스 (커뮤니티/벤더 비공식 — 라벨 유지)

- **멀티숏 단일 실행**: Seedance 계열은 한 생성 실행에 복수 숏(각기 앵글·길이·프롬프트)을 정의할 수 있고(multishot ≤6), 조명·캐릭터·환경이 숏 간 일관 유지된 공식 사례 존재(Freepik Studios 5연속 숏). 같은 씬의 짧은 연속 숏은 개별 클립 N회보다 멀티숏 1회를 먼저 검토 — 비용·일관성 동시 이득. [공식 블로그 사례 — 원문 재확인 필요]
- **FLF 프롬프트 작법** [커뮤니티 컨센서스]: 시작/끝 이미지가 이미 보여주는 것을 재서술하지 말고 **모션·카메라·무드만** 기술. 첫 20~30단어에 주체+핵심 액션(모델이 이 구간으로 lock). 모션은 단일하고 매끄럽게. FLF는 "엔딩이 포인트"(리빌·변신·루프)일 때 최적.
- **POV 유지 6요소** [커뮤니티 컨센서스, 다수 수렴]: ①카메라 정체성 명명(헬멧캠/체스트마운트/대시캠) ②프레임 내 신체 앵커(손·발) ③감각적 로케이션 디테일 ④비트 단위 액션 ⑤명명된 광원·팔레트 앵커 ⑥카메라 홀드 절("the camera holds its line"). 실패 모드: 신체 앵커 부재 = 무중력감, 모델 confidence 저하 = 3인칭 드리프트.
- ⚠️ 채택 금지: 3rd party의 수치 가중치 시스템(character weight 0.9류)은 공식 API 파라미터로 미확인 — 개념(락 문구+변경 범위 명시)만 쓰고 수치는 문서화하지 않는다.
- 재조사 대기: BytePlus ModelArk 공식 프롬프트 가이드 3건(Seedream 4.x·Seedance 2.0/1.0) — SPA라 미추출, 확보 시 이 절을 공식 근거로 승격.

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
