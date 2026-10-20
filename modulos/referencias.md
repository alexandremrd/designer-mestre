# Módulo Referências · decodificar referência → KV do cliente

Ativar com `/designer-mestre ref` (aliases: `referencia`, `moodboard`) ou quando o usuário mandar imagens dizendo "referência", "inspiração", "analisa". Transforma imagens soltas em **fichas curtas reutilizáveis**. Objetivo: analisar UMA vez, nunca reabrir a imagem.

## 1. Economia (regra principal)
- Ver as referências **uma vez**, juntas: montar uma prancha (`_prancha_refs.jpg`, ≤ 2000 px de largura, 4–8 por folha) e ler só a prancha. Abrir uma imagem isolada só se um detalhe não der para ler na prancha.
- Gravar o resultado como **texto**. Depois disso, o agente lê só o arquivo de texto (nunca as imagens) para criar.
- Ficha com teto de ~700 caracteres. Arquivo do cliente com teto de ~8 KB; passou disso, fundir fichas parecidas.
- Sem análise de cor por script em cada imagem: estimar pela prancha; medir com script só se a cor for virar token.

## 2. Onde salvar
| O quê | Onde |
|---|---|
| Imagens de referência (cópias 1024 px) | `[Cliente]\Compartilhada\Referências\KV_Inspiracao\[AAAA-MM]\` |
| Prancha de conferência | mesma pasta, `_prancha_refs.jpg` |
| Fichas + conversão para o KV + banco de ideias | `[Cliente]\_DESIGN\referencias.md` |
| Referência universal (sem cliente) | não existe: toda ficha mora num cliente |

## 3. Ficha (uma por referência)
```
### R[n] · [apelido curto] · [arquivo]
Técnica: grid/composição · hierarquia tipográfica (peso/caixa/alinhamento) · tratamento de foto (ângulo, lente, luz, cor) · grafismo · CTA.
Olhar criativo: a ideia por trás (metáfora, tensão, recorte) em 1 frase.
Peça publicitária: por que funciona / onde falha.
No KV [cliente]: o que entra (traduzido para tokens do cliente) · o que NÃO entra (vetos).
Usar em: tipo de post/slide onde rende mais.
```

## 4. Síntese (fim do arquivo)
- **Padrões recorrentes** (3–6 linhas): o que várias referências fazem igual.
- **Receitas para o KV** (3–6): combinações prontas, ex.: "Capa cinematográfica = foto real full-bleed contra-luz + degradê navy 55% + headline ExtraBold com 1 palavra-chave laranja".
- **Banco de ideias** (5–10 linhas): conceitos de post/slide derivados, já no KV, prontos para briefing futuro.
- **Não copiar:** o que é marca registrada/recurso de outra empresa (logo, slogan, mascote, layout idêntico).

## 5. Uso na criação
- Fast-Track lê `referencias.md` só quando o pedido citar ideia nova, "mais criativo", "menos simples" ou uma ficha (`R3`).
- Em cada prévia, citar no topo em 1 linha quais fichas/receitas foram usadas.
- Receita aprovada pelo usuário sobe para `## 2. O QUE FAZER` do `design_system.md`.

## Checklist
- [ ] Prancha única lida; nenhuma imagem reaberta depois
- [ ] Fichas ≤ 700 caracteres, com conversão ao KV e vetos
- [ ] Síntese com receitas + banco de ideias
- [ ] Cópias 1024 px em `KV_Inspiracao\`; nada de logo/slogan de terceiro na peça
