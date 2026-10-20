# Módulo Ads — Criativos estáticos e carrossel (SVG-First)

Entrega: prévia PNG renderizada do SVG → após "aprovado", Feed + Story editáveis no Figma (`figma.md`), SVGs em `Trabalho\` e PNGs em `Exportados\` da solicitação `[CA]` ou `[PA]`.

## 1. Base
- Se existir arquétipo aprovado em `_DESIGN\templates\` (`E1.svg`, `E2.svg`...), clonar o SVG e só injetar copy e imagem.
- Molduras, divisores, gradientes (`<defs>`), posição da logo (`<g transform>`) e âncoras de texto (`<text x y>` + `<tspan>`) têm coordenadas fixas vindas do `design_system.md`.

## 2. Formatos e safe zones (salvo regra do cliente)
- Feed 4:5: `viewBox="0 0 1080 1350"`.
- Story/Reels 9:16: `viewBox="0 0 1080 1920"`. Texto, logo e botões fora de 250 px do topo, 340 px da base (450 px em Reels) e 80–90 px das laterais.
- Feed e Story da mesma variação = mesma cena adaptada.
- Carrossel: mesmo `viewBox` em todos os cards, seguindo a progressão de arquétipos do cliente (ex.: capa E1 → internos E2 → endcard E3).

## 3. Camadas padrão (cliente sem arquétipo próprio)
1. `<g id="BG_Foto_Fundo">`: fundo + foto com `<clipPath>` e gradiente de fusão na área de leitura.
2. `<g id="Grafismos_Moldura">`: elementos de marca do KV.
3. `<g id="Bloco_Tipografico">`: headline; apoio em até 2–3 linhas a 40–50% do tamanho da headline.
4. `<g id="CTA_e_Logo">`: botão (`<rect rx>` + `<text>`) e `<g id="Logo_Oficial">` com os paths originais em escala uniforme.

## 4. Render da prévia
Renderizar em tamanho real via headless browser com um wrapper mínimo: `<style>@import url('[Google Fonts]'); body{margin:0;width:1080px;height:1350px;overflow:hidden}</style>` + o `<svg>` inline. Prancha local: `python assets\img_qa.py prancha Exportados\*.png -o Trabalho\_prancha.jpg` e olhar só ela. Antes de mostrar: P0 + crítica da lei 8 do núcleo (sem abrir `qualidade.md`).

## 5. Imagem
Foto do cliente primeiro. Faltou: `imagem.md` (gerador local). Texto, rótulo e logo nunca na imagem gerada: entram no SVG.

## 6. Nomenclatura
A do briefing. Sem ela: `[CLIENTE]_[CAMPANHA]_[AAAAMM]_E[n]_[FEED|STORY].png`. Revisões `_V2`, `_V3`.
