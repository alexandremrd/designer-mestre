#!/usr/bin/env node
// Builds index.html of style 03 · VSL with the kit of the approved reference (kit/, untouched).
// Run in the project's engine folder (<P>/motor, the copy of this template/ with vsl.json, src/ and assets/):
//   node assemble.mjs                 full composition
//   node assemble.mjs --camera-only     camera only in the same layouts and timings (safe-zone base: render/_camera-only.mp4);
//                                   run again without the option after the render
// What it does:
// - copies kit/kit.js, kit.css, fonts/ and sfx/ to assets/ and GSAP 3.14.2 from node_modules (npm install);
// - creates src/index.template.html (from the kit), src/beats.js (from beats-template.js) and vsl.json (from vsl-default.json) if missing;
// - reads assets/transcript.json ({"words":[{"text","start","end"}],"audio_duration_secs"}) + assets/caption-fixes.json;
// - turns on the caption that follows the mouth if assets/face-track.json exists (tools/track-mouth.py);
// - turns on the presenter cutout if assets/matte.webm exists;
// - applies the SKIN (skin-resolved.json here or in the parent folder): colors → kit variables (assets/pele.css),
//   fonts → assets/fonts/fontes.css; with origin "nativa" nothing changes and the result is the reference's;
// - applies the SOUND: vsl.json default = "enxuto" (R2); skin with effects off → none; intensity 0.3 → enxuto
//   and −3 dB; 0.6 or absent → whatever vsl.json says; 0.85 → "referencia" (the exact sound of the approved video);
// - writes index.html and meta.json; prints the summary.
import { readFileSync, writeFileSync, existsSync, cpSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const MOD = dirname(fileURLToPath(import.meta.url));
const M = join(MOD, "kit");
const SO_CAMERA = process.argv.includes("--camera-only");
const read = (p, d) => (existsSync(p) ? JSON.parse(readFileSync(p, "utf8")) : d);

mkdirSync("assets", { recursive: true });
for (const f of ["kit.js", "kit.css"]) cpSync(join(M, f), join("assets", f));
// GSAP 3.14.2 comes from the project's npm (same file as the reference; the library license stays in node_modules)
const gsapSrc = ["node_modules/gsap/dist/gsap.min.js", join(MOD, "node_modules/gsap/dist/gsap.min.js")].find(existsSync);
if (!gsapSrc) { console.error("GSAP missing: run npm install at the project root (package.json of the template)"); process.exit(1); }
cpSync(gsapSrc, join("assets", "gsap.min.js"));
cpSync(join(M, "fonts"), join("assets", "fonts"), { recursive: true });
cpSync(join(M, "sfx"), join("assets", "sfx"), { recursive: true });
mkdirSync("src", { recursive: true });
if (!existsSync("src/index.template.html")) cpSync(join(M, "index.template.html"), "src/index.template.html");
if (!existsSync("src/beats.js")) cpSync(join(MOD, "beats-template.js"), "src/beats.js");
if (!existsSync("vsl.json")) cpSync(join(MOD, "vsl-default.json"), "vsl.json");

const t = JSON.parse(readFileSync("assets/transcript.json", "utf8"));
const cfg = read("vsl.json", {});
for (const k of Object.keys(cfg)) if (k.startsWith("_")) delete cfg[k]; // comment keys
const dur = +(cfg.dur || t.audio_duration_secs).toFixed(3);
cfg.dur = dur;

// transcription fixes (names/terms Whisper gets wrong): assets/caption-fixes.json {"wrong": "right"}
const fix = read("assets/caption-fixes.json", {});
const fixW = (s) => { if (s in fix) return fix[s]; const m = s.match(/^(.*?)([.,!?;:]*)$/); return m && m[1] in fix ? fix[m[1]] + m[2] : s; };
const words = t.words.map((w) => ({ text: fixW(w.text), start: +w.start.toFixed(3), end: +w.end.toFixed(3) }));
const face = existsSync("assets/face-track.json") ? JSON.parse(readFileSync("assets/face-track.json", "utf8")) : null;

// ---------------- skin ----------------
const pelePath = ["skin-resolved.json", "../skin-resolved.json"].find(existsSync);
const pele = pelePath ? read(pelePath, null) : null;
const hex = (h) => { const x = h.replace("#", ""); const n = parseInt(x.length === 3 ? x.split("").map((c) => c + c).join("") : x, 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
const toHex = (c) => "#" + c.map((v) => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("");
const mix = (a, b, k) => toHex(hex(a).map((v, i) => v + (hex(b)[i] - v) * k)); // k=0 → a, k=1 → b
const lt = (c, k) => mix(c, "#ffffff", k), dk = (c, k) => mix(c, "#000000", k);
const rgb = (c) => hex(c).join(",");
let peleCss = "", peleNota = "native (same as the reference)";
const cores = pele && pele.cores;
if (cores && !String(cores.origem || "nativa").startsWith("nativa")) {
  const { fundo: F, texto: T, destaque: D, apoio: A, acento2: X } = cores;
  peleCss += `#vsl{
  --bg0:${dk(F, 0.45)}; --bg1:${F}; --bg2:${lt(F, 0.12)}; --bg3:${lt(F, 0.25)}; --panel2:${dk(F, 0.15)}; --thumb:${lt(F, 0.08)};
  --panelRGB:${rgb(lt(F, 0.1))}; --panel2RGB:${rgb(dk(F, 0.2))}; --shadowRGB:${rgb(dk(F, 0.8))};
  --blob1:${mix(D, F, 0.3)}; --blob2:${mix(dk(D, 0.35), F, 0.3)}; --blob3:${mix(dk(D, 0.2), F, 0.3)};
  --acc:${D}; --acc2:${lt(D, 0.08)}; --deep:${dk(D, 0.1)}; --accRGB:${rgb(D)};
  --btnA:${D}; --btnB:${lt(D, 0.2)};
  --tintTopRGB:${rgb(dk(D, 0.3))}; --tintMidRGB:${rgb(dk(D, 0.6))}; --tintEndRGB:${rgb(dk(D, 0.88))};
  --lav:${A}; --lav2:${dk(A, 0.08)}; --lavT:${lt(A, 0.4)}; --hiRGB:${rgb(A)};
  --tint2:linear-gradient(100deg,rgba(${rgb(A)},.55) 0%,rgba(${rgb(D)},.25) 45%,rgba(${rgb(lt(D, 0.2))},.35) 100%);
  --white:${T}; --muted:${X}; --dim:${dk(X, 0.35)};
}
#vsl, html, body{ color:${T}; }\n`;
  peleNota = `colors ${cores.origem}`;
}
const fontes = pele && pele.fontes;
let fontesLink = "";
if (fontes && existsSync("assets/fonts/fontes.css")) {
  const fam = (s) => s && s.familia && s.nativa !== true && s.familia !== "nativa" ? `"${s.familia}"` : null;
  const fd = fam(fontes.destaque), fs = fam(fontes.texto);
  if (fd || fs) {
    fontesLink = `<link rel="stylesheet" href="assets/fonts/fontes.css">\n`;
    peleCss += `#vsl{ ${fd ? `--fD:${fd},sans-serif;` : ""} ${fs ? `--fS:${fs},sans-serif;` : ""} }\n`;
    peleNota += ` · fonts${[fd, fs].filter(Boolean).join(" / ")}`;
  }
}
if (peleCss) writeFileSync("assets/pele.css", "/* generated by assemble.mjs from skin-resolved.json — do not edit */\n" + peleCss);

// ---------------- sound ----------------
let sfxNota = cfg.sfxModo === "enxuto" ? "lean (R2)" : "as in the reference";
const som = pele && pele.som;
if (som && som.sfx === false) { cfg.sfx = false; sfxNota = "off (skin)"; }
else if (som && som.sfxIntensidade != null) {
  const base = cfg.sfxVol ?? 0.55;
  if (som.sfxIntensidade <= 0.3) { cfg.sfxModo = "enxuto"; cfg.sfxVol = +(base * 0.708).toFixed(3); sfxNota = "lean (R2) −3 dB"; }
  else if (som.sfxIntensidade >= 0.85) { cfg.sfxModo = "referencia"; sfxNota = "as in the reference (~1.4/s; verify.py fails the SFX item)"; }
}
if (SO_CAMERA) { cfg.sfx = false; sfxNota = "none (camera only)"; }
const sfxFiltro = cfg.sfxModo === "enxuto" ? readFileSync(join(MOD, "sfx-lean.js"), "utf8") : "";

// ---------------- matte and music ----------------
const matte = existsSync("assets/matte.webm")
  ? `<div class="lens" id="lensMatte"><video id="matte" src="assets/matte.webm" data-start="0" data-duration="${dur}" data-track-index="2" muted playsinline></video></div>`
  : "<!-- no assets/matte.webm: 'behind the head' text stays in front -->";
let music = "";
if (cfg.music && existsSync(join("assets", cfg.music.file))) {
  const s = cfg.music.start || 0;
  music = `<audio id="music" src="assets/${cfg.music.file}" data-start="${s}" data-duration="${(dur - s).toFixed(3)}" data-track-index="3" data-volume="${cfg.music.volume ?? 0.18}"></audio>`;
}

// ---------------- index.html ----------------
const beats = readFileSync("src/beats.js", "utf8");
let html = readFileSync("src/index.template.html", "utf8")
  .replaceAll("__DUR__", String(dur)).replace("__CFG__", JSON.stringify(cfg)).replace("__WORDS__", JSON.stringify(words)).replace("__FACE__", JSON.stringify(face))
  .replace("__CLASS__", `t-${cfg.theme || "roxo"} f-${cfg.font || "padrao"}`)
  .replace("__MATTE__", matte).replace("__MUSIC__", music).replace("__BEATS__", beats + (sfxFiltro ? "\n" + sfxFiltro : ""));
if (peleCss) html = html.replace('<link rel="stylesheet" href="assets/kit.css">', `<link rel="stylesheet" href="assets/kit.css">\n${fontesLink}<link rel="stylesheet" href="assets/pele.css">`);
if (SO_CAMERA) html = html.replace("</head>", `<style>#ui,#cap,#fx,#behind,#inset,#cover,#under{display:none!important}</style>\n</head>`);
writeFileSync("index.html", html);
const meta = read("meta.json", {});
Object.assign(meta, { id: "vsl", width: 1080, height: 1920, fps: 30 });
writeFileSync("meta.json", JSON.stringify(meta, null, 2));
if (!existsSync("hyperframes.json")) cpSync(join(MOD, "hyperframes.json"), "hyperframes.json");
console.log(`index.html ok${SO_CAMERA ? " (CAMERA ONLY — run again without --camera-only after the render)" : ""} — ${dur}s · ${words.length} words · mouth: ${face ? "yes" : "NO (run tools/track-mouth.py)"} · matte: ${matte.startsWith("<div") ? "yes" : "no"} · music: ${music ? "yes" : "no"} · skin: ${peleNota} · sfx: ${sfxNota}`);
