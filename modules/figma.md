# Figma Module — Editable Native Layout, Visual Parity and Token Export

Read and executed only after the "approved" on the preview **and** when the user chooses to assemble in Figma (or when they ask to edit an existing Figma file directly). If the user approves the preview but asks only for PNG or SVG (or does not ask for Figma), do not open or assemble in Figma. Goal when triggered: rebuild the visual hierarchy in native Figma layers, keeping parity with the approved reference; complex vector assets may remain as imported vectors when that better preserves the drawing.

---

## Format principle: SVG is not a native Figma document
An SVG can preserve vector appearance and, depending on the content, parts of the text and groups; it **does not encode Auto Layout, components, constraints, variables, styles nor Figma's spacing semantics**. `<g id>` and names in the XML do not guarantee an editable layer tree to the file's standard. Do not promise that pasting/dragging the SVG correctly creates frames, native text or Auto Layout.

When the user wants only a vector file for use, deliver the SVG. When they want to work/edit in Figma, treat the approved SVG as a visual reference and asset source; rebuild the layout in native Figma nodes. Use imported vectors/SVG only where fidelity of curves, illustrations, masks or complex effects justifies it. Keep text, logo, CTA and layout blocks in native layers whenever possible. This way, visual parity does not depend on flattening the whole piece, and the structure stays understandable.

## Choosing the method: brand piece or product screen
- **Ad, post, KV or brand composition:** prioritize the approved direction and freedom of composition. Organize text, logo, CTA, photo and graphics in named native layers; use absolute positioning where the art-directed composition requires it. Apply Auto Layout only to groups that really flow (for example, text and button or repeated items). Do not look for or create components, variables or a complete library for an isolated piece; reuse existing resources when pertinent.
- **App/site screen built from code or description:** the specialist UI/Figma route leads this work. Use `figma-use` and `figma-generate-design` together when the file has a relevant design-system library; the second skill is for screens composed with published components/variables/styles, not a generic SVG converter. For interface critique or design-to-code, keep the specialist route set out in the core.
- **Do not duplicate the design system:** inspect existing screens and instances before searching for/creating resources. If the local variable search comes back empty, that does not prove published libraries have no variables; use the available design-system search before concluding there are no tokens. Search for components, variables or styles only when the deliverable and the file justify it.

## 1. Route A — Official Connector / Direct Execution (Preferred)
- Connector off: ask to enable it.
- **Before creating:** inspect the target page/file and identify existing naming conventions, components, variables, styles, fonts and grids. Reuse them when pertinent; do not invent a parallel library.
- **Native frame and layout:** first create the root frame named for the piece/campaign; structure the semantic blocks in frames/text nodes, applying Auto Layout, padding, gap and `HUG`/`FILL` where the content flows. Do not force Auto Layout in overlapping art-directed compositions: use absolute positioning when it is intentional.
- **Vectors:** use native nodes for simple shapes. Import the approved SVG (for example, `figma.createNodeFromSvg`, if available in the connector) for complex illustrations or graphics, checking bounds and structure after importing; do not use the whole SVG as a substitute for the editable layout.
- **Native text:** `await figma.loadFontAsync({ family, style })` always **before** setting characters or typographic properties, using the exact family and weight from `design_system.md` or the styles existing in the file. If unavailable, follow the core's U3 (ask first; never swap the font silently); do not silently convert text to vector.
- **Photo:** `IMAGE` fill (`scaleMode: "FILL"` or `"CROP"`); blend gradient/scrim in a separate layer above.
- **Logo:** `createNodeFromSvg` of the official file, named `Logo_[Cliente]_Oficial`, proportion locked.
- **Hierarchy and names:** follow the file/team convention. If none exists, use stable semantic names (e.g. `Post / Feed`, `Background`, `Hero image`, `Headline`, `Body`, `CTA`, `Logo`). Group by function; do not create dozens of layers for decorative paths nor rename everything with generic indexes.
- **Auto Layout and spacing:** identify content relationships before defining layout: stacks of text/buttons/repeated items normally use Auto Layout; hero, photography and overlapping elements can stay in absolute position. Use values consistent with existing tokens/frames and preserve visual intent; do not deduce gap from `<g>` nor turn every SVG coordinate into padding.
- **Connector quota:** the Figma connector has a call limit (Starter/View plans run out fast). Use it only to analyze (one metadata read and one full-size export per frame) and to export. Create, iterate and check outside Figma; apply to the file only after the approval, in a batch per frame. Validate with one export per milestone, not at every step. Keep the IDs of the altered nodes for targeted fixes, without recreating the whole piece to fix a detail.
- **Text and components:** load the exact font before editing native text; confirm the available family and style and declare a fallback if needed. When reusing a component instance, prefer its exposed text/variant properties over changing inner nodes without need. Do not convert text to vector to work around a missing font without warning.
- **Recovery:** on error, stop and read the message before any new call. Connector limit reached: do not reread nor try via the browser, and do not hand the work to the user. Find the pieces yourself: client folders (previous rounds, `Imagens\IA\`, `Tratadas\`, `Referências\`), exported SVG/PNG the user points to (a Figma SVG carries the image embedded in base64: extract, swap and render again) and the product's collection. Ask for a file only after exhausting these sources; deliver the piece as an image. Confirm page, IDs and current state by inspection when the cause is unclear; fix only the affected step and retry in a bounded way. Never assume partial operations were reverted or applied without checking.
- **Visual parity:** export a PNG of the Figma frame at the same size as the reference and compare visually; use `python assets\check_image.py parity preview.png figma.png` (contrast, palette, board and image parity) when available. RMSE is a signal of pixel difference, not proof of good layer structure or Auto Layout. Check structure and appearance separately.

---

## 2. Route B — Local Engines for Figma Desktop (`figma_engine\`)
When operating via local plugins in Figma Desktop, choose one of the two modes contained in `figma_engine\`:

1. **Batch Code Execution Mode (`figma_execute` — 90%+ token savings):**
   - Instead of dozens of individual calls, send a single JavaScript block to create complete hierarchies, apply Auto-Layout, bind tokens and audit accessibility:
   - `await figma.status()` → checks connection.
   - `await figma.create({ type: 'frame' | 'card' | 'text' | 'button' | 'nav', name, width, height, x, y, layout: { direction: 'col'|'row', gap, padding }, fill, cornerRadius, children: [...] })` → creates a complete tree in 1 call.
   - `await figma.query({ target: 'selection' | 'name:Elemento' })` and `await figma.modify({ target, fill, textColor, maxWidth, layoutSizingHorizontal: 'FILL' })` → batch query and edit.
   - `await figma.toComponent({ target, name })` and `await figma.createVariants({ target, property, values })` → componentization and variants.
   - `await figma.createToken({ collection, name, type, value })`, `await figma.bindToken({ target, property, token })` and `await figma.syncTokens({ from | to })` → variables and tokens.
   - `await figma.accessibility({ target: 'selection' | 'page', level: 'AA', autoFix: true })` → audit and automatic fix of WCAG contrast and touch targets (≥ 44×44 px). `autoFix` only on a working copy or with the user's yes; never on the approved file.
   - `await figma.export({ target, format: 'png' | 'svg' | 'pdf', scale: 2 })` → final export.
   - Detailed API rules in `figma_engine\rules\*.md` (read only the needed rule if in doubt about syntax).

2. **Bidirectional Socket Mode (42 Granular Real-Time Tools):**
   - Inspection (`get_document_info`, `get_selection`, `read_my_design`, `get_node_info`, `get_nodes_info`, `get_styles`, `get_local_components`), Creation (`create_frame`, `create_text`, `create_rectangle`, `create_section`, `create_component_instance`, `clone_node`), Auto-Layout (`set_layout_mode`, `set_padding`, `set_axis_align`, `set_layout_sizing`, `set_item_spacing`, `move_node`, `resize_node`, `set_corner_radius`), Style (`set_fill_color`, `set_stroke_color`, `set_image_fill`), Bulk Text (`scan_text_nodes`, `set_text_content`, `set_multiple_text_contents`), Instance Propagation (`get_instance_overrides`, `set_instance_overrides`), Annotations/Prototyping (`set_annotation`, `create_connections`) and Export (`export_node_as_image`).

3. **DOM/HTML → Vector Layers and Auto-Layout Conversion:**
   - To bring an approved LP or HTML component into Figma: map computed styles (`getComputedStyle`) and box model, converting containers (`section`, `div`, `header`) into Frames with Auto-Layout, texts into `TEXT` nodes with loaded fonts, images into `IMAGE` fill and inline SVGs into native vectors.

---

## 3. Route C — SVG for vector use (No Connector)
- Save the clean SVG in `Trabalho\` for delivery/vector use: text with explicit family/weight, images referenced or embedded according to the delivery format, resources in `<defs>` and no external dependencies/`foreignObject` when that harms use. Check with `assets\logo\svg_audit.py` (`quality.md` §K) before delivering.
- Semantic `<g>` and `id` help inspect and organize the SVG, but do not guarantee conversion to native layers or Auto Layout in Figma. If the user needs editable Figma structure without a connector, deliver the SVG as a vector reference and explain that manual reconstruction is needed; do not declare the Auto Layout requirement met by the SVG.
- **Full Design System Export via Figma Desktop Console (when requested without a connector):**
  - Generate a standalone JS script (for `Plugins > Development > Open Console`) that automatically creates:
    1. **Color Styles** organized with `/` (`Primary/50`..`900`, `Neutral/50`..`900`, `Semantic/Success|Warning|Error|Info`, `Surface/Canvas|Surface-1..3`, `Border/Hairline`) via `figma.createPaintStyle()`;
    2. **Text Styles** (`Heading/Display`, `Heading/H1..H4`, `Body/Large|Regular|Small`, `Label/Eyebrow`) loading the fonts with `await figma.loadFontAsync()` before `figma.createTextStyle()`;
    3. **Effect Styles** (`Shadow/SM|MD|LG|XL`) via `figma.createEffectStyle()`;
    4. **Variable Collection (`Design Tokens`)** with native `Light` and `Dark` modes via `figma.variables.createVariableCollection("Design Tokens")`, populating all semantic colors and `radius` (`FLOAT`) with `variable.setValueForMode(modeId, val)`.

## 4. Approved Template Memory
New approved structure: save the SVG skeleton (without heavy Base64) in `_DESIGN\templates\[arquetipo].svg` and record it in `## 2. O QUE FAZER` of `design_system.md`.

## Method references
- [Figma Use Skill](https://github.com/coderabbitai/codex-plugin/tree/35779b453cca18aa7cd3176f0bb73a8c75d11da8/plugins/figma/skills/figma-use): reference for tree inspection, small operations, returned IDs, font loading and validation/recovery. Use as an API guide when the tool and flow are compatible; details specific to one `use_figma` implementation are not universal rules.
- [Figma Design Generator](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/figma-generate-design): conditional reference for app/web screens that reuse published components, variables and styles. Screen capture via `generate_figma_design` is a parity reference for web apps; it is not a required step for ads, SVGs or work without a rendered app.
- Methods extracted for this module, without copying the skills or their code examples in full. None of them is specific to repairing imported SVG; they do not promise automatic conversion of SVG to semantic layers or Auto Layout.
