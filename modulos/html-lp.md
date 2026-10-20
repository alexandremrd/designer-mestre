# Submódulo HTML — Criar LP/site

Lido junto com `html.md` quando a página é nova.

## Estrutura de LP que converte

Esta seção define a **estrutura** da página. O **texto** continua sendo a copy aprovada (lei 2 do núcleo): se o briefing não trouxer o texto de uma seção, pedir, nunca inventar.

Ordem de rolagem de referência (ajustar à temperatura do tráfego):
1. **Hero:** promessa clara em 3–5 segundos (resultado + para quem), subtítulo, CTA principal visível sem rolar no desktop e no mobile, e prova curta se houver.
2. **Problema / dor:** o cenário atual do público.
3. **Solução / mecanismo:** o que é diferente nesta oferta.
4. **Benefícios:** escritos como resultado ("para você…"), não como característica.
5. **Prova:** depoimentos reais, números confirmados, logos de clientes e certificações confirmadas.
6. **Oferta / como funciona:** passos, o que está incluso e condição comercial.
7. **Objeções / FAQ:** preço, confiança, tempo, complexidade.
8. **CTA final** + formulário ou botão. Repetir o CTA a cada 2–3 seções em páginas longas.

Temperatura do tráfego:
- **frio:** página mais longa, com mais prova e educação;
- **quente:** página mais curta, com oferta e CTA cedo.

Checagem de conversão:
- o que chama a atenção primeiro é a promessa ou o CTA?
- há um único objetivo por página?
- existe atrito desnecessário, como campos demais no formulário ou links que levam para fora?

---

## Direção visual

- **Uma ideia forte por página**, vinda do `design_system.md`. Evitar layouts genéricos (texto à esquerda e imagem à direita repetido em todas as seções, hero só com ícone e texto) sem um tratamento próprio.
- **Paleta:** as cores da KV, com 3–5 cores mais os neutros. Cor tem significado: CTA numa cor, informação em outra. Nunca usar cor só para decorar.
- **Espaçamento:** grade de 8 px (8, 16, 24, 32, 48, 64, 96). Mesmo respiro entre seções equivalentes.
- **Raio e sombra** seguem a KV. Sem KV, usar sombras sutis e no máximo 2 raios diferentes na página.
- **Imagens:** a ordem de busca e as regras de `Compartilhada\Imagens\` estão no núcleo (seção 3). Nunca entregar com placeholder (`placehold.co`, `picsum`, lorem). Imagem gerada por IA fica salva em `IA\`.
- **Microinterações:** hover, foco e estado ativo em todo elemento clicável, com transições de 150–300 ms. Animação de entrada é discreta e sempre segura (ver `html.md`).
- **Teste final de qualidade:** a página parece feita sob medida para essa marca? Se servisse para qualquer cliente trocando só o logo, iterar.

---

## Tipografia

- **Texto corrido:** 16–20 px (`clamp(1rem, 0.95rem + 0.3vw, 1.125rem)`), line-height 1.4–1.6 e no máximo `65ch` de largura.
- **Escala:** proporção fixa de 1.2–1.333 a partir do corpo. Sem tamanhos arbitrários. Exemplo com corpo 18 e proporção 1.25: H3 22, H2 28, H1 36–56 (com `clamp`).
- **Famílias:** no máximo 2 (a da KV mais a substituta do Google Fonts registrada). Contraste entre títulos e texto vem de peso e tamanho, não de uma terceira fonte.
- **Propriedades:**
  - `text-wrap: balance` nos títulos e `text-wrap: pretty` nos parágrafos;
  - `font-kerning: normal`;
  - `letter-spacing` só em texto em CAIXA ALTA (0.05–0.12em);
  - números de tabela com `font-variant-numeric: tabular-nums`.
- **Carregamento:**
  - `preconnect` para fonts.googleapis/gstatic e `display=swap`;
  - só os pesos usados;
  - fallback de sistema na pilha de fontes.
- Nunca usar `vw` sozinho em tamanho de fonte: quebra o zoom. Usar `clamp()`.

---

## Desempenho (Core Web Vitals)

Metas: LCP < 2,5 s, CLS < 0,1, INP < 200 ms.

- **Imagem principal do hero:** `fetchpriority="high"`, sem `loading="lazy"`, com `width` e `height`.
- **Demais imagens:** `loading="lazy" decoding="async"`, com `width`, `height` e/ou `aspect-ratio`, para não deslocar o layout.
- **Formatos:** WebP ou AVIF quando o construtor aceitar; JPG para foto e SVG para ícone. Nunca uma imagem maior que 2× o tamanho exibido.
- **Scripts:** JS no fim do `<body>`. Sem bibliotecas pesadas para efeitos que CSS resolve (jQuery, AOS, GSAP só se o pedido exigir).
- **Vídeos de fundo:** `muted playsinline loop preload="metadata"` e `poster`. No mobile, considerar só o poster.

---

## SEO e compartilhamento

- `<html lang="pt-BR">`, um único `<h1>` e títulos em hierarquia, sem pular nível.
- `<title>` com até 60 caracteres (promessa + marca) e `meta description` com 150–160.
- `canonical`, `og:title`, `og:description`, `og:image` (1200×630 hospedada) e favicon.
- Dados estruturados JSON-LD **só com informação real**: `Organization` com nome, site e logo, e `FAQPage` quando a página tiver FAQ.
- Links externos com `rel="noopener"` quando abrem em nova aba.

---

## Acessibilidade (WCAG 2.1 AA)

- Contraste de no mínimo 4.5:1 no texto (3:1 em texto de 24 px ou mais, ou bold de 18,66 px ou mais).
- Todo campo com `<label>` visível, sem depender só do placeholder. Erros anunciados com `aria-live`.
- `alt` descritivo em imagem com conteúdo e `alt=""` em imagem decorativa.
- Link "pular para o formulário/conteúdo", ordem de tab lógica e foco sempre visível.
- Alvos de toque de pelo menos 44×44 px no mobile.
- Nenhuma informação transmitida só por cor.
