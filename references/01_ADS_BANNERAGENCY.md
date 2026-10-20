# 01 · Criativos Publicitários Multicamadas & BannerAgency (Sony)

## Arquitetura de Camadas (Baseada no Sony BannerAgency)
Todo anúncio publicitário de alta conversão gerado pelo agente divide-se estritamente em quatro camadas funcionais:

1. **Camada 1: Fundo / Background Comercial 8K**
   - Gerado via IA fotográfica com iluminação comercial difusa.
   - Amplo espaço negativo calmo reservado no topo (Feed) ou terço superior (Stories) para absorver o bloco de texto.
   - Proibido ruído visual atrás da área da headline.

2. **Camada 2: Produto / Sujeito com Sombra de Contato Orgânica**
   - Produto autêntico recortado (canal alfa transparente).
   - Proibido fundos cinzas ou caixas opacas.
   - Sombra de contato projetada: `Y: 12px`, `Blur: 24px`, `Opacity: 25%`, cor derivada do ambiente escurecido.

3. **Camada 3: Bloco Tipográfico Hierarquizado**
   - Headline: Fonte Bold/Black (700-900), alto contraste com o fundo.
   - Subheadline / Apoio: Regular (400), no máximo 2 linhas, tamanho correspondente a 40-50% da headline.
   - Selo numérico / Badge: Fundo contrastante com texto em caixa alta.

4. **Camada 4: Call-to-Action (Botão de Conversão)**
   - Cor de ação da marca, padding generoso (`16px 32px`), cantos arredondados (`8px` a `12px`), texto claro em negrito.

---

## Matriz Canônica de 4 Variações de Campanha

| Variação | Ângulo Estratégico | Decisão Visual | Aplicação Recomendada |
| :--- | :--- | :--- | :--- |
| **01** | **Rapidez / Conveniência** | Destaque numérico imediato (ex: "2 HORAS", "Hoje"), selo de tempo em cor vibrante | Produto em profundidade, texto dominante no topo |
| **02** | **Economia / Valor Comercial** | Condição comercial em evidência (ex: "Frete Grátis", "Condição Especial") | Composição centralizada ou produtos alinhados lado a lado |
| **03** | **Segurança / Especialista** | Um produto dominante em primeiro plano, bancada técnica ou contexto de credibilidade | Texto lateralizado com espaço negativo calmo |
| **04** | **Variedade / Amplitude** | Linha de produtos em perspectiva sequencial (maior no primeiro plano) | Fundo amplo demonstrando linha completa de opções |

---

## Safe Zones Milimétricas
* **Feed (4:5 | 1080x1350):** Topo calmo para texto e CTA; produto na base ou terço médio.
* **Stories (9:16 | 1080x1920):** Topo (250px livre para interface do Instagram) e base (200px livre para barra de mensagem). Produto na metade inferior.
* **Paridade:** Feed e Stories da mesma variação utilizam rigorosamente a **mesma cena fotográfica**.
