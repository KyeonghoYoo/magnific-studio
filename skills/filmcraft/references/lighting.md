# Lighting — 조명

Canonical lighting vocabulary and the scene-level lighting contract. Lighting continuity is the **#1 documented AI-pipeline failure** — this file carries the fix.
**Read this when:** setting `visual_grammar.lighting_bible` at /ms-plan; filling `scene.lighting` at /ms-storyboard; composing keyframe prompts at /ms-produce; judging lighting_continuity at QA.

## THE SCENE LIGHTING CONTRACT (organizing spine)

Lighting is authored ONCE per scene as a struct, rendered into ONE lighting sentence, and injected **byte-identical** into every keyframe prompt of that scene. Paraphrase IS the failure mode — a struct cannot be paraphrased. Per-shot overrides require a logged reason (= telling the script supervisor before you move the key).

```
scene.lighting: {
  time_of_day:   dawn | golden_hour | day | overcast | blue_hour | night | interior_day | interior_night
  key_direction: front | front_left | front_right | side_left | side_right | back_left | back_right | top | under | ambient
  key_quality:   hard | soft
  ratio:         flat_1_1 | mild_2_1 | standard_4_1 | low_key_8_1 | extreme_16_1
  contrast_proxy: <REQUIRED — from the canonical table below, never invented per shot>
  color_temp_k:  1800–7500 (+ color_note gloss — emit Kelvin AND gloss, never Kelvin alone)
  pattern:       none | rembrandt | loop | split | butterfly | broad | short | rim | silhouette   (optional; portrait geometry)
  motivation:    string|null — the plausible source ("window", "the desk lamp is the ONLY light source, casting light onto the subject")
  exposure_bias: bright | neutral | dark
}
```

**Canonical ratio → proxy table (byte-stable; the proxy is what enters the prompt):**

| ratio | stops | contrast_proxy (verbatim) | Register |
|---|---|---|---|
| flat_1_1 | 0 | "flat even illumination, shadow side as bright as the key, seamless shadowless light" | comedy, corporate, sanitized |
| mild_2_1 | 1 | "gentle modeling, shadow side one stop under, soft shadow detail" | romance, friendly interview |
| standard_4_1 | 2 | "clear shadow side, visible but detailed shadow" | standard drama default |
| low_key_8_1 | 3 | "shadow side barely visible, deep shadow, only a sliver of detail" | noir, thriller, moral ambiguity |
| extreme_16_1 | 4 | "shadow side reads near-black, subject edge lost in shadow" | horror, chiaroscuro, near-silhouette |

**HILL — high-key / low-key are RATIO CLASSES, not brightness.** A noir frame is full of hot speculars; a high-key frame can be dim. `key_class` (high_key ⇔ ≤2:1, low_key ⇔ ≥8:1) is DERIVED for QA only and **never enters a prompt** (models trained on photo tags read "high-key" as "bright"). Brightness is the separate field `exposure_bias`.

## 1. CANONICAL TERMS

### Sources & roles

| Term | KR | Use when | Effect | Prompt phrase | QA / Caveat |
|---|---|---|---|---|---|
| key light | 키 라이트(주광) | every setup — the reference all else is ratio'd to | defines form, shadow direction, base exposure | "key light from [direction], [quality]" | direction consistent across the scene |
| fill light | 필 라이트(보조광) | deliberate contrast control | opens or preserves shadow detail | (expressed via the ratio PROXY, never "fill") | — |
| rim / backlight | 림/역광 | separation from a same-tone background; mystery, glamour | bright edge separates figure; depth | "thin rim light from behind, bright edge separating subject from background" | models bloom rims into full glow — say "thin/narrow edge only" |
| kicker | 키커 | dimension on the shadow-side cheek/shoulder | subtle dark-side sculpting | "low kicker light on the shadow-side cheek" | — |
| background light | 배경광 | prevent subject melting into background; independent mood | depth separation | "background lit separately in [tone], subject in [tone]" | — |
| catchlight | 캐치라이트(눈빛) | any close-up where the eyes must read alive | absence reads dead-eyed/exhausted/villainous | "catchlight visible in the eyes, small specular highlight" | models omit/misplace — state explicitly, expect cross-shot variance |
| practical | 프랙티컬(극중 광원) | in-frame lamp/neon/candle/TV selling the motivated source | grounds light in the story world; production value | "lit only by the [practical] in frame, warm pool of light around it — the [practical] is the ONLY light source, casting light onto [subject]" | models render practicals as decorative unless told they ILLUMINATE |
| motivated lighting | 동기부여 조명 | default doctrine for naturalistic work | invisible craft; believability | motivation field names the source | unmotivated stylization is a choice, logged |
| available light | 어베일러블 라이트 | documentary naturalism, verité | maximal realism | "lit only by available light, naturalistic" | — |
| negative fill | 네거티브 필 | deepening shadow by subtraction (flat overcast) | dimensionality without hot spots | **do not name it** — models cannot subtract; emit the RESULTING shadow ("shadow side deepened, no ambient bounce") | QA-only concept |

### Quality & contrast

| Term | KR | Use when | Effect | Prompt phrase | Caveat |
|---|---|---|---|---|---|
| hard light | 하드 라이트 | tension, noir, sun, single bulb | crisp shadow edges, high specularity, reveals texture | "hard direct light, sharp-edged shadows" | — |
| soft light | 소프트 라이트 | glamour, romance, naturalism, flattering skin | gradual wraparound falloff | "soft diffused light, gentle shadow falloff, large source" | — |
| bounce / book light | 바운스/북 라이트 | very soft invisible-source key (beauty, interview) | extremely soft wraparound | "light bounced off a large white surface, very soft wraparound" | describe the effect, not the rig |
| exposure_bias | 노출 바이어스 | overall brightness intent — SEPARATE from ratio | bright = airy/optimistic; dark = somber/serious | "bright airy exposure" / "dark, underexposed mood" | this is what "high-key exposure" colloquially meant — renamed to avoid the ratio collision |

### Direction patterns (portrait geometry; optional field — validate against key_direction)

| Pattern | KR | Geometry | Register | Prompt phrase | Caveat |
|---|---|---|---|---|---|
| rembrandt | 렘브란트 | key 45–60° off-axis, elevated → small lit TRIANGLE on the shadow cheek | dignified drama, painterly | "Rembrandt lighting, triangle of light on the shadow cheek, key at 45 degrees" | canonical = strict triangle (eye-width × nose-length, far eye lit); industry drift tags any 45° key "Rembrandt" — the triangle is the test; models produce a vague glow unless the triangle is named |
| loop | 루프 | key 30–45°, small nose shadow NOT touching the cheek | approachable everyday default | "loop lighting, small nose shadow not touching the cheek, soft modeling" | loop 30–45° / rembrandt 45–60° / split 90° = a continuum [v] |
| split | 스플릿 | key at 90° — exactly half the face lit | duality, inner conflict, interrogation | "split lighting, hard vertical divide, half the face in shadow" | — |
| butterfly | 버터플라이 | key on-axis, high, ~45° down → symmetrical shadow under the nose | old-Hollywood glamour, beauty | "butterfly lighting, key high and centered, small symmetrical nose shadow" | hollows eyes without under-fill |
| broad | 브로드 | key lights the side of a turned face TOWARD camera | widens the face, brightens mood | "broad lighting, camera-facing side of the turned face lit" | — |
| short | 쇼트 | key lights the side turned AWAY from camera | slimming, contoured, dramatic | "short lighting, far side of the turned face lit, near side falling to shadow" | — |
| rim (pattern) | 림 실루엣 | edge-only emphasis against darkness | graphic, sculptural | "edge light tracing the profile against a dark background" | — |
| silhouette | 실루엣 | anonymity, iconicity, mystery | subject = pure shape | "full silhouette against a bright background, subject in complete shadow, only the outline visible" | models restore facial detail for legibility — repeat the negation-free constraint ("in complete shadow, only the outline"); retries expected |
| top / under (via key_direction) | 탑/언더 | top = interrogation/ominous or divine-if-soft; under = horror inversion | hard downward sockets / unnatural up-shadows | "harsh top light, deep eye-socket shadows" / "uplight from below, unnatural inverted shadows" | direction field carries these; pattern stays none |

### Color temperature & time of day

| Term | KR | Kelvin | Prompt phrase |
|---|---|---|---|
| candle / fire | 촛불/화톳불 | ≈1800–2000K | "warm firelight flicker, orange glow on faces" (stills: describe the instant's shadow irregularity; flicker is the video stage's job) |
| tungsten practical | 텅스텐 | 2700–3200K | "warm tungsten lamplight, 3200K" |
| golden_hour | 골든아워 | ≈3000–4000K → 1800–2000K at horizon; sun 0–6° [v]; duration is latitude/season dependent — ~20–30 min near the equator, 60–90+ min at mid latitudes (Seoul ~37.5°N) | "golden hour, warm low-angle sun, long soft shadows" — name the LOW ANGLE + LONG SHADOWS or models render a static orange filter |
| day (5600K) | 주광 | 5600K | "neutral daylight, 5600K" |
| overcast | 흐림 | ~6000–7500K (working default — published ranges vary widely, ~4600–8000K) | "soft overcast daylight, even diffused light" — directionless; add shape via a described shadow side |
| blue_hour | 블루아워 | sun below horizon; deep blue ambient | "blue hour, deep blue sky, no direct sun, warm practicals glowing" |
| mixed warm-cool | 웜-쿨 교차 | e.g. 3000K practical vs 6500K window | "warm lamplight key against cool blue window light, color contrast" — the lighting-side origin of teal-orange |
| sodium vapor | 나트륨등 | ≈2000–2200K, near-monochrome spectrum | "sodium vapor streetlight glow, amber-orange night" — REAL sodium desaturates (models tint instead); modern city LED varies ~3000–5000K by city/retrofit generation (warm-LED policies trending), so amber is a period/style choice [v] |
| fluorescent institutional | 형광등 | 3500–4300K + green spike [v] | "flat overhead fluorescent light, slight green tint, sterile institutional mood" |

### Named looks (prompt recipes)

| Look | KR | Recipe (prompt kernel) |
|---|---|---|
| chiaroscuro | 키아로스쿠로 | "single hard source, deep black shadows, painterly high contrast" + extreme_16_1 proxy |
| film noir venetian | 누아르 베네시안 | "hard key through venetian blinds, striped shadows across the face, deep blacks, wet street reflections" |
| neon noir | 네온 누아르 | "magenta and cyan neon practicals as the only light, wet reflective street, deep shadow" (light sources must be IN the prompt — grading flat footage won't convince) |
| Vermeer window | 베르메르 창광 | "soft window light from one side, gentle falloff, quiet domestic interior" |
| candlelight naturalism | 촛불 자연광 | "lit entirely by candlelight, warm flicker, deep surrounding darkness, period naturalism" |
| moonlight convention | 월광 블루 | "cool blue moonlight, silvery highlights, night exterior" — a CONVENTION, not physics (real moonlight ≈4100–4500K warm-neutral) |
| volumetric / god rays | 볼류메트릭/갓레이 | "volumetric light shafts through haze, god rays through the [window/canopy], visible dust in the beam" |
| halation / lens-facing source | 헐레이션 | "light source facing the lens, flare and soft halation bloom around highlights" (prompt-side only — no ffmpeg halation) |

## 2. DOCTRINE

1. **The text is the set.** No physical set persists between generations, so the lighting sentence IS the lighting plot: struct → one sentence → byte-identical in every keyframe prompt of the scene. Validator: `distinct(lighting_sentence) per scene == 1`.
2. **Ratio numbers are spec; proxies are prompts.** "8:1" never enters a prompt (weakly parsed); the canonical proxy sentence does. The number stays in the artifact for QA.
3. **Light must have a reason.** Default doctrine is motivated light (window, lamp, sun, fire, screen, neon). Unmotivated stylization is legal but logged. When a practical is the source, say it ILLUMINATES ("the only light source, casting light onto…") or it renders decorative.
4. **Direction is a character statement:** front = open/flat · side = conflicted/dimensional · back = mystery/iconic · top = judgment (or grace, if soft) · under = wrongness.
5. **One scene, one key.** The key does not change direction/quality/temperature between shots of one scene without a story reason + logged override. This is ordinary set discipline — here it is also the single highest-ROI consistency lever in the pipeline.
6. **Banned prompt terms:** bare ratio numbers · key_class words (high-key/low-key) · negative_fill (emit the resulting shadow) · day_for_night (unreliable — prompt blue_hour or "moonlit overcast" and finish in ffmpeg) · magic_hour (ambiguous — use golden_hour or blue_hour).
7. **Exteriors:** sun as backlight, faces filled by described bounce ("sun behind the subject, face softly filled"); overcast = a giant directionless softbox — add shape by describing the shadow side.

## 3. DECISION TABLE — mood/genre → lighting

Every cell in the schema-field columns is a LITERAL value an authoring agent copies verbatim — `color_temp_k` cells are single integer defaults (usable bands + source prose live in the motivation column).

| Mood/Genre | key_direction | ratio | color_temp_k | key_quality | pattern | motivation (prose) |
|---|---|---|---|---|---|---|
| Romance / intimate | front_left \| front_right | mild_2_1 | 3000 | soft | loop | warm practical lamp (band 2700–3200) |
| Everyday drama | side_left \| side_right | standard_4_1 | 5600 | soft | loop | window daylight — set scene-true from the §2 time_of_day table |
| Noir / crime | side_left \| side_right | low_key_8_1 \| extreme_16_1 | 3200 | hard | split \| rembrandt | venetian blinds, street practicals; cool ambient goes in color_note |
| Horror / dread | under \| top | extreme_16_1 | 3200 | hard | none | single hard source below/above (band 2000–4300 by source: candle→bare bulb) |
| Comedy / corporate | front | flat_1_1 \| mild_2_1 | 4300 | soft | none | even office/daylight (band 3500–5600) |
| Sci-fi / tech | side_left \| top | standard_4_1 \| low_key_8_1 | 6500 | hard | rim | colored kicker practicals, magenta/cyan accents (band 5600–7500) |
| Period naturalism | side_left \| side_right | standard_4_1 \| low_key_8_1 | 5600 | soft | none | window (5600) or candle (1900) as the ONLY source — pick per scene, scene-true |
| Epic golden | back_left \| back_right | mild_2_1 \| standard_4_1 | 3400 | soft | rim | low sun as backlight, sky as fill (band 3000–4000) |
| Domestic quiet | side_left \| side_right | standard_4_1 | 5600 | soft | none | Vermeer window, heavily diffused |
| Action / blockbuster | back_left \| back_right | standard_4_1 | 6000 | hard | rim | cool ambient (band 5600–6500) against warm practicals |

## 4. NUMERIC ANCHORS [v]

- Kelvin: candle 1800–2000 · household 2700–2800 · tungsten 3200 · fluorescent 3500–4300 (+green spike) · daylight 5600 · overcast ~6000–7500 (working default) · open shade 7000–8000 · blue sky 9000–20000 · sodium ≈2000–2200 (near-monochrome) · LED street ~3000–5000 (city/retrofit dependent)
- Ratio ↔ stops: 1:1=0 · 2:1=1 · 4:1=2 · 8:1=3 · 16:1=4 (each stop doubles)
- Pattern angles: loop 30–45° · rembrandt 45–60° · split 90° · butterfly on-axis ~45° down
- Golden hour: sun 0–6°; duration is latitude/season dependent — ~20–30 min near the equator, 60–90+ min at mid latitudes (Seoul ~37.5°N)

## 5. ALIASES & DO-NOT-CONFUSE

| Canonical | Aliases |
|---|---|
| ratio classes (flat_1_1…extreme_16_1) | "1:1/2:1/4:1/8:1/16:1", key-to-fill ratio |
| key_class (derived, QA-only) | high-key, low-key |
| exposure_bias | "high-key exposure"(colloquial), bright/dark exposure |
| rembrandt | 45-degree lighting (loose) |
| stabilizer note | — lighting has no support axis; that's camera |
| golden_hour / blue_hour | magic hour (BANNED — ambiguous between the two) |
| motivated single soft source | Deakins-style (style-name — use the description, not the name) |

**Do not confuse:** high/low-key (RATIO) vs exposure_bias (BRIGHTNESS) · pattern (facial shadow geometry) vs key_direction (physical position) — validate compatibility · negative fill (subtraction concept, QA) vs "deepened shadow" (the promptable result) · halation (prompt-side bloom) vs any ffmpeg op (none exists).

## 6. AI-GEN CAVEATS

- **Default bias = flat/safe frontal light.** Without explicit direction + quality + proxy, models render even, low-contrast light regardless of mood words.
- **Cross-shot drift is the #1 failure** [v — 2025 relighting research]: "warm window light" reinterpreted per generation. The byte-identical scene sentence is the countermeasure; treat any paraphrase as a defect.
- **Practicals render decorative** unless told they are THE source.
- **Silhouettes resist:** models restore facial detail for legibility — repeat the negation-free constraint ("subject in complete shadow, only the outline visible") and expect retries.
- **Rim lights bloom** into halos — "thin edge only."
- **Numeric-only specs are weak:** Kelvin + gloss; ratio + proxy; pattern + geometry.
- **Day-for-night fails at generation** — solve at framing (exclude sky) + grade in post.
- **Narrow-spectrum sources** (sodium/fluorescent) render as a tint, not desaturation/spike — usually acceptable; note it at QA.
