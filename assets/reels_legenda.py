#!/usr/bin/env python3
# reels_legenda.py - /designer-mestre v13
# Video do cliente -> transcricao por palavra -> legenda .ass no KV -> overlay PNG -> trilha -> MP4.
# Dependencias: ffmpeg/ffprobe no PATH; faster-whisper (pip) so se nao houver --srt.
# Uso minimo:
#   python reels_legenda.py --video in.mp4 --overlay overlay.png --fonte "EB Garamond" --fontsdir fontes --out final.mp4
# Fluxo sem retrabalho: 1a rodada gera <out>.srt para revisao; se houver erro de fala,
# corrigir o .srt e rodar de novo com --srt <out>.srt (pula a transcricao).
import argparse, json, os, re, shutil, subprocess, sys, tempfile

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit("ERRO ffmpeg:\n" + r.stderr[-2500:])
    return r

def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True).stdout
    return float(out.strip())

def tem_audio(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                          "stream=index", "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return bool(out.strip())

# ---------- transcricao ----------
def transcrever(video, modelo, idioma):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper ausente: pip install faster-whisper  (ou passe --srt arquivo.srt)")
    m = None
    for dev, ct in (("cuda", "float16"), ("cpu", "int8")):
        try:
            m = WhisperModel(modelo, device=dev, compute_type=ct); break
        except Exception:
            continue
    if m is None:
        sys.exit("Nao carregou o modelo Whisper. Sem internet para baixar? Use --srt.")
    segs, _ = m.transcribe(video, language=idioma, word_timestamps=True, vad_filter=True)
    pal = []
    for s in segs:
        for w in s.words or []:
            t = w.word.strip()
            if t:
                pal.append({"s": round(w.start, 3), "e": round(w.end, 3), "t": t})
    return pal

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
        # distribui o tempo pelo tamanho de cada palavra
        pesos = [len(p) + 1 for p in texto]; tot = sum(pesos); t = a
        for p, w in zip(texto, pesos):
            d = (b - a) * w / tot
            pal.append({"s": round(t, 3), "e": round(t + d, 3), "t": p}); t += d
    return pal

def fmt_srt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

# ---------- blocos de legenda ----------
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

# ---------- corte de pausas ----------
def segmentos(pal, total, limiar, folga=0.15):
    if not pal:
        return [(0.0, total)]
    segs, ini = [], max(0.0, pal[0]["s"] - folga)
    for a, b in zip(pal, pal[1:]):
        if b["s"] - a["e"] > limiar:
            segs.append((ini, a["e"] + folga)); ini = b["s"] - folga
    segs.append((ini, min(total, pal[-1]["e"] + 0.6)))
    return segs

def remapear(pal, segs):
    out, acc = [], 0.0
    for a, b in segs:
        for w in pal:
            if a <= w["s"] < b:
                out.append({"s": w["s"] - a + acc, "e": min(w["e"], b) - a + acc, "t": w["t"]})
        acc += b - a
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
    estilo = (f"Style: L,{a.fonte},{a.tamanho},{ass_cor(a.cor)},{ass_cor(a.cor)},{ass_cor(a.contorno)},"
              f"{ass_cor(a.contorno, '80')},{-1 if a.negrito else 0},{-1 if a.italico else 0},0,0,100,100,0,0,"
              f"1,{a.borda},{a.sombra},2,{a.margem_x},{a.margem_x},{1920 - a.y},1")
    ev = []
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
        f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n"
                "ScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, "
                "SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, "
                "Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
                + estilo + "\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
                + "\n".join(ev) + "\n")

# ---------- main ----------
def main():
    p = argparse.ArgumentParser(description="Legenda + overlay + trilha para Reels 1080x1920")
    p.add_argument("--video", required=True); p.add_argument("--out", required=True)
    p.add_argument("--overlay", help="PNG 1080x1920 com transparencia (moldura/logo do Figma)")
    p.add_argument("--intro", help="PNG mostrado sobre o video nos primeiros --intro-s segundos")
    p.add_argument("--intro-s", type=float, default=2.0)
    p.add_argument("--srt", help="pula a transcricao e usa este .srt (revisado)")
    p.add_argument("--modelo", default="small"); p.add_argument("--idioma", default=None)
    p.add_argument("--fonte", default="Arial"); p.add_argument("--fontsdir", help="pasta com os .ttf/.otf do KV")
    p.add_argument("--tamanho", type=int, default=64)
    p.add_argument("--cor", default="#FFFFFF"); p.add_argument("--destaque", default="", help="HEX da palavra falada; vazio = sem destaque")
    p.add_argument("--contorno", default="#000000"); p.add_argument("--borda", type=float, default=3)
    p.add_argument("--sombra", type=float, default=0)
    p.add_argument("--negrito", action="store_true"); p.add_argument("--italico", action="store_true")
    p.add_argument("--caixa-alta", action="store_true")
    p.add_argument("--y", type=int, default=1400, help="base da legenda em px (safe zone Reels: <= 1470)")
    p.add_argument("--margem-x", type=int, default=90)
    p.add_argument("--palavras", type=int, default=4); p.add_argument("--max-car", type=int, default=26)
    p.add_argument("--cortar-pausas", type=float, default=0, help="corta silencios maiores que N s (0 = nao corta)")
    p.add_argument("--musica"); p.add_argument("--musica-db", type=float, default=-20)
    p.add_argument("--bitrate", default="16M"); p.add_argument("--so-transcrever", action="store_true")
    a = p.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} nao encontrado no PATH (Windows: winget install Gyan.FFmpeg)")
    video = os.path.abspath(a.video); out = os.path.abspath(a.out); base = os.path.splitext(out)[0]
    total = dur(video)

    pal = ler_srt(a.srt) if a.srt else transcrever(video, a.modelo, a.idioma)
    if not pal:
        sys.exit("Nenhuma fala encontrada.")
    if not a.srt:
        salvar_srt(blocos(pal, a.palavras, a.max_car), base + ".srt")
        json.dump(pal, open(base + "_palavras.json", "w", encoding="utf-8"), ensure_ascii=False)
        print(f"[ok] transcricao: {base}.srt (revise; se corrigir, rode de novo com --srt)")
    if a.so_transcrever:
        return

    segs = segmentos(pal, total, a.cortar_pausas) if a.cortar_pausas > 0 else [(0.0, total)]
    if len(segs) > 1:
        pal = remapear(pal, segs)
    bl = blocos(pal, a.palavras, a.max_car)

    tmp = tempfile.mkdtemp(prefix="reels_")
    gerar_ass(bl, a, os.path.join(tmp, "leg.ass"))
    if a.fontsdir:
        shutil.copytree(a.fontsdir, os.path.join(tmp, "fonts"), dirs_exist_ok=True)

    inp = ["-i", video]; idx = 1; fc = []
    audio = tem_audio(video)
    if len(segs) > 1:
        vp = "".join(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS[v{i}];" for i, (s, e) in enumerate(segs))
        ap = "".join(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS[a{i}];" for i, (s, e) in enumerate(segs)) if audio else ""
        ordem = "".join(f"[v{i}]" + (f"[a{i}]" if audio else "") for i in range(len(segs)))
        fc.append(vp + ap + ordem + f"concat=n={len(segs)}:v=1:a={1 if audio else 0}[vc]" + ("[ac]" if audio else ""))
        vsrc, asrc = "[vc]", "[ac]"
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
    fc.append(f"{cur}format=yuv420p[vout]")
    amap = []
    if audio:
        fc.append(f"{asrc}loudnorm=I=-16:TP=-1.5:LRA=11[voz]")
        if a.musica:
            inp += ["-stream_loop", "-1", "-i", os.path.abspath(a.musica)]
            d = sum(e - s for s, e in segs)
            fc.append(f"[{idx}:a]volume={a.musica_db}dB,afade=t=out:st={max(0, d - 1.5):.2f}:d=1.5[mus];"
                      f"[voz][mus]amix=inputs=2:duration=first:normalize=0[aout]")
            idx += 1
        else:
            fc.append("[voz]anull[aout]")
        amap = ["-map", "[aout]", "-c:a", "aac", "-b:a", "192k"]
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + inp + [
        "-filter_complex", ";".join(fc), "-map", "[vout]"] + amap + [
        "-c:v", "libx264", "-preset", "medium", "-b:v", a.bitrate, "-maxrate", a.bitrate, "-bufsize", "32M",
        "-r", "30", "-movflags", "+faststart", "-shortest", out]
    sh(cmd, cwd=tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[ok] {out}  ({dur(out):.1f}s, {os.path.getsize(out)/1e6:.1f} MB)")

if __name__ == "__main__":
    main()
