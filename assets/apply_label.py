"""Applies the real label artwork (rasterized PDF) on top of a cylindrical bottle in a scene.

Usage (one slot per call; call again on the output for the next slot):
  python apply_label.py --scene scene.jpg --artwork artwork.png --output output.jpg \
      --box X0 Y0 X1 Y1 --body Y0 Y1 --center CX --radius R [--factor 2] [--ss 3]

--box   sticker rectangle in the scene (scene px, decimals accepted), from the left to the right edge of the bottle
--body   rows of the flat artwork where the label body is (without stripes or bleed)
--center  column of the flat artwork that falls on the front center of the bottle
--radius    radius of the cylinder in the flat artwork (artwork px); the artwork is curved with arcsin at the edges
--factor   enlarges the scene first (Lanczos); the --box coordinates remain those of the original scene
--ss      supersampling of the mask and the mapping (edge antialiasing)

Preserves the bottle's shadow: the brightness of the area becomes a light map (median/gauss without the old ink)
multiplied onto the artwork. Artwork is never rewritten by AI. Uniform scale by the radius: no x/y distortion;
any leftover height is filled with white, not stretched.
"""
import argparse
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates, gaussian_filter

Image.MAX_IMAGE_PIXELS = None


def aplicar(cena, arte, caixa, corpo, cx, raio, fator=1, ss=3):
    W, H = cena.size
    S = cena.resize((W * fator, H * fator), Image.LANCZOS) if fator > 1 else cena.copy()
    f = fator
    X0, Y0, X1, Y1 = (v * f for v in caixa)
    SY0, SY1 = corpo
    half = (X1 - X0) / 2
    xc = (X0 + X1) / 2
    k = half / raio                                   # scene px per artwork px (uniform)
    pad = ((Y1 - Y0) / k - (SY1 - SY0)) / 2           # white margin above and below the body
    xi0, xi1 = int(np.floor(X0)), int(np.ceil(X1))
    yi0, yi1 = int(np.floor(Y0)), int(np.ceil(Y1))
    w, h = xi1 - xi0, yi1 - yi0

    sa = k * ss
    small = np.asarray(arte.resize((max(1, int(arte.width * sa)), max(1, int(arte.height * sa))),
                                   Image.LANCZOS)).astype(float)
    xs = xi0 + (np.arange(w * ss) + 0.5) / ss
    ys = yi0 + (np.arange(h * ss) + 0.5) / ss
    XX, YY = np.meshgrid(xs, ys)
    inside = ((XX >= X0) & (XX <= X1) & (YY >= Y0) & (YY <= Y1)).astype(float)
    th = np.arcsin(np.clip((XX - xc) / half, -1, 1))  # cylinder curvature
    ax = cx + raio * th
    ay = SY0 - pad + (YY - Y0) / k
    body = (ay >= SY0) & (ay <= SY1)
    lab = np.stack([map_coordinates(small[..., c], [ay * sa - 0.5, ax * sa - 0.5],
                                    order=1, mode='nearest') for c in range(3)], -1)
    lab[~body] = 255.0

    def down(a):
        return a.reshape(h, ss, w, ss, *a.shape[2:]).mean((1, 3))

    a = down(inside)
    labp = down(lab * inside[..., None]) / np.maximum(a[..., None], 1e-6)

    sc = np.asarray(S.crop((xi0, yi0, xi1, yi1))).astype(float)
    m = int(np.ceil(3 * f))
    inner = sc.mean(2)[m:-m, m:-m]
    luz = np.pad(gaussian_filter(inner, 1.5 * f ** 0.5, mode='nearest'), m, mode='edge')
    labp = labp * np.clip(luz / 255.0, 0.3, 1.0)[..., None]  # bottle shadow over the artwork

    res = sc * (1 - a[..., None]) + labp * a[..., None]
    out = np.asarray(S).astype(float)
    out[yi0:yi1, xi0:xi1] = res
    return Image.fromarray(np.clip(out + 0.5, 0, 255).astype('uint8')), pad


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--scene', dest='cena', required=True)
    p.add_argument('--artwork', dest='arte', required=True)
    p.add_argument('--output', dest='saida', required=True)
    p.add_argument('--box', dest='caixa', nargs=4, type=float, required=True, metavar=('X0', 'Y0', 'X1', 'Y1'))
    p.add_argument('--body', dest='corpo', nargs=2, type=float, required=True, metavar=('Y0', 'Y1'))
    p.add_argument('--center', dest='centro', type=float, required=True)
    p.add_argument('--radius', dest='raio', type=float, required=True)
    p.add_argument('--factor', dest='fator', type=int, default=1)
    p.add_argument('--ss', type=int, default=3)
    a = p.parse_args()
    img, pad = aplicar(Image.open(a.cena).convert('RGB'), Image.open(a.arte).convert('RGB'),
                       a.caixa, a.corpo, a.centro, a.raio, a.fator, a.ss)
    img.save(a.saida, quality=97, subsampling=0)
    print(a.saida, img.size, 'white margin (artwork px):', round(pad, 1))


if __name__ == '__main__':
    main()
