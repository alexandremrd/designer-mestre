#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recursos.py - Registro unico dos caminhos dos recursos locais do /designer-mestre.

Tudo que a skill roda no PC (geradores, ferramentas, modelos, caches) mora numa pasta raiz escolhida pelo
usuario, separada por categoria. Os scripts perguntam o caminho aqui, em vez de guardar caminho fixo, para que
mover ou renomear a raiz (motor_local.py organizar) nao quebre nada. O registro fica em
%USERPROFILE%\\.designer-mestre\\motor_local.json, que atualizacoes da skill nao apagam.

  python recursos.py            (mostra raiz, categorias e onde cada recurso esta)
"""
import json, os

CFG = os.path.join(os.path.expanduser("~"), ".designer-mestre", "motor_local.json")

# chave -> subpasta dentro da raiz. Categorias: Geradores (criam imagem, 3D, video), Ferramentas (apoio:
# navegador, conversores, bibliotecas), Modelos (pesos usados por mais de um script), Cache (downloads reaproveitaveis).
PADRAO = {
    "comfyui": r"Geradores\ComfyUI",
    "blender": r"Geradores\Blender",
    "playwright": r"Ferramentas\playwright",
    "node": r"Ferramentas\node",
    "ffmpeg": r"Ferramentas\ffmpeg",
    "whisper": r"Modelos\whisper",
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
    """Caminho registrado do recurso; sem registro, o lugar padrao dentro da raiz (ou None sem raiz)."""
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
    """Aponta o processo atual (e os filhos) para os recursos da raiz. Nao mexe nas variaveis do Windows."""
    pw = existe("playwright")
    if pw and not os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = pw
    ff = existe("ffmpeg")
    if ff:
        bin_ff = os.path.join(ff, "bin") if os.path.isdir(os.path.join(ff, "bin")) else ff
        os.environ["PATH"] = bin_ff + os.pathsep + os.environ.get("PATH", "")


if __name__ == "__main__":
    print(f"raiz: {raiz() or 'nao definida (motor_local.py motores --pasta <local>)'}")
    for k in PADRAO:
        p = caminho(k)
        print(f"  {k:10} {p or '-'}  {'(ok)' if p and os.path.exists(p) else '(ausente)'}")
