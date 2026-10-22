#!/usr/bin/env node
// tratar_imagem.mjs - ULTIMO RECURSO do /designer-mestre quando nenhum gerador funciona (Regra da Falha, SKILL.md §0.6).
// Trata imagem EXISTENTE com sharp (libvips): enquadrar, ampliar, compor. Nao cria imagem nova; qualidade inferior a geracao.
// Instalar 1x:  cd assets && npm i sharp
//
//   node tratar_imagem.mjs enquadrar <in> -o "...\Tratadas\nome_trat.png" [-a 4:5] [--largura 1080]
//   node tratar_imagem.mjs ampliar   <in> -o "...\Tratadas\nome_trat.png" [--escala 2]
//   node tratar_imagem.mjs compor    <fundo> <frente> -o "...\Tratadas\nome_trat.png" [--x 0 --y 0 --largura-frente 600]
import fs from "node:fs";
import path from "node:path";

let sharp;
try { sharp = (await import("sharp")).default; }
catch { console.error("[sem-sharp] Rode: cd assets && npm i sharp"); process.exit(1); }

const ASPECT = { "1:1": 1, "4:5": 4 / 5, "3:4": 3 / 4, "9:16": 9 / 16, "16:9": 16 / 9, "4:3": 4 / 3 };
const [cmd, ...rest] = process.argv.slice(2);
const pos = [], opt = {};
for (let i = 0; i < rest.length; i++) {
  if (rest[i].startsWith("-")) opt[rest[i].replace(/^-+/, "")] = rest[++i];
  else pos.push(rest[i]);
}
const out = opt.o || opt.out;
const fail = (m) => { console.error(m); process.exit(1); };
if (!cmd || !out || !pos.length) fail("uso: ver cabecalho de tratar_imagem.mjs");
for (const p of pos) if (!fs.existsSync(p)) fail(`[erro] arquivo nao encontrado: ${p}`);

// Lei 5: tratado vai so para Imagens\Tratadas (nunca Originais/Banco/Referencias).
const dest = path.resolve(out).replaceAll("/", "\\").toLowerCase();
if (/\\(originais|banco de imagens|refer[eê]ncias)\\/.test(dest)) fail(`[erro] destino proibido: ${out}`);
if (!dest.includes("\\tratadas\\")) fail(`[erro] destino fora de Imagens\\Tratadas\\: ${out}`);
fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });

const fino = (img) => img.sharpen({ sigma: 0.6 });
let info;
if (cmd === "enquadrar") {
  const r = ASPECT[opt.a || "4:5"] ?? fail("[erro] -a: " + Object.keys(ASPECT).join(" "));
  const w = Number(opt.largura || 1080), h = Math.round(w / r);
  info = `enquadrar ${opt.a || "4:5"} ${w}x${h} (corte por atencao)`;
  await fino(sharp(pos[0]).resize(w, h, { fit: "cover", position: sharp.strategy.attention, kernel: "lanczos3" })).toFile(out);
} else if (cmd === "ampliar") {
  const k = Number(opt.escala || 2), m = await sharp(pos[0]).metadata();
  info = `ampliar x${k} lanczos3 (interpolacao, sem detalhe novo)`;
  await fino(sharp(pos[0]).resize(m.width * k, m.height * k, { kernel: "lanczos3" })).toFile(out);
} else if (cmd === "compor") {
  if (pos.length < 2) fail("[erro] compor <fundo> <frente>");
  let frente = sharp(pos[1]);
  if (opt["largura-frente"]) frente = frente.resize(Number(opt["largura-frente"]));
  info = `compor ${path.basename(pos[1])} sobre ${path.basename(pos[0])} em ${opt.x || 0},${opt.y || 0}`;
  await sharp(pos[0]).composite([{ input: await frente.toBuffer(), left: Number(opt.x || 0), top: Number(opt.y || 0) }]).toFile(out);
} else fail(`[erro] comando desconhecido: ${cmd}`);

fs.writeFileSync(out.replace(/\.[^.\\/]+$/, "") + ".txt",
  `ferramenta: sharp (ultimo recurso)\nqualidade: INFERIOR a geracao, usuario avisado\noperacao: ${info}\n` +
  `origem: ${pos.join("; ")}\ndata: ${new Date().toISOString().slice(0, 16).replace("T", " ")}\n`, "utf8");
console.log(`[ok] ${out}  (qualidade inferior: avisar o usuario)`);
