---
name: post-production-director
description: |
  후반 편집 스테이지 디렉터. Use when: (1) /ms-post 실행, (2) 최종 컷의 트리밍/트랜지션/음악/자막/파생본 작업, (3) 합성본(Full Cut)이 나온 뒤 납품 준비를 할 때. 산출물: edit_plan.json(정본) + 최종 납품 파일(들) + production_manifest 갱신.
---

# Post-Production Director — 후반 편집

먼저 `magnific-studio-core` 스킬을 읽었는지 확인한다. 입력: `production_manifest.json`의 숏별 clip(succeeded) 또는 `final_video`.

생성 파이프라인(Magnific)의 구조적 한계 — 단순 이어붙이기, 균일한 클립 길이, 무음, 트랜지션/자막/믹스 부재 — 를 여기서 해소한다.
실행 환경: 샌드박스 **ffmpeg**(+한글 폰트) / 필요 시 **librosa**(음악 분석)·**WhisperX/faster-whisper**(워드 타이밍). MoneyPrinterTurbo·ShortGPT의 ffmpeg 후반 자동화, Remotion의 Caption 스키마, OpenMontage의 렌더-후 자기검수 패턴을 참고(코드 미복사)한다.

## 정본 = edit_plan.json (edit-as-data)

후반의 정본 아티팩트는 **선언적 편집 계획** `edit_plan.json`(`schemas/edit_plan.schema.json`)이다. 에이전트는 창작 결정(컷·트림·전환·자막·음악·납품본)을 **데이터로 기술**하고, 결정적 ffmpeg 실행기가 이를 렌더한다(ShortGPT의 편집 마크업 패턴). 이렇게 분리하면 렌더 실패·재편집이 계획 데이터의 수정으로 환원되고, 어느 지점에서든 재개된다. **계획을 확정받은 뒤에만 렌더한다.**

## 절차

### Step 0 — 소재 수집

`creations_get`으로 숏별 클립 mp4 `url`을 얻어 `.studio/<project>/renders/`로 내려받는다. manifest의 씬 순서가 타임라인 기준. 각 소스의 실제 fps/해상도/길이를 `ffprobe`로 확인해 `edit_plan.source`에 기록한다(가정 금지).

### Step 1 — 편집 계획 (사용자 확정)

컷 리스트를 표로 제시하고 `edit_plan.json` 초안으로 확정받는다: 숏별 사용 구간(in/out 트림), 전환(cut/dissolve/fade), 자막, 음악, 목표 총 길이, 납품본 매트릭스.

**리듬 원칙 — 균일 길이를 그대로 두지 마라.** 생성 클립이 4초 균일이면 감정 비트에 따라 완급을 준다: 설정부 짧게(2~3초), 클라이맥스·표정 비트 길게(4초+). 콘티의 `duration_sec` 목표가 1차 기준이다(실전 1편: 15클립×4초=60초 → 콘티 목표합 53초 → 디졸브 3회로 ~48초).

**자막/카피 밀도.** 릴스는 3~5개의 짧은 카피가 표준이다(실전: 자막 3 + 엔드카드 슬로건 1). 카피는 브랜드 보이스 규칙 준수, 금지어 회피. 서사 전환점(후킹 오프닝, 반전, CTA)에 배치한다.

계획과 그 근거는 decision_log에 기록한다.

### Step 2 — 음악과 싱크

두 경로 중 사용자 선택: (a) `audio_music_generate`(분위기·구조·길이 지정, **simulate_cost 견적 먼저**), (b) 사용자 제공 음원(라이선스 고지).

**서사와 음악의 빌드를 같은 지점에 정렬한다.** 소진→해방 같은 무드 전환 서사면 음악 빌드업/드롭이 그 전환점(예: 밤 라이딩 시작)에 떨어져야 한다. 정렬은 감(感)이 아니라 측정으로:

```python
import librosa, numpy as np
y, sr = librosa.load("music.wav")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr); beat_t = librosa.frames_to_time(beats, sr=sr)
rms = librosa.feature.rms(y=y)[0]; rms_t = librosa.times_like(rms, sr=sr)
build_t = rms_t[np.argmax(np.diff(rms))]      # RMS 급상승 지점 = 빌드/드롭
# sync_offset = (서사 전환 타임라인 지점) - build_t  → 음악을 그만큼 밀거나 당긴다
```

컷 포인트를 비트에 스냅하면 리듬이 산다(`snap(t)=beat_t[argmin(|beat_t-t|)]`). 하이프 몽타주는 onset(`librosa.onset.onset_detect`), 시네마틱은 비트. **최소 컷 길이 ~0.4초**(스트로빙 방지). 실전 1편: RMS 빌드(25s)를 밤 라이딩 시작(20s)에 맞춰 음악 오프셋 5s로 정렬.

### Step 3 — ffmpeg 조립

원칙: **입력 정규화 → 트림 → 전환 체인 → 오디오 믹스 → 자막 번인 → 라우드니스 → 인코딩**. 컷 우선, 디졸브는 필요한 전환에만.

**3a. 입력 정규화(필수).** xfade/concat은 입력 속성이 다르면 깨진다. 모든 클립을 동일 fps·해상도·SAR·픽셀포맷으로 맞춘다: `fps=30,scale=W:H:force_original_aspect_ratio=decrease,pad=W:H:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p`. VFR 소스는 CFR로 강제.

**3b. 트림.** 프레임 정확 트림은 재인코딩 `-ss/-to`. freeze_tail이 있으면 마지막 프레임을 `tpad=stop_mode=clone:stop_duration=N`으로 정지 연장(UI 화면 픽셀정확 CTA 마감 등).

**3c. 디졸브 체인 — 오프셋 누적 산식.** xfade는 매 전환마다 타임라인을 `duration`만큼 당긴다. N클립, 전환 길이 t:
```
offset_k = (d0 + d1 + … + d[k-1]) − k*t        # k번째 전환의 offset
최종 길이  = Σd − (N−1)*t
```
전체 체인을 **하나의 filter_complex**로 처리한다(중간 파일 금지). 예: 각 5초 3클립·t=1s → offset은 4, 8(9 아님).

**3d. 오디오.** 생성 클립 자체 오디오는 기본 제거(`clip_audio: strip` — 컷 간 앰비언스 불일치 방지). 음악 베드를 깔고, VO가 있으면 음악에 **사이드체인 덕킹**:
```
[music][vo]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[duck];
[duck][vo]amix=inputs=2:duration=longest
```
효과음은 타이밍 맞춰 개별로만 얹는다. **최종 라우드니스는 2-pass loudnorm**(measure→apply, `linear=true`): I=-14, TP=-1.5, LRA=11.

**3e. 자막/타이포 — libass 우선.** 스타일·카라오케는 ASS(`subtitles=file.ass:fontsdir=/fonts`), 단일 정적 라벨만 `drawtext`. **한글 폰트는 Pretendard 또는 Noto Sans CJK KR**(기본 폰트는 두부박스 tofu). 한글 텍스트는 인라인 `text=`가 아니라 `.ass`/`textfile=`로 넘겨 셸 이스케이프를 피한다. 세이프마진: 1080×1920에서 하단 ~320–420px(자막/음악바), 우측 ~120–250px(액션레일), 상단 ~120–220px. ASS `Alignment: 2` + `MarginV≈360`, `PlayResX/Y=1080/1920`.

카라오케 팝 자막(WhisperX 워드 타이밍이 있을 때): `\k<cs>`=즉시 전환, `\kf<cs>`=좌→우 스윕, `\t(0,150,\fscx110\fscy110)`=팝 스케일, `\fad()`=페이드. `\k` 값 = 워드 지속×100(centiseconds). 워드 타이밍은 Remotion `Caption`(`{word,start_ms,end_ms}`) 스키마로 통일해 `edit_plan.captions[].word_timings`에 저장한다.

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

렌더-후 자기검수를 **하드 게이트**로 둔다(OpenMontage 패턴, 재구현). `ffprobe`로 길이·해상도·오디오 스트림·라우드니스를 확인하고, 대표 프레임을 **4지점(0%/33%/66%/95%) 추출**해 육안 점검:

- 블랙/깨진 프레임 없음, 전환 아티팩트 없음
- 오디오 무음/클리핑 없음, 라우드니스 타깃(-14 LUFS) 근사
- 자막이 실제로 번인됐고 오탈자·잘림 없음(특히 생성 UI 화면은 전환 중 텍스트가 재작화돼 오탈자가 생김 — 필요 시 마지막 0.3초를 LF 스틸 프리즈로 교체해 픽셀정확 CTA로 마감)
- 세이프존 침범 없음

하나라도 실패하면 납품하지 않고 `edit_plan.qc.passed=false`로 원인과 조치를 남긴다. 통과 시 최종 파일을 **사용자 폴더**(마케팅/납품 폴더)에 저장하고, `edit_plan.deliverables[].path`와 `production_manifest`의 `_deliverables`에 경로·파생본을 기록한다.

### Step 6 — Magnific 아카이브 (기록처 단일화)

편집은 ffmpeg가 하지만 **무엇을 어떻게 편집했는지는 Magnific Space에 남긴다** — 소재 그래프 + 최종본 + 편집 명세가 한 Space에 모이면 Space가 단일 기록처가 된다(사용자 요구: "모든 워크플로우를 Magnific에 기록"). QC 통과한 납품본마다:

1. **최종본 업로드**: `creations_request_upload(mimeType)` → 반환된 `proxyUploadUrl`에 파일 바이트를 **HTTP PUT**(`Content-Type` 지정, 원시 바이너리 — MCP 인자로 바이트를 넘기지 않는다. 재-PUT은 429이니 실패 시 새 타깃 요청) → `creations_finalize_upload(path)`로 creation 생성. (영상 ≤200MB)
2. **Space에 배치**: `spaces_add_creations(spaceId, [creationId])`로 노드 추가 → `spaces_edit`로 노드명을 `★ FINAL <비율> <길이>`로 변경.
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
