"""Project-wide id checks that c3source does not do (run on an extracted build folder).
- every sid is unique in the project (all JSON files)
- every instance uid is unique across layouts and singleton objects
- every object type used by a layout exists, and its plugin-id is listed in project.c3proj usedAddons
- every plugin object without instances (Keyboard, Touch, LocalStorage, Audio) has a singleglobal-inst
Usage: python3 tools/check_ids.py <folder>"""
import collections, glob, json, os, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "check9"
SINGLETON_PLUGINS = {"Keyboard", "Touch", "LocalStorage", "Audio"}
problems = []

def load(p):
    return json.load(open(p, encoding="utf-8"))

def walk(o, fn):
    if isinstance(o, dict):
        for k, v in o.items():
            fn(k, v, o)
            walk(v, fn)
    elif isinstance(o, list):
        for x in o:
            walk(x, fn)

files = [p for p in glob.glob(os.path.join(ROOT, "**", "*.json"), recursive=True) if not p.endswith("uistate.json")]
files += [p for p in glob.glob(os.path.join(ROOT, "*.json")) if not p.endswith("uistate.json") and p not in files]
sids = collections.Counter()
for p in files:
    walk(load(p), lambda k, v, o: sids.update([v]) if k == "sid" and isinstance(v, (int, float)) else None)
for v, n in sids.items():
    if n > 1:
        problems.append(f"duplicate sid {v} x{n}")

uids = collections.Counter()
for p in glob.glob(os.path.join(ROOT, "layouts", "*.json")):
    walk(load(p), lambda k, v, o: uids.update([o["uid"]]) if k == "type" and isinstance(v, str) and "uid" in o else None)
objtypes = {}
for p in glob.glob(os.path.join(ROOT, "objectTypes", "**", "*.json"), recursive=True):
    d = load(p)
    objtypes[d["name"]] = d
    if "singleglobal-inst" in d:
        uids.update([d["singleglobal-inst"]["uid"]])
    if d.get("plugin-id") in SINGLETON_PLUGINS and "singleglobal-inst" not in d:
        problems.append(f"plugin object {d['name']} has no singleglobal-inst")
for u, n in uids.items():
    if n > 1:
        problems.append(f"duplicate uid {u} x{n} (layouts and singletons)")

proj = load(os.path.join(ROOT, "project.c3proj"))
addons = {a["id"] for a in proj.get("usedAddons", [])}
for name, d in objtypes.items():
    pid = d.get("plugin-id")
    if pid not in addons:
        problems.append(f"object {name} uses plugin {pid} not listed in usedAddons")
for p in glob.glob(os.path.join(ROOT, "layouts", "*.json")):
    def chk(k, v, o):
        if k == "type" and isinstance(v, str) and "uid" in o and v not in objtypes:
            problems.append(f"{os.path.basename(p)}: instance of unknown object type {v}")
    walk(load(p), chk)

print("sids:", len(sids), "uids:", len(uids), "object types:", len(objtypes))
print("problems:", len(problems))
for m in problems[:40]:
    print("  ", m)
sys.exit(1 if problems else 0)
