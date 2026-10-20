# 06 · Decks e Apresentações Comerciais em HTML (Colli Engine)

## Arquitetura de Slides 1600x900 em HTML/CSS Puro

Para apresentações, propostas comerciais e relatórios de alto impacto visual sem a fragilidade do PowerPoint:

1. **Formato Nativo 16:9:** Cada slide é renderizado em um contêiner fixo com proporção `1600x900px`, centralizado e escalável no navegador.
2. **Assets Embutidos em Base64:** Logotipos e grafismos são convertidos para Data URIs Base64 (`data:image/png;base64,...`), garantindo que o arquivo `.html` seja 100% independente e funcione offline.
3. **Ritmo Visual e Cadência de Slides:**
   - Alternância de slides claros e escuros (`.slide.dark`, `.slide.white`, `.slide.accent`).
   - Arquétipos de layout: Slide de Abertura com logo de alto contraste, Slide de Problema/Cenário com dados em destaque, Slide de Solução com grid modular e Slide de Fechamento com CTA.
4. **Navegação Interativa Integrada:** Suporte a teclas de seta (Esquerda/Direita), barra de progresso visual no topo e paginação discreta no rodapé.
