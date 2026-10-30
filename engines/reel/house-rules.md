# House rules — apply to ALL styles

*Lessons from real production. Every style obeys this block. When a rule here conflicts with a
style's rule, **this one prevails**.*

## R1 · The face is never covered
No image, card, chip, panel, stamp, title or motion sits over the presenter's face (forehead to chin), not
darkened, not "just for an instant". To show something while they talk, in order of preference:
1. **Split screen:** graphics in the top half (y 270–810), camera in the bottom half with the whole face
   (the video moves down ≈ 990 − top of the head) and caption at the seam (y ≈ 830). Instant cut
   when a full-screen scene hides the switch; otherwise, a 0.4 s slide with the caption hidden.
2. **Below the face:** small objects (chips, 2–3 small cards, lettering) between the chin and the caption.
3. **Own background scene:** a screen without the presenter, with the elements spread out.

"Behind the head" titles (with the presenter cut out) only when there is room above the head: measure
the top of the head (`tools/face.py`). With less than ~300 px free, switch to lettering on the
chest. Every snapshot is checked for this rule; a frame with anything over the face fails.

## R2 · Sound effects used sparingly
At most **~0.85 SFX per second** (a 40 s reel has ~34, not 45).
- The whoosh only on a real scene switch.
- The beat/hit only on a stamp, X or impact moment.
- No sound on a small chip, a minor list item or an element that enters < 0.6 s after another sound.
- Low volumes (0.1–0.2 of the voice volume).
- Typing: natural sample, human rhythm (~9 keys/s), continuous over the whole stretch, never a
  synthetic burst; ≈ 12 dB below the voice.
- Sounds generated locally, no license involved (`tools/sfx.sh`):
  - whoosh: `ffmpeg -f lavfi -i "anoisesrc=color=pink:d=0.55" -af "highpass=f=300,lowpass=f=5500,afade=t=in:d=0.28,afade=t=out:st=0.3:d=0.25" whoosh.wav`;
  - hit: 52 Hz sine with 0.6 s decay;
  - pop: 1.25 kHz for 90 ms;
  - tick: 50 ms white noise with high-pass.

## R3 · Real, verified material
- Every spoken claim that becomes a screen is checked against an **official page** (date of the lookup noted).
- Every number on screen has a source (official price, plan, period).
- **Image priority:** 1. official screenshot/logo; 2. Wikimedia Commons / Openverse with license;
  3. the presenter's own files; 4. **declared illustration**: own HTML, fictional company,
  labeled as an illustration.
- **Never invent:** logo, cover, screenshot, number, result or follower count. A brand without a
  free logo enters as text only.
- CAPTCHA/anti-bot is never bypassed: switch tools or ask the presenter for the screenshot.
- Everything listed in `assets/SOURCES.md` (file, origin, license, date).
- If speech and screen use different currencies or units, check consistency and flag it in the delivery.

## R4 · Natural color on the face
No aggressive grade: the face stays natural. The color identity lives in the graphics (cards,
pills, glows), not in the skin. Approved values when there is a grade:
`saturate(1.04) contrast(1.05) brightness(0.97)`; tint layers ≤ 0.3.
A stronger grade only with a before × after shown and approved. In this skill the camera color is only the
approved filter from `vsl.json`; any extra grade respects this ceiling.

## R5 · Cut: no clipped word
- Remove pauses, breaths, "ééé", stutters and restarts, keeping the **last** correct take. A
  sentence repeated to fix the meaning also counts; the meaning decides.
- The sound-based cut clips the start and end of words in fast speech. **Every splice is checked** with
  a windowed transcript at the end of each segment.
- Clipped word → protect the stretch (keep the whole raw interval) and cut again.
- Never mix raw times with clean-video times. After any trim, retranscribe and
  remap everything that depended on the times.
- The cut belongs to the cut engine (`cut/`); the style receives the already clean video (`clean.mp4`).

## R6 · Caption with the right text
- Correct the transcript by hand before assembling. Typical transcription errors in this niche:

  | Transcription | Correct |
  |---|---|
  | Cloud | Claude |
  | A | IA |
  | Gama | Gamma |
  | carrocéis | carrosséis |
  | vim | envio |
  | Powerpoint | PowerPoint |

- Product names always as the brand writes them.
- CTA code word in UPPERCASE.
- Keep the original (`transcript-raw.json`) and correct by time, not by text, when the word
  repeats ("A" of "IA" × "A partir").

## R7 · Safe zone
- **Organic Reels/Shorts:** all text/UI in x 90–990, y 220–1520, and nothing in the button column
  (x > 940 and y > 1150).
- **Ad:** x 65–1015, y 270–1248.
- Backgrounds and decoration may bleed.
- Check with `tools/safe-zone.py` (sweep every 0.25 s).

## R8 · Final audio
- Integrated **−14 LUFS (±0.5)**, peak ≤ −0.5 dBFS, without re-encoding the image (`-c:v copy`).
- Two-pass loudnorm, or gain + limiter when linear loudnorm leaves the peak at 0 dBFS.
- In zsh, use `${var}` with braces inside filters.

## R9 · Verification before delivering
1. lint with 0 errors; 2. snapshot at each beat and each transition; 3. face (R1), safe zone (R7),
legible text and nothing cut off; 4. render; 5. audio (R8); 6. frame sheet of the final; 7. `VERIFY.md`
with duration, LUFS, what was protected in the cut, the caption corrections and the open points.
**Never publish or send the video.**

## R10 · Isolated environment
Paths come from environment variables (`WHISPER_PYTHON`, `FACE_MODEL`, `RVM_MODEL`, `CHROME`),
never from fixed user folders. Problems already seen: transcription "finishing" with no file → pin
`av==16.1.0`; snapshot breaking with a postcss error → `npm ci` at the root; cache folder that does not
exist → create it before downloading.

## R11 · Presenter profile
Name, @ and avatar come from the presenter's `perfil.json`. The avatar may be a frame from the video itself,
cropped. Follower count only if the presenter provides it. **No third-party name** (another
creator, course or product that is not the presenter's) appears in the video or in the project files.
