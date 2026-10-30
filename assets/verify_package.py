#!/usr/bin/env python3
"""Checks whether the skill package is ready to go to Git: universal, with nothing from a client and no generated file.

Run before any `git add` or publication (the rule is in `MAINTENANCE.md`). Failed = do not publish.

What it checks:
  1. Client name: the names come from the folders in `D:\\Clientes` (or the path given in --clients), so the skill does not need
     to store any name. Searches for each one in the package text, ignoring third-party code and reference data.
  2. Generated file: folders and files that are born inside a delivery (Trabalho, Aprovação, Exportados, _DESIGN, videos, zips).
  3. Dated episode inside a rule: dates (dd/mm/yyyy) in core, modules and shortcuts. A date belongs to the history, not to the rule.
  4. Lean Laws: each Law in `SKILL.md` must be a short principle; procedure goes to the owning module.
  5. `.gitignore`: must not block the template `Clientes\\_CLIENT_TEMPLATE`, which the skill must ship.
  6. Control character in the text: a backslash path that turned into `\\f`, `\\v` or `\\a` when written.
  7. Open skills standard (agentskills.io): valid `name` equal to the folder, `description` up to 1024, up to 500 lines, uppercase `SKILL.md`.

Usage:
    python verify_package.py [--clients "D:\\Clientes"]
"""
import argparse
import os
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
IGNORAR_PASTAS = {"node_modules", ".git", "__pycache__"}
# third-party code and data: their text is not ours and may contain common words
TERCEIROS = [("engines", "uiux"), ("engines", "designlang"), ("engines", "reel"), ("figma_engine",),
             ("references", "taste"), ("references", "motion"), ("references", "logo"), ("references", "huashu"),
             ("references", "design_skills"), ("assets", "taste"), ("assets", "huashu"), ("assets", "logo")]
EXT_TEXTO = {".md", ".py", ".ps1", ".mjs", ".cjs", ".js", ".json", ".html", ".css", ".cmd", ".txt", ".csv"}
ARQUIVOS_DE_REGRA = ["SKILL.md", "delivery.md", "standards.md", "operations.md"]
GERADOS_PASTAS = {"Trabalho", "Aprovação", "Exportados", "_DESIGN", "Compartilhada", "output"}
GERADOS_EXT = {".mp4", ".mov", ".zip", ".psd", ".ai", ".docx", ".pdf"}
DATA = re.compile(r"\b[0-3]?\d/[01]?\d/20\d\d\b")
LIMITE_LEI = 600  # characters per Law
CONTROLE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")  # \f, \v, \a... that a badly written backslash path leaves in the text


def em_terceiros(rel):
    return any(rel.parts[:len(t)] == t for t in TERCEIROS)


def arquivos_texto():
    for dp, dn, fn in os.walk(RAIZ):
        dn[:] = [d for d in dn if d not in IGNORAR_PASTAS]
        for f in fn:
            p = pathlib.Path(dp) / f
            if p.suffix.lower() in EXT_TEXTO:
                yield p, p.relative_to(RAIZ)


def nomes_de_clientes(pasta):
    pasta = pathlib.Path(pasta)
    if not pasta.is_dir():
        return None
    nomes = [d.name for d in pasta.iterdir() if d.is_dir() and not d.name.startswith(("_", "."))]
    return [n for n in nomes if len(n) >= 3]


def principal():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clients", dest="clientes", default=r"D:\Clientes", help="folder where the client folders live")
    ap.add_argument("--ignore", dest="ignorar", nargs="*", default=[], help="client names that are also common words in the package, for this run only")
    a = ap.parse_args()
    falhas = []

    # 1. client names
    nomes = nomes_de_clientes(a.clientes)
    if nomes is None:
        print(f"WARNING: clients folder not found ({a.clientes}); the name check was skipped.")
    else:
        nomes = [n for n in nomes if n.lower() not in {x.lower() for x in a.ignorar}]
        # a single-word name matches only the exact spelling of the folder (avoids confusing a client with the common word spelled the same);
        # a multi-word name matches case-insensitively
        padroes = [(n, re.compile(r"(?<![\w])" + r"\s+".join(map(re.escape, n.split())) + r"(?![\w])", 0 if len(n.split()) == 1 else re.I)) for n in nomes]
        for p, rel in arquivos_texto():
            if em_terceiros(rel):
                continue
            try:
                texto = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for n, rx in padroes:
                m = rx.search(texto)
                if m:
                    linha = texto.count("\n", 0, m.start()) + 1
                    falhas.append(f"client name in {rel}:{linha}")
                    break

    # 1b. control character (backslash path that turned into \f, \v or \a when written)
    for p, rel in arquivos_texto():
        if em_terceiros(rel):
            continue
        try:
            texto = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        m = CONTROLE.search(texto)
        if m:
            falhas.append(f"control character in {rel}:{texto.count(chr(10), 0, m.start()) + 1} (badly written backslash)")

    # 2. generated file
    for dp, dn, fn in os.walk(RAIZ):
        dn[:] = [d for d in dn if d not in IGNORAR_PASTAS]
        rel_dir = pathlib.Path(dp).relative_to(RAIZ)
        if em_terceiros(rel_dir):
            dn[:] = []
            continue
        for d in dn:
            if d in GERADOS_PASTAS or d.startswith("_legado"):
                falhas.append(f"generated folder inside the package: {rel_dir / d}")
        for f in fn:
            if pathlib.Path(f).suffix.lower() in GERADOS_EXT and not em_terceiros(rel_dir / f):
                falhas.append(f"generated file inside the package: {rel_dir / f}")

    # 3. dated episode in the rules
    regras = [RAIZ / f for f in ARQUIVOS_DE_REGRA] + sorted((RAIZ / "modules").glob("*.md")) + sorted((RAIZ / "shortcuts").glob("*/SKILL.md"))
    for p in regras:
        if p.is_file():
            for i, linha in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if DATA.search(linha):
                    falhas.append(f"date in a rule (goes to EVOLUTION.md): {p.relative_to(RAIZ)}:{i}")

    # 4. Lean Laws
    nucleo = (RAIZ / "SKILL.md").read_text(encoding="utf-8")
    bloco = re.search(r"## 4\. Laws.*?(?=\n## )", nucleo, re.S)
    if bloco:
        for linha in bloco.group(0).splitlines():
            if re.match(r"\d+\. \*\*", linha) and len(linha) > LIMITE_LEI:
                falhas.append(f"Law too long ({len(linha)} characters; limit {LIMITE_LEI}): {linha[:50]}...")

    # 5. .gitignore
    gi = RAIZ / ".gitignore"
    if gi.is_file():
        linhas = [l.strip() for l in gi.read_text(encoding="utf-8-sig").splitlines()]
        if "Clients/" in linhas or "Clients" in linhas:
            falhas.append(".gitignore blocks the whole Clients/ and hides the _CLIENT_TEMPLATE template")
        elif "!Clients/_CLIENT_TEMPLATE/" not in linhas:
            falhas.append(".gitignore does not unblock Clients/_CLIENT_TEMPLATE/")

    # 6. open skills standard (agentskills.io): name, description, size and file case, so every agent can read the skill
    for p in [RAIZ / "SKILL.md"] + sorted((RAIZ / "atalhos").glob("*/SKILL.md")):
        rel = p.relative_to(RAIZ)
        texto = p.read_text(encoding="utf-8-sig", errors="replace")
        fm = re.match(r"---\r?\n(.*?)\r?\n---", texto, re.S)
        if not fm:
            falhas.append(f"{rel}: no YAML frontmatter")
            continue
        nome = re.search(r'(?m)^name:\s*"?([^"\r\n]+)"?', fm.group(1))
        desc = re.search(r'(?m)^description:\s*"?(.+?)"?\s*$', fm.group(1))
        nome = nome.group(1).strip() if nome else ""
        desc = desc.group(1) if desc else ""
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", nome) or len(nome) > 64:
            falhas.append(f"{rel}: invalid name ({nome!r}): lowercase, digits and hyphens, up to 64, no leading, trailing or double hyphen")
        if p.parent != RAIZ and nome != p.parent.name:
            falhas.append(f"{rel}: name ({nome}) differs from the folder ({p.parent.name})")
        if not desc or len(desc) > 1024 or re.search(r"<[a-zA-Z/]", desc):
            falhas.append(f"{rel}: description empty, above 1024 characters or with an XML tag ({len(desc)})")
        if len(texto.splitlines()) > 500:
            falhas.append(f"{rel}: more than 500 lines; move the detail to a support file")
        if p.name != "SKILL.md":
            falhas.append(f"{rel}: the file must be named SKILL.md (uppercase; Gemini CLI requires it)")

    if falhas:
        print(f"{len(falhas)} problem(s):")
        for f in falhas:
            print(" -", f)
        sys.exit(1)
    print("universal package: no client name, no generated file, rules without dates, lean Laws, correct .gitignore, frontmatter in the open standard")


if __name__ == "__main__":
    principal()
