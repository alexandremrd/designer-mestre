#!/usr/bin/env python3
"""Presenter cutout (matte) with Robust Video Matting, for titles behind the head and compositing.

Usage: RVM_PYTHON=~/.venvs/rvm/bin/python  $RVM_PYTHON tools/crop.py <video> <output folder> [--from 0] [--to end]
      [--width W --height H] [--model resnet50|mobilenetv3] [--reduce 0.25]
Output: <folder>/matte/fg.mov (ProRes 4444 with alpha, same frame rate as the original) and <folder>/matte/fg.webm (VP9 with alpha,
to use in <video> in HyperFrames). Runs in the Python of the venv that has torch (RVM_PYTHON variable, rule R10); downloads
the model through torch.hub the first time. On 2560×1440 video it takes a few minutes per minute of video (MPS/CPU).
"""
import argparse, json, os, subprocess, sys

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("pasta"); ap.add_argument("--from", dest="de", type=float, default=0.0); ap.add_argument("--to", dest="ate", type=float); ap.add_argument("--width", dest="largura", type=int); ap.add_argument("--height", dest="altura", type=int); ap.add_argument("--model", dest="modelo", default="resnet50"); ap.add_argument("--reduce", dest="reduzir", type=float, default=0.25)
    a = ap.parse_args()
    try: import numpy as np, torch
    except ImportError: sys.exit("needs torch: run with the Python of the RVM venv (RVM_PYTHON=.../bin/python) or install torch, torchvision, numpy")
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate:format=duration", "-of", "json", a.video], capture_output=True, text=True).stdout)
    s = j["streams"][0]; W = a.largura or s["width"]; H = a.altura or s["height"]; FPS = s["r_frame_rate"]; fim = a.ate or float(j["format"]["duration"])
    out = os.path.join(a.pasta, "matte"); os.makedirs(out, exist_ok=True); mov = os.path.join(out, "fg.mov"); webm = os.path.join(out, "fg.webm")
    dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.hub.load("PeterL1n/RobustVideoMatting", a.modelo, pretrained=True, trust_repo=True).eval().to(dev)
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(a.de), "-to", str(fim), "-i", a.video, "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-"], stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", FPS, "-i", "-", "-c:v", "prores_ks", "-profile:v", "4", "-qscale:v", "9", "-pix_fmt", "yuva444p10le", "-alpha_bits", "8", mov], stdin=subprocess.PIPE)
    n = W * H * 3; rec = [None] * 4; first = True; count = 0
    with torch.no_grad():
        while True:
            buf = rd.stdout.read(n)
            if len(buf) < n: break
            frame = torch.from_numpy(np.frombuffer(buf, np.uint8).copy()).view(H, W, 3).permute(2, 0, 1).float().div(255).unsqueeze(0).to(dev)
            if first:
                for _ in range(12): fgr, pha, *rec = model(frame, *rec, downsample_ratio=a.reduzir)
                first = False
            fgr, pha, *rec = model(frame, *rec, downsample_ratio=a.reduzir)
            rgba = torch.cat([fgr[0], pha[0]], 0).permute(1, 2, 0).mul(255).clamp(0, 255).byte().cpu().numpy()
            wr.stdin.write(rgba.tobytes()); count += 1
            if count % 48 == 0: print(f"{count} frames", flush=True)
    wr.stdin.close(); wr.wait(); rd.wait()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mov, "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "24", "-an", webm], check=True)
    json.dump({"quadros": count, "largura": W, "altura": H, "fps": FPS, "de": a.de, "ate": fim, "mov": mov, "webm": webm}, open(os.path.join(out, "matte.json"), "w"), indent=1)
    print(f"done: {count} frames →{mov} e {webm}")

if __name__ == "__main__": main()
