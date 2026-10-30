# Style 03 · VSL with animated interface
*The video is a conversation that turns into interface: the camera alternates full screen with punch-in and split screen with the presenter in a card, and each spoken keyword gets an element that enters exactly on the word.*

> Specification distilled from a real reel produced in this style (it is the engine of the `reel` skill) (38.8 s, 1080×1920, 30 fps, −14 LUFS),
> recorded in a dark studio with purple and blue light from a 2560×1440 horizontal raw footage of 40.9 s.
> The reference frames are in `attachments/` (section 13). The colors and fonts cited here are the reference's
> **native** values; the skin (`skin.json`) can swap them by role.

> **BUNDLED ENGINE — use it, do not rebuild it.** The `template/` folder is the exact engine that produced the approved reference:
> `kit/` (`K.*` kit: layouts, pieces, caption that follows the mouth, grade, SFX — untouched), `assemble.mjs`, `prepare.sh`,
> `tools/` and `example/` (the whole approved video: beats, map, sources, images, log and the video at 540p;
> reassembled, it comes out identical to the original, pixel by pixel). Copy `template/` to `<P>/motor` and follow `template/README.md`.
> **Never write a new engine nor edit `kit/`.** Each new video writes only its `src/beats.js` (the map of that
> content) and adjusts `vsl.json` (measured framing). Flow in section 10.0.

---

## 0 · In one sentence + the 3 signs

**In one sentence:** the presenter talks and the screen responds — everything they say becomes an interface piece that is born
on the word, in a constant alternation between full screen (FULL, with punch-in) and split screen (SPLIT, content
on top and the presenter in a card below), with true content on screen and soft color on the face.

**The 3 signs (invariants — if one is missing, it is not this style):**
1. **Animated FULL ↔ SPLIT.** The camera alternates between full screen with punch-in and split screen with the presenter
   in a card with marked corners in the bottom half. The switch is always animated (0.45 s), never a hard cut.
2. **Each keyword gets an element that enters exactly on the word.** Nothing enters at "guessed
   seconds": every entry is anchored to the word's onset in the transcript. Something new appears every 1.5–3 s.
3. **True interface, of glass, with the color in the graphics and not on the skin.** The panels are dark glass
   cards with a glow in the `destaque` color; the facts, prices and logos come from official sources or from a declared
   illustration; the face keeps a natural color.

---

## 1 · The engine on one page

This style obeys the **house rules R1–R11** (`house-rules.md`, at the skill root). The ones it strains are
marked below.

1. **The video is a conversation that turns into interface.** The presenter never disappears for long. The camera alternates
   between FULL (full screen with punch-in) and SPLIT (content on top, the presenter in a card below). Each
   spoken keyword gets an element that enters **exactly on the word**.
2. **Everything is anchored to the transcript, never to guessed seconds.** The engine resolves the time of each piece by an
   *exact phrase* from the transcript (`K.at("exact phrase", n)` returns the onset of the first word of the n-th
   occurrence; `K.end("exact phrase")` returns the end of the last) and **throws an error if the phrase does not exist**. A snapshot
   with no overlay at all is the classic symptom of a broken anchor.
3. **The screen content is true** (R3). Facts come from official pages, prices from the official
   pricing pages and logos from Wikimedia Commons. Product screens that do not exist for capture become a **declared
   illustration**, made with a fictional company. Production lesson: *"search for screenshots and everything you need"*
   — no generic screen and no invented number.
4. **The cut is tight, but no word is clipped** (R5). The style receives the already clean video from the cut engine
   (`cut/`), with J/L on; every splice was checked by transcription. No pause > 0.35 s remains.
5. **The color is soft** (R4). Production lesson: the default grade of the origin style was *"too aggressive and
   dark"*. The `destaque` color stays in the screens and the glows; on the face, only a touch (filter
   `saturate(1.04) contrast(1.05) brightness(0.97)` and tint layers 0.3 / 0.25).
6. **The face is never covered** (R1). Texts stay on the chest or in split screen. This style **strains R1**
   in three pieces — title behind the head, top kicker and stamp — which only enter when there is room above the
   head (section 3.5); in the reference framing, none of them fit and all moved down to the chest.
7. **Caption that follows the mouth.** The caption is 1–3 words under the chin, following the head; it disappears by itself
   in SPLIT and is hidden in every lettering on the chest and in every layout switch.
8. **Lean sound by default** (R2). The kit puts an effect on each piece (the approved reference has ~1.4/s). The default is
   `"sfxModo": "enxuto"`: the large pieces (glitch, stamp, click, switches) and the typing stay, up to 0.8 effect/s
   counting everything, and `verify.py` approves. The reference's exact sound (`"referencia"`) only enters on request (`"sfxModo": "referencia"`
   in `vsl.json`), and fails the verifier's SFX item.
9. **Signature hook:** 1–2 s of desaturated "raw" with camcorder HUD → glitch → the grade in the `destaque` color
   comes in.
10. **It comes verified before delivery** (R9). Lint, snapshot at each beat and each switch, safe zone every
    0.25 s, audio at −14 LUFS and `VERIFY.md` with the evidence.

---

## 2 · Format and general numbers

| Item | Value |
|---|---|
| Typical duration | 35–45 s (reference: 38.8 s from a 40.9 s raw) |
| Resolution · fps | 1080×1920 · 30 fps |
| Accepted raw | horizontal (e.g.: 2560×1440) cropped from the center to 9:16, or native vertical |
| Layouts | FULL (full screen with punch-in) · SPLIT (content on top, presenter card below) · PIP (small presenter) · takeover (screen without the presenter) |
| Target layout proportion | FULL ~40 % · SPLIT ~45 % · PIP ~8 % · takeover ~7 % (the reference ended ~50/50 FULL/SPLIT, no PIP) |
| Cadence of novelty | something new on screen every 1.5–3 s |
| Base punch-in | **measured per video**: 1.06 in the reference (the origin default, 1.22, crops too much when the face already takes up much of the frame) |
| Extra impact punch | 1.14–1.20, on a hard cut, on an impact phrase |
| Layout switch | always animated, 0.45 s, `power3.inOut` |
| Entries | blur → sharp, 0.22–0.5 s, `power3.out` |
| Exits | blur + fade, 0.2–0.25 s |
| Residual pauses in the clean video | none > 0.35 s (reference: only two, of 0.31 s and 0.29 s) |
| SFX | ≤ 0.85 per second (R2); overall volume ~0.4 |
| Final audio | −14 LUFS (±0.5), peak ≤ −0.5 dBFS (the render comes out at ~−25 LUFS and is normalized afterward) |
| Safe zone | x 90–990 · y 220–1520; nothing in the button column (x > 940 and y > 1150) |

---

## 3 · Layouts and framing (px at 1080×1920)

### 3.1 Framing parameters (values approved in the reference)

These parameters are read by the style's generator. The face and head ones come from `tools/face.py`
and are **measured on a frame of the clean video with the punch already applied**.

| Parameter | Approved value | What it is |
|---|---|---|
| `punch` | 1.06 | base scale of FULL (measure per video) |
| video position in FULL | `50% 28%` | `object-position` of the camera in full screen |
| video position in SPLIT | `50% 26%` | `object-position` of the camera inside the card |
| video position in PIP | `50% 24%` | `object-position` of the camera in the PIP |
| face box | x 310 · y 300 · w 540 · h 680 | region nothing may cover (R1) |
| head point | x 580 · y 620 | center used by the caption that follows the mouth |
| top of content in SPLIT (`topY`) | 240 | just below the safe zone (220) |
| caption line (`capY`) | 1500 | lower limit of the caption, inside the safe zone |
| color filter | `saturate(1.04) contrast(1.05) brightness(0.97)` | R4 |
| tint 1 · tint 2 | 0.30 · 0.25 | opacity of the two color layers over the camera |

In the reference the head goes from ~y 150 to ~y 1000 in FULL: the head is high in the frame and that decides almost everything
about the framing (see 3.5).

### 3.2 FULL (full screen with punch-in)
- The camera takes the whole frame, at scale `punch` (1.06) and `object-position 50% 28%`.
- Extra punch (1.14–1.20) on an impact phrase, applied as a **hard cut** between phrases — it is the only hard cut
  allowed in the style (the FULL↔SPLIT switch is never hard).
- Everything that enters in FULL stays **on the chest**, between the chin and the caption:

  | Element | Position |
  |---|---|
  | Stacked lettering | `top` 1150–1180 |
  | Pills | y 1250–1390 |
  | Small panel (e.g.: export panel) | box y 1170–1470 |
  | CTA button | y 1300 |

### 3.3 SPLIT (content on top, presenter in a card below)
- **Content:** y 240–960, x 90–990 (header with kicker + title at the top, panel/grid/fan below).
- **Presenter card:** bottom half, with the video at `object-position 50% 26%` and a corner frame
  (four "L"s in the corners, like a camcorder viewfinder), the whole face inside the card.
- The caption that follows the mouth **disappears by itself** in SPLIT (the content above already carries the text).
- Inside SPLIT, the elements' tops cannot coincide: the fan of slides enters at `top` 600 so as not to
  land on top of the progress bar (production lesson).

### 3.4 PIP and takeover
- **PIP:** the small presenter (`object-position 50% 24%`) with content dominating the screen. The reference did not
  use it; it stays as an option for stretches where the interface needs the whole screen without losing the presenter.
- **Takeover:** interface-only scene, without the presenter (~7 % of the video, at most). It is the 3rd option of R1.

### 3.5 The FULL ↔ SPLIT seam
- Switch always animated: 0.45 s, `power3.inOut`. The video shrinks/grows between the full frame and the card.
- **The mouth caption is hidden on every switch**, from `t − 0.05 s` to `t + 0.5 s`: it follows the frame
  shrinking and "leaks" outside the safe zone if left on (production lesson: the safe-zone sweep
  flagged text exactly at the reference's 25.7 s transition). The style's generator does this automatically.
- A light transition (flash or light leak) may cover the switch when the scene calls for impact.

### 3.6 What the head height decides (tension with R1)
Measure the top of the head with `tools/face.py`. With **less than ~300 px free above the head**:
- title behind the head (with the presenter cut out) **off** — in the reference the head covered almost the
  whole title and it became illegible; in its place, stacked lettering on the chest (`top` ~1150) with the mouth
  caption hidden over the same interval;
- top kicker (y 250) **forbidden** — it touches the hair; it goes to the chest or becomes a pill;
- top stamp (x 600, y 300) **forbidden** — it hits the top of the head; it goes to the chest, next to the panel.
The generator's default is the chest; the top of the frame is only freed when the measurement shows room.

---

## 4 · Cut and rhythm

### 4.1 Contract with the cut engine
The cut of the raw footage does not belong to the style. The cut engine (`cut/`) removes pauses, breaths, "ééé", stutters and restarts,
checks each splice by transcription and delivers `clean.mp4` (30 fps, keyframe every 1 s) + `cut_words.json`,
obeying R5. This style asks the engine for **J/L on (4 frames)**: the voice enters a little before the image
at each splice, which hides the cuts in a video where the camera is always moving.

The style starts at the clean video. After any new trim, retranscribe and remap everything that depended on the
times (scenes, SFX, emphases, face tracking) — never mix raw times with clean-video times.

### 4.2 Where the cut falls
- **Between phrases, in FULL:** extra punch on a hard cut (1.14–1.20) on the impact phrase.
- **On the keyword:** there is no cut — the piece enters exactly at the word's onset, over the camera.
- **On the layout switch:** animated transition of 0.45 s, placed at the start of the phrase that calls for the content
  (e.g.: the switch to SPLIT enters at "economizar", and the price panel starts revealing in the same phrase).
- **In a light scene:** flash or light leak at the onset of the word that becomes the "turn" (e.g.: "totalmente", "tudo").

### 4.3 Cadence
- Something new every 1.5–3 s: either a layout switch, or a new piece, or a new step inside a panel.
- A panel reveals its steps **word by word** (e.g.: price line 1 → line 2 → struck-out total → "R$ 0"),
  each step on its word.
- Grid of cards: each card enters on the spoken name ("Slides", "Docs", "Design" → 3 entries in ~2 s).
- Reading-time rule: a pill or lettering stays until the end of the phrase (`fim("frase")`) or until the next
  piece in the same place; never less than ~0.8 s on screen.

### 4.4 Pauses
None > 0.35 s in the clean video. A 0.44 s pause that remained in the reference was removed by shortening the protected
window of the cut — a pause that remains after assembly is remapped by the engine, never by hand.

---

## 5 · Motion

### 5.1 Entries
- **Blur → sharp:** `opacity 0`, `blur 8–18 px`, and `y 10–26 px` **or** `scale 0.8–0.96` → final state in
  0.22–0.5 s, `power3.out`.
- Three flavors of lettering: `blur` (the default above), `glow` (sharp with a glow in the `destaque` color that
  pulses once) and `letters` (letter by letter, for the impact phrase).
- Interface pieces (panel, chat, grid) enter with the same blur → sharp; their **inner steps** enter
  each on its word, with the same curve, and may carry their own SFX only if they are "large".

### 5.2 Exits
- Blur + fade in 0.2–0.25 s. Nothing disappears on a hard cut except the camera on the impact punch.

### 5.3 Camera
- **Layout switch always animated:** 0.45 s, `power3.inOut`. Never a hard FULL↔SPLIT cut.
- **FULL is always punch-in.** Extra punch (1.14–1.20) on a hard cut on the impact phrase.
- The mouth caption follows the head point; during the switch it is hidden (3.5).

### 5.4 Light transitions
- **Flash:** short white peak at the word's onset, with configurable `peak` (~0.6–0.8).
- **Light leak:** light stain in the `destaque` color crossing the frame for `d` seconds (~0.6 s), used to
  cover a SPLIT → FULL switch.
- **Glitch:** only in the hook, right after the camcorder HUD, together with the boom.

### 5.5 Cursor and typing
- **Typing request:** the request text enters the chat field at `cps` characters per second (~18–24), and the
  send button "presses" at `send` (end of the spoken phrase).
- **CTA button:** the cursor slides to the button and clicks at `clickAt` (onset of the code word).
- **Drawn arrow:** in the export panel, the arrow between the deck and the logos is drawn (stroke) in ~0.4 s.

### 5.6 What is NEVER done
- Hard cut between FULL and SPLIT.
- Entry before the word (anticipating) or at "guessed seconds".
- "3D layers" (fake depth with layer parallax) — vetoed at the style's origin.
- Animating `scale`/`scaleX` without including `opacity` in the destination: the piece vanishes in the render.
- Animating `left`: lint fails it; animate with `x`.
- Covering the face, darkening it "just for an instant" or putting a piece in the button column.

---

## 6 · Caption

- **Mode:** caption of **1–3 words**, no pill, that **follows the mouth** — positioned under the chin from
  `face.json` (face tracking by keyframe) and following the head when it moves.
- **Font:** text font (native: Plus Jakarta Sans 700/800), in the `texto` color (native `#ffffff`).
- **Accent words:** a list declared per video (e.g.: "Claude", "utiliza", "fácil", "prontos",
  "PowerPoint", "carrossel", "link") comes out in the `apoio` color (native `#b9a3ff`, lavender).
- **In SPLIT:** disappears by itself (the header above carries the idea).
- **In lettering on the chest:** hidden over the same interval as the lettering, so as not to fight it.
- **On layout switch:** hidden from `t − 0.05 s` to `t + 0.5 s` (automatic in the generator).
- **Lower limit:** `capY` 1500, inside the safe zone.
- **Text:** transcript corrected by hand before assembling (R6), keeping the original; the CTA code word
  in UPPERCASE ("SLIDES"). Typical corrections seen in the reference: Cloud → Claude · A → IA · Gama → Gamma ·
  carrocéis → carrosséis · vim → envio · "slides" (in the CTA) → SLIDES.
- A repeated word calls for an anchor with more context (`âncora("te entregar")`, not `âncora("entregar")`), or the
  n-th occurrence (`âncora("slides", 3)`).

---

## 7 · Pieces and screens

### 7.1 Scene layers (bottom to top)
1. camera video with color grade (CSS filter + two tint layers in the `destaque` color, opacities
   0.30 and 0.25);
2. optional presenter matte (only for title behind the head, when it fits);
3. glass overlays (panels, pills, cards, lettering);
4. caption that follows the mouth.

### 7.2 Native palette (by role)

| Role | Native | Where |
|---|---|---|
| `fundo` | `#1f123d` (variants `#0e0b1e`, `#2d1f50`) | SPLIT background, panel glass |
| `texto` | `#ffffff` | lettering, titles, caption |
| `destaque` | `#8b5cf6` / `#9b63ff` | accent: glows, borders, icons, button (gradient `#8b55ff → #a47fff`) |
| `apoio` | `#b9a3ff` (lavender) | accent words in the caption and in titles |
| `acento2` | `#a59cc4` (muted) | kickers, small labels, price font |

**Native fonts:** highlight font = wide Anybody 900 (display, UPPERCASE in lettering); text font =
Plus Jakarta Sans 700/800 (text and UI); technical font = JetBrains Mono (camcorder HUD, technical labels).

### 7.3 Glass
Dark glass card: `fundo` background at ~70–80 % with background blur, 1 px border in `destaque` at ~25 %,
radius ~24 px, soft glow (`box-shadow` in the `destaque` color, no blown-out glow — see "glow without blowing out"
in the gates). The presenter card in SPLIT uses the same language, with the four corners in "L".

### 7.4 Catalog of pieces (the vocabulary of the style's generator)
Every piece receives its time by phrase anchor and, optionally, `until` (when it leaves). Colors by role.

| Piece | When it enters | Composition |
|---|---|---|
| **Camcorder HUD** `(t0, t1, {label})` | hook, first 1–2 s | desaturated camera, corners in "L", "REC" with dot, timecode in technical font, small label in the lower corner (e.g.: "NOVIDADE · CLAUDE") |
| **Glitch** `(t)` | end of the HUD | RGB shift + slices for ~0.2 s; the boom and the color grade come in |
| **Punch** `(t, scale)` | between phrases | reframes the camera on a hard cut (1.06 base; 1.14–1.20 on impact) |
| **Layout** `('split' \| 'full', t)` | start of the phrase that calls for content | animated switch of 0.45 s; hides the caption automatically |
| **Stacked lettering** `([{text, t, style}], {top, until})` | impact phrase in FULL | one line per word/group, highlight font in uppercase, `top` 1150–1180 (chest); styles `blur` / `glow` / `letters` |
| **Hide caption** `(a, b)` | together with lettering and switches | hides the mouth caption over the interval |
| **Flash** `(t, {peak})` · **Light leak** `(t, d)` | phrase turns, switches | light transition (5.4) |
| **Pill** `(text, t, {y, icon, kind, up, until})` | short statement in FULL | glass capsule with icon and glow in `destaque`, y 1250–1390; `kind: 'strike'` = struck out (for what you stop paying) |
| **Section header** `({kicker, title, acc}, t, {y, until})` | top of SPLIT | small kicker in `acento2` + title in `texto` with accent words in `apoio` |
| **Panel** `(html, t, {box, steps: [{sel, t, anim, sfx}], until})` | SPLIT (or chest, if small) | glass card with own HTML; each `step` reveals a selector on its word (price table, chat, export panel) |
| **Grid of cards** `([{img, label, icon, t}], {top, cols, w, h, gx, until})` | spoken list | cards with image + label + icon, each entering on the spoken name |
| **Typing request** `(text, t, {x, y, w, cps, send, until})` | "é só você pedir…" | chat field with the text typing and the send at `send` |
| **Progress bar** `(label, t, d, {box, until})` | "ele vai preparar…" | bar with label and percentage, filling in `d` seconds |
| **Fan** `(imgs, t, {top, w, h, until})` | "todos os slides" / carousel | 3–4 images in a fan, slight rotation, entering in cascade |
| **Stamp** `(text, t, {x, y, rot, until})` | "prontos" | rotated stamp with hit; **on the chest**, never at the top (3.6) |
| **Dashed frame** `(text, t, {box}).recebe(img, t, {w, h})` | "um roteiro" | frame with dashed border and uppercase label that receives the document when it is said |
| **Kicker** `(text, t, {y, until})` | short supporting phrase | small text in `acento2`; **on the chest**, never at y 250 (3.6) |
| **CTA button** `(text, t, {y, w, clickAt})` | final CTA | button with `destaque` gradient, cursor that clicks at `clickAt`, y 1300 |
| **Mouth caption** `({accent: […]})` | the whole video | section 6 |
| `âncora(frase, n)` · `fim(frase)` | everything | times from the transcript (n = n-th occurrence) |

**Pieces in the vocabulary that the reference did not use** (they exist in the style, available): title behind the head
(needs a matte and room above the head), HUD on the face, 3D row, logo orbit, wall of cards,
isolated logo, scrolling ticker; before/after, price tag, progress ring, DM bubble, terminal;
versus, piece explosion; and the "live editing" family (cut audio wave, comparison, style
panel, flow, comment, cursor). **Vetoed:** 3D layers with parallax.

### 7.5 The reference screens (composition of each)
- **Price panel (SPLIT, 3.2–6.1 s):** header "Quanto você deixa de pagar / Por ano, sem o Claude";
  glass table with row "Gamma Pro · R$ 840/ano" → row "Canva Pro · R$ 290/ano" → total "R$ 1.130"
  struck out → "Com o Claude · R$ 0" in `apoio`; footer with the price source (official pages, annual plan).
  Brands without a free logo enter **as text only**.
- **Grid of 3 cards (SPLIT, 6.2–8.1 s):** kicker "Elas se chamam" + title "Slides · Docs · Design";
  three cards with the illustrative image and the label with icon, each on the spoken name.
- **Chat + request (SPLIT, 11.9–16.0 s):** glass card imitating the product's chat (avatar, name, "Como posso
  te ajudar hoje?"), field with the request typing ("Crie uma apresentação comercial p…") and send button.
- **Progress → fan (SPLIT, 16.0–18.8 s):** header "Sua apresentação pronta", bar "Criando os slides"
  up to 97–100 %, then fan of 3 slides at `top` 600.
- **Export panel (FULL, on the chest, 18.8–23.9 s):** box y 1170–1470 with kicker "Exportar apresentação",
  deck thumbnail → drawn arrow → official logos (PowerPoint / Google Slides, from Wikimedia Commons).
- **"ROTEIRO" frame + carousel (SPLIT, 25.6–32.9 s):** header "Na mesma conversa / Do roteiro ao
  carrossel"; new request typing ("Agora cria um roteiro d…"); dashed frame "ROTEIRO" receives the
  document; then fan of 4 carousel slides + badge "Carrossel no Instagram" with the official logo.
- **Struck-out pills + lettering (FULL, 32.9–36.8 s):** pills "GAMMA" and "CANVA" struck out on the chest → flash →
  lettering "TUDO EM / 1 CONVERSA".
- **CTA (FULL, 36.8–38.8 s):** button "COMENTA SLIDES →" at y 1300 with cursor clicking at the onset of "SLIDES";
  kicker "Link direto na sua DM" **on the chest** (in the reference it was at y 250 and was flagged as an error).

### 7.6 Declared illustration (when there is no official screenshot)
Product screens that do not exist for capture were made in own HTML and rendered to JPG by a
headless browser (browser path via the `CHROME` variable, R10):
- palette faithful to the imitated product (in the reference: cream `#faf9f5`, terracotta `#d97757`, Inter + Source Serif —
  recreated-interface colors stay literal);
- fictional company (in the reference, a bakery), never imitating a real client;
- pieces: 4 business-proposal slides, 1 "roteiro" document, 1 design canvas and 4 carousel slides;
- every declared illustration in `assets/SOURCES.md` and in the delivery.

---

## 8 · Sound

- **Parent rule: R2** (≤ 0.85 SFX/s; whoosh only on a real scene switch; hit only on a stamp, X or impact;
  nothing on a small piece nor on a piece that enters < 0.6 s after another sound; volumes 0.1–0.2 of the voice).
- **Where the style puts sound:** only on large pieces — layout switch (whoosh), panel (short whoosh on
  entry), CTA (pop on the click), stamp (hit), glitch (boom, only in the hook). Pills, grid cards, inner panel
  steps and kickers enter **without sound**.
- **Volume and density:** the default is `"sfxModo": "enxuto"` (`template/sfx-lean.js`, decision of 28/10/2026). It
  applies R2 without touching the kit: ≤ 0.8 effect/s counting typing, as `verify.py` counts. In the test with the
  example, 31 effects remained (0.80/s) and the verification approved. The skin adjusts: intensity 0.3 → lean and −3 dB;
  0.6 → lean; 0.85 → the reference's exact sound (`"referencia"`, ≈ 1.4/s, which fails the verifier's SFX
  item); effects off → no sound besides the voice.
- **Boom:** once, on the hook's glitch.
- **Typing:** in the typing request, natural sample at ~9 keys/s, continuous over the stretch, ≈ 12 dB below
  the voice (R2).
- **Soundtrack:** the reference has no music track; only voice + SFX. If a track enters, it stays ≥ 13 LU below the voice.
- **Source of the sounds:** `template/kit/sfx/` (procedural effects generated by `template/tools/generate-sfx.mjs`, no third-party license).
- **Count per second** checked at build before the render (gate 8 of section 11).

---

## 9 · Skin

**What the skin swaps** (`skin.json`): the two fonts (highlight / text) and the five color roles (fundo, texto,
destaque, apoio, acento2). The button gradient derives from `destaque` (from `destaque` to `destaque` 20 % lighter);
the two tint layers over the camera use `destaque` at opacities 0.30 and 0.25.

**What stays fixed, whatever the skin:**
- the face color filter (`saturate(1.04) contrast(1.05) brightness(0.97)`) and the tint ceiling 0.3 (R4);
- the HUD's technical font (native: JetBrains Mono) — it is part of the hook's signature;
- the recreated-interface colors (product chat, illustrations) — faithful to the product;
- the official logos (never recolored);
- the geometry: punch, positions, tops, safe zone, durations and easings.

**Mood:** dark. The style was calibrated for a dark studio with colored light; with a light or neutral raw,
the grade may go up **only with a before × after shown and approved** (`attachments/color-before-after.jpg` is the
example of what "aggressive" × "soft" means).

---

## 10 · Step-by-step pipeline

### 10.0 With the bundled engine (the default path)
```bash
S=${REEL_SKILL:-~/.claude/skills/reel}; cd <P>
cp -R "$S/template" motor && cd motor
bash prepare.sh      # 9:16 camera (cut/clean-916-grade.mp4) + voice (cut/cut.wav), transcript (preparo/palavras.json),
                      # skin fonts, material from assets/oficiais, npm install, mouth tracking, 1st assembly
```
Then, the sequence of phases 1 and 2 of `template/README.md`:
- **Phase 1:** transcript checked → `vsl.json` measured → material + SOURCES → `assets/map.md` → `src/beats.js` →
  `node assemble.mjs` + lint → `../entrega/plan.json` → `node tools/cards.mjs`.
- **Phase 2:** snapshots → safe zone → render → camera-only → `tools/final-audio-vsl.sh` → `sounds.json` → sheet → `verify.py`.

`assemble.mjs` applies the skin (`skin-resolved.json`): colors → kit variables; fonts → `fontes.css`; sound → mode and
volume. With the native skin, the result has the reference's colors. Steps 10.1–10.13 below detail each stage and the
criteria.

### 10.1 Cut (cut engine `cut/`, 4-frame J/L on)
- **In:** the raw (horizontal or vertical).
- **Out:** `clean.mp4` (30 fps, keyframe every 1 s — `-g 30`), `cut.wav`, `cut16k.wav`, `edl.json`,
  `cut_words.json`.
- **Criterion:** no clipped word (each splice checked by windowed transcription), no pause
  > 0.35 s, last correct take of each phrase (R5). Illustrative example of what the sound-based cut clips in fast
  speech and needs to be protected: "economizar", "pedir pra ele", "pro seu negócio", "um roteiro",
  "carrosséis no" — each became a protected interval of the raw, and the cut ran again.

### 10.2 9:16 crop
- **In:** `clean.mp4` + `edl.json` (to read the raw at full resolution when the raw is horizontal).
- **Out:** `assets/clean.mp4` 1080×1920 with the center of the horizontal cropped, 30 fps, keyframe every 1 s and the voice
  from `cut.wav` (done by `template/prepare.sh`).
- **Criterion:** whole face in the frame; the chosen base punch (1.06) does not crop the head or the chin.

### 10.3 Transcription and correction
- **In:** `clean.mp4` (or `cut16k.wav`) → `tools/prepare.py <video> <folder>`.
- **Out:** `palavras.json` (word by word with times), pauses > 0.4 s, `meta.json`; plus a legible `words.txt`
  (words with times and pauses) for reading the map.
- **Criterion:** transcript corrected by hand (R6) with the original kept in `transcript-raw.json`; the
  correction is by time when the word repeats; the CTA code word in uppercase.
- Format the generator reads: `{"words":[{"text","start","end"}],"audio_duration_secs"}`.

### 10.4 Face
- **Caption that follows the mouth:** `template/tools/track-mouth.py` (MediaPipe with `VSL_PYTHON` + `FACE_MODEL`;
  without MediaPipe, OpenCV) generates `assets/face-track.json`, which the kit reads (`K.mouthCaps`). `prepare.sh` already runs it; without
  it, there is no caption.
- **In:** `clean.mp4` → `tools/face.py <video> <folder>` (measurements for the framing).
- **Out:** `face.json` per keyframe (top of head, chin, center, width) + framing suggestions.
- **Criterion:** face box and head point measured **with the punch applied**; decision recorded: title
  behind the head on only with ≥ ~300 px free above the head.

### 10.5 Matte (optional)
- **In:** `clean.mp4` → `tools/crop.py <video> <folder>` (model via the `RVM_MODEL` variable).
- **Out:** presenter `matte/`.
- **Criterion:** only runs if step 10.4 freed a title behind the head; otherwise, skip (in the reference the matte was
  generated and was not used).

### 10.6 Research and materials (mandatory before the beats)
- **In:** the corrected transcript — each claim and each number said.
- **Out:** `assets/SOURCES.md` (file, origin, URL, license, lookup date); `assets/img/` with official
  logos and screenshots; `assets/mock/` with the declared illustrations (own HTML → JPG).
- **Criterion (R3):** each fact with an official page; each price with an official pricing page, currency and period;
  logos from Wikimedia Commons or brand as text only; CAPTCHA never bypassed (read the page in a normal
  browser); speech and screen in different currencies checked and flagged in the delivery (in the reference: speech
  "centenas de dólares", screen "R$ 1.130/ano" ≈ US$ 200 — consistent, flagged).

### 10.7 Beat map
- **In:** `words.txt`, `face.json`, `SOURCES.md`.
- **Out:** `assets/map.md` — table time × speech × camera × piece (template in section 12).
- **Criterion:** something new every 1.5–3 s; layout proportion near the target; no piece planned for the
  top of the frame if 10.4 did not free it. **Show the map before assembling**, unless the request says to go
  straight ahead.

### 10.8 Composition (bundled engine + `npx hyperframes`)
- **In:** the map, the framing parameters (3.1), the transcript.
- **Out:** the project's HTML composition, with one piece call per map line.
- **Criterion:** `npx hyperframes lint` with 0 errors. The engine (`template/kit/kit.js`) already meets the requirements
  below, except those marked ⚑, which are the responsibility of whoever writes `beats.js`:
  - every entry anchored to a transcript phrase; **nonexistent phrase throws an error** (never falls to time 0);
  - n-th occurrence and phrase end available;
  - ⚑ mouth caption hidden on every layout switch (`K.hideMouth(t − 0.05, t + 0.5)`) and on every lettering
    on the chest (`K.hideMouth` over the `K.stack` interval) — as in `template/example/beats-example.js`;
  - ⚑ title behind the head only when 10.4 freed it; kicker and stamp on the chest (the example has them at the top of
    the head — see `template/example/READ-FIRST.md`, "what to fix");
  - SFX in lean mode by default (section 8), which prints the per-second count to the console;
  - base punch read from `vsl.json` (measured per video), never fixed.
  - Lesson: a snapshot with no overlay at all = broken anchor; open the composition in the browser and read the console.

### 10.9 Snapshots and safe zone
- **In:** the composition.
- **Out:** `npx hyperframes snapshot` at each beat and each layout switch → `snapshots/`;
  `tools/safe-zone.py <video>` (sweep every 0.25 s).
- **Criterion:** face free in all frames (R1); nothing cut off; nothing overlapping (coinciding tops in
  SPLIT); legible text; glow without blowing out; safe zone OK (x 90–990, y 220–1520, nothing in the button column).

### 10.10 Render and color
- **In:** the approved composition → `npx hyperframes render -q high -o renders/<slug>-render-bruto.mp4`.
- **Out:** the raw render (comes out at ~−25 LUFS).
- **Criterion:** color within R4 (the `gradeFilter` and tints in `vsl.json` are already the approved values);
  a stronger grade only with an approved before × after.

### 10.11 Final audio
- **In:** the raw render → `bash tools/final-audio-vsl.sh <raw> <output>` (in the engine folder).
- **Out:** `render/reel-vN.mp4` at −14 LUFS (±0.3), true peak ≤ −1 dBTP, image copied (`-c:v copy`), AAC 192 kbps
  48 kHz, `+faststart`.
- **Criterion:** the kit's effects have fast attacks. The skill's common `final-audio.sh` (linear loudnorm +
  limiter at 0.94) left the peak at +1.2 dBTP in this style. The style's finish uses gain + limiter at
  192 kHz, with the gain calibrated in up to 3 passes. In the test it gave −14.3 LUFS and −0.92 dBTP.

### 10.12 Verification and delivery
- **In:** the final → `tools/verify.py <folder>`.
- **Out:** `VERIFY.md` with duration, LUFS and peak, words protected in the cut, caption corrections, lint,
  safe zone, what was fixed in the snapshots, frame sheet of the final and open points.
- **Criterion:** all gates of section 11. **Never publish or send the video.**

### 10.13 Environment
Everything isolated by environment variable (R10): `WHISPER_PYTHON`, `FACE_MODEL`, `RVM_MODEL`, `CHROME`. Nothing
written to the user's global folders. Problems already seen: transcription "finishing" with no file → pin
`av==16.1.0`; snapshot breaking with a postcss error → `npm ci` at the root; nonexistent cache folder → create it
before downloading.

---

## 11 · Numeric acceptance (gates — nothing is delivered without passing)

| # | Gate | Target |
|---|---|---|
| 1 | Cut | all splices checked; no clipped word; no pause > 0.35 s |
| 2 | Caption | transcript corrected (product names, acronyms, code word in uppercase); original kept |
| 3 | Facts | each claim and each number with a source in `SOURCES.md`; illustrations declared; currencies checked |
| 4 | Lint | `npx hyperframes lint` = 0 errors |
| 5 | Snapshots | 1 per beat + 1 per layout switch: face free · nothing cut off · nothing overlapping · legible text · glow without blowing out |
| 6 | Safe zone | `tools/safe-zone.py` = OK (x 90–990 · y 220–1520 · nothing at x > 940 ∧ y > 1150), sweep every 0.25 s |
| 7 | Color | filter `saturate(1.04) contrast(1.05) brightness(0.97)`, tints ≤ 0.3 / 0.25 — or approved before × after |
| 8 | SFX | ≤ 0.85/s; overall volume ~0.4; only large pieces; nothing < 0.6 s after another sound |
| 9 | Audio | −14 LUFS (±0.5); peak ≤ −0.5 dBFS; image not re-encoded |
| 10 | Motion | layout switches at 0.45 s `power3.inOut`; entries 0.22–0.5 s; something new every 1.5–3 s |
| 11 | Sync | each piece at the onset of the anchored word (tolerance: 1 frame); no piece before the word |
| 12 | Duration · format | 1080×1920 · 30 fps · 35–45 s |
| 13 | `VERIFY.md` | written, with evidence; video **not** published or sent |

---

## 12 · Production lessons

### 12.1 The fixes that made the result "approved"

**L-1 · Real material.** No generic screen or invented number. Research is a mandatory step of the
pipeline (10.6), before writing the beats. Priority: official screenshot/logo → Commons → declared illustration
with a fictional company. CAPTCHA is never bypassed: switch tools.

**L-2 · Soft color.** The origin style's default grade was calibrated to "make it purple" and, on top of
a studio that is already dark with colored light, it darkened and oversaturated the face.

| Parameter | Origin default (rejected) | **Approved** |
|---|---|---|
| color filter | `saturate(1.08) contrast(1.2) brightness(0.8)` | `saturate(1.04) contrast(1.05) brightness(0.97)` |
| tint 1 | 0.85 | **0.30** |
| tint 2 | 0.55 | **0.25** |

Start from the approved values. Only raise the grade with a light or neutral raw, and show the before × after before
rendering. The identity color comes from the screens, pills and glows, not from painting the face.

**L-3 · Face never covered.** Lettering and pills on the chest, heavy content in SPLIT. The exceptions that
appeared and were flagged: small top kickers (y 250) touching the hair and the "PRONTOS ✓" stamp
(x 600, y 300) hitting the top of the head → both to the chest. Mandatory face check in all
snapshots; a frame with anything over the face fails.

**L-4 · Title behind the head does not work with a high head.** The origin style's mark became illegible
because the head covered almost everything. Solution: stacked lettering on the chest (`top` ~1150) with the mouth caption
hidden over the same interval. Rule: measure the top of the head; < ~300 px free → turn off the title behind.

**L-5 · Fewer sound effects.** The automatic SFX of each piece, at 0.55, went past the mark. SFX only on large
pieces, volume ~0.4, per-second count at build.

### 12.2 Technical fixes along the way

| Symptom | Cause | Fix |
|---|---|---|
| Transcription "finishes" without generating a file | new `av` library incompatible with the transcriber | pin `av==16.1.0` in the environment |
| Words clipped in the cut | the voice detector discards weak starts/ends in fast speech | protect the raw interval + check each splice by windowed transcription (cut engine, `cut/`) |
| 0.44 s pause that remained | protected interval too wide | shorten the interval and cut again |
| Title behind the head illegible | high head in the frame | lettering on the chest (L-4) |
| Fan of slides on top of the progress bar | tops coinciding in SPLIT | fan moved down to `top` 600 |
| Caption leaking on the FULL → SPLIT switch (25.7 s) | the caption follows the frame shrinking | hide the caption from `t − 0.05` to `t + 0.5` on every switch (automatic in the generator) |
| Safe-zone sweep flagging text | caption in the transition | the same hiding |
| Snapshot with no overlay at all | phrase anchor threw an error (phrase does not exist) | open in the browser, read the console, anchor with more context |
| Snapshot breaks with a postcss error | corrupted `node_modules` | `npm ci` at the root |
| Audio at −25 LUFS | the render does not normalize | two-pass loudnorm (10.11) |
| ffmpeg filter broken in zsh | `$var:l` is a zsh modifier | `${var}` |
| CAPTCHA in the headless browser | the site's anti-bot protection | normal browser, no bypass |
| Piece vanishes in the render | animation of only `scale`/`scaleX` | include `opacity` in the destination |
| Lint fails the animation | animating `left` | animate with `x` |
| Anchor catches the wrong word | repeated word | more context in the phrase or n-th occurrence |
| Slow seek / wrong frame in the clean video | few keyframes | `clean.mp4` with keyframe every 1 s (`-g 30`) |

### 12.3 The reference's real map (38.8 s) — template of `map.md`

| Time | Speech | Camera | Piece |
|---|---|---|---|
| 0.0–1.0 | "O Claude acabou de lançar" | FULL raw | camcorder HUD "NOVIDADE · CLAUDE" → glitch + boom |
| 1.0–2.1 | "três ferramentas de IA" | FULL, punch 1.14 | lettering on the chest: 3 FERRAMENTAS / DE IA |
| 2.1–3.2 | "totalmente gratuitas" | FULL | flash + TOTALMENTE / GRATUITAS + pill "Em todos os planos · até no Free" |
| 3.2–6.1 | "economizar centenas de dólares por ano" | SPLIT | panel: Gamma Pro R$ 840 → Canva Pro R$ 290 → total R$ 1.130 struck out → "Com o Claude R$ 0" + price source |
| 6.2–8.1 | "Slides, Docs e Design" | SPLIT | 3 cards, each on the spoken name |
| 8.1–10.6 | "ficam dentro do chat que você já utiliza" | light leak → FULL | pill "Dentro do chat do Claude" |
| 10.6–11.9 | "E pra utilizar é muito fácil" | FULL, punch 1.16 | kicker "É muito fácil" (on the chest) |
| 11.9–16.0 | "é só você pedir… apresentação comercial pro seu negócio" | SPLIT | chat + request typing |
| 16.0–18.8 | "ele vai preparar todos os slides" | SPLIT | bar "Criando os slides" → fan of 3 slides |
| 18.8–23.9 | "slides prontos… exportar… PowerPoint ou Google Slides" | FULL | stamp PRONTOS ✓ (on the chest) → panel on the chest: deck → drawn arrow → logos |
| 23.9–25.6 | "Mas a novidade não para só nos slides" | FULL, punch 1.2 | lettering NÃO PARA / SÓ NOS SLIDES |
| 25.6–32.9 | "mesma conversa… roteiro… carrosséis no Instagram" | SPLIT | new request → ROTEIRO frame receives the doc → carousel fan + Instagram badge |
| 32.9–36.8 | "em vez de pagar pelo Gamma ou pelo Canva… tudo em uma única conversa" | FULL | struck-out pills GAMMA / CANVA → flash → TUDO EM / 1 CONVERSA |
| 36.8–38.8 | "Comenta SLIDES e eu te envio o link" | FULL | CTA button with cursor + kicker "Link direto na sua DM" (on the chest) |

The writing flow is always: **first the map** (time × speech × camera × piece), **then** the generator
code, with piece calls only — one per map line.

### 12.4 What became the standard of this style (differences from the origin)
- color filter and tints at the approved values (L-2);
- punch measured per video (1.06 in the reference framing);
- SFX at 0.4 and only on large pieces (L-5);
- title behind the head turned off automatically with a high head; lettering on the chest (L-4);
- kicker and stamp never over the head: default on the chest (L-3);
- mouth caption hidden automatically on every layout switch;
- research of facts and materials as a mandatory step before the beats, with `SOURCES.md` and the generator of
  declared illustrations as a piece of the style;
- automatic splice checking (already in the cut engine, `cut/`);
- audio normalization as the final render step;
- face check in the snapshots;
- paths isolated by environment variable;
- ask or show the beat map before assembling, when the request does not say to go straight ahead.
- Out of this style's scope: the light look and the AI video generation part of the origin (they become
  separate styles).

---

## 13 · Attachments

| File | What it shows |
|---|---|
| `attachments/frames-01.png` | board with 16 frames of the approved reference reel: the hook's camcorder HUD, lettering on the chest (3 FERRAMENTAS / DE IA, TOTALMENTE / GRATUITAS), SPLITs with grid of cards, chat + request typing, progress bar, ROTEIRO frame and carousel fan, export panel on the chest, pill "Dentro do chat do Claude", lettering NÃO PARA / SÓ NOS SLIDES and TUDO EM / 1 CONVERSA, and the CTA button |
| `attachments/color-before-after.jpg` | the same frame with the origin grade (aggressive, dark) × the approved grade (soft), and a SPLIT with the price panel beside it — the visual reference for rule R4 in this style |

Both images are renders of the reference project itself (no third-party video frame).

## 14 · Engine, template and example (what is in the `template/` folder)

| Path | What it is |
|---|---|
| `template/README.md` | the step by step of phases 1 and 2 with this engine (what the agent brief says to follow) |
| `template/kit/` | the approved reference's engine, untouched: `kit.js` (`K.*` kit), `kit.css` (themes and geometry), `index.template.html`, `fonts/`, `sfx/` (procedural effects, no third-party license). GSAP 3.14.2 comes from `npm` |
| `template/assemble.mjs` | assembles `index.html` from `src/beats.js` + transcript + `vsl.json` + mouth tracking + skin + sound; `--camera-only` generates the camera-only base |
| `template/prepare.sh` | 9:16 camera with the voice, transcript, fonts and project material, `npm install`, mouth tracking, 1st assembly |
| `template/vsl-default.json` | the initial `vsl.json` of every new video (approved color and grade; framing to measure) |
| `template/beats-template.js` | the initial `beats.js`: grammar, rules and commented recipes |
| `template/sfx-lean.js` | the lean mode filter (R2) |
| `template/package.json` | `hyperframes` 0.7.109 (the reference's version), `gsap` 3.14.2, `playwright` |
| `template/tools/` | `track-mouth.py`, `cards.mjs` (phase 1 cards), `sounds.mjs` (`sounds.json`), `final-audio-vsl.sh` (−14 LUFS, peak ≤ −1 dBTP), `sheet.sh` (final's sheet), `safe-zone-dom.mjs`, `illustrations/`, `generate-sfx.mjs` |
| `template/example/` | the complete approved reel (`READ-FIRST.md`, `beats-example.js`, map, sources, images, `progress-example.md`, video at 540p) |

**Fidelity test (28/10/2026):** the example reassembled with `assemble.mjs` generated an `index.html` byte-for-byte identical to the
reference's. Of 18 frames compared, 17 came out pixel-identical and 1 with a PSNR of 72 dB.
