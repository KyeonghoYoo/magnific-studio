# Production Design — Filmcraft Reference

Read this when: world/costume design at /ms-plan and /ms-characters; environment/prop description in keyframe prompts; design continuity at QA.

Scope: environment, sets, props, wardrobe, texture, palette — the AUTHORED visual world. Character facial/body identity is OUT of scope (contract-enforced via character reference banks, not this lexicon); the costume rows below cover wardrobe as a designed object, not identity-lock mechanics.

## Canonical Terms

### Discipline & Ownership

| Term | KR | Use when | Effect | Prompt phrase | QA (+Caveat) |
|---|---|---|---|---|---|
| Production Design | 프로덕션 디자인 | /ms-plan kickoff, before any asset is designed | Unifying creative authorship of the entire visual world — architecture, sets, props, palette — under one coherent concept; raises perceived craft/budget | "cohesive production design, unified world aesthetic" | Diffusion models hold no persistent world-state — each keyframe designs the world in isolation unless a shared World Bible/reference bank anchors every prompt |
| Art Direction | 아트 디렉션 | Any budgeting/scheduling/feasibility discussion distinct from the creative concept | Operational execution of the PD's concept — drafting, scheduling, feasibility; NOT the concept itself | n/a — process term, not a prompt fragment | Do not merge into Art Director's authority — Art Direction is the FUNCTION; Art Director is the ROLE performing it |
| Art Director (Film) | 아트 디렉터(영화) | Any film/episodic pipeline note naming a department manager under the Production Designer | Department manager executing the PD's concept — budget, drafting, schedule; reports to the Production Designer | n/a — role title, not a prompt fragment | False friend with Art Director (Advertising) — see Doctrine §13 |
| Art Director (Advertising) | 아트 디렉터(광고) | Any ad/commercial pipeline note naming the campaign visual-concept author | Campaign visual-concept AUTHOR under a Creative Director — closer to a film Production Designer in authority than to a film Art Director | n/a — role title, not a prompt fragment | False friend with Art Director (Film) — NEVER use "Art Director" unqualified across departments |
| Set Decoration | 세트 데코레이션 | /ms-plan or /ms-produce — dressing a built/generated set to complete its story logic | Furnishing/dressing a set — furniture, textiles, wall art, tabletop objects; converts "a set" into "a place a specific person lives in" | "richly dressed set, lived-in furnishings" | Gen defaults to showroom-generic — explicitly prompt density/era/wear logic (see Set Dressing) |
| Property Master | 프롭 마스터 | /ms-characters or /ms-plan — any object an actor physically handles | Owns hand props — objects actors physically handle, distinct from background dressing; actor-handled objects carry disproportionate story weight | "[locked object] in hand, story-relevant object detail" | Highest-frequency AI continuity failure lives here — see Hero Prop for the locked-reference mitigation |
| Costume Design | 의상 디자인 | /ms-characters — everything a character wears | A separate department (NOT part of the art department) — everything a character wears; palette-coordinates with production design only | n/a — see Costume Arc / Silhouette / Costume Color Blocking | Wrong framing under-prioritizes costume continuity — never silently absorb into a generic "production design" prompt block |

### World-Building & Research

| Term | KR | Use when | Effect | Prompt phrase | QA (+Caveat) |
|---|---|---|---|---|---|
| Mood Board | 무드보드 | /ms-plan, earliest exploratory pass, before any original asset is designed | Curated reference-image collage establishing color/texture/tone before original assets | n/a — supply as actual image references, not words | Supply as style-ref images, never describe a mood board in text — words underspecify tone |
| Design Concept | 디자인 콘셉트 | /ms-plan kickoff, before any asset is designed | The single unifying metaphor every visual department translates (e.g. "a hospital that looks like a cathedral") | "world governed by a singular design concept: [metaphor]" | Encode as a written doc feeding every prompt; maps to `visual_grammar.design_concept` — write once, never re-author per shot |
| Visual Research | 비주얼 리서치 | /ms-plan — systematic period/place/subculture gathering before design work starts | Systematic gathering of period/place/subculture reference before design work | "researched period-accurate detail, archival reference" | Models blend eras/regions by averaging — specific decade/region/named-artifact terms fight drift (see Authenticity Anchor) |
| Period & Place Authenticity Anchor | 시대·장소 고증 앵커 | /ms-plan or /ms-produce keyframe prompt — any period/place-specific detail | A few highly specific, verifiable details outweigh broad generic ones (heuristic: 3 correct specifics > 30 generic) | "[specific era/place]-accurate detail: [named anchor object]" | Name make/model/pattern explicitly or gen defaults to cliché — correct anchors buy credibility for invented elements too |
| World Bible | 월드 바이블 | /ms-plan output; cited by /ms-characters, /ms-storyboard, /ms-produce, and QA at every later stage | Consolidated doc of every locked design decision — palette, materials, silhouettes, prop rules | n/a — injected as a shared context block, never a discrete phrase | THE artifact reference banks are built from — inject as shared context into every prompt, NEVER re-typed per shot (see Doctrine §1) |
| Lookbook | 룩북 | /ms-characters or /ms-plan finalization — locking visual identity before production | The approved, finalized reference set locking visual identity for production | n/a — image-reference contract, not a text prompt | Ground-truth visual contract downstream generations must match; version-lock it — regenerating against a stale lookbook is a common failure |

### Sets, Props & Texture

| Term | KR | Use when | Effect | Prompt phrase | QA (+Caveat) |
|---|---|---|---|---|---|
| Set Dressing | 세트 드레싱 | /ms-produce keyframe prompt — completing a set's story logic | The act and the objects of dressing a set to complete its story logic | "detailed set dressing, specific background objects" | Under-dresses (showroom) or over-dresses (noise) — explicit density + logic cues ("sparse," "cluttered but purposeful") |
| Hero Prop | 히어로 프롭 | /ms-characters or /ms-plan prop lock; re-cited at every /ms-produce keyframe featuring the object | Named, story-critical object — must be visually exact and repeatable across every shot; any visible drift breaks trust instantly | "[locked object description], consistent hero prop" | Highest-frequency AI continuity failure — hand-prop shape/label/color drifts; REQUIRES a locked reference image driving every generation, never re-described |
| Background Prop | 백그라운드 프롭 | /ms-produce keyframe prompt — non-handled objects completing realism | Non-handled objects completing realism, no plot function; low individual scrutiny, collectively signals "real place" | n/a — covered by Set Dressing prompt phrasing | Lower continuity risk — some variance is tolerable, even desirable (avoids repeating-asset "video game" look); do not spend Hero-Prop-grade lock budget here |
| Standing Set / Redress | 스탠딩 세트 / 리드레스 | /ms-plan location planning → spaces-engineer environment reuse | A built/generated set kept and re-dressed to serve as a different location | "[location] redress of [standing set], [new dressing description]" | Maps to reusing one locked environment/Space and varying dressing prompts — cheaper and more consistent than regenerating geometry per shot (see Doctrine §12) |
| Patina & Distressing | 패티나 & 디스트레싱 | /ms-produce keyframe prompt — any surface/object/costume implying age or use | Controlled wear/aging/history on surfaces/objects/costumes, graded light/medium/heavy; separates "lived-in credible" from "prop-store pristine" | "weathered" / "worn" / "distressed" / "aged patina" (opposite state: "pristine" / "showroom-new") | Gen defaults to mid-clean; over-weighting → implausible uniform grime — pair with material-specific wear logic (rust ≠ fraying ≠ dust) |
| Continuity Photos/Notes | 컨티뉴이티 사진·기록 | Cross-stage — any item whose exact state must reproduce across shots/days | Photographing/logging exact state of every item for reproduction across takes/days | n/a — workflow practice, not a prompt fragment | Pre-digital ancestor of the reference bank — treat every locked reference image AS the continuity record |
| Scale & Proportion | 스케일과 비례 | /ms-plan world-building or /ms-produce keyframe prompt — any space carrying emotional meaning through size | Manipulating space size/ceiling height/object scale relative to characters to encode meaning (cramped = oppressive/intimate; cavernous = power/isolation/awe) | "low oppressive ceiling, cramped scale" / "cavernous scale, dwarfing negative space" | Human-to-room scale unstable across sequences — anchor with explicit human-reference proportions, verify against locked environment geometry |
| Fenestration | 개구부(창호) 구성 | /ms-produce keyframe prompt — any window/door used as compositional infrastructure | Windows/doors/openings as deliberate compositional/framing infrastructure | "framed by [window/doorway], light motivated through opening" | AI places openings with no light-logic — cross-check against `scenes[].lighting.motivation` before treating as pure composition (see Doctrine §10) |
| Visual Motif & Symbolic Prop | 비주얼 모티프 & 상징 소품 | /ms-plan world-building — any object/shape/color meant to recur and accumulate meaning | Object/shape/color recurring to accumulate meaning beyond literal function | "recurring [object/motif], consistent across every appearance" | Lock the motif's exact form via reference image — re-describing invites redesign-by-drift |

### Costume

| Term | KR | Use when | Effect | Prompt phrase | QA (+Caveat) |
|---|---|---|---|---|---|
| Costume Arc | 의상 아크 | /ms-characters costume lock; re-stated per shot at /ms-storyboard or /ms-produce when the act/beat changes | Wardrobe progression (silhouette, palette, condition) tracking the character's internal arc | "[character] costume, act [N] state: [silhouette/palette]" | Must be parameterized explicitly per shot — arcs don't emerge on their own (see Doctrine §4) |
| Silhouette | 실루엣 | /ms-characters costume lock — primary cross-shot consistency anchor | The outer shape a costume creates — first-read, distance-legible signal; readable in backlight/long shot | "[sharp / soft / angular / flowing] silhouette" | The MOST drift-resistant trait to lock for cross-shot consistency — more stable than fine texture/color (see Doctrine §2) |
| Costume Color Blocking | 의상 컬러 블로킹 | /ms-characters or /ms-storyboard — any multi-character/faction frame | Each character/faction gets a distinct, consistent color zone — instant "who's who / who's aligned" parsing without close-ups | "[character] in signature [color] block, distinct from ensemble" | Multi-character frames homogenize palette by default — state each character's color per figure (see Doctrine §5) |
| Costume Multiples | 코스튬 멀티플 | /ms-characters — establishing the locked reference for a costume state | Identical duplicate garments for one costume state (damage/stunts/continuity); count scales with stunt/damage load — from a few to dozens; NO fixed industry minimum | n/a — enforced via ONE locked reference image, not a prompt phrase | Direct analog to reference-bank enforcement — one locked reference image = the "digital multiple" (see Doctrine §3) |
| Costume Breakdown | 의상 브레이크다운 | /ms-produce keyframe prompt — any costume state implying elapsed time/hardship | Artificially aging a garment to match circumstances/timeline; pristine clothes after days stranded breaks credibility instantly | "breakdown-aged garment, [light/medium/heavy] wear matching [circumstance]" | Gen defaults to new-looking wardrobe — specify breakdown level per shot; same 3-tier doctrine as Patina & Distressing |
| Costume Plot | 코스튬 플롯 | /ms-storyboard — mapping every costume change against every scene's shot list | Master schedule mapping every costume change against every scene — the costume continuity spine | n/a — scheduling artifact; grounds the per-shot costume state authors write into keyframe prompts | Cross-check against Costume Arc before locking a scene's shot list — a missed change reads as a continuity error, not a style choice |

### Palette Coordination

| Term | KR | Use when | Effect | Prompt phrase | QA (+Caveat) |
|---|---|---|---|---|---|
| Location Color Identity | 로케이션 컬러 아이덴티티 | /ms-plan world-building; re-injected at every /ms-produce keyframe for a recurring location | A location's assigned dominant palette, reused every recurrence | "[location] in its established color identity: [palette]" | Log in World Bible → `visual_grammar.location_palettes`; re-inject per generation, never re-derived from scratch (see Doctrine §14) |
| Wardrobe-Set Palette Coordination | 의상-세트 팔레트 조응 | /ms-produce keyframe prompt — any shot where wardrobe and environment share the frame | Blending wardrobe into environment palette (belonging) or contrasting it (isolation/importance); 60/30/10 across combined wardrobe+set color mass [v] | "[character] palette blended into environment" / "…contrasted against environment for emphasis" | State the relationship explicitly (blend vs contrast) — gen will not infer intent from palette values alone; dominant/subordinate/accent tiers = `visual_grammar.palette` |
| Palette Pollution | 팔레트 오염 | /ms-produce keyframe prompt authoring + quality-reviewer QA pass | Uncoordinated color noise entering frame from props/dressing/wardrobe, unchecked against the intended palette; a single stray saturated object breaks color-driven mood/brand cohesion | "controlled palette — dominant/subordinate/accent only; plain unbranded packaging for anything off-palette" | Chronic highest-frequency failure — gen adds unrequested colorful clutter by default. Fix = positive reframe in-prompt (Doctrine §7) + human QA pass vs the 60/30/10 target; do NOT rely on negative_prompt (capability-gated, projection-layer only) |

### Commercial & Brand

| Term | KR | Use when | Effect | Prompt phrase | QA (+Caveat) |
|---|---|---|---|---|---|
| Hero Shot Staging | 히어로 샷 스테이징 | /ms-produce keyframe prompt — any product-as-subject commercial shot | Compositional treatment for a product as undisputed subject — pedestal, isolating negative space, key falloff to background | "product on pedestal, isolated by negative space, single key light falloff to black background" | AI clutters product shots by default — counter with explicit single-subject framing + negative-space composition; do not author a negative prompt (house lint bans it — see Doctrine §7) |
| Pack Shot | 팩샷 | /ms-produce final keyframe — the ad's closing beat | Final hero-clean product shot (with packaging) — the ad's closing beat; near-universally centered/symmetrical, brand-color background | "clean centered pack shot, plain brand-color background, single hero product" | Label/logo text is an AI weak point (garbled typography) — needs a locked product reference image, never text-described branding (see Greeking) |
| Greeking | 그리킹(브랜드 흐림 처리) | /ms-produce keyframe prompt — any prop/dressing carrying a real-world brand mark | Obscuring/replacing real brand logos on props/dressing to avoid clearance issues | "generic unbranded packaging" / "logo turned from camera" | Composite-from-asset doctrine: legible marks are NEVER text-described or generated — legal exposure. Enforced via `visual_grammar.prohibitions.greeking_required`; NO baked text in generated clips either way, all text burns in post (`baked_text_forbidden`) — never a negative prompt (see Doctrine §8) |

## Doctrine

1. **World bible primacy.** Every locked palette/prop/silhouette/set decision is written ONCE into the World Bible, then injected as shared context into every keyframe prompt and every reference-bank build — never re-typed or re-derived per shot. `Design Concept` → `visual_grammar.design_concept`.
2. **Lock hierarchy by drift risk.** Hero Prop (object) and Silhouette (costume) are the two highest-value locks in this file's domain: hand-prop drift is the single highest-frequency AI continuity failure; silhouette is the most drift-resistant identity trait — lock it first when finer cues (texture/color) prove unstable.
3. **Costume multiples = digital multiples.** Physical production builds identical duplicate garments per principal costume for damage/stunts/continuity — the count scales with stunt/damage load, from a few to dozens. Our pipeline's equivalent is ONE locked reference image per costume state — that single asset replaces the entire multiple set.
4. **Costume arc never emerges on its own.** Silhouette/palette/condition progression must be parameterized explicitly per shot (tie to act/beat) — never assumed from a general character-arc prompt.
5. **Multi-character color blocking.** State each figure's costume color block individually in any multi-character frame — gen homogenizes palette across figures by default.
6. **Wear logic is 3-tier and material-specific.** light / medium / heavy breakdown; name the material-appropriate decay (rust ≠ fraying ≠ dust), never a bare "worn." Default-pristine bias: any shot implying hardship/time/use MUST state breakdown level explicitly or gen renders showroom-new.
7. **Palette pollution — positive reframe only.** Never author a negative prompt ("no stray colors"). State the controlled palette itself ("plain unbranded packaging," "controlled palette: dominant/subordinate/accent only") — matches the house negation ban (filmcraft prompt-construction core rule).
8. **Greeking is composite-from-asset, not a negative prompt.** Any legible brand mark/label/plot-critical text = composited from a locked real asset (Pack Shot), NEVER text-described, NEVER generated, NEVER "fixed" with a negative prompt — legal exposure, not a style choice.
9. **Scale anchors to a human reference.** Always state an explicit human-reference proportion; verify against the locked environment/Space geometry rather than re-deriving scale per shot.
10. **Fenestration cross-checks lighting.** Window/door placement is composition infrastructure ONLY after it clears the scene's `scenes[].lighting.motivation` — an opening with no light logic reads as fake.
11. **Authenticity anchor heuristic.** 3 correct specifics (named decade/region/make-model) beat 30 generic ones. Always name; never gesture.
12. **Standing Set / Redress = locked-environment reuse economy.** Redress one locked Space across multiple scenes instead of regenerating geometry — cheaper AND more consistent (fewer generations = less drift surface).
13. **Art Director is a false friend.** NEVER use "Art Director" unqualified — qualify as `art_director_film` or `art_director_advertising` in any cross-department note; the two roles do not share a reporting line, a skill set, or an authority.
14. **Location Color Identity re-injects every recurrence.** Sourced from the World Bible, not re-invented per generation — it is what makes "we're back at X" read through color alone.

## Decision Tables

### A. Story Intent → Design Choice

| Intent | Design Choice |
|---|---|
| Confinement / repression | Low ceilings, cramped scale, blocked/small windows, warm-dim palette |
| Liberation / power gained | Cavernous scale, high ceilings, expansive negative space, palette opens/cools |
| World in decline | Heavy patina + distressing, desaturated palette, broken fenestration |
| Sterile control / utopia-façade | Pristine surfaces, symmetric dressing, tight monochrome-adjacent palette |
| Corruption arc | Silhouette sharpens + palette darkens act-over-act; dressing lived-in → curated/cold |
| Found-family warmth | Wardrobe-set palette blended (analogous); mismatched-but-harmonious props |
| Faction/ensemble clarity | Costume color blocking, held constant |
| Brand hero launch | Hero shot staging — pedestal + negative space + single key + brand-accent palette |

### B. Object/Task → Owning Department

| Object / Task | Owner |
|---|---|
| Weapon/phone/letter (actor-handled) | Property Master |
| Background bookshelf/furniture | Set Decoration |
| Wall paint, architectural finish | Production Design → Art Direction |
| What a character wears | Costume Design (separate department) |
| Skin/age makeup | HMU (coordinated with costume, not owned by it) |
| The unifying "big idea" | Production Designer |
| Ad-campaign visual concept | Creative Director + `art_director_advertising` — NOT the film role |

## Numeric Anchors [v]

- Costume Multiples: no fixed industry minimum — the count scales with stunt/damage load, from a few to dozens per principal costume. [costume supervision practice; a fixed "minimum 3" is not verifiable]
- Wardrobe-Set Palette Coordination: 60/30/10 split (dominant/subordinate/accent) across combined wardrobe+set color mass — convention, not law. [house convention, adapted from the general interior-design 60/30/10 rule — see Aliases disclosure]
- "Best Art Direction" → "Best Production Design": AMPAS renamed the Oscar category in 2012 (85th ceremony) — the naming-history root of the PD/AD ambiguity. [v — AMPAS Designers Branch]
- Drafting scale: 1/4"=1'-0" (1:48) ground plans, 1/2"=1'-0" models — physical-production provenance, not a prompt-authored value. [v — ADG]
- Authenticity anchors: ~3 correct specifics outweigh ~30 generic ones — craft heuristic, not independently [v]-sourced (see Period & Place Authenticity Anchor).

## Aliases & Do-Not-Confuse

**Pipeline-coined labels (disclosure):** *Authenticity Anchor*, *Location Color Identity*, *Palette Pollution*, and *60/30/10 applied as a film-design rule* are HOUSE-COINED names for real, verifiable practices (period research anchoring · per-location palette consistency · uncontrolled color clutter · interior-design color hierarchy). Use them freely inside this pipeline; do not cite them as standard industry terminology.

- **World Bible** ← alias: Style Bible (same artifact, two names in source literature — this file's canonical term is World Bible).
- **Background Prop** ← alias: Dressing Prop.
- **Property Master** ← alias: Props (colloquial short form; "hand props" = the objects themselves).
- **Costume Breakdown** ← alias: Aging (costume-specific instance of the general Patina & Distressing wear-logic doctrine — same 3-tier/material-specific rule, different department).
- **Standing Set / Redress**: two halves of one economy — Standing Set = the built/locked environment that persists; Redress = the act of re-dressing it for a new location. Always paired, never split.
- **Production Designer vs `art_director_film`**: modern default = Production Designer owns concept, `art_director_film` is operational (budget/draft/schedule) under the PD. Pre-1990s credits used "Art Director" as the TOP title, predating the 2012 Oscar rename; smaller/international productions may still top-title "Art Director" — confirm per market before assuming seniority from the title alone.
- **`art_director_film` vs `art_director_advertising`**: total false-friend, DO NOT interchange. Film: department manager under the Production Designer. Advertising: campaign visual-concept AUTHOR under a Creative Director — closer in authority to a film Production Designer than to a film Art Director. "Art Director" unqualified is BANNED in cross-department notes.
- **Set Decoration vs Set Dressing**: department/discipline (who) vs the act-and-objects (what/how) — both standard terms, they coexist, they are not synonyms.
- **Props vs Set Decoration boundary**: touch/use → Property Master; walk-past/background → Set Decoration. Borderline objects need an explicit hand-off note — the same touch/use test decides which asset gets Hero-Prop-grade locked-reference treatment.
- **Costume Design ≠ Art Department**: parallel department reporting outside Production Design/Art Direction; only palette-coordinates with them (see Wardrobe-Set Palette Coordination). Never silently fold costume into a generic "production design" prompt block.
- **Patina & Distressing vs Costume Breakdown**: same wear-logic doctrine (3-tier, material-specific), applied to surfaces/sets/props vs garments respectively — cite whichever term matches the asset class.

## AI-Gen Caveats

Pre-flight checklist (run before generation, per filmcraft A6):

1. **Hand-prop drift** (Hero Prop, Property Master) — highest-frequency failure. Lock via reference image; never re-describe from scratch shot-to-shot.
2. **Asymmetric wardrobe + flop** — a garment with an asymmetric closure/patch/detail invalidates the character reference bank if the clip is later horizontally flipped for a screen-direction fix. Flag asymmetric costume pieces explicitly in the World Bible/character sheet so post never flops that shot (`flop_forbidden`; house rule H9).
3. **Costume re-roll** — text-only costume description regenerates a plausible but non-identical garment. Requires reference-bank-enforced sheet + explicit Costume Arc state per shot.
4. **Palette pollution** — gen adds unrequested colorful clutter. Fix with positive reframe (Doctrine §7), never a negative prompt; QA checks against the 60/30/10 target.
5. **Logo/typography hallucination** — clearance risk. Fix is Greeking (composite from a locked Pack Shot asset) — never text-described branding, never a negative prompt.
6. **Default-pristine bias** — gen defaults to showroom-new. State breakdown/patina level explicitly on every shot implying time, use, or hardship.
7. **Scale/proportion instability** — human-to-room scale drifts across a sequence. Anchor with an explicit human-reference proportion + the locked environment/Space geometry.
8. **Era/region averaging** — diffusion models blend eras/regions toward a generic mean. Name the specific decade/region/make-model; image references outperform text.
9. **Cross-department palette bleed** — costume/set/props drift toward independently-chosen palettes. One palette spec (blend-vs-contrast intent stated) injected into every department's prompt from the World Bible.
10. **Showroom-generic set dec** — gen under-dresses by default. Explicit density + era + wear-logic cues ("sparse," "cluttered but purposeful").
11. **Fenestration with no light logic** — AI places openings compositionally, ignoring the actual light source. Cross-check against `scenes[].lighting.motivation` before treating as pure composition.
12. **World-state statelessness** — diffusion models hold no persistent world-state between keyframes. Every prompt carries the World Bible context explicitly; nothing "just remembered" from a prior shot.
13. **Standing-set reuse advantage** — redress one locked environment instead of regenerating geometry each time; cheaper AND reduces drift surface.
