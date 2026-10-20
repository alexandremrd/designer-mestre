# Módulo Qualidade — checagem final por tipo
Ler só a seção do tipo da entrega. O KV do cliente vence qualquer regra daqui. Consulta offline: `python engines\uiux\scripts\search.py "<tema>" --domain ux|typography|color|landing|chart -n 3`. Ferramentas locais: `assets\img_qa.py` (§G).

## A. Anti-"cara de IA" (toda peça)
**P0 — reprovar sempre (salvo se estiver no KV do cliente):**
1. Acento índigo/violeta padrão de IA: `#6366F1 #4F46E5 #8B5CF6 #A855F7` e vizinhos.
2. Degradê roxo→azul de dois pontos no hero.
3. Emoji como ícone.
4. Card arredondado com borda colorida só à esquerda.
5. Métrica inventada ("10× mais rápido") ou copy de enchimento (lorem, "Recurso 1").
6. Sans genérica no título quando o KV define serifa/display.
7. Imagem placeholder (Unsplash/placehold) na entrega.

**P1 — corrigir se der:** gradiente em tudo; glass sem função; blobs; card dentro de card; animação de scroll em tudo; LP no roteiro Hero→Features→Preço→FAQ→CTA sem nenhuma variação; mais de ~12 HEX soltos fora dos tokens.

**Acento cirúrgico:** neutros 70–90% da área, acento 5–10%, semânticas 0–5%; no máximo 2 usos visíveis do acento por tela/peça.
**Regra 80/20:** 80% padrão comprovado do KV + 20% num único gesto marcante (um recorte de foto, uma palavra em destaque, um grafismo, um detalhe do produto). Peça "simples demais" = falta o 20%; peça "carregada" = mais de um gesto.

## B. LP / HTML / app
1. **Estados:** carregando, vazio, erro, sucesso (ou "n/a" com motivo).
2. **Acessibilidade:** contraste 4.5:1 (`img_qa.py contraste`); `:focus-visible`; `label` ligado ao input; botão só-ícone com `aria-label`; decorativo `alt=""` + `aria-hidden`; nada clicável em `div` sem `role`/teclado; erros com `aria-describedby` + `role=alert`; sem `tabindex` positivo.
3. **Toque:** alvos ≥ 44 px, 8 px entre alvos; hover nunca é o único gatilho.
4. **Layout:** corpo ≥ 16 px; espaçamento 4/8/16/24/48/96; reservar dimensão de grids/imagens (sem CLS); sem rolagem horizontal em 375/768/1024/1440.
5. **Performance:** imagens via `img_qa.py web` (WebP/AVIF sem metadados), `loading=lazy` abaixo da dobra.
6. Revisão pelo **render** nas larguras-alvo, não pela leitura do código.

## C. Motion (HTML, Remotion, vídeo)
- Animar só `transform` e `opacity`. Durações 0.08 / 0.18 / 0.35 / 0.6 / 1.0 s; escala 0.95–1.04; stagger 0.05–0.10 s.
- Movimento só se chama atenção, mostra estado ou dá continuidade. `prefers-reduced-motion`: só fade ≤ 0.2 s.
- Corte no beat: 60/BPM s por batida (30 fps: 1800/BPM frames). Um acento de cor por cena.

## D. Deck
- Cada slide cabe na tela (`100dvh`, `overflow:hidden`); conteúdo demais = dividir, nunca encolher a fonte.
- Densidade: título + subtítulo; 4–6 bullets; grid ≤ 6 cards; 1 citação; 1 imagem principal.
- Ritmo: nunca 3+ slides seguidos no mesmo fundo; deck de 8+ slides tem ≥ 1 abertura escura e ≥ 1 clara.
- Navegação: setas/Espaço/PageDown, Home/End, swipe ≥ 50 px, `aria-current` no indicador.
- Conferir em 1920×1080, 1280×720 e 375×667.

## E. Copy de anúncio e social
- Uma afirmação concreta por peça; especificidade > adjetivo. Vídeo curto: problema ou resultado nos 3 primeiros segundos.
- Carrossel: as legendas dos cards leem como uma frase contínua.
- Proibido (salvo na copy do cliente): "game-changer", "revolucionário", "de ponta", "no cenário atual", "não é X, é Y", falsa curiosidade, pergunta-isca.
- Copy do cliente é literal: estas regras **apontam** risco em 1 linha, não reescrevem.

## F. Imagem por IA
- Conferir contra a mestra: silhueta, cores, proporção, itens proibidos (`produto.md`). Falhou: trocar seed ou subir `--ref` de ângulo; 3 tentativas e parar.
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
Nota 0–10 em 5 eixos, cada nota citando um elemento da peça: **Conceito** (bate com o KV/briefing) · **Hierarquia** · **Detalhe** (alinhamento, acentos, kerning, safe zone) · **Função** (lê em 1 s no feed / CTA claro) · **Gesto** (o 20%).
Faixas: 0–4 quebrado · 5–6 funcional · 7–8 forte · 9–10 excepcional. A nota final é a **pior faixa sustentada**, não a média; média > 8 é suspeita. Qualquer eixo < 7: corrigir uma vez antes de mostrar (poucas correções decisivas, não retoque geral). Mostrar ao usuário só 1 linha: `Crítica: 8·7·8·9·7 → forte (ajustei hierarquia)`.

## I. Tipografia e hierarquia (estático, LP, deck)
- 1 ponto de entrada dominante; no máximo 3 níveis visíveis por tela. Peso **salta** (400→700), não escorrega (400/500/600/700 juntos).
- Até 2 famílias; 6–8 tamanhos por peça, razão 1.2–1.25.
- Entrelinha: título 1.0–1.2; corpo 1.4–1.6. Nunca título > 1.3 nem corpo < 1.3.
- Tracking: CAIXA ALTA +0.06 a +0.1 em (obrigatório); títulos ≥ 32 px −0.01 a −0.02 em; display ≥ 48 px −0.02 a −0.03 em; corpo 0.
- Linha de leitura 50–75 caracteres (`max-width:65ch`).
- Fundo: preto puro e branco puro só se o KV mandar; senão `#0F0F0F` / `#FAFAFA`.

