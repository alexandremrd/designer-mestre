# Designer Mestre (`/designer-mestre`)

O **Designer Mestre** é uma skill para produção de entregáveis visuais ligados a uma marca. Quando o pedido exige, pode analisar materiais fornecidos e fontes públicas acessíveis para extrair posicionamento, identidade e referências; cria anúncios, páginas, apresentações, vídeos ou imagens conforme o pedido e as ferramentas disponíveis na sessão. Em criação visual nova, a bancada é iterada com o usuário e a direção é aprovada antes de escolher/exportar o arquivo final, exceto quando o usuário pede entrega direta. A memória é específica do cliente e depende dos arquivos e do feedback disponíveis: não há aprendizado autônomo entre sessões.

## Como instalar sem complicação

Na v19.31, o fluxo de mudança aprovada é: atualizar a fonte, escolher a combinação de engine e bancada com maior potência adequada ao conceito, executar `Instalador.cmd`, conferir os destinos por SHA-256 e publicar os arquivos e informações relevantes no repositório GitHub (remoto `origin`). O instalador preserva arquivos extras. Recarregue a IDE para descobrir a skill; destinos opcionais dependem do ambiente. A página do GitHub mantém apenas as quatro atualizações mais recentes.

## Visão geral técnica

**Designer Mestre** é uma skill de criação visual. No Cold Start ou quando solicitado, analisa fontes acessíveis de site, Instagram, briefing e criativos, separando evidência de inferência; compara concorrentes quando isso for pertinente e mantém a memória isolada por cliente. Cobre ads, posts, LP/HTML, deck, vídeo, motion, imagem/3D e Figma, conforme ferramentas efetivamente disponíveis. Chamada: `/designer-mestre`.

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
- **Evolução unificada:** regra nova substitui a antiga no módulo dono do tema; valor usado por 2+ módulos mora nos Padrões `U1–U11` do núcleo.

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
├── SKILL.md            ← núcleo (v19): carga mínima, rotas, ciclo de entrega, Gate de KV, leis hierárquicas, padrões U1–U11, memória
├── modulos\            ← lidos só quando o pedido é daquele tipo (consolidados por domínio)
│   ├── briefing.md     ← tradutor de briefing (só o que é do designer)
│   ├── ads.md          ← direção de arte, composição e bancada flexível de ads
│   ├── video.md        ← edição de vídeo do cliente (legenda + KV) + roteiro/UGC/IA + motion
│   ├── html.md         ← LP/site novo, ajuste, formulário, SEO, a11y, QA
│   ├── html-extrair.md ← anexo: clonar/otimizar construtor, embed `</>`, recriar de print
│   ├── html-relatorio.md ← anexo: página-relatório
│   ├── kv-logo.md      ← Cold Start, MIV Scanner, Brand Book, Logo nova e Design System (tokens/DESIGN.md)
│   ├── imagem.md       ← arsenal, prompt por motor, fotografia, compositing, Vision Decomposer, Pass³
│   ├── imagem-produto.md ← anexo: produto fiel / 360 / turnaround
│   ├── imagem-personagem.md ← anexo: rosto recorrente
│   ├── deck.md         ← apresentações e preview iterável; engine/formato por necessidade
│   ├── referencias.md  ← decodificador de referências em fichas e receitas no KV
│   ├── figma.md        ← montagem 1:1 no Figma após aprovação
│   ├── pen.md          ← prototipação rápida (absorveu `pen_engine\SKILL.md`)
│   └── qualidade.md    ← checagem final por tipo (artefatos genéricos, a11y, motion, deck, copy, QA)
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
2. O agente registra a mudança na fonte e no changelog; antes da aprovação, não instala nem publica.
3. Após aprovação, o agente instala e verifica por SHA-256, sincroniza os arquivos e metadados pertinentes no GitHub, e atualiza a lista pública para manter somente as quatro notas mais recentes.

Só regras universais entram aqui. Preferência de cliente vai no `design_system.md` dele.

## Changelog
- v19.31 (22/10/2026, instalada em 7 destinos): preserva a pesquisa criativa v19.30 — proposição/prova publicitária, direção fotográfica e cinematográfica, pôster, oferta/funil opcionais e beats de vídeo — retirando SVG/PNG e HTML de deck como formatos obrigatórios. Nova peça escolhe a engine/bancada mais potente adequada ao conceito e itera em preview; após aprovação, o usuário escolhe formato final e padrão de saída. HTML/CSS/JS, SVG, PPTX/Python, raster, Figma e composições híbridas são opções conforme ferramenta e uso; sites HTML continuam pixel-perfect. A cópia instalada foi conferida por SHA-256.
- v19.30 (22/10/2026, somente na fonte): pesquisa de GitHub sobre direção de arte, fotografia publicitária, criação de anúncio, cinema e pôster; síntese preservada na v19.31.
- v19.29 (22/10/2026): formaliza o ciclo aprovado: atualizar a fonte, reinstalar e verificar por SHA-256, publicar no GitHub e manter somente quatro notas públicas.
- v19.28 (22/10/2026): fortalece a criação de ads com handoffs entre composição, referências, direção fotográfica e gate visual pós-render; instalado e verificado em 7 destinos.
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
