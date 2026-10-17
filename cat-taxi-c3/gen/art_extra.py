"""PIL art for generic shapes (buttons, cards, bars, overlays, lines). Colours copied from the HTML."""
import json, os
from PIL import Image, ImageDraw
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "sprites")
MAN = os.path.join(OUT, "manifest.json")

BTN_COLORS = ["#fffdf7", "#fffcf7", "#edb847", "#568dce", "#67b6a4", "#f8d36d", "#f9d575", "#f5cf67", "#b4ecbf",
              "#9ee4f5", "#e6e4dd", "#f6d06b", "#f7d46d", "#f5a48e", "#f5d47b", "#f5dda8", "#b9f2f2", "#f8d16d",
              "#edc5b8", "#d9ddd4", "#f0d389", "#eec0ae", "#f7d376", "#bedfc4", "#c8ecae", "#fff0aa", "#f5f1e9",
              "#ffe8a9", "#ffefb9", "#fffef6", "#eee8dc", "#e7e2d9", "#fffcf6", "#fff5df"]
CARD_COLORS = ["#fffdf8", "#fffef9", "#fffdf4", "#faf8f1", "#fff6dd", "#fffdf7", "#fffdf6", "#fffdf2", "#fffaf0"]

def _rr(im, box, r, fill, outline=None, lw=2):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=lw)

def button_png(color):
    W, H = 250, 150
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # shadow (HTML: fillRound(x+2,y+4,w,h,'#a09a8a4d',9))
    _rr(im, (2 + 4, 4 + 6, 2 + 4 + 240 - 1, 4 + 6 + 140 - 1), 9, (0xa0, 0x9a, 0x8a, 0x4d))
    # body (HTML: fillRound(x,y,w,h,color,9,outline,2.2))
    _rr(im, (4, 6, 4 + 240 - 1, 6 + 140 - 1), 9, color, (0x51, 0x4a, 0x41, 255), 3)
    return im

def card_png(color):
    W, H = 250, 150
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    _rr(im, (6, 8, 6 + 240 - 1, 8 + 140 - 1), 11, (0x39, 0x36, 0x20, 0x20))
    _rr(im, (4, 6, 4 + 240 - 1, 6 + 140 - 1), 11, color, (0x5b, 0x57, 0x4f, 255), 3)
    return im

def solid_rr(color, alpha=255, stroke=None, r=5, w=50, h=12):
    W, H = w + 4, h + 4
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rgba = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5)) + (alpha,)
    _rr(im, (1, 1, W - 2, H - 2), r, rgba, stroke, 2 if stroke else 0)
    return im

def dim_png(color_hex, alpha):
    im = Image.new("RGBA", (560, 746), tuple(int(color_hex[i:i + 2], 16) for i in (1, 3, 5)) + (alpha,))
    return im

def lock_png():
    # HTML drawLock: four corner brackets, orange #e8842c, width 3
    W, H = 80, 80
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = (0xe8, 0x84, 0x2c, 255)
    for sx, sy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        cx = W / 2 + sx * 25; cy = H / 2 + sy * 18
        d.line([(cx - sx * 10, cy), (cx, cy)], fill=c, width=3)
        d.line([(cx, cy), (cx, cy - sy * 10)], fill=c, width=3)
    return im

def dot_png(color_hex, alpha=255):
    im = Image.new("RGBA", (4, 4), tuple(int(color_hex[i:i + 2], 16) for i in (1, 3, 5)) + (alpha,))
    return im

def ellipse_png(color_hex, w=12, h=12):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse((0, 0, w - 1, h - 1), fill=tuple(int(color_hex[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    return im

def circle_png(fill, stroke, r, lw):
    d = 2 * r + 4
    im = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse((2, 2, d - 3, d - 3), fill=tuple(fill), outline=tuple(stroke) + (255,), width=lw)
    return im

def needle_png():
    # HTML: line [[0,12],[0,-23]] stroke #567e60 width 2.6 ; origin = pivot, 23 px from the top
    im = Image.new("RGBA", (5, 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).line([(2, 0), (2, 35)], fill=(0x56, 0x7e, 0x60, 255), width=3)
    return im

def star_png():
    # HTML: 10-point star, outer r 10, inner r 4.5, fill #f2c94c, stroke #8f7420
    import math
    im = Image.new("RGBA", (30, 30), (0, 0, 0, 0))
    pts = []
    for i in range(10):
        r = 10 if i % 2 == 0 else 4.5
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((15 + math.cos(a) * r, 15 + math.sin(a) * r))
    ImageDraw.Draw(im).polygon(pts, fill=(0xf2, 0xc9, 0x4c, 255), outline=(0x8f, 0x74, 0x20, 255))
    return im

def rr_art(fill, stroke, r, w, h, lw, alpha=255):
    im = Image.new("RGBA", (w + 4, h + 4), (0, 0, 0, 0))
    rgba = tuple(int(fill[i:i + 2], 16) for i in (1, 3, 5)) + (alpha,)
    st = tuple(int(stroke[i:i + 2], 16) for i in (1, 3, 5)) + (255,) if stroke else None
    _rr(im, (1, 1, w + 1, h + 1), r, rgba, st, int(lw) if lw else 0)
    return im

def build():
    man = json.load(open(MAN))
    made = {}
    def save(key, im, origin=None):
        fn = f"{key}.png"
        im.save(os.path.join(OUT, fn))
        w, h = im.size
        ox, oy = origin if origin else (w // 2, h // 2)
        man[key] = {"file": fn, "w": w, "h": h, "ox": ox, "oy": oy, "opaque": False}
        made[key] = fn
    for c in BTN_COLORS:
        save("btn_" + c[1:], button_png(tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)))
    for c in CARD_COLORS:
        save("card_" + c[1:], card_png(tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)))
    # bars (generic rounded rect, stretched per instance)
    for key, col in [("bar_xp_bg", "#fffefa"), ("bar_xp_fill", "#efc359"), ("bar_boss_bg", "#faf7e9"),
                     ("bar_boss_fill", "#6dbd65"), ("bar_hp_bg", "#e4e7df"), ("bar_hp_ok", "#6aca51"),
                     ("bar_hp_bad", "#ec816e"), ("bar_enemy_fill", "#6aca51"), ("bar_gold", "#f2c94c"),
                     ("bar_dark", "#48443d"), ("bar_bg_warm", "#fffcf6"), ("hud_box", "#e8e5d9")]:
        save(key, solid_rr(col, 255, None, 6, 60, 12))
    save("hud_box_alpha", solid_rr("#e8e5d9", 196, None, 8, 94, 33))
    save("dim_defeat", dim_png("#272928", 0x95))
    save("dim_pause", dim_png("#242925", 0x9c))
    save("dim_popup", dim_png("#252420", 0x9e))
    save("dim_black", dim_png("#000000", 255))
    save("flash_red", dim_png("#df4646", 255))
    save("lock_corners", lock_png())
    save("pix_white", dot_png("#ffffff", 255), origin=(0, 0))
    save("pix_dark", dot_png("#3c4344", 255), origin=(0, 0))
    save("pix_tracer", dot_png("#f3bd5b", 255), origin=(0, 0))
    save("pix_speed", dot_png("#3c4344", 255), origin=(0, 0))
    save("pix_gold", dot_png("#ffe6a1", 255), origin=(0, 0))
    save("dot_gold", ellipse_png("#ffe6a1", 12, 12))
    save("dot_green", ellipse_png("#65cb67", 12, 12))
    # cell states of the garage grid (HTML: fillRound(x,y,90,56,fill,7,stroke,1.8))
    for key, fill, stroke in [("cell_sel", "#ffefb9", "#d7a138"), ("cell_nor", "#fffef6", "#9c9488"),
                              ("cell_emp", "#eee8dc", "#9c9488")]:
        save(key, rr_art(fill, stroke, 7, 90, 56, 1.8))
    save("lock_badge", rr_art("#e7e2d9", None, 5, 25, 23, 0, alpha=0xd7))
    save("dot_84c974", ellipse_png("#84c974", 18, 18))
    save("btn_clear", Image.new("RGBA", (250, 150), (0, 0, 0, 0)))
    # HUD circles (HTML: ell(45,95,24,24,'#fffefaed', stroke, 2)) and the weapon dial (ell(210,681,32,32,...))
    save("circ_on", circle_png((255, 254, 250, 0xed), (0x65, 0xba, 0x67), 24, 2))
    save("circ_off", circle_png((255, 254, 250, 0xed), (0x8a, 0x8b, 0x7e), 24, 2))
    save("dial_norm", circle_png((255, 253, 240, 0x8a), (0x6a, 0x69, 0x60), 32, 2))
    save("dial_buff", circle_png((0xb3, 0xe3, 0xa1, 0xb5), (0x6a, 0x69, 0x60), 32, 2))
    save("needle", needle_png())
    save("star_gold", star_png())
    save("guide_panel", rr_art("#fffdf2", "#8f8a76", 13, 384, 149, 2, alpha=0xf1))
    save("guide_title", rr_art("#f2d88a", None, 8, 366, 28, 0))
    save("sign_wood", rr_art("#b97a44", "#6a4826", 5, 82, 44, 2))
    for col in ["#c3c1b9", "#77716a", "#c0afa0", "#5c5a54", "#9e9d90", "#3c4344", "#fffdf4"]:
        save("pix_" + col[1:], dot_png(col, 255), origin=(0, 0))
    json.dump(man, open(MAN, "w"), indent=1)
    return made

if __name__ == "__main__":
    m = build()
    print("extra sprites", len(m))
