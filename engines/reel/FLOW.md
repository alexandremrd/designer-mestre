---
name: reel
description: Edits a REEL / Short / vertical 9:16 video from start to finish, with no panel and no choices — the person sends their raw recording of themselves talking and the skill CUTS (removes silences, breaths, "éé", stutters, mistakes, restarts and repetitions, using the sound-based cut engine approved in production) and EDITS with the "VSL with animated interface" engine (the same engine, kit and rules that produced the approved reference reel — camera alternating full screen with punch-in and split screen, each keyword becoming an interface piece that enters exactly on the word, caption that follows the mouth, lean sound effects, −14 LUFS). Delivers a verified render/reel-v1.mp4 and iterates on request. ALWAYS use when asked to "edit this reel", "cut and edit", "make the reel from this video", "assemble this raw footage", "edit this video for Instagram", "clean and edit", "make the VSL", or when handed a vertical/horizontal spoken video to turn into a quick reel — even without naming the skill. It is NOT the reel studio with panel and styles (that is another skill), NOT for long YouTube video, showreel without someone talking, script, copy or carousel.
---

# reel · cuts and edits in the VSL engine

One skill, two engines, zero panel. The person sends the video; you cut with the **cut engine**
(`cut/`) and edit with the **VSL engine** (`template/`, the untouched kit that produced the approved reference),
following the **house rules** (`house-rules.md`, they prevail over everything) and **STYLE.md** (the engine spec).
The result is the same the studio would deliver in the VSL style with the native skin: same colors, fonts, sound and
rules. **Never publish or send the video** (R9). **No third-party name** in the video or in the files (R11).

Read before starting (in this order, in full): `house-rules.md` → `cut/CUT.md` → `STYLE.md` →
`template/README.md` → `template/example/READ-FIRST.md`. Lesson that pays for the reading: **the quality standard is the example,
not a minimum** (`template/example/beats-example.js` is the yardstick; each video has its own map).

## Skill map
```
SKILL.md              this file (the flow)
house-rules.md     R1–R11: face never covered, sparing SFX, real material, no clipped word, −14 LUFS…
STYLE.md             the VSL engine spec: layouts, framing, motion, caption, pieces, sound, pipeline, acceptance, lessons
skin.json             the native values (fonts, five colors, invariants) — the reference skin
cut/                cut engine: CUT.md (script) · references/ROUGH-CUT.md (the why) · scripts/ · example/
template/               VSL engine: kit/ (untouched) · assemble.mjs · prepare.sh · tools/ · example/ (the approved reel) · README.md
tools/          prepare.py · face.py · anchors.py · verify.py · safe-zone.py · crop.py · final-audio.sh
attachments/               reference frames and the color before × after
```
`S=~/.claude/skills/reel` (or `REEL_SKILL`). Environment variables (R10): `WHISPER_MODEL`, `VSL_PYTHON`
(Python with mediapipe or opencv), `FACE_MODEL`, `VSL_NODE_MODULES`, `CHROME`, `RVM_PYTHON` (matte only).

## Flow (fixed order)

### 0 · Project
1. Create **one folder per reel** next to the video: `reel-<slug>/` with `cut/`, `render/`, `qa/`, `entrega/`,
   `assets/`. Never reuse another edit; never write to the raw footage folder outside it.
2. First time on the machine: `python3 $S/cut/scripts/0-check.py` (ffmpeg, whisper-cli, numpy, model).
3. Say in one line what will happen ("Cutting and editing in the VSL engine; v1 arrives in a few minutes")
   and warn before each slow step. Long steps run in the background.

### 1 · Cut (cut engine, `cut/CUT.md` in full)
`B=$S/cut/scripts` · everything in `cut/`:
```bash
python3 $B/1-takes.py "<bruto>" corte && cat cut/takes.txt      # READ in full before choosing
# write cut/keeps.json (keeps rules: the best complete take of each sentence; false starts out)
python3 $B/2-fillers.py corte
python3 $B/3-cut.py "<bruto>" corte                                  # 4-frame J/L (the VSL standard)
python3 $B/4-review.py corte --prompt "<proper names in the video>" && cat cut/review.txt
```
Criterion (R5): all `review.txt` blocks approved; **no clipped word**; no pause > 0.25 s.
Clipped word → protect the interval (`raw`/`force`) and cut again. If the person says the video is **already
clean**, skip: `cp "<video>" cut/clean.mp4` and transcribe with `$S/tools/prepare.py cut/clean.mp4 preparo`.
Outputs: `cut/clean.mp4`, `cut.wav`, `edl.json`, `cut_words.json`.

### 2 · VSL engine · prepare
```bash
cp -R "$S/template" motor && cd motor && bash prepare.sh
```
Makes the 9:16 camera with the voice (`assets/clean.mp4`), the transcript in the kit format, `npm install`, the mouth
tracking and the 1st assembly. Without `skin-resolved.json` the skin is the **native** one (the reference's): do not create one.

### 3 · Phase 1 · plan (`template/README.md`)
1. **Transcript** (R6): correct `assets/transcript.json` by hand (Cloud → Claude, A → IA, names as the brand
   writes them, CTA code word in UPPERCASE); the original stays in `transcript-whisper.json`.
2. **Framing**: `python3 $S/tools/face.py assets/clean.mp4 ../preparo --916` and measure on a frame
   with the punch applied → `vsl.json` (`punch`, `face`, `head`, `fullPos`, `splitPos`; color and grade do **not** change).
   Less than ~300 px free above the head → nothing at the top in FULL: lettering, kicker and stamp on the chest (R1).
3. **Real material** (R3): official screenshots and logos in `assets/img/` + `../assets/SOURCES.md` (origin, license,
   date); fact and price with an official page; screen without a screenshot → declared illustration (`tools/illustrations/`).
   Never invent a logo, number or screenshot.
4. **Map → beats**: `assets/map.md` (time × speech × camera × piece, like `example/map.md`) and then
   `src/beats.js`, one `K.*` call per map line, times only via `K.at("exact phrase")` (read
   `example/beats-example.js` in full first). Something new every 1.5–3 s; FULL ≈ SPLIT; `K.hideMouth` on every
   switch and on every lettering; `K.mouthCaps` last.
5. `node assemble.mjs && npx hyperframes lint` (0 errors; empty snapshot = broken anchor, read the console).
6. `../entrega/plan.json` (n, layout, de, ate, fala, tela) and `node tools/cards.mjs` → `entrega/cards/P01.png…`.

**Gate:** by default **go straight to phase 2** — the person asked for speed. Stop and show the map or the cards only
if they ask ("show me first") or if there is a content doubt only they can resolve (fact, price, name).

### 4 · Phase 2 · render (`template/README.md`)
```bash
npx hyperframes snapshot --at <each switch and each beat> -o snapshots      # face free (R1), nothing cut off/overlapping
node tools/safe-zone-dom.mjs . --strict                           # "zona segura OK"
npx hyperframes render -q high -o ../render/_reel-raw.mp4
node assemble.mjs --camera-only && npx hyperframes render -q high -o ../render/_camera-only.mp4 && node assemble.mjs
bash tools/final-audio-vsl.sh ../render/_reel-raw.mp4 ../render/reel-v1.mp4   # −14 LUFS ±0.3 · peak ≤ −1 dBTP
node tools/sounds.mjs && bash tools/sheet.sh ../render/reel-v1.mp4 ../qa/final-sheet.png
python3 "$S/tools/verify.py" .. --video render/reel-v1.mp4 --sfx ../sounds.json --camera ../render/_camera-only.mp4
```
Then write `MINUTAGEM.md` (beat by beat: time, speech, what appears, layout, sound) and `progress.md` in the project
folder. **Critique before showing:** `VERIFY.md` fully approved, frame sheet, R1 (face), R2 (SFX ≤ 0.8/s
in lean mode), R6 (caption), R7 (safe zone), R8 (audio). Up to 2 adjustment rounds before delivering.

### 5 · Delivery and iteration
Reply with: path of `reel-v1.mp4`, duration (raw → cut → final), LUFS and peak, number of screens and of
effects, what was left out in the cut and what was protected, caption corrections, sources of the facts, open
points. Requested adjustment → `reel-v<N+1>.mp4` (previous versions stay in `render/`); cut change →
retranscribe and remap (`cut/scripts/remap.py`), never retime by hand.

## Conduct rules
- **The engines are not rewritten.** `template/kit/` and `cut/scripts/` stay untouched; each video writes only
  `src/beats.js`, `vsl.json`, `keeps.json` and the adjustments. A cut parameter changes only via the diagnosis in
  section 9 of `cut/references/ROUGH-CUT.md`, one at a time, recorded.
- **One version per round**, complete and verified.
- **Lean sound** (`"sfxModo": "enxuto"`, the `vsl-default.json` default): ≤ 0.8 effect/s counting typing,
  typing always continuous. The reference's exact sound (`"referencia"`) only on request.
- **Real material** always; illustration only if declared. **Face never covered.** **Safe zone.**
- **You produce** in this session. If the person asks for a specific agent or model, launch a
  general-purpose agent with this SKILL.md + `STYLE.md` + `template/README.md` as the brief and critique the delivery.
- Something failed (ffmpeg, whisper, model, npm, Chrome)? Say in one line what to do; `cut/scripts/0-check.py`
  diagnoses the machine.
