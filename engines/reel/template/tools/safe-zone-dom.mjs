#!/usr/bin/env node
// Safe zone (R7) read from the composition's DOM: walks the whole timeline and lists every TEXT (and every element
// marked data-safe="ui") visible outside the safe area. More precise than the contact sheet: it points at the element.
//   node safe-zone-dom.mjs <project> [--profile reels|ads] [--step 0.25] [--strict] [--caption-bottom 1640]
// Profiles:  reels (default): x 90–990, y 220–1520, nothing in the button column (x > 940 and y > 1150)
//            ads   (Meta ad): x 65–1015, y 270–1248
// Intentional exceptions: data-safe="ignore" (on the element or an ancestor); caption with its own limit:
// data-safe="caption" + --caption-bottom. Uses the project's playwright (npm install) and the system Chrome
// (or CHROME=<executable>).
import { createRequire } from 'node:module';
import { resolve, join } from 'node:path';
import { readFileSync, existsSync } from 'node:fs';

const args = process.argv.slice(2);
const proj = resolve(args.find((a) => !a.startsWith('--') && !/^[\d.]+$/.test(a)) || '.');
const opt = (k, d) => (args.includes(k) ? args[args.indexOf(k) + 1] : d);
const PROFILES = {
  reels: { left: 90, right: 990, top: 220, bottom: 1520, colX: 940, colY: 1150 },
  ads: { left: 65, right: 1015, top: 270, bottom: 1248, colX: 9999, colY: 9999 },
};
const prof = opt('--profile', 'reels');
const S = PROFILES[prof];
if (!S) { console.error(`unknown profile: ${prof}`); process.exit(2); }
const step = +opt('--step', 0.25);
const capBottom = +opt('--caption-bottom', S.bottom);
const require = createRequire(join(proj, 'package.json'));
const { chromium } = require('playwright');
const html = join(proj, 'index.html');
if (!existsSync(html)) { console.error(`no index.html in ${proj}`); process.exit(2); }
const src = readFileSync(html, 'utf8');
if (/data-composition-src=/.test(src)) console.warn('warning: project with sub-compositions — elements inside them are not checked here (use hyperframes preview + snapshot).');

const b = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : { channel: 'chrome' });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
p.on('pageerror', (e) => console.log('page error:', e.message));
await p.goto('file:///' + html.split('\\').join('/'), { waitUntil: 'domcontentloaded' });
let id = null;
for (let i = 0; i < 80 && !id; i++) {
  id = await p.evaluate(() => {
    const root = document.querySelector('[data-composition-id]');
    const k = root && root.getAttribute('data-composition-id');
    return k && window.__timelines && window.__timelines[k] ? k : null;
  });
  if (!id) await p.waitForTimeout(250);
}
if (!id) { console.error('timeline not found (window.__timelines)'); await b.close(); process.exit(2); }
const info = await p.evaluate((id) => {
  const r = document.querySelector(`[data-composition-id="${id}"]`);
  return { w: +r.getAttribute('data-width') || r.offsetWidth, h: +r.getAttribute('data-height') || r.offsetHeight, dur: window.__timelines[id].duration() };
}, id);
if (info.h <= info.w) { console.log(`not vertical (${info.w}×${info.h}) — nothing to check`); await b.close(); process.exit(0); }
const k = info.w / 1080;
const issues = new Map();
for (let t = 0; t <= info.dur; t += step) {
  const found = await p.evaluate(({ id, t, S, k, capBottom }) => {
    window.__timelines[id].seek(t, false);
    const root = document.querySelector(`[data-composition-id="${id}"]`), base = root.getBoundingClientRect();
    // like the renderer: an element with data-start/data-duration only exists inside its time window
    const live = (e) => { if (e === root || !e.hasAttribute('data-start')) return true; const s = parseFloat(e.getAttribute('data-start')), d = parseFloat(e.getAttribute('data-duration')); if (isNaN(s)) return true; return t >= s && (isNaN(d) || t < s + d); };
    const vis = (el) => { let o = 1; for (let e = el; e && e !== root.parentElement; e = e.parentElement) { if (!live(e)) return 0; const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return 0; o *= +cs.opacity; } return o; };
    const ignored = (el) => !!el.closest('[data-safe="ignore"]');
    const out = [];
    const check = (el, r, label) => {
      const bottom = el.closest('[data-safe="caption"]') ? capBottom : S.bottom;
      const x0 = (r.left - base.left) / k, y0 = (r.top - base.top) / k, x1 = (r.right - base.left) / k, y1 = (r.bottom - base.top) / k;
      if (x1 < 0 || y1 < 0 || x0 > 1080 || y0 > 1920) return; // outside the frame = invisible
      const bad = [];
      if (y0 < S.top - 2) bad.push('top');
      if (y1 > bottom + 2) bad.push('bottom');
      if (x0 < S.left - 2) bad.push('left');
      if (x1 > S.right + 2) bad.push('right');
      if (x1 > S.colX && y1 > S.colY) bad.push('app buttons');
      if (bad.length) out.push(`${bad.join('+')} :: ${label.slice(0, 44)} [${Math.round(x0)},${Math.round(y0)},${Math.round(x1)},${Math.round(y1)}]`);
    };
    const rg = document.createRange();
    for (const el of root.querySelectorAll('*')) {
      if (/^(VIDEO|AUDIO|SCRIPT|STYLE|TEMPLATE)$/.test(el.tagName) || ignored(el)) continue;
      const ui = el.getAttribute('data-safe') === 'ui';
      const texts = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim());
      if (!texts.length && !ui) continue;
      if (vis(el) < 0.08) continue;
      if (ui) { const r = el.getBoundingClientRect(); if (r.width > 3 && r.height > 3) check(el, r, '[ui] ' + (el.textContent || el.className || el.tagName).trim()); continue; }
      let L = 1e9, T = 1e9, R = -1e9, B = -1e9;
      for (const n of texts) { rg.selectNodeContents(n); const q = rg.getBoundingClientRect(); if (q.width < 1) continue; L = Math.min(L, q.left); T = Math.min(T, q.top); R = Math.max(R, q.right); B = Math.max(B, q.bottom); }
      if (R > L) check(el, { left: L, top: T, right: R, bottom: B }, el.textContent.trim());
    }
    return out;
  }, { id, t, S, k, capBottom });
  for (const f of found) { if (!issues.has(f)) issues.set(f, []); issues.get(f).push(t.toFixed(2)); }
}
await b.close();
if (!issues.size) { console.log(`safe zone OK — profile ${prof}, ${info.dur.toFixed(1)} s, step ${step} s`); process.exit(0); }
const rows = [...issues].sort((a, b) => +a[1][0] - +b[1][0]);
console.log(`${rows.length} safe zone problem(s) — profile ${prof} (x ${S.left}–${S.right}, y ${S.top}–${S.bottom}):`);
for (const [msg, ts] of rows) console.log(`  ${ts[0]}–${ts[ts.length - 1]} s  ${msg}`);
process.exit(args.includes('--strict') ? 1 : 0);
