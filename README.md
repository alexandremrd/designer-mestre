# Designer Mestre (`/designer-mestre`)

O **Designer Mestre** é um assistente completo de criação visual. Ele recebe o seu pedido ou briefing, consulta e extrai a identidade visual, referências e conteúdos diretamente do seu site e redes sociais (cores, fontes e logotipo) e gera anúncios, páginas web, apresentações, vídeos com legenda ou imagens hiper-realistas por inteligência artificial. Você sempre visualiza uma prévia antes, aprova o resultado e escolhe se quer o arquivo final pronto para uso ou montado no Figma. Além disso, ele grava tudo o que você aprovou ou reprovou para manter o padrão e nunca repetir erros.

## Como instalar sem complicação

Para instalar, baixe o projeto pelo botão verde **Code > Download ZIP** no GitHub e extraia a pasta no seu computador. Abra a pasta descompactada e dê **dois cliques no arquivo `Instalador.cmd`**. Ele configura tudo sozinho em poucos segundos. Ao terminar, abra o seu assistente de inteligência artificial e comece a usar digitando `/designer-mestre`.

## Visão geral técnica

**Designer Mestre** é um agente unificado e autônomo de design e criação visual. Cobre todo pedido de design ou de cliente (briefing, ads, posts, LP/HTML, deck, vídeo, motion, imagem/3D por IA, Figma), mantém a memória isolada de cada cliente e aprende continuamente qual ferramenta entrega o melhor resultado. Chamada: `/designer-mestre`.

## Fluxo
1. **Briefing:** o texto, e-mail ou PDF do cliente vira `briefing.md`.
2. **Tipo de pedido:** mecânico (legenda, redimensionar, trocar texto ou cor) é executado direto; criativo novo passa por prévia e, após o "aprovado", pergunta se o usuário quer a entrega final no **Figma**, em **PNG** ou em **SVG** (só gerando o que for solicitado).
3. **Gate de KV:** antes de gerar, lê o `design_system.md` do cliente (cores, fontes, logo, vetos). Cliente sem KV passa pelo Cold Start (`kv-logo.md`).
4. **Módulo do pedido:** abre só o módulo da rota (e o anexo, quando a rota pede); dentro dele, só a Parte do pedido.
5. **QA e entrega:** confere uma prancha (cortes, safe zone, copy, logo) e aplica a crítica anti-IA antes de entregar. Salva em pasta padronizada por ano, mês e data.

## Leis principais
- **Logo:** nunca é criada nem alterada. Usa só o arquivo original, ou o placeholder `LOGO [CLIENTE]`.
- **Copy:** literal, sem inventar CTA, selo ou número, e sem promessas absolutas.
- **Isolamento:** nada de um cliente vaza para outro.
- **Peça estática:** SVG de coordenadas absolutas (1080×1350 ou 1080×1920).
- **Exportação final e Figma:** após aprovar a prévia, o agente pergunta se quer montar no **Figma** ou exportar em **PNG** / **SVG** — só executa o formato que o usuário pedir.
- **Anti-IA:** reprova o índigo/violeta genérico de IA, o degradê roxo→azul e o emoji usado como ícone.
- **Fontes e direitos:** extrai só o que é acessível (DOM renderizado, CSS computado, arquivos enviados); bloqueio = pede HTML salvo ou print. Referência de terceiros transfere técnica, nunca identidade. Código absorvido mantém a licença original.
- **Evolução unificada:** regra nova substitui a antiga no módulo dono do tema; valor usado por 2+ módulos mora nos Padrões `U1–U8` do núcleo.

## Memória, motores autônomos e auto-aprendizado
- **Memória por cliente:** `D:\Clientes\[Cliente]\_DESIGN\` (`design_system.md` e `historico.md`). Cada erro, aprovação e receita vencedora é gravado uma vez, no fim do trabalho.
- **Geração de imagem (arsenal completo + adaptadores de física + aprendizado da máquina):** inclui **Antigravity (Nano Banana Pro)**, subagente `image-generator` / geradores nativos da IDE, **motor local** (`assets\gerar_imagem.py` com FLUX.2 klein 4B / SDXL / Flux), motores multimodais estruturados e **Rota Híbrida** (cena gerada + produto/logo real em SVG com física de sombra de contato). A máquina adapta a gramática do prompt à física de cada modelo e aprende qual opção é a melhor para si em cada tarefa, registrando tudo em `Imagens\IA\`.
- **QA de imagem autônomo:** `assets\img_qa.py` (prancha, paridade RMSE, paleta, contraste WCAG, trim de bbox e conversão WebP rodando direto no motor interno Chromium/Canvas, sem depender de softwares externos).
- **Vídeo e legenda autônomo:** `assets\reels_legenda.py` (sincronização palavra a palavra, legenda queimada no KV, corte de pausas, overlay e áudio normalizado).
- **Motor offline UI/UX & 84 Brand Design Systems:** `engines\uiux` (paletas, fontes, padrões de landing page e 84 sistemas de design completos de marcas globais consultáveis 100% offline via `--domain brand` e `--brand <slug>`).

## Onde fica o agente
O agente pode ser salvo em qualquer pasta (`<PASTA_DO_AGENTE>`). A cópia editada na pasta raiz é a fonte; depois de alterar, rode `Instalador.cmd` para localizar todas as IDEs do computador e sincronizar a skill automaticamente. **Nota de economia de tokens:** o arquivo `Instalador.cmd` é exclusivamente para instalação — o agente nunca deve abri-lo ou analisá-lo em sessões. As alterações sobrescrevem os arquivos, sem backups duplicados.

## Estrutura

```text
<PASTA_DO_AGENTE>\
├── SKILL.md            ← núcleo (v19): carga mínima, rotas, ciclo de entrega, Gate de KV, leis hierárquicas, padrões U1–U8, memória
├── modulos\            ← lidos só quando o pedido é daquele tipo (consolidados por domínio)
│   ├── briefing.md     ← tradutor de briefing (só o que é do designer)
│   ├── ads.md          ← criativos estáticos Feed/Story e carrossel (SVG-First)
│   ├── video.md        ← edição de vídeo do cliente (legenda + KV) + roteiro/UGC/IA + motion
│   ├── html.md         ← LP/site novo, ajuste, formulário, SEO, a11y, QA
│   ├── html-extrair.md ← anexo: clonar/otimizar construtor, embed `</>`, recriar de print
│   ├── html-relatorio.md ← anexo: página-relatório
│   ├── kv-logo.md      ← Cold Start, MIV Scanner, Brand Book, Logo nova e Design System (tokens/DESIGN.md)
│   ├── imagem.md       ← arsenal, prompt por motor, fotografia, compositing, Vision Decomposer, Pass³
│   ├── imagem-produto.md ← anexo: produto fiel / 360 / turnaround
│   ├── imagem-personagem.md ← anexo: rosto recorrente
│   ├── deck.md         ← apresentações 1600×900
│   ├── referencias.md  ← decodificador de referências em fichas e receitas no KV
│   ├── figma.md        ← montagem 1:1 no Figma após aprovação
│   ├── pen.md          ← prototipação rápida (absorveu `pen_engine\SKILL.md`)
│   └── qualidade.md    ← checagem final por tipo (anti-IA, a11y, motion, deck, copy, QA)
├── assets\             ← gerar_imagem.py · img_qa.py · reels_legenda.py · base_lp.html · qa_html.py · validacao-forms.js/.css · base_deck.html · validate_deck.py
├── engines\uiux\       ← motor offline de paletas, fontes, padrões de LP e regras UX
├── references\  figma_engine\
├── Clientes\_TEMPLATE_CLIENTE\  ← design_system.md + historico.md
├── NOTICE.md           ← avisos de licença de terceiros (conformidade; não lido pelo agente)
└── Instalador.cmd      ← instalador universal para todas as IDEs (não analisar)
```

A memória de cada cliente fica em `D:\Clientes\[Cliente]\_DESIGN\` (`design_system.md` + `historico.md` + `templates\`). Nada de cliente mora nesta pasta.

## Como alterar
1. Pedir a mudança ("atualiza o /designer-mestre: ...").
2. O agente sobrescreve o arquivo aqui e registra no Changelog.
3. Rodar `Instalador.cmd`.

Só regras universais entram aqui. Preferência de cliente vai no `design_system.md` dele.

## Changelog
- v9–v15: prévia aprovada antes do Figma; versão única sem backups; Fast-Track de KV + `design_system.md` único + SVG-First; núcleo enxuto; pedido mecânico vs criativo novo; legenda por palavra no KV (`reels_legenda.py`); dossiê de produto 360 e fichas de referências; scripts `gerar_imagem.py` e `img_qa.py`; tradutor de briefing (`briefing.md`).
- v16 (20/10/2026): **renomeado para Designer Mestre** (`/designer-mestre`); nome pessoal removido de todos os arquivos; caminhos fixos trocados por `<PASTA_DO_AGENTE>`.
- v16.1 (20/10/2026): **otimização universal de LPs extraídas e descrição da skill** — regras universais para LPs de construtor (unificação de CTAs pelo maior peso tipográfico com seta lateral interna e hover consistente na cor de ação; escala fluida entre breakpoints com respiro lateral simétrico e sem cortes de texto; centralização e padding interno simétrico de 24 px nos 4 lados para formulários sobre caixa/card de fundo no mobile). `SKILL.md`: `description` atualizada com o resumo claro do agente/skill.
- v17 (20/10/2026): **consolidação de módulos e padronização de `Referências\`** — módulos de mesmo domínio fundidos sem perda de conteúdo (`video.md`, `html.md`, `kv-logo.md`, `imagem.md`); removidos créditos/referências de terceiros e adicionada diretiva interna de soberania e evolução unificada; pasta `Referencias\` padronizada com acento (`Referências\`) em todos os arquivos e clientes.
- v17.1 (20/10/2026): **autonomia total sem dependência de apps/sites de terceiros, arsenal completo de imagem com auto-aprendizado e exportação final sob escolha** — `imagem.md`, `SKILL.md` e `README.md` mantêm todas as opções ativas (Antigravity / Nano Banana Pro, subagente `image-generator` / nativo da IDE, motor local FLUX.2 klein 4B / SDXL / Flux e Rota Híbrida IA+SVG) com ciclo de aprendizado contínuo onde a máquina descobre e registra qual gerador é melhor para si em cada tarefa; `assets\img_qa.py` reescrito para rodar 100% autônomo via Chromium/Canvas; exportação final após aprovação não força o Figma (pergunta sempre se quer Figma, PNG ou SVG e só gera o que for solicitado).
- v17.2 (20/10/2026): **atalhos técnicos de Product Turnaround Sheet 360 (`360`, `turnaround`, `multiview`, `manual 360`) + pesquisa web automática de especificações geométricas + lei anti-corte e Endcard rico em `ads.md`** — proibido recortar imagens em tiras estreitas/espremidas e proibido último slide de carrossel vazio apenas com logo e CTA em fundo liso.
- v18.0 (20/10/2026): **absorção unificada de motores de Direção de Arte, 84 Brand Design Systems reais, Adaptadores de Física por Modelo de IA, Fotografia Comercial, Manipulação Física, Vision Decomposer, Taste Engine, Dramaturgia de Vídeo e Taxonomia Anti-Slop** — (1) 84 sistemas de design reais integrados em `engines\uiux\data\brands.csv` e `design_md\` (`--domain brand` e `--brand <slug>`), com Escada de Superfícies de 4 níveis (`Surface Ladder`), Lei de Polaridade de Tracking Tipográfico e 9 seções canônicas de `DESIGN.md` em `kv-logo.md` e `html.md`; (2) Direção de Arte Publicitária (`Insight → Tensão → Proposição Visual`, 16 Territórios Criativos, ideação estrutural SIT/Bisociação/Inversão, Ponto Focal Único e 3 testes de Preflight Perceptivo: Miniatura 100×100, Escala de Cinza e Zero Tangências Acidentais) em `ads.md`; (3) Adaptadores de Física por Modelo (prosa natural sem números secos de câmera + Spatial JSON + 14 refs no Nano Banana Pro; 70/30 + SLCT óptico no FLUX.2 local; 5-Slot + World Knowledge Anchors + Edição Atômica `Change/Preserve/Constraints`), 5 Leis de Prevenção de Alucinação, Física de Fotografia Comercial (luz de 3 pontos 2:1 vs 8:1, melanina fiel, materiais/anisotropia/SSS/cáusticas), Manipulação Física (AO + Cast Shadow + Color Bounce + Fresnel + Light Wrap), Panter Mode, Vision Decomposer e Teste Pass³ em `imagem.md`; (4) Pipeline Taste Engine em 4 etapas e Mixagem de Referências por Função Exclusiva em `referencias.md`; (5) Dramaturgia Cinematográfica (Fórmula de Cena, 3 Detalhes Físicos, Regra dos 6 de Murch, 12 movimentos/6 ângulos e física por motor Veo/Kling/Seedance/Sora/Hailuo) em `video.md`; (6) Taxonomia das 10 Famílias de AI Slop e Ordem Cirúrgica de Subtração em `qualidade.md`; (7) Extração e análise irrestrita sem bloqueios em todo o agente.
- v18.1 (20/10/2026): **consolidação total da Memória de Engenharia, Apresentações HTML (`1600×900`), Brand Book 14 páginas, Extrator de Embed Blindado, Ads Patterns, Vídeo Sprint/UGC/Motion, Figma Console Export e Auditoria Cirúrgica** — (1) `deck.md`: viewport fixo `1600×900` com escala canônica `visualViewport`, 12 arquétipos semânticos (incluindo `Hub & Network` com classes posicionais `node-nw..node-s` e `node-float`), cadência de 4 fundos (Light + adaptação 100% Dark Mode), higiene tipográfica e QA em 4 viewports; (2) `html.md`: extrator de componentes `/embed` com 10 regras invioláveis, escopo CSS/IIFE, correção de modal no `<body>` e marquee full-bleed (`#b_xxx` vs `.e_xxx`), gate de qualificação B2B, estabilidade mobile-first de formulários e ordem de decisão de 5 passos para HTML de apresentação; (3) `kv-logo.md`: arquitetura completa de Brand Book 16:9 em 14 páginas (`cqi`, grids `5/7` e `4/8`, seção `2.10` de usos incorretos da logo em CSS); (4) `ads.md`: 7 padrões canônicos de varredura ocular, 70–90% de engajamento de canvas e matemática de proporção de logo (15–20% L, 10–15% A); (5) `imagem.md`: regras anti-contaminação de fundo, schema JSONL de 9 chaves, geometria multi-view (`30° FOV`, azimutes `30°..330°`, elevações `20°/-10°`, normal/depth matting) e modo `Apply/Replace`; (6) `video.md`: Sprint 30s/15s em 5 blocos com 3 ganchos (Dor/Curiosidade/Oferta), parâmetros vocais PT-BR, mixagem `-6/-18/-12 dB`, 7 pilares de UGC realista, anatomia cinematográfica em 10 elementos e física spring (`damping: 12, stiffness: 150, mass: 0.5`); (7) `figma.md`: execução JS em lote, socket de 42 ferramentas e script autônomo de Console para criar `PaintStyles`, `TextStyles`, `EffectStyles` e `Variables` (`Light`/`Dark`); (8) `SKILL.md` e `qualidade.md`: cirurgia de código (menor mudança completa, causa-raiz), injeção de regras em subagentes, auditoria de código em 6 eixos (`Bug · Risk · Scale · Missing Check · Speed · Lean`) e remoção total de arquivos redundantes e menções de terceiros.
- v19 (20/10/2026): **núcleo enxuto (carga mínima por rota), anexos sob demanda, pen_engine integrado, figma_engine/ENGINE.md desindexado de skills isoladas e precisão de coordenada de legenda Reels (--y = base <= 1470)**.
- v19 (detalhe): **reestruturação lógica e de tokens** — núcleo com carga mínima (lista do que nunca abrir; ferramenta ausente = pula sem anunciar), tabela de rotas com anexos sob demanda, ciclo de entrega único (mecânico × criativo, formato final, teto de iteração 1 mutação/3 passes), leis fundidas com a hierarquia de autoridade, Padrões universais `U1–U8` como fonte única (contraste, safe zone, tipografia/tracking, superfícies 4 níveis, espaço/viewports, P0, crítica, prancha); `html.md` e `imagem.md` divididos em anexos (`html-extrair`, `html-relatorio`, `imagem-produto`, `imagem-personagem`); `qualidade.md`, `ads.md`, `kv-logo.md` citam `U#` em vez de repetir valores; divergências corrigidas (escala 1.333→1.25, eyebrow +0.10→+0.12em, surface-4 no `DESIGN.md`, mixagem dB×LUFS); `pen_engine` absorvido em `pen.md`; removidas as diretivas de contornar bloqueio/403 e de apagar créditos/licenças (substituídas pela §6 Fontes e direitos).
- v19.1 (20/10/2026): **reauditoria das fontes (ui-ux-pro-max, awesome-design-md, pasta Memória)** — motor `engines\uiux` e 84 `DESIGN.md` conferidos contra o upstream (íntegros); créditos de terceiros só no `NOTICE.md` discreto, nunca nas entregas, crédito visível apenas quando a licença exigir (§6); novos `assets\base_deck.html` e `assets\validate_deck.py` (QA estático de deck); lacunas integradas de forma condensada: formatos de banner/display/impressão e pisos tipográficos (`ads.md`), proteção e tamanho mínimo de logo (lei 3), foco/justificado/dark tonal (U1/U3/U4), erros de formulário e uso da lib IBGE/MX existente (`html.md`), marquee/iframe/print (`html-extrair.md`), status, cards e gráficos SVG (`html-relatorio.md`), chrome e paginação do brand book, testes e entrega de logo nova, 3 camadas de token (`kv-logo.md`), sequências UGC, claims e motores Runway/Luma/Pika, aviso de licença Remotion (`video.md`), transparência e lote (`imagem.md`), motion e prova de código (`qualidade.md`).
- v19.2 (20/10/2026): **matriz de eficiência de modelos na IDE** — diretrizes no núcleo (§0.8) e documentação: Sonnet 5/4.6 como padrão para 80% do fluxo (código, SVG, HTML, Figma, Decks); Haiku 5.5/4.5 para tarefas mecânicas, legendas e leitura rápida; Opus 5.5/5 para Brand Books 14p, Design Systems do zero e ideação estrutural; contraindicação do Opus 3 legado.
- v19.3 (20/10/2026): **`html.md` — CTA interno confiável em builders e teto de caracteres por versão** — (1) nova falha catalogada: CTA (`.link_interno`) que não rola até o alvo porque um script externo (GTM/tracking) intercepta o clique lendo `data-bloco`/`data-bloco-mobile` e ignora o `href`; regra: sincronizar os dois atributos no mesmo id e reforçar com JS próprio em capture (`preventDefault` + `scrollIntoView`), testando com clique real (hit-test) nos 3 breakpoints; (2) teto de caracteres de importação do construtor não é fixo entre versões (uma versão nova pode aceitar menos que a anterior) — em qualquer `Ajuste` perto do limite, todo JS/CSS novo entra minificado e o tamanho final é conferido antes de reentregar; teto real descoberto vai para o `design_system.md` do cliente. Origem: ajuste de LP do cliente Alabastro Vasos (botões do formulário MQL + recusa de importação do V4 Page Builder).

## Eficiência de Modelos na IDE (Claude / Anthropic)
- **Sonnet 5 / 4.6 (Padrão Recomendado — 80% do dia a dia):** criação de anúncios estáticos em SVG (Feed/Stories/carrossel), landing pages e sites em HTML único blindado, formulários e embeds, apresentações em HTML 1600×900, automações no Figma e geração de código frontend. Equilíbrio ótimo entre obediência estrita às leis do KV, rigor geométrico e velocidade.
- **Haiku 5.5 / 4.5 (Tarefas Mecânicas e Baixo Consumo):** ajustes pontuais rápidos (trocar texto/cor em SVG pronto, redimensionamentos mecânicos), legendagem e cortes de vídeo (`reels_legenda.py`), QA de contraste/bbox e subagentes leves de leitura.
- **Opus 5.5 / 5 (Direção de Arte Pesada e Concepção):** Cold Start de clientes novos, criação de Design Systems e Brand Books de 14 páginas do zero (`kv-logo.md`), ideação publicitária complexa (16 territórios) e análise densa de manuais de marca de 50+ páginas. *(Nota: evitar o modelo legado Opus 3, por ser consideravelmente mais lento e ter menor precisão de código frontend do que o Sonnet 5).*
- v19.1 (20/10/2026): Prévia visível obrigatória (§2) e subagente só devolve caminhos; árvore única de imagens `Imagens\{Originais, Banco de Imagens, Tratadas, IA}` (Lei 5) + trava de destino no `gerar_imagem.py`; `imagem-produto.md`: curadoria da mestra, fundo neutro na referência 360 (também personagem), mestra provisória `_gerada`, inventário de interior; `imagem.md` Parte C (imagem publicitária/hero); template de cliente com `Tratadas\` e pastas de Produtos/Personagens; novo `EVOLUCAO.md` (memória do agente, lido só ao alterá-lo).
