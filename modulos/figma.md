# Módulo Figma — Entrega editável (paridade 1:1 com o SVG)

Só é lido depois do "aprovado" na prévia (salvo o usuário mandar ir direto ao Figma ou pedir edição de um arquivo existente). Objetivo: cada elemento como camada nativa editável, com a geometria exata do SVG aprovado.

## Rota A — Conector oficial (preferida)
- Conector desligado: pedir para ativar. Carregar `figma-use` antes de `use_figma`.
- Vetores (molduras, divisores) via `figma.createNodeFromSvg` com as coordenadas do SVG.
- Texto nativo: `figma.loadFontAsync` com a fonte e o peso do `design_system.md` (nunca cair em Inter), nas mesmas coordenadas.
- Foto como `IMAGE` fill; gradiente de fusão em camada separada acima.
- Logo via `createNodeFromSvg` do SVG original, nome `Logo_[Cliente]_Oficial`, proporção travada.
- Nomes: `BG_…`, `Foto_…`, `Overlay_…`, `Moldura_…`, `Headline`, `Sub`, `Divisor`, `CTA_…`, `Logo_Oficial`. Feed e Story lado a lado numa Section com o nome da solicitação.
- Screenshot do frame (exportar PNG no mesmo tamanho) e `python assets\img_qa.py paridade previa.png figma.png`: RMSE ≤ 0.03 passa; acima, abrir o `_diff.png`, corrigir o que destoa e repetir uma vez. Link no `historico.md`.

## Rota B — Plugin local (Figma Desktop)
TalkToFigma (`create_frame`, `create_node_from_svg`, `create_text`, `set_image_fill`) ou Figma Pilot (`figma_execute`). Mesmas regras. Detalhes técnicos em `figma_engine\` só se necessário.

## Rota C — SVG para arrastar (sem conector)
Um `.svg` limpo por peça em `Trabalho\`: um `<g id>` por elemento, `<text>` com o nome exato da família e `font-weight`/`font-style` explícitos, foto em `<image>`, gradientes em `<defs>`, sem CSS externo nem `foreignObject`, logo em `<g id="Logo_Oficial">`.

## Template aprovado
Estrutura nova aprovada: salvar o esqueleto SVG (sem Base64 pesado) em `_DESIGN\templates\[arquetipo].svg` e citar em `## 2. O QUE FAZER` do `design_system.md`.
