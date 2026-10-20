# 11 · Figma Agent Intelligence (Figma Pilot, TalkToFigma, Code Connect & HTML-to-Figma)

Este módulo consolida 100% da inteligência e das ferramentas dos agentes de ponta do ecossistema Figma, integrados nativamente ao comando unificado `/design`.

---

## 🏗️ ARQUITETURA DE 4 MOTORES DE FIGMA INCORPORADOS

```
                        AGENTE UNIFICADO /design
                                   ↓
┌────────────────────────────────────────────────────────────────────────┐
│                   MOTORES DE INTELIGÊNCIA COM FIGMA                    │
├────────────────────────────────┬───────────────────────────────────────┤
│ 1. FIGMA PILOT (Code Exec)     │ 2. TALK TO FIGMA (MCP Bidirecional)   │
│ - figma_execute (JS na API)    │ - 42 Ferramentas granulares via Socket│
│ - 90%+ economia de tokens      │ - Edição de nós em tempo real         │
│ - Autolayout & Accessibility   │ - Bulk text & Instance override       │
├────────────────────────────────┼───────────────────────────────────────┤
│ 3. HTML-TO-FIGMA (BuilderIO)   │ 4. CODE CONNECT (Design System Bridge)│
│ - Conversão HTML/CSS -> Figma  │ - Mapeamento Figma <-> React/HTML     │
│ - Vetores nativos e autolayout │ - Snippets de produção no Dev Mode    │
└────────────────────────────────┴───────────────────────────────────────┘
```

---

## 1. ⚡ MOTOR 1: FIGMA PILOT (CODE EXECUTION ENGINE)

O **Figma Pilot** substitui dezenas de chamadas lentas de ferramentas por um interpretador de JavaScript que roda diretamente dentro da sandbox do plugin Figma, economizando até 90% do contexto de tokens.

### A. Estrutura do `figma_execute`
```javascript
// Exemplo canônico: Criação de Card com Auto-Layout e Verificação de Acessibilidade
await figma.create({
  type: 'card',
  name: 'Campaign Card 2026',
  layout: {
    layoutMode: 'VERTICAL',
    padding: { top: 24, right: 24, bottom: 24, left: 24 },
    itemSpacing: 16,
    primaryAxisAlignItems: 'CENTER',
    counterAxisAlignItems: 'STRETCH'
  },
  fills: [{ type: 'SOLID', color: '#0A0A0B' }],
  cornerRadius: 16,
  children: [
    { type: 'text', content: 'Headline de Impacto', fontSize: 28, fontWeight: 700, fill: '#FFFFFF' },
    { type: 'text', content: 'Subtítulo persuasivo com suporte ao KV', fontSize: 16, fill: '#A1A1AA' },
    {
      type: 'button',
      name: 'CTA Button',
      content: 'Aproveitar Oferta',
      fills: [{ type: 'SOLID', color: '#2563EB' }],
      cornerRadius: 8,
      padding: { horizontal: 20, vertical: 12 }
    }
  ]
});

// Auditoria WCAG Automática
const { violations } = await figma.accessibility({ target: 'selection' });
if (violations.length > 0) {
  console.log(`Corrigindo automaticamente ${violations.length} problemas de contraste.`);
  for (const v of violations) {
    await figma.modify({ target: v.nodeId, fill: v.suggestedFill });
  }
}
```

### B. APIs Nativas Suportadas:
- `figma.create({ type, name, layout, fills, strokes, cornerRadius, children })`
- `figma.modify({ target, fills, text, autolayout, effects, opacity })`
- `figma.query({ target: 'selection' | 'id' | 'name' })`
- `figma.accessibility({ target, level: 'AA' | 'AAA' })`
- `figma.tokens.bind({ target, tokenName })`
- `figma.export({ target, format: 'PNG' | 'SVG' | 'PDF', scale: 2 })`

---

## 2. 🔌 MOTOR 2: TALK TO FIGMA (MCP BIDIRECIONAL DE 42 FERRAMENTAS)

Inspirado na arquitetura de Sonny Lazuardi (Grab), permite comandos diretos em linguagem natural para manipular o arquivo aberto em tempo real via WebSocket local:

### As 42 Capacidades Nativas Mapeadas:
1. **Inspeção & Leitura:** `get_document_info`, `get_selection`, `read_my_design`, `get_node_info`, `get_nodes_info`, `get_styles`, `get_local_components`, `get_reactions`.
2. **Criação & Estrutura:** `create_rectangle`, `create_frame`, `create_text`, `create_section`, `create_component_instance`, `create_connections`, `clone_node`.
3. **Geometria & Auto-Layout:** `move_node`, `resize_node`, `set_corner_radius`, `set_layout_mode` (`HORIZONTAL` / `VERTICAL` / `NONE`), `set_padding`, `set_axis_align`, `set_layout_sizing`, `set_item_spacing`, `set_parent`.
4. **Cores & Estilos:** `set_fill_color`, `set_stroke_color`, `set_image_fill`.
5. **Manipulação em Massa de Texto:** `set_text_content`, `scan_text_nodes`, `scan_nodes_by_types`, `set_multiple_text_contents`.
6. **Propagação de Instâncias (Instance Overrides):** `get_instance_overrides`, `set_instance_overrides` (propaga customizações de um componente para múltiplos nós de uma só vez).
7. **Prototipagem & Anotações:** `get_annotations`, `set_annotation`, `set_multiple_annotations`, `set_default_connector`, `create_connections`.
8. **Exportação & Foco:** `export_node_as_image`, `set_focus`, `set_selections`, `delete_node`, `delete_multiple_nodes`, `rename_node`.

---

## 3. 🌐 MOTOR 3: HTML-TO-FIGMA (BUILDER.IO ENGINE)

Permite converter qualquer página web, Landing Page ou bloco visual HTML gerado pelo `/design` em elementos nativos e editáveis no Figma:
- Lê estilos computados (`getComputedStyle`), box model e hierarquia DOM.
- Transforma tags `div`, `section`, `header` em Frames com Auto-Layout.
- Transforma textos em nós nativos de Text com fontes mapeadas.
- Transforma `img` e `background-image` em nós com preenchimento do tipo `IMAGE`.
- Transforma SVGs inline em nós de vetor perfeitos sem distorção.

---

## 4. 🔗 MOTOR 4: CODE CONNECT (SINCRONIZAÇÃO DE DESIGN SYSTEM)

Ponte oficial para desenvolvedores e Dev Mode:
- Mapeia componentes do código de produção para as variantes do Figma.
- Suporta mapeamento de props: `figma.string`, `figma.boolean`, `figma.enum`, `figma.instance`, `figma.children`.
- Gera templates de código diretamente utilizáveis no Figma Dev Mode.

---

## 🚀 FLUXO DE USO NO AGENTE UNIFICADO `/design`:

O usuário pode escolher o fluxo conforme sua necessidade:
1. **Fluxo Ágil (Recomendado - Sem Dependências):** O agente gera a peça no **Interactive Canvas** e entrega o bloco **SVG Estruturado** ou código vetorial com botão de copiar para colar direto no Figma (cria frames, textos e vetores na hora).
2. **Fluxo Autônomo com Figma Aberto (`/design figma execute`):** Gera scripts executáveis para o plugin **Figma Pilot** que criam telas complexas, layouts responsivos e auditam acessibilidade via JavaScript puro.
3. **Fluxo em Tempo Real via Socket (`/design figma socket`):** Dispara comandos para o plugin **TalkToFigma** para alterar textos, cores e instâncias em lote com o arquivo aberto.
