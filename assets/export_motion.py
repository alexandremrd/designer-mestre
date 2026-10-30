"""Exports an approved HTML motion (video.md §6 and §7).

The preview must expose window.__render(t) (positions the timeline without playing audio)
and window.__DUR (duration in s), and be served over local HTTP (fonts and relative paths).

Usage:
  uv run --with imageio-ffmpeg --with playwright python export_motion.py mp4 <url> <output.mp4> \
      [--voice voiceover.mp3] [--track soundtrack.mp3] [--vol 0.18 | --lufs -14] [--fps 30] [--size 1080x1350]
  uv run --with playwright python export_motion.py screens <url> <folder> <prefix> name=time [name=time ...] [--size 1080x1350]
--size (default 1080x1920) sets the viewport and crop; the preview stage must have that size.

Renders through the system's Edge (channel msedge), without downloading a browser. ffmpeg comes from imageio-ffmpeg,
because Playwright's stripped-down ffmpeg has no audio codecs.
"""
import argparse
import subprocess
from pathlib import Path

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resources; resources.aplicar_env()  # browser and ffmpeg in the resource root
import check_export, gpu_acceleration
from playwright.sync_api import sync_playwright

W, H = 1080, 1920  # default; --size changes it


def abrir(p, url):
    b = p.chromium.launch(channel="msedge", args=gpu_acceleration.chromium_args())  # U13: raster and compositing on the GPU
    page = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    page.goto(url, wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    # no preview controls: stage at scale 1 filling the viewport
    page.add_style_tag(content="#ctl{display:none!important} #wrap{inset:0!important}")
    page.evaluate("document.getElementById('stage').style.transform='none'")
    return b, page


def achar_ffmpeg():
    """ffmpeg with audio codecs: the one from imageio-ffmpeg or the one in the user's resource root (resources.py puts it on PATH).
    With neither, ask for authorization to install in the central location, never on C: nor in ~/.cache."""
    import shutil
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass
    ff = shutil.which("ffmpeg")
    if ff:
        return ff
    sys.exit("[no ffmpeg] Ask the user for authorization to install ffmpeg in their central resource location "
             f"({resources.raiz() or 'root not yet set: ask where the resources live'}).")


def mp4(a):
    ff = achar_ffmpeg()
    saida = Path(a.saida); saida.parent.mkdir(parents=True, exist_ok=True)
    so_video = saida.with_name(saida.stem + "_sem_audio.mp4")
    with sync_playwright() as p:
        b, page = abrir(p, a.url)
        dur = page.evaluate("window.__DUR")
        n = int(round(dur * a.fps))
        enc = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(a.fps),
                                "-i", "-", *gpu_acceleration.h264(ff, ["-c:v", "libx264", "-preset", "slow", "-crf", "16",
                                                          "-pix_fmt", "yuv420p"], cq=16),
                                str(so_video)], stdin=subprocess.PIPE)
        for i in range(n):
            page.evaluate(f"window.__render({i / a.fps})")
            enc.stdin.write(page.screenshot(type="png", clip={"x": 0, "y": 0, "width": W, "height": H}))
            if i % 150 == 0:
                print(f"frame {i}/{n}", flush=True)
        enc.stdin.close(); enc.wait(); b.close()
    if enc.returncode != 0:
        sys.exit(f"[error] ffmpeg failed while encoding (code {enc.returncode}); {saida} was not generated")
    if not a.voz and not a.trilha:
        so_video.replace(saida); conferir_final(saida, dur, a); return
    ins, filtros, mix = ["-i", str(so_video)], [], []
    ganho = f"loudnorm=I={a.lufs}:TP=-1.5:LRA=9" if a.lufs is not None else f"volume={a.vol}"  # --lufs: soundtrack alone
    if a.voz:
        ins += ["-i", a.voz]; filtros.append(f"[{len(mix) + 1}:a]aformat=channel_layouts=stereo,apad,atrim=0:{dur}[v]"); mix.append("[v]")
    if a.trilha:
        ins += ["-i", a.trilha]
        # mono voice + stereo soundtrack: force stereo on both, otherwise amix comes out mono
        filtros.append(f"[{len(mix) + 1}:a]aformat=channel_layouts=stereo,{ganho},afade=t=in:st=0:d=1,"
                       f"afade=t=out:st={dur - 2}:d=2,atrim=0:{dur}[m]"); mix.append("[m]")
    filtros.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0,alimiter=limit=0.95[a]")
    subprocess.run([ff, "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(filtros),
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-t", str(dur), "-movflags", "+faststart", str(saida)], check=True)
    so_video.unlink()  # its own temporary, referenced by nothing
    conferir_final(saida, dur, a)


def conferir_final(saida, dur, a):
    # quality.md §K: only prints ok if the file passes the check
    if not check_export.conferir(str(saida), dur, a.fps, f"{W}x{H}"):
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
    m.add_argument("--voice", dest="voz"); m.add_argument("--track", dest="trilha"); m.add_argument("--vol", type=float, default=0.18); m.add_argument("--lufs", type=float)
    m.add_argument("--fps", type=int, default=30); m.set_defaults(f=mp4)
    t = sub.add_parser("screens"); t.add_argument("url"); t.add_argument("pasta"); t.add_argument("prefixo")
    t.add_argument("pares", nargs="+"); t.set_defaults(f=telas)
    for p in (m, t):
        p.add_argument("--size", dest="tamanho", default="1080x1920", help="WxH of the stage, e.g. 1080x1350")
    a = ap.parse_args()
    W, H = (int(x) for x in a.tamanho.lower().split("x"))
    a.f(a)
