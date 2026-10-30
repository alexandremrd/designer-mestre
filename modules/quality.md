# Quality Module — Final Check by Type and Execution Risks
Read only the section for the delivery type; the **correction unit, source of truth and board** of each type are in the cycle of `delivery.md` §2. A new static creative opens §§A and H after render; U6–U8 remain the base standards, and this review is the independent concept and craft gate. The KV beats any rule here. Offline lookup: `python engines\uiux\scripts\search.py "<topic>" --domain ux|typography|color|landing|chart|brand -n 3`. Local tools: `assets\check_image.py` (§G).

## A. Review of generic artifacts and execution risks (every piece)
**P0:** U6 of the core.

Use these signals to locate problems, **not as a blacklist nor automatic rejection**. Complexity, centering, multiple focal points, expressive typography, chrome, bokeh, intense color, decorative UI and texture can be valid decisions when intentional, coherent with the KV and legible. Investigate when there is no demonstrable function, there is a layer conflict, or the execution distracts from the message:
1. **Concept:** adjectives replace a specific idea; when the effect is removed, the relation to the message disappears.
2. **Composition:** accidental competition, elements with no spatial relation, or unintentional tangents.
3. **Effects and materials:** lighting/reflections incompatible with the scene, or stacked effects without visual motivation.
4. **Typography:** fake/illegible text, roles with no functional distinction, or styles that hinder reading.
5. **Image:** altered anatomy/identity, artificial detail, or treatment that contradicts the scene/KV.
6. **Supporting elements:** dashboards, charts, 3D objects, labels, textures or ornaments with no clear role.
7. **Brand:** identity reduced to a generic code, or altered logo.

**Single list of generic-piece signals** (gathers Taste, anti-slop and frontend-design; each item is valid when it has a function or comes from the KV, the question is "what does this serve in this piece?"): tiny uppercase label above every title; badge or pill above the main title; one title word changed in color, italic or underline; 01/02/03 on content that is not a sequence; arrow → on every button; identical cards with an icon in a square; decorative gradient; the same soft shadow on everything; stacked glass and blur; cream background with terracotta; black with one neon; fake dashboard of gray bars; invented testimonial, client logo or number; AI spark and star icons; design-tool ornaments (crosses, rulers, guide lines); the same fade entrance on every block. Removing the ornament without putting anything in its place leaves the piece empty: fill with scale, complete content or a real image (`references\taste\tells.md`, why and dates).

**Surgical correction:** point to the observable element and the consequence; fix the causing layer. Do not apply scoring, limit counts or a fixed subtraction order. Remove or change an element only when it causes the problem — not to make every piece minimalist.

## B. LP / HTML / app
1. **States:** loading, empty, error, success (or "n/a" with reason).
2. **Accessibility:** U1 (`check_image.py contrast`); `:focus-visible`; `label` tied to the input; icon-only button with `aria-label`; decorative `alt=""` + `aria-hidden`; nothing clickable on a `div` without `role`/keyboard; errors with `aria-describedby` + `role=alert`; no positive `tabindex`.
3. **Touch:** U1; hover is never the only trigger.
4. **Layout:** U1/U3/U4/U5; reserve dimensions of grids and images (no CLS); no horizontal scroll at the U5 viewports.
5. **Performance:** images via `check_image.py web` (WebP/AVIF without metadata), `loading=lazy` below the fold.
6. Review by the **render** at the target widths, not by reading the code.

## C. Motion (HTML, programmatic animation, video)
Full method and recipes in `references\motion\` (design-motion-principles, MIT; open only the file the task uses). There is no quota here: context decides, and only real delivery risk generates a warning to the user.
- **Frequency gate, before animating:** how often does the user trigger this? Rare (monthly): expression welcome. Occasional (daily): subtle and fast. Frequent (hundreds per day) or by keyboard shortcut: no animation. LP, deck and campaign piece are rare moments, so they have creative freedom; dashboard and daily-use tool call for restraint.
- **Weight by context** (sets duration, easing and how much moves): productivity and dashboard follow Emil (restraint, under 300 ms, 180 ms usually suffices); polished product interface follows Jakub (200–500 ms, entrance = opacity + `translateY` + blur, exit subtler than entrance, spring with `bounce: 0`); creative, playful and portfolio follow Jhey (whatever serves the effect; easing has personality, elastic does not fit in a bank). Mixed pieces are weighed by part. Readings: `emil-kowalski.md`, `jakub-krehel.md`, `jhey-tompkins.md`.
- **Recipes, plain HTML/CSS first** (`motion-cookbook.md`): entrance and exit and `fill-mode: backwards` (§1), easing, `linear()` and stagger (§2), `@property` (§7), `clip-path` reveal (§9), transition instead of keyframe when the user can retrigger (§11), `transform-origin` from the logical origin (§13), scroll with `IntersectionObserver` as fallback (§14). The React and Framer Motion recipes stay as a suggestion (`references\alternatives.md`).
- **Starting point when context says nothing:** 0.18 / 0.35 / 0.6 s; scale 0.95–1.04; stagger 0.05–0.10 s; exit at 60–70% of the entrance. They are a reference, not a ceiling.
- **Warn the user only when there is real risk:** base state invisible without JS or without animation (title never starts at `opacity:0`, `html.md` §1); missing `prefers-reduced-motion` (no displacement, at most fade ≤ 0.2 s, final state preserved); animation of a layout property (`width`, `height`, `top`, `left`) that causes reflow; attention loop with no way to pause, or vestibular trigger (large zoom, spin, parallax) without warning; animation as the only path to state.
- **Motion or 3D change declared new:** measure the difference against the previous version (pixels or frames at fixed scroll points) before showing; the user's "it looks the same" is a proof failure, not a taste one.
- **When writing:** self-check against `creation-gotchas.md` (motion without purpose, `scale(0)`, plain `ease`, exit equal to entrance, scattered `will-change`). **When auditing existing animation:** `audit-checklist.md` and `anti-checklist.md`, plus the search for gaps, which in HTML is a state change without transition (toggled `display`, `height` without `transition`). The generic-motion patterns in `anti-checklist.md` (pulse, hover-scale on everything, stagger on every list, the same entrance on 4 or more blocks) are signals to investigate, as in §A.
- **Gradients:** generate at final resolution, preserving precision through to output; apply discreet dithering when needed and avoid lossy intermediate compressions. Check banding and stability in the final file at 100% and in playback.
- Cut on the beat: 60/BPM s per beat (30 fps: 1800/BPM frames). One color accent per scene. LP: CSS before JS.
- **Gate before showing the preview** (the user must not be the QA): Before showing, check the complete states and the transitions in playback and in each aspect ratio, including full playback and the pause, resume and seek controls at an intermediate point. The voice must follow the timeline position; independent provisional speech does not prove sync. Validate the render function at non-sequential times: the same instant must produce the same frame, without depending on transitions still in progress. Record the observed result. (1) Each text stays on screen long enough to be read in full and enters in the voice stretch checked by the content of the speech, not only by counting pauses. (2) No element cut by a container (SVG or box `overflow`) nor by the camera/zoom; leaving the safe zone is allowed, cutting is not. (3) The highlighted item is never covered by another. (4) Preserve reading units at line breaks, consistency of weight and alignment across list items, and intentional contrast between levels; measure the gaps between stacked blocks and keep highlights proportional to their neighbors. Use vector markers compatible with the KV when they help reading. (5) Validate the seams between media: absence of accidental cuts, empty bands, black frames and framing jumps. Separate working from perceived quality: timeline advance, FPS and transform differences do not prove fluidity. Compare the previous version and the revision in playback, at the size of use, against the critique received; describe only the observed improvement. If you cannot evaluate it visually in motion, declare that limit. In the same viewer, check the version identifier, the code actually loaded and the motion mode. In an audiovisual preview requested with full motion, offer explicit full playback and a reduced option; do not silently suppress the media animation because of the interface's animation preference.

## D. Deck (1600×900)
- Each slide fits the `1600×900` canvas (`overflow:hidden`), centered with `translate(-50%, -50%) scale(var(--deck-scale, 1))` via `visualViewport`; too much content = split or change archetype, never shrink the font below the minimum (`h2 >= 44px`, `h3 >= 20px`, body `>= 17px`).
- Copy and list hygiene: zero loose hyphen in prose (` - `), zero `–`, `—` or `~`; zero metalanguage (*"in this slide"*); zero orphan words on the last line; every `<li>` with an outline SVG icon (`24×24`); logos inlined in Base64.
- Rhythm: never > 2 consecutive slides with the same background and same composition.
- Navigation: arrows/Space/PageDown, Home/End, previous/next buttons and progress bar.
- Check centering (`±1px` of symmetric margin) at `1024×768`, `1366×768`, `1600×900` and `1920×1080`.

## E. Ad and social copy
- One concrete claim per piece; specificity > adjective. Short video: problem or result in the first 3 seconds.
- Carousel: the card captions read as one continuous sentence.
- Support: the KV's job title or "Talk to our team"; never an invented name or channel.
- Forbidden (except in the client's copy): "game-changer", "revolutionary", "cutting-edge", "in today's landscape", "it's not X, it's Y", false curiosity, bait question.
- Client copy is literal: these rules **flag** risk in 1 line, they do not rewrite.
- Check U9 on the final board: does the scene support the copy's claim, and does the copy give context to the scene? A generic product photo next to a specific promise fails; the proportion between the two depends on the reading, not on a fixed percentage.

## F. AI image
- Run the **Pass³ Test** (`image.md` Part B §6: Physics 2s · Detail 5s · Brand 3s) and check against the master: silhouette, colors, proportion, relevant contact shadows and forbidden items (`PRODUTO_*.md` / `PERSONAGEM_*.md`). If it fails, fix the cause by editing, new generation or another suitable method; iterate while there is progress, with no fixed cap, and stop when new attempts do not improve the result.
- No invented text/logo/watermark in the image. Product label: the priority is the original's real label applied on top; only if it fails repeatedly does another path enter (e.g. the generator writes the transcribed text, checked letter by letter), see `image-product.md` §2.4.

## G. Local technical check (`assets\check_image.py`)
| When | Command |
|---|---|
| See all pieces at once | `prancha Exportados\*.png -o Trabalho\_board.jpg` |
| Assembled Figma × approved preview | `paridade preview.png figma.png` (RMSE ≤ 0.03; above that, open the `_diff.png`) |
| Measure color of a photo/logo/reference that will become a token | `paleta arquivo -n 6` |
| Text/background pair | `contraste "#FFF" "#F26B1D"` |
| PNG logo with excess margin | `bbox logo.png` (crops, does not resize) |

## H. Visual gate before delivering (new creative)
Compare briefing, KV, approved references and final render side by side; do not assign scores. Literal copy, identity, rights or scene↔argument relation violated = immediate rejection. First, reread `## Reprovado` and `## Aprovado` of the client's `_DESIGN\guia.md` and confirm item by item that no already-vetoed error came back and that the approved recipes were applied. Examine five criteria with visible evidence: **Concept** — is there a specific mechanism that makes the thesis visible, beyond adjectives and theme? **Hierarchy** — in thumbnail, does the eye enter the right idea and travel it without accidental competition? **Craft** — Judge the element within the composition and at the size of use: it must be recognizable, support the argument and take part in the occupation of space. If it looks like another object or merely fills a corner, fix its shape, scale, position or integration with light and background; preserve the reading breathing room. **KV** — does each important layer (background, photo/light, type, texture/effect, shape/signature) have an authorized origin and was it adapted without copying the composition? **Distinction** — does the piece differ structurally from previous layouts and from the references without losing the client's visual family?
**Do not approve** when the direction merely combines correct elements (color, logo, photo, headline and graphic) without explaining why those relations are specific to the message; when a campaign motif becomes a decorative mask with no function; or when the piece remains recognizable as a generic template once the logo and brand name are hidden. A rejection must point to the layer and the concrete change; fix that cause and check the new render. Report a score only if the user asks.

**Redo with references:** open the client's and external references, study composition, light, overlap and material, and translate to the KV. The client's background, layout and piece structure can be reused and derived; do not clone a recent or characteristic element from another piece (nor from a reference), avoid caricatured icon or illustration and give each screen its own arrangement, without repeating the same mold.

**Eye route** (Taste `references\taste\critique.md`; look at the screenshot, not the code, because the code carries its intention): (1) one second, then five as a stranger: what it is, for whom, what to do; (2) squint: two or three large masses, not many small ones; (3) cover the logo: would the piece serve a competitor?; (4) count the left edges of the text blocks: two or three, reused; (5) space and frame: equal margins, hole by accident or rest by decision; (6) typography: decisive jump from body to title, orphan, measure; (7) color: who has the largest area, where is the accent; (8) image: does each do a job?; (9) repetition: the same layout in consecutive sections is the template showing; (10) mobile as its own composition; (11) fill: composed poster or narrow column with dead floor; (12) substance: the requested information is complete; (13) collisions; (14) competitor test and the "living thing". No scores or score caps. Correction order: the idea, the hierarchy, the composition, the typography, the image, the color, the detail and, last, the motion.

**Advertising:** confirm that the proposition is understandable, that the visual/textual proof is authorized and that the action matches the briefing. Without comparable data, this is a review of quality and intent — not a sales forecast. If there are metrics, record source, window, format and context; do not attribute causality to the visual without adequate comparison.

**Poster/key visual:** check the first impact in thumbnail and the recovery of the essential information at the intended reading size/distance. Evaluate the relation between typography, image, field and material; do not demand a fixed number of levels, density, overlaps or finishing effect.

## I. Typography and hierarchy (static, LP, deck)
- Define entry, path and number of levels for the message, format and distance. A dominant entry point helps many pieces, but posters, editorial compositions and narratives may use a deliberate path/multiple focal points; do not impose a three-level cap. Prefer clear typographic contrasts when they help, but scale, weight, width, position and space can grade the hierarchy. In interface, preserve usability; in creatives, do not reduce expression just to meet a quota.
- Use the distinct sizes demanded by the piece's real roles; 3–5 can serve as an initial reference in a simple composition, never as a quota or cap. Web/deck use the scale the function needs. Families, leading, tracking, measure and backgrounds: U3/U4.
- Multiple focal points only when deliberate: in the same panel, one dominant title; the others drop a level in scale or weight. Two texts of the same weight competing is an accident.
- Rhythm and occupation (static, carousel, story): use the whole format inside the safe area, with no blocks crowded into corners nor dead floor. Define a spacing scale first (e.g. 8/16/32/64 px) and use only it between groups; logo and tags are the only exception.
- Consistency across screens: background and supporting colors come from the same token on all; compare by pixel sample. Balloon, arrow and box are a single shape, with the same color; pills, buttons, chips and icons are the size of their content, keep proportion and align to the text margin; never stretch to the container width.
- In a carousel the H1 keeps the same size on all screens; if the content does not fit, split into more screens instead of shrinking the title.
- Punctuation is copy: a question ends in "?", CTA without a final period, unless the official copy says otherwise. Check at the end.

## J. Surgical Audit of Code, Scripts and Components (`HTML/CSS/JS/Python`)
When reviewing, auditing or refactoring code, LPs, embeds or internal engines, inspect and fix in this exact order of priority:
1. **Bug:** empty/zero/null inputs, array/viewport limits, time zone, UTF-8 encoding and divergence between selectors/callers.
2. **Risk:** injection in `innerHTML` without sanitization, exposed keys/credentials, swallowed errors (empty `catch {}`) and mutation of global variables in embeds.
3. **Scale:** race conditions in listeners/timers, unbounded lists/loops and `O(n²)` DOM searches inside `scroll`/`resize` events.
4. **Missing Check:** every parser, form or non-trivial branch requires explicit input validation and a safe fallback.
5. **Speed:** eliminate repeated layout reads (`getBoundingClientRect` in a loop), forced reflows and unnecessary re-renders.
6. **Lean:** delete dead code, orphan selectors and single-use abstractions; merge duplicate functions; prefer native platform/stdlib APIs over external dependencies. Intentional technical limits get a comment `shortcut: <limit>, <upgrade trigger>`.
7. **Proof:** bug = find all callers before editing and fix the cause at the shared point; new non-trivial logic (branch, parser, money, security) leaves 1 assert/test. A review finding only with a concrete case (`input X → result Y`), grouped as Must · Should · Optional. Before writing: does it already exist? → native/stdlib → installed dependency → minimum; trimming never cuts validation, security or accessibility.

## K. Exported file (every export)
Check the file that goes to the user, decoded or reopened, not the preview, because the exporter changes color, range, fonts and duration without warning. Failed = fix and export again before delivering.
- **Image (PNG/JPG/WebP):** dimension and aspect ratio of the requested format, sRGB profile, weight suited to the channel, sharp text at 100%.
- **Video (MP4/MOV/WebM):** duration and fps constant as requested; `yuv420p` in tv range (a JPG source becomes `yuvj420p` in full range and changes contrast in some players); audio present and measured (voice at -16 LUFS; engine Reels at -14 LUFS, `video.md` §3); first frame not black; loop: jump from last to first ≈ step between neighboring frames.
- **HTML / preview:** opens without internet, console without errors, logo, images and fonts embedded.
- **SVG:** reopen in the user's editor; without it, require zero `<style>`, `@font-face`, class or filter and text in outlines. Run `python -I <AG>\assets\logo\svg_audit.py file.svg` and fix `<style>`, editor metadata and tiny details before delivering.
- **PDF / deck:** fonts embedded, page count, working links.
- **Derived from an approved preview (Figma, crop, another format):** parity with the preview (`check_image.py parity`; RMSE ≤ 0.03).
