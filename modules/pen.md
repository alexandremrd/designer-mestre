# Headless Vector Canvas Module (`.pen`) — Fast Exploration of Screens, Mockups and Dashboards

Optional module for fast exploration of app layouts, dashboards, wireframes and mockups structured as vector JSON (`.pen`) rendered to PNG 2×/4×. The result works as a preview/draft; final delivery follows `delivery.md` §2.

1. **Setup:** check availability of the local `pen` binary (`pen version`).
2. **Authentication:** `pen status`. Requires a session authenticated by the user; never create an account nor type passwords/codes automatically — if not authenticated, use the agent's native HTML/SVG generation or warn in 1 line.
3. **Prompt:** pass the literal briefing and attach the client's `design_system.md` with `-f` (along with photos/references) and a `.lib.pen` library with `-l` when one exists.
4. **Execution and Iteration:**
   - Create: `pen --out <name>.pen --prompt "<briefing>" -f <design_system.md> --export <name>.png --export-scale 2` (timeout ≥ 600000 ms).
   - Iterate preserving the node tree: `pen --in <v1>.pen --out <v2>.pen --prompt "<targeted adjustment>" --export <v2>.png --export-scale 2`.
5. **Logo:** never AI-generated. Use a placeholder and apply the official vector file afterward.
6. Save in `Trabalho\` of the request folder and record in `historico.md`.
7. **Flags:** `--out/-o` (required) · `--prompt/-p` · `--prompt-file/-f` · `--in/-i` (iterate) · `--export/-e` (`.png` `.webp` `.pdf`) · `--export-scale` (default 2) · `--agent` (`claude` `google` `codex`). Help: `pen --help`.
