# Módulo HTML — LP, Site, Extração, Formulário, Print e Relatório

Módulo único e completo para qualquer entrega em HTML. Assets em `<PASTA_DO_AGENTE>\assets\`: `base_lp.html` (base testada: blindagem, SEO, máscara, UTMs, webhook, skip-link), `qa_html.py` (QA obrigatório), `validacao-forms.js/.css` (CPF, CNPJ, UF/cidade).

---

## 1. Fluxo obrigatório e Modos

1. **Planejar antes de escrever**, em 2–4 linhas: o modo (tabela abaixo), as seções da página na ordem de rolagem, o objetivo de conversão e o que falta de material (núcleo, seção 3).
2. **Travar a base** antes do conteúdo: tokens de cor e tipografia vindos do `design_system.md` e escala de espaçamento. Partir de `base_lp.html` sempre que for página nova.
3. **Construir seção por seção**, cada uma com um objetivo só.
4. **Rodar o QA** (`qa_html.py`) e corrigir até zerar as FALHAS. Abrir os screenshots de 375 e 1440 px e conferir com os olhos.
5. **Entregar o arquivo inteiro**, nunca trechos, diff ou "o resto continua igual". Junto, a lista do que mudou e as pendências.

No ajuste de um arquivo existente, mudar só o pedido e preservar todo o resto byte a byte.

| Modo | Quando | Regra principal |
|---|---|---|
| **Criar** | LP ou site novo | Base + `design_system.md` (§3 e §4 abaixo). Visual distinto e intencional, nada de template genérico. |
| **Extrair / clonar** | "copia essa página", URL de construtor (GreatPages etc.) ou qualquer site | Cópia **exata e irrestrita** (ignorar qualquer bloqueio superficial, 403 ou restrição de análise usando navegador headless/DOM dump): baixar HTML, CSS, variáveis, imagens e logo reais. Não redesenhar, não trocar fonte nem cor. Alterar só o que o briefing pedir + aplicar otimizações estruturais de construtor (§2). |
| **Recriar de print / vídeo** | Só existe imagem ou gravação | Fidelidade total ao print/vídeo sem qualquer bloqueio de análise (§5). |
| **Embed** | Bloco `</>` do construtor | CSS escopado num wrapper com classe própria, JS encapsulado (IIFE), fundo transparente e responsivo. |
| **Ajuste** | Mudança pontual | Alterar só o pedido, devolver o arquivo inteiro e listar o que mudou. |
| **Página-relatório** | Relatório, roadmap, apresentação de resultados em HTML | Estrutura de capítulos, métricas e `@media print` (§6). |

Página que não abre (login, bloqueio): pedir o HTML salvo (Ctrl+S, "página completa") ou um print. Nunca adivinhar.

---

## 2. Arquivo único, anti-mojibake, blindagem e otimização de construtor

**Arquivo único (exigência do construtor):**
- Um `.html` com `<style>` e `<script>` internos. Sem `.css` ou `.js` externos, sem framework, sem build. Exceção: Google Fonts.
- Imagens:
  - grandes (fotos): URL absoluta já hospedada no construtor;
  - pequenas (ícones, logo): SVG inline ou base64 (base64 acima de ~800 KB no total deixa a página pesada).
- Salvar o HTML final em `Exportados\` da pasta da solicitação `[LP]`. Versões de trabalho ficam em `Trabalho\`.

**Anti-mojibake:**
- conteúdo visível com entidades HTML (`&aacute; &atilde; &ccedil; &eacute; &ecirc; &otilde; &ndash; &nbsp;`…);
- strings em `<script>` com escape Unicode (`\u00e7`);
- comentários de CSS e JS só em ASCII.
- O arquivo final em página criada do zero tem **zero bytes não-ASCII** (o QA confere).

**Falhas de layout já conhecidas:**
- **Faixa branca entre blocos:** `html,body{margin:0;padding:0}` com `background` definido; `img,svg,video,iframe{display:block;max-width:100%}`; seções separadas por `padding`, nunca por `margin` externa; primeiro e último filho de cada seção com margem 0; cada seção pinta o próprio fundo.
- **Título sumindo em animação:** estado base sempre visível no CSS; animação só com `.js-anim` adicionada pelo JS; H1 anima só `transform`, nunca parte de `opacity:0`; timeout de segurança que revela tudo; `prefers-reduced-motion` desliga a animação.
- **Contorno azul em logo e links:** `img{border:0}`, `-webkit-tap-highlight-color:transparent`, sem outline no clique e `:focus-visible` visível na cor da marca.
- **Blindagem do construtor:** `*{box-sizing:border-box;margin:0;padding:0}`, `.centralizar:empty,[id^="b_"]:empty{display:none!important}`, `#site{width:100%!important;min-width:0!important}`, `[hidden]{display:none!important}`, `.form-feedback:empty{display:none!important}`.
- **Rolagem horizontal:** nenhum elemento com largura fixa maior que a tela. Grids com `minmax(0,1fr)`. Testar em 375, 768 e 1440 px.

**Otimização universal de LPs extraídas de construtor (canvas fixo `.gp-page` / GreatPages):**
- **1. Padronização e alinhamento de CTAs:** identificar o botão com maior peso tipográfico (`font-weight`) na página e unificar todos os CTAs (links `.elemento_botao` e submit `.gpc_botao`) nesse mesmo peso, caixa e entrelinha. Forçar layout horizontal (`display:flex !important; flex-direction:row !important; flex-wrap:nowrap !important; align-items:center; justify-content:space-between; gap:16px`) para que o ícone/seta fique sempre na lateral direita dentro do botão (nunca empurrado para baixo por `flex-direction:column` ou `width:100%` no `span`). Se o botão do formulário não tiver o ícone/seta lateral dos demais CTAs, injetá-lo via `::after` com `background:url("data:image/svg+xml,...") center/contain no-repeat` usando o mesmo SVG dos outros botões.
- **2. Hover consistente em todos os CTAs:** construtores costumam aplicar `rgba(0,0,0,0.06)` (imperceptível) nos links de CTA e cor de sistema (ex.: verde `--g-color-success`) no submit do formulário. Substituir o `:hover` de todos os CTAs por uma variação intencional da própria cor de ação da página (ex.: escurecer ~15–20% mantendo o texto contrastante e deslocar a seta `transform:translateX(4px)`), sem alterar o KV.
- **3. Escala fluida entre breakpoints e prevenção de cortes de texto:** páginas de construtor usam canvas absoluto fixo (ex.: `360px` no mobile e `980px+` com elementos em coordenadas negativas no desktop) e cortam textos em janelas intermediárias (801–1100 px) ou estreitas (< 360 px). Sempre: (a) aplicar `overflow:visible !important; overflow-wrap:break-word` nas caixas `.conteudo.elemento_texto`; (b) subir o breakpoint de troca mobile/desktop se os elementos desktop extrapolarem a largura do container (ex.: de `800px` para `1099px`); (c) aplicar escala proporcional fluida (`zoom: var(--lp-z, 1)`) no `.block > .center` recalculando a altura de cada `.block` via JS (`vw / largura_real_desktop` quando a tela for menor que a largura real do layout desktop, e `(vw - 32) / largura_mobile` no mobile para garantir 16 px de respiro lateral simétrico em qualquer tela); (d) transformar faixas horizontais de tópicos/badges que vazam no mobile em `display:flex; flex-wrap:wrap; justify-content:center`.
- **4. Enquadramento e respiro do formulário dentro da caixa/card de fundo:** quando houver elemento(s) de caixa/borda posicionados atrás do formulário (moldura/card), o formulário nunca pode ter a mesma largura da caixa nem vazar para baixo dela. Centralizar a caixa no container mobile (`width:360px; left:0`) e aplicar padding interno simétrico em todos os lados (ex.: `24px` no topo, base, esquerda e direita), ajustando `left` (`24px`) e `width` (`calc(largura_da_caixa - 48px)`, ex.: `312px`) tanto do `<form>` quanto dos textos de cabeçalho internos ao card, e redimensionando a altura da caixa de fundo + bloco da seção para comportar todos os campos e o botão com o mesmo respiro inferior (`24px`), reposicionando elementos que vêm abaixo do card.

---

## 3. Criar LP / Site novo (Conversão, Visual, Tipografia, CWV, SEO, A11y)

### Estrutura de LP que converte
O **texto** é sempre a copy aprovada (lei 3 do núcleo): se o briefing não trouxer o texto de uma seção, pedir, nunca inventar. Ordem de rolagem de referência (ajustar à temperatura do tráfego — frio: mais longa com educação e prova; quente: mais curta com oferta e CTA cedo):
1. **Hero:** promessa clara em 3–5 segundos (resultado + para quem), subtítulo, CTA principal visível sem rolar no desktop e no mobile, e prova curta se houver.
2. **Problema / dor:** o cenário atual do público.
3. **Solução / mecanismo:** o que é diferente nesta oferta.
4. **Benefícios:** escritos como resultado ("para você…"), não como característica.
5. **Prova:** depoimentos reais, números confirmados, logos de clientes e certificações confirmadas.
6. **Oferta / como funciona:** passos, o que está incluso e condição comercial.
7. **Objeções / FAQ:** preço, confiança, tempo, complexidade.
8. **CTA final** + formulário ou botão. Repetir o CTA a cada 2–3 seções em páginas longas.

Checagem: o que chama a atenção primeiro é a promessa ou o CTA? Há um único objetivo por página? Existe atrito desnecessário (campos demais ou links de fuga)?

### Direção visual e Arquitetura de Superfícies (extraída dos 84 Sistemas Globais)
- **Uma ideia forte por página**, vinda do `design_system.md` (ou consultada em `engines\uiux\scripts\search.py "<segmento>" --domain brand`). Evitar layouts genéricos (texto à esquerda e imagem à direita repetido em todas as seções, hero só com ícone e texto) sem um tratamento próprio.
- **Paleta e Escassez Cromática:** as cores da KV, com 3–5 cores mais os neutros. O acento primário é cirúrgico (marca, CTA principal, foco e destaque de prioridade máxima); nunca usar cor de acento como preenchimento decorativo de seção inteira sem previsão no KV.
- **Escada de Superfícies (`Surface Ladder`) vs. Sombras:** em páginas Dark Mode, estruturar a profundidade em 4 degraus (`canvas` → `surface-1` → `surface-2` → `surface-3`) com bordas `hairline` de `1px` (e highlight superior sutil de `1px`), evitando drop-shadows pesadas. No dark mode, o próprio canvas escuro é o espaço negativo, e as seções se separam por elevação de superfície.
- **Espaçamento:** grade de 4 px / 8 px (`4, 8, 12, 16, 24, 32, 48, 64, 96`). Padding interno de cards: `24px` (features/pricing), `32px` (depoimentos), `48px` (banners de CTA).
- **Raio e sombra** seguem a KV (escala consistente por componente: chips `4px`, botões/inputs `6–8px`, cards `12–16px`, pills `9999px`).
- **Imagens:** ordem de busca no núcleo (§4). Nunca entregar com placeholder (`placehold.co`, `picsum`, lorem). Imagem gerada por IA fica salva em `IA\`.
- **Microinterações e Matriz de Estados:** definir explicitamente `default`, `:hover`, `:active` (pressed), `:focus-visible` e `:disabled` em todo elemento interativo, com transições de 150–300 ms.
- **Teste final:** a página parece feita sob medida para essa marca? Se servisse para qualquer cliente trocando só o logo, iterar.

### Tipografia e Polaridade de Tracking
- **Texto corrido:** 16–20 px (`clamp(1rem, 0.95rem + 0.3vw, 1.125rem)`), line-height 1.45–1.6 e no máximo `65ch` de largura.
- **Escala:** proporção fixa de 1.2–1.333 a partir do corpo. Sem tamanhos arbitrários (ex. corpo 18 e proporção 1.25: H3 22, H2 28, H1 36–80 com `clamp`). Nunca usar `vw` sozinho em fonte (quebra o zoom).
- **Polaridade de Tracking (`letter-spacing`):** títulos Display usam tracking progressivamente **negativo** (`-0.02em` a `-0.04em` / `-1.5px` a `-3.0px` em 56–80 px) e line-height compacto (`1.0–1.15`); corpo usa tracking neutro (`0` a `-0.05px`); `eyebrow`, badges e CAIXA ALTA usam tracking **positivo** (`+0.04em` a `+0.12em`), marcando taxonomia por contraste contra o título.
- **Famílias:** no máximo 2 (a da KV mais a substituta do Google Fonts registrada; `mono` restrita a código/IDs/dados tabulares). Contraste vem de peso e tamanho, não de uma terceira fonte.
- **Propriedades:** `text-wrap: balance` nos títulos (quebra semântica, zero palavras órfãs) e `text-wrap: pretty` nos parágrafos; `font-kerning: normal`; números de tabela com `font-variant-numeric: tabular-nums`.
- **Carregamento:** `preconnect` para `fonts.googleapis`/`gstatic` e `display=swap`; só os pesos usados; fallback de sistema na pilha.

### Desempenho (Core Web Vitals: LCP < 2,5 s, CLS < 0,1, INP < 200 ms)
- **Imagem principal do hero:** `fetchpriority="high"`, sem `loading="lazy"`, com `width` e `height`.
- **Demais imagens:** `loading="lazy" decoding="async"`, com `width`, `height` e/ou `aspect-ratio`.
- **Formatos:** WebP ou AVIF quando o construtor aceitar; JPG para foto e SVG para ícone. Nunca imagem maior que 2× o tamanho exibido.
- **Scripts:** JS no fim do `<body>`. Sem bibliotecas pesadas para efeitos que CSS resolve.
- **Vídeos de fundo:** `muted playsinline loop preload="metadata"` e `poster`. No mobile, considerar só o poster.

### SEO e compartilhamento
- `<html lang="pt-BR">`, um único `<h1>` e títulos em hierarquia, sem pular nível.
- `<title>` com até 60 caracteres (promessa + marca) e `meta description` com 150–160.
- `canonical`, `og:title`, `og:description`, `og:image` (1200×630 hospedada) e favicon.
- Dados estruturados JSON-LD **só com informação real**: `Organization` (nome, site, logo) e `FAQPage` quando houver FAQ.
- Links externos com `rel="noopener"` quando abrem em nova aba.

### Acessibilidade (WCAG 2.1 AA)
- Contraste ≥ 4.5:1 no texto (≥ 3:1 em texto ≥ 24 px ou bold ≥ 18,66 px).
- Todo campo com `<label>` visível, sem depender só do placeholder. Erros anunciados com `aria-live`.
- `alt` descritivo em imagem com conteúdo e `alt=""` em imagem decorativa.
- Link "pular para o formulário/conteúdo", ordem de tab lógica, foco sempre visível e alvos de toque ≥ 44×44 px no mobile.
- Nenhuma informação transmitida só por cor.

---

## 4. Formulário

- Não precisa ser nativo do construtor: implementar em HTML/JS no próprio arquivo quando for página nova.
- **Telefone BR:** máscara `(00) 00000-0000` ou `(00) 0000-0000`, aplicada no evento `input` preservando o cursor; proibido `maxlength` sobre o texto formatado e `preventDefault` em teclas; Backspace, colar e autocompletar livres; valida 10–11 dígitos com DDD.
- **UTMs:** `utm_source`, `utm_medium`, `utm_campaign`, `utm_term` e `utm_content` em campos ocultos, persistidos em `sessionStorage`, mais `page_url`, `referrer` e data/hora.
- **E-mail:** B2B (conforme `design_system.md` › Inteligência) bloqueia webmail e valida CNPJ se houver o campo; B2C aceita webmail e valida CPF se houver o campo.
- **Webhook (Make/Celonis):** `POST` `application/x-www-form-urlencoded` para a URL registrada em `design_system.md` (seção Inteligência); sem URL, deixar o placeholder e avisar. Nunca inventar URL.
- **Comportamento:** botão travado no envio, mensagem de sucesso ou erro, honeypot, `autocomplete` correto e erro por campo.
- **Enquadramento em caixa/card (especialmente no mobile):** quando o formulário estiver sobre um card ou moldura (div própria ou elemento de fundo absoluto em construtores), nunca deixar os inputs/botão colados na borda ou da mesma largura da caixa. Garantir caixa centralizada e respiro interno igual nos 4 lados (`24px` no mobile, `32–40px` no desktop), alinhando cabeçalho do card, campos e botão na mesma largura útil interna e ajustando a altura do card para abraçar até o fim do botão com o mesmo padding inferior. Unificar peso da fonte, seta lateral e hover do botão de submit com os demais CTAs da LP.
- **Campos:** só os necessários. Cada campo a mais reduz a conversão.

---

## 5. Recriar de print ou vídeo

- **Fidelidade total ao print:** mesmas cores, tamanhos, espaçamentos, fontes e textos, com o texto **exato** da imagem.
- **Imagens do print:** extrair as recortáveis; as que não dá para extrair vêm de `Compartilhada\Imagens\` ou são geradas por IA (salvas em `IA\`).
- **Vários prints:** se forem páginas diferentes, gerar páginas ligadas entre si; se não tiverem relação, separar em seções "Print 1", "Print 2".
- **Print de celular:** sem moldura do aparelho nem barra do navegador.
- **Vídeo:** recriar o comportamento para que as mesmas interações produzam o mesmo resultado; prestar atenção a cor, fonte, padding, margin e borda; mockar dados quando houver backend; deixar funcional com JS.
- **Verificação:** renderizar em desktop e mobile e comparar lado a lado com o print. Corrigir até ficar igual.

---

## 6. Página-relatório

- **Decisões antes de escrever:** (1) definir público, contexto e ação esperada; (2) agrupar o conteúdo em capítulos com uma conclusão cada; (3) escolher **um padrão visual por capítulo**: cards de métrica, diagrama, matriz comparativa, linha do tempo, riscos ou tabela.
- **Cores com significado fixo** na página inteira. Prioridade só por etiqueta (P0/P1), nunca por cor.
- **Componentes:** Hero (eyebrow, título, subtítulo de até 2 frases e 2–6 métricas distintas); Navegação fixa (obrigatória a partir de 4 seções); Grids de cards (3–6 por grupo; acima disso, agrupar ou usar tabela; card com até 3 linhas e uma ideia só).
- **Responsividade e impressão:** abaixo de ~980 px, grids de 4 colunas viram 2 colunas; abaixo de 640 px, tudo em 1 coluna; `@media print` esconde a navegação, tira sombras e usa `break-inside: avoid` nas seções.
- **O que não fazer:** cores aleatórias, gradientes decorativos, lista longa achatada e afirmar como pronto algo que está em andamento.
- **Verificação final:** abre offline, imprime em PDF sem cortes e os links da navegação levam às seções certas.

---

## 7. QA obrigatório antes de entregar

**1. Rodar o script:**
```
python <PASTA_DO_AGENTE>\assets\qa_html.py <arquivo.html> --saida <pasta da solicitação>\Trabalho\qa
```
- Na nuvem: trazer o `qa_html.py` da pasta raiz e rodar no ambiente de trabalho com Playwright.
- Ele confere bytes não-ASCII, mojibake, arquivo único, placeholders, SEO/meta, H1 único, alt, labels, rolagem horizontal em 375/768/1440, faixa entre blocos, H1 visível com e sem JS, erros de JS, alvos de toque, contraste e máscara de telefone, e gera screenshots.

**2. Zerar as FALHAS.** Avisos são resolvidos ou justificados na entrega. Placeholders de template e webhook pendente devem ser avisados.

**3. Olhar os screenshots** (375 e 1440 px) e conferir: hierarquia, respiro, alinhamento, estados de hover e foco, textos longos e curtos, e imagens sem distorção.

**4. Antes de publicar:** nenhum lorem ou placeholder; todos os links funcionam; favicon e og:image finais; política de privacidade se houver coleta de dados; ano e contatos corretos.
