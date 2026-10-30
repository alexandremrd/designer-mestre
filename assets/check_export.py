#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_export.py - Checks the exported file before saying "done" (implements quality.md §K).

Usage:
  uv run --with imageio-ffmpeg python check_export.py <file> [--duration S] [--fps N] [--size WxH]
Video (mp4/mov/webm): duration, fps, pix_fmt, color range (tv/pc), resolution and audio presence, read from the
ffmpeg header (imageio-ffmpeg does not ship ffprobe). mp4 requires yuv420p (not yuvj420p) and tv range.
Image (png/jpg/webp): size > 0 and dimensions; without PIL installed, skips reading the dimensions.
One line per check, [ok] or [fail]; exit code 1 if there is any failure.
Also importable: conferir(caminho, duracao=None, fps=None, tamanho=None) -> True if everything is ok.
"""
import argparse, os, re, shutil, subprocess, sys

VIDEO = (".mp4", ".mov", ".webm", ".m4v")
IMAGEM = (".png", ".jpg", ".jpeg", ".webp")


def achar_ffmpeg():
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("[error] ffmpeg missing: run with  uv run --with imageio-ffmpeg python check_export.py ...")


def _tam(txt):
    try:
        l, a = txt.lower().split("x")
        return int(l), int(a)
    except ValueError:
        sys.exit(f"[error] invalid --size: {txt} (use WxH, e.g. 1080x1350)")


def _conferir_video(caminho, duracao, fps, tamanho, linha):
    cab = subprocess.run([achar_ffmpeg(), "-hide_banner", "-i", caminho], capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stderr
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", cab)
    v = re.search(r"Video: .*", cab)
    if not d or not v:
        return linha(False, "header without duration/video: unreadable file or no video track")
    dur = int(d[1]) * 3600 + int(d[2]) * 60 + float(d[3])
    ok = True
    v = v[0]
    pix = re.search(r"Video: [^,]+(?:\([^)]*\))*[^,]*, (\w+)(?:\(([^)]*)\))?", v)
    pixfmt = pix[1] if pix else "?"
    faixa = "pc" if pixfmt.startswith("yuvj") else "tv"
    if pix and pix[2]:
        m = re.match(r"(tv|pc)", pix[2])
        faixa = m[1] if m else faixa
    res = re.search(r", (\d{2,5})x(\d{2,5})", v)
    f = re.search(r"([\d.]+) fps", v)
    audio = "Audio:" in cab
    ok &= linha(os.path.getsize(caminho) > 0, f"file size {os.path.getsize(caminho)} bytes")
    if caminho.lower().endswith((".mp4", ".m4v")):
        ok &= linha(pixfmt == "yuv420p", f"pix_fmt {pixfmt} (mp4 requires yuv420p, never yuvj420p)")
        ok &= linha(faixa == "tv", f"color range {faixa} (expected tv)")
    else:
        ok &= linha(True, f"pix_fmt {pixfmt}, range {faixa}")
    ok &= linha(bool(res), f"resolution {res[1]}x{res[2]}" if res else "resolution not read")
    if tamanho and res:
        ok &= linha((int(res[1]), int(res[2])) == _tam(tamanho), f"size {res[1]}x{res[2]} (expected {tamanho})")
    ok &= linha(True, f"duration {dur:.2f} s")
    if duracao is not None:
        ok &= linha(abs(dur - duracao) <= 0.05, f"duration {dur:.2f} s (expected {duracao} +-0.05)")
    ok &= linha(bool(f), f"fps {f[1]}" if f else "fps not read")
    if fps is not None and f:
        ok &= linha(abs(float(f[1]) - fps) < 0.01, f"fps {f[1]} (expected {fps})")
    ok &= linha(True, "audio: " + ("yes" if audio else "no"))
    return ok


def _conferir_imagem(caminho, tamanho, linha):
    n = os.path.getsize(caminho)
    ok = linha(n > 0, f"file size {n} bytes")
    try:
        from PIL import Image
    except ImportError:
        print("[ok] PIL missing: dimensions not checked")
        return ok
    try:
        with Image.open(caminho) as im:
            im.load()
            w, h = im.size
    except Exception as e:
        return linha(False, f"unreadable image ({e})")
    ok &= linha(True, f"dimensions {w}x{h}")
    if tamanho:
        ok &= linha((w, h) == _tam(tamanho), f"size {w}x{h} (expected {tamanho})")
    return ok


def conferir(caminho, duracao=None, fps=None, tamanho=None):
    def linha(cond, msg):
        print(f"[{'ok' if cond else 'fail'}] {msg}")
        return bool(cond)

    if not os.path.isfile(caminho):
        return linha(False, f"file not found: {caminho}")
    ext = os.path.splitext(caminho)[1].lower()
    if ext in VIDEO:
        return _conferir_video(caminho, duracao, fps, tamanho, linha)
    if ext in IMAGEM:
        return _conferir_imagem(caminho, tamanho, linha)
    return linha(False, f"unsupported extension: {ext}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Checks the exported file (quality.md §K)")
    ap.add_argument("arquivo")
    ap.add_argument("--duration", dest="duracao", type=float, help="expected seconds (tolerance 0.05)")
    ap.add_argument("--fps", type=float)
    ap.add_argument("--size", dest="tamanho", help="expected WxH, e.g. 1080x1350")
    a = ap.parse_args()
    sys.exit(0 if conferir(a.arquivo, a.duracao, a.fps, a.tamanho) else 1)
