---
name: quality-reviewer
description: |
  교차 스킬 — 생성 산출물의 자동 자기검수(QA). Use when: (1) 키프레임/클립/최종 렌더를 승인 게이트에 올리기 직전, (2) production-director·post-production-director가 심사를 요청할 때, (3) 승인을 "증거 기반"으로 만들 때. 산출물: review 객체(축별 점수 + verdict + issues + 원인 층위)를 정본 아티팩트에 부착.
---

# Quality Reviewer — 자동 자기검수 (증거 기반 승인)

먼저 `magnific-studio-core`를 읽었는지 확인한다. 이 스킬은 특정 스테이지 전용이 아니라 **모든 생성 게이트에 붙는 심사 계층**이다(OpenMontage의 렌더-후 자기검수 패턴을 재구현 — 코드 미복사).

## 원칙 — 승인은 증거로 한다

Magnific Studio의 승인 게이트는 이진(예/아니오)이 아니라 **증거 기반**이다: 사용자에게 승인을 요청하기 전에 산출물을 자동 심사해 **점수·이슈·원인 층위**를 `review`로 남기고, 그 요약을 게이트에서 함께 제시한다. 사용자는 "감"이 아니라 근거를 보고 판단한다. 심사는 생성이 아니므로 **크레딧 0**(프레임 읽기·추론).

## 심사 방식 (재생 없이 프레임 기반)

- **키프레임(이미지)** — 이미지를 직접 읽어 판단.
- **클립(영상)** — `creations_get`의 **preview-grid**(≈50프레임 시트) + start/end frame으로 프레임 단위 판단(재생 불필요).
- **최종 렌더** — 4지점(0%/33%/66%/95%) 프레임 추출 + `ffprobe`(길이·해상도·오디오·라우드니스) — post-production-director의 QC와 동일.
- **배치가 크면 서브에이전트(Task)에 위임**해 병렬 심사하고 결과만 회수한다. 위임해도 크레딧 0.

## 루브릭 (축 · 각 pass/revise/fail)

| 축 | 본다 | 근거 |
|---|---|---|
| **brand_fit** | 브랜드 보이스·금지어·색/톤이 project_brief.style을 지키는가 | 브랜드 정합 |
| **character_consistency** | 이목구비·체형·헤어가 `reference_bank`/시트와 일치하는가 | 캐릭터 계약(core 규칙 5) |
| **prompt_adherence** | first_frame_desc/motion_desc가 실제로 구현됐는가 | 묘사 정확성 |
| **spatial_continuity** | 인물 배치(좌/우)·구도가 인접 숏과 모순 없는가 | 공간 연속성 |
| **technical** | 워핑·텔레포트·블랙프레임·자막 오탈자·경계 아티팩트가 없는가 | 기술 결함 |
| **lighting_continuity** | 씬 조명 계약(scenes[].lighting — 키 방향·질감·비율·색온도)이 씬 전 숏에서 유지되는가 | filmcraft #1 AI 실패 축 |
| **motion_quality** | easing(등속 부유 없음)·moving hold(마네킹 정지 없음)·follow-through·무게(임팩트+settle)·gesture economy(동작 ≤2) | filmcraft/animation-motion.md 결함→수정 표 |
| **flf_adherence** | (FLF 클립) 마지막 프레임이 공급한 LF와 일치하는가 — SSIM/pHash 대조. 미달=서빙 경로가 LF 무시 | 기계 검증 |
| **grammar** | shot_size·angle·movement·screen_direction이 콘티 값과 일치하고 visual_grammar 계약(무브 규칙·룩·팔레트)을 지키는가. 이동 무브가 시차 없이 렌더되면(=줌으로) prompt_adherence FAIL | filmcraft 통제 어휘 |

최종 렌더는 여기에 **loudness(-14 LUFS 근사)·safe_zone·caption_present·dynamics(LRA<4LU warn — cinematic/longform/brand만)·sfx_coverage(가시 임팩트·보행에 music-only=fail)·color_consistency**를 추가한다.

**pre-flight lint(생성 전, 0크레딧)** — 심사보다 앞선 방어선: 빈 토큰 블록리스트(masterpiece/8k/artstation…), 부정 구문(no/without+명사 → 긍정 재구성), hex/비율 숫자 프롬프트 유입, 이동 무브의 foreground_anchor 부재, 씬 조명 문장 byte-identity. 위반 프롬프트는 실행 전에 반려한다(filmcraft/references/prompting.md 체크리스트).

## 시점·공간 정합 축 (키프레임 필수 — 파일럿 1 실증 2건)

- `pov_integrity` — POV/1인칭 숏에서 시점 주체의 신체가 모순되게 보이는가(자기 헬멧·뒤통수가 프레임 과점 = 3인칭 오염). "seen from X's helmet"류 시점 서술은 모델이 "X의 헬멧을 그려라"로 오독한다 — 프레임 요소를 직접 열거하는 서술("the view directly over the handlebar and mirrors")이 정본.
- `traffic_grammar` — 차량·바이크의 차선 위치·통행 방향·교통 규칙 정합(중앙선 밟기, 역주행처럼 읽히는 배치). 콘티 `axis.a_side`가 프롬프트에 실제로 투영됐는지 대조한다 — axis에 적고 프롬프트에 안 옮기면 잡히지 않는다.

## verdict와 원인 층위

- 어느 축이든 `fail`이면 전체 verdict는 `revise`(수정 가능) 또는 `fail`(폐기). 전 축 `pass`면 `pass`.
- `revise`/`fail`에는 **원인 층위**를 붙인다: `keyframe`(키프레임 결함) / `prompt`(프롬프트 모호) / `model`(모델 한계) / `edit`(후반 처리). 해당 층에서 고친다 — 키프레임 결함을 프롬프트·모델 승급으로 때우면 반복 실패(실증).
- 재생성으로 못 고치는 **생성 클립 고유 특성**(도입 색감 전환·엔드카드 정착·베이크 텍스트)은 결함이 아니라 `edit` 층위로 표시해 후반(Step 3b)으로 넘긴다.

## review 아티팩트 형태

키프레임/클립 심사는 `production_manifest`의 해당 숏 `review`에, 최종 렌더는 `edit_plan.qc`에 기록한다:

```jsonc
"review": {
  "keyframe": {
    "axes": { "brand_fit": "pass", "character_consistency": "pass",
              "prompt_adherence": "revise", "spatial_continuity": "pass", "technical": "pass" },
    "verdict": "revise",
    "cause_layer": "prompt",
    "issues": ["first_frame_desc의 '노을' 톤이 약함 — 프롬프트에 시간대 명시"],
    "reviewed_by": "agent"        // agent(자동) | user(사용자 확인)
  },
  "clip": { "...": "..." }
}
```

`consistency_check`(pass/fail/na)는 이 review의 `character_consistency` 축을 빠르게 요약한 필드다 — review가 있으면 그로부터 채운다.

## 게이트 연결

1. 생성(키프레임/클립/렌더) 후, 승인 요청 **전에** 이 스킬로 자동 심사한다.
2. `review`를 아티팩트에 기록하고, **게이트에서 요약(축 점수 + 이슈 + 원인 층위)을 사용자에게 제시**한다.
3. verdict가 `revise`/`fail`이면 원인 층위에서 수정 후 재심사(루프). `pass`만 승인 후보로 올린다.
4. 자동 심사와 사용자 최종 판단은 별개다 — 자동은 `reviewed_by: agent`, 사용자가 확인하면 `user`로 승격.

## 하드 룰

1. **증거 없는 승인 요청 금지**: 생성 스테이지는 `review` 없이 승인 게이트를 올리지 않는다.
2. **심사는 무과금**: 프레임 읽기·추론·서브에이전트 위임 모두 크레딧 0 — 견적 불필요.
3. **원인 층위 필수**: revise/fail은 반드시 층위를 분류해 올바른 스테이지에서 고친다.
