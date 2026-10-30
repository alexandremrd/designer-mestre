#!/usr/bin/env node
// Exports each illustrative screen (element with an id) of its own HTML as JPG — "declared illustration" (R3).
//   node render-illustrations.mjs <file.html> <output folder> [id1 id2 …]
// Without ids, exports every element with class="shot". Uses the composition project's playwright (run at its root)
// and the system Chrome (or CHROME=<executable>). Register each file in assets/SOURCES.md as an illustration.
import { createRequire } from "node:module";
import { resolve, join } from "node:path";
const require = createRequire(join(process.cwd(), "package.json"));
const { chromium } = require("playwright");
const [html, outDir, ...ids] = process.argv.slice(2);
if (!html || !outDir) { console.error("usage: render-illustrations.mjs <file.html> <folder> [ids…]"); process.exit(1); }
const b = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : { channel: "chrome" });
const p = await b.newPage({ viewport: { width: 1700, height: 1000 }, deviceScaleFactor: 1 });
await p.goto("file://" + resolve(html), { waitUntil: "networkidle" });
await p.evaluate(() => document.fonts.ready);
const lista = ids.length ? ids : await p.$$eval(".shot[id]", (els) => els.map((e) => e.id));
for (const id of lista) { await (await p.$("#" + id)).screenshot({ path: join(outDir, `${id}.jpg`), quality: 90, type: "jpeg" }); }
console.log(`${lista.length} illustrations → ${outDir}`); await b.close();
