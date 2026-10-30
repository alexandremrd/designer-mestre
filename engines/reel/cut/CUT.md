
# Cut engine · module 1 (the breakdown)
*Short script of the `reel` skill's cut engine (`cut/` folder). Identical to the engine approved in production in Oct/2026; the full document is `references/ROUGH-CUT.md`.*

**The rule in one sentence:** *you decide what stays by reading; the sound decides where to cut.* The choice of takes
is editorial, made on the real text of each stretch. The exact cut point is measured on the audio, never on Whisper's
word time.

The full document, with the why of each rule, the calibration, the diagnosis and the annotated breakdown of the
approved case, is in **`references/ROUGH-CUT.md`**. Read sections 5 (choosing takes) and 7 (acceptance
criteria) before the first cut of the session. The approved case is in `example/`, with `takes.txt`,
`keeps.json`, `edl.json` and `review.txt`.

## Flow

`S=~/.claude/skills/reel/cut/scripts` · `PASTA` = one working folder per video, created next to the
raw footage (e.g.: `<raw footage folder>/corte-<date>`). On Windows, run with `PYTHONUTF8=1` and use `python` in place of
`python3`.

Before each slow step (steps 1, 2 and 3), warn in one line ("Transcribing the takes, takes a few
minutes.") and run in the background.

0. **Machine ready?** The first time on each machine: `python3 $S/0-check.py`. If something is missing, it says
   how to install it.
1. **Take map:** `python3 $S/1-takes.py "<bruto>" PASTA`, then **read `PASTA/takes.txt`
   in full**. The script finds the speech by energy and transcribes each stretch by itself. Restarts show up as
   similar lines in sequence; false starts, as short lines ending in "...".
2. **Keeps:** write `PASTA/keeps.json` → `{"keeps":[{"from","to","why"}]}` (seconds **of the source**, in the
   order of the final video). The rules are right below.
   Then run `python3 $S/2-fillers.py PASTA` and read the output, which shows the "éé/hum" inside each keep.
3. **Engine:** `python3 $S/3-cut.py "<bruto>" PASTA` (`--jl 4` is the default; `--jl 0` turns J/L off;
   `--sem-video` generates only the audio and the edl). Fine adjustments go in `PASTA/adjustments.json`
   `{"cut":[[a,b]],"keep":[t],"force":[[a,b]]}`, with source times.
4. **Check:** `python3 $S/4-review.py PASTA --prompt "<proper names in the video>"`. Read
   `review.txt` **in full**. If any criterion fails, go back to step 2 or 3.
5. **Only if the visual edit already existed** and the cut changed: remap the times with `scripts/remap.py`
   (`Mapa(velho, novo).novo(t)`). Do not retime by hand.

## Keeps rules (summary of section 5)

- **One sentence, one take: the best complete one.** Discard the incomplete ones (end in "...", stop midway) and
  the ones with a stumble. Among the complete ones, the default is the **most recent**. The exception is when it is longer or
  has a crutch and another is equally complete and leaner: then the lean one stays.
- **A one-word false start also goes.** If two takes are less than 1 s apart, the `from`
  goes **flush** against the start of the good take, so the margin does not reach the false start.
- **Margin of 0.1 to 0.2 s** around the text. The engine snaps the edge to the nearest silence, searching
  outward from the text.
- **Joining takes** only pays off when each piece starts and ends at a sentence end and the result is more
  correct or leaner.
- **If different takes say different things**, choose by the correct information. If it is impossible to know
  which is correct, **ask** whoever recorded. In other cases, decide and record it in the `why`.
- **Always out:** "alô, alô", sound test, cough, "deixa eu refazer", off-script comment.
- **First syllable clipped:** advance the `from`, mark the keep with `"raw": true` or use `force`.

## Acceptance criteria (do not deliver without all of them)

| `review.txt` block | Must come out |
|---|---|
| Cut text | each sentence only once, no clipped word (a Whisper **name** error does not fail: fix it in the caption) |
| Adjacent repetitions | "nenhuma" (or an intentional repetition, recorded) |
| Splices (±2 s, no prompt) | all legible, no half word or mumbled restart. Starting mid-sentence is Whisper, not the cut: confirm in the neighboring window |
| Pauses > 0.25 s | "nenhuma" |

**Whisper traps:** it invents speech in long silence, hides repetition in long transcription, swallows the
start of a short clip, invents "é, ah, hum" when it receives the filler prompt on a short window, and sometimes
skips a whole sentence in the long transcription. Before concluding that something vanished, transcribe only that window.

## Delivery

Cut ready in `PASTA/clean.mp4`. For the style, `cut.wav`, `edl.json` and `cut_words.json` remain; the full
contract is in section 8 of the document. Short report, written in the user's language:

```
Cut ready: <path of clean.mp4>  ·  <raw duration> → <cut duration>
Takes used: <list with source time and the "why">
Left out: <false starts, abandoned sentences, tests, coughs...>
Fillers removed: <n>
Review: repetitions ok · joins ok · pauses ok
Uncertainties: <content decisions taken; what can only be validated by listening>
```

**Do not do in this module:** 9:16 crop, drawn captions, images, soundtrack, volume normalization (all
belong to the style). Never delete the raw footage nor write inside its folder outside the working `PASTA`.

## Tuning this skill

It was validated on one raw recording (male voice, close dynamic microphone, treated room). When a cut comes out
wrong on another recording:
1. find the symptom in the table in section 9 of the document (symptom → cause → adjustment);
2. change **one** parameter at a time at the top of `scripts/3-cut.py` (`REF_DB`, `HOLE`, `ISLAND`, `LEAD`, `TAIL`)
   or handle the case with `adjustments.json`;
3. record it in section 16 of the document: what changed, on what kind of recording and why.
If a change holds for all recordings, change the default. If it holds only for one type (lavalier, noisy
environment), note it as a profile in section 16 instead of changing the default.
