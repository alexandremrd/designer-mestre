# KV, Brand Book, Logo and Design System Module (84 Reference Design Systems)

Unified module for extracting/validating Visual Identity (Cold Start), creating a Brand Book and a new Logo, consulting the 84 real bundled design systems (`engines\uiux`) and structuring/exporting Design System tokens (`tokens.css` and `DESIGN.md`). Extract only what is accessible (`operations.md` §6).

---

## Part A · Cold Start — New Client or Incomplete KV

Full study when there is no `_DESIGN\design_system.md` or when `CLIENTE_NOVO: SIM`. After consolidating the sources and pending items, mark `CLIENTE_NOVO: NÃO`, even if `STATUS_KV` remains `PARCIAL`. An existing client with a partial KV gets only the analysis of the pending items relevant to the request; full review only when requested.

### 1. Folder structure
Existing client: do not move or delete anything without need; create only what the request needs. New client: create the tree **including the four empty image folders** and copy `<AG>\Clients\_CLIENT_TEMPLATE\design_system.md` to `_DESIGN\`. Assets received outside the tree are classified into their categories; preserve paths already provided by the user when moving would affect existing uses.

```text
D:\Clientes\[Cliente]\
  _DESIGN\
    design_system.md     ← client's single memory
    historico.md         ← 1 line per delivery (write-only)
    templates\           ← approved SVG skeletons (E1.svg, E2.svg...)
    Personagens\         ← (optional) dossiers of recurring characters
    Produtos\            ← (optional) dossiers of recurring products
  Compartilhada\
    Identidade Visual\   ← logos, MIV, fonts, brand book (never overwrite)
    Referências\         ← references sent (save only)
    Imagens\  Originais\ (read-only) · Banco de Imagens\ · Tratadas\ · IA\
    Vídeos\   Originais\ · Banco\
  [AAAA]\[MM - Mês]\[AAAA-MM-DD] [TIPO] Título\
    briefing.md · Referências\ · Trabalho\ · Exportados\
```
Types: `CA` Ads creative · `PA` content plan/organic · `EV` edited video · `MT` motion · `LP` landing page/HTML · `KV` identity · `DK` deck · `IM` image · `OT` other.
Old client with separate `KV.md`, `NAO_FAZER.md`, `aprovados.md`, `inteligencia.md`: unify into `design_system.md` (without deleting the old ones).

### 1.1 Brand asset protocol (named brand in any piece)
- **Logo measurements (detail of Law 3):** protection area = symbol height (min. 16 px); minimum 120 px wide (symbol only 32 px).
Applies to the client and to any recognizable brand or product that appears in the piece (comparison, ranking, review). Asset outweighs rule: logo, product image and interface capture identify the brand more than color and font. Color and font without logo, product or interface are not enough, and a silhouette drawn in place of the real product is not valid.
1. **Ask for the list at once:** logo (SVG or PNG), official product images, interface captures, colors, fonts and manual. Whatever the user has, they send.
2. **Search the official channel:** `/brand`, `/press`, product page, app store, launch video. The client always uses their own file (Law 3), never an aggregator's. For a third-party brand merely cited in the piece, icon aggregators (svgl.app, simpleicons.org) work, with the network approval.
3. **Download and really check:** the file opens and is not an empty page of a few bytes; logo with a version for light and dark backgrounds; product image at 2000 px or more, clean and from more than one angle; current interface capture without another person's data.
4. **A few good ones beat many average ones:** search several sources, gather candidates and keep the best (resolution, clear origin, coherence with the brand, matching light and style, own role in the piece). Logo is the exception: if it exists, use it; if not found, stop and ask (Law 3).
5. **Record** in `_DESIGN\design_system.md` §3 KV: origin, date and paths. Colors only from the official file. A demo color inside a capture is not the brand color, and a brand may have two faces (marketing site and product interface): record both and choose by use.
6. **Facts before assumptions:** existence, version and launch of a product are verified on the internet before any decision (core stance).
Total failure: no logo, stop and ask; physical product, ask the user or use an image generated from an official reference (`image-product.md`) and, last, an honest placeholder; interface, ask for a capture from the user's account. Never fill in silently with a silhouette or generic gradient. Detail and commands: `references\huashu\brand-asset-protocol.md`.

### 2. Deep analysis and brand intelligence (once)
1. `Compartilhada\Identidade Visual\`: MIV, brand guide and logos. Render each logo only once and note file, layout, color and bbox proportion.
2. Figma links in the briefing (`get_design_context` / `get_screenshot`).
3. Previous pieces: inventory the relevant series and study **all the references the user indicates**. For a new client or one without `design_system.md`, the initial reading must reveal patterns and exceptions, not be limited to 2–3 pieces. Use a board of all pertinent creatives; in the SVGs, inspect `viewBox`, colors, fonts, hierarchy, masks, embedded photos and recurring elements without dumping base64 into the context. Record the **role** of each recurring element (logo, brand motif, mask, image or ornament), not just its shape and color; see `ads.md` §3. Open individual pieces only for details the board does not show. If the user asks to decode the KV from their own references, also apply `ads.md` §2.3 and separate brand system, campaign platform and isolated piece. After consolidating in the KV, future sessions use the Fast-Track.
4. Site or Instagram: if the links do not come in the briefing, locate the public presence by brand name and region when the match is unambiguous; if there are homonymous profiles, confirm before attributing content. Combine content and appearance. On the site, prioritize home and pages that explain company, offer, cases/proof and contact; extract text, structure, images and, when accessible, CSS tokens (`--*`), computed colors, fonts, surfaces and components. On Instagram, observe bio/link, highlights and pinned posts, recent grid and a sample of accessible Reels/posts; do not infer reach or intent from a single piece. Record the observed window and date. Blocked access = `operations.md` §6; do not circumvent login, blocking or platform limit.
5. **Positioning and benchmark** (new client; also when requested for an existing client):
   - Gather evidence of the own presence before formulating strategy: what the brand claims, to whom, which need it serves, which benefit it promises, which proofs it presents, which language and visual codes it repeats. Always separate **observed**, **inferred** and **unconfirmed**; an isolated bio, aesthetic or claim does not prove positioning or differentiator.
   - Take a manageable and representative sample: up to 5 key site pages and up to 12 recent/pinned content items per profile, expanding only if there are relevant series/campaigns or the sample is insufficient. Examine the render/visual when available, not just captions or metadata. Preserve URL, title/position and access date for each strategic finding.
   - When public metrics are available, record them as a snapshot of the collection. If used, calculate the interaction proxy per post `(likes + comments) / followers × 100` and report numerator, denominator, sample and date. It is descriptive; it is not equivalent to reach, conversion or causality. Do not compare posts of different formats/ages without caveat, nor fill in hidden metrics.
   - If the segment and region are clear, identify up to 3–5 comparable references, distinguishing direct, adjacent and aspirational competitor. Compare the same dimensions across brands: explicit audience, category/territory, promise, proof, offer, tone, visual codes and content formats. If the set is uncertain, present the selection as a hypothesis or ask for confirmation before treating it as direct competition.
   - Extract patterns and differences, not an invented ranking. Ad frequency is a signal of investment/creative continuity, not evidence of conversion; public likes/views do not prove sales or relative performance without comparable context. Never invent market share, audience, result, offer or technical attribute.
   - End with an actionable synthesis: observed vs. desired positioning (if there is a briefing), proof points and gaps, site↔social coherence, visual/verbal codes to preserve, differentiation opportunities and 1–3 possible creative territories. Define voice with 3–5 behavioral attributes (what they mean and do not mean), observed examples and how the tone changes per channel without losing identity. Each recommendation must point to the evidence that motivated it; territories are hypotheses for creation, not a new approved KV.
   - Record in `design_system.md` only durable and concise knowledge. For in-depth analysis or comparative matrix, deliver a separate report in the request's directory; do not dump raw research into the brand's memory.
   - Scraping via Apify/an external service is optional and only if already configured and the request justifies it. Before any paid execution, broad collection or data sending, confirm platform, scope, volume and cost/limit with the user. Without that, use accessible public sources, tools already available or inputs provided by the user. Do not install CLI, dependencies or connectors as an automatic part of Cold Start.
7. If the client has no KV or asks for inspiration from major global brands, consult the internal engine of **84 real Design Systems**:
   - Search by segment/aesthetic: `python "<AG>\engines\uiux\scripts\search.py" "<segmento ou estética>" --domain brand -n 3`
   - Full reading of a reference brand's `DESIGN.md` (e.g. `linear.app`, `stripe`, `apple`, `ferrari`, `bugatti`, `lamborghini`, `nike`, `airbnb`, `runwayml`, `vercel`, `raycast`, `oura`): `python "<AG>\engines\uiux\scripts\search.py" "<slug>" --brand`
8. Extract and consolidate in `_DESIGN\design_system.md`:
   - concept, feeling and symbol;
   - logo versions (name · layout · color · bbox);
   - palette by role (HEX, RGB, CMYK, **4-level Surface Ladder** `canvas` → `surface-1`..`surface-4` + `hairline`, semantic colors, WCAG contrast, accent scarcity rule and forbidden colors);
   - typography by level (official with weight, case, **tracking polarity** — negative in display, neutral in body, positive in eyebrow/label — + Google Fonts substitute for Figma/SVG);
   - graphics, SVG archetypes, composition/breathing room/logo position/footer, photography (theme · people · framing · light · treatment · relation to the copy), safe zones, tone of voice and pillars, What to Do (Approved) and What Not to Do (Vetoes);
   - offers/products mentioned in the sources, in 1–3 lines per item with the origin and degree of confirmation; separate observed commercial description from confirmed technical attribute. This guides the next scene without inventing benefits.
9. Contradictions or essential missing items (logo, palette or font) go to `## 5. Decisões Pendentes` keeping `PARCIAL`; when complete, mark `STATUS_KV: VALIDADO`.
10. Client already `VALIDADO` on an old template: new empty fields do **not** downgrade the status nor trigger a new analysis.
- Client emails as a source: record by block (header, body, footer) background, list/icon and button; becomes KV only with confirmation.

**Short evidence matrix (in the analysis/report; memory receives only the synthesis):**
| Type | Rule |
|---|---|
| Observed | Short quote, visual element or data present in the source; include URL/file, location and date. |
| Inference | Strategic interpretation derived from cited evidence; mark as hypothesis and indicate high/medium/low confidence. |
| Gap | Important information without public evidence; record as unconfirmed, without filling in by plausibility. |

Keep source and inference side by side. Describe visual style by verifiable elements (palette, typography, framing, light, composition, rhythm and recurrence), not by loose adjectives such as “premium” or “modern”.

**Method references consulted** (inspiration, not installed dependencies): [Apify Ultimate Scraper](https://github.com/apify/agent-skills/tree/f22557f15941aa6a5bc7539f0408d509d4a32ab6/skills/apify-ultimate-scraper) for source/flow selection and limits; [Apify Ads Intelligence](https://github.com/apify/awesome-skills/tree/1eb0cd0c12e35a0d0a17c23f0f462d7062fd5813/skills/apify-ads-intelligence) and [Competitive Ads Extractor](https://github.com/ComposioHQ/awesome-claude-skills/tree/be2a406907dbc61b73e6827ded415c96139d13a2/competitive-ads-extractor) for message and creative analysis; [Brand Review](https://github.com/anthropics/knowledge-work-plugins/tree/a266ab8c3c754a3ccf7a634044fc1595fc06e50e/marketing/skills/brand-review) for voice dimensions; [Competitor Analysis](https://github.com/langchain-ai/deepagents/tree/a2f88434c5a4b5ce5244c468bb9f69b27831842d/examples/deploy-gtm-agent/skills/competitor-analysis) for comparative matrix and gaps; [Naksha Studio](https://github.com/Adityaraj0421/naksha-studio/blob/f5275255d1c5417026508c5e294cf6d27ec8809d/commands/brand-strategy.md) for positioning audit across touchpoints; [UPPAbaby Brand Review](https://github.com/zrosenfield/sharepoint-ai-skills/blob/62d6481ac3b7d59d5248af46164e037d33d88650/Skills/uppababy-brand-review/SKILL.md) for explicit visual criteria and evidence. The patterns were rewritten for this flow; none of them provides, by itself, the whole KV extraction cycle through site, Instagram and campaigns. Do not incorporate commands that circumvent blocks nor claim results without data.

---

## Part B · Brand Book (16:9 Visual Identity Manual) and New Logo

### 1. Brand Book (16:9 HTML/CSS Layout and Export)
Save in `Compartilhada\Identidade Visual\` and, if requested after approval, on the "Brand" page in Figma (with styles and variables), without altering existing official files.
- **Mandatory Asset Review before generating:** audit what exists (`✓`), what is incomplete (`⚠`) and which optional sections will be omitted (`✗`, e.g. omit `2.4 Construction/Grid` if there is no `construcao.svg` mesh; never invent a Pantone code if it was not provided), presenting the page estimate before the final composition. A multi-brand client gets 1 brandbook per brand + `index.html` as a unified cover-index.
- **Hierarchical Master Table of Contents and Catalog of 14 Page Types (`aspect-ratio: 16/9`, `max-width: 1600px`, margins `96px × 80px`, 12-column grid with layouts `5/7`, `4/8` and `6/6`, scalable typography in `cqi`):**
  - `00 Cover` + `00 Table of Contents` + full-page **Section Dividers** before each macro-section (`01` to `07`) with giant number (`62cqi`) and pagination `001` in the footer;
  - `01 The Brand`: `1.1` About · `1.2` Purpose/Mission/Vision · `1.3` Values · `1.4` Personality and Tone of Voice · `1.5` Manifesto;
  - `02 Logotype`: `2.1` Concept · `2.2` Primary Version · `2.3` Variations (`2×2` or `3×2`) · `2.4` Construction/Grid · `2.5` Protection Area (`X`) · `2.6` Minimum Reduction (`mm` print and `px` digital) · `2.7` Monochrome (positive/negative/B&W) · `2.8` Uses on Backgrounds · `2.9` Co-branding · `2.10` **Incorrect Uses** (`3×2` or `4×2` grid generated automatically by applying CSS transformations to the official logo — `scaleX(1.4)`, `scaleY(0.6)`, `rotate(15deg)`, `hue-rotate(180deg)`, `-webkit-text-stroke`, `drop-shadow`, `opacity: 0.3`, background without contrast — with a red diagonal prohibition band and technical caption);
  - `03 Colors`: `3.1` Primary (Hero mode for 1 color or proportional Grid) · `3.2` Secondary · `3.3` Neutrals (`50–900` scale keeping constant hue and saturating the middle) · `3.4` Gradients · `3.5` Usage Proportions (90% neutral / 10% brand in the editorial template, or 60% brand color in the expressive template);
  - `04 Typography`: `4.1` Primary (giant `Aa` with primary/accent contrast + weights) · `4.2` Secondary · `4.3` Tabular hierarchy (`Display 13cqi`, `H1 3cqi`, `H2 1.8cqi`, `H3 1.3cqi`, `Body 1cqi`, `Caption 0.72cqi`) · `4.4` Best Practices;
  - `05 Graphic Elements`: `5.1` Graphics/Patterns · `5.2` Iconography · `5.3` Photography Direction · `5.4` Textures;
  - `06 Applications` (irregular grid with 1 dominant mockup per page) and `07 Closing`.
- **Chrome:** 12 px uppercase header +0.12em (brand on the left; `NN SECTION / N.N` on the right); 11 px footer `Brandbook [Brand] · v1.0` + page in 3 digits; covers and dividers without header. Flat (no gradient/shadow) unless the brand uses it.
- **Pagination:** 2.3 with 8+ variations, 3.1 with 5+ colors or 06 with 9+ applications = split into pages, 1 dominant mockup per page. Applications only those requested/existing (business card 85×55 mm, A4, DL/C5 envelope, email signature ≤ 600 px).

### 2. New logo (only on request for something new)
- **Trigger:** the user asks for a **new** logo, brand or identity ("I want a new logo", "new brand", "new identity", "create a logo"). "Brand" or "identity" without "new" nor a create verb do not activate and follow the existing KV ("use the brand", "apply the identity"). When in doubt between applying and creating, ask in 1 line. A missing logo in an ordinary request remains Law 3 (placeholder `LOGO [CLIENTE]` and ask for the original). Client who already has a logo: confirm whether it is a redesign (`references\logo\redesign.md`) or a new brand.
- **Method:** `references\logo\METHOD.md` (logo-design, MIT) leads the phases: brief, research and category clichés, 8 to 12 one-sentence concepts, the 3 strongest in SVG (black first), tests and refinement in two rounds and **checkpoint: show the 3 concepts and wait** before the kit; the kit only after the yes. In-depth material on demand in `references\logo\` (`principles`, `discovery-brief`, `mark-types`, `visual-techniques`, `color`, `typography`, `svg-construction`, `testing-checklist`, `presentation-delivery`, `identity-system`, `redesign`, `critique`, `process`). The original project's library of 1,432 logos is not included (they are third-party brands): `search_library.py` and `--refs-industry`, cited in METHOD.md, do not exist here. To see the category, use internet research and the real competition, only to study, never to copy or trace.
- **Tools** (`assets\logo\`, Python standard library only, run with `python -I`): `svg_audit.py` checks the SVG; `preview_sheet.py` assembles the test sheet (sizes, 16/32 px, backgrounds, 1 color, blur); `concept_sheet.py` generates the checkpoint concepts image; `render_png.py` converts SVG to PNG (uses Chrome or Edge); `export_variants.py` generates black, white, mono, icon and favicon; `presentation_board.py` assembles the presentation with sector mockups (template in `assets\logo\presentation-spec.example.json`).
- **Core rules still apply:** Law 3 (existing logo never altered), Law 4 (name exactly as the client wrote it), U3 (font with a license that allows logo use; letters built as curves, no `<text>` in the final file) and a third-party brand never imitated. There is no registration guarantee: recommend a professional prior-art search.
- **Delivery:** SVG (preferred) + 2× transparent PNG + vector PDF; positive, negative and monochrome versions, in `Compartilhada\Identidade Visual\`, recorded in the logo table of `_DESIGN\design_system.md`. From then on the existing-logo law applies. The concept criterion is an idea explainable in one sentence, distinct from the category, simple, relevant and strong at 16 px.

---

## Part C · Design System, Surface Architecture and Token Export (`tokens.css` & `DESIGN.md`)

Reference + logo + typography → analysis → tokens → preview for approval → export in the chosen formats (and variables/components in Figma if requested after approval). The source of truth is the client's `_DESIGN\design_system.md` (`STATUS_KV: VALIDADO`).

### 1. Design System Engineering Laws (extracted from 84 Global Systems)
1. **4-Level Surface Ladder (`Surface Ladder`) vs. Shadows:**
   - Define `canvas` (base background), `surface-1` (standard cards and panels), `surface-2` (highlighted/hover cards), `surface-3` (sub-nav/dropdowns), `surface-4` (elevated modal elements) + `hairline` (`1px`) and `hairline-strong` (focus/hover) borders.
   - In **Dark Mode** interfaces, hierarchy and depth come from **elevation on the surface ladder + 1 px hairline border** (and subtle 1 px top highlight), never from heavy black drop-shadows. In dark mode, the dark canvas itself is the breathing room, and sections are separated by surface elevation.
2. **Chromatic Scarcity and Action States:**
   - Reserve the primary chromatic accent (`{colors.primary}`) exclusively for: brand, primary CTA (`button-primary`), focus ring (`primary-focus`) and surgical highlight. Explicitly define `{colors.primary-hover}` and `{colors.primary-focus}`. Secondary buttons use `{colors.surface-1}` + `{colors.hairline}` border or transparent ghost style.
3. **Typographic Tracking Polarity Law:**
   - **Display (`display-xl` 56–112 px):** progressively **negative** tracking (`-0.03em` to `-0.04em` / `-1.8px` to `-3.5px`) and compact line-height (`0.95–1.10`).
   - **Body (`16–18 px`):** neutral tracking (`0` to `-0.05px`) and comfortable line-height (`1.45–1.60`).
   - **Eyebrow / Badges / Micro-labels (`10–13 px`):** **positive** tracking (`+0.04em` to `+0.12em` / `+0.4px` to `+1.4px`), creating immediate taxonomic contrast against the negative-tracking headings.
4. **Mandatory tokens (CSS layers):**
   - **A1 · brand-mandatory:** `--bg` `--fg` `--accent` `--font-display`.
   - **A2 · mandatory with default:** `--fg-2` `--surface` `--surface-2` `--border` `--success` `--error` `--font-body` `--radius` `--space-4` (16 px) `--motion-fast` (0.18 s).
   - Name always by **function**, never by color (`--accent`, not `--laranja`).
- **3 token layers:** primitives (ramps, 4 px scale, type 1.2–1.25) → semantic by function (`--accent`, `--surface-1`, `--fg-2`, `--success/--warning/--error/--info` + `*-foreground` pair ≥ 4.5:1) → component (`--btn-bg: var(--accent)`). Pieces use only semantics; theme swaps only the semantic layer. DTCG export (`$value/$type`) optional for Figma variables.
- Component: sizes sm/md/lg · styles default/outline/ghost/destructive · states default/hover/focus/disabled/loading.

### 2. Exports (on request: "export the design system", LP, or site extraction)
Save in `_DESIGN\export\` (not read by the KV Gate):
1. **`tokens.css`** — `:root{}` with A1+A2, surface ladder and typographic scale (`--fs-display` … `--fs-caption`, ratio 1.2–1.25).
2. **Full `DESIGN.md` (9-section standard + YAML frontmatter):**
```yaml
---
version: alpha
name: [Cliente]
description: "[Resumo denso da atmosfera visual, canvas, superfície, acento cromático, tipografia e ritmo de página]"
colors:
  primary: "#..."
  on-primary: "#..."
  primary-hover: "#..."
  primary-focus: "#..."
  ink: "#..."
  ink-muted: "#..."
  ink-subtle: "#..."
  canvas: "#..."
  surface-1: "#..."
  surface-2: "#..."
  surface-3: "#..."
  surface-4: "#..."
  hairline: "#..."
  hairline-strong: "#..."
  semantic-success: "#..."
typography:
  display-xl: { fontFamily: "...", fontSize: 72px, fontWeight: 600, lineHeight: 1.05, letterSpacing: -2.5px }
  headline:   { fontFamily: "...", fontSize: 32px, fontWeight: 600, lineHeight: 1.15, letterSpacing: -0.8px }
  body:       { fontFamily: "...", fontSize: 16px, fontWeight: 400, lineHeight: 1.50, letterSpacing: 0 }
  eyebrow:    { fontFamily: "...", fontSize: 13px, fontWeight: 500, lineHeight: 1.30, letterSpacing: 0.6px }
  button:     { fontFamily: "...", fontSize: 14px, fontWeight: 600, lineHeight: 1.20, letterSpacing: 0 }
rounded: { xs: 4px, sm: 6px, md: 8px, lg: 12px, xl: 16px, pill: 9999px }
spacing: { xxs: 4px, xs: 8px, sm: 12px, md: 16px, lg: 24px, xl: 32px, xxl: 48px, section: 96px }
components:
  button-primary: { backgroundColor: "{colors.primary}", textColor: "{colors.on-primary}", typography: "{typography.button}", rounded: "{rounded.md}", padding: "10px 18px" }
---
```
**9 mandatory H2 Sections in the `DESIGN.md` body:**
1. `Overview` (Visual Theme, Mood, Surface Ladder philosophy, Page Rhythm & Key Characteristics)
2. `Colors` (Brand & Accent, Surface Ladder, Text Hierarchy, Semantic)
3. `Typography` (Font Families, Hierarchy Table, Tracking Principles & Open-Source Font Substitutes)
4. `Layout` (Spacing System base 4px/8px, Grid & Container widths, Whitespace Philosophy)
5. `Elevation & Depth` (Level 0..4 table, hairline vs shadow, Decorative Depth)
6. `Shapes` (Border Radius Scale by component, Photography & Illustration Geometry)
7. `Components` (`button-primary` with hover/pressed/focus, `button-secondary`, `feature-card`, `pricing-card`, `text-input`, `top-nav`, `footer` referencing `{colors.*}`)
8. `Do's and Don'ts` (derived from the client's `## 2. O QUE FAZER` and `## 1. NÃO FAZER`)
9. `Responsive Behavior & Iteration Guide` (Breakpoints `1440 / 1280 / 1024 / 768 / 480 px`, Touch Targets `≥ 44px`, Collapsing Strategy).
3. **Single HTML preview:** visual catalog with `#HEX` swatches and WCAG contrast (`check_image.py contrast` (contrast, palette, board and image parity)), typographic scale, buttons in all states (`Primary`, `Hover`, `Secondary`, `Ghost`, `Disabled`), cards on the surface ladder and Light/Dark toggle.
