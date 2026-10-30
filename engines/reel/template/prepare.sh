#!/usr/bin/env bash
# prepare.sh — prepares the style 03 · VSL composition inside the engine folder (<P>/motor, the copy of this template/).
# Run in <P>/motor:   bash prepare.sh
# Standalone (outside the studio):   bash prepare.sh --video clean.mp4 [--words cut_words.json|palavras.json|transcript.json] [--audio cut.wav]
#
# Reads from the studio project (the parent folder, P):
#   camera   P/cut/clean-916-grade.mp4 (9:16 already graded, if any) → else clean-916.mp4 → else cut/clean.mp4
#   voice    P/cut/cut.wav (else the camera's own audio)
#   words    P/preparo/palavras.json (corrected, R6) → else P/cut/cut_words.json
#   fonts    P/assets/fonts/ (skin's fontes.css) · real material P/assets/oficiais/ and P/assets/gerados/ → assets/img/
# Writes here (in the engine folder):
#   assets/clean.mp4        1080×1920, 30 fps, keyframe every 1 s (-g 30), with the voice (horizontal → center crop)
#   assets/transcript.json  {"words":[{"text","start","end"}],"audio_duration_secs"} (+ transcript-whisper.json, the original copy)
#   assets/face-track.json  mouth tracking (tools/track-mouth.py: MediaPipe; without it, OpenCV)
#   node_modules/           npm install (hyperframes 0.7.109, gsap 3.14.2, playwright) — or VSL_NODE_MODULES=<ready folder>
#   vsl.json, src/beats.js, src/index.template.html, index.html (first assembly)
# Variables (R10): VSL_PYTHON (Python with mediapipe/opencv; default python3), FACE_MODEL, VSL_NODE_MODULES, CHROME.
set -euo pipefail
M="$(cd "$(dirname "$0")" && pwd)"; cd "$M"; P="$(cd .. && pwd)"
VIDEO=""; PALAVRAS=""; AUDIO=""
while [[ $# -gt 0 ]]; do case "$1" in
  --video) VIDEO="$2"; shift 2;; --words) PALAVRAS="$2"; shift 2;; --audio) AUDIO="$2"; shift 2;;
  *) echo "unknown option: $1"; exit 1;; esac; done
mkdir -p assets/img src snapshots
PY="${VSL_PYTHON:-python3}"

# --- inputs ---
if [[ -z "$VIDEO" ]]; then
  for f in "$P/cut/clean-916-grade.mp4" "$P/cut/clean-916.mp4" "$P/cut/clean.mp4"; do [[ -f "$f" ]] && { VIDEO="$f"; break; }; done
fi
[[ -z "$AUDIO" && -f "$P/cut/cut.wav" ]] && AUDIO="$P/cut/cut.wav"
if [[ -z "$PALAVRAS" ]]; then
  for f in "$P/preparo/palavras.json" "$P/cut/cut_words.json"; do [[ -f "$f" ]] && { PALAVRAS="$f"; break; }; done
fi
[[ -f "${VIDEO:-}" ]] || { echo "camera not found (cut/clean-916-grade.mp4 or --video)"; exit 1; }
echo "camera: $VIDEO"; echo "voice: ${AUDIO:-(from the camera itself)}"; echo "words: ${PALAVRAS:-(none — transcribe first)}"

# --- 9:16 camera with the voice, keyframe every 1 s (without it the render freezes frames) ---
read -r W H < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$VIDEO" | tr ',' ' ')
VF="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
[[ "$W" == 1080 && "$H" == 1920 ]] && VF="null"
if [[ -n "$AUDIO" ]]; then
  ffmpeg -v error -y -i "$VIDEO" -i "$AUDIO" -map 0:v:0 -map 1:a:0 -vf "$VF" -r 30 -c:v libx264 -crf 16 -preset medium -g 30 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart assets/clean.mp4
else
  ffmpeg -v error -y -i "$VIDEO" -map 0:v:0 -map '0:a:0?' -vf "$VF" -r 30 -c:v libx264 -crf 16 -preset medium -g 30 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -ar 48000 -movflags +faststart assets/clean.mp4
fi
echo "assets/clean.mp4 ready (${W}×${H} → 1080×1920)"

# --- transcript in the kit's format ---
if [[ -n "$PALAVRAS" ]]; then
  python3 - "$PALAVRAS" assets/clean.mp4 assets <<'PY'
import json, subprocess, sys, os
src, video, out = sys.argv[1:4]
d = json.load(open(src, encoding="utf-8"))
if isinstance(d, dict) and "words" in d: W = [{"text": w["text"], "start": w["start"], "end": w["end"]} for w in d["words"]]
elif d and isinstance(d[0], list): W = [{"text": t, "start": a, "end": b} for a, b, t in d]          # cut_words.json
else: W = [{"text": w["t"], "start": w["i"], "end": w["f"]} for w in d]                            # preparo/palavras.json
W = [w for w in W if str(w["text"]).strip()]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video], capture_output=True, text=True).stdout)
t = {"words": [{"text": str(w["text"]).strip(), "start": round(float(w["start"]), 3), "end": round(float(w["end"]), 3)} for w in W], "audio_duration_secs": round(dur, 3)}
if not os.path.exists(os.path.join(out, "transcript-whisper.json")): json.dump(t, open(os.path.join(out, "transcript-whisper.json"), "w", encoding="utf-8"), ensure_ascii=False)
json.dump(t, open(os.path.join(out, "transcript.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(f"assets/transcript.json: {len(t['words'])} words, {dur:.2f} s — check names and the CTA code word (R6)")
PY
fi

# --- skin fonts and real project material ---
if [[ -d "$P/assets/fonts" ]]; then cp -R "$P/assets/fonts/." assets/fonts/ 2>/dev/null || true; fi
for d in "$P/assets/oficiais" "$P/assets/gerados"; do if [[ -d "$d" ]]; then cp -R "$d/." assets/img/ 2>/dev/null || true; fi; done

# --- dependencies (reference versions) ---
if [[ ! -e node_modules ]]; then
  if [[ -n "${VSL_NODE_MODULES:-}" && -d "$VSL_NODE_MODULES" ]]; then ln -s "$VSL_NODE_MODULES" node_modules; echo "node_modules: $VSL_NODE_MODULES"
  else npm install --no-audit --no-fund --silent && echo "npm ok (hyperframes 0.7.109 · gsap 3.14.2)"; fi
fi

# --- mouth tracking (the caption that follows the mouth depends on it) ---
"$PY" tools/track-mouth.py assets/clean.mp4 assets/face-track.json || echo "WARNING: mouth tracking failed — without it there is no caption (set VSL_PYTHON with mediapipe or opencv)"

# --- first assembly ---
node assemble.mjs
cat <<EOF

Engine ready at: $M
Phase 1: check assets/transcript.json (R6) · measure face/head/punch on a frame → vsl.json · material → assets/img + ../assets/SOURCES.md
        · assets/map.md → src/beats.js (ruler: example/beats-example.js) · ../entrega/plan.json → node tools/cards.mjs
Phase 2: see README.md (render, camera-only, audio, sounds.json, sheet, safe zone, VERIFY).
EOF
