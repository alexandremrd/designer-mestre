# Módulo Figma — Layout Nativo Editável, Paridade Visual e Exportação de Tokens

Só é lido e executado depois do "aprovado" na prévia **e** quando o usuário escolher montar no Figma (ou quando pedir edição direta de um arquivo Figma existente). Se o usuário aprovar a prévia mas pedir apenas PNG ou SVG (ou não pedir Figma), não abrir nem montar no Figma. Objetivo quando acionado: reconstruir a hierarquia visual em camadas Figma nativas, mantendo a paridade com a referência aprovada; ativos vetoriais complexos podem permanecer como vetores importados quando isso preservar melhor o desenho.

---

## Princípio de formato: SVG não é documento nativo do Figma
Um SVG pode preservar aparência vetorial e, dependendo do conteúdo, partes do texto e dos grupos; ele **não codifica Auto Layout, componentes, constraints, variables, estilos nem a semântica de espaçamento do Figma**. `<g id>` e nomes no XML não garantem uma árvore de camadas editável conforme o padrão do arquivo. Não prometa que colar/arrastar o SVG cria frames, texto nativo ou Auto Layout corretamente.

Quando o usuário quer apenas um arquivo vetorial para uso, entregue o SVG. Quando quer trabalhar/editar no Figma, trate o SVG aprovado como referência visual e fonte de ativos; reconstrua o layout em nós Figma nativos. Use vetores/SVG importados apenas onde a fidelidade de curvas, ilustrações, máscaras ou efeitos complexos justificar. Mantenha texto, logo, CTA e blocos de layout em camadas nativas sempre que possível. Assim, a paridade visual não depende de achatar a peça inteira, e a estrutura permanece compreensível.

## Escolha do método: peça de marca ou tela de produto
- **Anúncio, post, KV ou composição de marca:** priorizar a direção aprovada e a liberdade de composição. Organizar texto, logo, CTA, foto e grafismos em camadas nativas nomeadas; usar posicionamento absoluto onde a composição art-directed exigir. Aplicar Auto Layout apenas a grupos que realmente fluem (por exemplo, texto e botão ou itens repetidos). Não procurar nem criar componentes, variáveis ou uma biblioteca completa para uma peça isolada; reutilizar recursos existentes quando forem pertinentes.
- **Tela de app/site construída a partir de código ou descrição:** a rota especialista de UI/Figma conduz esse trabalho. Usar em conjunto `figma-use` e `figma-generate-design` quando o arquivo tiver uma biblioteca de design system relevante; a segunda skill é para telas compostas com componentes/variáveis/estilos publicados, não um conversor genérico de SVG. Para crítica de interface ou design-to-code, manter a rota especialista prevista no núcleo.
- **Não duplicar sistema de design:** inspecionar telas e instâncias existentes antes de buscar/criar recursos. Se a busca local de variáveis vier vazia, isso não prova que bibliotecas publicadas não tenham variáveis; usar a busca de design system disponível antes de concluir que não há tokens. Buscar componentes, variáveis ou estilos só quando o entregável e o arquivo justificarem.

## 1. Rota A — Conector Oficial / Execução Direta (Preferida)
- Conector desligado: pedir para ativar.
- **Antes de criar:** inspecionar a página/arquivo alvo e identificar convenções de nomes, componentes, variáveis, estilos, fontes e grids existentes. Reutilize-os quando pertinentes; não invente uma biblioteca paralela.
- **Frame e layout nativos:** criar primeiro o frame raiz nomeado conforme a peça/campanha; estruturar os blocos semânticos em frames/text nodes, aplicando Auto Layout, padding, gap e `HUG`/`FILL` onde o conteúdo flui. Não force Auto Layout em composições art-directed sobrepostas: use posicionamento absoluto quando ele for intencional.
- **Vetores:** usar nós nativos para formas simples. Importar o SVG aprovado (por exemplo, `figma.createNodeFromSvg`, se disponível no conector) para ilustrações ou grafismos complexos, conferindo bounds e estrutura após importar; não usar o SVG inteiro como substituto do layout editável.
- **Texto nativo:** `await figma.loadFontAsync({ family, style })` sempre **antes** de definir caracteres ou propriedades tipográficas, usando a família e o peso exatos do `design_system.md` ou os estilos existentes no arquivo. Se indisponível, escolher fallback compatível e avisar; não converter silenciosamente texto em vetor.
- **Foto:** preenchimento `IMAGE` (`scaleMode: "FILL"` ou `"CROP"`); gradiente de fusão/scrim em camada separada acima.
- **Logo:** `createNodeFromSvg` do arquivo oficial, nomeada `Logo_[Cliente]_Oficial`, proporção travada.
- **Hierarquia e nomes:** seguir a convenção do arquivo/equipe. Se não existir, usar nomes semânticos estáveis (ex.: `Post / Feed`, `Background`, `Hero image`, `Headline`, `Body`, `CTA`, `Logo`). Agrupar por função; não criar dezenas de camadas para paths decorativos nem renomear tudo com índices genéricos.
- **Auto Layout e espaçamento:** identificar relações de conteúdo antes de definir layout: stacks de texto/botões/itens repetidos normalmente usam Auto Layout; hero, fotografia e elementos sobrepostos podem permanecer em posição absoluta. Usar valores consistentes com os tokens/frames existentes e preservar intenção visual; não deduzir gap de `<g>` nem transformar cada coordenada SVG em padding.
- **Construir e validar em etapas:** começar com inspeção somente leitura; criar a estrutura raiz; então montar blocos lógicos, validando hierarquia, limites e screenshot em marcos relevantes antes de avançar. Retornar/guardar IDs dos nós criados ou alterados quando a ferramenta oferecer IDs, para correções direcionadas. Conferir metadados (tipos, nomes, parent, layoutMode, padding, itemSpacing, sizing, fontes) e screenshot após a composição. Não enviar uma operação monolítica para criar tudo de uma vez nem recriar a peça inteira para corrigir um detalhe.
- **Texto e componentes:** carregar a fonte exata antes de editar texto nativo; confirmar a família e o estilo disponíveis e declarar fallback se necessário. Ao reutilizar uma instância de componente, preferir suas propriedades de texto/variante expostas em vez de alterar nós internos sem necessidade. Não converter texto em vetor para contornar fonte ausente sem avisar.
- **Recuperação:** em erro, parar e ler a mensagem antes de qualquer nova chamada. Confirmar página, IDs e estado atual com inspeção quando a causa não estiver clara; corrigir apenas o passo afetado e tentar novamente de forma delimitada. Nunca presumir que operações parciais foram revertidas ou aplicadas sem verificar.
- **Paridade visual:** exportar PNG do frame Figma no mesmo tamanho da referência e comparar visualmente; usar `python assets\img_qa.py paridade previa.png figma.png` quando disponível. RMSE é sinal de diferença de pixels, não prova de boa estrutura de camadas ou Auto Layout. Verificar estrutura e aspecto separadamente.

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

## 3. Rota C — SVG para uso vetorial (Sem Conector)
- Salvar o SVG limpo em `Trabalho\` para entrega/uso vetorial: texto com família/peso explícitos, imagens referenciadas ou incorporadas conforme o formato de entrega, recursos em `<defs>` e sem dependências externas/`foreignObject` quando isso prejudicar o uso.
- `<g>` e `id` semânticos ajudam a inspecionar e organizar o SVG, mas não garantem conversão em camadas nativas ou Auto Layout no Figma. Se o usuário precisar de estrutura editável do Figma sem conector, entregar o SVG como referência vetorial e explicar que a reconstrução manual é necessária; não declarar o requisito de Auto Layout atendido pelo SVG.
- **Exportação de Design System Completo via Console do Figma Desktop (quando solicitado sem conector):**
  - Gerar script JS autônomo (para `Plugins > Development > Open Console`) que cria automaticamente:
    1. **Color Styles** organizados com `/` (`Primary/50`..`900`, `Neutral/50`..`900`, `Semantic/Success|Warning|Error|Info`, `Surface/Canvas|Surface-1..3`, `Border/Hairline`) via `figma.createPaintStyle()`;
    2. **Text Styles** (`Heading/Display`, `Heading/H1..H4`, `Body/Large|Regular|Small`, `Label/Eyebrow`) carregando as fontes com `await figma.loadFontAsync()` antes de `figma.createTextStyle()`;
    3. **Effect Styles** (`Shadow/SM|MD|LG|XL`) via `figma.createEffectStyle()`;
    4. **Variable Collection (`Design Tokens`)** com modos `Light` e `Dark` nativos via `figma.variables.createVariableCollection("Design Tokens")`, populando todas as cores semânticas e `radius` (`FLOAT`) com `variable.setValueForMode(modeId, val)`.

## 4. Memória de Template Aprovado
Estrutura nova aprovada: salvar o esqueleto SVG (sem Base64 pesado) em `_DESIGN\templates\[arquetipo].svg` e registrar em `## 2. O QUE FAZER` do `design_system.md`.

## Referências de método
- [Figma Use Skill](https://github.com/coderabbitai/codex-plugin/tree/35779b453cca18aa7cd3176f0bb73a8c75d11da8/plugins/figma/skills/figma-use): referência para inspeção da árvore, operações pequenas, IDs retornados, carregamento de fontes e validação/recuperação. Usar como guia da API quando a ferramenta e o fluxo forem compatíveis; detalhes específicos de uma implementação de `use_figma` não são regras universais.
- [Figma Design Generator](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/figma-generate-design): referência condicional para telas de app/web que reutilizam componentes, variáveis e estilos publicados. A captura de tela por `generate_figma_design` é uma referência de paridade para web apps; não é um passo necessário para anúncios, SVGs ou trabalhos sem app renderizado.
- Métodos extraídos para este módulo, sem copiar integralmente as skills nem seus exemplos de código. Nenhuma delas é específica para reparar SVG importado; não prometem conversão automática de SVG para camadas semânticas ou Auto Layout.
