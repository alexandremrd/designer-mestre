"""Exporta um motion HTML aprovado (video.md Parte C).

A prévia precisa expor window.__render(t) (posiciona a timeline sem tocar áudio)
e window.__DUR (duração em s), e estar servida por HTTP local (fontes e caminhos relativos).

Uso:
  uv run --with imageio-ffmpeg --with playwright python motion_export.py mp4 <url> <saida.mp4> \
      [--voz narracao.mp3] [--trilha trilha.mp3] [--vol 0.18] [--fps 30] [--tamanho 1080x1350]
  uv run --with playwright python motion_export.py telas <url> <pasta> <prefixo> nome=tempo [nome=tempo ...] [--tamanho 1080x1350]
--tamanho (padrão 1080x1920) define viewport e recorte; o palco da prévia precisa ter esse tamanho.

Render pelo Edge do sistema (channel msedge), sem baixar navegador. O ffmpeg vem do imageio-ffmpeg,
porque o ffmpeg reduzido do Playwright não tem codecs de áudio.
"""
import argparse
import subprocess
from pathlib import Path

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recursos; recursos.aplicar_env()  # navegador e ffmpeg na raiz dos recursos
import conferir_export
from playwright.sync_api import sync_playwright

W, H = 1080, 1920  # padrão; --tamanho troca


def abrir(p, url):
    b = p.chromium.launch(channel="msedge")
    page = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    page.goto(url, wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    # sem controles da prévia: palco em escala 1 ocupando a viewport
    page.add_style_tag(content="#ctl{display:none!important} #wrap{inset:0!important}")
    page.evaluate("document.getElementById('stage').style.transform='none'")
    return b, page


def mp4(a):
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    saida = Path(a.saida); saida.parent.mkdir(parents=True, exist_ok=True)
    so_video = saida.with_name(saida.stem + "_sem_audio.mp4")
    with sync_playwright() as p:
        b, page = abrir(p, a.url)
        dur = page.evaluate("window.__DUR")
        n = int(round(dur * a.fps))
        enc = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(a.fps),
                                "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                                "-pix_fmt", "yuv420p", str(so_video)], stdin=subprocess.PIPE)
        for i in range(n):
            page.evaluate(f"window.__render({i / a.fps})")
            enc.stdin.write(page.screenshot(type="png", clip={"x": 0, "y": 0, "width": W, "height": H}))
            if i % 150 == 0:
                print(f"quadro {i}/{n}", flush=True)
        enc.stdin.close(); enc.wait(); b.close()
    if enc.returncode != 0:
        sys.exit(f"[erro] ffmpeg falhou ao codificar (codigo {enc.returncode}); {saida} nao foi gerado")
    if not a.voz and not a.trilha:
        so_video.replace(saida); conferir_final(saida, dur, a); return
    ins, filtros, mix = ["-i", str(so_video)], [], []
    if a.voz:
        ins += ["-i", a.voz]; filtros.append(f"[{len(mix) + 1}:a]aformat=channel_layouts=stereo,apad,atrim=0:{dur}[v]"); mix.append("[v]")
    if a.trilha:
        ins += ["-i", a.trilha]
        # voz mono + trilha estéreo: forçar estéreo nas duas, senão o amix sai mono
        filtros.append(f"[{len(mix) + 1}:a]aformat=channel_layouts=stereo,volume={a.vol},afade=t=in:st=0:d=1,"
                       f"afade=t=out:st={dur - 2}:d=2,atrim=0:{dur}[m]"); mix.append("[m]")
    filtros.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0,alimiter=limit=0.95[a]")
    subprocess.run([ff, "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(filtros),
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-t", str(dur), "-movflags", "+faststart", str(saida)], check=True)
    so_video.unlink()  # temporário próprio, não referenciado por nada
    conferir_final(saida, dur, a)


def conferir_final(saida, dur, a):
    # qualidade.md §K: so imprime ok se o arquivo passa na conferencia
    if not conferir_export.conferir(str(saida), dur, a.fps, f"{W}x{H}"):
        sys.exit(1)
    print("ok", saida)


def telas(a):
    out = Path(a.pasta); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b, page = abrir(p, a.url)
        for par in a.pares:
            nome, t = par.split("=")
            page.evaluate(f"window.__render({float(t)})")
            page.wait_for_timeout(120)
            alvo = out / f"{a.prefixo}_{nome}.png"
            page.screenshot(path=str(alvo), clip={"x": 0, "y": 0, "width": W, "height": H})
            print(alvo.name)
        b.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("mp4"); m.add_argument("url"); m.add_argument("saida")
    m.add_argument("--voz"); m.add_argument("--trilha"); m.add_argument("--vol", type=float, default=0.18)
    m.add_argument("--fps", type=int, default=30); m.set_defaults(f=mp4)
    t = sub.add_parser("telas"); t.add_argument("url"); t.add_argument("pasta"); t.add_argument("prefixo")
    t.add_argument("pares", nargs="+"); t.set_defaults(f=telas)
    for p in (m, t):
        p.add_argument("--tamanho", default="1080x1920", help="LxA do palco, ex.: 1080x1350")
    a = ap.parse_args()
    W, H = (int(x) for x in a.tamanho.lower().split("x"))
    a.f(a)
