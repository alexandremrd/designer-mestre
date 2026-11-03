# Designer Mestre (`/designer-mestre`)

**Designer Mestre** is a skill for producing and reading visual materials tied to a brand. It can describe and interpret images, answer visual questions, extract legible text and compare references through native multimodal capability; ad analysis and KV decoding keep their specialist modules. When the request requires it, it also analyzes provided materials and accessible public sources to extract positioning, identity and references; it creates ads, pages, presentations, videos or images according to the request and the tools available in the session. In new visual creation, the workbench is iterated with the user and the direction is approved before choosing/exporting the final file, except when the user asks for direct delivery. Memory is client-specific and depends on the files and feedback available: there is no autonomous learning between sessions.

## How to install

Run `Installer.cmd` (or `Installer.ps1 -Yes`). It keeps one physical folder, `Arquivos`, and links it as `designer-mestre` in each AI's skills folder, so every AI reads and edits the same files. Reload the skills in the open AI afterwards. The installer never publishes to GitHub, and client memory and credentials stay outside the package.

## Technical overview

**Designer Mestre** is a visual creation and reading skill. At Cold Start or when requested, it analyzes images and accessible sources from a site, Instagram, briefing and creatives, separating evidence from inference; it compares references/competitors when relevant and keeps memory isolated per client. It covers ads, posts, LP/HTML, deck, video, motion, image/3D and Figma, according to the tools actually available. Call: `/designer-mestre`.

## Flow
1. **Briefing:** a long text, e-mail or PDF can be organized into `briefing.md` when the task requires it.
2. **Creation workbench:** a new piece opens an iterable view in the medium best suited to the idea and the available tools; preview and final format are different decisions.
3. **KV gate:** before generating, it reads the client's `design_system.md` (colors, fonts, logo, vetoes). A client without a KV goes through Cold Start (`kv-logo.md`).
4. **Request module:** opens only the route's module (and the appendix, when the route asks for it); inside it, only the Part for the request.
5. **Approval and export:** after approval, confirm the final formats and the export standard, unless the user already defined them or a client preference is on record. Run QA relevant to the destination and save the chosen files in the agreed path.

At Cold Start, it distinguishes observation from inference, records sources and dates, maps visual and verbal codes and turns findings into positioning, proofs, gaps and creative opportunities. Scraping/external services are optional; it does not install dependencies or start paid collection automatically.

## Core Laws
- **Logo:** never created or altered. Uses only the original file, or the placeholder `LOGO [CLIENTE]`.
- **Copy:** literal, no invented CTA, badge or number, and no absolute promises.
- **Isolation:** nothing from one client leaks to another.
- **Workbench and final file:** choose the engine and the authoring/preview medium by creation, render and editing potential for the piece. SVG, PNG, HTML, PPTX, PDF, native Figma and hybrid compositions serve distinct needs; none is the default final format.
- **HTML site:** preserves the pixel-perfect requirement of the HTML route. The freedom among engines applies to the workbench of other visual pieces and does not relax this requirement.
- **Visual direction:** choices are judged by their role in the idea, in the KV and in legibility; intense color, gradients, textures and expressive resources are not vetoed in themselves.
- **Sources and rights:** extracts only what is accessible (rendered DOM, computed CSS, uploaded files); blocked = asks for saved HTML or a screenshot. A third-party reference transfers technique, never identity. Absorbed code keeps the original license.
- **Unified evolution:** a new rule replaces the old one in the module that owns the topic; a value used by 2+ modules lives in the Universal standards `U1–U12` of the core.

## Memory and available tools
- **Memory per client:** `D:\Clientes\[Cliente]\_DESIGN\` (`guia.md` with approved/rejected in suggestions, `design_system.md` with KV and business, `historico.md`).
- **Agent guide:** `GUIDE.md` gathers trends with no client, in brief suggestions; `/aprenda` rewrites the guides at the end of each project. Record only durable knowledge and feedback actually received; do not presume approval, rejection or automatic learning.
- **Image generation:** the modules document adapters and engine options, including local and integrated engines when installed and available. The skill does not guarantee access to a model or generation execution in every session.
- **Image QA:** `assets\check_image.py` offers operations such as board, RMSE parity, palette, WCAG contrast, bbox trim and WebP conversion; each operation depends on the requirements and the available runtime.
- **Video and captions:** `assets\caption_reels.py` offers caption sync, cuts and treatments described in the module; validate dependencies and availability before promising execution.
- **Voiceover and sound effects:** `assets\generate_audio.py` generates TTS and effects through the ElevenLabs API (Python standard library only); each user does their own login (`npx -y @elevenlabs/cli@latest onboard init` in `%USERPROFILE%\.designer-mestre\`, guided by the AI), the key stays outside the skill and each generation spends credits from their account.
- **Offline UI/UX engine and 84 Design Systems:** `engines\uiux` includes local collections queryable with `--domain brand` and `--brand <slug>`, without replacing the client's validated KV.

## Where the agent lives
The agent can be saved in any folder (`<PASTA_DO_AGENTE>`). The edited copy in the root folder is the source; **after the version is approved**, run `Installer.cmd` to locate the computer's IDEs and sync the skill. **Token-saving note:** the `Installer.cmd` file is exclusively for installation — the agent must never open or analyze it in sessions. Changes are made in the single physical source; the local accesses point to it, with no duplicate copies or backups.

## Structure

```text
<PASTA_DO_AGENTE>\
├── GUIDE.md            ← suggestions with no client, read at the start
├── SKILL.md            ← core: minimal load, routes, KV gate, Laws and index of the support files
├── delivery.md          ← delivery cycle, proof, redo, wrap-up, names, folders and memory (read before every piece)
├── standards.md          ← universal standards U1–U13 (cited by the modules)
├── operations.md         ← Failure Rule, one-time approval, spending, credentials, connectors and rights
├── MAINTENANCE.md       ← shared source, changing the agent and publishing (read only when touching the skill)
├── modules\            ← read only when the request is of that type (consolidated by domain)
│   ├── briefing.md     ← briefing translator (only what belongs to the designer)
│   ├── ads.md          ← single studio for advertising pieces and references: direction, engines (uiux first), composition, formats, analysis and adjustment (absorbed referencias.md)
│   ├── video.md        ← single studio for video and motion: cut, motion (kit, template or animated page), caption, voice, script and AI direction (replaces reel.md)
│   ├── html.md         ← single studio for HTML: LP, site, form, extract, embed, recreate, tokens, report and deck (replaces html-extrair, html-relatorio and deck)
│   ├── kv-logo.md      ← Cold Start, MIV Scanner, Brand Book, new Logo and Design System (tokens/DESIGN.md)
│   ├── image.md       ← arsenal, multimodal reading/analysis, visual OCR, prompt, photography, Vision Decomposer, Pass³
│   ├── image-product.md ← appendix: faithful product / 360 / turnaround
│   ├── image-character.md ← appendix: recurring face
│   ├── figma.md        ← 1:1 assembly in Figma after approval
│   ├── pen.md          ← quick prototyping (absorbed `pen_engine\SKILL.md`)
│   └── quality.md    ← final check by type (generic artifacts, a11y, motion, deck, copy, QA)
├── assets\             ← generate_image.py · generate_audio.py · check_image.py · caption_reels.py · base_lp.html · check_html.py · form-validation.js/.css · base_deck.html · check_deck.py
├── engines\uiux\       ← offline engine of palettes, fonts, LP patterns and UX rules
├── engines\designlang\ ← token extraction from a site (install dependencies only with approval)
├── references\  figma_engine\  ← taste\ motion\ logo\ huashu\ variants\ alternatives.md (on-demand appendices)
├── Clients\_CLIENT_TEMPLATE\  ← design_system.md + historico.md + mapa.md (client card read by the scripts)
├── NOTICE.md           ← third-party license notices (compliance; not read by the agent)
└── Installer.cmd      ← universal installer for all IDEs (do not analyze)
```

Each client's memory lives in `D:\Clientes\[Cliente]\_DESIGN\` (`design_system.md` + `historico.md` + `templates\`). Nothing of a client lives in this folder.

## How to change
1. Ask for the change ("update /designer-mestre: ...").
2. The agent records the change in the source and in the changelog; before approval, it neither installs nor publishes.
3. After approval, the agent installs and verifies by SHA-256, only when explicitly requested, syncs the relevant files and metadata on GitHub, and updates the public list to keep only the four most recent notes.

Only universal rules go here. A client preference goes in their `design_system.md`.

## Changelog
- v21.8 (2026-11-03): pending list closed (tests move to real deliveries, core cap about 16 KB, ffmpeg CPU exception declared); the closing reply never says Done while pending items are open.
- v21.7 (2026-11-03): ads rules: live-site H1 and palette before composing, one closed copy across formats, outlined SVG with every editable SVG.
- v21.6 (2026-11-03): `skill_alerts` line names the 3 most urgent open items with a suggested resolution; README documents the source folder name.
- v21.5 (2026-11-03): closing reply after the final approval is a single checklist in the core §0.8 (wrap-up with the `Exportados` folder, folder reveal, `skill_alerts`, `/aprenda` diagnosis).

## Model Efficiency in the IDE
Choose by the work, not by a fixed brand. Names, availability and limits change; use the IDE's selector to confirm the current model. Prefer mechanical deterministic tasks to a generative model when a script/tool already does the job. Vision models analyze references, but that does not mean they also generate or edit images.

| Work | Anthropic Claude | OpenAI / ChatGPT | Google Gemini | GitHub Copilot |
|---|---|---|---|---|
| One-off adjustment, simple QA, short reading | **Haiku 5.5** — high scale and low latency | **GPT-6 Luna** — focused tasks and high volume | **Gemini 3.5 Flash-Lite** — fast high-volume execution | **Auto · Efficiency**, or GPT-6 Luna if it appears in the selector |
| Frontend, SVG, HTML, forms, Figma and daily iteration | **Sonnet 5.5** — balance of speed and capability | **GPT-6.1 Sol** — complex coding at a lower cost than Astra; test in the IDE flow | **Gemini 3.8 Flash** — long-running software engineering; preview in the consulted catalog | **Auto · Balance**; GPT-5.6 Terra for general coding or GPT-6 Sol for agentic coding, if available |
| Architecture, Cold Start, Design System, long Brand Book or hard debugging | **Opus 5.5** for long agentic coding; **Fable 5.1** for the most demanding reasoning | **GPT-6 Astra** — demanding reasoning and coding work | **Gemini 4 Argon** — complex software engineering and autonomous agents | **Auto · Intelligence**; GPT-6 Astra for long agentic tasks, if available |
| Briefing with images, visual references or screenshot reading | Current Claude models accept images; check availability in the IDE | Current GPT with image input enabled | Multimodal Gemini with image input | Available model that accepts images; support depends on the selector/integration |

The names above are the models/families that appear in the documentation consulted on **2026-10-22**; some, like Gemini 3.8 Flash, are in preview. Confirm version, availability and price in the product in use: API catalog, ChatGPT and the Copilot selector are not interchangeable. Vision models analyze references, but that does not mean they also generate or edit images.

**Operational and token standard:** start with the balanced model for code/layout; step down to a fast option on small, verifiable tasks; escalate to stronger reasoning when there is ambiguity, extensive context or structural decisions. Reduce context by bringing only the core, the module and the relevant files; provide briefing, constraints and QA criteria once in a compact format; use existing scripts for deterministic validations instead of asking the model to redo the check through text. In Copilot, the **Efficiency / Balance / Intelligence** tiers adjust the priority of cost, balance or quality of automatic routing. To really choose, compare with the same briefing, files, criteria and QA. In UI, measure the full cycle until approval — iterations and visual corrections included — not just speed or tokens per call. There is no reproducible public benchmark cited here that proves a single winner for visual frontend.

**GitHub community signal (anecdotal):** in [“Mocking Up the UI Before AI Builds It”](https://github.com/mattbrailsford/mattbrailsford.dev/discussions/77), the author reports, in one project, that about 60% of late adjustments were to match the existing interface and 30% were decisions about content/presentation; proposes lightweight HTML mockups before coding. It is an individual experience, not a model comparison or benchmark; it indicates that previews and early visual criteria can reduce correction cycles, not that a specific brand is superior.

### Research and references
The recommendations summarize capabilities and profiles declared by the vendors; they do not establish a ranking among brands. Official documentation:

- Anthropic: [Models overview](https://platform.claude.com/docs/en/models/overview) · [Choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
- OpenAI: [Models](https://developers.openai.com/api/docs/models) · [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) · [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) · [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra)
- Google: [Gemini models](https://ai.google.dev/gemini-api/docs/models) · [Gemini 3.8 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) · [Gemini 4 Argon](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon)
- GitHub Copilot: [Model comparison](https://docs.github.com/en/copilot/reference/ai-models/model-comparison) · [Auto model selection and tiers](https://docs.github.com/en/copilot/concepts/models/auto-model-selection)
- Community: [Mocking Up the UI Before AI Builds It](https://github.com/mattbrailsford/mattbrailsford.dev/discussions/77) — report on mockups and UI rework, not a comparative model test.
