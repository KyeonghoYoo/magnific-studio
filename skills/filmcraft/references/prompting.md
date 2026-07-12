# Prompting — Prompt-Projection Layer | KR: 프롬프트 투영 계층

*Read this when: composing ANY generation prompt at `/ms-produce`; pre-flight linting before `spaces_run`.*

**Scope.** This file owns every model-facing prompt string in the pipeline — how a prompt is assembled, ordered, and linted. It does NOT define the controlled vocabulary itself (camera-movement taxonomy, lighting-plot fields, shot framing) — those live in the sibling lexicon references in this directory and in `docs/filmcraft-rulings.md` §1. Model names, versions, and dated facts live ONLY in `model-matrix.md` — this file never names a model.

## 1. Projection Principle | KR: 투영 원칙

Two layers, one projection (rulings A1). Canonical artifacts — `storyboard.json`, `project_brief.json`, `edit_plan.json` — store MODEL-FREE controlled vocabulary. This file's deterministic tables render prompts FROM that record at produce time (production-director, applied before every `spaces_run`). The projection may reorder, expand, translate the record into prompt text — it may NEVER deform the record. If a rule below would require inventing a value the canonical artifact doesn't have, that's a storyboard defect, not a projection job.

Every branch in this file keys on a **capability flag**, never a model name (rulings A2):

```
model_profile = {
  negative_prompt: bool,
  max_moves_per_shot: int,
  named_tag_syntax: bool,
  flf_support: bool,
  camera_param_object: bool,
  legal_durations: [int, ...],   // seconds
  text_render_ok: bool,
  native_audio: bool
}
```

`model_profile` is written into `production_manifest.json` at produce Step 1 from `video_models_list`/`images_models_list` — that's production-director's job, not this file's. This file only *consumes* it. Resolve flag values per campaign in `model-matrix.md`.

## 2. Ordering Templates — the fork | KR: 순서 템플릿 — 정지/영상 분기

No universal ordinal exists (Google contradicts itself — documented). We fork by OUTPUT TYPE, not by model.

**KEYFRAME (T2I) — subject-first:**
```
[image type / shot size] → [subject + identity handle] → [static pose / action state]
  → [environment] → [composition] → [lighting sentence] → [lens/optics] → [stock/style]
```

**CLIP (I2V/T2V) — camera-early heuristic (a heuristic, not a mandate):**
```
[camera movement + speed] → [subject appearance phrase] → [ONE action, max 2]
  → [environment cue] → [settle clause]
```

| Slot | Rule |
|---|---|
| lighting sentence (keyframe) | byte-identical per scene — pulled verbatim from `scenes[].lighting`, never re-authored per shot (§10 lint #5) |
| identity handle (keyframe) | resolve per §3 |
| action (clip) | max 2, one preferred — exceeding this reliably produces "ignore everything after the first action and loop" |
| settle clause (clip) | always appended — "…then settle on [composition]"; last 10–15% of the clip is non-travel |

Sentence-form prose is the house default, not comma-tag stacking — current-generation prompt encoders parse natural sentences, and tag-era weighting syntax (see §5 blocklist) actively damages output on them. No universal word-count ceiling exists — tolerance is a capability, not a constant; default to a concise 60–150 words unless `model-matrix.md` documents wider tolerance for the active family this campaign.

**One-move law cross-reference:** exactly one `camera.movement` object per shot is the storyboard default. Produce-time merge of adjacent same-position shots into one multi-move prompt is legal ONLY when `model_profile.max_moves_per_shot ≥ 2` — and is never hand-authored in storyboard (rulings V5). Treat any family not yet verified this campaign as `max_moves_per_shot = 1`.

## 3. Identity-Handle Fork | KR: 정체성 핸들 분기

Storyboard stores `{{char:key}}` placeholders (in prompt-bound fields) plus one `appearance_phrase` per character in `characters.json`. Projection resolves the placeholder per `model_profile` at produce time:

| Condition | Resolves to |
|---|---|
| reference wired ∧ `named_tag_syntax=true` | model tag (`@name` / `<<<name>>>` / `@Image N` — see `model-matrix.md` for this campaign's actual syntax) |
| reference wired ∧ `named_tag_syntax=false` | `appearance_phrase` (verbatim) + reference image citation |
| no reference wired (rare; `citation_required=false`) | `appearance_phrase` verbatim from `characters.json` — never paraphrased |

`motion_desc` ALWAYS uses appearance phrases regardless of the fork above — with 2+ figures in a shot, the video model needs to know WHICH one performs the action, and it doesn't parse `{{char:key}}` or names. The named-tag resolution above governs the addressing/identity field only, never action disambiguation.

**Never paraphrase.** Copy the exact `appearance_phrase` string into every prompt occurrence — synonym substitution is the best cross-model-validated drift cause (a bare name carries zero visual payload; the phrase is strongest paired with an actual reference-image citation: identity lives in the reference, action lives in the prompt).

Blocking check: an unresolved `{{char:key}}` placeholder reaching `spaces_run` = ERROR (prompt-assembly defect, not a generation retry).

## 4. Negative Doctrine | KR: 네거티브 프롬프트 원칙 — 긍정 재구성

Positive reframing is the house default EVERYWHERE, independent of capability. Reframe table (compiler-owned — extend only here, never ad hoc per shot):

| Banned negative | Positive reframe |
|---|---|
| "no cars" | "empty street" |
| "no buildings" | "a desolate landscape" |
| "no camera shake" | "locked-off static shot on a tripod" |
| "no logos" | "plain unbranded packaging, blank matte label" |
| "no extra people" | "the street is deserted except for the subject" |

**Why:** attention-capture backfire — naming an unwanted element paradoxically invokes it ("no camera shake" → the model fixates on "shake"). This is the single clearest cross-model convergent finding in the prompting literature.

`negative_prompt` is NOT an authoring field. Storyboard/prompt authors never write negative text. Projection populates a negative field ONLY when `model_profile.negative_prompt=true`, translating FROM the same reframe table above — never freehand negatives, even when a field exists to hold them.

**BLOCKING LINT:** any emitted prompt matching negation-word + noun (`no|without|avoid|don't` + a following noun) = ERROR. Run before every `spaces_run` (§10).

## 5. Empty-Token Blocklist | KR: 공허 토큰 블록리스트

Blocking — verbatim ban in any emitted prompt:

`masterpiece` · `best quality` · `8k` · `4k` · `highly detailed` · `trending on artstation` · `award-winning` (bare) · `professional` (bare) · `octane render` · `unreal engine 5` · `(word:1.4)`-style weighting · `score_9` · `epic` (bare) · `moody` (bare) · `"dramatic lighting"` (bare) · `"beautiful composition"`

**CINEMATIC PAIRING RULE:** "cinematic" is valid ONLY co-occurring with ≥1 concrete technical noun: film stock | camera body | `<N>mm` | `f/<N>` | named lighting pattern | aspect ratio. Bare "cinematic" collapses toward one narrow generic look (dark, desaturated, haze, vague flare) — not banned outright, but pairing is REQUIRED.

**ENDORSED class:** named hardware/film stocks — the single best-evidenced positive-token category (independently convergent vendor endorsement). This is why `look.film_stock` is a first-class `visual_grammar` field (rulings §1.6) — it's the most reliable style lever available, not decoration.

| Token class | Verdict |
|---|---|
| masterpiece / best quality | legacy-encoder relic; placebo-to-harmful on current models |
| 8k / 4k | placebo |
| highly detailed | placebo |
| cinematic (bare) | disputed — REQUIRE pairing |
| trending on artstation | placebo [v] |
| award-winning / professional (bare) | placebo-leaning |
| hyperrealistic | weak standalone — pair with concrete camera/lens/stock |
| octane render / unreal engine 5 | unverified, likely placebo |
| named hardware / film stock | effective — best-evidenced category |

## 6. Motion Token Kit | KR: 모션 토큰 키트 — 투영이 자동 부착

Compiler-appended defaults — never authored per-shot in storyboard (source: `visual_grammar.motion_bible`, rulings §1.6):

| Token | When appended |
|---|---|
| easing | always |
| settle | always — the clip-template settle clause (§2) |
| moving_hold | subject holds a pose/position (prevents dead-frame "floaty" look) |
| anticipation | deliberate/weighted actions |
| gesture economy | HARD CAP — max 2 actions per clip |

Physics vocabulary (gravity, momentum, inertia, weight) is a STYLE SIGNAL steering motion QUALITY — not a literal simulation guarantee. Even the best-scoring family still lands well short of fully physics-correct on independent benchmarking [v]; use physics words to push toward "heavier" / "less floaty," never to promise correctness.

## 7. Text & Brand | KR: 텍스트·브랜드 — 베이크 금지

No baked text, ever — all legible text burns in during post-production, never generated. Any legible brand mark, product label, packaging, or plot-critical text = COMPOSITE from a locked real asset (`greeking` = canonical term for the placeholder-text technique), never text-described, never generated, and never entrusted to a negative prompt (legal exposure).

For STILLS where on-image text generation is genuinely unavoidable (concept exploration only — never a final asset): quote-plus-font technique — desired text in quotes AND a separate font/typography spec. Text-under-motion remains a near-universal unsolved failure (§11) — this technique does not extend to clips.

## 8. Audio Labels | KR: 오디오 라벨 — capability-gated

Populated ONLY when `model_profile.native_audio=true`:

- Quoted dialogue attributed by **appearance descriptor**, never by character name or `{{char:key}}` — e.g. *the woman wearing pink says: "…"* (same disambiguation discipline as `motion_desc` — §3).
- `SFX:` prefix for sound effects.
- `Ambient noise:` prefix for ambience.
- No music label exists in this syntax — music is never requested inline; it routes through `audio.music_cues` (rulings §1.5), not prompt text.

When `native_audio=false`: dialogue/SFX/ambience are produced through the separate audio pipeline (`audio_tts` / `audio_music_generate` / stock-sourced SFX) — never attempted via prompt text on a model that can't render audio.

## 9. Consistency Machinery | KR: 일관성 기계장치

- **Re-anchor to ORIGINAL references** (`conform_from_source`, rulings H7): always re-feed the original unedited reference asset per generation. Never chain a generated output into the next generation as its own reference. The one permitted exception (last-frame chaining) is capped at 1 generation and requires upscale + color-normalize + a `decision_log` entry.
- **Reference-sheet workflow:** 3–5 clean angles (frontal, 3/4, wide) on a plain background, never combined into one composite sheet. vendor guides report that 2–4 well-chosen images typically outperform 6 redundant ones [vendor-guide claim, not independently benchmarked]. Wide/small-in-frame references are riskier (more reinterpretation room) — weight the set toward closer angles when in doubt.
- **Restart-per-scene:** moving an established character into a new scene re-supplies the reference fresh. Don't rely on accumulated session memory for identity.
- **Batch/sequence modes are a CAPABILITY**, not a default assumption — only invoke multi-image batch-consistency calls when `model-matrix.md` documents support for the active family this campaign; otherwise the baseline path is single-generation + reference citation (production-director Step 3).

## 10. Pre-Flight Lint Checklist | KR: 프리플라이트 린트 — 생성 전, 크레딧 0

Run ALL SIX before every `spaces_run` (rulings A6 — hygiene checked BEFORE generation; `quality-reviewer` review happens after). Zero credits — static text checks only.

1. **Empty-token blocklist scan** (§5) — ERROR on match.
2. **Negation scan** — `no|without|avoid|don't` + noun (§4) — ERROR on match.
3. **Hex/ratio-number scan** — bare hex color codes and bare lighting ratios (e.g. "8:1") are BANNED in emitted prompts; use the canonical ratio→proxy sentence (rulings §1.3), never an invented per-shot substitute.
4. **`foreground_anchor` presence** — REQUIRED on every TRANSLATION-class camera move (dolly/truck/pedestal/crane/arc); missing = ERROR ("we pay dolly price, get a zoom").
5. **Lighting-sentence byte-identity** — the rendered lighting sentence must be byte-identical across every keyframe prompt within one scene (rulings §1.3 validator). The #1 documented AI failure, made mechanical.
6. **Appearance-phrase verbatim check** — every `appearance_phrase` occurrence in an emitted prompt must string-match `characters.json` verbatim (§3).

## 11. Failure → Fix | KR: 실패 유형 → 대응

| Failure | What's happening | Fix | Evidence |
|---|---|---|---|
| Hands | architectural weakness across current families | avoid close-ups on hands; regenerate, don't prompt-patch | [v] convergent |
| Baked/on-image text | rankings shuffle every 2–3 months; ALL families degrade once animated | quote+font for stills only (§7); no confirmed video-stage fix — never rely on generated text for a final deliverable | [v] |
| Faces at distance / crowds | model guesses under ambiguity → distortion/flicker | keep hero emotional beats MCU-or-tighter (storyboard rule H2); crowds are known-weak everywhere, strength varies by family | [v] convergent |
| Identity drift (single clip) | faces drift first; no persistent memory across frames | mitigated, not solved, by reference citation + appearance-phrase anchoring (§3, §9) | [v] |
| Identity drift (cross-shot) | improves generation-over-generation but two-characters-interacting still blurs everywhere | anchor frames (production-director Step 3, anchor-frame designation) + growing `reference_bank` | [v], family-dependent — reverify per campaign |
| Morphing | complex motion breaks interpolation; worse at stitched multi-minute durations | gesture economy max 2 actions (§6); shorter clips; settle doctrine (§2) | [v] |
| Floaty motion | models default to slow/safe motion for consistency | pacing camera language + environment-in-motion cues + physics-as-style vocabulary (§6) | [v] |
| Background flicker | underspecified environment → model guesses; high-frequency patterns (plaid/houndstooth) are notorious triggers | cover subject + environment + camera explicitly every prompt; avoid load-bearing high-frequency patterns | [v] |
| Prompt leakage | style words can bleed into content (e.g. a mood/genre word silently forcing an unwanted visual property) | treat as a RISK pattern, not a confirmed mechanism beyond the one studied case ("film noir → forced B&W" is plausible but UNCONFIRMED) | [unverified beyond cited study] — flag, don't over-correct |
