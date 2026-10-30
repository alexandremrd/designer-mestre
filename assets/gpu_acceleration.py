#!/usr/bin/env python3
"""GPU first (`standards.md` U13): picks the accelerated path and falls back to the CPU by itself.

  python gpu_acceleration.py            # status: GPU, VRAM and whether ffmpeg encodes with NVENC
  python gpu_acceleration.py profile     # machine profile: quality tier and what to pick for each task (--json for another script)
  from gpu_acceleration import h264, chromium_args

h264(ff, cpu_args, cq=18, bitrate=None, bufsize=None) -> video codec args.
  Tests NVENC with 1 frame; passed = returns h264_nvenc at high quality, otherwise returns cpu_args.
  With bitrate (capped CBR/VBR mode) uses -b:v/-maxrate; without it uses -cq (constant quality).
chromium_args() -> Chromium/Edge flags to rasterize and composite on the GPU.
"""
import functools, subprocess, sys


def nvidia():
    """(name, vram_gb) of the NVIDIA GPU, or (None, 0)."""
    try:
        o = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=15).stdout.strip().splitlines()[0]
        nome, mem = [x.strip() for x in o.split(",")]
        return nome, float(mem) / 1024
    except Exception:
        return None, 0


def _nvenc_args(cq, bitrate, bufsize):
    a = ["-c:v", "h264_nvenc", "-preset", "p7", "-tune", "hq", "-rc", "vbr", "-spatial-aq", "1",
         "-pix_fmt", "yuv420p"]
    if bitrate:
        a += ["-b:v", bitrate, "-maxrate", bitrate] + (["-bufsize", bufsize] if bufsize else [])
    else:
        a += ["-cq", str(cq), "-b:v", "0"]
    return a


@functools.lru_cache(maxsize=None)
def nvenc_ok(ff):
    """True if this ffmpeg encodes with NVENC on this machine (1-frame test, with the same args)."""
    try:
        r = subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                            "color=c=black:s=256x256:d=0.1", *_nvenc_args(18, None, None), "-f", "null", "-"],
                           capture_output=True, timeout=60)
        return r.returncode == 0
    except Exception:
        return False


def h264(ff, cpu_args, cq=18, bitrate=None, bufsize=None):
    if nvenc_ok(ff):
        print("[gpu] H.264 encode on NVENC", flush=True)
        return _nvenc_args(cq, bitrate, bufsize)
    print("[gpu] NVENC unavailable in this ffmpeg; H.264 encode on the CPU", flush=True)
    return cpu_args


def chromium_args():
    return ["--enable-gpu-rasterization", "--ignore-gpu-blocklist", "--enable-zero-copy", "--use-angle=d3d11"] \
        if sys.platform == "win32" else ["--enable-gpu-rasterization", "--ignore-gpu-blocklist"]


def preparar_cuda():
    """Puts on the process search path the CUDA DLLs (cuBLAS) that CTranslate2 and faster-whisper require.
    Without them the GPU loads the model and fails at transcription, and the script would silently fall back to the CPU. Looks first in PATH
    and then in the `Ferramentas` folders of the resource root (e.g. whisper.cpp-cuda). Returns True if found."""
    import glob, os
    if any(d and os.path.isfile(os.path.join(d, "cublas64_12.dll")) for d in os.environ.get("PATH", "").split(os.pathsep)):
        return True
    try:
        import resources
        raiz = resources.raiz()
    except Exception:
        raiz = None
    if raiz:
        for pasta in glob.glob(os.path.join(raiz, "Ferramentas", "*")):
            if os.path.isfile(os.path.join(pasta, "cublas64_12.dll")):
                os.environ["PATH"] = pasta + os.pathsep + os.environ.get("PATH", "")
                if hasattr(os, "add_dll_directory"):
                    os.add_dll_directory(pasta)
                return True
    return False


def _ram_gb():
    """Total RAM in GB (Windows via ctypes; otherwise None)."""
    try:
        import ctypes
        class MEM(ctypes.Structure):
            _fields_ = [("l", ctypes.c_ulong), ("u", ctypes.c_ulong), ("total", ctypes.c_ulonglong), ("livre", ctypes.c_ulonglong),
                        ("a", ctypes.c_ulonglong), ("b", ctypes.c_ulonglong), ("c", ctypes.c_ulonglong), ("d", ctypes.c_ulonglong), ("e", ctypes.c_ulonglong)]
        m = MEM(); m.l = ctypes.sizeof(MEM)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        return round(m.total / 1024 ** 3, 1)
    except Exception:
        return None


def patamar(vram_gb):
    """Quality tier the card sustains: 'sem GPU' (no GPU), 'basico' (< 6 GB), 'medio' (6 to 12 GB) or 'alto' (12 GB or more)."""
    if vram_gb <= 0:
        return "sem GPU"
    return "alto" if vram_gb >= 12 else "medio" if vram_gb >= 6 else "basico"


def perfil(ff=None):
    """What to pick for each task on this machine: always the highest tier the hardware can handle, GPU before CPU."""
    import shutil
    try:
        import resources
        resources.aplicar_env()
    except Exception:
        pass
    ff = ff or shutil.which("ffmpeg")
    nome, vram = nvidia()
    nivel = patamar(vram)
    nvenc = bool(ff) and nvenc_ok(ff)
    whisper = {"alto": "large-v3-turbo, then medium, on the GPU", "medio": "large-v3-turbo, then medium, on the GPU",
               "basico": "small on the GPU", "sem GPU": "small on the CPU (int8)"}[nivel]
    return {"gpu": nome, "vram_gb": round(vram, 1), "ram_gb": _ram_gb(), "patamar": nivel, "ffmpeg": ff, "nvenc": nvenc,
            "encode_h264": "h264_nvenc (p7, cq 15 to 18, high quality)" if nvenc else "libx264 (preset slow, crf 16): no NVENC in this ffmpeg",
            "transcricao": "Whisper: " + whisper + " (faster-whisper first, whisper.cpp with CUDA as fallback; the largest installed model; never downloads without the user's yes)",
            "navegador": "Chromium with " + " ".join(chromium_args()),
            "imagem_local": "local_engine.py detect picks the model the VRAM can handle; run it before generating",
            "regra": "highest quality the hardware sustains, GPU before CPU; CPU only on failure or proven insufficient VRAM"}


if __name__ == "__main__" and "profile" in sys.argv[1:]:
    import json
    p = perfil()
    if "--json" in sys.argv:
        print(json.dumps(p, ensure_ascii=False, indent=1))
    else:
        print(f"Machine: {p['gpu'] or 'no NVIDIA GPU'} · VRAM {p['vram_gb']} GB · RAM {p['ram_gb']} GB · tier {p['patamar'].upper()}")
        for k in ("encode_h264", "transcricao", "navegador", "imagem_local", "regra"):
            print(f"  {k}: {p[k]}")
elif __name__ == "__main__":
    import shutil
    nome, vram = nvidia()
    print(f"GPU: {nome or 'no NVIDIA'} · VRAM {vram:.1f} GB")
    ff = shutil.which("ffmpeg")
    if not ff:
        try:
            import imageio_ffmpeg; ff = imageio_ffmpeg.get_ffmpeg_exe()
        except ImportError:
            pass
    print(f"ffmpeg: {ff or 'not found'} · NVENC: {'yes' if ff and nvenc_ok(ff) else 'no'}")
