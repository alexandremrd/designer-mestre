#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
consent.py - The user's one-time yes per capability, recorded once and valid across every AI that uses the skill.

The user approves a capability (local engine, partner AI, connector/MCP) only once; the approval is kept in
%USERPROFILE%\\.consentimentos-ia.json, outside any skill (an update does not erase it) and read by all AIs
(Claude, Gemini, Codex...). After that the capability runs silently. A paid account enters here only within what the
user has already contracted (conta_paga.<name>); going beyond the contract or a usage-billed API without a free tier is never recorded:
it asks for a yes at each generation, with the warning from the `overage` command (`operations.md` §0.6, Spending).

Commands (exit code: 0 = approved, 3 = no approval):
  python consent.py view <capability>
  python consent.py register <capability> [--note "what the user approved"]
  python consent.py revoke <capability>
  python consent.py list
  python consent.py overage <provider> "<estimated cost>"   (question text for each generation; nothing is recorded)
Capabilities used by the skill: local_engine.instalar, local_engine.usar, ia_parceira.<name> (e.g. ia_parceira.codex),
conector.<name> (e.g. conector.adobe), conta_paga.<name> (e.g. conta_paga.elevenlabs, only within the contract).
"""
import argparse, json, os, sys, time

ARQ = os.path.join(os.path.expanduser("~"), ".consentimentos-ia.json")


def ler(estrito=False):
    if not os.path.exists(ARQ):
        return {}
    try:
        with open(ARQ, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        # file exists but cannot be read: whoever writes cannot proceed, otherwise it erases the existing approvals
        if estrito:
            sys.exit(f"[error] {ARQ} unreadable; nothing was written so as not to erase the existing approvals; "
                     "fix or move the file")
        return {}


def aprovado(cap):
    return cap in ler()


def gravar(d):
    # write to .tmp and swap, so a crash midway does not truncate the approvals file
    with open(ARQ + ".tmp", "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(ARQ + ".tmp", ARQ)


def registrar(cap, nota=""):
    d = ler(estrito=True)
    d[cap] = {"data": time.strftime("%Y-%m-%d %H:%M"), "nota": nota}
    gravar(d)


def main():
    ap = argparse.ArgumentParser(description="The user's one-time yes per capability")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("view", "register", "revoke"):
        p = sub.add_parser(c)
        p.add_argument("capacidade")
        if c == "register":
            p.add_argument("--note", dest="nota", default="")
    sub.add_parser("list")
    e = sub.add_parser("overage")
    e.add_argument("provedor")
    e.add_argument("custo")
    a = ap.parse_args()
    if a.cmd == "overage":
        print(f"QUESTION (at each generation, never recorded): This generation is not covered by what you have already contracted "
              f"with {a.provedor}. It will be billed by {a.provedor} itself, to your account, and not by the skill: estimated "
              f"cost {a.custo}. May I generate this (1) image?")
    elif a.cmd == "list":
        for k, v in ler().items():
            print(f"{k}: approved on {v['data']} {v.get('nota') or ''}")
    elif a.cmd == "view":
        if aprovado(a.capacidade):
            print(f"[approved] {a.capacidade}")
        else:
            print(f"[no-approval] {a.capacidade}: ask the user once; with the yes, "
                  f"run: consent.py register {a.capacidade}")
            sys.exit(3)
    elif a.cmd == "register":
        registrar(a.capacidade, a.nota)
        print(f"[ok] {a.capacidade} approved and recorded in {ARQ}")
    else:
        d = ler(estrito=True)
        d.pop(a.capacidade, None)
        gravar(d)
        print(f"[ok] {a.capacidade} revoked")


if __name__ == "__main__":
    main()
