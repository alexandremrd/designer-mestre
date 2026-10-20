---
name: pen-design
description: >
  Create high-quality visual designs — websites, app screens, dashboards, slides, marketing materials, social media graphics — using the pen.dev CLI tool. Use this skill whenever the user wants to create, generate, or visualize any kind of UI design, mockup, wireframe, layout, webpage, app screen, presentation slide, poster, banner, or marketing asset. Also use it when the user says things like "design me a...", "make a visual for...", "create a mockup of...", "what would X look like?", or wants to turn an idea into a visual. Even if the user doesn't mention "pen.dev" or "design tool" explicitly — if they want something visual created, this is the skill to use.
---

# pen.dev Design Engine

Create professional visual designs from natural language descriptions using the pen.dev CLI. pen.dev is a headless design tool that generates `.pen` files (a structured JSON design format) and can export them as images.

## Setup & CLI

The CLI is installed globally at `@pen.dev/cli` (`pen`).
Run `pen --help` or `pen status` to check configuration.

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
