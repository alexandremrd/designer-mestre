# Designer Mestre (`/designer-mestre`)

O **Designer Mestre** é uma skill para produção e leitura de materiais visuais ligados a uma marca. Pode descrever e interpretar imagens, responder perguntas visuais, extrair texto legível e comparar referências pela capacidade multimodal nativa; análise de anúncios e decodificação de KV preservam seus módulos especialistas. Quando o pedido exige, também analisa materiais fornecidos e fontes públicas acessíveis para extrair posicionamento, identidade e referências; cria anúncios, páginas, apresentações, vídeos ou imagens conforme o pedido e as ferramentas disponíveis na sessão. Em criação visual nova, a bancada é iterada com o usuário e a direção é aprovada antes de escolher/exportar o arquivo final, exceto quando o usuário pede entrega direta. A memória é específica do cliente e depende dos arquivos e do feedback disponíveis: não há aprendizado autônomo entre sessões.

## Como instalar sem complicação

Na v19.34, leitura de imagem usa primeiro a capacidade multimodal nativa da sessão, sem instalar skills, SDKs ou configurar API externa; locução e efeitos sonoros usam a API ElevenLabs só quando há chave configurada. O fluxo de mudança aprovada é: atualizar a fonte, escolher a combinação de engine e bancada com maior potência adequada ao conceito, executar `Instalador.cmd`, conferir os destinos por SHA-256 e publicar os arquivos e informações relevantes no repositório GitHub canônico (remoto `origin` da fonte). O instalador preserva arquivos extras, nunca copia credenciais (`.env*`, `*.key`) e não toca na memória dos clientes nem nas credenciais do usuário, que ficam fora da pasta da skill. Recarregue a IDE para descobrir a skill; destinos opcionais dependem do ambiente. A página do GitHub mantém apenas as quatro atualizações mais recentes.

## Visão geral técnica

**Designer Mestre** é uma skill de criação e leitura visual. No Cold Start ou quando solicitado, analisa imagens e fontes acessíveis de site, Instagram, briefing e criativos, separando evidência de inferência; compara referências/concorrentes quando pertinente e mantém a memória isolada por cliente. Cobre ads, posts, LP/HTML, deck, vídeo, motion, imagem/3D e Figma, conforme ferramentas efetivamente disponíveis. Chamada: `/designer-mestre`.

## Fluxo
1. **Briefing:** texto, e-mail ou PDF longo pode ser organizado em `briefing.md` quando a tarefa exigir.
2. **Bancada de criação:** nova peça abre uma visualização iterável no meio mais adequado à ideia e às ferramentas disponíveis; preview e formato final são decisões diferentes.
3. **Gate de KV:** antes de gerar, lê o `design_system.md` do cliente (cores, fontes, logo, vetos). Cliente sem KV passa pelo Cold Start (`kv-logo.md`).
4. **Módulo do pedido:** abre só o módulo da rota (e o anexo, quando a rota pede); dentro dele, só a Parte do pedido.
5. **Aprovação e exportação:** depois da aprovação, confirme os formatos finais e o padrão de exportação, salvo se o usuário já os definiu ou houver preferência de cliente registrada. Faça QA pertinente ao destino e salve os arquivos escolhidos no caminho acordado.

No Cold Start, distingue observação de inferência, registra fontes e datas, mapeia códigos visuais e verbais e transforma achados em posicionamento, provas, lacunas e oportunidades criativas. Scraping/serviços externos são opcionais; não instala dependências nem inicia coleta paga automaticamente.

## Leis principais
- **Logo:** nunca é criada nem alterada. Usa só o arquivo original, ou o placeholder `LOGO [CLIENTE]`.
- **Copy:** literal, sem inventar CTA, selo ou número, e sem promessas absolutas.
- **Isolamento:** nada de um cliente vaza para outro.
- **Bancada e arquivo final:** escolha engine e meio de autoria/preview pelo potencial de criação, render e edição para a peça. SVG, PNG, HTML, PPTX, PDF, Figma nativo e composições híbridas atendem necessidades distintas; nenhum é o formato final padrão.
- **Site em HTML:** preserva o requisito pixel-perfect da rota HTML. A liberdade entre engines aplica-se à bancada de outras peças visuais e não relaxa esse requisito.
- **Direção visual:** escolhas são julgadas pelo papel na ideia, no KV e na legibilidade; cor intensa, gradientes, texturas e recursos expressivos não são vetados por si.
- **Fontes e direitos:** extrai só o que é acessível (DOM renderizado, CSS computado, arquivos enviados); bloqueio = pede HTML salvo ou print. Referência de terceiros transfere técnica, nunca identidade. Código absorvido mantém a licença original.
- **Evolução unificada:** regra nova substitui a antiga no módulo dono do tema; valor usado por 2+ módulos mora nos Padrões `U1–U12` do núcleo.

## Memória e ferramentas disponíveis
- **Memória por cliente:** `D:\Clientes\[Cliente]\_DESIGN\` (`guia.md` com aprovado/reprovado em sugestões, `design_system.md` com KV e negócio, `historico.md`).
- **Guia do agente:** `GUIA.md` reúne tendências sem cliente, em sugestões breves; o `/aprenda` reescreve os guias ao fim de cada projeto. Registre apenas conhecimento durável e feedback efetivamente recebido; não presuma aprovação, reprovação ou aprendizado automático.
- **Geração de imagem:** os módulos documentam adaptadores e opções de motor, incluindo motores locais e integrados quando instalados e disponíveis. A skill não garante acesso a um modelo ou execução de geração em toda sessão.
- **QA de imagem:** `assets\img_qa.py` oferece operações como prancha, paridade RMSE, paleta, contraste WCAG, trim de bbox e conversão WebP; cada operação depende dos requisitos e do runtime disponível.
- **Vídeo e legenda:** `assets\reels_legenda.py` oferece sincronização de legenda, cortes e tratamentos descritos no módulo; valide dependências e disponibilidade antes de prometer execução.
- **Locução e efeitos sonoros:** `assets\gerar_audio.py` gera TTS e efeitos pela API ElevenLabs (só biblioteca padrão do Python); cada usuário faz o próprio login (`npx -y @elevenlabs/cli@latest onboard init` em `%USERPROFILE%\.designer-mestre\`, guiado pela IA), a chave fica fora da skill e cada geração gasta créditos da conta dele.
- **Motor offline UI/UX e 84 Design Systems:** `engines\uiux` inclui coleções locais consultáveis por `--domain brand` e `--brand <slug>`, sem substituir o KV validado do cliente.

## Onde fica o agente
O agente pode ser salvo em qualquer pasta (`<PASTA_DO_AGENTE>`). A cópia editada na pasta raiz é a fonte; **após aprovação da versão**, rode `Instalador.cmd` para localizar as IDEs do computador e sincronizar a skill. **Nota de economia de tokens:** o arquivo `Instalador.cmd` é exclusivamente para instalação — o agente nunca deve abri-lo ou analisá-lo em sessões. As alterações sobrescrevem os arquivos, sem backups duplicados.

## Estrutura

```text
<PASTA_DO_AGENTE>\
├── GUIA.md            ← sugestões sem cliente, lidas no início
├── SKILL.md            ← núcleo (v19): carga mínima, rotas, ciclo de entrega, Gate de KV, leis hierárquicas, padrões U1–U12, memória
├── modulos\            ← lidos só quando o pedido é daquele tipo (consolidados por domínio)
│   ├── briefing.md     ← tradutor de briefing (só o que é do designer)
│   ├── ads.md          ← direção de arte, composição e bancada flexível de ads
│   ├── video.md        ← edição de vídeo do cliente (legenda + KV) + roteiro/UGC/IA + motion
│   ├── html.md         ← LP/site novo, ajuste, formulário, SEO, a11y, QA
│   ├── html-extrair.md ← anexo: clonar/otimizar construtor, embed `</>`, recriar de print
│   ├── html-relatorio.md ← anexo: página-relatório
│   ├── kv-logo.md      ← Cold Start, MIV Scanner, Brand Book, Logo nova e Design System (tokens/DESIGN.md)
│   ├── imagem.md       ← arsenal, leitura/análise multimodal, OCR visual, prompt, fotografia, Vision Decomposer, Pass³
│   ├── imagem-produto.md ← anexo: produto fiel / 360 / turnaround
│   ├── imagem-personagem.md ← anexo: rosto recorrente
│   ├── deck.md         ← apresentações e preview iterável; engine/formato por necessidade
│   ├── referencias.md  ← decodificador de referências em fichas e receitas no KV
│   ├── figma.md        ← montagem 1:1 no Figma após aprovação
│   ├── pen.md          ← prototipação rápida (absorveu `pen_engine\SKILL.md`)
│   └── qualidade.md    ← checagem final por tipo (artefatos genéricos, a11y, motion, deck, copy, QA)
├── assets\             ← gerar_imagem.py · gerar_audio.py · img_qa.py · reels_legenda.py · base_lp.html · qa_html.py · validacao-forms.js/.css · base_deck.html · validate_deck.py
├── engines\uiux\       ← motor offline de paletas, fontes, padrões de LP e regras UX
├── engines\designlang\ ← extração de tokens de um site (instalar dependências só com aval)
├── references\  figma_engine\  ← taste\ motion\ logo\ huashu\ variantes\ alternativas.md (anexos sob demanda)
├── Clientes\_TEMPLATE_CLIENTE\  ← design_system.md + historico.md
├── NOTICE.md           ← avisos de licença de terceiros (conformidade; não lido pelo agente)
└── Instalador.cmd      ← instalador universal para todas as IDEs (não analisar)
```

A memória de cada cliente fica em `D:\Clientes\[Cliente]\_DESIGN\` (`design_system.md` + `historico.md` + `templates\`). Nada de cliente mora nesta pasta.

## Como alterar
1. Pedir a mudança ("atualiza o /designer-mestre: ...").
2. O agente registra a mudança na fonte e no changelog; antes da aprovação, não instala nem publica.
3. Após aprovação, o agente instala e verifica por SHA-256, sincroniza os arquivos e metadados pertinentes no GitHub, e atualiza a lista pública para manter somente as quatro notas mais recentes.

Só regras universais entram aqui. Preferência de cliente vai no `design_system.md` dele.

## Changelog
- v19.89 (27/10/2026): `imagem-personagem.md` §3 com motores de referência para rosto e regra de parar sem referência; `imagem.md` B §2 com vocabulário de consulta de luz, lente, grade e textura; cabeçalho do `SKILL.md` alinhado à versão.
- v19.88 (27/10/2026): `imagem-produto.md` §5: execução do `/input` e do kit com a receita de kit validada (Codex com 3 imagens, escala medida, refino por recortes, arte real do PDF por cima) no lugar do render colado nos slots; `/input` trava a cena exceto o que o usuário listar; novo `assets\aplicar_rotulo.py` (arte do PDF em cilindro, sombra preservada).
- v19.87 (26/10/2026): `imagem-produto.md` ?5 unifica `/produto-conceito` e `/designer-mestre /input` para 1..N produtos (adapta??o de slots na cena, compositing determin?stico do render oficial + PDF da embalagem em alta resolu??o com luz/refra??o da cena, Prancha de Aprova??o 1:1 por Slot e refa??o isolada estilo `/360-produto`); `Instalador.ps1` sincroniza a fonte em `D:` e subpastas at? n?vel 7.
- v19.86 (26/10/2026): `/produto-conceito` ?5 com invent?rio da entrada e da pasta do cliente, imagem enviada como base, lado a lado antes de mostrar, diverg?ncia volta ao 360 e gerador forte.
- v19.85 (26/10/2026): `/produto-conceito` cobre linha ou kit inteiro (um item por rodada, sem 360 parte do original) e usa `Imagens\IA\` como hist?rico quando n?o h? `[CONCEITO]`.
- v19.84 (26/10/2026): Atalho `/produto-conceito`, `imagem-produto.md` ?5 e `references/conceito/` (foto conceito de produto: IA escolhe o conceito por estudo, anti-repeti??o, aprova??o e refa??o do 360); t?cnicas de 5 skills do GitHub em texto pr?prio.
- v19.83 (26/10/2026): Fusão de Taste, design-motion, logo-design, designlang, huashu-design e variantes Anthropic nas rotas existentes; HTML pixel-perfect (LP, site, slides) como prioridade e framework/variantes como saída alternativa; logo nova só com "nova".
- v19.82 (26/10/2026): Refação universal (ciclo do 360 para toda entrega) e produto com 360 condicional à insuficiência da extração do original.
- v19.81 (26/10/2026): Fecho com gatilho explícito: qualquer resposta que cite task, peça ou entrega usa o bloco de entrega, sem títulos, listas nem tabelas.
- v19.80 (26/10/2026): Rótulo de produto: arte real aplicada por cima como prioridade, gerador escreve só como caminho alternativo após falhas repetidas.
- v19.79 (26/10/2026): Produto fiel: ordem das fontes de embalagem em 3 níveis (arquivo original da embalagem, referências locais, internet só sem as duas).
- v19.78 (26/10/2026): Imagem gerada por qualquer motor (inclui IA parceira) salva na hora em `IA\` com `.txt`; fundo e cena de produto viram ativo reutilizável, criado e aprovado à parte e só depois aplicado na peça.
- v19.77 (26/10/2026): Produto 360 em cena de kit: receita verificada (3 referências ao gerador, arte real do rótulo aplicada por cima, refino por recortes com contexto, ordem de geradores) e Figma sem cota: achar as peças sozinho antes de pedir arquivo ao usuário.
- v19.76 (26/10/2026): Figma: cota do conector tratada como limitada (analisar/exportar com poucas chamadas, aplicar em lote só após o aprovado) e recuperação ao atingir o limite (pedir PNGs e comentários, entregar como imagem).
- v19.75 (26/10/2026): Produto 360, rota 1b: rótulo ou adesivo na área reta, centralizado entre o início das curvas (a posição medida em render com perspectiva desloca); a perspectiva da fonte inclui a elipse de fundo e topo redondos vistos de cima ou de baixo (separar forma e ângulo; a forma tem que parar em pé); emendas com a curva saindo tangente da reta, sem inverter a curvatura.
- v19.74 (26/10/2026): "Prova antes de afirmar" no ciclo de entrega (conferir em tamanho real contra a fonte, buscar insumo antes de dá-lo por ausente, medir após 2 falhas, não sobrescrever ativo aprovado, conferir o arquivo exportado) e `qualidade.md` §K por tipo de arquivo. Auditoria da skill inteira: módulos alinhados à prova; scripts sem sucesso falso, com `--substituir` para sobrescrever, avais protegidos contra arquivo ilegível e novo `assets\conferir_export.py`. Produto 360: qualidade da embalagem como Regra de Ouro (arte em PDF > render do fabricante > foto); rota 1b com perfil abaixo do pixel, relevo do adesivo e arte em alta e opaca, mantendo o realismo do render.
- v19.73 (24/10/2026): Produto e Personagem 360 ampliados com técnicas de 6 skills do GitHub (texto próprio): U12 com execução consistente e motores externos como opção; Product Spin 360° (Blender, vídeo com referência, visualizador), vista explodida, corte, variantes da prancha e argila 3D em `imagem-produto.md`; biblioteca de identidade, Expression Sheet, referências com papel e pose travada em `imagem-personagem.md`; atalhos `/360-produto` e `/360-personagem`. Recursos locais: `motor_local.py` detecta motores já instalados e duplicatas, reaproveita em vez de instalar de novo, organiza tudo numa raiz escolhida pelo usuário (Geradores, Ferramentas, Modelos, Cache) com registro único em `assets\recursos.py`, reescreve os caminhos ao mover ou renomear e grava as variáveis do usuário dos caches do uv, npm e Playwright; sharp instalado uma vez em `Ferramentas\node`. Rota 1b do giro: produto de revolução modelado em 3D a partir da própria foto, com a impressão real aplicada; `img_qa.py` acha arquivos em pastas com `[TIPO]` no nome. Antes de declarar que não há foto melhor do produto, buscar na web e pedir à CDN da loja o arquivo original (`imagem-produto.md` §1).
- v19.72 (24/10/2026): Insumos em baixa resolução checados na triagem (`briefing.md` §1); fluxo em `imagem.md` §4 com upscale determinístico local primeiro, pergunta de autorização para IA, prompt de cópia fiel 1:1, busca no GitHub via web após 2 falhas, parada após 2 falhas pós-busca e organização em `Imagens\IA\[Item]\`. Trilha no `video.md` exige licença comercial na pasta `Música\`.
- v19.71 (24/10/2026): 360 um item por rodada (lei da marca em texto; apoio cruzado só entre itens semelhantes); construção da embalagem define verso e laterais sem foto; rótulo transcrito e escrito pela IA, com o SVG como reserva; prévia de prancha legendada.
- v19.70 (24/10/2026): GUIA: pulsar = escala + brilho, sem mudar cor; selo e aviso usam a pílula do KV; feedback vago de movimento = uma camada por rodada.
- v19.69 (24/10/2026): narração longa ganha versão condensada antes de gerar a voz; Parte C com densidade de motion (mudança por frase, cena a cada 4–6 s, transições com direção, regressiva esvazia).
- v19.68 (24/10/2026): `Aprovação\` só com a peça (motion = prévia HTML autossuficiente com áudio; estático = imagem); prints e prancha ficam em `Trabalho\`.
- v19.67 (24/10/2026): nova subpasta `Aprovação` só com o que o usuário avalia; o explorador abre nela (prévias) ou em `Exportados` (finais), nunca em `Trabalho`.
- v19.66 (24/10/2026): Localização no formato que o agente abre (cartão de arquivo, explorador, file:///) + caminho para copiar; prévia reprovada é excluída quando substituída, exceto imagem gerada por IA.
- v19.65 (24/10/2026): motion com narração IA por padrão ("sem locução" no briefing = perguntar citando o trecho); prévia autossuficiente conferida no visualizador do usuário; GUIA: respiro e contraste de pesos.
- v19.64 (24/10/2026): Produto e Personagem 360 geram vistas ausentes após pesquisa, com revisão e aprovação; fontes seguras prevalecem sobre IA. Linguagem crítica e verificação de incertezas no núcleo.
- v19.63 (24/10/2026): Three.js como opção pertinente; alternativas verificadas em falhas e autorização única para dependências necessárias.
- v19.62 (23/10/2026): controle de qualidade de degradês animados cobre banding, precisão, resolução e compressão da exportação final.
- v19.61 (23/10/2026): entradas e saídas suaves também para elementos gráficos do vídeo; avaliação temporal de fluidez.
- v19.60 (23/10/2026): vídeo com H1 animada de abertura, fechamento H1 + CTA e cortes que preservam fala e respiro; animação de legenda não pode prejudicar sincronização.
- v19.59 (23/10/2026): Localização inclui link para abrir a pasta das entregas, além dos links individuais dos arquivos.
- v19.58 (23/10/2026): estáticos sociais entregam Feed e Stories com composição adaptada e conferência dos dois tamanhos antes da conclusão, salvo exceção explícita.
- v19.57 (23/10/2026): fecho com um bloco por entrega, cada um só com o próprio contexto, arquivos e pedido; guia do agente: CTA sai no componente de CTA do KV, nunca como texto solto.
- v19.56 (23/10/2026): `reels_legenda.py` com legenda de 1 linha e até 3 palavras por padrão (sem quebra) e cross dissolve em cada corte (`--fade`, padrão 0,25 s, áudio com acrossfade); regra fixa do usuário registrada no `GUIA.md`.
- v19.55 (23/10/2026): corte de fala em vídeo segue plano de montagem da Parte B §1 (arco, 3 funções, Murch, respiro) mostrado em tabela com a prévia; `reels_legenda.py` sem dependência de ffmpeg no PATH, transcrição com queda GPU→CPU e novos `--caixa --remover --respiro --gancho --endcard`; escolha técnica sempre em pergunta com opções. Fecho por task sem rótulos, exceto `Localização:` (nome, emoji de status escolhido pelo contexto, contexto, impedimentos, arquivos) e última linha de estado em negrito: ⏸ Parado, esperando você / ✅ Concluído. Aviso de 1 linha antes de etapa longa. Abrir a pasta a cada prévia e aprovação final vira preferência perguntada uma única vez e gravada (`consentimento.py`, `preferencia.abrir_pasta`).
- v19.54 (23/10/2026): fonte pedida e não instalada (U3): pergunta a cada fonte se pode instalar; com o sim, pesquisa a origem oficial, baixa só versão gratuita ou licenciada, instala para o usuário sem admin e usa o nome exato; fonte paga = pedir o arquivo; nunca fallback silencioso.
- v19.53 (23/10/2026): aval único: motor local, IA parceira e conector/MCP sem custo pedem o sim uma vez, gravado por `consentimento.py` e válido em toda IA; depois rodam em silêncio. Conta paga: sim único dentro do contratado; passar do contratado ou API cobrada por uso pede sim a cada geração, avisando que quem cobra é o provedor da IA, não a skill (`consentimento.py excedente`). `motor_local.py` analisa o PC, recomenda só o que cabe, traz a pergunta pronta, mostra o plano antes de baixar e tem o roteiro `guia` para a IA instalar sozinha (sem git usa o zip oficial; sem Python compatível instala o oficial). `gerar_imagem.py` recusa sem aval e liga o motor sozinho.
- v19.52 (23/10/2026): motor local opcional sem app de terceiros: `motor_local.py` instala (com permissão, fora da skill) e liga/desliga o ComfyUI como servidor sem interface com FLUX.2 klein 4B + encoder fp4 (Apache 2.0 conferida em cada arquivo, ~7,7 GB); `gerar_imagem.py gerar` comanda o ComfyUI pela API (`--motor auto|comfy|ed`), com edição multirreferência.
- v19.51 (23/10/2026): toda resposta fecha com o bloco **Onde está** (pasta do projeto + cada arquivo da rodada); pasta da entrega usa o nome da tarefa enviado pelo usuário; exportar abre `Exportados\` no explorador.
- v19.50 (23/10/2026): instalador acha toda e qualquer cópia da skill no perfil (inclui OpenCode e Qwen) e aceita `-Sim` para atualizar sem perguntar; atualização aprovada vai para todas as cópias.
- v19.49 (23/10/2026): falha sem fallback automático vira pergunta com opções verificadas (IA parceira em apps instalados, MCP com a capacidade, motor local, API), escolha = sim do gasto; motion confirma narração e trilha no início; `motion_export.py` com `--tamanho` e saída sempre estéreo; regra fixa H1 sem ponto final no `GUIA.md`.
- v19.48 (23/10/2026): `EVOLUCAO.md` vira caderno de manutenção (estado, casos de teste, pendências; ~2 KB); tendências de criação passam ao `GUIA.md`; publicar no GitHub só com pedido explícito.
- v19.47 (23/10/2026): guias de sugestões em duas camadas: `GUIA.md` do agente (sem cliente) e `_DESIGN\guia.md` de cada cliente (aprovado/reprovado), escritos pelo /aprenda ao fim de cada projeto, que também enxuga o núcleo.
- v19.46 (23/10/2026): detecta motores e IAs locais já instalados antes de propor instalação; papéis definidos: Claude raciocina e confere, local faz o determinístico, imagem final usa o gerador que acerta em menos rodadas.
- v19.45 (23/10/2026): motor local é opção oferecida ao usuário, não regra; nova opção de modelo 3D local + img2img para vistas de produto sem foto real; imagens reprovadas vão para `IA\Não aprovadas\` com o motivo.

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
- v19.5 (20/10/2026): Leitura seletiva para imagem e QA; preview visível durante criação; aprovação antes de escolher/exportar o arquivo final, salvo pedido direto; matriz de modelos removida do núcleo; evolução exige localizar função equivalente, preservar capacidade e medir tokens, tempo e qualidade.
- v19.2 (20/10/2026): Pacote 360 é entrada do gerador com referência, nunca recorte colado em cenário; Rota Híbrida restrita a logo/texto/rótulo; §0.6 para e avisa quando o fallback troca o método (gate em `imagem-produto.md` §3).
- v19.1 (20/10/2026): Prévia visível obrigatória (§2) e subagente só devolve caminhos; árvore única de imagens `Imagens\{Originais, Banco de Imagens, Tratadas, IA}` (Lei 5) + trava de destino no `gerar_imagem.py`; `imagem-produto.md`: curadoria da mestra, fundo neutro na referência 360 (também personagem), mestra provisória `_gerada`, inventário de interior; `imagem.md` Parte C (imagem publicitária/hero); template de cliente com `Tratadas\` e pastas de Produtos/Personagens; novo `EVOLUCAO.md` (memória do agente, lido só ao alterá-lo).
