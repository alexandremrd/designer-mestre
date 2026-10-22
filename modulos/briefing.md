# Módulo Briefing — extrair execução do ruído

Ativa com `/designer-mestre briefing` (aliases `brief`, `traduz`) ou automaticamente quando o pedido chega como briefing (texto longo, e-mail, áudio transcrito, PDF, doc, print de WhatsApp). Roda **antes** do módulo da tarefa. O resultado é uma lista curta do que executar, não um resumo do documento.

## 1. Regras
- **Triagem:** partir do pedido atual e extrair verbos de entrega (ex.: organizar acervo, analisar criativos, criar peça, exportar). Repetições, histórico de revisões, nomes de revisores, links e instruções gerais só entram se mudarem uma dessas ações. Pedido atual explícito vence material antigo; briefing é fonte, não lista automática de tarefas.
- **Pesos de direção (internos, sem imprimir a conta):** `5` = texto que irá **na peça** (tag, headline, apoio, CTA: dirige assunto, sujeito e cena); `2` = nota de arte específica da peça, usada somente se reforçar a copy; `1` = contexto geral do briefing; `0` = histórico, revisão já concluída, link ou pessoa apenas mencionada. Maior peso vence conflito criativo. KV, direitos, fidelidade e restrições explícitas do pedido atual são limites obrigatórios, não pontos. Pessoa, objeto ou exigência de foto citados fora da copy não viram sujeito obrigatório por repetição; só o pedido atual explícito pode promovê-los a requisito visual.
- **Só o necessário para executar.** Para cada ação, guardar saída verificável, formato/quantidade quando houver, insumos indispensáveis e restrições que afetam a execução. Estratégia, mídia, verba, métricas e contexto geral não viram itens nem seção de descarte. Dedução necessária = `(suposto)`; não inventar entrega.
- **Copy:** quando a ação inclui peça com texto, transcrever literalmente o texto aplicável; não reescrever nem misturar copy de outras peças. Ausência de copy só bloqueia quando o texto é indispensável à v1.
- **Imagem:** usar a copy de peso `5` para definir a cena; procurar foto real pertinente e autorizada quando ela servir essa cena. Se não houver, gerar ou compor outra solução e identificar a origem. Nota genérica sobre banco/foto real não bloqueia nem impõe retrato; só parar quando o pedido atual exigir o ativo específico ou ele for indispensável à fidelidade/prova factual.
- **Conflito com o KV** (cor, fonte, recurso vetado no `design_system.md`): apontar em 1 linha quando afetar a peça; o KV vence salvo decisão explícita do usuário no pedido atual. Nota geral do briefing não muda identidade.
- **Perguntas:** no máximo 3, só as que impedem a v1, cada uma com a opção recomendada. O resto vira suposição declarada.
- **Tamanho:** cabe numa tela. Uma linha por ação, em ordem de dependência e prazo. Sem introdução ou resumo do briefing.

## 2. Formato da saída
```
Fazer · [Cliente]
1. [Ação + objeto + saída verificável]
2. [Ação + objeto + saída verificável]

Necessário para executar: [só arquivos, copy literal, formato e restrições ligados às ações acima]
Bloqueia: [apenas falta que impede uma das ações; até 3 perguntas com recomendação]
Próximo passo: [primeira ação que pode começar agora]
```
Linha sem conteúdo some (não escrever "nenhum"). Várias peças podem usar tabela compacta de formato/quantidade **dentro da ação de criar**, sem substituir a lista de ações.

## 3. Depois da tradução
- Nada bloqueia: seguir direto para a primeira ação na mesma resposta (organização, análise ou peça).
- Gravar a lista e insumos aplicáveis como `briefing.md` na pasta da solicitação (`[AAAA]\[MM - Mês]\[AAAA-MM-DD] [TIPO] Título\`). O `design_system.md` recebe apenas aprendizado durável da marca, não a lista da campanha.
- Resposta do usuário a um "Bloqueia" atualiza a linha afetada, sem refazer a triagem inteira.

## 4. Leitura de fontes
- PDF/Doc/e-mail: ler uma vez. Print/áudio: transcrever só o que altera uma ação ou insumo indispensável.
- Abrir apenas links e pastas necessários às ações extraídas; acesso falho a material irrelevante não bloqueia. Conflito que altera entrega, KV ou copy: mostrar trechos e fontes; perguntar só se não houver decisão atual do usuário.
