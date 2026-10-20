# 05 · Brand Kit Real & MIV Scanner (Decupagem de Marca & Design Systems)

## 1. Motor Brand Kit Real & MIV Scanner
O agente possui motor nativo para processar manuais em PDF (inclusive arquivos complexos de 20MB+), arquivos vetoriais (.AI / .SVG) e bancos de imagem oficiais de qualquer cliente:

### Componentes Mapeados e Extraídos:
1. **Paleta Cromática Estruturada:**
   - Cor Primária e Secundária da marca com códigos `#HEX`.
   - Escala tonal de 50 a 900 para superfícies Dark e Light.
   - Cores de Ação / CTA e Semânticas (Success, Warning, Error, Info).
   - Teste de contraste WCAG 4.5:1 obrigatório em todos os pares texto/fundo.
2. **Sistema Tipográfico:**
   - Fonte Display (Headlines de impacto): pesos Bold/Black (700-900).
   - Fonte Body / Apoio: pesos Regular/Medium (400-500) com line-height calibrado.
   - Tamanhos proporcionais via `clamp()` para responsividade.
3. **Diretrizes e Guardrails do KV:**
   - Iluminação característica de estúdio (ex: Chiaroscuro comercial, Rim lights, luz suave).
   - Composição de grid e Safe Zones (Feed 4:5 e Stories 9:16).
   - Lista explícita de elementos proibidos (proibição de caixas opacas, distorção de logo, etc.).

---

## 2. Gravação na memória do cliente
Tudo vai para o arquivo único `D:\Clientes\[Cliente]\_DESIGN\design_system.md` (seções 1 NÃO FAZER · 2 O QUE FAZER · 3 KV · 4 Inteligência). Os antigos `GUIA_DE_MARCA.md`, `ESTILO.md` e `NAO_FAZER.md` são legado: unificar, nunca gravar neles. Cor medida de logo/foto: `python assets\img_qa.py paleta <arquivo>`. Exportar `tokens.css`/`DESIGN.md` só pelo `modulos/design-system.md`.

---

## 3. Preview Standalone no Canvas / Artifact
Antes de qualquer exportação, o agente gera um preview HTML standalone contendo swatches de cores com códigos `#HEX`, demonstração de escala tipográfica, exemplos de botões em seus diferentes estados (Primary, Secondary, Ghost, Disabled), cards com elevações de sombra, toggle funcional Light/Dark Mode e botão com 1 clique para "Copiar SVG para Figma".
