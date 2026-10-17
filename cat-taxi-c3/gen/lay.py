"""Layout JSON helpers. Positions/sizes are given in HTML units (420x746) and converted to layout units."""
import copy, json, os
from ev import sid
from cfg import lx, ly
from objects import MAN, TEXT_OBJ
from ids import nid
K = 6 / 7
TPL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "template")

_uid = [0]
def uid():
    _uid[0] += 1
    return _uid[0]

def hexrgba(c, a=1.0):
    c = c.lstrip("#")
    if len(c) == 8:
        a = int(c[6:8], 16) / 255
        c = c[:6]
    return [int(c[0:2], 16) / 255, int(c[2:4], 16) / 255, int(c[4:6], 16) / 255, a]

def layer(name, bg=(1, 1, 1, 1), transparent=True, interactive=True, visible=True):
    return {"name": name, "overriden": 0, "subLayers": [], "instances": [], "sid": sid(),
            "effectTypes": [], "isInitiallyVisible": visible, "isInitiallyInteractive": interactive,
            "isHTMLElementsLayer": False, "color": [1, 1, 1, 1], "backgroundColor": list(bg),
            "isTransparent": transparent, "sampling": "auto", "parallaxX": 1, "parallaxY": 1,
            "scaleRate": 1, "forceOwnTexture": False, "renderingMode": "3d", "drawOrder": "z-order",
            "useRenderCells": False, "blendMode": "normal", "zElevation": 0, "global": False}

def guide_layer():
    src = json.load(open(os.path.join(TPL, "layouts\\Game.json"), encoding="utf-8"))
    g = copy.deepcopy(src["layers"][0])
    assert g["name"] == "Template"
    g["sid"] = sid()
    g["isInitiallyInteractive"] = False
    for i in g["instances"]:
        i["uid"] = uid()
        i["sid"] = sid()
    return g

class Lay:
    """A layout under construction. Layers are added in draw order (first = bottom)."""
    def __init__(self, name, event_sheet):
        self.name = name
        self.sheet = event_sheet
        self.layers = {}
        self.order = []
        self.add_layer("Background")

    def add_layer(self, name, visible=True, interactive=True):
        if name not in self.layers:
            self.layers[name] = layer(name, (0.95, 0.93, 0.85, 1), False, interactive, visible)
            self.order.append(name)
        return name

    def _inst(self, obj, x, y, w, h, anim, props, ivars):
        return {"type": obj, "properties": props, "uid": uid(), "sid": sid(), "tags": "",
                "instanceVariables": ivars, "behaviors": {}, "materialSurfaceType": "smooth",
                "showing": True, "locked": False,
                "world": {"x": x, "y": y, "width": w, "height": h, "originX": 0.5, "originY": 0.5,
                          "color": [1, 1, 1, 1], "z": 0, "angle": 0}}

    def img(self, layer_name, obj, anim, x, y, scale=1.0, w=None, h=None, id_=None, visible=True, angle=0.0, ivars=None):
        """Sprite instance at HTML position (x,y). scale = HTML scale; w/h override HTML size."""
        self.add_layer(layer_name)
        mw, mh = MAN_SIZE(obj, anim)
        W = w * K if w is not None else mw * scale * K
        H = h * K if h is not None else mh * scale * K
        props = {"initially-visible": visible, "initial-animation": anim, "initial-frame": 0,
                 "enable-collisions": False, "live-preview": False}
        iv = dict(ivars or {})
        if id_ is not None:
            iv["id"] = id_
        inst = self._inst(obj, lx(x), ly(y), W, H, anim, props, iv)
        inst["world"]["angle"] = angle
        self.layers[layer_name]["instances"].append(inst)
        return inst

    def txt(self, layer_name, text, x, y, size=18, color="#30302c", align="center", tid=None, w=380,
            bold=True, wrap=False, visible=True, lines_h=None):
        """Text instance. x is the left edge (align left), centre (center) or right edge (right)."""
        self.add_layer(layer_name)
        bw = w * K
        cx = x + (w / 2 if align == "left" else -w / 2 if align == "right" else 0)
        bh = (lines_h or size * 2) * K
        props = {"text": text, "enable-bbcode": False, "font": "Arial", "size": round(size * K, 3), "line-height": 0,
                 "bold": bold, "italic": False, "color": hexrgba(color),
                 "horizontal-alignment": align, "vertical-alignment": "center",
                 "wrapping": "word" if wrap else "none", "text-direction": "ltr", "icon-set": -1,
                 "initially-visible": visible, "origin": "center", "read-aloud": False}
        iv = {}
        if tid is not None:
            iv["id"] = tid
        inst = self._inst(TEXT_OBJ, lx(cx), ly(y), bw, bh, "", props, iv)
        self.layers[layer_name]["instances"].append(inst)
        return inst

    def btn(self, layer_name, bid, x, y, w, h, label, color="#fffdf7", size=18, fg="#33322f", visible=True, tid=None):
        """Button = Btn sprite (stretched) + Txt label. bid is the instance id used by touch events."""
        self.img(layer_name, "Btn", f"c{color[1:].lower()}", x + w / 2, y + h / 2, w=w, h=h, id_=bid, visible=visible)
        if label is not None:
            self.txt(layer_name, label, x + w / 2, y + h / 2, size=size, color=fg,
                     tid=tid if tid is not None else nid(f"lbl{bid}"), w=w, bold=True, visible=visible)

    def card(self, layer_name, x, y, w, h, color="#fffdf8", id_=None):
        return self.img(layer_name, "Card", f"c{color[1:].lower()}", x + w / 2, y + h / 2, w=w, h=h, id_=id_)

    def rect(self, layer_name, key, x, y, w, h, id_=None, visible=True):
        """Shape sprite stretched over the rectangle (x,y,w,h) in HTML units (top-left corner)."""
        return self.img(layer_name, "Shape", key, x + w / 2, y + h / 2, w=w, h=h, id_=id_, visible=visible)

    def to_json(self):
        lay = {"name": self.name, "sid": sid(), "nonworld-instances": [], "effectTypes": [],
               "width": 480, "height": 640, "unboundedScrolling": False, "sampling": "auto",
               "ambientLight": 0.03, "vpX": 0.5, "vpY": 0.5, "projection": "perspective",
               "layers": [], "eventSheet": self.sheet}
        layers = []
        layers.append(guide_layer())
        for n in self.order:
            layers.append(self.layers[n])
        lay["layers"] = layers
        return lay

def MAN_SIZE(obj, anim):
    from objects import OBJECTS
    anims, _ = OBJECTS[obj]
    key = dict(anims)[anim]
    e = MAN[key]
    return e["w"], e["h"]
