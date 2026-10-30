#!/usr/bin/env python3
"""Safe zone (R7): contact sheet of frames every 0.25 s with the box drawn + automatic alert on the margins.

Usage: tools/safe-zone.py <video 1080x1920> [--profile reels|anuncio] [--step 0.25] [--output folder]
      [--camera camera-only-video.mp4]
Output: <output>/safe-zone.png (contact sheet with the box) and <output>/safe-zone.json with the suspect
moments. The alert compares, in the strips outside the box, the edge density of the final video with that of the
camera-only video (if --camera is given) or with a fixed threshold; it only points out WHERE to look, the final decision is visual.
Profiles: reels = x 90–990, y 220–1520, and button column x>940 & y>1150 forbidden; anuncio = x 65–1015, y 270–1248.
"""
import argparse, json, os, subprocess, sys, tempfile
import numpy as np
try: import cv2
except ImportError: sys.exit("needs opencv: python3 -m pip install opencv-python-headless numpy")

PERFIS = {"reels": {"x": (90, 990), "y": (220, 1520), "botoes": (940, 1150)}, "anuncio": {"x": (65, 1015), "y": (270, 1248), "botoes": None}}

def quadros(video, passo, d):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", f"fps=1/{passo},scale=1080:1920", os.path.join(d, "q-%04d.png")], check=True)
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.startswith("q-"))

def densidade(img, caixa, botoes):
    g = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 80, 160) > 0
    h, w = g.shape; mask = np.ones_like(g, dtype=bool)
    mask[caixa["y"][0]:caixa["y"][1], caixa["x"][0]:caixa["x"][1]] = False  # inside the box does not matter
    fora = g & mask
    val = {"topo": fora[:caixa["y"][0]].mean(), "base": fora[caixa["y"][1]:].mean(), "esq": fora[:, :caixa["x"][0]].mean(), "dir": fora[:, caixa["x"][1]:].mean()}
    if botoes: val["botoes"] = g[botoes[1]:, botoes[0]:].mean()
    return {k: float(round(v, 4)) for k, v in val.items()}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--profile", dest="perfil", default="reels", choices=PERFIS); ap.add_argument("--step", dest="passo", type=float, default=0.25); ap.add_argument("--output", dest="saida"); ap.add_argument("--camera"); ap.add_argument("--threshold", dest="limiar", type=float, default=0.012)
    a = ap.parse_args(); caixa = PERFIS[a.perfil]; saida = a.saida or os.path.dirname(os.path.abspath(a.video)); os.makedirs(saida, exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        qs = quadros(a.video, a.passo, d); cam = quadros(a.camera, a.passo, os.path.join(d, "c")) if a.camera and os.makedirs(os.path.join(d, "c"), exist_ok=True) is None else []
        suspeitos, tiles = [], []
        for k, q in enumerate(qs):
            img = cv2.imread(q); t = round(k * a.passo, 2); dv = densidade(img, caixa, caixa["botoes"])
            ref = densidade(cv2.imread(cam[k]), caixa, caixa["botoes"]) if k < len(cam) else None
            alerta = [z for z, v in dv.items() if (v - (ref[z] if ref else 0)) > a.limiar]
            if alerta: suspeitos.append({"t": t, "zonas": alerta, "densidade": dv})
            cv2.rectangle(img, (caixa["x"][0], caixa["y"][0]), (caixa["x"][1], caixa["y"][1]), (0, 255, 120), 4)
            if caixa["botoes"]: cv2.rectangle(img, (caixa["botoes"][0], caixa["botoes"][1]), (1080, 1920), (0, 80, 255), 4)
            if alerta: cv2.rectangle(img, (0, 0), (1079, 1919), (0, 0, 255), 18)
            cv2.putText(img, f"{t:.2f}s" + (" !" + ",".join(alerta) if alerta else ""), (24, 80), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 255), 6)
            tiles.append(cv2.resize(img, (270, 480)))
        col = 8; linhas = [np.hstack(tiles[i:i + col] + [np.zeros((480, 270, 3), np.uint8)] * (col - len(tiles[i:i + col]))) for i in range(0, len(tiles), col)]
        cv2.imwrite(os.path.join(saida, "safe-zone.png"), np.vstack(linhas))
    json.dump({"perfil": a.perfil, "passo": a.passo, "quadros": len(qs), "suspeitos": suspeitos}, open(os.path.join(saida, "safe-zone.json"), "w"), indent=1)
    print(f"{len(qs)} frames · {len(suspeitos)} suspects → {saida}/safe-zone.png" + ("" if not suspeitos else f" · look at: {[s['t'] for s in suspeitos][:12]}"))
    sys.exit(1 if suspeitos else 0)

if __name__ == "__main__": main()
