# Módulo HTML — núcleo (v3)

Todo pedido de HTML lê este arquivo. Depois, só o submódulo do modo:
- **Criar LP/site novo:** + `html-lp.md` (conversão, visual, tipografia, desempenho, SEO, acessibilidade)
- **Recriar de print/vídeo:** + `html-print.md`
- **Página-relatório:** + `html-relatorio.md`
- **Tem formulário:** + `html-form.md`
- **Extrair/clonar, embed, ajuste:** só este arquivo.

Assets em `<PASTA_DO_AGENTE>\assets\`: `base_lp.html` (base testada: blindagem, SEO, máscara, UTMs, webhook, skip-link), `qa_html.py` (QA obrigatório), `validacao-forms.js/.css` (CPF, CNPJ, UF/cidade). Créditos em `CREDITOS_HTML.md`.

## Fluxo obrigatório

1. **Planejar antes de escrever**, em 2–4 linhas: o modo (tabela Modos), as seções da página na ordem de rolagem, o objetivo de conversão e o que falta de material (núcleo, seção 3).
2. **Travar a base** antes do conteúdo: tokens de cor e tipografia vindos do `design_system.md` e escala de espaçamento. Partir de `base_lp.html` sempre que for página nova.
3. **Construir seção por seção**, cada uma com um objetivo só.
4. **Rodar o QA** (`qa_html.py`) e corrigir até zerar as FALHAS. Abrir os screenshots de 375 e 1440 px e conferir com os olhos.
5. **Entregar o arquivo inteiro**, nunca trechos, diff ou "o resto continua igual". Junto, a lista do que mudou e as pendências.

No ajuste de um arquivo existente, mudar só o pedido e preservar todo o resto byte a byte.

---

## Modos

| Modo | Quando | Regra principal |
|---|---|---|
| **Criar** | LP ou site novo | Base + `design_system.md`. Visual distinto e intencional, nada de template genérico. |
| **Extrair / clonar** | "copia essa página", URL do GreatPages | Cópia **exata**: baixar HTML, CSS, imagens e logo reais. Não redesenhar, não trocar fonte nem cor. Alterar só o que o briefing pedir. |
| **Recriar de print / vídeo** | Só existe imagem ou gravação | `html-print.md`. |
| **Embed** | Bloco `</>` do construtor | CSS escopado num wrapper com classe própria, JS encapsulado (IIFE), fundo transparente e responsivo. |
| **Ajuste** | Mudança pontual | Alterar só o pedido, devolver o arquivo inteiro e listar o que mudou. |
| **Página-relatório** | Relatório, roadmap, apresentação de resultados em HTML | `html-relatorio.md`. |

Página que não abre (login, bloqueio): pedir o HTML salvo (Ctrl+S, "página completa") ou um print. Nunca adivinhar.

---

## Arquivo único, anti-mojibake e prevenção de falhas

**Arquivo único (exigência do construtor):**
- Um `.html` com `<style>` e `<script>` internos. Sem `.css` ou `.js` externos, sem framework, sem build. Exceção: Google Fonts.
- Imagens:
  - grandes (fotos): URL absoluta já hospedada no construtor;
  - pequenas (ícones, logo): SVG inline ou base64.
  - Base64 acima de ~800 KB no total deixa a página pesada.
- Salvar o HTML final em `Exportados\` da pasta da solicitação `[LP]`. Versões de trabalho ficam em `Trabalho\`.

**Anti-mojibake:**
- conteúdo visível com entidades HTML (`&aacute; &atilde; &ccedil; &eacute; &ecirc; &otilde; &ndash; &nbsp;`…);
- strings em `<script>` com escape Unicode (`\u00e7`);
- comentários de CSS e JS só em ASCII.

O arquivo final tem **zero bytes não-ASCII**. O QA confere.

**Falhas de layout já conhecidas:**
- **Faixa branca entre blocos:**
  - `html,body{margin:0;padding:0}` com `background` definido;
  - `img,svg,video,iframe{display:block;max-width:100%}`;
  - seções separadas por `padding`, nunca por `margin` externa;
  - primeiro e último filho de cada seção com margem 0;
  - cada seção pinta o próprio fundo.
- **Título sumindo em animação:**
  - estado base sempre visível no CSS;
  - animação só com `.js-anim` adicionada pelo JS;
  - H1 anima só `transform`, nunca parte de `opacity:0`;
  - timeout de segurança que revela tudo;
  - `prefers-reduced-motion` desliga a animação.
- **Contorno azul em logo e links:** `img{border:0}`, `-webkit-tap-highlight-color:transparent`, sem outline no clique e `:focus-visible` visível na cor da marca.
- **Blindagem do construtor:** `*{box-sizing:border-box;margin:0;padding:0}`, `.centralizar:empty,[id^="b_"]:empty{display:none!important}`, `#site{width:100%!important;min-width:0!important}`, `[hidden]{display:none!important}`, `.form-feedback:empty{display:none!important}`.
- **Rolagem horizontal:** nenhum elemento com largura fixa maior que a tela. Grids com `minmax(0,1fr)`. Testar em 375, 768 e 1440 px.

---

## QA obrigatório antes de entregar

**1. Rodar o script:**
```
python <PASTA_DO_AGENTE>\assets\qa_html.py <arquivo.html> --saida <pasta da solicitação>\Trabalho\qa
```
- Na nuvem: trazer o `qa_html.py` da pasta raiz e rodar no ambiente de trabalho com Playwright.
- Ele confere bytes não-ASCII, mojibake, arquivo único, placeholders, SEO/meta, H1 único, alt, labels e rolagem horizontal em 375/768/1440.
- Também confere faixa entre blocos, H1 visível com e sem JS, erros de JS, alvos de toque, contraste e máscara de telefone.
- Gera screenshots.

**2. Zerar as FALHAS.** Avisos são resolvidos ou justificados na entrega. Placeholders de template e webhook pendente devem ser avisados.

**3. Olhar os screenshots** (375 e 1440 px) e conferir:
- hierarquia;
- respiro;
- alinhamento;
- estados de hover e foco;
- textos longos e curtos;
- imagens sem distorção.

**4. Antes de publicar:**
- nenhum lorem ou placeholder;
- todos os links funcionam;
- favicon e og:image finais;
- política de privacidade, se houver coleta de dados;
- ano e contatos corretos.
