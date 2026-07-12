# Emotion Recipes — Cross-Department Cookbook

Cross-department recipes: dramatic goal → coordinated technique stack. Read this when: expanding scenes into shots at `/ms-storyboard`; when a beat's FEELING is known but its technique stack is not. Values are canonical filmcraft vocabulary — see per-department references for definitions.

**How to read a row.** A recipe is a CHORD, not a menu — every department plays the same note or the beat fails (§3).
- `size` `angle` `movement` `lens/dof` = shot-level fields. `lighting` `palette` = **scene-level** fields (`scenes[].lighting` is injected byte-identical into every keyframe of the scene).
- `contrast_proxy` is **derived** from `ratio` (byte-stable compiler table) — never invented per shot, never emitted as a number.
- `movement` reads `base·direction·speed·support · anchor`. `foreground_anchor` is REQUIRED for `dolly truck pedestal crane arc` (V2); `speed` is absent for `static whip_pan crash_zoom`; one movement object per shot (V5).
- **`prompt kernel` is a KEYFRAME (T2I) sentence — static by construction.** Camera movement never appears in it (ruling 1.7 ordering fork); the `movement` column renders into the CLIP prompt separately. Kernels carry no ratio numbers, no key-class words, no negations, no hex, no blocklist tokens.
- `{{char:key}}` = identity placeholder resolved by the projection layer. `[product]` = composited locked asset — never text-described.

---

## 1. THE RECIPES

### 1.1 Tension & Threat

| Goal | size | angle | movement | lens/dof | lighting (ratio·dir·qual·K·bias·pattern) | palette & grade | sound & music | edit | prompt kernel (static) |
|---|---|---|---|---|---|---|---|---|---|
| **Mounting Dread \| 고조되는 불안** | `medium_close_up` | `eye_level` | `dolly·in·slow·locked` · anchor: doorframe edge | 50mm / `medium` | `low_key_8_1` · `top` · `hard` · 2200K (sodium) · `dark` · `none` | complementary/mono, sick-green or crushed-cool bias; ffmpeg cool colorbalance + curves crush | strip BG to a low drone; slow riser sparse→dense; hold silence before the hit. Music: harmonic-minor tension, tremolo strings. `score` · `beat_snap: offset` | `cut` only. Shots LENGTHEN toward the beat (ASL rises past 6s). Hold — do not cut on the impact | medium close-up of {{char:hero}} frozen mid-turn toward an unseen sound, cramped hallway, foreground doorframe occluding one edge, single hard overhead practical, shadow side barely visible with only a sliver of detail, 2200K sodium cast, 50mm, medium depth of field |
| **Sudden Shock \| 돌발 충격** | `extreme_close_up` | `eye_level` | `static·locked` (the CUT is the shock). `crash_zoom·in·locked` = licensed break → V4 WARN + post fallback | 85mm / `shallow` | **inherit the scene block byte-identical** — a shock is a SHOT, not a scene. A light change here = a new scene | inherit. Spike via SOUND + CUT, never a mid-scene grade change | dropout 200–500ms pre-impact → hard transient on-frame → post-hit silence. Hole-punch the mix. `sfx.duck_others_ms` | hard `cut` on the transient. Deliberate 3-rung size jump (flags the ≤2-rung validator — expected, §5) | extreme close-up of [the object], hard-lit detail filling the frame, the same single overhead source as the room, shadow side barely visible with only a sliver of detail, 85mm, shallow depth of field |
| **Suspense (audience knows) \| 서스펜스 (관객 우위)** | `wide` | `eye_level` | `static·locked` — the held tableau implicates the viewer | 28mm / `deep` | `standard_4_1` · `front_left` · `soft` · 3200K · `neutral` · `loop` — **deliberately innocent** (§5) | baseline, cooling begins; contrast slightly up (rising-complication row) | strip BG, low drone under; relentless minor ostinato, pulsing low strings. Music = pressure, never announcement. `score` · `offset` | LONG holds; `cut` on look (they glance and MISS it); cross-cut alternation accelerates as convergence nears | wide shot, {{char:hero}} absorbed in a task in the foreground, the intruder standing still and unnoticed in the deep background plane, ordinary soft window light from front-left, clear shadow side with visible but detailed shadow, 3200K, 28mm, deep depth of field, depth-staged composition |
| **Unease / Wrongness \| 불편함·이물감** | `medium_close_up` | `eye_level` · `dutch_deg: 10` | `static·locked` + `centered_symmetry` (order that is *too* ordered) | 21mm / `deep` (edge distortion at close distance) | `standard_4_1` · `top` · `hard` · 4000K (fluorescent + green spike) · `neutral` · `none` | complementary/mono, sick-green mids; ffmpeg cool + curves crush | atonal whole-tone clusters, prepared piano, dreamlike and uncanny. A room hum that should not be there. Ambience stays **anempathetic** — mechanically oblivious, not ironic | `cut`. Hold one beat past comfort. **Jump cut licensed** (<30°, same scale) — the defect is the point (§5) | medium close-up of {{char:hero}} centered and symmetrical in a sterile corridor, canted 10 degrees, hard overhead fluorescent light with a green spike, clear shadow side with visible but detailed shadow, 4000K, 21mm at close distance with edge distortion, deep depth of field |

### 1.2 Intimacy & Connection

| Goal | size | angle | movement | lens/dof | lighting (ratio·dir·qual·K·bias·pattern) | palette & grade | sound & music | edit | prompt kernel (static) |
|---|---|---|---|---|---|---|---|---|---|
| **Intimacy / Tenderness \| 친밀함·다정함** | `medium_close_up` | `eye_level` | `dolly·in·slow·locked` · anchor: the near shoulder | 85mm / `shallow` | `mild_2_1` · `front_left` · `soft` · 2800K (household) · `neutral` · `loop` | analogous warm; warm colorbalance, lifted blacks | close perspective, audible breath; sparse solo instrument, restraint. Silence carries more than the cue. `score` · `offset` | ASL lengthens (8s+); `cut` on look; matched `ots` singles, `dirty` (⟹ `shallow` auto) | medium close-up of {{char:a}} leaning in, hands still on the table, warm domestic interior, large soft loop-pattern key from front-left, gentle modeling with the shadow side one stop under and soft shadow detail, 2800K, 85mm, shallow depth of field |
| **Romance \| 로맨스** | `medium` · `two_shot` (exactly 2, by count) | `eye_level` | `arc·left·slow·stabilized` · `arc_degrees: 90` · anchor: the foreground hedge — **partial arc, never a full orbit** | 50mm / `shallow` | `mild_2_1` · `back_left` · `soft` · 3400K (`golden_hour`) · `bright` · `rim` | analogous warm; `kodak_portra_400`, `diffusion: light`; warm colorbalance, lifted blacks | warm major-key orchestral, open string voicings, hopeful and resolved. **Music enters AFTER the key line, then swells** — confirmation, not anticipation | `cut` on look; `dissolve` 1200ms for the montage tier; two_shot ⇄ `ots` singles | medium two-shot of {{char:a}} and {{char:b}} facing each other at golden hour, soft backlight from back-left rimming both figures, gentle modeling with the shadow side one stop under and soft shadow detail, 3400K, 50mm, shallow depth of field, Kodak Portra 400 |
| **Trust / Authority \| 신뢰·권위** | `medium_close_up` | `eye_level` (an angle is an argument — §3) · `gaze_target: to_camera` | `static·locked` — stillness IS credibility; drift undermines it | 85mm / `shallow` | `mild_2_1` · `front_left` · `soft` · 4000K · `bright` · `broad` | cool complementary, blue-cool; raised gamma; skin held on the vectorscope line (≈123°) | dialogue-forward, minimal ambience, room tone under pauses; subtle underscore, **never wall-to-wall**. `audio.voiceover.mode: character_sync` | `cut`; long holds; `function: cutaway` to hands/product hides the trims (H4: scene ≥3 shots ⟹ ≥1 insert\|cutaway\|reaction) | medium close-up of {{char:founder}} seated and still, addressing the lens directly, office interior softly out of focus behind, large soft frontal key from front-left with even fill, gentle modeling with the shadow side one stop under and soft shadow detail, 4000K, 85mm, shallow depth of field |
| **Vulnerability / Confession \| 취약함·고백** | `close_up` | `high` (diminish) | `static·locked` — the confession is a HOLD | 85mm / `shallow` | `standard_4_1` · `side_left` · `soft` · 3200K · `dark` · `rembrandt` | desaturated, lifted blacks, flat curve (the numb variant, not the crushed one) | close and dry; audible breath; ambience thins 1–2s before the line. Solo piano, unaccompanied, extremely sparse. `audio.voiceover.mode: internal_monologue` when interior | hold long; `cut` on look; the LISTENER's `function: reaction` shot is the payoff. Cut on question | close-up of {{char:hero}} from a high angle, eyes down, chin tucked, bare room with one lamp, soft Rembrandt key from side-left, clear shadow side with visible but detailed shadow, 3200K, 85mm, shallow depth of field |

### 1.3 Power & Scale

| Goal | size | angle | movement | lens/dof | lighting (ratio·dir·qual·K·bias·pattern) | palette & grade | sound & music | edit | prompt kernel (static) |
|---|---|---|---|---|---|---|---|---|---|
| **Power / Dominance \| 권력·지배** | `medium_full` | `low` | `dolly·in·slow·locked` · anchor: the foreground desk edge | 28mm / `medium` (foreground-driven) | `low_key_8_1` · `top` · `hard` · 3200K (tungsten) · `dark` · `none` | complementary; warm tungsten key against cool ambient; contrast up, shadows crushed | chromatic descending brass and low piano, sense of doom. Wide room tone = a big room. Everyone else falls silent when they speak | `cut`. The dominant HOLDS; the subordinate gets shorter shots — **asymmetric ASL is power made rhythmic** | medium full shot of {{char:boss}} from a low angle behind a foreground desk edge, standing squared to the lens, hard tungsten top light in a dark panelled office, shadow side barely visible with only a sliver of detail, 3200K, underexposed, 28mm, medium depth of field |
| **Awe / Scale \| 경외·스케일** | `extreme_wide` | `high` | `crane·up·slow·drone` · anchor: the foreground ridgeline | 24mm / `deep` | `standard_4_1` · `back_right` · `hard` · 3400K (`golden_hour`) · `bright` · `rim` | complementary (warm key vs cool sky); saturated; grade at prompt level + moderate colorbalance | the sound OPENS: wide ambience, long reverb tail, sub floor. Swell enters ON the reveal, after the cut | HOLD long (an EWS needs scan time). Preceded by a tight shot — the size jump MAKES the scale (breaks ≤2-rung, §5). **Pair with an MCU reaction** (§3 H2 floor) | extreme wide shot, {{char:hero}} a small figure on a foreground ridgeline against a vast valley, hard golden-hour sun from back-right rimming the ridge, clear shadow side with visible but detailed shadow, 3400K, 24mm, deep depth of field, depth-staged composition |
| **Triumph / Liberation \| 승리·해방** | `full` | `low` | `crane·up·slow·stabilized` · anchor: the foreground barrier | 35mm / `deep` | `mild_2_1` · `back_left` · `hard` · 5600K · `bright` · `rim` | saturation returns **above** baseline; warms again; contrast normalizes, softer highlight rolloff | warm major-key orchestral, open string voicings. The music BREAKS OUT — it has been withheld. This is the one beat that earns a full swell | `cut` on action, accelerate INTO the beat, then HOLD on the payoff — **the release lives in the hold**. `fade_through_black` legal iff the act closes | full shot of {{char:hero}} from a low angle, arms open, standing in a cavernous hall with expansive negative space, hard backlight from back-left, gentle modeling with the shadow side one stop under and soft shadow detail, 5600K, slightly overexposed, 35mm, deep depth of field |
| **Urgency / Chaos \| 긴박·혼돈** | `medium` | `eye_level` · `dutch_deg: 12` | `pan·right·fast·handheld` · `subject_relation: follow` (whip_pan is a *seam*, not a shot — §5) | 24mm / `deep` | `standard_4_1` · `back_right` · `hard` · 5600K cool ambient, warm practicals as motivation · `neutral` · `rim` | complementary; teal shadow / orange skin; moderate colorbalance, high contrast | dense layered beds → **dropout before the impact**. Relentless minor ostinato, pulsing low strings, driving percussion. `beat_snap: offset` in narrative; `snap` only in hype-montage | ASL collapses to 1–2s; `cut` on action mid-motion (2–6f overlap); pattern interrupt every 3–5s; `hidden_join: whip` on the seams | medium shot of {{char:hero}} mid-stride shoving through a crowd, handheld framing canted 12 degrees, hard cool backlight from back-right with warm practicals behind, clear shadow side with visible but detailed shadow, 5600K, 24mm, deep depth of field |
| **Determination / Resolve \| 결의·의지** | `medium_full` | `low` | `dolly·out·normal·locked` · `subject_relation: lead` · anchor: the foreground doorway — the camera GIVES GROUND | 50mm / `medium` | `standard_4_1` · `back_left` · `hard` · 5600K · `neutral` · `rim` | saturation normalizing and firming; contrast firming | minor ostinato building. **Footsteps clear and on-frame** — hero-walking shots without footsteps are a delivery-gate BLOCK, not a taste call | the shot HOLDS. ASL lengthens against the chaos it follows. `cut` · `screen_direction: toward_camera` | medium full shot of {{char:hero}} walking directly toward the lens, jaw set, shoulders squared, a burning corridor behind, hard backlight from back-left, clear shadow side with visible but detailed shadow, 5600K, 50mm, medium depth of field |

### 1.4 Loss & Interiority

| Goal | size | angle | movement | lens/dof | lighting (ratio·dir·qual·K·bias·pattern) | palette & grade | sound & music | edit | prompt kernel (static) |
|---|---|---|---|---|---|---|---|---|---|
| **Isolation / Loneliness \| 고립·외로움** | `extreme_wide` | `high` | `dolly·out·slow·locked` · anchor: the foreground railing · *fork: `zoom·out` if the register is flat/clinical/surveillance* | 28mm / `deep` | `flat_1_1` · `ambient` · `soft` · 7000K (`overcast`) · **`dark`** · `none` — flat ratio + dark bias is the numb look, and the reason `exposure_bias` is a SEPARATE field | desaturated cool; low sat + cool colorbalance + flattened curve | ambience only, far perspective. Music absent or one sustained tone. Floor still applies: ≥1 ambience bed per location | long holds; `cut`; the subject ENTERS and EXITS — bracket with `framing: empty_frame`. `dissolve` for time passing | extreme wide shot from a high angle, {{char:hero}} small and off-center against an empty plaza, soft overcast ambient light, flat even illumination, shadow side as bright as the key, seamless shadowless light, 7000K, underexposed, 28mm, deep depth of field, negative-space composition |
| **Grief \| 비탄·상실** | `medium_close_up` (H2 floor) — paired with a held `full` `function: master` tableau | `eye_level` | `static·locked` — the witness frame. The camera does not editorialize | 50mm / `medium` | `standard_4_1` · `side_left` · `soft` · 5600K (`interior_day`, window key) · `dark` · `loop` | most desaturated, coolest; **flattest (numb)**, not crushed | silence-forward. Ambience continues indifferently — a clock, a fridge (anempathetic). Solo piano, unaccompanied, room to breathe, entering AFTER the beat | the LONGEST holds in the piece. `cut`. `fade_through_black` iff the act closes here | medium close-up of {{char:hero}} bowed, one hand flattening slowly on the tabletop and staying there, an untouched room behind, soft window key from side-left, clear shadow side with visible but detailed shadow, 5600K, underexposed, 50mm, medium depth of field |
| **Nostalgia / Memory \| 향수·기억** | `medium_full` | `eye_level` (`low` reads as a child's memory) | `pan·right·slow·handheld` — the home-movie drift (`pan` ∉ TRANSLATION ⟹ anchor exempt) | 35mm / `medium` | `mild_2_1` · `back_right` · `soft` · 3400K (`golden_hour`) · `bright` · `rim` | analogous warm, saturation slightly above baseline; `super8` stock + `grain: super8` + `diffusion: medium`; warm colorbalance, lifted blacks | pentatonic major, plucked harp and acoustic guitar, nostalgic. Perspective distant and filtered. `diegesis: trans_diegetic` crosses the memory boundary; `audio.voiceover.mode: internal_monologue` | `dissolve` — the canonical memory transition (1200ms; ellipsis-tier 3000–5000ms for a long jump). `dip_to_white` sparingly (dated) | medium full shot of {{char:mother}} mid-laugh in a sunlit backyard, warm golden-hour backlight from back-right, gentle modeling with the shadow side one stop under and soft shadow detail, 3400K, slightly overexposed, 35mm, medium depth of field, Super 8 grain |
| **Interiority / Dissociation \| 내면·해리** | `medium_close_up` | `eye_level` · `dutch_deg: 5` | `dolly_zoom·in·slow·locked` — RED: V4 WARN + documented post fallback REQUIRED. Hold 2–5s+ or the warp never registers | 50mm / `shallow` (the keyframe carries ONE lens; the focal warp is a clip-time effect) | `mild_2_1` · `ambient` · `soft` · 4000K · `neutral` · `none` — sourceless, unreal light | pastel/desaturated, soft, lifted, low contrast (the numb-flat variant) | atonal whole-tone clusters, prepared piano. The room DUCKS away; breath stays close and dry. `audio.voiceover.mode: internal_monologue` = non-diegetic ducking + close/dry perspective | the shot runs LONG, past comfort. `cut` in, `dissolve` out. `function: cutaway` to an unrelated detail = the mind wandering | medium close-up of {{char:hero}} staring past the lens, face still, a crowded room falling out of focus behind, soft sourceless ambient light, gentle modeling with the shadow side one stop under and soft shadow detail, 4000K, 50mm, shallow depth of field, canted 5 degrees |

### 1.5 Joy & Release

| Goal | size | angle | movement | lens/dof | lighting (ratio·dir·qual·K·bias·pattern) | palette & grade | sound & music | edit | prompt kernel (static) |
|---|---|---|---|---|---|---|---|---|---|
| **Joy / Playfulness \| 기쁨·장난기** | `medium_full` (joy is physical — bodies need room) | `eye_level` | `truck·left·normal·stabilized` · `subject_relation: follow` · anchor: the foreground hedge | 35mm / `medium` | `mild_2_1` · `front_left` · `soft` · 5600K (`day`) · `bright` · `broad` | saturated warm, above baseline; analogous or triadic; soft rolloff, lifted blacks | pentatonic major, plucked harp and acoustic guitar; diegetic laughter, footfalls, wind. `beat_snap: snap` licensed iff `type: montage_sequence` | brisk ASL 2–4s; `cut` on action; `dissolve` for a joy montage (`cut_sync: beat_grid` legal here) | medium full shot of {{char:hero}} mid-run through a sunlit park, arms loose, laughing, soft broad daylight key from front-left, gentle modeling with the shadow side one stop under and soft shadow detail, 5600K, slightly overexposed, 35mm, medium depth of field |
| **Comedy Beat \| 코미디 비트** | `medium` (the gag needs the whole body legible) | `eye_level` · `dutch_deg: 0` · `centered_symmetry` | `crash_zoom·in·locked` — RED: V4 WARN. Fallback = a hard `cut` to a tighter size, and it works | 35mm / `deep` — deep focus keeps the gag readable | `flat_1_1` · `front` · `soft` · 5600K · `bright` · `broad` — **the flat light is the straight man** | neutral, natural saturation; the grade NORMALIZES. A moody grade kills the joke | tight exaggerated synced hits. **Literal sync (Mickey-Mousing) is CRAFT here — the only genre where it is** (§5). Post-hit silence for the reaction. `beat_snap: snap` | beat-snap licensed. `cut` on the transient. The `function: reaction` shot is the punchline — hold it one beat past comfort. Rule of three needs near-identical size/angle/lens across 3 clips | medium shot of {{char:hero}} deadpan and centred, a chaotic mess behind them, soft frontal light, flat even illumination, shadow side as bright as the key, seamless shadowless light, bright exposure, 5600K, 35mm, deep depth of field, centered symmetrical composition |
| **Wonder / Discovery \| 경이·발견** | `wide` (the reveal) — **MANDATORY pair** with an MCU-or-tighter `function: reaction` | `low` | `pedestal·up·slow·stabilized` · anchor: the foreground fern — the rise-reveal, then settle | 28mm / `deep` | `standard_4_1` · `back_right` · `hard` · 5600K · `bright` · `rim` · motivation: sun through the canopy | triadic, saturation above baseline; heightened at prompt level | lydian mode, bright synth and celesta, sense of wonder. The new space's ambience **pre-laps** under the previous shot — `audio.ambience[].in` = cut time − 330…1000ms (cue placement, sound-music D7). Music enters AFTER | reveal → HOLD. `cut` on look. Music as confirmation, not anticipation. `dissolve` iff time passes | wide shot from a low angle, {{char:hero}} small at the frame edge looking up, a vast canopy opening above with hard sun shafts from back-right, clear shadow side with visible but detailed shadow, 5600K, slightly overexposed, 28mm, deep depth of field, leading-lines composition |

### 1.6 Commercial Beats

| Goal | size | angle | movement | lens/dof | lighting (ratio·dir·qual·K·bias·pattern) | palette & grade | sound & music | edit | prompt kernel (static) |
|---|---|---|---|---|---|---|---|---|---|
| **Product Hero / Desire \| 제품 히어로·욕망** | `close_up` · `single` | `low` | `arc·left·slow·stabilized` · `arc_degrees: 90` · anchor: the pedestal edge — **partial arc, never a full orbit** (arc>120 = RED) | 85mm / `shallow` | `low_key_8_1` · `side_right` · `soft` key + hard rim · 5600K · `dark` · `rim` · motivation: one softbox above-right, background falling to black | brand palette at 60/30/10. **The exact brand colour is achieved in ffmpeg, never prompted** (hex is a blocking lint). The label/logo is COMPOSITED from a locked asset — never text-described (greeking) | designed hyper-real material sound: the click, the snap, the pour. **A hard FX on every visible impact is a delivery-gate BLOCK.** Music minimal, textural, building | short rhythmic `function: insert` cuts. Note: `insert` auto-suggests `generation_strategy: stock` — **that suggestion does NOT apply to a branded asset** (§5) | close-up of [product] on a pedestal from a slightly low angle, isolated in negative space, single soft key from side-right with a hard rim, background falling to black, shadow side barely visible with only a sliver of detail, 5600K, 85mm, shallow depth of field |
| **CTA / Close \| CTA·클로징** | `medium` · `single` or `empty_frame` | `eye_level` · `gaze_target: to_camera` | `static·locked` — **always.** Any movement fights the text burn-in | 50mm / `shallow` (text reads over a soft background) | `mild_2_1` · `front_left` · `soft` · 5600K · `bright` · `broad` | brand palette; the accent colour is reserved for the CTA element (the "10" of 60/30/10). Exact hex in ffmpeg post | VO + on-screen text on BOTH channels (>60% mobile is sound-off). Duck music 9–12 dB under VO. The final cadence lands ON the logo. Budget: EN :30 ≈ 60–80 words · KR :30 ≈ 150–170 음절 [provisional, P6-1] | the longest static HOLD in the piece (the eye must read, then act). `cut` in; `end_fade_ms` on the tail. This is one of the ≤3 beat-sync tentpoles | medium shot, [product] centered with clean negative space reserved in the lower third of the frame, soft even frontal key from front-left, gentle modeling with the shadow side one stop under and soft shadow detail, 5600K, 50mm, shallow depth of field — **all copy burns in post; the generated plate carries image only** |

---

## 2. COMBINATION RULES (doctrine)

### R1 — Departments must AGREE. A recipe is a chord; a department playing a different chord is a defect.
Canonical incompatibilities (each is a lint candidate, not a style opinion):

| Contradiction | Why it fails |
|---|---|
| dread/horror × `flat_1_1` or `exposure_bias: bright` | The light disarms the threat. Dread needs `low_key_8_1`+ and `dark`. |
| comedy × `low_key_8_1` / `extreme_16_1` / `shallow` | A graded, isolated gag is not funny. Comedy needs `flat_1_1`–`mild_2_1` and `deep`. |
| intimacy × `extreme_wide` + `deep` | Contradicts proxemics: intimate distance maps to CU/ECU, not to a landscape. |
| trust/authority × `low` or `high` angle | An angle is an argument. `eye_level` is the trust axis; a low-angle founder reads as a threat. |
| grief × warm/saturated grade | Contradicts the color-script low-point row (most desaturated, coolest). |
| **suspense × horror lighting** | Announces the threat and destroys the dramatic irony. The audience's KNOWLEDGE is the weapon — not the key light. |
| awe/scale × `shallow` | Scale is built from depth cues; shallow DoF destroys them. |
| CTA × any `movement.base ≠ static` | The move fights the burn-in and the read. |
| product/CTA × prompted brand hex or described logo | Blocking lint + legal exposure. Composite from a locked asset. |
| any recipe × a key-class word ("high-key") or a bare ratio ("8:1") in a prompt | Models read "high-key" as *bright*. Emit the `contrast_proxy` string instead. |
| narrative recipe × `cut_sync: beat_grid` | Trips `beat_locked_cutting`. A beat grid driving cuts INVERTS Murch's Rule of Six (rhythm 10% < emotion 51%). Licensed only for comedy/hype-montage. |

**H2 floor (interior state).** Any shot whose JOB is a character's interior state = `medium_close_up` or tighter AND a described playable physical **verb**, never an adjective ("her hand flattens on the tabletop and stays there", not "she is grieving"). Recipes that live wide — isolation, awe, wonder, grief's tableau — must PAIR the wide with an MCU-or-tighter `function: reaction`: **the wide carries the situation, the tight carries the state.** Isolation is the single exception where the frame *is* the emotion (negative space) — the pairing still applies to the reaction that follows.

### R2 — Escalation = amplitude increase, not sign alternation.
**"Kind" is formally the scene's value-shift DIRECTION: `+→−` or `−→+`** (story-structure.md: `value_shift{from,to}` + the polarity-progression row). Requirement: `scene(n).kind ≠ scene(n+1).kind` **AND** `|delta(n+1)| > |delta(n)|` through the midpoint. Two consecutive scenes on the same recipe at the same amplitude = **flatline** — the exact defect the value-shift rule exists to catch. Amplitude is raised by moving departments together:

| Axis | Escalation direction |
|---|---|
| shot_size | tightens along the ladder (`wide`→`medium`→`close_up`) — but ≤2 rungs per step inside a scene |
| lighting ratio | deepens (`mild_2_1`→`standard_4_1`→`low_key_8_1`→`extreme_16_1`) |
| lens_mm | departs from the ~50mm normal in either direction (compress or distort) |
| ASL | shortens — **except dread, which escalates by LENGTHENING.** The inversion is the point |
| saturation | departs baseline → most desaturated at the low point → returns **above** baseline at resolution |
| music | density rises. The one available move above maximum density is **silence before the hit** — the highest-amplitude gesture in the kit |

### R3 — One dominant recipe per scene. Recipe changes happen at scene boundaries.
This is a **schema consequence**, not a preference: `scenes[].lighting` is injected byte-identical into every keyframe of the scene, and the validator `distinct(lighting_sentence) per scene == 1` FAILS otherwise. Therefore:
- A recipe change **is** a scene boundary. dread → shock → grief is either three scenes, or one dread scene in which shock and grief are SHOT-level beats living under the dread lighting block.
- Shot-level beats (`insert`, `cutaway`, `reaction`, the shock) **inherit the scene lighting** and escalate only through size / angle / movement / sound / cut.
- A genuine mid-scene light change (the lamp goes out) is legal ONLY with `lighting_override_reason` logged — the schema equivalent of telling the script supervisor before you move the key.
- Boundary transition semantics: `cut` = no meaning · `soft_cut` (200–400ms) = **technical repair only, carries no time**, and head-trim is tried first · `dissolve` (1200ms; 3000–5000ms ellipsis tier) = time passed · `fade_through_black` = act/chapter punctuation, **RESERVED** — a recipe change alone does not earn it.

### R4 — Format overrides: shorts compress recipes to hook grammar.
- Hook clamped **≤3s absolute** — intro-retention (past 3s) target ≥70%; strong hooks hold 80–90% through the first 3s; pattern interrupt every 3–5s (owner: editing-grammar) [v, vendor-analytics sourced — mirrors story-structure.md §Numeric Anchors].
- **<20s → 3 beats** (hook / turn / payoff): ONE recipe for the hook, ONE for the payoff. **No establisher** — format wins (H3); where one is truly needed, `function: establishing` → stock candidate.
- Cuts every 2–4s; pattern interrupt every 3–5s. A recipe whose payoff needs an 8s hold does not survive a short — pick a different recipe, do not compress the hold.
- **9:16:** subject in the 15–40% zone from the top; bottom 15–25% is caption-unsafe → the recipe's composition must reserve it. Compose natively; do not centre-crop from 16:9.
- **>60% mobile sound-off:** every recipe's sound layer needs a VISUAL twin. **A recipe whose emotion lives only in the score does not survive shorts.** On-screen text is the cheapest, most reliable channel.
- Wall-to-wall music is CORRECT for 15–60s music-led shorts; the ≥95%-of-timeline WARN gates to `cinematic_short|longform` only.
- `beat_snap`: comedy/hype/montage → `snap`; cinematic/brand/longform → `offset` (60–150ms).

---

## 3. WORKED EXAMPLES

### A. Thriller cold open — 30s, 3 scenes. Demonstrates R3 (shock as a SHOT, not a scene).
```jsonc
// Escalation: standard_4_1 → low_key_8_1 → mild_2_1(ambient/unreal).  ASL: long → longest → numb.
s1  recipe: suspense_audience_knows          // end_polarity: unease (small delta)
    lighting: { time_of_day: interior_night, key_direction: front_left, key_quality: soft,
                ratio: standard_4_1, contrast_proxy: "clear shadow side, visible but detailed shadow",
                color_temp_k: 3200, pattern: loop, exposure_bias: neutral,
                motivation: "the desk lamp is the ONLY light source in the room" }
    sh1 { shot_size: wide, angle: eye_level, framing: single, lens_mm: 28, dof: deep,
          composition_tags: [depth_staged, foreground_occlusion], function: master,
          screen_direction: neutral, movement: { base: static, support: locked } }
    sh2 { shot_size: medium_close_up, angle: eye_level, framing: single, lens_mm: 50, dof: shallow,
          gaze_target: off_left, function: reaction, movement: { base: static, support: locked } }
    audio: { music_cues: [{ cue_id: M1, diegesis: score, why: "slow riser under the suspense hold" }],
             beat_snap: { mode: offset, offset_ms: 90 } }

s2  recipe: mounting_dread  →  the SHOCK is sh5, a shot inside this scene    // end_polarity: fear (delta ↑↑)
    transition_in: { type: cut }                       // recipe change = scene boundary
    lighting: { time_of_day: interior_night, key_direction: top, key_quality: hard,
                ratio: low_key_8_1, contrast_proxy: "shadow side barely visible, deep shadow, only a sliver of detail",
                color_temp_k: 2200, pattern: none, exposure_bias: dark,
                motivation: "a single sodium streetlamp through the blinds" }
    sh3 { shot_size: medium_close_up, angle: eye_level, lens_mm: 50, dof: medium,
          movement: { base: dolly, direction: in, speed: slow, support: locked,
                      foreground_anchor: "the doorframe edge in the foreground" } }
    sh4 { shot_size: medium, angle: eye_level, lens_mm: 50, dof: medium, function: reaction,
          gaze_target: off_right, movement: { base: static, support: locked } }
    sh5 { shot_size: extreme_close_up, angle: eye_level, lens_mm: 85, dof: shallow,   // ← SHOCK
          movement: { base: static, support: locked },
          notes: "3-rung ladder jump — deliberate; the jump IS the beat. Lighting INHERITED, unchanged." }
    audio: { sfx: [{ id: X1, at_sec: 18.4, duck_others_ms: 400 }] }   // dropout → transient → silence

s3  recipe: interiority_dissociation                                    // end_polarity: numb (delta ↑↑↑)
    transition_in: { type: cut }
    lighting: { key_direction: ambient, key_quality: soft, ratio: mild_2_1,
                contrast_proxy: "gentle modeling, shadow side one stop under, soft shadow detail",
                color_temp_k: 4000, pattern: none, exposure_bias: neutral, motivation: null }
    sh6 { shot_size: medium_close_up, angle: eye_level, dutch_deg: 5, lens_mm: 50, dof: shallow,
          movement: { base: dolly_zoom, direction: in, speed: slow, support: locked,
                      foreground_anchor: "the overturned chair" },
          notes: "V4 WARN (dolly_zoom = RED). Post fallback: static plate + focus-breathing grade." }
    audio: { vo: { mode: internal_monologue } }        // non-diegetic ducking + close/dry perspective
    end: { end_fade_ms: 900 }
```

### B. Brand PAS 30s — problem → solution → close. Demonstrates R4 (format) + commercial rules.
```jsonc
s1  recipe: unease_wrongness            // PROBLEM.  hook ≤3s, no establisher (H3)
    lighting: { time_of_day: interior_day, key_direction: top, key_quality: hard, ratio: standard_4_1,
                contrast_proxy: "clear shadow side, visible but detailed shadow",
                color_temp_k: 4000, pattern: none, exposure_bias: neutral,
                motivation: "overhead office fluorescents" }
    sh1 { shot_size: medium_close_up, angle: eye_level, dutch_deg: 10, lens_mm: 21, dof: deep,
          composition_tags: [centered_symmetry], movement: { base: static, support: locked } }
    sh2 { shot_size: extreme_close_up, angle: eye_level, lens_mm: 85, dof: shallow, function: insert }

s2  recipe: determination_resolve       // SOLUTION.  amplitude ↑: ratio holds, ASL lengthens, sat rises
    transition_in: { type: cut }
    lighting: { time_of_day: day, key_direction: back_left, key_quality: hard, ratio: standard_4_1,
                contrast_proxy: "clear shadow side, visible but detailed shadow",
                color_temp_k: 5600, pattern: rim, exposure_bias: neutral, motivation: "low sun down the street" }
    sh3 { shot_size: medium_full, angle: low, lens_mm: 50, dof: medium, screen_direction: toward_camera,
          movement: { base: dolly, direction: out, speed: normal, support: locked,
                      subject_relation: lead, foreground_anchor: "the foreground doorway" } }
    audio: { sfx: [{ id: X2, at_sec: 12.0 }] }   // footsteps — hero-walking floor, BLOCKING

s3  recipe: product_hero_desire  →  CTA is sh6, a shot inside this scene
    transition_in: { type: cut }
    lighting: { key_direction: side_right, key_quality: soft, ratio: low_key_8_1,
                contrast_proxy: "shadow side barely visible, deep shadow, only a sliver of detail",
                color_temp_k: 5600, pattern: rim, exposure_bias: dark,
                motivation: "one softbox above-right; the background falls to black" }
    palette_note: "brand accent at 60/30/10; exact hex achieved in ffmpeg, never prompted"
    sh4 { shot_size: close_up, angle: low, framing: single, lens_mm: 85, dof: shallow,
          movement: { base: arc, direction: left, speed: slow, support: stabilized,
                      arc_degrees: 90, foreground_anchor: "the pedestal edge" },
          notes: "label COMPOSITED from locked asset — stock auto-suggest does not apply" }
    sh5 { shot_size: extreme_close_up, angle: eye_level, lens_mm: 85, dof: shallow, function: insert }
    sh6 { shot_size: medium, angle: eye_level, framing: single, gaze_target: to_camera,   // ← CTA
          lens_mm: 50, dof: shallow, composition_tags: [negative_space],
          movement: { base: static, support: locked },
          notes: "lower third reserved for burn-in. 9:16: bottom 15–25% caption-unsafe. No baked text." }
    audio: { beat_snap: { mode: offset, offset_ms: 90 } }   // CTA = 1 of the ≤3 sync tentpoles
    end: { end_fade_ms: 600 }
```

### C. Character arc — grief → memory → liberation. Demonstrates R2 (saturation arc) + transition semantics.
```jsonc
s1  recipe: grief                                       // color script: MOST desaturated, coolest, flattest
    lighting: { time_of_day: interior_day, key_direction: side_left, key_quality: soft, ratio: standard_4_1,
                contrast_proxy: "clear shadow side, visible but detailed shadow",
                color_temp_k: 5600, pattern: loop, exposure_bias: dark, motivation: "the one window" }
    sh1 { shot_size: full, angle: eye_level, framing: single, lens_mm: 50, dof: medium,
          function: master, movement: { base: static, support: locked } }        // the witness tableau
    sh2 { shot_size: medium_close_up, angle: eye_level, lens_mm: 50, dof: medium,
          movement: { base: static, support: locked },
          notes: "H2: the interior-state beat. Playable verb — 'one hand flattens on the tabletop and stays there'." }

s2  recipe: nostalgia_memory                            // saturation lifts ABOVE baseline; warm
    transition_in: { type: dissolve, duration_ms: 3200 }     // ellipsis tier — time passed, substantially
    lighting: { time_of_day: golden_hour, key_direction: back_right, key_quality: soft, ratio: mild_2_1,
                contrast_proxy: "gentle modeling, shadow side one stop under, soft shadow detail",
                color_temp_k: 3400, pattern: rim, exposure_bias: bright, motivation: "the late sun" }
    palette_note: "super8 stock + super8 grain + medium diffusion; warm colorbalance, lifted blacks"
    sh3 { shot_size: medium_full, angle: low, lens_mm: 35, dof: medium,
          movement: { base: pan, direction: right, speed: slow, support: handheld } }
    audio: { music_cues: [{ cue_id: M2, diegesis: trans_diegetic,
                            why: "the theme crosses the memory boundary", derived_from: M1,
                            transform: { pitch_semitones: 0, tempo_ratio: 0.85 } }] }  // leitmotif: SAME stem

s3  recipe: triumph_liberation                          // saturation returns above baseline; warms; rolloff softens
    transition_in: { type: dissolve, duration_ms: 1200 }
    lighting: { time_of_day: day, key_direction: back_left, key_quality: hard, ratio: mild_2_1,
                contrast_proxy: "gentle modeling, shadow side one stop under, soft shadow detail",
                color_temp_k: 5600, pattern: rim, exposure_bias: bright, motivation: "open sky" }
    sh4 { shot_size: full, angle: low, framing: single, lens_mm: 35, dof: deep,
          movement: { base: crane, direction: up, speed: slow, support: stabilized,
                      foreground_anchor: "the foreground barrier" } }
    sh5 { shot_size: extreme_wide, angle: high, lens_mm: 24, dof: deep,
          composition_tags: [negative_space, depth_staged],
          movement: { base: static, support: locked },
          notes: "full → extreme_wide = 4-rung jump. Deliberate: the release lives in the hold." }
    end: { end_fade_ms: 1400 }                          // fade_through_black tier — the act closes
```

---

## 4. ALIASES & LICENSED DEFAULT-BREAKS

Every entry below is a rule this cookbook **deliberately breaks**. Breaking it elsewhere is a defect; breaking it here is the craft. Log the break; do not silence the validator.

1. **Comedy = beat-snap legal.** `beat_snap: snap` + literal image/score sync (Mickey-Mousing) is CRAFT in comedy — the one genre where it is. Everywhere else a median |cut−beat| <30ms trips the `beat_locked_cutting` flag, because a beat grid driving cuts inverts Murch's Rule of Six (rhythm 10% < emotion 51%). Note the term is precise: Mickey-Mousing = SCORE mimics ACTION; it is not a synonym for beat-locked cutting.
2. **Horror = under-lighting legal.** `angle: underneath` (90° straight up) and `key_direction: under` are legal values and fill a real representational gap. Anywhere else, under-lighting reads as a *mistake*, not a mood.
3. **Shock and Awe break the size ladder on purpose.** The ≤2-rung-per-scene validator will flag `medium → extreme_close_up` (shock, 3 rungs) and `close_up → extreme_wide` (awe, 5 rungs). Expected. **The jump IS the beat** — a shock delivered inside the ladder is not a shock.
4. **Unease = jump cut legal.** <30° + same scale is a defect everywhere else (regenerate a wider delta). In an unease recipe you *commit* to it as style — the discontinuity is the wrongness.
5. **Suspense = innocent light.** Suspense is manufactured by INFORMATION (staging + sound), never by the key. A suspense scene lit like horror gives the game away and collapses dramatic irony into surprise. Hitchcock's distinction is a lighting rule as much as a story one.
6. **Grief takes no crying close-up.** Facial micro-expression is unreliable at ANY size in AI-gen; the body and the silhouette are the primary carriers. Grief's interior beat is still MCU-or-tighter (H2) but its content is a **posture and a playable verb**, never an emotion adjective — adjective prompts produce vague acting faces.
7. **Dolly⇄zoom fork.** Isolation and interiority may render `zoom·out` instead of `dolly·out` when the register is flat / clinical / surveillance. The substitution is **never silent** — log it in `decision_log`. A `dolly` rendered with no parallax is a `prompt_adherence` FAIL, not an acceptable near-miss.
8. **RED-risk moves in these recipes require a documented post fallback** (V4 WARN): `dolly_zoom` (interiority) → static plate + focus-breathing grade · `crash_zoom` (comedy) → hard cut to a tighter size · `whip_pan` (urgency) → `cut` with `hidden_join: whip` · `arc_degrees > 120` → split into two shots. **whip_pan is a SEAM, not a shot** — author the chaos as `pan·fast·handheld` and put the whip on the join.
9. **Branded inserts are not stock.** `function: insert|cutaway|establishing` auto-suggests `generation_strategy: stock` (characterless by definition). That auto-suggest **does not apply** to a branded product insert: composite from a locked real asset. Legal exposure is never entrusted to a negative prompt.
10. **`stitched_oner` truth-in-labeling.** The determination and triumph recipes read as continuous. Client copy says "designed as a continuous take" — **never** "single take". `long_take` is reserved for single-pass material.

### Flagged defects (for Phase 5/6 — found while authoring, not fixed here)
- **`flat_1_1` canonical proxy — RESOLVED.** The proxy formerly ended in a negated clause ("no visible shadow edge"), tripping the blocking negation lint (ruling 1.7). The canonical string in `lighting.md` is now fully positive: **"flat even illumination, shadow side as bright as the key, seamless shadowless light"** — kernels emit it verbatim (byte-stable, never re-worded per shot).
- **`dutch_deg` is capped at 0–45 — a DELIBERATE cap, not an oversight** (see shot-grammar.md): research documents an extreme 45–90° band, but beyond ~45° generated geometry degrades and identity references distort. No recipe here needs it; a psychological-break recipe would require a cap-raise proposal, not a silent workaround.
