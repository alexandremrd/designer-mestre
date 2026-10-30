# Catalog of scripts and engines

Index of everything the skill executes. Look here before creating a new function: if the result already exists, extend the owning script. The **Formerly** column helps find old links (client notes, scripts from past deliveries). The scripts run from the skill folder; brand data comes from the client card (`_DESIGN\mapa.md`, template in `Clients\_CLIENT_TEMPLATE\mapa.md`).

## Skill scripts (`assets\`)

| Script | What it does | Triggered by | Formerly |
|---|---|---|---|
| `skill_alerts.py` | Shows in up to 4 lines what needs attention: open and overdue pending items from `EVOLUTION.md`, `verify_package.py` failure, and incomplete client card; silence if nothing | core §0, end of session | (new) |
| `client_card.py` | Reads the client card (`_DESIGN\mapa.md`): fonts, colors, paths, Reels template. Run it with the delivery folder to check. | all assembly scripts | (new) |
| `gpu_acceleration.py` | Chooses the graphics card (NVENC, accelerated Chromium), falls back to the CPU on its own and states the reason; `profile` shows the machine's tier and the choice for each task; `preparar_cuda` finds the CUDA DLLs | `export_motion`, `caption_reels`, `assemble_reels`, cut engine | `gpu.py` |
| `preview_adjustments.js` | Live adjustment panel (color, size, density) in the preview | `html.md` §4 | `tweaks.js` |
| `apply_label.py` | Pastes the real label artwork (PDF) onto a cylindrical bottle in a scene | `image-product.md` §5 | — |
| `base_deck.html`, `base_lp.html` | Starting points for a 1600×900 deck and a single-file LP | `html.md` §8 and §2 | — |
| `check_deck.py` | Checks the HTML deck (structure, file contract) before delivering | `html.md` §8.5 | `validate_deck.py` |
| `check_export.py` | Checks the exported file: format, color, audio, dimensions | `quality.md` §K | — |
| `check_html.py` | Checks the HTML page: non-ASCII bytes, single file, placeholders, SEO, images without alt text, horizontal scroll, screen captures | `html.md` §9 | `qa_html.py` |
| `check_image.py` | Visual checking tools: contrast between colors, comparison board, palette of an image, preview × Figma parity, object bounding-box crop | `quality.md` §G | `img_qa.py` |
| `check_video.py` | Checks the MP4 before showing: format, frame 0, pauses, animated entrance and exit | `video.md` §8 | `gate_video.py` |
| `consent.py` | Records and queries the user's one-time "yes" per capability | `operations.md` §0.6, `html.md` | — |
| `export_motion.py` | Exports the approved HTML motion: MP4, screens, and source file | `video.md` §6 and §7 | `motion_export.py` |
| `generate_audio.py` | Voiceover and sound effects via voice API | `video.md` §3 | — |
| `generate_image.py` | Generates an image through the available engine, upscales and logs it in `IA\` | `image.md` Part A | — |
| `caption_reels.py` | Captions, overlay, and closing on already-cut video; syncs captions; transcribes on the GPU with `--whisper-engine auto` (faster-whisper large-v3-turbo, whisper.cpp as reserve) and caption `--style` | `video.md` §6.2 | `reels_legenda.py` |
| `product_mask.py` | Finds the product in the original and returns the mask for cutout and treatment | `treat_image.mjs` | — |
| `local_engine.py` | Analyzes the PC, installs and starts the local image generator (with the user's approval) | `image.md` Part A | — |
| `resources.py` | Registry of the resource root paths and **catalog** of what the skill uses: `catalog` (installed, real size, what is missing), `explain <chave>` (the short download question), and `outside` (what stayed outside the root) | all; `operations.md` §0.7 | — |
| `run_reel_cut.ps1` | Runs a script of the Reels cut engine with the right environment | `video.md` | `reel_run.ps1` |
| `treat_image.mjs` | Last resort without a generator: frames, upscales, and composes an existing image | `operations.md` §0.6 | — |
| `verify_package.py` | Checks whether the package can go to Git: no client name, no generated file, rules without dates, lean Laws, and correct `.gitignore` | `MAINTENANCE.md`, after every skill edit | (new) |
| `form-validation.js` and `.css` | Form validation: mask, UTMs, error states | `html.md` §5 | `validacao-forms.*` |

## Reels assembly (`assets\reel_assembly\`, README there)

| Script | What it does | Formerly |
|---|---|---|
| `assemble_reels.py` | Assembles the Reels: captions, zoom, frame, pieces, sounds, and audio at −14 LUFS | `reel_matriz\build_reel.py` |
| `render_frames.py` | Generates the animated pieces frame by frame | `render_frames.py` |
| `check_safe_zone.py` | Warns of a piece that invades the Reels safe zone | `zona_segura.py` |
| `generate_html_preview.py` | Single-file HTML preview for approval | `previa_html.py` |
| `pieces_template.html` | Ready-made pieces (numeral, ring, signboard, pills, click callout) | `overlay.html` |
| `reels_script_example.json` | Template of a video's data (highlights, zoom, effects) | (new) |

The whole folder was called `reel_matriz` and held the assembly of a client's video; it is now universal.

## Engines (third-party code: keep the original name, to receive updates)

| Engine | What it does | Activated by |
|---|---|---|
| `engines\uiux` (`search.py`, `design_system.py`) | Searches styles, palettes, typographies, and design systems of reference brands | `html.md`, `kv-logo.md`, `quality.md`, core §3 |
| `engines\reel` | Cut and edit engine for spoken video: cuts, effects kit, style rules | `video.md` |
| `engines\designlang` | Extracts tokens and design language from a site (color, type, spacing) | `html.md` §6.4 |
| `figma_engine` | Assembles native layout in Figma Desktop through granular tools | `figma.md` Route B |
| `assets\taste` (`draw.mjs`, `assets.mjs`) | Draws visual directions and downloads assets for LP and series | `ads.md` §3, `html.md` §3 |
| `assets\huashu` | Presentation conversions and export (HTML to PPTX) | `html.md` §8.4 |
| `assets\logo` | Method and scripts for a new logo and SVG checking | `kv-logo.md` Part B |

## Tools without a GPU path (declared exception of U13)
| Tool | Why it runs on CPU |
|---|---|
| `treat_image.mjs` | uses `sharp` (libvips), which has no GPU acceleration; it is the last resort without a generator |
| `product_mask.py` | CPU OpenCV template matching; the whole image is processed at once and the task is short |
| `check_*` (`deck`, `export`, `video`), `client_card.py`, `verify_package.py`, `skill_alerts.py` | light analysis of text, files, and frames with Pillow, numpy, or stdlib |
| `ffmpeg` filters of `assemble_reels.py` (scale, composition) | run on CPU; the encode goes to NVENC. Moving the scale to the GPU is a pending item |
