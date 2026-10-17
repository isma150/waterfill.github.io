"""Object types. Sprite objects use the rendered PNGs (sprites/manifest.json); Text and plugin objects follow the template."""
import json, os, shutil
from ev import sid
from art_extra import BTN_COLORS, CARD_COLORS

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPR = os.path.join(BASE, "sprites")
MAN = json.load(open(os.path.join(SPR, "manifest.json")))

def _hex(c):
    return c[1:].lower()

SHAPE_KEYS = ["bar_xp_bg", "bar_xp_fill", "bar_boss_bg", "bar_boss_fill", "bar_hp_bg", "bar_hp_ok", "bar_hp_bad",
              "bar_gold", "bar_dark", "hud_box", "hud_box_alpha", "bar_bg_warm", "bar_enemy_fill",
              "dim_defeat", "dim_pause", "dim_popup", "dim_black", "flash_red", "lock_corners", "pix_white",
              "pix_dark", "pix_tracer", "pix_speed", "pix_gold", "dot_gold", "dot_green", "cell_sel", "cell_nor",
              "cell_emp", "lock_badge", "dot_84c974", "sign_wood", "btn_clear", "circ_on", "circ_off", "dial_norm", "dial_buff", "needle", "star_gold", "guide_panel", "guide_title", "pix_c3c1b9", "pix_77716a", "pix_c0afa0", "pix_5c5a54",
              "pix_9e9d90", "pix_3c4344", "pix_fffdf4", "pix_fffdf4"]
SHAPE_KEYS = list(dict.fromkeys(SHAPE_KEYS))
# name -> (animations [(anim, spriteKey)], instance variables [(name, type, init)])
N = "number"
OBJECTS = {
    "Bg": ([(t, f"bg_{t}") for t in ["city", "blue", "mountain", "sunset", "rose", "paper", "garage", "map", "black"]], []),
    "Taxi": ([("taxi", "veh_taxi"), ("blue", "veh_blue"), ("mint", "veh_mint"), ("home", "veh_taxi_home")], [("id", N, "0")]),
    "Enemy": ([("police", "enemy_police"), ("ambulance", "enemy_ambulance"), ("van", "enemy_van")], [
        ("id", N, "0"), ("lane", N, "210"), ("laneFrom", N, "210"), ("laneTo", N, "210"), ("laneT", N, "1"),
        ("laneDur", N, "0.9"), ("d", N, "-0.45"), ("vd", N, "0"), ("hoverD", N, "-0.05"), ("dodge", N, "0"),
        ("dodgeCd", N, "1"), ("state", N, "0"), ("hold", N, "0"), ("hp", N, "1"), ("maxHp", N, "1"),
        ("roll", N, "0"), ("dodgeNow", N, "0"), ("kind", N, "0"),
        ("fire", N, "1"), ("age", N, "0"), ("training", N, "0"), ("sx", N, "210"), ("sy", N, "0"), ("sc", N, "1"),
        ("dist", N, "0"), ("inAoe", N, "0"), ("isTarget", N, "0"), ("pick", N, "0")]),
    "Boss": ([(t, f"boss_{t}") for t in ["convoy", "armored", "green", "orange", "police"]], [
        ("id", N, "0"), ("lane", N, "210"), ("laneFrom", N, "210"), ("laneTo", N, "210"), ("laneT", N, "1"),
        ("laneDur", N, "0.9"), ("d", N, "-0.45"), ("vd", N, "0.11"), ("hoverD", N, "-0.055"), ("hp", N, "1"),
        ("maxHp", N, "1"), ("fire", N, "1"), ("age", N, "0"), ("phase", N, "1"), ("state", N, "0"),
        ("sx", N, "210"), ("sy", N, "0"), ("sc", N, "1"), ("dist", N, "0"), ("inAoe", N, "0"),
        ("isTarget", N, "0"), ("pick", N, "0")]),
    "Shot": ([("dyn", "shot_dynamite")], [
        ("id", N, "0"), ("x0", N, "210"), ("d0", N, "0"), ("xl", N, "210"), ("dl", N, "0.5"), ("fly", N, "1"),
        ("age", N, "0"), ("exploded", N, "0"), ("done", N, "0"), ("training", N, "0"), ("sx", N, "210"),
        ("sy", N, "0"), ("sc", N, "1"), ("d", N, "0"), ("landed", N, "0"), ("dist", N, "0")]),
    "Warn": ([("warn", "shot_warning")], [("owner", N, "0"), ("sx", N, "210"), ("sy", N, "0"), ("sc", N, "1")]),
    "Pickup": ([("crate", "pick_crate"), ("coin", "pick_coin")], [
        ("id", N, "0"), ("progress", N, "0.02"), ("duration", N, "2.25"), ("amount", N, "25"), ("lane", N, "210"),
        ("training", N, "0"), ("collected", N, "0"), ("sx", N, "210"), ("sy", N, "0"), ("sc", N, "1"), ("pick", N, "0"),
        ("prev", N, "0"), ("dist", N, "0"), ("isCrate", N, "0")]),
    "Fx": ([("blast", "fx_blast"), ("burst", "fx_burst"), ("hurt", "fx_hurt"), ("miss", "fx_miss"),
            ("muzzle", "dot_gold"), ("tracer", "pix_tracer"), ("spark", "dot_gold")], [
        ("life", N, "0.5"), ("t", N, "0"), ("vx", N, "0"), ("vy", N, "0"), ("x0", N, "0"), ("y0", N, "0")]),
    "EnemyBar": ([("bg", "bar_hp_bg"), ("fill", "bar_enemy_fill")], [("owner", N, "0"), ("frac", N, "1")]),
    "Speed": ([("line", "pix_speed")], [("idx", N, "0")]),
    "Btn": ([(f"c{_hex(c)}", f"btn_{_hex(c)}") for c in BTN_COLORS] + [("cclear", "btn_clear")], [("id", N, "0")]),
    "Card": ([(f"c{_hex(c)}", f"card_{_hex(c)}") for c in CARD_COLORS], [("id", N, "0")]),
    "Shape": ([(k, k) for k in SHAPE_KEYS], [("id", N, "0")]),
    "Needle": ([("needle", "needle")], [("id", N, "0")]),
    "Icon": ([(k, k) for k in ["pick_coin", "pick_gem", "key_on", "key_off", "wpn_pistol", "wpn_bomb", "wpn_shot",
                               "wpn_machine", "cat_a", "cat_b", "cat_c", "cat_d", "cat_e", "cat_f"]], [("id", N, "0")]),
    "Wheel": ([("wheel", "wheel")], [("id", N, "0")]),
    "Logo": ([("logo", "title_logo")], [("id", N, "0")]),
    "Cloud": ([("cloud", "cloud_home")], [("id", N, "0")]),
    "Node": ([("normal", "node_normal"), ("active", "node_active"), ("locked", "node_locked")], [("id", N, "0")]),
    "Roulette": ([("base", "roulette_base")], [("id", N, "0")]),
}
# text object (Text plugin): one type, styles come from instance properties in the layouts
TEXT_OBJ = "Txt"
TEXT_OBJ_HIT = "TxtHit"
PLUGIN_TEMPLATE_OBJECTS = ["Audio", "Touch", "LocalStorage", "BgSample", "PauseBg", "UI_Sprites", "TemplateSprite"]
NEW_PLUGIN_OBJECTS = {"Keyboard": "Keyboard"}   # UNVERIFIED: plugin id used for keyboard input

# uids are project-wide: singleton instances take numbers far above the layout instances (1..~500)
_singleton_uid = [900000]
def next_singleton_uid():
    _singleton_uid[0] += 1
    return _singleton_uid[0]

def _initial(vtype, value):
    """Object-type instance variables store number types as numbers (C3 expects a finite number there; the
    "expected finite number" error came from the string "0"). Event variables keep strings, as in the template."""
    if vtype == "number":
        f = float(value)
        return int(f) if f.is_integer() else f
    return value

def _sprite_json(name, anims, ivars):
    animations = []
    for anim, key in anims:
        e = MAN[key]
        frame = {"width": e["w"], "height": e["h"], "originX": round(e["ox"] / e["w"], 6),
                 "originY": round(e["oy"] / e["h"], 6), "originalSource": "", "exportFormat": "lossless",
                 "exportQuality": 0.8, "fileType": "image/png", "imageSpriteId": sid(),
                 "useCollisionPoly": False, "duration": 1, "tag": ""}
        animations.append({"frames": [frame], "sid": sid(), "name": anim, "isLooping": False,
                           "isPingPong": False, "repeatCount": 1, "repeatTo": 0, "speed": 5})
    return {"name": name, "plugin-id": "Sprite", "sid": sid(), "isGlobal": False, "editorNewInstanceIsReplica": True,
            "instanceVariables": [{"name": n, "type": t, "initialValue": _initial(t, v), "desc": "", "show": True, "sid": sid()}
                                  for n, t, v in ivars],
            "behaviorTypes": [], "effectTypes": [], "animations": {"items": animations, "subfolders": []}}

def _text_json(name):
    return {"name": name, "plugin-id": "Text", "sid": sid(), "isGlobal": False, "editorNewInstanceIsReplica": True,
            "instanceVariables": [{"name": "id", "type": "number", "initialValue": 0, "desc": "", "show": True, "sid": sid()}],
            "behaviorTypes": [], "effectTypes": []}

def write_objects(out_dir, obj_dir):
    """Writes objectTypes/<name>.json and copies the images to images/<name>-<anim>-000.png. Returns names."""
    names = []
    for name, (anims, ivars) in OBJECTS.items():
        with open(os.path.join(obj_dir, f"{name}.json"), "w", encoding="utf-8") as fh:
            json.dump(_sprite_json(name, anims, ivars), fh, indent=1)
        for anim, key in anims:
            src = os.path.join(SPR, MAN[key]["file"])
            dst = os.path.join(out_dir, "images", f"{name.lower()}-{anim.lower()}-000.png")
            shutil.copyfile(src, dst)
        names.append(name)
    for name in [TEXT_OBJ, TEXT_OBJ_HIT]:
        with open(os.path.join(obj_dir, f"{name}.json"), "w", encoding="utf-8") as fh:
            json.dump(_text_json(name), fh, indent=1)
        names.append(name)
    for name, pid in NEW_PLUGIN_OBJECTS.items():
        # plugin objects without instances are singletons: the template's Touch/LocalStorage/Audio carry a
        # "singleglobal-inst" entry; without it C3 has no instance to load for the object type
        with open(os.path.join(obj_dir, f"{name}.json"), "w", encoding="utf-8") as fh:
            # same shape as the template's Touch object: name, plugin-id, sid, singleglobal-inst
            json.dump({"name": name, "plugin-id": pid, "sid": sid(),
                       "singleglobal-inst": {"type": name, "properties": {}, "uid": next_singleton_uid(), "sid": sid(),
                                             "tags": ""}}, fh, indent=1)
        names.append(name)
    return names
