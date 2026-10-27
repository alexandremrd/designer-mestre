# Módulo Qualidade — Checagem Final por Tipo e Riscos de Execução
Ler só a seção do tipo da entrega. Criativo estático novo abre §§A e H depois do render; U6–U8 continuam sendo os padrões base, e esta revisão é o gate independente de conceito e craft. O KV vence qualquer regra daqui. Consulta offline: `python engines\uiux\scripts\search.py "<tema>" --domain ux|typography|color|landing|chart|brand -n 3`. Ferramentas locais: `assets\img_qa.py` (§G).

## A. Revisão de artefatos genéricos e riscos de execução (toda peça)
**P0:** U6 do núcleo.

Use estes sinais para localizar problemas, **não como blacklist nem reprovação automática**. Complexidade, centralização, múltiplos focos, tipografia expressiva, cromo, bokeh, cor intensa, UI decorativa e textura podem ser decisões válidas quando intencionais, coerentes com o KV e legíveis. Investigue quando não houver função demonstrável, houver conflito de camada ou a execução distrair da mensagem:
1. **Conceito:** adjetivos substituem uma ideia específica; ao retirar o efeito, a relação com a mensagem desaparece.
2. **Composição:** disputa acidental, elementos sem relação espacial ou tangências não intencionais.
3. **Efeitos e materiais:** iluminação/reflexos incompatíveis com a cena, ou efeitos empilhados sem motivação visual.
4. **Tipografia:** texto falso/ilegível, papéis sem distinção funcional ou estilos que dificultam a leitura.
5. **Imagem:** anatomia/identidade alterada, detalhe artificial ou tratamento que contradiz a cena/KV.
6. **Elementos de apoio:** dashboards, gráficos, objetos 3D, rótulos, texturas ou ornamentos sem papel claro.
7. **Marca:** identidade reduzida a um código genérico, ou logo alterada.

**Lista única de sinais de peça genérica** (reúne Taste, anti-slop e frontend-design; cada item é válido quando tem função ou vem do KV, a pergunta é "o que isso serve nesta peça?"): rótulo minúsculo em caixa alta acima de todo título; selo ou pílula acima do título principal; uma palavra do título trocada de cor, itálico ou sublinhado; 01/02/03 em conteúdo que não é sequência; seta → em todo botão; cards idênticos com ícone em quadrado; gradiente decorativo; a mesma sombra suave em tudo; vidro e blur empilhados; fundo creme com terracota; preto com um neon; dashboard falso de barras cinza; depoimento, logo de cliente ou número inventado; ícones de faísca e estrela de IA; ornamentos de ferramenta de design (cruzes, réguas, linhas-guia); a mesma entrada em fade em todo bloco. Tirar o enfeite sem pôr nada no lugar deixa a peça vazia: preencher com escala, conteúdo completo ou imagem real (`references\taste\tells.md`, por quê e datas).

**Correção cirúrgica:** aponte o elemento observável e a consequência; corrija a camada causadora. Não aplique pontuação, quantidade-limite nem ordem fixa de subtração. Remova ou altere um elemento apenas quando ele causar o problema — não para tornar toda peça minimalista.

## B. LP / HTML / app
1. **Estados:** carregando, vazio, erro, sucesso (ou "n/a" com motivo).
2. **Acessibilidade:** U1 (`img_qa.py contraste`); `:focus-visible`; `label` ligado ao input; botão só-ícone com `aria-label`; decorativo `alt=""` + `aria-hidden`; nada clicável em `div` sem `role`/teclado; erros com `aria-describedby` + `role=alert`; sem `tabindex` positivo.
3. **Toque:** U1; hover nunca é o único gatilho.
4. **Layout:** U1/U3/U4/U5; reservar dimensão de grids e imagens (sem CLS); sem rolagem horizontal nos viewports U5.
5. **Performance:** imagens via `img_qa.py web` (WebP/AVIF sem metadados), `loading=lazy` abaixo da dobra.
6. Revisão pelo **render** nas larguras-alvo, não pela leitura do código.

## C. Motion (HTML, animação programática, vídeo)
Método e receitas completos em `references\motion\` (design-motion-principles, MIT; abrir só o arquivo que a tarefa usa). Aqui não há cota: o contexto decide, e só risco real de entrega gera aviso ao usuário.
- **Frequency gate, antes de animar:** quantas vezes o usuário dispara isso? Raro (mensal): expressão bem-vinda. Ocasional (diário): sutil e rápido. Frequente (centenas por dia) ou por atalho de teclado: sem animação. LP, deck e peça de campanha são momentos raros, então têm liberdade criativa; dashboard e ferramenta de uso diário pedem contenção.
- **Peso por contexto** (define duração, easing e quanto se move): produtividade e dashboard seguem Emil (restrição, abaixo de 300 ms, 180 ms costuma bastar); interface de produto polida segue Jakub (200–500 ms, entrada = opacidade + `translateY` + blur, saída mais sutil que a entrada, mola com `bounce: 0`); criativo, lúdico e portfólio seguem Jhey (o que servir ao efeito; easing tem personalidade, elástico não cabe em banco). Peças mistas pesam por parte. Leituras: `emil-kowalski.md`, `jakub-krehel.md`, `jhey-tompkins.md`.
- **Receitas, HTML/CSS puro primeiro** (`motion-cookbook.md`): entrada e saída e `fill-mode: backwards` (§1), easing, `linear()` e stagger (§2), `@property` (§7), reveal por `clip-path` (§9), transição em vez de keyframe quando o usuário pode reativar (§11), `transform-origin` pela origem lógica (§13), scroll com `IntersectionObserver` de reserva (§14). As receitas em React e Framer Motion ficam como sugestão (`references\alternativas.md`).
- **Ponto de partida quando o contexto não disser nada:** 0,18 / 0,35 / 0,6 s; escala 0,95–1,04; stagger 0,05–0,10 s; saída em 60–70% da entrada. São referência, não teto.
- **Avisar o usuário só quando houver risco real:** estado base invisível sem JS ou sem animação (título nunca nasce `opacity:0`, `html.md` §2); falta de `prefers-reduced-motion` (sem deslocamento, no máximo fade ≤ 0,2 s, estado final preservado); animação de propriedade de layout (`width`, `height`, `top`, `left`) que causa reflow; loop de atenção sem como pausar ou gatilho vestibular (zoom grande, giro, parallax) sem aviso; animação como única via de estado.
- **Ao escrever:** autoverificar contra `creation-gotchas.md` (movimento sem propósito, `scale(0)`, `ease` puro, saída igual à entrada, `will-change` espalhado). **Ao auditar animação existente:** `audit-checklist.md` e `anti-checklist.md`, mais a busca de lacunas, que em HTML é troca de estado sem transição (`display` alternado, `height` sem `transition`). Os padrões de motion genérico do `anti-checklist.md` (pulso, hover-scale em tudo, stagger em toda lista, a mesma entrada em 4 ou mais blocos) são sinais para investigar, como no §A.
- **Degradês:** gerar na resolução final, preservando precisão até a saída; aplicar dithering discreto quando necessário e evitar compressões intermediárias com perdas. Conferir faixas e estabilidade no arquivo final a 100% e em reprodução.
- Corte no beat: 60/BPM s por batida (30 fps: 1800/BPM frames). Um acento de cor por cena. LP: CSS antes de JS.
- **Gate antes de mostrar a prévia** (o usuário não deve ser o QA): tocar em tempo real, não só quadro parado. (1) Cada texto fica na tela o tempo de ser lido inteiro e entra no trecho da voz conferido pelo conteúdo da fala, não só pela contagem de pausas. (2) Nenhum elemento cortado por contêiner (`overflow` de SVG ou caixa) nem pela câmera/zoom; sair da safe zone pode, cortar não. (3) O item em destaque nunca fica encoberto por outro. (4) Espaços entre blocos empilhados são medidos no render e ficam iguais. (5) Níveis de texto diferem em peso e tamanho, e destaques ficam proporcionais aos vizinhos.

## D. Deck (1600×900)
- Cada slide cabe no canvas `1600×900` (`overflow:hidden`), centralizado com `translate(-50%, -50%) scale(var(--deck-scale, 1))` via `visualViewport`; conteúdo demais = dividir ou mudar arquétipo, nunca encolher a fonte abaixo do mínimo (`h2 >= 44px`, `h3 >= 20px`, corpo `>= 17px`).
- Higiene de copy e lista: zero hífen solto em prosa (` - `), zero `–`, `—` ou `~`; zero metalinguagem (*"neste slide"*); zero palavras órfãs na última linha; todo `<li>` com ícone SVG outline (`24×24`); logos inlinadas em Base64.
- Ritmo: nunca > 2 slides seguidos com o mesmo fundo e mesma composição.
- Navegação: setas/Espaço/PageDown, Home/End, botões anterior/próximo e barra de progresso.
- Conferir centralização (`±1px` de margem simétrica) em `1024×768`, `1366×768`, `1600×900` e `1920×1080`.

## E. Copy de anúncio e social
- Uma afirmação concreta por peça; especificidade > adjetivo. Vídeo curto: problema ou resultado nos 3 primeiros segundos.
- Carrossel: as legendas dos cards leem como uma frase contínua.
- Proibido (salvo na copy do cliente): "game-changer", "revolucionário", "de ponta", "no cenário atual", "não é X, é Y", falsa curiosidade, pergunta-isca.
- Copy do cliente é literal: estas regras **apontam** risco em 1 linha, não reescrevem.
- Conferir U9 na prancha final: a cena sustenta a afirmação da copy, e a copy dá contexto à cena? Foto genérica de produto ao lado de promessa específica reprova; proporção entre ambos depende da leitura, não de percentual fixo.

## F. Imagem por IA
- Rodar o **Teste Pass³** (`imagem.md` Parte B §6: Física 2s · Detalhe 5s · Marca 3s) e conferir contra a mestra: silhueta, cores, proporção, sombras de contato relevantes e itens proibidos (`PRODUTO_*.md` / `PERSONAGEM_*.md`). Se falhar, corrigir a causa por edição, nova geração ou outro método adequado; iterar enquanto houver progresso, sem teto fixo, e parar quando novas tentativas não melhorarem o resultado.
- Nada de texto/logo/marca d'água inventado na imagem. Rótulo de produto: a prioridade é o rótulo real do original aplicado por cima; só se falhar de forma repetida entra outro caminho (ex.: o gerador escreve o texto transcrito, conferido letra por letra), ver `imagem-produto.md` §2.4.

## G. Conferência técnica local (`assets\img_qa.py`)
| Quando | Comando |
|---|---|
| Ver todas as peças de uma vez | `prancha Exportados\*.png -o Trabalho\_prancha.jpg` |
| Figma montado × prévia aprovada | `paridade previa.png figma.png` (RMSE ≤ 0.03; acima, abrir o `_diff.png`) |
| Medir cor de foto/logo/referência que vai virar token | `paleta arquivo -n 6` |
| Par texto/fundo | `contraste "#FFF" "#F26B1D"` |
| Logo PNG com sobra | `bbox logo.png` (recorta, não redimensiona) |

## H. Gate visual antes de entregar (criativo novo)
Compare briefing, KV, referências aprovadas e render final lado a lado; não atribua notas. Copy literal, identidade, direitos ou relação cena↔argumento violados = rejeição imediata. Examine cinco perguntas com evidência visível: **Conceito** — há um mecanismo específico que torna a tese visível, além de adjetivos e tema? **Hierarquia** — em miniatura, o olhar entra na ideia certa e a percorre sem disputa acidental? **Craft** — crop, escala tipográfica, alinhamentos, ritmo, contraste e acabamento parecem decisões deliberadas, não defaults do gerador? **KV** — cada camada importante (fundo, foto/luz, tipo, textura/efeito, forma/assinatura) tem origem autorizada e foi adaptada sem copiar a composição? **Distinção** — a peça difere estruturalmente de layouts anteriores e das referências sem perder a família visual do cliente?
**Não aprovar** quando a direção só combina elementos corretos (cor, logo, foto, headline e grafismo) sem explicar por que essas relações são específicas à mensagem; quando um motivo de campanha vira máscara decorativa sem função; ou quando a peça continua reconhecível como um template genérico ao ocultar logo e nome da marca. Reprovação deve apontar a camada e a mudança concreta; corrigir essa causa e conferir o novo render. Só relatar uma pontuação se o usuário pedir.

**Roteiro do olhar** (Taste `references\taste\critique.md`; olhe o screenshot, não o código, porque o código carrega a sua intenção): (1) um segundo, depois cinco como estranho: o que é, para quem, o que fazer; (2) apertar os olhos: duas ou três massas grandes, não muitas pequenas; (3) cobrir a logo: a peça serviria a um concorrente?; (4) contar as bordas esquerdas dos blocos de texto: duas ou três, reaproveitadas; (5) espaço e moldura: margens iguais, buraco por acidente ou descanso por decisão; (6) tipografia: salto decisivo do corpo ao título, órfã, medida; (7) cor: quem tem a maior área, onde está o acento; (8) imagem: cada uma faz um trabalho?; (9) repetição: o mesmo layout em seções seguidas é o template aparecendo; (10) celular como composição própria; (11) preenchimento: pôster composto ou coluna estreita com chão morto; (12) substância: a informação pedida está completa; (13) colisões; (14) teste do concorrente e a "coisa viva". Sem notas nem tetos de pontuação. Ordem de correção: a ideia, a hierarquia, a composição, a tipografia, a imagem, a cor, o detalhe e, por último, o motion.

**Publicidade:** confirme que a proposição é compreensível, que a prova visual/textual está autorizada e que a ação corresponde ao briefing. Sem dados comparáveis, isso é revisão de qualidade e intenção — não previsão de vendas. Se houver métricas, registre fonte, janela, formato e contexto; não atribua causalidade ao visual sem comparação adequada.

**Pôster/key visual:** confira o primeiro impacto em miniatura e a recuperação da informação essencial no tamanho/distância de leitura previstos. Avalie a relação entre tipografia, imagem, campo e material; não exija número fixo de níveis, densidade, sobreposições ou efeito de acabamento.

## I. Tipografia e hierarquia (estático, LP, deck)
- Defina entrada, percurso e quantidade de níveis para a mensagem, formato e distância. Um ponto de entrada dominante ajuda muitas peças, mas pôsteres, composições editoriais e narrativas podem usar percurso/múltiplos focos deliberados; não imponha teto de três níveis. Prefira contrastes tipográficos claros quando ajudam, mas escala, peso, largura, posição e espaço podem graduar a hierarquia. Em interface, preserve a usabilidade; em criativos, não reduza expressão só para cumprir quota.
- Use os tamanhos distintos exigidos pelos papéis reais da peça; 3–5 podem servir de referência inicial em uma composição simples, nunca como quota ou teto. Web/deck usam a escala necessária à função. Famílias, entrelinha, tracking, medida e fundos: U3/U4.

## J. Auditoria Cirúrgica de Código, Scripts e Componentes (`HTML/CSS/JS/Python`)
Ao revisar, auditar ou refatorar código, LPs, embeds ou motores internos, inspecionar e corrigir na ordem exata de prioridade:
1. **Bug:** entradas vazias/zero/nulas, limites de array/viewport, fuso horário, encoding UTF-8 e divergência entre seletores/chamadores.
2. **Risk:** injeção em `innerHTML` sem sanitização, chaves/credenciais expostas, erros silenciados (`catch {}` vazio) e mutação de variáveis globais em embeds.
3. **Scale:** condições de corrida em listeners/timers, listas/loops sem limite e buscas `O(n²)` no DOM dentro de eventos de `scroll`/`resize`.
4. **Missing Check:** todo parser, formulário ou ramo não-trivial exige validação explícita de entrada e fallback seguro.
5. **Speed:** eliminar leituras repetidas de layout (`getBoundingClientRect` em loop), reflows forçados e re-renderizações desnecessárias.
6. **Lean:** deletar código morto, seletores órfãos e abstrações de uso único; fundir funções duplicadas; preferir APIs nativas da plataforma/stdlib em vez de dependências externas. Limites técnicos intencionais recebem comentário `shortcut: <limite>, <gatilho de upgrade>`.
7. **Prova:** bug = buscar todos os chamadores antes de editar e corrigir a causa no ponto compartilhado; lógica nova não trivial (ramo, parser, dinheiro, segurança) deixa 1 assert/teste. Achado de revisão só com caso concreto (`entrada X → resultado Y`), agrupado em Deve · Deveria · Opcional. Antes de escrever: já existe? → nativo/stdlib → dependência instalada → mínimo; enxugar nunca corta validação, segurança ou acessibilidade.

## K. Arquivo exportado (toda exportação)
Conferir o arquivo que vai para o usuário, decodificado ou reaberto, não a prévia, porque o exportador muda cor, faixa, fontes e duração sem avisar. Falhou = corrigir e exportar de novo antes de entregar.
- **Imagem (PNG/JPG/WebP):** dimensão e proporção do formato pedido, perfil sRGB, peso adequado ao canal, texto nítido a 100%.
- **Vídeo (MP4/MOV/WebM):** duração e fps constantes como pedidos; `yuv420p` na faixa tv (JPG de origem vira `yuvj420p` em faixa cheia e muda o contraste em alguns players); áudio presente e voz em -16 LUFS quando houver (`video.md`); primeiro quadro não preto; loop: salto do último para o primeiro ≈ passo entre quadros vizinhos.
- **HTML / prévia:** abre sem internet, console sem erro, logo, imagens e fontes embutidos.
- **PDF / deck:** fontes embutidas, número de páginas, links funcionando.
- **Derivado de prévia aprovada (Figma, recorte, outro formato):** paridade com a prévia (`img_qa.py paridade`; RMSE ≤ 0.03).
