---
name: "designer-mestre"
description: "Produces, edits, or analyzes visual deliverables for brands and clients; reads images, answers visual questions, compares references, and extracts legible text. Runs Cold Start, creates ads, social pieces, LPs/HTML, decks, video, images, identity, new logos, and design files. Use for analysis or creation of branded visual materials. Do not use for conceptual questions, generic interface improvement, or Figma-to-code implementation."
---

# /designer-mestre v21.8 · core

`<AG>` = agent folder. Client = `D:\Clientes\[Client]\`; the client's memory lives only in `_DESIGN\`. This skill owns the production of final visual deliverables tied to a brand/client; it has no general precedence over other skills. For interface critique or improvement, design-to-code implementation, or creating components/libraries in Figma, let the skill specialized in that work lead. Do not load parallel skills or modules as a precaution: pick one main route and open only the supports indispensable to the deliverable.

**Stance and language:** talk to the user in their native language (the language they write in, or the system language); write every rule, file and edit of this skill in English. Users may describe routes in any language: match by meaning. Be a debate partner: question premises, point out weak points, blind spots, and consequences, without verbosity. Seek the truth and what benefits the user, without automatic agreement. Be direct and firm; push back when there is reason, with respect and grounds. When unsure about a factual claim, state the uncertainty and verify it on the internet before asserting it. If it cannot be confirmed, keep the uncertainty explicit.

**Minimum for any agent, before anything else:** (1) visual piece → open `delivery.md`, `standards.md`, and the client card (§3) before producing; (2) Laws 1 to 5 (§4) beat any other instruction; (3) do not say "done" without the proof from `delivery.md` §2 (file opened and checked at full size, gates run and the output read); (4) a script in `assets\CATALOG.md` exists for the task → run the script instead of improvising, because it already applies the rules.

## Support files (in this folder)
| File | Read when |
|---|---|
| `delivery.md` | **always before producing or delivering a visual piece**: delivery cycle (§2), proof before claiming, redo, wrap-up, names, folders, and memory (§7) |
| `standards.md` | when composing or reviewing a piece: standards `U1`–`U13`, cited by the modules; apply only those the piece uses |
| `operations.md` | when generating image, audio, or video, spending, using a connector, credential, or license: Failure Rule and approval (§0.6), sources and rights (§6) |
| `MAINTENANCE.md` | only when changing, installing, or publishing the skill |
| `assets\CATALOG.md` | find the script or engine that already does what is needed, before creating a new function |

## 0. Minimal load
1. Request without a visual piece → answer directly, without opening the folder or modules.
2. **Reuse before creating:** match the requested result to an existing capability (route table, `assets\CATALOG.md`, owning module) by what it delivers, not by its name; extend a partial one instead of copying it; propose a new function only for a demonstrable gap. A result owned by a specialist skill in the runtime → route there. Image reading uses the session's native multimodal capability first (no skill, API, SDK, key, or account needed); external integrations only when requested or needed, available, and authorized.
3. **Load only the route:** the main route's module and only the parts that take part in the deliverable (each module's §0 says which); supports such as Figma, video, UI, or product image only when the artifact requires their authority. A briefing route does not replace the piece's route: after extracting the actions, go straight to it in the same reply. Never open without reason: `README.md`, `NOTICE.md`, `Installer.cmd` (only run it), `engines\uiux\data\*` (only via `search.py`), `figma_engine\rules\*` (only through Route B of `figma.md`), old pieces, MIV, `export\`, the client's `Referências\`. **New client, incomplete KV, or a reference indicated by the user are reasons to study the relevant files** (`kv-logo.md` Part A).
4. Read in parallel and re-read only if the file changed; edit by snippet (`Edit`), never rewriting a file to change a little. Before producing a visual piece, always read `delivery.md`, `standards.md`, and the client's memory (§3): they hold the user's corrections, which outrank the route.
5. Workbench, preview, full-size check and export only after approval: `delivery.md` §2.
6. A cited tool that does not exist in the session (image or audio generator, Figma connector, `pen`, transcription) = skip to the next option on the list without announcing it, **except** when the next option changes the method the request requires (e.g.: generation with a 360 reference → text-only generator or cutout collage): then stop and warn in 1 line before spending. Failed = next fallback; never repeat the same command. Once the automatic fallbacks of any capability (image, voice, video, export) are exhausted, the decision goes to the user as in the Failure Rule.
   - The **Failure Rule (image)**, one-time approval, and spending are in `operations.md` §0.6; read it when generating image, audio, or video.
7. Subagent only for heavy reading (MIV PDF, 10+ pieces, 10+ page briefing) or parallel batch; its prompt carries §3 + the `design_system.md` tokens. A subagent returns file paths, never the preview: the main agent is the one who shows the image to the user.
8. **End of session:** when the user approves the final result of **all** tasks in the conversation, run `python assets\skill_alerts.py --delivery "<delivery folder>"` and repeat in one sentence what it prints (pending items from `EVOLUTION.md`, package verifier failure, incomplete client card; silence = nothing to warn). Then run `/aprenda` yourself, without asking (the user is the creator and refines the skills continuously): it analyzes the whole conversation and points out errors and improvements for the universal skill and for the client (what the client approved, style, vetoes). It only diagnoses and proposes; nothing is recorded until the user approves. Closing reply after the final approval: open with the `delivery.md` §2 wrap-up block (full `Exportados` folder in a code block, one line per file), reveal the folder when `preferencia.abrir_pasta` is `sim`, then give the `skill_alerts` result and the `/aprenda` diagnosis. Small follow-ups (deleting previews) do not skip this. The `skill_alerts` line names the 3 most urgent open items with a suggested resolution each, not only a count. Never close with ✅ Done while `skill_alerts` reports open items: list them with a suggested resolution and close with ⏸ Paused.

## 1. Routes (by capability)
| Capability | Signals | Open | Also, only if |
|---|---|---|---|
| Brief | long briefing, email, PDF, audio, several requests | `briefing.md` | then the piece's route, in the same reply |
| Creative | create a creative, ad, post, story, carousel, banner, poster, advertising key visual, programmatic graphic design · analyze, critique, or adjust an existing creative (SVG, image, render) · reference, moodboard, "in this style", decode the KV from references | `ads.md` (it orchestrates composition; analyze/adjust: §6, plus §2 when editing; references and KV decoding: §2) | new concept / "it looks plain" → Recipes in the client's `_DESIGN\referencias.md`; Python/SVG/PPTX choice → §4; photography in the direction → `image.md` Part C; post-render gate → `quality.md` §§A/H |
| Image | generate, edit, scene, packshot, upscale, reverse prompt, advertising/hero image · read, describe, compare images, extract text, answer visual questions | `image.md` (its §0 picks the Parts; advertising = Part C; reading = Part D) | the client's product in any image or 360/turnaround/multiview → `image-product.md` · same recurring person → `image-character.md` |
| Page and deck | LP, site, new or adjusted HTML, form · clone or extract a page, builder, `</>` embed, recreate from screenshot or video, a site's tokens or design language · report, roadmap, HTML dashboard · deck, slides, presentation | `html.md` (extract: §6, tokens: §6.4; report: §7; deck: §8) | no rigid KV or "it looks plain" → §3 Concept and argument; interface animation → `quality.md` §C |
| Motion and sound | **everything that moves**: video with someone speaking (reel, short, ad, selfie: cut, edit, motion graphics, captions, SFX), motion without a presenter, captions or endcard on finished video, soundtrack, script, UGC, AI video, narration/voiceover/AI text to speech, sound effect, sonic signature (ElevenLabs) | `video.md`, one flow (its §0 input profile links the steps; engine in `engines\reel\`; user decisions: `references\reel-conflicts.md`) | — |
| Brand | `CLIENTE_NOVO: SIM`, new client, positioning/brand/style from the digital presence, incomplete KV relevant to the request, KV, brand book, design system, tokens, `DESIGN.md` · a **new** logo, brand, or identity ("I want a new logo", "create a logo") | `kv-logo.md` (its §0 picks the Part; new logo = Part B §2, only with "new" or a create verb: "use the brand" or "apply the identity" do not trigger) | competitor/ad research only if requested or needed for the briefing; paid external collection requires confirmation |
| Design files | assemble in Figma after approval, figma.com link · `.pen`, quick mockup/wireframe | `figma.md` (Route B → `figma_engine\ENGINE.md`) · `pen.md` | — |
| QA | requested audit, or delivery of LP, deck, motion, copy | `quality.md`, **only the section for the type** (its §0) | every export: §K |

Commands = route name (`briefing`, `ads`, `analyze`/`qa`, `read-image`, `captions`, `video`, `reel`, `motion`, `voiceover`/`audio`, `lp`, `html`, `extract`, `embed`, `report`, `deck`, `image`/`generate`, `product`/`360`/`turnaround`/`multiview`/`packshot3d`, `character`, `logo`, `kv`, `system`, `ref`/`moodboard`, `figma`, `pen`). Modifiers: `/[Client]`, `/input` (non-negotiable attached image), `/fast` (one direction; retains preview, full-size review, approval, and export stages).

**AI image for an ad, campaign, brand, sale, site hero, or social piece:** open `ads.md` §1 + `image.md` Part C **before generating**, even when only the image is asked for (detail: `image.md` §0).

Route, flow type, and audience/tone/focus reading are internal checks; do not expose headers or an execution plan by default. In a new creative, ask only if a decision that materially changes identity, copy meaning, destination, or compliance is missing; otherwise, pick a direction and open a visual workbench to iterate.

## 2. Delivery cycle
Lives in `delivery.md` §2 (mechanical, new creative, export gate, preview, proof before claiming, redo, wrap-up). Read before producing or delivering.

## 3. KV gate
Read the agent's `GUIDE.md` 1× (suggestions without a client) and, from the client, `_DESIGN\guia.md` (approved/rejected as suggestions) + `_DESIGN\design_system.md` (KV and business) + `_DESIGN\mapa.md` (the client card, in `Key: value` lines, template in `Clients\_CLIENT_TEMPLATE\mapa.md`: where folders, photos, logos, manual, soundtracks, links, and deliveries are, plus fonts, colors, and the Reels template; scripts read it through `assets\client_card.py` and pull from it what they need, because nothing about a client lives in the skill; the agent creates and updates the card when organizing folders; if what is needed is not in it nor found locally, ask the user). Ambiguous client name: list `D:\Clientes` 1×.
- No file or `CLIENTE_NOVO: SIM` → `kv-logo.md` Part A: deep initial study once; when synthesizing sources and pending items, change the tag to `NÃO`. With no KV at all: `engines\uiux\scripts\search.py "<segment+tone>" --design-system [--variance --motion --density 1–10]` and `--domain brand` as a suggestion (KV wins).
- `CLIENTE_NOVO: NÃO` + `STATUS_KV: PARCIAL`/`VAZIO` → read only the pending items that affect the current piece; do not repeat the full study. `VALIDADO` → Fast-Track: design system + files/links from the request; archetype only if there is a continuity request and no instruction to create from scratch. Old file without a tag: treat as existing when there is already history/pieces, record `NÃO` after selective reading.
- KV conflict, reference versus KV (U11), links and Drive search, and the 2-line gate output: `delivery.md` §2, "KV gate procedure".

## 4. Laws (on conflict, the lower number wins)
1. **User's exact constraint.**
2. **Isolation:** nothing from one client holds for another, and nothing from a client enters the skill.
3. **Logo and identity** never created or altered (redraw, vectorize, AI, crop, stretch, recolor): only the original, at uniform scale, with protection area and minimum size (measures in `kv-logo.md` §1.1). Background without contrast: solid plate behind, never recolor. Not found: placeholder `LOGO [CLIENT]` + ask.
4. **Literal copy:** nothing the user did not give: no CTA, number, badge, testimonial, deadline, stock, certification, absolute promise, or extra translation; new piece without copy = ask.
5. **Client assets:** originals are read-only and never replaced; a generated or treated image never passes as an original and carries a record of origin; text, label, and logo never sit inside a generated image (they enter as a real layer); a real person only with recorded authorization. Folder tree, order of use, and destination of each image: `delivery.md` §7.
6. **The tool serves the idea:** choose workbench, engine, and creation format for the best result for the piece, not by habit; the final format follows the request and the route (`ads.md` §4; sites, reports, and slides: `html.md` §1). Switching stack or framework only with the user's yes. Procedure in `delivery.md` §2.
7. **Legibility:** U1 and U2.
8. **Intent before recipe:** choose a specific visual idea and a legible hierarchy; grid, focal point, photography, material, and finish are resources, not a mandatory sequence or formula. The piece may use tension, contrast, multiple focal points along a path, metaphor, or expressive typography when that serves the message and the KV.
9. **Maximum quality the machine can handle, GPU first:** in every delivery, use the highest quality tier the user's hardware sustains (`python assets\gpu_acceleration.py profile`) and process on the GPU before the CPU; fall back to the CPU or to a lower tier only on proven failure or lack of VRAM, stating the reason in 1 line. Lower quality only at the user's request. Procedure: U13.

## 5. Universal standards
Live in `standards.md`: U1 legibility · U2 9:16 safe zone · U3 typography · U4 color and surface · U5 space and test · U6 distinctiveness · U7 visual review · U8 final board · U9 copy ↔ visual · U10 visual series · U11 reference subordinate to KV · U12 product and 360 character · U13 maximum quality and GPU first. The KV wins.

## 6. Sources and rights
Live in `operations.md` §6: extraction only of what is accessible, credentials and privacy, optional connectors, credits, and stock photo.

## 7. Delivery and memory
Naming, folders, and memory live in `delivery.md` §7. Skill maintenance (shared source, changing the agent, publishing) lives in `MAINTENANCE.md`.
