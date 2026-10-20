# Módulo Qualidade — Checagem Final por Tipo e Taxonomia Anti-Slop
Ler só a seção do tipo da entrega. O KV do cliente vence qualquer regra daqui. Consulta offline: `python engines\uiux\scripts\search.py "<tema>" --domain ux|typography|color|landing|chart|brand -n 3`. Ferramentas locais: `assets\img_qa.py` (§G).

## A. Anti-"cara de IA" e Taxonomia das 10 Famílias de AI Slop (toda peça)
**P0 — reprovar sempre (salvo se estiver no KV do cliente):**
1. Acento índigo/violeta padrão de IA: `#6366F1 #4F46E5 #8B5CF6 #A855F7` e vizinhos.
2. Degradê roxo→azul de dois pontos no hero.
3. Emoji como ícone.
4. Card arredondado com borda colorida só à esquerda.
5. Métrica inventada ("10× mais rápido") ou copy de enchimento (lorem, "Recurso 1").
6. Sans genérica no título quando o KV define serifa/display.
7. Imagem placeholder (Unsplash/placehold) na entrega.

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
- **Acento cirúrgico:** neutros 70–90% da área, acento 5–10%, semânticas 0–5%; no máximo 2 usos visíveis do acento por tela/peça.
- **Regra 80/20:** 80% padrão comprovado do KV + 20% num único gesto marcante (um recorte de foto, uma palavra em destaque, um grafismo, um detalhe do produto).

## B. LP / HTML / app
1. **Estados:** carregando, vazio, erro, sucesso (ou "n/a" com motivo).
2. **Acessibilidade:** contraste 4.5:1 (`img_qa.py contraste`); `:focus-visible`; `label` ligado ao input; botão só-ícone com `aria-label`; decorativo `alt=""` + `aria-hidden`; nada clicável em `div` sem `role`/teclado; erros com `aria-describedby` + `role=alert`; sem `tabindex` positivo.
3. **Toque:** alvos ≥ 44 px, 8 px entre alvos; hover nunca é o único gatilho.
4. **Layout e Superfícies:** corpo ≥ 16 px; espaçamento 4/8/16/24/48/96; escada de superfícies (`canvas` → `surface-1`..`surface-4` + `hairline` 1px) no dark mode; reservar dimensão de grids/imagens (sem CLS); sem rolagem horizontal em 375/768/1024/1440.
5. **Performance:** imagens via `img_qa.py web` (WebP/AVIF sem metadados), `loading=lazy` abaixo da dobra.
6. Revisão pelo **render** nas larguras-alvo, não pela leitura do código.

## C. Motion (HTML, animação programática, vídeo)
- Animar só `transform` e `opacity`. Durações 0.08 / 0.18 / 0.35 / 0.6 / 1.0 s; escala 0.95–1.04; stagger 0.05–0.10 s.
- Movimento só se chama atenção, mostra estado ou dá continuidade. `prefers-reduced-motion`: só fade ≤ 0.2 s.
- Corte no beat: 60/BPM s por batida (30 fps: 1800/BPM frames). Um acento de cor por cena.

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

## H. Crítica antes de entregar (criativo novo)
Nota 0–10 em 5 eixos, cada nota citando um elemento da peça: **Conceito** (proposição visual + KV/briefing) · **Hierarquia** (ponto focal único + miniatura 100×100 + grayscale) · **Detalhe** (alinhamento, acentos, kerning, zero tangências acidentais, safe zone) · **Função** (lê em 1 s no feed / CTA claro) · **Gesto** (o 20%).
Faixas: 0–4 quebrado · 5–6 funcional · 7–8 forte · 9–10 excepcional. A nota final é a **pior faixa sustentada**, não a média; média > 8 é suspeita. Qualquer eixo < 7: corrigir uma vez na camada responsável antes de mostrar. Mostrar ao usuário só 1 linha: `Crítica: 8·7·8·9·7 → forte (ajustei hierarquia)`.

## I. Tipografia e hierarquia (estático, LP, deck)
- 1 ponto de entrada dominante; no máximo 3 níveis visíveis por tela. Peso **salta** (400→700), não escorrega (400/500/600/700 juntos).
- Até 2 famílias; 6–8 tamanhos por peça, razão 1.2–1.25. Quebra de linha sempre semântica (zero palavras órfãs).
- Entrelinha: título 0.95–1.15; subhead 1.2–1.3; corpo 1.45–1.6. Nunca título > 1.3 nem corpo < 1.3.
- Polaridade de Tracking: CAIXA ALTA / `eyebrow` / badges `+0.04` a `+0.12 em` (`+0.4px` a `+1.4px`, obrigatório); títulos ≥ 32 px `-0.01` a `-0.02 em`; display ≥ 56 px `-0.03` a `-0.04 em` (`-1.8px` a `-3.5px`); corpo `0`.
- Linha de leitura 45–75 caracteres (`max-width:65ch`).
- Fundo: preto puro e branco puro só se o KV mandar; senão `#0F0F0F` / `#FAFAFA`.

## J. Auditoria Cirúrgica de Código, Scripts e Componentes (`HTML/CSS/JS/Python`)
Ao revisar, auditar ou refatorar código, LPs, embeds ou motores internos, inspecionar e corrigir na ordem exata de prioridade:
1. **Bug:** entradas vazias/zero/nulas, limites de array/viewport, fuso horário, encoding UTF-8 e divergência entre seletores/chamadores.
2. **Risk:** injeção em `innerHTML` sem sanitização, chaves/credenciais expostas, erros silenciados (`catch {}` vazio) e mutação de variáveis globais em embeds.
3. **Scale:** condições de corrida em listeners/timers, listas/loops sem limite e buscas `O(n²)` no DOM dentro de eventos de `scroll`/`resize`.
4. **Missing Check:** todo parser, formulário ou ramo não-trivial exige validação explícita de entrada e fallback seguro.
5. **Speed:** eliminar leituras repetidas de layout (`getBoundingClientRect` em loop), reflows forçados e re-renderizações desnecessárias.
6. **Lean:** deletar código morto, seletores órfãos e abstrações de uso único; fundir funções duplicadas; preferir APIs nativas da plataforma/stdlib em vez de dependências externas. Limites técnicos intencionais recebem comentário `shortcut: <limite>, <gatilho de upgrade>`.
