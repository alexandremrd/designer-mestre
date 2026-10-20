---
name: pen-engine
description: >
  Motor interno de canvas vetorial estruturado (.pen JSON) para prototipação rápida de layouts, telas, slides e peças gráficas via linha de comando.
---

# Motor Interno de Canvas Vetorial (`.pen`)

Gera e itera arquivos estruturados `.pen` (JSON vetorial de layout) com exportação direta para PNG/WebP/PDF em alta resolução.

## Setup & CLI

O binário `pen` opera via linha de comando local.
Rode `pen --help` ou `pen status` para checar a configuração.

### Core Command:
```bash
pen --out <output.pen> --prompt "<design description>" --export <output.png> --export-scale 2
```

### Key Flags:
- `--out, -o`: Path to `.pen` structured JSON design file (required)
- `--prompt, -p`: Natural language description passed directly
- `--prompt-file, -f`: Image or file attachment for reference style
- `--export, -e`: Target path for rendered visual (`.png`, `.webp`, `.pdf`)
- `--export-scale`: Resolution multiplier (default 2 for high-res crisp design)
- `--in, -i`: Previous `.pen` file for iterations
- `--agent`: Agent provider (`claude`, `google`, `codex`)
