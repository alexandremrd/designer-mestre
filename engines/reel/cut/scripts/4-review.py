"""Step 4 — mandatory check of the cut (never deliver without running it and READING the output).

1. full transcription of the cut, word by word (becomes the basis of the captions: cut_words.json);
2. each SPLICE transcribed on its own in a ±2 s window — that is where mumbled restarts,
   duplicated "então" and half words that the long transcription hides show up;
3. automatic hunt for glued repetition (same word/expression of 1 to 4 words twice in a row);
4. leftover pauses (> 0.25 s below the speech threshold).

usage:  python3 4-review.py FOLDER [--prompt "proper names in the video"]
output: FOLDER/cut_words.json, FOLDER/review.txt (and the same on screen)
"""
import json, os, subprocess, sys, unicodedata
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from common import palavras, recorte, texto, PROMPT_NOMES

P = sys.argv[1]
args = sys.argv[2:]
prompt = args[args.index("--prompt") + 1] if "--prompt" in args else PROMPT_NOMES
edl = json.load(open(f"{P}/edl.json"))
total = edl[-1]["out"] + edl[-1]["dur"]
rel = []

ws = palavras(f"{P}/cut16k.wav", prompt)
json.dump(ws, open(f"{P}/cut_words.json", "w"), ensure_ascii=False)
rel.append("== CUT TEXT (read it in full) ==\n" + " ".join(t for a, b, t in ws) + "\n")

def nz(s): return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if c.isalnum())
toks = [nz(t) for a, b, t in ws]
rep = []
for k in range(1, 5):
    for i in range(len(toks) - 2 * k + 1):
        if toks[i:i + k] == toks[i + k:i + 2 * k] and any(len(x) > 2 for x in toks[i:i + k]):
            rep.append(f"  {ws[i][0]:6.2f}s  \"{' '.join(t for a, b, t in ws[i:i + 2 * k])}\"")
rel.append("== GLUED REPETITIONS ==\n" + ("\n".join(rep) if rep else "  none") + "\n")

rel.append("== SPLICES (±2 s window, transcribed on its own) ==")
tmp = f"{P}/_jan.wav"
for c in edl[1:]:
    t = c["out"]
    recorte(f"{P}/cut16k.wav", max(0, t - 2), min(total, t + 2), tmp)
    # no prompt: in a short window the fillers prompt makes Whisper INVENT "é, ah, hum"
    rel.append(f"  {t:6.2f}s  (source {c['src']:.2f}) :: {texto(tmp)}")
os.remove(tmp)

r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{P}/cut.wav", "-af", "silencedetect=noise=-38dB:d=0.25",
                    "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
pausas = [l.split("silence_end: ")[1] for l in r.splitlines() if "silence_end" in l]
rel.append("\n== LEFTOVER PAUSES > 0.25 s ==\n" + ("\n".join("  end " + p for p in pausas) if pausas else "  none"))
rel.append(f"\ncut duration: {total:.2f}s")

out = "\n".join(rel) + "\n"
open(f"{P}/review.txt", "w").write(out)
print(out)
