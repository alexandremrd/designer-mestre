"""Turn a word into one SVG path with overlapping contours unioned.

Why: `-webkit-text-stroke` and `<text>` strokes draw every internal contour of a glyph
(overlaps in the "a", "k", italics), and clipped pseudo-elements cut italic overhangs.
A unioned path strokes only the outer outline and can take an SVG gradient for a shine.

Usage:
  python text_to_svg_path.py --font Font-Italic.ttf --text Black [--tracking -0.04] [--out path.json]
Prints the viewBox and the path `d` (y axis already flipped, baseline at y=0); with --out
writes {"d": ..., "viewBox": "x y w h", "bounds": [...]}.
Needs: pip install fonttools skia-pathops
"""
import argparse
import json
import sys

from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from pathops import Path, PathPen


def num(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def build(font_path, text, tracking_em=0.0, pad=12):
    f = TTFont(font_path)
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f['head'].unitsPerEm
    path = Path()
    pen = PathPen(path)
    x = 0.0
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
        x += gs[g].width + tracking_em * upm
    path.simplify(fix_winding=True)
    rec = RecordingPen()
    path.draw(rec)
    d = []
    for op, args in rec.value:
        if op == 'moveTo':
            d.append('M%s %s' % (num(args[0][0]), num(args[0][1])))
        elif op == 'lineTo':
            d.append('L%s %s' % (num(args[0][0]), num(args[0][1])))
        elif op == 'qCurveTo':
            pts = list(args)
            for i in range(len(pts) - 1):
                a = pts[i]
                e = ((a[0] + pts[i + 1][0]) / 2, (a[1] + pts[i + 1][1]) / 2) if i < len(pts) - 2 else pts[-1]
                d.append('Q%s %s %s %s' % (num(a[0]), num(a[1]), num(e[0]), num(e[1])))
        elif op == 'curveTo':
            d.append('C' + ' '.join('%s %s' % (num(q[0]), num(q[1])) for q in args))
        elif op in ('closePath', 'endPath'):
            d.append('Z')
    x0, y0, x1, y1 = path.bounds
    vb = '%s %s %s %s' % (num(x0 - pad), num(y0 - pad), num(x1 - x0 + 2 * pad), num(y1 - y0 + 2 * pad))
    return {'d': ''.join(d), 'viewBox': vb, 'bounds': [x0, y0, x1, y1]}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--font', required=True)
    ap.add_argument('--text', required=True)
    ap.add_argument('--tracking', type=float, default=0.0, help='letter spacing in em, e.g. -0.04')
    ap.add_argument('--out')
    a = ap.parse_args()
    r = build(a.font, a.text, a.tracking)
    if a.out:
        json.dump(r, open(a.out, 'w'))
    print('viewBox', r['viewBox'], '| path chars', len(r['d']))
    if not a.out:
        sys.stdout.write(r['d'] + '\n')
