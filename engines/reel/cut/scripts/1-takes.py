"""Step 1 — map of TAKES in the raw footage: where there is speech and what was said in each segment.

Do not trust the word-by-word transcription of the whole video: in long silences Whisper invents text
(repeats the previous sentence) and shifts the timings. Here speech is found by ENERGY and each segment is
transcribed on its own — that is what really shows the restarts, abandoned sentences and false starts.

usage:  python3 1-takes.py VIDEO FOLDER
output: FOLDER/audio16k.wav, FOLDER/takes.json, FOLDER/takes.txt  (read the .txt to choose the keeps)
"""
import json, os, sys, wave
import numpy as np
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from common import audio16k, recorte, texto, PROMPT_VICIOS

VIDEO, P = sys.argv[1], sys.argv[2]
os.makedirs(P, exist_ok=True)
wav = f"{P}/audio16k.wav"
audio16k(VIDEO, wav)

w = wave.open(wav)
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
n = len(x) // 160
db = 20 * np.log10(np.sqrt((x[:n * 160].reshape(n, 160) ** 2).mean(1)) + 1e-9)   # 10 ms
thr = np.percentile(db, 10) + 18          # room noise floor + 18 dB
sp = db > thr

regioes, i = [], 0
while i < n:
    if sp[i]:
        j = i
        while j < n and (sp[j] or sp[j:j + 15].any()):   # merge gaps < 0.15 s
            j += 1
        regioes.append((i / 100, j / 100)); i = j
    else:
        i += 1

linhas, saida = [], []
tmp = f"{P}/_trecho.wav"
for a, b in regioes:
    if b - a < 0.3:
        continue
    a0, b0 = max(0, a - 0.15), b + 0.15
    recorte(wav, a0, b0, tmp)
    t = texto(tmp, PROMPT_VICIOS)
    saida.append({"from": round(a0, 2), "to": round(b0, 2), "texto": t})
    linhas.append(f"{a0:7.2f}-{b0:7.2f} ({b0 - a0:4.1f}s) :: {t}")
    print(linhas[-1], flush=True)
os.remove(tmp)
json.dump(saida, open(f"{P}/takes.json", "w"), ensure_ascii=False, indent=1)
open(f"{P}/takes.txt", "w").write("\n".join(linhas) + "\n")
