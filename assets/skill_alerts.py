#!/usr/bin/env python3
"""Skill alerts: what needs your attention, in up to 4 lines. Silence when there is nothing.

Why it exists: `EVOLUTION.md` is only read when someone calls it, so pending items and package failures stayed invisible. This script
gathers, in one place, what deserves a warning at the end of the session:
  1. open pending items in `EVOLUTION.md` (lines `- [ ] YYYY-MM-DD · priority · item · who decides`), with the overdue ones
     (open for more than 14 days) highlighted;
  2. `verify_package.py` failure (client name, generated file, date in a rule, long Law, `.gitignore`);
  3. incomplete client card (with `--delivery`): no `_DESIGN\\mapa.md`, no `Fonts` or no `Client code`.

Usage (at the end of the session, after the final approval of all tasks, and before /aprenda if it was cited; show the user what it prints, in one sentence):
    python skill_alerts.py [--delivery "<delivery folder>"]
Never blocks: always ends with exit code 0.
"""
import argparse
import datetime
import pathlib
import re
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
VENCIDA_DIAS = 14
LINHA = re.compile(r"^- \[ \] (\d{4}-\d{2}-\d{2}) · (high|medium|low|alta|média|baixa) · (.+?)(?: · ([^·]+))?$")


def pendencias():
    arq = RAIZ / "EVOLUTION.md"
    if not arq.is_file():
        return []
    achadas = []
    for linha in arq.read_text(encoding="utf-8", errors="replace").splitlines():
        m = LINHA.match(linha.strip())
        if m:
            achadas.append((m.group(1), m.group(2), m.group(3).strip(), (m.group(4) or "").strip()))
    return achadas


def avisos_de_pendencias():
    abertas = pendencias()
    if not abertas:
        return []
    hoje = datetime.date.today()
    peso = {"high": 0, "medium": 1, "low": 2, "alta": 0, "média": 1, "baixa": 2}  # English and old Portuguese words
    abertas.sort(key=lambda p: (peso[p[1]], p[0]))
    vencidas = [p for p in abertas if (hoje - datetime.date.fromisoformat(p[0])).days > VENCIDA_DIAS]
    corta = lambda t: t if len(t) <= 80 else t[:80].rsplit(" ", 1)[0] + "…"
    topo = "; ".join(corta(p[2]) + (f" (decides: {p[3]})" if p[3] else "") for p in abertas[:2])
    texto = f"⚠️ `EVOLUTION.md`: {len(abertas)} open pending item(s)"
    if vencidas:
        texto += f", {len(vencidas)} overdue for more than {VENCIDA_DIAS} days"
    return [texto + f". Most urgent: {topo}."]


def avisos_do_pacote():
    verificador = AQUI / "verify_package.py"
    if not verificador.is_file():
        return []
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", str(verificador)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
    except (subprocess.TimeoutExpired, OSError):
        return ["⚠️ `verify_package.py` did not finish; run it by hand before publishing."]
    if r.returncode == 0:
        return []
    problemas = [l.strip("- ").strip() for l in r.stdout.splitlines() if l.startswith(" -")]
    return [f"⚠️ The skill package is not ready for Git ({len(problemas)} problem(s)): " + "; ".join(problemas[:2]) + "."]


def avisos_da_ficha(entrega):
    import client_card
    ficha = client_card.ler(partida=entrega)
    if not ficha:
        return ["⚠️ This client has no `_DESIGN\\mapa.md` (client card). The scripts use neutral font and color until it exists; template in `Clientes\\_CLIENT_TEMPLATE\\mapa.md`."]
    faltam = [c for c in ("Fonts", "Client code") if not client_card.pegar(ficha, c)]
    if faltam:
        return ["⚠️ Client card missing: " + ", ".join(faltam) + "."]
    return []


def principal():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--delivery", dest="entrega", help="delivery folder, to check the client card")
    a = ap.parse_args()
    linhas = avisos_de_pendencias() + avisos_do_pacote()
    if a.entrega:
        linhas += avisos_da_ficha(a.entrega)
    for l in linhas[:4]:
        print(l)


if __name__ == "__main__":
    principal()
