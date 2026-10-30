#!/usr/bin/env node
// Static cards of phase 1 (references/delivery.md): one 1080×1920 PNG per screen of the plan, taken from the engine itself
// in the middle of each screen (or at the screen's "t_card", if any), with the real camera, the pieces positioned and the caption.
// Run in the engine folder, after writing ../entrega/plan.json (n, layout, de, ate, fala, tela) and assembling:
//   node tools/cards.mjs            → ../entrega/cards/P01.png… and the "imagem" field of each screen filled in
// The image url carries ?v=<file hash>: a card that did not change keeps its url (and the status the person gave it).
import { readFileSync, writeFileSync, existsSync, mkdirSync, copyFileSync, readdirSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { join } from "node:path";
const PL = join("..", "entrega", "plan.json"), OUT = join("..", "entrega", "cards"), TMP = join("snapshots", "_cards");
if (!existsSync(PL)) { console.error("missing ../entrega/plan.json"); process.exit(1); }
const planta = JSON.parse(readFileSync(PL, "utf8"));
const tempos = planta.map((p) => +(p.t_card ?? (p.de + (p.ate - p.de) / 2)).toFixed(2));
rmSync(TMP, { recursive: true, force: true }); mkdirSync(OUT, { recursive: true });
execFileSync("npx", ["hyperframes", "snapshot", "--at", tempos.join(","), "-o", TMP], { stdio: ["ignore", "ignore", "inherit"] });
const frames = readdirSync(TMP).filter((f) => /^frame-\d+-at-/.test(f)).sort();
planta.forEach((p, i) => {
  const nome = `P${String(p.n ?? i + 1).padStart(2, "0")}.png`;
  copyFileSync(join(TMP, frames[i]), join(OUT, nome));
  const h = createHash("sha1").update(readFileSync(join(OUT, nome))).digest("hex").slice(0, 8);
  p.imagem = `entrega/cards/${nome}?v=${h}`;
});
writeFileSync(PL, JSON.stringify(planta, null, 2));
console.log(`${planta.length} cards in ../entrega/cards/ (times:${tempos.join(", ")})`);
