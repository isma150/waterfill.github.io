"""Game sheet, part 7: buttons (AUTO, pause, SALTAR), tunnel and guide texts, pause and defeat texts, theme backdrop.
HTML: drawHUD AUTO button L511, pause button L512, drawTunnelMask/Bonus L532-537, drawGuidedOverlay L433-439,
pauseScreen L567, defeatScreen L566, drawBackdrop themes L57."""
from ev import *
from ids import nid
from sheet_menus import txt_live, click
from sheet_game5 import finish_actions
from sheet_common import TOAST
from sheet_game6 import X, Y

THEME_NAMES = ["city", "blue", "mountain", "sunset", "rose"]
GUIDE_TITLES = ["1/4  APRENDE A CONDUCIR", "2/4  DESTRUYE AL POLICIA", "3/4  ESQUIVA LA DINAMITA", "4/4  RECOGE OBJETOS"]

def buttons_events():
    auto_ok = [CMPV("mGuide", 0, 0), CMPV("mTunnel", 0, 0)]
    return [G("Game buttons", [
        B([TOUCH("Btn", "start"), IV("Btn", "id", 0, nid("game.auto")), CMPV("mAuto", 0, 0)] + auto_ok +
          TOAST("game", "AUTO ACTIVADO: EL COCHE CONDUCE SOLO", 1.7)[0],
          [SETV("mAuto", 1), SETV("mTouchUI", 1)] + TOAST("game", "AUTO ACTIVADO: EL COCHE CONDUCE SOLO", 1.7)[1]),
        B([TOUCH("Btn", "start"), IV("Btn", "id", 0, nid("game.auto")), CMPV("mAuto", 0, 1)] + auto_ok +
          TOAST("game", "MANUAL: TU CONTROLAS EL COCHE", 1.7)[0],
          [SETV("mAuto", 0), SETV("mTouchUI", 1)] + TOAST("game", "MANUAL: TU CONTROLAS EL COCHE", 1.7)[1]),
        B([TOUCH("Btn", "end"), IV("Btn", "id", 0, nid("game.auto"))], [SETV("mTouchUI", 0)]),
        click("game.pause", [SETV("screen", 6), SETV("paused", 1), LAYER_VIS("Pause", 1)], popup_gate=False,
              extra=[CMPV("screen", 0, 5), CMPV("mGuide", 0, 0)]),
        click("game.skip", finish_actions() + [SETV("mTunnel", 0)], popup_gate=False, extra=[CMPV("mGuide", 0, 1)]),
    ])]

def tunnel_and_guide_events():
    tun = nid("tun.line1"); tun2 = nid("tun.line2"); bonus = nid("tun.bonus")
    ev = []
    ev.append(G("Tunnel fade (iris closed after 0.63 s)", [
        B([TICK(), CMPV("mTunnel", 0, 1), CMPV("mTunnelT", 4, 0.63), IV("Shape", "id", 0, nid("tun.fade"))], [VIS("Shape", True)]),
        B([TICK(), CMPV("mTunnel", 0, 0), IV("Shape", "id", 0, nid("tun.fade"))], [VIS("Shape", False)]),
        B([TICK(), CMPV("mTunnelT", 2, 0.63), IV("Shape", "id", 0, nid("tun.fade"))], [VIS("Shape", False)]),
    ]))
    ev.append(G("Tunnel texts", [
        B([TICK(), CMPV("mTunnel", 0, 1), IV("Txt", "id", 0, tun)], [VIS("Txt", True)]),
        B([TICK(), CMPV("mTunnel", 0, 0), IV("Txt", "id", 0, tun)], [VIS("Txt", False)]),
        txt_live("tun.line1", '"TUTORIAL COMPLETE"', [CMPV("mTunnelTrain", 0, 1)]),
        txt_live("tun.line1", '"WAVE " & mWave & " COMPLETE"', [CMPV("mTunnelTrain", 0, 0)]),
        B([TICK(), CMPV("mTunnel", 0, 1), IV("Txt", "id", 0, tun2)], [VIS("Txt", True)]),
        B([TICK(), CMPV("mTunnel", 0, 0), IV("Txt", "id", 0, tun2)], [VIS("Txt", False)]),
        txt_live("tun.line2", '"WAVE 1 INCOMING"', [CMPV("mTunnelTrain", 0, 1)]),
        txt_live("tun.line2", '"WAVE 6 · BOSS"', [CMPV("mTunnelTrain", 0, 0), CMPV("mWave", 5, 5)]),
        txt_live("tun.line2", '"WAVE " & (mWave+1) & " INCOMING"', [CMPV("mTunnelTrain", 0, 0), CMPV("mWave", 2, 5)]),
        B([TICK(), CMPV("mBonusT", 2, 1.6), CMPV("mBonusV", 4, 0), IV("Txt", "id", 0, bonus)], [VIS("Txt", True)]),
        B([TICK(), CMPV("mBonusT", 5, 1.6), IV("Txt", "id", 0, bonus)], [VIS("Txt", False)]),
        txt_live("tun.bonus", 'mBonusV/2 & " x2 Bonus"'),
    ]))
    ev.append(G("Guide overlay", [
        B([TICK(), CMPV("mGuide", 0, 1)], [LAYER_VIS("Guide", 1)]),
        B([TICK(), CMPV("mGuide", 0, 0)], [LAYER_VIS("Guide", 0)]),
        txt_live("guide.title", f'"{GUIDE_TITLES[0]}"', [CMPV("mGuideStage", 0, 0)]),
        txt_live("guide.title", f'"{GUIDE_TITLES[1]}"', [CMPV("mGuideStage", 0, 1)]),
        txt_live("guide.title", f'"{GUIDE_TITLES[2]}"', [CMPV("mGuideStage", 0, 2)]),
        txt_live("guide.title", f'"{GUIDE_TITLES[3]}"', [CMPV("mGuideStage", 5, 3)]),
        txt_live("guide.body", '""', [CMPV("mGuideStage", 0, 0)]),
        txt_live("guide.body", '"¡Perfecto! El policía ha sido destruido."', [CMPV("mGuideStage", 0, 1), CMPV("mGuideHit", 0, 1)]),
        txt_live("guide.body", '"Colócate al lado del coche. Tus gatos disparan solos."', [CMPV("mGuideStage", 0, 1), CMPV("mGuideHit", 0, 0)]),
        txt_live("guide.body", '"¡Has esquivado la dinamita!"', [CMPV("mGuideStage", 0, 2), CMPV("mGuideAvoided", 0, 1)]),
        txt_live("guide.body", '"Mira la señal roja. Cuando lancen dinamita, cambia de carril."', [CMPV("mGuideStage", 0, 2), CMPV("mGuideAvoided", 0, 0)]),
        txt_live("guide.body", '"Ponte en la trayectoria de la caja verde y la moneda."', [CMPV("mGuideStage", 0, 3)]),
        txt_live("guide.hint", '"ARRASTRA HACIA DERECHA  →"', [CMPV("mGuideStage", 0, 0), CMPV("mGuideLeft", 0, 1)]),
        txt_live("guide.hint", '"ARRASTRA HACIA IZQUIERDA  ←"', [CMPV("mGuideStage", 0, 0), CMPV("mGuideLeft", 0, 0)]),
        txt_live("guide.hint", '"¡OBJETIVO CONSEGUIDO!"', [CMPV("mGuideStage", 0, 1), CMPV("mGuideHit", 0, 1)]),
        txt_live("guide.hint", '"NO TIENES QUE PULSAR PARA DISPARAR"', [CMPV("mGuideStage", 0, 1), CMPV("mGuideHit", 0, 0)]),
        txt_live("guide.hint", '"Intentos: " & (mGuideRetry+1)', [CMPV("mGuideStage", 0, 2), CMPV("mGuideRetry", 4, 0)]),
        txt_live("guide.hint", '"ALEJA EL TAXI DE LA ZONA ROJA"', [CMPV("mGuideStage", 0, 2), CMPV("mGuideRetry", 3, 0)]),
        txt_live("guide.hint", '""', [CMPV("mGuideStage", 5, 3)]),
        txt_live("guide.marks", '"Izq ✓     Der " & "✓"', [CMPV("mGuideStage", 0, 0), CMPV("mGuideLeft", 0, 1), CMPV("mGuideRight", 0, 1)]),
        txt_live("guide.marks", '"Izq ✓     Der ○"', [CMPV("mGuideStage", 0, 0), CMPV("mGuideLeft", 0, 1), CMPV("mGuideRight", 0, 0)]),
        txt_live("guide.marks", '"Izq ○     Der ✓"', [CMPV("mGuideStage", 0, 0), CMPV("mGuideLeft", 0, 0), CMPV("mGuideRight", 0, 1)]),
        txt_live("guide.marks", '"Izq ○     Der ○"', [CMPV("mGuideStage", 0, 0), CMPV("mGuideLeft", 0, 0), CMPV("mGuideRight", 0, 0)]),
        txt_live("guide.marks", '"Caja ✓     Moneda ✓"', [CMPV("mGuideStage", 0, 3), CMPV("mGuideCrate", 0, 1), CMPV("mGuideCoin", 0, 1)]),
        txt_live("guide.marks", '"Caja ✓     Moneda ○"', [CMPV("mGuideStage", 0, 3), CMPV("mGuideCrate", 0, 1), CMPV("mGuideCoin", 0, 0)]),
        txt_live("guide.marks", '"Caja ○     Moneda ✓"', [CMPV("mGuideStage", 0, 3), CMPV("mGuideCrate", 0, 0), CMPV("mGuideCoin", 0, 1)]),
        txt_live("guide.marks", '"Caja ○     Moneda ○"', [CMPV("mGuideStage", 0, 3), CMPV("mGuideCrate", 0, 0), CMPV("mGuideCoin", 0, 0)]),
    ]))
    return ev

def theme_events():
    return [G("Backdrop theme", [B([TICK(), CMPV("mTheme", 0, k)], [ANIM("Bg", name)])
                                 for k, name in enumerate(THEME_NAMES)])]

def pause_defeat_text_events():
    return [G("Pause and defeat text", [
        txt_live("pause.wave", '"Wave " & mWave & " / 6"'),
    ])]

def shake_events():
    """HTML drawGame: while m.shake > 0 and reduced motion is off, the whole frame is translated by
    rnd(-shake, shake) and rnd(-0.38*shake, 0.38*shake). Here the Game view is scrolled instead (confirmed
    System 'scroll-to-position' from the template). Centred otherwise. The four centre events are exclusive with the shake event."""
    shaking = [TICK(), CMPV("mShake", 4, 0), CMPV("reducedMotion", 0, 0), CMPV("screen", 4, 4), CMPV("screen", 2, 8)]
    centre = lambda cond: B([TICK()] + cond, [A("scroll-to-position", "System", x="240", y="320")])
    return [G("Screen shake", [
        B(shaking, [A("scroll-to-position", "System", x="240-random(-1,1)*mShake",
                      y="320-random(-1,1)*mShake*0.38")]),
        centre([CMPV("mShake", 3, 0)]),
        centre([CMPV("reducedMotion", 0, 1)]),
        centre([CMPV("screen", 2, 5)]),
        centre([CMPV("screen", 4, 7)]),
    ])]

