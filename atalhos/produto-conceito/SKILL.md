---
name: "produto-conceito"
description: "Atalho do /designer-mestre para foto conceito de produto e aplicação de 1..N produtos reais em cena (/input): imagem de campanha que transmite uma ideia, sentimento, metáfora ou narrativa usando o produto com embalagem inalterada, rótulo 100% legível e prancha de aprovação por slot estilo /360-produto. Use quando o usuário chamar /produto-conceito, /designer-mestre /input com produto, ou pedir foto conceito, aplicar produtos em imagem de conceito, metáfora visual ou editorial de campanha."
---

# /produto-conceito

Atalho: não tem regras próprias. Carregue o núcleo `SKILL.md` da skill `designer-mestre` (pasta irmã desta, no mesmo diretório de skills) e siga-o inteiro, porque autorização, acervo do cliente, gasto, aval único e fecho moram lá. Depois abra `modulos/imagem.md` Partes A–B, `ads.md` §1 + `imagem.md` Parte C (é imagem de marca), `modulos/imagem-produto.md` §§1–3 (fontes do produto, gate do gerador e rótulo real) e §5, que é o dono desta entrega (cobre tanto criar conceito do zero quanto aplicar 1..N produtos em cena enviada com `/input`), com a biblioteca `references/conceito/biblioteca.md` só ao compor cena nova. Aprovação (prancha lado a lado por slot `1..N`) e refação isolada por produto seguem o padrão do `/360-produto`.

Argumentos livres: `/input` (opcional, trava a imagem-conceito enviada), cliente, pastas/nomes de 1..N produtos e conceito. Sem `/input`, a IA escolhe o conceito por estudo do produto, do cliente e do histórico; com `/input` ou imagem-conceito anexa, preserva a cena e aplica todos os produtos listados com embalagem e rótulo originais legíveis. Sem cliente ou produto claro, pergunte uma vez.
