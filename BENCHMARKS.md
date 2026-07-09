# Magnific Studio — 경쟁 OSS 벤치마크 (2026)

> 목적: 유명·고스타 OSS "AI 영상 제작 하네스/에이전트/파이프라인"을 조사·비교·평가하고, Magnific Studio의 갭과 차별점, 도입 로드맵을 도출한다.
> 방법: 2026년 7월 GitHub 라이브 확인(별표·라이선스·최종 push). 별표는 대략치이며 결정 전 재확인 권장. 어떤 프로젝트의 코드도 복사하지 않았다(설계 참고만).

## 1. 비교표 (브랜드 광고 파이프라인 관련도 순)

범례: ✅ 강함 · ◑ 부분 · ✗ 없음 · n/a 해당 없음

| # | 프로젝트 | ★ | 라이선스 | 에이전트 | 캐릭터 일관성 | 콘티/카메라 | 후반/편집 | 비용 거버넌스 | 아티팩트/재현성 | 9:16 납품 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **OpenMontage** | ~4.2k | **AGPL-3.0** ⚠ | ✅ 디렉터스킬+체크포인트+승인 | ◑ 백엔드 의존 | ◑ 스크립트/타임라인 | ✅ 실사+생성 | ✗ | ✅ 체크포인트 | ✅ |
| 2 | **ViMax** (HKUDS) | ~7.5k | MIT ✅ | ✅ Dir/Writer/Producer | ◑ | ◑ | ◑ | ✗ | ◑ | ◑ |
| 3 | **VideoClaw** (ex-FilmAgent) | ~1.6k | MIT ✅ | ✅ 스킬+세션 JSON | ◑ | ◑ 스크립트/콘티 JSON | ◑ | ✗ | ✅ 세션 JSON 트리 | ◑ |
| 4 | **MovieAgent** (showlab) | ~0.35k | **없음** ⚠ | ✅ CoT 멀티에이전트 | ✅ 캐릭터 뱅크+ROICtrl | ✅ 계층 CoT 카메라 | ◑ | ✗ | ◑ | ◑ |
| 5 | **MoneyPrinterTurbo** | **~60k** | MIT ✅ | ✗ 선형 | ✗ 스톡 | ✗ | ✅ TTS/자막/BGM | ✗ | ◑ | ✅ |
| 6 | **ShortGPT** | ~7.4k(휴면) | MIT ✅ | ◑ 편집 DSL | ✗ | ✗ | ✅ edit-as-language | ✗ | ◑ | ✅ |
| 7 | **VideoAgent** (HKUDS) | ~0.72k | MIT ✅ | ✅ 편집/리메이크 | n/a | ◑ | ✅ 에이전틱 편집 | ✗ | ◑ | ◑ |
| 8 | **AI-YT-Shorts-Gen** | ~3–4k | MIT ✅ | ◑ 하이라이트 LLM | n/a | ✗ | ✅ 오토크롭 | ✗ | ◑ | ✅ |
| 9 | **Remotion** | ~52k | **기업 유료** ⚠ | ✗ 라이브러리 | n/a | ✅ 데이터드리븐 | ✅ 렌더 | ✗ | ✅ 코드=소스 | ✅ |
| 10 | **MoviePy / Motion Canvas / Revideo** | 14/19/4k | MIT ✅ | ✗ 라이브러리 | n/a | ◑ | ✅ 렌더 | ✗ | ✅ | ◑ |
| — | **Magnific Studio** | — | 자체 | ✅ 기획→후반 하네스 | ✅ **계약 강제(v0.4.0 reference_bank+인용)** | ✅ 콘티+키프레임 | ✅ ffmpeg+edit-as-data | ✅ **승인+비용 게이트** | ✅ **JSON 계약+Decision Log** | ✅ |

**핵심 판독**
1. **비용 거버넌스 × 타입드 계약**의 교집합은 이 분야에서 비어 있다 — Magnific Studio만 채운다.
2. 가장 직접적 경쟁자 **OpenMontage는 AGPL이고 예산 게이트가 없다.**
3. 최다 star(MoneyPrinterTurbo ~60k, Remotion ~52k)는 **에이전틱하지도, 캐릭터 기반도 아니다**(스톡 몽타주/렌더 라이브러리).

## 2. 프로젝트별 요지

- **OpenMontage** (AGPL-3.0, 활발) — 철학이 우리와 거의 동일: 스테이지별 "디렉터 스킬(md)" + 에이전트 자기검수 + 디스크 체크포인트 + 승인 게이트. 생성/실사 이중 파이프라인. **넘어야 할 기준선.** 단 AGPL(코드 재사용 시 전염)·비용게이트 부재·52툴/500스킬 과대. → 아이디어만 참고, 코드 미사용.
- **ViMax** (MIT, ~7.5k) — 최고 star의 *진짜* 에이전틱 idea→video 하네스. Director/Screenwriter/Producer 역할 분해가 우리 파이프라인에 1:1 매핑. 이미 v0.1부터 차용. 비용/브랜드 레이어 없음.
- **VideoClaw** (구 FilmAgent, MIT) — 스킬 폴더 + 세션 JSON + script/image/video 아티팩트 트리. **아티팩트 레이아웃이 우리와 가장 유사** — 구조 참고 가치.
- **MovieAgent** (라이선스 없음) — 캐릭터 뱅크 → 일관성 방법론의 정본. **소프트웨어로는 채택 불가(라이선스), 설계 인용용.**
- **MoneyPrinterTurbo** (MIT, ~60k) — 스톡 기반 페이스리스 공장. TTS+자막+BGM 자동조립 참고.
- **ShortGPT** (MIT, 휴면) — LLM이 편집 DSL을 내는 edit-as-data의 선례. 우리 후반 정본(edit_plan)의 개념 뿌리.
- **Remotion** (기업 유료) — 데이터드리븐 오버레이/엔드카드/로고버그. **4인+ 영리팀은 유료** — 스케일 시 비용 부채. 대안: MoviePy/ffmpeg(라이선스 클린).

## 3. 갭 분석 (Magnific Studio 기준)

### (i) 도입 권장 — 고레버리지
1. **각 생성 스테이지 뒤 자동 자기검수(비전-LLM QA) → 승인 게이트에 증거 부착** (OpenMontage 패턴). 승인을 "감(感)"이 아니라 점수(브랜드적합·캐릭터일관·프롬프트준수)로. 키프레임/클립 채택 직전에 삽입, 점수를 계약 JSON에 기록.
2. **캐릭터 일관성 계약 + 참조 뱅크**(MovieAgent 캐릭터 뱅크, VideoClaw 캐릭터 JSON). `characters.json`에 잠금 시드/참조 이미지 id/스타일 참조를 두고, 하류 `images_generate`·`video_generate`가 **id로 인용하도록 강제**. 캐릭터 브랜드 광고 품질의 최대 결정 요인.
3. **스톡/하이브리드 숏 전략 필드**(OpenMontage 이중 파이프라인 + MPT 스톡). 콘티 계약의 숏에 `generative | stock | hybrid`를 두고, 비히어로(설정·B롤)는 Freepik 스톡으로 비용 절감 → 비용게이트 서사 강화.
4. **edit-as-data EDL 성숙화**(ShortGPT). 이미 `edit_plan.json`이 있으니, 버전드 스키마 + 재렌더 멱등성으로 마감 — 생성 재소비 없이 diff·재렌더·A/B.
5. **표준 후반 오디오 스택**: TTS 보이스오버 + 자동 자막 타이밍 + BGM 덕킹. 모든 숏폼 공장이 기본 제공하는 테이블 스테이크스.

### (ii) 있으면 좋음
6. Remotion/Revideo 렌더 타깃(데이터드리븐 로어서드·엔드카드·로고). *주의: Remotion 4인+ 유료.*
7. 카메라/블로킹 플래너(MovieAgent CoT) → 콘티 비트별 카메라 무브 산출, `images_change_camera` 연동.
8. 하이라이트/오토크롭 유틸(AI-YT-Shorts-Gen) — 완성 16:9 히어로 컷을 9:16 다변형으로.
9. 스킬/파이프라인 패키징(OpenMontage 500스킬, VideoClaw 스킬폴더) — 스테이지를 설치형 버전드 스킬로.

### (iii) 의도적 범위 밖
- 3D 가상 스튜디오 시뮬레이션(FilmAgent) — 매체가 다름.
- 로컬 GPU 모델 호스팅/LoRA 학습(MovieAgent ROICtrl) — 우리 논지는 *관리형 MCP 품질*.
- 장편 영화 생성(MovieAgent/MovieDreamer) — 브랜드 릴스는 숏폼.
- 기존 영상 이해/리메이크(VideoAgent) — 인접 제품.
- **OpenMontage 코드 직접 차용 금지 — AGPL-3.0 비호환.**

## 4. 방어 가능한 차별점

1. **타입드 JSON 스테이지 계약이 파이프라인의 척추.** 경쟁작은 아티팩트를 파일/체크포인트로 남기지만 스키마 계약은 아니다 → 결정적 재실행·부분 재실행·diff 가능.
2. **비용 거버넌스가 1급 게이트.** 벤치마크 전체에서(직접 경쟁 OpenMontage 포함) 예산 게이트를 노출하는 프로젝트는 0. 유료 생성 백엔드에 `simulate_cost→승인→집행` 루프는 에이전시/기업 셀링포인트.
3. **Decision Log + 승인 게이트 = 감사 가능·재현 가능 프로덕션.** "왜 이 숏을, 얼마에, 누가 승인" 추적 — 브랜드/에이전시 워크플로에 특화.
4. **큐레이션된 단일 백엔드(Magnific) 품질 + 관대한 라이선스.** 필드는 "모델 불문이나 일관성 낮음". AGPL(OpenMontage)·유료(Remotion)와 달리 라이선스 통제권 보유.
5. **Claude Code 하네스 에르고노믹스.** OpenMontage의 52툴/500스킬 스프롤보다 계약 기반으로 타이트 — 낮은 온보딩 비용.

## 5. Adopt-now 로드맵 (상위 5, 우선순위)

| # | 항목 | 슬롯 | 근거 |
|---|---|---|---|
| 1 | ✅ **v0.4.0 반영** — 캐릭터 일관성 계약 + 참조 뱅크(id 인용 강제·프로버넌스) | 캐릭터 스테이지 | 캐릭터 광고 품질 1순위 결정 요인. `reference_bank`+`consistency_policy`+manifest `references_used`/`consistency_check` |
| 2 | ✅ **v0.5.0 반영** — 스테이지별 자동 자기검수 QA(`quality-reviewer`) → 승인 게이트에 증거 | 각 생성 게이트 | 승인을 이진→증거기반으로. 축별 `review`(verdict+원인층위) → manifest, 무과금 |
| 3 | ✅ **v0.6.0 반영** — edit_plan EDL 버전드 스키마 + 재렌더 멱등성 | 후반 | 생성 재소비 없이 diff/재렌더/A-B, 비용게이트와 복리 |
| 4 | ✅ **v0.7.0 반영** — 콘티 계약에 generative/stock/hybrid 숏 전략 | 콘티 | 비히어로 비용 절감, 비용게이트 서사 강화. `generation_strategy`+`stock` 필드 |
| 5 | ✅ **v0.8.0 반영** — 표준 후반 오디오(TTS 내레이션+VO 워드타이밍 카라오케 자막+BGM 덕킹) | 후반 | 완성 릴스 테이블 스테이크스. `audio.voiceover`+`ducking`, WhisperX→captions.word_timings |

> **Adopt-now 로드맵 5/5 완주(v0.4.0→v0.8.0).** 벤치마크에서 도출한 상위 5개 개선을 모두 반영했다.

**하지 말 것:** OpenMontage 코드 차용(AGPL) · 로컬 GPU/LoRA 호스팅 · 장편/3D 시뮬레이션.

## 출처

- OpenMontage https://github.com/calesthio/OpenMontage · ViMax https://github.com/HKUDS/ViMax · VideoClaw https://github.com/HITsz-TMG/VideoClaw · MovieAgent https://github.com/showlab/MovieAgent · MoneyPrinterTurbo https://github.com/harry0703/MoneyPrinterTurbo · ShortGPT https://github.com/RayVentura/ShortGPT · VideoAgent https://github.com/HKUDS/VideoAgent · AI-YT-Shorts-Gen https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator · Remotion https://www.remotion.dev/docs/license · MoviePy https://github.com/Zulko/moviepy · Motion Canvas https://github.com/motion-canvas/motion-canvas · Revideo https://github.com/redotvideo/revideo

> 별표·라이선스·활동성은 2026-07 기준 라이브 확인값이며 변동한다. 채택 결정 전 재확인.
