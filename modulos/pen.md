# Módulo Canvas Vetorial Headless (`.pen`) — Exploração Rápida de Telas, Mockups e Dashboards

Módulo opcional para exploração rápida de layouts de aplicativos, dashboards, wireframes e mockups estruturados em JSON vetorial (`.pen`) renderizados em PNG 2×/4×. O resultado funciona como prévia/rascunho; a entrega final segue o núcleo §2.

1. **Setup:** verificar disponibilidade do binário local `pen` (`pen version`).
2. **Autenticação:** `pen status`. Requer sessão autenticada pelo usuário; nunca criar conta nem digitar senhas/códigos automaticamente — se não estiver autenticado, usar a geração nativa em HTML/SVG do agente ou avisar em 1 linha.
3. **Prompt:** passar o briefing literal e anexar o `design_system.md` do cliente com `-f` (junto com fotos/referências) e biblioteca `.lib.pen` com `-l` quando existir.
4. **Execução e Iteração:**
   - Criar: `pen --out <nome>.pen --prompt "<briefing>" -f <design_system.md> --export <nome>.png --export-scale 2` (timeout ≥ 600000 ms).
   - Iterar preservando a árvore de nós: `pen --in <v1>.pen --out <v2>.pen --prompt "<ajuste pontual>" --export <v2>.png --export-scale 2`.
5. **Logo:** nunca gerada por IA. Usar placeholder e aplicar o arquivo vetorial oficial depois.
6. Salvar em `Trabalho\` da pasta da solicitação e registrar no `historico.md`.
7. **Flags:** `--out/-o` (obrigatório) · `--prompt/-p` · `--prompt-file/-f` · `--in/-i` (iterar) · `--export/-e` (`.png` `.webp` `.pdf`) · `--export-scale` (padrão 2) · `--agent` (`claude` `google` `codex`). Ajuda: `pen --help`.
