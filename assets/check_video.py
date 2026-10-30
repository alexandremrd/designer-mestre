#!/usr/bin/env python3
# check_video.py - /designer-mestre: checks the exported MP4 before showing it to the user (video.md §8).
# Verifies the decoded file, not the intent: format, frame 0, uncut pauses, animated entry/exit.
# Usage: uv run --with imageio-ffmpeg --with numpy --with pillow python check_video.py video.mp4 [--intro 2.8] [--end 3.9] [--breaths 2] [--max-pause 0.6]
import argparse, re, subprocess, sys
import numpy as np
import shutil
FF = shutil.which("ffmpeg")  # PATH first (run_reel_cut.ps1 applies D:\Recursos IA); imageio-ffmpeg only if missing
if not FF:
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()

def info(v):
    return subprocess.run([FF, "-hide_banner", "-i", v], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr

def quadro(v, t):
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{t:.3f}", "-i", v, "-frames:v", "1", "-vf", "scale=270:480", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(480, 270, 3).astype(np.float32) if len(raw) == 480 * 270 * 3 else None

def main():
    p = argparse.ArgumentParser(); p.add_argument("video")
    p.add_argument("--intro", type=float, default=0, help="duration of the entry screen (s)")
    p.add_argument("--end", dest="fim", type=float, default=0, help="duration of the exit screen (s)")
    p.add_argument("--breaths", dest="respiros", type=int, default=2, help="long pauses allowed (hook and before the CTA)")
    p.add_argument("--max-pause", dest="max_pausa", type=float, default=0.6)
    a = p.parse_args(); v = a.video; res = []
    i = info(v); dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", i).expand(r"\1 \2 \3").split()[0]) * 0
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", i).groups(); dur = int(h) * 3600 + int(m) * 60 + float(s)
    ok = lambda c, msg: res.append((bool(c), msg))
    ok("1080x1920" in i and "SAR 1:1" in i and "yuv420p" in i, "format 1080x1920, SAR 1:1, yuv420p")
    f0 = quadro(v, 0.0)
    cinza = f0 is not None and f0.std() < 4 and 90 < f0.mean() < 170 and abs(f0[..., 0].mean() - f0[..., 2].mean()) < 6
    ok(f0 is not None and not cinza, "frame 0 is not flat gray")
    if a.intro > 0.8:
        d = np.abs(quadro(v, 0.2) - quadro(v, min(1.4, a.intro - 0.2))).mean()
        ok(d > 1.0, f"animated entry (variation between frames {d:.1f})")
    if a.fim > 1.5:
        d = np.abs(quadro(v, dur - a.fim + 0.3) - quadro(v, dur - 0.1)).mean()
        ok(d > 1.0, f"animated exit (variation between frames {d:.1f})")
    raw = subprocess.run([FF, "-v", "error", "-i", v, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    au = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    rm = np.array([float(np.sqrt((au[k:k + 160] ** 2).mean())) for k in range(0, len(au) - 160, 160)])
    i0, i1 = int((a.intro + 0.1) * 100), int((dur - a.fim - 0.1) * 100)
    pausas, k = [], i0
    while k < i1:
        if rm[k] < 0.004:
            j = k
            while j < i1 and rm[j] < 0.004: j += 1
            if (j - k) / 100 > a.max_pausa: pausas.append((k / 100, (j - k) / 100))
            k = j
        else: k += 1
    ok(len(pausas) <= a.respiros, f"pauses > {a.max_pausa}s in speech: {len(pausas)} (allowed {a.respiros})" + ("" if len(pausas) <= a.respiros else " -> " + ", ".join(f"{t:.1f}s({d:.2f})" for t, d in pausas)))
    for c, msg in res: print(("PASS " if c else "FAIL ") + msg)
    print(f"duration {dur:.2f}s")
    sys.exit(0 if all(c for c, _ in res) else 1)

if __name__ == "__main__":
    main()
