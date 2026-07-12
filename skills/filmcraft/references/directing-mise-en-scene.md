# Directing — Mise-en-scène, Blocking & Continuity
KR: 연출 — 미장센·블로킹·연속성

**Read this when:** staging characters and designing continuity at `/ms-storyboard`; performance description in keyframe/motion prompts.

Scope: WHO stands where and why, HOW cuts preserve space, HOW performance reads as emotion — under a 5–10s generated-clip pipeline. Adjacent ownership: optics/deep focus/`lens_mm` → lens/camera reference · cut rhythm/ASL/transition mechanics → editing reference · lighting plot → lighting reference · VO/music → sound reference. Source: internal research dossier (directing dept, not shipped). Binding: `docs/filmcraft-rulings.md` §1.2–1.3, H1–H12, L1–L14.

---

## 1. CANONICAL TERMS

### 1.1 Blocking & Staging

| Term | KR | Use when | Effect | Prompt phrase | QA (+Caveat) |
|---|---|---|---|---|---|
| Actor Vector | 배우 벡터 | Any blocking needing felt directional momentum (pursuit, attraction, escape, confrontation) | Graphic/index/motion vectors read as continuing off-frame until countered; continuing=momentum, opposing=conflict, converging=confrontation | "walks screen-right, eyeline and shoulders angled screen-right, matching her arm pointing at the door frame-right" | prompt_adherence; restate explicitly per shot — no cross-generation vector memory |
| Triangle Staging | 트라이앵글 스테이징 | Multi-character dialogue needing shot variety without re-blocking | One camera setup yields clean singles/two-shots/group shots inside one consistent axis | "Triangle — A foreground-left, B mid-right, C background-center; all eyelines and axis legible from one setup" | spatial_continuity; lock relative positions/scale in a reference image, reuse across the scene's singles/two-shots |
| Staging in Depth | 심도 연출 (다층 미장센) | Audience must hold two narrative threads at once (fg conversation, bg threat) | Builds tension via visual density + viewer-directed discovery; ≠ deep focus (optics) — see §2 D10 | "Foreground: two argue. Background, small but sharp: a third figure enters through the door" | technical; cap at 2 planes — multi-plane sharp focus + multi-identity coherence both fail; else convert to a Dolly/Pan Reveal |
| Entrances/Exits (Frame-Edge Grammar) | 프레임 인/아웃 | Any entrance/exit, esp. across cuts or independently generated clips | Exit edge must match next shot's entry edge for continuous travel; re-entering the SAME edge implies reversal/return | "Shot A: exits frame-right. Shot B (new location): enters frame-left, same pace/angle" | spatial_continuity; must be manually tracked and restated per prompt — no persistence across generations |
| Movement Toward/Away from Camera | 카메라를 향한/멀어지는 이동 | Escalation beats (confrontation/threat/revelation) or resolution beats (departure/isolation) | Z-axis as emotional signal: approach compresses proxemic distance/raises stakes, withdrawal opens/reads as surrender | "She walks steadily toward camera, full shot to MCU, as she delivers the accusation" | prompt_adherence; reliable for first+last-frame interpolation — only 2 clear endpoint scales/positions needed |
| Cross & Counter-Cross | 크로스·카운터크로스 | Power/attention must shift visibly mid-scene without cutting | One actor crosses to rebalance the frame/shift dominance, answered by a complementary counter-move | "He crosses left-to-right past her to the window; she counter-crosses behind him into the vacated space" | technical; FLF collapses a multi-beat move to start/end blocking only — specify occlusion order (who passes in front) explicitly in text |
| Group Staging Hierarchy | 그룹 스테이징 위계 | Ensemble shots needing legible pecking order without dialogue | Dominance stack (largest/closest to lens, highest, most central, sharpest focus, brightest key) reads pre-verbally | "Boss centered, closest to camera, upper-frame; two subordinates flanking, lower, further back, softer focus" | character_consistency; relative scale/height across multiple characters drifts — lock a group reference image, reuse |
| Open vs Closed Staging | 열린/닫힌 스테이징 | Closed = formal/theatrical control; open = naturalism/surveillance/documentary energy | Closed reads composed/classical; open reads candid/unstable/voyeuristic | "Closed: both symmetric, full bodies, balanced negative space. Open: one back fills left edge, off-balance" | prompt_adherence |
| Business (Prop Action) | 비즈니스 (소품 행동) | Establishing traits/nervous states/status economically; filling static dialogue with subtext | Small, repeated prop activity reveals interiority indirectly | "He straightens the same stack of papers three times while she talks, never meeting her eyes" | character_consistency; prop identity/position needs the same reference-locking discipline as characters — see §2 D13 |
| Hall's Proxemic Distances | 홀의 근접학적 거리 | Choosing shot size to match a scene's social/emotional distance, independent of literal blocking distance | Shot size alone signals relational closeness before content is read — mapping in §4 [v] | "Former lovers reunite — frame at personal-distance MCU even though blocking places them at social distance" | prompt_adherence |
| Power Positioning in Frame | 프레임 내 권력 포지셔닝 | Status is contested or must be read visually | Higher/centered/foreground = dominant; contradicting expected positions signals irony or a coming reversal | "Interrogator stands, head near top-frame, foreground-left; suspect sits, small, centered, lower, further back" | spatial_continuity |

### 1.2 Continuity System

| Term | KR | Use when | Effect | Prompt phrase | QA (+Caveat) |
|---|---|---|---|---|---|
| Axis Establishment & Re-establishment | 축 설정·재설정 | Start of any 2+-subject scene; after a break/cutaway or when a new spatial relationship is needed | Fixes the 180° line via an early geography/master shot; machine-encoded as `scenes[].axis` — see §2 D1 | "Geography shot: A frame-left facing right, B frame-right facing left, table between — defines the line" | spatial_continuity; save this frame as the scene's geography reference keyframe (§6 #9) — every later shot cites it, never re-derives position from text |
| Legal Axis Crossings | 합법적 축 교차 | Story requires reframing a spatial relationship | 4 sanctioned methods preserve clarity through a reversal — see §2 D2 + §3.2 | "Insert a symmetrical two-shot (neutral) between the old-axis single and the new-axis single to license the flip" | spatial_continuity; method 3 (cutaway/insert) is the cheapest/most reliable default — exact axis-matching across separate generations is fragile |
| 30° Rule | 30도 법칙 | Cutting between two shots of the same subject | Below-threshold angular change reads as a jump cut; ≥30° or a size-rung change reads as deliberate — INTENT FLAG, not a block (§2 D3) [v] | "Cut from 3/4-front MS to profile MCU (>30° plus size change), not front MS to near-identical front MS" | technical; flag two same-subject generations at near-identical angles as jump-cut risk |
| Eyeline Match Geometry | 시선 매치 기하학 | Any look→subject or look→POV cut | Off-frame gaze direction/vertical angle must correspond to the framing/implied position of what's looked at; qualitative only — NO degree tolerance (§2 D4) | "A looks screen-right and slightly up. Cut to B, positioned screen-left of implied space, at a height justifying the angle" | spatial_continuity; state `gaze_target` + implied height explicitly in BOTH shots' prompts — open research item P6-4 |
| Screen Direction Preservation | 스크린 방향 일관성 | Any journey/travel sequence | Established travel direction persists across cuts/scenes until a deliberate, motivated reversal; machine field = `screen_direction` | "Every shot of the journey keeps the car moving screen-right; the return trip opens with a neutral head-on shot before flipping" | spatial_continuity; HIGHEST-RISK failure point — L/R prompts documented unreliable [v]; NEVER repair with ffmpeg flop — banned by default (H9, §2 D14) |
| Match on Action (MOA) | 동작 일치 편집 | Actions that would otherwise force an awkward static-pose cut | A few frames of motion overlap disguise the cut — NOT a graphic/conceptual match cut (editing reference) | "Shot A ends mid-turn, head rotating; Shot B begins a few degrees further into the same rotation from a new angle" | technical; frame-accurate overlap across independent generations is unreliable — match A's LAST frame / B's FIRST frame to the same mid-action pose, smooth any pop with a short cross-dissolve in post |
| Coverage vs Découpage (H4) | 커버리지 대 데쿠파주 | Découpage always; coverage only for hero scenes carrying the key emotional beat | Découpage (shot breakdown) is MANDATORY — the clip ceiling forces it; coverage (redundant master+singles+insert) is a deliberate hero-scene-only spend, not the default (§2 D11) | "Coverage set (hero scene): (1) wide master, (2) clean single A, (3) clean single B, (4) hand insert" | prompt_adherence; validator: scene ≥3 shots ⟹ ≥1 insert/cutaway/reaction (H4) |
| Shot-Reverse-Shot Conventions | 숏-리버스숏 관습 | Standard two-person dialogue coverage | Matched OTS/singles from consistent, axis-legal positions; mismatch feels "off" even unnamed | "A's OTS: MCU past B's shoulder, B's shoulder occupies the same lower-frame % as A's shoulder in B's reverse OTS" | spatial_continuity; each OTS is a separate generation — explicitly match shoulder-framing %, camera height, implied focal length in both prompts |
| Neutral/On-Axis Shot | 뉴트럴 샷 | As a hinge to legally cross the axis, or to open/close a scene with spatial neutrality | Symmetrical shot on the 180° line, no "side," safe to cut to from either side — resets spatial bookkeeping; the DEFAULT cheap join (§2 D2) | "Symmetrical head-on two-shot, both equidistant from lens, before cutting to reversed-axis coverage" | spatial_continuity; cheapest, most reliable pipeline joint between two independently generated shots of uncertain axis-match |
| Clean/Dirty Single & OTS Pairing | 클린/더티 싱글 | Dirty keeps conversational context; clean isolates for emotional focus (interrogation/breakdown/revelation) | Dirty/OTS keeps the relationship visually present; clean isolates and intensifies; `dirty` field ⟹ auto shallow `dof` | "Dirty single on A: soft, dark sliver of B's shoulder lower-frame-right. Clean single on A for the confession beat" | spatial_continuity; keep the same choice (clean vs dirty, which shoulder side) consistent within one scene's generations |

### 1.3 POV & Address

| Term | KR | Use when | Effect | Prompt phrase | QA (+Caveat) |
|---|---|---|---|---|---|
| Objective vs Subjective Camera | 객관적/주관적 카메라 | Objective by default; subjective when the audience must see exactly what a character sees | Subjective raises identification, creates tension/unease if overused | "Objective: camera watches both from outside. Subjective: camera IS A's eyes, looking at B" | prompt_adherence |
| POV Sequence Structure (Look → POV → Reaction) | POV 시퀀스 구조 | Establishing what a character notices and how it affects them | 3-shot grammar constructs subjectivity; the reaction shot is where meaning lands (Kuleshov, §1.6) | "(1) A turns, eyes widening, looking screen-left off-frame. (2) POV: open door, matched eyeline. (3) A's face, reaction" | spatial_continuity; all 3 are independent generations — gaze angle/height set in shot 1 must be manually copied into shot 2; `framing:pov` requires `pov_of` set + emits "no visible camera or hands" |
| Free Indirect Subjectivity | 자유간접주관 | Emotional coloring without committing to a literal POV shot | Camera stays objective but is stylistically inflected by the character's state — ambiguity between narrator/character consciousness | "Camera stays objective (full body visible) but drifts and tilts unsteadily, pace slowing as her anxiety builds" | prompt_adherence; describe via concrete camera behavior (drift/hesitation/tilt/rack focus) — the abstract term won't render; contested lineage (Pasolini vs Deleuze), loose craft register |
| Dream/Memory Framing | 꿈·회상 프레이밍 | Flashback, dream, fantasy, subjective memory distortion | Soft focus/desaturation/slow motion/altered frame rate/dissolve bookends signal "not current/literal" before content registers | "Diffusion haze over the frame, desaturated toward blue, 60%-speed movement, dissolve in from the present-day shot" | technical; CHEAP WIN — global style tokens (not positional/continuity requirements) prompt reliably; deploy when a scene's axis/eyeline/identity continuity is otherwise fragile (§2 D9) |
| Direct Address | 정면 응시 (제4의 벽 파괴) | Deliberate in comedy/mockumentary/PSA/ad pitches/confessionals; an error if accidental | Collapses narrative distance; implicates/addresses the viewer | "She turns, eyes locking with the lens, a half-smile, speaking straight to camera" | prompt_adherence; models default to "safe" 3/4 gaze, avoid precise lens-height eye contact — needs emphatic prompting + retries |

### 1.4 Reveals

| Term | KR | Use when | Effect | Prompt phrase | QA (+Caveat) |
|---|---|---|---|---|---|
| Dolly/Pan Reveal | 달리·팬 리빌 | Building anticipation before a reveal, or recontextualizing | Camera move discloses previously excluded information; feels "discovered," not cut-presented | "Camera pans right across the empty room, decelerating to reveal a motionless figure in the corner" | prompt_adherence; feasible within a single generation — PREFER over multi-shot reveals |
| Foreground-Blocker Reveal | 전경 차단 리빌 | A reveal needs a "natural," non-cut trigger | Foreground object/person obstructs until it moves, unblocking to disclose something new; feels environmentally motivated | "A passing truck fills the foreground for a beat; as it clears, a character who wasn't there before stands across the street" | technical; doubles as a disguised join point between two generated clips — the blocker covers the cut like a whip pan |
| Mirror Reveal | 거울 리빌 | Compact reveal of a hidden presence/face | Reflective surface discloses what direct frame excludes; uncanny/doubled register | "Her back to camera at the vanity; the mirror reflects her face, and a second figure in the doorway she hasn't noticed" | technical — HIGH RISK, ACTIVE AI FAILURE MODE, verified research [v]; avoid single-gen for plot-critical beats — composite in post, or substitute a Turn Reveal/Foreground-Blocker (§2 D8). DO NOT CONFUSE with flop/"mirror" (§5) — unrelated |
| Over-the-Shoulder Turn Reveal | 턴 리빌 | Withholding identity/reaction until a chosen beat | Character with back/profile to camera turns to disclose face/expression at the reveal beat | "Back to camera, shoulders tense; on the door slam she turns fully, revealing tears already streaking her face" | prompt_adherence; a same-shot turn (single generation) is more reliable than a cut-based reveal — set pre-turn pose and post-turn expression as the first/last-frame pair |
| Delayed Reveal / Offscreen Space (Bresson/Haneke) | 지연된 리빌 (오프스크린 공간) | Violence/trauma/information whose impact is stronger implied than shown | Withholds the event, holds on reaction/empty frame/offscreen sound — six implied zones, see §4 [v] | "Hold on the empty doorway and offscreen-left struggle sounds; cut to her face only after, catching her breath" | prompt_adherence; strong pipeline-friendly technique — shifts the burden from a continuity-fragile action to sound design + reaction framing |
| Dramatic Irony Staging | 극적 아이러니 스테이징 | Building suspense/dread from anticipation rather than surprise | Frame holds a visible threat/fact the audience registers but the character does not (Hitchcockian engine) | "She chats casually foreground, unaware; deep background through the window, an unrecognized car pulls up" | technical; requires two simultaneous legible planes at correct relative focus/scale — apply Staging-in-Depth's 2-plane-max guidance |

### 1.5 Motif & Symbol

| Term | KR | Use when | Effect | Prompt phrase | QA (+Caveat) |
|---|---|---|---|---|---|
| Visual Motif Repetition with Variation | 시각적 모티프 반복·변주 | Marking character/thematic development by returning to a transformed "same" image | Recurring composition/gesture/framing changes meaning through context; rewards attentive viewers | "Act 1: alone at the window, arms crossed, closed staging. Act 3: same window/framing, but open staging, another figure beside her" | spatial_continuity; requires precise cross-scene framing consistency — lock camera position/lens/composition as a reusable template |
| Plant-Payoff Imagery | 플랜트-페이오프 이미지 | Any object/image that will matter later (visual Chekhov's gun) | Early unremarked detail recurs with dramatic significance; payoff feels earned/inevitable in hindsight | "Plant: a cracked watch face, background insert, unremarked. Payoff: same watch, centered and sharp, stopped at the accident's moment" | character_consistency; plant/payoff shots generate far apart — save the object's reference image from the plant shot, reuse verbatim at the payoff |
| Color/Object Motifs (staging side) | 색채·오브제 모티프 | Coordinating with color/production-design to reinforce a motif through blocking | Consistent placement/handling/blocking treatment of a symbolic object reinforces thematic throughlines physically | "The red scarf is staged in her hands, foreground, whenever she lies; absent or discarded background when she tells the truth" | character_consistency; treat the motif object as a locked reference asset across every appearance — same system as Business (§2 D13) |

### 1.6 Performance

| Term | KR | Use when | Effect | Prompt phrase | QA (+Caveat) |
|---|---|---|---|---|---|
| Playable Actions/Verbs | 플레이어블 액션 (동사형 연기 지시) | Any performance direction, and any keyframe/motion prompt describing what a character is doing | Concrete transitive action (accuse, comfort, dismiss) produces legible specific behavior; adjective-only direction produces vague "acting faces" (§2 D5/D6) | "She clutches the letter to her chest and backs toward the door" (playable) — NOT "she is sad and scared" (unplayable) | prompt_adherence; models render concrete verbs far more reliably than abstract emotion words — always translate an adjective beat into a playable action (H2) |
| Emotion Through Body & Gesture (Readable Silhouette) | 신체 연기·실루엣 가독성 | Shot sizes where facial nuance can't be trusted; general staging-clarity check | Pose/gesture stays legible reduced to a flat black silhouette — separate limbs from torso, avoid overlapping "blob" poses | "Shoulders collapsed inward, one arm wrapped across the body, head turned away — reads 'shutting down' even in silhouette" | character_consistency; PRIMARY emotional carrier at ALL sizes in AI-gen, not just wide — facial nuance unreliable even in CU (H2) |
| Micro-Expressions vs Distance | 거리별 미세표정 신뢰도 | Deciding whether a beat needs a close-up or body staging | Subtle facial expression only reliably renders at close sizes in craft theory — AI-gen is STRICTER: unreliable even in CU | "Save the tear and lip tremor for the CU; the wide covering the same beat relies on posture and hand gesture" | technical; default to body/gesture as primary channel at ALL sizes, not only medium/wide (H2) |
| Reaction-Shot Primacy | 리액션숏 우선성 | Structuring dialogue/POV sequences — ensure a reaction shot receives the "real" beat | Emotional meaning lands on the listener/observer's reaction, not the speaker/triggering action; cutting away undercuts the scene | "After the accusation lands, cut to and HOLD on the accused's face/posture — that shot delivers the scene's meaning" | prompt_adherence; carry the reaction's meaning via body/gesture staging or wider framing rather than a subtle facial CU; DOCTRINE-level, paired with Kuleshov Effect (§2 D7) |
| Kuleshov Effect | 쿨레쇼프 효과 | Underlies POV sequences and reaction-shot primacy — invoke when deciding what to cut TO | Audience infers emotion by juxtaposing a neutral shot against what follows; the same performance reads as hunger/grief/desire depending on the next shot | "Generate the reaction shot as genuinely neutral/ambiguous if the following POV insert should define its meaning" | prompt_adherence; cost-saving — one neutral reaction pairs with different POV inserts for different readings; taught as DOCTRINE, evidentiary status: original footage lost, replications mixed (L3, §2 D7) |

---

## 2. DOCTRINE

D1. **Axis is machine state, not folklore.** Every scene carries a structured `scenes[].axis` block: `{established_by_shot_id, a: <char>, b: <char>, a_side: left|right, note}` — the shot that first fixed the 180° line, the two subjects defining it, and which side `a` occupies. Every shot where a subject moves or looks sets `camera.screen_direction: left|right|toward_camera|away_from_camera|neutral`. Axis-legality becomes a checkable field pair, not an inference from prose — the schema IS the continuity log Axis Establishment (§1.2) used to require a script supervisor's memory.

D2. **Four legal crossings, one cheap default.** (1) neutral/on-axis hinge shot, (2) camera physically crosses during an uncut move, (3) cutaway/insert then resume on the new axis, (4) subject visibly crosses the line, redrawing it. All four preserve clarity. For this pipeline, method (3) — inserting a Neutral/On-Axis Shot (§1.2) — is the DEFAULT: exact axis-matching across two independently generated clips is fragile, but a symmetrical neutral shot is cheap, safe to cut to from either side, and carries no cross-generation state requirement.

D3. **30° rule is an intent flag, never a block.** Below-threshold angular/size change between consecutive same-subject shots reads as a jump cut. Encode it as a QA warning on the pair, not a generation-time validator — some cuts (soft_cut technical repairs, deliberate jump-cut style) legitimately violate it. Pair with a shot-size-rung change when angle alone is unavailable.

D4. **Eyeline has no degree number.** The 15–20° eyeline-to-camera tolerance in older craft literature is an unsourced folk number — REJECTED. Controlled vocabulary uses `gaze_target: to_camera|off_left|off_right|off_up|off_down|at:<char>|none` and a qualitative rule only: a gaze reads clearly on-lens or clearly off-lens; nothing between is authored. Precise geometric wording remains an open research item (P6-4) — do not invent a tolerance band to fill the gap.

D5. **Emotional beats: MCU-or-tighter AND a playable verb — never an adjective (H2).** Merges two findings: (a) micro-expression is unreliable at ANY shot size in generative video, even ECU, so shot size alone never guarantees legible emotion; (b) adjective-only direction ("she is sad") produces vague "acting faces" regardless of size. Rule: an emotional beat must BOTH be framed `medium_close_up`-or-tighter AND be written as a concrete transitive action a character does (Playable Actions, §1.6) — body/silhouette carries the beat, the tight frame is necessary but not sufficient. Run the Silhouette Readability Test on every emotional beat: strip the pose to a flat black silhouette — if the state doesn't read, the staging is the problem, not the shot size.

D6. **Playable-action lineage: borrow the surface principle, not one school.** Stanislavski's action/objective system, Mamet & Macy's Practical Aesthetics, and Meisner all converge on the same transitive-verb surface principle from different theoretical roots. Cite the technique, not a single lineage — the convergence itself is the evidence.

D7. **Reaction-shot primacy + Kuleshov, taught as doctrine with evidentiary status stated (L3).** Meaning lands on the reactor, not the speaker or the triggering action — DOCTRINE-level guidance for sequencing POV/dialogue coverage. Its foundational proof, the Kuleshov experiments, has an honest evidentiary gap: the original footage is lost, and modern replications are mixed. Teach the effect as the working model for what a cut TO accomplishes; do not cite it as settled empirical fact.

D8. **Mirror reveals are an active, verified AI failure mode.** Diffusion/video models render geometrically wrong or incomplete reflections (Reflecting Reality, MirrorFusion, MirrorVerse — research-verified, not a craft guess). Never single-generate a plot-critical Mirror Reveal (§1.4). Default remedy: composite in post, or substitute an Over-the-Shoulder Turn Reveal or Foreground-Blocker Reveal — both reliable single-generation alternatives delivering the same beat.

D9. **Dream/memory framing is a cheap win that covers drift.** Its markers (soft focus, desaturation, slow motion, dissolve bookends) are GLOBAL STYLE TOKENS, not positional or cross-shot continuity requirements, so they prompt reliably where axis/eyeline/identity fields do not. Deploy deliberately on a scene whose continuity is otherwise fragile — the stylization reads as authored intent, not as drift.

D10. **Deep space ≠ deep focus ≠ staging in depth (L2).** Deep space is a mise-en-scène fact: meaningful elements exist at multiple distances from camera. Deep focus is an optics fact: multiple planes render sharp (owned by the lens/camera reference, not here). Staging in depth is the DIRECTING technique of using deep space for simultaneous action. Deep space staged with shallow focus (one plane sharp, others soft but legible) is common and fully expressible — staging-in-depth does not imply a deep-focus lens choice.

D11. **Coverage vs découpage — the ceiling forces shot breakdown (H4).** The 5–10s generated-clip ceiling makes true single-take, multi-beat designed scenes infeasible. Découpage (breaking a scene into discrete planned shots) is therefore the MANDATORY default, not a style choice. Coverage (shooting redundant alternates — master + singles + insert of the SAME beat, for edit-time flexibility) remains a deliberate, additional spend reserved for hero scenes carrying the scene's key emotional beat. Validator: any scene with ≥3 shots must carry ≥1 shot with `function: insert|cutaway|reaction`. Practical split: dialogue scene needing flexible edit → coverage set as separate generations; single emotional beat, no angle change → one designed shot; complex multi-beat blocking wanting a oner → break into designed shots joined by hidden Match on Action, labeled `stitched_oner` (§5).

D12. **Geography reference keyframe, one per scene.** The shot that establishes the axis (Axis Establishment, §1.2) is saved as the scene's reference image. Every later shot in the scene cites this frame rather than re-deriving character position/scale from text — the single highest-leverage fix for the #1 AI production concern: no persistent identity/position across generations (MIT AI Film Hack 2025) [v].

D13. **Prop and motif objects are reference-locked like characters.** Business props (§1.1), plant-payoff objects, and color/object motifs (§1.5) all require the same reference-image discipline as character identity: generate once, save, cite on every reappearance — never re-describe from text alone at the payoff.

D14. **Flop is banned by default (H9).** Repairing a Screen Direction Preservation violation (§1.2) with an ffmpeg horizontal flip is FORBIDDEN as the default rule — any character-carrying shot that is flopped invalidates the character reference bank outright (a mirrored face ≠ the reference sheet). Text/logos, jewelry-side, hair part, scars, handedness, vehicle steering side, and asymmetric wardrobe are AGGRAVATORS that make the damage visible even in non-character shots — they are not the trigger condition. No `hflip` field exists in the schema; its absence is the ban. Default remedy: regenerate the shot, or bridge with a Neutral/On-Axis Shot or a cutaway.

---

## 3. DECISION TABLES

### 3.1 Dramatic intent → blocking choice

| Intent | Staging choice |
|---|---|
| Growing intimacy/threat | Move subject toward camera (Z-axis); tighten `shot_size` |
| Isolation/resignation/farewell | Move subject away; widen; Open Staging |
| Power imbalance | Foreground+height for dominant; background/lower/off-center for subordinate (Power Positioning) |
| Alliance forming | Cross to close proxemic gap; bodies angled toward each other |
| Betrayal/rupture | Counter-cross breaking the triangle; Open Staging replaces Closed |
| Hidden threat audience should feel | Threat in background plane, character unaware foreground (Staging in Depth, 2-plane max) |
| Confession/vulnerability | Closed, symmetric staging; reduce depth layers; intimate proxemics + MCU-or-tighter + playable action (D5) |
| Ensemble hierarchy reveal | Staggered Group Staging Hierarchy; dominant figure apex/foreground/center |

### 3.2 Continuity situation → axis handling

| Situation | Choice |
|---|---|
| Scene continues same location/beat | Maintain established `scenes[].axis` — no new axis; `screen_direction` continues its prior value |
| Need a new angle, <30° available | Cutaway/insert first (`function:cutaway`/`insert`), or a ≥2-rung `shot_size` change |
| Must reverse geography | Neutral/On-Axis Shot, OR camera crosses during an uncut move, OR cutaway then declare a new axis (`established_by_shot_id` updates) |
| Character reverses travel direction | Motivate onscreen (visible turn) so `screen_direction` visibly re-draws — never silently flip the field |
| Joining two independently AI-generated shots | Default: Neutral/On-Axis Shot as the join (D2) |
| Fixing a drifted `screen_direction` post-generation | Regenerate, or insert a bridging shot — NEVER ffmpeg flop (banned by default, D14/H9) |

### 3.3 Reveal goal → technique

| Goal | Technique |
|---|---|
| Audience complicit/anxious ahead of the character | Dramatic Irony Staging |
| Inside a character's literal perception | True POV — `framing:pov` + `pov_of` set, bookended by look/reaction (POV Sequence Structure) |
| Emotional coloring without full subjectivity | Free Indirect Subjectivity (drift/tilt/pace, described concretely) |
| Withhold payoff to build dread | Delayed Reveal / Offscreen Space |
| Payoff of a planted image | Visual Motif Repetition or Plant-Payoff — repeat the locked reference composition, with variation |
| Compact hidden-presence reveal, low risk | Foreground-Blocker Reveal or Over-the-Shoulder Turn Reveal |
| Compact hidden-presence reveal, plot-critical | NEVER single-gen Mirror Reveal (D8) — composite in post |

---

## 4. NUMERIC ANCHORS

- **Shot-size cut-lines** (never cut at a joint): `extreme_wide` subject ≤10–15% frame height · `wide` full body + substantial environment · `full` full body, edges near head/feet · `medium_full` = **mid-thigh** (≡ cowboy ≡ American ≡ plan américain — aliases, never values; the knee/mid-thigh two-rung split is REJECTED as unsourced and joint-cutting) · `medium` waist · `medium_close_up` chest · `close_up` shoulders · `extreme_close_up` detail ("Italian shot" = eyes-only alias).
- **Hall's proxemic zones → shot size** [v] (Edward T. Hall, *The Hidden Dimension*, 1966): intimate 0–18in (0–45cm) → `close_up`/`extreme_close_up` · personal 1.5–4ft (46cm–1.2m) → `medium_close_up`/`medium` · social 4–12ft (1.2–3.7m) → `medium`/`full` · public 12ft+ (3.7m+) → `wide`/`extreme_wide`. Signals relational closeness independent of literal blocking distance.
- **30° rule** — classical continuity convention, formalized in editing textbooks (Hurbis-Cherrier; Corrigan & White), not a single-author citation: ≥30° camera-position change between consecutive same-subject shots, OR a `shot_size`-rung change, else jump-cut flag (D3). No fixed numeric threshold exists for how "on-axis" a Neutral Shot must be — treat qualitatively, do not invent a number.
- **Burch's six offscreen zones** [v] (Noël Burch, *Theory of Film Practice*, 1973): beyond each of the 4 frame edges (top/bottom/left/right) + behind the set + behind the camera. Used by Delayed Reveal / Offscreen Space to place what's withheld.
- **Eyeline: no degree number** (D4) — the previously circulated 15–20° figure is retired, not a fallback; qualitative on-lens/off-lens rule only.
- **Pipeline clip ceiling**: 5–10s per generated shot — the numeric driver that makes découpage mandatory (D11).
- **`dutch_deg`**: 0–45, a separate ROLL field from `angle` (alias: canted/dutch angle) — full taxonomy in the camera/lens reference; relevant here where a canted low angle pairs with Power Positioning/Group Staging dominance framing.

---

## 5. ALIASES & DO-NOT-CONFUSE

**Aliases (canonical ← informal)**
- `medium_full` ← cowboy, American (shot), plan américain
- `function:insert`/`cutaway` ← b-roll (broadcast term; glossed to insert/cutaway in narrative context, L4)
- Gilligan cut ← gloss only, not a distinct schema value (L4)
- canted ← dutch angle, `dutch_deg` > 0

**Do-not-confuse**
- **Deep space ≠ deep focus ≠ staging in depth** (D10/L2) — three different layers; only the last is authored in this file.
- **Mirror Reveal (staging device, §1.4) ≠ flop/"mirror" (ffmpeg horizontal flip, H9)** — same everyday word, opposite domains: one is a reflective-surface reveal technique (high AI risk); the other is a banned post-production geometry operation. Never let "mirror" in a note mean both.
- **Coverage ≠ découpage** (D11/H4) — coverage is the redundant-alternates SPEND (hero scenes only); découpage is the MANDATORY shot breakdown itself. Older phrasing used "coverage" for both; corrected.
- **Insert (re-emphasizes what the master covered) ≠ Cutaway (NEW material, returns)** (L7) — both are `function` enum values, distinguished by whether the material was already visible in the master.
- **POV shot: strict vs loose** — controlled vocabulary uses the strict definition (`framing:pov` = true optical-subjective camera, `pov_of` required); "industry POV" for any shot merely near a character's position is loose slang, gloss only, never authored as `framing:pov`.
- **Match on Action ≠ graphic/conceptual match cut** — MOA is action-continuity across an axis-legal cut; a graphic match (shape/motion-conceptual rhyme) belongs to the editing reference, not staged here.
- **"Long take" ≠ "stitched oner"** — reserve `long_take` for genuine single-pass material; a sequence built from disguised Match on Action / Foreground-Blocker joins is a `stitched_oner`. Client-facing copy: "designed as a continuous take" — NEVER "single take" (truth-in-labeling, ruling 1.4).
- **Free Indirect Subjectivity ≠ true POV ≠ Objective Camera** — a three-point spectrum, not a binary; free indirect keeps the body visible (objective framing) while the camera's behavior (drift/tilt/pace) carries the subjective coloring.

---

## 6. AI-GEN CAVEATS

1. **No persistent character identity/position across generations** — #1 ranked production concern (MIT AI Film Hack 2025) [v]. Mitigate with a geography reference keyframe per scene (D12) + reference-lock every character/prop/motif (D13).
2. **Axis state is not tracked by the model** — `scenes[].axis` + `screen_direction` must be authored explicitly per shot; nothing carries over between generations.
3. **Neutral/insert join is the forced-cheap default** for crossing shots between two independent generations (D2) — plan for it, don't treat it as a fallback.
4. **Eyeline drifts** — state `gaze_target` and implied height explicitly in BOTH the look shot and the answering shot; no shared memory between them.
5. **Mirrors are a verified, active failure mode** [v] — never single-generate a plot-critical Mirror Reveal (D8).
6. **Left/right directional prompting is documented unreliable** [v] — treat generated `screen_direction` as provisional; anchor position to a fixed in-frame landmark in the text too, not only "screen-left/right."
7. **ffmpeg flop is banned by default as a direction fix** — any flopped character shot invalidates the reference bank; text/logos/asymmetric identity markers are aggravators, not the trigger (H9/D14). Regenerate or bridge instead; no `hflip` field exists.
8. **First+last-frame interpolation cannot specify a mid-beat** — split into two clips so the mid-state becomes an explicit keyframe (relevant to Cross & Counter-Cross, multi-beat blocking).
9. **Multi-character staging compounds identity/scale drift** — one locked geography reference keyframe per scene, reused, never re-derived (D12).
10. **Facial micro-expression is unreliable at ANY shot size** — body/silhouette is the primary emotional carrier everywhere, not only in wide shots (D5/H2); reserve facial CUs for stark, simple expressions only.
11. **Dream/memory framing is a reliable cheap win** — global style tokens prompt consistently; deploy to cover a scene whose continuity is otherwise fragile (D9).
12. **True long-take staging-in-depth is infeasible under the clip ceiling** — simulate with disguised Match on Action / Foreground-Blocker joins; label the result `stitched_oner`, never "single take."
13. **Découpage is mandatory, not optional** (D11/H4) — budget every multi-beat scene as discrete shots from the start; coverage is the hero-beat add-on, never the default.

---
Traceability: D1–D14 ↔ rulings H1–H12/L1–L14 as cited inline. Numeric anchors marked [v] are inherited research figures subject to Phase 6 spot-check (P6-6); eyeline wording is open research (P6-4).
