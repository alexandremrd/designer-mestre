#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
consentimento.py - Sim unico do usuario por capacidade, gravado uma vez e valido em toda IA que use a skill.

O usuario aprova uma capacidade (motor local, IA parceira, conector/MCP) uma unica vez; o aval fica em
%USERPROFILE%\\.consentimentos-ia.json, fora de qualquer skill (atualizacao nao apaga) e lido por todas as IAs
(Claude, Gemini, Codex...). Depois disso a capacidade roda em silencio. Conta paga entra aqui so dentro do que o
usuario ja contratou (conta_paga.<nome>); passar do contratado ou API cobrada por uso sem franquia nunca e gravado:
pede sim a cada geracao, com o aviso do comando `excedente` (SKILL.md §0.6, Gasto).

Comandos (codigo de saida: 0 = aprovado, 3 = sem aval):
  python consentimento.py ver <capacidade>
  python consentimento.py registrar <capacidade> [--nota "o que o usuario aprovou"]
  python consentimento.py revogar <capacidade>
  python consentimento.py listar
  python consentimento.py excedente <provedor> "<custo estimado>"   (texto da pergunta a cada geracao; nada e gravado)
Capacidades usadas pela skill: motor_local.instalar, motor_local.usar, ia_parceira.<nome> (ex.: ia_parceira.codex),
conector.<nome> (ex.: conector.adobe), conta_paga.<nome> (ex.: conta_paga.elevenlabs, so dentro do contratado).
"""
import argparse, json, os, sys, time

ARQ = os.path.join(os.path.expanduser("~"), ".consentimentos-ia.json")


def ler():
    try:
        return json.load(open(ARQ, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def aprovado(cap):
    return cap in ler()


def registrar(cap, nota=""):
    d = ler()
    d[cap] = {"data": time.strftime("%Y-%m-%d %H:%M"), "nota": nota}
    with open(ARQ, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)


def main():
    ap = argparse.ArgumentParser(description="Sim unico do usuario por capacidade")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("ver", "registrar", "revogar"):
        p = sub.add_parser(c)
        p.add_argument("capacidade")
        if c == "registrar":
            p.add_argument("--nota", default="")
    sub.add_parser("listar")
    e = sub.add_parser("excedente")
    e.add_argument("provedor")
    e.add_argument("custo")
    a = ap.parse_args()
    if a.cmd == "excedente":
        print(f"PERGUNTA (a cada geracao, nunca gravada): Esta geracao nao esta coberta pelo que voce ja contratou "
              f"no {a.provedor}. Ela sera cobrada pelo proprio {a.provedor}, na sua conta, e nao pela skill: custo "
              f"estimado {a.custo}. Posso gerar esta (1) imagem?")
    elif a.cmd == "listar":
        for k, v in ler().items():
            print(f"{k}: aprovado em {v['data']} {v.get('nota') or ''}")
    elif a.cmd == "ver":
        if aprovado(a.capacidade):
            print(f"[aprovado] {a.capacidade}")
        else:
            print(f"[sem-aval] {a.capacidade}: perguntar 1 vez ao usuario; com o sim, "
                  f"rodar: consentimento.py registrar {a.capacidade}")
            sys.exit(3)
    elif a.cmd == "registrar":
        registrar(a.capacidade, a.nota)
        print(f"[ok] {a.capacidade} aprovado e gravado em {ARQ}")
    else:
        d = ler()
        d.pop(a.capacidade, None)
        with open(ARQ, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print(f"[ok] {a.capacidade} revogado")


if __name__ == "__main__":
    main()
