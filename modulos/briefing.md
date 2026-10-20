# Módulo Briefing — tradutor (o que o designer precisa fazer, e só isso)

Ativa com `/designer-mestre briefing` (aliases `brief`, `traduz`) ou automaticamente quando o pedido chega como briefing (texto longo, e-mail, áudio transcrito, PDF, doc, print de WhatsApp). Roda **antes** do módulo da peça. Saída curta, sempre no formato abaixo; nada fora dele.

## 1. Regras
- **Só design.** Traduzir em peças, formatos, material e restrições. Estratégia, mídia, verba, público-alvo, oferta, copywriting, cronograma de campanha e métricas ficam fora: aparecem só em "Fora do meu escopo", em 1 linha cada, sem opinião.
- **Nada inventado.** Cada item vem do briefing. Dedução necessária = marcar `(suposto)`. Sem fonte e sem dedução segura = vai para "Bloqueia".
- **Copy:** transcrever literal o que o cliente escreveu; não reescrever, não completar, não sugerir. Sem copy = "Bloqueia".
- **Conflito com o KV** (cor, fonte, recurso vetado no `design_system.md`): apontar em 1 linha; o KV vence salvo se o briefing pedir a exceção de forma explícita.
- **Perguntas:** no máximo 3, só as que impedem a v1, cada uma com a opção recomendada. O resto vira suposição declarada.
- **Tamanho:** cabe numa tela. Sem introdução, sem resumo do briefing, sem "entendi que".
- Briefing com várias entregas: uma linha por peça na tabela; ordem = prazo, depois dependência (KV antes das peças, foto antes do criativo).

## 2. Formato da saída
```
Briefing · [Cliente] · [Campanha/assunto] · prazo [data | não informado]

| # | Peça | Formato / tamanho | Qtd | Módulo | Status |
|---|---|---|---|---|---|
| 1 | Post feed | 1080×1350 | 3 | ads | pronto p/ criar |
| 2 | Story | 1080×1920 | 3 | ads | falta copy |

Copy (literal): "…" → peça 1 · "…" → peça 2 · [sem copy: peças 2–3]
Material: logo [ok/falta] · fotos [ok: caminho | falta] · links [abertos | não abriu: X]
Restrições: [obrigatório do cliente: selo, disclaimer, CTA, prazo legal] · [vetos do KV que pesam aqui]
Suposições: [ex.: Story = mesma cena do Feed (suposto)]
Bloqueia: 1) … (recomendo: …)  2) …
Fora do meu escopo: [ex.: definir público da campanha · verba de mídia]
Próximo passo: [peça 1 em prévia agora | aguardando item X]
```
Linha sem conteúdo some (não escrever "nenhum").

## 3. Depois da tradução
- Nada bloqueia: seguir direto para o módulo da peça 1 na mesma resposta.
- Gravar a tabela como `briefing.md` na pasta da solicitação (`[AAAA]\[MM - Mês]\[AAAA-MM-DD] [TIPO] Título\`). O `design_system.md` não recebe nada de campanha (é só marca).
- Resposta do usuário a um "Bloqueia" atualiza o `briefing.md` (sobrescreve a linha), sem refazer a tradução inteira.

## 4. Leitura de fontes
- PDF/Doc/e-mail: ler uma vez. Print/áudio: transcrever só o que vira item da tabela.
- Links do briefing são leitura obrigatória (núcleo §3). Não abriu = "Material: não abriu: X" + 1 pergunta.
- Briefing que contradiz a si mesmo (ex.: "3 posts" e depois "carrossel de 5"): 1 pergunta, com as duas leituras.
