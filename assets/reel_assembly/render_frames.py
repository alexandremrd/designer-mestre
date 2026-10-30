#!/usr/bin/env python3
"""Renders the animated pieces of the Reels (pieces.html) frame by frame, as PNG with a transparent background.

When to use: after writing the pieces in `<delivery>\\Trabalho\\reel\\pieces.html` and having the clean cut in `cut\\clean.mp4`.
The brand colors and fonts come from the client card (`_DESIGN\\mapa.md`, read by client_card.py), never from the HTML.

Usage:
    python render_frames.py --delivery "<delivery folder>" todos            -> frames\\0000.png ... at 30 frames per second
    python render_frames.py --delivery "<delivery folder>" tempos 1.0 7.5   -> qa\\peca_<t>.png, only to check instants
"""
import argparse
import pathlib
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import resources  # noqa: E402
import client_card  # noqa: E402
import gpu_acceleration  # noqa: E402

resources.aplicar_env()  # browser and ffmpeg in the resource root
from playwright.sync_api import sync_playwright  # noqa: E402

QUADROS_POR_SEGUNDO = 30

# color variable name in the piece -> client card key, neutral fallback color
CORES = [
    ("--fundo", "Background color", "#101010"),
    ("--fundo2", "Secondary background color", "#1c1c1c"),
    ("--acento", "Accent color", "#8a8a8a"),
    ("--acento2", "Light accent color", "#c0c0c0"),
    ("--claro", "Text color", "#f5f5f5"),
    ("--neve", "Strong text color", "#ffffff"),
]


def css_da_ficha(ficha):
    """Builds the color variables and the fonts (files in the card's `Fonts` folder). Warns about what is missing."""
    linhas, avisos = [], []
    variaveis = []
    for variavel, chave, reserva in CORES:
        cor = client_card.pegar_cor(ficha, chave, None)
        if cor is None:
            avisos.append(f"client card without `{chave}`: using {reserva}")
            cor = reserva
        variaveis.append(f"{variavel}:{cor}")
    linhas.append(":root{" + ";".join(variaveis) + "}")
    pasta_fontes = client_card.pegar(ficha, "Fonts")
    for familia, chave, estilo in (("FT", "Title font", "normal"), ("FT", "Italic title font", "italic"), ("FX", "Text font", "normal")):
        arquivo = client_card.pegar(ficha, chave)
        if pasta_fontes and arquivo:
            caminho = pathlib.Path(pasta_fontes) / arquivo
            if caminho.is_file():
                peso = "font-weight:100 900;" if familia == "FX" else ""
                linhas.append(f"@font-face{{font-family:'{familia}';src:url('{caminho.as_uri()}');font-style:{estilo};{peso}}}")
                continue
            avisos.append(f"font not found: {caminho}")
        else:
            avisos.append(f"client card without `{chave}` or `Fonts`: the piece uses a fallback font")
    return "\n".join(linhas), avisos


def duracao_do_corte(reel):
    saida = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(reel / "cut" / "clean.mp4")],
                           capture_output=True, text=True).stdout.strip()
    return float(saida)


def principal():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--delivery", dest="entrega", default=".", help="delivery folder (the one that contains Trabalho)")
    ap.add_argument("modo", choices=["todos", "tempos"])
    ap.add_argument("tempos", nargs="*", type=float, help="instants in seconds, in `tempos` mode")
    a = ap.parse_args()

    reel = pathlib.Path(a.entrega).resolve() / "Trabalho" / "reel"
    modelo = reel / "pieces.html"
    if not modelo.is_file():
        sys.exit(f"Could not find {modelo}. Copy pieces_template.html there and write the video's pieces.")

    ficha = client_card.ler(partida=reel)
    if not ficha:
        print("WARNING: no client card (`_DESIGN\\mapa.md`); the piece comes out with neutral colors and font.")
        css, avisos = css_da_ficha({})
    else:
        css, avisos = css_da_ficha(ficha)
    for aviso in avisos:
        print("WARNING:", aviso)

    html = modelo.read_text(encoding="utf-8")
    if "/*FICHA_DO_CLIENTE*/" not in html:
        sys.exit("pieces.html lost the /*FICHA_DO_CLIENTE*/ marker (see pieces_template.html).")
    temporario = reel / "_pieces_with_card.html"
    temporario.write_text(html.replace("/*FICHA_DO_CLIENTE*/", css), encoding="utf-8")

    with sync_playwright() as p:
        navegador = p.chromium.launch(args=["--force-device-scale-factor=1", "--allow-file-access-from-files", *gpu_acceleration.chromium_args()])
        pagina = navegador.new_page(viewport={"width": 1080, "height": 1920})
        pagina.goto(temporario.as_uri())
        pagina.evaluate("document.fonts.ready")
        pagina.wait_for_timeout(600)
        if a.modo == "tempos":
            (reel / "qa").mkdir(exist_ok=True)
            for t in a.tempos:
                pagina.evaluate(f"__render({t})")
                pagina.screenshot(path=str(reel / "qa" / f"peca_{t:05.2f}.png"), omit_background=True)
            print("check written to", reel / "qa")
        else:
            pasta_quadros = reel / "frames"
            pasta_quadros.mkdir(exist_ok=True)
            vazio = None
            total = int(duracao_do_corte(reel) * QUADROS_POR_SEGUNDO) + 1
            for i in range(total):
                visivel = pagina.evaluate(f"__render({i / QUADROS_POR_SEGUNDO})")
                if not visivel and vazio is not None:
                    dados = vazio
                else:
                    dados = pagina.screenshot(type="png", omit_background=True)
                    if not visivel:
                        vazio = dados
                (pasta_quadros / f"{i:04d}.png").write_bytes(dados)
            print("frames:", total)
        navegador.close()
    temporario.unlink(missing_ok=True)


if __name__ == "__main__":
    principal()
