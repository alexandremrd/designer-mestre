#!/usr/bin/env python3
# caption_reels.py - /designer-mestre v19.55
# Client video -> word-level transcription -> .ass caption in the KV -> PNG overlay -> soundtrack -> endcard -> MP4.
# Dependencies: ffmpeg on PATH or the imageio-ffmpeg package (uv run --with imageio-ffmpeg ...);
# faster-whisper (pip) only if --srt is not given.
# Minimal usage:
#   python caption_reels.py --video in.mp4 --overlay overlay.png --font "EB Garamond" --fontsdir fontes --out final.mp4
# No-rework flow: the 1st run writes <out>.srt for review; if there is a speech error,
# fix the .srt and run again with --srt <out>.srt (skips transcription).
import argparse, json, os, re, shutil, subprocess, sys, tempfile

def achar_ffmpeg():
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg missing: run with  uv run --with imageio-ffmpeg python caption_reels.py ...  "
                 "(or winget install Gyan.FFmpeg)")

FF = achar_ffmpeg()

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit("ffmpeg ERROR:\n" + r.stderr[-2500:])
    return r

def info(path):
    # no ffprobe: imageio-ffmpeg only ships ffmpeg, so read the header from ffmpeg itself
    return subprocess.run([FF, "-hide_banner", "-i", path], capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stderr

def dur(path):
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info(path)).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)

def tem_audio(path):
    return "Audio:" in info(path)

# ---------- transcription ----------
# Two routes, both on the GPU and with the large model (large-v3-turbo):
#   faster = faster-whisper (CTranslate2): per-word timing with voice filter, the most faithful for captions
#   cpp    = whisper.cpp with CUDA (the same engine as the reel cut): per-word timing via 1-word segments
# `--whisper-engine auto` follows ORDEM_AUTO (the order measured on this computer) and falls back to the other route if one fails, stating the reason.
ORDEM_AUTO = ["faster", "cpp"]


def candidatos(modelo, dev):
    """Models to try, from best to minimum. `auto` = the best the GPU sustains and that is already in the resource root;
    the second value True = only if already installed (never downloads a large model without the user's yes)."""
    if modelo != "auto":
        return [(modelo, False)]
    if dev != "cuda":
        return [("small", False)]
    return [("large-v3-turbo", True), ("medium", True), ("small", False)]


def transcrever_faster(video, modelo, idioma):
    try:
        from faster_whisper import WhisperModel
        import numpy as np
    except ImportError:
        raise RuntimeError("faster-whisper missing: pip install faster-whisper")
    # audio decoded by ffmpeg: avoids faster-whisper's PyAV decoder, which breaks between versions
    raw = subprocess.run([FF, "-v", "error", "-i", video, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    erro = None
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import resources  # Whisper models in the resource root
    try:
        import gpu_acceleration
        gpu_acceleration.preparar_cuda()  # CUDA DLLs on the path: without them the GPU would fail and fall back to the CPU
    except Exception:
        pass
    for dev, ct in (("cuda", "float16"), ("cpu", "int8")):
        try:
            m = None
            for nome, so_local in candidatos(modelo, dev):
                try:
                    m = WhisperModel(nome, device=dev, compute_type=ct, download_root=resources.caminho("whisper"), local_files_only=so_local)
                    print(f"[whisper] faster-whisper {nome} on {dev}", flush=True)
                    break
                except Exception as e_modelo:
                    erro = e_modelo
            if m is None:
                raise erro or RuntimeError("no transcription model available")
            segs, _ = m.transcribe(audio, language=idioma, word_timestamps=True, vad_filter=True)
            pal = []
            # the GPU may load the model and fail only here (e.g. cuBLAS missing); that is why the whole loop stays in the try
            for sg in segs:
                for w in sg.words or []:
                    t = w.word.strip()
                    if t:
                        pal.append({"s": round(w.start, 3), "e": round(w.end, 3), "t": t})
            return pal
        except Exception as e:
            erro = e
            print(f"[whisper] {dev} failed ({type(e).__name__}: {str(e)[:160]}); trying the next path", flush=True)
    raise RuntimeError(f"faster-whisper failed on GPU and CPU ({erro})")


def transcrever_cpp(video, idioma):
    """whisper.cpp with CUDA + ggml-large-v3-turbo model from the resource root; returns the same format as faster-whisper."""
    import json, tempfile
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import resources
    pasta = resources.existe("whisper_cpp_cuda")
    modelos = resources.existe("whisper")
    cli = os.path.join(pasta, "whisper-cli.exe") if pasta else None
    ggml = os.path.join(modelos, "ggml-large-v3-turbo.bin") if modelos else None
    if not (cli and os.path.isfile(cli) and ggml and os.path.isfile(ggml)):
        raise RuntimeError("whisper.cpp with CUDA or the ggml-large-v3-turbo model are not in the resource root (python assets\\resources.py explain whisper_cpp_cuda)")
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "a.wav")
        subprocess.run([FF, "-v", "error", "-y", "-i", video, "-ac", "1", "-ar", "16000", wav], check=True)
        base = os.path.join(d, "w")
        cmd = [cli, "-m", ggml, "-f", wav, "-l", idioma or "auto", "-ojf", "-ml", "1", "-sow", "-of", base, "-np"]
        ambiente = dict(os.environ, PATH=pasta + os.pathsep + os.environ.get("PATH", ""))
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=ambiente)
        if r.returncode:
            raise RuntimeError("whisper-cli failed: " + (r.stderr or r.stdout)[-200:])
        dados = json.load(open(base + ".json", encoding="utf-8"))
    pal = []
    for sg in dados.get("transcription", []):
        t = (sg.get("text") or "").strip()
        if t and not (t.startswith("[") and t.endswith("]")):  # drop markers like [MUSICA]
            pal.append({"s": round(sg["offsets"]["from"] / 1000, 3), "e": round(sg["offsets"]["to"] / 1000, 3), "t": t})
    print("[whisper] whisper.cpp (CUDA) large-v3-turbo", flush=True)
    return pal


def transcrever(video, modelo, idioma, motor="auto"):
    ordem = list(ORDEM_AUTO) if motor == "auto" else [motor] + [m for m in ORDEM_AUTO if m != motor]
    erro = None
    for rota in ordem:
        try:
            return transcrever_faster(video, modelo, idioma) if rota == "faster" else transcrever_cpp(video, idioma)
        except Exception as e:
            erro = e
            print(f"[whisper] route {rota} failed ({type(e).__name__}: {str(e)[:160]}); trying the other", flush=True)
    sys.exit(f"Whisper failed on all routes ({erro}). Use --srt or see `python assets\\resources.py explain whisper`.")

def remover(pal, faixas):
    # drop words that start inside the "a-b" (s) ranges: forbidden speech or outside the briefing
    if not faixas:
        return pal
    fx = [tuple(float(x) for x in f.split("-")) for f in faixas]
    return [w for w in pal if not any(a <= w["s"] < b for a, b in fx)]

def ler_srt(path):
    txt = open(path, encoding="utf-8-sig").read()
    pal = []
    for bloco in re.split(r"\n\s*\n", txt.strip()):
        linhas = bloco.strip().splitlines()
        tl = next((l for l in linhas if "-->" in l), None)
        if not tl:
            continue
        def ts(x):
            h, m, s = x.strip().replace(",", ".").split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
        a, b = [ts(x) for x in tl.split("-->")]
        texto = " ".join(linhas[linhas.index(tl) + 1:]).split()
        if not texto:
            continue
        # distribute the time by the length of each word
        pesos = [len(p) + 1 for p in texto]; tot = sum(pesos); t = a
        for p, w in zip(texto, pesos):
            d = (b - a) * w / tot
            pal.append({"s": round(t, 3), "e": round(t + d, 3), "t": p}); t += d
    return pal

def fmt_srt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

# ---------- caption blocks ----------
def blocos(pal, max_pal, max_car):
    out, cur = [], []
    for i, w in enumerate(pal):
        cur.append(w)
        fim_frase = re.search(r"[.!?,;:]$", w["t"])
        pausa = i + 1 < len(pal) and pal[i + 1]["s"] - w["e"] > 0.35
        texto = " ".join(x["t"] for x in cur)
        if len(cur) >= max_pal or len(texto) >= max_car or fim_frase or pausa:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out

def salvar_srt(bl, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, b in enumerate(bl, 1):
            f.write(f"{i}\n{fmt_srt(b[0]['s'])} --> {fmt_srt(b[-1]['e'])}\n{' '.join(w['t'] for w in b)}\n\n")

# ---------- pause cutting ----------
def energia(video):
    # RMS every 10 ms of the real audio: Whisper's word end is off by up to ~0.3 s and would clip the tail of speech
    import numpy as np
    raw = subprocess.run([FF, "-v", "error", "-i", video, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    au = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    return [float(np.sqrt((au[i:i + 160] ** 2).mean())) for i in range(0, len(au) - 160, 160)]

def silencio(rm, t0, t1, thr=0.004):
    # longest continuous stretch below the threshold within [t0, t1]
    i0, i1, best, i = int(max(0, t0) * 100), min(int(t1 * 100), len(rm)), (0, 0), int(max(0, t0) * 100)
    while i < i1:
        if rm[i] < thr:
            j = i
            while j < i1 and rm[j] < thr:
                j += 1
            if j - i > best[1] - best[0]:
                best = (i, j)
            i = j
        else:
            i += 1
    return best[0] / 100, best[1] / 100

def segmentos(pal, total, limiar, folga=0.18, respiros=(), rm=None):
    if not pal:
        return [(0.0, total)]
    segs, ini = [], max(0.0, pal[0]["s"] - folga)
    for a, b in zip(pal, pal[1:]):
        # pause marked in the cut plan (before the impact or the CTA) stays whole
        if any(a["e"] <= t <= b["s"] for t in respiros):
            continue
        if b["s"] - a["e"] > max(limiar, 2 * folga + 0.1):
            if rm:  # cut only inside measured silence; without enough silence, no cut
                sa, sb = silencio(rm, a["e"] - 0.15, b["s"] + 0.15)
                if sb - sa >= 2 * folga + 0.1:
                    segs.append((ini, sa + folga)); ini = sb - folga
            else:
                segs.append((ini, a["e"] + folga)); ini = b["s"] - folga
    segs.append((ini, min(total, pal[-1]["e"] + 0.6)))
    return dividir_por_energia(segs, limiar, folga, respiros, rm) if rm else segs

def dividir_por_energia(segs, limiar, folga, respiros, rm):
    # pauses that Whisper does not separate (short word gap, long real silence): still pauses
    out, minimo = [], max(limiar, 2 * folga + 0.1)
    for s0, e0 in segs:
        ini, i, i1 = s0, int(s0 * 100), min(int(e0 * 100), len(rm))
        while i < i1:
            if rm[i] < 0.004:
                j = i
                while j < i1 and rm[j] < 0.004:
                    j += 1
                a, b = i / 100, j / 100
                if b - a >= minimo and not any(a <= t <= b for t in respiros) and a - ini > 0.3 and e0 - b > 0.4:
                    out.append((ini, a + folga)); ini = b - folga
                i = j
            else:
                i += 1
        out.append((ini, e0))
    return out

def remapear(pal, segs, fade=0.0):
    # with dissolve, each cut overlaps `fade` s on both sides, so the timeline shrinks by that per cut
    out, acc = [], 0.0
    for a, b in segs:
        for w in pal:
            if a <= w["s"] < b:
                out.append({"s": w["s"] - a + acc, "e": min(w["e"], b) - a + acc, "t": w["t"]})
        acc += b - a - fade
    return out

# ---------- ASS ----------
def ass_cor(hexc, alpha="00"):
    h = hexc.lstrip("#")
    return f"&H{alpha}{h[4:6]}{h[2:4]}{h[0:2]}".upper()

def ass_t(t):
    cs = int(round(t * 100)); h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h}:{m:02}:{s:02}.{cs:02}"

def esc(t):
    return t.replace("\\", "").replace("{", "(").replace("}", ")")

def gerar_ass(bl, a, path):
    # --box: BorderStyle 3 = solid box behind each line, in the --outline color, with --border as padding
    bs, sombra_cor = (3, ass_cor(a.contorno)) if a.caixa else (1, ass_cor(a.contorno, "80"))
    def st(nome, tam, base):
        return (f"Style: {nome},{a.fonte},{tam},{ass_cor(a.cor)},{ass_cor(a.cor)},{ass_cor(a.contorno)},"
                f"{sombra_cor},{-1 if a.negrito else 0},{-1 if a.italico else 0},0,0,100,100,0,0,"
                f"{bs},{a.borda},{a.sombra},2,{a.margem_x},{a.margem_x},{1920 - base},1")
    estilo = st("L", a.tamanho, a.y)
    ev = []
    if a.gancho:
        # hook readable on the 1st frame (works muted); captions start when it leaves
        estilo += "\n" + st("G", a.gancho_tam or a.tamanho, a.y)
        txt = "\\N".join(esc(l) for l in a.gancho.split("|"))
        ev.append(f"Dialogue: 1,{ass_t(0)},{ass_t(a.gancho_s)},G,,0,0,0,,{txt}")
        bl = [b for b in bl if b[0]["s"] >= a.gancho_s - 0.05]
    for b in bl:
        fim_bloco = b[-1]["e"]
        for i, w in enumerate(b):
            ini = w["s"]
            fim = b[i + 1]["s"] if i + 1 < len(b) else fim_bloco
            if fim - ini < 0.04:
                continue
            partes = []
            for j, x in enumerate(b):
                txt = esc(x["t"].upper() if a.caixa_alta else x["t"])
                partes.append(f"{{\\c{ass_cor(a.destaque)}}}{txt}{{\\c{ass_cor(a.cor)}}}" if (a.destaque and j == i) else txt)
            ev.append(f"Dialogue: 0,{ass_t(ini)},{ass_t(fim)},L,,0,0,0,,{' '.join(partes)}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n"
                "ScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, "
                "SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, "
                "Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
                + estilo + "\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
                + "\n".join(ev) + "\n")

# ---------- default caption variants ----------
# Each variant is a combination of options that already exist; whatever the user passes on the command line overrides the variant.
# (The DYNAMIC caption, with occasional highlighted words, transitions and element animation, is the reel's style: it is not an option of this tool.)
ESTILOS = {
    "standard": {},                                                      # 1 line, up to 3 words that follow the speech, highlight if a color is given
    "stable": {"palavras": 8, "max_car": 34, "tamanho": 54},          # short 1-line phrases, calm reading (explainer, longer video)
    "box": {"palavras": 6, "max_car": 30, "tamanho": 54, "caixa": True},  # short phrases in a solid box in the --outline color
}


# ---------- main ----------
def main():
    p = argparse.ArgumentParser(description="Caption + overlay + soundtrack for 1080x1920 Reels")
    p.add_argument("--video", required=True); p.add_argument("--out", required=True)
    p.add_argument("--style", dest="estilo", choices=list(ESTILOS), default="standard", help="default caption variant: standard, stable or box; options passed by hand override the variant")
    p.add_argument("--overlay", help="PNG 1080x1920 with transparency (frame/logo from Figma)")
    p.add_argument("--intro", help="PNG shown over the video for the first --intro-s seconds")
    p.add_argument("--intro-s", type=float, default=2.0)
    p.add_argument("--srt", help="skip transcription and use this (reviewed) .srt")
    p.add_argument("--whisper-engine", dest="motor_whisper", choices=["auto", "faster", "cpp"], default="auto", help="transcription route: faster (faster-whisper), cpp (whisper.cpp with CUDA) or auto (measured order; falls back to the other if it fails)")
    p.add_argument("--model", dest="modelo", default="auto", help="auto = the best model the GPU sustains and that is already installed (large-v3-turbo, medium, small)"); p.add_argument("--language", dest="idioma", default=None)
    p.add_argument("--font", dest="fonte", default="Arial"); p.add_argument("--fontsdir", help="folder with the KV's .ttf/.otf files")
    p.add_argument("--size", dest="tamanho", type=int, default=64)
    p.add_argument("--color", dest="cor", default="#FFFFFF"); p.add_argument("--highlight", dest="destaque", default="", help="HEX of the spoken word; empty = no highlight")
    p.add_argument("--outline", dest="contorno", default="#000000"); p.add_argument("--border", dest="borda", type=float, default=3)
    p.add_argument("--shadow", dest="sombra", type=float, default=0)
    p.add_argument("--bold", dest="negrito", action="store_true"); p.add_argument("--italic", dest="italico", action="store_true")
    p.add_argument("--uppercase", dest="caixa_alta", action="store_true")
    p.add_argument("--y", type=int, default=1400, help="caption baseline in px (Reels safe zone: <= 1470)")
    p.add_argument("--margin-x", dest="margem_x", type=int, default=90)
    p.add_argument("--words", dest="palavras", type=int, default=3); p.add_argument("--max-chars", dest="max_car", type=int, default=24)
    p.add_argument("--fade", type=float, default=0.25, help="cross dissolve at each cut (s); 0 = hard cut")
    p.add_argument("--cut-pauses", dest="cortar_pausas", type=float, default=0.45, help="cuts silences longer than N s (default 0.45; 0 = no cut). A natural pause of ~0.36 s remains")
    p.add_argument("--slack", dest="folga", type=float, default=0.18, help="silence kept on each side of the cut (s)")
    p.add_argument("--music", dest="musica"); p.add_argument("--music-db", dest="musica_db", type=float, default=-20)
    p.add_argument("--bitrate", default="16M"); p.add_argument("--transcribe-only", dest="so_transcrever", action="store_true")
    p.add_argument("--box", dest="caixa", action="store_true", help="caption in a solid box in the --outline color (--border = padding)")
    p.add_argument("--remove", dest="remover", action="append", default=[], metavar="A-B",
                   help="removes from the video the speech that starts between A and B s (repeatable); use for a stretch outside the briefing")
    p.add_argument("--breath", dest="respiro", action="append", type=float, default=[], metavar="T",
                   help="keeps the pause that contains the instant T s (repeatable; rhythm of the cut plan)")
    p.add_argument("--hook", dest="gancho", help="hook text on the 1st frame, lines separated by |")
    p.add_argument("--hook-s", dest="gancho_s", type=float, default=3.0, help="until when the hook stays (s, final video time)")
    p.add_argument("--hook-size", dest="gancho_tam", type=int, default=0)
    p.add_argument("--endcard", help="1080x1920 PNG of the endcard, enters at the end with a fade")
    p.add_argument("--endcard-s", type=float, default=2.5)
    a = p.parse_args()
    for chave, valor in ESTILOS[a.estilo].items():
        if getattr(a, chave) == p.get_default(chave):
            setattr(a, chave, valor)

    video = os.path.abspath(a.video); out = os.path.abspath(a.out); base = os.path.splitext(out)[0]
    total = dur(video)

    pal = ler_srt(a.srt) if a.srt else transcrever(video, a.modelo, a.idioma, a.motor_whisper)
    if not pal:
        sys.exit("No speech found.")
    if not a.srt:
        salvar_srt(blocos(pal, a.palavras, a.max_car), base + ".srt")
        json.dump(pal, open(base + "_palavras.json", "w", encoding="utf-8"), ensure_ascii=False)
        print(f"[ok] transcription: {base}.srt (review it; if you fix it, run again with --srt)")
    if a.so_transcrever:
        return
    pal = remover(pal, a.remover)

    if a.cortar_pausas > 0:
        segs = segmentos(pal, total, a.cortar_pausas, a.folga, respiros=a.respiro, rm=energia(video) if tem_audio(video) else None)
    elif a.remover:
        segs = segmentos(pal, total, 0.6, a.folga, respiros=a.respiro, rm=energia(video) if tem_audio(video) else None)  # without cutting pauses, the gap of the removed stretch still has to be opened
    else:
        segs = [(0.0, total)]
    fade = min(a.fade, min(e - s for s, e in segs) / 3) if len(segs) > 1 else 0.0
    # cuts stay inside measured silence: the dissolve fits in the voice-free margin (folga)
    fade = min(fade, max(0.0, a.folga - 0.08)) if len(segs) > 1 else 0.0
    if len(segs) > 1:
        pal = remapear(pal, segs, fade)
    bl = blocos(pal, a.palavras, a.max_car)

    tmp = tempfile.mkdtemp(prefix="reels_")
    gerar_ass(bl, a, os.path.join(tmp, "leg.ass"))
    if a.fontsdir:
        shutil.copytree(a.fontsdir, os.path.join(tmp, "fonts"), dirs_exist_ok=True)

    inp = ["-i", video]; idx = 1; fc = []
    audio = tem_audio(video)
    if len(segs) > 1:
        # Dissolve only in the pause; without margin, concatenate without overlapping voice.
        for i, (s, e) in enumerate(segs):
            fc.append(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS,fps=30,format=yuv420p,setsar=1[v{i}]")
            if audio:
                fc.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS[a{i}]")
        vant, aant, comp = "[v0]", "[a0]", segs[0][1] - segs[0][0]
        for i in range(1, len(segs)):
            fc.append(f"{vant}[v{i}]xfade=transition=fade:duration={fade:.3f}:offset={comp - fade:.3f}[x{i}]" if fade >= 0.001 else
                      f"{vant}[v{i}]concat=n=2:v=1:a=0[x{i}]")
            vant = f"[x{i}]"
            if audio:
                fc.append(f"{aant}[a{i}]acrossfade=d={fade:.3f}:c1=tri:c2=tri[y{i}]" if fade >= 0.001 else
                          f"{aant}[a{i}]concat=n=2:v=0:a=1[y{i}]")
                aant = f"[y{i}]"
            comp += segs[i][1] - segs[i][0] - fade
        vsrc, asrc = vant, aant
    else:
        vsrc, asrc = "[0:v]", "[0:a]"
    fc.append(f"{vsrc}scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[b0]")
    cur = "[b0]"
    if a.overlay:
        inp += ["-i", os.path.abspath(a.overlay)]
        fc.append(f"[{idx}:v]scale=1080:1920[ov];{cur}[ov]overlay=0:0[b1]"); cur = "[b1]"; idx += 1
    fdir = ":fontsdir=fonts" if a.fontsdir else ""
    fc.append(f"{cur}ass=leg.ass{fdir}[b2]"); cur = "[b2]"
    if a.intro:
        inp += ["-loop", "1", "-t", str(a.intro_s), "-i", os.path.abspath(a.intro)]
        fc.append(f"[{idx}:v]scale=1080:1920,format=rgba[it];{cur}[it]overlay=0:0:enable='lt(t,{a.intro_s})':eof_action=pass[b3]")
        cur = "[b3]"; idx += 1
    d_fala = sum(e - s for s, e in segs) - fade * (len(segs) - 1)
    if a.endcard:
        inp += ["-loop", "1", "-t", str(a.endcard_s), "-framerate", "30", "-i", os.path.abspath(a.endcard)]
        fc.append(f"{cur}format=yuv420p[pre];[{idx}:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[ec];"
                  f"[pre][ec]xfade=transition=fade:duration=0.35:offset={d_fala - 0.35:.3f}[vout]")
        idx += 1
    else:
        fc.append(f"{cur}format=yuv420p[vout]")
    d_total = d_fala + (a.endcard_s - 0.35 if a.endcard else 0)
    amap = []
    if audio:
        pad = f",apad=pad_dur={a.endcard_s},atrim=0:{d_total:.3f}" if a.endcard else ""
        fc.append(f"{asrc}loudnorm=I=-16:TP=-1.5:LRA=11{pad}[voz]")
        if a.musica:
            inp += ["-stream_loop", "-1", "-i", os.path.abspath(a.musica)]
            d = d_total
            fc.append(f"[{idx}:a]volume={a.musica_db}dB,afade=t=out:st={max(0, d - 1.5):.2f}:d=1.5[mus];"
                      f"[voz][mus]amix=inputs=2:duration=first:normalize=0[aout]")
            idx += 1
        else:
            fc.append("[voz]anull[aout]")
        amap = ["-map", "[aout]", "-c:a", "aac", "-b:a", "192k"]
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import gpu_acceleration  # U13: NVENC when ffmpeg supports it, libx264 as fallback
    venc = gpu_acceleration.h264(FF, ["-c:v", "libx264", "-preset", "medium", "-b:v", a.bitrate, "-maxrate", a.bitrate,
                         "-bufsize", "32M"], bitrate=a.bitrate, bufsize="32M")
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "error"] + inp + [
        "-filter_complex", ";".join(fc), "-map", "[vout]"] + amap + venc + [
        "-r", "30", "-movflags", "+faststart", "-shortest", out]
    sh(cmd, cwd=tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import check_export  # quality.md §K: only says ok if the file passes the check
    if not check_export.conferir(out, fps=30, tamanho="1080x1920"):
        sys.exit(1)
    print(f"[ok] {out}  ({dur(out):.1f}s, {os.path.getsize(out)/1e6:.1f} MB)")

if __name__ == "__main__":
    main()
