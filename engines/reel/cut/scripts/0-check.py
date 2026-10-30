"""Step 0 — checks that the machine has everything for the Raw Edit and says how to install what is missing.

usage:  python3 0-check.py
"""
import os, platform, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ok = True
mac = platform.system() == "Darwin"
win = platform.system() == "Windows"

def linha(nome, passou, dica=""):
    global ok
    ok &= passou
    print(f"[{'ok' if passou else 'MISSING'}] {nome}" + ("" if passou else f"\n       → {dica}"))

ff = shutil.which("ffmpeg")
ver = ""
if ff:
    ver = subprocess.run([ff, "-version"], capture_output=True, text=True).stdout.split("\n")[0]
linha(f"ffmpeg {ver.split(' ')[2] if ver else ''}", bool(ff),
      "Mac: brew install ffmpeg · Windows: winget install Gyan.FFmpeg")

w = shutil.which("whisper-cli") or shutil.which("whisper-cpp") or shutil.which("main")
linha("whisper-cli (whisper.cpp)", bool(w),
      "Mac: brew install whisper-cpp · Windows: download the 'whisper-bin-x64' zip from github.com/ggml-org/whisper.cpp/releases and add the folder to PATH")

try:
    import numpy
    linha(f"numpy {numpy.__version__} (python {platform.python_version()})", True)
except ImportError:
    linha("numpy", False, f"{sys.executable} -m pip install numpy")

from common import MODELOS_PADRAO
m = os.environ.get("WHISPER_MODEL")
cands = [m] if m else MODELOS_PADRAO
achado = next((os.path.expanduser(c) for c in cands if c and os.path.exists(os.path.expanduser(c))), None)
linha(f"Whisper model {achado or ''}", bool(achado),
      "download ggml-large-v3-turbo.bin (1.6 GB) from huggingface.co/ggerganov/whisper.cpp to "
      "~/.cache/whisper-cpp/  (or set WHISPER_MODEL to the path)")

print("\nAll set." if ok else "\nInstall what is missing and run again.")
sys.exit(0 if ok else 1)
