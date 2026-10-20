# 07 · Motion Design Automatizado (MovimentAI & Remotion)

## 1. O Princípio MovimentAI: Separação de Lógica e Identidade

O maior desperdício de tempo em motion design é o trabalho mecânico de substituição de textos e troca de cores. A solução divide o projeto em dois eixos independentes:

| Eixo | O que é | Como Opera |
| :--- | :--- | :--- |
| **Comps (Momentos)** | Os blocos estruturais do vídeo — Abertura, Headline, Dado/Número, Citação, CTA | Construídos como templates neutros reutilizáveis |
| **KV (Skin)** | A identidade visual da marca — Cores HEX, Fontes, Logotipo, Áudio | Aplicado dinamicamente sobre as comps neutras |

---

## 2. Segmentação Lógica de Copy
A decisão de onde cortar e tipar cenas é baseada em regras semânticas:
* **Gancho (Hook):** Linha inicial interrogativa (`?`) ou afirmação curta de alto impacto.
* **Cena de Dado:** Presença de números, `%` ou valores monetários (`R$`).
* **Cena de Citação:** Presença de aspas ou atribuição de autor.
* **CTA:** Verbos imperativos de ação direcionada ao espectador.

---

## 3. Renderização Programática via Remotion (`@remotion/still`)
Para criativos estáticos de alta resolução e animações baseadas em código:
* Renderização direta de frames `1080x1350` e `1080x1920` através de HTML/React, sem necessidade de carregar interfaces pesadas do After Effects quando a demanda exigir velocidade.
