<!-- SHIPPED SNAPSHOT of the internal arbitration record (.omc/research/filmcraft/_rulings.md).
     The .omc/ directory is gitignored — this copy exists so reference-file citations resolve in fresh clones. -->

> **Phase 6 verification amendments (2026-07):** cross-verification (605 entries, 5 batches) forced these corrections over the original rulings where they conflict — (a) `flat_1_1` canonical proxy re-worded fully positive: "flat even illumination, shadow side as bright as the key, seamless shadowless light"; (b) Hall proxemics: social 4–12ft (1.2–3.7m), public 12ft+ (3.7m+); (c) editorial transition duration tiers restated 24fps-canonical (soft_cut 250–500ms default 300 · dissolve 1000–2000ms default 1000 · fades 500–2000ms); (d) 30° rule re-attributed to classical continuity convention (textbook formalization), not Mascelli single-author; (e) costume-multiples fixed "minimum 3" retracted — count scales with stunt/damage load; (f) J/L-cuts authored via cue in-point placement — no signed-offset schema fields exist. (g) the ruling's `vo.mode` shorthand shipped as `audio.voiceover.mode` {narration|internal_monologue|character_sync} in edit_plan.schema.json. (h) post-gate backlog shipped: `audio.voiceover.start_sec`+`duck` (renderer VO mix-in + bed sidechain ducking, SFX excluded) · `color.scene_trims[]` (shot_id-keyed per-clip eq/colorbalance) · real-render smoke passed on ffmpeg 8.1.

# filmcraft — Phase 3 FINAL RULINGS (Chief Arbiter Synthesis)

Inputs: 12 dept research reports + 37-item agenda + 3 adversarial verdicts (academic / practitioner / ai) + 19 newly-found collisions.
Arbitration principle: **definitions → academic wins; schema surface area → practitioner wins; verifiability → ai wins.**
Everything below is BINDING for Phase 4 (writing), Phase 5 (integration), Phase 6 (verification).

## 0. ARCHITECTURE RULINGS (unanimous or near-unanimous)

A1. **Two layers, one projection.** Canonical artifacts (storyboard/brief/edit_plan) store MODEL-FREE controlled vocabulary. A deterministic PROMPT-PROJECTION layer (tables in `filmcraft/references/prompting.md`, applied by production-director at produce time) renders prompts from the record. The projection may reorder, expand, and translate; it may NEVER deform the record. (academic "projection layer" ≡ ai "compiler" ≡ practitioner "renderer translates".)

A2. **No model name in any normative rule.** Normative rules key on capability flags only: `{negative_prompt, max_moves_per_shot, named_tag_syntax, flf_support, camera_param_object, legal_durations[], text_render_ok, native_audio}`. A dated `references/model-matrix.md` ("verify per campaign", + typosquat blocklist) is the ONLY place model names/versions live. production-director's current "Kling/Runway=1, Veo/Sora=multi" note is DELETED (model-hardcoded AND factually wrong). model_profile is written into production_manifest at produce Step 1 from video_models_list.

A3. **storyboard gains a `scenes[]` object** (was: bare scene_id strings — the biggest structural gap, blocks lighting lock/axis/palette/montage/beat mapping). Scene-level defaults + shot-level override-with-reason is the mechanism that keeps per-shot surface area sane (practitioner: "the lighting plot and the floor plan are separate documents").

A4. **Schema ⊆ renderer capability.** No transition/effect enum value without a code path in scripts/render_edit_plan.py. Values added in Phase 5 only together with renderer support.

A5. **All lexicon timings in MILLISECONDS** (+ frame table per fps in the reference). Frame counts in research assumed 24fps; renderer defaults 30.

A6. **Pre-flight lint before generation, review after.** Prompt hygiene (blocklist, negation ban, hex ban, foreground_anchor, verbatim lighting) is checked BEFORE spaces_run at zero cost. quality-reviewer's post-gen axes gain: lighting_continuity, motion_quality, flf_adherence (grammar_compliance is split, not added as one blob).

## 1. CONTROLLED VOCABULARY — FINAL (schema-facing, snake_case)

### 1.1 camera.movement (exactly ONE object per shot — one-move law)
```
base:      static | pan | tilt | dolly | truck | pedestal | crane | arc | zoom | dolly_zoom | roll | whip_pan | crash_zoom
direction: pan|truck|whip_pan|arc → left|right · tilt|pedestal|crane → up|down
           dolly|zoom|dolly_zoom|crash_zoom → in|out · roll → cw|ccw · static → (absent)
speed:     slow | normal | fast          (absent for static/whip_pan/crash_zoom — speed-coded by definition)
support:   locked | handheld | stabilized | drone      (default locked; steadicam,gimbal → stabilized)
subject_relation: none | follow | lead   (optional, default none)
arc_degrees: 30–360                      (REQUIRED iff base=arc; "orbit" = alias for arc@360; compiler may emit "orbits around" ≥270°)
foreground_anchor: string                (REQUIRED iff base ∈ TRANSLATION = {dolly, truck, pedestal, crane, arc})
```
- LEXICON teaches the truth the flat schema compresses (academic definitional layer): **zoom is an optical change, not a camera movement** (no parallax — the entire dolly/zoom distinction); dolly_zoom is canonically the compound {dolly,in}+{zoom,out}; whip_pan/crash_zoom are speed-coded variants. The schema keeps them as base values because models treat them as qualitatively distinct requests (blur-to-streak / instant snap) and single-value validators stay simple.
- BANNED enum values (authoring aliases that MUST resolve at write time): push_in, pull_back, slow_push_in, tracking, orbit, jib, boom, crab, swish_pan, zolly, vertigo, trombone, steadicam, gimbal, zoom_in, zoom_out(as base names).
- `movement_intent` (push_in|pull_back|reveal|escort|withdraw) allowed as NON-normative prose gloss in notes.
- Validators: V1 direction ∈ valid_set(base)=ERROR · V2 TRANSLATION without foreground_anchor=ERROR ("we pay dolly price, get a zoom") · V3 speed=fast ∧ TRANSLATION=WARN (warping) · V4 dolly_zoom|crash_zoom|whip_pan ∨ arc_degrees>120 = WARN + documented post fallback required in notes · V5 >1 movement object=ERROR (produce-time merge of adjacent same-position shots allowed only when model_profile.max_moves_per_shot ≥2 — never authored).
- Risk register (derived, lexicon table): green(static,pan,tilt,zoom,dolly,truck,pedestal) / amber(crane,arc≤120,stabilized/handheld follow,drone) / red(arc>120,dolly_zoom,whip_pan,crash_zoom,roll).
- **Dolly⇄zoom fork** (intent-driven): dimensional/immersive → dolly + named foreground element; flat/clinical/surveillance intent OR repeated background warp → zoom. Substitution is NEVER silent: rendering a dolly with no parallax = prompt_adherence FAIL (core rule 4 강등 금지); fallback dolly→zoom is logged in decision_log.
- Settle doctrine: every move **starts AND ends on a composed frame**; projection appends "…then settle on [composition]"; last 10–15% of clip = no travel (PIPELINE HEURISTIC, not canon). Term: `camera_settle` (vs `impact_settle` in motion kit — N2 collision resolved).
- Direction convention: arc/orbit direction names the CAMERA'S TRAVEL, never the subject's apparent rotation.

### 1.2 camera framing/size/angle
```
shot_size: extreme_wide | wide | full | medium_full | medium | medium_close_up | close_up | extreme_close_up
angle:     eye_level | low | high | overhead | underneath | bird_eye | worm_eye
dutch_deg: 0–45 (default 0; separate ROLL field — low-angle canted shots must be expressible; alias: canted)
framing:   single | two_shot | group | empty_frame | ots | pov
dirty:     bool (optional; single/ots only — clean vs dirty)
function:  none | establishing | master | insert | cutaway | reaction | transition   (optional, default none — EDITORIAL role, cannot be read off the frame)
pov_of:    <character key> (REQUIRED iff framing=pov; strict optical-position definition)
gaze_target: to_camera | off_left | off_right | off_up | off_down | at:<character key> | none   (optional; replaces the rejected 15–20° eyeline number)
screen_direction: left | right | toward_camera | away_from_camera | neutral   (REQUIRED when a subject moves or looks; neutral = the legal axis-crossing hinge)
composition_tags: array ≤3 of rule_of_thirds | centered_symmetry | leading_lines | frame_in_frame | negative_space | depth_staged | foreground_occlusion   (optional)
lens_mm:   integer 14–600 — ALL VALUES FULL-FRAME EQUIVALENT (single global statement; replaces free-string lens)
dof:       shallow | medium | deep      (ots/dirty ⟹ shallow auto-emitted — foreground shoulder renders sharp by default)
position_id: keep as-is
```
- shot_size cut-lines (lexicon, dual nomenclature ELS/LS/FS/MLS/MS/MCU/CU/ECU): extreme_wide subject ≤10–15% frame height · wide full body + substantial environment · full full body, edges near head/feet · **medium_full = MID-THIGH** (≡ plan américain ≡ American ≡ cowboy — aliases, never values; the knee/mid-thigh two-rung split REJECTED as unsourced and contradicting the never-cut-at-a-joint rule) · medium waist · MCU chest · CU shoulders · ECU detail ("Italian shot"=eyes-only alias). Never cut at a joint.
- angle definitions are GEOMETRIC, never intent-based: overhead = 90° straight down at close/human scale · underneath = 90° straight up (new value — fills a real representational gap) · bird_eye = high-altitude aerial vantage pitched steeply down · worm_eye = ground-level pitched steeply up with strong foreshortening (projection adds foreshortening + wide-lens cue). camera_height axis REJECTED (folds into angle; hip/knee/ground-level = prompt phrases in the lexicon).
- three_shot → group (≥3). headroom/lead_room = NOT schema fields (implicit in size; lexicon documents them as prompt language). golden_ratio = NOT a tag (retained in lexicon with the unsupported-claims caveat). open/closed staging = lexicon concepts, not tags.
- Validators: ots|dirty ⟹ ≥2 characters · pov ⟹ pov_of set + "no visible camera or hands" emitted · insert|cutaway|establishing ⟹ auto-suggest generation_strategy:stock (characterless by definition — resolves the establishing-shot 3-way collision: format wins for shorts; where needed, it's a stock candidate) · two_shot = exactly 2 (definition by COUNT only) · size ladder jump ≤2 rungs within a scene (flag).

### 1.3 scenes[] (NEW object in storyboard)
```
scenes[]: {
  scene_id, slugline_ref,
  type: normal | montage_sequence,
  cut_sync: free | motion | beat_grid          (montage/format-driven)
  axis: { established_by_shot_id, a: <char>, b: <char>, a_side: left|right, note },
  lighting: {                                   ← THE LIGHTING PLOT. Injected byte-identical into every keyframe prompt of the scene.
    time_of_day: dawn | golden_hour | day | overcast | blue_hour | night | interior_day | interior_night,
    key_direction: front | front_left | front_right | side_left | side_right | back_left | back_right | top | under | ambient,
    key_quality: hard | soft,
    ratio: flat_1_1 | mild_2_1 | standard_4_1 | low_key_8_1 | extreme_16_1,
    contrast_proxy: string (REQUIRED — from the canonical table below, never invented per shot),
    color_temp_k: integer (+ color_note gloss; projection emits Kelvin AND gloss, never Kelvin alone),
    pattern: none | rembrandt | loop | split | butterfly | broad | short | rim | silhouette   (optional; portrait geometry),
    motivation: string|null ("window", "the desk lamp is the ONLY light source…", practicals),
    exposure_bias: bright | neutral | dark      (SEPARATE from ratio — resolves the high-key double definition)
  },
  palette_note: string|null (scene override of the project color script),
  lighting_override_reason: per-shot overrides require a logged reason (= telling the script supervisor before moving the key)
}
```
- Canonical ratio→proxy table (compiler-owned, byte-stable): flat_1_1 "flat even illumination, shadow side as bright as the key, seamless shadowless light" · mild_2_1 "gentle modeling, shadow side one stop under, soft shadow detail" · standard_4_1 "clear shadow side, visible but detailed shadow" · low_key_8_1 "shadow side barely visible, deep shadow, only a sliver of detail" · extreme_16_1 "shadow side reads near-black, subject edge lost in shadow".
- key_class (high_key|mid|low_key) is DERIVED from ratio (≤2:1 high, ≥8:1 low) — QA-only, NEVER emitted into prompts (models read "high-key" as bright), NEVER independently settable. **High/low-key = ratio classes, not brightness** (HILL, unanimous after N1 fix).
- BANNED prompt terms: bare ratio numbers, key_class words, negative_fill (models can't subtract — emit the resulting shadow), day_for_night (use blue_hour / "moonlit overcast" + achieve in ffmpeg), magic_hour (ambiguous — use golden_hour|blue_hour). moonlight-blue documented as CONVENTION (physical moonlight ≈4100–4500K).
- Validator: distinct(lighting_sentence) per scene == 1, else FAIL. (#1 documented AI failure made mechanical.)

### 1.4 edit_plan transitions (schema speaks EDITORIAL; renderer translates) — schema_version 2.0
```
transition_in.type: cut | soft_cut | dissolve | fade_through_black | fade_from_black | dip_to_white
                  | wipe_left | wipe_right | slide_up | slide_down | iris_open | clock_wipe
duration_ms: int (soft_cut 200–400 default 300; dissolve 800–1600 default 1200, ellipsis-tier 3000–5000; fades 400–1500)
timeline-level: opening_fade_ms (fade in from black on first clip) · end_fade_ms (fade to black on last clip tail)
hidden_join: null | whip | object_wipe | dark_frame   (annotation on a cut — post needs the seam logged; renderer treats as cut)
```
- Renderer mapping (tool namespace, never the lexicon): soft_cut|dissolve → xfade=fade · fade_through_black → xfade=fadeblack · dip_to_white → xfade=fadewhite · wipe_left/right → wipeleft/right · slide_up/down → slideup/down · iris_open → circleopen · clock_wipe → radial · opening/end fades → fade filter (not xfade).
- **DELETED: `fade` (ambiguity trap — an author typing film grammar got a crossfade) and `dissolve`-as-ffmpeg-noise-dither (a documented-banned value was selectable).** ffmpeg's dissolve is renamed `dither_dissolve` in docs and is NOT exposed. Legacy migration: fade→dissolve · dissolve→dissolve+WARN · fadeblack→fade_through_black · fadewhite→dip_to_white · wipeleft→wipe_left etc.
- Semantics (lexicon): soft_cut = TECHNICAL repair (first-frame tonal pop, near-jump-cut) — invisible, carries NO temporal meaning, EXEMPT from punctuation reservation; precedence: head-trim FIRST (free, lossless), soft_cut only if trimming cuts needed content. dissolve = time passed (duration encodes the weight of the ellipsis). fades = act/chapter punctuation — act-reservation rule survives, applied to the semantic tier only. wipes/iris/clock = stylized, announce themselves (flagged, allowed).
- hidden_cut is NOT a transition value (no renderer path). Oners: built at generation (foreground blocker/whip-blur in keyframes), joined with cut + hidden_join annotation. **Terminology: `long_take` reserved for single-pass material; stitched = `stitched_oner`/invisible-cut sequence. Client copy: "designed as a continuous take", NEVER "single take"** (truth-in-labeling HILL).

### 1.5 audio & music
```
audio.music_cues[]: { cue_id ("M1","M2"…), source, in, out, diegesis: score|source|trans_diegetic,
                      provenance: generated|licensed (licensed ⟹ license field REQUIRED, empty = delivery BLOCK),
                      gain_db, why (spotting rationale), derived_from?: cue_id, transform?: {pitch_semitones, tempo_ratio} }
audio.sfx[]:       { id, source, at_sec, gain_db, duck_others_ms? }
audio.ambience[]:  { source, in, out, gain_db }
audio.beat_snap:   { mode: snap|offset|off, offset_ms: 60–150 }   (defaults: comedy/hype/montage→snap; cinematic/brand/longform→offset)
vo.mode: narration | internal_monologue | character_sync           (internal_monologue = canonical term "internal diegetic sound" (B&T);
                                                                    treatment: non-diegetic ducking + close/dry perspective)
transition audio: audio_in_offset_ms (negative = pre-lap) · audio_out_offset_ms (positive = trail) ← [SUPERSEDED by amendment (f): these offset fields were NEVER shipped — J/L is authored via cue placement (`music_cues[].in/out`, `sfx[].at_sec`, `ambience[].in`); see sound-music.md D7]
                  — J-cut/L-cut are GLOSSED ALIASES only (most-reversed pair; signed numbers cannot be reversed)
```
- "soundtrack" is NOT a cue type (it is the whole audio program / the album) — REJECTED as enum.
- Music doctrine: cues are spotted (in/out + why), never wall-to-wall — WARN when one cue ≥95% of timeline, gated to cinematic_short|longform (wall-to-wall is CORRECT for 15–60s music-led shorts). Leitmotif = render theme ONCE, every recurrence transforms the SAME stem (pitch/tempo/instrumentation preserving interval contour) — re-prompting a recurring theme = schema violation (it is by definition not a leitmotif).
- **Beat-sync doctrine (revises v0.3 "snap cuts to beat"): cut on PICTURE (action/look/sound event); sync only the TENTPOLES (≤3: hook, turn, CTA/final).** Global beat-snap survives only for hype-montage/comedy. QC: median |cut−beat| <30ms on a non-comedic profile ⟹ flag **`beat_locked_cutting`** (NOT "mickey-mousing" — that term = SCORE mimics ACTION, valid in comedy/animation; the principled ban: a beat grid driving cuts INVERTS Murch's Rule of Six, rhythm 10% < emotion 51%).
- Delivery gate (blocking): no deliverable ships music-only when picture contains visible impacts or hero walking — floor = 1 ambience bed per location + footsteps on hero walking shots + hard FX on every visible impact (stock-sourced; declared in edit_plan, never silently omitted). Validator: shot.sound[] non-empty ∧ no edit_plan destination ⟹ QC FAIL.
- QC dynamics axis: measure LRA (EBU R128 standard metric — do NOT invent variance metrics); WARN < 4 LU only for cinematic_short|longform|brand (never shorts_reels); threshold provisional until calibrated on two productions.
- VO budgets: EN 160–180wpm (:15≈30–40w · :30≈60–80w · :60≈150w, write to ~90%); **KR budgets in SYLLABLES (provisional: ≈5–5.5 syl/s → :15≈75–85음절 · :30≈150–170음절 · :60≈300–330음절 — VERIFY in Phase 6)**; captions budgeted in CHARACTERS. Pause taxonomy 0.3s/1s/2s, 120ms floor; per-sentence TTS calls ≥3 sentences; pre-TTS budget check = BLOCKING.

### 1.6 project_brief.visual_grammar (REQUIRED — the per-project style bible; model-free)
```
visual_grammar: {
  design_concept: string,                              # the unifying metaphor
  palette: { dominant, subordinate, accent, harmony, forbidden[] },      # 60/30/10
  color_script: [ { beat, palette_target, saturation, temperature } ],   # per-beat arc (Pixar practice)
  location_palettes: { <location>: string },
  lighting_bible: { default (scene.lighting shape), motivation_doctrine: motivated|stylized },
  lens_bible: { default_mm per shot_size class, aperture_default, dof_default, format_note: "all mm FF-equivalent" },
  look: { film_stock: none|kodak_portra_400|kodak_vision3_500t|cinestill_800t|kodak_trix|ilford_hp5|super8|arri_alexa,
          lens_character: spherical|anamorphic|vintage, grain: none|fine_35mm|coarse_16mm|super8, diffusion: none|light|medium|heavy },
  camera_bible: { default_support, settle_required: true, movement_rules: { max_moves_per_shot: 1, banned_bases[] } },
  grade: { show_lut?, per_scene_trim: true, correction_before_grade: true },
  motion_bible: { easing_required: true, moving_hold_required: true, gesture_economy_max: 2, shutter_look: natural_180 },
  sound_bible: { diegesis_default, loudness_target, lra_floor? },
  prohibitions: { empty_tokens: [标准 blocklist], greeking_required: bool, flop_forbidden: true, baked_text_forbidden: true }
}
required subfields: palette, lighting_bible, lens_bible, camera_bible  (highest measured drift ROI)
model_profile = SIBLING artifact in production_manifest (dated, disposable) — NEVER inside visual_grammar.
```

### 1.7 Prompt construction (projection tables — filmcraft/references/prompting.md)
- **Ordering fork (no universal ordinal — Google contradicts itself):** KEYFRAME (T2I): [image type/shot size] → [subject + identity handle] → [static pose/action state] → [environment] → [composition] → [lighting sentence] → [lens/optics] → [stock/style]. CLIP (I2V/T2V): [camera movement + speed] → [subject appearance phrase] → [ONE action (max 2)] → [environment cue] → [settle clause].
- **Identity handle fork (revises storyboard rule 2, which was scoped to motion_desc all along):** storyboard stores `{{char:key}}` placeholders + appearance_phrase. Projection resolves per model_profile: reference wired + named_tag_syntax → @name / <<<name>>> / @Image N; reference wired, no tag syntax → appearance_phrase + reference image; no reference (rare; citation_required=false) → appearance_phrase verbatim from characters.json (never paraphrased). motion_desc ALWAYS uses appearance phrases (with 2+ figures the video model must know which one moves).
- **Negative prompting doctrine:** positive reframing is the house default everywhere ("empty street" not "no cars"; "locked-off static shot on a tripod" not "no camera shake" — attention-capture backfire documented). negative_prompt is NOT an authoring field; projection populates it ONLY when model_profile.negative_prompt=true, from a compiler-owned reframe table. LINT (blocking): /\b(no|without|avoid|don't)\b/ + noun in any emitted prompt = ERROR.
- **Empty-token blocklist (blocking lint):** masterpiece, best quality, 8k, 4k, highly detailed, trending on artstation, award-winning(bare), professional(bare), octane render, unreal engine 5, (word:1.4), score_9, epic(bare), moody(bare), "dramatic lighting"(bare), "beautiful composition". **"cinematic" valid ONLY with ≥1 concrete technical noun co-occurring** (film stock | camera body | <N>mm | f/<N> | named lighting pattern | aspect ratio). Endorsed token class: named hardware/film stocks (best-evidenced category).
- Brand/text: any legible brand mark, product label, packaging, or plot-critical text = COMPOSITE from a locked real asset, never text-described, never generated (greeking = canonical term; legal exposure — never entrusted to negative prompts). NO baked text in generated clips; all text burns in post.
- Every storyboard field must be resolvable to an OBSERVABLE.

## 2. HOUSE-RULE AMENDMENTS (existing skills — Phase 5 edits)

H1. storyboard-director rule 2 → identity-handle fork (see 1.7). Rule 6-1/6-0 keep; screen_direction now a FIELD.
H2. storyboard-director rule 5-1 merged with directing evidence: **emotional beats = MCU-or-tighter AND a described playable physical action (verb), never an adjective** (micro-expression unreliable at ANY size; adjective prompts produce vague acting faces).
H3. storyboard-director rule 3 (open wide) + format rules + model weakness resolved: for shorts/ads format wins (no establisher); where an establisher is needed → function:establishing → stock candidate by default.
H4. Coverage naming corrected: the clip ceiling forces **découpage (shot breakdown)** — mandatory; **coverage** (redundant master+singles+insert) stays a deliberate hero-scene-only spend (existing rule was already right; the agenda's wording was wrong). Validator: scene ≥3 shots ⟹ ≥1 insert|cutaway|reaction.
H5. production-director Step 1 model note → capability flags + model-matrix appendix (A2).
H6. production-director FLF rules KEEP + strengthen: FLF legal only when FF and LF share camera position (same size/angle/lens_mm/dof); a size change = two shots or one move rendered FF-only. `variation_type` stays a COST label; its schema description is rewritten so `large` no longer describes cross-position changes (which are now illegal as FLF pairs). NEW mechanical check: SSIM/pHash compare clip final frame vs supplied LF → quality-reviewer axis flf_adherence (serving paths have silently dropped LFs).
H7. Chaining rule KEEP, renamed **conform_from_source**: last frame allowed as non-authoritative reference CITATION; banned as chained source keyframe (≥2 gens); the single permitted chain requires upscale + color-normalize + decision_log entry.
H8. post-production: transitions per 1.4 (soft_cut precedence AFTER head-trim); beat-snap per 1.5; music_cues/sfx/ambience per 1.5; audio_in/out_offset_ms [SUPERSEDED — amendment (f): never shipped, cue placement instead]; show_lut + per-scene trim [amended: show_lut uniform + per-scene trim BOTH implemented — `color.scene_trims[]`] replaces single-LUT-per-sequence absolutism (one LUT would flatten the color script); hidden_join logging; duration handles: storyboard duration_sec = TIMELINE intent + head handle 0.5s + tail handle 0.3s — beat validator sums timeline durations (arithmetic observed in production 1, now encoded); produce-time gen_duration_s = nearest legal duration ≥ intent+handles from model_profile.legal_durations[].
H9. ffmpeg horizontal flip (`flop`): BANNED when frame contains text/logos/jewelry-side/hair part/scars/handedness/vehicle steering side (LHD-RHD, KR-critical)/asymmetric wardrobe — AND a flop invalidates the character reference bank (mirrored face ≠ sheet). Default remedy: regenerate or neutral insert. No hflip field exists (absence = ban).
H10. quality-reviewer axes add: lighting_continuity, motion_quality (easing/moving-hold/weight), flf_adherence, dynamics(LRA), beat_locked_cutting flag, sfx-destination check, color_consistency (signalstats). Plus pre-flight lint list (A6) runs BEFORE generation.
H11. magnific-studio-core: add filmcraft routing rule (read the index before each stage; artifacts must use controlled vocabulary; projection tables own prompt strings) + the blocklist as a hard rule + truth-in-labeling (stitched oner).
H12. characters/spaces-engineer: reference selection heuristics unchanged; add named-tag resolution note (1.7).

## 3. LEXICON-ONLY RULINGS (Phase 4 writing directives)
L1. Normal lens defined by FORMAT DIAGONAL (FF ≈43mm; S35 ≈28mm), 50mm noted as stills convention. All mm published as FF-equivalent.
L2. deep space (mise-en-scène) ≠ deep focus (optics) ≠ staging in depth (using deep space for simultaneous action) — deep space + shallow focus is expressible and common.
L3. Kuleshov taught as foundational DOCTRINE with evidentiary status stated (original footage lost; replications mixed).
L4. Gilligan cut = gloss only. b-roll = broadcast term, glossed to insert/cutaway in narrative context.
L5. montage: schema value `montage_sequence`; informal "montage" acceptable for the device in prose; "Soviet montage"/"montage theory" for the theory; Eisenstein's 5 methods + collision-vs-linkage documented as concepts (Pudovkin's linkage is Eisenstein's RIVAL, not a sixth method — editing.md's enum error corrected). No montage_mode enum.
L6. anempathetic (indifferent/mechanically oblivious — Chion) ≠ ironic (registered authorial contrast) — different prompt phrasings.
L7. two-shot defined by COUNT; conventions to params. Insert (re-emphasizes what the master covered) vs cutaway (NEW material, returns) distinction kept — editorial function axis.
L8. Rembrandt strictness: canonical triangle definition given; loose 45° usage flagged as industry drift. Loop 30–45°, Rembrandt 45–60°, split 90° as continuum note.
L9. Physics vocabulary = style signal, not simulation (Thomas & Johnston: the ILLUSION of life); every impact = guaranteed post-fix point (physics_risk flag → cutaway pre-planned).
L10. "35mm" always disambiguated: lens/film/format. Film stocks: CineStill 800T glow ≠ Vision3 500T clean (same emulsion, opposite halation).
L11. Eyeline: NO degree tolerance published (unsourced folk number rejected) — qualitative rule + gaze_target enum; marked open research.
L12. FLF adherence rankings: NOT asserted (research gap) — replaced by the per-clip SSIM measurement (H6).
L13. AI-caveat framing: keyframe→I2V (pose-to-pose) documented as the industry-verified drift mitigation — our architecture is the mitigation.
L14. Aliases table (canonical ← aliases): medium_full ← cowboy, american, plan américain · wide ← long shot · stabilized ← steadicam, gimbal · arc@360 ← orbit · dissolve ← crossfade, mix, lap dissolve · fade_through_black ← fade to black (join) · soft_cut ← micro-dissolve, blend cut · audio lead/trail ← J-cut/L-cut, pre-lap/post-lap · internal_monologue ← internal diegetic sound, metadiegetic · dutch_deg ← canted, dutch angle · flop ← horizontal flip, mirror.

## 4. VERDICT TALLY (agenda items — final)
1 conform_from_source (H7) · 2 four-axis adopted w/ flat-base compromise (1.1) · 3 framing/function split + medium_full + bird/worm kept geometric + dutch_deg + underneath (1.2) · 4 dolly⇄zoom fork + anchor (1.1) · 5 prompt=mood, ffmpeg=precision + show_lut/scene trim (H8) · 6 découpage/coverage corrected (H4) · 7 flop ban (H9) · 8 lens_mm + disambiguation (1.2, L10) · 9 number REJECTED → gaze_target (1.2, L11) · 10 soft_cut/dissolve tiers in ms (1.4) · 11 editorial enum, dissolve/fade deleted, renderer maps (1.4) · 12 recruitment REJECTED (≡ break_into_two); + optional debate/uncoded STC beats ≥90s · 13 duration tiers adopted; <20s = setup/turn/payoff naming (hook/catalyst/final_image skeleton); hook clamp lives in format namespace · 14 ratio-defined key classes, exposure_bias separate (1.3) · 15 canonical proxy table (1.3) · 16 scene lighting struct, byte-identical (1.3) · 17 motion token kit, compiler-appended, camera_settle/impact_settle (1.1, H10) · 18 composite-from-asset + positive reframe + QC gate (1.7) · 19 art director false-friend glossary (L) · 20 montage_sequence + theory split; mode enum rejected (L5) · 21 settle both-ends (1.1) · 22 stitched_oner truth-in-labeling + hidden_join (1.4) · 23 tentpole sync + beat_locked_cutting + genre-gated snap (1.5) · 24 named cues, spotting ≥60s, wall-to-wall format-gated (1.5) · 25 diegesis: score|source|trans_diegetic + provenance; soundtrack rejected (1.5) · 26 signed audio offsets; J/L aliases; internal_monologue (1.5) · 27 sfx/ambience arrays + destination validator + delivery gate (1.5) · 28 leitmotif same-stem law (1.5) · 29 LRA standard metric, format-gated WARN (1.5) · 30 budgets: EN words, KR SYLLABLES (provisional), pre-TTS block (1.5) · 31 identity-handle fork via placeholders (1.7) · 32 one-move law authored; produce-time merge behind capability flag (1.1) · 33 ordering fork still/video (1.7) · 34 positive reframing + capability-gated negatives + lint (1.7) · 35 blocklist + cinematic pairing (1.7) · 36 capability flags + dated matrix (A2) · 37 physics=style + flf_adherence measurement (L9, H6).

## 5. OPEN ITEMS → Phase 6 verification
P6-1 KR syllable budgets (provisional numbers — verify against KR VO industry norms).
P6-2 LRA floor 4 LU (provisional — calibrate; record on first two productions).
P6-3 SSIM/pHash threshold for flf_adherence (pick after first measurement batch).
P6-4 Eyeline qualitative rule wording (open research; no number).
P6-5 Kelvin table + golden-hour ranges spot-check ([v] inherited from research).
P6-6 All [v]-tagged numerics inherited into references: spot-check 10% sample + all safety-critical ones.
