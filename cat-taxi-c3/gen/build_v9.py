"""Assembles the Construct 3 project (.c3p) for the v9 port from the generator modules."""
import copy, json, os, re, shutil, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ev import sid, USED, VAR, CMPV, SETV, TICK, B
from cfg import PERSIST, RUNTIME
from ids import all_ids, nid
import objects
from layouts_menu import build_home, build_map, build_results, build_garage, build_shop, build_roulette, build_settings
from layout_game import build_game
import sheet_menus, sheet_menus2, sheet_menus3, sheet_menus4, sheet_game1, sheet_game2, sheet_game3, sheet_game4, sheet_game5, sheet_game6, sheet_game7
from sheet_common import common
from ev import G, NOTE

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "template")
OUT = os.path.join(BASE, "c3build9")
OUT_C3P = os.path.join(BASE, "CatTaxi_v9_port.c3p")

def _event_vars(evs, out):
    for e in evs:
        if e.get("eventType") == "block":
            for c in e.get("conditions", []) + e.get("actions", []):
                if c["id"] in ("set-eventvar-value", "compare-eventvar"):
                    name = c["parameters"]["variable"]
                    if "." not in name:
                        out.add(name)
        if e.get("children"):
            _event_vars(e["children"], out)
        if e.get("eventType") == "group":
            _event_vars(e.get("children", []), out)

def globals_sheet():
    """Every event variable is declared here: the declared lists plus any name the events use (logged)."""
    vars_, seen = [], set()
    for n, init in RUNTIME + PERSIST:
        if n not in seen:
            seen.add(n)
            vars_.append(VAR(n, init))
    used = set()
    for build, sheet_name, sheet_fn in LAYOUTS:
        evs = sheet_menus.home_sheet_events() if sheet_fn is sheet_home else sheet_fn()
        _event_vars(evs, used)
    missing = sorted(used - seen)
    for n in missing:
        seen.add(n)
        vars_.append(VAR(n, 0))
    print("auto-declared event variables:", missing)
    return vars_

def sheet_home():
    return [NOTE("Event Home: global variables (top level = global, as in the template) and the Home screen.")] + \
        globals_sheet() + sheet_menus.home_sheet_events()

def sheet_game():
    ev = [NOTE("Event Game: run start, timeline, enemies, shots, pickups, targeting, shooting, auto-pilot.")]
    ev += common("game")
    ev += sheet_game1.start_events()
    ev += sheet_game1.player_move_events()
    ev += sheet_game1.timers_events()
    ev += sheet_game1.wave_setup_events()
    ev += sheet_game1.quota_events() if hasattr(sheet_game1, "quota_events") else []
    ev += sheet_game1.boss_spawn_events()
    ev += sheet_game2.spawn_events()
    ev += sheet_game2.boss_spawn_events()
    ev += sheet_game2.enemy_ai_events()
    ev += sheet_game2.boss_ai_events()
    ev += sheet_game1.wave_end_events()
    ev += sheet_game1.tunnel_events()
    ev += sheet_game4.reset_events()
    ev += sheet_game4.target_events()
    ev += sheet_game4.weapon_events()
    ev += sheet_game3.dynamite_events()
    ev += sheet_game3.shot_events()
    ev += sheet_game3.pickup_events()
    ev += sheet_game3.kill_events()
    ev += sheet_game4.shoot_events()
    ev += sheet_game4.auto_events()
    ev += sheet_game4.lock_events()
    ev += sheet_game1.victory_defeat_events()
    ev += sheet_game1.pause_exit_events()
    ev += sheet_game5.guide_events()
    ev += sheet_game5.guide_events2()
    ev += sheet_game6.taxi_events()
    ev += sheet_game6.enemy_visual_events()
    ev += sheet_game6.speed_events()
    ev += sheet_game6.hud_events()
    ev += sheet_game7.buttons_events()
    ev += sheet_game7.tunnel_and_guide_events()
    ev += sheet_game7.theme_events()
    ev += sheet_game7.pause_defeat_text_events()
    from sheet_common import TOAST
    c, a = TOAST("game", "TUTORIAL EN PARTIDA · CONDUCE TÚ", 2.5)
    ev.append(B([TICK(), CMPV("pendingToast", 4, 0)] + c, a + [SETV("pendingToast", 0)]))
    c, a = TOAST("game", "MODO MANUAL · ARRASTRA PARA CONDUCIR", 2.2)
    ev.append(B([TICK(), CMPV("startToast", 0, 1)] + c, a + [SETV("startToast", 0)]))
    return ev

def sheet_results():
    return sheet_menus.results_sheet_events()

def sheet_map():
    return sheet_menus.map_sheet_events()

def sheet_garage():
    return (sheet_menus.garage_sheet_events() + sheet_menus2.garage_actions() + sheet_menus2.garage_labels()
            + sheet_menus2.garage_detail_events())

def sheet_roulette():
    return sheet_menus3.roulette_sheet_events()

def sheet_shop():
    return sheet_menus4.shop_sheet_events()

def sheet_settings():
    return sheet_menus4.settings_sheet_events()

LAYOUTS = [(build_home, "Event Home", sheet_home), (build_map, "Event Map", sheet_map),
           (build_garage, "Event Garage", sheet_garage), (build_shop, "Event Shop", sheet_shop),
           (build_roulette, "Event Roulette", sheet_roulette), (build_settings, "Event Settings", sheet_settings),
           (build_game, "Event Game", sheet_game), (build_results, "Event Results", sheet_results)]

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(TPL, OUT)
    # remove template layouts, sheets and UI state (flat files named with backslashes)
    for rel in list(os.listdir(OUT)):
        p = os.path.join(OUT, rel)
        if rel.endswith(".uistate.json") or rel.startswith("layouts\\") or rel.startswith("eventSheets\\"):
            if os.path.isfile(p):
                os.remove(p)
    for d in ["images", "layouts", "eventSheets", "objectTypes"]:
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    obj_names = objects.write_objects(OUT, os.path.join(OUT, "objectTypes"))
    layout_names, sheet_names = [], []
    for build, sheet_name, sheet_fn in LAYOUTS:
        L = build()
        ev = sheet_fn()
        sh = {"name": sheet_name, "events": ev, "sid": sid()}
        with open(os.path.join(OUT, "eventSheets", f"{sheet_name}.json"), "w", encoding="utf-8") as fh:
            json.dump(sh, fh, indent=1, ensure_ascii=False)
        with open(os.path.join(OUT, "layouts", f"{L.name}.json"), "w", encoding="utf-8") as fh:
            json.dump(L.to_json(), fh, indent=1, ensure_ascii=False)
        layout_names.append(L.name)
        sheet_names.append(sheet_name)
    pj = json.load(open(os.path.join(OUT, "project.c3proj"), encoding="utf-8"))
    pj["name"] = "Cat Taxi v9 (Construct port)"
    pj["objectTypes"]["items"] = pj["objectTypes"]["items"] + [n for n in obj_names if n not in pj["objectTypes"]["items"]]
    pj["layouts"] = {"items": layout_names, "subfolders": []}
    pj["eventSheets"] = {"items": sheet_names, "subfolders": []}
    pj["firstLayout"] = "Home"
    ids = {"Text", "Keyboard"}
    have = {a["id"] for a in pj["usedAddons"]}
    for pid in sorted(ids):
        if pid not in have:
            pj["usedAddons"].append({"type": "plugin", "id": pid, "name": pid, "author": "Scirra", "bundled": False})
    with open(os.path.join(OUT, "project.c3proj"), "w", encoding="utf-8") as fh:
        json.dump(pj, fh, indent=1, ensure_ascii=False)
    if os.path.exists(OUT_C3P):
        os.remove(OUT_C3P)
    with zipfile.ZipFile(OUT_C3P, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(OUT):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, OUT).replace("/", "\\")
                z.write(full, rel)
    dump = {f"{k[0]}|{k[1]}|{k[2]}": sorted(v) for k, v in USED.items()}
    json.dump(dump, open(os.path.join(BASE, "used_aces.json"), "w"), indent=1, ensure_ascii=False)
    print("written", OUT_C3P, "layouts", layout_names, "sheets", len(sheet_names), "aces", len(dump))

if __name__ == "__main__":
    main()
