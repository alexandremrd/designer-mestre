# huashu-design: o que veio e o que ficou de fora

Fonte: alchaincyf/huashu-design, commit 4fc7bfd (2026-10-23), MIT (relicenciada em 2026-05-14; antes tinha licença de uso pessoal). Texto original em chinês, preservado; a integração está nos módulos do designer-mestre, nos pontos abaixo. Licença em `assets/huashu/LICENSE`.

| Arquivo | Para que serve aqui | Onde é chamado |
|---|---|---|
| `brand-asset-protocol.md` | Ativos de marca antes de cor e fonte: pedir, buscar no oficial, baixar, conferir, registrar | `kv-logo.md` Parte A §1.1 |
| `workflow.md` | Cinco perguntas por peça; fluxo de alinhamento antes de produzir | `ads.md` §1 |
| `directions.md` | Três direções reais com seis candidatos em miniatura | `references/alternativas.md` (saída alternativa) |
| `tweaks-system.md` | Ideia do painel de ajuste ao vivo; a versão em JS puro é `assets/tweaks.js` | `html.md` §3 |
| `pptx-from-rendered-html.md` | Deck HTML pronto para PPTX editável, lendo o render | `deck.md` §3 |
| `storyboard-basics.md`, `camera-language.md`, `animation-pitfalls.md`, `animation-best-practices.md`, `ui-demo-animation.md`, `gsap-recipes.md`, `video-export.md` | Roteiro de produção de animação e vídeo | `video.md` Parte C |

Scripts em `assets/huashu/`: `pptx_from_rendered.py` (testado com um deck HTML de 2 slides: 4 caixas de texto, 1 forma, sem texto perdido; precisa de `-X utf8` no Windows), `convert-formats.sh` (receita de GIF), molduras e cursor em JSX (caminho com framework).

## Não incorporado
- **Áudio:** as 6 trilhas BGM e os efeitos sonoros (`assets/*.mp3`, `assets/sfx`): o projeto não informa a licença deles.
- **Rota de PPTX por reescrita** (`html2pptx.js`, `export_deck_pptx.mjs`, `editable-pptx.md`): exige escrever o HTML com 4 restrições (sem degradê, sem fundo em texto); contradiz o pixel-perfect e duplica a rota por render.
- **Renderizadores de vídeo** (`render-video.js`, `render-video-seek.js`): duplicam `assets/motion_export.py`, que já faz o render por quadro com `window.__render(t)`.
- **Memória global de gosto** (`learn.py`, `~/.huashu-design/`) e **livro-razão em arquivo global** (`design_lint.py ledger`): conflitam com a memória por cliente e com a Lei 2; o equivalente é o `historico.md` do cliente.
- **Hook** `design-gate-hook.sh`: configuração persistente.
- **Arquitetura de deck de vários arquivos com parede de visão geral, 1920×1080** (`deck_stage.js`, `deck_index.html`): o `deck.md` usa 1600×900 em arquivo único.
- **Marca d'água** "Created by Huashu-Design" (texto de `video-export.md`): crédito de terceiros não entra na peça do cliente (núcleo §6).
- **Nuvem:** `scripts/cloud/*` (revisão por IA de vídeo, TTS de terceiros): exigem chave.
