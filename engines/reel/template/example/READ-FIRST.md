# Approved example — the reference reel of this style

This is the video that defined the standard of style 03, approved as is: "3 ferramentas grátis do Claude",
38.8 s, 1080×1920, 30 fps, −14 LUFS. It was assembled with **this same engine** (`../kit/`, untouched).
Reassembled from this folder, the `index.html` comes out byte-for-byte identical to the original, and the frames come out
pixel-identical.

**Use it as a quality yardstick, not as a mold.** Each new video has its own beat map, made from what
is said in it. What you copy from here is the level:
- density (something new every 1.5–3 s);
- precision (everything enters on the word);
- truth (facts with a source, declared illustration);
- finish (glass, glow, animated camera switch, caption that follows the mouth).

## Files
| File | What it is |
|---|---|
| `approved-reference-540p.mp4` | the approved video, at reduced resolution, to watch and compare frames |
| `beats-example.js` | the complete visual script (15 beats); it is the best reference for using the `K.*` kit |
| `vsl.json` | the approved framing and color (`gradeFilter`, `tint`, `tint2`, `punch` 1.06…) |
| `map.md` | the time × speech × camera × piece map (the format a new video's `assets/map.md` must have) |
| `SOURCES.md` | the sources of the facts, prices and images (the standard of rule R3) |
| `transcript.json` | the corrected transcript (R6) that the beats anchor to |
| `face-track.json` | the mouth tracking used by the caption |
| `progress-example.md` | the production path: cut, transcript, framing, real material, verification and the color fix |
| `img/` | official logos (Wikimedia Commons) and the illustrative screens (fictional company "Padaria Trigo & Mel") |

## Reassemble the example (engine test)
In the project's engine folder (`<P>/motor`, the copy of `template/`), after `prepare.sh` with the example video:
```bash
cp example/beats-example.js src/beats.js && cp example/vsl.json . && cp example/img/* assets/img/
cp example/transcript.json example/face-track.json assets/
node assemble.mjs && npx hyperframes lint
```
The example's camera video does not ship with the skill. With the original `clean.mp4`, the `index.html` comes out byte-for-byte identical.

## What to fix when reusing a stretch of this example
The example was approved before rule R1 (face never covered) became explicit. Three pieces touch the head and
**must not be copied at the same position**:
- **stamp "PRONTOS ✓"** (`K.stamp`, x 600, y 300): sits on the forehead, at ~20 s. In a new video, put it on the chest,
  next to the export panel (y ≥ 1150);
- **kicker "É muito fácil"** (`K.kickerTop`, y 250) and **"Link direto na sua DM"** (y 250): touch the hair.
  In a new video, use a pill on the chest (`K.pill`, y ~1390) or put the kicker in a SPLIT stretch.

## Sound
The example has the kit's effects unfiltered: 56 effects in 38.8 s (≈ 1.4/s, counting typing). That is the exact sound
of the approved video, and the example's `vsl.json` reproduces it. **In a new video, the default is lean** (`"sfxModo":
"enxuto"` in `vsl-default.json`): the large pieces and the typing stay, up to 0.8 effect/s, and `verify.py` approves.
In the example, lean ends up with 31 effects (0.80/s).
