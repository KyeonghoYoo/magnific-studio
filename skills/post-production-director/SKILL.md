---
name: post-production-director
description: |
  후반 편집 스테이지 디렉터. Use when: (1) /ms-post 실행, (2) 최종 컷의 트리밍/트랜지션/음악/자막/파생본 작업, (3) 합성본(Full Cut)이 나온 뒤 납품 준비를 할 때. 산출물: edit_plan.json(정본) + 최종 납품 파일(들) + production_manifest 갱신.
---

# Post-Production Director — 후반 편집

먼저 `magnific-studio-core`·`quality-reviewer` 스킬을 읽었는지 확인한다. 입력: `production_manifest.json`의 숏별 clip(succeeded) 또는 `final_video`.

생성 파이프라인(Magnific)의 구조적 한계 — 단순 이어붙이기, 균일한 클립 길이, 무음, 트랜지션/자막/믹스 부재 — 를 여기서 해소한다.
실행 환경: 샌드박스 **ffmpeg**(+한글 폰트) / 필요 시 **librosa**(음악 분석)·**WhisperX/faster-whisper**(워드 타이밍). MoneyPrinterTurbo·ShortGPT의 ffmpeg 후반 자동화, Remotion의 Caption 워드타이밍 개념, OpenMontage의 렌더-후 자기검수 패턴을 참고(코드 미복사)한다.

## 정본 = edit_plan.json (edit-as-data)

후반의 정본 아티팩트는 **선언적 편집 계획** `edit_plan.json`(`schemas/edit_plan.schema.json`)이다. 에이전트는 창작 결정(컷·트림·전환·자막·음악·납품본)을 **데이터로 기술**하고, 결정적 ffmpeg 실행기가 이를 렌더한다(ShortGPT의 편집 마크업 패턴). **실행기는 플러그인 동봉 스크립트 `scripts/render_edit_plan.py`다** — `python3 scripts/render_edit_plan.py <edit_plan.json> --renders-dir <소재 경로> --out <출력> --qc-dir <QC 프레임 경로>` 한 줄로 정규화→트림(+freeze_tail)→경계 xfade→자막 번인→음악 믹스→라우드니스 2-pass→QC 프레임 추출까지 수행한다(스모크 테스트 검증 완료). 에이전트는 임의 ffmpeg 스크립트를 즉석에서 다시 쓰지 말고 이 실행기를 먼저 쓰고, 실행기가 지원하지 않는 특수 처리만 수동 ffmpeg로 보강한 뒤 그 내용을 edit_plan `notes`에 남긴다. 컷 판단이 갈릴 때는 Murch Rule of Six 가중(감정51>스토리23>리듬10>시선7>화면5>공간4 — storyboard-director 편집 문법 부록)을 따른다. 이렇게 분리하면 렌더 실패·재편집이 계획 데이터의 수정으로 환원되고, 어느 지점에서든 재개된다. **계획을 확정받은 뒤에만 렌더한다.**

**버전드·멱등 렌더(v0.6.0).** edit_plan은 `schema_version`·`pipeline_version`을 갖고, **모든 렌더 파라미터를 `render` 블록에 명시**한다(암묵값 금지). 동일 edit_plan + 동일 소스 → **프레임 결정적 재렌더**(인코더 파라미터 고정, 컨테이너 타임스탬프만 예외). 재렌더는 **생성 재소비 0** — 소스 클립은 이미 있고 ffmpeg만 다시 돈다. 따라서 편집은 diff·재렌더·A/B가 자유롭다. **A/B 변형**은 `variants[]`에 base 대비 오버라이드(자막·음악·일부 트림)만 기술해 같은 소스로 다변형을 뽑는다(카피 A/B 등).

## 절차

### Step 0 — 소재 수집

`creations_get`으로 숏별 클립 mp4 `url`을 얻어 `.studio/<project>/renders/`로 내려받는다. manifest의 씬 순서가 타임라인 기준. 각 소스의 실제 fps/해상도/길이를 `ffprobe`로 확인해 `edit_plan.source`에 기록하고(가정 금지), **소스 지문**(clip_id·duration·size_bytes, 필요 시 sha256)을 `source.clips[]`에 남긴다. 재렌더 전 지문을 대조해 소스가 바뀌었으면(=stale) 경고한다 — 멱등성 가드. 확정된 렌더 파라미터는 `render` 블록에, `pipeline_version`에 현재 플러그인 버전을 기록한다.

### Step 1 — 편집 계획 (사용자 확정)

컷 리스트를 표로 제시하고 `edit_plan.json` 초안으로 확정받는다: 숏별 사용 구간(in/out 트림), 전환(cut/dissolve/fade), 자막, 음악, 목표 총 길이, 납품본 매트릭스.

**리듬 원칙 — 균일 길이를 그대로 두지 마라.** 생성 클립이 4초 균일이면 감정 비트에 따라 완급을 준다: 설정부 짧게(2~3초), 클라이맥스·표정 비트 길게(4초+). 콘티의 `duration_sec` 목표가 1차 기준이다(실전 1편: 15클립×4초=60초 → 콘티 목표합 53초 → 디졸브 3회로 ~48초).

**자막/카피 밀도.** 릴스는 3~5개의 짧은 카피가 표준이다(실전: 자막 3 + 엔드카드 슬로건 1). 카피는 브랜드 보이스 규칙 준수, 금지어 회피. 서사 전환점(후킹 오프닝, 반전, CTA)에 배치한다.

계획과 그 근거는 decision_log에 기록한다.

### Step 2 — 오디오 스택 (음악 · VO · 자막 타이밍)

**음악.** 두 경로 중 사용자 선택: (a) `audio_music_generate`(분위기·구조·길이 지정, **simulate_cost 견적 먼저**), (b) 사용자 제공 음원(라이선스 고지).

**내레이션 VO(선택, `audio.voiceover`).** 대본이 있으면 `audio_voices_list`로 보이스를 고르고 `audio_tts`로 생성한다(**과금 — 견적 게이트**). 대본은 브랜드 보이스 준수. VO가 있으면 음악에 **사이드체인 덕킹**(Step 3d)을 적용해 말 위에서 음악이 자동으로 눌린다.

**VO→자동 자막 타이밍(`voiceover.auto_captions`).** VO를 `WhisperX`/`faster-whisper`로 강제정렬해 워드 타이밍을 뽑고, 자체 워드타이밍 스키마(`{word,start_ms,end_ms}` — Remotion Caption 개념 참고, Remotion 실제 타입은 `{text,startMs,endMs,…}`)로 `captions[].word_timings`를 채운다 → Step 3e의 ASS `\k` 카라오케로 번인. 손으로 타이밍을 찍지 않아도 프로급 팝 자막이 나온다.

**서사와 음악의 빌드를 같은 지점에 정렬한다.** 소진→해방 같은 무드 전환 서사면 음악 빌드업/드롭이 그 전환점(예: 밤 라이딩 시작)에 떨어져야 한다. 정렬은 감(感)이 아니라 측정으로:

```python
import librosa, numpy as np
y, sr = librosa.load("music.wav")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr); beat_t = librosa.frames_to_time(beats, sr=sr)
rms = librosa.feature.rms(y=y)[0]; rms_t = librosa.times_like(rms, sr=sr)
build_t = rms_t[np.argmax(np.diff(rms))]      # RMS 급상승 지점 = 빌드/드롭
# sync_offset = (서사 전환 타임라인 지점) - build_t  → 음악을 그만큼 밀거나 당긴다
```

**비트 싱크 독트린(v1.1 개정 — 우발적 비트 고정 방지).** 컷은 **그림**(액션/시선/사운드 이벤트)에서 하고, 비트 싱크는 **텐트폴 ≤3개**(훅·전환점·CTA/마지막)만 정확히 건다. 전 컷을 비트에 스냅하면 드라마가 샴푸 광고처럼 읽힌다(`beat_locked_cutting` — 비트 그리드가 컷을 몰면 Murch 가중의 역전: 리듬 10% < 감정 51%). `audio.beat_snap`: comedy/hype/montage_sequence → `snap`(전 컷 스냅 합법 — 그 장르에선 문자 그대로의 싱크가 크래프트), cinematic/brand/longform → `offset`(비트 근처 컷에 60–150ms 오프셋 허용). 하이프 몽타주는 onset(`librosa.onset.onset_detect`), 시네마틱은 비트. **최소 컷 길이 ~0.4초**(스트로빙 방지). QC: 비코미디 프로파일에서 |컷−비트| 중앙값 <30ms면 beat_locked_cutting 플래그. 실전 1편: RMS 빌드(25s)를 밤 라이딩 시작(20s)에 맞춰 음악 오프셋 5s로 정렬 — 텐트폴 싱크의 예.

**음악은 명명된 큐다(스포팅).** ≥60s 또는 3씬 이상이면 `audio.music_cues[]`(M1, M2…)로 — 큐마다 in/out과 "왜 여기서"(스포팅 근거)를 기록하고 wall-to-wall을 피한다(15–60s 음악 주도 숏폼은 단일 큐가 정상). 큐 태그: `diegesis`(score=덕킹만 / source=원근 EQ·리버브 필요 / trans_diegetic=lo-fi 스템→풀 스코어 스템 크로스페이드 2생성 기법), `provenance`(licensed면 license 필수 — 비면 렌더 차단). **라이트모티프는 같은 스템의 변형 재사용**(pitch/tempo 변환 후 파일을 큐 source로) — 재프롬프트는 정의상 라이트모티프가 아니다(매번 다른 테마가 나온다).

### Step 3 — ffmpeg 조립

원칙: **입력 정규화 → 트림 → 전환 체인 → 오디오 믹스 → 자막 번인 → 라우드니스 → 인코딩**. 컷 우선, 디졸브는 필요한 전환에만.

**3a. 입력 정규화(필수).** xfade/concat은 입력 속성이 다르면 깨진다. 모든 클립을 동일 fps·해상도·SAR·픽셀포맷으로 맞춘다: `fps=30,scale=W:H:force_original_aspect_ratio=decrease,pad=W:H:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p`. VFR 소스는 CFR로 강제.

**3b. 트림 — 생성 클립 특성 보정.** 프레임 정확 트림은 재인코딩 `-ss/-to`. 생성(I2V) 클립은 다음 특성이 있어 트림으로 잡는다(실전 2편 도출):
- **첫 0.3~0.5초 색감/그레이드 전환** — 정지 첫 프레임에서 모션으로 넘어갈 때 톤이 튄다. 도입/설정 컷은 헤드를 ~0.5초 트림해 제거한다.
- **엔드카드/로고는 클립 끝에서 정착** — 페이드인·세팅이 클립 후반이므로 `in`을 끝쪽으로 잡거나, `freeze_tail`(`tpad=stop_mode=clone:stop_duration=N`)로 끝 프레임을 정지 연장해 로고 노출을 늘린다.
- **베이크된 텍스트 중복 금지** — 엔드카드 슬로건·로고가 이미 클립에 렌더돼 있으면 자막으로 다시 오버레이하지 않는다(이중 노출). QC에서 확인.
UI 화면 픽셀정확 CTA 마감도 `freeze_tail`로 처리.

**3c. 전환 — 편집실 어휘(v2), 렌더러가 번역한다.** edit_plan의 전환은 filmcraft 정본 이름으로 쓴다(`filmcraft/references/editing-grammar.md`):

| 값 | 의미 | 길이(ms) |
|---|---|---|
| `cut` | 기본값 — 의미 없음 | 0 |
| `soft_cut` | **기술적 보정**(첫 프레임 톤 팝·유사 점프컷) — 시간 의미 없음, 막 구두점 예약 면제. **헤드 트림이 우선**(무손실), 트림이 내용을 깎을 때만 사용 | 250–500 (기본 300 = 6–12f@24) |
| `dissolve` | 시간 경과 — 길이가 생략의 무게 | 1000–2000 (기본 1000 = 정전 24프레임 디졸브) / 대형 생략 3000–5000 |
| `fade_through_black` / `dip_to_white` | 막·챕터 구두점(예약 규칙 유지) / 회상·플래시(드묾) | 500–2000 |
| `wipe_left/right`, `slide_up/down`, `iris_open/iris_close`, `clock_wipe` | 양식적 — 스스로를 드러냄. 의도 시만 | — |

렌더러(`render_edit_plan.py`)가 ffmpeg xfade로 번역하며, **ffmpeg의 노이즈 디더 `dissolve`는 어떤 경로로도 노출되지 않는다**(생성 클립에서 지지직거림 — 실전 지적). v1 이름(fade/fadeblack/…)은 경고 후 자동 매핑. 스티치드 원테이크 이음은 `hidden_join`(whip/object_wipe/dark_frame)으로 주석 — 후반·재그레이드가 솔기를 알아야 한다. 머리/꼬리 페이드는 `render.opening_fade_ms/end_fade_ms`(기본 500/1000). 오프셋 산식(offset_k = Σd − k·t)은 렌더러의 경계 블렌드 방식과 수학적으로 동치 — 수동 ffmpeg를 쓸 때만 필요.

**3d. 오디오.** 생성 클립 자체 오디오는 기본 제거(`clip_audio: strip` — 컷 간 앰비언스 불일치 방지). 음악 베드를 깔고, VO가 있으면 음악에 **사이드체인 덕킹**:
```
[music][vo]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[duck];
[duck][vo]amix=inputs=2:duration=longest
```
**SFX·앰비언스는 배송 게이트다(무게감 = AI 티 방어).** 화면에 **충돌·임팩트·주인공 보행**이 보이는데 music-only로 납품하면 QC FAIL — 발소리·하드 이펙트 없는 움직임은 일반 시청자에게도 '무게 없음'으로 읽히는 가장 큰 AI 티다. 최소 바닥: **location당 앰비언스 베드 1개**(`audio.ambience[]` — populated/exterior 씬의 완전 무음은 믹스 오류로 읽힘) + **히어로 보행 숏의 발소리** + **가시 임팩트마다 하드 이펙트 1개**(`audio.sfx[]`, 컷/임팩트 프레임에 `at_sec` 정렬). 소싱은 `stock_search`(오디오) — 생성 경로가 없다. **storyboard `shots[].sound[]` 큐는 반드시 edit_plan에 목적지를 갖는다**(비면 QC FAIL — 무단 유실 금지). 렌더러가 music_cues+ambience+sfx를 amix로 믹스한다(VO 덕킹은 기존 수동 레시피 유지).

효과음은 타이밍 맞춰 개별로만 얹는다. **최종 라우드니스는 2-pass loudnorm**(measure→apply, `linear=true`): I=-14, TP=-1.5, LRA=11. 단일 패스 loudnorm은 언더슈트하기 쉬우니(실전: -12.5로 나옴), 렌더 후 `ebur128`로 통합값을 **재측정하고 `volume=(-14 − 측정값)dB`로 보정**한다(비디오는 copy, 오디오만 재인코딩 → 빠름). **다이내믹스 QA**: 같은 ebur128 패스의 **LRA**가 4LU 미만이면(잠정치 — 실측 2편으로 캘리브레이션 예정) cinematic_short/longform/brand에서 warn — 스펙 통과(-14)와 좋은 믹스는 다르다(벽돌 믹스 탐지). shorts_reels는 적용 제외.

**3e. 자막/타이포 — libass 우선.** 스타일·카라오케는 ASS(`subtitles=file.ass:fontsdir=/fonts`), 단일 정적 라벨만 `drawtext`. **한글 폰트는 Pretendard 또는 Noto Sans CJK KR**(기본 폰트는 두부박스 tofu). 한글 텍스트는 인라인 `text=`가 아니라 `.ass`/`textfile=`로 넘겨 셸 이스케이프를 피한다. 세이프마진: 1080×1920에서 하단 ~320–420px(자막/음악바), 우측 ~120–250px(액션레일), 상단 ~120–220px. ASS `Alignment: 2` + `MarginV≈360`, `PlayResX/Y=1080/1920`.

한글 카피는 한 줄에 들어가는지 확인한다 — 세로 프레임 폭(720/1080)에서 긴 문장은 넘치거나 잘린다. 폰트 크기를 줄이거나 `WrapStyle 0`(스마트 랩)로 자동 줄바꿈을 허용하고, QC 프레임에서 실제 렌더를 육안 확인한다(실전: '오늘도 헬멧은 벽에 걸려만 있다.'가 한 줄에 맞도록 크기 조정).

카라오케 팝 자막(WhisperX 워드 타이밍이 있을 때): `\k<cs>`=즉시 전환, `\kf<cs>`=좌→우 스윕, `\t(0,150,\fscx110\fscy110)`=팝 스케일, `\fad()`=페이드. `\k` 값 = 워드 지속×100(centiseconds). 워드 타이밍은 자체 스키마(`{word,start_ms,end_ms}` — Remotion Caption 개념 참고)로 통일해 `edit_plan.captions[].word_timings`에 저장한다.

**3e-2. 그레이드 — show LUT + 씬 트림.** 그레이드 구조는 **show LUT(시퀀스 균일) + 씬별 트림**이다(단일 LUT 절대주의는 컬러 스크립트를 뭉갠다 — filmcraft/color-grading.md). `color.show_lut`(.cube)을 지정하면 렌더러가 자막 번인 **전에** lut3d로 균일 적용한다 — 생성 클립 간 색 드리프트 마스킹의 최우선 도구. 샷 매칭은 히스토그램이 아니라 **히어로 숏**(씬에서 가장 좋은 프레임)에 맞춘다. 씬별 eq 트림은 수동 ffmpeg(로드맵). 생성 출력은 log가 아니다 — **log 디코드 LUT 적용 금지**.

**3f. 인코딩.** H.264 High, `yuv420p`, `-movflags +faststart`, AAC 192k, 30fps(모션 많으면 60).

### Step 4 — 파생본 (납품 매트릭스)

마스터 1개를 만들고 플랫폼 파생을 뽑는다. **비율 파생은 크롭이 아니라 재구도**가 원칙이다(storyboard-director 규칙 6-0). 재구성 사다리(품질 우선순위):

1. **native(최선)** — 9:16 전용으로 재구도해 재생성한 소재를 사용. Magnific에 영상 리프레임 툴이 없고 크롭은 와이드 구도를 훼손하므로, 세로 릴스는 `[9:16]` 브랜치를 네이티브 재생성하는 것이 유일한 고품질 경로다(실전 결정). 이 경우 후반은 세로 소재로 별도 조립한다.
2. **blur_pad(안전 폴백)** — 재생성 불가 시. 콘텐츠 손실 0, 프리미엄한 룩: `split`→배경 `scale=increase,crop,boxblur`→전경 `scale`→`overlay=center`.
3. **pad / center_crop** — 단색 패드 또는 중앙 크롭. 크롭은 구도를 통제한 숏에만(피사체 참수 위험).
4. **auto_reframe** — 콘텐츠 인식 세로 리프레임. Google AutoFlip은 2023 단종 — 유지되는 대안은 `pyautoflip` 또는 `auto-vertical-reframe`(얼굴/포즈/세일런시 추적). 지터 위험 있어 hero 단일 피사체 숏에 한정.

**비율별 문법 이원화(실전 규칙).** 16:9의 측면 병주 투샷이 9:16에서는 후방 추적 투샷으로 바뀌는 등, 같은 서사라도 비율별로 숏 문법이 갈린다 — 파생본은 소재 자체가 다를 수 있음을 전제한다.

컷다운(15/30초): 후킹 숏 우선 재배열 허용 — 단 스토리 인과가 깨지지 않는 범위에서.

### Step 5 — 자동 검수(QC)와 납품

렌더-후 자기검수를 **하드 게이트**로 둔다 — 이는 `quality-reviewer`의 최종 렌더 심사다(축에 loudness·safe_zone·caption_present 추가). `ffprobe`로 길이·해상도·오디오 스트림·라우드니스를 확인하고, 대표 프레임을 **4지점(0%/33%/66%/95%) 추출**해 육안 점검:

- 블랙/깨진 프레임 없음, 전환 아티팩트 없음
- 오디오 무음/클리핑 없음, 라우드니스 타깃(-14 LUFS) 근사
- 자막이 실제로 번인됐고 오탈자·잘림 없음(특히 생성 UI 화면은 전환 중 텍스트가 재작화돼 오탈자가 생김 — 필요 시 마지막 0.3초를 LF 스틸 프리즈로 교체해 픽셀정확 CTA로 마감)
- 세이프존 침범 없음

하나라도 실패하면 납품하지 않고 `edit_plan.qc.passed=false`로 원인과 조치를 남긴다. 통과 시 최종 파일을 **사용자 폴더**(마케팅/납품 폴더)에 저장하고, `edit_plan.deliverables[].path`와 `production_manifest`의 `_deliverables`에 경로·파생본을 기록한다.

### Step 6 — Magnific 아카이브 (기록처 단일화)

편집은 ffmpeg가 하지만 **무엇을 어떻게 편집했는지는 Magnific Space에 남긴다** — 소재 그래프 + 최종본 + 편집 명세가 한 Space에 모이면 Space가 단일 기록처가 된다(사용자 요구: "모든 워크플로우를 Magnific에 기록"). QC 통과한 납품본마다:

1. **최종본 업로드**: `creations_request_upload(mimeType)` → 반환된 `proxyUploadUrl`에 파일 바이트를 **HTTP PUT**(`Content-Type` 지정, 원시 바이너리 — MCP 인자로 바이트를 넘기지 않는다. 재-PUT은 429이니 실패 시 새 타깃 요청) → `creations_finalize_upload(path)`로 creation 생성. (영상 ≤200MB)
2. **Space에 배치**: `spaces_add_creations(spaceId, [creationId])`로 노드 추가 → `spaces_edit`로 노드명을 `★ FINAL <비율> <길이>`로 변경. 납품본이 여러 개면 캔버스 한 영역(예: 우상단 deliverables 열)에 모아 라벨링해 보드가 커져도 탐색 가능하게 한다.
3. **편집 레시피 노드**: `spaces_edit`로 최종본 노드 오른쪽에 텍스트 노드를 추가하고 `edit_plan` 요약(스펙·컷 구조·전환·자막 전문·음악 싱크·QC 결과 + `edit_plan.json` 경로)을 담는다. 편집 후 `spaces_edit_status` 폴링 → `spaces_state`/`spaces_get_nodes`로 검증(spaces-engineer 규약).
4. 업로드 creation id와 Space 노드 id를 `edit_plan.deliverables[].magnific_creation`/`space_node`와 `production_manifest._deliverables.magnific_archive`에 기록.

Magnific은 편집을 실행하지 못하므로(타임라인/트랜지션/자막/믹스 툴 없음) 이 단계는 **실행이 아니라 아카이브**다 — 재현은 항상 `edit_plan.json` + ffmpeg로 한다.

## 납품 스펙 매트릭스 (2026, 재확인 대상)

마스터 1개: **1080×1920, 9:16, H.264 High, yuv420p, MP4 +faststart, AAC, 30fps, -14 LUFS/-1.5 dBTP**.

| 스펙 | Instagram Reels | YouTube Shorts | TikTok |
|---|---|---|---|
| 해상도/비율 | 1080×1920 9:16 | 1080×1920 ≤9:16 | 1080×1920 9:16 |
| 최대 길이 | ~3분(초과분 신규노출 제한) | **≤180초** | 앱 10분/업로드 60분 |
| 프레임레이트 | 30(모션 60) | 30/60 | 30(모션 60) |
| 비트레이트 | 4~5Mbps@1080p | 8~10+Mbps 내보내기 | ~5Mbps@30 |
| 라우드니스 | ~-14–-16 LUFS | -14 LUFS | ~-14–-16 LUFS |

세이프존 공통: 중심 ~900×1400px 안에 핵심 요소. 최대 길이·LUFS·세이프마진은 플랫폼이 수시 변경 — **캠페인마다 재확인**.

## 하드 룰

1. **계획 우선 렌더 후행**: `edit_plan.json`을 사용자 확정(`approved_by_user`) 없이 최종 렌더/납품하지 않는다.
2. **QC 게이트**: 자동 검수 미통과본은 납품하지 않는다. 완료를 주장하기 전에 ffprobe·프레임으로 증명한다(증거 원칙).
3. **업스케일**(`video_upscale`)은 편집 확정 **후** 최종본에만 — 재편집마다 재과금 방지, 실행 전 견적 필수.
4. **원본 클립은 삭제하지 않는다**(재편집 소재). renders/에 보존.
5. **음악 저작권**: 생성 트랙 외 음원은 사용자에게 라이선스 확인을 고지한다.
6. **강등 금지**: 요청된 전환·자막·믹스를 조용히 생략하지 않는다 — 불가하면 blocker로 보고.
7. **아카이브 필수**: 납품본은 Magnific Space에 최종본 노드 + 편집 레시피 텍스트 노드로 기록한다(Step 6). Space가 소재·최종본·명세의 단일 기록처가 되게 한다.
8. **멱등 재렌더**: edit_plan은 버전드·결정적이다. 재렌더·A/B 변형은 **생성 재소비 0**(소스 클립 재사용, ffmpeg만 재실행) — 견적 불필요. 재렌더 전 `source.clips` 지문을 대조하고, 변형은 `variants[]` 오버라이드로만 기술한다(소스 재생성 금지).
