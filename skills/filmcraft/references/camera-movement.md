# Camera Movement — 카메라 무브먼트

Canonical vocabulary and doctrine for camera movement in AI video generation.
**Read this when:** choosing `camera.movement` at /ms-storyboard; writing motion prompts at /ms-produce; diagnosing a move that rendered wrong.

## The movement object (schema shape — exactly ONE per shot)

```
movement: {
  base:      static | pan | tilt | dolly | truck | pedestal | crane | arc | zoom | dolly_zoom | roll | whip_pan | crash_zoom
  direction: pan|truck|whip_pan|arc → left|right · tilt|pedestal|crane → up|down
             dolly|zoom|dolly_zoom|crash_zoom → in|out · roll → cw|ccw · static → (absent)
  speed:     slow | normal | fast        (absent for static/whip_pan/crash_zoom — speed-coded by definition)
  support:   locked | handheld | stabilized | drone      (default locked)
  subject_relation: none | follow | lead                 (optional)
  arc_degrees: 30–360                    (REQUIRED iff base=arc; "orbit" = alias for arc@360)
  foreground_anchor: "<named element>"   (REQUIRED iff base ∈ {dolly, truck} — the documented zoom-substitution failure;
                                          RECOMMENDED for pedestal/crane/arc — omit only with a parallax note: on open/aerial
                                          frames the parallax comes from background planes shearing, not a foreground object)
}
```

**Definitional truth the flat schema compresses** (the lexicon teaches what the schema flattens):
a **zoom is an optical change, not a camera movement** — the focal length changes, the camera does not travel, and **no parallax** is produced. That absence of parallax is the entire basis of the dolly/zoom distinction. `dolly_zoom` is canonically the *compound* {dolly in + zoom out} (or the inverse); `whip_pan` and `crash_zoom` are speed-coded variants of pan/zoom. They remain single schema values because current video models treat "blur-to-streak" and "instant snap" as qualitatively different requests, and single-value validation stays simple.

## 1. CANONICAL TERMS

### Base movements

| Term | KR | Use when | Effect | Prompt phrase | QA | Caveat |
|---|---|---|---|---|---|---|
| static | 고정 쇼트 | objectivity, dread-through-stillness, deadpan, tableau; fallback when a move keeps failing | frame becomes a stage the viewer reads actively | "locked-off static shot, no camera movement" | zero drift/translation in clip | the reliability fallback — every current model executes it |
| pan | 팬 | reveal space left/right; follow lateral motion; connect two subjects in one take | keeps viewer spatially oriented; observational | "slow pan left across the room" | rotation only — no translation | among the most reliable moves |
| tilt | 틸트 | reveal height; follow vertical motion | awe/scale (up), grounding/vulnerability (down) | "slow tilt up to reveal the tower" | rotation only, vertical | reliable |
| dolly | 달리 | in = intimacy, mounting focus, realization; out = isolation, context reveal, letting go | parallax shift reads dimensional/immersive — "we move into the space" | "slow dolly in toward the subject's face, passing the [foreground element]" | **parallax visible** — background planes shift relative to foreground | models render a zoom instead when no parallax cue exists — hence foreground_anchor REQUIRED |
| truck | 트럭 | reveal lateral environment; parallel a walking subject; walk-and-talk | subject compositionally stable while the world scrolls — escort energy | "camera trucks right, keeping pace with the subject, past the [foreground element]" | lateral translation + parallax | anchor REQUIRED |
| pedestal | 페데스탈 | subtle vertical reframe on a standing/sitting subject | quiet reframe that shouldn't call attention to itself | "camera pedestals up slightly, staying level" | vertical translation, no arc/tilt | smallest, slowest move in the kit; anchor RECOMMENDED not required (bare studio/interview frames often have no foreground — WARN) |
| crane | 크레인 | grand reveals, scale statements, floating over/into a scene | grandeur, omniscience, biggest-beat punctuation | "crane up past the [foreground element], revealing the full [environment], then settle" (open/aerial frames: omit the anchor, note the background-plane parallax) | vertical travel + reveal | direction REQUIRED; anchor RECOMMENDED (WARN if absent, not ERROR); crane+arc compound = two sequential shots |
| arc | 아크 (부분 선회) | revealing dimensionality; transitioning between two facing angles; hero/product showcase (arc_degrees high) | dynamic without showiness; parallax sells depth | "camera arcs 90 degrees around the subject, left to right, the [foreground element] sweeping past in the near field" | curve traveled ≈ arc_degrees; subject stays framed | an arc genuinely needs parallax to read — anchor strongly recommended (WARN if absent); risk scales with degrees — ≤120° holds up, 360° melts geometry; split large arcs into 2–3 partials stitched in post |
| zoom | 줌 | fast/cheap reframe; deliberate flat/clinical/surveillance feel; crash variant for shock | background does NOT shift relative to foreground — "the space is picked out and flattened" | "zoom in on the subject's face" / "extremely slow creeping zoom" | magnification change, no parallax | the most reliable "get closer" RESULT — but never a silent substitute for dolly (see fork) |
| dolly_zoom | 돌리 줌 | direction in (dolly-in + zoom-out): background stretches AWAY — unreality, vertigo; direction out (dolly-out + zoom-in): background rushes IN — dawning horror. "Vertigo effect" names the TECHNIQUE as a whole (either direction), not one of them | subject fixed in frame while the world warps — most disorienting move in the kit | "dolly zoom: camera pushes in while the background stretches and warps away, subject stays the same size" | subject scale constant, background perspective visibly warps | not a trained primitive in any major model [v] — expect approximation; plan a post fallback (locked subject plate + background scale-warp) |
| roll | 롤 | disorientation, chaos, impact/falling; stylized transition | strongest "something is wrong" cue as MOTION | "camera rolls 20 degrees clockwise during the impact" | horizon visibly rotates during clip | under-rendered/smeared by most models — a static canted frame (`dutch_deg`, shot-grammar.md) is far more reliable |
| whip_pan | 휩 팬 | urgency, comic timing, scene-to-scene bridge, "snap to" a new subject | kinetic jolt; hides a cut | "fast whip pan left, motion blur streaks, snapping to [subject]" | blur streaks present; resolves on a legible frame | models blur reliably but rarely land a precise end composition; a whip-to-whip match join is a POST job (`hidden_join: whip`) |
| crash_zoom | 크래시 줌 | shock beat, comedy punctuation | breaks rhythm on purpose | "sudden crash zoom in on [subject]" | near-instant magnification snap | models render fast-but-gradual, not a true snap — often needs a post speed-ramp |

### Speed, support, relation

| Term | KR | Use when | Effect | Prompt phrase | QA | Caveat |
|---|---|---|---|---|---|---|
| speed: slow | 저속 | dread, grandeur, intimacy — the default emotional register of a push | reads deliberate, authored | "slow dolly in" | move occupies most of clip duration | slow modifiers are markedly MORE reliable than fast [v — vendor guidance] |
| speed: normal | 보통 | neutral coverage; pace-matching a walking subject | unmarked | (no modifier needed) | — | — |
| speed: fast | 고속 | urgency, chase energy | kinetic, risky | "fast truck right" | — | fast + translation = warping/artifact trails — WARN; consider generating normal speed + post speed-ramp |
| support: locked | 삼각대 고정 | default; classical invisible technique | machine-steady | (default — no token) | no shake | — |
| support: handheld | 핸드헬드 | urgency, verité truth-claim, chaos, subjective immediacy | a body is present, not a machine | "loose handheld camera, subtle shake" / "frantic handheld energy" | visible micro-shake | energy is a dial — say "subtle"/"frantic" explicitly |
| support: stabilized | 스태빌라이즈드 | intimate unbroken following that should feel alive; walk-and-talks | floating glide with felt presence | "smooth stabilized tracking, subtle organic float" | smooth travel, minor sway | steadicam/gimbal distinction has zero generation consequence — both compile here (aliases) |
| support: drone | 드론 | aerial establishers; fly-over/fly-through | god's-eye orientation or visceral velocity | "aerial drone shot flying over the [landscape]" / "camera flies through the [archway] at speed" | altitude/aperture traversal | fly-through is a genuine AI STRENGTH — impossible practical rigs are where gen video outperforms production [v] |
| subject_relation: follow | 팔로우 | entering a space through the character's momentum; withholding what's ahead | viewer inhabits momentum, not sightline | "camera follows behind the subject as they walk" | camera trails subject at constant distance | — |
| subject_relation: lead | 리드 | privileging face/resolve during motion; heroic or confrontational walk-ups | viewer watches the character, not the destination | "camera leads in front of the subject, facing them as they approach" | camera precedes subject, facing back | — |

### Compounds & reveals (built from primitives — never authored as one generation)

| Term | KR | Use when | Recipe | Caveat |
|---|---|---|---|---|
| rise-reveal | 라이즈 리빌 | "and then we see the whole picture" — scale/twist reveal, sequence punctuation | crane up (+ tilt handled by model), settle on the reveal: "camera rises, revealing the full valley beyond the ridge, then settles" | single-direction crane is reliable; crane+arc compound is not — decompose |
| top-down descend | 탑다운 디센드 | cold-open entry; god's-eye→human-scale transition | "top-down aerial shot descending toward the subject, settling at eye level" | drone support |
| compound move (dolly+pan, crane+tilt) | 복합 무브 | classical Hollywood grammar — reveal + reposition in one gesture | AUTHOR AS TWO SEQUENTIAL SHOTS. Compound moves are the single weakest generation category [v] | compound moves EXIST and are classical — the one-move law is a pipeline constraint, not film grammar (see Doctrine 2); decomposing one gesture into two cuts has an aesthetic cost — log it |
| oner (stitched) | 스티치드 원테이크 | virtuoso continuity set-pieces | sequence of single-move clips joined with `hidden_join` (whip/object_wipe/dark_frame) | a true long take is DEFINED by the absence of a cut — stitched material is a `stitched_oner`; client copy says "designed as a continuous take", never "single take" |

## 2. DOCTRINE

1. **One-move law (authoring).** Exactly one movement object per shot; two moves = two shots. Six vendor guides independently confirm multi-move prompts degrade both moves [v]. Produce-time exception — NARROW: only on models with **documented native multi-move composition** (a capability feature, e.g. bracket tokens or composable motion concepts — see model-matrix), never as a default optimization, always an explicit logged decision, and both moves are QA'd independently. Prompt-level merging on ordinary models contradicts the vendor evidence and the §6 compound-moves caveat — don't. Never silently drop a move (강등 금지).
2. **The law is a pipeline constraint, not film grammar.** Classical cinema is built on compound moves (crane boom-down-and-pan). The lexicon records the truth; the constraint lives with the models and may relax as they improve.
3. **Parallax doctrine.** Physical camera movement is only legible through parallax, and parallax requires planes that shear against each other. **dolly and truck REQUIRE a named `foreground_anchor`** ("…passing the parked scooter in the left foreground") — the documented failure is a dolly with no parallax cue rendering as a disguised zoom: you pay dolly price, get a flat read. For pedestal/crane/arc the anchor is strongly RECOMMENDED (WARN): on open/aerial frames (a crane over a valley, a drone over a city) there may be no foreground plane — the parallax then comes from background planes shearing, which the prompt should note instead.
4. **Dolly ⇄ zoom fork (intent-driven, never silent).**
   - Intent = dimensional/immersive ("we move into the space") → `dolly` + foreground_anchor.
   - Intent = flat/clinical/surveillance, or a simple reframe, or the background keeps warping on retries → `zoom`.
   - A `dolly` that renders with no parallax = `prompt_adherence` FAIL at review — not an acceptable outcome. A deliberate dolly→zoom fallback is legal but LOGGED in decision_log (core rule 4: no silent demotion).
5. **camera_settle (both ends).** Every move **starts AND ends on a composed frame** — a move that doesn't start composed cannot be cut INTO; a move that doesn't land reads as an accident or a cut-off render. Prompt shape: "opens on [composition], [move], then settles on [final composition]." Reserve the last 10–15% of clip duration for settling (pipeline heuristic, not canon). Distinct from `impact_settle` (animation-motion.md — a body absorbing a landing).
6. **Direction names the CAMERA'S travel**, never the subject's apparent rotation. "arc left" = the camera travels screen-left around the subject (consistent with pan_left = camera rotates left).
7. **When stillness is stronger.** A held static (tableau) implicates the viewer as witness (Ozu, Haneke) — the deliberate refusal of movement is a choice, not an absence. Emotional beats often read better on a static or minimal move than on a showy one; if a move has no motivation (new information or emotional shift), cut it.

## 3. DECISION TABLES

**Emotion/goal → movement**

| Goal | movement | speed | Why |
|---|---|---|---|
| Mounting dread | dolly in | slow | tightens frame, removes escape |
| Intimacy | dolly in | slow | parallax pulls viewer close |
| Isolation / abandonment | dolly out (or zoom out for clinical distance) | slow | negative space grows |
| Grandeur / scale | crane up | slow | subject shrinks into world |
| Wonder / discovery | rise-reveal (crane up + settle) | slow | unveils new information |
| Urgency / chaos | whip_pan, or truck/dolly fast + handheld | fast | kinetic disorientation |
| Shock revelation | dolly_zoom (either direction) | — | world warps, subject fixed |
| Comedy punctuation | crash_zoom | — | breaks rhythm on purpose |
| Moral distance / witness | static (tableau) | — | implicates the viewer |
| Subjective immersion | truck/dolly + support handheld or stabilized, subject_relation follow | normal | embodied presence |
| Hero / product reveal | arc 90–120° | slow | showcases form at low AI risk |
| Empowerment | dolly in + angle low (shot-grammar) | slow–normal | subject dominates frame |
| Scene transition | whip_pan (or POST `hidden_join: whip`) | — | hides the cut |
| Elegant procession | truck + stabilized | slow | dignified, unbroken |

**AI reliability risk register (derived from base — governs retry budget & fallbacks)**

| Tier | Moves | Rule |
|---|---|---|
| GREEN | static, pan, tilt, zoom, dolly, truck, pedestal | generate freely |
| AMBER | crane, arc ≤120°, handheld/stabilized follow, drone | 1 retry, then simplify |
| RED | arc >120°, dolly_zoom, whip_pan, crash_zoom, roll | requires a documented POST fallback in notes BEFORE generation (speed-ramp, canted frame, partial-arc stitch, plate warp) |

**Authoring validators (checked before generation, zero credits)**

| # | Rule | Severity |
|---|---|---|
| V1 | direction ∈ valid set for base | ERROR |
| V2a | base ∈ {dolly, truck} without foreground_anchor | ERROR (renders as a disguised zoom) |
| V2b | base ∈ {pedestal, crane, arc} without foreground_anchor AND without a parallax note | WARN (legal on open/aerial frames) |
| V3 | speed=fast on a translation base | WARN (warping) |
| V4 | dolly_zoom, crash_zoom, whip_pan, or arc_degrees>120 without a post fallback in notes | WARN |
| V5 | more than one movement object on a shot | ERROR |

## 4. NUMERIC ANCHORS

- Pan/tilt judder rule: don't cross a full frame-width (pan) or frame-height (tilt) faster than ~7000ms at 24fps — strobing on high-contrast edges [v — RED Digital Cinema].
- Slow push: 3000–6000ms+ of travel for a subtle read; settle reserve ≈ last 10–15% of clip.
- Arc: state degrees; full 360° needs ≈8000–15000ms to not feel rushed — beyond most single-generation caps, hence partial-arc stitching.
- Dolly_zoom: hold 2000–5000ms+ for the warp to register (craft heuristic).
- Whip_pan / crash_zoom: the in-motion phase is <1000ms by definition.
- Clip ceilings and per-model duration steps: see references/model-matrix.md (dated — verify per campaign).

## 5. ALIASES & DO-NOT-CONFUSE

| Canonical | Aliases (authoring input only — MUST resolve before saving) |
|---|---|
| dolly (in/out) | push in, pull back, push-in, pull-out, slow_push_in (legacy = dolly+in+slow) |
| truck | track, tracking shot, crab |
| crane | jib, boom (boom = the verb for the vertical motion) |
| arc @360 | orbit, 360 orbit, turntable |
| stabilized | steadicam, gimbal (brand/rig distinction has no generation consequence) |
| whip_pan | swish pan, whip tilt (vertical variant folds in) |
| dolly_zoom | zolly, vertigo effect, contra-zoom, trombone shot |
| zoom | (optical change — NOT a movement; "zoom_in/zoom_out" as base names are banned, use base:zoom + direction) |
| movement_intent gloss | push_in, pull_back, reveal, escort, withdraw — allowed as PROSE in notes, never as enum values |

**Do not confuse:**
- **dolly vs zoom** — parallax vs magnification; different meanings, not interchangeable renders (Doctrine 4).
- **roll (motion) vs dutch_deg (held state)** — a canted FRAME is shot-grammar's `dutch_deg`; `roll` is the frame visibly rotating during the clip. If roll keeps failing, a held cant is the reliable substitute.
- **camera_settle vs impact_settle** — a move landing on a composition vs a body absorbing a landing (animation-motion.md).
- **whip_pan (generated move) vs hidden_join: whip (post transition)** — same word, different departments, different cost: generating a whip costs credits and rarely lands the end frame; the post join is free and deterministic. Default to the post join for scene bridges.
- **arc direction** — camera travel, not subject rotation (Doctrine 6).

## 6. AI-GEN CAVEATS

- **Compound moves are the single weakest generation category** [v] — decompose into sequential single-move clips (matches the one-move law).
- **Full 360° orbits melt geometry** — occluded detail is reinvented on reappearance; texture flicker, background warp [v]. Partial arcs ≤120°, stitched in post.
- **Translation without an anchor renders as zoom** — the highest-leverage single fix in this file (Doctrine 3).
- **Fast motion warps subjects** — generate slower, speed-ramp in post.
- **Dolly_zoom is not a trained primitive anywhere** [v] — treat as approximation + post fallback.
- **Identity drifts when the angle changes radically or a new generation starts** — keyframe-first (FF/FLF) is the mitigation; reuse seeds where supported.
- **True oners are impossible in one generation** (duration caps) — stitched_oner with logged hidden joins; never claim "single take."
- **Roll motion smears** — substitute a held dutch_deg frame.
- **Speed modifiers: slow ≫ fast in reliability** [v]; models default slow because gradual change is easier to keep consistent.
