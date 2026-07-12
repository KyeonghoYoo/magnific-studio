# Lenses & Optics — 렌즈와 광학 (키프레임 = 사진)

Canonical lens, depth-of-field, filtration, and film-texture vocabulary. Keyframes are photographs — this file is decisive at T2I time.
**Read this when:** setting `visual_grammar.lens_bible` and `look` at /ms-plan; choosing `lens_mm`/`dof` at /ms-storyboard; composing keyframe prompts at /ms-produce.

**GLOBAL RULE: every focal length in this pipeline is FULL-FRAME EQUIVALENT** (`lens_mm` integer field). A bare mm number has no defined angle of view without a format (a 35mm lens on Super 35 frames like a 50mm on FF). The token "35mm" is three different things — ALWAYS disambiguate: **"35mm lens"** (focal length) / **"shot on 35mm film"** (gauge/texture) / **"full-frame (36×24mm)"** (sensor format).

## 1. CANONICAL TERMS

### Focal bands (FF-equivalent)

| Term | KR | Band | Use when | Effect | Prompt phrase | Caveat |
|---|---|---|---|---|---|---|
| ultra_wide | 초광각 | 14–24mm | unease, immersion, vastness, distortion-as-meaning | expands space; stretches edges; foreground dominance | "16mm ultra-wide lens, expansive distorted perspective" | mm tokens shift FOV reliably on sentence-encoder models [v] |
| wide | 광각 | 24–35mm | environmental context, geography, ensemble staging | context-rich frame | "24mm wide-angle, environmental context" | — |
| normal | 표준 | ≈40–58mm | neutral observation, no perspective editorializing | perceptually neutral proportions | "50mm lens, natural undistorted perspective" | two live conventions: PHOTOGRAPHIC normal = the format diagonal (FF ≈43mm; S35 ≈28mm); CINE/SMPE convention ≈2× diagonal (S35 ≈56mm) — contested; this pipeline sidesteps it by publishing everything FF-equivalent |
| short_tele | 중망원(인물) | 85–135mm | intimacy, isolation, flattering close-ups | mild compression; minimizes facial distortion | "85mm portrait lens, subject isolated from the background" | "85mm portrait lens" = one of the most reliable optical tokens across model families [v] |
| long_tele | 망원 | 200mm+ | voyeurism, surveillance, compression stacking | flattened depth planes; narrow FOV | "200mm telephoto compression, stacked flattened background layers" | — |
| fisheye | 어안 | <14mm, uncorrected | altered/subjective POV, disorientation | barrel distortion, curved horizon | "fisheye lens distortion, curved wide-angle POV" | — |

**Perspective truth (doctrine-level):** facial "distortion" is caused by CAMERA-TO-SUBJECT DISTANCE, not focal length itself — near distances exaggerate features at any focal length, far distances flatten (indicative heuristic: roughly <1m vs >3m — craft rule of thumb, not a verified constant; §4). The focal length chooses how much of the scene you keep at that distance. Prompt the pairing: "close-up with wide-angle distortion" vs "portrait compression from a distance."

### Depth of field & focus

| Term | KR | Use when | Effect | Prompt phrase | QA / Caveat |
|---|---|---|---|---|---|
| dof: shallow | 얕은 심도 | subjectivity, romance, beauty, attention-funneling | subject isolation, creamy blur | "shallow depth of field, f/1.8, subject sharp, background dissolving into bokeh" | THE most reliably steerable optical instruction — number + phrase together beat either alone [v] |
| dof: medium | 중간 심도 | neutral coverage | balanced legibility | "f/4, moderate depth of field" | — |
| dof: deep | 딥 포커스 | ensemble staging, environmental storytelling, simultaneous planes | democratic frame — fore/mid/background all sharp | "deep focus, sharp from foreground to background, f/11" | deep FOCUS (optics) ≠ deep SPACE (staging distance — directing-mise-en-scene.md); deep space + shallow focus is a common modern look |
| bokeh (shape) | 보케 | art-directing HOW the blur looks | creamy round / swirly vintage / oval anamorphic | "smooth creamy bokeh" / "swirly vintage bokeh" / "oval anamorphic bokeh" | shape is NOT inferred from a DoF instruction — name it explicitly [v] |
| aperture | 조리개 | precise-feeling DoF/exposure anchor | lower f/ = shallower + brighter | "f/1.8 aperture" | full stops: 1.0 1.4 2 2.8 4 5.6 8 11 16 22; numeric f-values steer blur even with no optics underneath [v] |
| rack focus | 랙 포커스 | attention transfer A→B without a cut ("edit within the frame") | guided eye | **two-keyframe technique**: FF "foreground sharp, background blurred" → LF "background sharp, foreground blurred" | a still cannot depict a rack — express only the start/end focus states |
| split diopter | 스플릿 디옵터 | stylized dual-plane sharpness with a visible seam | two sharp planes, De Palma register | "split diopter shot, foreground and background both sharp, subtle blur seam between" | stylized — use knowingly |
| hyperfocal | 과초점 | planning deep-focus frames | max sharp zone | "sharp from foreground to infinity" | — |
| lens breathing | 렌즈 브리딩 | flagging unwanted zoom-like shift during a focus pull | parasitic FOV change | "minimal focus breathing, breathing-free focus pull" (request its absence — note: PARFOCAL is a different property: holding focus through a ZOOM) | video-stage concern |

### Lens character & filtration

| Term | KR | Use when | Effect | Prompt phrase | Caveat |
|---|---|---|---|---|---|
| spherical | 구면(표준) 렌즈 | neutral modern baseline | clean, un-stylized | "spherical lens, clean round bokeh, no distortion" | default |
| anamorphic | 아나모픽 | scope/prestige register | oval bokeh, horizontal blue flare, 2.39:1, gentle edge distortion | "anamorphic lens, 2.39:1, oval bokeh, horizontal blue lens flare" | the cluster works as an ENSEMBLE; "anamorphic bokeh" is a top-yield token [v]; naming real glass (e.g. "Panavision C-Series") boosts fidelity on gear-aware encoders [v] |
| anamorphic flare | 아나모픽 플레어 | instant "cinema glass" signal | horizontal cyan streak | "horizontal blue anamorphic lens flare streaking across the frame" | [v] high-yield |
| vintage glass | 빈티지 렌즈 | nostalgia, imperfection-as-authenticity, period | low contrast, soft corners, warm flare | "vintage lens character, soft low-contrast rendering, warm flare, gentle corner softness" | — |
| diffusion | 디퓨전(프로미스트류) | de-digitizing a clinical image; dreamy high-key | highlight bloom, lowered micro-contrast | "soft diffusion filter look, gentle highlight bloom, dreamy filmic haze" — grade the strength with light/medium/heavy | **prompt the EFFECT, never the brand** — filter brand names are unrecognized [v] |
| polarizer | 편광 필터 | saturated skies, glare-free water/glass | deepened blue sky, cut reflections | "polarized deep blue sky, glare-free water reflections" | ND has no visual signature — exposure rationale only, never prompt it |
| halation | 헐레이션 | tungsten night, neon, practicals-heavy frames | warm halo blooming from bright points | "warm halation glow around lights" — more consistent when PAIRED with a named stock (cinestill_800t) [v] | prompt-side only; no ffmpeg halation |
| bloom | 블룸 | ethereal high-key, sun glare | soft highlight overflow into midtones | "soft bloom on highlights, glowing overexposed light sources" | — |
| chromatic aberration | 색수차 | cheap-lens/vintage/doc authenticity cue | purple-green edge fringing | "subtle purple-green chromatic aberration at the edges" | sparingly |

### Film stocks & texture (`look.film_stock` enum — the best-evidenced token class [v])

| Enum value | KR | Signature | Use when | Prompt phrase |
|---|---|---|---|---|
| kodak_portra_400 | 코닥 포트라 400 | warm-neutral skin, gentle contrast, fine grain | flattering daylight portraiture, editorial warmth | "Kodak Portra 400 look, soft warm skin tones, gentle contrast, fine grain" |
| kodak_vision3_500t | 코닥 비전3 500T | CLEAN tungsten night (halation suppressed) | naturalistic night interiors without the glow artifact | "Kodak Vision3 500T tungsten stock, clean night-interior color, minimal halation" |
| cinestill_800t | 씨네스틸 800T | red halation halos around lights | neon-lit urban night, glowing practicals | "CineStill 800T look, neon halation glow around lights, tungsten-balanced shadows" |
| kodak_trix / ilford_hp5 | 트라이엑스/HP5 | punchy grainy B&W | photojournalism, war/street, timelessness | "Tri-X black and white, high contrast, grainy photojournalistic look" |
| super8 | 슈퍼8 | heavy warm grain, light leaks, gate weave | memory, home-movie framing, dream | "Super 8 home movie texture, heavy grain, warm faded color, light leaks" |
| arri_alexa | 알렉사(디지털) | smooth non-clipping highlight rolloff | prestige digital cinema register | "shot on ARRI Alexa, smooth highlight rolloff, filmic digital color science" |
| (grain fields) | 그레인 | gauge-only: fine_35mm / coarse_16mm / heavy_8mm (the super8 STOCK look — color+leaks+weave — is owned by film_stock; grain carries texture only) | baseline "shot on film" texture | "35mm film grain, organic texture" / "16mm grain, gritty documentary texture" / "heavy 8mm grain" |

**Stock trap:** CineStill 800T IS Vision3 500T with the anti-halation backing removed — same emulsion, OPPOSITE halation behavior. "Authentic tungsten stock" and "the CineStill glow" are different asks [v].

### Exposure (brightness intent — NOT lighting ratio)

| Term | KR | Use when | Prompt phrase | Note |
|---|---|---|---|---|
| exposure_bias: bright | 밝은 노출 | comedy, beauty, idealized worlds | "bright airy exposure, minimal shadow density" | **renamed from the source's "high-key exposure"** — high/low-key are LIGHTING RATIO classes owned by lighting.md (N1); this field is brightness only |
| exposure_bias: neutral | 중립 노출 | default | — | — |
| exposure_bias: dark | 어두운 노출 | somber, dread, night interiority | "dark, underexposed mood, deep tonality" | pair with the lighting ratio proxy, not with "low-key" |
| silhouette exposure | 실루엣 노출 | anonymity, iconicity, backlit romance | "silhouette against a bright backlit sky, subject in complete shadow" | expose-for-background concept |
| blown-highlight style | 하이라이트 날림 | glowy overexposed mood | "bright blown-out highlights, glowing overexposed style" | deliberate style, not an error |
| zone placement | 존 시스템 | precise tonal placement language | "skin tones at Zone VI, shadow detail held at Zone III" | Adams/Archer: 11 zones (0–X), 1 stop apart, Zone V = 18% gray [v] |

## 2. DOCTRINE

1. **Distance is the real variable; focal length is what you keep.** Choose camera-to-subject distance for the psychology (near = confrontation/distortion, far = observation/compression), then the band that frames it.
2. **Number + phrase, together.** "f/1.8" alone or "shallow depth of field" alone underperforms the pair [v]. The projection always emits both.
3. **Concrete technical nouns beat adjectives.** A named stock or body bundles color+contrast+grain into one reliable token; "filmic" bundles nothing. This is the endorsed token class (prompting.md blocklist governs the banned one).
4. **One look, stated once.** `visual_grammar.look` (stock/lens_character/grain/diffusion) is project-level and injected verbatim — per-shot look drift is a defect, not variety.
5. **ots/dirty framings always state shallow** (auto-emitted — foreground shoulders render sharp by default).
6. **T-stops are set jargon, not prompt language** — no model distinguishes T from f [v]; use f-stops.
7. **Grain is an approximation.** Prompted "film grain" renders as a uniformish noise overlay, not density-correlated silver halide [v] — acceptable as mood; final texture uniformity is post's job (grain/dither also masks banding — color-grading.md).

## 3. DECISION TABLES

**Story intent → focal / distance / DoF**

| Intent | lens_mm | Distance | dof |
|---|---|---|---|
| Intimacy / vulnerability | 85–135 | close | shallow (f/1.4–2.8) |
| Unease / disorientation | 14–24 | very close | deep, or shallow with edge distortion |
| Environmental context / scale | 24–35 | mid | medium-deep (f/5.6–8) |
| Neutral realism | 40–58 | natural | medium (f/4–5.6) |
| Voyeurism / surveillance | 200+ | far | shallow (compression-driven) |
| Ensemble / simultaneous planes | 24–35 | mid-wide | deep (f/11+) |
| Power / dominance | <35 | very close foreground | foreground-driven |

**Mood → stock/look**

| Mood | look |
|---|---|
| Warm nostalgic daylight | kodak_portra_400 |
| Neon urban night | cinestill_800t |
| Clean tungsten night interior | kodak_vision3_500t |
| Gritty documentary/war | kodak_trix / ilford_hp5 (pushed) |
| Memory / childhood | super8 |
| Prestige digital | arri_alexa |
| Scope blockbuster | anamorphic + 2.39:1 + oval bokeh |

**Function → character + diffusion**

| Function | lens_character | diffusion |
|---|---|---|
| "Real cinema" signal | anamorphic (+flare) | none |
| Period / imperfect authenticity | vintage | none or light |
| Clean modern baseline | spherical | none |
| Soften digital sharpness | spherical | light–medium |
| Dreamy / ethereal | spherical soft | medium–heavy |

## 4. NUMERIC ANCHORS [v]

- Focal bands (FF-equiv): ultra_wide 14–24 · wide 24–35 · normal 40–58 (diagonal ≈43) · short_tele 85–135 · long_tele 200+
- f-stop full stops: 1.0 · 1.4 · 2 · 2.8 · 4 · 5.6 · 8 · 11 · 16 · 22 (T-value ≥ f-number; prompt f only)
- Anamorphic squeezes 1.33×/1.5×/1.8×/2× — desqueezed aspect = SENSOR aspect × squeeze (classic 2.39:1 = 2× on 6:5 open-gate natively — 2× on 4:3 gives 2.67:1, side-cropped to 2.39 in post; or 1.33× on 16:9 ≈ 2.37; 2× on 16:9 → 3.56:1); aspect canon: 1.85:1 flat · 2.39:1 scope (2.35:1 = pre-1970 colloquial) · 2.20:1 70mm · 1.43:1 IMAX
- Perspective distortion: near distances exaggerate features, far distances flatten (any focal length) — indicative heuristic: roughly <1m vs >3m (craft rule of thumb, not a verified constant)
- Zone system: 11 zones (0–X), 1 stop apart, Zone V = 18% gray
- Stocks: Portra 400/800 · Vision3 EI 500T · CineStill rated 800T (often shot EI 320–500) · Tri-X/HP5 400 (push 800/1600)

## 5. ALIASES & DO-NOT-CONFUSE

| Canonical | Aliases |
|---|---|
| lens_mm (FF-equiv) | focal length, "Xmm" (always emitted as "Xmm lens") |
| dof shallow/deep | wide open / stopped down |
| exposure_bias | "high-key/low-key exposure" (colloquial — RENAMED; ratio classes live in lighting.md) |
| diffusion light/medium/heavy | Black Pro-Mist 1/8–1/4 / 1/2 / 1–2 (brand grades — prompt the effect) |
| anamorphic flare | horizontal blue streak flare |
| film gauge texture | "35mm/16mm/8mm film" (gauge ≠ focal length ≠ format) |

**Do not confuse:** "35mm" three ways (lens/film/format — always qualify) · deep focus (optics) vs deep space (staging) · grain (photochemical, density-correlated) vs noise (uniform overlay — what AI actually renders) · CineStill glow vs Vision3 clean · T-stop (set) vs f-stop (prompt) · bokeh AMOUNT (dof) vs bokeh SHAPE (named separately).

## 6. AI-GEN CAVEATS

- **Shallow DoF + numeric f-stop = the most universally reliable optical instruction** [v]; "85mm portrait lens" comparably strong [v].
- **Named stocks/bodies are high-leverage tokens** — each bundles color science + contrast + grain [v]; gear-aware text encoders reward real product nouns [v].
- **Bokeh shape must be named** — never inferred [v].
- **Filter/diffusion brand names unrecognized** — prompt observable effects [v].
- **Numeric triads (ISO+shutter+f) without descriptive language** are inconsistent on tag-encoder models; sentence-encoder models tolerate them inside full sentences [v].
- **Prompted grain ≈ uniform noise** — approximation, not physical texture [v]; final grain pass in post.
- **Rack focus / breathing are video-stage behaviors** — stills carry only endpoint focus states; unwanted focus drift in I2V gets flagged at clip QA (often caused by mismatched FF/LF dof — production FLF rule).
