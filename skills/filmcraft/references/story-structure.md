# Story Structure — 서사 구조와 씬 크래프트

Canonical narrative-structure, scene-craft, character, and commercial-framework vocabulary.
**Read this when:** planning at /ms-plan (structure selection, beat_map, controlling idea); validating beats and value shifts at /ms-storyboard.

## 1. CANONICAL TERMS

### Macro structure

| Term | KR | Use when | Effect | Artifact instruction | QA / Caveat |
|---|---|---|---|---|---|
| catalyst | 촉발 사건 | the disturbance that ruptures the status quo — EVERY duration | stakes-in-motion; the reason to keep watching | beat_map: `catalyst` at ~11% (or the 3s clamp — see tiers). ≡ inciting incident ≡ call to adventure (aliases — pick ONE label per project) | do NOT add a "recruitment" beat — the protagonist's commitment IS `break_into_two` (~22%); adding it duplicates an existing slot |
| break_into_two | 2막 진입(결단) | the protagonist COMMITS and enters the new situation | the disturbance becomes a story | beat_map ~22%; must carry the commitment decision | the world-event/decision split is catalyst vs break_into_two — already two beats |
| debate | 주저(디베이트) | the gap between disturbance and commitment (≥90s pieces) | reluctance humanizes; raises the cost of commitment | optional beat 11–22% | compress into montage below 45s |
| midpoint | 미드포인트 | the plan inverts — false victory or false defeat | recalibrates stakes at the center | beat_map 50% | — |
| all_is_lost | 최악의 순간 | the visible moment of loss | lowest external point | beat_map ~68% | distinct from dark_night (the AFTERMATH) |
| dark_night | 어둠의 밤 | the low REFLECTION before the final push (≥90s) | interiorizes the loss | optional 68–77% | — |
| break_into_three | 3막 진입 | the insight that enables the finale | synthesis → action | beat_map ~77% | — |
| final_image | 파이널 이미지 | proof of change — the opening's mirror | closes the arc visually | opening_image/final_image mirror pair (already a house field) | — |
| theme_stated / b_story / fun_and_games / bad_guys_close_in / finale | 주제 선언/B스토리/재미와 놀이/조여오는 위협/피날레 | texture beats for ≥90s pieces | fills the tentpoles with movement | optional beats (STC percentages in anchors) | 15-beat granularity does not survive <60s |
| three_act (Field) | 3막 구조 | goal-driven narrative with a clean spine | familiar causal engine | PP1 ~25% · midpoint 50% · PP2 ~75%; pinches 37.5/62.5% [v] | percentages were calibrated on features — below ~20s use the 3-beat form, not "compressed acts" |
| story_circle (Harmon) | 스토리 서클 | episodic/serial; complete arc in a tight container | a full "lap" of departure and return | 8 steps ≈12.5% each [v] | cleanest 1:1 mapping to clip counts at 45–75s (≈1 step per clip) |
| sequence_method (8-sequence) | 8시퀀스 기법 | any multi-scene piece | in the source method a SEQUENCE (~1/8 of a feature, itself several scenes) is a mini-movie with its own goal/obstacle/partial resolution | SCALE-COLLAPSE mapping: in a ≤120s piece, one storyboard scene (2–4 clips) plays the structural role a sequence plays in a feature — a deliberate adaptation, not the method's own containment | the strongest natural fit for this pipeline |
| kishotenketsu | 기승전결 | mood pieces, slice-of-life ads, brand-world films where a villain would feel forced | recontextualizing twist (転) without manufactured jeopardy | 4 beats ≈25% each; the twist RE-FRAMES beats 1–2 | the twist needs a VISUAL pivot (match-cut / FLF continuity) or it reads as an unrelated shot; "non-driving-conflict," not "conflict-free" |
| heros_journey (Vogler) | 영웅의 여정 | transformation-driven brand films, origin stories | legible growth arc | select 4–6 load-bearing stages (call, threshold, ordeal, return) | 12 stages do NOT fit 30–120s 1:1 |
| freytag (medial climax) | 프라이타그 피라미드 | tragedy-inflected pieces — a deliberate, flagged choice | symmetrical rise-and-fall; climax at the CENTER | log the choice; retention data pulls against it for ads | never a default for commercial content |

### Scene craft

| Term | KR | Use when | Effect | Artifact instruction | QA / Caveat |
|---|---|---|---|---|---|
| value_shift | 가치전환 | EVERY scene (house field) | a scene is a unit of CHANGE — start and end on different charges | `value_shift {from,to,mechanism}`; from==to = non-event → cut or merge | already enforced; this file adds the PROGRESSION rule below |
| polarity progression | 극성 진행 | chaining scenes | escalating AMPLITUDE, not just alternating sign | alternation is the DEFAULT texture; a same-kind run is legal when AMPLITUDE grows — measured on department axes, anchor deltas are ordinal hints not a metric (Diminishing Returns targets repeated FEELING, not repeated sign — McKee's Thematic Square progression is itself one long fall); the ONE hard sign rule: climax end-charge flips vs the scene before it (crisis↔climax) — emotion-recipes R2/M1–M4 | AI clips are planned independently — carry the prior scene's end-polarity into the next scene's brief ("continuing from a false-victory high…") |
| objective / obstacle / tactic | 목표/장애/전술 | any scene at risk of "characters talking" | converts dialogue into filmable behavior | scene summary names all three; tactic SHIFTS mid-scene = the scene works | tactic shifts need visible behavioral change across clips |
| turning point | 터닝 포인트 | placing the clip break for maximum charge | revelation + decision + action | end a clip on the revelation (CU); open the next on the decided action | — |
| the gap | 갭(기대-결과) | a tactic fails; improvisation | surprising-yet-inevitable | expectation → different result → REACTION beat | the reaction needs its own clip/frame — compressed into one clip it reads as nothing happened |
| setup / payoff | 복선/회수 | any plant meant to make a later turn feel earned | retroactive "oh!" | plant = unremarked insert (function: insert, 1–2s); payoff = same object recontextualized | encode plant & payoff as LINKED shot fields; repeat the EXACT visual token in both prompts (cross-clip memory does not exist) |
| chekhovs_gun | 체호프의 총 | storyboard audit | unfired promises waste attention; unearned payoffs break trust | QA: every close-up insert must recur or be cut | AI keyframes ADD incidental salient objects that read as plants — treat any strong visual singleton as an implicit promise |
| plant-to-payoff distance | 복선-회수 간격 | calibrating placement in short form | too close = telegraphed; too far = forgotten | ≤90s: plant in the first 40%, pay off within 2–4 clips; visual plants over verbal (mute-first viewing) | — |
| dramatic irony | 극적 아이러니 | suspense without a countdown; comedy/cringe | the audience leans forward, wanting to warn | storyboard as TWO explicit shots (audience view + character's ignorance) | a single clip cannot carry the double knowledge |
| suspense vs surprise | 서스펜스 대 서프라이즈 | deciding when the audience learns of the threat | Hitchcock: surprise ≈15 seconds of shock; suspense ≈15 minutes of engagement [v] | default SUSPENSE-FORWARD (reveal to camera early); reserve true surprise for the FINAL clip | twist endings are structurally expensive in ≤10s clips |
| iceberg (show-don't-tell) | 빙산 이론 | any beat at risk of exposition dialogue | implication over statement (7/8 underwater [v]) | replace VO explanation with a telling image | **INVERTS FOR AI: the model has no offscreen imagination — the hidden 7/8 must be written INTO the prompt even though only 1/8 appears on screen**; omitting it produces a blank, not subtext |
| in_medias_res / cold_open | 사건 한복판 시작/콜드 오픈 | short-form default openings | skips preamble; curiosity carries | cold open: logo/title only after the hook shots | anchor with 2–4 words of on-screen text or it reads context-free; respect platform skip timing (~5s) |
| button | 버튼(씬 마감 비트) | every scene at risk of trailing off | one decisive final beat per scene | final ~1s = a visibly DIFFERENT beat (held reaction, small new action), then hard cut | comedy variant "blow/topper" — comedic escalation only |
| obligatory scene | 필수 장면 | genre audit | the scene the premise PROMISED | confirm the storyboard contains it explicitly | Archer's 5 classes [v] |
| non-repetition | 비반복 원칙 | full-board review | no two consecutive scenes turn the same way at the same magnitude | list value shifts in order; flag adjacent duplicates | — |

### Character & theme

| Term | KR | Use when | Effect | Artifact instruction | Caveat |
|---|---|---|---|---|---|
| want vs need | 원트/니드 | any protagonist beyond a goal-chaser | the gap between them makes the climax EARNED | brief: want (external, stated early) + need (internal, resolved at finale) | — |
| positive change arc | 포지티브 아크 | transformation brand films, before/after | visible internal change | opening_image = living the Lie; final_image = same framing, living the Truth | high expressive delta stresses character consistency hardest |
| flat arc | 플랫 아크 | founder story, expert testimonial — brand as mentor | authority/stability; the WORLD changes | protagonist's stated belief invariant start-to-end | cheapest/safest arc for AI pipelines (low expressive delta) |
| negative arc | 네거티브 아크 | cautionary/PSA, villain origin | warning/catharsis | final_image mirrors opening but WORSE — confirm intentional | disillusionment / fall / corruption variants [v] |
| antagonism principle | 대립의 원칙 | diagnosing a flat scene | a story's power is capped by what opposes it | strengthen the OBSTACLE before rewriting the hero | — |
| cast orchestration | 캐릭터 오케스트레이션 | 2+ characters | each supporting character embodies a distinct stance toward the theme | character sheet: protagonist=value A, foil=−A, skeptic=A-wrong-reason, mentor=A-earned | — |
| controlling idea | 컨트롤링 아이디어 | before any brief | one sentence: VALUE + CAUSE | "[value] prevails/fails because of [cause]" — every craft choice checked against it | — |
| image system | 이미지 시스템 | pieces ≥60s / ≥3 scenes | subconscious cohesion through a recurring motif | assign one motif, transformed at clips ~1/mid/final | must be a NAMED, repeated token per clip — motifs do not emerge across independent prompts |
| archplot / miniplot / antiplot | 아크/미니/안티플롯 | calibrating design mode | closed-causal vs internal-open vs anti-causal | CTA-driven ads default ARCHPLOT | miniplot/antiplot ambiguity in AI short-form reads as generation failure, not art |

### Logline & commercial frameworks

| Term | KR | Use when | Artifact instruction | Caveat |
|---|---|---|---|---|
| logline formula | 로그라인 공식 | first artifact of the brief | "when [catalyst], a [specific protagonist] must [goal] or else [stakes], against [obstacle]" — 3 load-bearing elements min, 5 strong [v] | unpitchable-in-one-breath = unfocused brief |
| high vs low concept | 하이/로우 콘셉트 | budgeting craft attention | high = premise carries; low = execution carries → extra character/tone pass | — |
| storybrand SB7 | 스토리브랜드 SB7 | every branded piece | the CUSTOMER is the hero; the brand is the GUIDE with a plan | guide_check: does the brand mentor rather than star? [v] |
| AIDA | AIDA 모델 | direct-response spots | map clip ranges to Attention/Interest/Desire/Action; flag empty stages [v] | — |
| PAS | 문제-자극-해결 | pain-point-led products | problem → intensify → solution | — |
| hook-retain-reward | 훅-리텐션-리워드 | algorithmic short-form distribution | hook 0–3s · pattern interrupt every 3–5s (owner: editing-grammar.md §4) · reward/CTA [v] | a DISTRIBUTION envelope layered OVER a story structure, never a replacement — alone it produces engagement without meaning |
| documentary modes (Nichols) | 다큐 6모드 | testimonial/UGC-style authenticity | pick ONE dominant mode (expository/observational/participatory/reflexive/performative/poetic) | mixed signals (VO argument over fly-on-wall footage) read untrustworthy [v] |
| commercial archetypes | 광고 원형 | format selection | problem-solution · testimonial · day-in-the-life (kishotenketsu) · hero product · founder story (flat arc) · before-after (mirror images) | — |

## 2. DOCTRINE

1. **Structure is chosen, not defaulted.** Match the structure to the goal (table below); a CTA ad on kishotenketsu or a mood film on AIDA are both category errors.
2. **The beat map is a contract with percentages, but the hook is a clamp:** hook = min(11%, **3s absolute**) — the 3s number is a FORMAT/RETENTION rule (format-director's namespace), not dramaturgy. Percentages govern only the beats after the hook.
3. **Below ~20 seconds you are not compressing three acts — you are using a different form:** `setup / turn / payoff` (mapped onto the hook / catalyst / final_image skeleton — no new enum values).
4. **Every scene turns; consecutive turns escalate.** value_shift is the unit; polarity progression is the chain rule.
5. **Every beat maps to at least one shot, and every shot serves a beat** (orphan-beat check — planning fiction is caught at validation, not at the edit).
6. **Suspense-forward by default.** Give the audience the bomb under the table; spend surprise only on the final clip.
7. **The iceberg is written into the prompt.** Show 1/8 on screen; write the 7/8 into the generation instruction — the model cannot imagine what it is not told.
8. **Kuleshov is doctrine, not data.** Juxtaposition manufactures meaning (the foundational principle of assembly) — taught as doctrine; the original experiment's footage is lost and replications are mixed. Sequencing is how independently generated clips acquire narrative meaning at all.

## 3. DECISION TABLES

**Goal/tone → structure**

| Goal | Structure | Why |
|---|---|---|
| Direct-response ad, clear CTA | three_act + AIDA envelope | clean gates, funnel-tested |
| Character/brand transformation | STC beats + positive change arc | visible before/after |
| Mood/brand-world, no antagonist | kishotenketsu | contrast without manufactured conflict |
| Founder/expert authority | flat arc + participatory doc mode | stable truth-holder |
| Episodic/serial | story_circle | ~1 step per clip at 45–75s |
| Multi-scene ≥90s | sequence_method scene grouping | legible mini-arcs (capacity: at ~90s ≈2 clips/scene at 5–6s; the full 8-scene × 3–4-clip form needs 160s+) |
| Testimonial/UGC | SB7 + observational/participatory mode | customer-as-hero |
| Cautionary | negative arc or PAS | warning register |

**Beat timing by duration (hook clamped ≤3s absolute)**

| Beat | 15s* | 30s | 60s | 90s | 120s |
|---|---|---|---|---|---|
| hook/catalyst | 2s | 3s | 3s | 3s | 3s |
| break_into_two (22%) | 3s | 7s | 13s | 20s | 26s |
| midpoint (50%) | 8s | 15s | 30s | 45s | 60s |
| all_is_lost (68%) | 10s | 20s | 41s | 61s | 82s |
| break_into_three (77%) | 12s | 23s | 46s | 69s | 92s |
| final_image | 15s | 30s | 60s | 90s | 120s |

*15s column shown for arithmetic only — <20s pieces use the 3-beat form, NOT this 5+-beat breakdown.

Tiers: **<20s → setup/turn/payoff (3-beat)** · 20–45s → 5-beat (drop all_is_lost, break_into_three) · ≥45s → full 7-tentpole · ≥90s → layer debate + uncoded STC beats.

**Genre → obligatory scenes**

| Genre | Obligatory | Convention | AI note |
|---|---|---|---|
| Horror | delayed reveal, final confrontation | false/ambiguous victory; silence-then-spike | held-frame silence is cheap and effective; anchor ambiguity with ONE deliberate cue or it reads as a glitch |
| Thriller | unmasking, midpoint reversal | ticking clock, red herring | on-screen timer graphics read clearly |
| Romance | meet-cute, black moment, grand gesture | the gesture's SPECIFICITY (not scale) earns it [v] | — |
| Comedy | callback/topper in the finale | rule of three | the three beats need near-identical framing to register as a pattern |
| Noir | confession, ambiguous ending | VO confession, no clean resolution | avoid a tidy final mirror |
| Action | hero's low point, escalating set-pieces | visible damage, ticking clock | escalation must be visually legible shot-to-shot |
| Branded-doc | talking-head + verité B-roll | ONE Nichols mode | — |

**Exposition → AI risk**

| Technique | When | AI risk |
|---|---|---|
| Iceberg image | emotional beats default | over-specify the prompt, under-specify the screen |
| Conflict-borne exposition | backstory mid-scene | needs two characters visibly disagreeing |
| On-screen text | short-form, sound-off | the cheapest reliable channel — use liberally (burned in post, never baked) |
| Cold open | hook-critical openings | caption anchor required |
| VO narration | expository doc mode only | don't mix over observational footage |

## 4. NUMERIC ANCHORS

- STC map (% of runtime) [v]: opening_image 1 · theme_stated 5 · catalyst 11 · debate 11–22 · break_into_two 22 · b_story 27 · fun_and_games 27–50 · midpoint 50 · bad_guys_close_in 50–68 · all_is_lost 68 · dark_night 68–77 · break_into_three 77 · finale 77–100 · final_image 100 (percentages authoritative over page counts)
- Field: PP1 ~25% · midpoint 50% · PP2 ~75% · pinches 37.5/62.5% [v] · Harmon: 8 × ~12.5% [v] · Vogler 12 (Campbell 17 = origin citation) [v]
- Hitchcock bomb: surprise ≈15s vs suspense ≈15min [v] · iceberg 7/8:1/8 [v] · SB7 = 7 elements, 3 problem levels [v] · AIDA 1898/1925 [v] · Archer 5 classes [v]
- Retention [v, POST-2023, vendor-analytics sourced]: intro-retention (past 3s) target ≥70% — strong hooks hold 80–90% through the first 3s; healthy view-rate 70–90%; pattern interrupt every 3–5s (owner: editing-grammar); >60% mobile sound-off
- 30s spot: hook 0–5s (core hook ≤3s) · message 5–20s · CTA 20–30s spoken+on-screen (word budgets live in sound-music.md — KR budgets in SYLLABLES)

## 5. ALIASES & DO-NOT-CONFUSE

| Canonical | Aliases |
|---|---|
| catalyst | inciting incident (Field/McKee), call to adventure (Vogler), disturbance — ONE label per project |
| break_into_two | plot point 1 (positional), commitment, threshold crossing |
| setup/turn/payoff (<20s) | hook/turn/payoff, 3-beat |
| montage_sequence | montage (US industry sense — see editing-grammar.md) |
| button | blow, topper, tag, capper (comedy-only variants) |
| dark_night | dark night of the soul |

**Do not confuse:** catalyst (world event) vs break_into_two (protagonist's decision) — two slots, never a third · all_is_lost (the loss) vs dark_night (the aftermath) · turning point (causal: revelation+decision+action) vs plot point (positional) — use the mechanism to justify the placement · flat arc (stated belief invariant) vs "no arc" (the WORLD must still change) · hook-retain-reward (distribution envelope) vs story structure (meaning) · kishotenketsu 転 (recontextualization) vs a plot twist (contradiction).

## 6. AI-GEN CAVEATS

- **Cross-clip memory does not exist** — plants/payoffs/motifs are LINKED FIELDS with the exact visual token repeated verbatim in both prompts.
- **Macro-structures don't survive 1:1 compression** — select 4–8 load-bearing beats; a beat without screen time is planning fiction (orphan check).
- **High-delta arcs stress identity consistency hardest** — flat arc is the cheap default; reserve change arcs for locked reference banks.
- **Dramatic irony requires an explicit two-shot split**; a single clip cannot know two things at once.
- **Twists are expensive, suspense is cheap** — structure the knowledge, not the shock.
- **Micro-performance beats (grand gesture, low point) render generically** — compensate with tighter framing + a playable action + sound design + cut rhythm, never with "more emotion" adjectives.
- **Ambiguity reads as error** in generated output — every intended ambiguity needs one unambiguous authored cue.
