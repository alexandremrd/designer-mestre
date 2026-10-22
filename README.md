# Designer Mestre (`/designer-mestre`)

O **Designer Mestre** é uma skill para produção de entregáveis visuais ligados a uma marca. Quando o pedido exige, pode analisar materiais fornecidos e fontes públicas acessíveis para extrair posicionamento, identidade e referências; cria anúncios, páginas, apresentações, vídeos ou imagens conforme o pedido e as ferramentas disponíveis na sessão. A prévia visual é entregue para peças com saída visual; aprovação prévia só é aguardada quando o usuário pede seleção ou quando uma decisão altera materialmente identidade, copy ou custo externo. A memória é específica do cliente e depende dos arquivos e do feedback disponíveis: não há aprendizado autônomo entre sessões.

## Como instalar sem complicação

Para instalar ou atualizar no Windows, extraia o repositório inteiro e confirme que `Instalador.cmd` e `Instalador.ps1` estão juntos. A v19.23 publicada estava sem o arquivo `.ps1` exigido pelo `.cmd`; a v19.25 o inclui. Execute `Instalador.cmd`, confira os destinos que ele listar e só então confirme a sincronização. O instalador preserva arquivos extras e verifica SHA-256. Reinicie/recarregue a IDE para ela descobrir a skill; destinos opcionais dependem do ambiente.

## Visão geral técnica

**Designer Mestre** é uma skill de criação visual. No Cold Start ou quando solicitado, analisa fontes acessíveis de site, Instagram, briefing e criativos, separando evidência de inferência; compara concorrentes quando isso for pertinente e mantém a memória isolada por cliente. Cobre ads, posts, LP/HTML, deck, vídeo, motion, imagem/3D e Figma, conforme ferramentas efetivamente disponíveis. Chamada: `/designer-mestre`.

## Fluxo
1. **Briefing:** texto, e-mail ou PDF longo pode ser organizado em `briefing.md` quando a tarefa exigir.
2. **Tipo de pedido:** ajustes mecânicos são executados diretamente; peça estática diagramada nova sai em SVG e PNG com prévia. Figma entra quando estiver disponível e for solicitado.
3. **Gate de KV:** antes de gerar, lê o `design_system.md` do cliente (cores, fontes, logo, vetos). Cliente sem KV passa pelo Cold Start (`kv-logo.md`).
4. **Módulo do pedido:** abre só o módulo da rota (e o anexo, quando a rota pede); dentro dele, só a Parte do pedido.
5. **QA e entrega:** confere a prancha e aspectos pertinentes (cortes, safe zone, copy, logo, coerência com a ideia e o KV), corrigindo problemas concretos sem blacklist estética universal. Salva em pasta padronizada por ano, mês e data quando o fluxo de arquivos estiver disponível.

No Cold Start, distingue observação de inferência, registra fontes e datas, mapeia códigos visuais e verbais e transforma achados em posicionamento, provas, lacunas e oportunidades criativas. Scraping/serviços externos são opcionais; não instala dependências nem inicia coleta paga automaticamente.

## Leis principais
- **Logo:** nunca é criada nem alterada. Usa só o arquivo original, ou o placeholder `LOGO [CLIENTE]`.
- **Copy:** literal, sem inventar CTA, selo ou número, e sem promessas absolutas.
- **Isolamento:** nada de um cliente vaza para outro.
- **Peça estática:** SVG de coordenadas absolutas (1080×1350 ou 1080×1920).
- **Exportação final e Figma:** peça estática diagramada é entregue em SVG e PNG sem nova escolha de formato enquanto o Figma estiver indisponível; Figma é opcional quando voltar.
- **Direção visual:** escolhas são julgadas pelo papel na ideia, no KV e na legibilidade; cor intensa, gradientes, texturas e recursos expressivos não são vetados por si.
- **Fontes e direitos:** extrai só o que é acessível (DOM renderizado, CSS computado, arquivos enviados); bloqueio = pede HTML salvo ou print. Referência de terceiros transfere técnica, nunca identidade. Código absorvido mantém a licença original.
- **Evolução unificada:** regra nova substitui a antiga no módulo dono do tema; valor usado por 2+ módulos mora nos Padrões `U1–U10` do núcleo.

## Memória e ferramentas disponíveis
- **Memória por cliente:** `D:\Clientes\[Cliente]\_DESIGN\` (`design_system.md` e `historico.md`). Registre apenas conhecimento durável e feedback efetivamente recebido; não presuma aprovação, reprovação ou aprendizado automático.
- **Geração de imagem:** os módulos documentam adaptadores e opções de motor, incluindo motores locais e integrados quando instalados e disponíveis. A skill não garante acesso a um modelo ou execução de geração em toda sessão.
- **QA de imagem:** `assets\img_qa.py` oferece operações como prancha, paridade RMSE, paleta, contraste WCAG, trim de bbox e conversão WebP; cada operação depende dos requisitos e do runtime disponível.
- **Vídeo e legenda:** `assets\reels_legenda.py` oferece sincronização de legenda, cortes e tratamentos descritos no módulo; valide dependências e disponibilidade antes de prometer execução.
- **Motor offline UI/UX e 84 Design Systems:** `engines\uiux` inclui coleções locais consultáveis por `--domain brand` e `--brand <slug>`, sem substituir o KV validado do cliente.

## Onde fica o agente
O agente pode ser salvo em qualquer pasta (`<PASTA_DO_AGENTE>`). A cópia editada na pasta raiz é a fonte; **após aprovação da versão**, rode `Instalador.cmd` para localizar as IDEs do computador e sincronizar a skill. **Nota de economia de tokens:** o arquivo `Instalador.cmd` é exclusivamente para instalação — o agente nunca deve abri-lo ou analisá-lo em sessões. As alterações sobrescrevem os arquivos, sem backups duplicados.

## Estrutura

```text
<PASTA_DO_AGENTE>\
├── SKILL.md            ← núcleo (v19): carga mínima, rotas, ciclo de entrega, Gate de KV, leis hierárquicas, padrões U1–U10, memória
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
3. Manter a revisão só na fonte até aprovação explícita; então rodar `Instalador.cmd` e conferir as cópias instaladas.

Só regras universais entram aqui. Preferência de cliente vai no `design_system.md` dele.

## Changelog
- v19.25 (22/10/2026): decodificação de KV de referência separa sistema de marca, plataforma de campanha e peça isolada; evidencia recorrência, confiança e lacunas antes de traduzir mecanismos ao KV do cliente, sem copiar composição. Integrações metodológicas reescritas de Naksha Studio e UPPAbaby Brand Review. README corrigido para refletir dependências reais, fluxo condicional, ferramentas por ambiente e ausência de autoaprendizado; incluído o `Instalador.ps1` que faltava no pacote público anterior.
- v19.24 (22/10/2026): diagnóstico de criatividade: templates automáticos, fórmulas de cor/tipografia/foco/hero, prompt técnico 70/30 e blacklist estética no gerador local podiam padronizar a criação. "Do zero" impede clonar; formato não determina layout; conceito novo explora três hipóteses privadas. Referências de campanha/editoriais agora definem ambição visual, com adaptação de mecanismos ao KV, sem cópia. Liberadas metáfora, tipografia expressiva, direção heroica e linguagem cromática conforme a ideia, preservando copy, identidade e fatos. Instalada e verificada por SHA-256 em 7 destinos.
- v19.23 (22/10/2026): métodos das skills Figma Use e Figma Design Generator integrados de forma condicional em `modulos\figma.md`: inspeção, trabalho incremental, IDs, fontes, busca por biblioteca e recuperação; telas de app/web separadas de anúncios art-directed. Referências ligadas, sem duplicar integralmente as skills. Instalada e verificada por SHA-256 em 7 destinos.
- v19.22 (rascunho na fonte, 22/10/2026): corrige expectativa de SVG→Figma: IDs/grupos não carregam Auto Layout ou semântica nativa; para arquivo Figma editável, construir frames/textos/camadas nativos, reutilizar DS existente e validar estrutura e screenshot separadamente. Referências Figma Use e Figma Design Generator consultadas. Instalação pendente de aprovação.
- v19.21 (rascunho na fonte, 22/10/2026): Cold Start agora inclui inteligência de marca baseada em evidências para website, Instagram, criativos e benchmark competitivo; amostra delimitada, síntese observado vs. inferido, lacunas e confirmação antes de scraping/serviços pagos. Template registra fontes, confiança, promessa/provas e códigos visuais observados. Fontes de método consultadas estão ligadas em `kv-logo.md`; CLI e dependências externas não foram instaladas. Instalação pendente de aprovação.
- v19.20 (rascunho na fonte, 22/10/2026): direção heroica/publicitária/cinematográfica preservada como modo criativo ativo quando adequada; análise de peças também funciona com raster e outros renders sem exigir SVG/XML. Instalação pendente de aprovação.
- v19.19 (rascunho na fonte, 22/10/2026): gatilho focado em entregáveis visuais e skills especialistas sem disputa de precedência; análise de SVG próprio separada de referência estética, com leitura do render + XML e achados concretos; criação sem contagens obrigatórias, zonas/camadas fixas ou prescrições decorativas para cards/endcards. Instalação pendente de aprovação.
- v19.18 (rascunho na fonte, 22/10/2026): instalador valida origem, sincroniza destinos globais sem apagar arquivos extras, verifica SHA-256 de todos os arquivos e pede confirmação antes de baixar `sharp`; matriz de modelos amplia-se além do Claude com critérios por tarefa, baseada em documentação oficial e relatos de comunidade identificados como anedóticos. Instalação pendente de aprovação.
- v19.17 (rascunho na fonte, 21/10/2026): motor de diagramação em `ads.md` passa por hierarquia, miniaturas de massas, grade e tipografia antes do acabamento; remove sete presets e taxa de ocupação, com veto observável na crítica. Instalação pendente de aprovação.
- v19.16 (rascunho na fonte, 21/10/2026): direção de arte passa à imagem o elo causal da copy antes de gerar; peça reprova metáfora apenas temática e tipografia com pesos sem função, com checagem no render. Instalação pendente de aprovação.
- v19.13 (21/10/2026): tag `CLIENTE_NOVO: SIM|NÃO` ativa o estudo inicial uma vez; cliente existente com KV parcial consulta apenas pendências pertinentes, sem repetir varredura.
- v19.12 (21/10/2026): cliente novo ganha pastas `Originais`, `Banco de Imagens`, `Tratadas` e `IA` desde o início; Cold Start sintetiza direção fotográfica e ofertas com fonte/certeza; evolução da skill informa status e versão instalada no fecho.
- v19.11 (21/10/2026): cliente novo/KV incompleto estuda a série visual indicada e a estrutura dos SVGs; conflito de identidade mostra trecho e fonte antes da decisão; foto obrigatória ausente não vira grafismo arbitrário.
- v19.10 (20/10/2026): peça estática diagramada sai em SVG autossuficiente e PNG por padrão enquanto Figma estiver indisponível; raster isolado permanece PNG, evitando SVG falso.
- v19.9 (20/10/2026): U10 mantém coerência temporal e ambiental em séries sem padronizar todas as fotos; prancha reprova imagem/crop/composição repetida entre cards. `ads.md` e `imagem.md` citam a regra única.
- v9–v15: prévia aprovada antes do Figma; versão única sem backups; Fast-Track de KV + `design_system.md` único + SVG-First; núcleo enxuto; pedido mecânico vs criativo novo; legenda por palavra no KV (`reels_legenda.py`); dossiê de produto 360 e fichas de referências; scripts `gerar_imagem.py` e `img_qa.py`; tradutor de briefing (`briefing.md`).
- v16 (20/10/2026): **renomeado para Designer Mestre** (`/designer-mestre`); nome pessoal removido de todos os arquivos; caminhos fixos trocados por `<PASTA_DO_AGENTE>`.
- v16.1 (20/10/2026): **otimização universal de LPs extraídas e descrição da skill** — regras universais para LPs de construtor (unificação de CTAs pelo maior peso tipográfico com seta lateral interna e hover consistente na cor de ação; escala fluida entre breakpoints com respiro lateral simétrico e sem cortes de texto; centralização e padding interno simétrico de 24 px nos 4 lados para formulários sobre caixa/card de fundo no mobile). `SKILL.md`: `description` atualizada com o resumo claro do agente/skill.
- v17 (20/10/2026): **consolidação de módulos e padronização de `Referências\`** — módulos de mesmo domínio fundidos sem perda de conteúdo (`video.md`, `html.md`, `kv-logo.md`, `imagem.md`); removidos créditos/referências de terceiros e adicionada diretiva interna de soberania e evolução unificada; pasta `Referencias\` padronizada com acento (`Referências\`) em todos os arquivos e clientes.
- v17.1 (20/10/2026): ampliou as opções documentadas de geração de imagem e adaptadores por motor, além da exportação final escolhida pelo usuário. A disponibilidade sempre depende do ambiente; não há mecanismo de autoaprendizado contínuo garantido pela skill.
- v17.2 (20/10/2026): **atalhos técnicos de Product Turnaround Sheet 360 (`360`, `turnaround`, `multiview`, `manual 360`) + pesquisa web automática de especificações geométricas + lei anti-corte e Endcard rico em `ads.md`** — proibido recortar imagens em tiras estreitas/espremidas e proibido último slide de carrossel vazio apenas com logo e CTA em fundo liso.
- v18.0 (20/10/2026): integrou referências de direção de arte, sistemas de design, adaptadores por motor de imagem, fotografia, Taste Engine, dramaturgia de vídeo e QA visual. As regras atuais de acesso a fontes e direitos foram definidas posteriormente; o changelog não substitui os módulos atuais.
- v18.1 (20/10/2026): **consolidação total da Memória de Engenharia, Apresentações HTML (`1600×900`), Brand Book 14 páginas, Extrator de Embed Blindado, Ads Patterns, Vídeo Sprint/UGC/Motion, Figma Console Export e Auditoria Cirúrgica** — (1) `deck.md`: viewport fixo `1600×900` com escala canônica `visualViewport`, 12 arquétipos semânticos (incluindo `Hub & Network` com classes posicionais `node-nw..node-s` e `node-float`), cadência de 4 fundos (Light + adaptação 100% Dark Mode), higiene tipográfica e QA em 4 viewports; (2) `html.md`: extrator de componentes `/embed` com 10 regras invioláveis, escopo CSS/IIFE, correção de modal no `<body>` e marquee full-bleed (`#b_xxx` vs `.e_xxx`), gate de qualificação B2B, estabilidade mobile-first de formulários e ordem de decisão de 5 passos para HTML de apresentação; (3) `kv-logo.md`: arquitetura completa de Brand Book 16:9 em 14 páginas (`cqi`, grids `5/7` e `4/8`, seção `2.10` de usos incorretos da logo em CSS); (4) `ads.md`: 7 padrões canônicos de varredura ocular, 70–90% de engajamento de canvas e matemática de proporção de logo (15–20% L, 10–15% A); (5) `imagem.md`: regras anti-contaminação de fundo, schema JSONL de 9 chaves, geometria multi-view (`30° FOV`, azimutes `30°..330°`, elevações `20°/-10°`, normal/depth matting) e modo `Apply/Replace`; (6) `video.md`: Sprint 30s/15s em 5 blocos com 3 ganchos (Dor/Curiosidade/Oferta), parâmetros vocais PT-BR, mixagem `-6/-18/-12 dB`, 7 pilares de UGC realista, anatomia cinematográfica em 10 elementos e física spring (`damping: 12, stiffness: 150, mass: 0.5`); (7) `figma.md`: execução JS em lote, socket de 42 ferramentas e script autônomo de Console para criar `PaintStyles`, `TextStyles`, `EffectStyles` e `Variables` (`Light`/`Dark`); (8) `SKILL.md` e `qualidade.md`: cirurgia de código (menor mudança completa, causa-raiz), injeção de regras em subagentes, auditoria de código em 6 eixos (`Bug · Risk · Scale · Missing Check · Speed · Lean`) e remoção total de arquivos redundantes e menções de terceiros.
- v19 (20/10/2026): **núcleo enxuto (carga mínima por rota), anexos sob demanda, pen_engine integrado, figma_engine/ENGINE.md desindexado de skills isoladas e precisão de coordenada de legenda Reels (--y = base <= 1470)**.
- v19 (detalhe): **reestruturação lógica e de tokens** — núcleo com carga mínima, tabela de rotas com anexos sob demanda, ciclo mecânico × criativo, leis com hierarquia e padrões universais como fonte única (contraste, safe zone, tipografia, superfícies, espaço/viewports, crítica e prancha); anexos especializados para HTML e imagem; módulos citam `U#` em vez de duplicar valores; `pen_engine` absorvido em `pen.md`; regras de acesso e licença corrigidas em versões posteriores.
- v19.1 (20/10/2026): **reauditoria das fontes (ui-ux-pro-max, awesome-design-md, pasta Memória)** — motor `engines\uiux` e 84 `DESIGN.md` conferidos contra o upstream (íntegros); créditos de terceiros só no `NOTICE.md` discreto, nunca nas entregas, crédito visível apenas quando a licença exigir (§6); novos `assets\base_deck.html` e `assets\validate_deck.py` (QA estático de deck); lacunas integradas de forma condensada: formatos de banner/display/impressão e pisos tipográficos (`ads.md`), proteção e tamanho mínimo de logo (lei 3), foco/justificado/dark tonal (U1/U3/U4), erros de formulário e uso da lib IBGE/MX existente (`html.md`), marquee/iframe/print (`html-extrair.md`), status, cards e gráficos SVG (`html-relatorio.md`), chrome e paginação do brand book, testes e entrega de logo nova, 3 camadas de token (`kv-logo.md`), sequências UGC, claims e motores Runway/Luma/Pika, aviso de licença Remotion (`video.md`), transparência e lote (`imagem.md`), motion e prova de código (`qualidade.md`).
- v19.2 (20/10/2026): **matriz de eficiência de modelos na IDE** — diretrizes no núcleo (§0.8) e documentação: Sonnet 5/4.6 como padrão para 80% do fluxo (código, SVG, HTML, Figma, Decks); Haiku 5.5/4.5 para tarefas mecânicas, legendas e leitura rápida; Opus 5.5/5 para Brand Books 14p, Design Systems do zero e ideação estrutural; contraindicação do Opus 3 legado.
- v19.15 (21/10/2026): pesos de direção para briefings (`copy na peça 5` > `nota da peça 2` > `contexto geral 1` > `menção/histórico 0`); instrução atual, KV, direitos e fidelidade seguem como limites. A proposição publicitária parte da copy. Versão aprovada para instalação.
- v19.14 (21/10/2026): briefing reduzido a ações executáveis, com foto real pertinente como preferência e fallback identificado quando indisponível; referência SVG analisada por função, textura, luz e relação entre ativos; cena ligada à proposição visual e QA comparativo.
- v19.3 (20/10/2026): **`html.md` — CTA interno confiável em builders e teto de caracteres por versão** — (1) nova falha catalogada: CTA (`.link_interno`) que não rola até o alvo porque um script externo (GTM/tracking) intercepta o clique lendo `data-bloco`/`data-bloco-mobile` e ignora o `href`; regra: sincronizar os dois atributos no mesmo id e reforçar com JS próprio em capture (`preventDefault` + `scrollIntoView`), testando com clique real (hit-test) nos 3 breakpoints; (2) teto de caracteres de importação do construtor não é fixo entre versões (uma versão nova pode aceitar menos que a anterior) — em qualquer `Ajuste` perto do limite, todo JS/CSS novo entra minificado e o tamanho final é conferido antes de reentregar; teto real descoberto vai para o `design_system.md` do cliente. Origem: ajuste de LP do cliente Alabastro Vasos (botões do formulário MQL + recusa de importação do V4 Page Builder).

## Eficiência de Modelos na IDE
Escolha pelo trabalho, não por uma marca fixa. Nomes, disponibilidade e limites mudam; use o seletor da IDE para confirmar o modelo atual. Prefira tarefas mecânicas determinísticas a um modelo generativo quando o script/ferramenta já resolve o trabalho. Modelos de visão analisam referências, mas isso não significa que também gerem ou editem imagens.

| Trabalho | Anthropic Claude | OpenAI / ChatGPT | Google Gemini | GitHub Copilot |
|---|---|---|---|---|
| Ajuste pontual, QA simples, leitura curta | **Haiku 5.5** — alta escala e baixa latência | **GPT-6 Luna** — tarefas focadas e volume alto | **Gemini 3.5 Flash-Lite** — execução rápida de alto volume | **Auto · Efficiency**, ou GPT-6 Luna se aparecer no seletor |
| Frontend, SVG, HTML, formulários, Figma e iteração diária | **Sonnet 5.5** — equilíbrio de velocidade e capacidade | **GPT-6.1 Sol** — coding complexo com custo menor que Astra; testar no fluxo da IDE | **Gemini 3.8 Flash** — engenharia de software de longa duração; preview no catálogo consultado | **Auto · Balance**; GPT-5.6 Terra para coding geral ou GPT-6 Sol para coding agentic, se disponíveis |
| Arquitetura, Cold Start, Design System, Brand Book longo ou depuração difícil | **Opus 5.5** para coding agentic longo; **Fable 5.1** para raciocínio mais exigente | **GPT-6 Astra** — trabalho exigente de raciocínio e coding | **Gemini 4 Argon** — engenharia de software complexa e agentes autônomos | **Auto · Intelligence**; GPT-6 Astra para tarefas agentic longas, se disponível |
| Briefing com imagens, referências visuais ou leitura de screenshot | Modelos Claude atuais aceitam imagem; conferir disponibilidade na IDE | GPT atual com entrada de imagem habilitada | Gemini multimodal com entrada de imagem | Modelo disponível que aceite imagem; o suporte depende do seletor/integração |

Os nomes acima são os modelos/famílias que aparecem nas documentações consultadas em **22/10/2026**; alguns, como Gemini 3.8 Flash, estão em preview. Confirme versão, disponibilidade e preço no produto em uso: catálogo de API, ChatGPT e seletor do Copilot não são intercambiáveis. Modelos de visão analisam referências, mas isso não significa que também gerem ou editem imagens.

**Padrão operacional e de tokens:** começar pelo modelo equilibrado para código/layout; descer para opção rápida em tarefas pequenas e verificáveis; escalar para raciocínio mais forte quando houver ambiguidade, contexto extenso ou decisões estruturais. Reduzir contexto trazendo apenas o núcleo, o módulo e os arquivos pertinentes; fornecer briefing, restrições e critérios de QA uma vez em formato compacto; usar scripts existentes em validações determinísticas em vez de pedir ao modelo que refaça a checagem por texto. No Copilot, os tiers **Efficiency / Balance / Intelligence** ajustam a prioridade de custo, equilíbrio ou qualidade do roteamento automático. Para escolher de verdade, comparar com o mesmo briefing, arquivos, critérios e QA. Em UI, medir o ciclo completo até aprovação — iterações e correções visuais incluídas — não só velocidade ou tokens por chamada. Não há benchmark público reproduzível citado aqui que prove um único vencedor para frontend visual.

**Sinal da comunidade GitHub (anedótico):** em [“Mocking Up the UI Before AI Builds It”](https://github.com/mattbrailsford/mattbrailsford.dev/discussions/77), o autor relata, em um projeto, que cerca de 60% dos ajustes tardios eram para combinar com a interface existente e 30% eram decisões sobre conteúdo/apresentação; propõe mockups HTML leves antes de codificar. É uma experiência individual, não comparação de modelos nem benchmark; indica que prévias e critérios visuais antecipados podem reduzir ciclos de correção, não que uma marca específica seja superior.

### Pesquisa e referências
As recomendações resumem capacidades e perfis declarados pelos fornecedores; não estabelecem um ranking entre marcas. Documentação oficial:

- Anthropic: [Models overview](https://platform.claude.com/docs/en/models/overview) · [Choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
- OpenAI: [Models](https://developers.openai.com/api/docs/models) · [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) · [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) · [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra)
- Google: [Gemini models](https://ai.google.dev/gemini-api/docs/models) · [Gemini 3.8 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) · [Gemini 4 Argon](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon)
- GitHub Copilot: [Model comparison](https://docs.github.com/en/copilot/reference/ai-models/model-comparison) · [Auto model selection and tiers](https://docs.github.com/en/copilot/concepts/models/auto-model-selection)
- Comunidade: [Mocking Up the UI Before AI Builds It](https://github.com/mattbrailsford/mattbrailsford.dev/discussions/77) — relato sobre mockup e retrabalho de UI, não teste comparativo de modelos.
- v19.8 (20/10/2026): U9 conecta copy literal à cena por prova, uso, consequência ou tensão; teste de concordância antes da geração e no QA; proporção imagem/texto livre.
- v19.7 (20/10/2026): Direção visual de imagem comercial vem da escolha do usuário, das referências atuais, da receita aprovada do cliente ou de base adaptável; referências opcionais decodificam câmera, luz, profundidade e atmosfera sem supor EXIF; removido rim light obrigatório.
- v19.6 (20/10/2026): Imagem comercial exige argumento e prova visual antes do prompt; direção cinematográfica física e ligada ao KV; 3 direções internas com 1 primeira geração; teste contra imagem genérica.
- v19.5 (20/10/2026): Leitura seletiva para imagem e QA; formato pedido entregue na v1 com prévia visível; aprovação só em decisões materiais; matriz de modelos removida do núcleo; evolução exige localizar função equivalente, preservar capacidade e medir tokens, tempo e qualidade.
- v19.2 (20/10/2026): Pacote 360 é entrada do gerador com referência, nunca recorte colado em cenário; Rota Híbrida restrita a logo/texto/rótulo; §0.6 para e avisa quando o fallback troca o método (gate em `imagem-produto.md` §3).
- v19.1 (20/10/2026): Prévia visível obrigatória (§2) e subagente só devolve caminhos; árvore única de imagens `Imagens\{Originais, Banco de Imagens, Tratadas, IA}` (Lei 5) + trava de destino no `gerar_imagem.py`; `imagem-produto.md`: curadoria da mestra, fundo neutro na referência 360 (também personagem), mestra provisória `_gerada`, inventário de interior; `imagem.md` Parte C (imagem publicitária/hero); template de cliente com `Tratadas\` e pastas de Produtos/Personagens; novo `EVOLUCAO.md` (memória do agente, lido só ao alterá-lo).
