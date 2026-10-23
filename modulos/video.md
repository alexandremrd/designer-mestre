# Módulo Vídeo, Edição (Legenda + KV), Dramaturgia para IA de Vídeo e Motion

Módulo autônomo e unificado para **edição mecânica** de vídeo do cliente (legenda queimada no KV + overlay + trilha + corte de pausas), **direção dramatúrgica** de roteiro/UGC/IA de vídeo e **motion design** programático. Opera com ferramentas nativas e scripts internos (`assets\reels_legenda.py`; locução e efeitos sonoros pela API ElevenLabs em `assets\gerar_audio.py`, Parte B §1.1).

---

## Parte A · Edição de vídeo do cliente (legenda + overlay + KV)

Pedido **mecânico**: executar direto, sem prévia de frames. A v1 renderizada é a prévia. Pasta `[EV]` (ou a que o usuário já criou).

### 1. Entrega mínima (sempre)
Legenda queimada no KV + overlay da marca + exportação 1080×1920. Todo o resto é extra declarado em 1 linha, nunca bloqueio:

| Extra | Padrão sem resposta |
|---|---|
| Cortar pausas | Sim, `--cortar-pausas 0.6` (o roteiro curto pede; a fala fica intacta) |
| Trilha | Usar a da pasta `Música\` se existir; senão sem trilha e avisar |
| Hook/headline no início | Usar o PNG de intro se existir no Figma/pasta; senão sem |
| Endcard/CTA | Só se o arquivo existir; não inventar copy |
| Divergência de headline no briefing | Afeta só a capa/intro; não bloqueia o vídeo |
- Reframe do master 9:16 para 1:1 ou 16:9 só se pedido, conferindo o enquadramento do rosto/produto em cada um.

### 2. Overlay
1. Frame 9:16 no Figma do cliente (link do pedido ou `_DESIGN\templates\overlay_9x16.png`): exportar PNG 1080×1920 **com transparência** (`get_screenshot` não preserva alpha; preferir export do Figma ou montar via SVG).
2. Sem frame: montar SVG 1080×1920 com moldura/gradiente/logo do `design_system.md`, renderizar PNG RGBA autonomamente no navegador headless da IDE e salvar em `Trabalho\`.
3. A faixa de legenda fica em área de leitura: gradiente escuro sob ela, nunca sobre o rosto. O parâmetro `--y` marca a **base (linha inferior)** da legenda: manter `base ≤ 1470` no frame 1080×1920 (ex.: `--y 1380` ou `--y 1400` deixa margem de segurança acima da UI inferior do Reels).

### 3. Transcrição e sincronização (autônoma em cadeia, sem travar)
A máquina escolhe o método disponível na sessão sem depender de serviços externos:
1. `.srt` já existente na pasta → `--srt`.
2. Transcrição multimodal nativa da própria IDE/agente (lendo o áudio/vídeo diretamente) ou motor de transcrição offline local → gera o `.srt` palavra a palavra.
3. Fala enviada pelo usuário → sincronização automática por detecção de silêncio e distribuição proporcional por sílaba/palavra (`--srt`).
Nunca legendar a partir do roteiro sem conferir com a fala real.

### 4. Comando
```
- `--y 1380`: define a **base** da legenda (em px a partir do topo; no ASS `Alignment=2`, `MarginV = 1920 - y`). Seguro para Reels (`base ≤ 1470`; padrão do script: 1400).
python "<AG>\assets\reels_legenda.py" ^
  --video "Original\x.mp4" --overlay "Trabalho\overlay.png" [--intro "Trabalho\intro.png" --intro-s 2] ^
  --fonte "<família exata do KV>" --fontsdir "<pasta com .ttf/.otf>" --tamanho 60 ^
  --cor <texto> --destaque <acento> --contorno <fundo escuro> --y 1380 ^
  --cortar-pausas 0.6 [--musica "Música\m.mp3" --musica-db -20] [--idioma pt] ^
  --out "Exportados\<nome do briefing>.mp4"
```
- 1ª rodada gera `<out>.srt`. Se o usuário corrigir uma palavra, rodar de novo com `--srt <out>.srt` (sem transcrever de novo).
- `--palavras 3–4` e `--max-car 22–26` para Reels; `--caixa-alta` só se o KV pedir.
- Saída: H.264 16 Mbps, AAC 192 k, voz normalizada a -16 LUFS.

### 5. Conferência e Memória
- **Conferência:** prancha com 3 frames (início, meio, fim) + duração + tamanho do arquivo. Checar: legenda dentro da safe zone, sem cobrir rosto/logo, fonte certa (não caiu em Arial), destaque legível, logo sem distorção, nenhuma palavra errada no `.srt`.
- **Memória:** overlay aprovado vira `_DESIGN\templates\overlay_9x16.png` + linha em `## 2. O QUE FAZER` com os parâmetros usados (fonte, tamanho, cores, y). O próximo vídeo do cliente sai com um comando só.

---

## Parte B · Roteiro, Dramaturgia Cinematográfica, UGC e Direção para IA de Vídeo

### 1. Estrutura de Roteiro Publicitário (Sprint de 30 s / 15 s), Voz e Regra dos 6 de Murch
- **Escolha de Formato pelo Objetivo Comercial:** Conversão direta/oferta → Apresentador/Avatar ou UGC de resposta direta · Produto visual/lifestyle → B-roll cinematográfico + locução · Prova social → UGC em 1ª pessoa · Teste misto → Gancho com pessoa (0–3 s) + B-roll de produto no corpo.
- **Arco de 5 Bullets (30 s, máx. 80 palavras faladas; ou 3 Bullets para 15 s com Gancho 0–3 s + Solução/Prova 4–11 s + CTA 12–15 s, máx. 40 palavras):**
  - `• GANCHO (0–3 s)`: para o scroll imediatamente — gerar sempre **3 opções de ângulo** (**Dor** / **Curiosidade** / **Oferta Direta**) e escolher a mais forte;
  - `• PROBLEMA (4–8 s)`: dor ou situação que o público reconhece na hora;
  - `• SOLUÇÃO (9–18 s)`: produto/serviço como resposta direta;
  - `• PROVA (19–24 s)`: resultado concreto, número confirmado ou demonstração visual;
  - `• CTA (25–30 s)`: ação única, clara e imperativa (máx. 2 frases faladas por bullet; variação A/B de teste troca **apenas** os primeiros 3 segundos do gancho).
- **Voz Primeiro & Mixagem de Áudio Padrão:** gerar e aprovar a locução antes de cortar o visual (o áudio dita o tempo exato dos cortes e o respiro das legendas). Parâmetros vocais recomendados para PT-BR natural: estabilidade `0.45–0.55` (`0.40` em UGC para soar espontâneo), similaridade `0.75`, estilo/expressividade `0.20–0.35`, velocidade `1.05–1.10`. Mixagem final: **Voz em `-16 LUFS` integrado · Trilha 12–14 dB abaixo da voz · SFX ~6 dB abaixo da voz**. Disparo de todos os renders de cena sempre em paralelo.
- **Dramaturgia e Fórmula de Cena (obrigatória antes do prompt):**
  - **Fórmula da Cena (1 frase):** `Desejo + Obstáculo + Geometria Espacial (Foreground / Midground / Background) + Direção do Olhar + Ritmo`.
  - **Lei dos 3 Detalhes Físicos por Take:** todo plano deve declarar (1) pressão ambiental (vento, vapor, reflexo de chuva, luz rasante), (2) micro-ação física do corpo/produto, e (3) âncora sonora ou motivo visual.
  - **Lei das 3 Funções:** um take deve mudar a emoção, avançar a ação ou aumentar a pressão; se não fizer nenhum dos três, cortar.
  - **Regra dos 6 de Murch no corte:** Emoção (51%) > História (23%) > Ritmo (10%) > Eye-trace (7%) > Plano 2D (5%) > Espaço 3D (4%).
  - **Escada de Montagem:** `longo → mais curto → mais curto → pausa respiratória → impacto`. A câmera só se move quando há mudança na cena.

### 1.0 Texto de narração para voz por IA (ElevenLabs, Artlist, Murf…)
- **Quando:** todo motion/vídeo com voz, já na análise do briefing (`briefing.md` §3), antes de qualquer cena. Também quando o usuário pedir só o texto da locução.
- **Objetivo único:** extrair do briefing/roteiro/copy o que é **falado**, em texto corrido e limpo, pronto para colar no gerador de voz. Não é revisão de copy nem roteiro novo.
- **Entra:** fala, locução, voz off, narração, diálogo e CTA **falado**, na ordem em que acontecem.
- **Sai (filtragem total):** indicações de cena e direção visual, tempos/cronometragem, texto na tela (lettering, telas, cartelas, chips), instruções de câmera, CTA visual, copy de anúncio/legenda do post, hashtags, fontes/créditos e disclaimers legais.
- **Limpeza:** remover marcadores ("Cena 3", "Narração:", "Áudio:", "Locução:", "VO:", "Fala:", nome do personagem antes da fala, colchetes de direção como "[pausa]" ou "(sorrindo)"). Um parágrafo por bloco de fala; sem bullets, aspas de abertura nem numeração.
- **Fidelidade:** manter palavras, ordem e variante linguística do original (PT-BR, PT-PT, EN…). Mexer só na pontuação para fluidez de leitura (vírgula, ponto, interrogação). Grafia de pronúncia (sigla, número, marca) só com ok do usuário.
- **Planos A/B/C com a mesma fala:** extrair uma vez e avisar. Falas diferentes: um texto por plano, identificado fora do texto.
- **Sem fala no material:** não inventar. Avisar e perguntar se cria a partir do lettering/copy; texto criado só segue após aprovação e é marcado como criado no `.txt`. Narração criada é fala, não lettering: frases completas e naturais, perguntas com "?", acentos certos e nenhum símbolo (/ * @ #) que não seja comando para a IA.
- **Saída:** mostrar o texto ao usuário e gravar `Trabalho\narracao.txt` (só o texto falado). Informar palavras e duração estimada (~2,5 palavras/s em PT-BR) contra a duração pedida; se passar, apontar quanto antes de gerar a voz.

### 1.1 Locução e efeitos sonoros (ElevenLabs · `assets\gerar_audio.py`)
- **Quando:** locução/voz off, narração de vídeo/motion/deck, TTS, efeito sonoro, assinatura sonora. Gera o áudio que o §1 (Voz Primeiro) aprova antes do corte.
- **Chave (conta do próprio usuário, núcleo §6):** procurada em `ELEVENLABS_API_KEY`, `--env-file`, `.env.local`/`.env` da pasta atual e `%USERPROFILE%\.designer-mestre\.env.local`. Sem chave: rodar `checar` primeiro; se faltar, criar `%USERPROFILE%\.designer-mestre\`, rodar ali `npx -y @elevenlabs/cli@latest onboard init` e seguir o que ele imprime — o usuário faz login/autoriza no navegador com a conta dele. Feito uma vez, vale para todos os projetos e sobrevive às atualizações da skill. Nunca pedir/aceitar chave no chat, nunca abrir/imprimir o `.env`, nunca pôr a chave em código. `checar` valida a chave e mostra o saldo sem gastar.
- **Texto falado = `Trabalho\narracao.txt` do §1.0** (lei 4): roteiro aprovado, sem CTA, número ou tradução a mais; pronúncia de marca/sigla se ajusta na grafia do texto falado (com ok do usuário), não na copy da peça.
- **Voz:** a aprovada no `design_system.md` do cliente vence. Sem registro: locução feminina padrão Christine (`TOXnXBKJSHqTwwqoWW0D`, Conversational & Podcast) no `eleven_v4`, sem audio tags salvo pedido (a API não as adiciona sozinha; o agente insere e mostra antes). Clonar voz de pessoa real só com autorização registrada (mesma regra de pessoa real da lei 5).
- **Plano free:** `checar` mostra o plano. No free a API só aceita vozes premade; voz da biblioteca (como a Christine) é gerada pelo usuário no site, e o rascunho sai pela API com premade (Bella `hpp4J3VqNfWAUOO0d1Us`). Uso no free é não comercial por decisão do mantenedor: seguir sem perguntar sobre licença.
- **Comandos:** `python "<AG>\assets\gerar_audio.py" falar "<texto>" -o "Trabalho\locucao_v1.mp3" [--voz ID --estabilidade --similaridade --estilo --velocidade]` (ajustes = parâmetros do §1) · `falar --arquivo roteiro.txt` · `efeito "<descrição física do som>" --duracao 3 -o "Trabalho\sfx.mp3"`. Cada saída ganha `.txt` com voz, modelo, ajustes e texto; nunca sobrescreve (`_v2`).
- **Créditos:** toda geração gasta créditos da conta. Gerar só o que o pedido exige; teste avulso, variações A/B e regravação sem mudança de texto/ajuste só com ok do usuário.
- **Fluxo:** rascunho em `Trabalho\` → usuário ouve e aprova → versão final em `Exportados\`; mixagem nos níveis do §1. Sem chave/rede: avisar em 1 linha e entregar roteiro + voz + ajustes prontos (Modo Manual).
- **Memória:** voz aprovada (voice_id, modelo, ajustes) vira 1 linha em `## 2. O QUE FAZER` / assinatura sonora do KV; voz reprovada vai para `## 1. NÃO FAZER`.

### 2. Vocabulário Canônico de Câmera (12 Movimentos e 6 Ângulos)
- **Movimentos:** `Push-in` (tensão/detalhe) · `Pull-back / Dolly out` (revelação de contexto) · `Tracking shot` (acompanhamento lateral) · `Pan` (rotação no eixo horizontal) · `Tilt` (eixo vertical, imponência) · `Crane up/down` (abertura/revelação vertical) · `Orbit / Arc` (giro 360° heroico no produto) · `Dolly zoom` (vertigem dramática) · `Handheld / Steadicam` (realismo UGC/documental) · `Static / Locked-off` (packshot limpo) · `Slow-motion` (luxo/impacto físico) · `Timelapse` (transformação temporal).
- **Ângulos:** `Eye-level` (neutro/humano) · `Low angle` (poder/aspiracional/luxo) · `High angle` (visão geral) · `Bird's eye / Top-down` (flat-lay geométrico) · `Dutch angle` (tensão) · `Over-the-shoulder / POV` (intimismo, unboxing).

### 3. Os 7 Pilares do UGC Ultra-Realista (Sem Cara de IA)
Para vídeos de criadores/usuários (Unboxing, Review/Depoimento com pequena hesitação natural *"tipo… como eu explico…"*, Rotina *"Day with"* ou Antes/Depois com mesma luz e ângulo), combater a perfeição sintética aplicando obrigatoriamente os **7 Pilares**:
1. **Câmera Imperfeita:** `handheld smartphone footage, slight natural camera shake, selfie front-facing angle slightly below eye level, 1-3 degree tilt, casual reframing mid-shot`.
2. **Iluminação Natural de Janela:** `natural side window lighting, slight overexposure on one side, no ring light reflections, visible soft shadows`.
3. **Ambiente Vivido Real:** `lived-in room background, everyday objects visible on shelves/counter, no studio backdrop, faint natural ambient room noise`.
4. **Performance Humana Autêntica:** `authentic human expressions, natural micro-pauses before speaking, genuine smile building slowly, unscripted hand gestures, occasional glance down at product`.
5. **Linguagem Óptica de Smartphone:** `shot on smartphone portrait mode, f/1.8 shallow bokeh, slight digital compression grain, warm slightly saturated colors, 9:16 vertical format`.
6. **Edição Orgânica:** cortes secos diretos, 1–2 jump cuts intencionais, durações variadas por plano (2 s, 4 s, 3 s) e ritmo calibrado por plataforma (TikTok 15–30 s rápido/saturado · Reels 30–60 s médio/lifestyle · Shorts 45–60 s informativo · Stories 15 s casual extremo).
7. **Especificidade da Persona e Produto em Uso Real:** roupa cotidiana real, cabelo natural, textura de pele real (`natural skin texture, pores visible, no beauty filter`) e interação física tátil com o produto. Depoimento só real ou claramente encenado por ator; nunca apresentar ficção como cliente verdadeiro.
- **Sequência por formato:** unboxing = reação ao pacote → abertura com esforço → 1º contato → reação sensorial → mostra à câmera; review = olhar à câmera → contexto → uso → ressalva curta → CTA da copy; antes/depois = mesma luz, ângulo e roupa. Pós: 1–2 jump cuts, legenda via `reels_legenda.py`, áudio ambiente baixo.

### 4. Anatomia de 10 Elementos do Prompt Cinematográfico & Adaptadores de Física por Motor
- **Prosa Cinematográfica Contínua em Inglês (80–150 palavras, verbos no presente, zero bullets dentro do prompt final, 1 ação principal por cena + Character Sheet fixo repetido entre cenas do mesmo projeto):**
  1. `Shot type & camera` → 2. `Subject & physical action` → 3. `Setting & 3-plane environment` → 4. `Lighting (source, direction, Key:Fill ratio, Kelvin)` → 5. `Color palette & mood` → 6. `Lens & depth of field (24mm/40mm anamorphic/50mm/85mm)` → 7. `Camera movement` → 8. `Atmosphere & texture (rain, steam, dust, 16mm/35mm grain)` → 9. `Visual style reference` → 10. `Duration & pacing`.
- **Adaptação por Motor:**
  - **Veo 3 / 3.1:** brilha em cenas cinematográficas longas, física coerente e áudio/SFX sincronizado (para UGC, exigir explicitamente `"phone camera quality, casual home lighting, not cinematic"`).
  - **Kling 2.6 / 3.0 Master:** brilha em *Image-to-Video* de produto e consistência de personagem (`[Character A: ...]` binding, `cfg_scale 0.3–0.5` para liberdade ou `0.7–0.9` para aderência estrita + campo de negative prompt).
  - **Seedance 2.5 / v1 Pro:** brilha em movimento corporal humano natural, UGC e sequências multi-plano de até 30 s com diálogo `{ Personagem: "fala" }`.
  - **Sora 2:** movimentos de câmera contínuos e transições espaciais suaves (4s / 8s / 12s).
  - **MiniMax Hailuo:** física volumétrica densa e vetores explícitos de câmera (`[Pan left]`, `[Dolly in]`, `[Orbit]`, intensidade `1–10`).
- **Filtro Anti-Slop de Vídeo:** proibido usar palavras vazias como `cinematic, epic, stunning, masterpiece, beautiful lighting, dynamic camera` — substituir sempre pela descrição física real da luz, lente e movimento. Manter bíblia de consistência em `Trabalho\` da pasta `[EV]`.
- Sem negações no prompt (descrever o que está em cena); negação só no campo negative do motor. Runway (câmera controlada/edição) · Luma (câmera criativa) · Pika (iteração rápida, prompt curto).
- **Claims:** nenhuma cena mostra garantia, resultado financeiro, comparação ou número sem fonte confirmada (lei 4); risco = 1 linha. Teste de ad: clareza e ritmo antes de grade de cor ou transição elaborada.

---

## Parte C · Motion Design Programático (Comps × Skin, Física de Mola e Ancoragem)

- **Separação Estrutural `Comps × Skin`:** construir os momentos do vídeo (**Comps**: `Abertura`, `Ancoragem`, `Bloco de Benefício 1..N`, `Dado/Número`, `Citação`, `Encerramento/CTA`) como componentes modulares reutilizáveis e injetar a identidade do cliente (**Skin**: cores `#HEX`, família tipográfica oficial, logo e assinatura sonora do `design_system.md`) por variáveis/props.
- **Segmentação Semântica da Copy e Tipografia Cinética (`KineticText`):**
  - Pergunta ou afirmação curta de impacto → **Abertura / Gancho** (palavras ou frases curtas gigantes entradas em sequência rápida de `30–45 frames` a `30 fps`, `fontSize: 110–150px`, `lineHeight: 1.05–1.1`, sobre fundo em zoom suave `scale 1 → 1.2` com `opacity: 0.3`);
  - Preço ou comparação de valor → **Cena de Ancoragem com Transição de Impacto** (ex.: exibir o valor/custo antigo nos primeiros `60 frames` e disparar micro-transição de impacto/deslocamento horizontal `interpolate([60, 65, 70], [-20, 20, 0])` revelando a condição principal em `160px` uppercase na cor de acento do KV);
  - Número, `%` ou `R$` → **Cena de Dado**; Aspas → **Citação**; Verbo imperativo → **Encerramento / CTA** (fundo preenchido na cor de ação do KV com contraste máximo de texto).
- **Física de Animação Baseada em Mola (`spring`):**
  - Escala de entrada de títulos: `spring({ fps, frame: frame - delay, config: { damping: 12, stiffness: 150, mass: 0.5 } })`;
  - Opacidade e movimentos de câmera suaves: `spring({ fps, frame: frame - delay, config: { damping: 200 } })`.
- Render programático em `1080×1350` (Feed) ou `1080×1920` (Reels/Stories, respeitando as safe zones do Story). Logo oficial nunca deformada. Projeto em `Trabalho\` e render final em `Exportados\` da solicitação `[MT]`. Checagem final: `qualidade.md` §C.
- **Entrega após aprovação:** MP4 + `Exportados\Telas\` (um PNG por cena, com tudo entrado e nada saindo) + SVG da tela quando ela for vetorial; quando não for (foto, print, HTML animado), `Exportados\Fonte\` com o `motion.html` autocontido (arquivos usados copiados para dentro, caminhos relativos internos). Receita: `assets\motion_export.py` (`mp4` e `telas`), que exige a prévia com `window.__render(t)` e `window.__DUR` e um servidor local servindo a pasta.
- **Licença Remotion:** grátis para pessoa física e empresa com até 3 funcionários; acima disso exige Company License — confirmar antes de usar em produção.
- **Adobe Express (opcional, núcleo §6):** com o conector na sessão, animar um design aprovado, corte rápido e redimensionamento de vídeo são alternativas ao render programático quando entregarem resultado melhor ou mais rápido para a peça; Comps × Skin, safe zones e logo intacta continuam valendo. Sem conector, seguir com Remotion/HTML.
