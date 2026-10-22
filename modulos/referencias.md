# Módulo Referências · Decodificar linguagem visual e KV → Regras Transferíveis

Ativar com `/designer-mestre ref` (aliases: `referencia`, `moodboard`), quando o usuário indicar imagens como referência/inspiração, ou pedir para entender o KV, a linguagem visual ou o estilo de uma marca/campanha de referência. Transforma materiais visuais em **fichas curtas reutilizáveis e regras transferíveis**. Se o usuário pedir análise ou ajuste de um criativo próprio em SVG, use `ads.md` §6: não confunda diagnóstico da peça com decodificação de referências. Objetivo: analisar cada referência uma vez e registrar uma síntese que possa orientar a criação sem reabrir o material.

## 1. Economia de Análise
- Ver as referências **uma vez**, juntas: montar uma prancha (`_prancha_refs.jpg`, ≤ 2000 px de largura, 4–8 por folha) e ler só a prancha. Abrir uma imagem isolada só se um detalhe não der para ler na prancha.
- Extrair óptica, luz, grid, proporções e paleta direto da imagem enviada.
- Gravar o resultado como **texto**. Depois disso, o agente lê só o arquivo de texto (nunca as imagens) para criar.
- Ficha de ativo com teto de ~700 caracteres. Síntese de sistema/campanha pode ocupar até 1,5 KB; arquivo do cliente com teto de ~8 KB. Passou disso, fundir fichas e retirar observações redundantes, sem apagar evidências que sustentam uma regra.
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

## 4. Engenharia reversa do sistema visual de uma referência
Ative esta leitura quando o pedido for entender o **KV da marca/campanha de referência**, não apenas tomar uma peça como inspiração. Leia a fonte indicada e classifique o objeto da análise:
- **Sistema de marca:** códigos duráveis que aparecem em pontos de contato ou campanhas diferentes.
- **KV/plataforma de campanha:** regras visuais recorrentes dentro de uma campanha específica; não generalize automaticamente para a marca inteira.
- **Peça isolada:** escolhas observáveis naquela execução; sem outras amostras, não as declare regras do sistema.

Monte uma pequena trilha de evidências com arquivo/URL, canal ou campanha e data/contexto disponível. Para cada conclusão, separe **observado**, **inferido** e **não verificável**. Registre confiança baixa quando houver uma só peça ou contexto incerto; recorrência em várias peças de uma campanha pode sustentar confiança média sobre aquele KV; confiança alta sobre código de marca exige recorrência coerente entre campanhas ou pontos de contato independentes. Repetição em peças da mesma campanha sustenta uma hipótese de KV de campanha, não necessariamente de identidade permanente. Contradições são variações ou lacunas a explicar, não ruído a apagar.

Compare relações e funções, não apenas cores ou objetos: papel e comportamento da logo; papéis cromáticos e contrastes; hierarquia e uso expressivo da tipografia; formas, grafismos e texturas recorrentes; tratamento de imagem e retrato; construção da composição, ritmo, densidade e espaço negativo; hierarquia de mensagem e adaptação por canal. Marque cada achado como **código recorrente**, **dispositivo de campanha**, **convenção de canal** ou **escolha pontual** e anote uma exceção relevante.

### Transferência para uma peça de cliente
1. Leia primeiro o `design_system.md`, as peças aprovadas pertinentes e as restrições deste briefing. Trate o KV comprovado como contrato para cor, tipografia, fotografia, luz/grade, efeitos, elementos gráficos e composição — não apenas como paleta ou logo.
2. Classifique a intenção das referências como **ambição**, **técnica** ou **pedido explícito de mudança de identidade**. Na ausência deste último, nenhuma referência externa revoga o KV. A falta de informação sobre um código do cliente não transforma automaticamente esse código em campo livre.
3. Para duas ou mais referências, siga §5 para atribuir funções sem misturar sistemas visuais. Em cada técnica escolhida, explicite a adaptação aos códigos do cliente e o que foi deliberadamente descartado.
4. Entregue uma direção executável, não adjetivos: crop e posição do retrato; luz e gradação compatíveis com a foto/KV; efeitos e grafismos permitidos; percurso e massas da composição; família e hierarquia tipográfica do cliente; paleta do cliente. Cada decisão visual deve apontar para a fonte do KV ou para a técnica específica que está sendo adaptada.
5. Faça uma comparação de preservação após o render. Se fotografia, contraste, cor, tipografia, efeitos ou assinatura gráfica passaram a pertencer à referência em vez do cliente, a adaptação falhou mesmo que a peça esteja bem acabada; corrija antes de entregar. Só altere um código do KV com pedido explícito do usuário.

O [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) informa agentes com regras concretas e organizadas por papel — tema, cores semânticas, hierarquia tipográfica, componentes, layout, profundidade e elevação, do's/don'ts e guia de prompt. Essa estrutura é útil para tornar um KV operacional e verificável. O repositório descreve principalmente sistemas de interfaces web; aplique sua clareza de papéis e restrições, não seus tokens ou componentes, a anúncios e fotografia de campanha.

Entregue a síntese em quatro blocos:
1. **Gramática visual observada** — elementos, relações e evidências que se repetem.
2. **Variação e limites** — o que muda entre peças/canais e quais hipóteses ainda são fracas.
3. **Tradução para o KV do cliente** — códigos do cliente que permanecem fixos; mecanismo de referência escolhido para cada camada; adaptação compatível; itens conflitantes descartados.
4. **Direção original** — uma execução específica que preserve os códigos do cliente em todas as camadas, melhore a relação entre mensagem e imagem e não copie o layout. Copy continua literal conforme a Lei 4; a análise de referência não autoriza reescrevê-la.

Uma referência de terceiros não se torna KV do cliente. Transfira a lógica visual em nível abstrato; não reutilize logo, assinatura, slogan, texto, mascote, assets proprietários nem composição distintiva. Para uma única imagem, descreva apenas o que ela permite observar e apresente o restante como hipótese, sem alegar que reconstruiu um brand book completo.

Calibração: um cartaz isolado → descreva a peça e deixe a identidade ampla como hipótese; vários anúncios de uma campanha → extraia o KV daquela campanha; os mesmos códigos em site, social e campanhas diferentes → considere-os candidatos a códigos recorrentes de marca, sempre citando as fontes. Guarde a leitura da referência em `referencias.md`; ela não substitui nem altera o `design_system.md` validado do cliente.

## 5. Atribuição de Função a Referências Múltiplas
Quando o usuário enviar **2 ou mais referências** para uma mesma peça:
- **Escolha uma referência principal** pela compatibilidade com o KV e a mensagem. Nomeie a função de cada complementar (por exemplo, luz, profundidade ou acabamento) e use sua técnica somente numa camada distinta e compatível do KV. Várias técnicas podem coexistir; não importe uma estética inteira nem combine paletas, tipografias ou gramáticas de composição conflitantes. A indicação explícita do usuário orienta a seleção, mas não altera o KV sem pedido claro de redesign.
- Produto/rosto real e KV do cliente não são substituídos por referência estética. Transferir mecanismos, não o assunto ou a identidade de terceiros.
- Se o usuário pedir engenharia reversa completa de 1 foto para gerar cena idêntica em IA, acionar o **Vision Decomposer** (`imagem.md` Parte B §5).

## 6. Síntese (fim do arquivo) e Uso na Criação
- **Padrões recorrentes** (3–6 linhas): o que várias referências fazem igual.
- **Receitas para o KV** (3–6): combinações prontas e acionáveis.
- **Banco de ideias** (5–10 linhas): conceitos de post/slide derivados, já no KV, prontos para briefing futuro.
- **Guarda de Originalidade:** descartar assunto literal, identidade de terceiros, logos, slogans ou mascotes da referência — transferir apenas a física de luz, proporção, ritmo e acabamento.
- Na criação com referências: citar em 1 linha quais fichas/funções (`R1 [Luz] + R3 [Câmera]`) foram aplicadas. Referência ausente não bloqueia a peça; usar a direção inicial de `imagem.md` Parte C. Receita aprovada sobe para `## 2. O QUE FAZER` do `design_system.md`.

**Referências de método consultadas** (inspiração metodológica; não são dependências instaladas nem material para copiar): [Naksha Studio — brand strategy](https://github.com/Adityaraj0421/naksha-studio/blob/f5275255d1c5417026508c5e294cf6d27ec8809d/commands/brand-strategy.md) para separar auditoria de posicionamento e comparar pontos de contato; [UPPAbaby Brand Review](https://github.com/zrosenfield/sharepoint-ai-skills/blob/62d6481ac3b7d59d5248af46164e037d33d88650/Skills/uppababy-brand-review/SKILL.md) para critérios visuais explícitos, evidências e limites de avaliação. Nenhum dos repositórios analisados executa sozinho o ciclo completo de descoberta de KV por site, Instagram e peças; classificação de recorrência e confiança é uma adaptação desta skill.
