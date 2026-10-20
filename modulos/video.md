# Módulo Vídeo, Edição (Legenda + KV) e Motion

Módulo unificado para **edição mecânica** de vídeo do cliente (legenda queimada no KV + overlay + trilha + corte de pausas), **criação** de roteiro/UGC/IA de vídeo e **motion design** programático (Remotion).

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
2. Sem frame: montar SVG 1080×1920 com moldura/gradiente/logo do `design_system.md`, renderizar PNG RGBA e salvar em `Trabalho\`.
3. A faixa de legenda fica em área de leitura: gradiente escuro sob ela, nunca sobre o rosto. Base da legenda em y ≤ 1470.

### 3. Transcrição (fallback em cadeia, sem parar)
1. `faster-whisper` local, palavra a palavra (`pip install faster-whisper`; baixa o modelo de `huggingface.co` na 1ª vez).
2. `.srt` existente na pasta (CapCut/Premiere) → `--srt`.
3. Texto colado pelo usuário → montar `.srt` por blocos de fala (`silencedetect`) e passar `--srt`.
Nunca legendar a partir do roteiro sem conferir com a fala.

### 4. Comando
```
python "%USERPROFILE%\.claude\skills\designer-mestre\assets\reels_legenda.py" ^
  --video "Original\x.mp4" --overlay "Trabalho\overlay.png" [--intro "Trabalho\intro.png" --intro-s 2] ^
  --fonte "<família exata do KV>" --fontsdir "<pasta com .ttf/.otf>" --tamanho 60 ^
  --cor <texto> --destaque <acento> --contorno <fundo escuro> --y 1380 ^
  --cortar-pausas 0.6 [--musica "Música\m.mp3" --musica-db -20] [--idioma en] ^
  --out "Exportados\<nome do briefing>.mp4"
```
- 1ª rodada gera `<out>.srt`. Se o usuário corrigir uma palavra, rodar de novo com `--srt <out>.srt` (sem transcrever de novo).
- `--palavras 3–4` e `--max-car 22–26` para Reels; `--caixa-alta` só se o KV pedir.
- Saída: H.264 16 Mbps, AAC 192 k, voz normalizada a -16 LUFS. Não exportar a 60+ Mbps: o Instagram recomprime.
- Rodar no PC (ver núcleo §2). Sem `device_bash`: entregar este comando preenchido para uma sessão Code.

### 5. Conferência e Memória
- **Conferência:** prancha com 3 frames (início, meio, fim) + duração + tamanho do arquivo. Checar: legenda dentro da safe zone, sem cobrir rosto/logo, fonte certa (não caiu em Arial), destaque legível, logo sem distorção, nenhuma palavra errada no `.srt`.
- **Memória:** overlay aprovado vira `_DESIGN\templates\overlay_9x16.png` + linha em `## 2. O QUE FAZER` com os parâmetros usados (fonte, tamanho, cores, y). O próximo vídeo do cliente sai com um comando só.

---

## Parte B · Roteiro, UGC e direção de cena para IA de vídeo

### 1. Roteiro (30 s)
Gancho 0–3 s · Problema 4–8 s · Solução 9–18 s · Prova 19–24 s · CTA 25–30 s. A voz vem primeiro e define o tempo; as cenas são feitas em paralelo.

### 2. UGC sem cara de IA
- Câmera de mão imperfeita e luz de janela; ambiente vivido; micro-pausas e gestos espontâneos; linguagem de smartphone em 9:16 com cortes secos; produto em uso real.
- Depoimento só real ou claramente encenado por ator; nunca apresentar como cliente verdadeiro.

### 3. Direção de cena para IA de vídeo (Sora, Veo, Kling, Runway)
Prosa densa em inglês, com tradução, nesta ordem: plano/câmera · sujeito e ação · cenário · luz (fonte, direção, Kelvin) · paleta e clima · lente e profundidade · movimento de câmera · atmosfera/textura · referência estética · duração e ritmo.
Manter uma bíblia de consistência entre as cenas do mesmo projeto, salva em `Trabalho\` da pasta da solicitação `[EV]`.

---

## Parte C · Motion Design (Remotion / animações)

- Separar **comps** neutros (abertura, headline, dado, citação, CTA) da **skin** do cliente (cores, fontes, logo e áudio do `design_system.md`).
- Segmentar a copy:
  - pergunta ou frase curta = gancho;
  - número, % ou R$ = cena de dado;
  - aspas = citação;
  - imperativo = CTA.
- Render programático com Remotion: stills 1080×1350/1920 ou vídeo.
- Safe zones do Story valem para o 9:16. Logo oficial, nunca animada de forma que deforme.
- Projeto em `Trabalho\` e render final em `Exportados\`, na pasta da solicitação `[MT]`.
- Checagem final: `qualidade.md` §C (tokens de duração, reduced-motion, corte no beat).
