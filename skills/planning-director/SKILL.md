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

`format-director` 스킬을 읽고, video_plan 결과의 열린 질문에 다음을 결합해 사용자에게 묻는다 (이미 답이 나온 항목은 다시 묻지 않는다):

- **format_profile** (cinematic_short / commercial_30 / shorts_reels / longform — format-director 표 참조) 및 파생 납품본 매트릭스
- **purpose** — brand(감정·기억 연결 극대화) 또는 activation(오퍼·CTA 중심). Binet&Field 60/40 기준으로 안내
- 목표 길이(초), 화면비(16:9 / 9:16 / 1:1) — 복수 비율이면 storyboard `aspect_variants`를 전제
- 시각 스타일 (cinematic / anime / 3D / 실사풍 등) + 피해야 할 요소
- 톤과 타깃 시청자
- **브랜드 자산 매니페스트** — 로고 파일(있으면 업로드 요청), 브랜드 컬러 hex, 슬로건, 보이스 규칙·금지어. 실물 UI/제품이 등장하면 스크린샷·에셋 확보(생성 재작화 금지 원칙)
- 예산 상한 (Magnific 크레딧; 모르면 `account_balance`로 잔액을 확인해 안내)

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

### Step 4 — 정본 아티팩트 확정

선택된 컨셉을 `schemas/project_brief.schema.json`에 맞춰 `project_brief.json`으로 저장한다. **스키마 필수 필드**: `format_profile`·`purpose`(required), 씬마다 `value_shift {from,to,mechanism}`(required — from==to면 비사건이므로 저장 전에 해소). 권장 필드: `brand_assets`(로고·컬러 hex·슬로건·보이스 규칙·금지어), `beat_map`(비트 백분율 배치 기록), `opening_image`/`final_image`(거울쌍). 산문 지시가 아니라 이 필드들이 하류 스테이지의 계약이다. 요약을 보여주고 승인받으면 `approved_by_user: true`, `stage_status: "approved"`로 갱신하고 다음 단계(/ms-characters)를 안내한다.
