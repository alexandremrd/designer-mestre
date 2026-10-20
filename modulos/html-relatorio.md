# Anexo HTML · Página-relatório
Carregado só junto com `html.md`. Para slides navegáveis use `deck.md`.

## Página-relatório (Presentation HTML & Executive Dashboards)

- **Ordem de Decisão (inviolável — nunca escrever conteúdo antes de travar os passos 1 a 4):**
  1. **Modo da Página (`Page Mode`):** definir público, contexto e narrativa antes do HTML (`summary-to-detail` para inventários/status; `chronological` para roadmaps/migrações; `problem-to-solution` para propostas; `capability-map` para arquitetura/plataforma; `comparison` para matrizes e antes/depois; `layered-architecture` para visões física/lógica/operacional).
  2. **Fluxo de Capítulos (`Chapter Flow`):** agrupar o material em seções com 1 missão clara cada (em documentos longos > 5.000 palavras, montar o plano de capítulos antes de redigir).
  3. **Padrão Visual Dominante por Capítulo:** atribuir 1 padrão visual a cada seção (grid de 4–5 cards de resumo com volume de texto equilibrado, diagrama de arquitetura em 3 colunas `left context → center detail → right context` com `align-items: stretch`, matriz comparativa, linha do tempo, registro de riscos ou tabela densa).
  4. **Mapeamento Semântico de Cores (travado uma única vez na página):** a mesma cor deve significar sempre a mesma categoria em todas as seções (ex.: azul = produção/ativo; verde = compartilhado/concluído; laranja = em andamento/assíncrono; roxo = serviço externo; amarelo = persistência/dados; vermelho = risco/alerta). Prioridade usa etiqueta explícita (`P0`, `P1`), nunca apenas cor.
  5. **Preenchimento de Conteúdo:** compacto, escaneável e 100% auto-contido (offline).
- **Componentes e Responsividade:** Hero enxuto (eyebrow, título, subtítulo ≤ 2 frases e 4–6 métricas numéricas de status); Navegação horizontal `sticky` (obrigatória a partir de 4 seções); espaçamento vertical uniforme entre seções (`20–24px`); abaixo de `980px`, grids de 4 colunas viram 2 colunas; abaixo de `640px`, 1 coluna; `@media print` oculta navegação, remove sombras e aplica `break-inside: avoid`.
- **Verificação final:** abre offline, imprime em PDF sem cortes e os links da navegação levam às seções certas.
- **Conteúdo:** abrir pelo resultado, estado atual ou decisão pedida; rótulo com nome de negócio (ID técnico só como texto secundário); cada item aparece em 1 lugar só.
- **Status:** distinguir implantado · em andamento · planejado; nunca "em produção" sem fonte. Cor = categoria, nunca prioridade.
- **Cards:** ≤ 3 linhas; > 6 do mesmo tipo = agrupar ou tabela; planos, pílula só funcional. Diagrama em 3 colunas: larguras iguais, mesma altura por linha, h3 em 1 linha.
- **Gráficos (SVG inline, nunca lib por CDN):** tendência = linha; comparação = barra (3–12 categorias); proporção = rosca só até 5; rótulo direto com unidade; nunca só cor; dado ≥ 3:1 contra o fundo.
