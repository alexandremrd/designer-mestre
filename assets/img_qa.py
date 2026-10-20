#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
img_qa.py - ferramentas locais de imagem do /designer-mestre (ImageMagick 7 `magick`).
Instalar uma vez: winget install ImageMagick.ImageMagick

  prancha   PNGs -> uma folha de conferencia (o agente olha 1 imagem, nao N)
  paridade  previa aprovada x screenshot do Figma -> RMSE + mapa de diferencas
  paleta    N cores dominantes (HEX + %) de foto/logo/referencia
  contraste razao WCAG entre dois HEX (passa 4.5 / 3.0?)
  bbox      recorta logo/PNG pelo conteudo (trim) sem redimensionar
  web       exporta WebP/AVIF leve para LP (sem metadados)

Exemplos:
  python img_qa.py prancha Exportados\\*.png -o Trabalho\\_prancha.jpg
  python img_qa.py paridade previa_feed.png figma_feed.png
  python img_qa.py paleta foto.jpg -n 6
  python img_qa.py contraste "#FFFFFF" "#F26B1D"
  python img_qa.py bbox logo.png -o logo_trim.png
  python img_qa.py web hero.png --largura 1600
"""
import argparse, glob, os, re, shutil, subprocess, sys


def magick():
    m = shutil.which("magick")
    if not m:
        sys.exit("[erro] ImageMagick ausente: winget install ImageMagick.ImageMagick")
    return m


def run(args, capture=False):
    r = subprocess.run([magick()] + args, capture_output=True, text=True)
    if r.returncode not in (0, 1):  # compare devolve 1 quando ha diferenca
        sys.exit("[erro] magick: " + (r.stderr or r.stdout)[:500])
    return (r.stdout + r.stderr) if capture else None


def expand(pats):
    out = []
    for p in pats:
        out += sorted(glob.glob(p)) or [p]
    return [p for p in out if os.path.isfile(p)]


def cmd_prancha(a):
    files = expand(a.arquivos)
    if not files:
        sys.exit("[erro] nenhum arquivo")
    cols = a.colunas or min(4, len(files))
    run(["montage", *files, "-label", "%t", "-font", "Arial", "-pointsize", "18",
         "-thumbnail", f"{a.lado}x{a.lado}>", "-geometry", "+12+12", "-tile", f"{cols}x",
         "-background", "#E9E9E9", a.out])
    print(f"[ok] {a.out}  ({len(files)} pecas)")


def cmd_paridade(a):
    w, h = run(["identify", "-format", "%w %h", a.previa], True).split()[:2]
    tmp = os.path.splitext(a.figma)[0] + "_norm.png"
    run([a.figma, "-resize", f"{w}x{h}!", tmp])
    diff = a.diff or os.path.splitext(a.previa)[0] + "_diff.png"
    txt = run(["compare", "-metric", "RMSE", a.previa, tmp, diff], True)
    m = re.search(r"\(([\d.e-]+)\)", txt)
    val = float(m.group(1)) if m else float("nan")
    os.remove(tmp)
    ok = val <= a.limite
    print(f"[{'ok' if ok else 'DIFERENTE'}] RMSE normalizado {val:.4f} (limite {a.limite}) · mapa: {diff}")
    sys.exit(0 if ok else 2)


def cmd_paleta(a):
    out = run([a.imagem, "-alpha", "off", "-resize", "200x200>", "+dither", "-colors", str(a.n), "-depth", "8",
               "-format", "%c", "histogram:info:-"], True)
    rows = []
    for line in out.splitlines():
        m = re.match(r"\s*(\d+):.*?(#[0-9A-Fa-f]{6})", line)
        if m:
            rows.append((int(m.group(1)), m.group(2).upper()))
    tot = sum(c for c, _ in rows) or 1
    for c, hx in sorted(rows, reverse=True):
        print(f"{hx}  {100 * c / tot:5.1f}%")


def lum(hx):
    hx = hx.lstrip("#")
    ch = [int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    ch = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def cmd_contraste(a):
    l1, l2 = sorted([lum(a.cor1), lum(a.cor2)], reverse=True)
    r = (l1 + 0.05) / (l2 + 0.05)
    print(f"{a.cor1} x {a.cor2} = {r:.2f}:1 · texto normal {'OK' if r >= 4.5 else 'FALHA'} (4.5) · "
          f"texto >= 24 px {'OK' if r >= 3 else 'FALHA'} (3.0)")


def cmd_bbox(a):
    out = a.out or os.path.splitext(a.imagem)[0] + "_trim.png"
    run([a.imagem, "-fuzz", f"{a.fuzz}%", "-trim", "+repage", out])
    print(f"[ok] {out}  bbox {run(['identify', '-format', '%wx%h', out], True).strip()}")


def cmd_web(a):
    base = os.path.splitext(a.imagem)[0]
    for ext, q in (("webp", 80), ("avif", 55)):
        out = f"{base}.{ext}"
        run([a.imagem, "-strip", "-resize", f"{a.largura}x>", "-quality", str(q), out])
        print(f"[ok] {out}  {os.path.getsize(out) // 1024} KB")


def main():
    ap = argparse.ArgumentParser(description="QA de imagem local /designer-mestre")
    s = ap.add_subparsers(dest="cmd", required=True)
    p = s.add_parser("prancha"); p.add_argument("arquivos", nargs="+"); p.add_argument("-o", "--out", required=True)
    p.add_argument("--colunas", type=int); p.add_argument("--lado", type=int, default=540); p.set_defaults(f=cmd_prancha)
    p = s.add_parser("paridade"); p.add_argument("previa"); p.add_argument("figma"); p.add_argument("--diff")
    p.add_argument("--limite", type=float, default=0.03); p.set_defaults(f=cmd_paridade)
    p = s.add_parser("paleta"); p.add_argument("imagem"); p.add_argument("-n", type=int, default=6); p.set_defaults(f=cmd_paleta)
    p = s.add_parser("contraste"); p.add_argument("cor1"); p.add_argument("cor2"); p.set_defaults(f=cmd_contraste)
    p = s.add_parser("bbox"); p.add_argument("imagem"); p.add_argument("-o", "--out"); p.add_argument("--fuzz", type=int, default=3)
    p.set_defaults(f=cmd_bbox)
    p = s.add_parser("web"); p.add_argument("imagem"); p.add_argument("--largura", type=int, default=1600); p.set_defaults(f=cmd_web)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
