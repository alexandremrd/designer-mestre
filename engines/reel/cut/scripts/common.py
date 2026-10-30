"""Shared pieces of the Raw Edit: 16 kHz audio, local Whisper (whisper-cli) and word reading.

Model: environment variable WHISPER_MODEL, or the first one that exists in MODELOS_PADRAO.
"""
import json, os, shutil, subprocess, sys, tempfile

MODELOS_PADRAO = [
    "~/.cache/whisper-cpp/ggml-large-v3-turbo.bin",
    "~/.cache/whisper-cpp/ggml-large-v3.bin",
    "~/.cache/whisper-cpp/ggml-medium.bin",
    "~/whisper.cpp/models/ggml-large-v3-turbo.bin",
]
PROMPT_VICIOS = "Éé, então, ããã, hum, é... tipo, éé, eh, ah, né, ããã, hum. Umm, éé."
PROMPT_NOMES = "Claude, Claude Code, IA, ChatGPT, Instagram, YouTube."   # change per video with --prompt


def modelo():
    m = os.environ.get("WHISPER_MODEL")
    cands = [m] if m else MODELOS_PADRAO
    for c in cands:
        p = os.path.expanduser(c)
        if os.path.exists(p):
            return p
    sys.exit("Whisper model not found. Run 0-check.py to see how to install it, "
             "or set WHISPER_MODEL=/path/ggml-large-v3-turbo.bin")


def _dtw(caminho):
    """Time-alignment preset (DTW) of whisper-cli for the model; None if not recognized."""
    nome = os.path.basename(caminho).replace("ggml-", "").replace(".bin", "")
    nome = nome.split("-q")[0]                           # ggml-large-v3-turbo-q5_0 → large-v3-turbo
    mapa = {"large-v3-turbo": "large.v3.turbo", "large-v3": "large.v3", "large-v2": "large.v2",
            "large-v1": "large.v1", "medium": "medium", "small": "small", "base": "base", "tiny": "tiny"}
    return mapa.get(nome)


def _whisper():
    w = shutil.which("whisper-cli") or shutil.which("whisper-cpp") or shutil.which("main")
    if not w:
        sys.exit("whisper-cli not found. Run 0-check.py to see how to install it.")
    return w


def audio16k(video, wav):
    """Mono 16 kHz for analysis and transcription."""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)


def recorte(wav, a, b, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", wav, out], check=True)


def texto(wav, prompt=None):
    """Running transcription (no timings) — to read what was said in a segment."""
    cmd = [_whisper(), "-m", modelo(), "-f", wav, "-l", "pt", "-nt", "-np"]
    if prompt:
        cmd += ["--prompt", prompt]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return " ".join(r.stdout.split())


def palavras(wav, prompt=None, deslocamento=0.0):
    """Word by word with timings: [(start, end, text)], adding `deslocamento` (offset: time of the segment in the source)."""
    m = modelo()
    with tempfile.TemporaryDirectory() as d:
        base = os.path.join(d, "w")
        cmd = [_whisper(), "-m", m, "-f", wav, "-l", "pt", "-ojf", "-ml", "1", "-sow", "-of", base, "-np"]
        if _dtw(m):
            cmd += ["-dtw", _dtw(m)]
        if prompt:
            cmd += ["--prompt", prompt]
        subprocess.run(cmd, capture_output=True)
        dados = json.load(open(base + ".json", encoding="utf-8"))
    out = []
    for s in dados["transcription"]:
        t = s["text"].strip()
        if t:
            out.append((round(deslocamento + s["offsets"]["from"] / 1000, 3),
                        round(deslocamento + s["offsets"]["to"] / 1000, 3), t))
    return out
