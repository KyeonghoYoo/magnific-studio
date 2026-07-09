# NOTICE

이 플러그인은 아래 오픈소스 프로젝트의 **설계 아이디어**를 참고했다. 어떤 프로젝트의 코드도 복사하거나 파생하지 않았다.

- **ViMax** (HKUDS, MIT) — https://github.com/hkuds/vimax
  참고한 아이디어: 기획/렌더 2단계 분리, 캐릭터 static/dynamic 특징 분리와 멀티뷰 레지스트리, 참조 이미지 선택 휴리스틱, variation_type 기반 렌더 모드 분기, 정적 스냅샷 프레임 규칙, 파일시스템 기반 산출물 캐싱.

- **OpenMontage** (calesthio, AGPLv3) — https://github.com/calesthio/OpenMontage
  참고한 아이디어(코드 미복사, AGPL 비전염): 스테이지별 정본 아티팩트 계약, 승인 게이트 강제, Decision Log, "디스크가 진실" 관찰 모델, 얇은 진입점 라우팅 패턴.

본 플러그인 자체는 MIT 라이선스로 배포된다.

## v0.2.0 추가 참고 (아이디어 차용, 코드 미복사)

- FilmAgent (HITsz-TMG, MIT — 현 VideoClaw로 리네임) — 다역할 비평-수정-검증 루프 개념
- MovieAgent (showlab, **라이선스 없음** — 참조만) — 계층적 CoT 기획 구조
- MoneyPrinterTurbo (harry0703, MIT) / ShortGPT (RayVentura, MIT) — ffmpeg/MoviePy 후반 자동화 파이프라인 패턴, ShortGPT의 편집 마크업(edit-as-data) 개념

## v0.3.0 후반 편집 추가 참고 (아이디어·스키마 차용, 코드 미복사)

- **OpenMontage** (calesthio, AGPLv3) — 렌더-후 ffprobe 자기검수 QC, 프로바이더 스코어링 개념. **코드 미복사·AGPL 비전염**, QC를 자체 재구현.
- **Remotion** (remotion.dev, 커스텀 라이선스 — 4인+ 유료) — `Caption` 스키마 `{word,start_ms,end_ms}`와 카라오케 페이징 **개념만** 차용. Remotion 코드·런타임 미사용, 자막은 libass(ASS `\k`)로 직접 구현해 라이선스 회피.
- **WhisperX** (m-bain, BSD-2) / **faster-whisper** (SYSTRAN, MIT) — 워드 단위 강제정렬 개념(선택적 워드타이밍 소스).
- **librosa** (ISC) — 비트/온셋/RMS 음악 구조 분석으로 컷 스냅·빌드 정렬.
- **MoviePy** (Zulko, MIT) — 불변 `.with_*` 합성 레이어(대안 실행기).
- **auto-editor** (WyattBlue) / **pyautoflip** / **auto-vertical-reframe** — 무음·모션 기반 오토컷, 콘텐츠 인식 세로 리프레임(AutoFlip 2023 단종 대체) 개념.

위 프로젝트들에서 코드는 복사하지 않았으며 설계 아이디어·데이터 스키마만 참고했다. 각 프로젝트의 상표·라이선스는 원저작자에 귀속된다.
