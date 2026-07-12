# Animation & Motion Principles

Read this when: writing motion prompts at /ms-produce; diagnosing motion flaws at clip QA.

Binding source: `docs/filmcraft-rulings.md` (shipped arbitration snapshot). Authorities: Thomas & Johnston, *The Illusion of Life* (1981) · Richard Williams, *Animator's Survival Kit* · 2025 AI-video temporal-drift research.

## Canonical Terms

Columns: Term | KR | Use when | Effect | Prompt phrase/instruction | QA | Caveat.

### The 12 Principles of Animation

| Term | KR | Use when | Effect | Prompt phrase/instruction | QA | Caveat |
|---|---|---|---|---|---|---|
| Squash and Stretch | 스쿼시 앤 스트레치 | Impacts, fast direction changes — keep SUBTLE for photoreal, not cartoon-register | Total absence = rigid/plasticky motion | "subtle compression on impact, slight stretch on the fastest point of the motion, volume preserved" | `motion_quality` axis — inspect impact/direction-change frames for any deformation at all | Gen defaults to rigid-body motion with zero deformation — hard, weightless shells |
| Anticipation | 예비동작 | Any deliberate action (jump, throw, turn) | Missing = causeless, robotic, instant actions | "brief wind-up / weight-shift before the [jump/throw/turn], then the action releases" | `motion_quality` axis — check for a visible wind-up frame before the action's midpoint | Most common gen failure for deliberate actions — jumps straight to the action's midpoint |
| Staging | 스테이징 | Composing so exactly one idea reads at a glance | Gen tends toward busy, multi-motion frames | "single clear readable action, secondary motion minimized, subject isolated against contrasting background" | Pairs with the Gesture Economy validator below — one readable action per clip | Gen is trained on averages, not directed composition — defaults to busy |
| Follow-Through & Overlapping Action | 팔로우 스루·오버래핑 액션 | Loose parts (hair, cloth, limbs) after the body stops | Absence = rigid puppet, everything stops in lockstep | "hair and clothing continue moving and settle a beat after the body stops, trailing limbs lag behind the turn" | `motion_quality` axis — hair/cloth/limb settle checked a few frames past the main stop | Signature AI tell — cloth/hair moves as one rigid sheet or freezes instantly |
| Slow In / Slow Out (Easing) | 슬로우 인·아웃 | Every authored movement, camera or subject | Without it, motion drifts at constant velocity no real mass exhibits | "eases into the motion, decelerates smoothly to a stop, no constant-speed drift" | **`motion_quality` axis (H10) — named example #1.** `flf_adherence` corroborates indirectly (does it actually stop where the LF says) | **THE defining AI motion failure** — the floaty, underwater-glide constant-velocity drift |
| Arcs | 아크(호 궤적) | Any joint-driven motion (limbs, head turns, thrown objects) | Straight-line motion reads mechanical even with correct timing | "motion follows a natural curved arc from the joint, not a straight line" | `motion_quality` axis — trace the motion path across frames, flag straight segments | Gen defaults to linear interpolation between poses unless arced explicitly |
| Secondary Action | 보조 동작 | One small supporting action alongside the main one | Enriches without competing | "add one small supporting gesture [adjusts collar] that doesn't compete with the main action" | Counts toward the Gesture Economy cap below — must not become a second competing action | Gen omits it entirely (dead body during dialogue) or over-generates unrelated simultaneous motion |
| Timing & Spacing (Weight) | 타이밍과 스페이싱 | Any motion where the subject's mass/material must read | Heavy = slow acceleration + wide-spaced extremes; light = quick, even timing | "[heavy: slow acceleration, weighted holds] / [light: quick, evenly-timed motion]" | **`motion_quality` axis (H10) — named example #3 ("weight")** | Gen assigns weight-agnostic timing by default — a boulder and a balloon move on the same curve |
| Exaggeration | 과장 | Pushing pose/expression/timing beyond strict realism, calibrated to style | Buys clarity the model won't supply on its own | "slightly heighten the pose/expression beyond neutral realism for clarity" | Manual — style-calibration judgment call, no mechanical axis | Over-push reads as uncanny in photoreal registers; under-push feeds the generic Appeal deficit below |
| Solid Drawing / Volume Consistency | 솔리드 드로잉(볼륨 일관성) | Any figure moving, turning, or changing pose across a clip | Difference between present-in-space and a flat, unstable image sequence | "consistent anatomical proportions and volume across the turn, no morphing or reshaping" | **`flf_adherence` axis (H6): SSIM/pHash of clip final frame vs supplied last-frame keyframe — measures drift directly** | **THE most notorious gen defect** — melting faces, changing limb lengths, merging fingers; no persistent volumetric model behind the pixels |
| Appeal | 어필 | Character/composition design, every generated figure | Well-designed and legible reads as charismatic, not just correct | (no single token — a design-time property, not a per-clip instruction) | Manual — subjective; check against the locked reference bank, not against the prompt | Default gen output regresses to an averaged, generic "AI look" — counter with deliberate stylization or a locked reference bank |
| Pose-to-Pose vs. Straight-Ahead | 포즈 투 포즈 vs 스트레이트 어헤드 | Always, architecturally — this pipeline's keyframe→I2V IS pose-to-pose | Planning key extremes then filling (controlled) beats generating continuously forward (spontaneous) for drift resistance | "lock to reference keyframe; anchor first/last frame" | **`flf_adherence` axis (H6) — this is the architecture the axis measures compliance for.** SSIM/pHash on final frame vs supplied LF | **Our keyframe→I2V architecture is the industry-verified drift-mitigation** (Sora Character Cameos, LoRA identity locks, FLF conditioning are structurally identical) — state this explicitly when identity drift is questioned |

### Pipeline-Adopted Motion Kit

Real working terms this pipeline needs that are NOT among Thomas & Johnston's historical 12 (see Do-Not-Confuse).

| Term | KR | Use when | Effect | Prompt phrase/instruction | QA | Caveat |
|---|---|---|---|---|---|---|
| Moving Hold | 무빙 홀드 | Any pause/idle beat — a "held" pose that's never fully static | True zero-motion reads as a frozen frame; a moving hold reads as a living being still holding | "subtle idle micro-motion: gentle breathing, slight weight shift, natural blink cycle, no fully static hold" | **`motion_quality` axis (H10) — named example #2 ("moving-hold").** Schema default: `visual_grammar.motion_bible.moving_hold_required = true` | THE direct fix for the most common AI idle-tell — the mannequin look during pauses. A vague "add idle motion" prompt produces uncontrolled drift, not a moving hold — be specific |
| Silhouette Readability | 실루엣 가독성 | Any pose that must read at a glance, especially wide/action shots | Pose identifiable from the solid black outline alone | "clean, unambiguous silhouette; limbs separated, not overlapping; subject value contrasts against background" | Manual — outline test: reduce frame to silhouette, check limb separation | Gen lets subject edges blend into background or limbs overlap into an ambiguous mass |
| impact_settle (Weight & Physicality) | 웨이트·피지컬리티 | Every impact/landing — contact + secondary bounce/absorption | Sells mass: the difference between a hit that lands and one that doesn't | "sharp impact frame on contact, brief settle/absorb afterward, weight transferred into the surface" | `motion_quality` axis; verify contact + settle frames exist. **Do not confuse with `camera_settle`** — see Do-Not-Confuse | Landings routinely show no compression/settle, consistent with models lacking a mass model. Every impact is a guaranteed post-fix point — plan for it |
| Gesture Economy | 제스처 이코노미 | Every clip — cap actions before writing the motion prompt, not after | Reads as directed performance; over-stuffed reads as aimless fidgeting + multiplied artifacts | "single deliberate action for this clip; everything else holds or moves minimally" | **Validator: motion_desc action-count ≤ `visual_grammar.motion_bible.gesture_economy_max` (default 2)** | Single-action prompts measurably reduce artifact surface area — this is a cost/risk control, not just a style preference |
| Line of Action | 라인 오브 액션 | Designing any static or dynamic pose | Strong line = dynamic and intentional; broken = stiff regardless of render detail | "pose built along one strong curved line of action, limbs and torso reinforcing the same directional energy" | Manual — trace one line through the pose; flag if limbs contradict the torso's direction | Photoreal keyframes often have technically clean but "dead" poses with no unifying line |
| Motion Blur & Shutter Angle | 모션 블러·셔터 앵글 | Any clip with fast subject or camera motion — this is a PHOTOGRAPHIC convention, not an animation principle | No blur = strobed/stuttery (cheap-CG and AI tell); matched blur = "filmic" fast motion | "180-degree shutter, natural motion blur trail" / "narrow shutter, crisp staccato motion, minimal blur" | Manual frame-step: blur streak length/direction matches stated shutter + velocity. Schema: `visual_grammar.motion_bible.shutter_look = natural_180` (default) | Gen blur is frequently absent, inconsistent, or speed-mismatched — treat `natural_180` as default unless the shot calls for narrow-shutter staccato |

## Doctrine

- **Physics vocabulary is a STYLE SIGNAL, not a simulation (L9).** Thomas & Johnston called this "the illusion of life" for a reason — squash/stretch, weight, and impact language steer a model toward physically-plausible-LOOKING motion; none of it is actual physics. Don't expect the consistency a simulator would guarantee.
- **Every impact is a guaranteed post-fix point.** Gen models routinely produce weightless landings with no compression/settle. Plan the post pass for every impact shot before generation, not as a contingency.
- **A `physics_risk` flag (물리 리스크 플래그) means a pre-planned cutaway, not a bigger prompt.** If a shot's physics is likely to read wrong (hard impacts, complex contact, fast direction changes), the mitigation is coverage — a cutaway to fall back on in the edit — not more descriptive language. No prompt fully solves physics-blindness.
- **Pose-to-pose via keyframe→I2V is the industry-verified drift-mitigation architecture (L13).** Sora Character Cameos, LoRA identity locks, and first/last-frame conditioning are structurally identical to this pipeline's keyframe method. State this explicitly whenever a stakeholder questions identity drift — this pipeline's architecture IS the state-of-the-art approach, not a workaround.
- **`visual_grammar.motion_bible` (ruling 1.6) hard-codes four of this table's terms as project-wide defaults:** `easing_required: true`, `moving_hold_required: true`, `gesture_economy_max: 2`, `shutter_look: natural_180`. Treat this lexicon's prompt tokens as what SATISFIES those flags, not as optional flourish — the schema is already committed to them.
- **Moving hold is the single highest-leverage micro-fix in this table.** It directly targets the most common AI idle-tell (mannequin freeze) with the cheapest possible prompt addition. Default-inject it into every held beat unless a frozen moment is the deliberate intent.

## Decision Table — AI Motion Flaw → Principle → Prompt Token

| Flaw | Principle | Token |
|---|---|---|
| Floaty constant-velocity drift | Slow In / Slow Out (Easing) | "eases in, decelerates to a hard stop" |
| Frozen/statue pauses | Moving Hold | "idle micro-motion: breathing, weight shift, blink" |
| Instant actions, no wind-up | Anticipation | "brief wind-up before the [action]" |
| Straight mechanical limb paths | Arcs | "natural arcing path from the joint" |
| Hair/cloth stops with body | Follow-Through & Overlapping Action | "hair and hem settle a beat after stopping" |
| Face/body melts between frames | Solid Drawing / Volume Consistency | "consistent proportions and volume, no morphing" |
| Cluttered competing motion | Staging + Gesture Economy | "single clear action; everything else holds" |
| Subject blends into background | Silhouette Readability | "clear silhouette contrast against background" |
| Weightless impacts | impact_settle | "impact frame: contact, compress, settle" |
| No blur / strobing fast motion | Motion Blur & Shutter Angle | "180-degree shutter, natural motion blur trail" |
| Flat lifeless pose | Line of Action / Appeal | "strong line of action, one unifying pose direction" |
| Identity drifts across the clip | Solid Drawing + Pose-to-Pose | "lock to reference keyframe; anchor first/last frame" |

## Numeric Anchors

- Shutter angle formula: speed = 1/(2×fps) at 180° [v]; 24fps → 1/48s [v]. Narrow 45–90° = crisp staccato hyper-real look (e.g. *Saving Private Ryan* combat) [v].
- Frame rates in use: 24/25/29.97/30/48/60 fps.
- Traditional "on 2s": 12 drawings/sec at 24fps [v] — classical animation economy baseline, cited for context only, not a gen-AI parameter.
- Schema default: `visual_grammar.motion_bible.gesture_economy_max = 2` (ruling 1.6) — the only hard numeric cap in this table.
- No numeric tolerance is published for anticipation wind-up length, moving-hold cadence, or easing curve shape — treat as qualitative (consistent with this lexicon's general rejection of unsourced folk numbers, cf. eyeline L11). Don't invent one.

## Aliases & Do-Not-Confuse

- **`impact_settle` vs `camera_settle` (collision ruling N2 — see `docs/filmcraft-rulings.md`).** Both use the word "settle" for unrelated things. `impact_settle` = a physical body absorbing contact force (this file). `camera_settle` = a camera move ending on a composed, static frame (`camera-movement.md`). Never borrow one term's language for the other's concept.
- **"Solid drawing" is inherited vocabulary, not a literal instruction.** This pipeline generates photoreal video, not hand-drawn frames — the term still means volume/proportion consistency across a turn; nobody is asking for a drawn look.
- **Moving hold vs. "just bad animation."** A moving hold is DELIBERATE, controlled, small residual motion (breathing, blink, weight shift). Uncontrolled drift from a vague "add some idle motion" prompt is not a moving hold — it's the same mannequin problem wearing a different prompt.
- **Mickey-mousing is NOT this file's business.** Score literally mimicking on-screen action is a sound-design term (valid in comedy/animation, owned by the audio/editing lexicon's `beat_locked_cutting` discussion) — don't reach for it here even though it sounds animation-adjacent.
- **The 12 Principles vs. the Pipeline-Adopted Motion Kit.** The 12 (first table) are Thomas & Johnston's canonical set. Moving Hold, Silhouette Readability, Line of Action, and Motion Blur & Shutter Angle (second table) are real industry working terms that are NOT among the historical 12 — don't cite them as if Disney's animators named them. **`impact_settle` and Gesture Economy are PIPELINE-COINED labels** (not industry terms at all) for real practices — weight/force absorption on contact, and less-is-more gesture direction respectively; use them in-schema, never in citations.

## AI-Gen Caveats

- **Physics-blind motion.** Gen models model pixel-transition statistics, not physical law — no compression on bounce, weightless impacts by default. Workaround: explicit weight/impact language; treat every impact as a guaranteed post-fix point.
- **Temporal identity drift / morphing.** Hair, eyes, outfits, and proportions mutate over a clip. This pipeline's keyframe-anchoring (pose-to-pose) is the industry-verified mitigation for this — state it explicitly, don't apologize for it.
- **Floaty constant velocity.** The single most common motion complaint. Fix with explicit ease tokens at generation time; curve-based speed ramps are the post-only fallback.
- **Frozen/statue idles.** Any pause defaults to a dead hold unless idle micro-motion is prompted explicitly — generic "add idle motion" phrasing isn't specific enough and produces uncontrolled drift instead.
- **Staging/gesture overload.** Constrain every clip to 1–2 named actions (Gesture Economy). Treat any unprompted extra motion in the output as an artifact to fix, not a bonus.
- **Generic "AI-look" appeal deficit.** Default output regresses to an averaged, generic look. Counter with a locked reference bank and deliberate stylization — not with more descriptive adjectives.
