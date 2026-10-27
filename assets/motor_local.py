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
import recursos

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
1. Antes de oferecer: `motor_local.py detectar`. Ele analisa GPU, VRAM, RAM, disco, Python e os motores ja
   instalados no PC (ComfyUI em qualquer forma, Forge/A1111, Fooocus, InvokeAI, Easy Diffusion, Blender, ffmpeg),
   e diz se o PC aguenta, qual modelo cabe e a pergunta pronta. PC sem condicao = nao oferecer o motor local.
   Motor ja instalado = reaproveitar; nunca instalar uma segunda copia do mesmo motor.
   Raiz dos recursos: o usuario escolhe local e nome (perguntar 1 vez) -> `motores --pasta <local>`; ela tem
   as categorias Geradores, Ferramentas, Modelos e Cache (ver recursos.py). Tudo que a skill instalar, com aval, vai para a
   categoria certa dentro dela. Os existentes (geradores, navegador do Playwright, sharp, Whisper, caches uv/npm)
   vao com `organizar` (plano) e `organizar --sim` (com o sim): ele move, reescreve os caminhos em scripts e
   configs, manda copias duplicadas para a Lixeira e grava as variaveis do usuario dos caches compartilhados.
   Trocar nome/local depois: `motores --pasta <novo> --sim`. App instalado pelo Windows (Blender, ffmpeg,
   ComfyUI Desktop) fica onde esta. Scripts leem os caminhos em recursos.py, nunca caminho fixo.
   Antes do --sim (organizar ou motores): mostrar ao usuario a saida do plano item por item e esperar o sim,
   porque o aval do local ou da regra nao cobre a lista (copias vao para a Lixeira, caches mudam de disco).
   Se a mudanca tambem alterou scripts da skill, reinstalar a skill ANTES de mover: a copia antiga procura os
   recursos no lugar velho e quebra no meio do caminho.
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
6. Remover duplicata (so com o pedido do usuario), nesta ordem, porque a copia "sobrando" costuma ter
   arquivos e scripts que dependem dela:
   a. Procurar o caminho da duplicata em configs E em scripts da pasta-mae e vizinhas (.py .sh .cmd .bat .ps1
      .json .yaml); script que aponta para ela = redirecionar para a copia mantida antes de remover.
   b. Comparar models, custom_nodes, input, output e user: o que so existe na duplicata passa para a copia
      mantida sem sobrescrever; modelo com mesmo nome e tamanho diferente = perguntar.
   c. Motor parado; mandar a pasta para a Lixeira (recuperavel), nunca apagar de vez; conferir antes se a
      Lixeira do disco comporta o tamanho. Depois, `detectar` deve mostrar uma copia so.
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
    """Python do ComfyUI: venv proprio, .venv (Desktop/uv) ou python_embeded (pacote portatil, pasta irma)."""
    exe = "python.exe" if os.name == "nt" else "python"
    pasta_bin = "Scripts" if os.name == "nt" else "bin"
    for c in (os.path.join(pasta, "venv", pasta_bin, exe), os.path.join(pasta, ".venv", pasta_bin, exe),
              os.path.join(os.path.dirname(pasta), "python_embeded", exe), os.path.join(pasta, "python_embeded", exe)):
        if os.path.isfile(c):
            return c
    return os.path.join(pasta, "venv", pasta_bin, exe)


# Motores ja instalados por fora (para reaproveitar e nao duplicar): nome -> arquivos que marcam a pasta.
MARCAS = {
    "ComfyUI": ("main.py", "comfy", "nodes.py"),
    "Forge/A1111": ("webui.py", "modules", "launch.py"),
    "Fooocus": ("entry_with_update.py", "fooocus_version.py"),
    "InvokeAI": ("invokeai.yaml",),
    "Easy Diffusion": ("ui", "scripts", "Start Stable Diffusion UI.cmd"),
}
PULAR = {"windows", "$recycle.bin", "system volume information", "programdata", "node_modules", ".git",
         "venv", ".venv", "site-packages", "__pycache__", "appdata", "models", "output", "input", "custom_nodes"}


def _marca(pasta):
    try:
        nomes = set(os.listdir(pasta))
    except OSError:
        return None
    for motor, marcas in MARCAS.items():
        if all(m in nomes for m in marcas):
            return motor
    return None


def _varrer(raiz, prof, achados):
    motor = _marca(raiz)
    if motor:
        achados.setdefault(motor, set()).add(os.path.normpath(raiz))
        return
    if prof <= 0:
        return
    try:
        with os.scandir(raiz) as it:
            for e in it:
                if e.is_dir(follow_symlinks=False) and e.name.lower() not in PULAR:
                    _varrer(e.path, prof - 1, achados)
    except OSError:
        pass


def instalados():
    """Motores de imagem/3D/video ja presentes no PC. Varredura rasa (segundos), sem baixar nada."""
    casa = os.path.expanduser("~")
    loc, roam = os.environ.get("LOCALAPPDATA", ""), os.environ.get("APPDATA", "")
    achados = {}
    raizes = [(f"{l}:\\", 3) for l, _ in discos()] + [
        (casa, 3), (os.path.join(casa, "Documents"), 3), (os.path.join(casa, "pinokio", "api"), 3),
        (os.path.join(roam, "StabilityMatrix", "Packages"), 2), (os.path.join(loc, "Programs"), 3)]
    c = cfg_ler()
    if c.get("motores"):
        raizes.insert(0, (c["motores"], 2))
    if c.get("pasta"):
        raizes.insert(0, (c["pasta"], 0))
    for raiz, prof in raizes:
        if os.path.isdir(raiz):
            _varrer(raiz, prof, achados)
    # ComfyUI Desktop guarda o codigo no app e os dados em Documents\ComfyUI (com .venv)
    desk = os.path.join(loc, "Programs", "@comfyorgcomfyui-electron")
    if os.path.isdir(desk):
        achados.setdefault("ComfyUI Desktop", set()).add(desk)
    blender = shutil.which("blender")
    if not blender:
        import glob
        achados_b = sorted(glob.glob(r"C:\Program Files\Blender Foundation\Blender*\blender.exe")
                           + glob.glob(r"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe"))
        blender = achados_b[-1] if achados_b else None
    if blender:
        achados.setdefault("Blender", set()).add(blender)
    if shutil.which("ffmpeg"):
        achados.setdefault("ffmpeg", set()).add(shutil.which("ffmpeg"))
    return {k: sorted(v) for k, v in achados.items()}


def comfy_existente(achados):
    """Melhor ComfyUI ja instalado: o configurado, senao um com Python proprio pronto."""
    pastas = achados.get("ComfyUI", [])
    cfg = cfg_ler().get("pasta")
    if cfg and os.path.normpath(cfg) in pastas:
        return os.path.normpath(cfg)
    for p in pastas:
        if os.path.isfile(py_venv(p)):
            return p
    return pastas[0] if pastas else None


# So motores que vivem numa pasta propria podem ir para Motores\; app instalado pelo Windows (Blender em
# Program Files, ffmpeg no PATH, ComfyUI Desktop) quebra registro e atalhos se for movido.
MOVIVEIS = ("ComfyUI", "Forge/A1111", "Fooocus", "InvokeAI", "Easy Diffusion")


def dentro(p, raiz):
    p, raiz = os.path.normcase(os.path.abspath(p)), os.path.normcase(os.path.abspath(raiz))
    return p == raiz or p.startswith(raiz.rstrip("\\/") + os.sep)


def pastas_moviveis(achados):
    """Pasta a mover de cada motor: no ComfyUI portatil e a pasta-mae, que leva junto o python_embeded."""
    out = []
    for motor in MOVIVEIS:
        for p in achados.get(motor, []):
            mae = os.path.dirname(p)
            out.append(mae if os.path.isdir(os.path.join(mae, "python_embeded")) else p)
    return list(dict.fromkeys(out))


def cmd_motores(a):
    c = cfg_ler()
    if not a.pasta:
        print(f"pasta raiz dos recursos: {c.get('motores') or 'nao definida (perguntar ao usuario)'}")
        return
    pasta = os.path.abspath(a.pasta)
    if os.path.abspath(os.path.dirname(__file__)).lower() in pasta.lower():
        sys.exit("[erro] a pasta raiz fica fora da pasta da skill (atualizacoes a sobrescrevem).")
    antiga = c.get("motores")
    if antiga and os.path.isdir(antiga) and os.path.normcase(antiga) != os.path.normcase(pasta):
        # trocar o nome/local da raiz = mover a raiz inteira e reescrever as referencias
        if os.path.exists(pasta):
            sys.exit(f"[erro] {pasta} ja existe; escolha outro nome ou esvazie-a")
        if not a.sim:
            print(f"PLANO: mover {antiga} -> {pasta} e reescrever os caminhos. COM O SIM: motores --pasta \"{pasta}\" --sim")
            return
        shutil.move(antiga, pasta)
        trocas = reescrever_referencias({antiga: pasta}, True, extras=[pasta])
        c = cfg_ler()
        c["motores"] = pasta
        for k, v in list(c.get("caminhos", {}).items()) + [("_pasta", c.get("pasta"))]:
            if v and dentro(v, antiga):
                novo = os.path.normpath(os.path.join(pasta, os.path.relpath(v, antiga)))
                if k == "_pasta":
                    c["pasta"] = novo
                else:
                    c["caminhos"][k] = novo
        cfg_gravar(c)
        variaveis_usuario(c, True)
        print(f"[ok] raiz movida para {pasta}; {sum(n for _, n in trocas)} referencia(s) atualizada(s)")
        return
    os.makedirs(pasta, exist_ok=True)
    for cat in recursos.CATEGORIAS:
        os.makedirs(os.path.join(pasta, cat), exist_ok=True)
    c["motores"] = pasta
    cfg_gravar(c)
    print(f"[ok] raiz dos recursos: {pasta} (Geradores, Ferramentas, Modelos, Cache). "
          "Recursos novos sao instalados aqui; para trazer os existentes: organizar")


def _saida(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30, shell=os.name == "nt").stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def copias_sharp():
    """Pastas node_modules com sharp dentro das copias da skill (uma por IA = duplicata)."""
    out, casa = [], os.path.expanduser("~")
    for top in os.listdir(casa):
        base = os.path.join(casa, top)
        if top.lower() == "appdata" or not os.path.isdir(base):
            continue
        for dirpath, dirs, _ in os.walk(base):
            if dirpath.count(os.sep) - base.count(os.sep) > 5:
                dirs[:] = []
                continue
            dirs[:] = [d for d in dirs if d.lower() not in ("node_modules", ".git", "venv", ".venv", "__pycache__")
                       or (d == "node_modules" and os.path.basename(dirpath) == "assets")]
            if os.path.basename(dirpath) == "node_modules" and os.path.isdir(os.path.join(dirpath, "sharp")) \
                    and os.path.basename(os.path.dirname(os.path.dirname(dirpath))) == "designer-mestre":
                out.append(dirpath)
                dirs[:] = []
    return out


def recursos_extras(c):
    """(chave, origem, destino) dos recursos de apoio que estao fora da raiz."""
    raiz, itens = c["motores"], []
    def add(chave, origem, destino=None):
        if origem and os.path.exists(origem) and not dentro(origem, raiz):
            itens.append((chave, os.path.normpath(origem), destino or os.path.join(raiz, recursos.PADRAO[chave])))
    loc = os.environ.get("LOCALAPPDATA", "")
    add("playwright", os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or os.path.join(loc, "ms-playwright"))
    sharp = copias_sharp()
    if sharp and not os.path.isdir(os.path.join(raiz, recursos.PADRAO["node"], "node_modules", "sharp")):
        add("node", sharp[0], os.path.join(raiz, recursos.PADRAO["node"], "node_modules"))
    hub = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
    if os.path.isdir(hub):
        for nome in sorted(os.listdir(hub)):
            if nome.startswith("models--Systran--faster-whisper"):
                add("whisper", os.path.join(hub, nome), os.path.join(raiz, recursos.PADRAO["whisper"], nome))
    add("cache_uv", os.environ.get("UV_CACHE_DIR") or _saida(["uv", "cache", "dir"]))
    add("cache_npm", os.environ.get("npm_config_cache") or _saida(["npm", "config", "get", "cache"]))
    return itens


def variaveis_usuario(c, aplicar):
    """Variaveis do usuario no Windows para caches e navegador compartilhados: uma copia so, usada por todos
    os programas (aval do usuario em 24/10/2026). Reversivel apagando as variaveis."""
    pares = {"UV_CACHE_DIR": "cache_uv", "npm_config_cache": "cache_npm", "PLAYWRIGHT_BROWSERS_PATH": "playwright"}
    feitas = []
    for var, chave in pares.items():
        alvo = c.get("caminhos", {}).get(chave)
        if not alvo or os.name != "nt":
            continue
        atual = _saida(["powershell", "-NoProfile", "-Command", f"[Environment]::GetEnvironmentVariable('{var}','User')"])
        if os.path.normcase(atual or "") == os.path.normcase(alvo):
            continue
        if aplicar:
            # aspas simples dobradas: caminho com ' quebraria a string do PowerShell
            r = subprocess.run(["powershell", "-NoProfile", "-Command",
                                f"[Environment]::SetEnvironmentVariable('{var}', '{alvo.replace(chr(39), chr(39) * 2)}', 'User')"],
                               check=False)
            if r.returncode != 0:
                print(f"[aviso] nao foi possivel gravar {var} (codigo {r.returncode})")
                continue
        feitas.append(f"{var}={alvo}")
    return feitas


EXT_REF = (".py", ".sh", ".cmd", ".bat", ".ps1", ".json", ".yaml", ".yml", ".ini", ".cfg", ".toml")


def _formas(caminho):
    """Formas de escrever o mesmo caminho em scripts: D:\\a\\b, D:/a/b, /d/a/b, D:\\\\a\\\\b."""
    caminho = os.path.normpath(caminho)
    drive, resto = os.path.splitdrive(caminho)
    fw = resto.replace("\\", "/")
    return {"win": caminho, "fw": drive + fw, "msys": "/" + drive[:1].lower() + fw, "esc": caminho.replace("\\", "\\\\")}


def reescrever_referencias(trocas, aplicar, extras=()):
    """Procura caminhos antigos em scripts e configs (discos e perfil, raso) e troca pelo novo, na mesma forma.
    Devolve [(arquivo, n_trocas)]. Arquivos binarios e pastas de ambiente ficam de fora (exceto os scripts do venv movido)."""
    import re
    regras = []
    for antigo, novo in trocas.items():
        fa, fn = _formas(antigo), _formas(novo)
        for k in fa:
            regras.append((re.compile(re.escape(fa[k]) + r"(?![\w.-])", re.IGNORECASE), fn[k]))
    arquivos = set()
    casa = os.path.expanduser("~")
    raizes = [(f"{l}:\\", 3) for l, _ in discos()] + [(casa, 4)]
    def coletar(raiz, prof):
        try:
            with os.scandir(raiz) as it:
                for e in it:
                    if e.is_file(follow_symlinks=False) and e.name.lower().endswith(EXT_REF) and e.stat().st_size < 1 << 20:
                        arquivos.add(e.path)
                    elif e.is_dir(follow_symlinks=False) and prof > 0 and e.name.lower() not in PULAR | {"skills", "cache", "geradores"}:
                        coletar(e.path, prof - 1)
        except OSError:
            pass
    for r, p in raizes:
        coletar(r, p)
    for base in extras:  # scripts de ativacao dos ambientes movidos (guardam o caminho antigo)
        for dirpath, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d.lower() not in ("lib", "site-packages", "node_modules", ".git", "models")]
            if os.path.basename(dirpath).lower() in ("scripts", "bin") or "pyvenv.cfg" in files:
                arquivos.update(os.path.join(dirpath, f) for f in files
                                if f == "pyvenv.cfg" or f == "activate"
                                or f.lower().endswith((".bat", ".ps1", ".sh", ".cmd", ".fish", ".csh", ".nu")))
    feitas = []
    for arq in sorted(arquivos):
        try:
            txt = open(arq, encoding="utf-8", newline="").read()
        except (OSError, UnicodeDecodeError):
            continue
        novo_txt, n = txt, 0
        for rx, sub in regras:
            novo_txt, k = rx.subn(lambda _m, s=sub: s, novo_txt)
            n += k
        if n and arq.lower().endswith(".sh"):
            # caminho novo com espaco em atribuicao sem aspas (PY=/d/Pasta Nova/x) quebraria no bash: colocar aspas
            novo_txt = re.sub(r'(?m)^([ \t]*(?:export[ \t]+)?\w+=)([^"\'\s][^\n]*?[ \t][^\n]*?)[ \t\r]*$',
                              lambda m: m.group(1) + '"' + m.group(2) + '"' if any(
                                  f in m.group(2) for t in trocas.values() for f in _formas(t).values()) else m.group(0),
                              novo_txt)
            for i, linha in enumerate(novo_txt.splitlines(), 1):
                for t in trocas.values():
                    for f in _formas(t).values():
                        j = linha.find(f)
                        if " " in f and j > 0 and linha[j - 1] not in "\"'" and not re.match(r"[ \t]*(export[ \t]+)?\w+=", linha):
                            print(f"  [revisar] {arq}:{i}: caminho com espaco sem aspas num comando; colocar entre aspas")
        if n:
            feitas.append((arq, n))
            if aplicar:
                open(arq, "w", encoding="utf-8", newline="").write(novo_txt)
    return feitas


def _lixeira(pasta):
    subprocess.run(["powershell", "-NoProfile", "-Command",
                    "Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory("
                    f"'{pasta}', 'OnlyErrorDialogs', 'SendToRecycleBin')"], check=False)


def cmd_organizar(a):
    c = cfg_ler()
    raiz = c.get("motores") or sys.exit("[falta] defina antes: motor_local.py motores --pasta <local escolhido pelo usuario>")
    achados = instalados()
    plano = []  # (chave, origem, destino)
    em_uso = c.get("pasta") or ""
    for origem in sorted(pastas_moviveis(achados), key=lambda o: not (em_uso and dentro(em_uso, o))):
        if dentro(origem, raiz) or dentro(raiz, origem):
            continue
        destino = os.path.join(raiz, "Geradores", os.path.basename(origem))
        n = 2
        while os.path.exists(destino) or destino in [d for _, _, d in plano]:
            destino = os.path.join(raiz, "Geradores", f"{os.path.basename(origem)} ({n})"); n += 1
        plano.append(("comfyui" if em_uso and dentro(em_uso, origem) else "gerador", origem, destino))
    plano += recursos_extras(c)
    sobras = copias_sharp()[1:] if any(k == "node" for k, _, _ in plano) else \
        (copias_sharp() if os.path.isdir(os.path.join(raiz, recursos.PADRAO["node"], "node_modules", "sharp")) else [])
    trocas = {o: d for _, o, d in plano}
    refs = reescrever_referencias(trocas, False) if trocas else []
    if not plano and not sobras:
        print(f"[ok] tudo ja esta em {raiz}")
        return
    print("PLANO (nada foi movido):" if not a.sim else "MOVENDO:")
    for k, o, d in plano:
        mesmo = os.path.splitdrive(o)[0].lower() == os.path.splitdrive(d)[0].lower()
        print(f"  [{k}] {o}  ->  {d}  ({'instantaneo' if mesmo else 'copia entre discos, demora'})")
    for s in sobras:
        print(f"  [duplicata] {s}  ->  Lixeira (o sharp passa a vir de {recursos.PADRAO['node']})")
    for arq, n in refs:
        print(f"  [caminho] {arq}: {n} referencia(s) atualizada(s)")
    var = variaveis_usuario({"caminhos": dict(c.get("caminhos", {}), **{k: d for k, _, d in plano})}, False)
    for v in var:
        print(f"  [variavel do usuario] {v}")
    nao = [f"{k}: {v[0]}" for k, v in achados.items() if k not in MOVIVEIS]
    if nao:
        print("  ficam onde estao (instalados pelo Windows): " + " | ".join(nao))
    if not a.sim:
        print("COM O SIM DO USUARIO: motor_local.py organizar --sim")
        return
    if rodando(1):
        sys.exit("[erro] motor ligado: motor_local.py parar antes de mover")
    for cat in recursos.CATEGORIAS:
        os.makedirs(os.path.join(raiz, cat), exist_ok=True)
    c.setdefault("caminhos", {})
    for k, o, d in plano:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        # Teste de trava: renomear no lugar falha no Windows se algum arquivo estiver aberto. Assim nada e copiado
        # pela metade nem apagado parcialmente enquanto outro programa (servidor MCP, navegador, uv) usa a pasta.
        teste = o + "~movendo"
        try:
            os.rename(o, teste)
        except OSError:
            print(f"  [em uso] {o}: fica onde esta. Fechar o programa que usa e rodar organizar --sim de novo.", flush=True)
            trocas.pop(o, None)
            continue
        try:
            if os.path.isdir(d):
                # destino ja existe (cache recriado por programa aberto antes da variavel): mesclar. shutil.move
                # poria a pasta DENTRO do destino. O que ja existe la fica; a sobra repetida vai para a Lixeira.
                for nome in os.listdir(teste):
                    if not os.path.exists(os.path.join(d, nome)):
                        shutil.move(os.path.join(teste, nome), os.path.join(d, nome))
                if os.listdir(teste):
                    _lixeira(teste)
                    print(f"  [lixeira] repetidos de {o} (ja existiam em {d})", flush=True)
                else:
                    os.rmdir(teste)
            else:
                shutil.move(teste, d)
        except (OSError, shutil.Error) as e:
            if os.path.exists(teste) and not os.path.exists(o):
                os.rename(teste, o)
            print(f"  [falhou] {o}: {e}. Nada foi registrado; rodar organizar --sim de novo.", flush=True)
            trocas.pop(o, None)
            continue
        print(f"  [ok] {d}", flush=True)
        if k == "comfyui":
            c["pasta"] = os.path.normpath(os.path.join(d, os.path.relpath(c["pasta"], o)))
            c["caminhos"]["comfyui"] = c["pasta"]
        elif k == "whisper":
            c["caminhos"]["whisper"] = os.path.dirname(d)
        elif k != "gerador":
            c["caminhos"][k] = d if k != "node" else os.path.dirname(d)
        cfg_gravar(c)
    for s in sobras:
        _lixeira(s)
        print(f"  [lixeira] {s}")
    feitas = reescrever_referencias(trocas, True, extras=[d for _, _, d in plano if os.path.isdir(d)])
    for arq, n in feitas:
        print(f"  [caminho] {arq}: {n}")
    for v in variaveis_usuario(c, True):
        print(f"  [variavel do usuario] {v} (vale para programas abertos depois)")
    for _, _, d in plano:
        movidos = {}
        _varrer(d, 1, movidos)
        for p in movidos.get("ComfyUI", []):
            vpy = py_venv(p)
            if os.path.isfile(vpy) and subprocess.run([vpy, "-c", "import torch"], capture_output=True).returncode:
                print(f"  [aviso] ambiente Python de {p} nao abriu depois de mover: motor_local.py instalar --pasta \"{p}\" --sim refaz so o ambiente")
    print(f"[ok] recursos organizados em {raiz}")


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
                cl = int(resp.headers.get("Content-Length") or 0)
                total = feito + cl
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
            # conexao cortada no meio termina o laco sem erro; so promove o .part se o tamanho bate
            if cl and os.path.getsize(part) != total:
                print(f"  [retomando {tentativa + 1}/5] download incompleto "
                      f"({os.path.getsize(part)}/{total} bytes)", flush=True)
                time.sleep(5)
                continue
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
    achados = instalados()
    existente = comfy_existente(achados)
    inst = existente if existente and os.path.isfile(py_venv(existente)) else None
    if existente:  # reaproveitar: so faltam os modelos ausentes (e o ambiente, se nao houver)
        faltam = [a for a in m["arquivos"] if not os.path.isfile(os.path.join(existente, "models", a[0], a[1]))]
        precisa = (m["download_gb"] if faltam else 0) + (0 if inst else EXTRA_GB)
    d = {"gpu": nome, "vram_gb": round(vram, 1), "ram_gb": round(ram, 1), "python": py, "git": bool(shutil.which("git")),
         "discos": ds, "instalado": inst, "existente": existente, "existentes": achados, "rodando": bool(rodando()),
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
    for motor, locais in achados.items():
        if len(locais) > 1 and motor != "ffmpeg":
            d["avisos"].append(f"{motor} em {len(locais)} pastas (duplicata): usar {existente if motor == 'ComfyUI' else locais[0]};"
                               " contar ao usuario e so remover as outras se ele pedir (roteiro no guia, passo 6)")
    if "ComfyUI Desktop" in achados and not existente:
        d["avisos"].append("ComfyUI Desktop instalado: perguntar se reaproveita os modelos dele antes de instalar outro")
    d["motores"] = c.get("motores")
    d["motores_sugerida"] = f"{ds[0][0]}:\\Recursos" if ds else None
    novo = os.path.join(c.get("motores") or d["motores_sugerida"] or "", recursos.PADRAO["comfyui"]) if (c.get("motores") or ds) else None
    d["pasta_sugerida"] = existente or c.get("pasta") or novo
    d["recomendado"] = None if d["faltas"] else "klein4b"
    return d


def pergunta(d):
    m = MODELOS["klein4b"]
    if d.get("existente"):
        return (f"Posso usar o ComfyUI que ja esta no seu PC ({d['existente']}) como gerador de imagens local? "
                f"Nao instalo outro: so acrescento o que faltar (~{d['precisa_gb']:.0f} GB), sem custo por imagem e sem "
                f"abrir nenhum programa. Modelo {m['nome'].split(' (')[0]}, licenca {m['licenca']}.")
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
    if d["existentes"]:
        print("JA INSTALADOS (reaproveitar, nao instalar de novo):")
        for motor, locais in d["existentes"].items():
            print(f"  {motor}: " + " | ".join(locais))
    else:
        print("ja instalados: nenhum motor de imagem, 3D ou video encontrado")
    for a in d["avisos"]:
        print(f"[aviso] {a}")
    if d["motores"]:
        fora = [p for p in pastas_moviveis(d["existentes"]) if not dentro(p, d["motores"])]
        print(f"raiz dos recursos: {d['motores']}" + (f" · {len(fora)} motor(es) fora dela: motor_local.py organizar" if fora else ""))
    else:
        print(f"raiz dos recursos: nao definida. PERGUNTAR ao usuario local e nome (sugestao {d['motores_sugerida']}), "
              "depois: motor_local.py motores --pasta <local> e motor_local.py organizar")
    if d["faltas"]:
        for f in d["faltas"]:
            print(f"[nao-recomendado] {f}")
        return
    aval = consentimento.aprovado("motor_local.usar")
    if d["instalado"]:
        print("[pronto] motor instalado" + (" e aprovado: usar em silencio" if aval else
              "; sem aval de uso: perguntar 1 vez e registrar motor_local.usar"))
    elif d["existente"]:
        print(f"[reaproveitar] ComfyUI existente em {d['existente']}: so prepara o que faltar (~{d['precisa_gb']:.0f} GB),"
              " sem baixar o motor de novo")
        if not aval:
            print(f"PERGUNTA (1 vez, ferramenta de perguntas): {pergunta(d)}")
        print(f"COM O SIM: motor_local.py instalar --pasta \"{d['existente']}\" --sim")
    else:
        print(f"[recomendado] klein4b em {d['pasta_sugerida']}")
        if not aval:
            print(f"PERGUNTA (1 vez, ferramenta de perguntas): {pergunta(d)}")
        print(f"COM O SIM: motor_local.py instalar --pasta \"{d['pasta_sugerida']}\" --sim")


def obter_codigo(pasta):
    if os.path.isfile(os.path.join(pasta, "main.py")) and os.path.normpath(pasta) != os.path.normpath(cfg_ler().get("pasta") or ""):
        print("  ComfyUI ja existe nesta pasta: reaproveitando, sem baixar nem atualizar o de outra instalacao", flush=True)
    elif os.path.isdir(os.path.join(pasta, ".git")) and shutil.which("git"):
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
    pronto = os.path.isfile(vpy) and subprocess.run([vpy, "-c", "import torch"], capture_output=True).returncode == 0
    if pronto:
        print("  ambiente existente com PyTorch: mantido como esta", flush=True)
    else:
        if not os.path.isfile(vpy):
            run([py, "-m", "venv", os.path.join(pasta, "venv")])
            vpy = py_venv(pasta)
        run([vpy, "-m", "pip", "install", "--upgrade", "pip", "-q"])
        run([vpy, "-m", "pip", "install", "torch", "torchvision", "torchaudio", "-q",
             "--index-url", f"https://download.pytorch.org/whl/{a.torch}"])
        run([vpy, "-m", "pip", "install", "-r", os.path.join(pasta, "requirements.txt"), "-q"])
    print(f"[3/4] baixando os modelos: {MODELOS[a.modelo]['nome']} · {MODELOS[a.modelo]['licenca']}", flush=True)
    outros = [p for p in d["existentes"].get("ComfyUI", []) if os.path.normpath(p) != os.path.normpath(pasta)]
    for sub, nome, url in MODELOS[a.modelo]["arquivos"]:
        destino = os.path.join(pasta, "models", sub, nome)
        copia = next((os.path.join(p, "models", sub, nome) for p in outros
                      if os.path.isfile(os.path.join(p, "models", sub, nome))), None)
        if copia and not os.path.isfile(destino):
            try:  # link no mesmo disco: mesmo arquivo, sem ocupar espaco de novo
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                os.link(copia, destino)
                print(f"  [reaproveitado] {nome} de {copia}")
                continue
            except OSError:
                pass
        baixar(url, destino)
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
    mo = sub.add_parser("motores", help="define (ou mostra) a pasta Motores escolhida pelo usuario")
    mo.add_argument("--pasta")
    mo.add_argument("--sim", action="store_true", help="aprovado: mover a raiz atual para o novo local")
    mo.set_defaults(f=cmd_motores)
    o = sub.add_parser("organizar", help="move para Motores\\ os motores de pasta propria ja instalados")
    o.add_argument("--sim", action="store_true", help="o usuario aprovou; sem isto so mostra o plano")
    o.set_defaults(f=cmd_organizar)
    sub.add_parser("parar").set_defaults(f=cmd_parar)
    sub.add_parser("status").set_defaults(f=cmd_status)
    sub.add_parser("modelos").set_defaults(f=cmd_modelos)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
