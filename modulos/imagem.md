# Módulo Imagem — Arsenal, Adaptadores por Motor, Direção Fotográfica, Composição Física e Vision Decomposer

Geração, direção de fotografia comercial, compositing físico, engenharia reversa e remasterização. Usar a primeira opção do arsenal disponível na sessão (núcleo §0.6); o aprendizado é a receita vencedora gravada no `design_system.md` (A.2), não memória implícita. Produto fiel/360 → `imagem-produto.md`; pessoa recorrente → `imagem-personagem.md`.

---

## Parte A · Arsenal Completo, Adaptadores de Física por Modelo e Auto-Aprendizado

### 1. Opções do Arsenal e Física Exata de Cada Motor (Model Physics Adapters)
Prompts genéricos falham porque cada família de modelo processa linguagem e óptica de forma diferente. O agente seleciona o motor e adapta automaticamente a gramática do prompt:

| Opção do Arsenal | Física e Gramática do Modelo | Como Operar |
|---|---|---|
| **1. Acervo Real do Cliente** | Verificado sempre primeiro (`Originais\` → `Banco de Imagens\` → `Tratadas\` → `IA\`, núcleo Lei 5) | Uso direto sem custo de geração |
| **2. Antigravity · Gemini Nano Banana Pro (`NB2 / NBP`) / Subagente `image-generator`** | **Prosa natural descritiva (1–2 parágrafos coesos)** descrevendo relações espaciais, luz, materiais e atmosfera. **Regra física crítica:** NÃO usar números secos de câmera (`50mm, f/1.4, ISO 100` — o modelo ignora); traduzir em perspectiva visual (*"compressed telephoto perspective with shallow focus and creamy bokeh"*). Suporta grounding real, proporções extremas (`1:8` a `8:1`, `4:5`, `9:16`, `16:9`), até **14 referências indexadas** (`[Ref 1: mestra]`) e **Spatial JSON / Thinking Mode** quando a cena tiver 5+ elementos distintos. | Chamar o gerador nativo do Antigravity / IDE e registrar em `Compartilhada\Imagens\IA\` com `.txt` (`python assets\gerar_imagem.py registrar <img_gerada> -o "<IA>\<nome>.png" --prompt "..." --ferramenta "Antigravity (Nano Banana Pro)" --ref mestra.jpg`) |
| **3. Motor Local (`assets\gerar_imagem.py` · FLUX.2 klein 4B / Flux Kontext / SDXL)** | **Estrutura densa 70/30 + SLCT (`Subject → Lighting → Camera → Technical`)** em inglês com parâmetros ópticos explícitos (`85mm lens, f/2.8, 5500K`), controle exato de `--seed`, `img2img` (`--init base.jpg --forca 0.25–0.55`) e multi-referência `--ref`. | `python assets\gerar_imagem.py gerar "<prompt EN>" [--ref mestra.jpg] -a 4:5 -o "<IA>\<nome>.png"` |
| **4. Edição por instrução (qualquer gerador que aceite imagem + texto)** | **Template de 5 Slots** (`Scene / Subject / Important Details / Use Case / Constraints`), **World Knowledge Anchors** (1 único âncora de Era, Cultura ou Fotógrafo/Diretor como *"Roger Deakins natural chiaroscuro"* ou *"Peter Lindbergh raw monochrome"* — proibido empilhar 2 âncoras) e **Contrato de Edição Atômica em 2 Colunas** (`Change / Preserve / Constraints`). | Compilar nos 5 slots ou no contrato de edição atômica |
| **5. Rota Híbrida (Cena por IA + Produto/Logo Real no SVG) & Canvas Autônomo** | Quando produto, embalagem ou logo exige geometria 100% intocável: gera-se o cenário/luz/pessoa na IA e compõe-se o recorte real do produto + logo vetorial no SVG com física de sombra de contato e light wrap. | Gerador para a cena + `<image>` e `<g id="Logo_Oficial">` no SVG + `assets\img_qa.py` |
| **6. Upscale e Remasterização 4K** | Finalização em alta resolução (2× ou 4×) e reconstrução de microtexturas sem alterar feições reais. | Upscaler nativo ou `python assets\gerar_imagem.py upscale in.png -o out.png --escala 2\|4` |

### 2. Como a Máquina Aprende (Memória Evolutiva e Regra "Editar em vez de Re-rolar")
1. **Leitura de performance passada:** antes de gerar, ler `## 2. O QUE FAZER` no `_DESIGN\design_system.md` (e `PRODUTO_*.md` / `PERSONAGEM_*.md`) para usar o motor e a estrutura de prompt já homologados no cliente.
2. **Adaptação imediata e 1 Mutação por Iteração:** se um motor não estiver disponível ou se a 1ª geração falhar em um eixo, trocar automaticamente de opção no arsenal ou aplicar **1 única mutação atômica** na camada responsável (luz, escala, perspectiva ou referência, máx. 3 passes). Se a imagem estiver **80% correta**, **editar atomicamente** (`Change: <1 ajuste> | Preserve: <rosto, produto, pose, luz, fundo> | Constraints: <zero deriva>`) em vez de re-rolar do zero.
3. **Registro de aprendizado:** toda saída (inclusive descartada e cena de produto) em `Compartilhada\Imagens\IA\AAAA-MM-DD_[solicitação]_[tema]_v[n].png` — nunca em `Originais\`, `Banco de Imagens\` ou `Referências\` de produto/personagem (o `gerar_imagem.py` recusa esses destinos) — gera `.txt` com `ferramenta`, `status`, `referencias`, `notas` e `PROMPT`. Na aprovação, gravar em 1 linha no `design_system.md` a receita vencedora.

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
- Geradores não entregam fundo transparente: gerar em fundo liso e remover o fundo, ou compor no SVG (Rota Híbrida). Prompt de fundo sem nome de marca.
- Lote: listar os conceitos em PT e aprovar o conjunto antes de gerar o `.jsonl` (1 job por linha).

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

### 5. Vision Decomposer (Engenharia Reversa Imagem → Prompt)
Quando o usuário anexar qualquer imagem pedindo para extrair o prompt, clonar a direção estética ou fazer style transfer, executar em **2 passos estritos**:
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

## Parte C · Imagem Publicitária (Hero Shot)
Imagem para anúncio não é "foto bonita": é a prova visual do argumento da peça. Antes de gerar, escrever a **Proposição Visual em 1 frase** (`ads.md` §1) e só então o prompt.
1. **Ficha de direção (1 linha cada, no `.txt`):** papel na peça (capa, prova, endcard) · território (`ads.md` §1) · ângulo do herói · lente · esquema de luz · hora/clima · área de respiro para texto (terço e lado, oposta ao herói) · tratamento de cor (sombras e altas puxadas para a paleta do KV) · 1 gesto marcante.
2. **Ângulo do herói por categoria** (adaptar ao KV): veículo/aeronave = ¾ frontal baixo (câmera na altura das rodas/trem), tele 85–135 mm para comprimir fundo, golden hour ou blue hour com rim light no contorno e piso molhado/polido refletindo; produto de mesa = 3/4 a 30–45°, f/8, key softbox + rim; arquitetura/imóvel = 24–35 mm com verticais corrigidas, crepúsculo com interiores acesos; pessoa = 85 mm, olhar com intenção, luz de janela; interior de veículo/aeronave/imóvel = 24–28 mm da posição do usuário (POV de quem senta), linhas convergindo para o ponto de interesse.
3. **Herói dominante:** ocupa 35–60% da área útil, silhueta inteira e legível na miniatura 100 px; nada corta bico, roda, cauda ou cabeça; fundo atrás do texto liso e calmo (desfoque, céu, parede, degradê natural).
4. **Física publicitária:** horizonte e altura de câmera coerentes; sombra de contato + sombra projetada; reflexo coerente no piso; luz de recorte separando herói escuro de fundo escuro; nada de HDR, halo ou saturação artificial.
5. **3 variações estruturais** quando for conceito novo (ângulo, luz/hora, ambiente), nunca só cor; mostrar as 3 numa prancha (núcleo §2) e gerar a peça só com a escolhida.
6. **Pass³ + teste publicitário:** além do Pass³ (Parte B §6), responder sim/não: o herói se entende em 1 s? há espaço limpo para headline e logo sem cobrir o herói? a cor já parece da marca antes do texto? Um "não" = 1 mutação na camada responsável.

