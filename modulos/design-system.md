# Módulo Design System

Referência + logo + tipografia → análise → tokens → prévia para aprovação → variáveis e componentes no Figma (`figma-generate-library` + `modulos/figma.md`). Ordem no Figma: variáveis primeiro, depois componentes com variantes e estados ligados aos tokens. Código existente: Code Connect.

## Fonte da verdade
O `_DESIGN\design_system.md` do cliente (`STATUS_KV: VALIDADO`). Tudo abaixo é **derivado** dele, gerado sob pedido e nunca editado à mão (editar = mudar o `design_system.md` e regerar).

## Tokens obrigatórios (camadas)
- **A1 · a marca precisa declarar:** `--bg` `--fg` `--accent` `--font-display`.
- **A2 · obrigatórios com padrão:** `--fg-2` `--surface` `--border` `--success` `--error` `--font-body` `--radius` `--space-4` (16 px) `--motion-fast` (0.18 s).
- **B · apelidos permitidos:** `--fg-2: var(--fg);` quando o KV não define.
- Nome por **função**, nunca por cor (`--accent`, não `--laranja`).

## Exportações (sob pedido: "exporta o design system", LP, outro agente/ferramenta)
Salvar em `_DESIGN\export\`:
1. **`tokens.css`** — `:root{}` com A1+A2+B e escala de tipo (`--fs-display` … `--fs-caption`, razão 1.2–1.25). É o que o `html.md` importa/cola no `<style>`.
2. **`DESIGN.md`** (formato aberto usado por Stitch e repositórios de DESIGN.md) — frontmatter YAML com tokens + prosa:
```yaml
---
version: alpha
name: [Cliente]
description: [conceito em 1 frase]
colors: { primary: "#…", ink: "#…", canvas: "#…", accent: "#…" }
typography:
  display: { fontFamily: "…", fontSize: 56px, fontWeight: 700, lineHeight: 1.05, letterSpacing: -1px }
  body:    { fontFamily: "…", fontSize: 16px, fontWeight: 400, lineHeight: 1.5 }
---
```
Seções H2 (≥ 7): Overview · Colors · Typography · Layout · Elevation & Depth · Shapes · Components · Do's and Don'ts · Responsive Behavior. Componentes referenciam tokens como `{colors.primary}`. Do's and Don'ts = o `## 1. NÃO FAZER` e `## 2. O QUE FAZER` do cliente, como regras curtas ("Don't recolor the logo").
3. **Prévia** HTML única: swatches com HEX e contraste (`img_qa.py contraste`), escala tipográfica, botões nos estados Primary/Secondary/Ghost/Disabled, cards com elevação.

## Gravar
Tokens, O Que Fazer, O Que Não Fazer e mapa de diretórios no `design_system.md` do cliente; link no `historico.md`. Os arquivos de `export\` não são lidos pelo Gate de KV.
