"""Menu layouts (HTML: homeScreen, drawMap, resultsScreen, garageScreen, shopScreen, rouletteScreen, settingsScreen)."""
from lay import Lay
from ids import nid
from cfg import BANKS, CARS, WEAPONS, WHEEL_LABELS

WHITE = "#fffdf8"

def common_ui(L, lname):
    """Toast (HTML #toast) and popup layer slots shared by every layout."""
    L.add_layer("Toast")
    L.img("Toast", "Card", "cfffaf0", 210, 90, w=353, h=40, id_=nid(f"{lname}.toastcard"), visible=False)
    L.txt("Toast", "", 210, 90, size=14, color="#2b2a27", tid=nid(f"{lname}.toasttxt"), w=340, visible=False)

def smallstats(L, layer, prefix):
    L.img(layer, "Icon", "pick_coin", 343, 28, scale=0.5)
    L.txt(layer, "0", 360, 28, size=13, color="#423b32", align="left", tid=nid(prefix + ".coins"), w=60)
    L.img(layer, "Icon", "pick_gem", 344, 51, scale=0.45)
    L.txt(layer, "0", 361, 51, size=13, color="#423b32", align="left", tid=nid(prefix + ".gems"), w=60)

def resource_bar(L, layer, y, prefix):
    L.rect(layer, "bar_bg_warm", 0, y, 420, 746 - y)
    L.rect(layer, "pix_77716a", 0, y, 420, 1.6)
    L.img(layer, "Icon", "pick_coin", 111, y + 23, scale=0.5)
    L.txt(layer, "0", 133, y + 23, size=17, color="#393938", align="left", tid=nid(prefix + ".rcoins"), w=120)
    L.img(layer, "Icon", "pick_gem", 274, y + 23, scale=0.55)
    L.txt(layer, "0", 295, y + 23, size=17, color="#333333", align="left", tid=nid(prefix + ".rgems"), w=80)

def header(L, layer, title):
    L.txt(layer, title, 210, 37, size=29, color="#30302c", tid=None)
    L.rect(layer, "pix_c0afa0", 92, 58, 236, 1.4)

def build_home():
    L = Lay("Home", "Event Home")
    L.img("Background", "Bg", "blue", 210, 373, w=560, h=746)
    L.add_layer("Scene")
    for i in range(4):
        L.img("Scene", "Cloud", "cloud", 55 + i * 107, 295 + (i % 2) * 12, scale=0.68, angle=(i - 1.5) * 0.08,
              id_=nid(f"home.cloud{i}"))
    L.img("Scene", "Taxi", "home", 211, 391, scale=1.20)
    L.img("Scene", "Icon", "cat_e", 329, 379, scale=0.85)
    L.img("Scene", "Logo", "logo", 210, 145, w=None, id_=nid("home.logo"))
    L.card("Scene", 49, 520, 322, 59, color="#fffef9")
    L.txt("Scene", "Rob the banks. Escape the cops!", 210, 544, size=18, color="#30302c")
    L.txt("Scene", "Steer • Dodge • Auto-shoot", 210, 566, size=14, color="#797068")
    L.btn("Scene", nid("btn.home.play"), 74, 603, 272, 60, "PLAY ▶", color="#f8d36d", size=29)
    L.btn("Scene", nid("btn.home.how"), 125, 672, 170, 44, "HOW TO PLAY", size=15)
    L.txt("Scene", "HTML5 · Tutorial por fases v9", 210, 729, size=11, color="#8c847b")
    common_ui(L, "home")
    return L

def build_map():
    L = Lay("Map", "Event Map")
    L.img("Background", "Bg", "map", 210, 373, w=560, h=746)
    L.add_layer("Nodes")
    mapnodes = [[210, 586], [322, 555], [259, 524], [119, 493], [121, 462], [262, 430], [322, 399], [207, 368],
                [97, 337], [163, 306], [302, 275], [297, 244], [156, 213], [99, 182], [216, 151]]
    for i, (x, y) in enumerate(mapnodes):
        L.img("Nodes", "Node", "normal", x, y, id_=nid(f"map.node{i}"))
    L.add_layer("UI")
    L.txt("UI", "Ranking", 96, 520, size=21, color="#4f9a52")
    L.txt("UI", "Stage", 100, 544, size=21, color="#4f9a52")
    L.card("UI", 43, 30, 334, 106, color="#fffdf4")
    L.txt("UI", "", 208, 52, size=20, color="#30302c", tid=nid("map.bankname"), w=320)
    L.txt("UI", "", 129, 87, size=17, color="#30302c", align="left", tid=nid("map.level"), w=150)
    L.txt("UI", "Balances", 287, 78, size=15, color="#30302c", align="center", w=120)
    L.img("UI", "Icon", "pick_coin", 280, 102, scale=0.5)
    L.txt("UI", "", 310, 102, size=15, color="#514935", align="left", tid=nid("map.balance"), w=120)
    L.btn("UI", nid("btn.map.garage"), 18, 645, 116, 44, "GARAGE", size=17)
    L.btn("UI", nid("btn.map.spin"), 150, 645, 101, 44, "SPIN", size=16)
    L.btn("UI", nid("btn.map.shop"), 266, 645, 134, 44, "SHOP", size=17)
    resource_bar(L, "UI", 697, "map")
    L.btn("UI", nid("btn.map.back"), 16, 701, 73, 39, "BACK", size=15)
    L.btn("UI", nid("btn.map.start"), 315, 701, 97, 39, "START ▶", color="#f5cf67", size=16)
    for i in range(4):
        L.img("UI", "Icon", "key_on", 171 + i * 23, 624, scale=0.5, id_=nid(f"map.key{i}"))
    L.txt("UI", "", 325, 624, size=15, color="#6e6458", tid=nid("map.keys"), w=60)
    common_ui(L, "map")
    return L

def build_results():
    L = Lay("Results", "Event Results")
    L.img("Background", "Bg", "black", 210, 373, w=560, h=746)
    L.add_layer("UI")
    L.txt("UI", "ESCAPE COMPLETE", 210, 103, size=27, color="#f9f6e9")
    L.txt("UI", "", 210, 148, size=17, color="#d1cec4", tid=nid("res.sub"), w=380)
    L.txt("UI", "Coins stolen from bank", 38, 384, size=16, color="#f5f5f1", align="left", w=300)
    L.txt("UI", "", 380, 384, size=18, color="#f5f5f1", align="right", tid=nid("res.bank"), w=200)
    L.txt("UI", "Earn money by destroying", 38, 425, size=15, color="#f5f5f1", align="left", w=300)
    L.txt("UI", "", 380, 425, size=18, color="#f5f5f1", align="right", tid=nid("res.kill"), w=200)
    L.txt("UI", "Perfect Bonus", 38, 467, size=16, color="#f5f5f1", align="left", w=300)
    L.txt("UI", "0", 380, 467, size=18, color="#f5f5f1", align="right", tid=nid("res.perfect"), w=200)
    L.rect("UI", "pix_c3c1b9", 38, 501, 344, 1.8)
    L.txt("UI", "Total", 43, 543, size=25, color="#fffdf0", align="left", w=200)
    L.img("UI", "Icon", "pick_coin", 291, 541, scale=0.65)
    L.txt("UI", "", 377, 543, size=25, color="#fff1ba", align="right", tid=nid("res.total"), w=200)
    L.txt("UI", "Results based on this run", 210, 611, size=12, color="#999891")
    L.btn("UI", nid("btn.res.spin"), 28, 657, 111, 55, "SPIN", color="#edc5b8", size=18)
    L.btn("UI", nid("btn.res.garage"), 150, 657, 120, 55, "GARAGE", color="#d9ddd4", size=18)
    L.btn("UI", nid("btn.res.map"), 280, 657, 115, 55, "MAP →", color="#f0d389", size=18)
    common_ui(L, "res")
    return L

def popup_layer(L, lname, with_confirm):
    """HTML drawPopup(): velo, tarjeta, icono, mensaje y botones. Icons and button groups are separate layers."""
    L.add_layer("Popup", visible=False)
    L.img("Popup", "Shape", "dim_popup", 210, 373, id_=nid(f"{lname}.popdim"))
    L.card("Popup", 36, 231, 348, 278, color="#fffdf6", id_=nid(f"{lname}.popcard"))
    L.txt("Popup", "", 210, 274, size=26, color="#34362e", tid=nid(f"{lname}.poptitle"), w=340)
    L.txt("Popup", "", 210, 395, size=17, color="#30302c", tid=nid(f"{lname}.popmsg"), w=315, wrap=True,
          lines_h=80)
    L.add_layer("PopCoin", visible=False); L.img("PopCoin", "Icon", "pick_coin", 210, 338, scale=1.55)
    L.add_layer("PopGem", visible=False); L.img("PopGem", "Icon", "pick_gem", 210, 337, scale=1.85)
    L.add_layer("PopGun", visible=False); L.img("PopGun", "Icon", "wpn_shot", 210, 337, scale=2.0)
    L.add_layer("PopWarn", visible=False); L.txt("PopWarn", "!", 210, 342, size=58, color="#e3a647", w=120)
    L.add_layer("PopNice", visible=True)
    L.btn("PopNice", nid(f"btn.{lname}.nice"), 113, 444, 194, 49, "NICE!", color="#f7d376", size=21)
    if with_confirm:
        L.add_layer("PopConfirm", visible=False)
        L.btn("PopConfirm", nid(f"btn.{lname}.cancel"), 55, 443, 141, 47, "CANCEL", size=17)
        L.btn("PopConfirm", nid(f"btn.{lname}.popreset"), 216, 443, 147, 47, "RESET", color="#eec0ae", size=17)

def build_garage():
    L = Lay("Garage", "Event Garage")
    L.img("Background", "Bg", "garage", 210, 373, w=560, h=746)
    L.add_layer("UI")
    L.btn("UI", nid("btn.gar.settings"), 12, 14, 32, 32, "⚙", size=16)
    L.txt("UI", "CAT GARAGE", 210, 31, size=25, color="#3d5149")
    smallstats(L, "UI", "gar")
    L.img("UI", "Taxi", "taxi", 210, 205, scale=0.74, id_=nid("gar.car"))
    L.img("UI", "Icon", "cat_a", 78, 209, scale=0.58)
    L.img("UI", "Icon", "cat_b", 344, 209, scale=0.58)
    for i, (name, t) in enumerate([("WEAPONS", 0), ("CARS", 1), ("CREW", 2)]):
        L.btn("UI", nid(f"btn.gar.tab{t}"), 11 + i * 139, 251, 131, 38, name, color="#fffcf7", size=15)
    L.card("UI", 14, 299, 392, 139, color="#faf8f1")
    # weapon detail (layer GearWeapon)
    L.add_layer("GearWeapon", visible=True)
    L.img("GearWeapon", "Icon", "wpn_pistol", 74, 350, scale=1.6, id_=nid("gar.wicon"))
    L.txt("GearWeapon", "", 155, 323, size=22, color="#3c3730", align="left", tid=nid("gar.wname"), w=230)
    L.txt("GearWeapon", "", 144, 354, size=16, color="#524d44", align="left", tid=nid("gar.wpower"), w=260)
    L.txt("GearWeapon", "", 144, 379, size=14, color="#635d50", align="left", tid=nid("gar.wrate"), w=260)
    L.btn("GearWeapon", nid("btn.gar.equip"), 155, 390, 106, 39, "EQUIP ✓", color="#b4ecbf", size=13)
    L.btn("GearWeapon", nid("btn.gar.wbuy"), 155, 390, 240, 39, None, color="#9ee4f5", size=13)
    L.txt("GearWeapon", "", 275, 410, size=13, color="#33322f", tid=nid("gar.wbuylbl"), w=240)
    # car detail (layer GearCar)
    L.add_layer("GearCar", visible=False)
    L.img("GearCar", "Taxi", "taxi", 78, 385, scale=0.43, id_=nid("gar.cprev"))
    L.txt("GearCar", "", 141, 330, size=21, color="#3a382f", align="left", tid=nid("gar.cname"), w=250)
    L.txt("GearCar", "Cosmetic variant · 1-hit danger", 142, 356, size=13, color="#645a50", align="left", w=260)
    L.btn("GearCar", nid("btn.gar.cbuy"), 153, 390, 241, 39, None, color="#9ee4f5", size=13)
    L.txt("GearCar", "", 273, 410, size=13, color="#33322f", tid=nid("gar.cbuylbl"), w=241)
    # crew detail (layer GearCrew)
    L.add_layer("GearCrew", visible=False)
    L.img("GearCrew", "Icon", "cat_c", 77, 371, scale=0.65)
    L.txt("GearCrew", "", 144, 332, size=21, color="#383634", align="left", tid=nid("gar.crname"), w=250)
    L.txt("GearCrew", "", 144, 357, size=13, color="#625a53", align="left", tid=nid("gar.crdesc"), w=260)
    L.btn("GearCrew", nid("btn.gar.crew"), 154, 394, 239, 34, None, color="#9ee4f5", size=14)
    L.txt("GearCrew", "", 273, 411, size=14, color="#33322f", tid=nid("gar.crlbl"), w=239)
    # grid: 12 cells; cell state images and the item graphic per tab
    for i in range(12):
        x, y = 17 + (i % 4) * 99, 457 + (i // 4) * 65
        L.img("UI", "Shape", "cell_nor", x + 45, y + 28, w=90, h=56, id_=nid(f"gar.cell{i}"))
        L.add_layer("GridWeapon", visible=True)
        L.img("GridWeapon", "Icon", ["wpn_pistol", "wpn_bomb", "wpn_shot", "wpn_machine"][i % 4], x + 45, y + 24, scale=0.78, id_=nid(f"gar.wcell{i}"))
        L.add_layer("GridCar", visible=False)
        L.img("GridCar", "Taxi", ["taxi", "blue", "mint", "taxi"][i % 4], x + 45, y + 48, scale=0.28, id_=nid(f"gar.ccell{i}"))
        L.add_layer("GridCrew", visible=False)
        L.txt("GridCrew", "", x + 45, y + 25, size=26, color="#3c3730", tid=nid(f"gar.gcell{i}"), w=60)
        L.txt("GridCrew", "", x + 45, y + 47, size=10, color="#3c3730", tid=nid(f"gar.ncell{i}"), w=88)
        L.add_layer("GridLock", visible=True)
        L.img("GridLock", "Shape", "lock_badge", x + 73.5, y + 14.5, w=25, h=23, id_=nid(f"gar.lockbg{i}"))
        L.txt("GridLock", "🔒", x + 74, y + 14, size=14, color="#3c3730", tid=nid(f"gar.lock{i}"), w=30)
        L.img("GridLock", "Shape", "dot_84c974", x + 75, y + 11, w=18, h=18, id_=nid(f"gar.okbg{i}"))
        L.txt("GridLock", "✓", x + 75, y + 10, size=12, color="#ffffff", tid=nid(f"gar.ok{i}"), w=20)
        L.txt("GridLock", "🔒", x + 45, y + 29, size=19, color="#b1a89b", tid=nid(f"gar.emptylock{i}"), w=60)
    L.btn("UI", nid("btn.gar.shop"), 23, 674, 150, 55, "SHOP", size=20)
    L.btn("UI", nid("btn.gar.next"), 244, 674, 153, 55, "NEXT →", color="#f6d06b", size=21)
    common_ui(L, "gar")
    return L

def build_shop():
    L = Lay("Shop", "Event Shop")
    L.img("Background", "Bg", "paper", 210, 373, w=560, h=746)
    L.add_layer("UI")
    header(L, "UI", "SHOP")
    smallstats(L, "UI", "shop")
    tabs = ["Car", "Driver", "Assist", "Pet", "Coin / Key"]
    for i, t in enumerate(tabs):
        L.btn("UI", nid(f"btn.shop.tab{i}"), 7 + i * 82, 83, 78, 37, t, color="#f5f1e9", size=11 if i == 4 else 14)
    # three item slots, one layer each; the tab decides which slots show (events)
    for s in range(3):
        y = 147 + s * 151
        ly_ = f"Slot{s}"
        L.add_layer(ly_, visible=(s == 0))
        L.card(ly_, 23, y, 374, 133, color="#fffdf8")
        L.img(ly_, "Taxi", ["blue", "mint", "taxi"][s], 87, y + 92, scale=0.44, id_=nid(f"shop.prev{s}"))
        L.img(ly_, "Icon", "cat_d", 87, y + 86, scale=0.65, id_=nid(f"shop.cat{s}"))
        L.txt(ly_, "", 84, y + 63, size=41, color="#d5ac45", tid=nid(f"shop.star{s}"), w=60)
        L.txt(ly_, "", 156, y + 33, size=20, color="#383b34", align="left", tid=nid(f"shop.name{s}"), w=240)
        L.txt(ly_, "", 156, y + 62, size=12, color="#797166", align="left", tid=nid(f"shop.detail{s}"), w=240)
        L.btn(ly_, nid(f"btn.shop.item{s}"), 147, y + 86, 232, 36, None, color="#c8ecae", size=14)
        L.txt(ly_, "", 263, y + 104, size=14, color="#33322f", tid=nid(f"shop.lbl{s}"), w=232)
    L.card("UI", 39, 601, 342, 55, color="#fff6dd")
    L.txt("UI", "Collect coins on every escape", 210, 620, size=15, color="#30302c", w=340)
    L.txt("UI", "No real-money purchases", 210, 640, size=13, color="#6b655e", w=340)
    L.btn("UI", nid("btn.shop.back"), 22, 674, 154, 54, "← BACK", size=20)
    L.btn("UI", nid("btn.shop.bankmap"), 207, 674, 190, 54, "BANK MAP →", color="#f7d46d", size=19)
    common_ui(L, "shop")
    return L

def build_roulette():
    L = Lay("Roulette", "Event Roulette")
    L.img("Background", "Bg", "paper", 210, 373, w=560, h=746)
    L.add_layer("UI")
    L.txt("UI", "LUCKY WHEEL", 210, 42, size=29, color="#30302c")
    L.txt("UI", "SPIN FOR REWARDS!", 210, 80, size=16, color="#756c5c")
    L.img("UI", "Roulette", "base", 210, 373, id_=nid("rou.base"))
    L.img("UI", "Wheel", "wheel", 210, 315, id_=nid("rou.wheel"))
    L.btn("UI", nid("btn.rou.spin"), 115, 576, 190, 61, "", color="#f5a48e", size=24)
    L.txt("UI", "", 210, 606, size=24, color="#fffdf6", tid=nid("rou.spinlbl"), w=190)
    L.btn("UI", nid("btn.rou.exit"), 17, 638, 140, 53, "EXIT", size=23)
    for i in range(4):
        L.img("UI", "Icon", "key_on", 283 + i * 27, 659, scale=0.5, id_=nid(f"rou.key{i}"))
    resource_bar(L, "UI", 703, "rou")
    popup_layer(L, "rou", with_confirm=False)
    common_ui(L, "rou")
    return L

def build_settings():
    L = Lay("Settings", "Event Settings")
    L.img("Background", "Bg", "paper", 210, 373, w=560, h=746)
    L.add_layer("UI")
    header(L, "UI", "SETTINGS")
    L.card("UI", 24, 103, 372, 332, color="#fffdf8")
    L.btn("UI", nid("btn.set.sound"), 57, 154, 307, 55, "", size=19)
    L.txt("UI", "", 210, 181, size=19, color="#33322f", tid=nid("set.soundlbl"), w=300)
    L.btn("UI", nid("btn.set.motion"), 57, 231, 307, 55, "", size=17)
    L.txt("UI", "", 210, 258, size=17, color="#33322f", tid=nid("set.motionlbl"), w=300)
    L.btn("UI", nid("btn.set.tutorial"), 57, 305, 307, 55, "REPLAY TUTORIAL", size=18)
    L.btn("UI", nid("btn.set.back"), 95, 494, 230, 60, "← BACK", color="#f5d47b", size=22)
    L.btn("UI", nid("btn.set.reset"), 116, 654, 188, 42, "RESET SAVE DATA", size=14)
    popup_layer(L, "set", with_confirm=True)
    common_ui(L, "set")
    return L
