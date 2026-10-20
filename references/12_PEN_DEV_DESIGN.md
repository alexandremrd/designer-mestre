# 12 · pen.dev Design Engine (Headless UI, Apps, Dashboards & Graphics)

O **pen.dev** é uma ferramenta de design headless orientada a IA integrada ao agente `/design` como opção de alta fidelidade para criação estruturada de telas, layouts e mockups visuais.

---

## 💡 O QUE É O PEN.DEV
O `pen.dev` opera através de uma CLI inteligente (`@pen.dev/cli`) que gera arquivos `.pen` (formato JSON estruturado proprietário com árvore de nós, estilos, layout flexível e vetores) e exporta imagens nítidas renderizadas em alta definição (2x/4x) em PNG, WebP ou PDF.

### Quando Usar `/design pen`:
- Geração completa de **telas de aplicativos** (iOS / Android).
- **Dashboards analíticos** e painéis administrativos complexos.
- **Wireframes e mockups de websites** e páginas institucionais.
- **Slides de apresentação**, pôsteres, banners de marketing e gráficos para redes sociais.
- Quando o usuário solicita: *"desenhe uma tela de..."*, *"crie um mockup de..."*, *"como ficaria o visual de..."*.

---

## 🛠️ CONFIGURAÇÃO & INSTALAÇÃO

O pacote foi instalado globalmente no ambiente via npm:
```bash
npm install -g @pen.dev/cli
```

### Verificação de Status:
```bash
pen version   # Exibe a versão instalada (ex: 0.3.12)
pen status    # Verifica autenticação do usuário
```

### Autenticação:
Para uso completo do agente pen.dev:
1. `pen login` (via navegador ou código de verificação) ou `pen signup`.
2. Alternativamente, definir a variável de ambiente `PEN_CLI_KEY`.
3. Provedores de agente suportados:
   - `--agent google` (utiliza Gemini via `GEMINI_API_KEY`)
   - `--agent claude` (padrão, utiliza Claude via assinatura ou `ANTHROPIC_API_KEY`)
   - `--agent codex` (via `pen codex-login`)

---

## 🚀 COMANDO CENTRAL NO `/design`

```bash
pen --out <caminho.pen> --prompt "<descrição do usuário>" --export <caminho.png> --export-scale 2
```

### Principais Parâmetros:
- `--out, -o <arquivo.pen>`: Caminho obrigatório onde o design `.pen` será salvo.
- `--prompt, -p "<texto>"`: A descrição exata do que o usuário deseja.
  > **Regra de Ouro do Prompt:** Passe a solicitação do usuário diretamente sem inflar ou inventar paletas/estruturas artificiais. O agente do pen.dev possui inteligência de design própria para definir layouts, tipografia, espaçamentos e hierarquia.
- `--prompt-file, -f <arquivo>`: Anexa imagem de referência ou arquivo de texto para direcionamento de estilo.
- `--export, -e <arquivo.png>`: Exporta a imagem renderizada final.
- `--export-scale 2`: Fator de escala (2x garante nitidez cristalina sem borrões).
- `--export-type`: `png` (padrão), `webp`, `jpeg`, `pdf`.
- `--in, -i <arquivo.pen>`: Design pré-existente para iterações incrementais.

---

## 🔄 FLUXO DE ITERAÇÃO VISUAL

Quando o usuário solicitar refinamentos em um design já criado:
```bash
pen --in designs/tela-v1.pen --out designs/tela-v2.pen --prompt "Mude o botão principal para azul cobalto e adicione um gráfico de linha no card superior" --export designs/tela-v2.png --export-scale 2
```

O pen.dev lê a árvore de nós existente no arquivo `.pen` anterior e aplica apenas as alterações solicitadas, mantendo o restante da consistência visual.

---

## 🔗 SINCRONIA COM O `/design` & CANVAS
1. Os arquivos `.pen` e imagens exportadas são salvos preferencialmente na pasta do projeto ou cliente (`designs/` ou `Clientes\[Cliente]\`).
2. O resultado visual `.png` renderizado abre imediatamente no **Interactive Canvas** do Antigravity para visualização pelo usuário.
3. Não substitui nenhum outro motor: soma-se ao ecossistema do `/design` ao lado de Figma, Remotion, Colli PPT e BannerAgency.
