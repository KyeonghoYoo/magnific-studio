---
name: character-director
description: |
  캐릭터 생성 스테이지 디렉터. Use when: (1) /ms-characters 실행, (2) 캐릭터 시트/외모 확정/Library 자산 등록 작업, (3) characters.json을 만들거나 수정할 때. 산출물: characters.json + Magnific Library 캐릭터 자산.
---

# Character Director — 캐릭터 생성

먼저 `magnific-studio-core` 스킬을 읽었는지 확인한다. 입력: 승인된 `project_brief.json`.

## 캐릭터 기술 원칙 (static/dynamic 분리)

캐릭터마다 두 층으로 특징을 기술한다:

- **static_features** — 이야기 내내 변하지 않는 것: 성별, 나이대, 인종/피부톤, 얼굴 특징(눈/코/입/윤곽), 체형, 헤어(색·길이·스타일). 캐릭터 동일성의 근거.
- **dynamic_features** — 씬에 따라 바뀔 수 있는 것: 의상, 소품, 상처/오염 등 상태.

이 분리가 중요한 이유: 이후 모든 프레임 생성에서 static은 절대 보존, dynamic은 씬 지시에 따라 교체되기 때문이다.

## 절차

### Step 1 — 캐릭터 목록과 시트 초안

project_brief의 씬 개요에서 시각적으로 등장하는 캐릭터를 추출하고, 캐릭터별 static/dynamic 특징 시트를 작성해 사용자와 확정한다. 씬을 넘나드는 동일 인물은 하나로 병합하되, 외모가 크게 달라지면(아역→성인 등) 별도 캐릭터로 분리한다.

### Step 2 — 기준 이미지 생성 (비용 게이트 통과 후)

캐릭터마다 **정면(front) 기준 이미지**를 T2I로 생성한다. 프롬프트 규칙:

- `static_features + 기본 dynamic_features + project_brief.style` 결합
- **순백 배경, 전신, 화면 중앙, 팔은 자연스럽게 내린 정규 포즈** 강제 — 이후 참조 이미지로 쓰기 좋은 형태
- 후보 2~3장 variation 생성 후 사용자에게 보여 선택받는다 (`creations_show`로 인라인 표시)

정면이 확정되면 정면 이미지를 참조로 **측면(side)·후면(back)**을 편집 생성한다 ("같은 인물, 같은 의상, 카메라만 90도/180도" 지시).

### Step 3 — Library 자산 등록

확정된 3뷰 이미지로 `library_create`를 호출해 캐릭터를 Magnific Library 자산으로 등록한다 (type: character, 이름과 static_features 요약을 description에). 이후 스테이지는 이 Library identifier를 `images_generate`/`video_generate`의 reference로 네이티브 참조한다. 기존 자산 수정은 `library_edit`로 하고, 절대 중복 `library_create`하지 않는다.

### Step 4 — 정본 아티팩트 확정

`characters.json`에 기록: 캐릭터 키(slug), 이름, static/dynamic features, library identifier, 3뷰 creation identifier, 대표 이미지 webUrl. 사용자 승인 후 `approved_by_user: true`.

## 프롬프트 함정 (실증 사례)

- **착용물 + 머리카락**: 헬멧·모자를 쓰는 캐릭터는 머리카락의 노출 경로를 명시한다 — "ponytail under a helmet"류는 헬멧 위 묶음머리로 그려진다. 올바른 기술: "헬멧이 정수리를 완전히 덮고, 머리는 헬멧 뒷단 아래 목덜미로 내려옴, 헬멧 위 머리/번 금지".
- **실물 제품/앱 UI**: 화면·로고·패키지가 식별 가능하게 등장하면 사용자에게 실제 스크린샷/에셋 업로드를 요청해 참조로 배선한다. 생성 모델의 UI 재작화는 브랜드 정합이 깨진다. 로고는 `images_remove_background`로 배경 제거 후 참조.
- **동시 다중 스크린 참조 금지**: 여러 앱 화면을 한 노드에 참조하면 화면이 섞인다 — 숏당 가장 상징적인 1장만.

## 품질 심사 기준 (variation 선택 시)

1. **캐릭터 일관성**: 성별·나이·이목구비·체형·헤어가 시트와 일치하는가
2. **참조 적합성**: 배경이 깨끗하고 포즈가 정규인가, 테두리/프레임/워터마크성 요소가 없는가
3. **스타일 일치**: project_brief.style과 맞는가
