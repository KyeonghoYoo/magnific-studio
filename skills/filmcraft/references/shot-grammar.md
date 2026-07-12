# Shot Grammar — 숏 문법 (사이즈·앵글·프레이밍·구도)

Canonical vocabulary for shot sizes, angles, framing, composition, and screen space.
**Read this when:** designing shots at /ms-storyboard; composing keyframe prompts at /ms-produce; checking spatial continuity at QA.

## 1. CANONICAL TERMS

### Shot size ladder (8 rungs — defined by CUT LINE, never by vibe)

| Term | KR | Abbrev | Cut line / definition | Use when | Effect | Prompt phrase |
|---|---|---|---|---|---|---|
| extreme_wide | 익스트림 와이드 | ELS/EWS | subject ≤10–15% of frame height [v] | establish place/scale/isolation; awe beats | geographic orientation; individual insignificance | "extreme wide shot, tiny figure dwarfed by [environment]" |
| wide | 와이드 | LS/WS | full body + substantial environment | blocking/geography; full-body action; group entrances | neutral-observational — subject AND context | "wide shot, full body, [subject] in [location]" |
| full | 풀 숏 | FS | full body, frame edges near head/feet | body language/costume/action with minimal environment | physical performance over setting | "full shot, head to toe, tight framing around full body" |
| medium_full | 미디엄 풀 | MLS | **cut MID-THIGH, above the knee** | hero intros, action-ready stances, face+hands legible together | readiness/capability | "framed from mid-thigh up, hands and face both visible" |
| medium | 미디엄 | MS | cut at waist | default dialogue/coverage; balances body language and face | conversational workhorse | "medium shot, waist up" |
| medium_close_up | 미디엄 클로즈업 | MCU | cut at chest | emphasize expression while retaining gesture | intimate without losing the body | "medium close-up, chest up, expressive framing" |
| close_up | 클로즈업 | CU | cut at shoulders/collarbone | emotional beats, reactions, full attention on the face | intimacy; isolates face from surroundings | "close-up, head and shoulders, face-focused" |
| extreme_close_up | 익스트림 클로즈업 | ECU | detail within the face or an object | peak tension; critical-object reveals; sensory emphasis | maximal intimacy or tension | "extreme close-up on [eyes/hands/object], filling the frame" |

- **Never cut a body exactly at a joint** (hip/knee/ankle/wrist) — the reason medium_full is defined at MID-THIGH, not the knee.
- Within one scene, adjacent shots should not jump more than 3 rungs (flag, not block) — prefer neighbor steps as guidance; a motivated wide(2)→medium(5) cut is ordinary language, not a violation.
- "Italian shot" (eyes-only ECU) = alias, not a value.

### Angles (GEOMETRIC definitions — pitch; roll lives in `dutch_deg`)

| Term | KR | Geometry | Use when | Effect | Prompt phrase | Caveat |
|---|---|---|---|---|---|---|
| eye_level | 아이레벨 | lens at subject eye height (working default ≈ shoulder height) | neutral, non-editorializing coverage | relatable, objective | "eye-level shot, neutral angle" | — |
| low | 로우 앵글 | lens below subject, pitched up | empower, heroize, threaten | subject reads larger, dominant | "low angle shot, camera looking up at [subject]" | — |
| high | 하이 앵글 | lens above subject, pitched down | diminish, isolate, make vulnerable | subject reads smaller, at the situation's mercy | "high angle shot, camera looking down at [subject]" | — |
| overhead | 오버헤드 (수직 부감) | lens axis ⟂ ground, 90° STRAIGHT DOWN, close/human scale (table, bed, floor) | graphic/abstract composition, flat-lay, choreography geometry | intimate, analytical, occasionally god-like | "top-down overhead shot, 90 degrees, camera directly above, close distance" | models conflate with bird_eye — disambiguate with "directly above, close" |
| underneath | 언더니스 (수직 앙각) | 90° STRAIGHT UP — geometric inverse of overhead (glass floor, canopy, sky). Discriminator vs worm_eye: the overhead subject/surface FILLS the frame, no horizon, no foreshortened standing subject | trapped-below POV, canopy/skylight reveals, falling-away framing | vertiginous, rarely-seen vantage | "camera looking straight up, the [canopy/skylight/face above] filling the frame" | rare in training data — expect retries; if QA cannot discriminate it from worm_eye in output, author worm_eye instead |
| bird_eye | 버드아이 (조감) | high-ALTITUDE aerial vantage, pitched steeply down (NOT necessarily 90°) | scale of a crowd/city/landscape; journey geography | subject small in a legible, mapped world | "bird's-eye view, high-altitude aerial perspective" | distinct from overhead by ALTITUDE, not intent |
| worm_eye | 웜즈아이 (극단 앙각) | ground-level lens pitched steeply up; strong 3-point foreshortening | maximize looming power of subject/structure; disorientation | subject towers; viewer feels small | "worm's-eye view from ground level looking up, dramatic foreshortening, wide-angle perspective" | underrepresented in training — projection adds foreshortening + wide-lens cue or models regress to mild low angle |

**`dutch_deg` (더치/캔티드 — a ROLL field, 0–45, separate from angle).** A canted horizon is a roll, not a pitch — keeping it separate means a *low-angle canted shot* is expressible (The Third Man). Bands: 5–15° subtle unease · 15–45° overt disorientation [v]. Research also documents an extreme 45–90° band — the schema DELIBERATELY caps `dutch_deg` at 45: beyond it, generated geometry degrades and identity references distort; treat 45 as the design ceiling, not a data gap. Prompt: "camera canted 20 degrees, tilted horizon line" — pair the degree with the mechanism; bare "dutch angle" is a weak token. A canted HELD frame (dutch_deg) is far more reliable than a rolling MOVE (camera-movement.md `roll`).

### Framing (who is in frame + vantage) — SPLIT from function (editorial role)

| framing | KR | Definition | Prompt phrase | QA |
|---|---|---|---|---|
| single | 싱글 | one subject in frame | "single shot of [subject]" | count=1 |
| two_shot | 투샷 | exactly TWO subjects — **defined by COUNT only**, at any size | "two-shot, [A] and [B] framed together, both faces visible" | count=2 |
| group | 그룹 숏 | three or more subjects | "group shot, [N] people, [dominant] nearest camera" | count≥3 |
| empty_frame | 빈 프레임 | no subjects — environment/object only | "empty deserted [location], still and unoccupied" | count=0 (positive reframe — "deserted/empty", never "no people") |
| ots | 오버 더 숄더 | camera behind one character's shoulder (soft), framing the other | "over-the-shoulder shot, foreground shoulder softly out of focus, [B] facing camera beyond" | ≥2 chars; foreground shoulder soft |
| pov | 시점 숏 | camera occupies a character's optical position (strict definition) | "first-person view through [character]'s eyes: [what they see], empty foreground, clear line of sight" | `pov_of` set; that character NOT in frame; foreground empty (positive reframe — never name the unwanted camera/hands) |

- `dirty: true` (더티) on single/ots = a sliver of the scene partner remains in frame — keeps the relationship present; clean isolates. Keep the choice (and the shoulder side) consistent within a scene.
- **ots/dirty ⟹ shallow DoF is auto-emitted** — foreground shoulders render distractingly sharp by default.

| function (editorial role — cannot be read off the frame) | KR | Definition | Pipeline note |
|---|---|---|---|
| establishing | 설정 숏 | opens a location/geography | models are WEAKEST at wide many-element geography → default `generation_strategy: stock` candidate; for shorts, format rules may delete it entirely (hook first) |
| master | 마스터 숏 | covers the whole scene with all principals; the geometry/wardrobe/lighting REFERENCE for every tighter shot | lock it first; it becomes the scene's reference frame |
| insert | 인서트 | close detail ALREADY covered in the master, re-emphasized | characterless → stock candidate; the highest-value seam-hider in the edit |
| cutaway | 컷어웨이 | material NOT covered in the master; returns to the main line | characterless → stock candidate; bridges jump cuts, hides glitches |
| reaction | 리액션 숏 | a character's response to the main action — where emotional meaning LANDS | pair with gaze_target; body carries the emotion (directing-mise-en-scene.md) |
| transition | 전환 숏 | exists to bridge scenes (arrival cut, match-cut target) | plan with the edit, not after it |

### Composition tags (`composition_tags`, array ≤3, optional)

| Tag | KR | Use when | Effect | Prompt phrase | Caveat |
|---|---|---|---|---|---|
| rule_of_thirds | 삼분할 | default off-center placement; dynamic/natural | more tension/energy than centering | "subject positioned on the left third, eyes on the upper third line" | models gravitate back to center — emit EXPLICIT placement, not the bare tag |
| centered_symmetry | 중앙 대칭 | order, control, artificiality, fate — or storybook whimsy | stable/powerful OR sterile/uncanny | "centered symmetrical composition, one-point perspective" | the model's gravitational default — easiest tag to land |
| leading_lines | 유도선 | guide the eye through a deep/busy frame | eye travels the path, lands on subject | "leading lines converging toward [subject]" | — |
| frame_in_frame | 프레임 속 프레임 | voyeurism, confinement, isolation within a busy space | observer feeling; entrapment or protection | "[subject] framed through [doorway/window], foreground framing the shot" | — |
| negative_space | 네거티브 스페이스 | isolation, vulnerability — or calm power | small subject in emptiness = lost; dominant subject in emptiness = invincible | "[subject] small within a large empty [environment], clearly separated by contrast" | — |
| depth_staged | 심도 스테이징 | foreground/midground/background layering for dimensionality | strong 3D sense; parallax fuel for moves | "foreground [element], midground [subject], background [environment], layered depth" | cap at 2 legible action planes |
| foreground_occlusion | 전경 가림 | partial foreground element concealing part of the subject | depth + mystery; voyeuristic vantage | "[foreground element] partially occluding [subject]" | on I2V, a persisting occluder is a flicker/morph risk — keep it static or describe its motion |

- `rule_of_thirds` ⊕ `centered_symmetry` are mutually exclusive.
- **golden_ratio is NOT a tag** — see Aliases (perceptual claims unsupported; stylistic descriptor only).
- Headroom (머리 위 여백) and lead room / looking room (진행·시선 방향 여백) are PROMPT LANGUAGE, not fields: "balanced headroom, eyes on the upper third" / "[subject] on the left third, facing right, negative space ahead of their gaze." Headroom scales inversely with shot tightness. Looking room (gaze) and lead room (motion) diverge when a subject walks one way while looking back — say which one you mean.

### Space & direction (the machine-checkable 180° system)

| Field | KR | Definition | Rule |
|---|---|---|---|
| scene.axis | 씬 축 | the 180° line, fixed by the scene's geography/master shot: `{established_by_shot_id, a, b, a_side}` | every shot containing A and B keeps A on `a_side` unless a legal crossing is logged |
| screen_direction | 스크린 방향 | subject's travel/facing in screen terms: left / right / toward_camera / away_from_camera / neutral | REQUIRED whenever a subject moves or looks; consistent across a travel sequence until a motivated, on-screen reversal |
| gaze_target | 시선 타깃 | to_camera / off_left / off_right / off_up / off_down / at:<character> / none | replaces any degree-based eyeline spec (rejected as unsourced); mutual gaze (A at:B, B at:A) ⟹ opposite screen directions |

Legal axis crossings (the four, from directing-mise-en-scene.md): neutral on-axis shot (the cheap default join between independently generated shots) · camera crosses during an uncut move · cutaway then re-enter on the new axis · subject visibly crosses, redrawing the line.

## 2. DOCTRINE

1. **Hitchcock's rule:** an object's size in frame is proportional to its narrative importance at that moment. Shot size is a story decision before it is an aesthetic one.
2. **Proxemics map to sizes** (Hall: intimate ≤45cm · personal ≤1.2m · social ≤3.7m · public beyond): intimate → ECU/CU · personal → MCU/MS · social → MS/FS · public → WS/ELS [v]. Frame the RELATIONSHIP, not just the body.
3. **Emotional beats: MCU-or-tighter AND a playable physical action** (transitive verb — "she clutches the letter"), never an adjective. Facial micro-expression is unreliable at ANY generated size; the body carries the emotion (merged house rule H2).
4. **Size ladder discipline:** prefer stepping through neighboring size groups — the three groups are FIXED: wide-group {extreme_wide, wide, full} · medium-group {medium_full, medium, medium_close_up} · close-group {close_up, extreme_close_up}; a >3-rung jump inside a scene is flagged unless motivated. The 30° rule is a separate, pure OR-gate: consecutive same-subject shots need ≥30° of angle change OR a clear size change — it does not stack with the ladder flag.
5. **The frame defines six offscreen zones** (beyond 4 edges, behind set, behind camera — Burch [v]): entrances/exits and off-screen sound expand the world at zero render cost.
6. **Aspect ratio changes the grammar, not just the crop:** 16:9 favors environment + lateral relationships; 9:16 favors one dominant subject in the upper-central band (focal zone ≈15–40% from top, bottom 15–25% caption-safe [v]); 1:1 favors centered, product-like framing. Vertical derivatives are RE-COMPOSITIONS with their own axis and screen direction — never center-crops.
7. **Every framing field must be resolvable to an observable** — if a reviewer can't verify it from the frame (or the cut, for `function`), it doesn't belong in the artifact.

## 3. DECISION TABLES

**Story goal → size**

| Goal | size |
|---|---|
| Establish place, scale, isolation | extreme_wide (function: establishing → stock candidate) |
| Full-body action, blocking, group entrance | wide / full |
| Hero intro, action-ready stance | medium_full |
| Neutral dialogue | medium |
| Building intimacy | medium_close_up |
| Peak emotional beat | close_up (+ playable action — Doctrine 3) |
| Critical object / sensory detail | extreme_close_up (function: insert) |
| Relationship / power between two | two_shot (size still stated separately) |

**Story goal → angle**

| Goal | angle |
|---|---|
| Neutral, objective | eye_level |
| Empower / heroize / threaten | low |
| Diminish / expose / endanger | high |
| Abstract geometry, flat-lay, ritual | overhead |
| Scale of crowd/city/landscape | bird_eye |
| Looming threat, powerless viewer | worm_eye |
| Trapped below, canopy reveal | underneath |
| Psychological instability | any + dutch_deg 5–45 |

**Effect → composition**

| Effect | tags / language |
|---|---|
| Dynamic tension | rule_of_thirds + explicit placement |
| Order, fate, artifice | centered_symmetry |
| Guide the eye in depth | leading_lines, depth_staged |
| Voyeurism / confinement | frame_in_frame (+ foreground_occlusion on stills) |
| Isolation or calm power | negative_space |
| Anticipation of motion | lead-room language ("negative space ahead of their movement") |
| Pre-signal importance | Hitchcock's rule — size up the object |

**Aspect grammar**

| Ratio | Strategy |
|---|---|
| 16:9 | thirds default; environment retained; lateral two-shots legal |
| 9:16 | subject upper-central (15–40% from top); bottom 15–25% caption-safe; NATIVE recomposition (lateral two-shots collapse — use rear-tracking or stacked staging); per-variant axis + screen_direction |
| 1:1 | centered/symmetric; tight margins; product/insert-friendly |

## 4. NUMERIC ANCHORS

- extreme_wide subject ≤10–15% frame height [v] · dutch bands 5–15° / 15–45° [v] (operative schema bands; the researched 45–90° extreme band is deliberately capped out — see the §1 dutch_deg note) · thirds lines at 33.3/66.6% [v]
- Headroom baseline: eyes ≈1/3 from top; shrinks CU→ECU, grows toward wide [v]
- 9:16 focal zone 15–40% from top; caption-unsafe bottom 15–25% [v]; 16:9→9:16 center-crop retains ≈32% of frame width [v] — recompose natively
- Proxemics (Hall, The Hidden Dimension): intimate 0–45cm → ECU/CU · personal 0.46–1.2m → MCU/MS · social 1.2–3.7m → MS/FS · public 3.7m+ → WS [v]
- 30° rule (pure OR-gate): consecutive same-subject shots differ ≥30° of camera angle OR a clear shot-size change (≥1 group step; groups enumerated in Doctrine 4), else jump-cut flag [v]

## 5. ALIASES & DO-NOT-CONFUSE

| Canonical | Aliases (authoring input only) |
|---|---|
| medium_full | cowboy shot, American shot, plan américain (genre-coded token — prompting "cowboy" drags Western wardrobe in; prompt the CUT LINE instead) |
| wide | long shot, LS |
| extreme_wide | extreme long shot, ELS, EWS |
| extreme_close_up (eyes) | Italian shot |
| overhead | god's-eye, top-down (90°, close) |
| bird_eye | aerial view (altitude) |
| dutch_deg | dutch angle, canted angle, oblique angle |
| function: insert/cutaway | b-roll (broadcast term — glossed, never a value) |
| (not a tag) golden_ratio | golden spiral, phi grid — stylistic descriptor; perceptual claims empirically unsupported; use rule_of_thirds |

**Do not confuse:**
- **overhead vs bird_eye** — 90° close-scale abstraction vs high-altitude scale; models conflate them, so the projection always emits the disambiguated phrase.
- **framing vs function** — a two_shot can be a master, a wide can be an establishing shot; one is what's IN the frame, the other is the shot's job in the cut.
- **insert vs cutaway** — insert re-shows what the master covered; cutaway shows NEW material and returns. Both cut back; only the cutaway widens the world.
- **looking room vs lead room** — gaze vs motion; they diverge and the prompt must say which.
- **wide vs full** — environment-forward vs body-forward; both show the whole body.

## 6. AI-GEN CAVEATS

- **Centering bias:** models re-center subjects even when off-center placement is requested — thirds prompts need explicit placement language ("left third, negative space right").
- **Multi-subject frames** (two_shot/group) carry elevated identity-bleed and limb-merge risk — anchor each figure: "A on the left third facing right, B on the right third facing left" + per-figure color blocking (production-design.md).
- **Extreme angles regress to safe defaults** — worm_eye/underneath/high dutch need geometry spelled out (foreshortening, vanishing points, degree).
- **Faces at distance distort** — below ~medium, don't rely on facial detail; silhouette and body pose carry the read.
- **Vertical is not rotated horizontal** — 9:16 needs vertical-native focal-zone language per shot.
- **Foreground occlusion on I2V** — persisting occluders flicker/morph; keep static or describe their motion.
- **ots foreground shoulders render sharp** — shallow-DoF clause is auto-emitted; verify at QA.
