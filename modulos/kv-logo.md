# Módulo KV, Brand book e Logo

## KV / Brand book (MIV Scanner — Cold Start)
Usado quando pedido ou quando um cliente novo entra na Rota B (Cold Start) sem `STATUS_KV: VALIDADO` em `_DESIGN\design_system.md`.
1. Ler o manual ou MIV, os logos, as fotos e as campanhas recebidas. Consultar site e Instagram se informados.
2. Extrair e consolidar:
   - conceito e símbolo;
   - versões da logo (renderizar cada arquivo uma única vez e anotar nome · layout · cor · proporção do bbox);
   - paleta (HEX, RGB, CMYK, escala 50–900, cores semânticas, contraste WCAG);
   - tipografia (oficial + substituta Google Fonts para o Figma/SVG);
   - grafismos, arquétipos SVG, fotografia (tema · pessoas · luz · contraste), conceito, tom de voz e pilares, O Que Fazer (Aprovados), O Que Não Fazer (Vetos, incluindo cores proibidas) e formatos, nos campos do `_TEMPLATE_CLIENTE\design_system.md`.
3. Contradições vão para `design_system.md › 5. Decisões Pendentes`.
4. Salvar tudo unificado em `_DESIGN\design_system.md` (atualizando para `STATUS_KV: VALIDADO`), o brand book em `Compartilhada\Identidade Visual\` e a página "Brand" no Figma, com estilos e variáveis. Nunca alterar arquivos oficiais já existentes nessa pasta.

Brand book em 16:9: capa, índice, logo (versões, área de proteção, tamanho mínimo, fundos, monocromia, usos indevidos), cores, tipografia, grafismos e aplicações. Skill de apoio, se instalada: `brandbook-guia-de-marca`.

## Logo nova (somente sob pedido explícito)
- Se o cliente já tem logo, confirmar que é redesign ou marca nova.
- Logo de cliente nunca é criada sem esse pedido explícito. Faltou logo num pedido comum: pedir (núcleo, 3.5).
- Etapas:
  1. Briefing: nome, setor, valores, público, concorrentes e restrições.
  2. Pesquisa de concorrência para diferenciar. Nunca imitar marca existente.
  3. Três rotas (símbolo, lettering, combinação) em vetor no Figma, com versões horizontal e vertical, cor/positivo/negativo, área de proteção e tamanho mínimo.
  4. Após aprovação, exportar SVG e PNG para `Compartilhada\Identidade Visual\` e registrar na tabela de logos do `_DESIGN\design_system.md`. A partir daí vale a lei 1 (logo existente).
