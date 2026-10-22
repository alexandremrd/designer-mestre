# EVOLUCAO · memória do agente /designer-mestre
> Ler ao alterar a skill. Manter conciso (~5 KB); preferências específicas ficam no `design_system.md` do cliente.

## Estado atual (v19.25 · instalada em 7 destinos e publicada · 2026-10-22)
- Conteúdo sob demanda: uma rota principal e anexos pertinentes. Skills especialistas conduzem crítica de interface e design-to-code.
- Cold Start usa fontes acessíveis; separa evidência, inferência e lacuna, com origem e data. Sem coleta paga, contorno de bloqueios ou fatos inventados.
- Imagens do cliente: `Compartilhada\Imagens\{Originais, Banco de Imagens, Tratadas, IA}`; geradas/tratadas nunca são originais. Toda saída visual deve ter prévia quando o canal permitir.
- Estático diagramado = SVG + PNG; raster isolado continua raster. SVG não transporta semântica/Auto Layout do Figma; para editar estruturalmente, reconstruir em nós nativos.
- v19.24 remove fórmulas criativas restritivas: “do zero” não clona layout; formato não determina composição; conceito novo considera alternativas. Metáfora, tipografia expressiva, direção heroica e cor intensa são válidas quando servem à ideia, KV e fatos.
- v19.25 separa sistema de marca, KV de campanha e peça isolada na engenharia reversa de referências. Documenta evidência, recorrência, exceções e confiança proporcional à amostra; traduz mecanismos ao KV do cliente sem copiar. Métodos de Naksha Studio e UPPAbaby Brand Review foram reescritos, não instalados. Inclui o `Instalador.ps1` ausente no release público anterior.
- Preferência do mantenedor: referências editoriais/de campanha com retrato integrado, tipografia grande, cor, textura e camadas indicam ambição, não preset. Adaptar mecanismos; nunca copiar identidade, layout ou copy.

## Histórico útil
- v19.18: instalador valida origem, preserva extras, confere SHA-256 e pede confirmação antes de baixar `sharp`.
- v19.19–20: menos presets; análise aceita raster; modo heroico permanece opcional.
- v19.21: Cold Start baseado em evidências para site, Instagram e concorrentes; confirmação antes de coleta paga.
- v19.22–23: SVG não é estrutura Figma; reconstrução nativa e validação de hierarquia/paridade. Generator de design só para telas app/web quando pertinente.
- v19.24: instalada e verificada por SHA-256 em 7 destinos locais; não publicada no GitHub.

## Decisões permanentes
- Mostrar prévia visual quando possível; separar imagens originais, licenciadas, tratadas e geradas.
- Preservar produto/pessoa; não inventar interiores de imóveis, veículos, aeronaves, embarcações ou lojas sem referência.
- Criativo respeita copy e identidade; metáfora não é prova. Sem referência, escolher direção própria sem impor estilo.
- Séries mantêm coerência ambiental e variam cenas; não repetem imagem/crop sem pedido.
- Crédito de terceiros só é removido se a licença permitir; créditos obrigatórios ficam discretos.
- Cliente novo/sem KV: estudar fontes pertinentes uma vez e registrar `CLIENTE_NOVO: SIM|NÃO`.
- Mudanças ficam na fonte até aprovação explícita para instalação; publicação externa também requer pedido explícito.

## Aprendizados e pendências
- Uma peça não comprova sistema de marca; repetição dentro de uma campanha sustenta hipótese de KV, não regra permanente.
- “Card de citação” é formato, não direção de arte. Em criação nova, ideia visual vem antes do arranjo padrão de foto e texto.
- Copy literal não exige ilustração literal; metáforas e abstrações podem expressar a ideia sem fingir evidência.
- Avaliar v19.24 em peça executiva/editorial, anúncio heroico e ajuste mecânico. Considerar OCR leve em `img_qa.py` para sinalizar texto acidental.
