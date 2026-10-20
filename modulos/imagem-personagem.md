# Anexo Imagem · Personagem / Rosto Recorrente
Carregado só junto com `imagem.md` (Partes A–B). Lei 5 do núcleo: pessoa real só com autorização registrada.

## Personagem / Rosto Recorrente (Fotos Reais → Padrão → Imagem Fiel)

Usado quando a peça mostra **a mesma pessoa** de forma recorrente (fundador, especialista, médico, palestrante, porta-voz). Tudo específico da pessoa mora exclusivamente em `[Cliente]\_DESIGN\Personagens\[Pessoa]\PERSONAGEM_[PESSOA].md` e `Referências\`.

### 1. Autorização e Limites
- Rosto de pessoa real em IA requer **autorização registrada** no dossiê (`Autorização: data · quem · arquivo`). Sem registro: gerar apenas como teste interno e avisar o usuário.
- Vetos do `design_system.md` prevalecem até ordem explícita do usuário (gravar decisão).
- Proibido: celebridade/figura pública externa, menor de idade, ou usar imagem gerada como depoimento real, ato clínico/técnico verdadeiro ou endosso que não ocorreu.

### 2. Construção do Padrão (uma vez por pessoa)
1. **Seleção de 4–8 fotos originais** (`Originais\[Pessoa]\`, intactas): frontal neutra, frontal sorrindo, close, ¾ esq./dir., meio corpo, sentado (olhos nítidos, luz uniforme, sem óculos escuros, filtro ou mão no rosto). **Mestra** = frontal com melhor luz.
2. **Pacote `_ref` + Atlas:** salvar cópias 2048 px (`_ref`) em `_DESIGN\Personagens\[Pessoa]\Referências\` + folha `atlas_[pessoa].jpg` apenas para inspeção humana (nunca enviar o atlas inteiro como referência única para não diluir traços). Vistas de referência geradas (frontal, ¾, perfil) seguem a regra de **fundo neutro sem cor** do `imagem-produto.md` §1; cenas da pessoa são saídas e vão para `Imagens\IA\`.
3. **Checklist facial + Regras corretivas + Descritor (EN):** numerar traços observáveis (cabelo/calvície, barba/bigode e padrão grisalho, sobrancelhas, olhos, formato facial/mandíbula, nariz, tom/textura de pele, orelhas, porte, expressão base), registrar regras corretivas contra desvios do modelo e fechar com o descritor em inglês + `"keep his/her facial features, bone structure and skin texture 100% identical to the reference photos"`.

### 3. Execução, Verificação e Homologação
- Usar geradores com suporte a referência de imagem (Antigravity / Nano Banana Pro com até 14 referências indexadas, subagente da IDE, ou motor local com `--ref`, enviando mestra + ângulo mais próximo, 3–4 fotos). No prompt, descrever **apenas o que muda** (cenário, luz, pose, enquadramento) + repetir o descritor 1×. Nunca posicionar texto sobre o rosto.
- Comparar resultado × mestra item a item do checklist. Se desviar (máx. 3 tentativas): (1) reforçar regra corretiva no prompt; (2) usar referência mais limpa e no mesmo ângulo; (3) gerar a cena/corpo primeiro e fazer inpainting/edição localizada só na cabeça com a mestra.
- **Homologação inicial:** validar 3 cenas (frontal neutra, ¾ sorrindo, meio corpo sentado) no KV do cliente antes de liberar para produção em escala.
