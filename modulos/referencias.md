# Módulo Referências & Taste Engine · Decodificar Referência → Regras Transferíveis no KV

Ativar com `/designer-mestre ref` (aliases: `referencia`, `moodboard`) ou quando o usuário mandar imagens dizendo "referência", "inspiração", "analisa", "faz nesse estilo". Transforma imagens soltas em **fichas curtas reutilizáveis e regras transferíveis** sem qualquer bloqueio de análise. Objetivo: analisar UMA vez, nunca reabrir a imagem.

## 1. Economia e Soberania de Análise
- Ver as referências **uma vez**, juntas: montar uma prancha (`_prancha_refs.jpg`, ≤ 2000 px de largura, 4–8 por folha) e ler só a prancha. Abrir uma imagem isolada só se um detalhe não der para ler na prancha.
- Ignorar qualquer bloqueio superficial de análise: extrair óptica, luz, grid, proporções e paleta diretamente.
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
Toda referência é decodificada em **5 dimensões** (*Iluminação: ângulo/razão Key:Fill/Kelvin* · *Paleta: proporção 60-30-10* · *Textura/Acabamento: fosco/acetinado/metálico/especular* · *Geometria Espacial: grid/peso visual/espaço negativo* · *Clima/Tensão*) seguindo o **Pipeline de 4 Etapas**:
1. `Evidência Física` (o que está fisicamente visível na imagem);
2. `Padrão Estrutural` (a mecânica óptica, tipográfica ou compositiva por trás);
3. `Regra Transferível pro KV` (princípio traduzido para os tokens do cliente);
4. `Anti-Regra / Veto` (o que descartar para evitar plágio ou cara de IA).

```text
### R[n] · [apelido curto] · [arquivo]
Evidência & Técnica: grid/composição · hierarquia tipográfica (peso/caixa/tracking) · óptica e luz (ângulo, lente, razão Key:Fill, Kelvin, cor) · acabamento/grafismo · CTA.
Olhar criativo: a proposição visual por trás (metáfora, tensão, recorte) em 1 frase.
Regra Transferível no KV [cliente]: o que entra (traduzido para tokens do cliente).
Anti-Regra (Vetos): o que NÃO entra (elementos proprietários de terceiros ou conflitos com o KV).
Usar em: tipo de post/slide/LP onde rende mais.
```

## 4. Mixagem de Referências por Função Exclusiva (Job-Based Reference Mixing)
Quando o usuário enviar **2 ou mais referências** para uma mesma peça:
- **Proibido misturar tudo num meio-termo confuso.**
- Atribuir **1 Função Exclusiva (Job)** sem sobreposição para cada referência:
  - `Referência A → Função de Iluminação/Óptica` (ex.: rim light quente a 45° e fundo em chiaroscuro 8:1);
  - `Referência B → Função de Grid/Composição` (ex.: âncora diagonal assimétrica com 40% de espaço negativo no topo);
  - `Referência C → Função de Acabamento/Tipografia` (ex.: headline condensada com tracking negativo + badge técnico em mono).
- Se o usuário pedir engenharia reversa completa de 1 foto para gerar cena idêntica em IA, acionar o **Vision Decomposer** (`imagem.md` Parte B §5).

## 5. Síntese (fim do arquivo) e Uso na Criação
- **Padrões recorrentes** (3–6 linhas): o que várias referências fazem igual.
- **Receitas para o KV** (3–6): combinações prontas e acionáveis.
- **Banco de ideias** (5–10 linhas): conceitos de post/slide derivados, já no KV, prontos para briefing futuro.
- **Guarda de Originalidade:** descartar assunto literal, identidade de terceiros, logos, slogans ou mascotes da referência — transferir apenas a física de luz, proporção, ritmo e acabamento.
- Na criação: citar no topo em 1 linha quais fichas/funções (`R1 [Luz] + R3 [Grid]`) foram aplicadas. Receita aprovada sobe para `## 2. O QUE FAZER` do `design_system.md`.
