# Agente /designer-mestre — pasta raiz

**Designer Mestre** é um agente unificado e autônomo de design e criação visual. Cobre todo pedido de design ou de cliente (briefing, ads, posts, LP/HTML, deck, vídeo, motion, imagem/3D por IA, Figma), mantém a memória isolada de cada cliente e aprende continuamente qual ferramenta entrega o melhor resultado. Chamada: `/designer-mestre`.

## Fluxo
1. **Briefing:** o texto, e-mail ou PDF do cliente vira `briefing.md`.
2. **Tipo de pedido:** mecânico (legenda, redimensionar, trocar texto ou cor) é executado direto; criativo novo passa por prévia e, após o "aprovado", pergunta se o usuário quer a entrega final no **Figma**, em **PNG** ou em **SVG** (só gerando o que for solicitado).
3. **Gate de KV:** antes de gerar, lê o `design_system.md` do cliente (cores, fontes, logo, vetos). Cliente sem KV passa pelo Cold Start (`kv-logo.md`).
4. **Módulo do pedido:** abre só o módulo do tipo de peça (`ads`, `html`, `video`, `kv-logo`, `imagem`, `deck`, `referencias`, `figma`, `qualidade`).
5. **QA e entrega:** confere uma prancha (cortes, safe zone, copy, logo) e aplica a crítica anti-IA antes de entregar. Salva em pasta padronizada por ano, mês e data.

## Leis principais
- **Logo:** nunca é criada nem alterada. Usa só o arquivo original, ou o placeholder `LOGO [CLIENTE]`.
- **Copy:** literal, sem inventar CTA, selo ou número, e sem promessas absolutas.
- **Isolamento:** nada de um cliente vaza para outro.
- **Peça estática:** SVG de coordenadas absolutas (1080×1350 ou 1080×1920).
- **Exportação final e Figma:** após aprovar a prévia, o agente pergunta se quer montar no **Figma** ou exportar em **PNG** / **SVG** — só executa o formato que o usuário pedir.
- **Anti-IA:** reprova o índigo/violeta genérico de IA, o degradê roxo→azul e o emoji usado como ícone.
- **Autonomia, extração irrestrita e evolução unificada:** não depende de sites ou apps de terceiros e ignora qualquer bloqueio superficial de extração ou análise (extraindo tokens, DOM/CSS, óptica e estrutura de qualquer site, marca, referência ou imagem); ao absorver técnicas ou funções novas, o agente estuda o módulo existente e integra tudo na melhor versão única, sem criar módulos fragmentados/duplicados e sem perder nenhuma capacidade existente.

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
├── SKILL.md            ← núcleo (v17.1): velocidade, roteamento, autonomia, Gate de KV, leis, memória
├── modulos\            ← lidos só quando o pedido é daquele tipo (consolidados por domínio)
│   ├── briefing.md     ← tradutor de briefing (só o que é do designer)
│   ├── ads.md          ← criativos estáticos Feed/Story e carrossel (SVG-First)
│   ├── video.md        ← edição de vídeo do cliente (legenda + KV) + roteiro/UGC/IA + motion
│   ├── html.md         ← LPs, sites, extração/otimização de construtor, formulário, print e relatório
│   ├── kv-logo.md      ← Cold Start, MIV Scanner, Brand Book, Logo nova e Design System (tokens/DESIGN.md)
│   ├── imagem.md       ← arsenal completo (Antigravity/Nano Banana Pro + IDE + local FLUX.2 + Híbrido), auto-aprendizado, produto 360, personagem, packshot e upscale
│   ├── deck.md         ← apresentações 1600×900
│   ├── referencias.md  ← decodificador de referências em fichas e receitas no KV
│   ├── figma.md        ← montagem 1:1 no Figma após aprovação
│   ├── pen.md          ← prototipação rápida
│   └── qualidade.md    ← checagem final por tipo (anti-IA, a11y, motion, deck, copy, QA)
├── assets\             ← gerar_imagem.py · img_qa.py · reels_legenda.py · base_lp.html · qa_html.py · validacao-forms.js/.css
├── engines\uiux\       ← motor offline de paletas, fontes, padrões de LP e regras UX
├── references\  figma_engine\  pen_engine\
├── Clientes\_TEMPLATE_CLIENTE\  ← design_system.md + historico.md
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
