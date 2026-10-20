# Módulo HTML — LP, Site, Extração, Formulário, Print e Relatório

Módulo único e completo para qualquer entrega em HTML. Assets em `<AG>\assets\`: `base_lp.html` (base testada: blindagem, SEO, máscara, UTMs, webhook, skip-link), `qa_html.py` (QA obrigatório), `validacao-forms.js/.css` (CPF, CNPJ, UF/cidade).

---

## 1. Fluxo obrigatório e Modos

1. **Topo** (núcleo §1) + 1 linha: seções na ordem de rolagem, objetivo de conversão e material faltante.
2. **Travar a base** antes do conteúdo: tokens de cor e tipografia vindos do `design_system.md` e escala de espaçamento. Partir de `base_lp.html` sempre que for página nova.
3. **Construir seção por seção**, cada uma com um objetivo só.
4. **Rodar o QA** (`qa_html.py`) e corrigir até zerar as FALHAS. Abrir os screenshots de 375 e 1440 px e conferir com os olhos.
5. **Entregar** pelo núcleo §2, com a lista do que mudou e as pendências.

No ajuste de um arquivo existente, mudar só o pedido e preservar todo o resto byte a byte.

| Modo | Quando | Regra principal |
|---|---|---|
| **Criar** | LP ou site novo | Base + `design_system.md` (§3 e §4 abaixo). Visual distinto e intencional, nada de template genérico. |
| **Extrair / clonar** | "copia essa página", URL de construtor ou site | Cópia exata do que for acessível (núcleo §6): HTML, CSS, variáveis, imagens e logo reais; sem redesenhar. → `html-extrair.md` §1 |
| **Recriar de print / vídeo** | Só existe imagem ou gravação | → `html-extrair.md` §3 |
| **Embed** | Bloco `</>` de construtor visual | → `html-extrair.md` §2 |
| **Ajuste** | Mudança pontual | Alterar só o pedido (núcleo §2: mecânico) e listar o que mudou. |
| **Página-relatório** | Relatório, roadmap, resultados em HTML | → `html-relatorio.md` |

Página que não abre (login, bloqueio): pedir o HTML salvo (Ctrl+S, "página completa") ou um print. Nunca adivinhar.

---

## 2. Arquivo único, anti-mojibake e blindagem

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

---

## 3. Criar LP / Site novo (Conversão, Visual, Tipografia, CWV, SEO, A11y)

### Estrutura de LP que converte
O **texto** é sempre a copy aprovada (lei 4 do núcleo): se o briefing não trouxer o texto de uma seção, pedir, nunca inventar. Ordem de rolagem de referência (ajustar à temperatura do tráfego — frio: mais longa com educação e prova; quente: mais curta com oferta e CTA cedo):
1. **Hero:** promessa clara em 3–5 segundos (resultado + para quem), subtítulo, CTA principal visível sem rolar no desktop e no mobile, e prova curta se houver.
2. **Problema / dor:** o cenário atual do público.
3. **Solução / mecanismo:** o que é diferente nesta oferta.
4. **Benefícios:** escritos como resultado ("para você…"), não como característica.
5. **Prova:** depoimentos reais, números confirmados, logos de clientes e certificações confirmadas.
6. **Oferta / como funciona:** passos, o que está incluso e condição comercial.
7. **Objeções / FAQ:** preço, confiança, tempo, complexidade.
8. **CTA final** + formulário ou botão. Repetir o CTA a cada 2–3 seções em páginas longas.

Checagem: o que chama a atenção primeiro é a promessa ou o CTA? Há um único objetivo por página? Existe atrito desnecessário (campos demais ou links de fuga)?

### Direção visual
- **Uma ideia forte por página**, vinda do `design_system.md` (ou consultada em `engines\uiux\scripts\search.py "<segmento>" --domain brand`). Evitar layouts genéricos (texto à esquerda e imagem à direita repetido em todas as seções, hero só com ícone e texto) sem um tratamento próprio.
- **Paleta e Escassez Cromática:** as cores da KV, com 3–5 cores mais os neutros. O acento primário é cirúrgico (marca, CTA principal, foco e destaque de prioridade máxima); nunca usar cor de acento como preenchimento decorativo de seção inteira sem previsão no KV.
- **Superfícies e acento:** U4 do núcleo; no dark, o próprio canvas é o espaço negativo e as seções se separam por elevação.
- **Espaçamento:** U5; padding de cards `24px` (features/pricing), `32px` (depoimentos), `48px` (banners de CTA).
- **Raio e sombra** seguem a KV (escala consistente por componente: chips `4px`, botões/inputs `6–8px`, cards `12–16px`, pills `9999px`).
- **Imagens:** ordem da lei 5 do núcleo. Nunca entregar com placeholder (`placehold.co`, `picsum`, lorem). Imagem gerada por IA fica salva em `IA\`.
- **Microinterações e Matriz de Estados:** definir explicitamente `default`, `:hover`, `:active` (pressed), `:focus-visible` e `:disabled` em todo elemento interativo, com transições de 150–300 ms.
- **Teste final:** a página parece feita sob medida para essa marca? Se servisse para qualquer cliente trocando só o logo, iterar.

### Tipografia
- **Texto corrido:** 16–20 px (`clamp(1rem, 0.95rem + 0.3vw, 1.125rem)`), line-height 1.45–1.6 e no máximo `65ch` de largura.
- **Escala, entrelinha e tracking:** U3 do núcleo; tamanhos com `clamp`, nunca `vw` sozinho (quebra o zoom).
- **Famílias:** U3; `mono` só para código, IDs e dados tabulares.
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
- Contraste e alvos de toque: U1.
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
- **Webhook:** `POST` `application/x-www-form-urlencoded` para a URL registrada em `design_system.md` (seção Inteligência); sem URL, deixar o placeholder e avisar. Nunca inventar URL. Em fluxos com **gates de qualificação B2B** (onde uma resposta desqualifica o lead no meio do form), disparar apenas Analytics/dataLayer + webhook com `qualificacao: "desqualificado"` nos desqualificados, reservando o pixel de conversão principal (`Lead` / MQL) exclusivamente para leads qualificados.
- **Estabilidade Mobile-First do Form (`validacao-forms.css`):** (1) reservar sempre a altura da mensagem de erro abaixo de cada input (`min-height: 16px` no `.form-msg` criado na carga) para o layout nunca "pular" ao validar; (2) travar altura máxima do form (`max-height: min(88svh, 680px)`) com rolagem interna no corpo (`overflow-y: auto; overscroll-behavior: contain`); (3) manter o botão de submit sempre visível em rodapé colado (`position: sticky; bottom: 0`); (4) inputs com `min-height: 44px` e `font-size: 16px` (evita zoom automático no iOS).
- **Comportamento:** botão travado no envio, mensagem de sucesso ou erro, honeypot, `autocomplete` correto e erro por campo.
- **Enquadramento em caixa/card (especialmente no mobile):** quando o formulário estiver sobre um card ou moldura (div própria ou elemento de fundo absoluto em construtores), nunca deixar os inputs/botão colados na borda ou da mesma largura da caixa. Garantir caixa centralizada e respiro interno igual nos 4 lados (`24px` no mobile, `32–40px` no desktop), alinhando cabeçalho do card, campos e botão na mesma largura útil interna e ajustando a altura do card para abraçar até o fim do botão com o mesmo padding inferior. Unificar peso da fonte, seta lateral e hover do botão de submit com os demais CTAs da LP.
- **Campos:** só os necessários. Cada campo a mais reduz a conversão.

---

## 5. QA obrigatório antes de entregar

**1. Rodar o script:**
```
python <AG>\assets\qa_html.py <arquivo.html> --saida <pasta da solicitação>\Trabalho\qa
```
- Na nuvem: trazer o `qa_html.py` da pasta raiz e rodar no ambiente de trabalho com Playwright.
- Ele confere bytes não-ASCII, mojibake, arquivo único, placeholders, SEO/meta, H1 único, alt, labels, rolagem horizontal em 375/768/1440, faixa entre blocos, H1 visível com e sem JS, erros de JS, alvos de toque, contraste e máscara de telefone, e gera screenshots.

**2. Zerar as FALHAS.** Avisos são resolvidos ou justificados na entrega. Placeholders de template e webhook pendente devem ser avisados.

**3. Olhar os screenshots** (375 e 1440 px) e conferir: hierarquia, respiro, alinhamento, estados de hover e foco, textos longos e curtos, e imagens sem distorção.

**4. Antes de publicar:** nenhum lorem ou placeholder; todos os links funcionam; favicon e og:image finais; política de privacidade se houver coleta de dados; ano e contatos corretos.
