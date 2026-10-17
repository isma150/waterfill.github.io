"""Shop, Roulette and Settings sheets plus the shared popup (HTML: shopScreen, rouletteScreen, settingsScreen, drawPopup)."""
from ev import *
from ids import nid
from cfg import PERSIST, WEAPONS, CARS, PRIZES
from sheet_common import TOAST
from sheet_menus import click, txt_live, BTN, obj_show

TAU = "6.283185307"

def popup_events(lname):
    """Popup of the layout lname (rou or set): visibility, texts and the NICE button."""
    """Popup layer visibility and texts. Codes: popTitle 1 YOU WON / 2 NEW WEAPON / 3 BONUS / 4 RESET PROGRESS?;
    popMsg 1 '+n COINS' / 2 '+n GEM' / 3 weapon unlocked (popAmount = weapon index 1..3) / 4 warning text;
    popKind 1 coin / 2 gem / 3 gun / 4 warn."""
    ev = [G("Popup visibility", [
        B([TICK(), CMPV("popupOpen", 0, 1)], [LAYER_VIS("Popup", 1)]),
        B([TICK(), CMPV("popupOpen", 0, 0)], [LAYER_VIS("Popup", 0), LAYER_VIS("PopCoin", 0), LAYER_VIS("PopGem", 0),
                                              LAYER_VIS("PopGun", 0), LAYER_VIS("PopWarn", 0),
                                              LAYER_VIS("PopNice", 1), LAYER_VIS("PopConfirm", 0)]),
        B([TICK(), CMPV("popupOpen", 0, 1), CMPV("popKind", 0, 1)], [LAYER_VIS("PopCoin", 1), LAYER_VIS("PopGem", 0),
                                                                     LAYER_VIS("PopGun", 0), LAYER_VIS("PopWarn", 0)]),
        B([TICK(), CMPV("popupOpen", 0, 1), CMPV("popKind", 0, 2)], [LAYER_VIS("PopCoin", 0), LAYER_VIS("PopGem", 1),
                                                                     LAYER_VIS("PopGun", 0), LAYER_VIS("PopWarn", 0)]),
        B([TICK(), CMPV("popupOpen", 0, 1), CMPV("popKind", 0, 3)], [LAYER_VIS("PopCoin", 0), LAYER_VIS("PopGem", 0),
                                                                     LAYER_VIS("PopGun", 1), LAYER_VIS("PopWarn", 0)]),
        B([TICK(), CMPV("popupOpen", 0, 1), CMPV("popKind", 0, 4)], [LAYER_VIS("PopCoin", 0), LAYER_VIS("PopGem", 0),
                                                                     LAYER_VIS("PopGun", 0), LAYER_VIS("PopWarn", 1)]),
        B([TICK(), CMPV("popupOpen", 0, 1), CMPV("popupConfirm", 0, 1)], [LAYER_VIS("PopNice", 0), LAYER_VIS("PopConfirm", 1)]),
        B([TICK(), CMPV("popupOpen", 0, 1), CMPV("popupConfirm", 0, 0)], [LAYER_VIS("PopNice", 1), LAYER_VIS("PopConfirm", 0)]),
    ])]
    t = nid(f"{lname}.poptitle"); m = nid(f"{lname}.popmsg")
    txts = [
        B([TICK(), IV("Txt", "id", 0, t), CMPV("popTitle", 0, 1)], [A("set-text", "Txt", text='"YOU WON!"')]),
        B([TICK(), IV("Txt", "id", 0, t), CMPV("popTitle", 0, 2)], [A("set-text", "Txt", text='"NEW WEAPON!"')]),
        B([TICK(), IV("Txt", "id", 0, t), CMPV("popTitle", 0, 3)], [A("set-text", "Txt", text='"BONUS!"')]),
        B([TICK(), IV("Txt", "id", 0, t), CMPV("popTitle", 0, 4)], [A("set-text", "Txt", text='"RESET PROGRESS?"')]),
        B([TICK(), IV("Txt", "id", 0, m), CMPV("popMsg", 0, 1)], [A("set-text", "Txt", text='"+" & popAmount & " COINS"')]),
        B([TICK(), IV("Txt", "id", 0, m), CMPV("popMsg", 0, 2)], [A("set-text", "Txt", text='"+" & popAmount & " GEM"')]),
        B([TICK(), IV("Txt", "id", 0, m), CMPV("popMsg", 0, 3), CMPV("popAmount", 0, 1)], [A("set-text", "Txt", text='"Bomb unlocked"')]),
        B([TICK(), IV("Txt", "id", 0, m), CMPV("popMsg", 0, 3), CMPV("popAmount", 0, 2)], [A("set-text", "Txt", text='"Shot unlocked"')]),
        B([TICK(), IV("Txt", "id", 0, m), CMPV("popMsg", 0, 3), CMPV("popAmount", 0, 3)], [A("set-text", "Txt", text='"Machine unlocked"')]),
        B([TICK(), IV("Txt", "id", 0, m), CMPV("popMsg", 0, 4)], [A("set-text", "Txt", text='"All coins and progress will be lost."')]),
    ]
    ev.append(G("Popup texts", txts))
    ev.append(G("Popup close", [click(f"{lname}.nice", [SETV("popupOpen", 0)], popup_gate=False)]))
    return ev

def spin_short(cost_expr, cond_count):
    tc, ta = TOAST("rou", "Not enough coins for a spin", 2)
    return click("rou.spin", ta, extra=[CMPV("spinActive", 0, 0), CMPV("coins", 2, cost_expr)] + cond_count + tc)

def spin_start(cost_expr, cost_num, cond_count):
    """Spin pressed: pay, count, pick the outcome and the target angle (HTML startSpin)."""
    return click("rou.spin", [
        SETV("coins", f"coins-{cost_num}"), SETV("spinCount", "spinCount+1"), SETV("needSave", 1),
        SETV("spinOutcome", "floor(random(0,8))"),
        SETV("spinTurns", "5+floor(random(0,3))"),
        SETV("spinFrom", "spinAngle"), SETV("spinT", 0),
        # desired slice: ((8-outcome) mod 8) * TAU/8 ; phase = start mod TAU
        SETV("spinDesired", f"((8-spinOutcome)-8*floor((8-spinOutcome)/8))*{TAU}/8"),
        SETV("spinPhase", f"spinAngle-{TAU}*floor(spinAngle/{TAU})"),
        SETV("spinTo", f"spinAngle+spinTurns*{TAU}+(spinDesired-spinPhase+{TAU}-{TAU}*floor((spinDesired-spinPhase+{TAU})/{TAU}))"),
        SETV("spinActive", 1),
    ], extra=[CMPV("spinActive", 0, 0), CMPV("coins", 5, cost_expr), *cond_count])

def award_events():
    """Prize per outcome (HTML awardSpin). PRIZES index = spinOutcome."""
    ev = []
    for k, (kind, n) in enumerate(PRIZES):
        base = [CMPV("awardNeeded", 0, 1), CMPV("spinOutcome", 0, k)]
        if kind == "coins":
            ev.append(B(base, [SETV("coins", f"coins+{n}"), SETV("popTitle", 1), SETV("popMsg", 1),
                               SETV("popAmount", n), SETV("popKind", 1), SETV("popupOpen", 1), SETV("needSave", 1), SETV("awardNeeded", 0)]))
        elif kind == "gems":
            ev.append(B(base, [SETV("gems", f"gems+{n}"), SETV("popTitle", 1), SETV("popMsg", 2),
                               SETV("popAmount", n), SETV("popKind", 2), SETV("popupOpen", 1), SETV("needSave", 1), SETV("awardNeeded", 0)]))
        else:   # weapon: first unowned of bomb, shot, machine (not equipped); otherwise +450 coins
            for wi, (wid, wname) in enumerate([("bomb", "Bomb"), ("shot", "Shot"), ("machine", "Machine")], start=1):
                ev.append(B(base + [CMPV(f"own_{wid}", 0, 0)],
                            [SETV(f"own_{wid}", 1), SETV("popTitle", 2), SETV("popMsg", 3), SETV("popAmount", wi),
                             SETV("popKind", 3), SETV("popupOpen", 1), SETV("needSave", 1), SETV("awardNeeded", 0)]))
            ev.append(B(base + [CMPV("own_bomb", 0, 1), CMPV("own_shot", 0, 1), CMPV("own_machine", 0, 1)],
                                            [SETV("coins", "coins+450"), SETV("popTitle", 3), SETV("popMsg", 1),
                                             SETV("popAmount", 450), SETV("popKind", 1), SETV("popupOpen", 1),
                                             SETV("needSave", 1), SETV("awardNeeded", 0)]))
    return ev

def roulette_sheet_events():
    ev = [NOTE("Roulette: spin (3.8 s, ease-out), prize, popup.")]
    from sheet_common import common
    ev += common("rou")
    ev += popup_events("rou")
    t = nid("rou.spinlbl")
    ev.append(G("Spin label", [
        B([TICK(), IV("Txt", "id", 0, t), CMPV("spinActive", 0, 0), CMPV("spinCount", 0, 0)], [A("set-text", "Txt", text='"SPIN  ¢ 100"')]),
        B([TICK(), IV("Txt", "id", 0, t), CMPV("spinActive", 0, 0), CMPV("spinCount", 0, 1)], [A("set-text", "Txt", text='"SPIN  ¢ 180"')]),
        B([TICK(), IV("Txt", "id", 0, t), CMPV("spinActive", 0, 0), CMPV("spinCount", 5, 2)], [A("set-text", "Txt", text='"SPIN  ¢ 250"')]),
        B([TICK(), IV("Txt", "id", 0, t), CMPV("spinActive", 0, 1)], [A("set-text", "Txt", text='"SPINNING..."')]),
    ]))
    ev.append(G("Spin button", [
        spin_start("100", 100, [CMPV("spinCount", 0, 0)]),
        spin_start("180", 180, [CMPV("spinCount", 0, 1)]),
        spin_start("250", 250, [CMPV("spinCount", 5, 2)]),
        # HTML startSpin L349: coins below the cost -> showToast('Not enough coins for a spin')
        spin_short("100", [CMPV("spinCount", 0, 0)]),
        spin_short("180", [CMPV("spinCount", 0, 1)]),
        spin_short("250", [CMPV("spinCount", 5, 2)]),
    ]))
    ev.append(G("Spin angle", [
        B([TICK(), CMPV("spinActive", 0, 1)], [
            SETV("spinT", "spinT+ddt"),
            SETV("spinAngle", "spinFrom+(spinTo-spinFrom)*(1-pow(1-min(1,spinT/3.8),5))"),
        ]),
        B([TICK(), CMPV("spinActive", 0, 1), CMPV("spinT", 5, 3.8)],
          [SETV("spinActive", 0), SETV("awardNeeded", 1), SETV("spinAngle", "spinTo")]),
        B([TICK(), IV("Wheel", "id", 0, nid("rou.wheel"))], [ANGLE("Wheel", "spinAngle")]),
    ]))
    ev.append(G("Award prize", award_events()))
    ev.append(G("Exit", [click("rou.exit", [SETV("screen", 1), GOTO("Map")])]))
    return ev
