#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
resources.py - Single registry of the local resource paths of /designer-mestre.

Everything the skill runs on the PC (generators, tools, models, caches) lives in a root folder chosen by the
user, separated by category. The scripts ask for the path here, instead of keeping a fixed path, so that
moving or renaming the root (local_engine.py organize) breaks nothing. The registry lives in
%USERPROFILE%\\.designer-mestre\\local_engine.json, which skill updates do not erase.

  python resources.py            (shows the root, categories and where each resource is)
"""
import json, os

CFG = os.path.join(os.path.expanduser("~"), ".designer-mestre", "local_engine.json")
# config written before the English rename: adopt it once so the resource root is not lost
_CFG_OLD = os.path.join(os.path.dirname(CFG), "motor_local.json")
if not os.path.exists(CFG) and os.path.exists(_CFG_OLD):
    os.replace(_CFG_OLD, CFG)

# key -> subfolder inside the root. Categories: Geradores (create image, 3D, video), Ferramentas (support:
# browser, converters, libraries), Modelos (weights used by more than one script), Cache (reusable downloads).
PADRAO = {
    "comfyui": r"Geradores\ComfyUI",
    "blender": r"Geradores\Blender",
    "playwright": r"Ferramentas\playwright",
    "node": r"Ferramentas\node",
    "designlang": r"Ferramentas\designlang",
    "ffmpeg": r"Ferramentas\ffmpeg",
    "whisper": r"Modelos\whisper",
    "whisper_cpp": r"Ferramentas\whisper.cpp",
    "whisper_cpp_cuda": r"Ferramentas\whisper.cpp-cuda",
    "chrome": r"Ferramentas\chrome",
    "cache_uv": r"Cache\uv",
    "cache_npm": r"Cache\npm",
}
CATEGORIAS = ("Geradores", "Ferramentas", "Modelos", "Cache")


def cfg():
    try:
        return json.load(open(CFG, encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {}


def raiz():
    return cfg().get("motores")


def caminho(chave):
    """Registered path of the resource; without a registration, the default place inside the root (or None without a root)."""
    c = cfg()
    if c.get("caminhos", {}).get(chave):
        return c["caminhos"][chave]
    if chave == "comfyui" and c.get("pasta"):
        return c["pasta"]
    return os.path.join(c["motores"], PADRAO[chave]) if c.get("motores") else None


def existe(chave):
    p = caminho(chave)
    return p if p and os.path.exists(p) else None


def aplicar_env():
    """Points the current process (and its children) to the root's resources. Does not touch Windows variables."""
    pw = existe("playwright")
    if pw and not os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = pw
    ff = existe("ffmpeg")
    if ff:
        bin_ff = os.path.join(ff, "bin") if os.path.isdir(os.path.join(ff, "bin")) else ff
        os.environ["PATH"] = bin_ff + os.pathsep + os.environ.get("PATH", "")
    # engine of the reel module (modules\video.md): whisper.cpp ggml model and Chrome
    wm = existe("whisper")
    if wm and not os.environ.get("WHISPER_MODEL"):
        for f in sorted(os.listdir(wm)):
            if f.startswith("ggml-") and f.endswith(".bin"):
                os.environ["WHISPER_MODEL"] = os.path.join(wm, f)
                break
    ch = existe("chrome")
    if ch and not os.environ.get("CHROME"):
        for cand in ("chrome.exe", os.path.join("chrome-win64", "chrome.exe")):
            if os.path.isfile(os.path.join(ch, cand)):
                os.environ["CHROME"] = os.path.join(ch, cand)
                break


# ---------------------------------------------------------------- catalog: what it is, what it is for and where the skill uses it
# Rule (operations.md §0.6): every resource lives in the root above and, before downloading or installing, the user gets the context from `explain` and gives the yes.
# `size` is only filled in when known; without it, check the size at the source before asking.
CATALOGO = {
    "ffmpeg": ("ffmpeg", "cut, caption, encode and measure video and audio", "video.md, caption_reels.py, assemble_reels.py, export_motion.py", "gyan.dev (official Windows build)", None),
    "playwright": ("Playwright Chromium", "render pages and animated pieces and take the check screenshots", "html.md, video.md, check_html.py, render_frames.py", "playwright.dev", None),
    "node": ("Node.js", "run the JavaScript scripts: direction draw, free photos, image treatment and designlang", "ads.md, html.md, treat_image.mjs", "nodejs.org", None),
    "designlang": ("designlang", "extract colors, fonts and scale from a live site", "html.md §6.4, ads.md §2", "github.com/Manavarya09/design-extract (MIT)", None),
    "whisper": ("Transcription models (faster-whisper)", "transcribe speech into captions, with per-word timing, on the GPU", "caption_reels.py (--model auto picks the largest installed)", "huggingface.co (Systran and mobiuslabsgmbh)", "small ~0.5 GB · medium ~1.5 GB · large-v3-turbo ~1.6 GB"),
    "whisper_cpp_cuda": ("whisper.cpp with CUDA (the ggml-large-v3-turbo model lives in Modelos\\whisper)", "GPU transcription for the reel cut engine and alternative route for captions", "video.md §2, run_reel_cut.ps1, caption_reels.py --whisper-engine cpp", "github.com/ggml-org/whisper.cpp and huggingface.co/ggerganov/whisper.cpp", None),
    "comfyui": ("ComfyUI + FLUX.2 klein 4B", "generate and edit images on your graphics card (local engine), with no per-image cost", "image.md Part A, generate_image.py, local_engine.py", "github.com/comfyanonymous/ComfyUI and huggingface.co/black-forest-labs", None),
    "blender": ("Blender", "deterministic 3D render: spin, exploded view and product cutout", "image-product.md §4", "blender.org", None),
    "chrome": ("Google Chrome", "browser of the reel kit (HyperFrames) when the Playwright Chromium will not do", "video.md §6 mode A", "google.com/chrome", None),
}


def _tamanho(p):
    """Human-readable size of a file or folder (or None)."""
    if not p or not os.path.exists(p):
        return None
    if os.path.isfile(p):
        total = os.path.getsize(p)
    else:
        total = 0
        for d, _, fs in os.walk(p):
            for f in fs:
                try:
                    total += os.path.getsize(os.path.join(d, f))
                except OSError:
                    pass
    return f"{total / 1024 ** 3:.1f} GB" if total >= 1024 ** 3 else f"{total / 1024 ** 2:.0f} MB"


def explicar(chave):
    """The 3-part context the user gets before a download: what (and the size), what for and where it goes. Short on purpose."""
    nome, para_que, usado, origem, tam = CATALOGO[chave]
    dest = caminho(chave) or "(set the root: local_engine.py engines --folder <path>)"
    if existe(chave):
        return f"{nome} is already in {dest} ({_tamanho(dest)}); nothing to download."
    peso = tam or "check the size at the source before asking"
    return (f"I need to download **{nome}** ({peso}, from {origem}). It is for {para_que}; the skill uses it in {usado}. "
            f"It goes to `{dest}`. May I download it?")


def fora_da_raiz():
    """Skill resources that ended up outside the root (e.g. the Hugging Face cache in the user's profile). Only lists; never deletes."""
    achados = []
    home = os.path.expanduser("~")
    hf = os.path.join(home, ".cache", "huggingface", "hub")
    if os.path.isdir(hf):
        for nome in os.listdir(hf):
            if "whisper" in nome.lower():
                achados.append((os.path.join(hf, nome), "whisper"))
    pcpp = os.path.join(home, ".cache", "whisper-cpp")
    if os.path.isdir(pcpp):
        achados.append((pcpp, "whisper"))
    return achados


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "explain" and len(sys.argv) > 2 and sys.argv[2] in CATALOGO:
        print(explicar(sys.argv[2]))
    elif cmd == "catalog":
        print(f"root: {raiz() or 'not set'}")
        for k, (nome, para_que, usado, origem, tam) in CATALOGO.items():
            p = existe(k)
            print(f"  {'[ok] ' if p else '[missing]'} {nome} ({_tamanho(p) or tam or 'size to be confirmed'}): {para_que}")
    elif cmd == "outside":
        achados = fora_da_raiz()
        if not achados:
            print("Nothing from the skill outside the root.")
        for p, chave in achados:
            ja = os.path.exists(os.path.join(caminho(chave) or "", os.path.basename(p)))
            print(f"outside the root: {p} ({_tamanho(p)}); " + (f"already copied to {caminho(chave)}: the original only takes up space and deleting it is up to you." if ja else f"destination: {caminho(chave)}. Copy it there; deleting the original is up to you."))
    else:
        print(f"root: {raiz() or 'not set (local_engine.py engines --folder <path>)'}")
        for k in PADRAO:
            p = caminho(k)
            print(f"  {k:17} {p or '-'}  {'(ok)' if p and os.path.exists(p) else '(absent)'}")
        print("  commands: catalog (what each resource is) · explain <key> (download question) · outside (what ended up outside the root)")
