# Magnific Studio — 설계 문서

> Magnific(구 Freepik) MCP의 Spaces를 실행 레이어로 쓰는 Claude Code 플러그인 하네스.
> 파이프라인: **기획 → 캐릭터 생성 → 콘티(스토리보드) → 영상 제작 → 후반 편집**

## 1. 설계 원천

| 출처 | 차용한 것 | 개선한 것 |
|---|---|---|
| **ViMax** (MIT) | Plan/Render 2단계 분리 + 리뷰 게이트, 캐릭터 static/dynamic 특징 분리, 멀티뷰(정면/측면/후면) 캐릭터 레지스트리, 참조 이미지 선택 휴리스틱("최근 프레임 우선, 같은 카메라 우선, 최대 8장"), variation_type(large/medium/small)으로 키프레임 수·비디오 모드 분기, "정적 스냅샷" 프레임 규칙, 파일시스템 = 진리의 원천 | 촬영 용어를 자유 텍스트가 아닌 **구조화된 enum 필드**로(shot_size/angle/movement/lens), 오케스트레이션을 코드 하드코딩이 아닌 **선언적 스테이지 계약**으로, 미배선 상태였던 N-variation + 심사 루프를 실제 배선 |
| **OpenMontage** (AGPLv3 — 아이디어만 차용, 코드 복사 금지) | 단계당 정본 아티팩트 1개 = 계약(JSON 스키마 검증), 승인 게이트 하드 강제, Decision Log(append-only, 거부 옵션 포함), "디스크가 진실, 보드는 관찰자", 얇은 진입점 → 단일 가이드 라우팅, 도구 호출 전 관련 스킬 필독 규칙 | 스킬 트리 단일화(이중 유지 금지), Claude Code 플러그인 표준 패키징(.claude-plugin), 파이프라인 1개를 프로덕션 품질로 좁게 |
| **Magnific MCP** | `video_plan`(기획), `library_create/edit`(캐릭터 자산), `spaces_create/edit/run`(워크플로), `simulate_spaces`(사전 비용 견적), `video_generate`+keyframes(숏 렌더), `video_concatenate`(합성) | — |
| **FilmAgent** (HITsz) | 다역할 비평-수정-검증(Critique-Correct-Verify) 루프 — 중간 산출물을 역할 관점으로 심사해 환각 감소 | 상시 멀티에이전트 대신 **스테이지별 경량 심사 루프**(3~4축 체크리스트 + 원인 층위 분류)로 비용 절감 |
| **MovieAgent** (showlab) | 계층적 CoT 기획(스크립트→씬→숏) + 캐릭터 뱅크 | 이미 스키마 계약으로 구조화되어 있어 검증 순서만 차용 |
| **MoneyPrinterTurbo / ShortGPT** | ffmpeg/MoviePy 후반 자동화(트림·자막·BGM·9:16), "초안 공장 + 인간 큐레이션" 운영관, ShortGPT의 **편집 마크업(edit-as-data)** — LLM이 선언적 EDL을 내면 결정적 렌더러가 실행 | 후반을 정식 5번째 스테이지(/ms-post)로 편입, 생성 클립 기반(스톡 아님), EDL을 정본 아티팩트 `edit_plan.json`으로 승격 |

### v0.3.0 후반 편집 추가 원천 (아이디어 차용, 코드 미복사)

| 출처 | 라이선스 | 차용한 것 | 우리 적용 |
|---|---|---|---|
| **OpenMontage** | AGPLv3 (코드 미복사) | 렌더-후 **ffprobe 자기검수 QC**(블랙프레임/무음/자막 누락 탐지 후 납품 거부), 프로바이더 스코어링 | QC를 /ms-post의 하드 게이트로 재구현 |
| **Remotion** | 커스텀(4인+ 유료 — 코드 미사용) | `Caption` 스키마 `{word,start_ms,end_ms}` + TikTok 카라오케 페이징 개념 | 스키마만 차용해 libass `\k` ASS 렌더로 구현(라이선스 회피) |
| **WhisperX / faster-whisper** | BSD-2 / MIT | 워드 단위 강제정렬(sub-100ms) | 카라오케 자막 워드 타이밍 소스(선택) |
| **librosa** | ISC | `beat_track`/`onset`/`rms` 음악 구조 분석 | 컷-비트 스냅 + RMS 빌드→서사 전환점 정렬 |
| **MoviePy** | MIT | 불변 `.with_*` 합성 레이어(v2 API) | ffmpeg 대안 실행기(오버레이 템플릿) |
| **pyautoflip / auto-vertical-reframe** | (repo 확인) | 콘텐츠 인식 세로 리프레임(AutoFlip 2023 단종 대체) | 재구도 사다리의 최후 폴백(auto_reframe) |

## 2. 아키텍처 개요

```
사용자
  │  /ms-plan → /ms-characters → /ms-storyboard → /ms-produce   (또는 /ms-pipeline 일괄)
  ▼
Claude Code (하네스 = 이 플러그인)
  ├─ commands/   슬래시 커맨드 = 단계 진입점 (얇은 라우터)
  ├─ skills/     디렉터 스킬 = 각 단계의 "어떻게" (프롬프트 기법 포함)
  ├─ schemas/    정본 아티팩트 JSON 스키마 = 단계 간 계약
  └─ .studio/<project>/   파일시스템 = 진리의 원천 (아티팩트, decision_log, 매니페스트)
  ▼
Magnific MCP (실행 레이어)
  ├─ Library: 캐릭터/스타일 자산 (재사용)
  ├─ Spaces: 씬 단위 노드 그래프 (spaces_edit 자연어 쿼리로 구축, spaces_run으로 실행)
  └─ video_generate / video_concatenate: 숏 클립 → 최종 영상
```

**핵심 통찰 — Spaces는 코드가 아니라 자연어로 조작한다.** `spaces_edit`는 노드 JSON을 직접 쓰는 API가 아니라 자연어 편집 쿼리를 받는 헤드리스 API다. 따라서 하네스의 실질 업무는 "구조화된 콘티(JSON) → 정확한 Space 편집 쿼리 시퀀스로 번역"이며, 이를 `spaces-engineer` 스킬이 전담한다.

## 3. 파이프라인 스테이지 계약

각 스테이지는 **정확히 하나의 정본 아티팩트**를 산출하고, 다음 스테이지는 그것만 신뢰한다.
비용이 드는 실행(렌더) 전에는 반드시 `simulate_spaces`/`simulate_cost` 견적 + 사용자 승인 게이트를 거친다.

| 스테이지 | 커맨드 | 입력 | 정본 아티팩트 | 승인 게이트 |
|---|---|---|---|---|
| 1. 기획 | `/ms-plan` | 아이디어(자유 텍스트) | `project_brief.json` | ✅ (컨셉 확정) |
| 2. 캐릭터 | `/ms-characters` | project_brief | `characters.json` + Magnific Library 자산 | ✅ (외모 확정, 생성 비용) |
| 3. 콘티 | `/ms-storyboard` | brief + characters | `storyboard.json` | ✅ (콘티 확정) |
| 4. 영상 | `/ms-produce` | storyboard + characters | `production_manifest.json` + 최종 영상 | ✅ (렌더 비용 견적 후) |

### 프로젝트 워크스페이스 규약

```
.studio/<project-slug>/
├── project_brief.json        # 1단계 정본
├── characters.json           # 2단계 정본 (reference_bank + consistency_policy 포함)
├── storyboard.json           # 3단계 정본
├── production_manifest.json  # 4단계 정본 (space/run/creation id, 클립 상태)
├── decision_log.jsonl        # append-only 의사결정 기록
└── renders/                  # 다운로드한 산출물 (선택)
```

- 모든 아티팩트에는 `stage_status`(draft|awaiting_approval|approved)와 `approved_by_user`(bool)가 있다. **`approved_by_user=true` 없이 다음 스테이지 진입 금지** (게이트 위반).
- 하네스는 **도구 결과나 파일 상태가 증명하지 않는 작업 완료를 주장하지 않는다** (ViMax agent.md 계약).
- 수정 시 하류 아티팩트에 `stale: true` 마킹 후 사용자에게 재실행 범위 안내 (stale 전파).

## 4. 스테이지별 설계

### 4.1 기획 (`/ms-plan` → planning-director 스킬)

1. 사용자 아이디어를 받아 **`video_plan` 툴을 먼저 호출** (Magnific 공식 기획 도구 — 모델 추천, 캐릭터 준비 목록, 15초 초과 시 멀티클립 분할까지 반환).
2. 그 결과에 하네스의 기획 문답(타깃 길이, 화면비, 스타일, 톤, 예산 상한)을 결합해 **컨셉 2~3안** 제시.
3. 선택된 컨셉을 `project_brief.json`으로 확정. logline / synopsis / style(시각 스타일 + 금지 요소) / duration / aspect_ratio / scenes[] (씬 개요) / budget_cap_credits.
4. Decision Log에 채택/기각 컨셉 기록.

### 4.2 캐릭터 생성 (`/ms-characters` → character-director 스킬)

- 캐릭터마다 **static_features**(변하지 않는 외모: 얼굴, 체형, 헤어)와 **dynamic_features**(의상, 소품)를 분리 기술 (ViMax 패턴).
- 생성 절차: 정면 기준 이미지 T2I 생성(흰 배경, 정규 포즈 강제) → 사용자 승인 → 정면 이미지를 참조로 측면/후면 편집 생성 → **`library_create`로 Magnific Library 캐릭터 자산 등록**.
- Library 등록이 핵심 개선점: ViMax는 로컬 파일 레지스트리였지만, Magnific Library는 이후 `images_generate`/`video_generate`의 reference로 **네이티브 참조** 가능하고 팀 공유도 된다.
- **캐릭터 일관성 계약(v0.4.0, 벤치마크 로드맵 1 반영).** 3뷰+Library를 캐릭터별 **`reference_bank`**(primary_ref·citation_ids·locked_seed·anchor_frames·style_refs)로 묶고, 전역 **`consistency_policy`**(`enforce_citation`·`min_citations`·`reference_selection`·`drift_action`)를 둔다. `enforce_citation=true`면 **캐릭터가 등장하는 모든 키프레임 생성은 뱅크 id를 인용(배선)해야 하며 텍스트만으로 정체성을 지어내는 생성은 금지**된다. production-director는 인용 id를 manifest `references_used`에, 3축 심사를 `consistency_check`에 기록하고, 포지션별 앵커 프레임은 뱅크에 누적된다. MovieAgent의 캐릭터 뱅크·VideoClaw의 캐릭터 JSON을 참고하되, 여기서는 **타입드 계약 + 하류 강제 + 프로버넌스**로 승격했다 — 필드에서 일관성이 "희망"인 것과 달리 계약으로 보장한다.
- `characters.json`에 각 캐릭터의 library identifier + 3뷰 creation identifier + reference_bank + 특징 기술 + 전역 consistency_policy를 기록.

### 4.3 콘티 (`/ms-storyboard` → storyboard-director 스킬)

ViMax에서 검증된 프롬프트 기법을 스킬에 내장하되, 촬영 용어는 구조화:

```jsonc
// storyboard.json 의 shot 하나
{
  "shot_id": "s01_sh03",
  "scene_id": "s01",
  "camera": {                     // ★ ViMax 개선점: enum으로 구조화
    "shot_size": "medium_close_up",   // extreme_wide|wide|full|medium|medium_close_up|close_up|extreme_close_up
    "angle": "eye_level",             // eye_level|high|low|overhead|dutch
    "movement": "slow_push_in",       // static|pan_*|tilt_*|dolly_*|slow_push_in|pull_back|handheld|orbit
    "lens": "50mm"
  },
  "variation_type": "small",      // small=첫프레임만+FF2V / medium·large=첫+끝프레임+FLF2V
  "characters": ["alice"],        // characters.json 키 참조
  "first_frame_desc": "...",      // 정적 스냅샷 규칙: 진행형 동작 금지
  "last_frame_desc": null,        // small이면 생략
  "motion_desc": "...",           // 캐릭터는 이름 아닌 외형 특징으로 지칭 (video 모델은 이름을 모름)
  "dialogue": [{ "speaker": "alice", "emotion": "happy", "line": "..." }],
  "sound": ["distant thunder"],
  "duration_sec": 5
}
```

- 첫 숏은 씬 환경을 확립하는 최대한 넓은 숏 (ViMax 규칙).
- 카메라 포지션 재사용 우선, 큰 무브먼트를 겪은 카메라는 이후 재사용 금지.
- Wide→Medium→Close-up 단계적 전환만 허용 (Long→Close-up 점프컷 금지).
- 콘티 시각화: 숏별 첫 프레임 러프를 **저비용 모델로 1장씩** 뽑아 콘티 보드(HTML)로 사용자 확인 — 선택 사항, 게이트 전 확인용.

### 4.4 영상 제작 (`/ms-produce` → production-director + spaces-engineer 스킬)

1. **Space 구축**: 씬당 1개 Space 생성(`spaces_create`) → `spaces_edit` 자연어 쿼리로 노드 그래프 구축 (캐릭터 Library 참조 → 숏별 키프레임 image 노드 → image-to-video 노드 → 체인). 편집 후 `spaces_edit_status` 폴링 → **`spaces_state`로 그래프가 의도와 일치하는지 검증** (필수).
2. **견적 게이트**: `simulate_spaces`로 크레딧 견적 → 예산 상한(project_brief.budget_cap_credits) 초과 시 차단, 사용자 승인 후 진행. **견적 없이 spaces_run 금지.**
3. **실행**: `spaces_run`(mode=downstream) → `spaces_run_status` 폴링. 실패 노드는 singular 모드로 개별 재실행 (성공한 상류 재과금 방지 — connected 모드는 명시적 전체 재실행에만).
4. **키프레임 품질 루프 + 자동 자기검수 QA**(v0.5.0, 벤치마크 로드맵 2 반영): 키프레임을 N=2~3장 variation 생성 → `quality-reviewer`가 축별(brand_fit·character_consistency·prompt_adherence·spatial_continuity·technical) 자동 심사해 `review`(verdict+원인 층위+issues)를 manifest에 부착하고 **증거와 함께 승인 게이트에 제시**. 클립도 preview-grid로 동일 심사. OpenMontage의 렌더-후 자기검수를 재구현하되, **승인 게이트를 이진→증거 기반으로** 승격했다(review 없이 승인 요청 금지). 심사는 무과금.
5. **합성**: 숏 클립들을 `video_concatenate`로 이어붙여 최종 영상. `production_manifest.json`에 모든 space/run/creation identifier와 상태 기록 → 어느 단계에서 끊겨도 재개 가능(idempotent resume).

### 오디오 (선택)

대사가 있으면 `audio_tts`(+`audio_voices_list`로 보이스 선택), 배경음악은 `audio_music_generate`. `video_speak`으로 립싱크 처리 가능한 모델이면 우선 적용.

### 4.5 후반 편집 (`/ms-post` → post-production-director 스킬) — v0.2.0 신설, v0.3.0 심화

Magnific 합성은 단순 이어붙이기(트랜지션·트림·믹스 불가)라서, 샌드박스 ffmpeg로 후반을 마감한다. v0.3.0에서 후반을 **edit-as-data 정본 + 결정적 실행기 + QC 게이트**로 정식화했다:

- **정본 `edit_plan.json`(edit-as-data).** 에이전트가 컷/트림/전환/자막/음악/납품본을 선언적 EDL로 기술하고, ffmpeg 실행기가 렌더한다. 렌더 실패·재편집이 계획 데이터 수정으로 환원되어 재개 가능(ShortGPT 패턴). 사용자 확정(`approved_by_user`) 후에만 최종 렌더.
- **구체 ffmpeg 레시피.** 입력 정규화(fps/scale/pad/setsar/yuv420p) → **xfade 오프셋 누적 산식**(`offset_k=Σd[0..k-1]−k·t`, 최종=`Σd−(N−1)·t`) → 오디오 믹스(생성 클립 오디오 strip, VO는 **sidechaincompress 덕킹**, **2-pass loudnorm** I=-14/TP=-1.5) → 자막 번인 → 인코딩(H.264 High/yuv420p/+faststart).
- **자막 = libass 우선.** 한글은 Pretendard/Noto Sans CJK KR, ASS `Alignment 2`+`MarginV≈360`(릴스 세이프존). 워드 카라오케는 Remotion `Caption` 스키마 → WhisperX 워드타이밍 → ASS `\k` 렌더. 한글은 `.ass`/`textfile`로 넘겨 셸 이스케이프 회피.
- **음악 싱크 = 측정.** librosa `beat_track`/`onset`/`rms`로 컷을 비트에 스냅하고, RMS 빌드 지점을 서사 전환점(예: 라이딩 시작)에 정렬(실전: 오프셋 5s).
- **비율 파생 = 재구도 사다리.** native(세로 전용 재생성, 최선) > blur_pad(안전) > pad/center_crop > auto_reframe(pyautoflip). 크롭은 구도 훼손이라 기본값 아님.
- **QC 하드 게이트.** 렌더 후 ffprobe + 4지점 프레임 추출로 블랙프레임/무음/자막 오탈자·누락/세이프존 침범을 자기검수하고, 실패본은 납품하지 않는다(OpenMontage 재구현).
- **Magnific 아카이브(기록처 단일화).** 편집은 ffmpeg가 실행하지만, 납품본을 Space에 다시 업로드(`creations_request_upload`→PUT→`finalize`→`spaces_add_creations`)하고 `edit_plan` 요약을 텍스트 노드로 캔버스에 붙여 **Space가 소재·최종본·편집명세의 단일 기록처**가 되게 한다. Magnific은 타임라인 편집 툴이 없어 실행처가 아니라 아카이브 — 재현은 `edit_plan.json`+ffmpeg.

**실전 2편(9:16 네이티브 릴스) 도출 규칙(v0.3.0):** ① 전환은 `fade`(크로스디졸브) 우선 — ffmpeg `dissolve`는 노이즈 디더라 생성 클립에서 지지직거림. ② 생성 클립은 첫 0.3~0.5초 색감 전환을 헤드 트림으로 제거, 엔드카드/로고는 끝에서 정착하므로 `freeze_tail`로 홀드 연장. ③ 클립에 이미 베이크된 슬로건·로고는 자막으로 재오버레이 금지. ④ 단일 loudnorm은 언더슈트하니 `ebur128` 재측정 후 `volume` 보정. ⑤ 한글 카피는 세로 폭에 한 줄로 들어가는지 QC 프레임에서 확인.

업스케일(`video_upscale`)은 편집 확정 후 최종본에만.

### 4.6 실행 2모드 — 과금 경로 실측 (v0.2.0, 실전 도출)

같은 모델이라도 **GUI 재생은 무제한 0크레딧, MCP 실행은 과금**인 플랜이 존재한다(실측: 이미지 75~150cr, 비디오 560~2,800cr/클립 vs GUI 0). 실측(`account_balance.unlimitedAppliesHere` + 1노드 전후 잔액 비교) 후:

- **agent-run**: MCP도 무제한/저가면 에이전트가 전량 실행
- **user-run(프롬프트-온리)**: 에이전트 = 그래프 구축·검증·검수, 사용자 = GUI 재생. 실행 순서 안내와 `currentCreationIdentifier` 변경 확인으로 루프를 닫는다

이 모드에서 파이프라인은 "에이전트가 수십 번의 정밀 배선과 프레임 단위 검수를, 사용자가 클릭을" 담당하는 협업 편집실이 된다. 실전 1편 기준 총 크레딧 소모 3(배경 제거 1회)으로 60초 프로모를 완주했다.

## 5. 횡단 규칙 (core 스킬)

1. **게이트**: `approved_by_user=true` 없는 스테이지 진행 금지. 비용 발생 전 견적 필수.
2. **증거 원칙**: 툴 결과/파일이 증명하지 않은 완료 주장 금지.
3. **Decision Log**: 모델/보이스/Space 구조 등 유의미한 선택은 기각 사유와 함께 append.
4. **Stale 전파**: 상류 아티팩트 수정 시 하류 stale 마킹 + 재실행 범위 보고.
5. **식별자 위생**: creation/space identifier는 아티팩트에만 기록, 사용자 대화에는 webUrl과 이름만.
6. **강등 금지**: 모션 요청을 정지 이미지로, 지정 모델을 다른 모델로 조용히 바꾸지 않는다. 불가하면 blocker 보고.

## 6. 플러그인 패키징

```
magnific-studio/
├── .claude-plugin/plugin.json      # 플러그인 매니페스트
├── .mcp.json                       # Magnific MCP 서버 선언
├── commands/                       # /ms-plan, /ms-characters, /ms-storyboard, /ms-produce, /ms-post, /ms-pipeline, /ms-status
├── skills/
│   ├── magnific-studio-core/       # 횡단 규칙 + 워크스페이스 규약 (모든 커맨드가 필독)
│   ├── planning-director/
│   ├── character-director/
│   ├── storyboard-director/
│   ├── production-director/
│   ├── spaces-engineer/            # spaces_edit 쿼리 작성·검증·실행 노하우
│   ├── post-production-director/   # ffmpeg 후반 마감 (edit_plan.json + QC 게이트)
│   └── quality-reviewer/           # 교차 QA — 자동 자기검수(review) → 증거 기반 승인
├── schemas/                        # 5개 정본 아티팩트 스키마 (project_brief/characters/storyboard/production_manifest/edit_plan)
├── BENCHMARKS.md                   # 2026 경쟁 OSS 비교·평가·로드맵
├── DESIGN.md
└── README.md
```

- 커맨드는 얇은 라우터: 해당 디렉터 스킬 + core 스킬을 읽고 절차를 따르라고만 지시 (OpenMontage의 "얇은 스텁 → 단일 가이드" 패턴, 단 스킬 트리는 단일).
- 라이선스: MIT. OpenMontage는 설계 아이디어 참고만 했으며 코드 미복사(AGPL 비전염) — NOTICE에 명기.

## 7. 리스크와 완충

| 리스크 | 완충 |
|---|---|
| `spaces_edit` 자연어 쿼리가 의도와 다른 그래프 생성 | 편집 후 `spaces_state` 검증 필수화, 불일치 시 수정 쿼리 재발행 (spaces-engineer 스킬의 검증 루프) |
| 크레딧 과소비 | 모든 실행 전 simulate_* 견적 + budget_cap + 승인 게이트 |
| 장시간 job 실패로 파이프라인 중단 | production_manifest에 상태 기록 → 실패 노드만 singular 재실행 |
| 캐릭터 드리프트 | Library 자산 네이티브 참조 + N-variation 심사 루프 |
| MCP 툴 스키마 변경 | 스킬은 툴 이름·의도 수준만 기술, 파라미터는 런타임 스키마 참조 |
| 후반 렌더 결함(블랙프레임·자막 오탈자·비율 훼손) | edit_plan 정본 + 렌더-후 ffprobe/프레임 QC 하드 게이트, 납품 전 자기검수 |
| xfade/자막 ffmpeg 함정(입력 불일치·오프셋·CJK 두부) | 입력 정규화 강제, 오프셋 누적 산식 문서화, libass+한글폰트 규약 |

## 8. 경쟁 포지셔닝과 로드맵 (v0.3.1 벤치마크)

2026 OSS 벤치마크 상세는 [BENCHMARKS.md](BENCHMARKS.md). 요약:

- **가장 직접적 경쟁자는 OpenMontage**(AGPL-3.0, ~4.2k★) — 디렉터-스킬+체크포인트+승인 게이트로 철학이 거의 동일하나, **비용 게이트가 없고 AGPL이라 코드 재사용 불가**. ViMax(MIT, 역할 분해)·VideoClaw(세션 JSON 트리)·MovieAgent(캐릭터 뱅크)는 설계 참고. 최다 star(MoneyPrinterTurbo ~60k, Remotion ~52k)는 에이전틱/캐릭터 기반이 아니다.
- **방어 가능한 차별점**: ① 타입드 JSON 스테이지 계약 ② 비용 거버넌스(이 분야에서 유일) ③ 감사 가능한 Decision Log ④ 큐레이션된 단일 백엔드(Magnific) 품질 + 관대한 라이선스 ⑤ 계약 기반의 낮은 온보딩(OpenMontage 52툴/500스킬 스프롤 대비).
- **채택 로드맵(Adopt-now 상위 5)**: (1) **✅ v0.4.0** — 캐릭터 일관성 계약 + 참조 뱅크(하류가 id로 인용 강제, 프로버넌스), (2) **✅ v0.5.0** — 스테이지별 자동 자기검수 QA(`quality-reviewer`) → 승인 게이트에 증거 부착(축별 `review`), (3) `edit_plan` EDL 버전드 스키마 + 재렌더 멱등성, (4) 콘티 계약에 `generative|stock|hybrid` 숏 전략(Freepik 스톡으로 비히어로 비용 절감), (5) 표준 후반 오디오 스택(TTS+자막 타이밍+BGM 덕킹).
- **범위 밖(의도)**: OpenMontage 코드 차용(AGPL), 로컬 GPU/LoRA 호스팅, 장편·3D 시뮬레이션, 기존 영상 이해/리메이크.

라이선스 원칙 재확인: 모든 참고는 **아이디어·데이터 스키마 수준**이며 코드 미복사. AGPL(OpenMontage)·기업 유료(Remotion)·라이선스 없음(MovieAgent) 프로젝트는 코드로 채택하지 않는다.
