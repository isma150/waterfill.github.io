"""Checks identifiers used inside expression strings of the built sheets.
Allowed: globals (top-level variables), instance variables of the objects referenced by the same event (and their
Object.var forms), functions and constants. Quoted strings are ignored."""
import json, os, re, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else "check9"
FUNCS = {"min", "max", "abs", "floor", "ceil", "round", "clamp", "pow", "sin", "cos", "exp", "random", "dt",
         "ln", "sqrt", "int", "tan", "atan2", "atan", "lerp", "mod", "hypot", "log", "pi", "e", "true", "false",
         "and", "or", "not", "Touch", "X", "Y", "Count", "ItemValue", "LocalStorage", "Keyboard", "Enemy", "Boss",
         "Shot", "Pickup", "Warn", "Fx", "Taxi", "Shape", "Txt", "Btn", "Card", "Node", "Icon", "Wheel", "Cloud", "Logo",
         "Speed", "Bg", "Audio", "Needle", "Roulette", "Card", "Taxi"}
objs_ivars = {}
for f in os.listdir(os.path.join(ROOT, "objectTypes")):
    if f.endswith(".json") and not f.startswith("UI"):
        d = json.load(open(os.path.join(ROOT, "objectTypes", f), encoding="utf-8"))
        if isinstance(d, dict) and "name" in d:
            objs_ivars[d["name"]] = {v["name"] for v in d.get("instanceVariables", [])}
home = json.load(open(os.path.join(ROOT, "eventSheets", "Event Home.json"), encoding="utf-8"))
globals_ = {e["name"] for e in home["events"] if e.get("eventType") == "variable"}
TOK = re.compile(r'"[^"]*"|[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)?|\d+\.?\d*')
problems = {}
def check_expr(expr, objs, where):
    s = re.sub(r'"[^"]*"', '""', expr)
    for tok in TOK.findall(s):
        if tok.startswith('"') or tok[0].isdigit():
            continue
        if "." in tok:
            a, b = tok.split(".", 1)
            if a in objs_ivars and b in objs_ivars[a]:
                continue
            if a in objs_ivars or a in FUNCS or a in ("Touch", "LocalStorage", "Keyboard"):
                continue
            if a in globals_ or a in ("Enemy", "Boss"):
                continue
            problems.setdefault(tok, set()).add(where)
            continue
        if tok in globals_ or tok in FUNCS or tok in objs_ivars:
            continue
        if any(tok in objs_ivars.get(o, set()) for o in objs):
            continue
        problems.setdefault(tok, set()).add(where)
def walk(evs, sheet, inherited_objs=()):
    for e in evs:
        if e.get("eventType") == "block":
            objs = set(inherited_objs)
            for c in e.get("conditions", []) + e.get("actions", []):
                oc = c.get("objectClass")
                if oc and oc != "System":
                    objs.add(oc)
            for c in e.get("conditions", []) + e.get("actions", []):
                for k, v in (c.get("parameters") or {}).items():
                    if isinstance(v, str):
                        check_expr(v, objs, f"{sheet}:{c['id']}.{k}")
            walk(e.get("children", []), sheet, objs)
        elif e.get("eventType") == "group":
            walk(e.get("children", []), sheet)
for f in sorted(os.listdir(os.path.join(ROOT, "eventSheets"))):
    if f.endswith(".json") and "uistate" not in f:
        d = json.load(open(os.path.join(ROOT, "eventSheets", f), encoding="utf-8"))
        walk(d["events"], f)
print("unknown identifiers:", len(problems))
for k in sorted(problems)[:80]:
    print(f"  {k:24s} {sorted(problems[k])[:2]}")

# instance variables named in conditions/actions must exist on the object type
iv_problems = {}
def walk_iv(evs, sheet):
    for e in evs:
        if e.get("eventType") == "block":
            for c in e.get("conditions", []) + e.get("actions", []):
                oc = c.get("objectClass")
                params = c.get("parameters") or {}
                if oc in objs_ivars and c["id"] in ("compare-instance-variable", "set-instvar-value"):
                    v = params.get("variable")
                    if v and v not in objs_ivars[oc]:
                        iv_problems.setdefault((oc, v), set()).add(sheet)
            walk_iv(e.get("children", []), sheet)
        elif e.get("eventType") == "group":
            walk_iv(e.get("children", []), sheet)
for f in sorted(os.listdir(os.path.join(ROOT, "eventSheets"))):
    if f.endswith(".json") and "uistate" not in f:
        d = json.load(open(os.path.join(ROOT, "eventSheets", f), encoding="utf-8"))
        walk_iv(d["events"], f)
print("undeclared instance variables:", len(iv_problems))
for k in sorted(iv_problems)[:40]:
    print("  ", k, sorted(iv_problems[k])[:2])
