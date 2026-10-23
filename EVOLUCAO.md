# EVOLUCAO · memória do agente /designer-mestre
> Caderno de manutenção: lido só ao alterar a skill, por isso não pesa nos pedidos de peça. Guarda estado, casos de teste e pendências; regras vigentes ficam no núcleo e nos módulos, tendências de criação no `GUIA.md`, cliente no `_DESIGN\guia.md` dele, histórico de versões no git. Teto ~2 KB.

## Estado atual
- v19.48 instalada e publicada. Memória em duas camadas de sugestões: `GUIA.md` (agente) e `_DESIGN\guia.md` (cliente); o `design_system.md` fica com KV e negócio.

## Casos de teste ao alterar a skill
- Card de citação com retrato, copy fechada e referência aprovada: três conceitos distintos, nenhum layout genérico ou cópia.
- Seis cards do mesmo ensaio: gramática comum, sem repetir enquadramento.
- Peça aprovada para Figma: a rota Figma cuida da estrutura nativa, sem duplicar o editor dentro de ads.
- Referência editorial com pedido só de acabamento: tipografia, luz e paleta do KV não mudam.
- Pedido que já tem capacidade instalada: estender o dono existente, não criar módulo paralelo.
- Imagem anexada: descrever sem pedir chave ou SDK; texto pequeno incerto não é completado.
- Produto com lado sem foto real: pedir referência antes de gerar esse lado.

## Pendências do agente
- **Chave colada no chat:** decisão do usuário é ajudar a conectar do jeito certo (link oficial, comando que ele mesmo roda, teste depois do "pronto"); texto ainda não aplicado ao núcleo §6.
- **Entregável completo desde o briefing:** listar todas as camadas do formato (vídeo = imagem + texto + voz + trilha + licença; estático = arte + legenda/CTA + formatos) e resolver as ausentes no início.
- **Insumo na resolução de saída:** pedir cedo arquivos em alta; captura do ambiente pode sair limitada.
- Considerar OCR leve em `img_qa.py` para sinalizar texto acidental.
