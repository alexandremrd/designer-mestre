# Módulo Deck — Apresentações, Narrativas Visuais e Bancada Iterável

Módulo unificado para criar apresentações e narrativas visuais de acordo com o briefing e o sistema do cliente. Separe a bancada iterável do arquivo final. HTML/CSS/JS pixel-perfect (canvas 1600×900, arquivo único, sem framework nem build) é o padrão de autoria e entrega; PowerPoint (`python-pptx`), PDF ou formato nativo entram quando o usuário pedir ou o uso exigir.

---

## 1. Definir a bancada e o canvas

- **Padrão:** slides em HTML pixel-perfect, conferido em relação ao briefing. Outro formato só por pedido ou necessidade real, sem trocar o padrão em silêncio.
- **Escolha guiada pela utilização:** identifique audiência, contexto de apresentação, conteúdo disponível, destino final, necessidade de edição, colaboração, impressão e capacidade do ambiente. Não transforme o nome "deck" em HTML, PPTX, proporção, quantidade de slides ou layout predeterminados. A bancada pode ser independente do arquivo que será exportado.
- **Preview no Browser:** quando estiver disponível, abra um canvas visual com a peça em andamento e ajuste HTML/CSS/JS ou conteúdo embutido ao iterar. Um canvas `16:9` é útil para slides widescreen, mas use proporção/dimensão provisória quando houver incerteza; não confunda o canvas do preview com a página ou slide final.
- **PowerPoint:** use `python-pptx` quando o usuário escolher PPTX ou quando requisitos de editabilidade/interoperabilidade justificarem propor esse formato. Crie elementos nativos sempre que possível; preservar imagem/render como imagem é opção apenas quando essa for a escolha/necessidade, não mecanismo automático de composição.
- **Outros meios:** PDF é exportação, não fonte editável; use ferramenta de conversão disponível apenas após o formato e qualidade requeridos estarem definidos. Figma nativo só quando pedido, pela rota `figma.md`.
- **Dimensões e segurança:** use o template/tokens do cliente apenas quando aprovados e pertinentes; caso contrário defina canvas e margens pela proporção, quantidade/tipo de conteúdo, ambiente de exibição e requisitos atuais de destino. Nunca confunda DPI de metadado com resolução física final. Para impressão, confirme trim, bleed, escala, perfil e prova com a gráfica/conferência.
- **Referência de preview widescreen (opcional):** quando 16:9 fizer sentido, este CSS de escala pode ajudar a inspecionar um slide no viewport; não é requisito de autoria ou exportação:
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
- **Tipografia e respiro:** escolha pela hierarquia da narrativa, tamanho real de apresentação, distância/viewport, conteúdo e tokens; evite reduzir o tipo apenas para forçar conteúdo em um slide. As medidas antigas de 1600×900 podem ser usadas como referência quando esse for o canvas escolhido, não como pisos/tetos universais.
- **Assets e arquivos:** inlining ajuda na portabilidade HTML/offline, mas não é obrigatório para preview ou quando caminhos/ativos externos forem parte da edição. Não embuta fontes/logos nem altere licenças sem necessidade.
- `assets\base_deck.html` é uma base opcional para decks compatíveis com HTML; não precisa ser usada para uma direção visual diferente ou para PPTX.

---

## 2. Seleção Semântica de Arquétipos e Cadência de Fundos

Escolher estrutura e ritmo pela **história, conteúdo, audiência e direção visual**. As ideias abaixo são repertório de opções, não mapeamento obrigatório por contagem:

| Sinal de conteúdo | Estruturas que podem servir |
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

- **Ritmo:** contraste de composição, densidade, escala e fundo pode criar cadência; escolha pelo material e pela linguagem visual, não por número obrigatório de tratamentos nem por limite de slides iguais.
- **Argumento antes do layout:** liste o deck como afirmações (uma por slide, com a prova) e corte o slide sem afirmação; só então escolha a estrutura da tabela. A copy continua literal (§3). Revisão: passadas 1, 2, 4, 9 e 11 do roteiro de `qualidade.md` §H; transição entre slides pelo gate de `qualidade.md` §C (apresentação é momento raro).
- **Dados:** só transformar em gráfico os dados autorizados; seguir `html-relatorio.md` quando o artefato for relatório/dashboard e usar formas/técnicas adequadas ao conteúdo.
- **Espaço:** áreas vazias, respiro e composições assimétricas são escolhas legítimas; não ampliar cards ou preencher canvas só para eliminar espaço.

---

## 3. Guardrails de conteúdo e integridade de dados

1. **Copy literal e transformações permitidas:** usar exclusivamente os fatos, números e argumentos fornecidos. É permitido quebrar frases longas em blocos paralelos, transformar listas em cards com ícones e converter pares em tabelas comparativas — mantendo 100% dos conceitos originais. É **proibido** inventar subtítulos explicativos, batizar metodologias não citadas, inferir números/eixos/períodos ou criar CTAs finais genéricos não presentes na copy.
2. **Acabamento editorial (quando fizer diferença):** ajuste quebras, órfãs, contraste, espaçamento, densidade e hierarquia para o meio e para a audiência. Hífen, travessão, emoji, bullets, lista sem ícones, parágrafo longo ou metalinguagem não são falhas automáticas; corrija apenas quando enfraquecer a leitura, o tom ou a intenção.

---

## 3. Iterar, aprovar e exportar

- Apresente a composição no Browser canvas quando disponível; caso contrário, mostre a representação visual viável do meio de criação. Receba feedback e edite a bancada, sem exigir que cada iteração tenha formato final ou arquivo exportado.
- Requisitos de conteúdo, claims, números, fonte e marca precisam continuar fiéis ao briefing. Review é ferramenta de melhoria; não reprove por preferência de estilo ou falta de um arquétipo.
- Depois da aprovação, confirme formato final, dimensão, compatibilidade e destino que ainda não estejam definidos. Exportar apenas formatos escolhidos; uma imagem da bancada não é o PPTX nem o PDF final.
- **PPTX editável a partir do deck HTML pronto:** `python -I -X utf8 <AG>\assets\huashu\pptx_from_rendered.py deck.html -o deck.pptx --selector ".slide"` (huashu-design, MIT). Lê as posições já renderizadas, então não pede reescrever o HTML: texto vira caixa editável, card vira forma, SVG e canvas viram imagem, e a conferência de texto perdido roda sozinha. Usa Playwright, python-pptx e Pillow, que já existem aqui; `-X utf8` evita erro de console no Windows. O canvas de 1600×900 sai com 22,2×12,5 pol (1 px = 1 pt). Com modelo do cliente: `--template modelo.pptx --layout "<nome>" --skip-class logo`, e a logo vem do layout. O HTML segue sendo a fonte e a entrega primária; o PPTX é derivado. Detalhes e armadilhas de texto: `references\huashu\pptx-from-rendered-html.md`. A rota que exige reescrever o HTML com 4 restrições (sem degradê, sem fundo em texto) contradiz o pixel-perfect e não vem.
- Se o formato escolhido for PPTX, verificar abertura do arquivo, número de slides, dimensões, texto, assets locais e bounds das formas. A validação estrutural não comprova fidelidade visual: renderizar/revisar no PowerPoint ou exportador disponível sempre antes de entregar (`qualidade.md` §K). Se não houver conversor, declarar e não afirmar que houve revisão de render.
- Se o formato for HTML, seguir a rota de preview e inspeção do deck. Para páginas/sites que não sejam slides, `html.md` preserva o requisito pixel-perfect em relação à referência/briefing e aos viewports-alvo.
- Se o formato final for impressão, seguir requisitos exatos de organizador/gráfica; requisitos ausentes são uma pergunta após aprovação, não motivo para inventar dimensões, sangria, DPI, cor ou certificado.

## 4. Interação e QA do preview HTML (quando HTML for a bancada ou arquivo escolhido)

- **Navegação e Acessibilidade:** botões anterior/próximo (`data-testid="prev-slide"` e `data-testid="next-slide"`, desabilitados no primeiro e no último slide), setas do teclado (`ArrowLeft`/`ArrowRight`), `Space`/`PageDown`, `Home`/`End`, swipe touch ≥ 50 px, barra `.progress-fill` chegando a 100% no último slide, contador atualizado e `@media (prefers-reduced-motion: reduce)` desativando animações contínuas.
- Confirme funcionamento de navegação/controles apenas se implementados e pertinentes; inspecione o preview em viewports que representem seu uso, sem lista canônica compulsória.
- A validação existente (`assets\validate_deck.py`) assume convenções específicas de HTML/slide. Rode apenas quando o arquivo se encaixar nesse contrato, explique avisos válidos para a peça e não imponha travessão, ícone em cada lista, fundos rotativos ou palavras máximas como regra geral de design.
- Revise contraste, overflow, fontes, interações, metadados e console conforme o conteúdo e o uso. Em artefato fora de HTML, use a ferramenta de validação correspondente, se disponível.
