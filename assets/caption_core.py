#!/usr/bin/env python3
"""caption_core.py - the caption engine shared by `caption_reels.py` (any video) and `reel_assembly/assemble_reels.py`
(video inside the client's Reels template). One place for: grouping words into caption blocks, splitting a block into
1 or 2 lines, ASS colors and times, and the ASS document. The reel engine's `K.mouthCaps` (mode A, kit untouched) is the
third caption path; it renders in the browser and does not use this module.

Words are dicts {"s": start_s, "e": end_s, "t": text}.
"""
import re

PUNCT_ALL = r"[.!?,;:]$"  # caption_reels: any punctuation closes a block
PUNCT_SHORT = r"[.,?]$"   # assemble_reels: the template's original rule


def group(words, max_words, max_chars=None, punct=PUNCT_ALL, pause=0.35):
    """Blocks of consecutive words. A block closes at `max_words`, at `max_chars` characters, at closing punctuation,
    or before a pause longer than `pause` s (None = ignore pauses)."""
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        texto = " ".join(x["t"] for x in cur)
        fim_frase = re.search(punct, w["t"])
        pausa = pause is not None and i + 1 < len(words) and words[i + 1]["s"] - w["e"] > pause
        if len(cur) >= max_words or (max_chars and len(texto) >= max_chars) or fim_frase or pausa:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def split_lines(parts, lines=1, plain=None):
    """Joins the parts of a block. With lines=2, breaks (ASS `\\N`) where the two lines come out closest in length;
    `plain` = the parts without ASS tags, used to measure (defaults to `parts`)."""
    if lines < 2 or len(parts) < 2:
        return " ".join(parts)
    plain = plain or parts
    corte = min(range(1, len(plain)), key=lambda i: (abs(len(" ".join(plain[:i])) - len(" ".join(plain[i:]))), -i))
    return " ".join(parts[:corte]) + "\\N" + " ".join(parts[corte:])


def ass_color(hexc, alpha="00"):
    """#RRGGBB -> ASS &HAABBGGRR (blue-green-red order)."""
    h = hexc.lstrip("#")
    return f"&H{alpha}{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def ass_time(t):
    """Seconds -> ASS H:MM:SS.cc."""
    cs = int(round(t * 100)); h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h}:{m:02}:{s:02}.{cs:02}"


def srt_time(t):
    """Seconds -> SRT HH:MM:SS,mmm."""
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def escape(t):
    """Text safe inside an ASS event (no override braces, no backslash)."""
    return t.replace("\\", "").replace("{", "(").replace("}", ")")
