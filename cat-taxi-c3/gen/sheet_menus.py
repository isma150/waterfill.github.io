"""Menu event sheets: Home, Map, Results, Garage (HTML: homeScreen, drawMap, resultsScreen, garageScreen)."""
from ev import *
from ids import nid
from cfg import PERSIST, BANKS, WEAPONS, CARS, PERSIST_KEY_PREFIX
from sheet_common import common, TOAST, TXT_PICK

def BTN(n):
    return nid("btn." + n)

def click(n, acts, extra=(), popup_gate=True):
    conds = [TOUCH("Btn", "start"), IV("Btn", "id", 0, BTN(n))]
    if popup_gate:
        conds.append(CMPV("popupOpen", 0, 0))
    return B(conds + list(extra), acts)

def txt_set(name, expr, extra=()):
    """Sets text once when the block runs (use inside every-tick for live values)."""
    return B([IV("Txt", "id", 0, nid(name))] + list(extra), [A("set-text", "Txt", text=str(expr))])

def txt_live(name, expr, extra=()):
    return B([TICK(), IV("Txt", "id", 0, nid(name))] + list(extra), [A("set-text", "Txt", text=str(expr))])

def obj_show(objname, oid, flag, extra=()):
    return B([TICK(), IV(objname, "id", 0, oid)] + list(extra), [VIS(objname, flag)])

def key_of(n):
    return f'"{PERSIST_KEY_PREFIX}{n}"'

def load_events():
    gets = [A("get-item", "LocalStorage", key=key_of(n)) for n, _ in PERSIST]
    gots = [B([C("on-item-get", "LocalStorage", key=key_of(n))], [SETV(n, "LocalStorage.ItemValue")]) for n, _ in PERSIST]
    return [G("Load saved data (LocalStorage, once)", [B([START(), CMPV("loadStarted", 0, 0)], [SETV("loadStarted", 1)] + gets)] + gots)]

def home_sheet_events():
    ev = [NOTE("Home: saved data is loaded here once. Globals are declared at the top of this sheet.")]
    ev += load_events()
    ev += common("home")
    ev += [
        G("Buttons", [
            click("home.play", [SETV("screen", 1), GOTO("Map")], extra=[CMPV("seenTutorial", 0, 1)]),
            click("home.play", [SETV("startReq", 1), SETV("startGuide", 1), SETV("startBank", 0), SETV("screen", 5),
                                GOTO("Game")], extra=[CMPV("seenTutorial", 0, 0)]),
            click("home.how", [SETV("startReq", 1), SETV("startGuide", 1), SETV("startBank", 0),
                               SETV("pendingToast", 1), SETV("screen", 5), GOTO("Game")]),
        ]),
        G("Keyboard: Enter on home", [
            B([C("on-key-pressed", "Keyboard", key="13"), CMPV("screen", 0, 0), CMPV("seenTutorial", 0, 1)],
              [SETV("screen", 1), GOTO("Map")]),
            B([C("on-key-pressed", "Keyboard", key="13"), CMPV("screen", 0, 0), CMPV("seenTutorial", 0, 0)],
              [SETV("startReq", 1), SETV("startGuide", 1), SETV("startBank", 0), SETV("screen", 5), GOTO("Game")]),
        ]),
    ]
    return ev

def map_sheet_events():
    ev = [NOTE("Map: nodes, bank card, START, keys.")]
    ev += common("map")
    nodes = []
    for i in range(15):
        nodes.append(B([TOUCH("Node", "start"), IV("Node", "id", 0, nid(f"map.node{i}")), CMPV("unlocked", 5, i)],
                       [SETV("selectedBank", i), SETV("needSave", 1)]))
    ev.append(G("Choose bank", nodes))
    anim = []
    for i in range(15):
        idc = [IV("Node", "id", 0, nid(f"map.node{i}"))]
        anim.append(B([TICK(), *idc, CMPV("unlocked", 2, i)], [ANIM("Node", "locked")]))
        anim.append(B([TICK(), *idc, CMPV("unlocked", 5, i), CMPV("selectedBank", 0, i)], [ANIM("Node", "active")]))
        anim.append(B([TICK(), *idc, CMPV("unlocked", 5, i), CMPV("selectedBank", 1, i)], [ANIM("Node", "normal")]))
    ev.append(G("Node pictures", anim))
    texts = []
    for k, b in enumerate(BANKS):
        texts.append(B([TICK(), IV("Txt", "id", 0, nid("map.bankname")), CMPV("selectedBank", 0, k)],
                       [A("set-text", "Txt", text=f'"{b[0]}"')]))
        texts.append(B([TICK(), IV("Txt", "id", 0, nid("map.level")), CMPV("selectedBank", 0, k)],
                       [A("set-text", "Txt", text=f'"Level : " & bank{k}_lvl')]))
        texts.append(B([TICK(), IV("Txt", "id", 0, nid("map.balance")), CMPV("selectedBank", 0, k)],
                       [A("set-text", "Txt", text=f"bank{k}_bal")]))
    ev.append(G("Bank card text", texts))
    ev.append(G("Buttons", [
        click("map.garage", [SETV("screen", 2), SETV("gearTab", 0), SETV("selectedItem", "weapon"), GOTO("Garage")]),
        click("map.spin", [SETV("spinActive", 0), SETV("screen", 4), GOTO("Roulette")]),
        click("map.shop", [SETV("screen", 3), GOTO("Shop")]),
        click("map.back", [SETV("screen", 0), GOTO("Home")]),
        click("map.start", [SETV("startReq", 1), SETV("startGuide", 0), SETV("startBank", "selectedBank"),
                            SETV("screen", 5), GOTO("Game")]),
    ]))
    ev.append(G("Keys and resources", [
        txt_live("map.keys", '"" & keys & "/4"'),
        txt_live("map.rcoins", "coins"), txt_live("map.rgems", "gems"),
        txt_live("map.rcoins", "coins"),
    ] + [obj_show("Icon", nid(f"map.key{i}"), True) for i in range(0)] + [
        B([TICK(), IV("Icon", "id", 0, nid(f"map.key{i}")), CMPV("keys", 4, i)], [ANIM("Icon", "key_on")]) for i in range(4)
    ] + [
        B([TICK(), IV("Icon", "id", 0, nid(f"map.key{i}")), CMPV("keys", 3, i)], [ANIM("Icon", "key_off")]) for i in range(4)
    ]))
    return ev

def results_sheet_events():
    ev = [NOTE("Results: shows the victory numbers and leads to Roulette, Garage or Map.")]
    ev += common("res")
    ev.append(G("Numbers", [
        txt_live("res.sub", '"WAVE 6   ·   LEVEL " & mLevel'),
        txt_live("res.bank", "mBankLoot"),
        txt_live("res.kill", "mKillLoot"),
        txt_live("res.perfect", "0"),
        txt_live("res.total", "mBankLoot + mKillLoot"),
    ]))
    ev.append(G("Buttons", [
        click("res.spin", [SETV("spinActive", 0), SETV("screen", 4), GOTO("Roulette")]),
        click("res.garage", [SETV("screen", 2), SETV("gearTab", 0), SETV("selectedItem", "weapon"), GOTO("Garage")]),
        click("res.map", [SETV("screen", 1), GOTO("Map")]),
    ]))
    return ev

def garage_sheet_events():
    ev = [NOTE("Garage: tabs, item grid, weapon/car/crew details.")]
    ev += common("gar")
    # tab visibility by layer
    ev.append(G("Tab layers", [
        B([TICK(), CMPV("gearTab", 0, 0)], [LAYER_VIS("GearWeapon", 1), LAYER_VIS("GearCar", 0), LAYER_VIS("GearCrew", 0),
                                            LAYER_VIS("GridWeapon", 1), LAYER_VIS("GridCar", 0), LAYER_VIS("GridCrew", 0)]),
        B([TICK(), CMPV("gearTab", 0, 1)], [LAYER_VIS("GearWeapon", 0), LAYER_VIS("GearCar", 1), LAYER_VIS("GearCrew", 0),
                                            LAYER_VIS("GridWeapon", 0), LAYER_VIS("GridCar", 1), LAYER_VIS("GridCrew", 0)]),
        B([TICK(), CMPV("gearTab", 0, 2)], [LAYER_VIS("GearWeapon", 0), LAYER_VIS("GearCar", 0), LAYER_VIS("GearCrew", 1),
                                            LAYER_VIS("GridWeapon", 0), LAYER_VIS("GridCar", 0), LAYER_VIS("GridCrew", 1)]),
    ]))
    # buttons
    tab_sel = []
    for t in range(3):
        tab_sel.append(B([TICK(), IV("Btn", "id", 0, BTN(f"gar.tab{t}")), CMPV("gearTab", 0, t)],
                         [ANIM("Btn", "cffe8a9")]))
        tab_sel.append(B([TICK(), IV("Btn", "id", 0, BTN(f"gar.tab{t}")), CMPV("gearTab", 1, t)],
                         [ANIM("Btn", "cfffcf7")]))
    ev.append(G("Tab colours", tab_sel))
    ev.append(G("Tabs", [
        click("gar.tab0", [SETV("gearTab", 0), SETV("selectedItem", "weapon")]),
        click("gar.tab1", [SETV("gearTab", 1), SETV("selectedItem", "car")]),
        click("gar.tab2", [SETV("gearTab", 2), SETV("selectedItem", 0)]),
        click("gar.settings", [SETV("prevScreen", 2), SETV("screen", 9), GOTO("Settings")]),
        click("gar.shop", [SETV("screen", 3), GOTO("Shop")]),
        click("gar.next", [SETV("screen", 1), GOTO("Map")]),
    ]))
    # grid cells: select an item of the current tab (counts: weapons 4, cars 3, crew 4)
    counts = {0: 4, 1: 3, 2: 4}
    cells = []
    for i in range(12):
        for t, c in counts.items():
            if i < c:
                cells.append(B([TOUCH("Shape", "start"), IV("Shape", "id", 0, nid(f"gar.cell{i}")),
                                CMPV("gearTab", 0, t)], [SETV("selectedItem", i)]))
    ev.append(G("Choose item", cells))
    shapes = []
    for i in range(12):
        for t, c in counts.items():
            if i < c:
                shapes.append(B([TICK(), IV("Shape", "id", 0, nid(f"gar.cell{i}")), CMPV("gearTab", 0, t),
                                 CMPV("selectedItem", 0, i)], [ANIM("Shape", "cell_sel")]))
                shapes.append(B([TICK(), IV("Shape", "id", 0, nid(f"gar.cell{i}")), CMPV("gearTab", 0, t),
                                 CMPV("selectedItem", 1, i)], [ANIM("Shape", "cell_nor")]))
            else:
                shapes.append(B([TICK(), IV("Shape", "id", 0, nid(f"gar.cell{i}")), CMPV("gearTab", 0, t)],
                                [ANIM("Shape", "cell_emp")]))
    ev.append(G("Cell colours", shapes))
    # lock badges, empty-slot locks and check marks (HTML garage: unowned -> lock, equipped -> check)
    own_var = {0: [None, "own_bomb", "own_shot", "own_machine"], 1: [None, "own_blue", "own_mint"],
               2: [None, "own_speedDriver", "own_medicCat", "own_luckyPet"]}
    equip_var = {0: "weapon", 1: "car", 2: None}
    marks = []
    for t in range(3):
        c = counts[t]
        for i in range(12):
            tc = [CMPV("gearTab", 0, t)]
            idc = lambda obj, nm: [TICK(), IV(obj, "id", 0, nid(nm))]
            if i >= c:   # empty slot: big lock icon in the middle
                marks.append(B(idc("Txt", f"gar.emptylock{i}") + tc, [VIS("Txt", True)]))
                continue
            marks.append(B(idc("Txt", f"gar.emptylock{i}") + tc, [VIS("Txt", False)]))
            v = own_var[t][i] if i < len(own_var[t]) else None
            if v is None:     # always owned (pistol, taxi, block)
                marks.append(B(idc("Txt", f"gar.lock{i}") + tc, [VIS("Txt", False)]))
                marks.append(B(idc("Shape", f"gar.lockbg{i}") + tc, [VIS("Shape", False)]))
            else:
                marks.append(B(idc("Txt", f"gar.lock{i}") + tc + [CMPV(v, 0, 0)], [VIS("Txt", True)]))
                marks.append(B(idc("Txt", f"gar.lock{i}") + tc + [CMPV(v, 1, 0)], [VIS("Txt", False)]))
                marks.append(B(idc("Shape", f"gar.lockbg{i}") + tc + [CMPV(v, 0, 0)], [VIS("Shape", True)]))
                marks.append(B(idc("Shape", f"gar.lockbg{i}") + tc + [CMPV(v, 1, 0)], [VIS("Shape", False)]))
            eq = equip_var[t]
            if eq is None:    # crew never shows a check mark
                marks.append(B(idc("Txt", f"gar.ok{i}") + tc, [VIS("Txt", False)]))
                marks.append(B(idc("Shape", f"gar.okbg{i}") + tc, [VIS("Shape", False)]))
            else:
                owned_ok = [] if v is None else [CMPV(v, 1, 0)]
                marks.append(B(idc("Txt", f"gar.ok{i}") + tc + owned_ok + [CMPV(eq, 0, i)], [VIS("Txt", True)]))
                marks.append(B(idc("Txt", f"gar.ok{i}") + tc + [CMPV(eq, 1, i)], [VIS("Txt", False)]))
                marks.append(B(idc("Shape", f"gar.okbg{i}") + tc + owned_ok + [CMPV(eq, 0, i)], [VIS("Shape", True)]))
                marks.append(B(idc("Shape", f"gar.okbg{i}") + tc + [CMPV(eq, 1, i)], [VIS("Shape", False)]))
    ev.append(G("Lock and check marks", marks))
    # weapon details (gearTab 0): name, power, rate, icon, buttons
    wdet = []
    for k, (wid, wname, base, rate, price) in enumerate(WEAPONS):
        cond = [CMPV("gearTab", 0, 0), CMPV("selectedItem", 0, k)]
        wdet.append(txt_live("gar.wname", f'"{wname}"', cond))
        wdet.append(txt_live("gar.wpower", f'"Power: " & round({base}*(1+upg_{wid}*0.36)*10)/10', cond))
        wdet.append(txt_live("gar.wrate", f'"shoot / 1 sec: {rate:.1f}"', cond))
        wdet.append(A_ICON(k, cond))
    ev.append(G("Weapon details", wdet))
    return ev

def A_ICON(k, cond):
    names = ["wpn_pistol", "wpn_bomb", "wpn_shot", "wpn_machine"]
    return B([TICK(), IV("Icon", "id", 0, nid("gar.wicon"))] + cond, [ANIM("Icon", names[k])])
