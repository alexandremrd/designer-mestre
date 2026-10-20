# Módulo pen.dev (opcional)

Para explorar ou gerar rápido, ou quando pedido com `/pen`. O resultado é rascunho; a peça final vai ao Figma (`modulos/figma.md`). Detalhes do CLI na skill `pen-design`, se instalada.

1. **Setup:** `which pen || npm install -g @pen.dev/cli`. Sem permissão, usar `npx pen`. Conferir a versão.
2. **Autenticação:** `pen status`. Precisa de usuário pen.dev, com login feito pelo usuário, e de agente autenticado. Não criar conta nem digitar senha ou código; se faltar, explicar e parar.
3. **Prompt:** o briefing literal. `design_system.md` do cliente entram como anexo `-f`, junto com fotos e referências. O `.lib.pen` do cliente entra com `-l`.
4. **Comando:** `pen --out <nome>.pen --prompt "<briefing>" -f <design_system.md> --export <nome>.png --export-scale 2`, com timeout ≥ 600000 ms. Avisar que leva 1–5 min. Iterar com `--in`.
5. **Logo:** nunca gerada pelo pen.dev. Usar placeholder e inserir o arquivo oficial depois. Abrir o PNG e conferir.
6. Salvar em `Trabalho\` da pasta da solicitação e registrar no `historico.md`.
