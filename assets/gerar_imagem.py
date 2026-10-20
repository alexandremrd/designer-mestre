#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_imagem.py - Utilitario de geracao local, upscale e registro universal de imagens do /designer-mestre.

A IDE tem autonomia para decidir o melhor caminho de geracao (ferramenta/subagente nativo da IDE,
motor local via Easy Diffusion em http://127.0.0.1:9000, ou composicao hibrida).
Toda imagem gerada por qualquer motor e salva/registrada em Compartilhada\\Imagens\\IA\\ com seu .txt
contendo ferramenta, modelo, seed, referencias e prompt para aprendizado continuo.

Comandos:
  python gerar_imagem.py registrar <imagem_gerada> -o "...\\IA\\2026-10-20_tema_v1.png" --prompt "..." --ferramenta "<motor>" [--ref mestra.jpg] [--status aprovado|descartado] [--notas "..."]
  python gerar_imagem.py ping
  python gerar_imagem.py modelos
  python gerar_imagem.py gerar "PROMPT EN" [--ref mestra.jpg] [--init base.jpg --forca 0.45] -a 4:5 -o "...\\IA\\nome.png"
  python gerar_imagem.py upscale foto.png -o foto_4x.png [--escala 2|4]
"""
import argparse, base64, json, os, shutil, sys, time, uuid
import urllib.request, urllib.error

ED = os.environ.get("ED_URL", "http://127.0.0.1:9000").rstrip("/")
SESSION = "designer-mestre"
SIZES = {"1:1": (1024, 1024), "4:5": (896, 1088), "3:4": (832, 1088),
         "9:16": (768, 1344), "16:9": (1344, 768), "4:3": (1088, 832)}
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
NEG = ("text, letters, watermark, logo, signature, ui, app interface, phone mockup, status bar, "
       "buttons, plastic skin, airbrushed face, oversaturated, artificial hdr, deformed, extra fingers, blurry, apple logo")


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


def sidecar(path, a, extra):
    with open(os.path.splitext(path)[0] + ".txt", "w", encoding="utf-8") as f:
        f.write(f"ferramenta: Motor local ({ED})\n{extra}\ndata: {time.strftime('%Y-%m-%d %H:%M')}\n\n"
                f"PROMPT:\n{getattr(a, 'prompt', '-')}\n\nNEGATIVO:\n{getattr(a, 'neg', '-')}\n")


def cmd_ping(_):
    code, buf = req("GET", f"/ping?session_id={SESSION}")
    print(code, buf.decode("utf-8", "replace")[:800])


def cmd_modelos(_):
    code, buf = req("GET", "/get/models")
    j = json.loads(buf)
    print(json.dumps(j.get("models", j), ensure_ascii=False, indent=1)[:4000])


def cmd_gerar(a):
    w, h = SIZES[a.aspect]
    body = {
        "request_id": uuid.uuid4().hex, "session_id": SESSION,
        "prompt": a.prompt, "negative_prompt": a.neg,
        "seed": a.seed if a.seed is not None else int(time.time()) % 2**31,
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


def cmd_upscale(a):
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
    g.add_argument("prompt", help="prompt em ingles (formula do imagem.md)")
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
    g.add_argument("--dry-run", action="store_true")
    g.set_defaults(f=cmd_gerar)
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
