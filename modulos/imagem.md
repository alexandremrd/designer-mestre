# Módulo Imagem — Arsenal Completo de Geradores, Auto-Aprendizado da Máquina, Produto Fiel (360), Personagem, Packshot e Upscale

Módulo autônomo e completo para geração, edição e remasterização de imagens. **Não depende de nenhum site ou app externo obrigatório** e mantém **todas as opções ativas** (Antigravity / Nano Banana Pro, subagentes nativos da IDE, modelos multimodais, motores locais como FLUX.2 klein / Easy Diffusion / ComfyUI, e composição vetorial híbrida). A máquina tem liberdade total para testar, comparar e aprender sozinha qual opção entrega a melhor fidelidade para o seu hardware, ambiente e cliente.

---

## Parte A · Arsenal Completo de Geração e Auto-Aprendizado da Máquina

### 1. Todas as opções disponíveis (a máquina escolhe e aprende qual é a melhor para si)
Nenhuma rota é bloqueada ou descartada. O agente avalia o que está ativo na sessão e escolhe — ou combina — a melhor opção para cada caso:

| Opção do Arsenal | Onde brilha | Como operar |
|---|---|---|
| **1. Acervo Real do Cliente** | Sempre verificado primeiro (`Originais\` → `Banco de Imagens\` → `IA\`) | Uso direto sem custo de geração |
| **2. Antigravity · Nano Banana Pro / Subagente `image-generator` / Nativo da IDE** | Fotorrealismo de ponta, compreensão profunda de prompt, edição contextual, preservação de produto/rosto com até múltiplas imagens de referência | Chamar o gerador nativo do Antigravity / IDE passando as referências (`Originais\` / `_ref`) e o prompt; registrar saída em `Compartilhada\Imagens\IA\` com `.txt` (`python assets\gerar_imagem.py registrar <img_gerada> -o "<IA>\<nome>.png" --prompt "..." --ferramenta "Antigravity (Nano Banana Pro)" --ref mestra.jpg`) |
| **3. Motor Local (`assets\gerar_imagem.py` · FLUX.2 klein 4B / SDXL / Flux / motor local)** | Autonomia 100% offline na máquina, controle exato de `--seed`, lotes rápidos, `img2img` com força controlada (`--init base.jpg --forca 0.25–0.55`) e `--ref` multi-referência | `python assets\gerar_imagem.py gerar "<prompt EN>" [--ref mestra.jpg] -a 4:5 -o "<IA>\<nome>.png"` |
| **4. Rota Híbrida (Cena por IA + Produto/Logo Real no SVG)** | Quando o produto, embalagem ou logo exige geometria 100% intocável: gera-se o cenário/luz/pessoa no melhor gerador (Antigravity/Nano Banana Pro ou local) e compõe-se o recorte real do produto + logo vetorial no SVG | Gerador para a cena + `<image>` e `<g id="Logo_Oficial">` no SVG |
| **5. Composição Vetorial e Canvas Autônomo** | Fundos abstratos, gradientes complexos, texturas, recortes, tratamento de cor e exportação WebP sem depender de softwares externos | SVG + `assets\img_qa.py` (autônomo via Chromium/Canvas) |
| **6. Upscale e Remasterização 4K** | Finalização em alta resolução (2× ou 4×) e reconstrução de microtexturas | Upscaler nativo da IDE ou `python assets\gerar_imagem.py upscale in.png -o out.png --escala 2|4` |

### 2. Como a Máquina Aprende (Memória Evolutiva de Geração)
A máquina constrói repertório próprio a cada execução para saber qual gerador funciona melhor para si em cada tipo de tarefa (retrato, packshot, 360, cenário arquitetônico, fundo):
1. **Leitura de performance passada:** antes de gerar, ler `## 2. O QUE FAZER` no `_DESIGN\design_system.md` (e `PRODUTO_*.md` / `PERSONAGEM_*.md` quando aplicável) para ver qual gerador (ex.: *Antigravity Nano Banana Pro* vs *FLUX.2 klein local* vs *Híbrido*), qual estrutura de prompt e quais parâmetros já tiveram aprovação direta.
2. **Adaptação imediata:** se um motor não estiver aberto/disponível na sessão ou se a 1ª geração apresentar desvio de anatomia, geometria ou textura, a máquina **troca automaticamente para outra opção do arsenal** na mesma resposta, sem travar e sem pedir permissão.
3. **Registro de aprendizado:** toda saída em `Compartilhada\Imagens\IA\AAAA-MM-DD_[solicitação]_[tema]_v[n].png` gera um `.txt` com `ferramenta`, `status` (`aprovado`/`descartado`), `referencias`, `notas` e `PROMPT`. Quando o usuário aprova a peça, a máquina grava em 1 linha no `design_system.md` a combinação vencedora (`[Tipo de cena] → melhor resultado com [Motor + parâmetros + estrutura]`), tornando-se mais rápida e precisa a cada pedido.

---

## Parte B · Engenharia de Prompt Fotorrealista, Packshot 3D, Retrato e Upscale

### 1. Fórmula e Decomposição Canônica do Prompt (sempre em inglês)
**Estrutura base (proporção 70/30):**
`[pessoa + ação] , [produto] identical to reference image 0 , [objetos do nicho] , [ambiente] , [luz] , 70 percent person and product, 30 percent environment , [estilo/câmera/lente/grão]`

- **Proporção de herói:** com pessoa + produto = `70 percent person and product, 30 percent environment`; só produto = `product fills 60 percent of frame, ample negative space for headline`.
- **Índice de referências:** `image 0` = mestra (melhor luz e nitidez), `image 1` = ângulo alvo, `image 2` = detalhe de textura/material.
- **Derivação automática do KV:** extrair de `_DESIGN\design_system.md` (sem perguntar ao usuário) a direção de luz/mood (`Foto · luz e tratamento`), perfil de pessoas (`Foto · pessoas`), paleta por papel e espaço negativo para a headline/logo.
- **Decomposição técnica fotorrealista (para cenas comerciais e editoriais de alta fidelidade):**
  - `scene`: ambiente real, contexto espacial e profundidade;
  - `hero`: sujeito/produto central, posição exata, acabamento de material (vidro, metal escovado, tecido, acrílico) e reflexos;
  - `lighting`: fonte, direção e temperatura (ex.: `softbox diffused lighting at 45 degrees, 5500K, clean contact shadows, no artificial fill`);
  - `camera & exposure`: câmera/lente e faixa dinâmica (ex.: `ARRI Alexa Mini LF, Zeiss 85mm T1.5, flat log exposure, natural saturation, subtle organic film grain`);
  - `avoid` (negativo): `text, letters, watermark, logo, signature, ui, app interface, phone mockup, status bar, buttons, plastic skin, airbrushed face, oversaturated, artificial HDR, deformed geometry, extra fingers, apple logo, patented device frames` + cores/formas proibidas do cliente.
- **Lei da tipografia/marca em IA:** texto, rótulo legível e logo **nunca** vêm da IA. Gerar a cena limpa e aplicar logo/rótulo real em vetor/camada no SVG ou Figma.
- **Modificadores rápidos:** `/input` referência inegociável (`--forca 0.25` no img2img) · `/pullout` plano aberto · `/wormsview` contra-plongée · `/floatingproduct` produto levitando · `/8k` `/besttexture` no acabamento/upscale.
- **Prompt Master (`/promptmaster`, sob pedido):** bloco enxuto derivado na hora do `design_system.md` para uso externo. Nunca salvar em arquivo.

### 2. Packshot 3D & Cena de Estúdio
- **Modo 1 · Estúdio novo:** pódios geométricos minimalistas ou acrílico translúcido, refrações cáusticas sutis, sombras de contato reais e amplo espaço negativo na zona do título (`Create a premium cinematic product photography scene. Preserve the exact shape, proportions, materials, colors and geometry of the reference product...`).
- **Modo 2 · Aplicação/substituição em cena aprovada:** manter o ambiente/cena base intacto (`--init` ou imagem base no Antigravity/IDE) e aplicar o produto da referência (`--ref`) com sombra de contato, reflexo de piso e temperatura de luz idênticos à cena (`Apply the reference product naturally into the scene preserving its exact geometry and materials, matching perspective, contact shadows and ambient lighting`).

### 3. Retrato Corporativo, Figurino e Telas Neutras
- **Preservação facial estrita (anti-embelezamento de IA):** manter 100% autênticos o formato dos olhos, expressão, rugas de expressão, microporos da pele e pelos faciais. Proibido `soft skin`, pele plastificada, filtro de rejuvenescimento, sorriso forçado ou alteração óssea.
- **Adaptação de figurino (alfaiataria):** quando pedido, substituir roupa casual por alfaiataria contemporânea (blazer/terno de corte moderno com trama de tecido visível, caimento e dobras naturais).
- **Dispositivos e telas neutras:** computadores, monitores e smartphones em cena devem ser genéricos e minimalistas — proibido exibir logotipos ou carcaças patenteadas (ex.: logo da Apple). Telas recebem conteúdo neutro ou gráfico vetorial no SVG.
- **Pôsteres de evento com múltiplos palestrantes:** disposição triangular canônica — speaker principal centralizado em primeiro plano (meio tronco para cima) e speakers secundários ligeiramente atrás à esquerda e à direita, com espaço negativo limpo para headline e data.

### 4. Upscale e Remasterização 4K UHD
- Reconstruir microtexturas (poros naturais, trama de linho/algodão/lã, reflexos metálicos, vidro), remover compressão/banding e preservar tons de pele.
- **Regra crítica em pessoas reais:** nunca ativar reconstrução facial generativa (`--rosto` / CodeFormer) sobre foto de pessoa real do cliente, pois reinventa traços faciais. Proibido alterar formato do rosto, proporções do corpo, logotipo ou geometria do produto.

---

## Parte C · Produto / Objeto Fiel por IA (Subject Reference + Turnaround 360)

Usado para aeronave, veículo, embalagem, máquina, imóvel ou peça que exige fidelidade exata ao exemplar real do cliente. Comandos: `produto`, `subject`, `twin`, `360`.

### 1. Organização e Regras de Ouro
- **Arquivos:** fotos reais em `[Cliente]\Compartilhada\Imagens\Originais\[Produto]\` (só leitura); dossiê em `[Cliente]\_DESIGN\Produtos\[Produto]\PRODUTO_[NOME].md`; referências tratadas em `[Cliente]\_DESIGN\Produtos\[Produto]\Referências\`.
- **Foto real primeiro:** se o briefing exigir "foto real", só usar IA com autorização explícita do usuário gravada no `design_system.md`.
- **Referência = exemplar DO CLIENTE:** modelo 3D externo ou foto de outro exemplar servem apenas como apoio de geometria, nunca como mestra (pintura, faixas, acabamentos e detalhes vêm exclusivamente das fotos reais do cliente). Nunca incluir matrícula, placa, número de série, marca d'água ou logo externo.

### 2. Construção do Padrão e Turnaround Sheet (uma vez por produto)
1. **Seleção de 4–8 vistas reais:** frontal (0°), ¾ frontal esq./dir. (45°), perfil lateral (90°), ¾ traseira, traseira, superior e 1–3 detalhes. **Mestra** = ¾ frontal com melhor luz e nitidez.
2. **Pacote `_ref` + Turnaround:** salvar cópias com 2048 px no lado maior (`_ref`) e montar `turnaround_[produto].jpg` (prancha em fundo neutro cinza claro com os ângulos canônicos, sombras de contato suaves e proporções idênticas).
3. **Geração de vista faltante:** se faltar um ângulo, gerar a partir da mestra + vista mais próxima no Antigravity (Nano Banana Pro) ou motor local (`Product turnaround view: exact same product as reference image 0 seen from <ângulo>, clean neutral studio cyclorama background, identical proportions and livery`), validar contra as fotos reais e marcar como `_gerada` (nunca vira mestra).
4. **Checklist de identidade + Regras corretivas + Descritor (EN):** numerar no `PRODUTO_[NOME].md` apenas o observável (silhueta, nº/forma de janelas ou aberturas, posição de motores/rodas/tampa, faixas e cores exatas, acabamento brilho/fosco, itens proibidos), adicionar regras curtas a cada erro detectado e fechar com o descritor em inglês + `"keep the object's shape, proportions, livery and details exactly as in the reference images; no text, no registration marks"`.

### 3. Execução e Verificação
- Enviar **mestra + vista do ângulo pedido + 1 detalhe** (3–4 imagens). Se a cena exigir precisão absoluta do produto sobre fundo real (ex.: hangar, estrada, bancada), testar tanto a geração integrada com referência (Nano Banana Pro / FLUX.2 klein) quanto a **Rota Híbrida** (gerar/usar o fundo e compor o produto no ângulo exato via SVG/Figma com sombra de contato e luz igualadas) — a máquina escolhe e aprende o que fica mais perfeito.
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
- Usar geradores com suporte a referência de imagem (Antigravity / Nano Banana Pro com até múltiplas referências de alta fidelidade, subagente da IDE, ou motor local com `--ref`, enviando mestra + ângulo mais próximo, 3–4 fotos). No prompt, descrever **apenas o que muda** (cenário, luz, pose, enquadramento) + repetir o descritor 1×. Nunca posicionar texto sobre o rosto.
- Comparar resultado × mestra item a item do checklist. Se desviar (máx. 3 tentativas): (1) reforçar regra corretiva no prompt; (2) usar referência mais limpa e no mesmo ângulo; (3) gerar a cena/corpo primeiro e fazer inpainting/edição localizada só na cabeça com a mestra.
- **Homologação inicial:** validar 3 cenas (frontal neutra, ¾ sorrindo, meio corpo sentado) no KV do cliente antes de liberar para produção em escala.
