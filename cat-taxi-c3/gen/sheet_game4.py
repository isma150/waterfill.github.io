"""Game sheet, part 4: targeting (HTML L483-486), shooting and damage (L371, hurtEnemy), auto-pilot (L446-452), lock (L483).
Pick semantics used: filters first, then PICK_LOWEST/PICK_HIGHEST (sub-event), then object actions on the picked instance."""
from ev import *
from ids import nid
from sheet_game2 import gate

def reset_events():
    """Clear per-tick flags before the aggregates run."""
    return [G("Per-tick reset", [
        B([TICK()], [SIV("Enemy", "isTarget", 0), SIV("Enemy", "pick", 0), SIV("Boss", "isTarget", 0),
                     SIV("Boss", "pick", 0), SETV("tBoss", 0), SETV("tAny", 0), SETV("aDanger", 0),
                     SETV("aPrize", 0), SETV("aBoss", 0), SETV("aEnemy", 0), SETV("aLock", 0)]),
    ])]

def target_events():
    """HTML L485: boss first, else the nearest enemy in the window (d in (-0.26,0.28), |lane-x|<100)."""
    win_e = [IV("Enemy", "d", 4, -0.26), IV("Enemy", "d", 2, 0.28), IV("Enemy", "dist", 2, 100)]
    win_b = [IV("Boss", "d", 4, -0.26), IV("Boss", "d", 2, 0.28), IV("Boss", "dist", 2, 100)]
    return [G("Choose target", [
        B(gate() + [CMPV("mBossSpawned", 0, 1)] + win_b,
          [SIV("Boss", "isTarget", 1), SETV("tBoss", 1), SETV("tSX", "Boss.sx")]),
        B(gate() + [CMPV("tBoss", 0, 0)] + win_e + [PICK_LOWEST("Enemy", "dist")],
          [SIV("Enemy", "isTarget", 1), SETV("tAny", 1), SETV("tSX", "Enemy.sx")]),
    ])]

def weapon_events():
    """Active weapon (bonus weapon while the crate buff lasts), rate, base and damage (HTML L484, L371)."""
    buff = "min(1,ceil(mWeaponBuff))"
    ev = [G("Active weapon", [
        B([TICK()], [SETV("mWeapon", f"weapon+{buff}*(mBonusWeapon-weapon)")]),
    ])]
    rows = []
    for k in range(4):
        base = {0: 3, 1: 12, 2: 4, 3: 2.5}[k]
        rate = {0: 6.8, 1: 1.1, 2: 3.2, 3: 11.2}[k]
        upg = ["upg_pistol", "upg_bomb", "upg_shot", "upg_machine"][k]
        rows.append(B([TICK(), CMPV("mWeapon", 0, k)],
                      [SETV("mRate", f"{rate}*(1+0.15*{buff})"), SETV("mBase", base),
                       SETV("mDmg", f"{base}*(1+0.36*{upg})*(1+min(0.3,(plevel-1)*0.025))*(1+0.4*{buff})"),
                       SETV("mHit", f"{base}*(1+0.36*{upg})*(1+min(0.3,(plevel-1)*0.025))*(1+0.4*{buff})*" + ("2.2" if k == 2 else "1"))]))
    ev.append(G("Weapon numbers", rows))
    return ev

def shoot_events():
    """HTML L486 and L371. Non-bomb weapons hit the target once. The bomb hits every enemy within 75 px of the target
    (the boss too), using the inAoe flags written just before."""
    ready = gate() + [CMPV("mBulletTimer", 3, 0)]
    not_bomb = [CMPV("mWeapon", 1, 1)]
    bomb = [CMPV("mWeapon", 0, 1)]
    ev = [G("Shooting timer", [B([TICK()], [SETV("mBulletTimer", "mBulletTimer-ddt")])])]
    ev.append(G("Hit target (not bomb)", [
        B(ready + not_bomb + [CMPV("tBoss", 0, 1)], [SETV("mBulletTimer", "1/mRate"), SIV("Boss", "hp", "hp-mHit")]),
        B(ready + not_bomb + [CMPV("tBoss", 0, 0), CMPV("tAny", 0, 1), IV("Enemy", "isTarget", 0, 1)],
          [SETV("mBulletTimer", "1/mRate"), SIV("Enemy", "hp", "hp-mHit")]),
    ]))
    ev.append(G("Bomb splash", [
        B(gate() + bomb, [SIV("Enemy", "inAoe", "min(1,ceil(max(0,75-abs(sx-tSX))))"),
                          SIV("Boss", "inAoe", "min(1,ceil(max(0,75-abs(sx-tSX))))")]),
        B(ready + bomb + [CMPV("tBoss", 0, 1)], [SETV("mBulletTimer", "1/mRate")]),
        B(ready + bomb + [CMPV("tBoss", 0, 0), CMPV("tAny", 0, 1)], [SETV("mBulletTimer", "1/mRate")]),
        B(ready + bomb + [IV("Enemy", "inAoe", 0, 1)], [SIV("Enemy", "hp", "hp-mDmg")]),
        B(ready + bomb + [CMPV("mBossSpawned", 0, 1), IV("Boss", "inAoe", 0, 1)], [SIV("Boss", "hp", "hp-mDmg")]),
    ]))
    ev.append(G("Idle timer", [
        B(gate() + [CMPV("tBoss", 0, 0), CMPV("tAny", 0, 0)], [SETV("mBulletTimer", "min(0,mBulletTimer)")]),
    ]))
    return ev

def auto_events():
    """HTML L446-452: danger (dynamite) > prize (crate) > boss > nearest enemy > idle sway."""
    on = gate() + [CMPV("mAuto", 0, 1)]
    ev = []
    ev.append(G("Auto: danger", [
        B(on + [IV("Shot", "exploded", 0, 0), IV("Shot", "dist", 2, 94), IV("Shot", "d", 4, 0.05)] +
          [PICK_LOWEST("Shot", "d")],
          [SETV("aDanger", 1), SETV("dangerXl", "Shot.xl")]),
    ]))
    ev.append(G("Auto: prize", [
        B(on + [CMPV("aDanger", 0, 0), IV("Pickup", "isCrate", 0, 1), IV("Pickup", "progress", 4, 0.5),
                IV("Pickup", "progress", 2, 1), IV("Pickup", "dist", 2, 175)] + [PICK_HIGHEST("Pickup", "progress")],
          [SETV("aPrize", 1), SETV("prizeX", "Pickup.lane")]),
    ]))
    ev.append(G("Auto: boss or nearest enemy", [
        B(on + [CMPV("mBossSpawned", 0, 1), IV("Boss", "d", 4, -0.4)], [SETV("aBoss", 1), SETV("bossLane", "Boss.lane")]),
        B(on + [CMPV("aBoss", 0, 0), IV("Enemy", "d", 4, -0.4)] + [PICK_LOWEST("Enemy", "dist")],
          [SETV("aEnemy", 1), SETV("enemyLane", "Enemy.lane")]),
    ]))
    # the target: priority order is encoded in the conditions (each aux flag excludes the lower ones)
    tgt = []
    tgt.append(B(on + [CMPV("aDanger", 0, 1), CMPV("mPX", 5, "dangerXl")], [SETV("mTarget", "clamp(dangerXl+123,58,362)")]))
    tgt.append(B(on + [CMPV("aDanger", 0, 1), CMPV("mPX", 2, "dangerXl")], [SETV("mTarget", "clamp(dangerXl-123,58,362)")]))
    tgt.append(B(on + [CMPV("aDanger", 0, 0), CMPV("aPrize", 0, 1)], [SETV("mTarget", "clamp(prizeX,64,356)")]))
    tgt.append(B(on + [CMPV("aDanger", 0, 0), CMPV("aPrize", 0, 0), CMPV("aBoss", 0, 1), CMPV("bossLane", 2, "mPX")],
                 [SETV("mTarget", "clamp(bossLane+70,58,362)")]))
    tgt.append(B(on + [CMPV("aDanger", 0, 0), CMPV("aPrize", 0, 0), CMPV("aBoss", 0, 1), CMPV("bossLane", 5, "mPX")],
                 [SETV("mTarget", "clamp(bossLane-70,58,362)")]))
    tgt.append(B(on + [CMPV("aDanger", 0, 0), CMPV("aPrize", 0, 0), CMPV("aBoss", 0, 0), CMPV("aEnemy", 0, 1),
                       CMPV("enemyLane", 2, "mPX")], [SETV("mTarget", "clamp(enemyLane+70,58,362)")]))
    tgt.append(B(on + [CMPV("aDanger", 0, 0), CMPV("aPrize", 0, 0), CMPV("aBoss", 0, 0), CMPV("aEnemy", 0, 1),
                       CMPV("enemyLane", 5, "mPX")], [SETV("mTarget", "clamp(enemyLane-70,58,362)")]))
    tgt.append(B(on + [CMPV("aDanger", 0, 0), CMPV("aPrize", 0, 0), CMPV("aBoss", 0, 0), CMPV("aEnemy", 0, 0)],
                 [SETV("mTarget", "clamp(210+sin(clock*1.12)*57,64,356)")]))
    ev.append(G("Auto: steering target", tgt))
    return ev

def lock_events():
    """HTML L483: the lock marker sits on the nearest enemy in (-0.4,0.2) within 130 px."""
    return [G("Lock marker", [
        B(gate() + [IV("Enemy", "d", 4, -0.4), IV("Enemy", "d", 2, 0.2), IV("Enemy", "dist", 2, 130)] +
          [PICK_LOWEST("Enemy", "dist")], [SIV("Enemy", "pick", 1), SETV("aLock", 1)]),
        B([TICK(), CMPV("aLock", 0, 0), IV("Shape", "id", 0, nid("game.lock"))], [VIS("Shape", False)]),
        B([TICK(), CMPV("aLock", 0, 1), IV("Shape", "id", 0, nid("game.lock")), IV("Enemy", "pick", 0, 1)],
          [VIS("Shape", True), POS("Shape", "60+Enemy.sx*0.857142857", "Enemy.sy*0.857142857")]),
    ])]
