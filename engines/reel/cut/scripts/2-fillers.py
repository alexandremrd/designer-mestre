"""Step 2 — transcription that does NOT hide fillers ("éé", "ããã", "hum"), only inside the chosen keeps.

Whisper normally erases hesitations; with a prompt full of them it starts writing them, and the cut
(3-cut.py) can remove each one. Transcribing per keep (not the whole video) avoids invented text
in long silences.

usage:  python3 2-fillers.py FOLDER          (reads FOLDER/keeps.json and FOLDER/audio16k.wav)
output: FOLDER/vicios/k{i}.json  (words with SOURCE time) and the text of each keep on screen
"""
import json, os, sys
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from common import recorte, palavras, PROMPT_VICIOS

P = sys.argv[1]
keeps = json.load(open(f"{P}/keeps.json"))["keeps"]
os.makedirs(f"{P}/vicios", exist_ok=True)
tmp = f"{P}/_keep.wav"
for i, k in enumerate(keeps):
    recorte(f"{P}/audio16k.wav", k["from"], k["to"], tmp)
    ws = palavras(tmp, PROMPT_VICIOS, deslocamento=k["from"])
    json.dump(ws, open(f"{P}/vicios/k{i}.json", "w"), ensure_ascii=False)
    print(f"[{i}] {k['from']:.2f}-{k['to']:.2f} {k.get('why', '')}\n    " +
          " ".join(f"{t}({a:.2f})" for a, b, t in ws) + "\n", flush=True)
os.remove(tmp)
