#!/usr/bin/env bash
# Contact sheet of the final video: 16 evenly spaced frames, 8×2, 216 px each (for the notes loop and VERIFY).
# Usage (in the engine folder):  bash tools/sheet.sh ../render/reel-v1.mp4 ../qa/final-sheet.png
set -euo pipefail
V="$1"; OUT="${2:-../qa/final-sheet.png}"; mkdir -p "$(dirname "$OUT")"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
STEP=$(python3 -c "print(round(${D}/16, 4))")
ffmpeg -v error -y -i "$V" -vf "fps=1/${STEP},scale=216:-1,tile=8x2" -frames:v 1 "$OUT"
echo "sheet: $OUT (one frame every ${STEP} s)"
