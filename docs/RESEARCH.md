# Magnific Studio — 리서치 종합: 관점 축, 가중 토론, 반영 결정 (v1.0.0)

> **평가 루프 결과 (종료 조건: 전 축 ≥90%)** — 1회차: A86 F80으로 미달 → 스키마 계약 바인딩 7건 반영 →
> 2회차: **A95 · B92 · C90 · D95 · E90 · F93 · G92 · H92, 가중 총점 92.7% — 전 축 통과, 루프 종료.**
> 잔여 하드닝 3건(deliverable required 승격, purpose==brand→brand_assets 조건부 필수,
> commercial/shorts→beat_map 조건부 필수)까지 반영 후 1.0.0 태깅.

> 2026-07 광범위 리서치(전통 영상 제작론 정전 15건 + AI 생성 영상 생태계: GitHub star 실측 상위 12 리포,
> 인용 순 학술 논문 8건, 상업 AI 필름 사례 3건)를 취합해 평가 축을 세우고, 축 간 가상 공격 토론으로
> 가중치를 정한 뒤, 그 가중치로 반영 우선순위를 결정한 기록. 출처 전체 목록은 하단.

## 1. 관점 축 (8축)

| 축 | 정의 | 근거 정전 |
|---|---|---|
| A. 서사 구조 | 신 가치전환, 비트 배치, 오프닝/파이널 대구 | McKee *Story*, Snyder *Save the Cat* |
| B. 숏 문법 | 180°/30° 규칙, 커버리지, 스크린 디렉션, 카메라 어휘 | Bordwell&Thompson *Film Art*, Katz *Shot by Shot*, Thompson&Bowen *Grammar of the Shot/Edit* |
| C. 편집·리듬 | Murch Rule of Six 컷 가중, ASL·1/f 리듬, 매칭 액션 | Murch *In the Blink of an Eye*, Cutting(Cornell) 주의 연구 |
| D. 일관성(AI 특화) | 키프레임 우선, 캐릭터 뱅크, FLF 쌍 검증, 체이닝 금지 | StoryDiffusion, Wan FLF2V 커뮤니티, 실전 2편 |
| E. 오디오 | 음악 빌드-서사 정렬, 라우드니스 표준, VO 덕킹 | EBU R128/BS.1770, librosa 관행 |
| F. 브랜드·포맷 효과 | 훅·프론트로딩, 브랜드 펄싱, 60/40, 세이프존 | YouTube ABCD(17k 캠페인 검증), TikTok Creative Codes, Teixeira, Binet&Field, Sharp, EBU R95 |
| G. 제작 관리·재현성 | 계약 아티팩트, 비용 게이트, 캐시·더티, 결정적 렌더, OTIO | ComfyUI 철학, OpenTimelineIO, PPM 관행, 실전 2편 |
| H. 품질 보증 | 비평-수정 루프, 증거 기반 게이트, N-후보 선별 | FilmAgent(Critique-Correct-Verify), VideoAgent, Anim-Director, AniMaker, Kalshi/Coca-Cola 사례 |

## 2. 가상 공격 토론 → 가중치

**라운드 1 — "일관성이 왕이다" (AI 엔지니어) vs "편집이 왕이다" (편집감독).**
엔지니어: AI 영상의 실패 모드 1위는 정체성 붕괴다 — 실전에서도 빈 키프레임 한 번에 헬멧·인물·바이크가 전부 무너졌다. 일관성 없으면 편집할 소재 자체가 없다. 편집감독: 그러나 Coca-Cola 사례(7만 클립→후반 100명)와 Kalshi(채택률 4%)가 증명하듯 **생성은 싸고 큐레이션·편집이 지배 비용**이다. Murch의 감정 51%는 소재가 아니라 컷이 만든다. **판정**: 일관성은 "게이트 통과의 전제"(없으면 0점)로 최고 가중, 편집은 "품질의 상한"으로 차상위. D=18, C=15.

**라운드 2 — "구조 없는 영상은 소음이다" (각본가) vs "숏폼에서 3막은 죽었다" (퍼포먼스 마케터).**
각본가: McKee의 가치전환 없는 신은 비사건이다 — 실전에서도 '이동 비트 누락'이 시청 어색함으로 즉시 드러났다. 마케터: 동의하되, 30초 이하에서 구조란 훅-바디-CTA다. ABCD는 17,000 캠페인으로 검증됐고 상기 효과의 90%는 첫 6초에서 결정된다. **판정**: 서사와 포맷 효과는 동률이되, **충돌 시 포맷이 우선**한다는 조건부 서열을 명문화. A=14, F=14.

**라운드 3 — "문법은 자동 검증 가능해야 가치 있다" (파이프라인 엔지니어) vs "규칙은 어길 때 아름답다" (시네마토그래퍼).**
엔지니어: 180°/30°/스크린 디렉션은 기계 판정 가능한 몇 안 되는 규칙이고, 실전의 교차 주행 사고 2회가 전부 이 축 부재였다. 시네마토그래퍼: Murch가 말했듯 하위 규칙은 감정을 위해 깨질 수 있다 — 규칙 엔진이 창의를 검열하면 안 된다. **판정**: 숏 문법은 "위반 시 플래그(차단 아님)" 방식으로 B=10. 관리·재현성은 이번 두 편의 완주를 실제로 가능케 한 기반이므로 G=10.

**라운드 4 — "QA는 비용이다" (프로듀서) vs "QA가 채택률을 만든다" (품질 책임).**
프로듀서: 심사가 생성보다 오래 걸리면 본말전도다. 품질: preview-grid 심사는 크레딧 0이고, 실전에서 불합격 6건을 납품 전에 전부 잡았다 — 원인 층위 분류가 재시도 비용을 절반으로 줄였다. **판정**: H=12 (관리보다 높게 — AI 파이프라인 특성상 큐레이션이 leverage). 오디오는 표준화가 잘 되어 있고(수치 타깃) 자동화 여지가 커서 E=7.

**최종 가중치**: D 일관성 18 · C 편집리듬 15 · A 서사 14 · F 브랜드포맷 14 · H 품질보증 12 · B 숏문법 10 · G 관리재현성 10 · E 오디오 7 (합 100).

## 3. 가중 반영 결정 (이번 v0.9.0에 들어간 것)

- **D(18)**: FLF 쌍 검증에 심도·샷사이즈 일치 추가, last-frame 체이닝 2세대 금지, 씬 키프레임 동일 배치 생성 권고, 캐릭터 뱅크(턴어라운드 3~5장) 명문화 — production/character-director.
- **C(15)**: Murch Rule of Six 가중(감정51>스토리23>리듬10>시선7>화면5>공간4)을 편집 판단 기준으로, ASL 파라미터·1/f 군집 리듬, 매칭 액션 컷 — storyboard/post-production-director.
- **A(14)**: 신 가치전환(± 뒤집기, 비사건 플래그), 비트 백분율 검증, 오프닝/파이널 거울쌍 — planning/storyboard-director.
- **F(14)**: 신규 **format-director** 스킬(프로파일 4종, 훅·펄싱·60/40·세이프존·라우드니스 매트릭스). 포맷>영화문법 우선순위 명문화.
- **H(12)**: 히어로 숏 차등 N-후보(AniMaker), 비평-수정 루프에 원인 층위(기존), review 객체 게이트 필수(기존 강화).
- **B(10)**: 180° 축·30° 규칙·커버리지 세트·eye-trace를 "위반 시 플래그"로 — storyboard-director.
- **G(10)**: **scripts/render_edit_plan.py**(결정적 실행기, 스모크 테스트 통과), 소스 지문 가드, 시드·모델 직렬화, OTIO 호환은 로드맵.
- **E(7)**: 기존 v0.6~0.8 후반 스택(빌드 정렬·2-pass 라우드니스·덕킹)이 이미 충족 — 유지.

## 4. 반영 보류 (로드맵)

- OTIO 내보내기 어댑터(G) / auto_reframe 통합(pyautoflip)(F) / LoRA 캐릭터 학습 경로(3씬 초과 시 손익분기)(D) / MCTS식 클립 선택(H) / VO 카라오케 실전 검증(E).

## 5. 출처 (요약)

**정전**: Bordwell&Thompson Film Art · Murch In the Blink of an Eye · McKee Story · Katz Shot by Shot · Snyder Save the Cat · Thompson&Bowen Grammar of the Edit/Shot · Cutting(Psych. Science 2010) · Teixeira(Marketing Science 2010, JMR 2012) · Binet&Field(IPA) · Sharp How Brands Grow · YouTube ABCD · TikTok Creative Codes · EBU R128/R95 · OpenTimelineIO.
**생태계(star 실측)**: ComfyUI 120k · MoneyPrinterTurbo 96.5k · Remotion 52.7k · Wan2.2 16.6k · MoviePy 14.8k · HunyuanVideo 12.3k · AnimateDiff 12.2k · ViMax 11.1k · LTX-Video 10.7k · ShortGPT 7.7k · StoryDiffusion 6.4k · editly/revideo.
**학술(인용 순)**: VideoDirectorGPT 151 · Mora ~100 · MovieAgent 68 · FilmAgent ~60 · Anim-Director 42 · DreamFactory 28 · VideoAgent 22 · AniMaker 8.
**사례**: Kalshi NBA(채택률 4%) · Coca-Cola Holiday(7만 클립+후반 100명) · 2026 AI 단편 표준 워크플로(모델 라우팅+통합 그레이딩+업스케일).
