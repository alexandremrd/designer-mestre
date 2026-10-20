#!/usr/bin/env python3
"""QA estático de deck HTML 1600x900 (deck.md §4). Uso: python validate_deck.py deck.html
Sai 1 se houver ERRO. Só stdlib."""
import re, sys
from html.parser import HTMLParser
from pathlib import Path

META = re.compile(r"\b(neste slide|nesta apresenta[cç][aã]o|como podemos ver|a seguir veremos|prompt|intelig[eê]ncia artificial)\b", re.I)
DASH = re.compile(r"[–—~]| - ")


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.stack = []; s.slides = []; s.li = []; s.ext = []; s.text = []; s.para = []
        s.in_skip = 0; s.cur_p = None; s.cur_li = None

    def handle_starttag(s, t, a):
        a = dict(a); s.stack.append(t)
        if t in ("script", "style"): s.in_skip += 1
        cls = a.get("class", "") or ""
        if t == "section" and "slide" in cls.split(): s.slides.append(cls)
        if t == "li": s.cur_li = {"svg": False, "line": s.getpos()[0]}; s.li.append(s.cur_li)
        if t == "svg" and s.cur_li is not None: s.cur_li["svg"] = True
        if t == "p": s.cur_p = []
        for k in ("src", "href"):
            v = a.get(k, "")
            if t in ("img", "script", "link", "image") and v and re.match(r"https?://", v) and "fonts.g" not in v:
                s.ext.append((s.getpos()[0], v[:80]))

    def handle_endtag(s, t):
        if t in ("script", "style"): s.in_skip = max(0, s.in_skip - 1)
        if t == "li": s.cur_li = None
        if t == "p" and s.cur_p is not None: s.para.append((s.getpos()[0], " ".join(s.cur_p).strip())); s.cur_p = None
        if s.stack: s.stack.pop()

    def handle_data(s, d):
        if s.in_skip or not d.strip(): return
        s.text.append((s.getpos()[0], d))
        if s.cur_p is not None: s.cur_p.append(d.strip())


def main(path):
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    p = P(); p.feed(raw)
    err, warn = [], []
    for ln, t in p.text:
        if DASH.search(t): err.append(f"L{ln} travessão/til/hífen solto: {t.strip()[:60]!r}")
        if META.search(t): err.append(f"L{ln} metalinguagem: {t.strip()[:60]!r}")
    err += [f"L{x['line']} <li> sem ícone SVG" for x in p.li if not x["svg"]]
    err += [f"L{ln} asset externo não embutido: {u}" for ln, u in p.ext]
    for need, msg in (("fitDeck", "sem fitDeck()"), ("visualViewport", "escala sem visualViewport"),
                      ("progress-fill", "sem .progress-fill"), ("prev-slide", "sem botão prev-slide"),
                      ("next-slide", "sem botão next-slide"), ("prefers-reduced-motion", "sem prefers-reduced-motion")):
        if need not in raw: err.append(msg)
    if not p.slides: err.append("nenhum <section class=\"slide\">")
    warn += [f"L{ln} parágrafo com {len(t)} caracteres (> 230)" for ln, t in p.para if len(t) > 230]
    bg = [next((c for c in ("hero", "depth", "spotlight") if c in c_.split()), "base") for c_ in p.slides]
    for i in range(2, len(bg)):
        if bg[i] == bg[i - 1] == bg[i - 2]: warn.append(f"slides {i-1}-{i+1}: 3 fundos '{bg[i]}' seguidos")
    print(f"{len(p.slides)} slides · {len(err)} ERRO · {len(warn)} AVISO")
    for e in err: print("ERRO ", e)
    for w in warn: print("AVISO", w)
    return 1 if err else 0


if __name__ == "__main__":
    if len(sys.argv) != 2: sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
