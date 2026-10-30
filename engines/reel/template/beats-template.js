// ============================================================================================================
// beats.js — the visual script of the reel in style 03 · VSL (engine of the approved reference).
// Only K.* calls with times from K.at("exact phrase from the transcript"). K.at THROWS if the phrase does not exist:
// fix the phrase, never guess seconds. Repeated word: K.at("phrase", n) = nth occurrence;
// more context solves it ("te entregar" instead of "entregar"). Full approved example: example/beats-example.js.
//
// Grammar (speech → camera → piece), in the order it appears in a typical reel:
//   "news/before" hook          FULL raw        K.camcorder(0, t, {label}) → K.glitch(t)
//   thesis sentence / number    FULL + punch    K.punch(t, 1.14–1.2) + K.stack([...]) on the CHEST (top ~1150) + K.hideMouth
//   fact with a source          FULL            K.pill("short text", t, {y: ~1390, icon, sm, up})
//   price / comparison          SPLIT           K.section + K.panel(table with .r1 .r2 … revealed in steps on the word)
//   list of 2–4 things          SPLIT           K.section + K.grid([{img,label,icon,t}])
//   "é só pedir…"               SPLIT           K.panel(chat) + K.prompt("request", t, {cps, send})
//   "ele faz…"                  SPLIT           K.progress(label, t, d) → K.fan([imgs], t)
//   finished result             FULL            K.stamp("PRONTOS ✓", t, {x, y}) ON THE CHEST + K.panel(export) y ≥ 1170
//   turn "mas não para…"        FULL + punch    K.stack on the chest
//   old way × new way           FULL            K.pill(name, t, {kind:"strike"}) → K.flash → K.stack
//   CTA                         FULL            K.cta("Comenta PALAVRA", t, {y:1300, clickAt}) + kicker ON THE CHEST
//   (end)                                       K.mouthCaps({accent:[keywords]}) — ALWAYS last
//
// Rules that keep the result at the reference's level:
// - every FULL↔SPLIT switch with K.layout (animated, 0.45 s) and K.hideMouth(t − 0.05, t + 0.5) at the same instant;
// - nothing over the face (R1): lettering, pills, stamp and kicker on the chest (y ≥ ~1150 in FULL); top only in SPLIT;
// - something new every 1.5–3 s; FULL ~50 % / SPLIT ~50 % (no PIP in the reference);
// - every number and every fact on screen with a source in assets/SOURCES.md; product screen without a screenshot = declared illustration.
// ============================================================================================================
const A = (p, n = 1, after = 0) => K.at(p, n, after);
const IMG = (f) => `assets/img/${f}`;
const SPLIT_TOP = 240;  // top of the content in SPLIT (safe zone starts at 220)
const CHEST = 1250;     // chest line for pills in full screen

// --- neutral starting point (works with any transcript; replace with the video's map) -------------------
const w = WORDS, t2 = w.length > 3 ? w[3].start : 1;
K.camcorder(0, t2 - 0.05, { label: "NOVIDADE" });
K.glitch(t2 - 0.05);
K.punch(t2 + 0.05, 1.14);

// --- 1) HOOK -----------------------------------------------------------------------------------------------
// const tG = A("first words of the thesis") - 0.05;
// K.camcorder(0, tG, { label: "NOVIDADE · PRODUTO" });
// K.glitch(tG);
// K.punch(tG + 0.1, 1.14);
// K.stack([{ text: "word 1", t: A("word 1") + 0.05, style: "blur" }, { text: "word 2", t: A("word 2"), style: "glow" }],
//         { top: 1180, until: A("next phrase") - 0.05 });
// K.hideMouth(tG, A("next phrase"));

// --- 2) SPLIT with panel revealed on the word -------------------------------------------------------------
// const t4 = A("panel phrase") - 0.08;
// K.layout("split", t4);
// K.hideMouth(t4 - 0.05, t4 + 0.5);
// K.section({ kicker: "Short kicker", title: "Title of 3–5 words", acc: [3, 4] }, t4 + 0.1, { y: SPLIT_TOP, until: A("following phrase") - 0.15 });
// K.panel(`<div class="r1">…</div><div class="r2">…</div>`, A("word of the 1st item") - 0.1, {
//   box: { x: 90, y: 390, w: 900, h: 560 },
//   steps: [{ sel: ".r1", t: A("word of the 1st item") }, { sel: ".r2", t: A("word of the 2nd item"), sfx: "ding" }],
//   until: A("following phrase") - 0.15 });

// --- 3) back to FULL --------------------------------------------------------------------------------------
// K.leak(A("return phrase") - 0.15, 0.55);
// K.layout("full", A("return phrase") - 0.1);
// K.pill("Short text with source", A("word"), { y: CHEST + 60, icon: "chat", up: true, until: A("next") - 0.05 });

// --- 4) CTA -----------------------------------------------------------------------------------------------
// K.punch(A("comenta") - 0.02, 1.06);
// K.cta("Comenta PALAVRA", A("comenta"), { y: 1300, w: 820, clickAt: 1.1 });

// caption that follows the mouth — ALWAYS last (reads the framing of each frame)
K.mouthCaps({ accent: [] });
