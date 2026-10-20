# Módulo Produto · Subject Reference (produto/objeto fiel por IA)

Nome técnico: **subject-driven generation com Subject Reference + turnaround sheet** (folha de vistas 360). É o `personagem.md` aplicado a objeto: aeronave, carro, embalagem, máquina, imóvel, peça. Carregar junto com `imagem.md`. Ativar com `/designer-mestre produto` (aliases: `subject`, `twin`, `360`). O que é de cada produto mora só na pasta do cliente; aqui fica só o método.

## 1. Onde fica cada coisa
| O quê | Onde |
|---|---|
| Fotos reais do produto | `[Cliente]\Compartilhada\Imagens\Originais\[Produto]\` (só leitura) |
| Padrão do produto | `[Cliente]\_DESIGN\Produtos\[Produto]\PRODUTO_[NOME].md` |
| Pacote de referência + turnaround | `[Cliente]\_DESIGN\Produtos\[Produto]\referencias\` |
| Imagens geradas (inclusive descartadas) | `[Cliente]\Compartilhada\Imagens\IA\` + `.txt` do prompt |

## 2. Regra de ouro (antes de gerar)
- **Foto real primeiro.** `Originais\` → `Banco de Imagens\` → só então IA. Se o briefing diz "foto real", IA só com o "ok" do usuário, registrado no `design_system.md`.
- **Referência = o produto DO CLIENTE.** Render de loja 3D, foto de terceiro ou de outro exemplar do modelo só entram como apoio de forma (geometria), nunca como mestra: pintura, faixas, logos e acabamentos vêm só das fotos reais do cliente. Marca d'água, matrícula/placa, número de série e logo de terceiro nunca vão para o prompt nem para a saída.
- Produto regulado ou técnico (aeronave, veículo, equipamento médico): não inventar peça, configuração, pintura ou versão que o cliente não tem.

## 3. Construir o padrão (uma vez por produto)
1. **Reunir** todas as fotos reais. Escolher **4–8 vistas** que cubram o turnaround: frente, ¾ frente E/D, lateral, ¾ traseira, traseira, detalhe 1–3 (ex.: motor, janela, cauda). Mestra = ¾ frente com melhor luz e nitidez.
2. **Pacote:** cópias com 2048 px no lado maior, nome `_ref`, e um `turnaround_[produto].jpg` (todas as vistas numa folha, fundo neutro) só para conferência humana e, quando a ferramenta aceitar 1 imagem só, como referência única.
3. **Faltou vista?** Gerar a vista que falta a partir da mestra em ferramenta de troca de ângulo local: `gerar_imagem.py gerar "same product as image 0, seen from <ângulo>, plain light-grey studio background" --ref mestra.jpg --ref vista_mais_proxima.jpg` (Easy Diffusion v4 + FLUX.2 klein 4B); image-to-3D local (TripoSR/InstantMesh, já em `Memória\`) só se o usuário pedir e **validar contra as fotos reais** antes de entrar no pacote. Vista gerada fica marcada `_gerada` e nunca vira mestra.
4. **Checklist de identidade** (só o observável, numerado): silhueta/proporção, nº e forma de janelas/aberturas, posição de motores/rodas, cauda/traseira, cores e faixas exatas (com posição), acabamento (brilho/fosco), elementos proibidos (matrícula, logo de terceiro).
5. **Regras corretivas:** linhas curtas contra erros do modelo ("não adicionar janela", "faixa azul termina antes do motor"). Crescem a cada falha.
6. **Descritor** (inglês, 1 parágrafo) + "keep the object's shape, proportions, livery and details exactly as in the reference images; no text, no registration marks".

## 4. Gerar
- **Ferramenta com referência** obrigatória — padrão local: Easy Diffusion **v4** + FLUX.2 klein **4B** com `--ref` (até 4: mestra, vista do ângulo, detalhe; ver `imagem.md` §1). Nuvem (Nano Banana, GPT Image, Runway) só se o usuário pedir pelo nome. Só texto não preserva o produto: sem ferramenta, entregar o prompt e parar.
- **Envio:** mestra + vista mais próxima do ângulo pedido + 1 detalhe (3–4 no total). Para inserir o produto numa foto real (ex.: hangar), enviar a **cena** como imagem base e o produto como referência; pedir escala, sombra de contato, reflexo do piso e luz coerentes com a cena.
- **Prompt:** briefing de fotógrafo; descrever só o que muda (cena, ângulo, luz, lente). Sem texto, logo, matrícula.
- **Composição alternativa (mais fiel):** gerar só o produto no ângulo certo e compor no SVG/Figma sobre a foto real, com sombra e cor ajustadas.

## 5. Verificar e corrigir
1. Comparar com a mestra item a item do checklist (passa/falha).
2. Falhou: (1) corrigir prompt com a regra corretiva; (2) trocar/limpar referências; (3) gerar produto isolado + compor; (4) só se recorrente em muitas peças: LoRA de produto. Máx. 3 tentativas por degrau.
3. Salvar tudo em `Imagens\IA\` (`AAAA-MM-DD_[titulo]_v[n].png` + `.txt`: ferramenta, referências, prompt, resultado do checklist). Atualizar o `PRODUTO_*.md` com regra nova.

## 6. Custo e segurança
- Geração local é grátis: até 4 variações por rodada, 3 rodadas. Geração em nuvem (só sob pedido): mostrar custo e pedir aprovação antes de cada rodada.
- Fotos do cliente enviadas a API vão a terceiros: dizer o serviço antes do primeiro uso. Chave só em variável de ambiente.
- Licença: render de loja 3D (ex.: Hum3D) é de terceiro; usar só como referência de forma, nunca na peça.

## Checklist
- [ ] Foto real tentada antes; uso de IA autorizado quando o briefing pede "real"
- [ ] Mestra = foto real do produto do cliente; vistas geradas marcadas `_gerada`
- [ ] Checklist de identidade + regras corretivas no `PRODUTO_*.md`
- [ ] Sem matrícula/placa/logo de terceiro/marca d'água na saída
- [ ] Saídas + `.txt` em `Imagens\IA\`; `historico.md` atualizado
