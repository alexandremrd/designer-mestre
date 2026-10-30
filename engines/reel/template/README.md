# Template of style 03 · VSL with animated interface

The ready-made engine of this style is **the same one that produced the approved reference** (38.8 s, 1080×1920). The kit lives in
`kit/`, untouched. Reassembled from `example/`, it generates an `index.html` byte-for-byte identical to the reference's,
and the frames come out pixel-identical. **What changes from reel to reel is only `src/beats.js`**, the map of that
content, and the framing measured in `vsl.json`. The skin (fonts, five colors, sound) is optional (`skin-resolved.json`
in the project folder); without it, colors, fonts and sound are the reference's: never hardcode a color or font in the code.

## What each file is
| File | Role |
|---|---|
| `kit/kit.js` · `kit/kit.css` | the engine: FULL/SPLIT/PIP cameras with animated switch, punch, grade, pieces (`K.stack`, `K.pill`, `K.panel`, `K.grid`, `K.prompt`, `K.fan`, `K.stamp`, `K.cta`…), caption that follows the mouth (`K.mouthCaps`), sound effects and speech anchors (`K.at`, which errors if the phrase does not exist). **Do not edit** |
| `kit/index.template.html` · `kit/fonts/` · `kit/sfx/` | the page, the native fonts (Anybody, Plus Jakarta Sans, JetBrains Mono) and the procedural effects (no third-party licenses) |
| `assemble.mjs` | assembles `index.html` = template + `src/beats.js` + transcript + `vsl.json` + mouth + skin + sound. `--camera-only` generates the camera-only version |
| `prepare.sh` | 9:16 camera with the voice (`assets/clean.mp4`), transcript in the kit format, fonts and project material, `npm install`, mouth tracking and the 1st assembly |
| `vsl-default.json` | the initial `vsl.json`: the approved color and grade (fixed, R4) and the framing to measure (`punch`, `face`, `head`, `fullPos`, `splitPos`) |
| `beats-template.js` | the initial `src/beats.js`: the speech → camera → piece grammar and the rules, with commented recipes |
| `sfx-lean.js` | the `"sfxModo": "enxuto"` mode, the default (R2: ≤ 0.8 effect/s counting typing), injected by `assemble.mjs` |
| `tools/track-mouth.py` | `assets/face-track.json` (MediaPipe; without it, OpenCV) — without this file the caption does not appear |
| `tools/cards.mjs` | the phase 1 cards: one PNG per screen of `../entrega/plan.json`, taken from the engine at the middle of the screen |
| `tools/sounds.mjs` | `../sounds.json` with the effects the kit created (density for VERIFY and the critic) |
| `tools/final-audio-vsl.sh` | the final audio of this style: gain + limiter at 192 kHz, calibrated in up to 3 passes (−14 LUFS ±0.3, peak ≤ −1 dBTP). Use this one, not the common `final-audio.sh`: with the fast attacks of the kit's effects, the common one lets the peak through (+1.2 dBTP in the test) |
| `tools/sheet.sh` | `../qa/final-sheet.png` (16 frames of the final) |
| `tools/safe-zone-dom.mjs` | the safe zone read from the DOM: points to the element outside the box (complements the skill's `safe-zone.py`) |
| `tools/illustrations/` | illustrative screens in own HTML → JPG (declared illustration, R3) |
| `tools/generate-sfx.mjs` | regenerates `kit/sfx/` |
| `example/` | **the whole approved reel**: `beats-example.js`, `vsl.json`, `map.md`, `SOURCES.md`, `transcript.json`, `face-track.json`, `img/`, `progress-example.md` and the video at 540p |

## Proof that the engine runs on this machine (no agent, ~1 min + render)
With the prepare step done, the example assembles in full:
`cp example/beats-example.js src/beats.js; cp example/vsl.json .; cp example/img/* assets/img/; cp example/transcript.json assets/`
and then `node assemble.mjs && npx hyperframes lint`. (The example's `vsl.json` has no `sfxModo`, so
it comes out with the reference's exact sound; for a new video, start from `vsl-default.json`, which already ships with the lean one.) The example's speech only anchors to the example's video. With
another video, `K.at` errors on the first phrase that does not exist, and that already proves the anchors work.

## How to produce with it (phase 1 and phase 2 of the brief)
```bash
P=<project folder>; S=${REEL_SKILL:-~/.claude/skills/reel}; cd "$P"
cp -R "$S/template" motor && cd motor
bash prepare.sh                       # 9:16 camera + voice, transcript, fonts/material, npm install, mouth, 1st assembly
# ---------- phase 1 · plan ----------
# 1. check assets/transcript.json (names as the brand writes them, CTA code word in uppercase — R6)
# 2. measure on a frame of assets/clean.mp4, with the punch applied: face {x,y,w,h}, head {x,y}, punch, fullPos, splitPos → vsl.json
#    (color, grade and tint do NOT change). High top of the head (< ~300 px free above)? Nothing at the top in FULL: everything on the chest (R1).
# 3. real material in assets/img/ and ../assets/SOURCES.md (official screenshots and logos; screen without a screenshot → tools/illustrations/)
# 4. assets/map.md (format: example/map.md) → src/beats.js (read example/beats-example.js in full first)
node assemble.mjs && npx hyperframes lint                       # 0 errors; empty snapshot = broken anchor (see the console)
# 5. write ../entrega/plan.json (n, layout FULL|SPLIT, de, ate, fala, tela) — one screen per map line
node tools/cards.mjs                                    # ../entrega/cards/P01.png… + filled-in image; stop and answer
# ---------- phase 2 · render (version N) ----------
npx hyperframes snapshot --at <each switch and each beat> -o snapshots   # face free (R1), nothing cut off, nothing overlapping
node tools/safe-zone-dom.mjs . --strict                       # "zona segura OK"
npx hyperframes render -q high -o ../render/_reel-raw.mp4
node assemble.mjs --camera-only && npx hyperframes render -q high -o ../render/_camera-only.mp4 && node assemble.mjs
bash tools/final-audio-vsl.sh ../render/_reel-raw.mp4 ../render/reel-vN.mp4   # −14 LUFS ±0.3, peak ≤ −1 dBTP
node tools/sounds.mjs                                             # ../sounds.json
bash tools/sheet.sh ../render/reel-vN.mp4 ../qa/final-sheet.png
python3 "$S/tools/verify.py" .. --video render/reel-vN.mp4 --sfx ../sounds.json --camera ../render/_camera-only.mp4
#   (S = the root of the reel skill; verify.py writes ../VERIFY.md and runs the safe zone → ../qa/safe-zone.png; --sfx and --camera are relative to this folder)
# MINUTAGEM.md (the map with the final times) and progress.md in the project folder, as in example/progress-example.md
```

## The quality standard is the example, not a minimum
The reel in `example/` is the yardstick. Before writing `beats.js`, watch `example/approved-reference-540p.mp4`
and read `example/beats-example.js` and `example/progress-example.md` in full. The expected level has four parts:
- **Density:** something new every 1.5–3 s, with FULL and SPLIT near 50/50.
- **Precision:** every piece enters on the word, via `K.at`.
- **Truth:**
  - price with the official pricing page and the date;
  - logos from Wikimedia Commons;
  - product screens without a screenshot become a declared illustration, with a fictional company.
- **Finish:**
  - animated camera switch, with `K.hideMouth(t − 0.05, t + 0.5)` on every switch;
  - lettering on the chest with `K.hideMouth` over the interval;
  - caption with the keywords in `accent`.

Each video has its own map: do not copy the example's screens, copy the level.

## What to fix relative to the example
The example was approved before rule R1 became explicit. Two of its pieces touch the head:
- the "PRONTOS ✓" stamp (x 600, y 300);
- the top kickers (y 250).

In a new video, stamp and kicker go on the chest (y ≥ 1150) or in a SPLIT stretch.

## What does not change (skin.json invariants)
- FULL ↔ SPLIT always in a 0.45 s animated switch.
- Each keyword gets a piece exactly on the word.
- The interface is dark glass, with the color in the graphic and not on the face: filter `saturate(1.04) contrast(1.05) brightness(0.97)` and tint 0.3 / 0.25.
- The hook is the camcorder HUD → glitch.
- Sound: lean by default (`"sfxModo": "enxuto"`, approved by `verify.py`). The reference's exact sound (`"referencia"`, ~1.4/s) only on request (`"sfxModo": "referencia"` in `vsl.json`).
- The house rules R1–R11 prevail.
