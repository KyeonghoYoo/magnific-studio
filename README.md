# Magnific Studio

Magnific(구 Freepik) MCP의 **Spaces**를 실행 레이어로 쓰는 Claude Code 영상 제작 하네스 플러그인.
**기획 → 캐릭터 생성 → 콘티(스토리보드) → 영상 제작 → 후반 편집**을 단계별 승인 게이트와 비용 견적을 갖춘 파이프라인으로 실행한다.

v0.2.0은 실제 브랜드 프로모 1편(15숏/60초)을 이 파이프라인으로 완주하며 검증된 실전 규칙들을 반영했다 — 총 크레딧 소모 3으로.

**v0.3.0**은 후반 편집(/ms-post)을 대폭 심화했다: **edit-as-data 정본(`edit_plan.json`)** + 구체 ffmpeg 레시피(디졸브 오프셋 누적 산식·사이드체인 덕킹·2-pass loudnorm −14 LUFS)·**librosa 음악 싱크**(비트 스냅 + RMS 빌드→서사 정렬)·**libass 한글 카라오케 자막**(Pretendard/Noto CJK, 릴스 세이프존)·**9:16 재구도 사다리**(native>blur_pad>crop>auto_reframe)·**렌더-후 QC 하드 게이트**(ffprobe+프레임 자기검수). OSS 하네스(OpenMontage/Remotion/WhisperX/librosa/MoviePy)의 검증된 패턴을 라이선스 안전하게 재구현. **실전 2편(같은 프로젝트의 9:16 네이티브 릴스)**으로 이 후반 워크플로우를 검증하며 전환 `fade`·헤드 트림·엔드카드 홀드·loudnorm 재측정 보정·Space 아카이브 규칙을 도출했다(추가 크레딧 소모 0).

**v0.4.0**은 2026 OSS 벤치마크([BENCHMARKS.md](BENCHMARKS.md)) 로드맵 1순위인 **캐릭터 일관성 계약**을 반영했다: 캐릭터별 `reference_bank`(primary_ref·citation_ids·locked_seed·anchor_frames) + 전역 `consistency_policy`로, **캐릭터가 등장하는 모든 키프레임 생성은 뱅크 id 인용을 강제**하고(텍스트만으로 정체성 생성 금지) 인용 내역을 manifest `references_used`/`consistency_check`에 프로버넌스로 남긴다. 필드에서 일관성이 "희망"인 것과 달리 **계약으로 보장**한다.

**v0.5.0**은 로드맵 2순위인 **자동 자기검수 QA**(`quality-reviewer` 교차 스킬)를 반영했다: 키프레임·클립·최종 렌더를 승인 게이트 **전에** 축별(brand_fit·character_consistency·prompt_adherence·spatial_continuity·technical)로 자동 심사해 `review`(verdict+원인 층위+issues)를 아티팩트에 부착하고, **승인을 이진→증거 기반으로** 승격했다(review 없이 승인 요청 금지). OpenMontage의 렌더-후 자기검수를 재구현했으며, 심사는 프레임 읽기·추론이라 **무과금**이다.

**v0.6.0**은 로드맵 3순위인 **버전드·멱등 edit_plan**을 반영했다: `schema_version`·`pipeline_version` + 모든 인코딩 파라미터를 담은 `render` 블록으로 **동일 계획+소스 → 프레임 결정적 재렌더**를 보장하고, `source.clips` 지문으로 소스 변경을 탐지한다. `variants[]` 오버라이드(자막·음악·일부 트림)로 **생성 재소비 0의 A/B 다변형**을 뽑는다 — 카피 A/B 등을 클립 재생성 없이 렌더. 비용 거버넌스와 복리로 작동한다.

**v0.7.0**은 로드맵 4순위인 **콘티 숏 생성 전략**을 반영했다: 숏마다 `generation_strategy`(generative·stock·hybrid)를 두어, 캐릭터·브랜드 식별자가 없는 설정 롱숏·B롤·인서트는 **Magnific 스톡**(`stock_search`→`stock_to_creation`)으로 대체해 비용·시간을 아낀다. 히어로 숏(캐릭터·감정 비트)만 생성에 예산을 집중 — 비용 게이트 서사를 직접 강화한다.

**v0.8.0**은 로드맵 5순위인 **표준 후반 오디오 스택**을 반영했다: `audio.voiceover`로 내레이션을 `audio_tts`로 생성(보이스 선택+견적)하고, VO를 `WhisperX`로 강제정렬해 **워드 타이밍 카라오케 자막**(`captions[].word_timings`)을 자동 생성하며, VO 위에서 음악을 **사이드체인 덕킹**한다. 이로써 결과물이 "키프레임에 모션 붙인 것"이 아니라 **완성된 광고**가 된다. — 이로써 **2026 OSS 벤치마크 Adopt-now 로드맵 5/5를 완주**했다.

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

이 저장소는 단일 플러그인이자 마켓플레이스다(`.claude-plugin/marketplace.json` 포함). 목적에 맞게 셋 중 하나:

### A. 마켓플레이스로 설치 (팀 공유·버전 관리, 권장)

GitHub 등 원격에 올린 뒤 Claude Code에서:

```shell
/plugin marketplace add <github-user>/magnific-studio
/plugin install magnific-studio@riderly-marketplace
```

로컬 폴더를 바로 마켓플레이스로 써도 된다:

```shell
/plugin marketplace add /path/to/magnific-studio
/plugin install magnific-studio@riderly-marketplace
```

### B. 설치 없이 바로 테스트 (개발용)

```bash
claude --plugin-dir /path/to/magnific-studio
```

### C. 매 세션 자동 로드 (개인 상시 사용)

```bash
cp -R /path/to/magnific-studio ~/.claude/skills/
```

→ `magnific-studio@skills-dir`로 자동 로드된다.

> **커맨드는 네임스페이스된다**: `/ms-plan` → `/magnific-studio:ms-plan`, `/ms-post` → `/magnific-studio:ms-post` 등 (플러그인 간 충돌 방지). 변경 후에는 `/reload-plugins`.
>
> **Claude 데스크톱 앱(Cowork)**도 동일한 마켓플레이스 체계를 쓴다 — 플러그인 관리에서 마켓플레이스를 추가해 설치한다. 배포 전 검증은 `claude plugin validate /path/to/magnific-studio`.

### Magnific MCP 연결

`.mcp.json`에 Magnific MCP 서버 선언이 포함되어 있어 플러그인 설치 시 자동 등록된다.
정확한 엔드포인트·인증은 [Magnific MCP 공식 문서](https://docs.magnific.com/modelcontextprotocol)를 확인해 맞춘다.
Claude 데스크톱/웹에서 커넥터로 이미 Magnific을 연결했다면 `.mcp.json` 없이도 동작한다(중복 시 `.mcp.json` 제거).

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
- 완성본은 Space에 최종본 노드 + 편집 레시피 텍스트 노드로 아카이브(기록처 단일화)

## 실전 2편(9:16 네이티브 릴스) 도출 규칙 (v0.3.0)

- 전환은 `fade`(크로스디졸브) 우선 — ffmpeg `dissolve`는 노이즈 디더라 생성 클립에서 지지직거림
- 생성(I2V) 클립은 첫 0.3~0.5초 색감 전환을 헤드 트림으로 제거
- 엔드카드/로고는 클립 끝에서 정착 → `freeze_tail`로 홀드 연장, 이미 베이크된 슬로건은 자막 재오버레이 금지
- 단일 loudnorm 언더슈트 → `ebur128` 재측정 후 `volume` 보정으로 −14 LUFS 정착
- 한글 카피는 세로 폭 한 줄 여부를 QC 프레임에서 확인

## 벤치마크 (경쟁 OSS 대비)

상세 비교·평가는 [BENCHMARKS.md](BENCHMARKS.md). 요지: 최대 경쟁자 **OpenMontage**(AGPL, 디렉터-스킬+체크포인트+승인)와 철학은 같으나, 본 플러그인의 방어점은 **① 타입드 JSON 스테이지 계약 ② 비용 게이트(이 분야에서 유일) ③ 감사 가능한 Decision Log ④ 큐레이션된 단일 백엔드(Magnific) 품질 + 관대한 라이선스**. 최다 star는 MoneyPrinterTurbo(~60k, MIT)지만 스톡 몽타주라 캐릭터 브랜드 광고와는 결이 다르다.

## 크레딧과 라이선스

MIT. 설계는 [ViMax](https://github.com/hkuds/vimax)(MIT), [OpenMontage](https://github.com/calesthio/OpenMontage)(AGPLv3 — 아이디어만), [FilmAgent](https://github.com/HITsz-TMG/FilmAgent)의 비평-수정 루프, [MovieAgent](https://github.com/showlab/MovieAgent)의 계층 CoT 기획, [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)/[ShortGPT](https://github.com/RayVentura/ShortGPT)의 ffmpeg 후반 자동화·edit-as-data 패턴을 참고했다. v0.3.0 후반 심화는 [Remotion](https://remotion.dev)의 Caption 스키마(개념만, 커스텀 라이선스 — 코드 미사용), [WhisperX](https://github.com/m-bain/whisperX)(BSD-2)·[librosa](https://librosa.org)(ISC)·[MoviePy](https://github.com/Zulko/moviepy)(MIT)의 패턴을 라이선스 안전하게 재구현했다 — NOTICE.md 참조.
