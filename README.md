# Magnific Studio

Magnific(구 Freepik) MCP의 **Spaces**를 실행 레이어로 쓰는 Claude Code 영상 제작 하네스 플러그인.
**기획 → 캐릭터 생성 → 콘티(스토리보드) → 영상 제작 → 후반 편집**을 단계별 승인 게이트와 비용 견적을 갖춘 파이프라인으로 실행한다.

v0.2.0은 실제 브랜드 프로모 1편(15숏/60초)을 이 파이프라인으로 완주하며 검증된 실전 규칙들을 반영했다 — 총 크레딧 소모 3으로.

**v0.3.0**은 후반 편집(/ms-post)을 대폭 심화했다: **edit-as-data 정본(`edit_plan.json`)** + 구체 ffmpeg 레시피(디졸브 오프셋 누적 산식·사이드체인 덕킹·2-pass loudnorm −14 LUFS)·**librosa 음악 싱크**(비트 스냅 + RMS 빌드→서사 정렬)·**libass 한글 카라오케 자막**(Pretendard/Noto CJK, 릴스 세이프존)·**9:16 재구도 사다리**(native>blur_pad>crop>auto_reframe)·**렌더-후 QC 하드 게이트**(ffprobe+프레임 자기검수). OSS 하네스(OpenMontage/Remotion/WhisperX/librosa/MoviePy)의 검증된 패턴을 라이선스 안전하게 재구현.

## 커맨드

| 커맨드 | 역할 |
|---|---|
| `/ms-plan [아이디어]` | 기획 — Magnific `video_plan` 기반 컨셉 2~3안 → `project_brief.json` |
| `/ms-characters` | 캐릭터 — static/dynamic 시트 → 3뷰 생성 → Magnific Library 자산 등록 |
| `/ms-storyboard` | 콘티 — 카메라를 enum으로 구조화한 숏 리스트 → `storyboard.json` |
| `/ms-produce` | 영상 — Space 구축(편집-검증 루프) → 견적 게이트 → 키프레임/클립 심사 루프 → 합성·시사 |
| `/ms-post` | 후반 — ffmpeg 트리밍/트랜지션/음악/자막/파생본(9:16 릴스) → 납품 |
| `/ms-pipeline [아이디어]` | 위 단계 일괄 실행 (게이트는 유지) |
| `/ms-status` | 진행 상황 보고 (읽기 전용) |

## 설치

```bash
# 플러그인 디렉토리를 클론/복사한 뒤 Claude Code에서
/plugin install <path-or-marketplace>/magnific-studio
```

Magnific MCP 연결이 필요하다. `.mcp.json`에 기본 선언이 포함되어 있으나,
정확한 엔드포인트와 인증 방식은 [Magnific MCP 공식 문서](https://docs.magnific.com/modelcontextprotocol)를 확인해 맞춰라.
Claude 데스크톱/웹에서 커넥터로 이미 Magnific을 연결했다면 `.mcp.json` 없이도 동작한다.

## 설계 원칙 (요약 — 상세는 DESIGN.md)

1. **단계당 정본 아티팩트 1개 = 계약.** JSON 스키마(`schemas/`)로 검증하고, 다음 단계는 그것만 신뢰한다.
2. **승인 게이트 + 비용 게이트.** `approved_by_user` 없이 다음 단계 진입 금지, `simulate_*` 견적 없이 실행 금지, 과금 경로는 실측(GUI/MCP가 다르다).
3. **파일시스템이 진리의 원천.** `.studio/<project>/`에 모든 상태 기록 → 어느 지점에서든 재개 가능.
4. **Spaces는 자연어로 조작한다.** `spaces_edit` 쿼리 → `spaces_state` 검증 루프 필수. 일괄 편집은 부분 반영될 수 있으니 전수 재확인.
5. **캐릭터 일관성 다중 방어**: static/dynamic 분리 → 3뷰 자산 → 참조 휴리스틱 → 심사 루프 → **키프레임에 없는 주체를 비디오 모델이 만들게 하지 않기**.
6. **Decision Log** — 모든 유의미한 선택을 기각 사유와 함께 append-only 기록.
7. **실패는 층위에서 고친다.** 클립 결함의 원인을 키프레임/프롬프트/모델로 분류하고 해당 층에서 수정 — 모델 승급은 마지막 수단.

## 실전 검증된 규칙 하이라이트 (v0.2.0)

- 무제한 플랜을 믿지 말고 실측: GUI 재생 0크레딧 vs MCP 실행 과금 (실행 2모드 — spaces-engineer)
- 복수 이동체 숏은 화면 기준 진행 방향 명시, 감정 비트는 medium 이상 + 최소 무브먼트 (storyboard-director)
- FLF 페어는 카메라 일치 검증, 불일치 시 FF-only 강등; 빈 첫 프레임에 주체 생성 금지 (production-director)
- 앱 UI/로고는 생성 대신 실측 스크린샷 원근 합성 (production-director)
- 씬 전환마다 이동/도착/매치컷 브리지 비트 검사 (storyboard-director)
- 헬멧 등 착용물은 머리카락 노출 경로 명시 (character-director)
- 클립 검수는 preview-grid 프레임 시트로, 재생 없이 (production-director)

## 후반 편집 규칙 하이라이트 (v0.3.0 — post-production-director)

- 후반 정본은 `edit_plan.json`(edit-as-data EDL) — 확정 후에만 렌더
- 디졸브 체인은 오프셋 누적 산식(`offset_k=Σd[0..k-1]−k·t`), 입력 정규화 필수
- 음악 싱크는 librosa 측정: 컷-비트 스냅 + RMS 빌드→서사 전환점 정렬
- 한글 자막은 libass(ASS `\k` 카라오케), Pretendard/Noto CJK, 릴스 세이프존 MarginV≈360
- 오디오는 클립 오디오 strip + (VO 시) 사이드체인 덕킹 + 2-pass loudnorm −14 LUFS
- 비율 파생은 크롭이 아니라 재구도 사다리(native>blur_pad>crop>auto_reframe)
- 납품 전 렌더-후 QC 하드 게이트(ffprobe + 4지점 프레임 자기검수)

## 크레딧과 라이선스

MIT. 설계는 [ViMax](https://github.com/hkuds/vimax)(MIT), [OpenMontage](https://github.com/calesthio/OpenMontage)(AGPLv3 — 아이디어만), [FilmAgent](https://github.com/HITsz-TMG/FilmAgent)의 비평-수정 루프, [MovieAgent](https://github.com/showlab/MovieAgent)의 계층 CoT 기획, [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)/[ShortGPT](https://github.com/RayVentura/ShortGPT)의 ffmpeg 후반 자동화·edit-as-data 패턴을 참고했다. v0.3.0 후반 심화는 [Remotion](https://remotion.dev)의 Caption 스키마(개념만, 커스텀 라이선스 — 코드 미사용), [WhisperX](https://github.com/m-bain/whisperX)(BSD-2)·[librosa](https://librosa.org)(ISC)·[MoviePy](https://github.com/Zulko/moviepy)(MIT)의 패턴을 라이선스 안전하게 재구현했다 — NOTICE.md 참조.
