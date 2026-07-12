---
name: planning-director
description: |
  기획 스테이지 디렉터. Use when: (1) /ms-plan 실행, (2) 사용자가 영상 아이디어를 주고 기획/컨셉을 요청할 때, (3) project_brief.json을 만들거나 수정할 때. 산출물: project_brief.json.
---

# Planning Director — 기획

먼저 `magnific-studio-core` 스킬을 읽었는지 확인한다.

## 절차

### Step 1 — 아이디어 접수와 video_plan

사용자 아이디어를 받으면 **가장 먼저 Magnific `video_plan` 툴을 호출**한다 (아이디어 원문을 verbatim으로 전달, 알고 있는 duration/aspect/style 힌트 포함). 이 툴은 브리프 초안, 열린 질문, 준비할 캐릭터 목록, 추천 모델, 15초 초과 시 멀티클립 분할 계획을 반환한다 — 이것이 기획의 뼈대다.

### Step 2 — 기획 문답

`format-director` 스킬과 `filmcraft/references/story-structure.md`·`emotion-recipes.md`를 읽고, video_plan 결과의 열린 질문에 다음을 결합해 사용자에게 묻는다 (이미 답이 나온 항목은 다시 묻지 않는다):

- **format_profile** (cinematic_short / commercial_30 / shorts_reels / longform — format-director 표 참조) 및 파생 납품본 매트릭스
- **purpose** — brand(감정·기억 연결 극대화) 또는 activation(오퍼·CTA 중심). Binet&Field 60/40 기준으로 안내
- 목표 길이(초), 화면비(16:9 / 9:16 / 1:1) — 복수 비율이면 storyboard `aspect_variants`를 전제
- 시각 스타일 (cinematic / anime / 3D / 실사풍 등) + 피해야 할 요소
- 톤과 타깃 시청자
- **브랜드 자산 매니페스트** — 로고 파일(있으면 업로드 요청), 브랜드 컬러 hex, 슬로건, 보이스 규칙·금지어. 실물 UI/제품이 등장하면 스크린샷·에셋 확보(생성 재작화 금지 원칙)
- 예산 상한 (Magnific 크레딧; 모르면 `account_balance`로 잔액을 확인해 안내)
- **Library 인벤토리**: `library_list`로 기존 자산(character/style/locations/color)을 확인해 재사용 후보를 브리프에 기록한다 — 같은 브랜드의 후속 캠페인이면 style/color 자산과 캐릭터가 이미 있을 수 있다(core 자산 계층 룰 1)

### Step 3 — 컨셉 2~3안

로그라인 + 시놉시스(3~5문장) + 씬 구성 개요 + 예상 숏 수 + 대략 비용 규모로 컨셉을 2~3안 제시하고 선택받는다. 채택/기각을 decision_log에 기록한다.

## 작법 규칙

- **Show, don't tell**: "그는 매우 화가 났다"가 아니라 "그는 주먹을 쥐었고, 손톱이 손바닥을 파고들었다"처럼 시각화 가능한 행동으로 쓴다.
- **비트 배치는 백분율로**: format_profile의 비트 구조(Save the Cat 축약 또는 훅-바디-CTA)를 러닝타임 백분율로 배치하고, 씬 개요가 비트를 커버하는지 검증한다. 첫 씬과 끝 씬은 변화 전/후의 거울쌍으로 설계한다.
- **씬마다 가치전환**: 각 씬 요약에 "무엇이 +→− 또는 −→+로 뒤집히는가"를 한 줄로 명시한다(McKee). 뒤집히는 게 없으면 그 씬을 빼거나 병합한다.
- 씬 개요의 환경은 slugline 형식으로 명확히: `INT. COFFEE SHOP - NIGHT`.
- 민감 요소는 대체물로 치환해 생성 거부를 예방한다 (예: 피 → 케첩, 무기 클로즈업 회피).
- 전체 길이가 15초를 넘으면 씬/숏 분할이 클립 단위(모델 최대 길이)와 맞아떨어지도록 video_plan의 분할 계획을 따른다.
- **2-티어 렌더 전략(대형 프로젝트)**: 총 숏이 많거나(20+) 예산이 민감하면, 저비용 모델·저해상도로 전 숏 애니메틱(러프 클립)을 먼저 만들어 편집 승인 후 승인 숏만 상위 품질로 최종 생성하는 계획을 브리프에 명시한다.

### Step 3.4 — 자산화 검토 (Library-first)

visual_grammar를 확정하면서 재사용 가능성을 검토한다: 팔레트가 브랜드 표준이면 `color` 자산으로, look이 스타일 포토/LoRA로 잠글 수 있으면 `style` 자산으로 등록을 제안한다(등록은 사용자 동의 시). `brandKitId`/`templateSlug`는 sqid를 이미 알 때만 — 대응 list 도구가 MCP 표면에 없다(core 룰 4).

### Step 3.5 — Visual Grammar Contract (시각 문법 계약) ★ v1.1 신규

컨셉이 정해지면 **감독의 스타일 바이블**을 계약으로 확정한다 — 실제 프로덕션에서 DP·감독이 "이 영화는 35mm, 느린 push-in만, 나트륨 팔레트"처럼 룩을 잠그는 것과 같다. `visual_grammar`(required)를 filmcraft 사전 값으로 채운다:

- **palette**(dominant/subordinate/accent + harmony + 금지색) 및 `color_script`(비트별 채도·온도 아크 — 예: 저점을 향해 탈색, 해방에서 채도 복귀), `location_palettes`
- **lighting_bible** — 기본 ratio(대비 클래스)·색온도·시간대·**motivation_doctrine**(motivated 기본)
- **lens_bible** — 사이즈 계열별 기본 mm(FF 환산)·기본 조리개·기본 심도
- **look** — film_stock(포트라/씨네스틸/알렉사…)·lens_character(구면/아나모픽/빈티지)·grain·diffusion — 구체 기술 명사가 최강 토큰이다("cinematic" 같은 추상어는 단독 금지)
- **camera_bible** — 기본 support·settle 필수·movement_rules(1무브 법칙 + 프로젝트 금지 무브)
- **prohibitions** — 상업물이면 greeking_required(브랜드 마크는 실물 합성만), flop_forbidden, baked_text_forbidden

감정 톤이 정해진 프로젝트는 `emotion-recipes.md`의 부서 합의 레시피에서 기본값을 가져온다. 이 계약은 콘티(씬 조명·무브 선택)→프롬프트 프로젝션→심사(grammar 축)까지 전 하류가 상속한다 — **프로젝트 단위 스타일 메모리의 실체**다.

### Step 4 — 정본 아티팩트 확정

선택된 컨셉을 `schemas/project_brief.schema.json`에 맞춰 `project_brief.json`으로 저장한다. **스키마 필수 필드**: `format_profile`·`purpose`·`visual_grammar`(required), 씬마다 `value_shift {from,to,mechanism}`(required — from==to면 비사건이므로 저장 전에 해소). **가치전환 체이닝**: 인접 씬의 극성은 종류가 다르고 진폭은 미드포인트까지 상승해야 한다(플랫라인 방지 — story-structure.md). 권장 필드: `brand_assets`(로고·컬러 hex·슬로건·보이스 규칙·금지어 — hex는 프롬프트가 아니라 LUT·참조 이미지로만 쓰인다), `beat_map`(백분율 배치; 비트↔숏 매핑 고아 검증 — 모든 비트는 ≥1 숏), `opening_image`/`final_image`(거울쌍). 산문 지시가 아니라 이 필드들이 하류 스테이지의 계약이다. 요약을 보여주고 승인받으면 `approved_by_user: true`, `stage_status: "approved"`로 갱신하고 다음 단계(/ms-characters)를 안내한다.
