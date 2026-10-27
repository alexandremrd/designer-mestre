#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conferir_export.py - Confere o arquivo exportado antes de dizer "pronto" (implementa qualidade.md §K).

Uso:
  uv run --with imageio-ffmpeg python conferir_export.py <arquivo> [--duracao S] [--fps N] [--tamanho LxA]
Video (mp4/mov/webm): duracao, fps, pix_fmt, faixa de cor (tv/pc), resolucao e presenca de audio, lidos do
cabecalho do ffmpeg (o imageio-ffmpeg nao traz ffprobe). mp4 exige yuv420p (nao yuvj420p) e faixa tv.
Imagem (png/jpg/webp): tamanho > 0 e dimensoes; sem PIL instalado, pula a leitura de dimensoes.
Uma linha por conferencia, [ok] ou [falha]; codigo de saida 1 se houver qualquer falha.
Tambem importavel: conferir(caminho, duracao=None, fps=None, tamanho=None) -> True se tudo ok.
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
        sys.exit("[erro] ffmpeg ausente: rode com  uv run --with imageio-ffmpeg python conferir_export.py ...")


def _tam(txt):
    try:
        l, a = txt.lower().split("x")
        return int(l), int(a)
    except ValueError:
        sys.exit(f"[erro] --tamanho invalido: {txt} (use LxA, ex.: 1080x1350)")


def _conferir_video(caminho, duracao, fps, tamanho, linha):
    cab = subprocess.run([achar_ffmpeg(), "-hide_banner", "-i", caminho], capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stderr
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", cab)
    v = re.search(r"Video: .*", cab)
    if not d or not v:
        return linha(False, "cabecalho sem duracao/video: arquivo ilegivel ou sem faixa de video")
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
    ok &= linha(os.path.getsize(caminho) > 0, f"tamanho do arquivo {os.path.getsize(caminho)} bytes")
    if caminho.lower().endswith((".mp4", ".m4v")):
        ok &= linha(pixfmt == "yuv420p", f"pix_fmt {pixfmt} (mp4 exige yuv420p, nunca yuvj420p)")
        ok &= linha(faixa == "tv", f"faixa de cor {faixa} (esperado tv)")
    else:
        ok &= linha(True, f"pix_fmt {pixfmt}, faixa {faixa}")
    ok &= linha(bool(res), f"resolucao {res[1]}x{res[2]}" if res else "resolucao nao lida")
    if tamanho and res:
        ok &= linha((int(res[1]), int(res[2])) == _tam(tamanho), f"tamanho {res[1]}x{res[2]} (esperado {tamanho})")
    ok &= linha(True, f"duracao {dur:.2f} s")
    if duracao is not None:
        ok &= linha(abs(dur - duracao) <= 0.05, f"duracao {dur:.2f} s (esperado {duracao} +-0.05)")
    ok &= linha(bool(f), f"fps {f[1]}" if f else "fps nao lido")
    if fps is not None and f:
        ok &= linha(abs(float(f[1]) - fps) < 0.01, f"fps {f[1]} (esperado {fps})")
    ok &= linha(True, "audio: " + ("sim" if audio else "nao"))
    return ok


def _conferir_imagem(caminho, tamanho, linha):
    n = os.path.getsize(caminho)
    ok = linha(n > 0, f"tamanho do arquivo {n} bytes")
    try:
        from PIL import Image
    except ImportError:
        print("[ok] PIL ausente: dimensoes nao conferidas")
        return ok
    try:
        with Image.open(caminho) as im:
            im.load()
            w, h = im.size
    except Exception as e:
        return linha(False, f"imagem ilegivel ({e})")
    ok &= linha(True, f"dimensoes {w}x{h}")
    if tamanho:
        ok &= linha((w, h) == _tam(tamanho), f"tamanho {w}x{h} (esperado {tamanho})")
    return ok


def conferir(caminho, duracao=None, fps=None, tamanho=None):
    def linha(cond, msg):
        print(f"[{'ok' if cond else 'falha'}] {msg}")
        return bool(cond)

    if not os.path.isfile(caminho):
        return linha(False, f"arquivo nao encontrado: {caminho}")
    ext = os.path.splitext(caminho)[1].lower()
    if ext in VIDEO:
        return _conferir_video(caminho, duracao, fps, tamanho, linha)
    if ext in IMAGEM:
        return _conferir_imagem(caminho, tamanho, linha)
    return linha(False, f"extensao nao suportada: {ext}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Confere o arquivo exportado (qualidade.md §K)")
    ap.add_argument("arquivo")
    ap.add_argument("--duracao", type=float, help="segundos esperados (tolerancia 0.05)")
    ap.add_argument("--fps", type=float)
    ap.add_argument("--tamanho", help="LxA esperado, ex.: 1080x1350")
    a = ap.parse_args()
    sys.exit(0 if conferir(a.arquivo, a.duracao, a.fps, a.tamanho) else 1)
