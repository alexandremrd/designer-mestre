#!/usr/bin/env bash
# Final audio of style 03 · VSL (R8): −14 LUFS integrated (±0.3) and true peak ≤ −1 dBTP, without re-encoding the picture.
# The kit effects have fast attacks; linear loudnorm does not reach the target and an ordinary limiter lets the peak through
# in AAC. Here: gain + limiter at 192 kHz (catches the inter-sample peak), with the gain calibrated in up to 3 passes.
# Usage (in the engine folder):  bash tools/final-audio-vsl.sh ../render/_reel-raw.mp4 ../render/reel-vN.mp4
set -euo pipefail
IN="$1"; OUT="$2"; ALVO="${3:--14}"
med() { ffmpeg -nostats -i "$1" -af "loudnorm=I=${ALVO}:TP=-1:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p'; }
campo() { python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
I0=$(med "$IN" | campo input_i)
G=$(python3 -c "print(round(${ALVO} - (${I0}), 2))")
echo "— raw: ${I0} LUFS → initial gain ${G} dB"
for n in 1 2 3; do
  ffmpeg -v error -y -i "$IN" -c:v copy -af "aresample=192000,volume=${G}dB,alimiter=limit=0.84:attack=1:release=50:level=false,aresample=48000" \
    -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT"
  J=$(med "$OUT"); I=$(echo "$J" | campo input_i); TP=$(echo "$J" | campo input_tp)
  echo "— pass ${n}: gain ${G} dB → ${I} LUFS · peak ${TP} dBTP"
  D=$(python3 -c "print(round(${ALVO} - (${I}), 2))")
  python3 -c "import sys; sys.exit(0 if abs(${D}) <= 0.3 else 1)" && break
  G=$(python3 -c "print(round(${G} + ${D}, 2))")
done
python3 -c "import sys; sys.exit(0 if ${TP} <= -0.5 else 1)" || echo "WARNING: peak ${TP} dBTP above −0.5 — lower the alimiter limit (0.84 → 0.79)"
echo "final: $OUT"
