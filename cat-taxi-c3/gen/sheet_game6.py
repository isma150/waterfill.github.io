"""Game sheet, part 6: visuals and HUD. Positions are HTML units converted with X=60+x*6/7, Y=y*6/7; sizes use the
factors of the HTML draw calls (enemy scale sc, boss 1.1*sc, dynamite 0.75*sc, coin 8.5*sc/20, crate sc)."""
from ev import *
from ids import nid
from sheet_game2 import gate
from sheet_menus import txt_live
from objects import MAN

K = "0.857142857"
def X(e): return f"60+({e})*{K}"
def Y(e): return f"({e})*{K}"
def W(key, factor): return f"{MAN[key]['w']}*({factor})*{K}"
def H(key, factor): return f"{MAN[key]['h']}*({factor})*{K}"

def taxi_events():
    ev = [G("Taxi", [
        B([TICK(), CMPV("screen", 0, 5)], [POS("Taxi", X("mPX"), Y("288.64")),
                                          ANGLE("Taxi", "clamp(-mVX/1200,-0.22,0.22)")]),
    ])]
    for k, (cid, key) in enumerate([("taxi", "veh_taxi"), ("blue", "veh_blue"), ("mint", "veh_mint")]):
        ev[0]["children"].append(B([TICK(), CMPV("car", 0, k)], [ANIM("Taxi", cid), SIZE("Taxi", W(key, "0.92"), H(key, "0.92"))]))
    return ev

def enemy_visual_events():
    ev = [G("Enemy sprites", [B([TICK()], [POS("Enemy", X("sx"), Y("sy"))])])]
    for k, key in enumerate(["enemy_police", "enemy_ambulance", "enemy_van"]):
        ev[0]["children"].append(B([TICK(), IV("Enemy", "kind", 0, k)], [SIZE("Enemy", W(key, "sc"), H(key, "sc"))]))
    ev.append(G("Boss sprites", [
        B([TICK(), CMPV("mBossSpawned", 0, 1)], [POS("Boss", X("sx"), Y("sy"))]),
    ] + [B([TICK(), CMPV("mBoss", 0, k)], [SIZE("Boss", W(f"boss_{kind}", "sc*1.1"), H(f"boss_{kind}", "sc*1.1"))])
         for k, kind in enumerate(["convoy", "armored", "green", "orange", "police"])]))
    ev.append(G("Dynamite sprites", [
        B([TICK()], [POS("Shot", X("sx"), Y("sy")), ANGLE("Shot", "sin(age*17)*0.38"),
                     SIZE("Shot", W("shot_dynamite", "sc*0.75"), H("shot_dynamite", "sc*0.75"))]),
        B([TICK()], [POS("Warn", X("sx"), Y("sy")), SIZE("Warn", W("shot_warning", "sc"), H("shot_warning", "sc"))]),
    ]))
    ev.append(G("Pickup sprites", [
        B([TICK(), IV("Pickup", "isCrate", 0, 0)], [POS("Pickup", X("sx"), Y("sy-10*sc")),
                                                    SIZE("Pickup", W("pick_coin", "8.5*sc/20"), H("pick_coin", "8.5*sc/20"))]),
        B([TICK(), IV("Pickup", "isCrate", 0, 1)], [POS("Pickup", X("sx"), Y("sy-2*sc")),
                                                    SIZE("Pickup", W("pick_crate", "sc"), H("pick_crate", "sc"))]),
    ]))
    return ev

def speed_events():
    """HTML L229-237: 22 lines along the road; reduced motion slows them down."""
    step = "clock*0.74*(1-0.72*reducedMotion)"
    x = f"(idx*0.072+{step})"
    u = f"({x}-floor({x}))"
    side = "(1-2*(idx-2*floor(idx/2)))"
    y1 = f"(297+449*pow({u},1.5))"
    y2 = f"(297+449*pow(min(0.999,{u}+0.035),1.5))"
    rx = f"(210+{side}*(148+90*{u}+(idx-5*floor(idx/5))*11))"
    dx = f"({side}*(11+{u}*39))"
    dy = f"({y2}-{y1})"
    return [G("Road speed lines", [
        B([TICK(), CMPV("screen", 0, 5)], [POS("Speed", X(f"{rx}+{dx}/2"), Y(f"({y1}+{y2})/2")),
                                          SIZE("Speed", f"sqrt({dx}*{dx}+{dy}*{dy})*{K}", f"(1+{u}*2.3)*{K}"),
                                          ANGLE("Speed", f"atan2({dy},{dx})")]),
    ])]

def hud_events():
    ev = []
    gwv = [CMPV("mGuide", 0, 0)]
    ev.append(G("HUD wave and level", [
        txt_live("hud.wave", '"WAVE " & mWave', gwv),
        txt_live("hud.wave", '"ENTRENAMIENTO"', [CMPV("mGuide", 0, 1)]),
        txt_live("hud.level", '"Level " & mLevel'),
    ]))
    ev.append(G("HUD timer", [
        txt_live("hud.timer", "ceil(mTunnelLeft)", [CMPV("mTunnel", 0, 1)]),
        txt_live("hud.timer", '"PASO " & min(4,mGuideStage+1) & "/4"', [CMPV("mTunnel", 0, 0), CMPV("mGuide", 0, 1)]),
        txt_live("hud.timer", '"BOSS"', [CMPV("mTunnel", 0, 0), CMPV("mGuide", 0, 0), CMPV("mWave", 0, 6)]),
        txt_live("hud.timer", '"CLEAR COPS"', [CMPV("mTunnel", 0, 0), CMPV("mGuide", 0, 0), CMPV("mWave", 2, 6),
                                             CMPV("mWaveTime", 5, "mWaveDur")]),
        txt_live("hud.timer", "round(max(0,mWaveDur-mWaveTime)*100)/100",
                 [CMPV("mTunnel", 0, 0), CMPV("mGuide", 0, 0), CMPV("mWave", 2, 6), CMPV("mWaveTime", 2, "mWaveDur")]),
    ]))
    ev.append(G("HUD money", [
        txt_live("hud.money", "round(mBankLoot+mKillLoot)"),
        B([TICK(), IV("Txt", "id", 0, nid("hud.money"))], [POS("Txt", X("clamp(mPX-8,48,380)+60"), Y("392"))]),
        B([TICK(), IV("Icon", "id", 0, nid("hud.coinicon"))], [POS("Icon", X("clamp(mPX-30,28,355)"), Y("392"))]),
    ]))
    ev.append(G("HUD experience", [
        txt_live("hud.lv", '"" & plevel & " Lv"'),
        txt_live("hud.xppct", 'floor(100*min(1,xp/(60+20*plevel))) & "%"'),
        B([TICK(), IV("Shape", "id", 0, nid("hud.xpfill"))],
          [SIZE("Shape", f"76*min(1,xp/(60+20*plevel))*{K}", f"9*{K}"),
           POS("Shape", X("58+38*min(1,xp/(60+20*plevel))"), Y("694.5"))]),
    ]))
    ev.append(G("HUD player hp", [
        B([TICK(), IV("Shape", "id", 0, nid("hud.hpbg"))], [POS("Shape", X("mPX-46+46"), Y("204.5"))]),
        B([TICK(), IV("Shape", "id", 0, nid("hud.hp"))],
          [SIZE("Shape", f"92*max(0,mHP/mMaxHP)*{K}", f"7*{K}"), POS("Shape", X("mPX-46+46*max(0,mHP/mMaxHP)"), Y("204.5"))]),
        B([TICK(), IV("Shape", "id", 0, nid("hud.hp")), CMPV("mHP", 4, 40)], [ANIM("Shape", "bar_hp_ok")]),
        B([TICK(), IV("Shape", "id", 0, nid("hud.hp")), CMPV("mHP", 3, 40)], [ANIM("Shape", "bar_hp_bad")]),
    ]))
    ev.append(G("HUD weapon dial", [
        B([TICK(), CMPV("mWeapon", 0, 0)], [ANGLE("Needle", "-1.2+2.4*min(3,upg_pistol)/3")]),
        B([TICK(), CMPV("mWeapon", 0, 1)], [ANGLE("Needle", "-1.2+2.4*min(3,upg_bomb)/3")]),
        B([TICK(), CMPV("mWeapon", 0, 2)], [ANGLE("Needle", "-1.2+2.4*min(3,upg_shot)/3")]),
        B([TICK(), CMPV("mWeapon", 0, 3)], [ANGLE("Needle", "-1.2+2.4*min(3,upg_machine)/3")]),
        B([TICK(), IV("Shape", "id", 0, nid("hud.dialbg")), CMPV("mWeaponBuff", 4, 0)], [ANIM("Shape", "dial_buff")]),
        B([TICK(), IV("Shape", "id", 0, nid("hud.dialbg")), CMPV("mWeaponBuff", 3, 0)], [ANIM("Shape", "dial_norm")]),
        txt_live("hud.dial", "floor(min(3,upg_pistol))", [CMPV("mWeaponBuff", 3, 0), CMPV("mWeapon", 0, 0)]),
        txt_live("hud.dial", "floor(min(3,upg_bomb))", [CMPV("mWeaponBuff", 3, 0), CMPV("mWeapon", 0, 1)]),
        txt_live("hud.dial", "floor(min(3,upg_shot))", [CMPV("mWeaponBuff", 3, 0), CMPV("mWeapon", 0, 2)]),
        txt_live("hud.dial", "floor(min(3,upg_machine))", [CMPV("mWeaponBuff", 3, 0), CMPV("mWeapon", 0, 3)]),
        txt_live("hud.dial", '""', [CMPV("mWeaponBuff", 4, 0)]),
        txt_live("hud.dialtime", 'ceil(mWeaponBuff) & "s"', [CMPV("mWeaponBuff", 4, 0)]),
        txt_live("hud.dialtime", '""', [CMPV("mWeaponBuff", 3, 0)]),
        B([TICK(), IV("Icon", "id", 0, nid("hud.bicon")), CMPV("mWeaponBuff", 4, 0)], [VIS("Icon", True)]),
        B([TICK(), IV("Icon", "id", 0, nid("hud.bicon")), CMPV("mWeaponBuff", 3, 0)], [VIS("Icon", False)]),
        B([TICK(), IV("Icon", "id", 0, nid("hud.bicon")), CMPV("mBonusWeapon", 0, 1)], [ANIM("Icon", "wpn_bomb")]),
        B([TICK(), IV("Icon", "id", 0, nid("hud.bicon")), CMPV("mBonusWeapon", 0, 2)], [ANIM("Icon", "wpn_shot")]),
        B([TICK(), IV("Icon", "id", 0, nid("hud.bicon")), CMPV("mBonusWeapon", 0, 3)], [ANIM("Icon", "wpn_machine")]),
    ]))
    ev.append(G("HUD auto button", [
        B([TICK(), IV("Shape", "id", 0, nid("hud.autoc")), CMPV("mAuto", 0, 1)], [ANIM("Shape", "circ_on")]),
        B([TICK(), IV("Shape", "id", 0, nid("hud.autoc")), CMPV("mAuto", 0, 0)], [ANIM("Shape", "circ_off")]),
        txt_live("hud.autolbl", '"AUTO"', [CMPV("mAuto", 0, 1)]),
        txt_live("hud.autolbl", '"MAN"', [CMPV("mAuto", 0, 0)]),
    ]))
    ev.append(G("HUD boss", [
        B([TICK(), IV("Boss", "hp", 5, -1000000)], [SETV("mBossRatio", "Boss.hp/Boss.maxHp")]),
        B([TICK(), CMPV("mBossRatio", 4, 0)], [LAYER_VIS("BossHUD", True)]),
        B([TICK(), CMPV("mBossRatio", 2, 0.0001)], [LAYER_VIS("BossHUD", False)]),
        B([TICK(), IV("Shape", "id", 0, nid("hud.bossfill"))],
          [SIZE("Shape", f"242*max(0,mBossRatio)*{K}", f"8*{K}"), POS("Shape", X("89+121*max(0,mBossRatio)"), Y("160"))]),
    ]))
    return ev
