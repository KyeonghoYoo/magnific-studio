# Editing Grammar — Cut, Transition, Montage, Rhythm

**KR: 편집 문법 — 컷·전환·몽타주·리듬**

Read this when: building `edit_plan.json` at `/ms-post`; planning cut points and transitions.

**Scope & integration.** This file owns cut/transition/montage/rhythm VOCABULARY and edit-time decisions for `edit_plan.json` (schema_version 2.0, shipped — see §5 legacy migration from v1). It does **not** own, and cross-references instead of repeating:
- Murch Rule of Six weights, 180°/30° axis rules, eye-trace, McKee scene-value turns → `storyboard-director` SKILL.md, "편집 문법 부록" (shot-design-time).
- Target ASL per format → `format-director` SKILL.md format-profile table.
- Beat-sync tolerance, `beat_locked_cutting` flag, tentpole mechanics → `filmcraft/references/sound-music.md`.
- Camera-side `whip_pan` (an in-shot camera.movement base value) → `filmcraft/references/camera-movement.md`. This file uses "whip-pan" only as a cut-disguise technique (`hidden_join:whip`).

All `transition_in.type` values below are schema_version-2.0-final (rulings §1.4, BINDING). No value is authored without a renderer code path (rulings A4) — gaps are flagged explicitly, not papered over.

## 1. Canonical Terms

Duration tiers referenced throughout (full ms/frame table in §4; canonical 24fps frame counts): **soft_cut** 250–500ms (default 300; = 6–12f@24) · **dissolve** 1000–2000ms (default 1000 — the canonical one-second/24-frame dissolve; ellipsis-tier 3000–5000) · **fades** (fade_through_black/dip_to_white) 500–2000ms (= 12–48f@24).

### Cut Typology

| Term | KR | Use when | Effect | edit_plan instruction | QA (+Caveat) |
|---|---|---|---|---|---|
| Hard Cut | 하드 컷 | Continuous time/space, high energy, no transitional meaning implied | Neutral-to-brisk; reads as "now" | `transition_in.type: cut` (duration_ms absent) | Default value — omitting transition_in on any non-first clip means cut. |
| Cut on Action | 동작 컷 | Physical action spans two setups | Cut becomes perceptually invisible | `type: cut`; set `timeline[].in`/`out` so the cut lands in the action's middle third, ~80–250ms overlap trim | Caveat: generated pairs rarely share true motion continuity — trim to peak motion blur, not literal pose match. |
| Cut on Look | 시선 컷 | Off-screen glance motivates a cut to its object | Curiosity answered same beat; reinforces POV | `type: cut` to the shot whose `gaze_target`/`pov_of` (storyboard shot-grammar) is the look's object | Caveat: verify the storyboard `gaze_target` actually points off-frame before scripting the cut — generated gaze is unstable. |
| Cut on Sound | 사운드 컷 | A sonic event (bang/slam/sting) motivates the cut | Cut feels causally justified | `type: cut`; align `timeline[].in` to the transient's attack (cross-ref `audio.sfx[].at_sec`), not its peak | QA: cut point − transient attack should read as one frame at target fps. |
| Match Cut (graphic/conceptual) | 매치 컷 | Visual-metaphor transitions, time-leaps, irony | Shape/color/theme carries across the substitution | `type: cut`; composition anchoring is a generation-time concern (keyframe prompt), not an edit_plan field — log rationale in `notes` | Caveat: lock A's end-frame / B's start-frame to a shared composition anchor AT GENERATION time — cheapest to fake with generative control. |
| Jump Cut | 점프 컷 | Style: Godardian discontinuity, time-skip, anxious tone. Error: avoid | Visible "jump" — same subject, too-similar angle/scale | `type: cut`; no dedicated intent field — log `notes: "intentional_discontinuity: <reason>"` when authored as style | QA: adjacent same-subject cuts under storyboard-director's 30° rule with no `notes` entry = FAIL (unintentional jump cut). Caveat: near-identical AI regenerations of "the same shot" are jump-cut-shaped by default. |
| Smash Cut (incl. Gilligan Cut) | 스매시 컷 | Abrupt collision of tonally/dynamically opposed scenes. Gilligan Cut = stated intent immediately cut against its opposite | Shock/comic whiplash | `type: cut`; no `contrast`/`pattern` field exists — log tonal-contrast rationale in `notes` | Narrow definition (tonal/dynamic contrast required) is canonical; "any abrupt cut" is industry-loose drift, flag if unintentional. |
| Cutaway & Insert | 컷어웨이 및 인서트 | Time compression, tension delay, covering a continuity gap | Elastic time without the viewer noticing | `type: cut`; role comes from the referenced shot's storyboard `function: insert\|cutaway` (rulings §1.2 / `shot-grammar.md`), edit_plan just cuts to `shot_id` | Caveat: the single highest-value tool for hiding generation seams — cut to insert/reaction to skip a broken hand/morph/physics glitch, then return. |
| Cross-Cutting / Parallel Editing | 교차 편집 | Suspense toward convergence; contrasting simultaneous fates | Alternation implies simultaneity | Pure `timeline[]` ordering — alternate `shot_id`s from each line; no structure field needed | QA: alternation should accelerate (shorter `out`−`in` spans) as the converge shot approaches. |
| Intercutting (conversation/call) | 인터컷 | Cross-cutting at close range, one conversation | Intimacy + exchange rhythm (vs cross-cutting's suspense) | Shot/reverse-shot ordering in `timeline[]`, keyed to storyboard `framing: ots` pairs | Caveat: two sides are separate generations with no shared timing — the edit manufactures the rhythm. |
| J-Cut (audio lead) | J컷(오디오 선행) | Anticipation; motivated seam | Audio belonging to the incoming scene starts before its picture | No dedicated field — place the incoming element's start BEFORE the picture cut: `music_cues[].in` or `sfx[].at_sec` = cut_time − 170…625ms (VO: shift the manual-mix in-point) | Clip audio is stripped in this pipeline — J/L applies to the built audio layer (cues/SFX/VO), planned as its own pass. |
| L-Cut (audio trail) | L컷(오디오 잔류) | Continuity glue | Audio belonging to the outgoing scene continues past the cut | No dedicated field — extend the outgoing element's end PAST the picture cut: `music_cues[].out` = cut_time + 170…830ms (VO: manual-mix out-point) | Same built-audio-layer note as J-Cut. |
| Invisible Cut (Hidden Cut) | 히든 컷 | Disguising a cut so a sequence reads as continuous | Apparent unbroken continuity | `type: cut`, `hidden_join: whip\|object_wipe\|dark_frame`; occlusion ≥125–170ms full-frame blur/black | No `hidden_cut` transition value exists (no renderer path — rulings 1.4). See E6 for stitched_oner labeling. |
| Pre-lap | 프리랩 | Scene-level J-cut — erases the "dead" scene boundary | Propulsive; scene change stops reading as a beat | Incoming scene's cue/ambience `in` = scene-cut time − 330…1000ms | Scene-level extension of J-Cut; same built-audio-layer note. |

### Transition Semantics

| Term | KR | Use when | Effect | edit_plan instruction | QA (+Caveat) |
|---|---|---|---|---|---|
| Soft Cut | 소프트 컷 (기술적 보정) | First-frame tonal pop, near-jump-cut repair — TECHNICAL, carries no temporal meaning | Invisible below ~500ms; the join reads as a clean cut | `type: soft_cut`, `duration_ms`: 250–500 (default 300; band = 6–12f@24); ALWAYS try `timeline[].in` head-trim first (free — the 500ms head handle exists for this, E2) | EXEMPT from the act-punctuation reservation (E3). Not a dissolve: if the audience should feel time pass, that is `dissolve` |
| Dissolve (Cross-Dissolve) | 디졸브 | Time passage, softening juxtaposition, parallelism/memory | Duration legibly encodes elapsed-time weight | `type: dissolve`, `duration_ms`: 1000–2000 (default 1000 = the canonical 24-frame dissolve); major time jump → ellipsis-tier 3000–5000 | Never used as a technical repair — that's `soft_cut` (E2). Do not confuse with ffmpeg's raw `dissolve` xfade (banned, see E1). |
| Fade To/From Black | 페이드 | Chapter/act closure or opening | Structural punctuation | Very first/last clip of the whole piece: render-level `opening_fade_ms`/`end_fade_ms` (fade FILTER, not a transition). Mid-timeline act break: `type: fade_through_black` — the xfade=fadeblack blend is symmetric (out through black, in from black); `duration_ms` is the FULL through-black length — xfade has no black-hold plateau, the black is momentary at the crossover midpoint; a real sustained black hold is a separate render op (inserted black segment), not a transition parameter | RESOLVED: `fade_from_black` is NOT an authorable transition value — the symmetric `fade_through_black` + duration covers mid-film black holds; head/tail fades are render fields. |
| Dip to White | 화이트 딥 | Flash of memory, dream entry, death convention — context-dependent | Suspends rather than ends | `type: dip_to_white`, `duration_ms` per fades tier | Use sparingly — increasingly dated convention; flag if used outside memory/dream/death context. |
| Wipe (Left/Right) | 와이프 | Stylized/retro "meanwhile"; silent-era pastiche, comedic punctuation | Overtly authored — announces itself | `type: wipe_left` or `wipe_right`, `duration_ms` per fades-envelope guidance (~400–1000ms, unratified — author's discretion) | Horizontal only. No `wipe_up`/`wipe_down` — vertical motion is `slide_up`/`slide_down` (§5 do-not-confuse). |
| Blur Dissolve (디포커스 전환) | 블러 디졸브 | Soft entry into a payoff/brand card, memory/consciousness shift — the outgoing image defocuses INTO the incoming one | Reads as emotional dissolve rather than optical wipe; softer than dip_to_white, warmer than a plain dissolve | `type: blur_dissolve` (xfade=hblur), `duration_ms`: 600–1200 | Payoff/endcard entries where a hard flash (dip_to_white) is too loud — e.g. riders-bonding shot → brand card (pilot 1 direction). Not a repair tool — that stays `soft_cut` |
| Iris Open / Iris Close | 아이리스 오픈/클로즈 | Nostalgic/comedic pastiche; silent-era framing device | Circular reveal (open) / the classic Griffith-era scene-ending punctuation (close) | `type: iris_open` (xfade=circleopen) / `type: iris_close` (xfade=circleclose) | Both stylized — announce themselves; the iris-OUT is historically the more canonical scene-ender |
| Clock Wipe | 시계 와이프 | Countdown/heist "time passing" punctuation, retro-serial pastiche | Radial reveal, overtly stylized | `type: clock_wipe` → renders `xfade=radial` | Stylized, flag if used outside genre-appropriate context. |
| Match Dissolve | 매치 디졸브 | Time-lapse aging, object/location evolving, thematic rhyme | Reads as transformation, not a cut | `type: dissolve` + composition-anchor lock at generation (identical framing/subject position in both prompts) — not a distinct schema value | Caveat: lock camera framing/subject position across both generations explicitly in the prompt. |
| Whip-Pan Transition | 휩팬 트랜지션 | Kinetic scene change, action/comedy convention | Fast blur-streak carries the cut | **Not a transition value.** `type: cut`, `hidden_join: whip`, blur peak ~80–250ms | Caveat: model motion blur is inconsistent — safer to add blur/streak in post over a static-camera generation. |
| Speed-Ramp Transition | 스피드 램프 트랜지션 | Short-form pacing, action beats, hyping a reveal | Rapid speed change at the boundary IS the transition | **Not a transition value.** `timeline[].speed` (0.2–4.0) ramped on the adjacent clip(s) into/out of the cut | Caveat: ramping generated clips exposes interpolation warping at extremes — safest on large-scale motion, never faces/text. |
| Luma/Texture-Driven Transition | 루마·텍스처 트랜지션 | Modern/organic changes; hiding a hard tonal mismatch | Matte motion masks the seam | **No renderer path — do not author** (rulings A4). Fallback: `dissolve` or a wipe; flag as a future renderer-support candidate | Rejected pending Phase 5 renderer support, not a schema value today. |

### Montage

| Term | KR | Use when | Effect | edit_plan instruction | QA (+Caveat) |
|---|---|---|---|---|---|
| Kuleshov Effect | 쿨레쇼프 효과 | Foundational — governs every assembly decision | Juxtaposition reads meaning into an identical neutral shot | Prose concept, no field — informs shot-ordering choices generally | Load-bearing for this pipeline: sequencing is HOW generated clips acquire meaning the generation step didn't supply. Evidentiary status: original footage lost, replications mixed (L3). |
| Eisenstein's Five Methods (Metric/Rhythmic/Tonal/Overtonal/Intellectual) | 에이젠슈타인 5가지 몽타주 | Metric→hype, Rhythmic→action, Tonal→mood, Overtonal→climax, Intellectual→thesis/irony | Named cutting logics for `montage_sequence` construction | Prose concept informing HOW to cut a `scenes[].type: montage_sequence` — **no `montage_mode` enum** | Authorial reasoning only; do not invent a schema field for the method chosen. |
| Pudovkin's Linkage (vs Eisenstein's Collision) | 푸도프킨 연결 몽타주 | Linkage: sequential bricks building continuity. Collision: juxtaposition builds an abstract idea | Linkage underlies continuity/montage-sequence; collision underlies intellectual/associative montage | Prose concept, no field — Pudovkin's linkage is Eisenstein's theoretical RIVAL, **not a sixth method** | Corrects source research's enum error (editing.md listed linkage as a 6th Eisenstein method — it is a competing framework, L5). |
| American Montage Sequence | 미국식 몽타주 시퀀스 | Time-compressed, music-scored progress sequence | Native fit for uniform short generated clips | `storyboard.scenes[].type: montage_sequence` + `cut_sync: beat_grid\|motion\|free` (upstream, rulings §1.3); edit_plan expresses the resulting shots as ordinary `cut`/`soft_cut` entries | Caveat: strong native fit — short uniform generated clips are already montage-shaped, lean into the form. |
| Contrapuntal (Asynchronous) Sound-Image Montage | 대위법적 사운드-이미지 몽타주 | Ironic commentary, unease (cheerful music over violence) | Sound deliberately in tension with image, beyond J/L overlap | No dedicated field — author via `audio.music_cues[].why` rationale; ironic pairing is a music-spotting decision | Distinguish from J/L (temporal overlap only) — this is semantic/tonal tension, not timing. |
| Cutting on the Beat | 비트 컷 | Hype-montage, comedy | Cut points locked to a music grid | `audio.beat_snap.mode: snap` (montage/hype default) — see `sound-music.md` for tolerance, `beat_locked_cutting` flag, and the "cut on picture, sync only tentpoles ≤3" doctrine | **Cross-ref only** — full beat-sync doctrine is owned by `sound-music.md`, not repeated here. |

### Rhythm & Pacing

| Term | KR | Use when | Effect | edit_plan instruction | QA (+Caveat) |
|---|---|---|---|---|---|
| Pearlman's Three Rhythms (Physical/Emotional/Event) | 펄먼의 3가지 리듬 | Diagnosing why a sequence feels off when ASL/1-f math checks out | A scene can be metrically fine and still fight itself (physical vs emotional rhythm) | Diagnostic prose concept, no field — re-examine `timeline[]` pacing choices when this triggers | Cross-ref `storyboard-director`'s 1/f-clustering line (편집 문법 부록) — this is the diagnostic layer above that statistic. |
| Editing on Movement vs. Editing on Rest | 무브먼트 컷 vs 정지 컷 | Movement: action/momentum. Rest: dramatic beats, comedy timing, dialogue | Energy carries through vs a beat completing before the cut | Choose `timeline[].in`/`out` relative to the action's completion point, not a fixed offset | — |
| Holds / Breathing Room | 홀드 (숨 고르기) | Extending a shot beyond its "efficient" cut point after a high-impact beat | Prevents the impact from being trampled; signals "this mattered" | Extend `timeline[].out`: relative rule ~1.5–3× LOCAL ASL (absolute ASL target from `format-director`) | The deliberate exception to 1/f — don't flag a Hold as an ASL violation. |
| Tension Curve Shaping | 긴장 곡선 설계 | Authoring shot-length rhythm across a sequence toward/away from a climax | Accelerating cadence into a peak, release via Hold after | Authorial arc across `timeline[]` shot-length choices, no field | Extends 1/f clustering (storyboard-director) from a statistical property into an authored arc — same statistic, editorial intent layered on top. |
| Pattern & Pattern Interrupt | 패턴 인터럽트 | Uniform-length clips feel monotonous | Breaks a rhythmic pattern to re-capture attention | Device via `freeze_tail`, a `speed` change, or an inserted cutaway `shot_id`, cadence ~3000–5000ms [v] | Caveat: directly mitigates uniform-clip monotony — the single biggest tell of AI-generated montage. |
| Trim Doctrine (shot level) | 트림 원칙 (숏 단위) | Every shot, universally | Eliminates dead frames; imagination fills the trim | `timeline[].in` += ~80–330ms, `timeline[].out` −= ~80–330ms (leave early / enter late) | Shot-level counterpart to the scene-level doctrine below. |
| "Cut When Something Changes" | "무언가 바뀔 때 컷한다" | Gate before adding any `timeline[]` entry | Filters reflexive uniform-interval cutting | Authorial gate, no field | QA: two adjacent entries with no compositional/informational delta between them = FAIL — cut where content changes, not where the clip file ends. |
| Dailies Selection ("The Select") | 데일리 셀렉트 | Choosing among alternative takes/candidates | Sets the quality ceiling of the whole edit | Pre-edit_plan: choose which `production_manifest` candidate becomes `timeline[].clip_id` | Maps directly to picking among generated variations — "performance truth" = does the motion read intentional; "technical" = artifact-free. |

### Scene-to-Scene

| Term | KR | Use when | Effect | edit_plan instruction | QA (+Caveat) |
|---|---|---|---|---|---|
| Enter Late / Leave Early (scene level) | 씬 단위 늦은 진입·이른 퇴장 | Every scene boundary | Starts at dramatic necessity, exits before the obvious conclusion | Scene-level application of Trim Doctrine to the first/last `timeline[]` entry of the scene | — |
| Cut on Question | 질문 컷 | Scene needs forward pull | Ends on an unresolved question the next scene answers | `type: cut` (or `soft_cut` if the join needs repair) — the "question" is a writing-time property, no dedicated field | — |
| Sound Bridge (scene level) | 사운드 브리지 | Scene needs forward pull without a hard audio break | Audio spans the boundary — pre-lap, trailing, or continuous bed | CUE PLACEMENT across the boundary — incoming `music_cues[].in`/`sfx[].at_sec` set BEFORE the cut (pre-lap) or outgoing `music_cues[].out` extended PAST it (trail) — or a continuous `audio.ambience[]` entry spanning both scenes | Sound half of the storyboard-director scene-connective-beat rule (item 8) — picture half lives there, audio half here. |
| Act Punctuation Pattern | 막 구두점 패턴 | Reserving one transition exclusively for act breaks | Its appearance signals structural weight (E3) | `type: fade_through_black` or `dissolve` (ellipsis-tier) RESERVED to act-boundary `timeline[]` indices only | QA: count(`fade_through_black`) at non-act-boundary indices must be 0. |

## 2. Doctrine

**E1. Schema speaks editorial; renderer translates.** `transition_in.type` is a controlled EDITORIAL vocabulary — never an ffmpeg filter name. The renderer owns the mapping table (Phase 5 code in `scripts/render_edit_plan.py`); this file documents it for authoring, not for re-deriving. Schema `dissolve` (editorial: "time passed") ≠ ffmpeg's raw `dissolve` xfade type (noise-dither, renamed `dither_dissolve` internally, never exposed, BANNED on generated clips — dither artifacts read as broken generation, not style).

**E2. `soft_cut` is a repair, not a transition-with-meaning.** It exists only to defuse a first-frame tonal pop / near-jump-cut; it is EXEMPT from the act-punctuation reservation (E3) because it carries no temporal claim. Precedence is fixed: try `timeline[].in` head-trim FIRST — free and lossless, since the source clip already carries a 500ms head handle (§4 duration handles) — before spending a `soft_cut` (250–500ms, default 300). Reach for `soft_cut` only when trimming would cut into needed content. `dissolve`'s duration is not a repair budget; it's how much narrative time the audience is told has passed.

**E3. Punctuation reservation.** The fades family (`fade_through_black`/`dip_to_white`, 500–2000ms; head/tail fades via `opening_fade_ms`/`end_fade_ms`) is reserved for act/chapter boundaries — its appearance signals structural weight. Spending one mid-act to paper over a bad join is a doctrine violation, not a style choice: it teaches the audience a false structural beat. `soft_cut` is the correct tool for mid-act repairs precisely because E2 exempts it from this reservation.

**E4. Montage is two words wearing one spelling.** `montage_sequence` is a schema value (`storyboard.scenes[].type`) naming a DEVICE — a time-compressed, music/beat-driven progress sequence (American usage). "Montage theory"/"Soviet montage" names a 1920s theoretical framework (Kuleshov, Eisenstein, Pudovkin) about how any juxtaposition manufactures meaning — it governs every cut in the pipeline, not only montage-sequence scenes, and has no schema surface at all. There is no `montage_mode` enum; Eisenstein's five methods and Pudovkin's linkage are documented CONCEPTS for authorial reasoning, never fields.

**E5. The rhythm toolkit serves targets it doesn't own.** Holds, pattern interrupts, and trim doctrine are the edit-time levers; the numbers they aim at — target ASL per format, Rule-of-Six cut-priority weights, 1/f tension clustering, beat-sync tentpole count — are owned upstream (`format-director`, `storyboard-director` 편집 문법 부록, `sound-music.md`). When Pearlman's three rhythms disagree even though the ASL/1-f math checks out, trust the diagnostic over the arithmetic.

**E6. Truth-in-labeling for stitched sequences.** This pipeline cannot generate a true continuous take. Every oner is a `stitched_oner` — cuts hidden via `hidden_join` (whip/object_wipe/dark_frame) at generation-planned occlusion points. Client-facing copy says "designed as a continuous take" — **never** "single take" or "one shot." `long_take` is reserved for genuinely single-pass source material, which this pipeline does not produce.

## 3. Decision Tables

**A. Trigger → Cut choice**

| Trigger | Choice |
|---|---|
| Physical motion spans the cut | Cut on action — mid-motion, ~80–250ms overlap trim |
| Character glances off-frame | Cut on look — to the `gaze_target` shot |
| Percussive audio event | Cut on sound — align to transient attack |
| Two setups too similar (<30° / same size-class — storyboard-director's threshold) | Commit as Jump Cut with `notes` intent flag (style), OR regenerate at a wider angle/size delta (error) |
| Bad frame / glitch / continuity gap | Cutaway/insert, or `hidden_join: object_wipe`/`dark_frame` over the bad frames |
| Simultaneous lines, building suspense | Cross-cut, accelerating alternation toward convergence |
| Scene needs forward pull | Cut on Question + outgoing audio out-point extended past the cut (L-cut via cue placement) |
| High-impact beat just landed | Hold — extend `out`, do not cut immediately |
| Uniform-length clips feel monotonous | Pattern Interrupt every 3000–5000ms |

**B. Meaning → Transition**

| Meaning | Transition |
|---|---|
| No meaning implied | `cut` |
| First-frame tonal pop / near-jump-cut (technical, not meaning) | `soft_cut` 250–500ms (after head-trim, E2) |
| Time passed, softly | `dissolve` 1000–2000ms |
| Time passed, substantially | `dissolve` ellipsis-tier 3000–5000ms |
| Chapter/act closes/opens (very first/last clip) | `opening_fade_ms`/`end_fade_ms` (render fields) |
| Chapter/act closes/opens (mid-timeline) | `fade_through_black` (symmetric; duration_ms = full transition length, no sustained hold) |
| Memory/dream/ambiguous | `dip_to_white` — sparingly, dated |
| Overt "meanwhile," stylized (horizontal) | `wipe_left`/`wipe_right` |
| Overt "meanwhile," stylized (vertical) | `slide_up`/`slide_down` |
| Nostalgic/comedic pastiche | `iris_open` / `iris_close` |
| Countdown/heist punctuation | `clock_wipe` |
| Same-subject transformation | `dissolve` + composition-anchor lock at generation |
| Kinetic scene change | `hidden_join: whip` on a `cut`, or a `speed` ramp on the adjacent clip — not a transition value |
| Organic mask over tonal mismatch | No renderer path — use `soft_cut`/`dissolve` instead (rejected pending Phase 5) |

**C. AI-gen defect → Edit-plan mitigation**

| Defect | Mitigation |
|---|---|
| Uniform clip lengths | Pattern Interrupt; vary via `speed`, `freeze_tail`, or an inserted cutaway |
| First-frame tonal pop at join | Head-trim `in` first (free); `soft_cut` 250–500ms only if trim is insufficient (E2) — **not** a `dissolve`, that would claim false narrative time |
| Baked motion doesn't match neighbor | Cutaway/insert between; never force a Match Cut |
| No clean dialogue stem | J/L (cue-placement pre-lap/trail) unavailable — regenerate with separated audio |
| Broken hand/morph mid-clip | Cutaway, or `hidden_join: object_wipe` over the bad frames |
| Inconsistent camera motion between angles | Static-camera generation (production-time) + `hidden_join: whip` only if disguising as a pan |
| Weak narrative link between shots | Kuleshov — sequencing manufactures the missing meaning, no field needed |
| End-frame coherence degradation | Default-trim the last frames — absorbed by the 300ms tail handle (§4) |

## 4. Numeric Anchors

All durations in milliseconds. Frame counts in source research assumed 24fps (rulings A5); renderer default is 30fps — both given.

| Tier | ms | f@24 | f@30 |
|---|---|---|---|
| soft_cut min | 250 | 6 | 8 |
| soft_cut default | 300 | 7 | 9 |
| soft_cut max | 500 | 12 | 15 |
| dissolve min | 1000 | 24 | 30 |
| dissolve default | 1000 | 24 | 30 |
| dissolve max | 2000 | 48 | 60 |
| dissolve ellipsis-tier min | 3000 | 72 | 90 |
| dissolve ellipsis-tier max | 5000 | 120 | 150 |
| fades family min | 500 | 12 | 15 |
| fades family max | 2000 | 48 | 60 |
| trim doctrine min (heads/tails) | 80 | 2 | 2 |
| trim doctrine max (heads/tails) | 330 | 8 | 10 |
| duration handle — head | 500 | 12 | 15 |
| duration handle — tail | 300 | 7 | 9 |

**Duration handles (H8).** `storyboard.shot.duration_sec` = timeline intent + 500ms head + 300ms tail. This is *why* head-trim is free in E2 (the handle exists precisely to absorb it) and why the tail exists: it also absorbs AI end-frame degradation (§3-C) as a side benefit — one handle, two jobs.

**Secondary numbers (source-inherited):**
- Cut-on-action overlap trim: ~80–250ms [v]
- J-cut lead: ~170–625ms dialogue; 1000ms+ ambience/music pre-lap
- L-cut trail: ~170–830ms reaction; seconds-scale VO-over-B-roll (open)
- Invisible-cut occlusion floor: ≥125–170ms full-frame blur/black
- Pre-lap (scene-level J-cut): ~330–1000ms
- Whip-pan blur peak: ~80–250ms
- Holds: relative 1.5–3× LOCAL ASL (absolute target: `format-director`)
- Pattern-interrupt cadence: 3000–5000ms [v]; hook window (first 10000ms): cut every 1500–2000ms [v]
- Cutaway/insert typical duration: 500–3000ms
- Perception floors [v]: subliminal 42–83ms · supraliminal 125–167ms · "flash cut" 83–208ms · visible-insert floor 250–500ms (psychophysics footnote: 1-frame stimuli at 24/30fps are predominantly unidentified)
- Jump-cut geometric threshold [v]: <30° reposition AND insufficient size-class change — shared constant, owned by `storyboard-director`'s 30° rule
- ASL historical trend [v] (context only, not an operative target): pre-1960 Hollywood ~8000–11000ms/shot → contemporary mainstream ~4000–6000ms/shot; extremes: *Bourne Supremacy* ~2400ms vs *2001* ~13000ms

## 5. Aliases & Do-Not-Confuse

**Canonical ← aliases**
| Canonical | Aliases |
|---|---|
| `dissolve` | crossfade, mix, lap dissolve |
| `fade_through_black` | fade to black (join) |
| `soft_cut` | micro-dissolve, blend cut |
| `dip_to_white` | white flash cut |
| audio lead/trail via cue placement (`music_cues[].in/out`, `sfx[].at_sec`) | J-cut/L-cut, pre-lap/post-lap (glossed aliases only — authored as cue timestamps; no named offset field exists) |
| Smash Cut | Gilligan Cut (narrow subtype: stated intent cut against its opposite) |
| Insert/Cutaway (narrative context) | b-roll (broadcast term — do not use in edit_plan `notes`) |
| `stitched_oner` | invisible-cut sequence, hidden-cut sequence |

**Legacy schema migration (v1.0 → v2.0, rulings §1.4 pattern):**
| v1.0 value | v2.0 value |
|---|---|
| `fade` | `dissolve` |
| `dissolve` (old, ffmpeg noise-dither) | `dissolve` (new, editorial) + WARN — re-author, semantics changed |
| `fadeblack` | `fade_through_black` |
| `fadewhite` | `dip_to_white` |
| `wipeleft` / `wiperight` | `wipe_left` / `wipe_right` |
| `slideup` / `slidedown` | `slide_up` / `slide_down` |
| `circleopen` | `iris_open` |
| `radial` | `clock_wipe` |

**Do-not-confuse**
- `dissolve` (schema, editorial "time passed") vs ffmpeg's raw `dissolve` xfade filter (noise-dither, banned, internal name `dither_dissolve`) — E1. The renderer's `xfade=fade` is what schema `dissolve` actually plays as.
- `soft_cut` (technical repair, no temporal meaning, punctuation-exempt) vs `dissolve` (meaningful ellipsis, duration = weight) — E2.
- `hidden_join` (annotation on a `cut`: whip/object_wipe/dark_frame) vs `hidden_cut` — **`hidden_cut` is not a transition value; there is no renderer path for it.**
- `wipe_left`/`wipe_right` (horizontal only) vs `slide_up`/`slide_down` (vertical only) — no `wipe_up` or `slide_left`.
- `iris_open` (reveal/opening) vs `iris_close` (scene-ending punctuation — the historically canonical member of the pair).
- Jump Cut as style (flagged, intentional) vs Jump Cut as error (unflagged, same geometry) — the geometric test (<30°/size-class) is identical; only the `notes` intent flag differs.
- Match Cut (broad — graphic/conceptual, no physical continuity required) vs Cut on Action (requires actual physical motion continuity across the cut).
- Whip-pan *transition* (`hidden_join: whip` on a cut, editing-time) vs `whip_pan` (a `camera.movement` base value, an in-shot camera technique — `camera-movement.md`) — same word, different department.
- `montage_sequence` (schema device, American usage) vs "montage"/"Soviet montage" (theory, unqualified use risks total miscommunication) — E4.
- `long_take` (genuine single-pass source, not produced by this pipeline) vs `stitched_oner` (this pipeline's actual output, always) — E6.

## 6. AI-Gen Caveats

Beyond the three caveats already threaded through §1–3 (uniform clip length → Pattern Interrupt; baked motion mismatch → cutaway, never a forced Match Cut; first-frame tonal pop → head-trim then `soft_cut`, E2):

- **Temporal drift within a single clip** [v]: lighting/texture/identity drifts first→last frame — a continuity error against itself. Keep clips short; cut before it accumulates.
- **Identity slip across clips** [v]: faces/clothing/objects shift between clips of the same subject — verify identity-lock before scripting continuity-dependent cuts (Cut on Action, Match Cut).
- **No true camera-to-camera geometry**: two generated "angles" aren't the same 3D space — eyeline/screen-direction (storyboard `gaze_target`/`screen_direction`) are approximations the edit must sell harder via Cut on Look discipline.
- **Motion-cadence mismatch**: different generations carry different smoothness/stutter at identical fps — perceptible cadence jolt at cuts; a Cutaway or `soft_cut` can mask it, a bare `cut` exposes it.
- **No usable diegetic audio**: J/L-cuts, Sound Bridges, and Cut on Sound all depend on a separately built audio layer — plan as a distinct pass, not assumed from generated clip audio (`audio.clip_audio` defaults to `strip`).
- **Loop/extend seam tell** [v]: extended clips carry a stitch seam — cover with a Hold/Cutaway, or a `hidden_join`.
- **Identity-lock vs lively-motion trade-off** [v]: tight consistency constraints → stiffer motion; looser → drift. Track which failure mode a clip was generated toward — it determines which cut tools are safe (stiff motion tolerates Cut on Action better; drifting identity needs Cutaway cover, not Match Cut).
- **No physical rack-focus/depth continuity**: focus-pull "transitions" won't intercut cleanly across different DoF simulations — do not author a rack-focus transition, there is no field or renderer path for it.
- **End-frame degradation**: coherence drops in final frames — default-trim the last frames, absorbed by the 300ms tail handle (§4).
- **Establishing-shot scarcity**: models are weaker at wide many-element geography shots — plan Cutaway/Insert-heavy coverage (storyboard `function: insert\|cutaway`) rather than relying on a single wide master to carry a scene.
