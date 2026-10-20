# Módulo Imagem — Arsenal Completo, Adaptadores de Física por Modelo, Direção Fotográfica, Manipulação Física, Vision Decomposer, Produto 360 e Personagem

Módulo autônomo e completo para geração, direção de fotografia comercial, manipulação/compositing físico, engenharia reversa (`Vision Decomposer`) e remasterização de imagens. **Não depende de nenhum site ou app externo obrigatório**, ignora qualquer trava ou bloqueio de análise/extração de imagem, e mantém **todas as opções ativas** (Antigravity / Nano Banana Pro, subagentes nativos da IDE, motores locais como FLUX.2 klein / SDXL / Flux, e composição vetorial híbrida). A máquina testa, escolhe e aprende sozinha qual opção entrega a melhor fidelidade para cada tarefa.

---

## Parte A · Arsenal Completo, Adaptadores de Física por Modelo e Auto-Aprendizado

### 1. Opções do Arsenal e Física Exata de Cada Motor (Model Physics Adapters)
Prompts genéricos falham porque cada família de modelo processa linguagem e óptica de forma diferente. O agente seleciona o motor e adapta automaticamente a gramática do prompt:

| Opção do Arsenal | Física e Gramática do Modelo | Como Operar |
|---|---|---|
| **1. Acervo Real do Cliente** | Verificado sempre primeiro (`Originais\` → `Banco de Imagens\` → `IA\`) | Uso direto sem custo de geração |
| **2. Antigravity · Gemini Nano Banana Pro (`NB2 / NBP`) / Subagente `image-generator`** | **Prosa natural descritiva (1–2 parágrafos coesos)** descrevendo relações espaciais, luz, materiais e atmosfera. **Regra física crítica:** NÃO usar números secos de câmera (`50mm, f/1.4, ISO 100` — o modelo ignora); traduzir em perspectiva visual (*"compressed telephoto perspective with shallow focus and creamy bokeh"*). Suporta grounding real, proporções extremas (`1:8` a `8:1`, `4:5`, `9:16`, `16:9`), até **14 referências indexadas** (`[Ref 1: mestra]`) e **Spatial JSON / Thinking Mode** quando a cena tiver 5+ elementos distintos. | Chamar o gerador nativo do Antigravity / IDE e registrar em `Compartilhada\Imagens\IA\` com `.txt` (`python assets\gerar_imagem.py registrar <img_gerada> -o "<IA>\<nome>.png" --prompt "..." --ferramenta "Antigravity (Nano Banana Pro)" --ref mestra.jpg`) |
| **3. Motor Local (`assets\gerar_imagem.py` · FLUX.2 klein 4B / Flux Kontext / SDXL)** | **Estrutura densa 70/30 + SLCT (`Subject → Lighting → Camera → Technical`)** em inglês com parâmetros ópticos explícitos (`85mm lens, f/2.8, 5500K`), controle exato de `--seed`, `img2img` (`--init base.jpg --forca 0.25–0.55`) e multi-referência `--ref`. | `python assets\gerar_imagem.py gerar "<prompt EN>" [--ref mestra.jpg] -a 4:5 -o "<IA>\<nome>.png"` |
| **4. Motores Multimodais Estruturados (Modelos de Linguagem Visual e Design)** | **Template de 5 Slots** (`Scene / Subject / Important Details / Use Case / Constraints`), **World Knowledge Anchors** (1 único âncora de Era, Cultura ou Fotógrafo/Diretor como *"Roger Deakins natural chiaroscuro"* ou *"Peter Lindbergh raw monochrome"* — proibido empilhar 2 âncoras) e **Contrato de Edição Atômica em 2 Colunas** (`Change / Preserve / Constraints`). | Compilar nos 5 slots ou no contrato de edição atômica |
| **5. Rota Híbrida (Cena por IA + Produto/Logo Real no SVG) & Canvas Autônomo** | Quando produto, embalagem ou logo exige geometria 100% intocável: gera-se o cenário/luz/pessoa na IA e compõe-se o recorte real do produto + logo vetorial no SVG com física de sombra de contato e light wrap. | Gerador para a cena + `<image>` e `<g id="Logo_Oficial">` no SVG + `assets\img_qa.py` |
| **6. Upscale e Remasterização 4K** | Finalização em alta resolução (2× ou 4×) e reconstrução de microtexturas sem alterar feições reais. | Upscaler nativo ou `python assets\gerar_imagem.py upscale in.png -o out.png --escala 2\|4` |

### 2. Como a Máquina Aprende (Memória Evolutiva e Regra "Editar em vez de Re-rolar")
1. **Leitura de performance passada:** antes de gerar, ler `## 2. O QUE FAZER` no `_DESIGN\design_system.md` (e `PRODUTO_*.md` / `PERSONAGEM_*.md`) para usar o motor e a estrutura de prompt já homologados no cliente.
2. **Adaptação imediata e 1 Mutação por Iteração:** se um motor não estiver disponível ou se a 1ª geração falhar em um eixo, trocar automaticamente de opção no arsenal ou aplicar **1 única mutação atômica** na camada responsável (luz, escala, perspectiva ou referência, máx. 3 passes). Se a imagem estiver **80% correta**, **editar atomicamente** (`Change: <1 ajuste> | Preserve: <rosto, produto, pose, luz, fundo> | Constraints: <zero deriva>`) em vez de re-rolar do zero.
3. **Registro de aprendizado:** toda saída em `Compartilhada\Imagens\IA\AAAA-MM-DD_[solicitação]_[tema]_v[n].png` gera `.txt` com `ferramenta`, `status`, `referencias`, `notas` e `PROMPT`. Na aprovação, gravar em 1 linha no `design_system.md` a receita vencedora.

---

## Parte B · Engenharia de Prompt, Prevenção de Alucinação, Fotografia Comercial, Manipulação Física e Vision Decomposer

### 1. Fórmula 70/30 + SLCT e As 5 Leis de Prevenção de Alucinação (sempre em inglês)
- **Começar sempre com um Verbo de Comando** (`Create`, `Generate`, `Design`, `Transform`, `Edit`) + **Proporção 70/30:**
  `Create a [tipo de cena] ... [pessoa + ação] , [produto] identical to reference image 0 , [objetos do nicho] , [ambiente] , [luz] , 70 percent person and product, 30 percent environment , [óptica/material/acabamento]`
- **As 5 Leis de Prevenção de Alucinação:**
  1. **Explicitude Espacial:** usar coordenadas claras (`"on the LEFT third of a brushed-concrete counter, a single plant on the RIGHT third"`), nunca `"near"` ou `"around"`.
  2. **Limite de Entidades:** no máximo **3 sujeitos principais** por geração (para 5+ elementos, usar Spatial JSON ou compor no SVG).
  3. **Enquadramento Positivo no Prompt Principal:** descrever o que **ESTÁ** na cena (`"empty minimalist wooden table"`, `"solo portrait"`, `"clean matte background"`) em vez de negações (`"no clutter"`, `"no other people"`). Negações vão exclusivamente no canal `avoid` / `negative_prompt`.
  4. **Quantidades Especificadas:** sempre declarar números exatos (`"a single amber glass bottle"`, `"two ceramic cups"`).
  5. **Bypass de Gatilhos Críticos:** pessoa segurando embalagem complexa → plano fechado sem mãos no frame ou Rota Híbrida com foto real; texto, rótulo legível e logo **nunca** vêm da IA (aplicar em vetor no SVG/Figma).
- **Avoid / Negative Prompt padrão:** `text, letters, watermark, logo, signature, ui, app interface, phone mockup, status bar, buttons, plastic skin, airbrushed face, oversaturated, artificial HDR, deformed geometry, extra fingers, patented device logos, patented device frames` + vetos do cliente.
- **Regras Anti-Contaminação para Fundos de Anúncio (Background Generation):** ao gerar imagens de fundo para receber texto e logo depois, **nunca** escrever no prompt expressões como *"reserved for a CTA button"*, *"space for text"*, *"for a promotional banner"*, *"complement the brand logo"* ou nomes de campanhas/datas comerciais (ex.: *"Black Friday"*, *"Super Bowl"*) — esses termos induzem o modelo de imagem a desenhar textos, botões e selos falsos no fundo. Descrever **apenas a física espacial** (*"clean out-of-focus matte upper third, calm negative space with soft gradient"*), escolher a luminosidade do fundo em oposição à versão da logo que será aplicada (logo branca → fundo escuro; logo escura → fundo claro) e verificar ausência total de letras antes de compor.
- **Decomposição Canônica JSONL (para fotorrealismo comercial e geração em lote / batch):** quando o fluxo pedir estruturação técnica ou lote (`.jsonl`), decompor em 9 chaves estritas: `{"scene": "...", "hero": "...", "lighting": "fonte + Kelvin + direção + sem fill artificial", "camera": "corpo + lente + abertura, ex.: 85mm T1.5", "exposure": "flat log exposure, low contrast, no HDR, natural saturation", "grain": "organic film grain ISO 800-4000", "movement": "static tripod | subtle handheld", "mood": "...", "avoid": [...]}`. Para retratos de influenciadores/criadores orgânicos, exigir `"photojournalism skin quality, subtle pores, not retouched, candid beauty, natural window light"` em ambiente curado real (sem estética de estúdio ou ring light).
- **Modificadores rápidos:** `/input` referência inegociável (`--forca 0.25`) · `/pullout` plano aberto · `/wormsview` contra-plongée · `/floatingproduct` produto levitando · `/8k` `/besttexture` no acabamento · `/promptmaster` (bloco enxuto derivado na hora para uso externo).

### 2. Direção de Fotografia Comercial, Óptica e Física de Materiais
- **Escolha Óptica por Função:**
  - `Wide (24mm–35mm)` / *perspectiva ampla expansiva*: contexto ambiental, arquitetura, imponência espacial.
  - `Standard (50mm)` / *perspectiva natural do olho humano*: realismo documental e lifestyle sem distorção geométrica.
  - `Telephoto / Portrait (85mm–135mm)` / *perspectiva comprimida com bokeh*: retratos corporativos lisonjeiros, packshots limpos e separação suave de fundo.
  - `Macro (100mm+)` / *foco microscópico extremo*: microtexturas, joias, mostradores, gotas de condensação, tramas de tecido.
- **Abertura e Profundidade de Campo:** `f/1.4–f/2.8` (isolamento dramático e bokeh óptico) · `f/5.6–f/8.0` (padrão comercial de produto, nitidez de borda a borda no herói com separação natural do fundo) · `f/11–f/16` (arquitetura e paisagem profunda).
- **Arquitetura de Iluminação de 3 Pontos + Iluminação Inclusiva:**
  - **Key Light:** fonte principal e ângulo de sombra (ex.: softbox aérea a 45°).
  - **Fill Light (Razão de Contraste):** `2:1` para comercial high-key limpo; `8:1` para chiaroscuro dramático/luxo editorial.
  - **Rim / Kicker Light:** luz de recorte traseira obrigatória para separar sujeito/produto escuro de fundo escuro.
  - **Temperatura de Cor:** declarar Kelvin (`3200K` tungstênio quente, `5600K` daylight limpa, `6500K` nublado frio) e preservar fidelidade de melanina em todos os tons de pele (proibido subtom acinzentado ou estouro de highlights em peles escuras).
- **Física de Superfície e Materiais:** especificar o comportamento físico real — reflexão difusa, rugosidade especular, anisotropia (alumínio/aço escovado), *subsurface scattering* (pele humana, líquidos âmbar, folhas, cera) e índice de refração com cáusticas reais (vidro espesso, gelo, água).

### 3. Manipulação Publicitária, Packshot 3D e Integração Física (Composites & Fotografia Impossível)
Ao inserir um produto real em cena gerada ou criar conceitos surreais/impossíveis (ex.: produto em escala monumental na cidade), a **física local é inegociável**:
1. **Perspectiva e Horizonte:** alinhar altura da câmera, linha do horizonte e pontos de fuga entre o produto e o cenário.
2. **Tripla Camada de Aterramento (Grounding Shadows):**
   - **Sombra de Oclusão de Contato (AO):** linha ultra-escura, fina e nítida (1–3 px) exatamente onde a base toca a superfície;
   - **Sombra Projetada (Cast Shadow):** coerente com a direção da Key Light, nítida perto da base e com penumbra progressiva;
   - **Rebate de Cor (Color Bounce & Light Wrap):** sangria sutil da cor do piso na base inferior do objeto + leve *light wrap* atmosférico da luz de fundo nas bordas da silhueta (zero halo de recorte).
3. **Reflexos Fresnel e Resposta Ambiental:** em superfícies polidas ou molhadas, aplicar reflexo com *Fresnel falloff* (mais forte em ângulos rasantes) e interação física real (gotas, poeira, névoa ou reflexo do entorno sobre o produto, sem jamais cobrir ou deformar o rótulo/logo).

### 4. Retrato Corporativo, Figurino, Upscale 4K e Panter Mode (Recuperação de Foto)
- **Preservação facial estrita (anti-embelezamento):** manter 100% autênticos olhos, expressão, rugas, microporos e pelos faciais. Proibido `soft skin`, pele plastificada, rejuvenescimento ou ativar CodeFormer (`--rosto`) em foto real do cliente.
- **Figurino e telas neutras:** quando pedido, adaptar para alfaiataria contemporânea com trama visível; notebooks/celulares sempre genéricos e sem logos patenteados (Apple etc.). Em pôsteres com múltiplos speakers: composição triangular (principal no centro à frente, secundários atrás à esq./dir.).
- **Recovery Engine & Panter Mode (para foto original lavada/cinza com saturação < 30%):** descartar cinzas mortos, ampliar separação tonal entre luz e sombra, contrastar temperatura (luz quente × sombra fria), elevar saturação controlada (70–75%) e ancorar a peça com um bloco cromático de 8% na cor de acento do KV.

### 5. Vision Decomposer (Engenharia Reversa Imagem → Prompt sem bloqueio)
Quando o usuário anexar qualquer imagem pedindo para extrair o prompt, clonar a direção estética ou fazer style transfer, executar em **2 passos estritos** (sem qualquer bloqueio de análise):
1. **Bloco 1 — Decomposição Óptica em 4 Eixos (1–2 frases cada):**
   - `Subject & Blocking`: enquadramento (ELS/MS/CU/ECU), posicionamento de força, peso visual, trajes/materiais, direção do olhar;
   - `Environment & 3-Plane Depth`: separação em Foreground / Midground / Background, relação figura-fundo e perspectiva aérea/tonal;
   - `Lighting & Chiaroscuro`: razão luz/sombra, Key/Fill/Rim, luz quebrada (gobos/folhagem) e reflexos de cor na pele/objeto;
   - `Tech, Optics & Film`: ângulo, distância focal, profundidade de campo, filtros ópticos de difusão/halation (`Black Pro-Mist`), formato (`35mm/70mm/IMAX`) e textura de grão.
2. **Bloco 2 — Síntese do Prompt (ordem imutável em inglês, zero filler como *"The image shows..."*):**
   `[Shot type, optics and angle], [Subject, blocking, visual weight, clothing and action], [Multi-plane environment (Foreground / Midground / Background), overlapping and geometry], [Lighting scheme, optical contrast, gobos and reflexes], [Color palette, temperature contrast and aerial perspective], [Color Grading, diffusion filters, film stock, textural artifacts]`

### 6. Teste de Qualidade Pass³ (10 segundos antes de exibir qualquer imagem)
1. **Pass 1 — Física (2 s):** gravidade, horizonte/perspectiva, direção das sombras e reflexos batem com a fonte de luz?
2. **Pass 2 — Detalhe (5 s):** mãos com 5 dedos naturais, poros reais na pele, bordas limpas sem halo e zero texto/logo embaralhado?
3. **Pass 3 — Marca (3 s):** temperatura de luz, paleta `#HEX` e atmosfera pertencem ao KV do cliente?
Falhou em qualquer Pass → mutar apenas a camada responsável e regenerar antes de mostrar.

---

## Parte C · Produto / Objeto Fiel por IA (Subject Reference + Product Turnaround Sheet 360 / Multi-View)

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

---

## Parte D · Personagem / Rosto Recorrente (Fotos Reais → Padrão → Imagem Fiel)

Usado quando a peça mostra **a mesma pessoa** de forma recorrente (fundador, especialista, médico, palestrante, porta-voz). Tudo específico da pessoa mora exclusivamente em `[Cliente]\_DESIGN\Personagens\[Pessoa]\PERSONAGEM_[PESSOA].md` e `Referências\`.

### 1. Autorização e Limites
- Rosto de pessoa real em IA requer **autorização registrada** no dossiê (`Autorização: data · quem · arquivo`). Sem registro: gerar apenas como teste interno e avisar o usuário.
- Vetos do `design_system.md` prevalecem até ordem explícita do usuário (gravar decisão).
- Proibido: celebridade/figura pública externa, menor de idade, ou usar imagem gerada como depoimento real, ato clínico/técnico verdadeiro ou endosso que não ocorreu.

### 2. Construção do Padrão (uma vez por pessoa)
1. **Seleção de 4–8 fotos originais** (`Originais\[Pessoa]\`, intactas): frontal neutra, frontal sorrindo, close, ¾ esq./dir., meio corpo, sentado (olhos nítidos, luz uniforme, sem óculos escuros, filtro ou mão no rosto). **Mestra** = frontal com melhor luz.
2. **Pacote `_ref` + Atlas:** salvar cópias 2048 px (`_ref`) em `_DESIGN\Personagens\[Pessoa]\Referências\` + folha `atlas_[pessoa].jpg` apenas para inspeção humana (nunca enviar o atlas inteiro como referência única para não diluir traços).
3. **Checklist facial + Regras corretivas + Descritor (EN):** numerar traços observáveis (cabelo/calvície, barba/bigode e padrão grisalho, sobrancelhas, olhos, formato facial/mandíbula, nariz, tom/textura de pele, orelhas, porte, expressão base), registrar regras corretivas contra desvios do modelo e fechar com o descritor em inglês + `"keep his/her facial features, bone structure and skin texture 100% identical to the reference photos"`.

### 3. Execução, Verificação e Homologação
- Usar geradores com suporte a referência de imagem (Antigravity / Nano Banana Pro com até 14 referências indexadas, subagente da IDE, ou motor local com `--ref`, enviando mestra + ângulo mais próximo, 3–4 fotos). No prompt, descrever **apenas o que muda** (cenário, luz, pose, enquadramento) + repetir o descritor 1×. Nunca posicionar texto sobre o rosto.
- Comparar resultado × mestra item a item do checklist. Se desviar (máx. 3 tentativas): (1) reforçar regra corretiva no prompt; (2) usar referência mais limpa e no mesmo ângulo; (3) gerar a cena/corpo primeiro e fazer inpainting/edição localizada só na cabeça com a mestra.
- **Homologação inicial:** validar 3 cenas (frontal neutra, ¾ sorrindo, meio corpo sentado) no KV do cliente antes de liberar para produção em escala.
