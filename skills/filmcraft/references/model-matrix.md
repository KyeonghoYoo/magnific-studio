# Model Matrix — Dated Appendix | KR: 모델 매트릭스 — 유효기간부 부록

**DATED APPENDIX — verified 2026-07. Model facts rot.** VERIFY PER CAMPAIGN via `video_models_list` / `images_models_list` + official docs before relying on any row below. Normative rules live in `prompting.md` and key on capability flags ONLY — nothing in this file is itself a rule; it just resolves flags to families.

## Capability Flag Schema

| Flag | Type | Meaning |
|---|---|---|
| `negative_prompt` | bool | true → `prompting.md` §4 populates a negative field from the reframe table; false → positive reframe only, no field exists |
| `max_moves_per_shot` | int | 1 = one-move law (default); ≥2 = produce-time adjacent-shot merge permitted (never hand-authored) |
| `named_tag_syntax` | bool | true → identity resolves to the family's native tag (`prompting.md` §3); false → `appearance_phrase` + reference image |
| `flf_support` | bool | true → first+last-frame keyframe pairs legal (`variation_type` medium/large); false → force FF-only downgrade |
| `camera_param_object` | bool | true → a structured camera object exists alongside text (text is still authored; the object is a redundant channel, not a replacement) |
| `legal_durations[]` | int[] (sec) | produce-time `gen_duration_s` = nearest legal duration ≥ intent + handles (rulings H8) |
| `text_render_ok` | bool | reserved — house rule bans baked text regardless of this flag (`prompting.md` §7) |
| `native_audio` | bool | true → `prompting.md` §8 audio-label syntax active; false → route through the audio pipeline only |

## Video Families — Camera & Identity

| Family (flagship) | Mechanism | max_moves_per_shot | named_tag_syntax | camera_param_object | flf_support |
|---|---|---|---|---|---|
| Veo (3.1) | text only | 1 (soft) | false (Ingredients: ≤3 ref images, appearance-phrase addressing) | false | true (First/Last-Frame, official) |
| Runway (Gen-4.5) | text choreography | 1–2 (soft) | true (`@name`) | false (text-only successor) | undocumented |
| Runway (Gen-3 Alpha Turbo + Aleph v1) | UI 6-axis + text | compound | true (`@name`) | true (UI panel) | undocumented |
| Kling (3.0/Omni) | `camera_control` object + text | 1 (soft) | true (`<<<name>>>`; O1 legacy `@Element1`) | true — community sources garble the pan/tilt axis mapping, verify before shipping | true (Frame Mode, official) |
| Hailuo/MiniMax (02/2.3) | `[Move]` brackets, inline & combinable | **≤3 — CAPABILITY EXCEPTION**, official cap | false (brackets are camera commands, not identity tags) | false | partial — End-Frame-Only mode (destination-first, not FF+LF) |
| Luma (Ray3/3.14) | composable Camera Motion Concepts (15 motion + 9 angle primitives) | **multiple — CAPABILITY EXCEPTION**, officially unbounded | false | false (named concept tokens) | undocumented — no Dutch-angle primitive (coverage gap) |
| Wan (2.1/2.2 open) | text (base); LoRA/Fun-Control checkpoint for reproducible paths | 1 | false | false (checkpoint swap is the de facto param channel) | community-implemented — serving-path dependent (a wrapper reportedly drops the last frame in some pipelines — UNVERIFIED against a primary source; test your serving path) |
| Seedance (1.0 Pro / 2.0 / 2.5) | text + `cameraFixed` bool gate | 1 default | true (`@Image N`) | false (bool gate, not a full object) | undocumented [row unverified against ByteDance primary docs — re-check before relying] |
| Sora (2 / 2 Pro) | text only | 1 strict | false (Cameo = consent-gated identity token, max 2/gen — not addressing syntax) | false | undocumented |

`flf_support`: cross-family adherence ranking is an ACKNOWLEDGED RESEARCH GAP (rulings L12) — don't rank from this column. Measure per-clip via SSIM/pHash (`quality-reviewer` `flf_adherence` axis, rulings H6).

## Video Families — Duration, Negative, Audio, Status

| Family (flagship) | negative_prompt | legal_durations (s) | Resolution | native_audio | Status |
|---|---|---|---|---|---|
| Veo (3.1) | true (`negativePrompt`; positive phrasing still recommended) | 4, 6, 8 (+extend) | 720p/1080p, 4K upscale | true (`SFX:` / `Ambient noise:` labels) | GA |
| Runway (Gen-4.5) | false, explicit — vendor docs: "opposite results" | 2–10 | 720p | false | GA; Gen-3 Alpha Turbo + Aleph v1 predecessor **sunsets 2026-07-30** (its UI camera panel goes with it) |
| Kling (3.0/Omni) | true, dedicated 2500-char field | 5, 10 (Director Mode ≤15/6-shot; extend ~3min) | ≤4K | undocumented | GA |
| Hailuo/MiniMax (02/2.3) | undocumented — community claim uncorroborated | 6 (any res) / 10 (≤768p) | ≤1080p | undocumented | GA |
| Luma (Ray3/3.14) | API yes; docs discourage | 5–10 (extend ~30) | 1080p, 4K upscale | undocumented | GA |
| Wan (2.1/2.2 open) | true (API/ComfyUI) | ~5 | 480/720p | undocumented | open-weight (2.5/2.6 closed successors exist) |
| Seedance (1.0 Pro / 2.0 / 2.5) | version-dependent (2.0+ works; 1.0 unclear) | 2–12 (1.0); 15 (2.0); 30 (2.5) | ≤1080p, 4K@2.5 | undocumented | GA |
| Sora (2 / 2 Pro) | not documented | 4–20 discrete | ≤1920×1080 | true (trailing speaker-labeled block; "a handful of sentences" cap on 5–10s clips) | **API sunsets 2026-09-24** — do not anchor new work on Sora |

`native_audio`: undocumented = treat as false (route through the audio pipeline, `prompting.md` §8) until verified per campaign.

## Image Families

| Family (flagship) | negative_prompt | named_tag_syntax | text_render_ok | Resolution | Status |
|---|---|---|---|---|---|
| Flux (2) | false, explicit | false | false (quote+font is a stills-only hack, no video path) | 4MP native | GA |
| Seedream (4.5/5.0) | legacy field, not promoted | false | undocumented | ≤4096² | GA — batch sequence-mode ≤9 mutually-consistent images/call, ~12 fused multi-ref inputs [CONFLICT: ByteDance-side material cites up to 15 batch / ~10 reference — figures may measure different modes; verify against primary docs before relying] |
| nano-banana (Gemini 3.1 Flash / 3 Pro Image) | false, architectural — positive reframing is doctrine | true — recommended even for multi-character stills | true (quote+font technique) | ≤4K, 14 ratios | GA |
| Imagen (4) | undocumented | false | undocumented | 1K/2K | **sunsets 2026-08-17** — migrate to nano-banana |

## One-Move Exceptions (capability, not default)

Default assumption for any family not yet verified this campaign: `max_moves_per_shot = 1`. Two families ship native multi-move composition as a first-class, officially documented feature — treat ONLY these as `max_moves_per_shot ≥ 2` until a new vendor doc says otherwise:
- **Hailuo/MiniMax**: `[Move]` brackets, ≤3 combined, official cap.
- **Luma Ray**: composable Camera Motion Concepts, multiple primitives, officially unbounded.

## Typosquat Blocklist

Verbatim — reject any tool/API endpoint matching: `klingaio.com`, `kling3-ai.com`, `kling4.co`, `klingmotioncontrol.com`, `cling-ai.com`, `hailuo02.net`, `hailuoaiminimax.com`, `minimax-ai.chat`.
