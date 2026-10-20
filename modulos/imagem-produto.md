# Anexo Imagem · Produto / Objeto Fiel (360 · Turnaround · Multi-View)
Carregado só junto com `imagem.md` (Partes A–B: arsenal, prompt, Pass³).

## Produto / Objeto Fiel por IA (Subject Reference + Product Turnaround Sheet 360 / Multi-View)

Usado para aeronave, veículo, embalagem, máquina, imóvel ou peça que exige fidelidade exata ao exemplar real do cliente.
**Nome técnico exato e gatilhos rápidos:** `Product Turnaround Sheet 360` (ou `Multi-View Consistency Sheet`). Ativa imediatamente com: `/designer-mestre 360`, `/designer-mestre turnaround`, `/designer-mestre multiview`, `/designer-mestre produto`, `manual 360`, `modelo 360`.

### 1. Organização e Regras de Ouro
- **Arquivos:** fotos reais em `[Cliente]\Compartilhada\Imagens\Originais\[Produto]\` (só leitura); dossiê manual 360 em `[Cliente]\_DESIGN\Produtos\[Produto]\PRODUTO_[NOME].md`; prancha e referências tratadas em `[Cliente]\_DESIGN\Produtos\[Produto]\Referências\turnaround_[produto].png`.
- **Pesquisa Técnica Automática (Web Search):** quando o cliente não tiver fotos de todos os ângulos do modelo exato (ex.: aeronave, veículo ou equipamento específico), pesquisar imediatamente na web as especificações geométricas exatas do fabricante/modelo (dimensões, número e formato de janelas, tipo de asa/ponta de asa, posição de motores, cauda/rodas) e cruzar com as fotos reais do cliente (para extrair a pintura/livery real e o cenário real, como a fachada do hangar/sede).
- **Foto real primeiro:** se o briefing exigir "foto real", só usar IA com autorização explícita do usuário gravada no `design_system.md`.
- **Referência = exemplar DO CLIENTE:** modelo 3D externo ou foto de outro exemplar servem apenas como apoio de geometria, nunca como mestra (pintura, faixas, acabamentos e detalhes vêm exclusivamente das fotos reais do cliente). Nunca incluir matrícula, placa, número de série, marca d'água ou logo externo.

### 2. Construção do Padrão, Geometria Multi-View e Turnaround Sheet (uma vez por produto)
1. **Seleção de 4–8 vistas reais e Parâmetros de Câmera Multi-View:** frontal (`0°`), ¾ frontal esq./dir. (`30°–45°`), perfil lateral (`90°`), ¾ traseira (`150° / 210°`), traseira (`180°`), lateral oposta (`270° / 330°`), superior (`top-down`) e 1–3 detalhes. Quando sintetizar ou calibrar pranchas multi-view consistentes a partir de 1 imagem frontal recortada (em canvas quadrado `>= 320×320 px` com objeto centralizado e tamanho normalizado), usar **FOV fixo de `30°`** (evita distorção de grande-angular em close-up de produto), azimutes relativos `30°, 90°, 150°, 210°, 270°, 330°` com elevações alternadas `20°` e `-10°`, e passes de mapa de normais (`view-space normal map`) + `depth map` para extração de máscara alfa com precisão de borda superior a 98%. **Mestra** = ¾ frontal com melhor luz e nitidez.
2. **Pacote `_ref` + Turnaround:** salvar cópias com 2048 px no lado maior (`_ref`) e montar `turnaround_[produto].jpg` (prancha em fundo neutro cinza claro com os ângulos canônicos, sombras de contato suaves e proporções idênticas).
3. **Geração de vista faltante e Modo de Aplicação/Substituição (`Apply/Replace`):**
   - Se faltar um ângulo, gerar a partir da mestra + vista mais próxima no Antigravity (Nano Banana Pro) ou motor local (`Product turnaround view: exact same product as reference image 0 seen from <ângulo>, clean neutral studio cyclorama background, identical proportions and livery, 30-degree FOV`), validar contra as fotos reais e marcar como `_gerada` (nunca vira mestra).
   - Para substituir um produto em cena já aprovada sem alterar o ambiente (`Replace Mode`): `"Apply the reference product to the image and remove traces of any other product in the same category. Preserve the original environment and lighting intact; maintain the exact shape, proportions, materials, colors, brand identity and geometry of the reference product with realistic contact shadows"`.
4. **Checklist de identidade + Regras corretivas + Descritor (EN):** numerar no `PRODUTO_[NOME].md` apenas o observável (silhueta, nº/forma de janelas ou aberturas, posição de motores/rodas/tampa, faixas e cores exatas, acabamento brilho/fosco, itens proibidos), adicionar regras curtas a cada erro detectado e fechar com o descritor em inglês + `"keep the object's shape, proportions, livery and details exactly as in the reference images; no text, no registration marks"`.

### 3. Execução e Verificação
- Enviar **mestra + vista do ângulo pedido + 1 detalhe** (3–4 imagens). Se a cena exigir precisão absoluta do produto sobre fundo real (ex.: hangar, estrada, bancada), testar tanto a geração integrada com referência (Nano Banana Pro / FLUX.2 klein) quanto a **Rota Híbrida** (gerar/usar o fundo e compor o produto no ângulo exato via SVG/Figma com sombra de contato AO + Cast Shadow e light wrap igualados) — a máquina escolhe e aprende o que fica mais perfeito.
- Conferir item a item do checklist contra a mestra (máx. 3 tentativas refinando regra corretiva ou trocando referência).
