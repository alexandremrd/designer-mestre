#!/usr/bin/env python3
"""Client card: reads `_DESIGN\\mapa.md` and gives the script what it needs (fonts, colors, Reels template, safe zone).

Why it exists: the skill is universal and stores nothing about any client. Everything that changes from brand to brand lives in a single
file inside the client folder (`D:\\Clientes\\[Client]\\_DESIGN\\mapa.md`), written as `Key: value` lines.
The scripts find the client folder by themselves (they climb the folders from the delivery until they find `_DESIGN`) and pull from there.

Format accepted in mapa.md (any of these, in any section):
    Fonts: D:\\Clientes\\Brand\\Compartilhada\\Identidade Visual\\Fontes
    - Accent color: #C8A97E
    **Caption font:** Albert Sans
    | Reels safe zone | 90 914 240 1470 |

Terminal usage (shows what was read, for checking):
    python client_card.py "<delivery or client folder>"

Usage in another script:
    import client_card
    ficha = client_card.ler(partida=delivery_folder)
    cor = client_card.pegar(ficha, "Accent color", "#C0C0C0")
"""
import pathlib
import re
import sys
import unicodedata


def _normalizar(texto):
    """Key without accents, lowercase and with single spaces: 'Título Fonte' -> 'titulo fonte'."""
    sem_acento = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(c for c in sem_acento if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", sem_acento.strip().lower())


def achar_pasta_cliente(partida=None):
    """Climbs the folders from `partida` until it finds one that contains `_DESIGN`. Returns None if not found."""
    pasta = pathlib.Path(partida or ".").resolve()
    for candidata in [pasta, *pasta.parents]:
        if (candidata / "_DESIGN").is_dir():
            return candidata
    return None


_LINHA_CHAVE = re.compile(r"^\s*(?:[-*]\s*)?\**([^:|*#\n]+?)\**\s*:\s*\**\s*(.+?)\s*$")
_LINHA_TABELA = re.compile(r"^\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$")


def ler(pasta_cliente=None, partida=None):
    """Returns {normalized key: value} read from `_DESIGN\\mapa.md`. Without the file, returns an empty dictionary."""
    cliente = pathlib.Path(pasta_cliente) if pasta_cliente else achar_pasta_cliente(partida)
    ficha = {}
    if not cliente:
        return ficha
    mapa = cliente / "_DESIGN" / "mapa.md"
    if not mapa.is_file():
        return ficha
    for linha in mapa.read_text(encoding="utf-8", errors="replace").splitlines():
        achado = _LINHA_TABELA.match(linha) or _LINHA_CHAVE.match(linha)
        if achado:
            chave = _normalizar(achado.group(1))
            valor = achado.group(2).strip().strip("`").strip()
            if chave and valor and not set(valor) <= set("-: "):
                ficha.setdefault(chave, valor)
    ficha["_pasta_cliente"] = str(cliente)
    return ficha


def pegar(ficha, chave, padrao=None):
    """Value of the key (ignoring accents and case) or the default."""
    return ficha.get(_normalizar(chave), padrao)


def pegar_cor(ficha, chave, padrao):
    """Card color in #RRGGBB format; a value outside the format is ignored and the default applies."""
    valor = pegar(ficha, chave)
    if valor and re.fullmatch(r"#[0-9a-fA-F]{6}", valor.strip()):
        return valor.strip()
    return padrao


def cor_para_legenda(cor_rgb, transparencia="00"):
    """#RRGGBB -> ASS caption format (&HAABBGGRR), which uses blue-green-red order."""
    r, g, b = cor_rgb[1:3], cor_rgb[3:5], cor_rgb[5:7]
    return f"&H{transparencia}{b}{g}{r}".upper()


if __name__ == "__main__":
    ficha = ler(partida=sys.argv[1] if len(sys.argv) > 1 else ".")
    if not ficha:
        print("No client card found: the client folder has no `_DESIGN\\mapa.md` (or the delivery is outside the client folder).")
        sys.exit(1)
    print("Client:", ficha.pop("_pasta_cliente"))
    for chave, valor in ficha.items():
        print(f"  {chave}: {valor}")
