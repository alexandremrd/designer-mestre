#!/usr/bin/env python3
"""
qa_html.py - QA automatico de paginas HTML do agente /design.

Uso:
    python qa_html.py pagina.html [--saida pasta] [--sem-render]

Gera <saida>/qa_relatorio.md e screenshots em 375, 768 e 1440 px.
Codigo de saida: 0 = sem FALHAS (pode ter avisos), 1 = ha FALHAS.

Verificacoes estaticas (sempre):
  - bytes nao-ASCII, mojibake (�, "A~", "??" no meio de palavra)
  - CSS/JS externos (exigencia de arquivo unico), placeholders e lorem ipsum
  - meta viewport, title, description, lang, og:image, canonical, favicon
  - um unico H1, hierarquia de titulos, imagens sem alt / sem width+height
  - inputs sem label, URL de webhook ainda placeholder, peso do arquivo e do base64
Verificacoes com navegador (Playwright + Chromium, se instalados):
  - rolagem horizontal em 375 / 768 / 1440 px
  - faixa entre secoes (gap > 1 px entre blocos vizinhos)
  - H1 visivel SEM JavaScript e COM JavaScript
  - erros de console, alvos de toque < 44 px no mobile, contraste de texto
  - mascara de telefone: digita, apaga e mantem os digitos
"""
import argparse
import os
import re
import sys
from html.parser import HTMLParser

FALHA, AVISO, OK = "FALHA", "AVISO", "OK"


class Coletor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []          # (tag, attrs dict)
        self.titulos = []       # (nivel, texto)
        self._em_titulo = None
        self._buf = ""
        self.title = ""
        self._em_title = False
        self.labels_for = set()
        self._label_depth = 0
        self.inputs_dentro_label = 0

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        self.tags.append((tag, a))
        if re.fullmatch(r"h[1-6]", tag):
            self._em_titulo = int(tag[1]); self._buf = ""
        if tag == "title":
            self._em_title = True
        if tag == "label":
            self._label_depth += 1
            if a.get("for"):
                self.labels_for.add(a["for"])
        if tag in ("input", "select", "textarea") and self._label_depth:
            a["_dentro_label"] = "1"

    def handle_endtag(self, tag):
        if self._em_titulo and tag == f"h{self._em_titulo}":
            self.titulos.append((self._em_titulo, self._buf.strip()))
            self._em_titulo = None
        if tag == "title":
            self._em_title = False
        if tag == "label" and self._label_depth:
            self._label_depth -= 1

    def handle_data(self, data):
        if self._em_titulo:
            self._buf += data
        if self._em_title:
            self.title += data


def estatico(caminho, raw, texto):
    r = []
    add = lambda nivel, item, det="": r.append((nivel, item, det))

    # Arquivo e caracteres
    kb = len(raw) / 1024
    add(OK if kb < 1500 else AVISO, "Peso do arquivo", f"{kb:.0f} KB")
    nao_ascii = [i + 1 for i, l in enumerate(raw.split(b"\n")) if any(b > 127 for b in l)]
    add(OK if not nao_ascii else FALHA, "Zero bytes nao-ASCII (anti-mojibake)",
        "" if not nao_ascii else f"{len(nao_ascii)} linha(s): {nao_ascii[:12]}")
    moj = []
    if "�" in texto: moj.append("caractere de substituicao")
    if re.search(r"Ã[\u0080-¿ -ÿ]", texto): moj.append("sequencia tipo 'Ã©'")
    if re.search(r"[A-Za-z]\?\?+[A-Za-z]", texto): moj.append("'??' dentro de palavra")
    add(OK if not moj else FALHA, "Sem texto corrompido", ", ".join(moj))
    b64 = sum(len(m) for m in re.findall(r"data:[^;]+;base64,[A-Za-z0-9+/=]+", texto)) / 1024
    add(OK if b64 < 800 else AVISO, "Imagens em base64",
        f"{b64:.0f} KB" + ("" if b64 < 800 else " (pesado: prefira URL hospedada no construtor)"))

    p = Coletor(); p.feed(texto)
    tags = p.tags
    def todos(t): return [a for (tg, a) in tags if tg == t]

    # Arquivo unico
    css_ext = [a.get("href") for a in todos("link") if "stylesheet" in a.get("rel", "") and "fonts.googleapis.com" not in a.get("href", "")]
    js_ext = [a.get("src") for a in todos("script") if a.get("src")]
    add(OK if not css_ext else FALHA, "Sem CSS externo (arquivo unico)", ", ".join(css_ext))
    add(OK if not js_ext else AVISO, "Sem JS externo (arquivo unico)", ", ".join(js_ext))

    # Placeholders
    pl = re.findall(r"(placehold\.co|via\.placeholder\.com|picsum\.photos|dummyimage\.com|placekitten|fakeimg|lorem ipsum)", texto, re.I)
    add(OK if not pl else FALHA, "Sem placeholders / lorem ipsum", ", ".join(sorted(set(x.lower() for x in pl))))
    marc = re.findall(r"\[(?:Headline|Subt|T&iacute;tulo|Texto|LOGO|CLIENTE)[^\]]{0,40}\]", texto)
    add(OK if not marc else AVISO, "Sem marcadores [ ] de template", f"{len(marc)} encontrado(s)" if marc else "")
    add(OK if "COLE_AQUI" not in texto else AVISO, "Webhook configurado", "URL ainda e placeholder" if "COLE_AQUI" in texto else "")

    # Head / SEO
    metas = todos("meta")
    def meta(n): return next((m.get("content", "") for m in metas if m.get("name", "").lower() == n or m.get("property", "").lower() == n), None)
    html_tag = next((a for (t, a) in tags if t == "html"), {})
    add(OK if html_tag.get("lang") else FALHA, "<html lang>", html_tag.get("lang", ""))
    add(OK if meta("viewport") else FALHA, "meta viewport")
    tl = len(p.title.strip())
    add(OK if 10 <= tl <= 65 else AVISO, "<title> (10-65 caracteres)", f"{tl} caracteres")
    d = meta("description")
    add(OK if d and 70 <= len(d) <= 170 else AVISO, "meta description (70-170)", f"{len(d)} caracteres" if d else "ausente")
    add(OK if meta("og:image") else AVISO, "og:image (compartilhamento)")
    add(OK if meta("og:title") else AVISO, "og:title")
    links = todos("link")
    add(OK if any("canonical" in l.get("rel", "") for l in links) else AVISO, "link canonical")
    add(OK if any("icon" in l.get("rel", "") for l in links) else AVISO, "favicon")

    # Estrutura
    h1s = [t for t in p.titulos if t[0] == 1]
    add(OK if len(h1s) == 1 else FALHA, "Exatamente um H1", f"{len(h1s)} H1")
    saltos = [f"H{a}->H{b}" for (a, _), (b, _) in zip(p.titulos, p.titulos[1:]) if b > a + 1]
    add(OK if not saltos else AVISO, "Hierarquia de titulos sem saltos", ", ".join(saltos[:6]))
    imgs = todos("img")
    sem_alt = [i.get("src", "")[:50] for i in imgs if "alt" not in i]
    sem_dim = [i.get("src", "")[:50] for i in imgs if not (i.get("width") and i.get("height"))]
    add(OK if not sem_alt else FALHA, "Imagens com alt", f"{len(sem_alt)} sem alt")
    add(OK if not sem_dim else AVISO, "Imagens com width/height (evita CLS)", f"{len(sem_dim)} sem dimensoes")
    campos = [a for (t, a) in tags if t in ("input", "select", "textarea") and a.get("type", "") not in ("hidden", "submit", "button")]
    sem_label = [c.get("name") or c.get("id") or "?" for c in campos
                 if not c.get("_dentro_label") and c.get("id", "") not in p.labels_for and not c.get("aria-label")
                 and c.get("tabindex") != "-1"]
    add(OK if not sem_label else FALHA, "Campos com label", ", ".join(sem_label))
    add(OK if re.search(r"prefers-reduced-motion", texto) or not re.search(r"@keyframes|transition", texto) else AVISO,
        "Respeita prefers-reduced-motion")
    return r


def render(caminho, saida):
    r = []
    add = lambda nivel, item, det="": r.append((nivel, item, det))
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        add(AVISO, "Render no navegador", "Playwright nao instalado: pip install playwright && playwright install chromium")
        return r
    url = "file:///" + os.path.abspath(caminho).replace("\\", "/").lstrip("/")
    exe = "/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None
    with sync_playwright() as pw:
        try:
            b = pw.chromium.launch(**({"executable_path": exe} if exe and os.path.isfile(exe) else {}))
        except Exception:
            b = pw.chromium.launch()
        erros = []
        for w in (375, 768, 1440):
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.on("console", lambda m: m.type == "error" and erros.append(m.text))
            pg.on("pageerror", lambda e: erros.append(str(e)))
            pg.route(re.compile(r"https://hook\..*make\.com.*|.*webhook.*"), lambda rt: rt.fulfill(status=200, body="ok"))
            pg.goto(url, wait_until="load"); pg.wait_for_timeout(3000)
            sw = pg.evaluate("Math.max(document.documentElement.scrollWidth, document.body.scrollWidth)")
            add(OK if sw <= w else FALHA, f"Sem rolagem horizontal em {w}px", f"largura do conteudo {sw}px")
            pg.screenshot(path=os.path.join(saida, f"qa_{w}.png"), full_page=True)
            if w == 375:
                gaps = pg.evaluate("""() => {
                  const sel = 'section, header, footer, main > div, body > div > section';
                  const els = [...document.querySelectorAll(sel)].filter(e => {
                    const r = e.getBoundingClientRect(); return r.height > 40 && getComputedStyle(e).position !== 'fixed';});
                  const out = []; const top = els.filter(e => !els.some(o => o !== e && o.contains(e)));
                  top.sort((a,b)=>a.getBoundingClientRect().top-b.getBoundingClientRect().top);
                  for (let i=1;i<top.length;i++){const a=top[i-1].getBoundingClientRect(), c=top[i].getBoundingClientRect();
                    const g=Math.round(c.top-a.bottom); if (g>1) out.push(g+'px antes de <'+top[i].tagName.toLowerCase()+(top[i].id?'#'+top[i].id:'')+'>');}
                  return out; }""")
                add(OK if not gaps else AVISO, "Sem faixa entre blocos", "; ".join(gaps[:6]))
                peq = pg.evaluate("""() => [...document.querySelectorAll('a, button, input, select, textarea')]
                  .filter(e => { const r=e.getBoundingClientRect(); const s=getComputedStyle(e);
                     return r.width>0 && r.height>0 && s.visibility!=='hidden' && (r.height<44 || r.width<44)
                       && !(e.tagName==='A' && getComputedStyle(e.parentElement).display.includes('inline') && e.closest('p,li'))
                       && e.tabIndex !== -1; })
                  .map(e => (e.tagName+' '+(e.innerText||e.name||'').trim()).slice(0,40))""")
                add(OK if not peq else AVISO, "Alvos de toque >= 44px (mobile)", f"{len(peq)}: " + "; ".join(peq[:5]))
                contraste = pg.evaluate("""() => {
                  const lum=c=>{const v=c.match(/[\\d.]+/g).slice(0,3).map(Number).map(x=>{x/=255;return x<=0.03928?x/12.92:Math.pow((x+0.055)/1.055,2.4)});return .2126*v[0]+.7152*v[1]+.0722*v[2];};
                  const bg=e=>{for(let n=e;n;n=n.parentElement){const s=getComputedStyle(n);if(s.backgroundImage!=='none')return null;
                     const m=s.backgroundColor.match(/[\\d.]+/g);if(m&&(m.length<4||+m[3]>0.9))return s.backgroundColor;}return 'rgb(255,255,255)';};
                  const out=[];const seen=new Set();
                  for(const e of document.querySelectorAll('body *')){
                    if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim().length>1))continue;
                    const s=getComputedStyle(e); const r=e.getBoundingClientRect(); if(!r.width||s.visibility==='hidden'||+s.opacity<0.1)continue;
                    const b=bg(e); if(!b)continue; const L1=lum(s.color),L2=lum(b);
                    const ratio=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05); const fs=parseFloat(s.fontSize);
                    const big=fs>=24||(fs>=18.66&&+s.fontWeight>=700); const min=big?3:4.5;
                    if(ratio<min){const t=e.textContent.trim().slice(0,30); if(!seen.has(t)){seen.add(t);out.push(t+' ('+ratio.toFixed(2)+':1)');}}}
                  return out;}""")
                add(OK if not contraste else AVISO, "Contraste de texto (WCAG AA)", f"{len(contraste)}: " + "; ".join(contraste[:5]))
                if pg.query_selector('input[type="tel"]'):
                    t = pg.query_selector('input[type="tel"]'); t.click(); t.fill("")
                    pg.keyboard.type("11987654321"); v1 = t.input_value()
                    pg.keyboard.press("Backspace"); pg.keyboard.press("Backspace"); v2 = t.input_value()
                    ok = re.sub(r"\D", "", v1) == "11987654321" and len(re.sub(r"\D", "", v2)) == 9
                    add(OK if ok else FALHA, "Mascara de telefone (digita e apaga)", f"'{v1}' -> '{v2}'")
            if w == 1440:
                h1 = pg.evaluate("""() => {const h=document.querySelector('h1'); if(!h) return 'sem h1';
                  const s=getComputedStyle(h), r=h.getBoundingClientRect();
                  return (+s.opacity>0.5 && s.visibility!=='hidden' && s.display!=='none' && r.height>0) ? 'ok' : 'opacity '+s.opacity;}""")
                add(OK if h1 == "ok" else FALHA, "H1 visivel com JS (apos 3 s)", h1)
            pg.close()
        ctx = b.new_context(java_script_enabled=False, viewport={"width": 1440, "height": 900})
        pg = ctx.new_page(); pg.goto(url)
        h1 = pg.evaluate("""() => {const h=document.querySelector('h1'); if(!h) return 'sem h1';
              const s=getComputedStyle(h), r=h.getBoundingClientRect();
              return (+s.opacity>0.5 && s.visibility!=='hidden' && s.display!=='none' && r.height>0) ? 'ok' : 'opacity '+s.opacity;}""")
        add(OK if h1 == "ok" else FALHA, "H1 visivel SEM JavaScript", h1)
        ctx.close()
        erros = sorted(set(erros))
        rede = [e for e in erros if "net::ERR_" in e or "Failed to load resource" in e]
        js = [e for e in erros if e not in rede]
        add(OK if not js else FALHA, "Sem erros de JavaScript", "; ".join(e[:80] for e in js[:4]))
        add(OK if not rede else AVISO, "Recursos externos carregaram", f"{len(rede)} falha(s) de rede (sem internet ou URL quebrada)")
        b.close()
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo")
    ap.add_argument("--saida", default=None)
    ap.add_argument("--sem-render", action="store_true")
    a = ap.parse_args()
    raw = open(a.arquivo, "rb").read()
    texto = raw.decode("utf-8", errors="replace")
    saida = a.saida or os.path.join(os.path.dirname(os.path.abspath(a.arquivo)), "qa")
    os.makedirs(saida, exist_ok=True)
    res = estatico(a.arquivo, raw, texto)
    if not a.sem_render:
        res += render(a.arquivo, saida)
    nf = sum(1 for n, _, _ in res if n == FALHA); na = sum(1 for n, _, _ in res if n == AVISO)
    linhas = [f"# QA - {os.path.basename(a.arquivo)}", "",
              f"**{nf} falha(s), {na} aviso(s)**", "", "| Status | Verificacao | Detalhe |", "|---|---|---|"]
    ordem = {FALHA: 0, AVISO: 1, OK: 2}
    for n, item, det in sorted(res, key=lambda x: ordem[x[0]]):
        linhas.append(f"| {n} | {item} | {det.replace('|', '/')} |")
    rel = "\n".join(linhas) + "\n"
    open(os.path.join(saida, "qa_relatorio.md"), "w", encoding="utf-8").write(rel)
    print(rel)
    print(f"Relatorio e screenshots em: {saida}")
    sys.exit(1 if nf else 0)


if __name__ == "__main__":
    main()
