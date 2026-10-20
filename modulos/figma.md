# Módulo Figma — Entrega Editável 1:1, Execução em Lote, Socket Bidirecional e Exportação de Tokens

Só é lido e executado depois do "aprovado" na prévia **e** quando o usuário escolher montar no Figma (ou quando pedir edição direta de um arquivo Figma existente). Se o usuário aprovar a prévia mas pedir apenas PNG ou SVG (ou não pedir Figma), não abrir nem montar no Figma. Objetivo quando acionado: cada elemento como camada nativa editável, com a geometria exata do SVG aprovado.

---

## 1. Rota A — Conector Oficial / Execução Direta (Preferida)
- Conector desligado: pedir para ativar.
- **Vetores** (molduras, divisores, ícones): `figma.createNodeFromSvg` nas coordenadas exatas do SVG aprovado.
- **Texto nativo:** `await figma.loadFontAsync({ family, style })` sempre **antes** de definir caracteres ou propriedades tipográficas, usando a família e o peso exatos do `design_system.md` (nunca cair em fonte padrão do sistema).
- **Foto:** preenchimento `IMAGE` (`scaleMode: "FILL"` ou `"CROP"`); gradiente de fusão/scrim em camada separada acima.
- **Logo:** `createNodeFromSvg` do arquivo oficial, nomeada `Logo_[Cliente]_Oficial`, proporção travada.
- **Hierarquia e Nomes das Camadas:** `BG_…`, `Foto_…`, `Overlay_…`, `Moldura_…`, `Headline`, `Sub`, `Divisor`, `CTA_…`, `Logo_Oficial`. Posicionar Feed e Story lado a lado dentro de uma `Section` com o nome da solicitação.
- **Paridade Visual Obrigatória:** exportar PNG do frame no mesmo tamanho e rodar `python assets\img_qa.py paridade previa.png figma.png`. RMSE ≤ 0.03 aprova; acima disso, abrir `_diff.png`, corrigir a divergência e repetir uma vez. Registrar link no `historico.md`.

---

## 2. Rota B — Motores Locais para Figma Desktop (`figma_engine\`)
Quando operar via plugins locais no Figma Desktop, escolher um dos dois modos contidos em `figma_engine\`:

1. **Modo de Execução de Código em Lote (`figma_execute` — 90%+ de economia de tokens):**
   - Em vez de dezenas de chamadas individuais, enviar um único bloco JavaScript para criar hierarquias completas, aplicar Auto-Layout, vincular tokens e auditar acessibilidade:
   - `await figma.status()` → verifica conexão.
   - `await figma.create({ type: 'frame' | 'card' | 'text' | 'button' | 'nav', name, width, height, x, y, layout: { direction: 'col'|'row', gap, padding }, fill, cornerRadius, children: [...] })` → cria árvore completa em 1 chamada.
   - `await figma.query({ target: 'selection' | 'name:Elemento' })` e `await figma.modify({ target, fill, textColor, maxWidth, layoutSizingHorizontal: 'FILL' })` → consulta e edita em lote.
   - `await figma.toComponent({ target, name })` e `await figma.createVariants({ target, property, values })` → componentização e variantes.
   - `await figma.createToken({ collection, name, type, value })`, `await figma.bindToken({ target, property, token })` e `await figma.syncTokens({ from | to })` → variáveis e tokens.
   - `await figma.accessibility({ target: 'selection' | 'page', level: 'AA', autoFix: true })` → auditoria e correção automática de contraste WCAG e alvos de toque (≥ 44×44 px).
   - `await figma.export({ target, format: 'png' | 'svg' | 'pdf', scale: 2 })` → exportação final.
   - Regras detalhadas da API em `figma_engine\rules\*.md` (ler apenas a regra necessária se houver dúvida de sintaxe).

2. **Modo de Socket Bidirecional (42 Ferramentas Granulares em Tempo Real):**
   - Inspeção (`get_document_info`, `get_selection`, `read_my_design`, `get_node_info`, `get_nodes_info`, `get_styles`, `get_local_components`), Criação (`create_frame`, `create_text`, `create_rectangle`, `create_section`, `create_component_instance`, `clone_node`), Auto-Layout (`set_layout_mode`, `set_padding`, `set_axis_align`, `set_layout_sizing`, `set_item_spacing`, `move_node`, `resize_node`, `set_corner_radius`), Estilo (`set_fill_color`, `set_stroke_color`, `set_image_fill`), Texto em Massa (`scan_text_nodes`, `set_text_content`, `set_multiple_text_contents`), Propagação de Instâncias (`get_instance_overrides`, `set_instance_overrides`), Anotações/Prototipagem (`set_annotation`, `create_connections`) e Exportação (`export_node_as_image`).

3. **Conversão DOM/HTML → Camadas Vetoriais e Auto-Layout:**
   - Para levar uma LP ou componente HTML aprovado ao Figma: mapear estilos computados (`getComputedStyle`) e box model convertendo containers (`section`, `div`, `header`) em Frames com Auto-Layout, textos em nós `TEXT` com fontes carregadas, imagens em `IMAGE` fill e SVGs inline em vetores nativos.

---

## 3. Rota C — SVG Limpo para Arrastar + Script de Design System (Sem Conector)
- **Peça visual (SVG 1 Clique):** salvar um `.svg` limpo por peça em `Trabalho\` com um `<g id>` por elemento, `<text>` com nome exato da família e `font-weight`/`font-style` explícitos, fotos em `<image>`, gradientes em `<defs>`, zero CSS externo ou `foreignObject`, e logo oficial em `<g id="Logo_Oficial">`. Ao colar ou arrastar no Figma, converte-se automaticamente em frames, textos e vetores editáveis.
- **Exportação de Design System Completo via Console do Figma Desktop (quando solicitado sem conector):**
  - Gerar script JS autônomo (para `Plugins > Development > Open Console`) que cria automaticamente:
    1. **Color Styles** organizados com `/` (`Primary/50`..`900`, `Neutral/50`..`900`, `Semantic/Success|Warning|Error|Info`, `Surface/Canvas|Surface-1..3`, `Border/Hairline`) via `figma.createPaintStyle()`;
    2. **Text Styles** (`Heading/Display`, `Heading/H1..H4`, `Body/Large|Regular|Small`, `Label/Eyebrow`) carregando as fontes com `await figma.loadFontAsync()` antes de `figma.createTextStyle()`;
    3. **Effect Styles** (`Shadow/SM|MD|LG|XL`) via `figma.createEffectStyle()`;
    4. **Variable Collection (`Design Tokens`)** com modos `Light` e `Dark` nativos via `figma.variables.createVariableCollection("Design Tokens")`, populando todas as cores semânticas e `radius` (`FLOAT`) com `variable.setValueForMode(modeId, val)`.

## 4. Memória de Template Aprovado
Estrutura nova aprovada: salvar o esqueleto SVG (sem Base64 pesado) em `_DESIGN\templates\[arquetipo].svg` e registrar em `## 2. O QUE FAZER` do `design_system.md`.
