#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_imagem.py - Utilitario de geracao local, upscale e registro universal de imagens do /designer-mestre.

A IDE tem autonomia para decidir o melhor caminho de geracao (ferramenta/subagente nativo da IDE,
motor local via ComfyUI sem interface em http://127.0.0.1:8188 (instalado e ligado por motor_local.py),
Easy Diffusion em http://127.0.0.1:9000 se ja existir, ou composicao hibrida).
Toda imagem gerada por qualquer motor e salva/registrada em Compartilhada\\Imagens\\IA\\ com seu .txt
contendo ferramenta, modelo, seed, referencias e prompt para aprendizado continuo.

Comandos:
  python gerar_imagem.py registrar <imagem_gerada> -o "...\\IA\\2026-10-20_tema_v1.png" --prompt "..." --ferramenta "<motor>" [--ref mestra.jpg] [--status aprovado|descartado] [--notas "..."]
  python gerar_imagem.py gemini "PROMPT" [--ref mestra.jpg] [--pro] -a 4:5 -o "...\\IA\\nome.png"   (exige GEMINI_API_KEY)
  python gerar_imagem.py ping
  python gerar_imagem.py modelos
  python gerar_imagem.py gerar "PROMPT EN" [--ref mestra.jpg] [--init base.jpg --forca 0.45] -a 4:5 -o "...\\IA\\nome.png" [--motor comfy|ed]
    (exige o aval unico motor_local.usar, gravado por consentimento.py; o ComfyUI liga sozinho)
  python gerar_imagem.py upscale foto.png -o foto_4x.png [--escala 2|4]
"""
import argparse, base64, json, os, shutil, subprocess, sys, time, uuid
import urllib.request, urllib.error, urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import consentimento

ED = os.environ.get("ED_URL", "http://127.0.0.1:9000").rstrip("/")
COMFY = os.environ.get("COMFY_URL", "http://127.0.0.1:8188").rstrip("/")
# FLUX.2 klein 4B destilado: 4 passos, cfg 1 (workflow oficial Comfy-Org/workflow_templates)
KLEIN = {"unet": "flux-2-klein-4b-fp8.safetensors", "clip": "qwen_3_4b_fp4_flux2.safetensors",
         "vae": "flux2-vae-klein4b.safetensors"}  # arquivos do catalogo do motor_local.py (todos Apache 2.0)
SESSION = "designer-mestre"
SIZES = {"1:1": (1024, 1024), "4:5": (896, 1088), "3:4": (832, 1088),
         "9:16": (768, 1344), "16:9": (1344, 768), "4:3": (1088, 832)}
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
NEG = "unintended text, watermark, signature, fabricated brand logo"


def req(method, path, body=None, timeout=30):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(ED + path, data=data, method=method,
                               headers={"Content-Type": "application/json"} if data else {})
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except urllib.error.URLError as e:
        sys.exit(f"[indisponivel] Motor local nao respondeu em {ED} ({e.reason}). "
                 "Use o gerador nativo da IDE ou inicie o motor local.")


def data_url(path):
    if not os.path.isfile(path):
        sys.exit(f"[erro] arquivo nao encontrado: {path}")
    ext = os.path.splitext(path)[1].lower()
    return f"data:{MIME.get(ext, 'image/png')};base64," + base64.b64encode(open(path, "rb").read()).decode()


def json_objects(buf):
    dec, i, out, s = json.JSONDecoder(), 0, [], buf.decode("utf-8", "replace")
    while i < len(s):
        j = s.find("{", i)
        if j < 0:
            break
        try:
            obj, i = dec.raw_decode(s, j)
            out.append(obj)
        except ValueError:
            i = j + 1
    return out


def wait(task_resp, timeout=900):
    j = json.loads(task_resp)
    stream = j.get("stream")
    if not stream:
        sys.exit("[erro] fila recusou a tarefa: " + json.dumps(j)[:500])
    t0 = time.time()
    while time.time() - t0 < timeout:
        code, buf = req("GET", stream, timeout=timeout)
        if code == 425:
            time.sleep(2)
            continue
        if code != 200:
            sys.exit(f"[erro] stream HTTP {code}: {buf[:300]!r}")
        for obj in reversed(json_objects(buf)):
            if obj.get("status") == "succeeded" and obj.get("output"):
                return obj
            if obj.get("status") == "failed":
                sys.exit("[erro] falha na renderizacao: " + str(obj.get("detail") or obj)[:500])
        time.sleep(2)
    sys.exit("[erro] tempo esgotado")


def save_outputs(res, out):
    paths = []
    base, ext = os.path.splitext(out)
    for n, item in enumerate(res["output"]):
        raw = item.get("data", "")
        raw = raw.split(",", 1)[1] if raw.startswith("data:") else raw
        p = out if n == 0 else f"{base}_{n + 1}{ext}"
        with open(p, "wb") as f:
            f.write(base64.b64decode(raw))
        paths.append((p, item.get("seed")))
    return paths


def sidecar(path, a, extra, ferramenta=f"Motor local ({ED})"):
    with open(os.path.splitext(path)[0] + ".txt", "w", encoding="utf-8") as f:
        f.write(f"ferramenta: {ferramenta}\n{extra}\ndata: {time.strftime('%Y-%m-%d %H:%M')}\n\n"
                f"PROMPT:\n{getattr(a, 'prompt', '-')}\n\nNEGATIVO:\n{getattr(a, 'neg', '-')}\n")


def comfy_no_ar(timeout=3):
    try:
        with urllib.request.urlopen(COMFY + "/system_stats", timeout=timeout):
            return True
    except (urllib.error.URLError, OSError):
        return False


def comfy_req(method, path, body=None, raw=None, ctype=None, timeout=60):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    hdr = {"Content-Type": ctype or "application/json"} if data else {}
    try:
        with urllib.request.urlopen(urllib.request.Request(COMFY + path, data=data, method=method, headers=hdr),
                                    timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"[erro] ComfyUI {path} HTTP {e.code}: {e.read()[:800]!r}")
    except urllib.error.URLError as e:
        sys.exit(f"[indisponivel] ComfyUI nao respondeu em {COMFY} ({e.reason}). "
                 "Ligar: python assets\\motor_local.py iniciar")


def comfy_upload(path):
    if not os.path.isfile(path):
        sys.exit(f"[erro] arquivo nao encontrado: {path}")
    b = uuid.uuid4().hex
    nome = os.path.basename(path)
    corpo = (f"--{b}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{nome}\"\r\n"
             f"Content-Type: {MIME.get(os.path.splitext(path)[1].lower(), 'image/png')}\r\n\r\n").encode() \
        + open(path, "rb").read() + f"\r\n--{b}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue" \
        f"\r\n--{b}--\r\n".encode()
    return json.loads(comfy_req("POST", "/upload/image", raw=corpo, ctype=f"multipart/form-data; boundary={b}"))["name"]


def comfy_workflow(prompt, w, h, seed, n, passos, refs):
    """Grafo da API equivalente ao template oficial do klein 4B destilado (t2i e edicao multirreferencia)."""
    g = {
        "unet": {"class_type": "UNETLoader", "inputs": {"unet_name": KLEIN["unet"], "weight_dtype": "default"}},
        "clip": {"class_type": "CLIPLoader", "inputs": {"clip_name": KLEIN["clip"], "type": "flux2", "device": "default"}},
        "vae": {"class_type": "VAELoader", "inputs": {"vae_name": KLEIN["vae"]}},
        "pos": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["clip", 0]}},
        "neg": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["pos", 0]}},
    }
    pos, neg = ["pos", 0], ["neg", 0]
    for i, nome in enumerate(refs):
        g[f"img{i}"] = {"class_type": "LoadImage", "inputs": {"image": nome}}
        g[f"esc{i}"] = {"class_type": "ImageScaleToTotalPixels",
                        "inputs": {"image": [f"img{i}", 0], "upscale_method": "nearest-exact",
                                   "megapixels": 1.0, "resolution_steps": 1}}
        g[f"lat{i}"] = {"class_type": "VAEEncode", "inputs": {"pixels": [f"esc{i}", 0], "vae": ["vae", 0]}}
        g[f"rp{i}"] = {"class_type": "ReferenceLatent", "inputs": {"conditioning": pos, "latent": [f"lat{i}", 0]}}
        g[f"rn{i}"] = {"class_type": "ReferenceLatent", "inputs": {"conditioning": neg, "latent": [f"lat{i}", 0]}}
        pos, neg = [f"rp{i}", 0], [f"rn{i}", 0]
    g.update({
        "guia": {"class_type": "CFGGuider", "inputs": {"model": ["unet", 0], "positive": pos, "negative": neg, "cfg": 1.0}},
        "amostr": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "sigmas": {"class_type": "Flux2Scheduler", "inputs": {"steps": passos, "width": w, "height": h}},
        "vazio": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": w, "height": h, "batch_size": n}},
        "ruido": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "sample": {"class_type": "SamplerCustomAdvanced",
                   "inputs": {"noise": ["ruido", 0], "guider": ["guia", 0], "sampler": ["amostr", 0],
                              "sigmas": ["sigmas", 0], "latent_image": ["vazio", 0]}},
        "dec": {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["vae", 0]}},
        "salvar": {"class_type": "SaveImage", "inputs": {"images": ["dec", 0], "filename_prefix": SESSION}},
    })
    return g


def cmd_gerar_comfy(a, w, h, seed):
    refs = ([a.init] if a.init else []) + a.ref[:4]
    if a.init:
        print("[info] klein edita por referencia: --init vira a imagem 1 e --forca nao se aplica; "
              "descreva no prompt o que muda e o que preserva.")
    passos = a.passos
    if a.dry_run:
        print(json.dumps(comfy_workflow(a.prompt, w, h, seed, a.n, passos, [os.path.basename(r) for r in refs]),
                         ensure_ascii=False, indent=1))
        return
    nomes = [comfy_upload(r) for r in refs]
    wf = comfy_workflow(a.prompt, w, h, seed, a.n, passos, nomes)
    pid = json.loads(comfy_req("POST", "/prompt", {"prompt": wf, "client_id": SESSION}))["prompt_id"]
    t0 = time.time()
    while time.time() - t0 < 900:
        hist = json.loads(comfy_req("GET", f"/history/{pid}")).get(pid)
        if hist and hist.get("status", {}).get("status_str") == "error":
            sys.exit("[erro] ComfyUI falhou: " + json.dumps(hist["status"].get("messages", []))[:800])
        if hist and hist.get("outputs", {}).get("salvar"):
            break
        time.sleep(1.5)
    else:
        sys.exit("[erro] tempo esgotado no ComfyUI")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    base, ext = os.path.splitext(a.out)
    for k, im in enumerate(hist["outputs"]["salvar"]["images"]):
        q = urllib.parse.urlencode({"filename": im["filename"], "subfolder": im["subfolder"], "type": im["type"]})
        p = a.out if k == 0 else f"{base}_{k + 1}{ext}"
        with open(p, "wb") as f:
            f.write(comfy_req("GET", f"/view?{q}"))
        sidecar(p, a, f"modelo: {KLEIN['unet']}\nseed: {seed} (lote {k + 1})\npassos: {passos}\n"
                      f"tamanho: {w}x{h} ({a.aspect})\nreferencias: {'; '.join(refs) or '-'}\n"
                      f"tempo: {time.time() - t0:.0f}s", ferramenta=f"Motor local ComfyUI ({COMFY})")
        print(f"[ok] {p}  seed {seed}")


def cmd_ping(_):
    print(f"ComfyUI {COMFY}: {'no ar' if comfy_no_ar() else 'parado'}")
    code, buf = req("GET", f"/ping?session_id={SESSION}") if not comfy_no_ar() else (0, b"")
    if code:
        print(code, buf.decode("utf-8", "replace")[:800])


def cmd_modelos(_):
    code, buf = req("GET", "/get/models")
    j = json.loads(buf)
    print(json.dumps(j.get("models", j), ensure_ascii=False, indent=1)[:4000])


def _destino_ok(out, pasta):
    """Lei 5: gerado vai so para Imagens\\IA; tratado para Imagens\\Tratadas. Nunca Originais/Banco/Referencias."""
    p = os.path.abspath(out).replace('/', '\\').lower()
    for proibido in ('\\originais\\', '\\banco de imagens\\', '\\referências\\', '\\referencias\\'):
        if proibido in p:
            sys.exit(f"[erro] destino proibido ({proibido.strip(chr(92))}): {out}\n  Use ...\\Compartilhada\\Imagens\\{pasta}\\")
    if f'\\{pasta.lower()}\\' not in p:
        sys.exit(f"[erro] destino fora de Imagens\\{pasta}\\: {out}")


def _aval_motor_local():
    """Motor local so roda com o sim unico do usuario, gravado por consentimento.py (vale em toda IA)."""
    if not consentimento.aprovado("motor_local.usar"):
        sys.exit("[sem-aval] motor local ainda nao aprovado pelo usuario. Rodar `motor_local.py detectar`, "
                 "fazer a pergunta 1 vez e, com o sim, `consentimento.py registrar motor_local.usar`.")


def cmd_gerar(a):
    if not a.dry_run:
        _destino_ok(a.out, 'IA')
    w, h = SIZES[a.aspect]
    seed = a.seed if a.seed is not None else int(time.time()) % 2**31
    if not a.dry_run:
        _aval_motor_local()
    if a.motor == "comfy":
        if not a.dry_run and not comfy_no_ar():
            r = subprocess.run([sys.executable, os.path.join(AQUI, "motor_local.py"), "iniciar"])
            if r.returncode:
                sys.exit("[erro] motor local nao ligou; ver: motor_local.py status / guia")
        return cmd_gerar_comfy(a, w, h, seed)
    body = {
        "request_id": uuid.uuid4().hex, "session_id": SESSION,
        "prompt": a.prompt, "negative_prompt": a.neg,
        "seed": seed,
        "width": w, "height": h, "num_outputs": a.n,
        "num_inference_steps": a.passos, "guidance_scale": a.cfg,
        "output_format": "png", "output_lossless": True,
        "vram_usage_level": a.vram, "block_nsfw": False, "stream_image_progress": False,
    }
    modelo = a.modelo or os.environ.get("ED_MODELO")
    if modelo:
        body["use_stable_diffusion_model"] = modelo
    if a.ref:
        body["ref_images"] = [data_url(p) for p in a.ref[:4]]
    if a.init:
        body["init_image"] = data_url(a.init)
        body["prompt_strength"] = a.forca
    if a.dry_run:
        show = {k: (f"<{len(v)} imagens>" if k == "ref_images" else ("<imagem>" if k == "init_image" else v))
                for k, v in body.items()}
        print(json.dumps(show, ensure_ascii=False, indent=1))
        return
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    code, buf = req("POST", "/render", body)
    if code != 200:
        sys.exit(f"[erro] /render HTTP {code}: {buf[:500]!r}"
                 + ("\n  Referencias exigem o motor v4 (Settings > Backend)." if a.ref else ""))
    res = wait(buf)
    for p, seed in save_outputs(res, a.out):
        sidecar(p, a, f"modelo: {modelo or 'padrao'}\nseed: {seed}\npassos: {a.passos} cfg: {a.cfg}\n"
                      f"tamanho: {w}x{h} ({a.aspect})\nreferencias: {'; '.join(a.ref) or '-'}\n"
                      f"init: {a.init or '-'} forca: {a.forca if a.init else '-'}")
        print(f"[ok] {p}  seed {seed}")


GEMINI = {"flash": "gemini-2.5-flash-image", "pro": "gemini-3-pro-image-preview"}


def cmd_gemini(a):
    """Gera pela Gemini API com a chave do proprio usuario (aistudio.google.com/apikey). Cobranca separada da assinatura."""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.exit("[sem-chave] GEMINI_API_KEY nao definida. Crie em https://aistudio.google.com/apikey e rode: "
                 'setx GEMINI_API_KEY "SUA_CHAVE" (reabra o terminal). Regra da Falha: parar e perguntar ao usuario.')
    _destino_ok(a.out, 'IA')
    modelo = os.environ.get("GEMINI_IMAGE_MODEL") or GEMINI["pro" if a.pro else "flash"]
    parts = [{"text": a.prompt}]
    for p in a.ref[:14]:
        mime, b64 = data_url(p)[5:].split(";base64,")
        parts.append({"inline_data": {"mime_type": mime, "data": b64}})
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": a.aspect}}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    r = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                               headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(r, timeout=300) as resp:
            j = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"[erro] Gemini HTTP {e.code}: {e.read()[:500]!r}")
    except urllib.error.URLError as e:
        sys.exit(f"[indisponivel] Gemini API inacessivel ({e.reason}).")
    imgs = [pt["inlineData"]["data"] for c in j.get("candidates", [])
            for pt in c.get("content", {}).get("parts", []) if "inlineData" in pt]
    if not imgs:
        sys.exit("[erro] Gemini nao devolveu imagem: " + json.dumps(j, ensure_ascii=False)[:500])
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    base, ext = os.path.splitext(a.out)
    for n, raw in enumerate(imgs):
        p = a.out if n == 0 else f"{base}_{n + 1}{ext}"
        with open(p, "wb") as f:
            f.write(base64.b64decode(raw))
        with open(os.path.splitext(p)[0] + ".txt", "w", encoding="utf-8") as f:
            f.write(f"ferramenta: Gemini API ({modelo})\nstatus: gerado\nreferencias: {'; '.join(a.ref) or '-'}\n"
                    f"proporcao: {a.aspect}\ndata: {time.strftime('%Y-%m-%d %H:%M')}\n\nPROMPT:\n{a.prompt}\n")
        print(f"[ok] {p}")


def cmd_upscale(a):
    _aval_motor_local()
    _destino_ok(a.out, 'IA' if '\\ia\\' in os.path.abspath(a.out).replace('/', '\\').lower() else 'Tratadas')
    filtros = ["realesrgan"] + (["codeformer"] if a.rosto else [])
    body = {"request_id": uuid.uuid4().hex, "session_id": SESSION, "image": data_url(a.imagem),
            "filter": filtros, "filter_params": {"scale": a.escala}, "output_format": "png",
            "output_lossless": True}
    code, buf = req("POST", "/filter", body)
    if code != 200:
        sys.exit(f"[erro] /filter HTTP {code}: {buf[:500]!r}")
    for p, _ in save_outputs(wait(buf), a.out):
        sidecar(p, a, f"upscale: {'+'.join(filtros)} x{a.escala}\norigem: {a.imagem}")
        print(f"[ok] {p}")


def cmd_registrar(a):
    """Copia imagem gerada por qualquer motor da IDE para Imagens\\IA\\ e grava o .txt de aprendizado."""
    if not os.path.isfile(a.imagem):
        sys.exit(f"[erro] arquivo nao encontrado: {a.imagem}")
    _destino_ok(a.out, 'IA')
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    base, ext = os.path.splitext(a.out)
    src_ext = os.path.splitext(a.imagem)[1].lower() or ".png"
    out = base + src_ext if ext.lower() != src_ext else a.out
    shutil.copy2(a.imagem, out)
    with open(base + ".txt", "w", encoding="utf-8") as f:
        f.write(f"ferramenta: {a.ferramenta}\nstatus: {a.status}\norigem: {a.imagem}\n"
                f"referencias: {'; '.join(a.ref) or '-'}\nnotas: {a.notas or '-'}\n"
                f"data: {time.strftime('%Y-%m-%d %H:%M')}\n\nPROMPT:\n{a.prompt}\n")
    print(f"[ok] {out}  + {base}.txt")


def main():
    ap = argparse.ArgumentParser(description="Gerador e registrador de imagens do /designer-mestre")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ping").set_defaults(f=cmd_ping)
    sub.add_parser("modelos").set_defaults(f=cmd_modelos)
    g = sub.add_parser("gerar")
    g.add_argument("prompt", help="prompt de acordo com a cena e a capacidade do modelo")
    g.add_argument("-o", "--out", required=True, help=".png em Compartilhada\\Imagens\\IA\\")
    g.add_argument("-a", "--aspect", default="4:5", choices=list(SIZES))
    g.add_argument("--ref", action="append", default=[], help="referencia (ate 4; mestra primeiro)")
    g.add_argument("--init", help="imagem base para img2img")
    g.add_argument("--forca", type=float, default=0.5, help="0.2 = quase igual a base, 0.8 = livre")
    g.add_argument("--neg", default=NEG)
    g.add_argument("--seed", type=int)
    g.add_argument("-n", type=int, default=1, help="variacoes por chamada")
    g.add_argument("--passos", type=int, default=4)
    g.add_argument("--cfg", type=float, default=1.0)
    g.add_argument("--modelo", help="nome do modelo local")
    g.add_argument("--vram", default="balanced", choices=["low", "balanced", "high"])
    g.add_argument("--motor", default="comfy", choices=["comfy", "ed"],
                   help="comfy = motor local da skill (liga sozinho); ed = Easy Diffusion ja instalado")
    g.add_argument("--dry-run", action="store_true")
    g.set_defaults(f=cmd_gerar)
    gm = sub.add_parser("gemini", help="gera pela Gemini API (chave propria em GEMINI_API_KEY)")
    gm.add_argument("prompt", help="prosa natural descritiva (imagem.md, opcao 2)")
    gm.add_argument("-o", "--out", required=True, help=".png em Compartilhada\\Imagens\\IA\\")
    gm.add_argument("-a", "--aspect", default="4:5", choices=list(SIZES))
    gm.add_argument("--ref", action="append", default=[], help="referencia (ate 14; mestra primeiro)")
    gm.add_argument("--pro", action="store_true", help="Nano Banana Pro (mais caro, melhor em texto/detalhe)")
    gm.set_defaults(f=cmd_gemini)
    u = sub.add_parser("upscale")
    u.add_argument("imagem")
    u.add_argument("-o", "--out", required=True)
    u.add_argument("--escala", type=int, default=2, choices=[2, 4])
    u.add_argument("--rosto", action="store_true", help="+ CodeFormer (nunca usar em pessoa real do cliente)")
    u.set_defaults(f=cmd_upscale)
    r = sub.add_parser("registrar", help="registra imagem gerada na IDE/qualquer motor com metadados de aprendizado")
    r.add_argument("imagem")
    r.add_argument("-o", "--out", required=True)
    r.add_argument("--prompt", required=True)
    r.add_argument("--ferramenta", default="IDE Native Image Generator")
    r.add_argument("--ref", action="append", default=[])
    r.add_argument("--status", default="gerado", choices=["gerado", "aprovado", "descartado"])
    r.add_argument("--notas", default="")
    r.set_defaults(f=cmd_registrar)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
