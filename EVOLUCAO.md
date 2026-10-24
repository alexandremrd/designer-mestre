# EVOLUCAO · memória do agente /designer-mestre
> Caderno de manutenção: lido só ao alterar a skill, por isso não pesa nos pedidos de peça. Guarda estado, casos de teste e pendências; regras vigentes ficam no núcleo e nos módulos, tendências de criação no `GUIA.md`, cliente no `_DESIGN\guia.md` dele, histórico de versões no git. Teto ~2 KB.

## Estado atual
- v19.53 instalada em 23/10/2026 nas cópias locais: motor local ComfyUI sem interface (t2i e edição por referência, ~1 min/imagem numa GPU de 8 GB) e aval único gravado (`consentimento.py`, vale em toda IA; conta paga = sim único dentro do contratado, excedente ou API por uso = sim a cada geração com aviso de que quem cobra é o provedor). Publicada no GitHub como release v19.53. Memória em duas camadas de sugestões: `GUIA.md` (agente) e `_DESIGN\guia.md` (cliente); o `design_system.md` fica com KV e negócio.

## Casos de teste ao alterar a skill
- Card de citação com retrato, copy fechada e referência aprovada: três conceitos distintos, nenhum layout genérico ou cópia.
- Seis cards do mesmo ensaio: gramática comum, sem repetir enquadramento.
- Peça aprovada para Figma: a rota Figma cuida da estrutura nativa, sem duplicar o editor dentro de ads.
- Referência editorial com pedido só de acabamento: tipografia, luz e paleta do KV não mudam.
- Pedido que já tem capacidade instalada: estender o dono existente, não criar módulo paralelo.
- Imagem anexada: descrever sem pedir chave ou SDK; texto pequeno incerto não é completado.
- Produto com lado sem foto real: pedir referência antes de gerar esse lado.
- Gerador falhou sem fallback automático: uma pergunta na ferramenta, só com opções verificadas (inclusive app da loja fora do PATH), recomendada primeiro, Modo Manual por último; motor local só aparece se o `detectar` disser que o PC aguenta.
- Usuário novo: nada pesado baixa ao instalar a skill; 1ª oferta do motor = uma pergunta simples (a do `detectar`); com o sim, a IA instala e usa sem perguntar de novo, em qualquer IA; sem aval, `gerar` recusa. PC sem GPU NVIDIA = motor não é oferecido.
- Motor local: `--ref` mantém o produto da imagem 1; motor ligado até a aprovação final, depois `parar`.

## Pendências do agente
- **Chave colada no chat:** decisão do usuário é ajudar a conectar do jeito certo (link oficial, comando que ele mesmo roda, teste depois do "pronto"); texto ainda não aplicado ao núcleo §6.
- **Entregável completo desde o briefing:** áudio do motion já aplicado (`video.md` Parte C); falta o resto das camadas (estático = arte + legenda/CTA + formatos; licença da trilha).
- **Insumo na resolução de saída:** pedir cedo arquivos em alta; captura do ambiente pode sair limitada.
- Considerar OCR leve em `img_qa.py` para sinalizar texto acidental.
