---
name: magnific-studio-quickstart
description: "Magnific Studio 5단계 워크플로 진입점·안내. Use when: 어떤 디렉터 스킬을 언제 쓸지 모를 때, 전체 영상 제작 파이프라인 개요가 필요할 때, Desktop에서 무엇이 되고 안 되는지 확인할 때."
---

# Magnific Studio — Quick Start (Claude Desktop 진입점)

Claude Code 플러그인 `magnific-studio`를 Claude Desktop으로 옮긴 스킬 세트의 안내다.
Desktop에는 **슬래시 커맨드(`/ms-*`)가 없으므로**, 아래 스테이지에 맞는 **디렉터 스킬을 직접 지시**해서 진행한다.

## 5단계 파이프라인

| 스테이지 | 사용할 스킬 | 정본 아티팩트 |
|---|---|---|
| 0. 횡단 규칙(항상 먼저) | `magnific-studio-core` | — |
| 1. 기획 | `planning-director` | `project_brief.json` |
| 2. 캐릭터 | `character-director` | `characters.json` + Library 자산 |
| 3. 콘티 | `storyboard-director` | `storyboard.json` |
| 4. 영상 제작 | `production-director` (+ `spaces-engineer`) | `production_manifest.json` |
| 5. 후반 편집 | `post-production-director` | `edit_plan.json` (+ 렌더는 Claude Code) |
| 심사(각 게이트) | `quality-reviewer` | `review` 객체 |

## 사용 방법

1. 먼저 "magnific-studio-core 규칙을 따라 진행해줘"라고 지시해 횡단 규칙을 로드한다.
2. 스테이지 순서대로 해당 디렉터 스킬을 지시한다. 예: "planning-director로 이 아이디어를 기획해줘".
3. 각 생성 게이트 전에 `quality-reviewer`로 자기검수하고 승인한다.
4. 생성 실행은 **Magnific 커넥터(MCP)** 도구로 이뤄진다 — Desktop 설정에서 커넥터가 연결돼 있어야 한다.

## Desktop 제약 (반드시 인지)

- **후반 렌더링 불가**: `post-production-director`는 Desktop에서 `edit_plan.json` **계획 수립까지**만 한다. 실제 ffmpeg/librosa/WhisperX 렌더는 Desktop 코드 실행 환경에 없으므로 **Claude Code에서 실행**한다.
- **슬래시 커맨드 없음**: `/ms-plan` 등은 Claude Code 전용. Desktop에서는 스킬 이름으로 지시한다.
- **네트워크는 커넥터 경유**: 외부 API는 스킬 코드에서 직접 호출하지 말고 Magnific 커넥터(MCP) 도구로 호출한다.

전체 파이프라인(기획→납품 렌더까지)을 끊김 없이 돌리려면 **Claude Code** 사용을 권장한다.
