# /product-concept fusion · traceability (the agent does not read)
Sources downloaded on 26/10/2026 and read in full (MIT by the fusion's author; the others by full extraction, table of 130 techniques). No external skill was installed.

| Source | Commit | License | State |
|---|---|---|---|
| sanky369/vibe-building-skills (creative-strategist, product-photography, shot-library) | e9714d8 | MIT | technique incorporated in our own text |
| jau123/MeiGen-AI-Design-MCP (product-photoshoot) | aef26a2 | MIT | technique incorporated; paid tools excluded |
| natsany/conceptual-photography-plan (SKILL + 3 references) | cca3595 | absent | technique only, our own text; license pending |
| gupsammy/Claudest (generate-image + 3 references) | 20c43ec | absent | technique only, our own text; license pending |
| inference-sh/skills (2 product photo guides) | 0cbf91c | absent | technique only, our own text; license pending |

| # | Capability | Origin | Destination and activation |
|---|---|---|---|
| 1 | Understand product, use, and natural world | sanky369, MeiGen, inference-sh | `image-product.md` §5 step 1; `library.md` §1 |
| 2 | Study the client and each reference (applies/does-not-apply verdict) | Designer Mestre only | `referencias.md` §§3–5, `guia.md`, `design_system.md`, `historico.md` |
| 3 | Choose concept, filters, anti-repetition | natsany, sanky369 | §5 step 2; `library.md` §2; `historico.md` `[CONCEITO]` |
| 4 | Integrated scene, background and surface, composition | sanky369, inference-sh, natsany | `library.md` §3; Pass³ (`image.md` §6). Light, shadow, angle, and optics already existed in `image.md` B §§2–3 and Part C: not duplicated |
| 5 | Prose prompt, positive exclusion, hyper-specific | gupsammy, natsany | `image.md` B1 (new positive exclusion); the rest already covered |
| 6 | References, editing, batch, continuity | gupsammy, MeiGen | `image.md` B1 (new references and editing); `library.md` §4 |
| 7 | Beauty and AI look | natsany | `library.md` §5; §5 step 5 |
| 8 | Feedback and variety | natsany, gupsammy | `library.md` §6; §5 steps 2 and 5 |

Excluded, with reason: recipes for light, shadow, angle, and film vocabulary (`image.md` already covers the principles and avoids presets); white-background packshot, Amazon requirements, and the 9-image sequence (already covered by `ads.md` and by the 360); inference.sh CLI, MeiGen API, Gemini/Nano Banana, and Midjourney flags (the author's tool); rules for people, 3:4 format, and scoring weights (the author's preference); mechanical engineering of props (object × object concept, outside brand scope); video frame extraction (video route).
Gap in the sources: none teaches choosing a concept from the product nor studying the client's references; those capabilities come from Designer Mestre itself (lines 2 and 3).
Pending: license of the three sources without a license; test `/product-concept` on a real piece (nothing has been generated yet).
