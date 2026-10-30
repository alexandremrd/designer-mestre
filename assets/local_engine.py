#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
local_engine.py - Analyzes the PC, installs and controls the /designer-mestre local image engine (headless ComfyUI).

The AI installs and operates it; the user only gives approval, once (consent.py). ComfyUI runs only as a
server (API at http://127.0.0.1:8188), opening no browser or app; generate_image.py is what drives it.
It installs outside the skill folder, downloading only from official sources (ComfyUI GitHub, PyTorch, Hugging Face).
The folder is stored in %USERPROFILE%\\.designer-mestre\\local_engine.json, which skill updates do not erase.

Commands:
  python local_engine.py guide                     (AI script: analyze, ask once, install, operate)
  python local_engine.py detect                 (analyzes the PC and recommends; brings the ready-made question for the user)
  python local_engine.py install [--folder X]     (without --yes it only shows the plan; with --yes it installs and records the approval)
  python local_engine.py start | stop | status | models
"""
import argparse, io, json, os, shutil, subprocess, sys, time, zipfile
import urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import consent
import resources

CFG = os.path.join(os.path.expanduser("~"), ".designer-mestre", "local_engine.json")
# config written before the English rename: adopt it once so the resource root is not lost
_CFG_OLD = os.path.join(os.path.dirname(CFG), "motor_local.json")
if not os.path.exists(CFG) and os.path.exists(_CFG_OLD):
    os.replace(_CFG_OLD, CFG)
URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188").rstrip("/")
REPO = "https://github.com/comfyanonymous/ComfyUI"
HF = "https://huggingface.co"
PY_OK = ((3, 10), (3, 13))  # versions with published PyTorch CUDA
EXTRA_GB = 6  # PyTorch + dependencies + headroom

# Catalog: only files whose license was checked in the repository each one is downloaded from (not just in the model):
# the same file name may exist in a repository with a different license. (folder in models\, file, url)
MODELOS = {
    "klein4b": {
        "nome": "FLUX.2 klein 4B fp8 (distilled, 4 steps, multi-reference)",
        "licenca": "Apache 2.0 on all files (commercial use)", "vram_min_gb": 8, "download_gb": 7.7,
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

GUIA = """AI SCRIPT - local image engine (the user only gives approval; the AI does everything else)
1. Before offering: `local_engine.py detect`. It analyzes GPU, VRAM, RAM, disk, Python and the engines already
   installed on the PC (ComfyUI in any form, Forge/A1111, Fooocus, InvokeAI, Easy Diffusion, Blender, ffmpeg),
   and says whether the PC can handle it, which model fits and the ready-made question. PC not up to it = do not offer the local engine.
   Engine already installed = reuse it; never install a second copy of the same engine.
   Resource root: the user chooses location and name (ask once) -> `engines --folder <location>`; it has
   the categories Geradores, Ferramentas, Modelos and Cache (see resources.py). Everything the skill installs, with approval, goes to the
   right category inside it. The existing ones (generators, Playwright browser, sharp, Whisper, uv/npm caches)
   go with `organize` (plan) and `organize --yes` (with the yes): it moves them, rewrites the paths in scripts and
   configs, sends duplicate copies to the Recycle Bin and records the user variables of the shared caches.
   Changing name/location later: `engines --folder <new> --yes`. Apps installed by Windows (Blender, ffmpeg,
   ComfyUI Desktop) stay where they are. Scripts read the paths from resources.py, never a fixed path.
   Before --yes (organize or engines): show the user the plan output item by item and wait for the yes,
   because the approval of the location or of the rule does not cover the list (copies go to the Recycle Bin, caches change disk).
   If the change also altered skill scripts, reinstall the skill BEFORE moving: the old copy looks for the
   resources in the old place and breaks halfway.
2. One-time approval: `consent.py view local_engine.usar`. Approved = proceed silently. No approval = ask the
   question from `detect` ONCE, in the question tool, in plain English (what it is, space, time,
   zero cost, how to remove). Refused = proceed with another generator and do not ask again in this session.
3. Install (only with the yes): `local_engine.py install --folder <suggested> --yes`, in the background. It records the
   approval to install and to use, so it is not asked again. While downloading, tell the user in 1 line per step
   (downloading the engine / the models / ready). Error: read the [missing]/[error] message, solve yourself whatever is
   solvable (e.g., running again resumes the download) and involve the user only if a new yes is needed.
4. Use: `generate_image.py generate ... --engine comfy` starts the engine by itself if it is stopped.
   Keep it on during the rounds; `local_engine.py stop` only after the final approval of the piece.
5. Remove (if the user asks): `local_engine.py stop`, delete the installed folder (confirm first) and
   `consent.py revoke local_engine.usar`.
6. Remove a duplicate (only at the user's request), in this order, because the "leftover" copy usually has
   files and scripts that depend on it:
   a. Search for the duplicate's path in configs AND in scripts of the parent and neighboring folders (.py .sh .cmd .bat .ps1
      .json .yaml); a script that points to it = redirect it to the kept copy before removing.
   b. Compare models, custom_nodes, input, output and user: what exists only in the duplicate moves to the kept
      copy without overwriting; a model with the same name and different size = ask.
   c. Engine stopped; send the folder to the Recycle Bin (recoverable), never delete permanently; first check that the
      disk's Recycle Bin can hold the size. Afterwards, `detect` must show a single copy.
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
    """ComfyUI's Python: own venv, .venv (Desktop/uv) or python_embeded (portable package, sibling folder)."""
    exe = "python.exe" if os.name == "nt" else "python"
    pasta_bin = "Scripts" if os.name == "nt" else "bin"
    for c in (os.path.join(pasta, "venv", pasta_bin, exe), os.path.join(pasta, ".venv", pasta_bin, exe),
              os.path.join(os.path.dirname(pasta), "python_embeded", exe), os.path.join(pasta, "python_embeded", exe)):
        if os.path.isfile(c):
            return c
    return os.path.join(pasta, "venv", pasta_bin, exe)


# Engines already installed elsewhere (to reuse and not duplicate): name -> files that mark the folder.
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
    """Image/3D/video engines already present on the PC. Shallow scan (seconds), downloads nothing."""
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
    # ComfyUI Desktop keeps the code in the app and the data in Documents\ComfyUI (with .venv)
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
    """Best ComfyUI already installed: the configured one, otherwise one with its own Python ready."""
    pastas = achados.get("ComfyUI", [])
    cfg = cfg_ler().get("pasta")
    if cfg and os.path.normpath(cfg) in pastas:
        return os.path.normpath(cfg)
    for p in pastas:
        if os.path.isfile(py_venv(p)):
            return p
    return pastas[0] if pastas else None


# Only engines that live in their own folder can go to Motores\; an app installed by Windows (Blender in
# Program Files, ffmpeg on PATH, ComfyUI Desktop) breaks its registry entries and shortcuts if moved.
MOVIVEIS = ("ComfyUI", "Forge/A1111", "Fooocus", "InvokeAI", "Easy Diffusion")


def dentro(p, raiz):
    p, raiz = os.path.normcase(os.path.abspath(p)), os.path.normcase(os.path.abspath(raiz))
    return p == raiz or p.startswith(raiz.rstrip("\\/") + os.sep)


def pastas_moviveis(achados):
    """Folder to move for each engine: for portable ComfyUI it is the parent folder, which carries the python_embeded along."""
    out = []
    for motor in MOVIVEIS:
        for p in achados.get(motor, []):
            mae = os.path.dirname(p)
            out.append(mae if os.path.isdir(os.path.join(mae, "python_embeded")) else p)
    return list(dict.fromkeys(out))


def cmd_motores(a):
    c = cfg_ler()
    if not a.pasta:
        print(f"resource root folder: {c.get('motores') or 'not set (ask the user)'}")
        return
    pasta = os.path.abspath(a.pasta)
    if os.path.abspath(os.path.dirname(__file__)).lower() in pasta.lower():
        sys.exit("[error] the root folder must be outside the skill folder (updates overwrite it).")
    antiga = c.get("motores")
    if antiga and os.path.isdir(antiga) and os.path.normcase(antiga) != os.path.normcase(pasta):
        # changing the root's name/location = move the whole root and rewrite the references
        if os.path.exists(pasta):
            sys.exit(f"[error] {pasta} already exists; choose another name or empty it")
        if not a.sim:
            print(f"PLAN: move {antiga} -> {pasta} and rewrite the paths. WITH THE YES: engines --folder \"{pasta}\" --yes")
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
        print(f"[ok] root moved to {pasta}; {sum(n for _, n in trocas)} reference(s) updated")
        return
    os.makedirs(pasta, exist_ok=True)
    for cat in resources.CATEGORIAS:
        os.makedirs(os.path.join(pasta, cat), exist_ok=True)
    c["motores"] = pasta
    cfg_gravar(c)
    print(f"[ok] resource root: {pasta} (Geradores, Ferramentas, Modelos, Cache). "
          "New resources are installed here; to bring in the existing ones: organize")


def _saida(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30, shell=os.name == "nt").stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def copias_sharp():
    """node_modules folders with sharp inside the skill copies (one per AI = duplicate)."""
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
    """(key, source, destination) of the support resources that are outside the root."""
    raiz, itens = c["motores"], []
    def add(chave, origem, destino=None):
        if origem and os.path.exists(origem) and not dentro(origem, raiz):
            itens.append((chave, os.path.normpath(origem), destino or os.path.join(raiz, resources.PADRAO[chave])))
    loc = os.environ.get("LOCALAPPDATA", "")
    add("playwright", os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or os.path.join(loc, "ms-playwright"))
    sharp = copias_sharp()
    if sharp and not os.path.isdir(os.path.join(raiz, resources.PADRAO["node"], "node_modules", "sharp")):
        add("node", sharp[0], os.path.join(raiz, resources.PADRAO["node"], "node_modules"))
    hub = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
    if os.path.isdir(hub):
        for nome in sorted(os.listdir(hub)):
            if nome.startswith("models--Systran--faster-whisper"):
                add("whisper", os.path.join(hub, nome), os.path.join(raiz, resources.PADRAO["whisper"], nome))
    add("cache_uv", os.environ.get("UV_CACHE_DIR") or _saida(["uv", "cache", "dir"]))
    add("cache_npm", os.environ.get("npm_config_cache") or _saida(["npm", "config", "get", "cache"]))
    return itens


def variaveis_usuario(c, aplicar):
    """Windows user variables for shared caches and browser: a single copy, used by all
    programs (user approval on 2026-10-24). Reversible by deleting the variables."""
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
            # doubled single quotes: a path with ' would break the PowerShell string
            r = subprocess.run(["powershell", "-NoProfile", "-Command",
                                f"[Environment]::SetEnvironmentVariable('{var}', '{alvo.replace(chr(39), chr(39) * 2)}', 'User')"],
                               check=False)
            if r.returncode != 0:
                print(f"[warning] could not write {var} (code {r.returncode})")
                continue
        feitas.append(f"{var}={alvo}")
    return feitas


EXT_REF = (".py", ".sh", ".cmd", ".bat", ".ps1", ".json", ".yaml", ".yml", ".ini", ".cfg", ".toml")


def _formas(caminho):
    """Ways of writing the same path in scripts: D:\\a\\b, D:/a/b, /d/a/b, D:\\\\a\\\\b."""
    caminho = os.path.normpath(caminho)
    drive, resto = os.path.splitdrive(caminho)
    fw = resto.replace("\\", "/")
    return {"win": caminho, "fw": drive + fw, "msys": "/" + drive[:1].lower() + fw, "esc": caminho.replace("\\", "\\\\")}


def reescrever_referencias(trocas, aplicar, extras=()):
    """Searches for old paths in scripts and configs (disks and profile, shallow) and swaps in the new one, in the same form.
    Returns [(file, n_swaps)]. Binary files and environment folders are left out (except the moved venv's scripts)."""
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
    for base in extras:  # activation scripts of the moved environments (they hold the old path)
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
            # new path with a space in an unquoted assignment (PY=/d/New Folder/x) would break in bash: add quotes
            novo_txt = re.sub(r'(?m)^([ \t]*(?:export[ \t]+)?\w+=)([^"\'\s][^\n]*?[ \t][^\n]*?)[ \t\r]*$',
                              lambda m: m.group(1) + '"' + m.group(2) + '"' if any(
                                  f in m.group(2) for t in trocas.values() for f in _formas(t).values()) else m.group(0),
                              novo_txt)
            for i, linha in enumerate(novo_txt.splitlines(), 1):
                for t in trocas.values():
                    for f in _formas(t).values():
                        j = linha.find(f)
                        if " " in f and j > 0 and linha[j - 1] not in "\"'" and not re.match(r"[ \t]*(export[ \t]+)?\w+=", linha):
                            print(f"  [revisar] {arq}:{i}: path with a space without quotes in a command; put it in quotes")
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
    raiz = c.get("motores") or sys.exit("[missing] set first: local_engine.py engines --folder <location chosen by the user>")
    achados = instalados()
    plano = []  # (key, source, destination)
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
        (copias_sharp() if os.path.isdir(os.path.join(raiz, resources.PADRAO["node"], "node_modules", "sharp")) else [])
    trocas = {o: d for _, o, d in plano}
    refs = reescrever_referencias(trocas, False) if trocas else []
    if not plano and not sobras:
        print(f"[ok] everything is already in {raiz}")
        return
    print("PLAN (nothing was moved):" if not a.sim else "MOVING:")
    for k, o, d in plano:
        mesmo = os.path.splitdrive(o)[0].lower() == os.path.splitdrive(d)[0].lower()
        print(f"  [{k}] {o}  ->  {d}  ({'instant' if mesmo else 'copy across disks, takes a while'})")
    for s in sobras:
        print(f"  [duplicata] {s}  ->  Recycle Bin (sharp will come from {resources.PADRAO['node']})")
    for arq, n in refs:
        print(f"  [caminho] {arq}: {n} reference(s) updated")
    var = variaveis_usuario({"caminhos": dict(c.get("caminhos", {}), **{k: d for k, _, d in plano})}, False)
    for v in var:
        print(f"  [variavel do usuario] {v}")
    nao = [f"{k}: {v[0]}" for k, v in achados.items() if k not in MOVIVEIS]
    if nao:
        print("  stay where they are (installed by Windows): " + " | ".join(nao))
    if not a.sim:
        print("WITH THE USER'S YES: local_engine.py organize --yes")
        return
    if rodando(1):
        sys.exit("[error] engine running: local_engine.py stop before moving")
    for cat in resources.CATEGORIAS:
        os.makedirs(os.path.join(raiz, cat), exist_ok=True)
    c.setdefault("caminhos", {})
    for k, o, d in plano:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        # Lock test: renaming in place fails on Windows if any file is open. This way nothing is half-copied
        # or partially deleted while another program (MCP server, browser, uv) uses the folder.
        teste = o + "~movendo"
        try:
            os.rename(o, teste)
        except OSError:
            print(f"  [em uso] {o}: stays where it is. Close the program using it and run organize --yes again.", flush=True)
            trocas.pop(o, None)
            continue
        try:
            if os.path.isdir(d):
                # destination already exists (cache recreated by a program opened before the variable): merge. shutil.move
                # would put the folder INSIDE the destination. What already exists there stays; the repeated leftover goes to the Recycle Bin.
                for nome in os.listdir(teste):
                    if not os.path.exists(os.path.join(d, nome)):
                        shutil.move(os.path.join(teste, nome), os.path.join(d, nome))
                if os.listdir(teste):
                    _lixeira(teste)
                    print(f"  [trash] duplicates of {o} (already existed in {d})", flush=True)
                else:
                    os.rmdir(teste)
            else:
                shutil.move(teste, d)
        except (OSError, shutil.Error) as e:
            if os.path.exists(teste) and not os.path.exists(o):
                os.rename(teste, o)
            print(f"  [failed] {o}: {e}. Nothing was recorded; run organize --yes again.", flush=True)
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
        print(f"  [trash] {s}")
    feitas = reescrever_referencias(trocas, True, extras=[d for _, _, d in plano if os.path.isdir(d)])
    for arq, n in feitas:
        print(f"  [caminho] {arq}: {n}")
    for v in variaveis_usuario(c, True):
        print(f"  [variavel do usuario] {v} (applies to programs opened afterwards)")
    for _, _, d in plano:
        movidos = {}
        _varrer(d, 1, movidos)
        for p in movidos.get("ComfyUI", []):
            vpy = py_venv(p)
            if os.path.isfile(vpy) and subprocess.run([vpy, "-c", "import torch"], capture_output=True).returncode:
                print(f"  [warning] Python environment of {p} did not open after moving: local_engine.py install --folder \"{p}\" --yes rebuilds only the environment")
    print(f"[ok] resources organized in {raiz}")


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
        sys.exit(f"[error] command failed ({r.returncode}): {' '.join(cmd)}\n"
                 "  Running install --yes again resumes where it stopped.")


def baixar(url, destino):
    """Download with resume (.part) and progress; skips an already complete file."""
    if os.path.isfile(destino):
        print(f"  [already exists] {os.path.basename(destino)}")
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
            # a connection cut midway ends the loop without error; only promote the .part if the size matches
            if cl and os.path.getsize(part) != total:
                print(f"  [resuming {tentativa + 1}/5] incomplete download "
                      f"({os.path.getsize(part)}/{total} bytes)", flush=True)
                time.sleep(5)
                continue
            os.replace(part, destino)
            print(f"  [ok] {os.path.basename(destino)}")
            return
        except (urllib.error.URLError, OSError) as e:
            print(f"  [resuming {tentativa + 1}/5] {e}", flush=True)
            time.sleep(5)
    sys.exit(f"[error] download failed: {url}\n  Running install --yes again resumes the download.")


def gpu():
    """(name, vram_gb) of the NVIDIA GPU, or (None, 0)."""
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
    """Path of a Python with published PyTorch CUDA: the current one or one from the py launcher."""
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
    """Full diagnosis; nothing is downloaded."""
    nome, vram = gpu()
    ram, py, ds = ram_gb(), python_ok(), discos()
    m = MODELOS["klein4b"]
    precisa = m["download_gb"] + EXTRA_GB
    c = cfg_ler()
    achados = instalados()
    existente = comfy_existente(achados)
    inst = existente if existente and os.path.isfile(py_venv(existente)) else None
    if existente:  # reuse: only the missing models are needed (and the environment, if there is none)
        faltam = [a for a in m["arquivos"] if not os.path.isfile(os.path.join(existente, "models", a[0], a[1]))]
        precisa = (m["download_gb"] if faltam else 0) + (0 if inst else EXTRA_GB)
    d = {"gpu": nome, "vram_gb": round(vram, 1), "ram_gb": round(ram, 1), "python": py, "git": bool(shutil.which("git")),
         "discos": ds, "instalado": inst, "existente": existente, "existentes": achados, "rodando": bool(rodando()),
         "precisa_gb": round(precisa, 1), "faltas": [], "avisos": []}
    if not nome:
        d["faltas"].append("no NVIDIA GPU: the local engine would be too slow; use another generator")
    elif vram < m["vram_min_gb"] - 0.5:
        d["faltas"].append(f"GPU with {vram:.0f} GB of VRAM; the model needs {m['vram_min_gb']} GB; use another generator")
    if ram and ram < 15:
        d["avisos"].append(f"{ram:.0f} GB of RAM: works, but slower (ideal 16 GB)")
    if not py:
        d["avisos"].append("no Python 3.10-3.13: the AI installs the official Python 3.12 first (winget) with the same approval")
    if not ds or ds[0][1] < precisa:
        d["faltas"].append(f"no disk with {precisa:.0f} GB free")
    for motor, locais in achados.items():
        if len(locais) > 1 and motor != "ffmpeg":
            d["avisos"].append(f"{motor} in {len(locais)} folders (duplicate): use {existente if motor == 'ComfyUI' else locais[0]};"
                               " tell the user and only remove the others if they ask (script in the guide, step 6)")
    if "ComfyUI Desktop" in achados and not existente:
        d["avisos"].append("ComfyUI Desktop installed: ask whether to reuse its models before installing another")
    d["motores"] = c.get("motores")
    d["motores_sugerida"] = f"{ds[0][0]}:\\Recursos" if ds else None
    novo = os.path.join(c.get("motores") or d["motores_sugerida"] or "", resources.PADRAO["comfyui"]) if (c.get("motores") or ds) else None
    d["pasta_sugerida"] = existente or c.get("pasta") or novo
    d["recomendado"] = None if d["faltas"] else "klein4b"
    return d


def pergunta(d):
    m = MODELOS["klein4b"]
    if d.get("existente"):
        return (f"May I use the ComfyUI already on your PC ({d['existente']}) as the local image generator? "
                f"I will not install another one: I only add what is missing (~{d['precisa_gb']:.0f} GB), at no cost per image and without "
                f"opening any program. Model {m['nome'].split(' (')[0]}, license {m['licenca']}.")
    return (f"May I install the local image generator on your PC? It runs on your graphics card ({d['gpu']}), "
            f"at no cost per image and without opening any program: I install and drive everything. It takes ~{d['precisa_gb']:.0f} GB "
            f"in {d['pasta_sugerida']}, ~15-30 min to download (only once) and generates each image in ~1 min. "
            f"Model {m['nome'].split(' (')[0]}, license {m['licenca']}. You can ask me to remove it whenever you want.")


def cmd_guia(_):
    print(GUIA)


def cmd_detectar(_):
    d = analisar()
    print(f"GPU: {d['gpu'] or 'no NVIDIA'} · VRAM {d['vram_gb']} GB · RAM {d['ram_gb']} GB")
    print("disks: " + ", ".join(f"{l}: {g:.0f} GB free" for l, g in d["discos"]))
    print(f"compatible python: {d['python'] or 'no'} · git: {'yes' if d['git'] else 'no (downloads the official zip)'}")
    print(f"installed: {d['instalado'] or 'no'} · running: {'yes' if d['rodando'] else 'no'}")
    if d["existentes"]:
        print("ALREADY INSTALLED (reuse, do not install again):")
        for motor, locais in d["existentes"].items():
            print(f"  {motor}: " + " | ".join(locais))
    else:
        print("already installed: no image, 3D or video engine found")
    for a in d["avisos"]:
        print(f"[warning] {a}")
    if d["motores"]:
        fora = [p for p in pastas_moviveis(d["existentes"]) if not dentro(p, d["motores"])]
        print(f"resource root: {d['motores']}" + (f" · {len(fora)} engine(s) outside it: local_engine.py organize" if fora else ""))
    else:
        print(f"resource root: not set. ASK the user for location and name (suggestion {d['motores_sugerida']}), "
              "then: local_engine.py engines --folder <location> and local_engine.py organize")
    if d["faltas"]:
        for f in d["faltas"]:
            print(f"[not-recommended] {f}")
        return
    aval = consent.aprovado("local_engine.usar")
    if d["instalado"]:
        print("[pronto] engine installed" + (" and approved: use silently" if aval else
              "; no approval to use: ask once and record local_engine.usar"))
    elif d["existente"]:
        print(f"[reaproveitar] existing ComfyUI in {d['existente']}: only prepares what is missing (~{d['precisa_gb']:.0f} GB),"
              " without downloading the engine again")
        if not aval:
            print(f"QUESTION (once, question tool): {pergunta(d)}")
        print(f"WITH THE YES: local_engine.py install --folder \"{d['existente']}\" --yes")
    else:
        print(f"[recomendado] klein4b in {d['pasta_sugerida']}")
        if not aval:
            print(f"QUESTION (once, question tool): {pergunta(d)}")
        print(f"WITH THE YES: local_engine.py install --folder \"{d['pasta_sugerida']}\" --yes")


def obter_codigo(pasta):
    if os.path.isfile(os.path.join(pasta, "main.py")) and os.path.normpath(pasta) != os.path.normpath(cfg_ler().get("pasta") or ""):
        print("  ComfyUI already exists in this folder: reusing it, without downloading or updating another installation's", flush=True)
    elif os.path.isdir(os.path.join(pasta, ".git")) and shutil.which("git"):
        run(["git", "-C", pasta, "pull", "--ff-only"])
    elif shutil.which("git") and not os.path.exists(pasta):
        run(["git", "clone", "--depth", "1", REPO + ".git", pasta])
    elif not os.path.isfile(os.path.join(pasta, "main.py")):
        print("  git missing: downloading the official GitHub zip", flush=True)
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
        print("PLAN (nothing was downloaded):")
        print(f"  folder: {pasta} · ~{d['precisa_gb']:.0f} GB · ~15-30 min · model {MODELOS[a.modelo]['nome']}")
        print(f"  license: {MODELOS[a.modelo]['licenca']} · sources: ComfyUI GitHub, PyTorch, Hugging Face")
        for f in d["faltas"]:
            print(f"  [not-recommended] {f}")
        print(f"QUESTION (once): {pergunta(d)}" if not d["faltas"] else "")
        print("WITH THE YES: repeat with --yes")
        return
    if d["faltas"] and not a.forcar:
        sys.exit("[not-recommended] " + "; ".join(d["faltas"]))
    if os.path.abspath(os.path.dirname(__file__)).lower() in pasta.lower():
        sys.exit("[error] install outside the skill folder (updates overwrite it).")
    py = d["python"]
    if not py:
        print("[0/4] Official Python 3.12 (winget)")
        run(["winget", "install", "-e", "--id", "Python.Python.3.12", "--silent",
             "--accept-package-agreements", "--accept-source-agreements"])
        py = python_ok() or sys.exit("[missing] Python 3.12 installed, but not found: reopen the terminal and repeat.")
    consent.registrar("local_engine.instalar", f"pasta {pasta}")
    consent.registrar("local_engine.usar", "approval given together with the installation")
    os.makedirs(os.path.dirname(pasta) or pasta, exist_ok=True)
    print("[1/4] downloading the engine (ComfyUI, official GitHub)", flush=True)
    obter_codigo(pasta)
    print("[2/4] preparing the environment (isolated Python + PyTorch CUDA)", flush=True)
    vpy = py_venv(pasta)
    pronto = os.path.isfile(vpy) and subprocess.run([vpy, "-c", "import torch"], capture_output=True).returncode == 0
    if pronto:
        print("  existing environment with PyTorch: kept as is", flush=True)
    else:
        if not os.path.isfile(vpy):
            run([py, "-m", "venv", os.path.join(pasta, "venv")])
            vpy = py_venv(pasta)
        run([vpy, "-m", "pip", "install", "--upgrade", "pip", "-q"])
        run([vpy, "-m", "pip", "install", "torch", "torchvision", "torchaudio", "-q",
             "--index-url", f"https://download.pytorch.org/whl/{a.torch}"])
        run([vpy, "-m", "pip", "install", "-r", os.path.join(pasta, "requirements.txt"), "-q"])
    print(f"[3/4] downloading the models: {MODELOS[a.modelo]['nome']} · {MODELOS[a.modelo]['licenca']}", flush=True)
    outros = [p for p in d["existentes"].get("ComfyUI", []) if os.path.normpath(p) != os.path.normpath(pasta)]
    for sub, nome, url in MODELOS[a.modelo]["arquivos"]:
        destino = os.path.join(pasta, "models", sub, nome)
        copia = next((os.path.join(p, "models", sub, nome) for p in outros
                      if os.path.isfile(os.path.join(p, "models", sub, nome))), None)
        if copia and not os.path.isfile(destino):
            try:  # link on the same disk: same file, taking no extra space
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                os.link(copia, destino)
                print(f"  [reused] {nome} from {copia}")
                continue
            except OSError:
                pass
        baixar(url, destino)
    print("[4/4] ready", flush=True)
    c = cfg_ler()
    c.update({"pasta": pasta, "modelo": a.modelo, "instalado_em": time.strftime("%Y-%m-%d %H:%M")})
    cfg_gravar(c)
    print(f"[ok] local engine installed in {pasta}; generate_image.py starts it by itself when needed.")


def cmd_iniciar(a):
    if rodando():
        print(f"[ok] already running at {URL}")
        return
    pasta = cfg_ler().get("pasta")
    if not pasta or not os.path.isfile(py_venv(pasta)):
        sys.exit("[nao-instalado] local engine missing. See: local_engine.py guide")
    porta = URL.rsplit(":", 1)[-1]
    log = open(os.path.join(pasta, "motor.log"), "w", encoding="utf-8")
    flags = (subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW) \
        if os.name == "nt" else 0
    cmd = [py_venv(pasta), "main.py", "--listen", "127.0.0.1", "--port", porta, "--disable-auto-launch"] + a.extra
    p = subprocess.Popen(cmd, cwd=pasta, stdout=log, stderr=subprocess.STDOUT, creationflags=flags)
    c = cfg_ler(); c["pid"] = p.pid; cfg_gravar(c)
    for _ in range(a.espera):
        if rodando():
            print(f"[ok] local engine up at {URL} (pid {p.pid}, log {pasta}\\motor.log)")
            return
        if p.poll() is not None:
            sys.exit(f"[error] engine exited on startup; see {pasta}\\motor.log")
        time.sleep(1)
    sys.exit(f"[error] engine did not respond within {a.espera}s; see {pasta}\\motor.log")


def cmd_parar(_):
    c = cfg_ler()
    pid = c.pop("pid", None)
    if pid:
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"] if os.name == "nt" else ["kill", str(pid)],
                       capture_output=True)
        cfg_gravar(c)
    print("[ok] engine stopped" if not rodando(1) else "[warning] still responding; it may have been started by another process")


def cmd_status(_):
    s = rodando()
    if not s:
        print(f"[stopped] {URL}  installed: {cfg_ler().get('pasta', 'no')}")
        return
    for d in s.get("devices", []):
        print(f"[rodando] {URL} · {d.get('name')} · free VRAM {d.get('vram_free', 0) / 2**30:.1f}"
              f"/{d.get('vram_total', 0) / 2**30:.1f} GB")


def cmd_modelos(_):
    pasta = cfg_ler().get("pasta")
    for k, m in MODELOS.items():
        ok = pasta and all(os.path.isfile(os.path.join(pasta, "models", s, n)) for s, n, _ in m["arquivos"])
        print(f"{k}: {m['nome']} · {m['licenca']} · VRAM >= {m['vram_min_gb']} GB · {m['download_gb']} GB"
              f" · {'downloaded' if ok else 'not downloaded'}")


def main():
    ap = argparse.ArgumentParser(description="Local engine (headless ComfyUI) of /designer-mestre")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("guide").set_defaults(f=cmd_guia)
    sub.add_parser("detect").set_defaults(f=cmd_detectar)
    i = sub.add_parser("install")
    i.add_argument("--folder", dest="pasta", help="default: disk with the most free space, <disk>:\\IA\\ComfyUI")
    i.add_argument("--yes", dest="sim", action="store_true", help="the user approved; without this it only shows the plan")
    i.add_argument("--force", dest="forcar", action="store_true", help="install even with hardware below the recommended")
    i.add_argument("--model", dest="modelo", default="klein4b", choices=list(MODELOS))
    i.add_argument("--torch", default="cu128", help="PyTorch index (cu128 covers RTX 50xx)")
    i.set_defaults(f=cmd_instalar)
    s = sub.add_parser("start")
    s.add_argument("--wait", dest="espera", type=int, default=180)
    s.add_argument("--extra", type=str.split, default=[], help='extra ComfyUI flags (e.g.: --extra="--lowvram")')
    s.set_defaults(f=cmd_iniciar)
    mo = sub.add_parser("engines", help="sets (or shows) the Motores folder chosen by the user")
    mo.add_argument("--folder", dest="pasta")
    mo.add_argument("--yes", dest="sim", action="store_true", help="approved: move the current root to the new location")
    mo.set_defaults(f=cmd_motores)
    o = sub.add_parser("organize", help="moves to Motores\\ the already installed engines that have their own folder")
    o.add_argument("--yes", dest="sim", action="store_true", help="the user approved; without this it only shows the plan")
    o.set_defaults(f=cmd_organizar)
    sub.add_parser("stop").set_defaults(f=cmd_parar)
    sub.add_parser("status").set_defaults(f=cmd_status)
    sub.add_parser("models").set_defaults(f=cmd_modelos)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
