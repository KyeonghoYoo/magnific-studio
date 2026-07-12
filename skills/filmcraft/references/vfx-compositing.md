# VFX & Compositing

Read this when: hybrid shots (stock plate + generated element) at /ms-produce; screen replacement; judging composite believability at QA.

Binding source: `docs/filmcraft-rulings.md` (shipped arbitration snapshot). Authorities: VES Handbook (Okun & Zwerman) · ASC Manual · this pipeline's practice.

## Canonical Terms

Columns: Term | KR | Use when | Effect | Prompt phrase/instruction | QA | Caveat.

### Plates & Isolation

| Term | KR | Use when | Effect | Prompt phrase/instruction | QA | Caveat |
|---|---|---|---|---|---|---|
| Plate | 플레이트(배경판) | Any hybrid shot — the photographed/stock background layer a generated element sits on | Anchors the composite in photographic reality | "match plate lighting direction, lens focal length, and color temperature before compositing foreground" | Composite's light direction/lens/color-temp cross-checked against plate | Gen-AI foregrounds default to the model's own implied lighting/lens — must be graded to match |
| Clean Plate | 클린 플레이트 | Wire/rig/marker removal, crowd thinning | Lets paint-out reconstruct occluded background without guessing | "paint-out reference: clean plate frame, reconstruct occluded background" | Paint-out seam invisible at 100% crop; no ghosting of removed subject | n/a — capture-time asset; gen-AI can't retroactively supply one (shoot it or matte-paint the gap) |
| Element | 엘리먼트 | Any individually captured/generated visual layer (smoke, fire, debris, creature) going into comp | Enables per-layer grading/timing control | "isolated [smoke/debris/fire] element on black, clean alpha edge, for compositing" | Alpha edge clean, no fringing; layer gradable independent of plate | Gen models output flat RGB, no native alpha — prompt a clean/rotoscopable backdrop, extract matte in post |
| Matte (Garbage / Holdout / Alpha) | 매트 | Defining which pixels are visible, excluded, or blocking another layer | Bad mattes are the #1 composite tell (crawling edges, wrong occlusion) | "clean alpha channel, no premultiplied fringing, holdout for foreground occlusion" | Inspect edges at hair/motion-blur frames for crawl or fringe | Gen-AI never emits an alpha channel — isolating a generated element is always a post-generation roto/key extraction, never assume one exists |
| Chroma Key (Green / Blue Screen) | 크로마키 | Isolating a subject via a uniformly-lit backing color | Green default; blue when the subject carries green/yellow content | "clean chroma key isolation, evenly lit backing, no spill on edges" | Spill-free edges; even backing (no hot spots) | Gen-video models don't key — hybrid isolation happens in traditional comp post-generation, on a prompted clean backdrop |
| Spill Suppression | 스필 서프레션 | After any key pull, before final comp | Removes the classic green/blue edge glow | "despill edges, neutralize green/blue color cast on hair and skin" | 100% crop on hair/skin edge — no residual color cast | n/a — standard comp step, identical for gen or camera-original elements |
| Rotoscoping (Roto) | 로토스코핑 | No clean key is possible — hand- or AI-assisted frame-by-frame mattes | Only path to isolate elements with no backing color | (post-only step; no generation prompt) | Human review required on every fine-hair / motion-blur frame | AI-assisted roto still needs human QA — it fails silently on hair and blur, not just obviously |
| Cleanup / Paint-Out | 클린업/페인트아웃 | Removing production artifacts (wires, rigs, markers) from a plate | Restores a clean background for compositing | "remove wire rig / marker, reconstruct background using clean-plate reference" | Reconstructed area shows no visible warp/smear vs neighboring frames | n/a — standard comp step; needs a clean-plate or paint reference regardless of what layer is generated |

### Integration Rules (the believability checklist)

| Term | KR | Use when | Effect | Prompt phrase/instruction | QA | Caveat |
|---|---|---|---|---|---|---|
| Light Direction & Color Match | 광원 방향·색온도 매칭 | Every hybrid composite, before any other integration pass | Mismatch is the fastest "fake" read | "match key light direction and color temperature to background plate" | `color_consistency` axis (signalstats): compare plate vs element mean RGB/luma; flag drift | THE most common, most damaging AI-gen compositing failure — gen defaults to its own implied light, not the plate's |
| Shadow Contact & Ambient Occlusion | 접지 그림자·AO | Any element touching a surface (feet, object base) | Absence reads "floating cutout"; presence alone can sell an imperfect comp | "add contact shadow at ground-touch point, soft ambient occlusion in surface creases" | Manual: contact shadow + AO present at every touch point — absence is an automatic fail | Gen hybrid foregrounds essentially never generate a correct contact shadow against a separate plate — always add in comp |
| Perspective & Lens Match | 원근·렌즈 매칭 | Placing any element into an existing plate | Wrong perspective reads "pasted flat" even with perfect color | "match plate focal length and horizon line, correct camera height for element placement" | Manual: horizon-line + vanishing-point overlay-grid check vs plate | Gen elements carry the prompt's implied lens, not the plate's actual camera — must be matched manually |
| Scale Cue | 스케일 단서 | Any element whose real-world size isn't self-evident | Tells the eye how large/far an element is | "include human-scale reference in frame, atmospheric haze falloff consistent with stated distance" | Manual: human-scale reference present; haze/DoF falloff consistent with stated distance | Gen models have no metric sense of the plate's real-world scale — must be prompted explicitly |
| Grain / Noise Match | 그레인·노이즈 매칭 | Any clean-rendered element over a photographed plate | Mismatched grain is a top-3 subconscious "fake" tell | "match plate grain/sensor noise size and density on composited element" | `color_consistency` axis (signalstats) noise-floor compare, or manual grain-size eyeball match; target = `visual_grammar.look.grain` enum | Gen output is cleaner or different-charactered than plates — needs a matching grain pass in post |
| Edge Treatment & Light Wrap | 엣지 처리·라이트 랩 | Every composited silhouette edge | Hard, un-wrapped edge is a fast cutout tell | "soft edge, light wrap from background color/brightness onto foreground silhouette edge" | Manual: 100% crop edge inspection — hard/un-wrapped edge = fail | Gen composites default to a hard, hand-cut-feeling edge unless explicitly softened and wrapped |
| Atmospheric Depth (Haze Desaturation) | 대기원근 | Any element with distance from camera to sell | Desaturation + contrast reduction + cool shift with distance | "desaturate and cool-shift background with distance, reduce contrast for atmospheric haze" | `color_consistency` axis (signalstats): desaturation/contrast gradient vs stated distance | Easy to skip when the gen element already reads "flat" — no dedicated ai_caveat beyond general grade discipline |
| Motion Blur Match | 모션 블러 매칭 | Any moving element composited into a plate with camera-original motion | Absent blur = strobing against a blurred plate | "directional motion blur matching plate shutter angle and element velocity" | Manual frame-step: blur streak length/direction vs plate's shutter reading (formula in `animation-motion.md` Numeric Anchors) | Gen-video blur is inconsistent frame-to-frame or absent entirely |
| Reflection / Interaction Pass | 반사·인터랙션 패스 | Any element contacting a reflective/wet/soft surface | High-leverage believability; absence reads as not truly "in" the scene | "add ground reflection / ripple / disturbance where element contacts surface" | Manual: reflection/ripple/disturbance present at every surface-contact frame | Gen elements essentially never generate correct contact interaction on a separate plate — add in comp |

### Set Extension & Screens

| Term | KR | Use when | Effect | Prompt phrase/instruction | QA | Caveat |
|---|---|---|---|---|---|---|
| Hybrid Shot | 하이브리드 숏 | Real/stock plate for one layer + generated element for another — this file's core subject | Budget targets only the layer that actually needs generation | "composite generated foreground onto stock plate background, matched light/shadow/grain/perspective" | Full Integration Rules checklist (9 rows above) applied at the seam | Most exposed shot type to every integration failure at once — the seam is the highest-risk QA point in the whole pipeline |
| Set Extension | 세트 익스텐션 | Digitally extending a physical set beyond its built limits | A small build reads as a massive location | "extend set beyond frame edge, match practical lighting and lens perspective at the seam" | Perspective/parallax holds through any camera movement; lighting continuous across the join | Lighting/parallax mismatch at the join breaks the illusion immediately |
| Digital Matte Painting (DMP) | 디지털 매트 페인팅 | Environments too costly or impossible to build/shoot | Delivers backgrounds no set could provide | "digital matte painting background, parallax-correct for camera move, matching plate light direction" | Parallax-correct under camera move; light direction matches plate | Breaks when perspective/parallax fails under camera movement — static-camera shots are far safer |
| Screen Replacement / Burn-In | 스크린 리플레이스먼트/번인 | Any in-shot screen content (phone, monitor, kiosk, HUD) | Matched perspective/reflections/brightness sells the device as live | "corner-pin screen content to tracked device surface, add glass reflection and brightness bloom matching scene light" | Manual: tracked corner-pin holds through the entire move — no swim, no gate-drift; bloom/reflection present whenever the screen is visible | Keyframe-generated screen content fails perspective the instant camera/device moves — ALWAYS treat as source art only, finish with a tracked corner-pin |

### Visualization

| Term | KR | Use when | Effect | Prompt phrase/instruction | QA | Caveat |
|---|---|---|---|---|---|---|
| Previz | 프리비즈 | Validating staging/creative intent before any spend | Catches creative/staging problems at near-zero cost | "rough previz pass: staging and blocking only, no final light/detail" | Creative-only — no pass/fail; gate is "does the sequence work?" | n/a |
| Techviz | 테크비즈 | Translating previz into physically real camera/rig specs for an actual shoot | Validates what's physically shootable — rig clearance, lens throw, stunt safety | (not promptable — physical pre-production, not a generation step) | n/a — cannot be QA'd by this pipeline at all | AI keyframe/clip gen CANNOT substitute — it validates nothing physical. Never claim techviz coverage from a generated preview |
| Postviz | 포스트비즈 | Cutting the edit against unfinished/placeholder VFX before final comp lands | Lets editorial pace-test a cut before expensive finishing | "rough comp placeholder: approximate final element for timing only" | Cut timed against placeholder; MUST be replaced before delivery — never ship postviz-grade comp | AI gen is a fast, usable postviz substitute — but flag every postviz shot so it isn't accidentally delivered |
| Animatic | 애니메틱 | Storyboard/previz frames cut to timing + temp audio, before production | Catches pacing/staging problems cheaply | "storyboard frames in sequence, temp timing and audio, no final imagery" | Pacing approved before any generation spend — cheapest gate in the pipeline | n/a |

### Atmosphere & Particles

| Term | KR | Use when | Effect | Prompt phrase/instruction | QA | Caveat |
|---|---|---|---|---|---|---|
| Volumetrics & God Rays | 볼류메트릭·갓레이 | Visible light scattering through a medium; beams through gaps | Cheap, strong depth/mood cue | "volumetric god rays through [gap/canopy/window], visible dust in the light shaft" | Dust/haze density consistent shot-to-shot within a scene | Overuse reads as generic "cinematic" cliché — pair with a concrete technical noun, don't rely on the mood word alone |
| Atmosphere Particulate (Dust / Embers / Rain Interaction) | 대기 파티클 | Foreground particle layer — dust motes, embers, rain | Sells atmosphere/weather as physically present | "drifting dust motes in light shaft" / "rain with splash and ripple interaction on wet surfaces" | Rain/dust MUST show surface interaction (splash/ripple/settle) — zero-interaction rain is an automatic synthetic-tell fail | Gen rain commonly falls with zero surface response — flag for a post interaction pass whenever the gen doesn't supply one |

## Doctrine

- **Invisible VFX (인비저블 VFX) is the standard.** The best VFX are never consciously noticed. QA question for every hybrid shot: "does this call attention to itself?" — if yes, it fails regardless of technical polish.
- **The hybrid seam is the highest-risk QA point in the entire pipeline.** A hybrid shot is exposed to every integration failure at once (light, shadow, perspective, grain, edge, blur, reflection). Budget a full integration pass as a certainty, not a contingency — never as an afterthought if time runs short.
- **The 9 Integration Rules ARE the quality-reviewer checklist for hybrid shots.** No single dedicated composite-quality axis exists yet — until one does, walk all 9 rows of the Integration Rules table per hybrid-tagged shot; each row's QA column above is the concrete pass/fail check.
- **Generated screen content is source art only.** Never trust a gen model to hold perspective through a camera or device move. Every screen-replacement shot finishes with a tracked corner-pin in post — no exceptions, regardless of how convincing the gen keyframe looks static.
- **Rain (and atmosphere particulate generally) needs surface interaction or it reads synthetic.** Splash, ripple, or settle on contact is not optional polish — zero-interaction rain/dust is one of the most recognizable synthetic tells and is flagged automatically at QA.

## Decision Tables

### A — Integration Problem → Technique

| Symptom | Fix |
|---|---|
| Foreground reads pasted-on / floating | Contact shadow + light wrap |
| Color/WB mismatch vs plate | Light-direction & color-match grade |
| Screen/UI flat or swims on move | Corner-pin warp + gamma/bloom burn-in |
| Green/blue fringing | Spill suppression + edge despill (not a harder key) |
| Distant background too sharp/saturated | Atmospheric-depth falloff |
| No reflection/ripple on wet surface | Reflection/interaction pass |
| Motion blur mismatch | Match shutter directionally + vector blur |
| Visible set-extension seam | Lens-distortion + grain match across the seam |
| Rig/wire visible | Clean-plate paint-out |
| CG/gen element "too clean" | Grain/noise match |
| Ambiguous creature/object scale | Scale-cue reference + atmospheric falloff |

### B — Visualization Stage → Question

| Question | Stage | AI substitute? |
|---|---|---|
| Does the sequence work creatively? | Previz | Yes |
| Can we physically shoot this? | Techviz | NEVER |
| Does the cut pace against unfinished VFX? | Postviz | Yes |

## Numeric Anchors

- Chroma key backing: physical green ≈ #00B140 [v]; digital green #00FF00 [v]; blue ≈ RGB(8,39,245), hue 225–240° [v].
- Shutter/motion-blur reference for matching plate blur: 180° shutter → 1/(2×fps); 24fps → 1/48s [v]. Full formula + narrow-shutter numbers live in `animation-motion.md`.
- Frame rates in use: 24/25/29.97/30/48/60 fps.
- All authored durations elsewhere in this lexicon are milliseconds (ruling A5) — not applicable to the figures above, which are optical/photographic constants, not authored timing fields.

## Aliases & Do-Not-Confuse

- **VFX vs SFX (guild-correct distinction).** **Practical Effect (프랙티컬 이펙트)** — an effect achieved physically in-camera (pyro, animatronics, prosthetics) — is SFX's domain, not VFX's. VFX = post-digital (comp, CG, roto — everything else in this file). Trade press blurs the two; guild contracts don't. Practical+digital hybrid ("practical explosion/debris plate enhanced with digital fire/smoke element, not fully CG") usually beats either alone — which is exactly why it shows up here: the SFX plate is frequently the plate half of a Hybrid Shot.
- **"VFX" umbrella creep.** The word now colloquially swallows SFX, CGI, AND generative AI. This pipeline's gen-AI output gets folded into "VFX" in casual conversation despite being neither guild — stay precise in production docs even if casual speech is loose.
- **Previz / Techviz / Postviz spelling & scope.** Spelling varies by studio (previs/previz); scope varies too. This lexicon's boundary is fixed: previz = creative-only, techviz = physical-only (never AI), postviz = editorial-placeholder-only.
- **Greeking (그리킹, brand/plot-critical text).** Canonical term and full rule live in `prompting.md` — any legible brand mark/label/text is a locked-asset composite, never generated. Relevant here because screen-replacement content is the most common place this collides with hybrid compositing.
- **`camera_settle` (NOT this file).** The end-of-move composed-frame hold is a camera-movement term — see `camera-movement.md`. Do not confuse with any "settle" language used for impact physics — that's `impact_settle`, owned by `animation-motion.md`.

## AI-Gen Caveats

- **No native alpha/matte.** Gen-video output is flat RGB — there is no key, no alpha channel, ever. Isolating a generated element requires either a prompted clean/rotoscopable backdrop (solid color, black) or full roto in traditional post. Plan the isolation pass before generating, not after.
- **Composite integration blindness.** Generated foregrounds never arrive with correct contact shadow, light wrap, or grain vs a separate plate. Budget a full integration pass as a certainty on every hybrid shot.
- **Screen-replacement perspective failure.** Generated screen content holds perspective only in the keyframe it was generated at — any camera or device move breaks it. Treat generated screen content as source art only; finish with a tracked corner-pin.
- **Grain/clean mismatch.** Gen output is characteristically cleaner (or differently-textured) than photographed plates. A grain/noise-match pass in post is close to mandatory on any hybrid shot, not an optional polish step.
- **Rain/particulate with no surface response.** Gen rain/dust commonly falls with zero splash, ripple, or disturbance on contact — one of the most recognizable synthetic tells. Flag for a post interaction pass whenever the gen doesn't supply one natively.
