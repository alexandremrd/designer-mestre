# Rough Cut

**Module 1 of the editing pipeline**
*Version 1.1 · 27/10/2026 · Status: approved in production · Skill: `~/.claude/skills/reel` (`cut/` folder)*

> This document is **self-sufficient**. Whoever reads it (person or agent) must be able to cut a raw video
> with the same quality as the approved v2 without having seen the conversation that originated it. It is the full reference of the
> `reel` skill, `cut/` folder (`CUT.md` is the short script; this document is the why). That is why it explains not only **what
> to do**, but also **why** each rule exists and **how to decide** when the rule does not cover the case.
>
> **Official source:** this file inside the skill. Adjustments are made here and recorded in section 16.

---

## Contents

0. [Where this module fits in the process](#0--where-this-module-fits-in-the-process)
1. [Glossary](#1--glossary)
2. [Principles](#2--principles-what-makes-the-result-good)
3. [Prerequisites and installation](#3--prerequisites)
4. [The flow, step by step](#4--the-flow-step-by-step)
5. [How to choose takes: the editorial reasoning](#5--how-to-choose-takes-the-editorial-reasoning)
6. [The cut engine from the inside](#6--the-cut-engine-from-the-inside)
7. [Check and acceptance criteria](#7--check-and-acceptance-criteria)
8. [Output contract: what the module delivers to the styles](#8--output-contract-what-the-module-delivers-to-the-styles)
9. [Diagnosis: symptom → cause → adjustment](#9--diagnosis-symptom--cause--adjustment)
10. [Whisper traps](#10--whisper-traps)
11. [Annotated example: the v2 breakdown](#11--annotated-example-the-v2-breakdown)
12. [History: what went wrong in v1 and became a rule](#12--history-what-went-wrong-in-v1-and-became-a-rule)
13. [Instructions for the agent](#13--instructions-for-the-agent-future-skill)
14. [From the package that did not make it in (optional)](#14--from-the-package-that-did-not-make-it-in-optional)
15. [Files and origin](#15--files-and-origin)
16. [Known limits and next steps](#16--known-limits-and-next-steps)

---

## 0 · Where this module fits in the process

```
 RAW (recording with mistakes, restarts, pauses)
   │
   ▼
 ┌──────────────────────────────────────────┐
 │ MODULE 1 · ROUGH CUT (this document)     │  → clean speech + time map
 └──────────────────────────────────────────┘
   │   clean.mp4 · cut.wav · edl.json · cut_words.json
   ▼
 ┌──────────────────────────────────────────┐
 │ MODULE 2 · EDITING STYLE 1 / 2 / 3        │  → framing, captions, images, zoom, effects, soundtrack
 │ (the person chooses the style)           │
 └──────────────────────────────────────────┘
   │
   ▼
 FINAL VIDEO
```

**Responsibility of this module:** decide **which speech stays** and **exactly where** each stretch starts and
ends. Nothing else.

**Outside this module:** format (9:16, 16:9), camera crop, drawn captions, images, zoom, soundtrack,
sound effects and color correction. That is the styles' responsibility.

**Boundary rule:** after this module, **no style goes back to the raw to choose speech**. If a style
needs another cut, it asks for a new round of this module and remaps its times (section 4, step 5).

---

## 1 · Glossary

| Term | Meaning |
|---|---|
| **Raw** | The original recording, uncut. It is the source of all "source" times. |
| **Take** | Each time a phrase was said. A phrase may have 1 to 4 takes in the raw. |
| **Restart** | A take repeated because the previous one did not come out good. |
| **False start** | A take that starts and is abandoned, sometimes on a single word ("Então..."). |
| **Abandoned phrase** | A take that starts well and stops midway ("É só você pedir..."). |
| **Filler (speech)** | Hesitation without content: "éé", "ããã", "hum", "eh", or a stretched conjunction ("eeee"). |
| **Keep** | A stretch of the raw chosen to stay (`from`/`to` in source seconds). It is the editorial decision. |
| **Segment** | Continuous piece of audio the engine keeps. A keep becomes 1 or more segments, because the internal pauses also go out. |
| **Splice** | The point where two segments meet in the final cut. |
| **Valley (of energy)** | The quietest instant near a cut point. Cutting in the valley does not cut a word. |
| **Tilt (spectral tilt)** | How much the low-frequency energy (80–900 Hz) exceeds the high (2–7 kHz), in dB. Voice has high tilt; breath and "sss" have low or negative tilt. |
| **Speech p90** | The volume below which 90 % of the frames with sound fall. It measures the voice's "recording level". |
| **LEAD / TAIL** | The margin kept before the first sound (0.06 s) and after the last (0.14 s) of each segment. |
| **HOLE** | The maximum size of silence that **stays** inside a phrase (0.20 s). Larger silence goes out. |
| **ISLAND** | The minimum size of a sound to count as speech (0.07 s). Smaller clicks are discarded. |
| **J / L cut** | In the J cut, the sound of the next phrase enters before the image: the old image continues a few frames. In the L cut, the image of the next phrase arrives before the sound. It makes the splice less dry. |
| **EDL** | *Edit decision list*: the list of segments with the time in the source and in the cut (`edl.json`). |
| **Source time / cut time** | Seconds counted in the raw vs. seconds counted in the cut video. **Never mix the two.** |

---

## 2 · Principles (what makes the result good)

1. **Who decides what stays is you, by reading; who decides where to cut is the sound.**
   The choice of takes is editorial, made by reading the real text of each stretch. The exact cut point is measured
   on the audio (volume, timbre and valley). Whisper's word time is **never** a cut point: it arrives
   shifted by tenths of a second and, in long silence, arrives invented.

2. **One phrase, one take: the best complete one.**
   Every restart, false start, abandoned phrase, "alô, alô", cough and test goes out. Among the complete takes,
   the default is the most recent, except when it is longer or has a crutch and another is equally complete and
   leaner (section 5).

3. **A one-word false start is also a restart.**
   It was v1's mistake: an aborted "Então..." stayed glued to the following "Então, ao invés de...". The keep starts
   **on the word that counts**.

4. **The long transcription hides repetitions. The check transcribes each splice on its own.**
   Whisper read "Então... Então, ao invés de" as a single "Então". That is why the check treats the splices
   one by one and looks for repetitions automatically.

5. **Breath is not speech. A good pause is up to 0.2 s.**
   The detector uses volume **and** timbre. With a volume-only threshold, breath passes as speech and the pause stays
   long (another v1 mistake).

6. **Right information above a whole take.**
   You may assemble a speech from pieces of different takes, as long as each piece starts and ends at a phrase
   end. When different takes say different things, choose the one that conveys the right information and, if
   in doubt, ask whoever recorded.

7. **The cut must not sound cut.**
   8/12 ms fade on each segment (no click), edge in the valley, LEAD/TAIL so as not to clip a syllable, and J/L on the
   splices.

8. **Nothing is delivered without the step 4 check read in full.**

---

## 3 · Prerequisites

Validated on a Mac M5 (macOS) with:

| Tool | Where | For what |
|---|---|---|
| `ffmpeg` 8.x | `/opt/homebrew/bin/ffmpeg` | extract audio, cut, encode |
| `whisper-cli` (whisper.cpp) | `/opt/homebrew/bin/whisper-cli` | local transcription, runs on the GPU (Metal) |
| Model `large-v3-turbo` | `~/.cache/whisper-cpp/ggml-large-v3-turbo.bin` (1.6 GB) | best balance between accuracy and speed in PT-BR |
| Python with numpy | `/usr/bin/python3` (3.9, numpy 2.0) | audio analysis and the engine |

To switch the model, set `WHISPER_MODEL=/path/to/template.bin` before running.

**On another machine, first run `python3 scripts/0-check.py`.** It checks ffmpeg, whisper-cli, numpy and the
model, and says how to install whatever is missing:

- **Mac:** `brew install ffmpeg whisper-cpp` · `pip3 install numpy`.
- **Windows:** `winget install Gyan.FFmpeg`; whisper.cpp comes from the `whisper-bin-x64` zip of the releases of
  github.com/ggml-org/whisper.cpp (put the folder in the PATH); `python -m pip install numpy`. Run the scripts with
  `PYTHONUTF8=1` and `python` in place of `python3`.
- **Model:** `ggml-large-v3-turbo.bin` (1.6 GB), from huggingface.co/ggerganov/whisper.cpp, in
  `~/.cache/whisper-cpp/`. Another model works (`medium`, `large-v3`): the time alignment is chosen
  by the file name. On a slow PC, `medium` is acceptable for step 1; splice accuracy drops a little.
- **Without a Mac**, the `clean.mp4` encoder is `libx264` (slower, same quality).

---

## 4 · The flow, step by step

All commands run in the scripts folder. `PASTA` is a working folder, **one per video**
(e.g.: `cortes/2026-11-03-reel-x`, next to the raw). The script creates the folder if it does not exist.

```bash
cd ~/.claude/skills/reel/cut/scripts
python3 0-check.py            # only the first time on each machine
```

### Step 1 · Take map

```bash
python3 1-takes.py "/path/to/raw.mp4" PASTA
```

**What it does.** The script extracts the audio at 16 kHz mono (`audio16k.wav`) and measures the volume every 10 ms. It marks
as "sound" everything above the room's noise floor + 18 dB (the floor is the volume below which 10 % of the
frames fall) and merges holes smaller than 0.15 s. Then it transcribes **each stretch on its own**, with 0.15 s of margin
on each side.

**Outputs.** `takes.txt`, to read, and `takes.json` (`[{from, to, texto}]`).

**Why not transcribe the whole video at once.** In a raw with restarts there are long silences, and in those
silences Whisper **invents speech**, usually repeating the previous phrase. The times also come out wrong. In the
v2 raw it produced 8 s of text in a stretch with no sound at all. Transcribing stretch by stretch eliminates that and
shows each restart separately.

**How to read.** Each line is `start-end (duration) :: text`. Restarts show up as similar lines in
sequence. False starts show up as short lines ending in "...". Real example:

```
 141.33- 141.94 ( 0.6s) :: Então...                                   ← false start: stays OUT
 142.77- 147.11 ( 4.3s) :: Então, ao invés de você pagar pelo Gama...  ← the take that counts
```

### Step 2 · Choose the keeps

It is the only judgment step. The full rules are in section 5. Write `PASTA/keeps.json`:

```json
{"keeps": [
  {"from": 5.80,   "to": 12.15,  "why": "gancho (tomada única)"},
  {"from": 142.80, "to": 149.50, "why": "Gamma/Canva + CTA (pula a falsa largada 'Então...' de 141,3)"}
]}
```

| Field | Required | Meaning |
|---|---|---|
| `from`, `to` | yes | **source** seconds, with 0.1 to 0.2 s of margin around the text. The engine snaps to the valley. |
| `why` | recommended | which take it is and what was skipped. Goes into the report. |
| `raw` | no | `true` = keeps the segment exactly as it is, without the detector (see section 5.4). |

The order of the keeps in the file is the order in the final video. It normally follows the source order, but it does not have to.

Then run the transcription that shows the fillers, only inside the keeps:

```bash
python3 2-fillers.py PASTA
```

The script transcribes each keep word by word, with a prompt full of "éé, ããã, hum, né", and writes
`vicios/k{i}.json` (source times). With that prompt Whisper **writes** the hesitations instead of erasing them,
and the engine manages to remove them. Read the output: an "éé" in the middle of a good phrase shows up here.

### Step 3 · The cut engine

```bash
python3 3-cut.py "/path/to/raw.mp4" PASTA
# options: --jl 4 (default; 0 turns off, 6 is smoother) · --sem-video (audio + edl only, faster)
```

The inner workings are in section 6. **Outputs:** `edl.json`, `cut.wav`, `cut16k.wav`,
`removed-fillers.txt` and `clean.mp4`. On screen appear the measured speech level, the thresholds used, how many
fillers went out, how many segments remained, in how many splices J/L entered and the final duration.

Fine adjustments without touching code, in `PASTA/adjustments.json` (**source** times):

```json
{"cut": [[143.10, 143.40]], "keep": [88.5], "force": [[60.2, 60.4]]}
```

- `cut`: forces a segment out (a "né" Whisper did not write, a mouth click).
- `keep`: protects a detected filler that must stay (a hesitation that is part of the joke).
- `force`: keeps a sound that is not voice and the detector would discard (finger snap, clap).

### Step 4 · Check

```bash
python3 4-review.py PASTA --prompt "Claude, Slides, Docs, Design, PowerPoint, Gamma, Canva"
# --prompt: proper names of THIS video (the default is generic: Claude, Claude Code, IA, ChatGPT, Instagram, YouTube)
```

The acceptance criteria are in section 7. The output goes into `review.txt` and `cut_words.json`. If
something fails, adjust `keeps.json`/`adjustments.json`, go back to step 3 and check again.

### Step 5 (only if the edit already existed) · Remap

If captions, cards, zooms or effects were already timed on a previous cut and the cut changed, **do not
retime by hand**:

```python
import os, sys; sys.path.insert(0, os.path.expanduser("~/.claude/skills/reel/cut/scripts"))
from remap import Mapa
m = Mapa("corte-antigo/cut_words.json", "corte-novo/cut_words.json")
m.novo(2.73)    # old time → new  (2.62 in v2)
m.velho(2.62)   # new time → old  (use this one to render frame by frame in the new time)
```

The script aligns the words in common between the two cuts and interpolates between them. An element timed on
word X stays on word X. That is how v2 kept the whole visual edit of v1.

---

## 5 · How to choose takes: the editorial reasoning

### 5.1 · For each phrase of the script

1. List in `takes.txt` all the takes of that phrase.
2. Discard the **incomplete** ones: those ending in "...", stopping midway or losing a piece of the idea.
3. Discard the ones with an **audible stumble**: swapped word ("você pode para ele escrever"), stutter,
   repeated word.
4. Among those left, the **default is the most recent**: in general whoever records repeats until it comes out good.
5. **Exception:** if the most recent is longer, has a crutch ("a partir daí, então", "por exemplo" left over)
   or sounds more dragged, and another is equally complete and leaner, stay with the lean one. Reels reward
   density.
6. **If different takes say different things** (whoever recorded changed the content from one take to another),
   choose by the **correct information**. If it is impossible to know which is correct, **ask** whoever recorded.

### 5.2 · Joining pieces of different takes

Allowed when:
- each piece starts and ends at a **phrase or clause end** (never in the middle of a word or of a
  syntagm);
- the intonation of the end of the first piece matches the start of the second (a phrase that ends falling
  followed by one that starts fresh);
- the result is more correct or leaner than any whole take.

Example from v2: "...escreva um documento de uma página." (take at 86 s) + "Ele pode até criar carrosséis no
Instagram pra acompanhar esse material." (take at 121 s). That way each tool got the right example.

### 5.3 · Keep edges

- Give **0.1 to 0.2 s of margin** before the first and after the last word. The engine looks for the valley outward from
  the text, so too much margin does no harm.
- The margin **cannot reach the neighboring take**. If two takes are less than 1 s apart (the case of the
  "Então..." 0.9 s from the good "Então"), the `from` goes **flush** against the start of the good take.
- The time that shows in `takes.txt` is the start of the stretch with margin. To find the exact start of the word,
  see `vicios/k{i}.json` (word time) and, in doubt, the volume in `audio16k.wav`.

### 5.4 · Weak word at the start

Whisper's word start time tends to come **late**, and a breathy word ("Se", a weak "E")
may fall below the detector's threshold. If the check shows the first syllable clipped:
1. advance that keep's `from` by 0.1 to 0.2 s; or
2. mark the keep with `"raw": true` (enters exactly as it is, without the detector); or
3. use `force` in `adjustments.json` only for that piece.

### 5.5 · What always goes out

"Alô, alô", sound tests, cough, throat clearing, "deixa eu refazer", off-script comments, laughter that is not
part of the content, false starts and abandoned phrases.

---

## 6 · The cut engine from the inside

This section explains each decision of `3-cut.py`, so that it can be adjusted safely.

### 6.1 · Sound analysis

- The audio is read at 16 kHz mono and split into **10 ms frames** (`HOP 160`), each analyzed in a
  **30 ms window** (`WIN 480`) with Hann.
- Per frame, the engine computes:
  - **volume** in dB (RMS);
  - **tilt** = energy of 80–900 Hz ÷ energy of 2–7 kHz, in dB.

### 6.2 · What is speech

```
speech = (volume > T1  AND  tilt > 12 dB)   OR   (volume > T2  AND  tilt > 0 dB)
```

- The first condition catches **normal voice**: moderate volume and low-frequency dominance.
- The second catches **strong consonants** ("s", "x", "ch"): higher-pitched, but loud.
- **Breath** is high-pitched and quiet, so it fails both and goes out. Room noise is quiet, so it also goes out.

**Calibration by recording level.** The original package uses fixed T1 = −33 dB and T2 = −26 dB, which only
works if the voice is recorded at a certain level. Here the engine measures the **speech p90** and shifts both
thresholds so that this p90 equals −20 dB:

```
REF_DB = −20 ;  OFF = p90 − REF_DB ;  T1 = −33 + OFF ;  T2 = −26 + OFF
```

`REF_DB` is the constant at the top of `3-cut.py`. **The lower the `REF_DB`, the higher the thresholds**, and the more the
engine cuts (−22 cuts more than −20; −18 cuts less).

In v2, p90 = −24.5 dB, OFF = −4.5, T1 = −37.5 dB and T2 = −30.5 dB.
*The −20 dB reference is our choice (the package does not declare the expected level) and was validated on this
video. If a very different recording gives trouble, this is the first number to revise (section 9).*

### 6.3 · Fillers

Read from `vicios/k*.json`:
- **Pure hesitation** ("aa", "ee", "eh", "ah", "hum", "hm", "uh", "umm", "mm", or any word made of a
  single repeated letter): the whole interval becomes silence.
- **Stretched conjunction** ("e", "a", "um", "o" with duration between 0.45 and 1.6 s): the first 0.14 s stay and the
  rest of the "eeee" goes out.
- Above 1.6 s, the engine does not cut on its own: it is a restart or a long pause, and the decision is editorial (keep or
  `ajustes.cut`).
- Everything that went out is listed in `removed-fillers.txt`.

### 6.4 · From frames to segments

| Rule | Value | Why |
|---|---|---|
| Holes smaller than `HOLE` inside speech **stay** | 0.20 s | it is the natural breathing room between words; removing it makes speech robotic |
| A hole created by removing a filler is **not** closed | — | otherwise the filler would come back |
| Islands of "speech" smaller than `ISLAND` go out | 0.07 s | mouth clicks, mouse click |
| `LEAD` before the first speech frame | 0.06 s | protects the word's attack |
| `TAIL` after the last speech frame | 0.14 s | protects the "s" and final vowels, which decay slowly |
| Keep edges → energy valley | start: 0.15 s backward and 0.03 s forward · end: 0.03 s backward and 0.15 s forward | the cut falls in the silence, searching outward from the text |
| Segments less than 0.08 s apart merge | 0.08 s | avoids micro-cuts |
| Start and end rounded to the 30 fps frame | 1/30 s | image and sound cut on the same frame |
| Segments shorter than 2 frames go out | 0.067 s | leftovers without content |

### 6.5 · Audio

- Read at **48 kHz stereo** from the raw (full quality, not the 16 kHz of the analysis).
- **8 ms fade-in and 12 ms fade-out** on each segment: eliminates the splice click without being audible
  as a fade.
- The engine does **not** apply compression, equalization or normalization. That is left to the style (v2 used
  a 70 Hz high-pass, 3:1 compressor and loudnorm −14 LUFS).

### 6.6 · J/L cuts

- They only enter on **real splices**, where at least 0.25 s went out between one segment and the other.
- They alternate: J, L, J, L... The offset is `--jl` frames (default 4 = 0.133 s).
- **J** (positive `vshift`): the image of the previous segment continues 4 frames after the sound of the next
  has started.
- **L** (negative `vshift`): the image of the next segment appears 4 frames before its sound.
- Effect: the splice sounds and looks natural, as in a real conversation, instead of "jumping" dry.
- To turn off: `--jl 0`. To make it more noticeable and smooth: `--jl 6`.

### 6.7 · Video

- `clean.mp4` comes out in the **raw's original framing** (no crop; the crop belongs to the style), at 30 fps,
  with a keyframe every 1 s (`-g 30`). Without frequent keyframes, renderers that jump in time freeze
  frames.
- Encoder: `h264_videotoolbox` at 16 Mb/s (fast on the Mac); if it fails, `libx264 -crf 18`.

---

## 7 · Check and acceptance criteria

`4-review.py` generates four blocks. To **accept** the cut, all must pass:

| Block | What it is | Acceptance criterion |
|---|---|---|
| **Cut text** | whole transcription, word by word | Read from start to finish. Every phrase of the script present only once, no clipped word, no missing verb. Whisper **name** errors ("Cláudio") do not fail: they are fixed in the caption. |
| **Adjacent repetitions** | the same word or expression (1 to 4 words) twice in a row | "nenhuma". An intentional repetition ("muito, muito fácil") may stay, as long as it is recorded in the report. |
| **Splices** | each cut point transcribed on its own in a ±2 s window, **without a prompt** | All legible and coherent: no half word, no mumbled restart, no duplicated word. |
| **Pauses** | silences above 0.25 s (below −38 dB) | "nenhuma". |

**Attention to the windows.** A splice's window sometimes shows the text starting midway (Whisper swallows the
start of short clips). That is **not** a defect of the cut. Confirm in the neighboring window or in the whole text.
A word that vanishes in **all** places is a defect.

**Final listening test.** The automatic check does not replace watching `clean.mp4` once. Mouth
sync and the naturalness of the splices are only validated by watching.

Result of v2: no repetition, no pause, 12 legible splices, 38.77 s.

---

## 8 · Output contract: what the module delivers to the styles

Everything stays inside `PASTA/`. **Every style consumes only these files.**

| File | Format | Time | Use in the style |
|---|---|---|---|
| `clean.mp4` | H.264 30 fps, original framing, with the cut's audio and J/L applied | cut | ready visual base, for styles that only overlay elements |
| `cut.wav` | 48 kHz stereo, untreated | cut | voice track: the style applies EQ, compression and loudness |
| `cut16k.wav` | 16 kHz mono | cut | transcription and analysis |
| `edl.json` | list of segments (below) | source ↔ cut | for whoever needs to go back to the raw at full resolution (e.g.: crop 9:16 from the original 2560×1440 without loss) |
| `cut_words.json` | `[[start, end, "word"], ...]` | cut | captions and syncing elements with words |
| `keeps.json`, `takes.txt`, `review.txt`, `removed-fillers.txt` | text/JSON | source | audit and report |

**Format of `edl.json`:**

```json
[
 {"src": 6.0,   "dur": 6.1333, "out": 0.0,  "nf": 184, "vshift": 0.0},
 {"src": 12.37, "dur": 1.2,    "out": 6.1333, "nf": 36, "vshift": 0.0},
 {"src": 13.87, "dur": 3.5667, "out": 7.3333, "nf": 107, "vshift": 0.1333}
]
```

| Field | Meaning |
|---|---|
| `src` | start of the segment **in the raw** (s) |
| `dur` | duration of the segment (s), exact multiple of 1/30 |
| `out` | start of the segment **in the cut** (s) |
| `nf` | duration in 30 fps frames |
| `vshift` | offset of the **image** cut between the previous segment and this one (+ = J, − = L, 0 = straight cut) |

**How a style computes, for an instant `T` of the cut, which raw frame to show and which audio to play:**

```
audio:  segment i with out_i ≤ T < out_i + dur_i     →  source = src_i + (T − out_i)
image:  VSTART_0 = 0 ;  VSTART_j = out_j + vshift_j
        segment j with VSTART_j ≤ T < VSTART_{j+1}  →  source = src_j + (T − out_j)
```

(This is exactly how v2's renderer read the 2560×1440 raw to crop the 9:16.)

**Captions:** `cut_words.json` comes from Whisper as it is. The style applies the name corrections
(section 10) and decides how to group and display the words.

---

## 9 · Diagnosis: symptom → cause → adjustment

| Symptom in the check / by ear | Probable cause | Adjustment |
|---|---|---|
| Doubled phrase or "então então" | keep caught a false start or two takes | move `from`/`to`; split into two keeps |
| First syllable clipped | breathy word below the threshold, or late `from` | advance `from` 0.1–0.2 s; `"raw": true`; `force` |
| End of word cut ("slide" instead of "slides") | TAIL short for this voice, or keep `to` short | extend `to`; raise `TAIL` to 0.18 |
| Audible breath between phrases | thresholds too low for this recording | check the printed p90; `REF_DB` from −20 to −22 (thresholds rise 2 dB) |
| Whole words vanishing in quiet stretches | thresholds too high (low voice, distant microphone) | `REF_DB` from −20 to −18 (thresholds drop 2 dB); `force` on the stretch |
| Speech sounding "machine-gun", no breathing room | small `HOLE` | raise `HOLE` to 0.25 |
| Pauses still noticeable | large `HOLE`, or silence with loud noise (air conditioning) | lower `HOLE` to 0.15; check the noise does not pass as speech |
| "éé" that stayed | Whisper did not write the filler | `ajustes.cut` with the interval |
| Hesitation that should stay was cut | filler detected in an intentional context | `ajustes.keep` with its start |
| Click at the splice | cut outside the valley | check the keep edge is not inside a word; larger margin |
| Splice looking like an image "jump" | J/L off or small | `--jl 4` or `--jl 6` |
| Mouth out of sync near the splice | J/L too large for that stretch | `--jl 2` or `--jl 0` |

The parameters `HOLE`, `ISLAND`, `LEAD`, `TAIL` and `REF_DB` are at the top of `3-cut.py`.
**Change one at a time** and record the change in section 16.

---

## 10 · Whisper traps

All of them happened in this video.

| Trap | How it shows up | What to do |
|---|---|---|
| **Invents speech in long silence** | repeats the previous phrase inside an 8 s silence | map takes by energy and transcribe stretch by stretch (step 1) |
| **Wrong word times** | several words with the same time; "stretched" sequences | never cut by word time; cut by sound (step 3) |
| **Hides repetition** | "Então... Então, ao invés" becomes a single "Então" | splices on their own + repetition hunt (step 4) |
| **Swallows the start of a short clip** | the splice window starts midway through the phrase | ±2 s window; confirm in the neighboring window or in the whole text |
| **Filler prompt on a short window invents fillers** | "é, ah, hum, é..." appears where there is nothing | filler prompt only on the keeps (step 2); splices **without** a prompt |
| **Skips a phrase in the long transcription** | "Ele pode até criar" vanished from the final file's transcription | transcribe only that window before concluding. The phrase was in the audio |
| **Gets names wrong** | see table below | fix in the caption; `--prompt` with proper names helps |

**Name corrections already seen (apply in the caption):**

| Whisper writes | Correct |
|---|---|
| Cláudio, Cloud, Claudio | **Claude** |
| de A (in "ferramentas de A") | **de IA** |
| Gama, ganho | **Gamma** |
| Câmbio, Can | **Canva** |
| te vi um link / tive um link | **te envio um link** |
| Designs, designing | **Design** |

---

## 11 · Annotated example: the v2 breakdown

**Raw:** example recording of 2 min 33, HEVC 2560×1440, 23.976 fps, the presenter
talking to the camera, several takes per phrase.
**Result:** 38.77 s, 13 segments, 6 splices with J/L, no filler, no pause above 0.21 s.
Files in `example/`.

### Phrase-by-phrase decision

| # | Phrase | Takes in the raw (s) | Chosen | Why |
|---|---|---|---|---|
| — | "Alô, alô" | 0.95 | **out** | sound test |
| 1 | Hook: "O Claude acabou de lançar três ferramentas de IA totalmente gratuitas…" | 5.81 | 5.80–12.15 | single, complete take |
| 2 | "Elas se chamam Slides, Docs e Design e ficam dentro do chat…" | 12.28 (with internal pause at 13.7) | 12.30–17.45 | single take; the 0.3 s internal pause goes out by itself in the engine |
| 3 | "E pra utilizar é muito fácil… apresentação comercial… ele prepara todos os slides" | 17.65 (abandoned) · 19.95 (abandoned) · 24.12 (ends in "e a...") · 30.84 (only the start) · 34.43 (abandoned) · **38.59–46.28** · 65.97–74.75 | 38.60–46.25 | The one at 38.6 s is complete and lean. The one at 66 s (more recent) is also complete, but longer and with a crutch ("pedir para ele aquilo que…", "A partir daí, então, ele vai preparar"). **Exception to rule 5.1.5.** |
| 4 | "Depois… você pode exportar… PowerPoint ou Google Slides" | 46.20 ("ou, por exemplo, Google Slides e...") · **78.88–84.48** | 78.90–84.45 | the one at 46 s has a leftover "por exemplo" and ends hanging on "e..."; the one at 79 s is the most recent and clean |
| 5 | "Mas essa novidade não para só nos slides. Na mesma conversa… um documento de uma página." | **86.16–92.17** · 94.14 (ends in "documento") · 108.85 (stumble: "pode para ele escrever") · 114.97 (complete, long: "página inteira para você utilizar no seu site"; "não para nos slides", without "só") · 131.15 (the last; changes the content to "roteiro → carrosséis") | 86.10–92.15 | complete and lean, with "documento de uma página", which is the right example for **Docs** |
| 6 | "Ele pode até criar carrosséis no Instagram pra acompanhar esse material." | **121.78–125.42** (tail of the 115 s take) | 121.80–125.35 | gives **Design** its example; **joining takes (5.2)**: starts at a phrase end and fits after "documento de uma página." |
| — | "Com base nesse material." | 140.00 | **out** | tail of the 131 s take, which was discarded |
| — | "Então..." | 141.33 | **out** | **one-word false start** (the v1 mistake) |
| 7 | "Então, ao invés de você pagar pelo Gamma ou pelo Canva… Comenta SLIDES e eu te envio um link…" | **142.77–149.53** | 142.80–149.50 | `from` flush against the start of the good take, so as not to reach the "Então..." 0.9 s earlier |

### What the engine did

```
speech level (p90) -24.5 dB → thresholds -37.5 / -30.5 dB
fillers removed: 0
13 segments · J/L on 6 splices · duration 38.77s
```

The 7 keeps became 13 segments, because internal pauses longer than 0.2 s went out. Examples: 12.37–13.57 and
13.87–17.43 (the pause between "Slides" and "Docs" went out); 38.67–43.87 and 44.00–46.20.

---

## 12 · History: what went wrong in v1 and became a rule

v1 was made without this method: cut by simple volume and check only by the long transcription.

| Mistake in v1 | Cause | Rule created |
|---|---|---|
| "Então" repeated before "Então, ao invés de…" | the keep started at 141.35 s and caught the false start; the long transcription merged the two "Então" | principle 3; section 5.3 (flush edge when takes are close); splices checked on their own |
| Pauses with breath between phrases | speech detected only by volume, with a low threshold (−52 dB), so breath counted as speech | principle 5; detector with volume + tilt and calibration by p90 |
| Edges with leftover breath | fixed margin after the last sound | edges in the valley; LEAD/TAIL of 0.06/0.14 s |
| Duration: 40.3 s | — | v2: 38.8 s with the same content |

---

## 13 · Instructions for the agent

(`SKILL.md` summarizes this. Here is the full version.) When asked to cut, break down, clean or
"remove the mistakes" from a recording:

1. **Confirm the raw** (path) and create the working `PASTA` next to it or in the project folder. Run
   `ffprobe` and note duration, resolution and fps.
2. **Before each slow step**, warn in one short line, in the user's language ("Transcribing the takes, it takes a few
   minutes."), so the wait does not look like a hang. Run the long steps in the background.
3. **Step 1**, then **read `takes.txt` in full**. Never choose keeps without having read all the takes.
4. **Step 2 (keeps):** follow section 5. **Ask** whoever recorded only when different takes say different
   things and it is impossible to know which is correct. In other cases, decide and record it in the `why`.
5. **Steps 2b, 3 and 4.** Read `review.txt` in full. If any criterion of section 7 fails, fix and repeat.
   Do not deliver with a failing criterion.
6. **Deliver** with this report (short, written in the user's language):

   ```
   Cut ready: <path of clean.mp4>  ·  <raw duration> → <cut duration>
   Takes used: <list with source and the "why">
   Left out: <false starts, abandoned sentences, tests, coughs...>
   Fillers removed: <n> (list in removed-fillers.txt)
   Review: repetitions <ok>, joins <ok>, pauses <ok>
   Uncertainties: <what can only be validated by listening, or content decisions taken>
   ```

7. **Do not do** in this module: 9:16 crop, drawn captions, images, soundtrack, volume normalization.
   That belongs to the style.
8. **Never** delete the raw nor write inside the raw's folder without a request. The working `PASTA` is
   disposable and can be redone.

---

## 14 · Optionals (only if asked)

Use only if asked:

- **Voice at 1.05x**: slightly speeds up the rhythm, preserving the pitch.
  `ffmpeg -i clean.mp4 -filter_complex "[0:v]setpts=PTS/1.05[v];[0:a]atempo=1.05[a]" -map "[v]" -map "[a]" -c:v libx264 -preset veryfast -crf 20 -r 30 -c:a aac -b:a 192k clean-105.mp4`.
  If used, redo `cut_words.json` over the sped-up file.
- **90 s ceiling per reel**: if the cut goes over, tell whoever recorded what can be dropped.
- **Automatic encoder** (NVIDIA / Quick Sync / AMD / Apple): here the Mac uses `h264_videotoolbox` and
  the other machines, `libx264`.

---

## 15 · Files

```
~/.claude/skills/reel/cut/
├── CUT.md                        the short script the agent follows (flow, rules, acceptance, delivery)
├── references/
│   └── ROUGH-CUT.md             ← this document (the why of everything)
├── scripts/
│   ├── 0-check.py                 step 0: checks ffmpeg, whisper-cli, numpy and model; says how to install
│   ├── common.py                    whisper-cli, 16 kHz audio, prompts (fillers and names), model choice
│   ├── 1-takes.py                step 1: take map by energy + real text of each stretch
│   ├── 2-fillers.py                 step 2b: transcription that does not hide fillers, per keep
│   ├── 3-cut.py                  step 3: the engine (sound + fillers + valley + J/L) → edl, cut.wav, clean.mp4
│   ├── 4-review.py               step 4: text, repetitions, ±2 s splices, pauses
│   └── remap.py                 step 5: carries times from an old cut to the new one
├── example/                        the approved v2 reference
│   ├── takes.txt                 the take map of the raw
│   ├── keeps.json                  the 7 editorial decisions, with the "why"
│   ├── edl.json                    the 13 resulting segments
│   └── review.txt             the approved check
```

**Regression test (on the machine that has the example raw):** after changing the engine, run steps 1 to
4 with `example/keeps.json` over the example raw
and compare the `edl.json` with `example/edl.json`. If the change was not meant to alter this case, they must be
identical.
