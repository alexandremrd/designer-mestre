"""Aplica a arte real do rótulo (PDF rasterizado) por cima de um frasco cilíndrico numa cena.

Uso (um slot por chamada; chame de novo sobre a saída para o slot seguinte):
  python aplicar_rotulo.py --cena cena.jpg --arte arte.png --saida saida.jpg \
      --caixa X0 Y0 X1 Y1 --corpo Y0 Y1 --centro CX --raio R [--fator 2] [--ss 3]

--caixa   retângulo do adesivo na cena (px da cena, decimais aceitos), da borda esquerda à direita do frasco
--corpo   linhas da arte plana onde está o corpo do rótulo (sem faixas ou sangria)
--centro  coluna da arte plana que cai no centro frontal do frasco
--raio    raio do cilindro na arte plana (px da arte); a arte é curvada com arcsin nas bordas
--fator   amplia a cena antes (Lanczos); as coordenadas de --caixa continuam as da cena original
--ss      supersampling da máscara e do mapeamento (antisserrilhado das bordas)

Preserva a sombra do frasco: o brilho da área vira mapa de luz (mediana/gauss sem a tinta antiga)
multiplicado na arte. Arte nunca é reescrita por IA. Escala uniforme pelo raio: sem distorção em x/y;
a altura que sobrar é preenchida com branco, não esticada.
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
    k = half / raio                                   # px de cena por px de arte (uniforme)
    pad = ((Y1 - Y0) / k - (SY1 - SY0)) / 2           # respiro branco acima e abaixo do corpo
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
    th = np.arcsin(np.clip((XX - xc) / half, -1, 1))  # curvatura de cilindro
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
    labp = labp * np.clip(luz / 255.0, 0.3, 1.0)[..., None]  # sombra do frasco sobre a arte

    res = sc * (1 - a[..., None]) + labp * a[..., None]
    out = np.asarray(S).astype(float)
    out[yi0:yi1, xi0:xi1] = res
    return Image.fromarray(np.clip(out + 0.5, 0, 255).astype('uint8')), pad


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--cena', required=True)
    p.add_argument('--arte', required=True)
    p.add_argument('--saida', required=True)
    p.add_argument('--caixa', nargs=4, type=float, required=True, metavar=('X0', 'Y0', 'X1', 'Y1'))
    p.add_argument('--corpo', nargs=2, type=float, required=True, metavar=('Y0', 'Y1'))
    p.add_argument('--centro', type=float, required=True)
    p.add_argument('--raio', type=float, required=True)
    p.add_argument('--fator', type=int, default=1)
    p.add_argument('--ss', type=int, default=3)
    a = p.parse_args()
    img, pad = aplicar(Image.open(a.cena).convert('RGB'), Image.open(a.arte).convert('RGB'),
                       a.caixa, a.corpo, a.centro, a.raio, a.fator, a.ss)
    img.save(a.saida, quality=97, subsampling=0)
    print(a.saida, img.size, 'respiro branco (px da arte):', round(pad, 1))


if __name__ == '__main__':
    main()
