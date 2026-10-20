# 02 · Packshots 3D, Turnaround Sheets & Multi-View (Zero123++, TripoSR, InstantMesh)

## 1. O Conceito de Product Turnaround Sheet (Mapa de Consistência)
Quando uma pessoa envia a imagem de um produto para a IA, o maior erro é tentar gerar a cena final diretamente, resultando em distorções e rótulos deformados.
O pipeline integrado (baseado em **Zero123++**, **TripoSR** e **InstantMesh**) soluciona isso gerando uma **prancha de consistência multi-ângulo**:

### A Prancha de 6 Ângulos Canônicos:
1. **Frontal (0°):** Vista limpa direta da embalagem e rótulo.
2. **Isométrico 45° Esquerda:** Profundidade e volumetria tridimensional.
3. **Isométrico 45° Direita:** Perspectiva comercial com luz de recorte.
4. **Perfil Lateral (90°):** Espessura, conectores, relevo ou tampa.
5. **Visão Superior (Top-down):** Geometria de fechamento e tampa.
6. **Perspectiva de Chão / Flutuante:** Ângulo dinâmico com sombra projetada.

### Prompt Mestre de Turnaround Sheet para IA Generativa:
```text
Product turnaround reference sheet of the attached product. A clean studio contact grid displaying the exact same product from 4 distinct angles: front view, 45-degree isometric three-quarter view, profile side view, and floating 3D perspective angle. Clean neutral grey cyclorama background, soft commercial studio lighting, natural contact shadows under each product, crisp high-end product photography, identical proportions and branding across all views, 8k resolution, photorealistic.
```

---

## 2. Packshot 3D Flutuante & Produto Premium (Floating Product 3D)

### Modo 1: Cena Completa de Estúdio (Nova Geração)
Gera uma cena comercial de alto luxo:
* Acrílicos translúcidos e pódios geométricos minimalistas.
* Refrações cáusticas de luz, partículas ou gotas d'água contextuais da marca.
* Amplo espaço negativo calmo no topo para headline.

```text
Create a premium, cinematic product photography scene. Preserve the exact shape, proportions, materials, colors, details, brand identity, and geometry of the reference product. Position the product with ample negative space surrounding it on an acrylic podium, soft studio caustics, commercial skincare lighting.

/floatingproduct /8k /highquality /besttexture
```

### Modo 2: Aplicação ou Substituição em Cena Existente (Replace/Apply)
Aplica o produto autêntico em uma imagem de fundo já aprovada, mantendo o ambiente intacto:
```text
Apply the product to the image and remove traces of any other product in the same category. Preserve the original image; simply apply or replace the product. Maintain the exact shape, materials, colors, details, brand identity, and geometry of the reference product. Position the product naturally with realistic contact shadows.

/floating_product /8k /high_quality /best_texture
```
