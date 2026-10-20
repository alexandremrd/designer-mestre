# Módulo Vídeo, Edição (Legenda + KV), Dramaturgia para IA de Vídeo e Motion

Módulo autônomo e unificado para **edição mecânica** de vídeo do cliente (legenda queimada no KV + overlay + trilha + corte de pausas), **direção dramatúrgica** de roteiro/UGC/IA de vídeo e **motion design** programático. Opera com ferramentas nativas e scripts internos (`assets\reels_legenda.py`), sem depender de sites ou aplicativos externos.

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

### 2. Overlay
1. Frame 9:16 no Figma do cliente (link do pedido ou `_DESIGN\templates\overlay_9x16.png`): exportar PNG 1080×1920 **com transparência** (`get_screenshot` não preserva alpha; preferir export do Figma ou montar via SVG).
2. Sem frame: montar SVG 1080×1920 com moldura/gradiente/logo do `design_system.md`, renderizar PNG RGBA autonomamente no navegador headless da IDE e salvar em `Trabalho\`.
3. A faixa de legenda fica em área de leitura: gradiente escuro sob ela, nunca sobre o rosto. Base da legenda em y ≤ 1470.

### 3. Transcrição e sincronização (autônoma em cadeia, sem travar)
A máquina escolhe o método disponível na sessão sem depender de serviços externos:
1. `.srt` já existente na pasta → `--srt`.
2. Transcrição multimodal nativa da própria IDE/agente (lendo o áudio/vídeo diretamente) ou motor de transcrição offline local → gera o `.srt` palavra a palavra.
3. Fala enviada pelo usuário → sincronização automática por detecção de silêncio e distribuição proporcional por sílaba/palavra (`--srt`).
Nunca legendar a partir do roteiro sem conferir com a fala real.

### 4. Comando
```
python "<PASTA_DO_AGENTE>\assets\reels_legenda.py" ^
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

### 1. Estrutura de Roteiro Publicitário (30 s) & Regra dos 6 de Walter Murch
- **Arco de 30 s:** Gancho 0–3 s (problema ou resultado concreto) · Problema 4–8 s · Solução/Mecanismo 9–18 s · Prova 19–24 s · CTA 25–30 s. A voz vem primeiro e define o tempo.
- **Dramaturgia e Fórmula de Cena (obrigatória antes do prompt):**
  - **Fórmula da Cena (1 frase):** `Desejo + Obstáculo + Geometria Espacial (Foreground / Midground / Background) + Direção do Olhar + Ritmo`.
  - **Lei dos 3 Detalhes Físicos por Take:** todo plano deve declarar (1) pressão ambiental (vento, vapor, reflexo de chuva, luz rasante), (2) micro-ação física do corpo/produto, e (3) âncora sonora ou motivo visual.
  - **Lei das 3 Funções:** um take deve mudar a emoção, avançar a ação ou aumentar a pressão; se não fizer nenhum dos três, cortar.
  - **Regra dos 6 de Murch no corte:** Emoção (51%) > História (23%) > Ritmo (10%) > Eye-trace (7%) > Plano 2D (5%) > Espaço 3D (4%).
  - **Escada de Montagem:** `longo → mais curto → mais curto → pausa respiratória → impacto`. A câmera só se move quando há mudança na cena.

### 2. Vocabulário Canônico de Câmera (12 Movimentos e 6 Ângulos)
- **Movimentos:** `Push-in` (tensão/detalhe) · `Pull-back / Dolly out` (revelação de contexto) · `Tracking shot` (acompanhamento lateral) · `Pan` (rotação no eixo horizontal) · `Tilt` (eixo vertical, imponência) · `Crane up/down` (abertura/revelação vertical) · `Orbit / Arc` (giro 360° heroico no produto) · `Dolly zoom` (vertigem dramática) · `Handheld / Steadicam` (realismo UGC/documental) · `Static / Locked-off` (packshot limpo) · `Slow-motion` (luxo/impacto físico) · `Timelapse` (transformação temporal).
- **Ângulos:** `Eye-level` (neutro/humano) · `Low angle` (poder/aspiracional/luxo) · `High angle` (visão geral) · `Bird's eye / Top-down` (flat-lay geométrico) · `Dutch angle` (tensão) · `Over-the-shoulder / POV` (intimismo, unboxing).

### 3. UGC Autêntico (Sem Cara de IA)
- **Fórmulas UGC (Unboxing, Review, Rotina):** câmera de mão com leve oscilação natural (`slightly shaky handheld, front-facing phone camera quality, not studio-perfect`), luz natural de janela, ambiente vivido real, micro-pausas espontâneas, formato 9:16 vertical com cortes secos e produto em uso real.
- Depoimento só real ou claramente encenado por ator; nunca apresentar como cliente verdadeiro.

### 4. Adaptadores de Física por Motor de Vídeo & Filtro Anti-Slop
- **Ordem densa em inglês (SLCT Cinematográfico):** `[Plano, Ângulo e Movimento de Câmera] + [Sujeito e Micro-ação Física] + [Cenário em 3 Planos e Pressão Ambiental] + [Luz: fonte, direção, razão Key:Fill, Kelvin] + [Paleta, Óptica/Lente, Grão e Ritmo/Duração]`.
- **Adaptação por Motor:**
  - **Veo 3 / 3.1:** brilha em cenas cinematográficas longas, física coerente e áudio/SFX sincronizado (para UGC, exigir explicitamente `"phone camera quality, casual home lighting, not cinematic"`).
  - **Kling 2.6 / 3.0 Master:** brilha em *Image-to-Video* de produto e consistência de personagem (`[Character A: ...]` binding, `cfg_scale 0.3–0.5` para liberdade ou `0.7–0.9` para aderência estrita + campo de negative prompt).
  - **Seedance 2.5 / v1 Pro:** brilha em movimento corporal humano natural, UGC e sequências multi-plano de até 30 s com diálogo `{ Personagem: "fala" }`.
  - **Sora 2:** movimentos de câmera contínuos e transições espaciais suaves (4s / 8s / 12s).
  - **MiniMax Hailuo:** física volumétrica densa e vetores explícitos de câmera (`[Pan left]`, `[Dolly in]`, `[Orbit]`, intensidade `1–10`).
- **Filtro Anti-Slop de Vídeo:** proibido usar palavras vazias como `cinematic, epic, stunning, masterpiece, beautiful lighting, dynamic camera` — substituir sempre pela descrição física real da luz, lente e movimento. Manter bíblia de consistência em `Trabalho\` da pasta `[EV]`.

---

## Parte C · Motion Design (animações programáticas)

- Separar **comps** neutros (abertura, headline, dado, citação, CTA) da **skin** do cliente (cores, fontes, logo e áudio do `design_system.md`).
- Segmentar a copy: pergunta/frase curta = gancho; número/%/R$ = cena de dado; aspas = citação; imperativo = CTA.
- Render programático em 1080×1350 ou 1080×1920. Safe zones do Story valem para o 9:16. Logo oficial nunca deformada.
- Projeto em `Trabalho\` e render final em `Exportados\`, na pasta da solicitação `[MT]`. Checagem final: `qualidade.md` §C.
