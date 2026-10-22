# Módulo Referências & Taste Engine · Decodificar Referência → Regras Transferíveis no KV

Ativar com `/designer-mestre ref` (aliases: `referencia`, `moodboard`) ou quando o usuário mandar imagens dizendo "referência", "inspiração", "analisa", "faz nesse estilo". Transforma imagens soltas em **fichas curtas reutilizáveis e regras transferíveis**. Objetivo: analisar UMA vez, nunca reabrir a imagem.

## 1. Economia de Análise
- Ver as referências **uma vez**, juntas: montar uma prancha (`_prancha_refs.jpg`, ≤ 2000 px de largura, 4–8 por folha) e ler só a prancha. Abrir uma imagem isolada só se um detalhe não der para ler na prancha.
- Extrair óptica, luz, grid, proporções e paleta direto da imagem enviada.
- Gravar o resultado como **texto**. Depois disso, o agente lê só o arquivo de texto (nunca as imagens) para criar.
- Ficha com teto de ~700 caracteres. Arquivo do cliente com teto de ~8 KB; passou disso, fundir fichas parecidas.
- Sem análise de cor por script em cada imagem: estimar pela prancha; medir com `img_qa.py paleta` só se a cor for virar token.

## 2. Onde salvar
| O quê | Onde |
|---|---|
| Imagens de referência (cópias 1024 px) | `[Cliente]\Compartilhada\Referências\KV_Inspiracao\[AAAA-MM]\` |
| Prancha de conferência | mesma pasta, `_prancha_refs.jpg` |
| Fichas + conversão para o KV + banco de ideias | `[Cliente]\_DESIGN\referencias.md` |
| Referência universal (sem cliente) | não existe: toda ficha mora num cliente |

## 3. Pipeline Taste Engine em 4 Etapas e Ficha Padrão
Toda referência é decodificada em **5 dimensões** (*Câmera: altura/ângulo, enquadramento e perspectiva* · *Luz: direção, dureza, contraste e fonte aparente* · *Profundidade: planos, foco e separação do herói* · *Atmosfera: cor, textura, clima e densidade* · *Composição: peso visual, espaço negativo e função comercial*) seguindo o **Pipeline de 4 Etapas**. Registrar o que é visível; lente, abertura, Kelvin, equipamento e prompt original são hipóteses, salvo metadado verificável. Se a referência não mostrar um eixo, deixar esse eixo livre para a direção do cliente.
1. `Evidência Física` (o que está fisicamente visível na imagem);
2. `Padrão Estrutural` (a mecânica óptica, tipográfica ou compositiva por trás);
3. `Regra Transferível pro KV` (princípio traduzido para os tokens do cliente);
4. `Anti-Regra / Veto` (o que descartar para evitar plágio ou cara de IA).

```text
### R[n] · [apelido curto] · [arquivo]
Evidência & Técnica: câmera/enquadramento/perspectiva · luz visível/direção/contraste · planos/foco · atmosfera/paleta/textura · composição/hierarquia/CTA quando houver.
Olhar criativo: a proposição visual por trás (metáfora, tensão, recorte) em 1 frase.
Regra Transferível no KV [cliente]: o que entra (traduzido para tokens do cliente).
Anti-Regra (Vetos): o que NÃO entra (elementos proprietários de terceiros ou conflitos com o KV).
Usar em: tipo de post/slide/LP onde rende mais.
```

## 4. Mixagem de Referências por Função Exclusiva (Job-Based Reference Mixing)
Quando o usuário enviar **2 ou mais referências** para uma mesma peça:
- **Proibido misturar tudo num meio-termo confuso.** Dar a cada referência um papel explícito, conforme a indicação do usuário ou a característica mais útil: câmera/composição, luz/profundidade, atmosfera/paleta, material/acabamento ou gesto narrativo. Uma referência pode fornecer mais de um eixo quando for coerente; declarar prioridade se houver conflito.
- Produto/rosto real e KV do cliente não são substituídos por referência estética. Transferir mecanismos, não o assunto ou a identidade de terceiros.
- Se o usuário pedir engenharia reversa completa de 1 foto para gerar cena idêntica em IA, acionar o **Vision Decomposer** (`imagem.md` Parte B §5).

## 5. Síntese (fim do arquivo) e Uso na Criação
- **Padrões recorrentes** (3–6 linhas): o que várias referências fazem igual.
- **Receitas para o KV** (3–6): combinações prontas e acionáveis.
- **Banco de ideias** (5–10 linhas): conceitos de post/slide derivados, já no KV, prontos para briefing futuro.
- **Guarda de Originalidade:** descartar assunto literal, identidade de terceiros, logos, slogans ou mascotes da referência — transferir apenas a física de luz, proporção, ritmo e acabamento.
- Na criação com referências: citar em 1 linha quais fichas/funções (`R1 [Luz] + R3 [Câmera]`) foram aplicadas. Referência ausente não bloqueia a peça; usar a direção inicial de `imagem.md` Parte C. Receita aprovada sobe para `## 2. O QUE FAZER` do `design_system.md`.
