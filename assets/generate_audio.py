#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_audio.py - Voiceover (TTS) and sound effects via the ElevenLabs API for /designer-mestre.

No dependencies: uses only the standard library. The key belongs to each user's account and comes from ELEVENLABS_API_KEY
in the environment or from a .env file (--env-file; default: .env.local/.env in the current folder and then
%USERPROFILE%\\.designer-mestre\\, outside the skill, preserved across updates). It is never printed or saved.
Each generated audio gets a .txt next to it with voice, model, settings and text, for the client's learning.

Commands:
  python generate_audio.py check                       (validates the key and shows credits; spends no credits)
  python generate_audio.py voices [--search george]       (lists available voice_id; spends no credits)
  python generate_audio.py speak "TEXT" -o "Trabalho\\voiceover_v1.mp3" [--voice ID] [--model eleven_multilingual_v2]
        [--stability 0.5 --similarity 0.75 --style 0.25 --speed 1.05] [--format mp3_44100_128]
  python generate_audio.py speak --file script.txt -o "..."   (text read from a file)
  python generate_audio.py effect "glass door opening, shopping mall" --duration 3 -o "Trabalho\\sfx_door.mp3"
"""
import argparse, json, os, sys, time
import urllib.request, urllib.error, urllib.parse

API = "https://api.elevenlabs.io"
VOZ_PADRAO = "JBFqnCBsd6RMkjVDRZzb"  # George, default voice of the ElevenLabs library
MODELO_PADRAO = "eleven_multilingual_v2"  # covers PT-BR


def carregar_chave(env_file):
    chave = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if chave:
        return chave
    pasta_usuario = os.path.join(os.path.expanduser("~"), ".designer-mestre")
    candidatos = [env_file] if env_file else [
        ".env.local", ".env", os.path.join(pasta_usuario, ".env.local"), os.path.join(pasta_usuario, ".env")]
    for caminho in candidatos:
        if not caminho or not os.path.isfile(caminho):
            continue
        with open(caminho, encoding="utf-8") as f:
            for linha in f:
                nome, sep, valor = linha.strip().partition("=")
                if sep and nome.strip().removeprefix("export ").strip() == "ELEVENLABS_API_KEY":
                    return valor.strip().strip('"').strip("'")
    sys.exit("[no key] ELEVENLABS_API_KEY missing. Create the folder %USERPROFILE%\\.designer-mestre, run there "
             "`npx -y @elevenlabs/cli@latest onboard init` and log in with your account (writes .env.local, "
             "preserved across updates). Never paste the key in the chat.")


def req(chave, method, path, body=None, query=None, timeout=120):
    url = API + path + ("?" + urllib.parse.urlencode(query) if query else "")
    data = json.dumps(body).encode() if body is not None else None
    headers = {"xi-api-key": chave}
    if data:
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode("utf-8", "replace")[:400]
        sys.exit(f"[error {e.code}] ElevenLabs rejected {path}: {detalhe}")
    except urllib.error.URLError as e:
        sys.exit(f"[unavailable] No connection to {API} ({e.reason}).")


def destino(saida, sobrescrever):
    if os.path.exists(saida) and not sobrescrever:
        sys.exit(f"[exists] {saida} already exists; use another name (_v2) or --overwrite.")
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)


def registrar(saida, campos):
    with open(os.path.splitext(saida)[0] + ".txt", "w", encoding="utf-8") as f:
        f.write(f"date: {time.strftime('%Y-%m-%d %H:%M')}\ntool: ElevenLabs API\n")
        for k, v in campos.items():
            f.write(f"{k}: {v}\n")


def cmd_checar(a, chave):
    sub = json.loads(req(chave, "GET", "/v1/user/subscription"))
    usados, limite = sub.get("character_count", 0), sub.get("character_limit", 0)
    print(f"Key OK | plan {sub.get('tier', '?')} | credits used {usados}/{limite} | remaining {limite - usados}")


def cmd_vozes(a, chave):
    vozes = json.loads(req(chave, "GET", "/v1/voices")).get("voices", [])
    busca = (a.busca or "").lower()
    for v in vozes:
        rotulos = ", ".join(f"{k}={val}" for k, val in (v.get("labels") or {}).items())
        linha = f"{v['voice_id']}  {v.get('name', '')}  [{v.get('category', '')}]  {rotulos}"
        if busca in linha.lower():
            print(linha)


ASSINATURAS = (b"ID3", b"\xff\xfb", b"\xff\xf3", b"\xff\xf2", b"RIFF", b"OggS", b"fLaC")


def audio_valido(audio, saida):
    """An empty or non-audio response (e.g. error JSON) cannot become 'saved'; check before writing."""
    if not audio or not audio.startswith(ASSINATURAS):
        sys.exit(f"[error] empty or invalid audio, nothing written: {saida}")


def cmd_falar(a, chave):
    texto = open(a.arquivo, encoding="utf-8").read().strip() if a.arquivo else (a.texto or "").strip()
    if not texto:
        sys.exit("[no text] Pass the text or --file.")
    destino(a.o, a.sobrescrever)
    ajustes = {"stability": a.estabilidade, "similarity_boost": a.similaridade,
               "style": a.estilo, "speed": a.velocidade, "use_speaker_boost": True}
    audio = req(chave, "POST", f"/v1/text-to-speech/{a.voz}",
                {"text": texto, "model_id": a.modelo, "voice_settings": ajustes},
                {"output_format": a.formato})
    audio_valido(audio, a.o)
    with open(a.o, "wb") as f:
        f.write(audio)
    registrar(a.o, {"type": "voiceover (TTS)", "voice": a.voz, "model": a.modelo, "format": a.formato,
                    "settings": json.dumps(ajustes), "characters": len(texto), "text": texto,
                    "status": "rascunho"})
    print(f"Voiceover saved to {a.o} ({len(audio) // 1024} KB, {len(texto)} characters)")


def cmd_efeito(a, chave):
    destino(a.o, a.sobrescrever)
    corpo = {"text": a.descricao, "prompt_influence": a.influencia}
    if a.duracao:
        corpo["duration_seconds"] = a.duracao
    audio = req(chave, "POST", "/v1/sound-generation", corpo, {"output_format": a.formato})
    audio_valido(audio, a.o)
    with open(a.o, "wb") as f:
        f.write(audio)
    registrar(a.o, {"type": "sound effect", "description": a.descricao, "duration": a.duracao or "auto",
                    "influence": a.influencia, "format": a.formato, "status": "rascunho"})
    print(f"Effect saved to {a.o} ({len(audio) // 1024} KB)")


def main():
    p = argparse.ArgumentParser(description="ElevenLabs voiceover and sound effects (/designer-mestre)")
    p.add_argument("--env-file", help=".env file with ELEVENLABS_API_KEY (default: .env.local/.env)")
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("check")
    v = sp.add_parser("voices")
    v.add_argument("--search", dest="busca")
    f = sp.add_parser("speak")
    f.add_argument("texto", nargs="?")
    f.add_argument("--file", dest="arquivo")
    f.add_argument("--voice", dest="voz", default=VOZ_PADRAO)
    f.add_argument("--model", dest="modelo", default=MODELO_PADRAO)
    f.add_argument("--stability", dest="estabilidade", type=float, default=0.5)
    f.add_argument("--similarity", dest="similaridade", type=float, default=0.75)
    f.add_argument("--style", dest="estilo", type=float, default=0.25)
    f.add_argument("--speed", dest="velocidade", type=float, default=1.05)
    e = sp.add_parser("effect")
    e.add_argument("descricao")
    e.add_argument("--duration", dest="duracao", type=float, help="0.5 to 30 s; omitted = automatic")
    e.add_argument("--influence", dest="influencia", type=float, default=0.3)
    for s in (f, e):
        s.add_argument("-o", required=True)
        s.add_argument("--format", dest="formato", default="mp3_44100_128")
        s.add_argument("--overwrite", dest="sobrescrever", action="store_true")
    a = p.parse_args()
    chave = carregar_chave(a.env_file)
    {"check": cmd_checar, "voices": cmd_vozes, "speak": cmd_falar, "effect": cmd_efeito}[a.cmd](a, chave)


if __name__ == "__main__":
    main()
