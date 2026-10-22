#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_audio.py - Locucao (TTS) e efeitos sonoros via API da ElevenLabs para o /designer-mestre.

Sem dependencias: usa so a biblioteca padrao. A chave e da conta de cada usuario e vem de ELEVENLABS_API_KEY
no ambiente ou de um arquivo .env (--env-file; padrao: .env.local/.env da pasta atual e depois
%USERPROFILE%\\.designer-mestre\\, fora da skill, preservado nas atualizacoes). Nunca e impressa nem gravada.
Cada audio gerado ganha um .txt ao lado com voz, modelo, ajustes e texto, para aprendizado do cliente.

Comandos:
  python gerar_audio.py checar                       (valida a chave e mostra creditos; nao gasta creditos)
  python gerar_audio.py vozes [--busca george]       (lista voice_id disponiveis; nao gasta creditos)
  python gerar_audio.py falar "TEXTO" -o "Trabalho\\locucao_v1.mp3" [--voz ID] [--modelo eleven_multilingual_v2]
        [--estabilidade 0.5 --similaridade 0.75 --estilo 0.25 --velocidade 1.05] [--formato mp3_44100_128]
  python gerar_audio.py falar --arquivo roteiro.txt -o "..."   (texto vindo de arquivo)
  python gerar_audio.py efeito "porta de vidro abrindo, shopping" --duracao 3 -o "Trabalho\\sfx_porta.mp3"
"""
import argparse, json, os, sys, time
import urllib.request, urllib.error, urllib.parse

API = "https://api.elevenlabs.io"
VOZ_PADRAO = "JBFqnCBsd6RMkjVDRZzb"  # George, voz padrao da biblioteca ElevenLabs
MODELO_PADRAO = "eleven_multilingual_v2"  # cobre PT-BR


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
    sys.exit("[sem chave] ELEVENLABS_API_KEY ausente. Crie a pasta %USERPROFILE%\\.designer-mestre, rode ali "
             "`npx -y @elevenlabs/cli@latest onboard init` e faca login com a sua conta (grava .env.local, "
             "preservado nas atualizacoes). Nunca cole a chave no chat.")


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
        sys.exit(f"[erro {e.code}] ElevenLabs recusou {path}: {detalhe}")
    except urllib.error.URLError as e:
        sys.exit(f"[indisponivel] Sem conexao com {API} ({e.reason}).")


def destino(saida, sobrescrever):
    if os.path.exists(saida) and not sobrescrever:
        sys.exit(f"[existe] {saida} ja existe; use outro nome (_v2) ou --sobrescrever.")
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)


def registrar(saida, campos):
    with open(os.path.splitext(saida)[0] + ".txt", "w", encoding="utf-8") as f:
        f.write(f"data: {time.strftime('%Y-%m-%d %H:%M')}\nferramenta: ElevenLabs API\n")
        for k, v in campos.items():
            f.write(f"{k}: {v}\n")


def cmd_checar(a, chave):
    sub = json.loads(req(chave, "GET", "/v1/user/subscription"))
    usados, limite = sub.get("character_count", 0), sub.get("character_limit", 0)
    print(f"Chave OK | plano {sub.get('tier', '?')} | creditos usados {usados}/{limite} | restam {limite - usados}")


def cmd_vozes(a, chave):
    vozes = json.loads(req(chave, "GET", "/v1/voices")).get("voices", [])
    busca = (a.busca or "").lower()
    for v in vozes:
        rotulos = ", ".join(f"{k}={val}" for k, val in (v.get("labels") or {}).items())
        linha = f"{v['voice_id']}  {v.get('name', '')}  [{v.get('category', '')}]  {rotulos}"
        if busca in linha.lower():
            print(linha)


def cmd_falar(a, chave):
    texto = open(a.arquivo, encoding="utf-8").read().strip() if a.arquivo else (a.texto or "").strip()
    if not texto:
        sys.exit("[sem texto] Passe o texto ou --arquivo.")
    destino(a.o, a.sobrescrever)
    ajustes = {"stability": a.estabilidade, "similarity_boost": a.similaridade,
               "style": a.estilo, "speed": a.velocidade, "use_speaker_boost": True}
    audio = req(chave, "POST", f"/v1/text-to-speech/{a.voz}",
                {"text": texto, "model_id": a.modelo, "voice_settings": ajustes},
                {"output_format": a.formato})
    with open(a.o, "wb") as f:
        f.write(audio)
    registrar(a.o, {"tipo": "locucao (TTS)", "voz": a.voz, "modelo": a.modelo, "formato": a.formato,
                    "ajustes": json.dumps(ajustes), "caracteres": len(texto), "texto": texto,
                    "status": "rascunho"})
    print(f"Locucao salva em {a.o} ({len(audio) // 1024} KB, {len(texto)} caracteres)")


def cmd_efeito(a, chave):
    destino(a.o, a.sobrescrever)
    corpo = {"text": a.descricao, "prompt_influence": a.influencia}
    if a.duracao:
        corpo["duration_seconds"] = a.duracao
    audio = req(chave, "POST", "/v1/sound-generation", corpo, {"output_format": a.formato})
    with open(a.o, "wb") as f:
        f.write(audio)
    registrar(a.o, {"tipo": "efeito sonoro", "descricao": a.descricao, "duracao": a.duracao or "auto",
                    "influencia": a.influencia, "formato": a.formato, "status": "rascunho"})
    print(f"Efeito salvo em {a.o} ({len(audio) // 1024} KB)")


def main():
    p = argparse.ArgumentParser(description="Locucao e efeitos sonoros ElevenLabs (/designer-mestre)")
    p.add_argument("--env-file", help="arquivo .env com ELEVENLABS_API_KEY (padrao: .env.local/.env)")
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("checar")
    v = sp.add_parser("vozes")
    v.add_argument("--busca")
    f = sp.add_parser("falar")
    f.add_argument("texto", nargs="?")
    f.add_argument("--arquivo")
    f.add_argument("--voz", default=VOZ_PADRAO)
    f.add_argument("--modelo", default=MODELO_PADRAO)
    f.add_argument("--estabilidade", type=float, default=0.5)
    f.add_argument("--similaridade", type=float, default=0.75)
    f.add_argument("--estilo", type=float, default=0.25)
    f.add_argument("--velocidade", type=float, default=1.05)
    e = sp.add_parser("efeito")
    e.add_argument("descricao")
    e.add_argument("--duracao", type=float, help="0.5 a 30 s; omitido = automatico")
    e.add_argument("--influencia", type=float, default=0.3)
    for s in (f, e):
        s.add_argument("-o", required=True)
        s.add_argument("--formato", default="mp3_44100_128")
        s.add_argument("--sobrescrever", action="store_true")
    a = p.parse_args()
    chave = carregar_chave(a.env_file)
    {"checar": cmd_checar, "vozes": cmd_vozes, "falar": cmd_falar, "efeito": cmd_efeito}[a.cmd](a, chave)


if __name__ == "__main__":
    main()
