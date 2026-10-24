#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
motor_local.py - Analisa o PC, instala e controla o motor local de imagem do /designer-mestre (ComfyUI sem interface).

Quem instala e opera e a IA; o usuario so da o aval, uma unica vez (consentimento.py). O ComfyUI roda so como
servidor (API em http://127.0.0.1:8188), sem abrir navegador nem app; quem comanda e o gerar_imagem.py.
Instala fora da pasta da skill, baixando apenas de fontes oficiais (GitHub do ComfyUI, PyTorch, Hugging Face).
A pasta fica em %USERPROFILE%\\.designer-mestre\\motor_local.json, que atualizacoes da skill nao apagam.

Comandos:
  python motor_local.py guia                     (roteiro da IA: analisar, perguntar 1 vez, instalar, operar)
  python motor_local.py detectar                 (analisa o PC e recomenda; traz a pergunta pronta para o usuario)
  python motor_local.py instalar [--pasta X]     (sem --sim so mostra o plano; com --sim instala e grava o aval)
  python motor_local.py iniciar | parar | status | modelos
"""
import argparse, io, json, os, shutil, subprocess, sys, time, zipfile
import urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import consentimento

CFG = os.path.join(os.path.expanduser("~"), ".designer-mestre", "motor_local.json")
URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188").rstrip("/")
REPO = "https://github.com/comfyanonymous/ComfyUI"
HF = "https://huggingface.co"
PY_OK = ((3, 10), (3, 13))  # versoes com PyTorch CUDA publicado
EXTRA_GB = 6  # PyTorch + dependencias + folga

# Catalogo: so arquivos com licenca conferida no repositorio de onde cada um e baixado (nao so no modelo):
# o mesmo nome de arquivo pode existir em repositorio de licenca diferente. (pasta em models\, arquivo, url)
MODELOS = {
    "klein4b": {
        "nome": "FLUX.2 klein 4B fp8 (destilado, 4 passos, multirreferencia)",
        "licenca": "Apache 2.0 em todos os arquivos (uso comercial)", "vram_min_gb": 8, "download_gb": 7.7,
        "arquivos": [
            ("diffusion_models", "flux-2-klein-4b-fp8.safetensors",
             f"{HF}/black-forest-labs/FLUX.2-klein-4b-fp8/resolve/main/flux-2-klein-4b-fp8.safetensors"),
            ("text_encoders", "qwen_3_4b_fp4_flux2.safetensors",
             f"{HF}/Comfy-Org/flux2-klein-4B/resolve/main/split_files/text_encoders/qwen_3_4b_fp4_flux2.safetensors"),
            ("vae", "flux2-vae-klein4b.safetensors",
             f"{HF}/Comfy-Org/flux2-klein-4B/resolve/main/split_files/vae/flux2-vae.safetensors"),
        ],
    },
}

GUIA = """ROTEIRO DA IA - motor local de imagem (o usuario so da o aval; a IA faz todo o resto)
1. Antes de oferecer: `motor_local.py detectar`. Ele analisa GPU, VRAM, RAM, disco, Python e o que ja existe,
   e diz se o PC aguenta, qual modelo cabe e a pergunta pronta. PC sem condicao = nao oferecer o motor local.
2. Aval unico: `consentimento.py ver motor_local.usar`. Aprovado = seguir em silencio. Sem aval = fazer a
   pergunta do `detectar` UMA vez, na ferramenta de perguntas, em portugues simples (o que e, espaco, tempo,
   custo zero, como remover). Recusou = seguir com outro gerador e nao perguntar de novo nesta sessao.
3. Instalar (so com o sim): `motor_local.py instalar --pasta <sugerida> --sim`, em segundo plano. Ele grava o
   aval de instalar e de usar, entao nao se pergunta de novo. Enquanto baixa, avisar o usuario em 1 linha por etapa
   (baixando o motor / os modelos / pronto). Erro: ler a mensagem [falta]/[erro], resolver voce mesmo o que for
   resolvivel (ex.: rodar de novo retoma o download) e so envolver o usuario se precisar de um novo sim.
4. Usar: `gerar_imagem.py gerar ... --motor comfy` liga o motor sozinho se estiver parado.
   Manter ligado durante as rodadas; `motor_local.py parar` so depois da aprovacao final da peca.
5. Remover (se o usuario pedir): `motor_local.py parar`, apagar a pasta instalada (confirmar antes) e
   `consentimento.py revogar motor_local.usar`.
"""


def cfg_ler():
    try:
        return json.load(open(CFG, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def cfg_gravar(d):
    os.makedirs(os.path.dirname(CFG), exist_ok=True)
    json.dump(d, open(CFG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def py_venv(pasta):
    return os.path.join(pasta, "venv", "Scripts" if os.name == "nt" else "bin",
                        "python.exe" if os.name == "nt" else "python")


def rodando(timeout=3):
    try:
        with urllib.request.urlopen(URL + "/system_stats", timeout=timeout) as r:
            return json.loads(r.read())
    except (urllib.error.URLError, OSError, ValueError):
        return None


def run(cmd, **kw):
    print("  >", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, **kw)
    if r.returncode:
        sys.exit(f"[erro] comando falhou ({r.returncode}): {' '.join(cmd)}\n"
                 "  Rodar instalar --sim de novo retoma de onde parou.")


def baixar(url, destino):
    """Download com retomada (.part) e progresso; pula arquivo ja completo."""
    if os.path.isfile(destino):
        print(f"  [ja existe] {os.path.basename(destino)}")
        return
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    part = destino + ".part"
    for tentativa in range(5):
        feito = os.path.getsize(part) if os.path.isfile(part) else 0
        r = urllib.request.Request(url, headers={"Range": f"bytes={feito}-"} if feito else {})
        try:
            with urllib.request.urlopen(r, timeout=60) as resp, open(part, "ab" if feito else "wb") as f:
                if feito and resp.status != 206:
                    f.truncate(0); feito = 0
                total = feito + int(resp.headers.get("Content-Length") or 0)
                t0, ult = time.time(), 0
                while True:
                    bloco = resp.read(1 << 20)
                    if not bloco:
                        break
                    f.write(bloco); feito += len(bloco)
                    if time.time() - ult > 5:
                        ult = time.time()
                        vel = (feito / (1 << 20)) / max(ult - t0, 1)
                        print(f"  {os.path.basename(destino)}: {feito / 2**30:.2f}/{total / 2**30:.2f} GB"
                              f" ({vel:.0f} MB/s)", flush=True)
            os.replace(part, destino)
            print(f"  [ok] {os.path.basename(destino)}")
            return
        except (urllib.error.URLError, OSError) as e:
            print(f"  [retomando {tentativa + 1}/5] {e}", flush=True)
            time.sleep(5)
    sys.exit(f"[erro] download falhou: {url}\n  Rodar instalar --sim de novo retoma o download.")


def gpu():
    """(nome, vram_gb) da GPU NVIDIA, ou (None, 0)."""
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=20).stdout.strip().splitlines()
        nome, mib = out[0].rsplit(",", 1)
        return nome.strip(), int(mib) / 1024
    except (OSError, subprocess.TimeoutExpired, ValueError, IndexError):
        return None, 0


def ram_gb():
    try:
        if os.name == "nt":
            import ctypes
            class M(ctypes.Structure):
                _fields_ = [("l", ctypes.c_ulong), ("p", ctypes.c_ulong), ("t", ctypes.c_ulonglong),
                            ("a", ctypes.c_ulonglong)] + [(f"x{i}", ctypes.c_ulonglong) for i in range(5)]
            m = M(); m.l = ctypes.sizeof(M)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return m.t / 2**30
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2**30
    except (OSError, ValueError, AttributeError):
        return 0


def python_ok():
    """Caminho de um Python com PyTorch CUDA publicado: o atual ou um do lancador py."""
    if PY_OK[0] <= sys.version_info[:2] <= PY_OK[1]:
        return sys.executable
    if shutil.which("py"):
        for v in ("3.13", "3.12", "3.11"):
            r = subprocess.run(["py", f"-{v}", "-c", "import sys;print(sys.executable)"], capture_output=True, text=True)
            if r.returncode == 0:
                return r.stdout.strip()
    return None


def discos():
    out = []
    for letra in "CDEFGHIJ":
        raiz = f"{letra}:\\"
        if os.path.exists(raiz):
            try:
                out.append((letra, shutil.disk_usage(raiz).free / 2**30))
            except OSError:
                pass
    return sorted(out, key=lambda x: -x[1])


def analisar():
    """Diagnostico completo; nada e baixado."""
    nome, vram = gpu()
    ram, py, ds = ram_gb(), python_ok(), discos()
    m = MODELOS["klein4b"]
    precisa = m["download_gb"] + EXTRA_GB
    c = cfg_ler()
    inst = c.get("pasta") and os.path.isfile(py_venv(c["pasta"]))
    d = {"gpu": nome, "vram_gb": round(vram, 1), "ram_gb": round(ram, 1), "python": py, "git": bool(shutil.which("git")),
         "discos": ds, "instalado": c.get("pasta") if inst else None, "rodando": bool(rodando()),
         "precisa_gb": round(precisa, 1), "faltas": [], "avisos": []}
    if not nome:
        d["faltas"].append("sem GPU NVIDIA: o motor local ficaria lento demais; usar outro gerador")
    elif vram < m["vram_min_gb"] - 0.5:
        d["faltas"].append(f"GPU com {vram:.0f} GB de VRAM; o modelo pede {m['vram_min_gb']} GB; usar outro gerador")
    if ram and ram < 15:
        d["avisos"].append(f"{ram:.0f} GB de RAM: funciona, mas mais lento (ideal 16 GB)")
    if not py:
        d["avisos"].append("sem Python 3.10-3.13: a IA instala o Python 3.12 oficial antes (winget) com o mesmo aval")
    if not ds or ds[0][1] < precisa:
        d["faltas"].append(f"nenhum disco com {precisa:.0f} GB livres")
    d["pasta_sugerida"] = c.get("pasta") or (f"{ds[0][0]}:\\IA\\ComfyUI" if ds else None)
    d["recomendado"] = None if d["faltas"] else "klein4b"
    return d


def pergunta(d):
    m = MODELOS["klein4b"]
    return (f"Posso instalar o gerador de imagens local no seu PC? Ele roda na sua placa de video ({d['gpu']}), "
            f"sem custo por imagem e sem abrir nenhum programa: eu instalo e comando tudo. Ocupa ~{d['precisa_gb']:.0f} GB "
            f"em {d['pasta_sugerida']}, leva ~15-30 min para baixar (uma vez so) e gera cada imagem em ~1 min. "
            f"Modelo {m['nome'].split(' (')[0]}, licenca {m['licenca']}. Voce pode pedir para remover quando quiser.")


def cmd_guia(_):
    print(GUIA)


def cmd_detectar(_):
    d = analisar()
    print(f"GPU: {d['gpu'] or 'nenhuma NVIDIA'} · VRAM {d['vram_gb']} GB · RAM {d['ram_gb']} GB")
    print("discos: " + ", ".join(f"{l}: {g:.0f} GB livres" for l, g in d["discos"]))
    print(f"python compativel: {d['python'] or 'nao'} · git: {'sim' if d['git'] else 'nao (baixa o zip oficial)'}")
    print(f"instalado: {d['instalado'] or 'nao'} · rodando: {'sim' if d['rodando'] else 'nao'}")
    for a in d["avisos"]:
        print(f"[aviso] {a}")
    if d["faltas"]:
        for f in d["faltas"]:
            print(f"[nao-recomendado] {f}")
        return
    aval = consentimento.aprovado("motor_local.usar")
    if d["instalado"]:
        print("[pronto] motor instalado" + (" e aprovado: usar em silencio" if aval else
              "; sem aval de uso: perguntar 1 vez e registrar motor_local.usar"))
    else:
        print(f"[recomendado] klein4b em {d['pasta_sugerida']}")
        if not aval:
            print(f"PERGUNTA (1 vez, ferramenta de perguntas): {pergunta(d)}")
        print(f"COM O SIM: motor_local.py instalar --pasta \"{d['pasta_sugerida']}\" --sim")


def obter_codigo(pasta):
    if os.path.isdir(os.path.join(pasta, ".git")) and shutil.which("git"):
        run(["git", "-C", pasta, "pull", "--ff-only"])
    elif shutil.which("git") and not os.path.exists(pasta):
        run(["git", "clone", "--depth", "1", REPO + ".git", pasta])
    elif not os.path.isfile(os.path.join(pasta, "main.py")):
        print("  git ausente: baixando o zip oficial do GitHub", flush=True)
        with urllib.request.urlopen(REPO + "/archive/refs/heads/master.zip", timeout=120) as r:
            z = zipfile.ZipFile(io.BytesIO(r.read()))
        raiz = z.namelist()[0].split("/")[0]
        for item in z.infolist():
            alvo = os.path.join(pasta, item.filename[len(raiz) + 1:])
            if item.is_dir():
                os.makedirs(alvo, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(alvo), exist_ok=True)
                with open(alvo, "wb") as f:
                    f.write(z.read(item))


def cmd_instalar(a):
    d = analisar()
    pasta = os.path.abspath(a.pasta or d["pasta_sugerida"] or "")
    if not a.sim:
        print("PLANO (nada foi baixado):")
        print(f"  pasta: {pasta} · ~{d['precisa_gb']:.0f} GB · ~15-30 min · modelo {MODELOS[a.modelo]['nome']}")
        print(f"  licenca: {MODELOS[a.modelo]['licenca']} · fontes: GitHub ComfyUI, PyTorch, Hugging Face")
        for f in d["faltas"]:
            print(f"  [nao-recomendado] {f}")
        print(f"PERGUNTA (1 vez): {pergunta(d)}" if not d["faltas"] else "")
        print("COM O SIM: repetir com --sim")
        return
    if d["faltas"] and not a.forcar:
        sys.exit("[nao-recomendado] " + "; ".join(d["faltas"]))
    if os.path.abspath(os.path.dirname(__file__)).lower() in pasta.lower():
        sys.exit("[erro] instale fora da pasta da skill (atualizacoes a sobrescrevem).")
    py = d["python"]
    if not py:
        print("[0/4] Python 3.12 oficial (winget)")
        run(["winget", "install", "-e", "--id", "Python.Python.3.12", "--silent",
             "--accept-package-agreements", "--accept-source-agreements"])
        py = python_ok() or sys.exit("[falta] Python 3.12 instalado, mas nao encontrado: reabrir o terminal e repetir.")
    consentimento.registrar("motor_local.instalar", f"pasta {pasta}")
    consentimento.registrar("motor_local.usar", "aval dado junto com a instalacao")
    os.makedirs(os.path.dirname(pasta) or pasta, exist_ok=True)
    print("[1/4] baixando o motor (ComfyUI, GitHub oficial)", flush=True)
    obter_codigo(pasta)
    print("[2/4] preparando o ambiente (Python isolado + PyTorch CUDA)", flush=True)
    vpy = py_venv(pasta)
    if not os.path.isfile(vpy):
        run([py, "-m", "venv", os.path.join(pasta, "venv")])
    run([vpy, "-m", "pip", "install", "--upgrade", "pip", "-q"])
    run([vpy, "-m", "pip", "install", "torch", "torchvision", "torchaudio", "-q",
         "--index-url", f"https://download.pytorch.org/whl/{a.torch}"])
    run([vpy, "-m", "pip", "install", "-r", os.path.join(pasta, "requirements.txt"), "-q"])
    print(f"[3/4] baixando os modelos: {MODELOS[a.modelo]['nome']} · {MODELOS[a.modelo]['licenca']}", flush=True)
    for sub, nome, url in MODELOS[a.modelo]["arquivos"]:
        baixar(url, os.path.join(pasta, "models", sub, nome))
    print("[4/4] pronto", flush=True)
    c = cfg_ler()
    c.update({"pasta": pasta, "modelo": a.modelo, "instalado_em": time.strftime("%Y-%m-%d %H:%M")})
    cfg_gravar(c)
    print(f"[ok] motor local instalado em {pasta}; o gerar_imagem.py liga sozinho quando precisar.")


def cmd_iniciar(a):
    if rodando():
        print(f"[ok] ja rodando em {URL}")
        return
    pasta = cfg_ler().get("pasta")
    if not pasta or not os.path.isfile(py_venv(pasta)):
        sys.exit("[nao-instalado] motor local ausente. Ver: motor_local.py guia")
    porta = URL.rsplit(":", 1)[-1]
    log = open(os.path.join(pasta, "motor.log"), "w", encoding="utf-8")
    flags = (subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW) \
        if os.name == "nt" else 0
    cmd = [py_venv(pasta), "main.py", "--listen", "127.0.0.1", "--port", porta, "--disable-auto-launch"] + a.extra
    p = subprocess.Popen(cmd, cwd=pasta, stdout=log, stderr=subprocess.STDOUT, creationflags=flags)
    c = cfg_ler(); c["pid"] = p.pid; cfg_gravar(c)
    for _ in range(a.espera):
        if rodando():
            print(f"[ok] motor local no ar em {URL} (pid {p.pid}, log {pasta}\\motor.log)")
            return
        if p.poll() is not None:
            sys.exit(f"[erro] motor encerrou ao iniciar; ver {pasta}\\motor.log")
        time.sleep(1)
    sys.exit(f"[erro] motor nao respondeu em {a.espera}s; ver {pasta}\\motor.log")


def cmd_parar(_):
    c = cfg_ler()
    pid = c.pop("pid", None)
    if pid:
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"] if os.name == "nt" else ["kill", str(pid)],
                       capture_output=True)
        cfg_gravar(c)
    print("[ok] motor parado" if not rodando(1) else "[aviso] ainda responde; pode ter sido iniciado por outro processo")


def cmd_status(_):
    s = rodando()
    if not s:
        print(f"[parado] {URL}  instalado: {cfg_ler().get('pasta', 'nao')}")
        return
    for d in s.get("devices", []):
        print(f"[rodando] {URL} · {d.get('name')} · VRAM livre {d.get('vram_free', 0) / 2**30:.1f}"
              f"/{d.get('vram_total', 0) / 2**30:.1f} GB")


def cmd_modelos(_):
    pasta = cfg_ler().get("pasta")
    for k, m in MODELOS.items():
        ok = pasta and all(os.path.isfile(os.path.join(pasta, "models", s, n)) for s, n, _ in m["arquivos"])
        print(f"{k}: {m['nome']} · {m['licenca']} · VRAM >= {m['vram_min_gb']} GB · {m['download_gb']} GB"
              f" · {'baixado' if ok else 'nao baixado'}")


def main():
    ap = argparse.ArgumentParser(description="Motor local (ComfyUI sem interface) do /designer-mestre")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("guia").set_defaults(f=cmd_guia)
    sub.add_parser("detectar").set_defaults(f=cmd_detectar)
    i = sub.add_parser("instalar")
    i.add_argument("--pasta", help="padrao: disco com mais espaco livre, <disco>:\\IA\\ComfyUI")
    i.add_argument("--sim", action="store_true", help="o usuario aprovou; sem isto so mostra o plano")
    i.add_argument("--forcar", action="store_true", help="instalar mesmo com hardware abaixo do recomendado")
    i.add_argument("--modelo", default="klein4b", choices=list(MODELOS))
    i.add_argument("--torch", default="cu128", help="indice do PyTorch (cu128 cobre RTX 50xx)")
    i.set_defaults(f=cmd_instalar)
    s = sub.add_parser("iniciar")
    s.add_argument("--espera", type=int, default=180)
    s.add_argument("--extra", type=str.split, default=[], help='flags extras do ComfyUI (ex.: --extra="--lowvram")')
    s.set_defaults(f=cmd_iniciar)
    sub.add_parser("parar").set_defaults(f=cmd_parar)
    sub.add_parser("status").set_defaults(f=cmd_status)
    sub.add_parser("modelos").set_defaults(f=cmd_modelos)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
