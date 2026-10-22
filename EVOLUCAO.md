# EVOLUCAO · memória do agente /designer-mestre
> Ler ao alterar a skill. Manter conciso (~5 KB); preferências específicas ficam no `design_system.md` do cliente.

## Estado atual (fonte e instalada v19.29 em 7 destinos · 2026-10-22)
- Conteúdo sob demanda: uma rota principal e anexos pertinentes. Skills especialistas conduzem crítica de interface e design-to-code.
- Cold Start usa fontes acessíveis; separa evidência, inferência e lacuna, com origem e data. Sem coleta paga, contorno de bloqueios ou fatos inventados.
- Imagens do cliente: `Compartilhada\Imagens\{Originais, Banco de Imagens, Tratadas, IA}`; geradas/tratadas nunca são originais. Toda saída visual deve ter prévia quando o canal permitir.
- Estático diagramado = SVG + PNG; raster isolado continua raster. SVG não transporta semântica/Auto Layout do Figma; para editar estruturalmente, reconstruir em nós nativos.
- v19.24 remove fórmulas criativas restritivas: “do zero” não clona layout; formato não determina composição; conceito novo considera alternativas. Metáfora, tipografia expressiva, direção heroica e cor intensa são válidas quando servem à ideia, KV e fatos.
- v19.25 separa sistema de marca, KV de campanha e peça isolada na engenharia reversa de referências. Documenta evidência, recorrência, exceções e confiança proporcional à amostra; traduz mecanismos ao KV do cliente sem copiar. Métodos de Naksha Studio e UPPAbaby Brand Review foram reescritos. Inclui o `Instalador.ps1` ausente no release público anterior.
- v19.26 corrige falha de preservação: referência deixa de ser direção estética concorrente. KV do cliente passa a ser contrato explícito para tipografia, fotografia/luz/grade, efeitos, grafismos e composição; referências externas só fornecem técnicas compatíveis, escolhidas separadamente e verificadas após render. Template de cliente registra essas camadas com fonte/confiança. Instalada e publicada.
- v19.27 adiciona análise de causa e inventário funcional antes de criar ou evoluir capacidade: consulta feedback/artefatos, skills, módulos, scripts e ferramentas disponíveis; classifica cobertura como completa, parcial ou lacuna comprovada. Sobreposições são sintetizadas por resultado, com núcleo comum e rotas para variantes; especialidades com artefatos/autoridade distintos permanecem separadas. Decodificação de referências tem um único dono (`referencias.md`); `ads.md` consome a síntese em vez de duplicar o pipeline. Instalada e publicada.
- v19.29 formaliza o ciclo aprovado: atualizar a fonte, reinstalar e verificar cópias por SHA-256, publicar no repositório canônico (remoto `origin`) e manter apenas as quatro atualizações mais recentes no README público. Instalada e verificada em 7 destinos.
- v19.28 corrige o gate fraco observado na V8: a rota de ads agora orquestra análise de referência, direção fotográfica e revisão independente sem carregar skills sem relação com o entregável; o módulo de imagem inclui seleção de ativos reais; `qualidade.md` §§A/H passa a reprovar conceito genérico, motivo decorativo, camada sem origem e acabamento default sem substituir julgamento por nota. Instalada e verificada por SHA-256 em 7 destinos. O caso de card de citação recusado será teste qualitativo: a direção aprovada não pode ser apenas foto + nuvem + texto, precisa mostrar relação visual com a tese e diferir da composição anterior.
- Preferência do mantenedor: referências editoriais/de campanha com retrato integrado, tipografia grande, cor, textura e camadas indicam ambição, não preset. Adaptar mecanismos; nunca copiar identidade, layout ou copy.

## Histórico útil
- v19.18: instalador valida origem, preserva extras, confere SHA-256 e pede confirmação antes de baixar `sharp`.
- v19.19–20: menos presets; análise aceita raster; modo heroico permanece opcional.
- v19.21: Cold Start baseado em evidências para site, Instagram e concorrentes; confirmação antes de coleta paga.
- v19.22–23: SVG não é estrutura Figma; reconstrução nativa e validação de hierarquia/paridade. Generator de design só para telas app/web quando pertinente.
- v19.24: instalada e verificada por SHA-256 em 7 destinos locais; publicada no GitHub.

## Decisões permanentes
- Mostrar prévia visual quando possível; separar imagens originais, licenciadas, tratadas e geradas.
- Preservar produto/pessoa; não inventar interiores de imóveis, veículos, aeronaves, embarcações ou lojas sem referência.
- Criativo respeita copy e identidade; metáfora não é prova. Sem referência, escolher direção própria sem impor estilo.
- Séries mantêm coerência ambiental e variam cenas; não repetem imagem/crop sem pedido.
- Crédito de terceiros só é removido se a licença permitir; créditos obrigatórios ficam discretos.
- Cliente novo/sem KV: estudar fontes pertinentes uma vez e registrar `CLIENTE_NOVO: SIM|NÃO`.
- Mudanças ficam na fonte até aprovação explícita para instalação; publicação externa também requer pedido explícito.

## Aprendizados e pendências
- Falha V8 (card de citação): nomear camadas do KV não garante tradução. O retrato de close, a forma de nuvem e a linha de dados estavam presentes, mas não articulavam visualmente a tese; a composição ainda lia como retrato recortado + headline sans em três linhas. A regra causal está no gate de Ads e Qualidade, não numa nova skill ou num carregamento indiscriminado de todas as skills.
- **Casos de regressão v19.28 (revisão qualitativa; não executados como benchmark):** (1) “Crie um card de citação para CEO com retrato, copy fechada e carrossel aprovado como referência; o layout anterior foi recusado.” Esperado: ads + KV + referências + direção fotográfica + gate A/H; três conceitos realmente distintos, nenhuma cópia, claim ou layout genérico. (2) “Monte seis cards com uma história e imagens do mesmo ensaio; preserve o sistema da marca sem repetir enquadramento.” Esperado: ads + referências + imagem + U10 + gate A/H, uma gramática comum com variação funcional de cena/crop e leitura contínua. (3) “Converta a peça aprovada em frames e camadas nativas no Figma.” Esperado: ads fornece a direção aprovada e a rota Figma cuida da estrutura nativa; não carregar UI web, vídeo ou duplicar o editor Figma dentro da rota de ads.
- Uma peça não comprova sistema de marca; repetição dentro de uma campanha sustenta hipótese de KV, não regra permanente.
- “Card de citação” é formato, não direção de arte. Em criação nova, ideia visual vem antes do arranjo padrão de foto e texto.
- Regressão a evitar: referência editorial não pode trocar por serifada a tipografia sans aprovada, mudar a luz/grade dos retratos nem importar sua paleta/composição quando o cliente pediu apenas acabamento. Testar também o caso oposto: redesign de KV só passa quando o usuário pede a mudança explicitamente.
- Regressão a evitar: criar função, prompt ou módulo novo antes de encontrar a capacidade instalada mais próxima. Testar roteamento para função existente, extensão de função parcial, preservação de especialista adjacente sem cópia e handoff entre análise de referências, composição do anúncio e geração de imagem.
- Copy literal não exige ilustração literal; metáforas e abstrações podem expressar a ideia sem fingir evidência.
- Avaliar v19.24 em peça executiva/editorial, anúncio heroico e ajuste mecânico. Considerar OCR leve em `img_qa.py` para sinalizar texto acidental.
