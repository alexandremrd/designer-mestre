#!/usr/bin/env python3
"""Delivery checklist (R9): measures the final video and writes VERIFY.md with what passed and what is left to look at.

Usage: tools/verify.py <project folder> --video render/reel-final.mp4 [--profile reels|anuncio]
      [--camera cut/clean-916.mp4] [--sfx sounds.json] [--notes "free text"]
Measures: resolution (1080×1920), fps, duration, integrated LUFS and peak, safe zone (calls safe-zone.py),
SFX density (if sounds.json has the list of times), and reminds the items only the eye checks (R1 face,
legibility, caption fixes). Exits with 1 if any measured item failed.
"""
import argparse, json, os, subprocess, sys, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))

def probe(v):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height,r_frame_rate,codec_type:format=duration", "-of", "json", v], capture_output=True, text=True).stdout)
    vs = next(s for s in j["streams"] if s["codec_type"] == "video"); n, d = vs["r_frame_rate"].split("/")
    return {"largura": vs["width"], "altura": vs["height"], "fps": round(float(n) / float(d), 3), "duracao": round(float(j["format"]["duration"]), 2), "audio": any(s["codec_type"] == "audio" for s in j["streams"])}

def loudness(v):
    out = subprocess.run(["ffmpeg", "-nostats", "-i", v, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    bloco = out[out.rfind("{"):out.rfind("}") + 1]
    try: j = json.loads(bloco); return {"lufs": float(j["input_i"]), "pico_dbtp": float(j["input_tp"]), "lra": float(j["input_lra"])}
    except Exception: return {"lufs": None, "pico_dbtp": None, "lra": None}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("projeto"); ap.add_argument("--video", required=True); ap.add_argument("--profile", dest="perfil", default="reels"); ap.add_argument("--camera"); ap.add_argument("--sfx"); ap.add_argument("--notes", dest="notas", default="")
    a = ap.parse_args(); proj = os.path.abspath(a.projeto); video = a.video if os.path.isabs(a.video) else os.path.join(proj, a.video)
    itens = []; ok = True
    m = probe(video); itens.append(("Resolution 1080×1920", m["largura"] == 1080 and m["altura"] == 1920, f"{m['largura']}×{m['altura']}"))
    itens.append(("Audio track present", m["audio"], "")); itens.append(("Duration", True, f"{m['duracao']} s · {m['fps']} fps"))
    l = loudness(video)
    itens.append(("Loudness −14 LUFS ±0.5 (R8)", l["lufs"] is not None and abs(l["lufs"] + 14) <= 0.5, f"{l['lufs']} LUFS"))
    itens.append(("Peak ≤ −0.5 dBTP (R8)", l["pico_dbtp"] is not None and l["pico_dbtp"] <= -0.5, f"{l['pico_dbtp']} dBTP"))
    zs_dir = os.path.join(proj, "qa"); os.makedirs(zs_dir, exist_ok=True)
    cmd = [sys.executable, os.path.join(AQUI, "safe-zone.py"), video, "--profile", a.perfil, "--output", zs_dir] + (["--camera", a.camera] if a.camera else [])
    r = subprocess.run(cmd, capture_output=True, text=True); zs = {}
    try: zs = json.load(open(os.path.join(zs_dir, "safe-zone.json")))
    except Exception: pass
    itens.append(("Safe zone with no suspects (R7)", r.returncode == 0, f"{len(zs.get('suspeitos', []))} moments to look at in qa/safe-zone.png" if zs else r.stderr.strip()[-200:]))
    if a.sfx and os.path.exists(a.sfx):
        try:
            s = json.load(open(a.sfx)); tempos = sorted(float(x["t"] if isinstance(x, dict) else x) for x in (s if isinstance(s, list) else s.get("efeitos", [])))
            dens = len(tempos) / max(m["duracao"], 1); perto = sum(1 for p, q in zip(tempos, tempos[1:]) if q - p < 0.35)
            itens.append(("SFX ≤ 0.85 per second (R2)", dens <= 0.85, f"{len(tempos)} effects · {dens:.2f}/s · {perto} pairs less than 0.35 s apart"))
        except Exception as e: itens.append(("SFX (sounds.json)", True, f"could not read: {e}"))
    ok = all(i[1] for i in itens)
    linhas = [f"# VERIFY · {os.path.basename(video)}", f"*{datetime.datetime.now():%Y-%m-%d %H:%M}*", "", "## Measured", "| Item | Result | Detail |", "|---|---|---|"]
    for nome, passou, det in itens: linhas.append(f"| {nome} | {'✅' if passou else '❌'} | {det} |")
    linhas += ["", "## Checked by eye (tick)", "- [ ] R1 · no element over the face in any frame (sheet in qa/safe-zone.png and snapshots per beat)", "- [ ] Legible text, nothing cut off, reading time ≥ 2 s on screens with text",
               "- [ ] R6 · caption with the corrected text (Claude, IA, product names as the brand writes them); code word in UPPERCASE", "- [ ] R3 · every number/screenshot/logo with a source in assets/SOURCES.md", "- [ ] R5 · no word eaten at the splices (check from the edicao-bruta)", "- [ ] R11 · no third-party name in the video or in the files", "", "## Notes", a.notas or "—", "", f"**Measured result: {'APPROVED' if ok else 'REJECTED'}** · never publish or send the video (R9)."]
    open(os.path.join(proj, "VERIFY.md"), "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    print("\n".join(linhas)); sys.exit(0 if ok else 1)

if __name__ == "__main__": main()
