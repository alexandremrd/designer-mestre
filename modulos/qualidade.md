# Módulo Qualidade — Checagem Final por Tipo e Taxonomia Anti-Slop
Ler só a seção do tipo da entrega. Criativo estático novo abre §§A e H depois do render; U6–U8 continuam sendo os padrões base, e esta revisão é o gate independente de conceito e craft. O KV vence qualquer regra daqui. Consulta offline: `python engines\uiux\scripts\search.py "<tema>" --domain ux|typography|color|landing|chart|brand -n 3`. Ferramentas locais: `assets\img_qa.py` (§G).

## A. Anti-"cara de IA" e Taxonomia das 10 Famílias de AI Slop (toda peça)
**P0:** U6 do núcleo.

**As 10 Famílias de AI Slop (auditar e eliminar o que não tem função):**
1. **Concept slop:** conceito baseado só em adjetivos (*"premium, futurista, cinematográfico"*) — se remover os efeitos especiais, a ideia desaparece.
2. **Composition slop:** tudo centralizado por inércia; 3+ elementos com o mesmo peso visual (*equal-emphasis*); fragmentos flutuando em volta do herói sem relação espacial; tangências acidentais entre bordas.
3. **Effect-stack slop:** glow + partículas + fumaça + lens flare + feixe holográfico empilhados sem fonte de luz motivada.
4. **Material slop:** cromo líquido, vidro, plástico translúcido e degradê brilhante misturados sem física de material; reflexos incompatíveis com o ambiente.
5. **Typography slop:** microcopy falso/ilegível, excesso de papéis tipográficos, cada linha com um estilo diferente ou texto jogado onde sobrou espaço.
6. **Photography slop:** pele plastificada, poros hiper-nitidificados artificialmente, bokeh extremo em todos os planos, grade cyan-orange gratuita, mãos/sombras fisicamente inconsistentes.
7. **Decorative UI slop:** dashboards, gráficos, pílulas ou porcentagens falsas usados como enfeite de fundo.
8. **3D-object slop:** esferas, anéis, fitas, cubos ou blobs 3D flutuando no fundo sem papel conceitual.
9. **Brand slop:** marca reduzida a um "banho de cor" genérico que serviria para qualquer concorrente, ou logo redesenhada/deformada.
10. **Detail entropy:** textura repetitiva e ruído de fundo que aumentam sem apoiar o ponto focal.

**Score de Pressão de Slop e Ordem Cirúrgica de Subtração:**
- **Severidade:** `Crítico` (1 = veto imediato: anatomia quebrada, identidade do produto alterada, logo corrompida, conceito trocado por efeito) · `Major` (3 pts cada; 2 Majors = veto) · `Minor` (1 pt cada; soma ≥ 6 pts = veto por acúmulo de aparência sintética).
- **Ordem Cirúrgica de Subtração (quando a peça estiver carregada):** remover nesta ordem exata até a hierarquia ficar cristalina: (1) efeitos sem função → (2) objetos de apoio duplicados → (3) containers/caixas e rótulos redundantes → (4) acentos de cor concorrentes → (5) microdetalhes que somem em tamanho normal de leitura → (6) famílias secundárias de estilo.

## B. LP / HTML / app
1. **Estados:** carregando, vazio, erro, sucesso (ou "n/a" com motivo).
2. **Acessibilidade:** U1 (`img_qa.py contraste`); `:focus-visible`; `label` ligado ao input; botão só-ícone com `aria-label`; decorativo `alt=""` + `aria-hidden`; nada clicável em `div` sem `role`/teclado; erros com `aria-describedby` + `role=alert`; sem `tabindex` positivo.
3. **Toque:** U1; hover nunca é o único gatilho.
4. **Layout:** U1/U3/U4/U5; reservar dimensão de grids e imagens (sem CLS); sem rolagem horizontal nos viewports U5.
5. **Performance:** imagens via `img_qa.py web` (WebP/AVIF sem metadados), `loading=lazy` abaixo da dobra.
6. Revisão pelo **render** nas larguras-alvo, não pela leitura do código.

## C. Motion (HTML, animação programática, vídeo)
- Animar só `transform` e `opacity`. Durações 0.08 / 0.18 / 0.35 / 0.6 / 1.0 s; escala 0.95–1.04; stagger 0.05–0.10 s.
- Movimento só se chama atenção, mostra estado ou dá continuidade. `prefers-reduced-motion`: só fade ≤ 0.2 s.
- Corte no beat: 60/BPM s por batida (30 fps: 1800/BPM frames). Um acento de cor por cena.
- Saída ≈ 60–70% da duração da entrada; máx. 1–2 elementos animados por tela; LP = 1 entrada orquestrada no carregamento (stagger acima), CSS antes de JS; animação nunca é a única via de estado.

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
- Rodar o **Teste Pass³** (`imagem.md` Parte B §6: Física 2s · Detalhe 5s · Marca 3s) e conferir contra a mestra: silhueta, cores, proporção, sombras de contato AO + Cast Shadow e itens proibidos (`PRODUTO_*.md` / `PERSONAGEM_*.md`). Falhou: 1 mutação atômica na camada responsável (máx. 3 tentativas).
- Nada de texto/logo/marca d'água na imagem; rótulo vem do SVG.

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

## I. Tipografia e hierarquia (estático, LP, deck)
- 1 ponto de entrada dominante; no máximo 3 níveis visíveis por tela. Peso **salta** (400→700), não escorrega (400/500/600/700 juntos).
- Em estático, começar com 3–5 tamanhos por peça; web/deck usam a escala necessária à função. Famílias, entrelinha, tracking, medida e fundos: U3/U4.

## J. Auditoria Cirúrgica de Código, Scripts e Componentes (`HTML/CSS/JS/Python`)
Ao revisar, auditar ou refatorar código, LPs, embeds ou motores internos, inspecionar e corrigir na ordem exata de prioridade:
1. **Bug:** entradas vazias/zero/nulas, limites de array/viewport, fuso horário, encoding UTF-8 e divergência entre seletores/chamadores.
2. **Risk:** injeção em `innerHTML` sem sanitização, chaves/credenciais expostas, erros silenciados (`catch {}` vazio) e mutação de variáveis globais em embeds.
3. **Scale:** condições de corrida em listeners/timers, listas/loops sem limite e buscas `O(n²)` no DOM dentro de eventos de `scroll`/`resize`.
4. **Missing Check:** todo parser, formulário ou ramo não-trivial exige validação explícita de entrada e fallback seguro.
5. **Speed:** eliminar leituras repetidas de layout (`getBoundingClientRect` em loop), reflows forçados e re-renderizações desnecessárias.
6. **Lean:** deletar código morto, seletores órfãos e abstrações de uso único; fundir funções duplicadas; preferir APIs nativas da plataforma/stdlib em vez de dependências externas. Limites técnicos intencionais recebem comentário `shortcut: <limite>, <gatilho de upgrade>`.
7. **Prova:** bug = buscar todos os chamadores antes de editar e corrigir a causa no ponto compartilhado; lógica nova não trivial (ramo, parser, dinheiro, segurança) deixa 1 assert/teste. Achado de revisão só com caso concreto (`entrada X → resultado Y`), agrupado em Deve · Deveria · Opcional. Antes de escrever: já existe? → nativo/stdlib → dependência instalada → mínimo; enxugar nunca corta validação, segurança ou acessibilidade.
