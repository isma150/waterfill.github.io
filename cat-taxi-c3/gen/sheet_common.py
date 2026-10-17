"""Events repeated in every layout sheet (no includes): clock, toast, save, sound toggle."""
from ev import *
from cfg import PERSIST, PERSIST_KEY_PREFIX
from ids import nid

def TXT_PICK(tid):
    """Condition that picks the Txt instance with this id (used together with a set-text action)."""
    return IV("Txt", "id", 0, tid)

def TOAST(lname, msg, seconds=2):
    """(extra conditions, actions) that show this layout's toast. Merge into the sender's event."""
    tid = nid(f"{lname}.toasttxt")
    return [TXT_PICK(tid)], [A("set-text", "Txt", text=f'"{msg}"'), SETV("toastOn", 1),
                             SETV("toastUntil", f"clock+{seconds}")]

def common(lname):
    card, txt = nid(f"{lname}.toastcard"), nid(f"{lname}.toasttxt")
    ev = [NOTE("Common: clock, toast, save, sound. Same events in every layout sheet."),
          G("Clock", [B([TICK()], [SETV("ddt", "min(dt, 0.042)"), SETV("clock", "clock+ddt")])]),
          G("Toast", [
              B([TICK(), CMPV("toastOn", 1, 1), CMPV("clock", 4, "toastUntil")], [SETV("toastOn", 0)]),
              # default position (10%): every screen except 5..7 (set first, the 71% events below override)
              B([TICK(), CMPV("toastOn", 1, 1), IV("Card", "id", 0, card)],
                [VIS("Card", True), POS("Card", "210", "75")]),
              B([TICK(), CMPV("toastOn", 1, 1), IV("Txt", "id", 0, txt)],
                [VIS("Txt", True), POS("Txt", "210", "93")]),
              # shown at 71% of the frame in game/pause/defeat (screen 5..7), otherwise at 10%
              B([TICK(), CMPV("toastOn", 1, 1), CMPV("screen", 5, 5), CMPV("screen", 3, 7), IV("Card", "id", 0, card)],
                [VIS("Card", True), POS("Card", "210", "530")]),
              B([TICK(), CMPV("toastOn", 1, 1), CMPV("screen", 5, 5), CMPV("screen", 3, 7), IV("Txt", "id", 0, txt)],
                [VIS("Txt", True), POS("Txt", "210", "548")]),
              B([TICK(), CMPV("toastOn", 1, 0), IV("Card", "id", 0, card)], [VIS("Card", False)]),
              B([TICK(), CMPV("toastOn", 1, 0), IV("Txt", "id", 0, txt)], [VIS("Txt", False)]),
          ]),
          G("Save", [
              B([TICK(), CMPV("needSave", 0, 1)],
                [A("set-item", "LocalStorage", key=f'"{PERSIST_KEY_PREFIX}{n}"', value=n) for n, _ in PERSIST]
                + [SETV("needSave", 0)]),
          ]),
          G("Sound toggle (M key)", [
              B([C("on-key-pressed", "Keyboard", key="77")],
                [SETV("sound", "1-sound"), SETV("needSave", 1)]),
          ]),
    ]
    return ev
