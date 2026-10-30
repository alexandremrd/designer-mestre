#!/usr/bin/env python3
"""Finds the time of a phrase (or word) in palavras.json: every element entry is anchored to speech.

Usage: tools/anchors.py <folder with palavras.json> "exact phrase" ["another phrase" ...] [--n 1] [--end] [--json]
  Prints the start (or the end, with --end) of the Nth occurrence of the phrase, in seconds. Error (exit 2) if the
  phrase does not exist: never guess a time. Compares ignoring accents, case or punctuation.
  With --json prints {"frase": {"i":…, "f":…, "palavras": […]}} for all the requested phrases.
In code (style generator): `from ancoras import Ancoras; A = Ancoras("preparo"); t = A.at("três ferramentas")`.
"""
import argparse, json, os, re, sys, unicodedata

def norm(s): return re.sub(r"[^\w ]", "", unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()).split()

class Ancoras:
    def __init__(self, pasta_ou_arquivo):
        arq = pasta_ou_arquivo if pasta_ou_arquivo.endswith(".json") else os.path.join(pasta_ou_arquivo, "palavras.json")
        self.pal = json.load(open(arq, encoding="utf-8")); self.tok = [norm(p["t"])[0] if norm(p["t"]) else "" for p in self.pal]
    def achar(self, frase, n=1):
        alvo = norm(frase); k = 0
        if not alvo: raise ValueError("empty phrase")
        for i in range(len(self.tok) - len(alvo) + 1):
            if self.tok[i:i + len(alvo)] == alvo:
                k += 1
                if k == n: ps = self.pal[i:i + len(alvo)]; return {"i": ps[0]["i"], "f": ps[-1]["f"], "palavras": ps}
        raise LookupError(f"phrase not found in the speech: {frase!r} (occurrence {n})")
    def at(self, frase, n=1): return self.achar(frase, n)["i"]
    def fim(self, frase, n=1): return self.achar(frase, n)["f"]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("pasta"); ap.add_argument("frases", nargs="+"); ap.add_argument("--n", type=int, default=1); ap.add_argument("--end", dest="fim", action="store_true"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args(); A = Ancoras(a.pasta); out = {}
    for fr in a.frases:
        try: out[fr] = A.achar(fr, a.n)
        except LookupError as e: print(f"ERROR: {e}", file=sys.stderr); sys.exit(2)
    if a.json: print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        for fr, r in out.items(): print(f"{(r['f'] if a.fim else r['i']):.3f}\t{fr}")

if __name__ == "__main__": main()
