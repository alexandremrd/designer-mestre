# Módulo Ads — Direção de Arte Publicitária, Ideação Estrutural, Criativos Estáticos e Carrossel (SVG-First)

Entrega: prévia renderizada do SVG na conversa → após "aprovado", perguntar ao usuário qual formato final deseja (**montar no Figma**, **exportar PNG** ou **exportar SVG** — só executar o formato solicitado; nada é montado no Figma nem exportado em PNG/SVG final sem pedido). Quando solicitado, SVGs ficam em `Trabalho\` e PNGs em `Exportados\` da solicitação `[CA]` ou `[PA]`.

## 1. Direção de Arte Publicitária & Ideação Estrutural (`Insight → Tensão → Proposição Visual`)
- **Proposição Visual em 1 Frase (obrigatória antes de compor):** toda peça nasce de uma frase concreta contendo `[Sujeito] + [Ação/Relação física] + [Ambiente/Campo] + [Prova Visual do Argumento]` (ex.: *"O frasco repousa sobre basalto preto molhado enquanto um arco d'água emoldura a silhueta, provando hidratação sem esconder o rótulo"* — nunca adjetivos vazios como *"visual moderno, cinematográfico e premium"*).
- **Mood como comportamento observável:** traduzir palavras abstratas em decisões físicas verificáveis (*"baixo ruído visual, saturação contida, bordas nítidas no produto, amplo espaço negativo no terço superior, 1 bloco tipográfico forte, zero lens flare ornamental"*).
- **Territórios Criativos Canônicos (escolher pelo objetivo comercial):** `product-as-hero` · `momento humano` · `contraste visual` · `exagero de escala` · `transformação antes/depois` · `contexto inesperado` · `metáfora conceitual` · `realismo documental` · `contenção editorial` · `macro tátil` · `minimalismo gráfico` · `cena cinematográfica` · `fotografia impossível (com física local rigorosa)` · `composição de objetos` · `storytelling ambiental`.
- **Ideação Anti-Clichê (quando o pedido exigir conceito novo ou campanha):**
  1. Identificar a **Tensão** (Cultural: o que o mercado diz vs. faz; de Categoria: o que promete vs. entrega; ou Humana: o que o público quer vs. o obstáculo).
  2. Aplicar métodos estruturais (SIT: Subtração, Multiplicação, Divisão, Unificação de Tarefa; Bisociação de 2 universos distantes; ou Inversão) e **descartar internamente as 3 primeiras ideias óbvias ("aquecimento convencional")**, entregando a partir da ideia 4+.
  3. Quando o usuário pedir variações/opções de direção, variar **ao menos 3 dimensões estruturais** (território, ângulo/relação de câmera, comportamento do sujeito, ambiente ou massa compositiva). Trocar apenas cor ou efeito não é nova direção.

## 2. Arquitetura de Ponto Focal, Base SVG e Preflight Perceptivo
- **Arquétipo existente:** se houver arquétipo aprovado em `_DESIGN\templates\` (`E1.svg`, `E2.svg`...), clonar o SVG e injetar copy e imagem mantendo coordenadas fixas do `design_system.md`.
- **Hierarquia de Ponto Focal Único:** exatamente **1 Ponto Focal Primário** (o herói que captura o olhar em < 1 s), 1 Âncora Secundária (contexto/apoio) e Elementos Terciários (headline, badge, logo). Proibido *"equal-emphasis"* (3+ elementos disputando o mesmo peso visual).
- **3 Testes de Preflight Perceptivo (antes de renderizar a prévia):**
  1. **Teste da Miniatura (100×100 px):** reduzida a miniatura, a silhueta do herói e a hierarquia continuam imediatamente legíveis?
  2. **Teste em Escala de Cinza:** sem cor, o contraste de luminância/valor separa claramente primeiro plano, fundo e tipografia?
  3. **Zero Tangências Acidentais:** elementos próximos devem ter **sobreposição decidida (≥ 15%)** ou **separação limpa** — proibido bordas apenas "encostando" ou quase tangenciando.

## 3. Formatos, Safe Zones e Leis Invioláveis de Composição
- **Feed 4:5:** `viewBox="0 0 1080 1350"`.
- **Story/Reels 9:16:** `viewBox="0 0 1080 1920"`. Texto, logo e botões fora de 250 px do topo, 340 px da base (450 px em Reels) e 80–90 px das laterais (margem segura mínima de 6–8%). Feed e Story da mesma variação = mesma cena adaptada.
- **Carrossel:** mesmo `viewBox` em todos os cards, seguindo a progressão de arquétipos do cliente (capa E1 → internos E2 → endcard E3) e leitura contínua entre os títulos.
- **Regras Anti-Corte e Endcard Forte (Invioláveis):**
  1. **Zero corte ou esmagamento de fotos:** nunca esticar, achatar ou recortar produtos/aeronaves/pessoas em tiras estreitas (`pill`, janelinha espremida ou círculo que decepa o objeto). Usar enquadramento editorial com respiro, fusão contínua em gradiente sobre o fundo do KV ou painel translúcido estruturado.
  2. **Proibido slide puramente "mudo" ou desconectado:** mesmo quando um slide não leva foto (ex.: restrição de imagem médica), estruturar com **UI/HUD técnico, diagrama vetorial da marca, numeração editorial de etapas ou grid arquitetônico** para manter peso visual equivalente aos demais cards.
  3. **Proibido último slide (Endcard/CTA) vazio só com logo + botão em fundo liso:** o card final de carrossel DEVE ter **cena heroica de fechamento** (ex.: foto noturna/editorial iluminada com fusão em degradê, silhueta/blueprint de fundo ou painel glassmorphism), **barra/chips de credenciais reais do KV** (ex.: anos de operação, bases, abrangência) + Logo em destaque + Botão CTA com alto contraste.

## 4. Camadas padrão, 7 Padrões de Layout e Dimensionamento da Logo
1. `<g id="BG_Foto_Fundo">`: fundo + foto com `<clipPath>` e gradiente de fusão/scrim na zona de leitura.
2. `<g id="Grafismos_Moldura">`: elementos de marca do KV.
3. `<g id="Bloco_Tipografico">`: headline (entrelinha 1.05–1.15, quebra de linha semântica e nunca palavra órfã isolada); apoio em até 2–3 linhas a 40–50% do tamanho da headline.
4. `<g id="CTA_e_Logo">`: botão (`<rect rx>` + `<text>`) isolado de ruído e `<g id="Logo_Oficial">` com os paths originais em escala uniforme.
- **7 Padrões Canônicos de Layout e Engajamento de Canvas (70–90% de utilização espacial):**
  1. **Left/Right Content:** textos alinhados a 20–30% (ou espelhados a 60–70%) da borda, deixando o lado oposto limpo para o herói fotográfico;
  2. **Z-Pattern / F-Pattern:** headline no topo esquerdo → ponto visual no topo direito → subhead na diagonal inferior → CTA no canto inferior direito (Z) ou escaneamento vertical à esquerda (F);
  3. **Centered / Pyramid:** eixo central simétrico (headline no terço superior, herói no centro, CTA na base);
  4. **Golden-Ratio / Rule-of-Thirds:** ponto focal e texto ancorados nas interseções de 1,618:1 ou terços;
  5. **Diagonal / Asymmetrical:** fluxo dinâmico em diagonal ou peso visual concentrado num lado equilibrado por espaço negativo generoso;
  6. **Top-Down Hierárquico:** progressão vertical com redução controlada de escala;
  7. **Grid Modular:** colunas e linhas explícitas com espaçamento proporcional (gaps de 8–10% em formatos pequenos, 10–15% em médios, 15–20% em grandes).
- **Dimensionamento e Proteção da Logo:** largura de `15–20%` da peça para logos horizontais (ou altura de `10–15%` para verticais), **nunca excedendo 25%** da menor dimensão da peça, com margem de proteção mínima de `16px` (ampliada sobre fundos fotográficos) e contraste verificado contra a luminosidade do fundo (fundo escuro pede logo clara/negativa; fundo claro pede logo escura/positiva).

## 5. Render da prévia, Imagem e Nomenclatura
- **Render:** via headless browser com wrapper mínimo (`<style>@import url('[Google Fonts]'); body{margin:0;width:1080px;height:1350px;overflow:hidden}</style>` + `<svg>` inline). Prancha local: `python assets\img_qa.py prancha Exportados\*.png -o Trabalho\_prancha.jpg` e olhar só ela. Aplicar P0 + crítica da lei 8 do núcleo.
- **Imagem:** acervo do cliente primeiro; faltou → `imagem.md`. Texto, rótulo e logo nunca na imagem gerada (entram no SVG).
- **Nomenclatura:** a do briefing; sem ela: `[CLIENTE]_[CAMPANHA]_[AAAAMM]_E[n]_[FEED|STORY].png`. Revisões `_V2`, `_V3`.
