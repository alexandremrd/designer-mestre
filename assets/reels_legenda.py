#!/usr/bin/env python3
# reels_legenda.py - /designer-mestre v19.55
# Video do cliente -> transcricao por palavra -> legenda .ass no KV -> overlay PNG -> trilha -> endcard -> MP4.
# Dependencias: ffmpeg no PATH ou o pacote imageio-ffmpeg (uv run --with imageio-ffmpeg ...);
# faster-whisper (pip) so se nao houver --srt.
# Uso minimo:
#   python reels_legenda.py --video in.mp4 --overlay overlay.png --fonte "EB Garamond" --fontsdir fontes --out final.mp4
# Fluxo sem retrabalho: 1a rodada gera <out>.srt para revisao; se houver erro de fala,
# corrigir o .srt e rodar de novo com --srt <out>.srt (pula a transcricao).
import argparse, json, os, re, shutil, subprocess, sys, tempfile

def achar_ffmpeg():
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg ausente: rode com  uv run --with imageio-ffmpeg python reels_legenda.py ...  "
                 "(ou winget install Gyan.FFmpeg)")

FF = achar_ffmpeg()

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit("ERRO ffmpeg:\n" + r.stderr[-2500:])
    return r

def info(path):
    # sem ffprobe: o imageio-ffmpeg so traz o ffmpeg, entao le o cabecalho do proprio ffmpeg
    return subprocess.run([FF, "-hide_banner", "-i", path], capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stderr

def dur(path):
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info(path)).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)

def tem_audio(path):
    return "Audio:" in info(path)

# ---------- transcricao ----------
def transcrever(video, modelo, idioma):
    try:
        from faster_whisper import WhisperModel
        import numpy as np
    except ImportError:
        sys.exit("faster-whisper ausente: pip install faster-whisper  (ou passe --srt arquivo.srt)")
    # audio decodificado pelo ffmpeg: evita o decodificador PyAV do faster-whisper, que quebra entre versoes
    raw = subprocess.run([FF, "-v", "error", "-i", video, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    erro = None
    for dev, ct in (("cuda", "float16"), ("cpu", "int8")):
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import recursos  # modelos do Whisper na raiz dos recursos, se definida
            m = WhisperModel(modelo, device=dev, compute_type=ct, download_root=recursos.caminho("whisper"))
            segs, _ = m.transcribe(audio, language=idioma, word_timestamps=True, vad_filter=True)
            pal = []
            # a GPU pode carregar o modelo e falhar so aqui (ex.: cuBLAS ausente); por isso o laco inteiro fica no try
            for s in segs:
                for w in s.words or []:
                    t = w.word.strip()
                    if t:
                        pal.append({"s": round(w.start, 3), "e": round(w.end, 3), "t": t})
            return pal
        except Exception as e:
            erro = e
    sys.exit(f"Whisper falhou na GPU e na CPU ({erro}). Sem internet para baixar o modelo? Use --srt.")

def remover(pal, faixas):
    # tira as palavras que comecam dentro das faixas "a-b" (s): fala proibida ou fora do briefing
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
def segmentos(pal, total, limiar, folga=0.35, respiros=()):
    if not pal:
        return [(0.0, total)]
    segs, ini = [], max(0.0, pal[0]["s"] - folga)
    for a, b in zip(pal, pal[1:]):
        # pausa marcada no plano de corte (antes do impacto ou do CTA) fica inteira
        if any(a["e"] <= t <= b["s"] for t in respiros):
            continue
        if b["s"] - a["e"] > max(limiar, 2 * folga + 0.1):
            segs.append((ini, a["e"] + folga)); ini = b["s"] - folga
    segs.append((ini, min(total, pal[-1]["e"] + 0.6)))
    return segs

def remapear(pal, segs, fade=0.0):
    # com dissolve, cada corte sobrepoe `fade` s dos dois lados, entao a linha do tempo encolhe isso por corte
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
    # --caixa: BorderStyle 3 = caixa solida atras de cada linha, na cor de --contorno, com --borda de respiro
    bs, sombra_cor = (3, ass_cor(a.contorno)) if a.caixa else (1, ass_cor(a.contorno, "80"))
    def st(nome, tam, base):
        return (f"Style: {nome},{a.fonte},{tam},{ass_cor(a.cor)},{ass_cor(a.cor)},{ass_cor(a.contorno)},"
                f"{sombra_cor},{-1 if a.negrito else 0},{-1 if a.italico else 0},0,0,100,100,0,0,"
                f"{bs},{a.borda},{a.sombra},2,{a.margem_x},{a.margem_x},{1920 - base},1")
    estilo = st("L", a.tamanho, a.y)
    ev = []
    if a.gancho:
        # gancho legivel no 1o frame (funciona no mudo); as legendas comecam quando ele sai
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
    p.add_argument("--palavras", type=int, default=3); p.add_argument("--max-car", type=int, default=24)
    p.add_argument("--fade", type=float, default=0.25, help="cross dissolve em cada corte (s); 0 = corte seco")
    p.add_argument("--cortar-pausas", type=float, default=0, help="corta silencios maiores que N s (0 = nao corta)")
    p.add_argument("--musica"); p.add_argument("--musica-db", type=float, default=-20)
    p.add_argument("--bitrate", default="16M"); p.add_argument("--so-transcrever", action="store_true")
    p.add_argument("--caixa", action="store_true", help="legenda em caixa solida na cor de --contorno (--borda = respiro)")
    p.add_argument("--remover", action="append", default=[], metavar="A-B",
                   help="tira do video a fala que comeca entre A e B s (repetivel); use para trecho fora do briefing")
    p.add_argument("--respiro", action="append", type=float, default=[], metavar="T",
                   help="mantem a pausa que contem o instante T s (repetivel; ritmo do plano de corte)")
    p.add_argument("--gancho", help="texto do gancho no 1o frame, linhas separadas por |")
    p.add_argument("--gancho-s", type=float, default=3.0, help="ate quando o gancho fica (s, tempo do video final)")
    p.add_argument("--gancho-tam", type=int, default=0)
    p.add_argument("--endcard", help="PNG 1080x1920 do endcard, entra no fim com fade")
    p.add_argument("--endcard-s", type=float, default=2.5)
    a = p.parse_args()

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
    pal = remover(pal, a.remover)

    if a.cortar_pausas > 0:
        segs = segmentos(pal, total, a.cortar_pausas, respiros=a.respiro)
    elif a.remover:
        segs = segmentos(pal, total, 0.6, respiros=a.respiro)  # sem cortar pausas, ainda e preciso abrir o buraco do trecho removido
    else:
        segs = [(0.0, total)]
    fade = min(a.fade, min(e - s for s, e in segs) / 3) if len(segs) > 1 else 0.0
    # A sobreposição de áudio cabe somente nas margens sem palavras.
    for left, right in zip(segs, segs[1:]):
        lp = [w for w in pal if left[0] <= w["s"] < left[1]]
        rp = [w for w in pal if right[0] <= w["s"] < right[1]]
        if lp and rp:
            fade = min(fade, max(0.0, left[1] - max(w["e"] for w in lp) - 0.08),
                       max(0.0, min(w["s"] for w in rp) - right[0] - 0.08))
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
        # Dissolve somente no respiro; sem margem, concatena sem sobrepor voz.
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
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "error"] + inp + [
        "-filter_complex", ";".join(fc), "-map", "[vout]"] + amap + [
        "-c:v", "libx264", "-preset", "medium", "-b:v", a.bitrate, "-maxrate", a.bitrate, "-bufsize", "32M",
        "-r", "30", "-movflags", "+faststart", "-shortest", out]
    sh(cmd, cwd=tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import conferir_export  # qualidade.md §K: so diz ok se o arquivo passa na conferencia
    if not conferir_export.conferir(out, fps=30, tamanho="1080x1920"):
        sys.exit(1)
    print(f"[ok] {out}  ({dur(out):.1f}s, {os.path.getsize(out)/1e6:.1f} MB)")

if __name__ == "__main__":
    main()
