#!/usr/bin/env python3
"""product_mask.py - full-frame product alpha, for `treat_image.mjs grade --mascara` and for depth cutout.

  python product_mask.py locate <original> <cutout_rgba.png> -o <alpha.png>
      finds where the library cutout sits in the original (template matching) and returns the alpha at the
      full frame of the original. The product pixels remain those of the original; also useful for edge cutout.
  python product_mask.py grabcut <original> --box x0,x1,y0,y1 -o <alpha.png>
      GrabCut at 1/6 scale; box in image fractions (0 to 1). PROTECTION mask only (soft edge):
      not suitable for the product to leave the frame.
Requires opencv-python and numpy (python -I; no rembg, which downloads a model)."""
import argparse
import sys

import cv2
import numpy as np


def localizar(original, recorte, saida):
    o = cv2.imread(original, 0)
    c = cv2.imread(recorte, cv2.IMREAD_UNCHANGED)
    if o is None or c is None or c.ndim < 3 or c.shape[2] < 4:
        sys.exit("[error] invalid original or cutout (the cutout needs an alpha channel)")
    a = c[:, :, 3]
    g = cv2.cvtColor(c[:, :, :3], cv2.COLOR_BGR2GRAY)
    s = 0.25
    os_ = cv2.resize(o, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    gs = cv2.resize(g, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    as_ = cv2.resize((a > 128).astype(np.uint8) * 255, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    res = cv2.matchTemplate(os_, gs, cv2.TM_CCORR_NORMED, mask=as_)
    _, mx, _, loc = cv2.minMaxLoc(res)
    x0, y0 = int(loc[0] / s), int(loc[1] / s)
    melhor = None
    for dy in range(-6, 7, 2):
        for dx in range(-6, 7, 2):
            x, y = x0 + dx, y0 + dy
            if x < 0 or y < 0 or y + g.shape[0] > o.shape[0] or x + g.shape[1] > o.shape[1]:
                continue
            d = np.abs(o[y:y + g.shape[0], x:x + g.shape[1]].astype(int) - g.astype(int))[a > 200].mean()
            if melhor is None or d < melhor[0]:
                melhor = (d, x, y)
    if melhor is None:
        sys.exit("[error] cutout does not fit in the original")
    d, x, y = melhor
    full = np.zeros(o.shape, np.uint8)
    full[y:y + g.shape[0], x:x + g.shape[1]] = a
    cv2.imwrite(saida, full)
    print(f"[ok] {saida} correlation={mx:.4f} mean_difference={d:.2f} position={x},{y}"
          + ("  [warning] high difference: check the position" if d > 25 else ""))


def grabcut(original, caixa, saida):
    im = cv2.imread(original)
    if im is None:
        sys.exit("[error] invalid original")
    x0, x1, y0, y1 = (float(v) for v in caixa.split(","))
    h0, w0 = im.shape[:2]
    sm = cv2.resize(im, None, fx=1 / 6, fy=1 / 6, interpolation=cv2.INTER_AREA)
    h, w = sm.shape[:2]
    rect = (int((x0 - .02) * w), int((y0 - .02) * h), int((x1 - x0 + .04) * w), int((y1 - y0 + .04) * h))
    m = np.zeros((h, w), np.uint8)
    cv2.grabCut(sm, m, rect, np.zeros((1, 65)), np.zeros((1, 65)), 8, cv2.GC_INIT_WITH_RECT)
    mk = np.where((m == 1) | (m == 3), 255, 0).astype(np.uint8)
    mk = cv2.dilate(cv2.morphologyEx(mk, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)), np.ones((5, 5), np.uint8))
    cv2.imwrite(saida, cv2.resize(mk, (w0, h0), interpolation=cv2.INTER_LINEAR))
    print(f"[ok] {saida} (protection mask; check it as an overlay before using)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("locate")
    a.add_argument("original"); a.add_argument("recorte"); a.add_argument("-o", required=True)
    b = sub.add_parser("grabcut")
    b.add_argument("original"); b.add_argument("--box", dest="caixa", required=True); b.add_argument("-o", required=True)
    r = p.parse_args()
    localizar(r.original, r.recorte, r.o) if r.cmd == "locate" else grabcut(r.original, r.caixa, r.o)
