# 릴리스 가이드 — 두 채널 업데이트 워크플로

`magnific-studio`는 **두 채널**로 배포된다. 채널마다 업데이트 방식이 다르니 릴리스마다 아래를 그대로 따른다.

| 채널 | 업데이트 방식 | 자동? |
|---|---|:---:|
| **Claude Code** (플러그인) | 마켓플레이스 갱신 + 플러그인 업데이트 | 조건부 (버전 bump + autoUpdate 시) |
| **Claude Desktop** (스킬) | `.zip` 재빌드 후 수동 재업로드 | ❌ (계정별 수동) |

---

## ⚠️ 두 가지 함정 (먼저 읽기)

1. **버전을 올리지 않으면 Claude Code는 업데이트되지 않는다.**
   이 플러그인은 명시적 버전(`plugin.json`·`marketplace.json`의 `version`)을 쓴다. 코드를 아무리 푸시해도 버전 숫자가 그대로면 캐시(`~/.claude/plugins/cache/riderly-marketplace/magnific-studio/<version>/`)가 유지돼 업데이트가 잡히지 않는다. **플러그인 런타임(skills/·commands/·schemas/·.mcp.json)을 고쳤다면 반드시 버전 bump.**

2. **Desktop 스킬은 GitHub와 연결이 없다.**
   업로드한 스킬은 정적 스냅샷이다. 저장소를 고쳐도 자동으로 바뀌지 않는다. **스킬 본문을 고쳤다면 재빌드 + 재업로드**해야 하고, 팀원이 있으면 **각자** 다시 올려야 한다.

> 문서(README 등)나 `desktop/` 툴링만 고쳤다면 플러그인 런타임이 아니므로 버전 bump·Desktop 재업로드 모두 불필요하다.

---

## 릴리스 절차

### 1. 변경 + (필요 시) 버전 bump

- `skills/` · `commands/` · `schemas/` · `.mcp.json` 중 하나라도 고쳤으면 **버전 bump**:
  - `.claude-plugin/plugin.json`의 `version`
  - `.claude-plugin/marketplace.json`의 해당 플러그인 `version`
  - (두 곳을 반드시 일치시킨다)
- 시맨틱 버저닝 권장: 버그픽스 `x.y.Z`, 기능 추가 `x.Y.0`, 파괴적 변경 `X.0.0`.

### 2. 커밋 + 푸시

```bash
git add -A
git commit -m "magnific-studio vX.Y.Z — <요약>"
git push origin master
```

### 3. Claude Code 채널 반영

**자동으로 하려면** — 소비하는 프로젝트의 `.claude/settings.json` 또는 전역 `~/.claude/settings.json`에 `autoUpdate: true`를 넣는다. 템플릿: [`.claude/settings.example.json`](.claude/settings.example.json). 적용 시 **다음 Claude Code 시작 때** 마켓플레이스 갱신 + 플러그인 업데이트가 자동으로 일어난다(세션 중이 아니라 시작 시점, 그리고 버전이 올랐을 때만).

**수동으로 하려면** — 실행 중인 세션에서:

```
/plugin marketplace update riderly-marketplace
/plugin update magnific-studio@riderly-marketplace
/reload-plugins
```

- 1줄: 마켓플레이스 메타데이터(최신 버전 카탈로그) 갱신
- 2줄: 설치된 플러그인을 최신 버전으로 업데이트
- 3줄: 현재 세션에 즉시 반영 (다음 세션부터는 시작 시 자동 로드)

### 4. Claude Desktop 채널 반영 (스킬 본문을 고쳤을 때만)

```bash
python3 desktop/build.py
```

- `skills/` 원본을 복사해 `description`을 200자 이내로 리라이트하고 `desktop/dist/*.zip`으로 패키징한다.
- **바뀐 zip만 표시**된다(`CHANGED`/`NEW`/`unchanged`). 표시된 것만 재업로드하면 된다.
- [claude.ai/customize/skills](https://claude.ai/customize/skills)에서 해당 스킬을 **삭제 후 재업로드**(덮어쓰기). 팀원은 각자 반복.

---

## 버전·description 규율

- **버전 일치**: `plugin.json`과 `marketplace.json`의 `version`은 항상 같아야 한다.
- **Desktop description ≤ 200자**: claude.ai 업로드는 `description`을 200자로 제한한다(API/스펙은 1024자). `build.py`가 빌드 시 이를 **검증하고 초과 시 실패**시킨다. 스킬의 `description`을 늘렸다면 `build.py`를 돌려 통과하는지 확인한다.
- **name 규칙**: 소문자·숫자·하이픈만, 64자 이내, 예약어(`claude`/`anthropic`)·XML 태그 금지.
- **원본 vs Desktop 사본**: `skills/`는 Claude Code용 전체 버전(그대로 유지), Desktop 축약본은 `build.py`가 매번 재생성한다 — Desktop용 사본을 손으로 수정하지 않는다.

---

## 요약 체크리스트

- [ ] 런타임 변경이면 `plugin.json` + `marketplace.json` 버전 bump (일치)
- [ ] `git commit` + `git push origin master`
- [ ] Claude Code: autoUpdate(자동) 또는 `/plugin marketplace update` → `/plugin update` → `/reload-plugins`(수동)
- [ ] Desktop(스킬 본문 변경 시): `python3 desktop/build.py` → `CHANGED`/`NEW` zip만 재업로드
