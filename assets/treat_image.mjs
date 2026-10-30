#!/usr/bin/env node
// treat_image.mjs - LAST RESORT of /designer-mestre when no generator works (Failure Rule, `operations.md` §0.6).
// Treats an EXISTING image with sharp (libvips): frame, enlarge, compose. Does not create a new image; quality inferior to generation.
// Install once:  npm i --prefix "<resource root>\Ferramentas\node" sharp   (one copy for all AIs;
//               without a defined root: cd assets && npm i sharp)
//
//   node treat_image.mjs frame <in> -o "...\Tratadas\name_trat.png" [-a 4:5] [--width 1080]
//   node treat_image.mjs enlarge   <in> -o "...\Tratadas\name_trat.png" [--scale 2]
//   node treat_image.mjs compose    <background> <front> -o "...\Tratadas\name_trat.png" [--x 0 --y 0 --front-width 600]
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { createRequire } from "node:module";

// sharp comes from the resource root (resources.py registry); without it, from the node_modules next to this file.
function pastaNode() {
  try {
    const c = JSON.parse(fs.readFileSync([ "local_engine.json", "motor_local.json" ].map((n) => path.join(os.homedir(), ".designer-mestre", n)).find((p) => fs.existsSync(p)) || "", "utf8").replace(/^﻿/, ""));
    return c.caminhos?.node || (c.motores ? path.join(c.motores, "Ferramentas", "node") : null);
  } catch { return null; }
}
let sharp;
try {
  const node = pastaNode();
  sharp = node && fs.existsSync(path.join(node, "node_modules", "sharp"))
    ? createRequire(path.join(node, "package.json"))("sharp")
    : (await import("sharp")).default;
}
catch (e) { console.error(`[no-sharp] ${String(e.message || e).split("\n")[0]}\nRun: npm i --prefix "<root>\\Ferramentas\\node" sharp   (the root comes from local_engine.json; \`python assets\\resources.py\` shows the path)`); process.exit(1); }

const ASPECT = { "1:1": 1, "4:5": 4 / 5, "3:4": 3 / 4, "9:16": 9 / 16, "16:9": 16 / 9, "4:3": 4 / 3 };
const [cmd, ...rest] = process.argv.slice(2);
const pos = [], opt = {};
for (let i = 0; i < rest.length; i++) {
  if (rest[i] === "--replace") opt.substituir = true;  // flag without a value
  else if (rest[i].startsWith("-")) opt[rest[i].replace(/^-+/, "")] = rest[++i];
  else pos.push(rest[i]);
}
const out = opt.o || opt.out;
const fail = (m) => { console.error(m); process.exit(1); };
if (!cmd || !out || !pos.length) fail("usage: see the header of treat_image.mjs");
for (const p of pos) if (!fs.existsSync(p)) fail(`[error] file not found: ${p}`);

// Law 5: treated goes only to Imagens\Tratadas (never Originais/Banco/Referencias).
const dest = path.resolve(out).replaceAll("/", "\\").toLowerCase();
if (/\\(originais|banco de imagens|refer[eê]ncias)\\/.test(dest)) fail(`[error] forbidden destination: ${out}`);
if (!dest.includes("\\tratadas\\")) fail(`[error] destination outside Imagens\\Tratadas\\: ${out}`);
if (fs.existsSync(out) && !opt.substituir) fail(`[error] ${out} already exists; use another name (version) or --replace`);
fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });

const fino = (img) => img.sharpen({ sigma: 0.6 });
let info;
if (cmd === "frame") {
  const r = ASPECT[opt.a || "4:5"] ?? fail("[error] -a: " + Object.keys(ASPECT).join(" "));
  const w = Number(opt.width || 1080), h = Math.round(w / r);
  info = `frame ${opt.a || "4:5"} ${w}x${h} (attention-based crop)`;
  await fino(sharp(pos[0]).resize(w, h, { fit: "cover", position: sharp.strategy.attention, kernel: "lanczos3" })).toFile(out);
} else if (cmd === "enlarge") {
  const k = Number(opt.scale || 2), m = await sharp(pos[0]).metadata();
  info = `enlarge x${k} lanczos3 (interpolation, no new detail)`;
  await fino(sharp(pos[0]).resize(m.width * k, m.height * k, { kernel: "lanczos3" })).toFile(out);
} else if (cmd === "compose") {
  if (pos.length < 2) fail("[error] compose <background> <front>");
  let frente = sharp(pos[1]);
  if (opt["front-width"]) frente = frente.resize(Number(opt["front-width"]));
  info = `compose ${path.basename(pos[1])} over ${path.basename(pos[0])} at${opt.x || 0},${opt.y || 0}`;
  await sharp(pos[0]).composite([{ input: await frente.toBuffer(), left: Number(opt.x || 0), top: Number(opt.y || 0) }]).toFile(out);
} else fail(`[error] unknown command: ${cmd}`);

// success only if the written file opens back with dimensions
const lido = await sharp(out).metadata().catch(() => ({}));
if (!lido.width || !lido.height) fail(`[error] empty or invalid output: ${out}`);

fs.writeFileSync(out.replace(/\.[^.\\/]+$/, "") + ".txt",
  `tool: sharp (last resort)\nquality: INFERIOR to generation, user warned\noperation: ${info}\n` +
  `source: ${pos.join("; ")}\ndate: ${new Date().toISOString().slice(0, 16).replace("T", " ")}\n`, "utf8");
console.log(`[ok] ${out}  (inferior quality: warn the user)`);
