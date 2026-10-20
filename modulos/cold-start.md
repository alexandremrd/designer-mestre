# Módulo Cold Start — Cliente novo ou KV incompleto

Usado só quando o cliente não tem `_DESIGN\design_system.md` ou o `STATUS_KV` é `PARCIAL`/`VAZIO`. Roda uma vez; depois o cliente entra no Fast-Track.

## 1. Estrutura de pastas

Cliente existente: não mover nem apagar nada; criar só o que o pedido precisa. Cliente novo: criar a árvore e copiar `<PASTA_DO_AGENTE>\Clientes\_TEMPLATE_CLIENTE\design_system.md` para `_DESIGN\`.

```text
D:\Clientes\[Cliente]\
  _DESIGN\
    design_system.md     ← memória única do cliente
    historico.md         ← 1 linha por entrega (só escrita)
    templates\           ← esqueletos SVG aprovados (E1.svg, E2.svg...)
    Personagens\         ← (opcional) dossiês de personagens recorrentes
  Compartilhada\
    Identidade Visual\   ← logos, MIV, fontes, brand book (nunca sobrescrever)
    Referencias\         ← referências enviadas (só salvar)
    Imagens\  Originais\ (só leitura) · Banco de Imagens\ · IA\
    Vídeos\   Originais\ · Banco\
  [AAAA]\[MM - Mês]\[AAAA-MM-DD] [TIPO] Título\
    briefing.md · Referencias\ · Trabalho\ · Exportados\
```

Tipos: `CA` criativo Ads · `PA` pauta/orgânico · `EV` vídeo editado · `MT` motion · `LP` landing page/HTML · `KV` identidade · `DK` deck · `IM` imagem · `OT` outros.

Cliente antigo com `KV.md`, `NAO_FAZER.md`, `aprovados.md`, `inteligencia.md` separados: unificar no `design_system.md` (sem apagar os antigos).

## 2. Análise profunda (uma vez)

1. `Compartilhada\Identidade Visual\`: MIV, guia de marca e logos. Renderizar cada logo e anotar arquivo, layout, cor e bbox.
2. Links de Figma do briefing (`get_design_context` / `get_screenshot`).
3. Peças anteriores do cliente, se houver: só as 2 ou 3 mais recentes.
4. Site ou Instagram informados no briefing.

## 3. Gravar

Preencher o `design_system.md` (conceito e sensação, paleta por papel com a regra de uso do acento, cores proibidas, tipografia por nível com peso e caixa + substituta Google Fonts, tabela de logos, composição/respiro/posição da logo/rodapé, foto em tema · pessoas · luz · contraste, safe zones, tom de voz e pilares) e marcar `STATUS_KV: VALIDADO`. O que não se deduz das peças fica `[A CONFIRMAR]`, sem inventar. Faltou algo essencial (logo, paleta ou fonte): manter `PARCIAL` e listar em `## 5. Decisões Pendentes`.

Cliente já `VALIDADO` num template antigo: campos novos vazios **não** rebaixam o status nem disparam nova análise. Preencher só quando o usuário pedir ("reveja o KV") ou quando uma aprovação/reprovação revelar o dado (gravação normal da seção 5 do núcleo).
