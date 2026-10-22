# Módulo KV, Brand Book, Logo e Design System (84 Design Systems de referência)

Módulo unificado para extração/validação de Identidade Visual (Cold Start), criação de Brand Book e Logo nova, consulta aos 84 sistemas de design reais embarcados (`engines\uiux`) e estruturação/exportação de tokens de Design System (`tokens.css` e `DESIGN.md`). Extração só do acessível (núcleo §6).

---

## Parte A · Cold Start — Cliente novo ou KV incompleto

Estudo completo quando não há `_DESIGN\design_system.md` ou quando `CLIENTE_NOVO: SIM`. Depois de consolidar as fontes e pendências, marcar `CLIENTE_NOVO: NÃO`, mesmo que `STATUS_KV` permaneça `PARCIAL`. Cliente existente com KV parcial recebe só a análise das pendências relevantes ao pedido; revisão completa apenas quando solicitada.

### 1. Estrutura de pastas
Cliente existente: não mover nem apagar nada sem necessidade; criar só o que o pedido precisa. Cliente novo: criar a árvore **inclusive as quatro pastas de imagem vazias** e copiar `<AG>\Clientes\_TEMPLATE_CLIENTE\design_system.md` para `_DESIGN\`. Ativos recebidos fora da árvore são classificados em suas categorias; preservar caminhos já fornecidos pelo usuário quando mover afetaria usos existentes.

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
    Imagens\  Originais\ (só leitura) · Banco de Imagens\ · Tratadas\ · IA\
    Vídeos\   Originais\ · Banco\
  [AAAA]\[MM - Mês]\[AAAA-MM-DD] [TIPO] Título\
    briefing.md · Referências\ · Trabalho\ · Exportados\
```
Tipos: `CA` criativo Ads · `PA` pauta/orgânico · `EV` vídeo editado · `MT` motion · `LP` landing page/HTML · `KV` identidade · `DK` deck · `IM` imagem · `OT` outros.
Cliente antigo com `KV.md`, `NAO_FAZER.md`, `aprovados.md`, `inteligencia.md` separados: unificar no `design_system.md` (sem apagar os antigos).

### 2. Análise profunda (MIV Scanner & Extração Web — uma vez)
1. `Compartilhada\Identidade Visual\`: MIV, guia de marca e logos. Renderizar cada logo uma única vez e anotar arquivo, layout, cor e proporção do bbox.
2. Links de Figma do briefing (`get_design_context` / `get_screenshot`).
3. Peças anteriores: inventariar as séries relevantes e estudar **todas as referências que o usuário indicar**. Para cliente novo ou sem `design_system.md`, a leitura inicial deve revelar padrões e exceções, não se limitar a 2–3 peças. Usar prancha de todos os criativos pertinentes; nos SVGs, inspecionar `viewBox`, cores, fontes, hierarquia, máscaras, fotos embutidas e elementos recorrentes sem despejar base64 no contexto. Registrar o **papel** de cada elemento recorrente (logo, motivo de marca, máscara, imagem ou ornamento), não só sua forma e cor; ver `ads.md` §2. Abrir peças individuais só para detalhes que a prancha não mostra. Depois de consolidar no KV, sessões futuras usam o Fast-Track.
4. Site ou Instagram informados no briefing (extrair variáveis CSS `--*`, paleta computada, escada de superfícies, famílias de fonte, raios de borda e estilos de botão diretamente via DOM/headless browser; bloqueado = núcleo §6).
5. Se o cliente não tiver KV ou pedir inspiração em grandes marcas globais, consultar o motor interno de **84 Design Systems reais**:
   - Busca por segmento/estética: `python "<AG>\engines\uiux\scripts\search.py" "<segmento ou estética>" --domain brand -n 3`
   - Leitura completa do `DESIGN.md` de uma marca de referência (ex.: `linear.app`, `stripe`, `apple`, `ferrari`, `bugatti`, `lamborghini`, `nike`, `airbnb`, `runwayml`, `vercel`, `raycast`, `oura`): `python "<AG>\engines\uiux\scripts\search.py" "<slug>" --brand`
6. Extrair e consolidar no `_DESIGN\design_system.md`:
   - conceito, sensação e símbolo;
   - versões da logo (nome · layout · cor · bbox);
   - paleta por papel (HEX, RGB, CMYK, **Escada de Superfícies de 4 níveis** `canvas` → `surface-1`..`surface-4` + `hairline`, cores semânticas, contraste WCAG, regra de escassez do acento e cores proibidas);
   - tipografia por nível (oficial com peso, caixa, **polaridade de tracking** — negativo em display, neutro em body, positivo em eyebrow/label — + substituta Google Fonts para Figma/SVG);
   - grafismos, arquétipos SVG, composição/respiro/posição da logo/rodapé, fotografia (tema · pessoas · enquadramento · luz · tratamento · relação com a copy), safe zones, tom de voz e pilares, O Que Fazer (Aprovados) e O Que Não Fazer (Vetos);
   - ofertas/produtos mencionados nas fontes, em 1–3 linhas por item com a origem e o grau de confirmação; separar descrição comercial observada de atributo técnico confirmado. Isso orienta a próxima cena sem inventar benefícios.
7. Contradições ou itens ausentes essenciais (logo, paleta ou fonte) vão para `## 5. Decisões Pendentes` mantendo `PARCIAL`; quando completo, marcar `STATUS_KV: VALIDADO`.
8. Cliente já `VALIDADO` num template antigo: campos novos vazios **não** rebaixam o status nem disparam nova análise.
- E-mails do cliente como fonte: registrar por bloco (cabeçalho, corpo, rodapé) fundo, lista/ícone e botão; vira KV só com confirmação.

---

## Parte B · Brand Book (Manual de Identidade Visual 16:9) e Logo nova

### 1. Brand Book (Diagramação HTML/CSS 16:9 e Exportação)
Salvar em `Compartilhada\Identidade Visual\` e, se solicitado após aprovação, na página "Brand" no Figma (com estilos e variáveis), sem alterar arquivos oficiais existentes.
- **Revisão Obrigatória de Ativos antes de gerar:** auditar o que existe (`✓`), o que está incompleto (`⚠`) e quais seções opcionais serão omitidas (`✗`, ex.: omitir `2.4 Construção/Grade` se não houver malha `construcao.svg`; nunca inventar código Pantone se não foi fornecido), apresentando a estimativa de páginas antes da composição final. Cliente multi-marca recebe 1 brandbook por marca + `index.html` de capa-índice unificada.
- **Sumário-Mestre Hierárquico e Catálogo de 14 Tipos de Página (`aspect-ratio: 16/9`, `max-width: 1600px`, margens `96px × 80px`, grid 12 colunas com layouts `5/7`, `4/8` e `6/6`, tipografia escalável em `cqi`):**
  - `00 Capa` + `00 Sumário` + **Divisores de Seção** de página cheia antes de cada macro-seção (`01` a `07`) com número gigante (`62cqi`) e paginação `001` no rodapé;
  - `01 A Marca`: `1.1` Sobre · `1.2` Propósito/Missão/Visão · `1.3` Valores · `1.4` Personalidade e Tom de Voz · `1.5` Manifesto;
  - `02 Logotipo`: `2.1` Conceito · `2.2` Versão Principal · `2.3` Variações (`2×2` ou `3×2`) · `2.4` Construção/Grade · `2.5` Área de Proteção (`X`) · `2.6` Redução Mínima (`mm` impresso e `px` digital) · `2.7` Monocromáticas (positivo/negativo/P&B) · `2.8` Usos sobre Fundos · `2.9` Co-branding · `2.10` **Usos Incorretos** (grid `3×2` ou `4×2` gerado automaticamente aplicando transformações CSS na logo oficial — `scaleX(1.4)`, `scaleY(0.6)`, `rotate(15deg)`, `hue-rotate(180deg)`, `-webkit-text-stroke`, `drop-shadow`, `opacity: 0.3`, fundo sem contraste — com faixa diagonal vermelha de proibição e legenda técnica);
  - `03 Cores`: `3.1` Principal (modo Hero para 1 cor ou Grid proporcional) · `3.2` Secundária · `3.3` Neutras (escala `50–900` mantendo matiz constante e saturando o meio) · `3.4` Gradientes · `3.5` Proporções de Uso (90% neutro / 10% marca no template editorial, ou 60% cor da marca no template expressivo);
  - `04 Tipografia`: `4.1` Principal (`Aa` gigante com contraste primária/acento + pesos) · `4.2` Secundária · `4.3` Hierarquia tabular (`Display 13cqi`, `H1 3cqi`, `H2 1.8cqi`, `H3 1.3cqi`, `Corpo 1cqi`, `Legenda 0.72cqi`) · `4.4` Boas Práticas;
  - `05 Elementos Gráficos`: `5.1` Grafismos/Patterns · `5.2` Iconografia · `5.3` Direção de Fotografia · `5.4` Texturas;
  - `06 Aplicações` (grid irregular com 1 mockup dominante por página) e `07 Encerramento`.
- **Chrome:** header 12 px caixa-alta +0.12em (marca à esq.; `NN SEÇÃO / N.N` à dir.); rodapé 11 px `Brandbook [Marca] · v1.0` + página em 3 dígitos; capas e divisores sem header. Flat (sem gradiente/sombra) salvo se a marca usar.
- **Paginação:** 2.3 com 8+ variações, 3.1 com 5+ cores ou 06 com 9+ aplicações = dividir em páginas, 1 mockup dominante por página. Aplicações só as pedidas/existentes (cartão 85×55 mm, A4, envelope DL/C5, assinatura de e-mail ≤ 600 px).

### 2. Logo nova (somente sob pedido explícito)
- Se o cliente já tem logo, confirmar que é redesign ou marca nova. Logo de cliente nunca é criada sem pedido explícito (faltou logo num pedido comum = pedir).
- Etapas:
  1. Briefing: nome, setor, valores, público, concorrentes e restrições.
  2. Pesquisa de concorrência para diferenciar (avaliando Distintividade 30%, Relevância 25%, Versatilidade 20%, Atemporalidade 15%, Executabilidade 10%). Nunca imitar marca existente.
  3. Três rotas (símbolo, lettering, combinação) em vetor, com versões horizontal e vertical, cor/positivo/negativo, área de proteção e tamanho mínimo.
  4. Após aprovação, exportar no formato escolhido e salvar SVG/PNG em `Compartilhada\Identidade Visual\`, registrando na tabela de logos do `_DESIGN\design_system.md`. A partir daí vale a lei da logo existente.
- **Testes antes de apresentar:** legível em 16×16, funciona em 1 cor e P&B, nada some em 32 px. Tipo pela função: wordmark (nome curto) · lettermark (nome longo) · símbolo (só com recall) · emblema (evitar).
- **Entrega:** SVG (preferido) + PNG transparente 2× + PDF vetorial; versões positiva, negativa e monocromática.

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
   - **Eyebrow / Badges / Micro-labels (`10–13 px`):** tracking **positivo** (`+0.04em` a `+0.12em` / `+0.4px` a `+1.4px`), criando contraste taxonômico imediato contra os títulos de tracking negativo.
4. **Tokens obrigatórios (camadas CSS):**
   - **A1 · obrigatórios da marca:** `--bg` `--fg` `--accent` `--font-display`.
   - **A2 · obrigatórios com padrão:** `--fg-2` `--surface` `--surface-2` `--border` `--success` `--error` `--font-body` `--radius` `--space-4` (16 px) `--motion-fast` (0.18 s).
   - Nome sempre por **função**, nunca por cor (`--accent`, não `--laranja`).
- **3 camadas de token:** primitivos (rampas, escala 4 px, tipo 1.2–1.25) → semânticos por função (`--accent`, `--surface-1`, `--fg-2`, `--success/--warning/--error/--info` + par `*-foreground` ≥ 4.5:1) → componente (`--btn-bg: var(--accent)`). Peças usam só semânticos; tema troca só a camada semântica. Export DTCG (`$value/$type`) opcional para variáveis do Figma.
- Componente: tamanhos sm/md/lg · estilos default/outline/ghost/destructive · estados default/hover/focus/disabled/loading.

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
