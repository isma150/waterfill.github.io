# Recovers alpha from black/white renders, crops to the drawn area, writes sprites/*.png and manifest.json.
import json, os
import numpy as np
from PIL import Image
BASE = os.path.dirname(os.path.abspath(__file__))
SPECS = json.load(open(os.path.join(BASE, "specs.json")))
out = {}
os.makedirs(os.path.join(BASE, "..", "sprites"), exist_ok=True)
for s in SPECS:
    name = s["name"]
    if s["mode"] == "opaque":
        im = Image.open(os.path.join(BASE, "raw", f"{name}_000000.png")).convert("RGB")
        # pad 70 px each side with edge colour: the layout is 480 wide, the HTML canvas is 420 (=> 560 HTML units)
        arr = np.asarray(im)
        arr = np.pad(arr, ((0, 0), (70, 70), (0, 0)), mode="edge")
        im = Image.fromarray(arr, "RGB")
        im.save(os.path.join(BASE, "..", "sprites", f"{name}.png"))
        out[name] = {"file": f"{name}.png", "w": im.width, "h": im.height, "ox": 280, "oy": 373, "opaque": True}
        continue
    b = np.asarray(Image.open(os.path.join(BASE, "raw", f"{name}_000000.png")).convert("RGB")).astype(np.float64)
    w = np.asarray(Image.open(os.path.join(BASE, "raw", f"{name}_ffffff.png")).convert("RGB")).astype(np.float64)
    a = 1.0 - (w - b).mean(axis=2) / 255.0
    a = np.clip(a, 0.0, 1.0)
    safe = np.maximum(a, 1e-6)[..., None]
    col = np.clip(b / safe, 0, 255)
    rgba = np.dstack([col, a * 255.0]).astype(np.uint8)
    ys, xs = np.where(a > 0.004)
    if len(xs) == 0:
        print("EMPTY", name); continue
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    crop = rgba[y0:y1, x0:x1]
    Image.fromarray(crop, "RGBA").save(os.path.join(BASE, "..", "sprites", f"{name}.png"))
    out[name] = {"file": f"{name}.png", "w": int(x1 - x0), "h": int(y1 - y0),
                 "ox": int(s["ax"] - x0), "oy": int(s["ay"] - y0), "opaque": False}
json.dump(out, open(os.path.join(BASE, "..", "sprites", "manifest.json"), "w"), indent=1)
print("sprites", len(out))
for k in ["veh_taxi", "enemy_police", "pick_coin", "wheel", "bg_city"]:
    print(k, out.get(k))
