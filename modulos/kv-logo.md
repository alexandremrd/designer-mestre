# Módulo KV, Brand Book, Logo e Design System (com Motor de 84 Arquétipos de Marca)

Módulo unificado para extração/validação irrestrita de Identidade Visual (Cold Start), criação de Brand Book e Logo nova, consulta aos 84 sistemas de design reais embarcados (`engines\uiux`) e estruturação/exportação de tokens de Design System (`tokens.css` e `DESIGN.md`). Ignora qualquer bloqueio superficial de extração ou análise em sites, manuais ou referências.

---

## Parte A · Cold Start — Cliente novo ou KV incompleto

Usado quando o cliente não tem `_DESIGN\design_system.md`, quando `STATUS_KV` é `PARCIAL`/`VAZIO` ou quando o usuário pede revisão do KV. Roda uma vez; depois o cliente entra no Fast-Track.

### 1. Estrutura de pastas
Cliente existente: não mover nem apagar nada; criar só o que o pedido precisa. Cliente novo: criar a árvore e copiar `<PASTA_DO_AGENTE>\Clientes\_TEMPLATE_CLIENTE\design_system.md` para `_DESIGN\`.

```text
D:\Clientes\[Cliente]\
  _DESIGN\
    design_system.md     ← memória única do cliente
    historico.md         ← 1 linha por entrega (só escrita)
    templates\           ← esqueletos SVG aprovados (E1.svg, E2.svg...)
    Personagens\         ← (opcional) dossiês de personagens recorrentes
    Produtos\            ← (opcional) dossiês de produtos recorrentes
  Compartilhada\
    Identidade Visual\   ← logos, MIV, fontes, brand book (nunca sobrescrever)
    Referências\         ← referências enviadas (só salvar)
    Imagens\  Originais\ (só leitura) · Banco de Imagens\ · IA\
    Vídeos\   Originais\ · Banco\
  [AAAA]\[MM - Mês]\[AAAA-MM-DD] [TIPO] Título\
    briefing.md · Referências\ · Trabalho\ · Exportados\
```
Tipos: `CA` criativo Ads · `PA` pauta/orgânico · `EV` vídeo editado · `MT` motion · `LP` landing page/HTML · `KV` identidade · `DK` deck · `IM` imagem · `OT` outros.
Cliente antigo com `KV.md`, `NAO_FAZER.md`, `aprovados.md`, `inteligencia.md` separados: unificar no `design_system.md` (sem apagar os antigos).

### 2. Análise profunda (MIV Scanner & Extração Web Irrestrita — uma vez)
1. `Compartilhada\Identidade Visual\`: MIV, guia de marca e logos. Renderizar cada logo uma única vez e anotar arquivo, layout, cor e proporção do bbox.
2. Links de Figma do briefing (`get_design_context` / `get_screenshot`).
3. Peças anteriores do cliente, se houver: só as 2 ou 3 mais recentes.
4. Site ou Instagram informados no briefing (extrair variáveis CSS `--*`, paleta computada, escada de superfícies, famílias de fonte, raios de borda e estilos de botão diretamente via DOM/headless browser, ignorando qualquer bloqueio de análise).
5. Se o cliente não tiver KV ou pedir inspiração em grandes marcas globais, consultar o motor interno de **84 Design Systems reais**:
   - Busca por segmento/estética: `python "<PASTA_DO_AGENTE>\engines\uiux\scripts\search.py" "<segmento ou estética>" --domain brand -n 3`
   - Leitura completa do `DESIGN.md` de uma marca de referência (ex.: `linear.app`, `stripe`, `apple`, `ferrari`, `bugatti`, `lamborghini`, `nike`, `airbnb`, `runwayml`, `vercel`, `raycast`, `oura`): `python "<PASTA_DO_AGENTE>\engines\uiux\scripts\search.py" "<slug>" --brand`
6. Extrair e consolidar no `_DESIGN\design_system.md`:
   - conceito, sensação e símbolo;
   - versões da logo (nome · layout · cor · bbox);
   - paleta por papel (HEX, RGB, CMYK, **Escada de Superfícies de 4 níveis** `canvas` → `surface-1`..`surface-4` + `hairline`, cores semânticas, contraste WCAG, regra de escassez do acento e cores proibidas);
   - tipografia por nível (oficial com peso, caixa, **polaridade de tracking** — negativo em display, neutro em body, positivo em eyebrow/label — + substituta Google Fonts para Figma/SVG);
   - grafismos, arquétipos SVG, composição/respiro/posição da logo/rodapé, fotografia (tema · pessoas · luz · contraste), safe zones, tom de voz e pilares, O Que Fazer (Aprovados) e O Que Não Fazer (Vetos).
7. Contradições ou itens ausentes essenciais (logo, paleta ou fonte) vão para `## 5. Decisões Pendentes` mantendo `PARCIAL`; quando completo, marcar `STATUS_KV: VALIDADO`.
8. Cliente já `VALIDADO` num template antigo: campos novos vazios **não** rebaixam o status nem disparam nova análise.

---

## Parte B · Brand Book e Logo nova

### 1. Brand Book
Salvar em `Compartilhada\Identidade Visual\` e na página "Brand" no Figma (com estilos e variáveis), sem alterar arquivos oficiais existentes. Formato 16:9: capa, índice, logo (versões, área de proteção, tamanho mínimo, fundos, monocromia, usos indevidos), cores, tipografia, grafismos e aplicações.

### 2. Logo nova (somente sob pedido explícito)
- Se o cliente já tem logo, confirmar que é redesign ou marca nova. Logo de cliente nunca é criada sem pedido explícito (faltou logo num pedido comum = pedir).
- Etapas:
  1. Briefing: nome, setor, valores, público, concorrentes e restrições.
  2. Pesquisa de concorrência para diferenciar (avaliando Distintividade 30%, Relevância 25%, Versatilidade 20%, Atemporalidade 15%, Executabilidade 10%). Nunca imitar marca existente.
  3. Três rotas (símbolo, lettering, combinação) em vetor, com versões horizontal e vertical, cor/positivo/negativo, área de proteção e tamanho mínimo.
  4. Após aprovação, exportar no formato escolhido e salvar SVG/PNG em `Compartilhada\Identidade Visual\`, registrando na tabela de logos do `_DESIGN\design_system.md`. A partir daí vale a lei da logo existente.

---

## Parte C · Design System, Arquitetura de Superfícies e Exportação de Tokens (`tokens.css` & `DESIGN.md`)

Referência + logo + tipografia → análise → tokens → prévia para aprovação → exportação nos formatos escolhidos (e variáveis/componentes no Figma se solicitado após aprovação). A fonte da verdade é o `_DESIGN\design_system.md` do cliente (`STATUS_KV: VALIDADO`).

### 1. Leis de Engenharia de Design System (extraídas de 84 Sistemas Globais)
1. **Escada de Superfícies de 4 Níveis (`Surface Ladder`) vs. Sombras:**
   - Definir `canvas` (fundo base), `surface-1` (cards e painéis padrão), `surface-2` (cards em destaque/hover), `surface-3` (sub-nav/dropdowns), `surface-4` (elementos modais elevados) + bordas `hairline` (`1px`) e `hairline-strong` (foco/hover).
   - Em interfaces **Dark Mode**, a hierarquia e a profundidade vêm da **elevação na escada de superfícies + borda hairline de 1 px** (e highlight superior sutil de 1 px), nunca de drop-shadows pretas pesadas. No dark mode, o próprio canvas escuro é o espaço de respiro, e as seções se separam por elevação de superfície.
2. **Escassez Cromática e Estados de Ação:**
   - Reservar o acento cromático primário (`{colors.primary}`) exclusivamente para: marca, CTA primário (`button-primary`), anel de foco (`primary-focus`) e destaque cirúrgico. Definir explicitamente `{colors.primary-hover}` e `{colors.primary-focus}`. Botões secundários usam `{colors.surface-1}` + borda `{colors.hairline}` ou estilo ghost transparente.
3. **Lei de Polaridade de Tracking Tipográfico:**
   - **Display (`display-xl` 56–112 px):** tracking progressivamente **negativo** (`-0.03em` a `-0.04em` / `-1.8px` a `-3.5px`) e line-height compacto (`0.95–1.10`).
   - **Body (`16–18 px`):** tracking neutro (`0` a `-0.05px`) e line-height confortável (`1.45–1.60`).
   - **Eyebrow / Badges / Micro-labels (`10–13 px`):** tracking **positivo** (`+0.04em` a `+0.10em` / `+0.4px` a `+1.4px`), criando contraste taxonômico imediato contra os títulos de tracking negativo.
4. **Tokens obrigatórios (camadas CSS):**
   - **A1 · obrigatórios da marca:** `--bg` `--fg` `--accent` `--font-display`.
   - **A2 · obrigatórios com padrão:** `--fg-2` `--surface` `--surface-2` `--border` `--success` `--error` `--font-body` `--radius` `--space-4` (16 px) `--motion-fast` (0.18 s).
   - Nome sempre por **função**, nunca por cor (`--accent`, não `--laranja`).

### 2. Exportações (sob pedido: "exporta o design system", LP, ou extração de site)
Salvar em `_DESIGN\export\` (não lidos pelo Gate de KV):
1. **`tokens.css`** — `:root{}` com A1+A2, escada de superfícies e escala tipográfica (`--fs-display` … `--fs-caption`, razão 1.2–1.25).
2. **`DESIGN.md` completo (padrão de 9 seções + YAML frontmatter):**
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
**9 Seções H2 obrigatórias no corpo do `DESIGN.md`:**
1. `Overview` (Visual Theme, Mood, Surface Ladder philosophy, Page Rhythm & Key Characteristics)
2. `Colors` (Brand & Accent, Surface Ladder, Text Hierarchy, Semantic)
3. `Typography` (Font Families, Hierarchy Table, Tracking Principles & Open-Source Font Substitutes)
4. `Layout` (Spacing System base 4px/8px, Grid & Container widths, Whitespace Philosophy)
5. `Elevation & Depth` (Level 0..4 table, hairline vs shadow, Decorative Depth)
6. `Shapes` (Border Radius Scale by component, Photography & Illustration Geometry)
7. `Components` (`button-primary` com hover/pressed/focus, `button-secondary`, `feature-card`, `pricing-card`, `text-input`, `top-nav`, `footer` referenciando `{colors.*}`)
8. `Do's and Don'ts` (derivados de `## 2. O QUE FAZER` e `## 1. NÃO FAZER` do cliente)
9. `Responsive Behavior & Iteration Guide` (Breakpoints `1440 / 1280 / 1024 / 768 / 480 px`, Touch Targets `≥ 44px`, Collapsing Strategy).
3. **Prévia HTML única:** catálogo visual com swatches `#HEX` e contraste WCAG (`img_qa.py contraste`), escala tipográfica, botões em todos os estados (`Primary`, `Hover`, `Secondary`, `Ghost`, `Disabled`), cards na escada de superfícies e toggle Light/Dark.
