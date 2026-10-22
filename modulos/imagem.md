# Módulo Imagem — Arsenal, Adaptadores por Motor, Direção Fotográfica, Composição Física e Vision Decomposer

Geração, direção de fotografia comercial, compositing físico, engenharia reversa e remasterização. Usar a primeira opção do arsenal disponível na sessão (núcleo §0.6); o aprendizado é a receita vencedora gravada no `design_system.md` (A.2), não memória implícita. Produto fiel/360 → `imagem-produto.md`; pessoa recorrente → `imagem-personagem.md`.

---

## Parte A · Arsenal Completo, Adaptadores de Física por Modelo e Auto-Aprendizado

### 1. Opções do Arsenal e Física Exata de Cada Motor (Model Physics Adapters)
Prompts genéricos falham porque cada família de modelo processa linguagem e óptica de forma diferente. O agente seleciona o motor e adapta automaticamente a gramática do prompt:

| Opção do Arsenal | Física e Gramática do Modelo | Como Operar |
|---|---|---|
| **1. Acervo Real do Cliente** | Verificado sempre primeiro (`Originais\` → `Banco de Imagens\` → `Tratadas\` → `IA\`, núcleo Lei 5) | Uso direto sem custo de geração |
| **2. Antigravity · Gemini Nano Banana Pro (`NB2 / NBP`) / Subagente `image-generator`** | Prosa natural costuma funcionar bem; descrever ideia, relações espaciais, luz, materiais e atmosfera de acordo com a cena. Usar termos ópticos em linguagem visual quando parâmetros técnicos não ajudarem este motor. Suporta grounding real, proporções variadas, referências indexadas e Spatial JSON / Thinking Mode quando a complexidade justificar. | Chamar o gerador nativo do Antigravity / IDE e registrar em `Compartilhada\Imagens\IA\` com `.txt` (`python assets\gerar_imagem.py registrar <img_gerada> -o "<IA>\<nome>.png" --prompt "..." --ferramenta "Antigravity (Nano Banana Pro)" --ref mestra.jpg`) |
| **2b. Gemini API (chave própria · portátil)** | Mesma gramática da opção 2. Flash por padrão; `--pro` = Nano Banana Pro. Chave em `GEMINI_API_KEY` (criar em aistudio.google.com/apikey; cobrança separada da assinatura Gemini). Modelo trocável em `GEMINI_IMAGE_MODEL`. | `python assets\gerar_imagem.py gemini "<prompt>" [--ref mestra.jpg] [--pro] -a 4:5 -o "<IA>\<nome>.png"` |
| **2c. Conector de imagem (Figma, Runway etc.)** | Bônus: usar se a sessão tiver a ferramenta. Gramática da opção 2. | Gerar pelo conector e `registrar` como na opção 2 |
| **3. Motor Local (`assets\gerar_imagem.py` · FLUX.2 klein 4B / Flux Kontext / SDXL)** | SLCT (`Subject → Lighting → Camera → Technical`) pode ajudar em cenas fotográficas controladas; escolha apenas os eixos que a ideia precisa. Proporção, parâmetros ópticos, `--seed`, `img2img` (`--init base.jpg --forca 0.25–0.55`) e multi-referência `--ref` são controles disponíveis, não presets visuais. | `python assets\gerar_imagem.py gerar "<prompt>" [--ref mestra.jpg] -a 4:5 -o "<IA>\<nome>.png"` |
| **4. Edição por instrução (qualquer gerador que aceite imagem + texto)** | Usar instruções claras sobre o que mudar, o que preservar e os limites de identidade. Slots e referências de linguagem podem ajudar quando aumentarem a precisão; são opcionais e não devem achatar uma ideia criativa. | Especificar a edição na estrutura mais clara para o motor |
| **5. Rota Híbrida (Cena por IA + Logo/Rótulo Real no SVG) & Canvas Autônomo** | Só para o que a IA não pode escrever: logo, texto, rótulo legível de embalagem, ou quando o usuário pedir colagem. **Nunca** para produto ou personagem com pacote 360/referência: o pacote condiciona o gerador e a cena nasce inteira com o produto (`imagem-produto.md` §3); recorte colado em cenário gerado reprova. | Gerador para a cena + `<image>` e `<g id="Logo_Oficial">` no SVG + `assets\img_qa.py` |
| **M. Modo Manual (fallback universal)** | Sem gerador na sessão: entregar o prompt pronto em bloco de código + proporção. O usuário gera no Gemini/Flow e salva a imagem na pasta. | `python assets\gerar_imagem.py registrar <img> -o "<IA>\<nome>.png" --prompt "..." --ferramenta "Gemini app (manual)"` |
| **Z. Último recurso (sem gerador)** | Trata imagem existente; não cria imagem nova. Avisar o usuário que a qualidade fica inferior. Ajuste fino manual: Graphite (editor.graphite.art, gratuito). | `node assets\tratar_imagem.mjs enquadrar\|ampliar\|compor <in> -o "<Tratadas>\<nome>_trat.png"` (1×: `cd assets && npm i sharp`) |
| **6. Upscale e Remasterização 4K** | Finalização em alta resolução (2× ou 4×) e reconstrução de microtexturas sem alterar feições reais. | Upscaler nativo ou `python assets\gerar_imagem.py upscale in.png -o out.png --escala 2\|4` |

### 2. Como a Máquina Aprende (Memória Evolutiva e Regra "Editar em vez de Re-rolar")
1. **Leitura de performance passada:** antes de gerar, ler `## 2. O QUE FAZER` no `_DESIGN\design_system.md` (e `PRODUTO_*.md` / `PERSONAGEM_*.md`) para usar o motor e a estrutura de prompt já homologados no cliente.
2. **Adaptação imediata e 1 Mutação por Iteração:** se um motor não estiver disponível, tentar o próximo **gerador** (2 → 2b → 2c → 3); nenhum disponível = Regra da Falha (`SKILL.md` §0.6) + Modo Manual; opção Z só como último recurso e com aviso. Se a 1ª geração falhar em um eixo, trocar de gerador ou aplicar **1 única mutação atômica** na camada responsável (luz, escala, perspectiva ou referência, máx. 3 passes). Se a imagem estiver **80% correta**, **editar atomicamente** (`Change: <1 ajuste> | Preserve: <rosto, produto, pose, luz, fundo> | Constraints: <zero deriva>`) em vez de re-rolar do zero.
3. **Registro de aprendizado:** toda saída (inclusive descartada e cena de produto) em `Compartilhada\Imagens\IA\AAAA-MM-DD_[solicitação]_[tema]_v[n].png` — nunca em `Originais\`, `Banco de Imagens\` ou `Referências\` de produto/personagem (o `gerar_imagem.py` recusa esses destinos) — gera `.txt` com `ferramenta`, `status`, `referencias`, `notas` e `PROMPT`. Na aprovação, gravar em 1 linha no `design_system.md` a receita vencedora.

---

## Parte B · Engenharia de Prompt, Prevenção de Alucinação, Fotografia Comercial, Manipulação Física e Vision Decomposer

### 1. Prompt por intenção, motor e cena
- Comece pela ideia visual e pela ação/relação que a imagem precisa expressar; escolha idioma, prosa, slots ou JSON conforme o motor e a complexidade. Não há verbo, idioma, proporção sujeito/ambiente ou modelo de prompt obrigatório.
- **Precisão quando necessária:** esclareça posição relativa quando houver risco de ambiguidade espacial, contagens quando o número for relevante, e limites de entidades quando o modelo estiver perdendo elementos. Simplifique ou divida uma cena apenas se isso melhorar o resultado; cenas densas e composições deliberadamente complexas não são proibidas.
- **Identidade e fatos:** preserve produto, pessoa, marca e detalhes solicitados; texto/logo/rótulo que precisem ficar exatos devem ser aplicados como ativos reais fora da imagem gerada. Metáforas e abstrações são bem-vindas quando não forem apresentadas como evidência factual.
- Use `avoid`/`negative_prompt` quando o motor oferecer esse canal e houver algo concreto a excluir; não descarte a abordagem natural do modelo por uma blacklist fixa.
- **Fundo para receber composição posterior:** se a imagem precisar de espaço de texto/logo, descreva a cena e as áreas de respiro visualmente. Evite instruções que peçam ao gerador que desenhe o texto, CTA ou selos reais; a orientação espacial pode ser positiva e integrada à cena.
- **Lote estruturado:** use JSONL ou slots somente quando o usuário pedir lote/estruturação ou quando a ferramenta exigir. Defina apenas campos úteis à tarefa; não imponha esquema técnico completo a uma imagem isolada.
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
  - **Rim / Kicker Light:** usar quando a separação de sujeito/produto escuro de fundo escuro pedir recorte; pode ser dispensada se a referência ou o KV resolverem a separação por valor, cor ou contorno.
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
   - `Tech, Optics & Film`: ângulo, perspectiva, profundidade de campo e textura visíveis; distância focal, filtro ou formato só como aproximação de efeito, nunca como metadado inferido com certeza.
2. **Bloco 2 — Síntese do Prompt (ordem imutável em inglês, zero filler como *"The image shows..."*):**
   `[Shot type, optics and angle], [Subject, blocking, visual weight, clothing and action], [Multi-plane environment (Foreground / Midground / Background), overlapping and geometry], [Lighting scheme, optical contrast, gobos and reflexes], [Color palette, temperature contrast and aerial perspective], [Color Grading, diffusion filters, film stock, textural artifacts]`

### 6. Teste de Qualidade Pass³ (10 segundos antes de exibir qualquer imagem)
1. **Pass 1 — Física (2 s):** gravidade, horizonte/perspectiva, direção das sombras e reflexos batem com a fonte de luz?
2. **Pass 2 — Detalhe (5 s):** mãos com 5 dedos naturais, poros reais na pele, bordas limpas sem halo e zero texto/logo embaralhado?
3. **Pass 3 — Marca (3 s):** temperatura de luz, paleta `#HEX` e atmosfera pertencem ao KV do cliente?
Falhou em qualquer Pass → mutar apenas a camada responsável e regenerar antes de mostrar.

---

## Parte C · Imagem Publicitária (Direção de Cena e Hero Shot)
Imagem para anúncio precisa sustentar o argumento comercial. Receber de `ads.md` §1 a **Proposição Visual**, a função do ativo e o elo da copy que a cena mostrará; sem eles, defini-los antes da curadoria ou do prompt. Esta parte também se aplica quando a imagem final é uma fotografia real já existente: selecionar o enquadramento, gesto, olhar, luz, profundidade e espaço negativo que expressem a intenção; não tratar “tem a pessoa certa” como direção suficiente. Aplicar U9: distinguir contexto de prova factual; uma cena elegante que só sugere o setor ou a tecnologia reprova. Sem diferencial confirmado, usar contexto já presente no briefing/KV; nunca inventar atributo, resultado ou claim. Se a cena servir igualmente a qualquer concorrente ao trocar a marca, ou só mostrar o produto sem relação com a copy, refazer a direção antes de gerar.
**Direção visual sem briefing técnico:** usuário decide qualquer eixo que especificar. Nos eixos livres, aplicar nesta ordem: referências visuais deste pedido (`referencias.md` §§3–4) → receita de imagem aprovada em `_DESIGN\design_system.md` → base inicial abaixo. KV e fidelidade de produto/pessoa limitam todas as fontes. Não pedir câmera, luz, profundidade ou atmosfera só porque faltou referência.
**Base inicial adaptável:** a ideia pode ser narrativa, simbólica, editorial, surreal ou documental; escolha o que melhor transforma a mensagem em imagem sem tratar metáfora como prova. Câmera, luz, escala, perspectiva, planos e atmosfera são decisões de direção, não uma ficha que exige todos os recursos em toda imagem. Em qualquer criativo novo que peça impacto — inclusive conteúdo executivo, educacional ou citação — considere ativamente a linguagem publicitária/heroica/cinematográfica e compare-a com alternativas mais contidas; não a reserve a campanhas de produto. Não imponha pôr do sol, piso molhado, bokeh, névoa, lente ou paleta cinematográfica como preset, nem rejeite esses recursos quando a cena os justificar. Após aprovação, registrar a combinação vencedora como receita do cliente (§7 do núcleo); antes disso é hipótese criativa, não padrão comprovado.
1. **Ficha de direção (1 linha cada, no `.txt`):** papel na peça (capa, prova, endcard) · argumento e prova visual · território (`ads.md` §1) · gesto do herói · enquadramento/perspectiva · luz motivada e contraste · profundidade/atmosfera · paleta do KV · área de respiro se houver texto posterior. Cada escolha deve apoiar o argumento; “cinematográfico”, “premium” e nomes de lentes sozinhos não são direção.
2. **Ângulo do herói por categoria (referência, não preset):** veículo/aeronave pode pedir ¾ baixo para mostrar forma e escala; produto de mesa, ¾ ou macro para revelar material/uso; arquitetura, perspectiva corrigida que mostre espaço habitável; pessoa, distância e olhar que sustentem a ação; interior, POV de quem usa. Escolher hora, clima, reflexo e luz pelo benefício e pelo KV. Pôr do sol, piso molhado, rim light e bokeh só entram quando tiverem função narrativa ou física.
3. **Hierarquia do herói:** imagem, tipografia ou símbolo podem ser protagonistas. Quando pessoa ou produto for o herói, dimensionar e cortar segundo o conceito e a identidade; evitar cortes acidentais que prejudiquem reconhecimento, sem impor percentual de área ou silhueta inteira. O fundo pode contrastar ou disputar deliberadamente quando isso compuser a ideia. Em retrato real, preferir um crop que preserve expressão e gesto pertinentes à mensagem; tratamento de cor deve respeitar pele e luz existentes, não aplicar tonalização ou halo genérico como atalho de marca.
4. **Coerência física:** verificar horizonte, sombras, reflexos, materiais e luz quando estiverem visíveis e forem relevantes; não adicionar sombra de contato, piso reflexivo ou luz de recorte a cenas que não precisam deles.
5. **Conceito novo:** usar a hipótese criativa já escolhida em `ads.md` §1 quando esse fluxo estiver ativo. Para imagem isolada, comparar ideias de forma leve antes de gerar; variedade de conceito vale mais que três renderizações quase iguais. Mostrar alternativas só quando o usuário pedir.
6. **Pass³ + teste publicitário:** conferir detalhes que realmente aparecem (identidade, mãos, texto acidental, contorno, perspectiva) e se a imagem realiza a intenção visual sem distorcer a marca ou afirmar fatos sem base. Não é obrigatório que toda imagem seja entendida em 1 s, tenha herói fotográfico dominante ou reserve espaço para copy.
7. **Série:** quando a imagem integra campanha/carrossel, aplicar U10 na ficha de direção e comparar as cenas na prancha; manter tempo e lógica ambiental coerentes, com composição distinta para cada mensagem.
