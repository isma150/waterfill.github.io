"""Garage actions, Shop, Roulette, Settings (HTML: garage buy/equip, shopScreen, rouletteScreen, settingsScreen)."""
from ev import *
from ids import nid
from ev import POS, SIZE
from cfg import PERSIST, WEAPONS, CARS, PRIZES, PERSIST_KEY_PREFIX
from sheet_common import TOAST
from sheet_menus import click, txt_live, BTN
from ids import nid

def with_toast(lname, msg, conds, acts):
    tc, ta = TOAST(lname, msg)
    return list(conds) + tc, list(acts) + ta

def garage_actions():
    ev = [NOTE("Garage actions: equip/buy/upgrade weapons, cars and crew.")]
    # ---- weapons (HTML buyWeapon / equipWeapon)
    wlist = []
    for k, (wid, wname, base, rate, price) in enumerate(WEAPONS):
        sel = [CMPV("gearTab", 0, 0), CMPV("selectedItem", 0, k)]
        if k == 0:
            owned = []
        else:
            owned = [CMPV(f"own_{wid}", 0, 1)]
        upg = f"upg_{wid}"
        cost = f"{price}+{upg}*100"
        # equip when owned and not already equipped
        if k == 0:
            eq = [CMPV("weapon", 1, k)]
        else:
            eq = [CMPV(f"own_{wid}", 0, 1), CMPV("weapon", 1, k)]
        cc, aa = with_toast("gar", f"{wname} equipped!", sel + eq, [SETV("weapon", k), SETV("needSave", 1)])
        wlist.append(click("gar.equip", aa, extra=cc))
        # buy / upgrade
        if k == 0:
            cc, aa = with_toast("gar", f"{wname} upgraded!", sel + [CMPV("coins", 5, cost)],
                                [SETV("coins", f"coins-({cost})"), SETV(upg, f"{upg}+1"), SETV("weapon", k),
                                 SETV("needSave", 1)])
            wlist.append(click("gar.wbuy", aa, extra=cc))
            cc, aa = with_toast("gar", "Not enough coins!", sel + [CMPV("coins", 2, cost)], [])
            wlist.append(click("gar.wbuy", aa, extra=cc))
        else:
            cc, aa = with_toast("gar", f"{wname} upgraded!", sel + owned + [CMPV("coins", 5, cost)],
                                [SETV("coins", f"coins-({cost})"), SETV(upg, f"{upg}+1"), SETV("weapon", k),
                                 SETV("needSave", 1)])
            wlist.append(click("gar.wbuy", aa, extra=cc))
            cc, aa = with_toast("gar", f"{wname} unlocked!", [CMPV("gearTab", 0, 0), CMPV("selectedItem", 0, k),
                                CMPV(f"own_{wid}", 1, 1), CMPV("coins", 5, price)],
                                [SETV("coins", f"coins-{price}"), SETV(f"own_{wid}", 1), SETV("weapon", k),
                                 SETV("needSave", 1)])
            wlist.append(click("gar.wbuy", aa, extra=cc))
            cc, aa = with_toast("gar", "Not enough coins!", sel + [CMPV(f"own_{wid}", 0, 0), CMPV("coins", 2, price)], [])
            wlist.append(click("gar.wbuy", aa, extra=cc))
        cc, aa = with_toast("gar", "Not enough coins!", sel + owned + [CMPV("coins", 2, cost)], [])
        wlist.append(click("gar.wbuy", aa, extra=cc))
    ev.append(G("Weapon buttons", wlist))
    # ---- cars (HTML buyCar / equipCar)
    clist = []
    for c, (cid, cname, hp, price) in enumerate(CARS):
        sel = [CMPV("gearTab", 0, 1), CMPV("selectedItem", 0, c)]
        if c == 0:
            own = []
        else:
            own = [CMPV(f"own_{cid}", 0, 1)]
        if c > 0:
            cc, aa = with_toast("gar", f"{cname} equipped!", sel + own + [CMPV("car", 1, c)],
                                [SETV("car", c), SETV("needSave", 1)])
            clist.append(click("gar.cbuy", aa, extra=cc))
            cc, aa = with_toast("gar", f"{cname} purchased (appearance only)!", sel + [CMPV(f"own_{cid}", 0, 0),
                                CMPV("coins", 5, price)],
                                [SETV("coins", f"coins-{price}"), SETV(f"own_{cid}", 1), SETV("car", c),
                                 SETV("needSave", 1)])
            clist.append(click("gar.cbuy", aa, extra=cc))
            cc, aa = with_toast("gar", "Not enough coins!", sel + [CMPV(f"own_{cid}", 0, 0), CMPV("coins", 2, price)], [])
            clist.append(click("gar.cbuy", aa, extra=cc))
        else:
            cc, aa = with_toast("gar", f"{cname} equipped!", sel + [CMPV("car", 1, 0)], [SETV("car", 0), SETV("needSave", 1)])
            clist.append(click("gar.cbuy", aa, extra=cc))
    ev.append(G("Car buttons", clist))
    # ---- crew (HTML: VISIT SHOP for Driver / Pet when not owned)
    crew_list = [
        click("gar.crew", [SETV("shopTab", 1), SETV("screen", 3), GOTO("Shop")],
              extra=[CMPV("gearTab", 0, 2), CMPV("selectedItem", 0, 1), CMPV("own_speedDriver", 0, 0)]),
        click("gar.crew", [SETV("shopTab", 3), SETV("screen", 3), GOTO("Shop")],
              extra=[CMPV("gearTab", 0, 2), CMPV("selectedItem", 0, 3), CMPV("own_luckyPet", 0, 0)]),
    ]
    ev.append(G("Crew buttons", crew_list))
    return ev

def garage_labels():
    """Labels and button positions that depend on the selected item."""
    ev = []
    # weapon buy button: UPGRADE (right, narrow) when owned and equipped/not, UNLOCK when not owned
    for k, (wid, wname, base, rate, price) in enumerate(WEAPONS):
        sel = [CMPV("gearTab", 0, 0), CMPV("selectedItem", 0, k)]
        cost = f"{price}+upg_{wid}*100"
        if k == 0:
            ev.append(B([TICK(), IV("Txt", "id", 0, nid("gar.wbuylbl")), *sel],
                        [A("set-text", "Txt", text=f'"UPGRADE ◉ " & {cost}')]))
        else:
            ev.append(B([TICK(), IV("Txt", "id", 0, nid("gar.wbuylbl")), *sel, CMPV(f"own_{wid}", 0, 1)],
                        [A("set-text", "Txt", text=f'"UPGRADE ◉ " & {cost}')]))
            ev.append(B([TICK(), IV("Txt", "id", 0, nid("gar.wbuylbl")), *sel, CMPV(f"own_{wid}", 0, 0)],
                        [A("set-text", "Txt", text=f'"UNLOCK ◉ " & {price}')]))
    return ev

def X(e):
    return f"60+({e})*0.857142857"

def Y(e):
    return f"({e})*0.857142857"

def W_(w):
    return f"({w})*0.857142857"

def H_(h):
    return f"({h})*0.857142857"

def garage_detail_events():
    """HTML L322-324: weapon EQUIP/UPGRADE placement, car and crew detail texts and buttons."""
    ev = []
    # weapon: EQUIP shows when owned and not equipped; UPGRADE moves right (269) then; else spans 155..395
    eq_btn, eq_lbl = nid("btn.gar.equip"), nid("lbl" + str(nid("btn.gar.equip")))
    wb, wbl = nid("btn.gar.wbuy"), nid("gar.wbuylbl")
    rows = []
    for k, (wid, wname, base, rate, price) in enumerate(WEAPONS):
        sel = [CMPV("gearTab", 0, 0), CMPV("selectedItem", 0, k)]
        own = [] if k == 0 else [CMPV(f"own_{wid}", 0, 1)]
        equipped = [CMPV("weapon", 0, k)]
        not_equipped = [CMPV("weapon", 1, k)]
        rows.append(B([TICK(), IV("Btn", "id", 0, eq_btn)] + sel + own + not_equipped, [VIS("Btn", True)]))
        rows.append(B([TICK(), IV("Txt", "id", 0, eq_lbl)] + sel + own + not_equipped, [VIS("Txt", True)]))
        rows.append(B([TICK(), IV("Btn", "id", 0, eq_btn)] + sel + equipped, [VIS("Btn", False)]))
        rows.append(B([TICK(), IV("Txt", "id", 0, eq_lbl)] + sel + equipped, [VIS("Txt", False)]))
        if k > 0:
            rows.append(B([TICK(), IV("Btn", "id", 0, eq_btn)] + sel + [CMPV(f"own_{wid}", 0, 0)], [VIS("Btn", False)]))
            rows.append(B([TICK(), IV("Txt", "id", 0, eq_lbl)] + sel + [CMPV(f"own_{wid}", 0, 0)], [VIS("Txt", False)]))
        # upgrade button: right half (x 269, w 126) when owned and not equipped, else full width (155, w 240)
        right = [POS("Btn", X("332"), Y("409.5")), SIZE("Btn", W_(126), H_(39)),
                 POS("Txt", X("332"), Y("410")), SIZE("Txt", W_(126), H_(39))]
        full = [POS("Btn", X("275"), Y("409.5")), SIZE("Btn", W_(240), H_(39)),
                POS("Txt", X("275"), Y("410"))]
        rows.append(B([TICK(), IV("Btn", "id", 0, wb)] + sel + own + not_equipped, [POS("Btn", X("332"), Y("409.5")), SIZE("Btn", W_(126), H_(39))]))
        rows.append(B([TICK(), IV("Txt", "id", 0, wbl)] + sel + own + not_equipped, [POS("Txt", X("332"), Y("410"))]))
        rows.append(B([TICK(), IV("Btn", "id", 0, wb)] + sel + equipped, [POS("Btn", X("275"), Y("409.5")), SIZE("Btn", W_(240), H_(39))]))
        rows.append(B([TICK(), IV("Txt", "id", 0, wbl)] + sel + equipped, [POS("Txt", X("275"), Y("410"))]))
        if k > 0:
            rows.append(B([TICK(), IV("Btn", "id", 0, wb)] + sel + [CMPV(f"own_{wid}", 0, 0)], [POS("Btn", X("275"), Y("409.5")), SIZE("Btn", W_(240), H_(39))]))
            rows.append(B([TICK(), IV("Txt", "id", 0, wbl)] + sel + [CMPV(f"own_{wid}", 0, 0)], [POS("Txt", X("275"), Y("410"))]))
    ev.append(G("Weapon equip and upgrade placement", rows))
    # car detail (HTML L323): preview, name, EQUIP / EQUIPPED / BUY label
    cars = []
    for c, (cid, cname, hp, price) in enumerate(CARS):
        sel = [CMPV("gearTab", 0, 1), CMPV("selectedItem", 0, c)]
        cars.append(B([TICK(), IV("Taxi", "id", 0, nid("gar.cprev"))] + sel, [ANIM("Taxi", cid)]))
        cars.append(txt_live("gar.cname", f'"{cname}"', sel))
        if c == 0:
            cars.append(txt_live("gar.cbuylbl", '"EQUIPPED ✓"', sel + [CMPV("car", 0, 0)]))
            cars.append(txt_live("gar.cbuylbl", '"EQUIP ✓"', sel + [CMPV("car", 1, 0)]))
        else:
            own = f"own_{cid}"
            cars.append(txt_live("gar.cbuylbl", '"EQUIPPED ✓"', sel + [CMPV(own, 1, 0), CMPV("car", 0, c)]))
            cars.append(txt_live("gar.cbuylbl", '"EQUIP ✓"', sel + [CMPV(own, 1, 0), CMPV("car", 1, c)]))
            cars.append(txt_live("gar.cbuylbl", f'"BUY ◉ {price}"', sel + [CMPV(own, 0, 0)]))
    ev.append(G("Car detail", cars))
    # crew detail (HTML L324): names, descriptions and the button label
    crew = [("1 Block", "Inactive in one-hit dynamite mode"), ("Speed Driver", "+25% steering speed"),
            ("Medic Cat", "Disabled: dynamite is lethal"), ("Lucky Pet", "+20% cash rewards")]
    crew_rows = []
    for k, (nm, ds) in enumerate(crew):
        sel = [CMPV("gearTab", 0, 2), CMPV("selectedItem", 0, k)]
        crew_rows.append(txt_live("gar.crname", f'"{nm}"', sel))
        crew_rows.append(txt_live("gar.crdesc", f'"{ds}"', sel))
    own_map = {1: "own_speedDriver", 3: "own_luckyPet"}
    crew_rows.append(txt_live("gar.crlbl", '"DISABLED · ONE HIT MODE"', [CMPV("gearTab", 0, 2), CMPV("selectedItem", 0, 0)]))
    crew_rows.append(txt_live("gar.crlbl", '"DISABLED · ONE HIT MODE"', [CMPV("gearTab", 0, 2), CMPV("selectedItem", 0, 2)]))
    for k, var in own_map.items():
        sel = [CMPV("gearTab", 0, 2), CMPV("selectedItem", 0, k)]
        crew_rows.append(txt_live("gar.crlbl", '"EQUIPPED ✓"', sel + [CMPV(var, 1, 0)]))
        crew_rows.append(txt_live("gar.crlbl", '"VISIT SHOP →"', sel + [CMPV(var, 0, 0)]))
    ev.append(G("Crew detail", crew_rows))
    return ev
