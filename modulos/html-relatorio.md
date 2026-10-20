# Submódulo HTML — Página-relatório

- **Decisões antes de escrever:**
  1. definir público, contexto e ação esperada;
  2. agrupar o conteúdo em capítulos com uma conclusão cada;
  3. escolher **um padrão visual por capítulo**: cards de métrica, diagrama, matriz comparativa, linha do tempo, riscos ou tabela.
- **Cores com significado fixo** na página inteira. Prioridade só por etiqueta (P0/P1), nunca por cor.
- **Componentes:**
  - **Hero:** eyebrow, título, subtítulo de até 2 frases e 2–6 métricas distintas.
  - **Navegação fixa:** obrigatória a partir de 4 seções.
  - **Grids de cards:** 3–6 por grupo. Acima disso, agrupar ou usar tabela. Card com até 3 linhas e uma ideia só.
- **Responsividade e impressão:**
  - abaixo de ~980 px, grids de 4 colunas viram 2 colunas;
  - abaixo de 640 px, tudo em 1 coluna;
  - `@media print` esconde a navegação, tira sombras e usa `break-inside: avoid` nas seções.
- **O que não fazer:** cores aleatórias, gradientes decorativos, lista longa achatada e afirmar como pronto algo que está em andamento.
- **Verificação final:** abre offline, imprime em PDF sem cortes e os links da navegação levam às seções certas.
