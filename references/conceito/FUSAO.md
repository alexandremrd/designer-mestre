# Fusão /produto-conceito · rastreabilidade (o agente não lê)
Fontes baixadas em 26/10/2026 e lidas por inteiro (MIT pelo autor da fusão; as demais por extração integral, tabela de 130 técnicas). Nenhuma skill externa foi instalada.

| Fonte | Commit | Licença | Estado |
|---|---|---|---|
| sanky369/vibe-building-skills (creative-strategist, product-photography, shot-library) | e9714d8 | MIT | técnica incorporada em texto próprio |
| jau123/MeiGen-AI-Design-MCP (product-photoshoot) | aef26a2 | MIT | técnica incorporada; ferramentas pagas excluídas |
| natsany/conceptual-photography-plan (SKILL + 3 referências) | cca3595 | ausente | só técnica, texto próprio; pendente de licença |
| gupsammy/Claudest (generate-image + 3 referências) | 20c43ec | ausente | só técnica, texto próprio; pendente de licença |
| inference-sh/skills (2 guias de foto de produto) | 0cbf91c | ausente | só técnica, texto próprio; pendente de licença |

| # | Capacidade | Origem | Destino e ativação |
|---|---|---|---|
| 1 | Entender produto, uso e mundo natural | sanky369, MeiGen, inference-sh | `imagem-produto.md` §5 passo 1; `biblioteca.md` §1 |
| 2 | Estudar cliente e cada referência (veredito aplica/não) | só Designer Mestre | `referencias.md` §§3–5, `guia.md`, `design_system.md`, `historico.md` |
| 3 | Escolher conceito, filtros, anti-repetição | natsany, sanky369 | §5 passo 2; `biblioteca.md` §2; `historico.md` `[CONCEITO]` |
| 4 | Cena integrada, fundo e superfície, composição | sanky369, inference-sh, natsany | `biblioteca.md` §3; Pass³ (`imagem.md` §6). Luz, sombra, ângulo e óptica já existiam em `imagem.md` B §§2–3 e Parte C: não duplicados |
| 5 | Prompt em prosa, exclusão positiva, hiperespecífico | gupsammy, natsany | `imagem.md` B1 (exclusão positiva nova); resto já coberto |
| 6 | Referências, edição, lote, continuidade | gupsammy, MeiGen | `imagem.md` B1 (referências e edição novas); `biblioteca.md` §4 |
| 7 | Beleza e aspecto de IA | natsany | `biblioteca.md` §5; §5 passo 5 |
| 8 | Feedback e variedade | natsany, gupsammy | `biblioteca.md` §6; §5 passos 2 e 5 |

Excluídos, com motivo: receitas de luz, sombra, ângulo e vocabulário de película (o `imagem.md` já cobre os princípios e evita presets); packshot de fundo branco, requisitos da Amazon e sequência de 9 imagens (já cobertos por `ads.md` e pelo 360); CLI do inference.sh, API do MeiGen, Gemini/Nano Banana e flags do Midjourney (ferramenta do autor); regras de pessoas, formato 3:4 e pesos de pontuação (preferência do autor); engenharia mecânica de props (conceito objeto × objeto, fora do escopo de marca); extração de frames de vídeo (rota de vídeo).
Lacuna das fontes: nenhuma ensina a escolher conceito a partir do produto nem estudar referências do cliente; essas capacidades vêm do próprio Designer Mestre (linhas 2 e 3).
Pendência: licença das três fontes sem licença; testar `/produto-conceito` numa peça real (nada foi gerado ainda).
