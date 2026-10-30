// ===== "lean" mode for sound effects (vsl.json "sfxModo": "enxuto"; injected by assemble.mjs after the beats) =====
// The default of this style. The kit puts sound on every piece (the approved reference has ~1.4 effects/s); this filter applies
// rule R2 without touching the kit, counting EVERYTHING (typing too, as verify.py counts):
// 1. keeps the sounds of the big pieces (glitch, boom, stamp, click, switch whoosh, ding) and the typing;
// 2. only keeps a small sound (pop, swoosh, tick, shimmer) when it falls ≥ 0.6 s after the last kept sound;
// 3. cuts small sounds (from the end to the start, every other one, in passes) until ≤ 0.8 effect/s;
// 4. if still over, cuts whoosh/swoosh and ding (never glitch, boom, stamp, click or typing).
(() => {
  const GRANDE = ["glitch", "boom", "stamp", "click", "whoosh", "ding"], FIXO = ["glitch", "boom", "stamp", "click", "type"];
  const ALVO = 0.8;
  const nome = (a) => a.getAttribute("src").replace(/^.*\/|\.wav$/g, "");
  const all = [...document.querySelectorAll('#vsl audio[src^="assets/sfx/"]')]
    .map((a) => ({ a, n: nome(a), t: +a.dataset.start })).sort((x, y) => x.t - y.t);
  let kept = [];
  let last = -9, lastBig = -9;
  for (const s of all) {
    if (s.n === "type") { kept.push(s); continue; }
    if (GRANDE.includes(s.n)) {
      if (s.t - lastBig < 0.25) { s.a.remove(); continue; }
      kept.push(s); last = lastBig = s.t; continue;
    }
    if (s.t - last >= 0.6) { kept.push(s); last = s.t; } else s.a.remove();
  }
  const dur = CFG.dur || 1, dens = () => kept.length / dur;
  const corta = (filtro) => {
    while (dens() > ALVO) {
      const lista = kept.filter(filtro);
      if (!lista.length) return;
      for (let i = lista.length - 1; i >= 0 && dens() > ALVO; i -= 2) { lista[i].a.remove(); kept = kept.filter((k) => k !== lista[i]); }
    }
  };
  corta((s) => !GRANDE.includes(s.n) && s.n !== "type");   // small ones
  corta((s) => !FIXO.includes(s.n));                         // whoosh, swoosh, ding
  console.log(`lean sfx: ${kept.length} effects (${dens().toFixed(2)}/s, typing included)`);
})();
