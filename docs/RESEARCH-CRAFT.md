# filmcraft 리서치·대심 토론·판정 기록 (v1.1.0)

> 목표: "매 추론"을 "정본 사전 참조"로. 전 부서 영화 기법을 실무·학술·AI 3중 검증으로 정합해
> 통제 어휘(스키마 enum)·하드 룰·프롬프트 프로젝션으로 하네스에 내장한다.
> 종료 기준: 전 항목 실무 활용성 교차검증 일치율 ≥95% + 정합성(enum⊆사전, 용어 드리프트 0).

## 1. 파이프라인

**P1 아키텍처** → **P2 리서치 fan-out**(12개 부서 에이전트, 웹 검증 — 수치·분쟁·2023 이후는 [v] 마킹 의무) → **P3 공격적 대심 토론**(3관점 × 37개 안건) → **수석 중재 판정**(`_rulings.md` — 배포 스냅숏 `docs/filmcraft-rulings.md`) → **P4 집필**(15 레퍼런스) → **P5 하네스 통합**(스키마 v2·렌더러 v2·스킬 6종 개정) → **P6 정량 검증 루프**.

부서: 각본구조 · 숏 문법 · 카메라 무브 · 렌즈/광학 · 조명 · 연출/미장센 · 편집 · 컬러 · 사운드/음악 · VFX/애니메이션 · 프로덕션 디자인 · AI 프롬프트 크래프트(브리지).

## 2. 대심 토론 — 3관점과 중재 원칙

| 관점 | 역할 | 대표 주장 |
|---|---|---|
| **학술 순수주의** | 정의 경계·정전 충실(Bordwell·Mascelli·Chion·Murch) | "줌은 카메라 무브먼트가 아니다(시차 없음)" · "더치는 롤이지 피치가 아니다 — angle enum에 두면 로우앵글 캔티드(제3의 사나이)를 표현 못 한다" · "high-key는 비율 클래스지 밝기가 아니다" |
| **현장 실무** | 세트·편집실에서 실제 쓰는 말·가르칠 수 있는 규칙 | "조명 플롯과 플로어 플랜은 별개 문서다 — 씬 레벨 블록으로 축 과잉을 구조적으로 해소" · "스키마는 편집실 언어로 말하고 렌더러가 번역한다" · "모델이 3무브를 허용해도 쓰지 마라 — 능력은 허가가 아니다" |
| **AI 파이프라인** | 검증 가능성·스키마 진화 비용·모델 스티어링 증거 | "2계층+프로젝션: 아티팩트는 모델-프리, 프롬프트는 컴파일" · "이동 무브에 foreground_anchor 없으면 달리 값 내고 줌을 받는다" · "규범에 모델명 금지 — Sora API는 2026-09-24에 죽는다" |

**중재 원칙: 정의는 학술이, 스키마 표면적은 실무가, 검증 가능성은 AI가 이긴다.**

### 대표 판정 (전체 37건 + 신규 충돌 19건은 `.omc/research/filmcraft/_rulings.md`)

- **카메라 무브 4축 확정**: base(13종)+direction+speed+support. 학술의 `optical` 5축 분리는 **사전 본문에서 진실로 가르치되** 스키마는 플랫 유지(에이전트 오기입·검증 단순성 — 실무+AI 승). `slow_push_in` 해체, push_in/tracking/orbit/steadicam 등 12개 별칭 **저작 시 해소 의무**.
- **더치 분리(학술 승)**: `dutch_deg`(롤 필드, 0–45)를 angle enum에서 분리 — 로우앵글 캔티드 표현 가능.
- **framing/function 분리(학술 승)**: insert/cutaway/master는 프레임만 봐선 판별 불가한 **편집 역할** — 별도 축. 설정 숏 3자 충돌(콘티 룰 "와이드로 열어라" × 모델 최약점 × 숏폼 훅 우선)은 `function: establishing → stock 후보`로 해소(실무 발견).
- **전환 어휘 전면 개편(만장일치 — 라이브 버그 2건 적발)**: 기존 스키마에서 ①금지된 ffmpeg 노이즈 디더 `dissolve`가 선택 가능했고 ②`fade`가 크로스디졸브를 의미해 암전 요청 시 오렌더. → 편집실 언어(soft_cut/dissolve/fade_through_black/…) + 렌더러 번역층. `soft_cut`(200–400ms)은 **의미 없는 기술적 보정**으로 신설 — 막 구두점 예약 규칙을 지키면서 첫 프레임 톤 팝을 잡는다.
- **비트 고정 컷팅(학술이 명명 교정)**: 자동 비트 스냅의 부작용은 mickey-mousing(스코어가 동작 모사 — 코미디에선 정당한 기법)이 아니라 `beat_locked_cutting`. 원칙적 금지 근거 = **Murch Rule of Six의 역전**(리듬 10% < 감정 51%). 컷은 그림에서, 싱크는 텐트폴 ≤3개만.
- **recruitment 비트 기각(학술 승)**: "세계 사건 vs 주인공 결단"은 이미 catalyst(~11%)와 break_into_two(~22%)로 존재 — 추가는 중복. 대신 `debate` 옵션 비트.
- **식별자 핸들 포크(AI 승, 실무가 스코프 교정)**: 참조 배선+태그 지원 → 모델 네이티브 태그(@name), 그 외 → 외형 문구. **기존 룰 2는 틀린 게 아니라 motion_desc 스코프였다** — 2인 프레임에서 비디오 모델은 외형으로만 움직일 대상을 구분한다.
- **모델명 추방(만장일치)**: production-director의 기존 모델 노트가 하드코딩+사실 오류(Sora=1무브 엄격, 멀티무브는 Hailuo/Luma)로 판명. capability 플래그 8종 + 날짜 있는 model-matrix.md로 대체.
- **거절된 것들**: 시선 각도 15–20° 허용치(비검증 통속 수치 — gaze_target enum으로 대체) · "soundtrack" 큐 타입(앨범/전체 트랙이지 큐 분류가 아님) · golden_ratio 구도 태그(지각 효과 비입증) · camera_height 축(angle에 접힘) · Eisenstein 5기법 enum(4/5가 프롬프트·ffmpeg 무차이 — 사전 개념으로만) · 단일 LUT 절대주의(컬러 스크립트를 뭉갬 — show LUT+씬 트림).

### 토론이 적발한 기존 하네스 결함 (5건)

1. edit_plan 전환 enum의 이중 함정(위 참조) — **schema_version 2.0으로 수정**
2. storyboard에 `scenes[]` 부재 — 씬 계약(조명·축)의 거주지 신설
3. `shots[].sound[]`의 후반 목적지 부재 — 기획된 효과음이 조용히 유실 → sfx/ambience 배열 + QC 검증
4. `variation_type: large`가 금지된 와이드↔클로즈업 FLF 페어를 장려 — FLF 합법조건(동일 카메라 포지션)으로 재정의
5. 길이 산술 불일치 — 콘티 합계가 트림·디졸브로 타임라인 대비 10–15% 부족(실전 1편에서 관찰됐으나 미인코딩) → **핸들 규칙**(+0.5s/+0.3s) 상류 인코딩

## 3. 반영 하이라이트 (v1.1.0)

- `skills/filmcraft/` 15 레퍼런스 + SKILL.md 인덱스 (스테이지 라우팅 매트릭스)
- 스키마 v2: storyboard(scenes[]·movement 객체·framing/function·screen_direction·gaze_target·lens_mm) / project_brief(visual_grammar required) / edit_plan(편집실 전환 어휘·music_cues·sfx·ambience·라이선스 게이트·show_lut)
- 렌더러 v2: 번역층·duration_ms·다중 오디오 amix·lut3d·페이드 설정화 (v1 하위호환 — 드라이런 검증; 실 ffmpeg 검증은 ffmpeg 설치 환경에서 재실행 필요)
- 스킬 개정 6종: core(사전 라우팅+횡단 하드 룰) · planning(Visual Grammar Contract 스텝 신설) · storyboard(씬 계약·병합 규칙·핸들) · production(capability 플래그·FLF 강화·conform_from_source·프로젝션) · post(전환 v2·스포팅·비트 독트린·SFX 게이트·show LUT) · quality-reviewer(신규 5축 + pre-flight lint)

## 4. 정량 검증 (P6) — 종료 기준 대비 결과

- **방법**: 집필에 참여하지 않은 독립 검증단 5개 에이전트가 15개 레퍼런스의 canonical 엔트리 **605건**을 5개 배치로 분할, 3기준(① 실무 실재성 — 실제 현장/문헌에서 쓰이는 용어·기법인가 ② 정의 정확성 — 수치·귀속·정의가 검증 가능한 출처와 일치하는가 ③ AI 번역 유효성 — 프롬프트/스키마 매핑이 실제 생성 파이프라인에서 작동하는가)으로 교차 판정. 수치·분쟁·2023년 이후 주장은 웹 재확인([v] 마커) 의무.
- **1차 판정**: 537 pass / 31 fail / 37 unsure = **88.8%**.
- **수정 패스**: fail 31건 전량 + unsure 유발 요인 수정 — 대표: 편집 지속시간 티어 30fps 오류→24fps 정본, Hall proxemics 수치(social 4–12ft/3.7m), 30° rule 재귀속(Mascelli 단독→고전 연속성 관행), flat_1_1 프록시 부정문→긍정문 재작성, costume multiples "minimum 3" 철회, J/L컷 가공 필드 인용 제거(큐 배치로 재표현), 파이프라인 조어 공시(impact_settle·Gesture Economy 등), KR 음절 예산 브레스 셰이브, 끊어진 .omc 인용→배포 스냅숏 `docs/filmcraft-rulings.md` 신설. 스키마 실보강: `audio.voiceover.mode` enum 추가, `parallax_note`·`iris_close` 등.
- **델타 재검증**: 수정된 fail/unsure 엔트리 68건만 동일 검증단 5명이 재판정(웹 재확인 24회+). 이 과정에서 검증단 스팟체크가 **수정이 만든/남긴 신규 결함 16건을 추가 발견**(대표: 삭제 필드 `audio_*_offset_ms` 고아 참조 — editing-grammar 4곳 + repo 전역 3곳, lighting §4 골든아워 미동기화, LUT 행↔스파인 모순, KR VO 예산의 화행 모드 오류[대화 5–5.5 syl/s → 낭독 3.5–4.5 syl/s 재산정]) — 전량 수정 후 재확인.
- **최종 판정**: **605 엔트리 중 601 pass = 99.3%** · fail 0 · unsure 4(0.7%) — 잔존 unsure는 전부 dated appendix(model-matrix.md)의 벤더 사실로, 행에 UNVERIFIED/CONFLICT 공시 마커를 기재해 "미검증을 검증필로 주장하지 않음" 원칙으로 처리. 검증단별: practitioner 16/16 · camera 8/8 · academic 14/14(+전역 스팟체크) · ai 125/125 슬라이스 100% · editing 8p/4u.
- **결정적 정합성 체크**: `scripts/lint_filmcraft.py` 6종(스키마 enum⊆사전 · 금지 별칭 · 파일 크기 ≤500행 · KR gloss · 인용 무결성 · empty-token 맥락) — **refs 15, 실패 0, 경고 0 통과**. 스키마 5종 JSON 유효.
- **환경 캐비앳**: 이 머신에 ffmpeg 미설치 — 렌더러 v2는 드라이런(서브프로세스 몽키패치로 필터그래프 캡처) 검증까지 완료, 실렌더 스모크는 ffmpeg(≥4.4, amix normalize=0) 환경에서 1회 필요.
- 상태: **게이트 통과 — 종료 기준 충족** (pass율 99.3% ≥ 95%, 결정적 정합성 체크 전부 통과)

### 후속 백로그 (P6 검증이 적립 — 판정과 무관한 로드맵)

1. `audio.voiceover.start_sec` 필드 + 렌더러 adelay 경로 — VO 프리랩/포스트랩 완전 저작화(현재: TTS 렌더 무음 패딩으로 대체, sound-music D7).
2. 보이스별 syl/s TTS 캘리브레이션(문장 1개 렌더 → ffprobe 길이 ÷ 음절수) — KR VO 예산 [PROVISIONAL] 해제.
3. per-scene `colorbalance`/`curves` trim 렌더러 경로 — 현재 declared manual pass(color-grading 스파인).
4. 캡션 per-duration 문자 예산표 — 현재 open item(sound-music §4), VO 예산 유용 금지만 명시된 상태.
5. emotion-recipes Example C에 씬별 `kind` 태그 — 극성 설계 재유도 필요(잘못 달면 R2 위반을 예제에 심음).
6. model-matrix Seedream/Wan/Seedance 행 1차 소스 재확인 — CONFLICT/UNVERIFIED 마커 해제 조건.
7. ffmpeg(≥4.4) 환경에서 렌더러 v2 실렌더 스모크 1회 — 현재 드라이런(필터그래프 캡처) 검증까지 완료.

## 5. 출처 계층

정전(부서별 상세는 각 레퍼런스 §5): Bordwell&Thompson · Mascelli Five C's · Katz · Murch · Eisenstein/Pudovkin/Kuleshov · Chion · Gorbman · Sonnenschein · Thomas&Johnston · Williams · Alton/ASC · Bellantoni · Storaro · Zettl · Hall · Burch · Block · Lumet · McKee/Field/Snyder/Vogler/Harmon/Gulino · Weiland · Miller(SB7) · Nichols · VES Handbook · SMPTE/ITU/EBU.
공식 프롬프트 가이드(2025–26): Google DeepMind/Cloud(Veo·nano-banana) · OpenAI(Sora 2 cookbook) · Runway · Kling · Luma · MiniMax · BFL(Flux) · ByteDance(Seedance/Seedream) · Alibaba(Wan).
학술(AI): arXiv 2506.15742(Kontext) · 2512.14691(물리 상식 벤치) · 2505.11425 · 2401.14425(artstation 토큰) · 2605.17500(스타일 누출).
