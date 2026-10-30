#!/usr/bin/env python3
"""Checks whether any Reels piece invades the safe zone (the area that the network's buttons and caption do not cover).

Walks through the video every 0.1 s and reports, piece by piece, what goes out of bounds. The fonts and colors of the client card are applied
before measuring, because the text width changes with the font. The default Reels safe zone is x 90 to 914 and y 240 to 1470;
the client can change it in the card with the line `Reels safe zone: 90 914 240 1470` (left right top bottom).

Usage:
    python check_safe_zone.py --delivery "<delivery folder>"
"""
import argparse
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent))
import client_card  # noqa: E402
import gpu_acceleration  # noqa: E402
from render_frames import css_da_ficha, duracao_do_corte  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

PADRAO = (90, 914, 240, 1470)

LER_PECAS = """(t)=>{__render(t);return [...document.querySelectorAll('.peca')].map((e,i)=>{const o=parseFloat(e.style.opacity||0);const r=e.getBoundingClientRect();
return o>0.05?[i,r.left,r.top,r.right,r.bottom,e.className+' '+(e.textContent||'').trim().slice(0,18)]:null}).filter(Boolean)}"""


def principal():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--delivery", dest="entrega", default=".", help="delivery folder (the one that contains Trabalho)")
    a = ap.parse_args()
    reel = pathlib.Path(a.entrega).resolve() / "Trabalho" / "reel"
    ficha = client_card.ler(partida=reel)
    zona = PADRAO
    texto_zona = client_card.pegar(ficha, "Reels safe zone")
    if texto_zona:
        numeros = [int(n) for n in texto_zona.replace(",", " ").split() if n.isdigit()]
        if len(numeros) == 4:
            zona = tuple(numeros)
    x0, x1, y0, y1 = zona
    css, _ = css_da_ficha(ficha)
    modelo = reel / "pieces.html"
    temporario = reel / "_pieces_with_card.html"
    temporario.write_text(modelo.read_text(encoding="utf-8").replace("/*FICHA_DO_CLIENTE*/", css), encoding="utf-8")
    fora = {}
    with sync_playwright() as p:
        navegador = p.chromium.launch(args=["--allow-file-access-from-files", *gpu_acceleration.chromium_args()])
        pagina = navegador.new_page(viewport={"width": 1080, "height": 1920})
        pagina.goto(temporario.as_uri())
        pagina.evaluate("document.fonts.ready")
        pagina.wait_for_timeout(600)
        for i in range(0, int(duracao_do_corte(reel) * 10) + 1):
            t = i / 10
            for indice, esq, topo, dir_, base, nome in pagina.evaluate(LER_PECAS, t):
                if esq < x0 - 0.5 or dir_ > x1 + 0.5 or topo < y0 - 0.5 or base > y1 + 0.5:
                    fora.setdefault((indice, nome), []).append((round(t, 1), round(esq), round(topo), round(dir_), round(base)))
        navegador.close()
    temporario.unlink(missing_ok=True)
    if not fora:
        print(f"safe zone OK (x {x0}-{x1}, y {y0}-{y1})")
        return
    for (indice, nome), amostras in fora.items():
        t, esq, topo, dir_, base = amostras[0]
        print(f"OUT: piece {indice} [{nome}] in {len(amostras)} samples; e.g.: t={t} box=({esq},{topo})-({dir_},{base})")
    sys.exit(1)


if __name__ == "__main__":
    principal()
