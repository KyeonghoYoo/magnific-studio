---
name: filmcraft
description: |
  영화 제작 전 부서 기법 정본 사전(할리우드 실무+정전 이론+AI 프롬프트 번역). Use when: (1) 모든 /ms-* 스테이지 시작 시 해당 스테이지 레퍼런스를 읽을 때, (2) 카메라·조명·편집·사운드 어휘를 아티팩트에 쓸 때, (3) 생성 프롬프트를 작성/린트할 때. 산출물: 없음(참조 전용) — 통제 어휘의 정본.
---

# filmcraft — The Canonical Film-Craft Lexicon

Authoritative, adversarially-verified vocabulary for every production department, with each term carrying: definition → when to use → screen effect → **AI prompt translation** → QA check. Built from 12 department research passes + a 3-lens adversarial debate (film-scholarship purist / working practitioner / AI-pipeline engineer); rulings in `docs/RESEARCH-CRAFT.md`.

**Prime directive:** artifacts store canonical vocabulary (model-free); prompts are RENDERED from artifacts by the deterministic projection tables in `references/prompting.md`. Never hand-write what the projection owns.

## Stage routing — read before you work

| Stage | Read first | Also |
|---|---|---|
| /ms-plan | story-structure, emotion-recipes | production-design (world/costume), color-grading (palette/color script) |
| /ms-characters | production-design (costume/silhouette/props) | lenses-optics (portrait bands) |
| /ms-storyboard | shot-grammar, camera-movement, lighting, directing-mise-en-scene, emotion-recipes | editing-grammar (cut planning), story-structure (beat validation) |
| /ms-produce | **prompting (mandatory — projection + pre-flight lint)**, camera-movement, lighting | animation-motion (motion tokens), vfx-compositing (hybrid shots), lenses-optics, **model-matrix (dated — verify per campaign)** |
| /ms-post | editing-grammar, sound-music, color-grading | — |
| quality-reviewer | each file's QA column | prompting (lint list), animation-motion (motion flaw table) |

## File inventory (references/)

| File | Owns |
|---|---|
| story-structure.md | Structures (3-act, story circle, sequence method, kishotenketsu), beats & duration tiers, scene craft (value shift, setup/payoff, suspense-vs-surprise), arcs, loglines, commercial frameworks |
| shot-grammar.md | 8-rung size ladder (cut lines), 7 angles (geometric) + dutch_deg, framing vs function split, composition tags, screen direction + 180° axis fields, aspect grammar |
| camera-movement.md | Movement object (base/direction/speed/support), one-move law, dolly⇄zoom fork, foreground_anchor/parallax doctrine, camera_settle, risk register (green/amber/red) |
| lenses-optics.md | Focal bands (FF-equivalent), DoF grammar, lens character/filtration, film stocks (enum), exposure_bias, token efficacy |
| lighting.md | Scene lighting struct (the byte-identical contract), canonical ratio→proxy table, patterns, Kelvin/time-of-day, named looks, banned prompt terms |
| directing-mise-en-scene.md | Blocking/staging, continuity system (axis, legal crossings, 30°), eyeline/gaze_target, POV grammar, reveals, motif, playable-action performance doctrine |
| editing-grammar.md | Cut typology, transition semantics (soft_cut/dissolve/fades + renderer mapping), montage naming, rhythm (Pearlman/holds/pattern interrupt), trim doctrine, stitched-oner truth-labeling |
| color-grading.md | Prompt-color=mood vs ffmpeg=precision split, show LUT + scene trim, color scripts, harmony, looks, skin/memory colors, banding |
| sound-music.md | Diegesis (score/source/trans), music cues & spotting, leitmotif same-stem law, beat-snap doctrine, SFX/ambience delivery gate, VO craft (EN wpm / KR syllables) |
| vfx-compositing.md | Integration checklist (light/shadow/perspective/grain/edge/atmosphere), hybrid-shot seam doctrine, screen replacement, previz/techviz limits |
| animation-motion.md | 12 principles → AI flaw→fix→token table, moving_hold, impact_settle, gesture economy, silhouette readability, shutter look |
| production-design.md | Department ownership, world bible→reference banks, hero props/costume (locked refs), patina levels, palette pollution, greeking, pack shots |
| emotion-recipes.md | ~22 dramatic goals → coordinated cross-department recipe rows (size+angle+move+lens+light+color+sound+edit + prompt kernel) |
| prompting.md | **The projection layer**: keyframe/clip ordering templates, identity-handle fork ({{char:key}} resolution), positive-reframe table, empty-token blocklist + cinematic pairing rule, motion token kit, pre-flight lint checklist |
| model-matrix.md | DATED capability matrix (verify per campaign) + capability-flag schema + typosquat blocklist. The ONLY place model names live. |

## Usage protocol

1. **Controlled vocabulary is law.** Artifact fields accept only canonical values; banned aliases (push_in, slow_push_in, tracking, orbit, steadicam, cowboy, J-cut-as-field…) must resolve at write time via each file's ALIASES table.
2. **Definitions live here, not in prompts.** e.g. high/low-key are RATIO classes (never brightness, never prompt tokens); a zoom is an optical change, not a camera movement; a stitched oner is never "a single take."
3. **Every scene inherits its lighting sentence byte-identically**; every translation move names a foreground anchor; every emotional beat is MCU+ with a playable action.
4. **Pre-flight lint before every paid generation** (prompting.md checklist) — blocklist, negation scan, hex/ratio-number scan, anchor presence, lighting byte-identity.
5. **Model facts rot.** Normative rules reference capability flags; consult model-matrix.md at produce Step 1 and re-verify per campaign.
6. Numeric values marked [v] were web-verified at authoring (2026-07); safety-critical numbers re-verified in the release QA loop (docs/RESEARCH-CRAFT.md).
