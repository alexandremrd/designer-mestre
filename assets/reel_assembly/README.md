# montagem_reels · spoken video inside the client template

Assembles the Reels of a spoken video when the client has an **approved template** (frame, gradient, logo, opening and closing) that cannot be redrawn: the cut and the motion pieces go on top of it. Everything about the brand comes from the **client card**; everything about the video comes from the **video script**. Neither lives in the skill.

## Where each piece of data comes from

| Data | Where it lives | Who reads it |
|---|---|---|
| Fonts, colors, template, safe zone | `D:\Clientes\[Cliente]\_DESIGN\mapa.md` (template: `Clients\_CLIENT_TEMPLATE\mapa.md`) | `client_card.py`, finding the client folder by itself from the delivery |
| Highlighted words, zoom, sound effects, durations | `<entrega>\Trabalho\reel\reels_script.json` (template: `reels_script_example.json`) | `assemble_reels.py` |
| Animated pieces | `<entrega>\Trabalho\reel\pieces.html` (template: `pieces_template.html`) | `render_frames.py`, `check_safe_zone.py` |
| Clean cut and timed words | `<entrega>\Trabalho\reel\cut\clean.mp4` and `cut_words.json` | all |

The scripts run from here, from the skill folder; the delivery only holds the video's data. A missing card or field produces an on-screen warning and uses a neutral value: it never swaps a brand font or color silently.

## Scripts

| Script | What it does | Card keys it uses |
|---|---|---|
| `client_card.py` (in `assets\`) | Reads `_DESIGN\mapa.md` and returns fonts, colors and paths. Run it with the delivery folder to check what was read. | all |
| `assemble_reels.py` | Assembles the Reels in stages: `captions` (1 to 3 words, highlight in the brand color) · `quadros` · `body` (zoom, gradient, frame, pieces, caption; NVENC) · `sounds` (effects by voice peak) · `closing` · `finalize` (joins and adjusts the audio to −14 LUFS) | `Fonts`, `Caption font`, `Caption color`, `Caption accent color`, `Reels template - ...` |
| `render_frames.py` | Generates the animated pieces frame by frame (30 per second, transparent PNG). `tempos` mode generates only instants to check. | colors, `Fonts`, `Title font`, `Text font` |
| `check_safe_zone.py` | Sweeps the video every 0.1 s and warns which piece invades the safe zone | `Reels safe zone` (default x 90–914, y 240–1470) |
| `generate_html_preview.py` | Single-file HTML preview (video and audio embedded) for the user to approve before the final MP4 | `Background color`, `Strong text color`, `Accent color`, `Caption font` |
| `pieces_template.html` | Ready-made pieces: numeral, number with ring, signboard, pills, connected dots, struck-out item, letter-by-letter phrase, glow, callout with cursor and click | colors and fonts go in the `/*FICHA_DO_CLIENTE*/` marker |
| `reels_script_example.json` | Template of a video's data | — |

## Steps
1. Make the cut (engine `engines\reel`, via `assets\run_reel_cut.ps1`) and the **approved beat grid** (`video.md` §5).
2. Check the card: `python assets\client_card.py "<delivery folder>"`. Something missing? Ask the user or fill in the client's `mapa.md`.
3. Copy `pieces_template.html` to `<entrega>\Trabalho\reel\pieces.html` and `reels_script_example.json` to `reels_script.json`; rewrite both with the times from `cut\cut_words.json` (anchor = moment the word is spoken).
4. Check instants with `render_frames.py --delivery "<folder>" tempos 1.0 7.5` and the safe zone with `check_safe_zone.py`; a piece never over the face (measure the chin; with zoom, pin the chin).
5. Run `assemble_reels.py --delivery "<folder>" --output "Exportados/Entrega #N - Reels - 1080x1920_V2.mp4" tudo`; generate the preview with `generate_html_preview.py` into `Aprovação\`; then `check_video.py` and the transcription of the final audio.

Template contract: the file indicated in `Reels template - closing` must expose `end(saida, ultimo_quadro, D)`, which creates the closing video from the last frame.

Lessons: paths with brackets require `-LiteralPath`; raw voice has ~23 dB of dynamics, so light compressor + limiter reach −14 LUFS; glass plate behind text over light clothing.
