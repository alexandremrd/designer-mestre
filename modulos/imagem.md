# Módulo Imagem — geração (Antigravity + local), packshot, retrato, prompt e upscale

## 1. Escada de geração (Antigravity do plano ou local; sem conta nova nem API)
Usar o primeiro degrau que resolve; nunca um que peça conta nova ou chave de API.

| Degrau | Quando | Como |
|---|---|---|
| 0. Foto real | sempre primeiro | `Originais\` → `Banco de Imagens\` (núcleo §4) |
| 1. Composição no SVG | fundo, textura, degradê, recorte | SVG/ImageMagick; sem IA |
| 2. **Antigravity (Nano Banana Pro, plano Pro)** — só quando a sessão roda no Antigravity | foto fotorreal, produto fiel, cena com pessoa: melhor fidelidade da escada | ferramenta nativa de imagem do agente (`generate_image`), com a mestra e até 2 vistas como referência; depois `gerar_imagem.py registrar <saída> -o "<IA>\<nome>.png" --prompt "..." --ref mestra.jpg` |
| 3. **Easy Diffusion local · motor v4 + FLUX.2 klein 4B** | produto/pessoa fiel com referência, cena nova | `python assets\gerar_imagem.py gerar "<prompt EN>" --ref mestra.jpg [--ref angulo.jpg] -a 4:5 -o "<IA>\<nome>.png"` |
| 4. Easy Diffusion img2img | mudar luz/cenário mantendo a composição de uma foto | `gerar ... --init base.jpg --forca 0.35–0.55` |
| 5. Upscale local | final em alta | `python assets\gerar_imagem.py upscale in.png -o out.png --escala 2` |
| 6. Sem gerador disponível | — | entregar o prompt pronto + 1 linha: "abra o Easy Diffusion e rode: <comando>". Nunca travar a peça. |

- Antes da 1ª geração da sessão: `gerar_imagem.py ping`. Falhou: degrau 5.
- **FLUX.2 klein 4B** = Apache 2.0 (uso comercial livre). O 9B é não comercial: **proibido em peça de cliente**.
- Referências exigem o motor **v4** (Easy Diffusion › Settings › Backend). v3.5 (Forge) não aceita `--ref`: usar img2img.
- Iterar em 1 MP (padrão do script); finalizar com `upscale`. `--seed` fixa para reproduzir; variação = trocar seed, não o prompt.
- Gerado é grátis, mas custa tempo de GPU: no máximo 4 variações por rodada, 3 rodadas por peça.
- **Antigravity:** a cota de imagem é do plano e separada da de texto; acabou = cair para o degrau 3 sem perguntar. Sessão no Claude Code não chama a ferramenta do Antigravity: se a peça pede fidelidade de Nano Banana, entregar o prompt + 1 linha "rodar no Antigravity: `/designer-mestre gerar ...`". Nunca usar scripts que reaproveitam o login do Antigravity fora dele (endpoint interno, risco de bloqueio da conta).
- Saída do Antigravity tem marca d'água invisível (SynthID); continua valendo a lei de não apresentar IA como foto real.
- GPT Image, Runway e Firefly: só se o usuário pedir pelo nome.

## 2. Fórmula do prompt (sempre em inglês)
`[pessoa + ação] , [produto] identical to reference image 0 , [objetos do nicho] , [ambiente] , [luz] , 70 percent person and product, 30 percent environment , [estilo/câmera]`

- Produto é herói: 70/30 (pessoa+produto / ambiente). Sem pessoa: `product fills 60 percent of frame`.
- Cada referência citada pelo índice: `image 0` = mestra, `image 1` = ângulo, `image 2` = detalhe.
- Derivar do `design_system.md`, sem perguntar: luz/mood de "Foto · luz e tratamento", pessoas de "Foto · pessoas", paleta da tabela.
- Negativo padrão já está no script (texto, logo, UI, mockup, pele plástica, HDR). Somar as cores e formas proibidas do cliente com `--neg`.
- **Texto, rótulo e logo nunca vêm da IA**: o modelo só imita parcialmente. Rótulo legível = gerar a cena e compor a arte real do rótulo/logo no SVG.
- Clonar pessoa real por IA não funciona bem e só com autorização (`personagem.md`).

Campos opcionais para detalhar (JSON, lotes em JSONL): `scene`, `hero`, `lighting` (softbox 45°, 5500K), `camera` (85mm T1.5), `exposure`, `grain`, `mood`, `avoid`.
Modificadores: `/input` referência inegociável (`--forca 0.25` no img2img) · `/pullout` plano aberto · `/wormsview` contra-plongée · `/floatingproduct` levitando · `/8k` `/besttexture` só no upscale.

**Prompt Master (`/promptmaster`, sob pedido):** bloco curto para colar numa IA externa, derivado na hora do `design_system.md` (papel, proibições, paleta por papel, família/peso/caixa, foto + overlay). Nunca salvar.

## 3. Salvar
Toda saída em `Compartilhada\Imagens\IA\AAAA-MM-DD_[solicitação]_[tema]_v[n].png`; o script grava o `.txt` ao lado (prompt, modelo, seed, referências). 1 linha no `historico.md`. Proibido apresentar IA como foto real quando enganar (equipe, obra, depoimento).

## 4. Packshot / 3D
- Prancha de consistência primeiro (frontal, 45° esq./dir., perfil 90°, topo, flutuante); depois a cena. Produto fiel: `produto.md`.
- Preservar forma, proporção, materiais, cores e marca. Modos: estúdio novo (pódio, cáusticas, espaço negativo no topo) ou produto numa cena aprovada (cena em `--init`, produto em `--ref`).

## 5. Retrato
Preservação facial estrita (olhos, expressão, rugas, microporos). Sem soft skin, pele plástica, sorriso forçado. Rosto recorrente: `personagem.md`. Upscale de pessoa real **sem** `--rosto` (CodeFormer reinventa traços). Pôster com 3 pessoas: triângulo com espaço negativo para o título.

## 6. Upscale / remasterização
`upscale --escala 2|4` (RealESRGAN local). Nunca alterar rosto, corpo, logo ou geometria do produto.

## Instalação (uma vez, no PC)
1. Easy Diffusion: instalador do pacote (`easydiffusion-main`) → `Start Stable Diffusion UI` (abre em `http://127.0.0.1:9000`). Requer GPU NVIDIA/AMD; FLUX.2 klein 4B pede ~12 GB de VRAM para ficar confortável (menos com versão GGUF, não testado aqui).
2. Settings › Backend › **v4**; reiniciar.
3. Baixar o FLUX.2 klein **4B** e colocar em `models\stable-diffusion\`; conferir com `gerar_imagem.py modelos`. Definir `ED_MODELO` com o nome exato.
Depois disso, nada sai do PC.
