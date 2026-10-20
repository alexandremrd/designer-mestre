# Agente /designer-mestre — pasta raiz

**Designer Mestre** é um agente unificado de design e criação visual. Cobre todo pedido de design ou de cliente (briefing, ads, posts, LP/HTML, deck, vídeo, motion, imagem/3D por IA, Figma) e mantém a memória isolada de cada cliente. Chamada: `/designer-mestre`.

## Fluxo
1. **Briefing:** o texto, e-mail ou PDF do cliente vira `briefing.md`.
2. **Tipo de pedido:** mecânico (legenda, redimensionar, trocar texto ou cor) é executado direto; criativo novo passa por prévia, espera o "aprovado" e só então vai para o Figma.
3. **Gate de KV:** antes de gerar, lê o `design_system.md` do cliente (cores, fontes, logo, vetos). Cliente sem KV passa pelo Cold Start (`kv-logo.md`).
4. **Módulo do pedido:** abre só o módulo do tipo de peça (`ads`, `html`, `video`, `kv-logo`, `imagem`, `deck`, `referencias`, `figma`, `qualidade`).
5. **QA e entrega:** confere uma prancha (cortes, safe zone, copy, logo) e aplica a crítica anti-IA antes de entregar. Salva em pasta padronizada por ano, mês e data.

## Leis principais
- **Logo:** nunca é criada nem alterada. Usa só o arquivo original, ou o placeholder `LOGO [CLIENTE]`.
- **Copy:** literal, sem inventar CTA, selo ou número, e sem promessas absolutas.
- **Isolamento:** nada de um cliente vaza para outro.
- **Peça estática:** SVG de coordenadas absolutas (1080×1350 ou 1080×1920).
- **Figma:** só depois do "aprovado".
- **Anti-IA:** reprova o índigo/violeta genérico de IA, o degradê roxo→azul e o emoji usado como ícone.
- **Evolução unificada:** ao absorver técnicas ou funções novas, o agente estuda o módulo existente e integra tudo na melhor versão única, sem criar módulos fragmentados/duplicados (salvo quando a separação economizar tokens) e sem perder nenhuma capacidade existente.

## Memória e ferramentas
- **Memória por cliente:** `D:\Clientes\[Cliente]\_DESIGN\` (`design_system.md` e `historico.md`). Cada erro ou aprovação é gravado uma vez, no fim do trabalho.
- **Geração de imagem:** a IDE escolhe livremente o melhor gerador disponível para o caso (ferramenta/subagente nativo da IDE ou motor local via `assets\gerar_imagem.py`), mantendo todas as regras de fidelidade e registro em `Imagens\IA\`.
- **QA de imagem:** `assets\img_qa.py` (ImageMagick).
- **Vídeo e legenda:** `assets\reels_legenda.py` (Whisper + ffmpeg).
- **Motor UI/UX:** `engines\uiux` (paletas, fontes e padrões de landing page).

## Onde fica o agente
O agente pode ser salvo em qualquer pasta (`<PASTA_DO_AGENTE>`). A cópia editada na pasta raiz é a fonte; depois de alterar, rode `INSTALAR_DESIGN_CLAUDE_CODE.cmd` para sincronizar nas ferramentas. As alterações sobrescrevem os arquivos, sem backups duplicados.

## Estrutura

```text
<PASTA_DO_AGENTE>\
├── SKILL.md            ← núcleo (v17): velocidade, roteamento, onde rodar, Gate de KV, leis, memória
├── modulos\            ← lidos só quando o pedido é daquele tipo (consolidados por domínio)
│   ├── briefing.md     ← tradutor de briefing (só o que é do designer)
│   ├── ads.md          ← criativos estáticos Feed/Story e carrossel (SVG-First)
│   ├── video.md        ← edição de vídeo do cliente (legenda + KV) + roteiro/UGC/IA + motion (Remotion)
│   ├── html.md         ← LPs, sites, extração/otimização de construtor, formulário, print e relatório
│   ├── kv-logo.md      ← Cold Start, MIV Scanner, Brand Book, Logo nova e Design System (tokens/DESIGN.md)
│   ├── imagem.md       ← geração (IDE ou local), produto fiel 360, personagem/rosto, packshot e upscale
│   ├── deck.md         ← apresentações 1600×900
│   ├── referencias.md  ← decodificador de referências em fichas e receitas no KV
│   ├── figma.md        ← montagem 1:1 no Figma após aprovação
│   ├── pen.md          ← prototipação rápida via pen.dev
│   └── qualidade.md    ← checagem final por tipo (anti-IA, a11y, motion, deck, copy, QA)
├── assets\             ← gerar_imagem.py · img_qa.py · reels_legenda.py · base_lp.html · qa_html.py · validacao-forms.js/.css
├── engines\uiux\       ← motor offline de paletas, fontes, padrões de LP e regras UX
├── references\  figma_engine\  pen_engine\
├── Clientes\_TEMPLATE_CLIENTE\  ← design_system.md + historico.md
└── INSTALAR_DESIGN_CLAUDE_CODE.cmd
```

A memória de cada cliente fica em `D:\Clientes\[Cliente]\_DESIGN\` (`design_system.md` + `historico.md` + `templates\`). Nada de cliente mora nesta pasta.

## Requisitos opcionais no PC
- **Imagem e QA local:** ImageMagick 7 (`winget install ImageMagick.ImageMagick`) e, para geração offline, Easy Diffusion com motor v4.
- **Vídeo e legenda:** `ffmpeg` (`winget install Gyan.FFmpeg`), Python 3.10+ e `faster-whisper`.

## Como alterar
1. Pedir a mudança ("atualiza o /designer-mestre: ...").
2. O agente sobrescreve o arquivo aqui e registra no Changelog.
3. Rodar `INSTALAR_DESIGN_CLAUDE_CODE.cmd`.

Só regras universais entram aqui. Preferência de cliente vai no `design_system.md` dele.

## Changelog
- v9–v15: prévia aprovada antes do Figma; versão única sem backups; Fast-Track de KV + `design_system.md` único + SVG-First; núcleo enxuto; pedido mecânico vs criativo novo; legenda por palavra no KV (`reels_legenda.py`); dossiê de produto 360 e fichas de referências; scripts `gerar_imagem.py` e `img_qa.py`; tradutor de briefing (`briefing.md`).
- v16 (20/10/2026): **renomeado para Designer Mestre** (`/designer-mestre`); nome pessoal removido de todos os arquivos; caminhos fixos trocados por `<PASTA_DO_AGENTE>`.
- v16.1 (20/10/2026): **otimização universal de LPs extraídas e descrição da skill** — regras universais para LPs de construtor (unificação de CTAs pelo maior peso tipográfico com seta lateral interna e hover consistente na cor de ação; escala fluida entre breakpoints com respiro lateral simétrico e sem cortes de texto; centralização e padding interno simétrico de 24 px nos 4 lados para formulários sobre caixa/card de fundo no mobile). `SKILL.md`: `description` atualizada com o resumo claro do agente/skill.
- v17 (20/10/2026): **consolidação de módulos, escolha livre de gerador de imagem pela IDE e padronização de `Referências\`** — módulos de mesmo domínio fundidos sem perda de conteúdo (`video-edicao` + `video` + `motion` → `video.md`; `html` + `html-lp` + `html-form` + `html-print` + `html-relatorio` → `html.md`; `cold-start` + `kv-logo` + `design-system` → `kv-logo.md`; `imagem` + `produto` + `personagem` → `imagem.md`); removidos créditos/referências de terceiros e adicionada diretiva interna de soberania e evolução unificada; removidas travas de gerador único em `imagem.md` (a IDE escolhe o melhor gerador mantendo todas as regras); pasta `Referencias\` padronizada com acento (`Referências\`) em todos os arquivos e clientes.
