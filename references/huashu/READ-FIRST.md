# huashu-design: what came in and what was left out

Source: alchaincyf/huashu-design, commit 4fc7bfd (2026-10-23), MIT (relicensed on 2026-05-14; before that it had a personal-use license). Original text in Chinese, preserved; the integration lives in the designer-mestre modules, at the points below. License in `assets/huashu/LICENSE`.

| File | What it is for here | Where it is called |
|---|---|---|
| `brand-asset-protocol.md` | Brand assets before color and font: ask, search the official source, download, check, record | `kv-logo.md` Part A §1.1 |
| `workflow.md` | Five questions per piece; alignment flow before producing | `ads.md` §1 |
| `directions.md` | Three real directions with six thumbnail candidates | `references/alternatives.md` (alternative output) |
| `tweaks-system.md` | Idea of the live adjustment panel; the plain-JS version is `assets/preview_adjustments.js` | `html.md` §3 |
| `pptx-from-rendered-html.md` | HTML deck ready for editable PPTX, reading the render | `deck.md` §3 |
| `storyboard-basics.md`, `camera-language.md`, `animation-pitfalls.md`, `animation-best-practices.md`, `ui-demo-animation.md`, `gsap-recipes.md`, `video-export.md` | Production script for animation and video | `video.md` Part C |

Scripts in `assets/huashu/`: `pptx_from_rendered.py` (tested with a 2-slide HTML deck: 4 text boxes, 1 shape, no lost text; needs `-X utf8` on Windows), `convert-formats.sh` (GIF recipe), frames and cursor in JSX (framework path).

## Not incorporated
- **Audio:** the 6 BGM tracks and the sound effects (`assets/*.mp3`, `assets/sfx`): the project does not state their license.
- **PPTX route by rewriting** (`html2pptx.js`, `export_deck_pptx.mjs`, `editable-pptx.md`): requires writing the HTML with 4 restrictions (no gradient, no background on text); contradicts pixel-perfect and duplicates the render route.
- **Video renderers** (`render-video.js`, `render-video-seek.js`): duplicate `assets/export_motion.py`, which already does frame-by-frame rendering with `window.__render(t)`.
- **Global taste memory** (`learn.py`, `~/.huashu-design/`) and **ledger in a global file** (`design_lint.py ledger`): conflict with per-client memory and with Law 2; the equivalent is the client's `historico.md`.
- **Hook** `design-gate-hook.sh`: persistent configuration.
- **Multi-file deck architecture with an overview wall, 1920×1080** (`deck_stage.js`, `deck_index.html`): `deck.md` uses 1600×900 in a single file.
- **Watermark** "Created by Huashu-Design" (text of `video-export.md`): third-party credit does not enter the client's piece (`operations.md` §6).
- **Cloud:** `scripts/cloud/*` (AI video review, third-party TTS): require a key.
