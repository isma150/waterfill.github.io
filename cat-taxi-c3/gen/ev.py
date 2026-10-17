"""Event-sheet helpers. Every ACE id used here is recorded in USED so the ledger can list it.
Ids marked VERIFIED were seen in the template, chef, c3source or liauw sources; the rest are UNVERIFIED."""
import random

_rng = random.Random(20261017)
_used_sids = set()

def sid():
    while True:
        v = _rng.randint(10**14, 10**15 - 1)
        if v not in _used_sids:
            _used_sids.add(v)
            return v

USED = {}  # (kind, objectClass, id) -> set of param keys

def _rec(kind, obj, aid, params):
    USED.setdefault((kind, obj, aid), set()).update(params.keys())

def C(cid, obj="System", **params):
    _rec("condition", obj, cid, params)
    return {"id": cid, "objectClass": obj, "sid": sid(), **({"parameters": params} if params else {})}

def A(aid, obj="System", **params):
    _rec("action", obj, aid, params)
    return {"id": aid, "objectClass": obj, "sid": sid(), **({"parameters": params} if params else {})}

def _fresh(o):
    """Copy of an event item with a new sid on every dict that has one. Conditions and actions are often reused
    (gate(), idc lists) in several events; C3 needs each sid to appear once, so reused items are copied here."""
    if isinstance(o, dict):
        n = {k: _fresh(v) for k, v in o.items()}
        if "sid" in n:
            n["sid"] = sid()
        return n
    if isinstance(o, list):
        return [_fresh(x) for x in o]
    return o

def B(conds, acts, children=None):
    e = {"eventType": "block", "conditions": [_fresh(c) for c in conds], "actions": [_fresh(a) for a in acts],
         "sid": sid()}
    if children:
        e["children"] = [_fresh(c) for c in children]
    return e

def G(title, children, active=True):
    return {"eventType": "group", "disabled": False, "title": title, "description": title,
            "isActiveOnStart": active, "children": [_fresh(c) for c in children], "sid": sid()}

def NOTE(text):
    return {"eventType": "comment", "text": text, "text-color": [0, 0, 0, 0], "background-color": [1, 1, 1, 1]}

def VAR(name, init="0"):
    return {"eventType": "variable", "name": name, "type": "number", "initialValue": str(init),
            "comment": "", "isStatic": False, "isConstant": False, "sid": sid()}

# ---- common ACEs
def TICK():
    return C("every-tick")

def START():
    return C("on-start-of-layout")

def SETV(var, expr):
    return A("set-eventvar-value", variable=var, value=str(expr))

def CMPV(var, comp, value):
    """Compare a global number. comp: 0 eq, 1 ne, 2 lt, 3 le, 4 gt, 5 ge (c3source / chef confirmed).
    An object expression such as Enemy.Count is compared with 'Compare two values' (chef: comparison codes 0..5)."""
    if "." in var:
        return C("compare-two-values", "System", **{"first-value": var, "comparison": comp, "second-value": str(value)})
    return C("compare-eventvar", variable=var, comparison=comp, value=str(value))

def CMPX(expr, comp, value):
    """Compare an expression with a value (compare two values; expressions may use globals and object expressions)."""
    return C("compare-two-values", "System", **{"first-value": str(expr), "comparison": comp, "second-value": str(value)})

def IV(obj, var, comp, value):
    """Compare an instance variable of obj (liauw: compare-instance-variable comparison/value/variable)."""
    return C("compare-instance-variable", obj, variable=var, comparison=comp, value=str(value))

def SIV(obj, var, expr):
    """Set an instance variable of picked obj instances (ACE id from liauw sources; param keys assumed)."""
    return A("set-instvar-value", obj, variable=var, value=str(expr))

def POS(obj, x, y):
    return A("set-position", obj, x=str(x), y=str(y))

def SIZE(obj, w, h):
    return A("set-size", obj, width=str(w), height=str(h))

def ANIM(obj, name):
    return A("set-animation", obj, animation=f'"{name}"')

def VIS(obj, flag):
    """chef gotcha 26: visibility is the enum 'visible' / 'invisible' (Sprite param name assumed: visibility)."""
    return A("set-visible", obj, visibility=("visible" if flag else "invisible"))

def ANGLE(obj, expr):
    return A("set-angle", obj, angle=str(expr))

def TEXT(obj, expr):
    return A("set-text", obj, text=str(expr))

def CREATE(obj, layer, x, y):
    return A("create-object", "System", **{"object-to-create": obj, "layer": f'"{layer}"', "template-name": '"default"',
                                           "create-hierarchy": True, "x": str(x), "y": str(y)})

def DESTROY(obj):
    return A("destroy", obj)

def GOTO(layout):
    return A("go-to-layout", "System", layout=layout)

def LAYER_VIS(layer, flag):
    """chef gotcha 25/26: layer name quoted, visibility 'visible' / 'invisible'."""
    return A("set-layer-visible", "System", layer=f'"{layer}"', visibility=("visible" if flag else "invisible"))

def TOUCH(obj, kind="start"):
    return C("on-touched-object", "Touch", object=obj, type=kind)

def OVERLAP(obj, other):
    return C("is-overlapping-another-object", obj, object=other)

def PICK_LOWEST(obj, var):
    """UNVERIFIED id: manual section 'Pick highest/lowest'. Keeps only the instance with the lowest instance variable."""
    return C("pick-lowest-instvar", obj, variable=var)

def PICK_HIGHEST(obj, var):
    return C("pick-highest-instvar", obj, variable=var)

def PLAY(tag, sound="", loop=False):
    return A("play", "Audio", tag=f'"{tag}"', file=f'"{sound}"', looping=("1" if loop else "0"))

def STOP_ALL():
    return A("stop-all", "Audio")

def WAIT(sec):
    return A("wait", "System", seconds=str(sec), **{"use-timescale": False})
