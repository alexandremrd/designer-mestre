#!/usr/bin/env python3
"""Generates the HTML preview of a Reels for the user to approve: a single file, with the video and audio embedded.

When to use: always before the final MP4. The preview goes in `Aprovação\\`; the MP4 only enters `Exportados\\` after the user's yes.
The file opens in any browser, plays on click or space bar and does not depend on the project folder.
The page colors and font come from the client card (`_DESIGN\\mapa.md`); without a card, the page uses neutral tones.

Usage:
    python generate_html_preview.py "<video.mp4>" "<output.html>" [--title "Piece name"]
"""
import argparse
import base64
import os
import pathlib
import subprocess
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import resources  # noqa: E402
import client_card  # noqa: E402
import gpu_acceleration  # noqa: E402

resources.aplicar_env()


def principal():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("saida")
    ap.add_argument("--title", dest="titulo", default="Reels preview")
    a = ap.parse_args()

    ficha = client_card.ler(partida=pathlib.Path(a.saida).resolve().parent)
    fundo = client_card.pegar_cor(ficha, "Background color", "#101010")
    texto = client_card.pegar_cor(ficha, "Strong text color", "#ffffff")
    destaque = client_card.pegar_cor(ficha, "Accent color", "#8a8a8a")
    fonte = client_card.pegar(ficha, "Caption font", "system-ui")

    leve = os.path.join(tempfile.mkdtemp(), "preview.mp4")
    codec = gpu_acceleration.h264("ffmpeg", ["-c:v", "libx264", "-crf", "27", "-preset", "medium", "-pix_fmt", "yuv420p"], cq=27)  # GPU first (U13)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-vf", "scale=540:960", *codec,
                    "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", leve], check=True)
    video64 = base64.b64encode(open(leve, "rb").read()).decode()
    titulo = a.titulo
    html = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + titulo + '</title>'
            f'<style>:root{{--fundo:{fundo};--texto:{texto};--highlight:{destaque}}}'
            f"html,body{{margin:0;height:100%;background:var(--fundo);color:var(--texto);font-family:'{fonte}',system-ui,sans-serif}}"
            '.pagina{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100%;gap:12px;padding:16px;box-sizing:border-box}'
            '.moldura{position:relative;height:min(82vh,960px);aspect-ratio:9/16;background:#000;border-radius:14px;overflow:hidden;cursor:pointer}'
            'video{width:100%;height:100%;display:block}.botao{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;transition:opacity .2s}'
            '.botao span{width:84px;height:84px;border-radius:50%;background:color-mix(in srgb,var(--fundo) 72%,transparent);border:1px solid var(--highlight);display:flex;align-items:center;justify-content:center}'
            '.botao svg{width:34px;fill:var(--texto);margin-left:5px}.moldura.tocando .botao{opacity:0;pointer-events:none}p{margin:0;font-size:14px;opacity:.75}</style></head><body><div class="pagina">'
            '<div class="moldura" id="moldura"><video id="video" playsinline preload="auto" src="data:video/mp4;base64,' + video64 + '"></video>'
            '<div class="botao"><span><svg viewBox="0 0 24 24"><path d="M6 4l14 8-14 8z"/></svg></span></div></div>'
            '<p>' + titulo + ' · preview 540x960 · space = play/pause</p></div>'
            "<script>const video=document.getElementById('video'),moldura=document.getElementById('moldura');const alternar=()=>video.paused?video.play():video.pause();moldura.onclick=alternar;"
            "addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();alternar()}});video.onplay=()=>moldura.classList.add('tocando');"
            "video.onpause=()=>moldura.classList.remove('tocando');video.onended=()=>moldura.classList.remove('tocando');</script></body></html>")
    os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
    open(a.saida, "w", encoding="utf-8").write(html)
    print("preview:", a.saida, len(html) // 1024, "KB")


if __name__ == "__main__":
    principal()
