# Magnific Studio — 설치 가이드 (Claude Code · Claude Desktop)

이 플러그인은 두 환경에 설치할 수 있다. **완전한 5단계 파이프라인(기획→납품 렌더)은 Claude Code**가 정답이고, **Claude Desktop은 기획·캐릭터·콘티·심사까지의 서브셋**이다(후반 ffmpeg 렌더는 Desktop 코드 실행 환경에 없다).

---

## A. Claude Code (권장 — 전체 기능)

플러그인 전체(커맨드 7 + 스킬 8 + Magnific MCP)가 그대로 작동한다.

### 설치

Claude Code 세션에서:

```
/plugin marketplace add KyeonghoYoo/magnific-studio
/plugin install magnific-studio@riderly-marketplace
```

- 1줄: GitHub 저장소를 마켓플레이스로 등록 (마켓플레이스 이름 `riderly-marketplace`)
- 2줄: 플러그인 설치 — 슬래시 커맨드, 스킬, 번들된 Magnific MCP(`.mcp.json`)가 자동 등록된다

### (선택) 프로젝트/전역 자동 활성화

프로젝트 공유용은 `.claude/settings.json`, 전역은 `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "riderly-marketplace": {
      "source": { "source": "github", "repo": "KyeonghoYoo/magnific-studio" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": {
    "magnific-studio@riderly-marketplace": true
  }
}
```

### 사용

```
/ms-plan  →  /ms-characters  →  /ms-storyboard  →  /ms-produce  →  /ms-post
/ms-pipeline (전체 자동)   /ms-status (진행 상황)
```

---

## B. Claude Desktop / Cowork (서브셋 — 스킬 + 커넥터)

Claude Desktop은 Claude Code 플러그인 포맷을 지원하지 않는다. 대신 **커스텀 Skill 업로드**와 **커스텀 커넥터**로 이식한다. 스킬 실행(코드 실행)은 Desktop의 **Cowork**(에이전트 실행 모드)에서 이뤄진다.

### 사전 조건

- 플랜: Pro / Max / Team / Enterprise (Free는 사전 제작 스킬만)
- **코드 실행(Code execution) 활성화 필수** — 이게 켜져야 Skills 설정이 나타난다
- 스킬은 **계정 단위 개인 설정**이라, 팀원은 각자 업로드해야 한다(조직 일괄 배포 불가)

### 1) Magnific 커넥터 추가

**설정 → 커넥터 → 커스텀 커넥터(원격)**
- URL: `https://mcp.magnific.com/mcp`
- 이름: `Magnific`

스킬은 이 커넥터의 MCP 도구를 호출한다. 외부 API는 스킬 코드에서 직접 호출하지 말고 커넥터를 경유한다(Desktop 스킬 네트워크 접근은 가변).

### 2) 스킬 .zip 업로드

`desktop/dist/*.zip` 9개를 **`claude.ai/customize/skills` (설정 → Customize → Skills → Upload)** 에서 하나씩 업로드한다. (웹에서 업로드하면 같은 계정의 Desktop 앱에도 나타난다.)

먼저 올리길 권장하는 순서:

1. `magnific-studio-core.zip` — 횡단 규칙(최우선)
2. `magnific-studio-quickstart.zip` — 진입점 안내
3. `planning-director.zip` · `character-director.zip` · `storyboard-director.zip`
4. `production-director.zip` · `spaces-engineer.zip` · `quality-reviewer.zip`
5. `post-production-director.zip` — **계획 수립까지만**(렌더는 Claude Code)

각 스킬의 `description`은 Claude Desktop의 **200자 제한**에 맞춰 축약돼 있다(원본 `skills/`는 Claude Code용 전체 버전).

### 3) 사용

Desktop에는 슬래시 커맨드가 없다. 채팅에서 스킬 이름으로 지시한다:

```
"magnific-studio-core 규칙을 따라 이 아이디어를 planning-director로 기획해줘"
```

`magnific-studio-quickstart` 스킬이 어느 스테이지에 어떤 스킬을 쓸지 안내한다.

### Desktop 제약 (요약)

| 구성 | Desktop | 비고 |
|---|---|---|
| 디렉터 스킬(기획·캐릭터·콘티·제작·심사) | ✅ | .zip 업로드 |
| Magnific 생성 도구 | ✅ | 커스텀 커넥터 |
| 슬래시 커맨드 `/ms-*` | ❌ | 스킬 이름으로 지시 |
| 후반 ffmpeg 렌더링 | ❌ | Claude Code 전용 |

---

## 빌드 (유지보수용)

Desktop용 .zip을 다시 생성하려면:

```
python3 desktop/build.py
```

`skills/`의 원본을 복사해 `description`만 200자 이내로 리라이트하고 `desktop/dist/*.zip`으로 패키징한다.
Desktop 전용 진입점 스킬 원본은 `desktop/skills-src/magnific-studio-quickstart/`에 있다.
