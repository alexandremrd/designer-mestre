# Progress of the reference reel (approved) — the path that led to the result

**Video:** "3 ferramentas grátis do Claude". The raw footage is horizontal, 2560×1440 and 40.9 s, in a dark studio with
colored light. The final is 38.8 s at 1080×1920, at −14 LUFS. Screens: 15 beats, with FULL and SPLIT near 50/50,
no PIP.

## 1 · Cut
Sound-based cut with 4-frame J/L. The cut clipped syllables in fast speech in five places: "economizar",
"pedir pra ele", "pro seu negócio", "um roteiro" and "carrosséis no". Each became a protected interval of the
raw footage, and the cut ran again. Every splice was checked by windowed transcription. Two natural
pauses remained (0.31 s and 0.29 s).

## 2 · Transcript (R6)
Corrections made by hand:

| Whisper | Correct |
|---|---|
| Cloud | Claude |
| A | IA |
| Gama | Gamma |
| carrocéis | carrosséis |
| vim | envio |
| slides | SLIDES (the CTA code word) |

## 3 · Framing
The face takes up a lot of the frame, so the base punch was 1.06, not 1.22. `face`/`head` were measured on a frame with
the punch applied. The top of the head sits almost at the top of the frame: the title behind the head became illegible and turned into
lettering on the chest (`K.stack`, top 1150–1180) with `K.hideMouth` over the same interval.

## 4 · Real material (R3)
- **Facts:** "grátis em todos os planos, até no Free" and "exporta para PowerPoint e Google Slides", both on official
  pages, with the date noted.
- **Prices:** on the official pt-BR pricing pages, annual plan (Gamma Pro R$ 840, Canva Pro R$ 290).
  - The page had anti-bot: read in a normal browser, never bypassed.
- **Logos:** from Wikimedia Commons. A brand without a free logo entered as text only.
- **Product screens:** there was no official capture, so they became an illustration in own HTML, with the fictional company
  "Padaria Trigo & Mel" (slides, document, design canvas, carousel), declared in SOURCES.
- **Currencies:** the speech says "centenas de dólares" and the screen shows R$ 1.130/year (≈ US$ 200). It is consistent, and it was flagged.

## 5 · Map → beats
See `map.md` and `beats-example.js`. For each line of speech, the piece that shows the idea:
- **Hook:** HUD "NOVIDADE · CLAUDE" → glitch.
- **Price:** panel with the lines revealed on the word, the struck-out total and "Com o Claude R$ 0".
- **List:** 3 cards, each on the spoken name.
- **Request:** chat + request typing → "Criando os slides" bar → fan of slides.
- **Export:** panel on the chest with a drawn arrow and logos.
- **Turn:** lettering on the chest.
- **Old × new:** struck-out pills → flash → "TUDO EM 1 CONVERSA".
- **CTA:** button with cursor.

The caption follows the mouth, with the keywords in `accent`.

## 6 · Verification
- Lint came out with 0 errors, and snapshots were taken at every beat and every camera switch.
- Snapshots fixed along the way:
  - the fan of slides was over the progress bar and moved down to top 600;
  - the caption leaked on the FULL→SPLIT switch at 25.7 s, and `K.hideMouth(t − 0.05, t + 0.5)` went in.
- The safe zone was swept every 0.25 s and came out OK.
- The render came out at −25 LUFS. Two-pass normalization brought it to −14 LUFS, with peak −0.6 dBFS.

## 7 · The fix that made the result "approved"
The first version had the source's color grade, which was too aggressive and dark on the face: contrast 1.2,
brightness 0.8, tint 0.85/0.55. The approved version uses `saturate(1.04) contrast(1.05) brightness(0.97)` with tint
0.3/0.25. The purple stayed in the screens and the glows; the face stayed natural.
