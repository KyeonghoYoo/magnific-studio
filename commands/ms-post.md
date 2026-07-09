---
description: "5단계 후반 편집 — 트리밍/트랜지션/음악/자막/파생본(릴스)까지 ffmpeg 기반 마감"
argument-hint: "[프로젝트 슬러그 (생략 시 자동 탐색)]"
---

Magnific Studio 파이프라인의 **후반 편집** 스테이지를 실행한다.

1. `magnific-studio-core` 스킬을 읽는다.
2. 대상 프로젝트: $ARGUMENTS (생략 시 `.studio/`에서 탐색)
3. **게이트 확인**: `production_manifest.json`에 숏 클립들이 succeeded 상태여야 한다. 아니면 중단하고 /ms-produce를 안내한다.
4. `post-production-director` 스킬을 읽고 절차를 따른다. 정본은 `edit_plan.json`(edit-as-data EDL, `schemas/edit_plan.schema.json`) — 이를 사용자 확정한 뒤에만 최종 렌더한다.
5. **하드 룰**: `audio_music_generate`/`video_upscale` 등 크레딧 소모 실행 전 견적 + 승인. 업스케일은 편집 확정 후 최종본에만. 납품 전 **자동 검수(QC) 게이트** 통과 필수(ffprobe + 4지점 프레임 육안 점검).
6. **Magnific 아카이브**: QC 통과한 납품본을 Space에 업로드(최종본 노드 + 편집 레시피 텍스트 노드)해 Space를 단일 기록처로 만든다(post-production-director Step 6).

산출물: `edit_plan.json` + 최종 납품 파일(마스터 + 파생본) + Space 아카이브 노드 + `production_manifest.json` 갱신.
