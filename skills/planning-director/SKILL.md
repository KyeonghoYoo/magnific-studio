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

video_plan 결과의 열린 질문에 다음을 결합해 사용자에게 묻는다 (이미 답이 나온 항목은 다시 묻지 않는다):

- 목표 길이(초), 화면비(16:9 / 9:16 / 1:1)
- 시각 스타일 (cinematic / anime / 3D / 실사풍 등) + 피해야 할 요소
- 톤과 타깃 시청자
- 예산 상한 (Magnific 크레딧; 모르면 `account_balance`로 잔액을 확인해 안내)

### Step 3 — 컨셉 2~3안

로그라인 + 시놉시스(3~5문장) + 씬 구성 개요 + 예상 숏 수 + 대략 비용 규모로 컨셉을 2~3안 제시하고 선택받는다. 채택/기각을 decision_log에 기록한다.

## 작법 규칙

- **Show, don't tell**: "그는 매우 화가 났다"가 아니라 "그는 주먹을 쥐었고, 손톱이 손바닥을 파고들었다"처럼 시각화 가능한 행동으로 쓴다.
- 씬 개요의 환경은 slugline 형식으로 명확히: `INT. COFFEE SHOP - NIGHT`.
- 민감 요소는 대체물로 치환해 생성 거부를 예방한다 (예: 피 → 케첩, 무기 클로즈업 회피).
- 전체 길이가 15초를 넘으면 씬/숏 분할이 클립 단위(모델 최대 길이)와 맞아떨어지도록 video_plan의 분할 계획을 따른다.

### Step 4 — 정본 아티팩트 확정

선택된 컨셉을 `schemas/project_brief.schema.json`에 맞춰 `project_brief.json`으로 저장한다. 요약을 보여주고 승인받으면 `approved_by_user: true`, `stage_status: "approved"`로 갱신하고 다음 단계(/ms-characters)를 안내한다.
