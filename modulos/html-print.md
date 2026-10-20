# Submódulo HTML — Recriar de print ou vídeo

- **Fidelidade total ao print:** mesmas cores, tamanhos, espaçamentos, fontes e textos, com o texto **exato** da imagem.
- **Imagens do print:**
  - extrair as recortáveis;
  - as que não dá para extrair vêm de `Compartilhada\Imagens\` ou são geradas por IA (salvas em `IA\`).
- **Vários prints:** se forem páginas diferentes, gerar páginas ligadas entre si; se não tiverem relação, separar em seções "Print 1", "Print 2".
- **Print de celular:** sem moldura do aparelho nem barra do navegador.
- **Vídeo:**
  - recriar o comportamento para que as mesmas interações produzam o mesmo resultado;
  - prestar atenção a cor, fonte, padding, margin e borda;
  - mockar dados quando houver backend;
  - deixar funcional com JS.
- **Verificação:** renderizar em desktop e mobile e comparar lado a lado com o print. Corrigir até ficar igual.
