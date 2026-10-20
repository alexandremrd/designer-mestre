# EVOLUCAO · memória do próprio agente /designer-mestre
> Ler **só ao alterar o agente** (núcleo §7). Guarda o estado atual, as decisões e os aprendizados para não reanalisar. Substituir linhas, não empilhar; teto ~5 KB. Nada de cliente aqui.

## Estado atual (v19.1 · 2026-10-20)
- Núcleo enxuto com rotas, Ciclo único (§2), Gate de KV, Leis, Padrões U1–U8, Fontes e direitos, Entrega e memória.
- Imagem: `imagem.md` (A arsenal/aprendizado · B prompt/foto/composite/decomposer/Pass³ · **C publicitária**) + anexos `imagem-produto.md` e `imagem-personagem.md`.
- Árvore de imagens do cliente (Lei 5): `Compartilhada\Imagens\{Originais, Banco de Imagens, Tratadas, IA}`. `assets\gerar_imagem.py` recusa salvar fora de `IA\`/`Tratadas\` e dentro de `Originais\`, `Banco de Imagens\` ou `Referências\`.
- Prévia: sempre mostrada como imagem ao usuário (§2 "Prévia visível"); conferência interna continua só pela prancha.

## Decisões do mantenedor (valem para todos os clientes)
1. Prévia visível obrigatória, nunca só texto.
2. Imagem gerada/tratada nunca em pasta de originais ou banco do cliente.
3. Referência 360 de produto e de personagem em fundo neutro sem cor; cena é saída, não referência.
4. Produto sem foto real + autorização → vista gerada aprovada vira mestra provisória `_gerada` até chegar foto real.
5. Produto com interior (aeronave, veículo, embarcação, imóvel, loja) → inventariar e registrar interior por configuração; sem foto interna, não gerar interior.
6. Imagem publicitária precisa de ficha de direção + ângulo de herói por categoria + 3 variações estruturais + teste publicitário (Parte C).
7. Tirar créditos de terceiros das entregas só quando a licença permitir; crédito obrigatório por licença fica em 1 linha discreta (núcleo §6). Não remover marca d'água/crédito de foto sem autorização.

## Aprendizados (causa → correção)
- Prévia não aparecia: nenhuma regra mandava mostrar; "olhar só a prancha" e o fecho "arquivo + 1 linha" eram lidos como "não exibir"; subagente devolvia só texto → §0.5, §0.7 e §2 corrigidos.
- IA salva junto dos originais: caminhos divergentes entre núcleo, template e módulos (`Imagens\` × `Banco de Imagens\`) e script sem trava → árvore única + trava no script.
- Pacote 360 fora do padrão: mestra escolhida por disponibilidade, não por qualidade (silhueta no pôr do sol, 300 px, crop inclinado, mockup) e versões de pintura misturadas → curadoria pontuada no `imagem-produto.md` §1.1.
- Render de loja 3D/foto com marca d'água serve só como geometria; nunca mestra nem peça.
- Faixas finas/pill/círculo que decepam aeronave reprovam (`ads.md` §3), salvo pedido literal do briefing (Lei 1).
- Endcard só com logo + botão em fundo liso reprova (`ads.md` §3.3).

## Pendências do agente
- `img_qa.py`: subcomando para checar texto/letras em imagem gerada (OCR leve) antes do Pass³.
- Testar a Parte C com um gerador real e gravar a receita vencedora por categoria.
