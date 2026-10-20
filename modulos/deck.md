# Módulo Deck — Apresentações e Relatórios Executivos 1600×900 (HTML Single-File Autônomo)

Módulo unificado para criação de apresentações comerciais, propostas estratégicas e decks executivos de alto impacto em HTML/CSS/JS único (`1600×900`, proporção `16:9`), 100% portáteis (offline) e fiéis ao `design_system.md` do cliente.

---

## 1. Geometria Canônica, Escala Responsiva e Portabilidade

- **Canvas nativo fixo:** `width: 1600px; height: 900px` (`overflow: hidden` em cada `<section class="slide">`). Margens seguras internas: `76px` topo, `96px` laterais, `108px` base (reservando a faixa inferior para logo de rodapé a `32px` da base, paginação e controles circulares de `48px` a `25px` da base / `52px` da direita).
- **Centralização e Escala Matemática no Viewport (Obrigatória):** o deck nunca depende de zoom manual do navegador e nunca ultrapassa `scale(1)` em telas grandes:
```css
html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; }
#viewport { position: fixed; inset: 0; overflow: hidden; }
#deck {
  position: absolute;
  width: 1600px;
  height: 900px;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%) scale(var(--deck-scale, 1));
  transform-origin: center center;
}
```
```js
function fitDeck() {
  var vw = (window.visualViewport && window.visualViewport.width) || document.documentElement.clientWidth || window.innerWidth;
  var vh = (window.visualViewport && window.visualViewport.height) || document.documentElement.clientHeight || window.innerHeight;
  var scale = Math.max(0.1, Math.min((vw - 16) / 1600, (vh - 16) / 900, 1));
  document.getElementById('deck').style.setProperty('--deck-scale', scale);
}
window.addEventListener('resize', fitDeck);
if (window.visualViewport) window.visualViewport.addEventListener('resize', fitDeck);
fitDeck();
```
- **Escala Tipográfica Recomendada (`1600×900`):**
  - `h1`: `72px–88px`, `line-height: 0.98–1.05`, `letter-spacing: -0.04em a -0.055em`, peso `600–800`.
  - `h2`: `48px–60px`, `line-height: 1.02–1.08`, `letter-spacing: -0.035em a -0.045em`, peso `600–700` (nunca abaixo de `44px`).
  - `h3` (título de card): `22px–26px`, `line-height: 1.15`, peso `600` (nunca abaixo de `20px`).
  - `.lede` (abertura): `24px–27px`, `line-height: 1.42`; corpo de card ≥ `17px` (nunca diminuir fonte antes de ajustar largura, quebras de linha ou grid).
  - `.eyebrow` / badges / números de slide: `12px`, `font-weight: 700`, `letter-spacing: +0.09em a +0.14em`, `text-transform: uppercase`.
- **Portabilidade 100% Offline (Inlining de Logos e Grafismos):** antes de entregar o `index.html`, converter todas as logos e imagens locais para Data URIs Base64 (`data:image/png;base64,...` ou SVG inline) para que o arquivo funcione isoladamente ao ser enviado ao cliente. Esconder a logo de rodapé na capa e no slide de encerramento quando a logo principal já estiver em destaque no centro/topo.

---

## 2. Seleção Semântica de Arquétipos e Cadência de Fundos

Escolher o arquétipo de cada slide pela **estrutura semântica da copy aprovada** (proibido repetir o mesmo grid de cards em todos os slides):

| Conteúdo aprovado | Arquétipo visual obrigatório |
|---|---|
| 1 afirmação decisiva de impacto | **Statement / Hero:** 1 frase dominante + 1 sistema abstrato/geométrico do KV |
| 4 capacidades ou pilares | **Grid 2×2** de cards com ícones |
| 5 capacidades ou pilares | **Grid Assimétrico:** 2×2 + 1 card vertical destacado à direita |
| 6 capacidades ou pilares | **Grid 3×2** de cards com ícones |
| Antes × Depois | **Split Flow:** 2 painéis grandes com fluxo direcional |
| Cenário antigo × Solução nova | **Comparison:** tabela comparativa de 2 colunas com altura generosa ou contraste lado a lado |
| Etapas sequenciais (até 6) | **Process / Timeline:** etapas horizontais conectadas (ou 2 linhas se > 6), alturas iguais, ícone por etapa e destaque no resultado final |
| Inteligência central + unidades/pontas | **Hub & Network:** círculo radial central + órbita tracejada + nós com classes posicionais explícitas (`node-nw`, `node-ne`, `node-sw`, `node-se`, `node-s` — nunca usar `:nth-child` quando houver elementos irmãos não-nó) e flutuação assíncrona (`node-float` com delays negativos distintos) |
| Métricas e números (≤ 5) | **Metric Wall:** dígitos gigantes (`big-number`), 1 resultado em destaque e legenda do período confirmado |
| 1 métrica dominante + atividades | **Allocation Ring:** anel animado dominante + grid de bullets com ícones |
| Indicadores operacionais | **Mockup de Dashboard** no estilo do produto/KV |
| Preço e condição comercial | **Price Card** + painel lateral de condições/entregáveis |

- **Cadência e Ritmo de Fundos (4 tratamentos derivados do `design_system.md`):**
  - Alternar entre `.slide.hero` (cor/gradiente institucional de impacto na capa, statements e fechamento), `.slide` (base editorial de leitura), `.slide.depth` (fundo escuro de profundidade) e `.slide.spotlight` (contraste limpo de marca).
  - Se o KV do cliente for 100% Dark Mode (ex.: preto + ouro/neon), manter os mesmos 4 tratamentos variando a densidade e a iluminação de fundo (base dark editorial · hero com glow ascendente na cor de acento · depth com radial superior · spotlight em carvão `#101010` com halo superior).
  - **Regra de ritmo:** proibido mais de 2 slides consecutivos com o mesmo fundo **e** a mesma composição.

---

## 3. Guardrails de Copy, Tipografia e Integridade de Dados

1. **Copy literal e transformações permitidas:** usar exclusivamente os fatos, números e argumentos fornecidos. É permitido quebrar frases longas em blocos paralelos, transformar listas em cards com ícones e converter pares em tabelas comparativas — mantendo 100% dos conceitos originais. É **proibido** inventar subtítulos explicativos, batizar metodologias não citadas, inferir números/eixos/períodos ou criar CTAs finais genéricos não presentes na copy.
2. **Higiene tipográfica obrigatória nos slides:**
   - **Proibido hífen solto em prosa (` - `), meia-risca (`–`), travessão (`—`) e til de aproximação (`~`):** substituir por dois-pontos, vírgula, ponto final ou separação visual em colunas/cards.
   - **Zero metalinguagem:** nunca escrever *"neste slide"*, *"nesta apresentação"*, *"como podemos ver"*, *"o layout mostra"* ou mencionar IA/prompts.
   - **Todo item de lista (`<li>`) exige ícone SVG:** usar apenas ícones SVG outline (`viewBox="0 0 24 24"`, `stroke-width: 2–2.3px`, `stroke-linecap: round`) dentro de contêineres de `50–68px`. Proibido bullet padrão sem ícone e proibido emojis.
   - **Zero palavras órfãs (viúvas):** nenhuma headline (`h1/h2/h3`) ou parágrafo pode terminar com 1 única palavra isolada na última linha. Ajustar com `<br>` semântico ou `max-width` e revalidar após o carregamento das fontes.
   - **Zero parágrafos longos (> 230 caracteres):** converter em estrutura visual (cards, comparativo, fluxo ou métricas).

---

## 4. Interação, QA Estático e Inspeção Visual Obrigatória

- **Navegação e Acessibilidade:** botões anterior/próximo (`data-testid="prev-slide"` e `data-testid="next-slide"`, desabilitados no primeiro e no último slide), setas do teclado (`ArrowLeft`/`ArrowRight`), `Space`/`PageDown`, `Home`/`End`, swipe touch ≥ 50 px, barra `.progress-fill` chegando a 100% no último slide, contador atualizado e `@media (prefers-reduced-motion: reduce)` desativando animações contínuas.
- **Verificação Obrigatória antes da entrega (`qualidade.md` §D):**
  1. Validar ausência de `–`, `—`, `~`, ` - `, placeholders, metalinguagem, `<li>` sem `<svg>` e logos externas não embutidas em base64.
  2. Testar centralização matemática (`left margin == right margin ±1px` e `top margin == bottom margin ±1px`, sem cortar bordas) nos 4 viewports canônicos: **`1024×768`**, **`1366×768`**, **`1600×900`** e **`1920×1080`**.
  3. Renderizar os slides em `1600×900`, montar prancha de contato (`python assets\img_qa.py prancha Trabalho\slides\*.png -o Trabalho\_prancha_deck.jpg`) e inspecionar individualmente slides densos (tabelas, processos, 5+ cards, hub) garantindo zero espaço morto acidental, zero colisão com o rodapé e console JS limpo.
