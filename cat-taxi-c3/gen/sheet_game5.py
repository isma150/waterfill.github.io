"""Game sheet, part 5: guided tutorial (HTML L414-439 updateGuidedMission, guideNewEnemy, guideNextStage,
finishGuidedMission, drawGuidedOverlay texts). Runs only while mGuide=1; the normal combat events are gated off."""
from ev import *
from ids import nid
from sheet_menus import txt_live
from sheet_game3 import pos_layout, _shot_init
from sheet_common import TOAST

def gg():
    """Guided gate: in the game, not paused, guided run, not in the training tunnel."""
    return [TICK(), CMPV("screen", 0, 5), CMPV("paused", 0, 0), CMPV("mGuide", 0, 1), CMPV("mTunnel", 0, 0)]

def st(k):
    return CMPV("mGuideStage", 0, k)

def next_stage(to):
    """guideNextStage: clear entities, stage++, reset the stage counters."""
    return [DESTROY("Enemy"), DESTROY("Shot"), DESTROY("Pickup"), DESTROY("Warn"),
            SETV("mGuideStage", to), SETV("mGuideTime", 0), SETV("mGuideReady", 0), SETV("mGuideWait", 0),
            SETV("mGuideShotMade", 0), SETV("mGuideSpawned", 0), SETV("mInv", 0)]

def guide_events():
    ev = []
    ev.append(G("Guided clocks", [
        B(gg(), [SETV("mSeconds", "mSeconds+ddt"), SETV("mGuideTime", "mGuideTime+ddt"), SETV("mWaveTime", 0),
                 SETV("mFlash", "max(0,mFlash-ddt)"), SETV("mAuto", 0), SETV("mInv", 0)]),
    ]))
    # stage 0: drag left past 117, then right past 294, hold 0.8 s
    ev.append(G("Guided stage 0: drive", [
        B(gg() + [st(0), CMPV("mPX", 2, 117)], [SETV("mGuideLeft", 1)]),
        B(gg() + [st(0), CMPV("mGuideLeft", 0, 1), CMPV("mPX", 4, 294)], [SETV("mGuideRight", 1)]),
        B(gg() + [st(0), CMPV("mGuideLeft", 0, 1), CMPV("mGuideRight", 0, 1)], [SETV("mGuideReady", "mGuideReady+ddt")]),
        B(gg() + [st(0), CMPV("mGuideReady", 4, 0.8)], next_stage(1)),
    ]))
    # stage 1: one training police car on the side away from the taxi (HTML guideNewEnemy: px<210 ? +115 : -115)
    def spawn_police(side_cond, offset):
        return B(gg() + [st(1), CMPV("mGuideSpawned", 0, 0)] + side_cond,
                 [SETV("mGuideSpawned", 1), SETV("mIdSeq", "mIdSeq+1"), CREATE("Enemy", "Actors", 0, 0),
                  ANIM("Enemy", "police"), SIV("Enemy", "id", "mIdSeq"), SIV("Enemy", "training", 1),
                  SIV("Enemy", "kind", 0), SIV("Enemy", "d", -0.38), SIV("Enemy", "vd", 0.48),
                  SIV("Enemy", "hoverD", -0.045), SIV("Enemy", "dodge", 0), SIV("Enemy", "dodgeCd", 99999),
                  SIV("Enemy", "fire", 9999), SIV("Enemy", "laneTo", f"clamp(mPX{offset},72,348)"),
                  SIV("Enemy", "lane", "laneTo"), SIV("Enemy", "laneFrom", "laneTo"), SIV("Enemy", "laneT", 1),
                  SIV("Enemy", "hp", 18), SIV("Enemy", "maxHp", 18), SIV("Enemy", "state", 0),
                  SIV("Enemy", "age", 0)])
    ev.append(G("Guided stage 1: destroy the police car", [
        spawn_police([CMPV("mPX", 2, 210)], "+115"),
        spawn_police([CMPV("mPX", 5, 210)], "-115"),
        B(gg() + [IV("Enemy", "training", 0, 1)],
          [SIV("Enemy", "d", "min(hoverD,d+vd*ddt)"), SIV("Enemy", "age", "age+ddt")]),
        B(gg() + [st(1), IV("Enemy", "training", 0, 1), IV("Enemy", "d", 4, -0.26), IV("Enemy", "dist", 2, 100)],
          [SETV("mBulletTimer", "mBulletTimer-ddt")]),
        B(gg() + [st(1), IV("Enemy", "training", 0, 1), IV("Enemy", "d", 4, -0.26), IV("Enemy", "dist", 2, 100),
                  CMPV("mBulletTimer", 3, 0)],
          [SETV("mBulletTimer", 0.22), SIV("Enemy", "hp", "hp-mDmg")]),
        B(gg() + [st(1), IV("Enemy", "training", 0, 1), IV("Enemy", "hp", 3, 0)], [DESTROY("Enemy")]),
        B(gg() + [st(1), CMPV("Enemy.Count", 0, 0)], [SETV("mGuideHit", 1), SETV("mGuideReady", "mGuideReady+ddt")]),
        B(gg() + [st(1), CMPV("mGuideReady", 4, 1.3)], next_stage(2)),
    ]))
    return ev

def finish_actions():
    """finishGuidedMission (HTML L419): leave the tutorial and start wave 1 of the same run.
    mSpawnFix makes the wave setup use spawnTimer 1.0 and pickupTimer 3 (see sheet_game1.wave_setup_events)."""
    return [DESTROY("Enemy"), DESTROY("Shot"), DESTROY("Pickup"), DESTROY("Warn"),
            SETV("mGuide", 0), SETV("mEndTunnel", 0), SETV("mTunnelTrain", 0), SETV("mTunnel", 0), SETV("mSpawnFix", 1),
            SETV("mGuideStage", 5), SETV("mGuideTime", 0), SETV("mGuideReady", 0),
            SETV("mWave", 1), SETV("mWaveTime", 0), SETV("mSeconds", 0), SETV("mSetupWave", 1),
            SETV("mBossSpawned", 0), SETV("mBulletTimer", 0), SETV("mWeaponBuff", 0), SETV("mBonusWeapon", 0),
            SETV("mTarget", "mPX"), SETV("mInv", 0), SETV("mAuto", 0), SETV("seenTutorial", 1), SETV("needSave", 1)]

def guide_events2():
    ev = []
    # training enemies (stage 1 and 2): approach, hover, and leave the tutorial stages when dead (no reward)
    ev.append(G("Guided pickup projection", [
        B([TICK(), IV("Pickup", "training", 0, 1)],
          [SIV("Pickup", "sx", "210+(lane-210)*(148+90*pow(clamp(1-clamp(progress,0,1.15),0,1),1.06))/148"),
           SIV("Pickup", "sy", "319+441*pow(min(max(1-clamp(progress,0,1.15),0),1.15),1.22)+100*min(1-clamp(progress,0,1.15),0)"),
           SIV("Pickup", "sc", "0.92*(1+0.6*max(clamp(1-clamp(progress,0,1.15),-0.5,1.15),0)+1.5*min(clamp(1-clamp(progress,0,1.15),-0.5,1.15),0))")]),
    ]))
    ev.append(G("Guided enemy kill", [
        B([TICK(), CMPV("screen", 0, 5), CMPV("mGuide", 0, 1), IV("Enemy", "training", 0, 1), IV("Enemy", "hp", 3, 0)],
          [DESTROY("Enemy")]),
    ]))
    # stage 2: the attacking police car (hp 999, HTML guideNewEnemy(true))
    def spawn_attacker(side_cond, offset):
        return B(gg() + [st(2), CMPV("mGuideSpawned", 0, 0)] + side_cond,
                 [SETV("mGuideSpawned", 1), SETV("mIdSeq", "mIdSeq+1"), CREATE("Enemy", "Actors", 0, 0),
                  ANIM("Enemy", "police"), SIV("Enemy", "id", "mIdSeq"), SIV("Enemy", "training", 1),
                  SIV("Enemy", "kind", 0), SIV("Enemy", "d", -0.38), SIV("Enemy", "vd", 0.48),
                  SIV("Enemy", "hoverD", -0.045), SIV("Enemy", "dodge", 0), SIV("Enemy", "dodgeCd", 99999),
                  SIV("Enemy", "fire", 9999), SIV("Enemy", "laneTo", f"clamp(mPX{offset},72,348)"),
                  SIV("Enemy", "lane", "laneTo"), SIV("Enemy", "laneFrom", "laneTo"), SIV("Enemy", "laneT", 1),
                  SIV("Enemy", "hp", 999), SIV("Enemy", "maxHp", 999), SIV("Enemy", "state", 0),
                  SIV("Enemy", "age", 0)])
    ev.append(G("Guided stage 2: attacking police", [
        spawn_attacker([CMPV("mPX", 2, 200)], "+60"),
        spawn_attacker([CMPV("mPX", 5, 200)], "-60"),
    ]))
    # stage 2: dynamite aimed at the taxi's lane (HTML L426): lands at clamp(px,75,345), 1.45 s, 0.54 depth
    # HTML showToast texts of the tutorial (L426-431), in the order they happen
    t_dyn = TOAST("game", "¡DINAMITA! APARTATE DEL AVISO ROJO", 1.4)
    t_casi = TOAST("game", "¡CASI! MUÉVETE LEJOS DEL ROJO", 1.5)
    t_bien = TOAST("game", "¡BIEN ESQUIVADO!", 1.15)
    t_arma = TOAST("game", "ARMA CONSEGUIDA!", 1)
    t_moneda = TOAST("game", "MONEDA CONSEGUIDA!", 1)
    ev.append(G("Guided stage 2: dynamite", [
        B(gg() + [st(2), CMPV("mGuideShotMade", 0, 0), CMPV("mGuideWait", 3, 0), CMPV("mGuideTime", 5, 1.65),
                  IV("Enemy", "training", 0, 1)] + t_dyn[0],
          [SETV("thLane", "Enemy.lane"), SETV("thD", "Enemy.d"), CREATE("Shot", "Actors", 0, 0), ANIM("Shot", "dyn"),
           SIV("Shot", "id", "mIdSeq"), SETV("mIdSeq", "mIdSeq+1"),
           SIV("Shot", "x0", "thLane"), SIV("Shot", "d0", "thD"), SIV("Shot", "xl", "clamp(mPX,75,345)"),
           SIV("Shot", "dl", 0.54), SIV("Shot", "fly", 1.45), SIV("Shot", "age", 0), SIV("Shot", "exploded", 0),
           SIV("Shot", "done", 0), SIV("Shot", "training", 1), SIV("Shot", "landed", 0), SIV("Shot", "d", "thD"),
           SETV("mGuideShotMade", 1),
           SETV("wxl", "clamp(mPX,75,345)"), SETV("wdl", 0.54), SETV("wid", "mIdSeq-1"),
           CREATE("Warn", "Actors", 0, 0), ANIM("Warn", "warn"), SIV("Warn", "owner", "wid"),
           SIV("Warn", "sx", "210+(wxl-210)*(148+90*pow(clamp(wdl,0,1),1.06))/148"),
           SIV("Warn", "sy", "319+441*pow(min(max(wdl,0),1.15),1.22)+100*min(wdl,0)"),
           SIV("Warn", "sc", "0.92*(1+0.6*max(clamp(wdl,-0.5,1.15),0)+1.5*min(clamp(wdl,-0.5,1.15),0))")] + t_dyn[1]),
        B(gg() + [st(2), CMPV("mGuideWait", 4, 0)], [SETV("mGuideWait", "mGuideWait-ddt")]),
        B(gg() + [st(2), IV("Shot", "training", 0, 1), IV("Shot", "exploded", 0, 0)],
          [SIV("Shot", "age", "age+ddt"), SIV("Shot", "dist", "abs(xl-mPX)"),
           SIV("Shot", "d", "d0+(dl-d0)*min(1,age/fly)-0.26*max(0,age-fly)"),
           SIV("Shot", "sx", "210+(x0+(xl-x0)*min(1,age/fly)-210)*(148+90*pow(clamp(d,0,1),1.06))/148"),
           SIV("Shot", "sy", "319+441*pow(min(max(d,0),1.15),1.22)+100*min(d,0)")]),
        # the retry (HTML L427: distance < 68) and the avoided shot
        B(gg() + [st(2), IV("Shot", "training", 0, 1), IV("Shot", "exploded", 0, 0), IV("Shot", "age", 5, "fly"),
                  IV("Shot", "d", 3, 0.052), IV("Shot", "dist", 2, 68)] + t_casi[0],
          [SETV("mGuideRetry", "mGuideRetry+1"), SETV("mGuideShotMade", 0), SETV("mGuideWait", 1.1),
           SIV("Shot", "exploded", 1), DESTROY("Shot"), DESTROY("Warn")] + t_casi[1]),
        B(gg() + [st(2), IV("Shot", "training", 0, 1), IV("Shot", "exploded", 0, 0), IV("Shot", "age", 5, "fly"),
                  IV("Shot", "d", 3, 0.052), IV("Shot", "dist", 5, 68)] + t_bien[0],
          [SETV("mGuideAvoided", 1), SIV("Shot", "exploded", 1), DESTROY("Shot"), DESTROY("Warn")] + t_bien[1]),
        B(gg() + [st(2), CMPV("mGuideAvoided", 0, 1)], [SETV("mGuideReady", "mGuideReady+ddt")]),
        B(gg() + [st(2), CMPV("mGuideReady", 4, 1.3)], next_stage(3)),
    ]))
    # stage 3: one crate, then one coin, spawned in the mirror lane (HTML L429-431)
    ev.append(G("Guided stage 3: pick up", [
        B(gg() + [st(3), CMPV("Pickup.Count", 0, 0), CMPV("mGuideWait", 3, 0)], [SETV("mGuideWait", "mGuideWait-ddt")]),
        B(gg() + [st(3), CMPV("Pickup.Count", 0, 0), CMPV("mGuideWait", 3, 0), CMPV("mGuideCrate", 0, 0), CMPV("mPX", 2, 210)],
          [SETV("mIdSeq", "mIdSeq+1"), CREATE("Pickup", "Actors", 0, 0), ANIM("Pickup", "crate"),
           SIV("Pickup", "id", "mIdSeq"), SIV("Pickup", "progress", 0.02), SIV("Pickup", "duration", 3.3),
           SIV("Pickup", "lane", "clamp(mPX+85,76,344)"), SIV("Pickup", "isCrate", 1), SIV("Pickup", "training", 1),
           SIV("Pickup", "collected", 0), SETV("mGuideWait", 0.9)]),
        B(gg() + [st(3), CMPV("Pickup.Count", 0, 0), CMPV("mGuideWait", 3, 0), CMPV("mGuideCrate", 0, 0), CMPV("mPX", 5, 210)],
          [SETV("mIdSeq", "mIdSeq+1"), CREATE("Pickup", "Actors", 0, 0), ANIM("Pickup", "crate"),
           SIV("Pickup", "id", "mIdSeq"), SIV("Pickup", "progress", 0.02), SIV("Pickup", "duration", 3.3),
           SIV("Pickup", "lane", "clamp(mPX-85,76,344)"), SIV("Pickup", "isCrate", 1), SIV("Pickup", "training", 1),
           SIV("Pickup", "collected", 0), SETV("mGuideWait", 0.9)]),
        B(gg() + [st(3), CMPV("Pickup.Count", 0, 0), CMPV("mGuideWait", 3, 0), CMPV("mGuideCrate", 0, 1), CMPV("mPX", 2, 210)],
          [SETV("mIdSeq", "mIdSeq+1"), CREATE("Pickup", "Actors", 0, 0), ANIM("Pickup", "coin"),
           SIV("Pickup", "id", "mIdSeq"), SIV("Pickup", "progress", 0.02), SIV("Pickup", "duration", 3.3),
           SIV("Pickup", "lane", "clamp(mPX+85,76,344)"), SIV("Pickup", "isCrate", 0), SIV("Pickup", "training", 1),
           SIV("Pickup", "collected", 0), SETV("mGuideWait", 0.9)]),
        B(gg() + [st(3), CMPV("Pickup.Count", 0, 0), CMPV("mGuideWait", 3, 0), CMPV("mGuideCrate", 0, 1), CMPV("mPX", 5, 210)],
          [SETV("mIdSeq", "mIdSeq+1"), CREATE("Pickup", "Actors", 0, 0), ANIM("Pickup", "coin"),
           SIV("Pickup", "id", "mIdSeq"), SIV("Pickup", "progress", 0.02), SIV("Pickup", "duration", 3.3),
           SIV("Pickup", "lane", "clamp(mPX-85,76,344)"), SIV("Pickup", "isCrate", 0), SIV("Pickup", "training", 1),
           SIV("Pickup", "collected", 0), SETV("mGuideWait", 0.9)]),
        B(gg() + [st(3), IV("Pickup", "training", 0, 1)],
          [SIV("Pickup", "prev", "progress"), SIV("Pickup", "progress", "progress+ddt/duration"),
           SIV("Pickup", "dist", "abs(lane-mPX)")]),
        B(gg() + [st(3), IV("Pickup", "training", 0, 1), IV("Pickup", "prev", 2, 0.95), IV("Pickup", "progress", 5, 0.95),
                  IV("Pickup", "dist", 2, 73), IV("Pickup", "isCrate", 0, 1)] + t_arma[0],
          [SETV("mGuideCrate", 1), SETV("mBonusWeapon", 2), SETV("mWeaponBuff", 10), DESTROY("Pickup")] + t_arma[1]),
        B(gg() + [st(3), IV("Pickup", "training", 0, 1), IV("Pickup", "prev", 2, 0.95), IV("Pickup", "progress", 5, 0.95),
                  IV("Pickup", "dist", 2, 58), IV("Pickup", "isCrate", 0, 0)] + t_moneda[0],
          [SETV("mGuideCoin", 1), DESTROY("Pickup")] + t_moneda[1]),
        B(gg() + [st(3), IV("Pickup", "progress", 4, 1.06)], [DESTROY("Pickup")]),
        B(gg() + [st(3), CMPV("mGuideCrate", 0, 1), CMPV("mGuideCoin", 0, 1)], [SETV("mGuideReady", "mGuideReady+ddt")]),
        B(gg() + [st(3), CMPV("mGuideReady", 4, 1.2)], next_stage(4) + [
            SETV("mTunnel", 1), SETV("mTunnelT", 0), SETV("mTunnelTrain", 1), SETV("mTunnelL", 0),
            SETV("mTunnelLeft", 0)]),
    ]))
    # the training tunnel ends the tutorial (HTML endTunnel: training -> finishGuidedMission)
    ev.append(G("Guided finish", [
        B([TICK(), CMPV("mEndTunnel", 0, 1), CMPV("mTunnelTrain", 0, 1)] + TOAST("game", "TUTORIAL SUPERADO · OLEADA 1", 2.1)[0],
          finish_actions() + TOAST("game", "TUTORIAL SUPERADO · OLEADA 1", 2.1)[1]),
    ]))
    return ev
