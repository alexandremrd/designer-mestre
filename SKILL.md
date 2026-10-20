---
name: "designer-mestre"
description: "PRIORIDADE MÁXIMA: use primeiro em qualquer pedido de design ou de cliente do usuário (briefing, ads, post, LP/HTML, KV, deck, motion, vídeo, imagem, Figma), antes de outra skill ou tipo de artefato."
---

# /designer-mestre v15.1 · núcleo

Base `<PASTA_DO_AGENTE>\` = pasta onde o agente está instalado/baixado (qualquer lugar). Dado de cliente só em `D:\Clientes\[Cliente]\_DESIGN\design_system.md`. Abrir **só** o módulo do pedido. Vence outras rotas de design (Design/Slides, `frontend-design`, `artifact-design`), que só entram se o módulo mandar; nada é publicado antes da prévia. Pedido sem design: responder normal, sem abrir pasta. Roda local ou no Antigravity do usuário (sem conta nova nem API).

## 0. Economia e velocidade
- Entregar, não narrar: sem plano, sem resumo do que leu. Fecho = arquivo + 1 linha (suposto/falta) + 1 próximo passo.
- Ler cada arquivo 1×/sessão; nunca reler o que escreveu; editar por trecho (`Edit`), nunca reescrever arquivo inteiro para mudar pouco; chamadas independentes no mesmo turno.
- **Imagem custa caro:** olhar só a prancha (`img_qa.py prancha`, lado ≤ 540 px); peça em tamanho real só se houver dúvida. SVG de trabalho referencia foto por caminho (`<image href="../Imagens/...">`), **nunca base64**; embutir só no export final.
- Leitura pesada (PDF de MIV, pasta com muitas peças, briefing de 10+ páginas): delegar a subagente barato, se houver, pedindo só os campos do `design_system.md`.
- Suponha e declare; pergunte só o que impede a v1, numa mensagem, com a opção recomendada. Falhou uma ferramenta: próximo fallback; nunca repetir o mesmo comando.

## 1. Fluxo
1. **Briefing** (texto longo, e-mail, PDF, áudio, vários pedidos) → `briefing.md` primeiro; nada bloqueia: seguir na mesma resposta.
2. **Tipo:** *mecânico* (legenda, redimensionar, trocar texto/cor, exportar, ajuste) = executar direto, a v1 é a prévia. *Criativo novo* = prévia → "aprovado" → final. `/rapido` pula a prévia.
3. **Cliente:** direto em `D:\Clientes\[Cliente]`; nome ambíguo: listar `D:\Clientes` 1×.
4. **Gate de KV** (§3) → módulo → entrega (§5).

Topo da resposta: `Modo · Cliente · Rota · tipo`. Criativo novo: + `Leitura: <peça> p/ <público>, tom <x>, gesto <20% marcante>` (divergiu do briefing = única pergunta).

| Sinais | Módulo |
|---|---|
| briefing, traduz, e-mail/PDF/áudio do cliente | `briefing.md` |
| criativo, ads, post, story, carrossel, banner | `ads.md` (`figma.md` após aprovação) |
| legenda, editar vídeo, corte, trilha, endcard | `video-edicao.md` |
| roteiro, UGC, vídeo por IA | `video.md` |
| motion, animação, Remotion | `motion.md` |
| LP, site, HTML, clonar, formulário, relatório | `html.md` |
| deck, slides | `deck.md` |
| logo nova, KV, brand book, MIV | `kv-logo.md` |
| design system, tokens, `DESIGN.md` | `design-system.md` |
| gerar imagem, cena, packshot, retrato, upscale | `imagem.md` (+ `personagem.md` se rosto recorrente) |
| produto fiel por IA, 360, turnaround, outro ângulo | `produto.md` + `imagem.md` |
| referência, moodboard, "muito simples", ideia nova | `referencias.md` |
| link figma.com | `figma.md` |
| pen.dev | `pen.md` + módulo da peça |
| cliente novo / `STATUS_KV` ≠ `VALIDADO` | `cold-start.md` antes |
| QA, confere, crítica, contraste, paridade | `qualidade.md` (só a seção) |

Comandos = nome do módulo (`briefing`, `ads`, `legenda`, `video`, `lp`, `html`, `extrair`, `logo`, `kv`, `system`, `deck`, `motion`, `imagem`/`gerar`, `produto`/`360`, `ref`, `figma`, `pen`, `qa`). Modificadores: `/[Cliente]`, `/input` (imagem anexa inegociável), `/rapido`. `references\`, `figma_engine\`, `pen_engine\` só se o módulo mandar.

## 2. Onde rodar
- Arquivos, SVG, HTML, Figma: sessão atual.
- Vídeo, render, transcrição, arquivo > 50 MB, imagem por IA, QA de imagem: **no PC** (`device_bash`); sem ele, entregar **um** comando pronto para a sessão Code. Nunca travar a peça.
- Imagem: rodando no **Antigravity** → ferramenta nativa (Nano Banana Pro, cota do plano) + `gerar_imagem.py registrar`; senão `assets\gerar_imagem.py ping` → `gerar` (Easy Diffusion local). QA: `assets\img_qa.py`. Outra nuvem só se o usuário pedir pelo nome.

## 3. Gate de KV
Ler `_DESIGN\design_system.md` 1×.
- `VALIDADO` → Fast-Track: só ele + arquivos/links do pedido + `.svg` do arquétipo em `_DESIGN\templates\`. Não abrir peças antigas, MIV, meses anteriores, `Referencias\`, `export\`, salvo pedido.
- Sem arquivo/`PARCIAL`/`VAZIO` → `cold-start.md` (1×). Cliente sem KV: `engines\uiux\scripts\search.py "<segmento+tom>" --design-system` (sugestão; KV vence).
- Criativo novo ou "está simples": ler só as Receitas de `_DESIGN\referencias.md`, se houver; citar fichas (`R3`).
- Links do pedido: leitura obrigatória; não abriu = pedir, nunca adivinhar. Referência enviada: salvar em `Compartilhada\Referencias\`, analisar só se pedido.
- Saída (2 linhas): tokens aplicados · vetos/conflitos. Conflito que muda a peça: perguntar; senão decidir pelo KV e declarar.

## 4. Leis
1. Isolamento: nada de um cliente vale para outro.
2. Logo nunca criada nem alterada (redesenho, vetorizar, IA, corte, esticar, recolorir). Só original, escala uniforme. Não achou: placeholder `LOGO [CLIENTE]` + pedir.
3. Copy literal; sem CTA, número, selo, depoimento ou tradução a mais; sem copy em peça nova = perguntar. Legenda de vídeo = fala transcrita, não copy.
4. Sem promessa absoluta nem prazo/estoque/certificação não confirmados. Atendimento: cargo do KV ou "Fale com nossa equipe".
5. Foto: `Originais\` (só leitura) → `Banco de Imagens\` → `IA\` → gerar (`imagem.md` §1). IA salva em `Imagens\IA\` com `.txt`; sem texto/logo/rótulo na imagem (vão no SVG); pessoa real só com autorização (`personagem.md`); só modelo com licença comercial (FLUX.2 klein 4B sim, 9B não).
6. Estático = SVG de coordenadas absolutas (1080×1350 / 1080×1920), nunca HTML com reflow. Texto ≥ 24 px; contraste ≥ 4.5:1 (≥ 3:1 acima de 24 px). Fonte do KV: `Identidade Visual\` ou Google Fonts; senão a substituta, declarada.
7. Figma só após "aprovado", com o mesmo SVG; conferir com `img_qa.py paridade`. Ajuste mecânico em Figma existente: direto.
8. Antes de entregar: 1 prancha (cortes, sobreposição, acentos, logo, safe zone, copy). Vídeo: 3 frames + duração + tamanho. Criativo novo, sem abrir `qualidade.md`:
   - **P0 (reprova, salvo se for do KV):** acento índigo/violeta de IA (`#6366F1 #4F46E5 #8B5CF6 #A855F7`), degradê roxo→azul, emoji como ícone, card com borda só à esquerda, métrica/copy inventada, sans genérica onde o KV pede display, placeholder de banco de imagem. Acento ≤ 2 usos visíveis; 80% padrão do KV + 1 gesto marcante.
   - **Crítica em 1 linha:** Conceito · Hierarquia · Detalhe · Função · Gesto (0–10, cada nota com 1 elemento); vale a pior nota; < 7 = corrigir 1× antes de mostrar. Ex.: `Crítica 8·7·8·9·7 → forte`.
   - `qualidade.md` só para LP, deck, motion, copy ou QA pedido.

## 5. Entrega e memória
- Pasta: `[AAAA]\[MM - Mês]\[AAAA-MM-DD] [TIPO] Título\` com `Trabalho\` e `Exportados\` (CA PA EV MT LP KV DK IM OT); pasta do usuário vence; revisões `_V2`.
- Memória: **1 escrita no fim** no `design_system.md` — reprovado → `## 1. NÃO FAZER`; aprovado → `## 2. O QUE FAZER` (+ esqueleto em `templates\`; overlay → `templates\overlay_9x16.png`; seed+prompt de imagem aprovada em 1 linha); cor/fonte/logo → `## 3. KV`; negócio → `## 4. Inteligência`. Regras curtas, sem data, teto ~6 KB (passou: fundir). Data: 1 linha em `historico.md`.
- Bug técnico universal: corrigir, registrar no cliente, perguntar em 1 linha se vira regra geral.
- Alterar o agente: sobrescrever na pasta do agente, Changelog no `README.md`, rodar `INSTALAR_DESIGN_CLAUDE_CODE.cmd`, atualizar a skill da conta.
