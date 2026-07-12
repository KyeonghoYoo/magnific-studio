# Sound & Music

**Read this when:** audio design at /ms-post (music cues, SFX, VO); music-gen prompts; TTS direction.

Scope note: clips arrive audio-stripped (no production sound). The pipeline builds every mix from TTS VO + generated music + stock SFX/ambience, combined in ffmpeg with sidechain ducking and 2-pass loudnorm. **This file does not restate mixing numbers** (ducking dB, LUFS targets, dBTP ceiling) — those are owned by the mixing/ffmpeg pipeline. This file owns the craft vocabulary, the schema contract, and the QA/caveats layered on top of that mix.

## 1. Canonical Terms

### 1.1 Taxonomy & Diegesis

| Term | KR | Use when | Effect | Pipeline instruction | QA (+Caveat) |
|---|---|---|---|---|---|
| Production/Sync Dialogue & ADR | 동시녹음·후시녹음 | N/A (capture) / re-voicing an existing line (ADR) | n/a — no native source | Fully replaced by TTS; ADR-equivalent = regenerate + re-align the TTS line — no lip-synced source exists to conform to | Flag scripts that assume production-sound texture (overlaps, interruptions) — TTS cannot produce it |
| Walla | 월라(군중 잡담음) | Populated background (crowd, café, street) | Absence in a crowd scene reads uncanny/artificial | No native source: music-gen "murmuring crowd bed, indistinct overlapping voices, speech unintelligible" — positive reframe; the negation lint covers ALL generation prompts including music-gen (shares the ducking channel) OR stock_search | §6.1 |
| Room Tone | 룸톤 | Under every TTS pause, across every cut | Prevents a pause/cut from reading as a dropout | Substitute a near-silent low-level texture bed (never true digital zero) under pauses | Do-not-confuse w/ Ambience (§5) |
| Foley (Footsteps, Cloth & Props) | 폴리(풋스텝·의상·소품음) | Every hero-walk, every prop-handling shot | Absence = weightless, floaty movement (the "weightlessness tell") | stock_search/stock_download timed to the cut — NOT generative | Delivery-gate floor item (D6) |
| Hard Effects (Hard FX) | 하드 이펙트 | Every visible on-screen impact (door slam, glass break) | Visible impact + no hard FX reads as a rendering error | stock_search/stock_download, placed at the exact cut frame in edit_plan | Delivery-gate floor item (D6); validator: visible impact ∧ no sfx[] entry ⟹ QC FAIL |
| Designed Sound & Sound Motif | 디자인 사운드와 사운드 모티프 | Creature vocals, sci-fi tech, non-realistic SFX | Sonic identity for the never-before-seen; reused verbatim = a non-musical leitmotif | Music-gen "texture" prompt as a short one-shot stem — generate ONCE, reuse verbatim via ffmpeg | Do-not-confuse w/ musical Leitmotif (§5) |
| BG / Ambience | 앰비언스 | Every populated or exterior scene | Total silence reads as a mix error; a BG shift implies time passing | Texture inside the music-gen prompt, or stock_search; one ambience[] bed per location | Delivery-gate floor item (D6) |
| Diegetic Sound | 다이제틱 사운드 | Sound the characters themselves can hear | — | A labeling decision in edit_plan (perspective/duck treatment), not a generation parameter | — |
| Non-Diegetic Sound | 논다이제틱 사운드 | Score, narrator VO — audience-only | — | Default treatment for our music bed + VO: no perspective/reverb matching required | Contrast w/ Trans-Diegetic below |
| Trans-Diegetic Music (`diegesis: trans_diegetic`) | 경계횡단 음악 | Source music (radio, in-room speaker) escalating to full underscore, or the reverse | Near-invisible emotional escalation — the audience already hears the source | **The two-stem crossfade technique**: generate a lo-fi/filtered "source-quality" stem + a full-score stem of the SAME material, crossfade in ffmpeg | Schema value on music_cues[].diegesis (D1) |

### 1.2 Perspective & Bridges

| Term | KR | Use when | Effect | Pipeline instruction | QA (+Caveat) |
|---|---|---|---|---|---|
| Off-Screen Sound | 화면 밖 소리 | Any frame-limited clip that needs to imply scale | Expands the perceived world at ZERO visual cost — the cheapest production value available | Cue off-screen texture/voice to imply what the clip can't afford to show | Highest-value single craft move in this pipeline |
| Acousmatic Sound & De-Acousmatization | 아쿠스마틱 사운드와 음원 노출 | A sound source withheld then revealed (Chion) | The reveal functions as a dramatic pivot | Hold a sound acousmatic across N shots in edit_plan; cut the reveal precisely on its clearest instance | Authored device, not an accident |
| Point of Audition (POA) | 청취 시점 | Deciding whose "ears" the mix represents | Perceptual (filtered/subjective) vs. spatial POA change what the audience trusts | Drives whether a filter chain applies to the full mix or a single track | — |
| Sound Perspective & Perspective Shift | 음향 원근감 | Every cut that changes shot scale | Mismatch (CU sound on a wide shot) reads as subtle "wrongness" before it's named | Generated stems arrive DRY regardless of shot size — impose shot-matched EQ/short reverb per cut in ffmpeg (CU=intimate/dry, wide=roomy/distant) | §6.8 |
| Pre-Lap / J-Cut (incoming audio leads the picture cut) | 프리랩(J컷) | Next scene should arrive with forward momentum | Anticipation | Authored by CUE PLACEMENT, not a named field: set the incoming element's in-point earlier than the cut timestamp (`music_cues[].in` / `sfx[].at_sec`; VO pre-lap: set `voiceover.start_sec` earlier than the cut — IMPLEMENTED, the renderer places the VO on the master timeline via adelay and sidechain-ducks the music+ambience bed under it, SFX excluded) | J-cut is a GLOSSED ALIAS only (§5) — there is no `audio_in_offset_ms`-style field |
| Post-Lap / L-Cut (outgoing audio trails the picture cut) | 포스트랩(L컷) | A beat should resolve over the NEXT image | Reflective, trailing | Authored by CUE PLACEMENT: extend the outgoing element's out-point past the cut timestamp (`music_cues[].out`; VO trail: the VO simply continues past the cut from its `start_sec` placement — no out-point field needed) | L-cut is a GLOSSED ALIAS only (§5); most-reversed pair in practice |
| Sound Match Cut | 사운드 매치컷 | A hard visual cut needs sonic connective tissue | Bridges two unrelated images (scream → train whistle) | Search task: select/trim music or TTS moments whose pitch/timbre pre-match on both sides of the cut | — |
| Audio Dissolve | 오디오 디졸브 | Any audio-to-audio crossfade | Smooths a transition between two audio sources | ffmpeg — crossfade duration + curve per transition | Audio-only op — do not confuse with the video `dissolve` transition value |

### 1.3 Silence & Dynamics

| Term | KR | Use when | Effect | Pipeline instruction | QA (+Caveat) |
|---|---|---|---|---|---|
| Dropout / Silence Before Impact | 드롭아웃(임팩트 전 무음) | Immediately before any major hit/reveal | The return reads louder than its actual level, purely from contrast | Scheduled ~200–500ms gain-to-near-zero on ambience/music just before the hit frame (§4) | Sequenced BEFORE Hole Punch, not interchangeable with it (§5) |
| Hole Punch | 홀 펀치 | The hit frame itself | One sound cuts through cleanly | Targeted short duck of ALL non-hero tracks at the timestamp — beyond the standing sidechain (MANUAL mix op, see D6 — no schema field) | Distinct op from the standing sidechain duck (already in the mix pipeline) |
| Dynamic Range as Drama | 다이내믹 레인지 | Whole-mix craft pass, pre-delivery | Preserves the quiet-loud gap so loud reads loud — a mix can pass loudnorm and still feel flat | Not a generation parameter — a craft QA pass | QA metric = LRA, EBU R128 standard (D9) — WARN <4 LU, provisional, gated to cinematic_short/longform/brand only (§4) |
| Muffle / Underwater / Tinnitus POV | 먹먹함·수중·이명 주관음향 | Concussive events, submersion, panic-narrowing | Simulates impaired hearing subjectively | ffmpeg low-pass filter (+ optional sine tone) for a duration, then a deliberate un-filter return | — |
| Heartbeat / Breath Interiority | 심장박동·호흡 내면음향 | Anxiety, fear, exertion conveyed from inside a character | One of the most reliable tension tools — the body syncs to a heard heartbeat | Stock/designed one-shot loop, tempo-ramped across the scene | — |
| Sound Distortion for Psychology | 심리적 음향 왜곡 | Altered mental state | Pitch-shift/granular smear/warp signals derangement | ffmpeg filters on designated tracks, scoped to a shot range | — |

### 1.4 Music Dramaturgy

| Term | KR | Use when | Effect | Pipeline instruction | QA (+Caveat) |
|---|---|---|---|---|---|
| Score vs. Source Music vs. Soundtrack | 스코어·소스뮤직·사운드트랙 구분 | Tagging every music cue | score=original non-diegetic; source=diegetic in-world; soundtrack=the WHOLE audio program (not a cue) | REQUIRED tag on every music_cues[] entry via `diegesis` (D1) | "soundtrack" is NOT a schema value — §5 |
| Underscore | 언더스코어 | Music under dialogue, subordinate level | Audiences often can't recall it played — intended | Prompt "sparse, supportive, low melodic activity, built to sit under dialogue" | Dense underscore fights the sidechain duck already in the mix |
| Emotional Amplification Scoring | 감정증폭형 스코어링 | Default/classical scoring choice | Music mirrors and intensifies the emotion already on screen | Mood-word prompting maps directly and reliably here (§3.B) | Lowest AI-gen risk of the music modes |
| Counterpoint & Anempathetic Music | 대위법적·무감정 음악 | Music should contrast the image | Unease, irony, Brechtian distance | Over-specify near-contradictory prompts ("cheerful children's music... playing under a violent scene, intentionally jarring") | §6.4; anempathetic (indifferent, Chion) ≠ ironic (registered contrast) — §5 |
| Leitmotif & Theme-Variation | 라이트모티프와 주제 변주 | A character/place/idea recurs across the cut | Hearing the theme = hearing the character, even off-screen | **SAME-STEM LAW (D4)**: render the base theme ONCE; every recurrence transforms that SAME stem via music_cues[].derived_from + .transform{pitch_semitones, tempo_ratio} | Re-prompting a recurring theme = schema violation, not a leitmotif; §6.2 |
| Mickey-Mousing | 미키마우징 | Comedy/animation/children's content ONLY | Literal hit-for-hit sync reads as craft there; in drama it reads cheap | Genre-gated — see §3.A | NOT `beat_locked_cutting` — §5 do-not-confuse |
| Needle Drop | 니들 드롭 | Wanting a recognizable pre-existing song | Imports cultural associations instantly | Out of scope for generation — approximate the FEELING (genre/era/instrumentation), never artist/title | §6.7 — copyright exposure |
| Music Spotting Doctrine, Wall-to-Wall & Cue Structure | 스포팅 원칙·전곡 도배·큐 구조 | Planning every music placement, before generation | Judicious spotting makes entrances felt as choices; wall-to-wall exhausts and devalues | Required step: each cue = named `cue_id` (M1, M2…) + in/out + one-line "why" (D1, D3) | WARN only when ≥95% timeline AND format ∈ {cinematic_short, longform}; CORRECT (no warning) for 15–60s music-led shorts_reels |

### 1.5 Trailer & Short-Form Grammar

| Term | KR | Use when | Effect | Pipeline instruction | QA (+Caveat) |
|---|---|---|---|---|---|
| Hit Point / Sync Point | 히트포인트 | A moment where music/SFX must precisely align with action | Clean hit reads masterful; a near-miss reads sloppier than no hit at all | librosa auto-alignment solves this mechanically | §6.3 — confirm the drop lands on the NARRATIVE turn, not just the loudest bar |
| Stinger | 스팅어 | One dramatic beat needs a sharp accent | Punctuates a single moment | <1s one-shot music-gen or stock hit on the hit-point frame, independent of the music-bed cue | Object at a timestamp — not the timestamp itself (do-not-confuse w/ Hit Point) |
| Riser & Whoosh | 라이저와 후시 | Building to a hit / crossing a transition | Riser = anticipation swell; whoosh = transient swipe | Riser = ascending stem ending exactly on the cut frame; whoosh = <500ms transient on the cut | — |
| Braam | 브람 | Trailer/hook cuts needing maximum weight | Sustained deep distorted brass hit (Inception-era trailer language) | Prompt: "deep sustained brass hit, distorted low end, trailer braam, cinematic impact" | Reserve for trailer/hook cuts — overuse flattens impact |
| Build-Drop Structure & Tempo–Cutting-Rhythm Interaction | 빌드-드롭과 템포-편집 리듬 | Any hook-driven short/trailer edit | Rising tension resolving into release; on-beat cutting=propulsive, off-beat=anxious | Choose music-gen BPM as a clean multiple/fraction of the intended cut rate BEFORE generation | Same failure mode as §6.3 — confirm RMS-detected drop = narrative turn |

### 1.6 VO Craft

| Term | KR | Use when | Effect | Pipeline instruction | QA (+Caveat) |
|---|---|---|---|---|---|
| VO Mode — narration / internal_monologue / character_sync | 내레이션·내적독백·캐릭터 동기화 | Tagging every VO track (`audio.voiceover.mode`) | narration=connective tissue; internal_monologue=canonical house term for Bordwell & Thompson's "internal diegetic sound" (audible to audience AND the narrating character only); character_sync=performance/lip-matched | internal_monologue treatment: non-diegetic ducking + close/dry perspective (D8) | Do not substitute "metadiegetic" or other literature terms in schema (§5) |
| VO Read Styles: Documentary / Commercial / Intimate | 낭독 스타일 | Selecting voice + delivery, per project or per beat | Read style alone resets audience expectations before a single fact lands | TTS voice-selection + prosody per style — apply per-sentence/per-beat, not globally | §6.6 |
| Pacing (Words-Per-Minute) | 낭독 속도 | Before every TTS generation call | Overruns force rush-cutting or truncated VO | Check word/syllable count against budgets BEFORE TTS generation — BLOCKING (D10) | Budgets in §4 |
| Writing for the Ear | 귀로 듣는 글쓰기 | Drafting any VO/narration script | Short sentences, one idea each, concrete verbs — avoids stacked clauses and homophone ambiguity | Pre-generation script QA pass; flag long subordinate clauses; front-load key information | — |
| Pause as Punctuation | 침묵의 구두점화 | Structuring pauses inside a VO script | Silence reads as structure, not dead air, when tagged deliberately | Explicit break/pause tags per taxonomy (§4) — don't rely on the model's uniform default pause | Per-sentence TTS calls ≥3 sentences (D10) |

## 2. Doctrine

**D1. Music cue schema (binding).** Every music placement is a named entry in `audio.music_cues[]`:
```
{ cue_id: "M1"|"M2"…, source, in, out,
  diegesis: score | source | trans_diegetic,
  provenance: generated | licensed   (licensed ⟹ license field REQUIRED — empty license = delivery BLOCK),
  gain_db, why (spotting rationale, one line),
  derived_from?: cue_id, transform?: { pitch_semitones, tempo_ratio } }
```
`derived_from` + `transform` are how a leitmotif recurrence is expressed in-schema — see D4. This is the ONLY place a music placement is recorded; there is no separate "soundtrack" object (D2).

**D2. "soundtrack" is not a schema value.** It names the whole audio program (the album concept), not a cue — never author it into `diegesis` or any enum. See §5.

**D3. Spotting is mandatory; wall-to-wall is a WARN, not a ban — and only for some formats.** Every cue needs in/out + a one-line "why" (the spotting rationale). A single cue covering ≥95% of the timeline triggers WARN, but ONLY when format ∈ {cinematic_short, longform}. For 15–60s music-led shorts/reels, wall-to-wall coverage is the CORRECT choice — do not raise the WARN there.

**D4. Leitmotif same-stem law (binding).** A recurring theme is rendered ONCE. Every later appearance transforms that SAME rendered stem — pitch-shift, tempo-change, re-instrumentation — while preserving the interval contour, expressed via `derived_from` + `transform`. Re-prompting a recurring theme from scratch is, by definition, not a leitmotif: it is a schema violation, because text-to-music generation has no memory across calls (§6.2) and will not reproduce the same melodic material twice.

**D5. Beat-sync doctrine (revises v0.3 "snap cuts to beat").** Cut on PICTURE — action, look, or sound event drives the cut point. Sync to the music beat ONLY the tentpoles, ≤3 per piece: hook, turn, CTA/final. Global beat-snap (`audio.beat_snap.mode: snap`) survives only for comedy/hype/montage; cinematic/brand/longform default to `mode: offset` (60–150ms off the nearest beat, §4) or `mode: off`. QC measures median |cut − beat|: <30ms on a non-comedic profile raises flag **`beat_locked_cutting`** — this is NOT mickey-mousing (§5). Principled reason for the ban: a beat grid driving cuts inverts Murch's Rule of Six, where rhythm is the LEAST-weighted editing priority (10%) and emotion the most (51%) — letting the least important criterion set the cut point is backwards.

**D6. Delivery gate — no music-only mix when picture shows physical events (BLOCKING).** A deliverable may not ship a music-only audio track when the picture contains visible impacts or a hero walking (the "weightlessness tell," §1.1). Floor requirement: one `ambience[]` bed per location + footsteps (`sfx[]`) on every hero-walk shot + a hard-FX `sfx[]` entry on every visible impact — all stock-sourced, gaps DECLARED in edit_plan, never silently omitted.
```
audio.sfx[]:      { id, shot_id, source, at_sec, gain_db }
audio.ambience[]: { source, in, out, gain_db }
```
Hole-punch ducks (§1.3) are a MANUAL mix op — sidechain/volume automation recorded in edit_plan notes; there is no per-SFX duck field.
Validator: `shot.sound[]` non-empty ∧ no matching edit_plan destination ⟹ QC FAIL.

**D7. J/L-cuts are authored by CUE PLACEMENT; there are no signed-offset fields.** A pre-lap (J-cut) is expressed by setting the incoming element's in-point earlier than the picture-cut timestamp (`music_cues[].in` / `sfx[].at_sec`; VO pre-lap: set `voiceover.start_sec` earlier than the cut — IMPLEMENTED, the renderer places the VO on the master timeline via adelay and sidechain-ducks the music+ambience bed under it, SFX excluded); a post-lap (L-cut) by extending the outgoing element's out-point past the cut (`music_cues[].out`; VO trail: the VO simply continues past the cut from its `start_sec` placement — no out-point field needed). J-cut/L-cut exist only as glossed aliases in prose/UI (§5) — they are the most-reversed pair in practice, and explicit cue timestamps can't be misread the way letter-names can. Fields like `audio_in_offset_ms`/`audio_out_offset_ms` do NOT exist in edit_plan — never cite them.

**D8. VO mode is a 3-value enum; internal_monologue is the house term.** `audio.voiceover.mode` ∈ `{narration, internal_monologue, character_sync}` (default `narration`). Do not substitute "metadiegetic" (Gorbman) or other literature terms in schema or prompts — gloss them, don't author them (§5).

**D9. Dynamics QA uses LRA, never an invented metric.** Measure Loudness Range (LRA, the EBU R128 standard metric) as the dynamics-as-drama check. WARN below 4 LU — provisional threshold pending calibration on two productions — gated to `cinematic_short/longform/brand` only, never `shorts_reels` (tight, consistent loudness is the correct target there). Ducking depth and integrated-loudness/dBTP targets for the mix itself belong to the ffmpeg sidechain-ducking + 2-pass loudnorm pipeline — not restated here.

**D10. VO budgets gate generation; captions budget separately.** Pre-TTS budget check is BLOCKING — script word/syllable count is checked against the duration budget (§4) BEFORE any TTS call. VO is budgeted in words (EN) or syllables (KR, provisional); captions are budgeted in CHARACTERS — a distinct count, since a script that fits the VO time budget can still overflow a caption line (character table in §4 — never borrow the VO wpm/syllable numbers for caption timing). TTS calls are issued per-sentence (≥3 sentences split individually) so rate/pitch/emphasis can vary; a single global TTS call flattens performance (§6.6).

## 3. Decision Tables

### 3.A Scene Intent → Sound/Music Treatment

| Intent | Sound Move | Music Move | Craft Note |
|---|---|---|---|
| Suspense build | Strip BG, low drone under | Slow riser, sparse→dense | Hold silence before the hit |
| Sudden impact | Dropout 200–500ms pre-impact, hard transient | Stinger/braam on-frame, post-hit silence | Hole-punch the mix |
| Emotional reveal | Ambience thins 1–2s before the line | Music enters AFTER the key line, then swells | Music = confirmation, not anticipation |
| Comedic beat | Tight exaggerated synced hits | Mickey-Mousing permitted | The one genre where literal sync = craft |
| Transition/montage | Crossfade beds, whoosh on cut | Tempo ramps to cut rate, motif fragments | Leitmotif fragments carry continuity |
| Intimate/vulnerable | Close perspective, audible breath | Sparse solo instrument, restraint | Silence can carry more weight |
| World-building | Layered BG + off-screen cues | Source music if location implies | Off-screen sound cheaply extends the world |
| Tragic irony | Ambience continues unaffected | Anempathetic/counterpoint | High-risk — needs narrative justification |
| Documentary/informational | Minimal ambience, dialogue-forward, room tone under pauses | Subtle underscore, never wall-to-wall | VO leads absolutely |
| Trailer/short-form hook | Riser/whoosh/braam on hard cuts | Build-drop synced to the hook cut | Fast pacing licenses excess |

### 3.B Key/Mode/Instrumentation → Mood (music-gen prompts)

| Key/Mode | Instrumentation | Mood | Prompt Phrase |
|---|---|---|---|
| Major diatonic | Strings + piano, open voicings | Warm, hopeful | "warm major-key orchestral, open string voicings, hopeful and resolved" |
| Natural minor | Low strings, sparse piano | Melancholic | "somber natural minor, sparse piano and low strings, reflective" |
| Dorian/modal | Woodwinds, folk | Bittersweet | "modal dorian folk-tinged score, woodwinds, bittersweet warmth" |
| Phrygian/harmonic minor | Tremolo strings, modal instruments | Exotic tension, dread | "harmonic-minor tension, tremolo strings, dread and unease" |
| Lydian | Bright synths, celesta | Wonder, whimsy | "lydian mode, bright synth and celesta, sense of wonder" |
| Whole-tone/atonal | Prepared piano, clusters | Disorientation, uncanny | "atonal whole-tone clusters, prepared piano, dreamlike and uncanny" |
| Minor ostinato | Pulsing strings/synth bass, percussion | Mounting urgency | "relentless minor ostinato, pulsing low strings, driving percussion" |
| Pentatonic major | Plucked harp/guitar | Innocence, nostalgia | "pentatonic major, plucked harp and acoustic guitar, nostalgic" |
| Chromatic descending | Brass, low piano | Doom, inevitability | "chromatic descending brass and piano, sense of doom" |
| Sparse/silence-forward | Solo or none | Intimacy, grief | "solo piano, unaccompanied, extremely sparse, room to breathe" |

## 4. Numeric Anchors ([v])

Mixing-stage numbers (ducking depth in dB, integrated LUFS targets, dBTP ceiling, platform loudness tiers) are already encoded in the ffmpeg sidechain-ducking + 2-pass loudnorm pipeline — deliberately not restated here.

- **VO pacing [v]:** 160–180 wpm commercial norm (~180 = ad-engagement optimum); word budgets :15≈30–40w · :30≈60–80w · :60≈150w; shave 5–10% for breath room — write to ~90% of budget, not 100%.
- **KR VO budgets, in SYLLABLES [v, PROVISIONAL — replace with measured per-voice constants]:** VO narration is READING speech, not conversation — Seoul Korean corpora measure reading articulation ≈3.3–3.5 syl/s vs conversational ≈5.0–5.2 syl/s; commercial VO runs slightly above lab reading → house band 3.5–4.5 syl/s × the same ~90% breath shave → **:15≈48–60음절 · :30≈95–120음절 · :60≈190–240음절**. Calibration roadmap (zero-cost, replaces the literature number): render ONE calibration sentence per voice via TTS, `ffprobe` duration ÷ syllable count = that voice's syl/s constant.
- **Pause taxonomy [v]:** comma-beat ≈0.3s · paragraph ≈1s · section ≈2s (convention, house styles vary) · dialogue-line ≈650–900ms · ≈120ms practical floor — below this a gap reads as a glitch, not a pause.
- **Dropout/hole-punch timing [v]:** ~200–500ms gain-to-near-zero, scheduled immediately before the hit frame.
- **Beat-snap offset tolerance [v]:** 60–150ms off the nearest beat, for `audio.beat_snap.mode: offset` on non-comedic genres.
- **Dynamics QA [v, PROVISIONAL — calibrate on first two productions]:** LRA WARN threshold <4 LU, gated to `cinematic_short/longform/brand` (never `shorts_reels`).
- **Caption character budgets [v — Netflix TTSG primary-fetched]** — DISTINCT from VO word/syllable budgets above: captions are READ, not spoken, so the ceiling is reading speed (CPS), not speech rate. Caption capacity deliberately exceeds VO pace (readers outpace speech) — the gap between the KR VO syllable budget (:30≈95–120) and the KR caption budget (:30≈360 chars) is CORRECT, not a bug.
  - EN: 42 CPL · max 2 lines (84 chars/cue ceiling) · adult 20 CPS / children 17 CPS (pre-2020 sources still quote 17 adult — stale) · cue duration 5/6s min (20f@24) – 7s max · ≥2-frame gap.
  - KR: 16 CPL · max 2 lines (32 chars/cue ceiling; Latin/spaces/punctuation count 0.5 char) · adult 12 CPS / children 9 CPS · SDH +2 (14/11) · same duration bounds.
  - Per-duration TOTAL budget = duration_sec × CPS: EN :15≈300 · :30≈600 · :60≈1200 chars | KR :15≈180 · :30≈360 · :60≈720 chars. Per-cue ceiling is duration-independent (CPL×lines binds before the 7s cap).
  - Broadcast fallback (BBC/SUBTLE consensus, slower non-streaming context): 12–15 CPS avg / 16–17 max · 32–42 CPL [v, secondary]. Note: "EBU R37" is A/V-sync spec, NOT a subtitling doc — never cite it for reading speed.
  - Short-form/vertical & karaoke word-timing: [PROVISIONAL — no governing standard exists] cues run 1–2s; karaoke per-word reveal is a different display mode — the CPS/CPL budget model does not apply to it. Default to the table above for static-line captions.
  - KR broadcast (KCC) numeric standard: NOT LOCATED (source PDFs unextractable) — anchor KR policy on the Netflix KR figures; do not cite KCC numbers.

## 5. Aliases & Do-Not-Confuse

**Aliases (canonical ← alias):**

| Canonical (schema) | Alias(es) | Note |
|---|---|---|
| pre-lap = incoming cue in-point placed BEFORE the picture cut (`music_cues[].in` / `sfx[].at_sec`) | J-cut | Timeline-shape mnemonic: audio pokes out early/LEFT of the block, like the top of a **J** — leads the picture. Gloss only — authored as cue placement, never as a named offset field (D7) |
| post-lap = outgoing cue out-point extended PAST the picture cut (`music_cues[].out`) | L-cut | Timeline-shape mnemonic: audio pokes out late/RIGHT of the block, like the foot of an **L** — trails the picture. Most-reversed pair in practice (direction is easy to misremember; an explicit cue timestamp can't be) |
| `audio.voiceover.mode: internal_monologue` | "internal diegetic sound" (Bordwell & Thompson) | House-adopted gloss; the schema value is `internal_monologue` |
| `diegesis: trans_diegetic` | metadiegetic (Gorbman) · fantastical gap (Stilwell) · "diegetic-to-nondiegetic transition" (plain editorial term) | No literature consensus — house picks `trans_diegetic` and glosses the rest |

**Do-not-confuse:**

- **Score vs. Source vs. Soundtrack (사운드트랙=전체 오디오 프로그램)** — score=original non-diegetic composition; source=diegetic in-world music; soundtrack=the ENTIRE audio program (not a cue type, not an enum value — D2).
- **Mickey-Mousing vs. `beat_locked_cutting` (비트에 억지로 맞춰진 컷 — QC 플래그)** — mickey-mousing = the SCORE mimics on-screen action (valid, even desirable, in comedy/animation); `beat_locked_cutting` = CUTS chase a music beat grid (a principled craft violation in any non-comedic genre, regardless of intent — D5).
- **Anempathetic vs. Ironic (Chion)** — anempathetic = music indifferent/mechanically oblivious to the image (nursery tune under tragedy, no authorial wink); ironic = a REGISTERED, deliberate authorial contrast. Different prompt phrasing for each.
- **Leitmotif vs. Sound Motif** — leitmotif = a MUSICAL theme, transformed via pitch/tempo/instrumentation on the same stem (music_cues[] schema, D4); sound motif = a non-musical DESIGNED SOUND (creature vocal, tech hum) reused verbatim — no melodic transform, just verbatim reuse.
- **Hard FX vs. Foley** — Hard FX = a single event tied to a visible impact (door slam); Foley = continuous PERFORMED sound tied to a character's physical movement (footsteps, cloth, prop handling). Both stock-sourced; different placement logic (single `at_sec` hit vs. a continuous bed matched to gait).
- **Room Tone vs. Ambience/BG** — Room Tone = the near-silent SIGNATURE of a location, filling pauses without a true digital-zero dropout; Ambience/BG = a fuller, often designed environmental texture bed establishing atmosphere. Room tone is "the silence"; ambience is "the sound of the place."
- **Dropout vs. Hole Punch** — dropout = a brief near-total silence BEFORE a hit; hole punch = a targeted duck of non-hero tracks AT the hit (something still sounds — the hero hit). Sequenced together, not interchangeable (§1.3).
- **Audio Dissolve vs. video `dissolve`** — Audio Dissolve is an audio-only ffmpeg crossfade between two audio sources; the video `dissolve` is a distinct edit_plan transition value (see camera/editing references) — same word, different track, different schema field.

## 6. AI-Gen Caveats

**§6.1 No dedicated SFX/Foley/ambience generation stage.** Clip arrives audio-stripped; only TTS + music-gen are native. Workarounds: (a) fold texture into the music-gen prompt (competes with the sidechain duck); (b) stock_search/stock_download for SFX/ambience/Foley; (c) flag as an explicit gap in edit_plan — never silently omit.

**§6.2 Leitmotif continuity.** Text-to-music has no memory of prior generation calls. Render the theme ONCE; reuse/pitch-shift/time-stretch the SAME stem across cues (or melody-conditioning where the model supports it). Re-prompting breaks the same-stem law (D4).

**§6.3 Structure vs. spotting.** Models don't understand "swell at the reveal"; RMS/beat alignment can lock onto a structurally WRONG moment (loudest ≠ narratively correct). Generate looser stems and pick the drop window by narrative review, or prompt explicit section lengths ("8-bar build, then percussive drop").

**§6.4 On-the-nose bias.** Counterpoint/anempathetic prompting needs to be over-specified and near-contradictory, or the model corrects back toward emotional congruence with the image.

**§6.5 Accidental Mickey-Mousing from auto-alignment.** Beat/RMS-synced cuts risk landing every hard cut exactly on a musical hit, reading as unintentionally comedic in drama. Workaround: deliberate offset tolerance (60–150ms off the nearest beat) for non-comedic genres — see beat-sync doctrine (D5).

**§6.6 TTS direction is coarse.** A single global style flattens performance and under-renders non-verbals (breath, laugh). Split the script into per-sentence/per-beat TTS calls with varied rate/pitch/emphasis + explicit break tags.

**§6.7 Needle-drop copyright exposure.** Prompting by artist/song name risks reproducing a recognizable fingerprint. Prompt genre/era/mood/instrumentation only, never artist/title.

**§6.8 Flat dynamics, dry acoustics at generation.** Stems arrive internally loud/consistent and acoustically dry. Treat as raw material: gain-automation/gating for dynamics, shot-matched convolution reverb/EQ for perspective — both applied in ffmpeg, downstream of generation.
