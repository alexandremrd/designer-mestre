# Agente /designer-mestre — pasta raiz

**Designer Mestre** é um agente de design universal. Cobre todo pedido de design ou de cliente (briefing, ads, posts, LP, deck, vídeo, imagem, Figma) e tem prioridade sobre qualquer outra skill de design. Chamada: `/designer-mestre`.

## Fluxo
1. **Briefing:** o texto, e-mail ou PDF do cliente vira `briefing.md`.
2. **Tipo de pedido:** mecânico (legenda, redimensionar, trocar texto ou cor) é executado direto; criativo novo passa por prévia, espera o "aprovado" e só então vai para o Figma.
3. **Gate de KV:** antes de gerar, lê o `design_system.md` do cliente (cores, fontes, logo, vetos). Cliente sem KV passa por `cold-start.md`.
4. **Módulo do pedido:** abre só o módulo do tipo de peça (`ads`, `html`, `deck`, `motion`, `imagem`, `produto`, `video-edicao`, `figma`...).
5. **QA e entrega:** confere uma prancha (cortes, safe zone, copy, logo) e aplica a crítica anti-IA antes de entregar. Salva em pasta padronizada por ano, mês e data.

## Leis principais
- **Logo:** nunca é criada nem alterada. Usa só o arquivo original, ou o placeholder `LOGO [CLIENTE]`.
- **Copy:** literal, sem inventar CTA, selo ou número, e sem promessas absolutas.
- **Isolamento:** nada de um cliente vaza para outro.
- **Peça estática:** SVG de coordenadas absolutas (1080×1350 ou 1080×1920).
- **Figma:** só depois do "aprovado".
- **Anti-IA:** reprova o índigo/violeta genérico de IA, o degradê roxo→azul e o emoji usado como ícone.

## Memória e ferramentas
- **Memória por cliente:** `[pasta de clientes]\[Cliente]\_DESIGN\` (`design_system.md` e `historico.md`). Cada erro ou aprovação é gravado uma vez, no fim do trabalho.
- **Imagem local:** `gerar_imagem.py` (Easy Diffusion + FLUX.2 klein 4B); no Antigravity, Nano Banana Pro.
- **QA de imagem:** `img_qa.py` (ImageMagick).
- **Vídeo e legenda:** `reels_legenda.py` (Whisper + ffmpeg).
- **Motor offline UI/UX:** `engines\uiux` (paletas, fontes e padrões de landing page).

## Onde fica o agente
O agente pode ser baixado e salvo em qualquer pasta. `<PASTA_DO_AGENTE>` nos arquivos significa a pasta onde ele está. A cópia que você edita é a fonte; depois de alterar, rode `INSTALAR_DESIGN_CLAUDE_CODE.cmd` (a partir dessa pasta) para instalar nas ferramentas. As alterações sobrescrevem os arquivos, sem backups.

## Estrutura

```text
<PASTA_DO_AGENTE>\
├── SKILL.md            ← núcleo (v15): velocidade, roteamento, onde rodar, Gate de KV, leis, memória
├── modulos\            ← lidos só quando o pedido é daquele tipo
│   ├── briefing.md     ← NOVO v15: tradutor de briefing (só o que é do designer)
│   ├── cold-start.md   ← cliente novo / KV incompleto (1 vez)
│   ├── ads.md · figma.md
│   ├── video-edicao.md ← NOVO: vídeo do cliente + legenda + overlay + trilha
│   ├── video.md        ← roteiro, UGC, vídeo por IA
│   ├── qualidade.md    ← NOVO: checagem final por tipo (anti-IA, a11y, motion, deck, copy, imagem IA)
│   ├── html.md · html-lp.md · html-print.md · html-relatorio.md · html-form.md
│   ├── kv-logo.md · design-system.md · deck.md · motion.md
│   ├── imagem.md       ← geração LOCAL (Easy Diffusion) + fórmula de prompt
│   ├── personagem.md · produto.md · referencias.md · pen.md
├── assets\             ← gerar_imagem.py (NOVO v15) · img_qa.py (NOVO v15) · reels_legenda.py · base_lp.html · qa_html.py · validacao-forms.js/.css
├── engines\uiux\       ← NOVO: motor offline UI UX Pro Max (paletas, fontes, padrões de LP, regras UX; MIT)
├── references\  figma_engine\  pen_engine\
├── Clientes\_TEMPLATE_CLIENTE\  ← design_system.md + historico.md
├── CREDITOS_HTML.md
└── INSTALAR_DESIGN_CLAUDE_CODE.cmd
```

A memória de cada cliente fica em `D:\Clientes\[Cliente]\_DESIGN\` (`design_system.md` + `historico.md` + `templates\`). Nada de cliente mora nesta pasta.

## Requisitos de imagem (uma vez, tudo local)
- ImageMagick 7: `winget install ImageMagick.ImageMagick` (prancha, paridade, paleta, contraste, WebP via `assets\img_qa.py`).
- Easy Diffusion (pacote `easydiffusion-main`): instalar, Settings › Backend › **v4**, reiniciar; colocar o FLUX.2 klein **4B** (Apache 2.0) em `models\stable-diffusion\`. GPU com ~12 GB de VRAM recomendada. Testar: `python assets\gerar_imagem.py ping`.
- Depois da instalação, nada sai do PC: sem conta, sem chave, sem API.

## Requisitos para vídeo (uma vez)
- `ffmpeg` no PATH: `winget install Gyan.FFmpeg`
- Python 3.10+ e `pip install faster-whisper` (o instalador oferece)
- Rodar edição de vídeo numa sessão **Code** do Claude Desktop (sem limite de rede e com acesso ao disco).

## Como alterar
1. Pedir a mudança ("atualiza o /designer-mestre: ...").
2. O agente sobrescreve o arquivo aqui e registra no Changelog.
3. Rodar `INSTALAR_DESIGN_CLAUDE_CODE.cmd`.

Só regras universais entram aqui. Preferência de cliente vai no `design_system.md` dele.

## Créditos de terceiros
- Regras de `qualidade.md` §A/§E/§H/§I e exportação `DESIGN.md` de `design-system.md` destiladas de Open Design (nexu-io/open-design) e awesome-design-md; fórmula 70/30 do `imagem.md` de gerar-imagem-skill. Nenhum código copiado.
- `assets\gerar_imagem.py` usa a API local do Easy Diffusion (cmdr2/easydiffusion); `assets\img_qa.py` chama o ImageMagick instalado.
- `engines\uiux\` — UI UX Pro Max, © 2024 Next Level Builder, MIT.
- Regras de `qualidade.md` destiladas de ECC (MIT), Ponytail (MIT) e claude-video (MIT); nenhum código deles foi copiado além do `engines\uiux\`.

## Changelog
- v9 (19/10/2026): prévia aprovada antes de montar no Figma.
- v10 (19/10/2026): uma versão só; versões novas sobrescrevem.
- v11 (19/10/2026): Fast-Track de KV, `design_system.md` único, SVG-First, regra de `Referencias\`.
- v12 (19/10/2026): enxuto — núcleo ~9 KB; Cold Start em módulo; `html.md` dividido; teto do `design_system.md`; memória numa escrita.
- v13 (19/10/2026): **rápido e sem travas** — seção 0 de velocidade (faça sem anunciar, suponha e declare, uma rodada de correção); pedido **mecânico** vs **criativo novo** (mecânico não tem prévia); seção "onde rodar" (vídeo/render no PC via sessão Code, comando pronto em vez de bloqueio); legenda = fala transcrita, não copy; novo `video-edicao.md` + `assets\reels_legenda.py` (Whisper por palavra, legenda .ass no KV com destaque, overlay PNG, corte de pausas, trilha, 16 Mbps, `.srt` para revisão); novo `qualidade.md`; motor offline `engines\uiux\` para cliente sem KV; `/rapido`.
- v13.1 (19/10/2026): `_TEMPLATE_CLIENTE\design_system.md` ampliado com o que valia do template externo de extração de KV — conceito e sensação, paleta por papel com regra do acento, cores/formas proibidas, tipografia por nível (peso + caixa), composição/respiro/posição da logo/rodapé, foto em tema · pessoas · luz · contraste, tom de voz e pilares; arquivo é só marca (campanha vai no `briefing.md`); clientes `VALIDADO` não são rebaixados. `imagem.md`: prompt deriva do KV, `avoid` padrão contra UI/mockup, `/promptmaster` gerado sob pedido e nunca salvo.
- v14 (20/10/2026): novo `modulos\produto.md` (Subject Reference / subject-driven generation + turnaround sheet: produto/objeto fiel por IA, mestra = foto real do cliente, checklist de identidade, composição em foto real) e novo `modulos\referencias.md` (prancha única → fichas de texto técnica + criativa + conversão ao KV, Receitas e Banco de ideias em `_DESIGN\referencias.md`, sem reabrir imagens). Comandos `produto` (`subject`/`twin`/`360`) e `ref` (`referencia`/`moodboard`); Gate lê Receitas em pedido criativo.
- v15 (20/10/2026): **imagem 100% local** — `assets\gerar_imagem.py` (Easy Diffusion em 127.0.0.1:9000: `ping`, `modelos`, `gerar` com até 4 `--ref` no motor v4 + FLUX.2 klein 4B, img2img `--init/--forca`, `upscale` RealESRGAN/CodeFormer; grava o `.txt` do prompt) e `assets\img_qa.py` (ImageMagick: `prancha`, `paridade` prévia×Figma por RMSE, `paleta`, `contraste` WCAG, `bbox`, `web` WebP/AVIF). `imagem.md` reescrito com a escada local e a fórmula 70/30 ("identical to reference image 0"; rótulo/logo só no SVG). `qualidade.md`: 7 P0 anti-IA com HEX, teto do acento, regra 80/20, crítica 5 eixos pela pior faixa (§H), números de tipografia (§I), ritmo de deck. `design-system.md`: camadas de token A1/A2/B e exportação derivada `tokens.css` + `DESIGN.md`. Núcleo: linha `Leitura:` em criativo novo, comandos `gerar`/`qa`, leis 5/7/8 ligadas aos scripts. `produto.md` sem dependência de nuvem. `references\05` deixa de citar os arquivos legados. Novo `modulos\briefing.md`: tradutor de briefing (tabela de peças, copy literal, bloqueios ≤ 3 com recomendação, fora do escopo do designer em 1 linha), salvo como `briefing.md` da solicitação; comando `briefing` (`brief`, `traduz`). Herdados da versão da conta: prioridade sobre outras rotas, regras de formulário HTML, referências enviadas. Avaliados e descartados: nanoGPT (treino de texto, sem uso em design).
- v15.1 (20/10/2026): **núcleo enxuto** — 13,7 KB → ~7 KB: §8 Essenciais sai da versão do PC (os módulos estão lá; fica só na skill da conta, comprimida); tabela de material fundida nas leis; P0 anti-IA + crítica dentro da lei 8 (criativo novo não abre mais o `qualidade.md`); regras de economia em §0 (prancha ≤ 540 px, SVG de trabalho sem base64, editar por trecho, leitura pesada delegada); descrição da skill encurtada (vai em toda sessão).
- v15.2 (20/10/2026): **Antigravity na geração de imagem** — degrau 2 do `imagem.md`: sessão no Antigravity usa a ferramenta nativa (Nano Banana Pro, cota do plano Pro) e registra com `gerar_imagem.py registrar` (copia para `Imagens\IA\` + `.txt`); cota esgotada cai para o Easy Diffusion; Claude Code entrega o comando para rodar no Antigravity; proibido reaproveitar o login do Antigravity fora dele.

- v16 (20/10/2026): **renomeado para Designer Mestre** (`/designer-mestre`); nome pessoal removido de todos os arquivos; caminhos fixos trocados por `<PASTA_DO_AGENTE>` (o agente roda de qualquer pasta); resumo do agente e fluxo adicionados ao topo deste README.
