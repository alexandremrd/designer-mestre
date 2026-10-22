# EVOLUCAO · memória do próprio agente /designer-mestre
> Ler **só ao alterar o agente** (núcleo §7). Guarda o estado atual, as decisões e os aprendizados para não reanalisar. Substituir linhas, não empilhar; teto ~5 KB. Nada de cliente aqui.

## Estado atual (v19.17 · fonte em revisão, não instalada · 2026-10-21)
- Núcleo enxuto com rotas, Ciclo único (§2), Gate de KV, Leis, Padrões U1–U10, Fontes e direitos, Entrega e memória. Cliente novo/KV incompleto exige estudo das séries pertinentes; referência indicada é lida inteira, inclusive estrutura SVG; conflito material mostra trecho e fonte antes da escolha. Evolução da skill: localizar função equivalente, integrar sem perder capacidade e avaliar tokens, tempo e qualidade observável (§7).
- Imagem: `imagem.md` (A arsenal/aprendizado · B prompt/foto/composite/decomposer/Pass³ · **C publicitária**) + anexos `imagem-produto.md` e `imagem-personagem.md`.
- Árvore de imagens do cliente (Lei 5): `Compartilhada\Imagens\{Originais, Banco de Imagens, Tratadas, IA}`. `assets\gerar_imagem.py` recusa salvar fora de `IA\`/`Tratadas\` e dentro de `Originais\`, `Banco de Imagens\` ou `Referências\`.
- Prévia: sempre mostrada como imagem ao usuário (§2 "Prévia visível"); conferência interna continua só pela prancha.
- Fluxo ágil: peça estática diagramada sai em SVG autossuficiente + PNG e prévia na v1 enquanto Figma estiver indisponível; raster isolado permanece PNG. Aprovação só para seleção de conceito, mudança de identidade/copy ou custo externo. Imagem comercial lê `ads.md` §1 + `imagem.md` Parte C; câmera/luz/profundidade/atmosfera vêm do pedido, da referência atual, da receita aprovada do cliente ou da base adaptável, nessa ordem, sob KV. Referência é opcional. QA extenso só quando pedido ou houver falha concreta.
- v19.17 na fonte: `ads.md` antepõe miniaturas de massas, grade, foco e tipografia ao SVG final; remove presets de layout e meta de ocupação. U7 reprova falhas observáveis antes da nota. A versão instalada permanece v19.16 até aprovação explícita.

## Decisões do mantenedor (valem para todos os clientes)
1. Prévia visível obrigatória, nunca só texto.
2. Imagem gerada/tratada nunca em pasta de originais ou banco do cliente.
3. Referência 360 de produto e de personagem em fundo neutro sem cor; cena é saída, não referência.
4. Produto sem foto real + autorização → vista gerada aprovada vira mestra provisória `_gerada` até chegar foto real.
5. Produto com interior (aeronave, veículo, embarcação, imóvel, loja) → inventariar e registrar interior por configuração; sem foto interna, não gerar interior.
6. Imagem publicitária precisa de argumento comercial alinhado à copy literal e prova/contexto visual, ficha de direção física, 3 direções internas e teste contra imagem genérica (Parte C); 3 imagens só quando pedidas. Sem referência: receita aprovada do cliente ou base candidata, nunca estilo fixo. Com referência: extrair mecanismos visíveis sem inventar EXIF. Proporção imagem/texto é variável (U9).
7. Tirar créditos de terceiros das entregas só quando a licença permitir; crédito obrigatório por licença fica em 1 linha discreta (núcleo §6). Não remover marca d'água/crédito de foto sem autorização.
8. Pacote 360 (produto/personagem) é referência de entrada do gerador de IA: a imagem publicitária nasce inteira com o produto. Recorte colado em cenário gerado ou recorte direto na peça = erro grave. Sem gerador com referência → parar e avisar, não degradar.
9. Série de campanha/carrossel tem contexto temporal e ambiental coerente, sem exigir gradação idêntica; cada card tem cena/composição própria. Mesma imagem ou crop equivalente em cards diferentes reprova, salvo pedido explícito (U10).
10. Enquanto Figma estiver indisponível, peça estática diagramada é entregue em SVG editável e PNG pronto para uso, sem perguntar formato; imagem raster isolada não recebe falso SVG.
11. Cliente novo ou sem KV validado requer análise suficiente dos arquivos relevantes; peças indicadas pelo usuário são examinadas como conjunto, inclusive estrutura SVG, sem limite artificial de 2–3 peças. Briefing e referência visual em conflito são mostrados com trechos/fonte antes de decidir. Foto obrigatória inacessível não é substituída silenciosamente por grafismo.
12. Cliente novo recebe árvore completa de imagens, mesmo vazia; a leitura dos criativos também resume direção fotográfica e ofertas/produtos com fonte e nível de confirmação. Ao sugerir alteração da skill, resposta final informa status, implementação e versão sincronizada.
13. Tag única `CLIENTE_NOVO: SIM|NÃO` no topo do design system aciona o estudo inicial uma vez; depois, KV parcial consulta só pendências relevantes. Evita reabrir todo o acervo em cada pedido.
14. Evoluções ficam na fonte até aprovação explícita para instalar. O briefing vira lista de ações executáveis e usa pesos internos: copy na peça `5`, nota de arte específica `2`, contexto geral `1`, histórico/menção `0`; pedido atual e KV/direitos são limites, não pontos. Foto real serve à cena quando pertinente e autorizada; ausência permite cena gerada identificada, salvo exigência atual ou necessidade de fidelidade/prova. O fluxo publicitário passa por funções dos ativos → relações do SVG → cena ligada à proposição → confronto lado a lado de briefing, referência e peça.

## Aprendizados (causa → correção)
- Prévia não aparecia: nenhuma regra mandava mostrar; "olhar só a prancha" e o fecho "arquivo + 1 linha" eram lidos como "não exibir"; subagente devolvia só texto → §0.5, §0.7 e §2 corrigidos.
- IA salva junto dos originais: caminhos divergentes entre núcleo, template e módulos (`Imagens\` × `Banco de Imagens\`) e script sem trava → árvore única + trava no script.
- Pacote 360 fora do padrão: mestra escolhida por disponibilidade, não por qualidade (silhueta no pôr do sol, 300 px, crop inclinado, mockup) e versões de pintura misturadas → curadoria pontuada no `imagem-produto.md` §1.1.
- Render de loja 3D/foto com marca d'água serve só como geometria; nunca mestra nem peça.
- Faixas finas/pill/círculo que decepam aeronave reprovam (`ads.md` §3), salvo pedido literal do briefing (Lei 1).
- Endcard só com logo + botão em fundo liso reprova (`ads.md` §3.3).

- Peça fora do KV: o agente seguiu literalmente a "estética" do doc (fundo claro) e ignorou o KV publicado e o arquétipo aprovado → Gate §3: KV publicado vence texto de direção de arte; clonar a última peça aprovada.

- Imagem "de catálogo" e tokens jogados fora: sem gerador com referência na sessão, o agente seguiu a regra "pular para a próxima opção sem anunciar", gerou cenários vazios só de texto e começou a colar os recortes 360 (Rota Híbrida permitida para produto no `imagem-produto.md` §3), além de transferir as cenas em base64 → §0.6 do núcleo para e avisa quando o fallback troca o método; Rota Híbrida restrita a logo/texto/rótulo; `imagem-produto.md` §3 com gate de gerador com referência.
- Imagem bonita sem força de venda ou travada num “cinematográfico” genérico: a rota seletiva e os presets viraram atalho → imagem comercial exige proposição/prova visual; referências atuais transferem câmera, luz, profundidade e atmosfera; sem referência, receita aprovada ou base funcional adaptável; decisões explícitas do cliente vencem.
- Foto de produto desconectada da copy: a proposição visual existente não mandava partir da afirmação literal → U9 liga copy à cena por causa, uso, consequência ou tensão; QA reprova foto genérica ao lado de promessa específica, sem impor 50/50.
- Série com dia/noite misturados e endcard repetindo o card anterior: sem diretriz de sequência, cenas eram geradas e avaliadas isoladamente → U10 fixa contexto temporal/ambiental e veta imagem/crop/composição equivalentes na prancha, preservando variação de câmera e intensidade.
- Cliente novo sem `_DESIGN`: série SVG indicada foi reduzida a amostra superficial, brief conflitante não foi mostrado, e banco fotográfico obrigatório virou geometria genérica → Cold Start estuda a série completa e SVGs; Gate exibe conflito; `ads.md` justifica suporte visual e não mascara ativo obrigatório ausente.
- Briefing com histórico, revisor citado e vários bancos de imagem levou a tarefas extras e à suposição de pôr a pessoa na arte → `briefing.md` extrai ações e insumos indispensáveis; menção/prioridade de pessoa não equivale a instrução de retrato; só conflitos materiais bloqueiam.
- Peça formalmente correta, mas visualmente fraca: retrato + headline empilhados, Arial por conveniência e linhas decorativas passaram nos checks técnicos sem uma composição memorável → `ads.md` agora testa 2–3 massas rápidas (ou 1 em `/rapido`), escolhe foco pela copy e usa espaço negativo/grade antes de efeitos; U7 veta foco ambíguo ou imagem sem tese antes da nota.
- Imagem esteticamente coerente, mas sem relação com a afirmação, e excesso de pesos tipográficos: o elo sujeito→ação→consequência não passava entre direção, fotografia e layout; U9 e `ads.md` §1 agora exigem elo legível antes do prompt e U3/`ads.md` §2 conferem pesos efetivos no PNG.

## Pendências do agente
- `img_qa.py`: subcomando para checar texto/letras em imagem gerada (OCR leve) antes do Pass³.
- Testar a Parte C com gerador real em dois cenários (com e sem referência) e gravar a receita aprovada por cliente, não presumir vencedor por categoria.
