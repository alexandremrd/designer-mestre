#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
img_qa.py - Motor autonomo de QA visual do /designer-mestre.
Nao exige instalacao de programas externos: funciona com Playwright/Chromium da IDE,
Pillow ou Python puro (stdlib), usando binarios do sistema apenas se ja existirem.

Comandos:
  prancha   PNGs -> uma folha de conferencia (lado <= 540 px)
  paridade  previa aprovada x screenshot do Figma -> RMSE + mapa de diferencas
  paleta    N cores dominantes (HEX + %) de foto/logo/referencia
  contraste razao WCAG entre dois HEX (passa 4.5 / 3.0?)
  bbox      recorta logo/PNG pelo conteudo (trim) sem redimensionar
  web       exporta WebP/AVIF leve para LP (sem metadados)
"""
import argparse, base64, glob, math, os, re, shutil, subprocess, sys


def expand(pats):
    out = []
    for p in pats:
        # escapa a pasta: o "[TIPO]" das pastas de entrega vira classe de caracteres no glob e não casa nada
        out += sorted(glob.glob(os.path.join(glob.escape(os.path.dirname(p)), os.path.basename(p)))) or [p]
    return [p for p in out if os.path.isfile(p)]


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


def _pw_eval(js_body, args_dict):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        res = pg.evaluate(f"async (a) => {{ {js_body} }}", args_dict)
        b.close()
        return res


def _data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".svg": "image/svg+xml"}.get(ext, "image/png")
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def _save_data_uri(uri, out):
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    raw = uri.split(",", 1)[1] if "," in uri else uri
    with open(out, "wb") as f:
        f.write(base64.b64decode(raw))


def cmd_prancha(a):
    files = expand(a.arquivos)
    if not files:
        sys.exit("[erro] nenhum arquivo encontrado")
    cols = a.colunas or min(4, len(files))
    items = [{"name": os.path.basename(f), "src": _data_uri(f)} for f in files]
    js = """
    const imgs = await Promise.all(a.items.map(it => new Promise((res) => {
        const im = new Image(); im.onload = () => res({im, name: it.name}); im.src = it.src;
    })));
    const s = a.lado, pad = 16, labelH = 26, cols = a.cols, rows = Math.ceil(imgs.length / cols);
    const c = document.createElement('canvas');
    c.width = cols * (s + pad) + pad;
    c.height = rows * (s + labelH + pad) + pad;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#E9E9E9'; ctx.fillRect(0, 0, c.width, c.height);
    ctx.font = '14px sans-serif'; ctx.textAlign = 'center';
    imgs.forEach((it, idx) => {
        const col = idx % cols, row = Math.floor(idx / cols);
        const x = pad + col * (s + pad), y = pad + row * (s + labelH + pad);
        const sc = Math.min(1, s / Math.max(it.im.width, it.im.height));
        const w = Math.round(it.im.width * sc), h = Math.round(it.im.height * sc);
        ctx.fillStyle = '#FFFFFF'; ctx.fillRect(x, y, s, s);
        ctx.drawImage(it.im, x + Math.round((s - w)/2), y + Math.round((s - h)/2), w, h);
        ctx.fillStyle = '#191919'; ctx.fillText(it.name.slice(0, 28), x + s/2, y + s + 18);
    });
    return c.toDataURL('image/jpeg', 0.88);
    """
    uri = _pw_eval(js, {"items": items, "lado": a.lado, "cols": cols})
    _save_data_uri(uri, a.out)
    print(f"[ok] {a.out}  ({len(files)} pecas)")


def cmd_paridade(a):
    diff = a.diff or os.path.splitext(a.previa)[0] + "_diff.png"
    js = """
    const load = src => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = src; });
    const [i1, i2] = await Promise.all([load(a.u1), load(a.u2)]);
    if (i1.width !== i2.width || i1.height !== i2.height) return {dif: [i1.width, i1.height, i2.width, i2.height]};
    const w = i1.width, h = i1.height;
    const c1 = document.createElement('canvas'), c2 = document.createElement('canvas'), cd = document.createElement('canvas');
    c1.width = c2.width = cd.width = w; c1.height = c2.height = cd.height = h;
    const x1 = c1.getContext('2d'), x2 = c2.getContext('2d'), xd = cd.getContext('2d');
    x1.drawImage(i1, 0, 0, w, h); x2.drawImage(i2, 0, 0, w, h);
    const d1 = x1.getImageData(0, 0, w, h).data, d2 = x2.getImageData(0, 0, w, h).data;
    const out = xd.createImageData(w, h);
    let sumSq = 0, n = w * h * 3;
    for (let i = 0; i < d1.length; i += 4) {
        const dr = (d1[i] - d2[i]) / 255, dg = (d1[i+1] - d2[i+1]) / 255, db = (d1[i+2] - d2[i+2]) / 255;
        sumSq += dr*dr + dg*dg + db*db;
        const err = Math.max(Math.abs(d1[i]-d2[i]), Math.abs(d1[i+1]-d2[i+1]), Math.abs(d1[i+2]-d2[i+2]));
        if (err > 12) { out.data[i] = 229; out.data[i+1] = 9; out.data[i+2] = 20; out.data[i+3] = 255; }
        else { out.data[i] = d1[i]; out.data[i+1] = d1[i+1]; out.data[i+2] = d1[i+2]; out.data[i+3] = 65; }
    }
    xd.putImageData(out, 0, 0);
    return {rmse: Math.sqrt(sumSq / n), diffUri: cd.toDataURL('image/png')};
    """
    res = _pw_eval(js, {"u1": _data_uri(a.previa), "u2": _data_uri(a.figma)})
    if "dif" in res:  # esticar uma imagem esconderia a diferenca real
        d = res["dif"]
        print(f"[falha] tamanhos diferentes {d[0]}x{d[1]} vs {d[2]}x{d[3]}")
        sys.exit(2)
    _save_data_uri(res["diffUri"], diff)
    val = float(res["rmse"])
    ok = val <= a.limite
    print(f"[{'ok' if ok else 'DIFERENTE'}] RMSE normalizado {val:.4f} (limite {a.limite}) · mapa: {diff}")
    sys.exit(0 if ok else 2)


def cmd_paleta(a):
    js = """
    const im = await new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = a.u; });
    const c = document.createElement('canvas'); c.width = 160; c.height = 160;
    const ctx = c.getContext('2d'); ctx.drawImage(im, 0, 0, 160, 160);
    const d = ctx.getImageData(0, 0, 160, 160).data;
    const counts = {}; let tot = 0;
    for (let i = 0; i < d.length; i += 4) {
        if (d[i+3] < 128) continue;
        const r = Math.min(255, Math.round(d[i]/16)*16), g = Math.min(255, Math.round(d[i+1]/16)*16), b = Math.min(255, Math.round(d[i+2]/16)*16);
        const hx = '#' + [r,g,b].map(x => x.toString(16).padStart(2,'0')).join('').toUpperCase();
        counts[hx] = (counts[hx] || 0) + 1; tot++;
    }
    return Object.entries(counts).sort((x,y) => y[1]-x[1]).slice(0, a.n).map(([hx, c]) => [hx, 100*c/(tot||1)]);
    """
    rows = _pw_eval(js, {"u": _data_uri(a.imagem), "n": a.n})
    for hx, pct in rows:
        print(f"{hx}  {pct:5.1f}%")


def cmd_bbox(a):
    out = a.out or os.path.splitext(a.imagem)[0] + "_trim.png"
    js = """
    const im = await new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = a.u; });
    const w = im.width, h = im.height, c = document.createElement('canvas'); c.width = w; c.height = h;
    const ctx = c.getContext('2d'); ctx.drawImage(im, 0, 0);
    const d = ctx.getImageData(0, 0, w, h).data;
    const br = d[0], bg = d[1], bb = d[2], ba = d[3], tol = a.fuzz * 2.55;
    const isBg = (i) => ba < 10 ? d[i+3] < 10 : (Math.abs(d[i]-br)<=tol && Math.abs(d[i+1]-bg)<=tol && Math.abs(d[i+2]-bb)<=tol && Math.abs(d[i+3]-ba)<=tol);
    let x0 = w, y0 = h, x1 = 0, y1 = 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        if (!isBg((y*w + x)*4)) { if (x < x0) x0 = x; if (y < y0) y0 = y; if (x > x1) x1 = x; if (y > y1) y1 = y; }
    }
    if (x1 < x0) { x0 = 0; y0 = 0; x1 = w - 1; y1 = h - 1; }
    const tw = x1 - x0 + 1, th = y1 - y0 + 1, co = document.createElement('canvas'); co.width = tw; co.height = th;
    co.getContext('2d').drawImage(c, x0, y0, tw, th, 0, 0, tw, th);
    return {w: tw, h: th, uri: co.toDataURL('image/png')};
    """
    res = _pw_eval(js, {"u": _data_uri(a.imagem), "fuzz": a.fuzz})
    _save_data_uri(res["uri"], out)
    print(f"[ok] {out}  bbox {res['w']}x{res['h']}")


def cmd_web(a):
    base = os.path.splitext(a.imagem)[0]
    js = """
    const im = await new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = a.u; });
    const sc = Math.min(1, a.w / im.width), w = Math.round(im.width * sc), h = Math.round(im.height * sc);
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    c.getContext('2d').drawImage(im, 0, 0, w, h);
    return c.toDataURL('image/webp', 0.82);
    """
    uri = _pw_eval(js, {"u": _data_uri(a.imagem), "w": a.largura})
    out = f"{base}.webp"
    if os.path.normcase(os.path.abspath(out)) == os.path.normcase(os.path.abspath(a.imagem)):
        out = f"{base}_otim.webp"  # entrada ja e .webp: nunca sobrescrever o original
    _save_data_uri(uri, out)
    print(f"[ok] {out}  {os.path.getsize(out) // 1024} KB")


def main():
    ap = argparse.ArgumentParser(description="Motor autonomo de QA visual /designer-mestre")
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
