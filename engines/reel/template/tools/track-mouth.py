"""Tracks MOUTH and face in the 9:16 video → assets/face-track.json (the caption that follows the mouth, K.mouthCaps).

Each frame: [t, mouthX, mouthY, mouthWidth, chinY, foreheadY, faceX0, faceX1] in video px (1080×1920),
smoothed (exponential moving average). A frame with no face repeats the last value.
Run in the engine folder:  $VSL_PYTHON tools/track-mouth.py [assets/clean.mp4] [assets/face-track.json]
Detector: MediaPipe Face Landmarker (the approved reference's; model in FACE_MODEL, R10, or downloaded to
./.modelos/). Without mediapipe, falls back to OpenCV (frontal Haar) with the mouth estimated from the face box — rougher,
but the caption still shows up below the chin.
"""
import json, os, sys, urllib.request
import cv2

src = sys.argv[1] if len(sys.argv) > 1 else "assets/clean.mp4"
out = sys.argv[2] if len(sys.argv) > 2 else "assets/face-track.json"
A = 0.35  # smoothing (0 = still, 1 = raw)


def mediapipe_detector():
    import mediapipe as mp
    from mediapipe.tasks.python import vision, BaseOptions
    model = os.environ.get("FACE_MODEL") or os.path.join(".modelos", "face_landmarker.task")
    if not os.path.exists(model):
        os.makedirs(os.path.dirname(model), exist_ok=True)
        urllib.request.urlretrieve("https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task", model)
    opts = vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=model), running_mode=vision.RunningMode.VIDEO,
                                        num_faces=1, min_face_detection_confidence=0.4, min_tracking_confidence=0.4)
    det = vision.FaceLandmarker.create_from_options(opts)

    def detect(img, ms, W, H):
        r = det.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), ms)
        if not r.face_landmarks: return None
        L = r.face_landmarks[0]
        P = lambda k: (L[k].x * W, L[k].y * H)
        (ux, uy), (lx, ly) = P(13), P(14)
        (cx0, _), (cx1, _) = P(61), P(291)
        xs = [p.x * W for p in L]
        return [(ux + lx) / 2, (uy + ly) / 2, abs(cx1 - cx0), P(152)[1], P(10)[1], min(xs), max(xs)]
    return detect, "mediapipe"


def opencv_detector():
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def detect(img, ms, W, H):
        k = 0.5
        g = cv2.cvtColor(cv2.resize(img, None, fx=k, fy=k), cv2.COLOR_BGR2GRAY)
        f = casc.detectMultiScale(g, 1.1, 5, minSize=(int(W * k * 0.18), int(W * k * 0.18)))
        if len(f) == 0: return None
        x, y, w, h = [v / k for v in max(f, key=lambda r: r[2] * r[3])]
        # average proportions of a frontal face in the Haar box: mouth at ~78 % of the height, chin at ~102 %, forehead at ~5 %
        return [x + w / 2, y + 0.78 * h, 0.36 * w, y + 1.02 * h, y + 0.05 * h, x, x + w]
    return detect, "opencv"


try: detect, nome = mediapipe_detector()
except Exception as e:
    print(f"mediapipe unavailable ({type(e).__name__}); using OpenCV")
    detect, nome = opencv_detector()

cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS) or 30; W = int(cap.get(3)); H = int(cap.get(4))
rows, last, sm, i = [], None, None, 0
while True:
    ok, img = cap.read()
    if not ok: break
    cur = detect(img, int(i * 1000 / fps), W, H)
    if cur is not None: last = cur
    cur = last
    if cur is not None:
        sm = cur if sm is None else [s + A * (c - s) for s, c in zip(sm, cur)]
        rows.append([round(i / fps, 3)] + [round(v, 1) for v in sm])
    i += 1
json.dump({"fps": fps, "w": W, "h": H, "detector": nome, "cols": ["t", "mx", "my", "mw", "chin", "top", "x0", "x1"], "rows": rows}, open(out, "w"))
print(f"{len(rows)} frames with a face out of {i} ({nome}) -> {out}")
