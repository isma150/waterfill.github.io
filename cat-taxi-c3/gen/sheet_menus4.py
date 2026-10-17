"""Shop and Settings sheets (HTML: shopScreen L334-337, buyCar/buyCrew L331-332, settingsScreen L351)."""
from ev import *
from ids import nid
from cfg import PERSIST, CARS
from sheet_common import common, TOAST
from sheet_menus import click, txt_live
from sheet_menus3 import popup_events

# shop items per tab: list of slots. kind: car / crew / locked
ITEMS = {
    0: [dict(name="Blue Roadster", detail="Cosmetic variant; 1-hit dynamite", kind="car", car=1, cost=40000, cur="coin", own="own_blue", pic="blue"),
        dict(name="Mint Racer", detail="Cosmetic variant; 1-hit dynamite", kind="car", car=2, cost=90000, cur="coin", own="own_mint", pic="mint"),
        dict(name="Engine Boost", detail="Disabled: HP has no effect", kind="locked", star=True)],
    1: [dict(name="Speed Driver", detail="Steering speed +25%", kind="crew", cost=90, cur="gem", own="own_speedDriver")],
    2: [dict(name="Medic Cat", detail="Disabled: dynamite is lethal", kind="locked", cat=True)],
    3: [dict(name="Lucky Pet", detail="+20% coins from destroyed cars", kind="crew", cost=40, cur="gem", own="own_luckyPet")],
    4: [dict(name="Shield Charge", detail="Disabled: dynamite is lethal", kind="locked", star=True),
        dict(name="Bank Reward", detail="Earn coins by escaping!", kind="locked", star=True)],
}
SLOTS = {0: 3, 1: 1, 2: 1, 3: 1, 4: 2}

def shop_sheet_events():
    ev = [NOTE("Shop: tabs, item slots (one layer per slot), buy and equip rules of the HTML.")]
    ev += common("shop")
    ev.append(G("Tabs", [click(f"shop.tab{i}", [SETV("shopTab", i)]) for i in range(5)]))
    ev.append(G("Tab colours", [
        B([TICK(), IV("Btn", "id", 0, nid(f"btn.shop.tab{i}")), CMPV("shopTab", 0, i)], [ANIM("Btn", "cfff0aa")])
        for i in range(5)] + [
        B([TICK(), IV("Btn", "id", 0, nid(f"btn.shop.tab{i}")), CMPV("shopTab", 1, i)], [ANIM("Btn", "cf5f1e9")])
        for i in range(5)]))
    # slot layers: slot s is visible when the tab has more than s items
    vis = []
    for t, n in SLOTS.items():
        acts = [LAYER_VIS(f"Slot{s}", s < n) for s in range(3)]
        vis.append(B([TICK(), CMPV("shopTab", 0, t)], acts))
    ev.append(G("Slot layers", vis))
    # texts, pictures and buttons per tab/slot
    texts = []
    for t in range(5):
        for s in range(3):
            if s >= SLOTS[t]:
                continue
            it = ITEMS[t][s]
            cond = [CMPV("shopTab", 0, t)]
            prev_vis = it["kind"] == "car"               # HTML: car preview when the item has a car
            cat_vis = it["kind"] in ("crew", "locked") and t in (1, 2, 3)
            texts.append(B([TICK(), IV("Taxi", "id", 0, nid(f"shop.prev{s}"))] + cond, [VIS("Taxi", prev_vis)]))
            texts.append(B([TICK(), IV("Icon", "id", 0, nid(f"shop.cat{s}"))] + cond, [VIS("Icon", cat_vis)]))
            texts.append(txt_live(f"shop.name{s}", f'"{it["name"]}"', cond))
            texts.append(txt_live(f"shop.detail{s}", f'"{it["detail"]}"', cond))
            star = it.get("star") or (t == 0 and s == 2)
            texts.append(txt_live(f"shop.star{s}", '"✦"' if star else '""', cond))
            if it["kind"] == "car":
                own = [CMPV(it["own"], 1, 0)]
                texts.append(B([TICK(), IV("Txt", "id", 0, nid(f"shop.lbl{s}"))] + cond + [CMPV(it["own"], 0, 0)],
                               [A("set-text", "Txt", text=f'"BUY ¢ {it["cost"]}"')]))
                texts.append(B([TICK(), IV("Txt", "id", 0, nid(f"shop.lbl{s}"))] + cond + own,
                               [A("set-text", "Txt", text='"EQUIP"')]))
            elif it["kind"] == "crew":
                texts.append(B([TICK(), IV("Txt", "id", 0, nid(f"shop.lbl{s}"))] + cond + [CMPV(it["own"], 0, 0)],
                               [A("set-text", "Txt", text=f'"BUY ◆ {it["cost"]}"')]))
                texts.append(B([TICK(), IV("Txt", "id", 0, nid(f"shop.lbl{s}"))] + cond + [CMPV(it["own"], 1, 0)],
                               [A("set-text", "Txt", text='"OWNED ✓"')]))
            else:
                texts.append(txt_live(f"shop.lbl{s}", '"COMING SOON"', cond))
    ev.append(G("Shop item texts", texts))
    # buy and equip
    buys = []
    for t, items in ITEMS.items():
        for s, it in enumerate(items):
            cond = [CMPV("shopTab", 0, t)]
            if it["kind"] == "car":
                for conds, acts in _car_click(it["car"], it, cond, it["own"]):
                    buys.append(click(f"shop.item{s}", acts, extra=conds))
            elif it["kind"] == "crew":
                for conds, acts in _crew_click(it, cond):
                    buys.append(click(f"shop.item{s}", acts, extra=conds))
    ev.append(G("Shop buttons", buys))
    ev.append(G("Back", [
        click("shop.back", [SETV("screen", 2), GOTO("Garage")]),
        click("shop.bankmap", [SETV("screen", 1), GOTO("Map")]),
    ]))
    return ev

def _car_click(c, it, cond, own):
    cname = it["name"]
    cid = ["taxi", "blue", "mint"][c]
    cc1, aa1 = TOAST("shop", "Car equipped!")
    cc2, aa2 = TOAST("shop", f"{cname} purchased (appearance only)!")
    cc3, aa3 = TOAST("shop", "Not enough coins!")
    owned = [CMPV(own, 1, 0)]
    return (list(cond) + owned + cc1, [SETV("car", c), SETV("needSave", 1)] + aa1), \
           (list(cond) + [CMPV(own, 0, 0), CMPV("coins", 5, it["cost"])] + cc2,
            [SETV("coins", f"coins-{it['cost']}"), SETV(own, 1), SETV("car", c), SETV("needSave", 1)] + aa2), \
           (list(cond) + [CMPV(own, 0, 0), CMPV("coins", 2, it["cost"])] + cc3, aa3)

def _crew_click(it, cond):
    cname = it["name"]
    own = it["own"]
    cc1, aa1 = TOAST("shop", "Crew already equipped!")
    cc2, aa2 = TOAST("shop", f"{cname} equipped!")
    cc3, aa3 = TOAST("shop", "Not enough gems!")
    return (list(cond) + [CMPV(own, 1, 0)] + cc1, aa1), \
           (list(cond) + [CMPV(own, 0, 0), CMPV("gems", 5, it["cost"])] + cc2,
            [SETV("gems", f"gems-{it['cost']}"), SETV(own, 1), SETV("needSave", 1)] + aa2), \
           (list(cond) + [CMPV(own, 0, 0), CMPV("gems", 2, it["cost"])] + cc3, aa3)

def settings_sheet_events():
    ev = [NOTE("Settings: sound, reduced motion, replay tutorial, reset (with confirmation popup).")]
    ev += common("set")
    ev += popup_events("set")
    ev.append(G("Labels", [
        txt_live("set.soundlbl", '"SOUND: ON"', [CMPV("sound", 0, 1)]),
        txt_live("set.soundlbl", '"SOUND: OFF"', [CMPV("sound", 0, 0)]),
        txt_live("set.motionlbl", '"REDUCED MOTION: ON"', [CMPV("reducedMotion", 0, 1)]),
        txt_live("set.motionlbl", '"REDUCED MOTION: OFF"', [CMPV("reducedMotion", 0, 0)]),
    ]))
    ev.append(G("Buttons", [
        click("set.sound", [SETV("sound", "1-sound"), SETV("needSave", 1)], extra=[]),
        click("set.motion", [SETV("reducedMotion", "1-reducedMotion"), SETV("needSave", 1)]),
        click("set.tutorial", [SETV("startReq", 1), SETV("startGuide", 1), SETV("startBank", 0),
                               SETV("pendingToast", 2), SETV("screen", 5), GOTO("Game")]),
        click("set.back", [SETV("screen", 2), GOTO("Garage")]),
        click("set.reset", [SETV("popupOpen", 1), SETV("popupConfirm", 1), SETV("popTitle", 4), SETV("popMsg", 5),
                            SETV("popKind", 4)]),
        click("set.cancel", [SETV("popupOpen", 0), SETV("popupConfirm", 0)], popup_gate=False,
              extra=[CMPV("popupConfirm", 0, 1)]),
        click("set.popreset", [SETV("needSave", 1), SETV("popupOpen", 0), SETV("popupConfirm", 0), SETV("screen", 0),
                               GOTO("Home")] + [SETV(n, v) for n, v in PERSIST], popup_gate=False,
              extra=[CMPV("popupConfirm", 0, 1)]),
    ]))
    return ev
