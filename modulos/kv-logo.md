# Módulo KV, Brand Book, Logo e Design System

Módulo unificado para extração/validação de Identidade Visual (Cold Start), criação de Brand Book e Logo nova, e estruturação/exportação de tokens de Design System (`tokens.css` e `DESIGN.md`).

---

## Parte A · Cold Start — Cliente novo ou KV incompleto

Usado quando o cliente não tem `_DESIGN\design_system.md`, quando `STATUS_KV` é `PARCIAL`/`VAZIO` ou quando o usuário pede revisão do KV. Roda uma vez; depois o cliente entra no Fast-Track.

### 1. Estrutura de pastas
Cliente existente: não mover nem apagar nada; criar só o que o pedido precisa. Cliente novo: criar a árvore e copiar `<PASTA_DO_AGENTE>\Clientes\_TEMPLATE_CLIENTE\design_system.md` para `_DESIGN\`.

```text
D:\Clientes\[Cliente]\
  _DESIGN\
    design_system.md     ← memória única do cliente
    historico.md         ← 1 linha por entrega (só escrita)
    templates\           ← esqueletos SVG aprovados (E1.svg, E2.svg...)
    Personagens\         ← (opcional) dossiês de personagens recorrentes
    Produtos\            ← (opcional) dossiês de produtos recorrentes
  Compartilhada\
    Identidade Visual\   ← logos, MIV, fontes, brand book (nunca sobrescrever)
    Referências\         ← referências enviadas (só salvar)
    Imagens\  Originais\ (só leitura) · Banco de Imagens\ · IA\
    Vídeos\   Originais\ · Banco\
  [AAAA]\[MM - Mês]\[AAAA-MM-DD] [TIPO] Título\
    briefing.md · Referências\ · Trabalho\ · Exportados\
```
Tipos: `CA` criativo Ads · `PA` pauta/orgânico · `EV` vídeo editado · `MT` motion · `LP` landing page/HTML · `KV` identidade · `DK` deck · `IM` imagem · `OT` outros.
Cliente antigo com `KV.md`, `NAO_FAZER.md`, `aprovados.md`, `inteligencia.md` separados: unificar no `design_system.md` (sem apagar os antigos).

### 2. Análise profunda (MIV Scanner — uma vez)
1. `Compartilhada\Identidade Visual\`: MIV, guia de marca e logos. Renderizar cada logo uma única vez e anotar arquivo, layout, cor e proporção do bbox.
2. Links de Figma do briefing (`get_design_context` / `get_screenshot`).
3. Peças anteriores do cliente, se houver: só as 2 ou 3 mais recentes.
4. Site ou Instagram informados no briefing.
5. Extrair e consolidar no `_DESIGN\design_system.md`:
   - conceito, sensação e símbolo;
   - versões da logo (nome · layout · cor · bbox);
   - paleta por papel (HEX, RGB, CMYK, escala 50–900, cores semânticas, contraste WCAG, regra de uso do acento e cores proibidas);
   - tipografia por nível (oficial com peso e caixa + substituta Google Fonts para Figma/SVG);
   - grafismos, arquétipos SVG, composição/respiro/posição da logo/rodapé, fotografia (tema · pessoas · luz · contraste), safe zones, tom de voz e pilares, O Que Fazer (Aprovados) e O Que Não Fazer (Vetos).
6. Contradições ou itens ausentes essenciais (logo, paleta ou fonte) vão para `## 5. Decisões Pendentes` mantendo `PARCIAL`; quando completo, marcar `STATUS_KV: VALIDADO`.
7. Cliente já `VALIDADO` num template antigo: campos novos vazios **não** rebaixam o status nem disparam nova análise.

---

## Parte B · Brand Book e Logo nova

### 1. Brand Book
Salvar em `Compartilhada\Identidade Visual\` e na página "Brand" no Figma (com estilos e variáveis), sem alterar arquivos oficiais existentes. Formato 16:9: capa, índice, logo (versões, área de proteção, tamanho mínimo, fundos, monocromia, usos indevidos), cores, tipografia, grafismos e aplicações.

### 2. Logo nova (somente sob pedido explícito)
- Se o cliente já tem logo, confirmar que é redesign ou marca nova. Logo de cliente nunca é criada sem pedido explícito (faltou logo num pedido comum = pedir).
- Etapas:
  1. Briefing: nome, setor, valores, público, concorrentes e restrições.
  2. Pesquisa de concorrência para diferenciar. Nunca imitar marca existente.
  3. Três rotas (símbolo, lettering, combinação) em vetor no Figma, com versões horizontal e vertical, cor/positivo/negativo, área de proteção e tamanho mínimo.
  4. Após aprovação, exportar SVG e PNG para `Compartilhada\Identidade Visual\` e registrar na tabela de logos do `_DESIGN\design_system.md`. A partir daí vale a lei da logo existente.

---

## Parte C · Design System e Exportação de Tokens

Referência + logo + tipografia → análise → tokens → prévia para aprovação → variáveis e componentes no Figma (`figma.md`: variáveis primeiro, depois componentes com variantes e estados ligados aos tokens; código existente via Code Connect).
A fonte da verdade é o `_DESIGN\design_system.md` do cliente (`STATUS_KV: VALIDADO`). Tudo abaixo é **derivado** dele, gerado sob pedido e nunca editado à mão.

### 1. Tokens obrigatórios (camadas)
- **A1 · a marca precisa declarar:** `--bg` `--fg` `--accent` `--font-display`.
- **A2 · obrigatórios com padrão:** `--fg-2` `--surface` `--border` `--success` `--error` `--font-body` `--radius` `--space-4` (16 px) `--motion-fast` (0.18 s).
- **B · apelidos permitidos:** `--fg-2: var(--fg);` quando o KV não define.
- Nome por **função**, nunca por cor (`--accent`, não `--laranja`).

### 2. Exportações (sob pedido: "exporta o design system", LP, outro agente/ferramenta)
Salvar em `_DESIGN\export\` (não lidos pelo Gate de KV):
1. **`tokens.css`** — `:root{}` com A1+A2+B e escala de tipo (`--fs-display` … `--fs-caption`, razão 1.2–1.25). É o que o `html.md` importa/cola no `<style>`.
2. **`DESIGN.md`** — frontmatter YAML com tokens + prosa:
```yaml
---
version: alpha
name: [Cliente]
description: [conceito em 1 frase]
colors: { primary: "#…", ink: "#…", canvas: "#…", accent: "#…" }
typography:
  display: { fontFamily: "…", fontSize: 56px, fontWeight: 700, lineHeight: 1.05, letterSpacing: -1px }
  body:    { fontFamily: "…", fontSize: 16px, fontWeight: 400, lineHeight: 1.5 }
---
```
Seções H2 (≥ 7): Overview · Colors · Typography · Layout · Elevation & Depth · Shapes · Components · Do's and Don'ts · Responsive Behavior. Componentes referenciam tokens como `{colors.primary}`. Do's and Don'ts = `## 1. NÃO FAZER` e `## 2. O QUE FAZER` do cliente.
3. **Prévia** HTML única: swatches com HEX e contraste (`img_qa.py contraste`), escala tipográfica, botões nos estados Primary/Secondary/Ghost/Disabled, cards com elevação.
