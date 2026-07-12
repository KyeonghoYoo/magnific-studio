# Color & Grading — 색채·그레이딩

Palette systems, color-as-narrative dramaturgy, the named-look catalog, and the ffmpeg-side technical grade. `lighting.md` owns light sources/ratio/temperature/`exposure_bias`; `production-design.md` owns art-department color-as-object-design (World Bible, wardrobe/set palette). This file owns color HARMONY, MOOD ASSOCIATION, NAMED LOOKS, and the POST-PRODUCTION grade.

**Read this when:** setting `visual_grammar.palette`/`color_script` at /ms-plan; scene palettes at /ms-storyboard; grading at /ms-post.

## THE SPLIT (organizing spine)

Prompted color is MOOD and art-direction language (named looks, temperature words) — it is NEVER a grading instruction. ffmpeg owns precision, determinism, and uniformity (hex codes, saturation %, exact splits). A hex/%/exact-split string inside a generation prompt is a hard lint ERROR; brand hex lives ONLY in `edit_plan.color` + reference images. Every table cell below is effectively tagged **Prompt** (generation-time) or **ffmpeg** (post-time) — sometimes both.

```
visual_grammar.grade: { show_lut?: string, correction_before_grade: true }
```

Grade structure, in order: correction (neutral) → match (to a hero shot) → ONE conservative `show_lut` for the project's look family (the renderer's implemented path — applied uniformly via lut3d). Per-scene trims keyed to `color_script` beats are IMPLEMENTED as `edit_plan.color.scene_trims[]` — shot_id-keyed `eq`/`colorbalance`, applied per-clip right after normalization (before xfade blends, so blend pieces inherit them). Per-scene palette DESIGN still happens at GENERATION time (per-beat palette words in prompts) — trims are correction, not design. Because the show LUT is uniform, keep it conservative so it does not flatten a designed multi-scene color script. `correction_before_grade: true` locks the order.

## 1. CANONICAL TERMS

### Process & Matching

| Term | KR | Use when | Effect | Prompt phrase OR ffmpeg op | QA (+Caveat) |
|---|---|---|---|---|---|
| Color Correction | 색보정(1차 보정) | always first, every shot | invisible when right — reads "normal," not a look | N/A — ffmpeg: `eq` neutral anchor + `signalstats` to confirm legal range | no physical camera to match against — this step is de facto cross-shot matching between independent generations |
| Shot Matching | 샷 매칭 | any scene with >1 shot, after correction | invisible continuity; breaks immersion if skipped | ffmpeg via `color.scene_trims[]` (shot_id-keyed, reproducible in-plan; hero-shot choice is still a human/QA judgment): trim every shot's `colorbalance`/`eq` to a **hero shot** (the best-exemplar frame), never to a synthetic averaged histogram | independently generated clips drift in WB/saturation from similar prompts — matching is mandatory, not optional |
| Color Grading (Creative Look) | 컬러 그레이딩 | after shots are matched — a scene/film-level pass | shapes emotional register independent of literal frame content | Prompt: name the look ("bleach-bypass war grade"), never raw parameters — ffmpeg: `lut3d` show LUT (implemented, uniform) — per-scene trim = `color.scene_trims[]` (implemented, shot_id-keyed `eq`/`colorbalance` + one-line `why`) | zero hex/%/numeric splits in prompt text — hard lint |
| Brand Hex Matching | 브랜드 헥스 매칭 | any shot carrying a contractual-exact brand/product color | numeric-exact reproduction a text prompt cannot guarantee | Prompt: reference image only, never the hex — ffmpeg: `edit_plan.color` target + `colorbalance`, verified by pixel-sample/`signalstats` | hex/%/split string inside a generation prompt = hard lint ERROR; logos/legible text additionally need full asset composite (prompting.md `greeking`) |
| Scene-Referred vs Display-Referred | 씬 레퍼드 vs 디스플레이 레퍼드 | deciding where a transform belongs in the pipeline | clarifies why "raw" isn't an option here | N/A — ffmpeg only ever sees display-referred (often 8-bit SDR) frames | gen-video output is already baked, not scene-referred — no raw to fall back to if a grade clips |

### Harmony & Palette Systems

| Term | KR | Use when | Effect | Prompt phrase OR ffmpeg op | QA (+Caveat) |
|---|---|---|---|---|---|
| Complementary Harmony | 보색 조화 | pop, subject/background separation, conflict | high vibrance/tension; aggressive if both halves equally saturated | "teal shadows, warm orange skin/highlights" — ffmpeg: `colorbalance` shadows→cyan, highlights→warm | keep the split asymmetric — see Teal and Orange for the named skin application |
| Split-Complementary Harmony | 분할 보색 조화 | complementary-level contrast without harshness | vibrant but softer, more "designed" | "amber base, cyan and violet accents" | — |
| Analogous Harmony | 유사색 조화 | unified mood, naturalistic scenes (sunset, fire, autumn) | cohesive, low tension; flat if overused | "warm analogous palette, amber through red, temperature held warm throughout" | positive phrasing only — never "no cool accents" (negation lint ERROR, prompting.md §5) |
| Triadic Harmony | 삼각 조화 | stylized, comic-book, fantasy, heightened-reality | vibrant, busy; balanced only if one hue dominates | "triadic palette, magenta/yellow/cyan, one dominant" | frame-wide balance is a lighting/composition decision — grading can't invent a missing third hue |
| Monochromatic Palette | 단색 팔레트 | intense psychological focus (grief, obsession) or stylized signature | minimal, intense, claustrophobic or elegant | "monochromatic blue palette, vary only value/saturation" | — |
| Monochromatic + Accent (`monochromatic_accent`) | 단색+강조 조화 | a mono field carrying ONE saturated narrative anchor (Sin City register; `visual_grammar.palette.harmony` value) | the anchor's meaning is amplified by the silence around it | "near-monochrome [hue] palette, [subject/prop] carries the only saturated [accent] in frame" | the harmony-scheme form of Accent Color + Saturation Discipline below — one scheme, three entries |
| Accent Color / Color Pop | 강조색 | directing eye to a character/prop; narrative significance | immediate focal pull | "desaturated scene, [subject] retains full saturated red" | hard to prompt reliably in one pass — safer to generate, then isolate + desaturate the rest in post |
| 60-30-10 Color Hierarchy | 60-30-10 색채 위계 | planning any deliberate palette (`visual_grammar.palette.dominant/subordinate/accent`) | visual hierarchy and calm even with multiple hues | "[dominant] environment, [subordinate] secondary elements, small [accent] detail" | approximate heuristic, not literal pixel count; pair with `palette.forbidden[]` — excluded colors enforced at both prompt and grade |
| Saturation Discipline (Single Anchor) | 채도 절제 | preventing "color soup" | anchor's impact rises by contrast with a quiet field | "muted/desaturated palette except [anchor]" — ffmpeg baseline: `eq=saturation=0.6` (band 0.5–0.7; eq params are expressions — never write a hyphenated range) | — |
| Color Script (Pixar Method) | 컬러 스크립트 | planning palette continuity before any shot is generated | guarantees the emotional curve reads through color alone — THE drift workaround in this pipeline | per-beat target restated INSIDE every shot's prompt for that beat (`color_script[].{beat,palette_target,saturation,temperature}`) | every shot in a beat carries that beat's palette words verbatim, not just a citation — see Doctrine #2 |
| Palette Progression Patterns | 팔레트 전개 패턴 | shaping how the palette moves across the arc | palette becomes a legible emotional timeline | state target saturation/temperature per beat — ffmpeg: `eq=saturation` stepped per scene-group | patterns: desaturate-to-low-point-then-restore · warm→cool betrayal shift · monochrome→color liberation |
| Location Palette Signature | 장소별 팔레트 시그니처 | multi-location stories, cross-cutting between worlds | instant orientation on cut | fix a named palette per location, repeat it VERBATIM every time (`visual_grammar.location_palettes.<location>`) — ffmpeg: dedicated LUT preset per location | reuse the same reference image too — see Doctrine #3; art-department authoring side = production-design.md's Location Color Identity (same field, complementary framing) |

### Color Dramaturgy

| Term | KR | Use when | Effect | Prompt phrase OR ffmpeg op | QA (+Caveat) |
|---|---|---|---|---|---|
| Bellantoni Color-Story Associations | 벨란토니 색채 서사 연상 | choosing a dominant hue to reinforce or ironically undercut | primes audience emotion below conscious notice | name hue + intended association — "sickly green fluorescent lighting, unease" | red=power/danger/passion · yellow=obsession/caution · blue=detachment/calm/melancholy · green=ambivalence/sickness · purple=mystical/mortality · orange=warmth/vitality — DEFAULTS, not laws (Doctrine #4) |
| Storaro Color-as-Dramaturgy | 스토라로의 색채 극작법 | planning a full-film color arc tied to the psychological journey | color shifts register as narrative punctuation across acts | describe the arc across acts — "cool clinical blue act 1 warming to amber act 3" — ffmpeg: distinct presets per act | — |
| Cultural Color Variance | 문화적 색채 차이 | any project for a non-Western audience, esp. KR/Asia | a "default" Western choice can misfire | flag target market in `project_brief`; sanity-check red/white/green before locking `visual_grammar.palette` | split claims by market — CN: red=luck/celebration, green hat=infidelity · KR: white=mourning ✓; red-as-celebration is weaker than CN; **a person's NAME written in RED reads as death in Korea — direct caption/on-screen-text hazard, add to commercial QC** · purple=royalty in BOTH traditions (no variance) |

### Looks Catalog
*(named looks — always prompt-side art direction first; ffmpeg reproduces/finishes)*

| Term | KR | Use when | Effect | Prompt phrase OR ffmpeg op | QA (+Caveat) |
|---|---|---|---|---|---|
| Teal and Orange | 틸앤오렌지 | skin pop against environment; "commercial blockbuster" look | high vibrance, polished; cliché if unrestrained | "cool teal shadows, warm sun-kissed skin, moderate contrast" — ffmpeg: `colorbalance` ±0.1–0.2 | a named application of Complementary Harmony, not a separate system; calibrated historically on lighter skin — pushed hard on deeper tones it caricatures, stay conservative and protect the skin line |
| Bleach Bypass | 블리치 바이패스 | war, grit, trauma, moral bleakness | harsh, silvery, "stripped" | "bleach-bypass war-film look, desaturated, high contrast, heavy grain" — ffmpeg: `eq=saturation=0.4:contrast=1.2` (usable band: sat 0.3–0.5, contrast 1.15–1.3 — eq params are EXPRESSIONS; a hyphenated range evaluates as subtraction) + `noise` for grain | do not confuse with Cross-Process — this DESATURATES (silver retention); ENR is the historical Technicolor process it emulates digitally |
| Day-for-Night | 데이 포 나이트 | night scenes where a real-night generation reads flat | simulated moonlit night; a lit sky is the usual tell | generation-time framing FIRST — sky excluded/overcast (lighting.md's `blue_hour`) — ffmpeg finishes the sell: darken + blue push + vignette | primarily a GENERATION problem, not a grade — if sky is visible in the plate, no grade sells it; the literal `day_for_night` string is a banned prompt token (lighting.md) |
| Film Emulation (Halation/Grain/Gate Weave) | 필름 에뮬레이션 | filmic/period/prestige look, or to mask banding | tactile, analog, "expensive"; grain mitigates banding | "16mm halation around neon, visible grain, slight gate weave" — ffmpeg: noise for grain only | halation is PROMPT-SIDE ONLY, no ffmpeg filter exists; `visual_grammar.look.film_stock` changes it — CineStill 800T glows, Vision3 500T stays clean despite similar tungsten lineage |
| Selective Color / Spot Color | 선택적 컬러 | singular narrative emphasis | extremely strong, unmistakable; cannot be subtle | "[element] rendered in full saturated [color], rest of frame monochrome" | easier at generation (mask/inpaint) than by ffmpeg keying |
| Neon/Cyberpunk Palette | 네온/사이버펑크 팔레트 | sci-fi, night urban, tech/dystopia | heightened, artificial, alienating-but-alluring | "neon magenta and cyan practicals, crushed blacks, wet reflective surfaces" | driven by in-frame light sources that must be prompted at generation — grading flat footage won't convince |
| Pastel / A24 Soft Look | 파스텔/A24 룩 | "elevated indie" register, dreamlike or twee | soft, muted, nostalgic-but-uneasy | "soft pastel palette, lifted blacks, gentle low-contrast, muted" — ffmpeg: `eq=contrast=0.9:saturation=0.78` (band: contrast 0.85–0.95, sat 0.7–0.85) | — |
| Sepia Nostalgia Tone | 세피아 | memory, flashback, historical framing | immediately codes "past" | "sepia-toned, antique photograph look" — ffmpeg: `colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131` (sepia coefficients — colorchannelmixer has NO presets; `curves` is the preset filter) | — |
| Cross-Process | 크로스 프로세스 | 90s fashion/music-video, grunge register | high-contrast cyan-shadow/yellow-green-highlight casts | "cross-processed film look, cyan shadows, yellow-green highlight cast" — ffmpeg: `curves=preset=cross_process` (built-in) | adds color casts, does not desaturate — see Bleach Bypass |
| Filmic Flat (Lifted-Black Trend) | 필믹 플랫 | deliberately, for a soft/hazy register — not as default | dreamy when intentional; cheap/unfinished when it's just missing contrast design | specify INTENT — "soft hazy morning light" — never bare "flat" | [v, disputed] colorists call this a preset fad — caution entry, not a recommendation; gen-video is never actually log (see Log Capture) |

### Tonal Shape & Technical

| Term | KR | Use when | Effect | Prompt phrase OR ffmpeg op | QA (+Caveat) |
|---|---|---|---|---|---|
| White Balance Storytelling Bias | 화이트밸런스 스토리텔링 바이어스 | the single most reliable one-lever mood tool | warm=nostalgia/comfort, cool=alienation/clinical/danger | "warm amber white-balance bias, nostalgic" / "cold blue-white balance, clinical" — ffmpeg: `colorbalance` single-axis | — |
| Gamma Mood | 감마 무드 | fast genre-coding (prestige drama vs comedy) | low midtones read serious, raised read light/optimistic | "darker midtones, somber" / "bright airy midtones" — ffmpeg: `eq=gamma=0.9` somber (band 0.85–0.95) / `eq=gamma=1.1` bright (band 1.05–1.15) | do not confuse with `exposure_bias` — that's a `lighting.md` generation-time field; this is a POST grading lever |
| Tonal Shape Control (Black Point + Highlight Rolloff) | 톤 셰이프 컨트롤 | lifted=dreamy/nostalgic; crushed=harsh/noir | biggest single lever for perceived "mood temperature" of contrast | "lifted, hazy shadows, soft filmic shoulder" / "deep crushed blacks, noir" — ffmpeg: curves black-end/shoulder points | crushing 8-bit sources risks shadow banding — pair with light grain |
| LUT (1D/3D .cube) | 룩업테이블(LUT) | applying one consistent look across many shots in one operation | bakes a look into one deterministic op | N/A — ffmpeg: `lut3d=file=look.cube` (or haldclut) | the renderer applies `edit_plan.color.show_lut` as ONE uniform pass — keep it conservative so it does not flatten a designed multi-scene color script; per-scene variance = generation-time palette words + `color.scene_trims[]` correction (see spine); LUT = the file, "look" = the creative target, "grade" = the act |
| Log Capture | 로그 촬영 | vocabulary/QC concept only in this pipeline | — | N/A | HARD BAN: gen models don't output log — never apply a log-decode LUT to gen-video output |
| SDR Delivery Space (Rec.709/sRGB) | SDR 딜리버리 공간 | confirming the target delivery space | shared primaries/D65, different transfer function | N/A — ffmpeg: confirm `-color_range` matches target | — |
| Wide-Gamut Delivery (P3) | 광색역 딜리버리(P3) | cinema/wide-gamut delivery targets | punchier reds/greens; clipping risk on 709 downconvert | N/A | — |
| ACES | ACES | QC vocabulary/context only here | device-independent scene-referred pipeline | N/A | ACES 2.0 shipped 2025 (reworked Output Transforms), governance → ASWF Aug 2025 — 1.x and 2.0 render differently [v] |
| 8-bit Banding | 8비트 밴딩 | always check skies, soft walls, bokeh, gradients | reads as a technical flaw | N/A — ffmpeg: light noise (dither) on gradient-heavy shots; avoid steep curves on 8-bit without grain | common gen-video artifact on generated skies/gradients — grain/dither doubles as Film Emulation |
| Legal Levels / Broadcast Safe | 리걸 레벨 | every delivery | signal stays within legal/studio-swing range | N/A — ffmpeg: `signalstats` min/max assertions per shot; explicit `-color_range` on encode | automate with signalstats — manual scope-checking doesn't scale to dozens of generated shots |
| Memory Colors | 기억색 | always — the primary QC anchor for "looks off" | deviation reads instantly as wrong | N/A — check sky/skin regions specifically | gen models sometimes render skies/foliage with a subtle wrong-hue cast a real camera never would |
| Skin Tone Line (Vectorscope) | 스킨톤 라인 | verifying skin isn't pushed off-natural; most important scope check | deviation reads instantly as sunburn/jaundice/"wrong" | N/A — no vectorscope in ffmpeg: `signalstats` on a skin crop as rough proxy, or QC by eye | phase angle ≈116–126°, simplified 123°, ±10° vendor variance [v]; highest-risk blind spot for ffmpeg-only — keep global grade intensity moderate |
| Skin Protection While Styling | 스킨 프로텍션 | any heavy stylized grade on shots with people | prevents actors reading sunburnt/sick under a strong grade | N/A | without scopes, favor conservative `colorbalance` magnitudes over precise keying |

## 2. DOCTRINE

1. **Pipeline order is fixed.** Correction → match (to a hero shot, never a synthetic averaged histogram) → look/grade. Never skip a stage.
2. **Color Script is the drift workaround, not a reference doc.** Per-beat targets (`color_script[].{beat,palette_target,saturation,temperature}`) are RESTATED inside every shot's keyframe prompt for that beat — filing it once and citing it is not enough, models carry no state between generations. Scene-level deviation from the arc goes through `scenes[].palette_note`.
3. **Location signatures restate verbatim**, same logic as #2, keyed by location: `visual_grammar.location_palettes.<location>` repeated word-for-word every time that location recurs, with the same reference image reused.
4. **Associations are defaults, not laws.** Bellantoni's color-emotion mapping is overridable by genre/context/saturation — and it is culture-bound: run Cultural Color Variance BEFORE locking a palette for a non-Western audience — split by market per that row (CN: red=luck/celebration · KR: white=mourning; a name written in RED reads as death — caption/on-screen-text QC hazard).
5. **Memory-color QC, conservatively.** Skin/sky/foliage are the primary "looks off" detectors because viewers have hard-wired expectations for them. ffmpeg has no vectorscope/waveform — `signalstats` on a crop is the only proxy — so keep grade magnitudes conservative; there's no scope to catch an overshoot before delivery.
6. **No persistent state is why any of this exists.** Hero-shot matching, Color Script re-injection, location-signature restatement, and the conservative uniform show LUT + `scene_trims[]` correction all exist because prompted color drifts shot to shot even from identical prompts.

## 3. DECISION TABLES

**A. Mood/Genre → Palette & Grade**

| Mood/Genre | Harmony | Bias | ffmpeg |
|---|---|---|---|
| Action/blockbuster | Complementary | Teal shadow/orange skin | `colorbalance` moderate |
| War/trauma/grit | Desaturated mono | Cool-neutral, silvery | low sat + high contrast + grain |
| Romance/nostalgia | Analogous warm | Warm amber WB | warm `colorbalance`, lifted blacks |
| Horror/thriller | Complementary/mono | Sick green or crushed cool | cool + curves crush |
| Sci-fi/cyberpunk | Triadic/complementary | Neon magenta-cyan, crushed | `colorbalance` extremes + contrast |
| Indie/dramedy | Pastel/desaturated | Soft, lifted, low contrast | low contrast + lifted curve |
| Fantasy/heightened | Triadic | Saturated | prompt-level mainly |
| Historical/period | Sepia or warm desaturated | Warm/brown | sepia mixer or warm `colorbalance` |
| Corporate/clinical | Cool complementary | Blue-cool, high key | cool + raised gamma |

**B. Arc Position → Progression**

| Position | Saturation | Temperature | Contrast |
|---|---|---|---|
| Setup/normalcy | Full/baseline | Neutral-warm | Moderate |
| Rising complication | Desaturation begins | Cooling starts | Slightly higher |
| Low point/crisis | Most desaturated | Coolest/starkest | Highest (crushed) or flattest (numb) |
| Resolution/liberation | Returns, often above baseline | Warms again | Normalizes, softer rolloff |

## 4. NUMERIC ANCHORS [v]

- Legal levels: Rec.709 8-bit 16–235 luma/16–240 chroma · 10-bit 64–940/64–960 · full range 0–255 [v]
- Gamma/gamut: Rec.709 gamma 2.4 (Rec.1886) vs sRGB ~2.2 · DCI-P3 white ~6300K, Display P3=D65 · gamut coverage 709 35.9%/P3 53.6%/2020 75.8% [v]
- Skin vectorscope angle: ≈116–126°, simplified 123° (+I axis), ±10° vendor variance [v]
- Hue-wheel geometry (definitional, not [v]): complementary 180° · split-complementary ±30° off the complement · triadic 120° spacing
- 60-30-10: design heuristic, approximate — not literal pixel count
- ffmpeg `colorbalance` range: params ∈ [-1.0, 1.0] [v] · teal-orange moderate use ±0.1–0.2 [v]
- Black point (8-bit): legal floor 16 · lifted target ~25–40 · crushed toward/below 16 [v]
- Grade emulation presets: bleach bypass `eq=saturation=0.4:contrast=1.2` (usable band: sat 0.3–0.5, contrast 1.15–1.3 — eq params are EXPRESSIONS; a hyphenated range evaluates as subtraction) [v] · pastel/A24 `eq=contrast=0.9:saturation=0.78` · saturation-discipline baseline `eq=saturation=0.6` · gamma mood `eq=gamma=0.9` somber / `eq=gamma=1.1` bright (single values only — bands live in the rows above)
- ENR silver retention: ~0–80 IR densitometer units [v]
- ACES: 2.0 shipped 2025; governance → ASWF Aug 2025 [v]

## 5. ALIASES & DO-NOT-CONFUSE

| Canonical | Aliases |
|---|---|
| Color Grading | color timing, "the grade," grading pass |
| Shot Matching | color matching, balancing |
| Teal and Orange | orange and teal, T&O, "blockbuster look" |
| Bleach Bypass | ENR (the historical Technicolor trade name for one bleach-bypass process) |
| Cross-Process | cross-processing, xpro |
| Filmic Flat | lifted-black look, "log look" |
| Day-for-Night | nuit américaine |
| LUT | look-up table, .cube |

**Do not confuse:** `exposure_bias` (BRIGHTNESS, a `lighting.md` generation-time field) vs Gamma Mood/Tonal Shape Control (POST grading levers) · high-key/low-key (RATIO classes, `lighting.md`) vs Tonal Shape Control (this file's post-grade contrast-design axis) · LUT (the deterministic file/transform) vs "look" (the creative target it encodes) vs "grade" (the act of getting there) · Teal and Orange (one named application) vs Complementary Harmony (the wheel relationship it draws on) · Color Script (the per-beat planning method) vs Palette Progression Patterns (the arc shapes it can encode) · Bleach Bypass (desaturates + contrast/grain) vs Cross-Process (adds color casts, no desaturation) · Filmic Flat (a deliberate style choice) vs Log Capture (gen-video is never actually log — nothing to imitate-from-source) · Location Palette Signature (this file, color-harmony/repetition angle) vs production-design.md's Location Color Identity (World Bible authoring/logging angle) — same `location_palettes` field, complementary framings.

## 6. AI-GEN CAVEATS

- **Prompted color is mood language, never a grading instruction.** Reliable for named looks/temperature words; unreliable for precision (hex, saturation %, wheel math).
- **Shot-to-shot consistency is not guaranteed, even from identical prompts.** No persistent scene state; I2V preserves intra-clip continuity, not inter-clip.
- **The ffmpeg pass absorbs both the technical match and the creative grade**, correction → match → look, in that order — never reversed.
- **Drift workarounds, in priority order:** Color Script re-injected per beat into every shot's prompt · same reference/style image reused across a scene's generations · conservative uniform show LUT + `scene_trims[]` correction (masks residual drift, doesn't fix it) · locked lighting-descriptor vocabulary shared with `lighting.md`.
- **"cinematic" is an empty token when bare** — pair with a concrete technical noun (film stock, camera body, `<N>mm`, f/`<N>`, named lighting pattern, aspect ratio); same discipline for bare "moody"/"dramatic lighting" — name the actual color/contrast move instead.
- **8-bit banding compounds:** generated skies/gradients + a range-stretching grade → visible banding. Grain/dither fixes it and doubles as film emulation.
- **No-scope risk:** ffmpeg has no vectorscope/waveform — pair every grade with `signalstats`/histogram checks; mandatory at generative shot volume, since manual scope-checking doesn't scale to dozens of generated shots.
- **Halation is prompt-reliable, ffmpeg-unavailable** — plan it at generation, never post.
- **Never apply a log-decode LUT to gen-video output** — there is no log capture in this pipeline to decode.
