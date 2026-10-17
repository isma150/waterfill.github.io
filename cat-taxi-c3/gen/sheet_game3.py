"""Game sheet, part 3: dynamite, pickups, kills, targeting, shooting, auto-pilot, lock marker.
HTML: throwFromEnemy 380, shots 487-498, pickups 500-507, hurtEnemy 370, takePickup 375, shootAt 371,
targeting 483-486, auto-pilot 446-452.
Rules: (see PROGRESS.md) one CREATE per event; values for a new instance are written right after it is created;
booleans are written as min(1,ceil(x)) so no comparison operators are needed inside expressions."""
from ev import *
from ids import nid
from sheet_common import TOAST, TOASTX
from sheet_game2 import gate

BULLET_RATE = {0: 6.8, 1: 1.1, 2: 3.2, 3: 11.2}
BULLET_BASE = {0: 3, 1: 12, 2: 4, 3: 2.5}
UPG_VAR = {0: "upg_pistol", 1: "upg_bomb", 2: "upg_shot", 3: "upg_machine"}
TH = "0.052"

def pos_layout(objname, x_expr, y_expr):
    """HTML units -> layout units: X = 60 + x*6/7, Y = y*6/7."""
    return POS(objname, f"60+({x_expr})*0.857142857", f"({y_expr})*0.857142857")

def dynamite_events():
    ev = []
    # enemies throw (HTML L477-479): extra throw first (it reads fire before the main throw resets it)
    throw_ok = gate() + [IV("Enemy", "fire", 3, 0), IV("Enemy", "d", 4, -0.16), IV("Enemy", "d", 2, -0.023)]
    ev.append(G("Extra dynamite (level 3+, wave 3+, 13%)", [
        B(throw_ok + [CMPV("mLevel", 4, 2), CMPV("mWave", 5, 3), CMPV("rThrow", 2, 0.13)],
          [SETV("thLane", "Enemy.lane"), SETV("thD", "Enemy.d"), CREATE("Shot", "Actors", 0, 0), ANIM("Shot", "dyn")]
          + _shot_init("thLane", "thD", "1.03+0.19*random()", "0.52+0.12*random()", "0")),
    ]))
    ev.append(G("Dynamite from enemies", [
        B(throw_ok, [
            SIV("Enemy", "fire", "(3.6+1.6*random())/(1+(mLevel-1)*0.04+(mWave-1)*0.06)"),
            SETV("thLane", "Enemy.lane"), SETV("thD", "Enemy.d"),
            CREATE("Shot", "Actors", 0, 0), ANIM("Shot", "dyn")] + _shot_init("thLane", "thD", "1.03+0.19*random()", "0.52+0.12*random()", "0")),
    ]))
    # boss throws (HTML L477-479 for the boss: phase divisor 1.35 / 1.15 / 1)
    bthrow = gate() + [CMPV("mBossSpawned", 0, 1), IV("Boss", "fire", 3, 0), IV("Boss", "d", 4, -0.16), IV("Boss", "d", 2, -0.023)]
    for ph, div in [(1, "1"), (2, "1.15"), (3, "1.35")]:
        ev.append(G(f"Boss dynamite phase {ph}", [
            B(bthrow + [IV("Boss", "phase", 0, ph)],
              [SIV("Boss", "fire", f"(2.9+1.0*random())/{div}/(1+(mLevel-1)*0.04+(mWave-1)*0.06)"),
               SETV("thLane", "Boss.lane"), SETV("thD", "Boss.d"),
               CREATE("Shot", "Actors", 0, 0), ANIM("Shot", "dyn")]
              + _shot_init("thLane", "thD", "1.03+0.19*random()", "0.52+0.12*random()", "0")),
        ]))
    return ev

def _shot_init(lane_var, d_var, fly, dl, training):
    """Runs right after CREATE Shot: the new Shot is the picked instance."""
    return [
        SETV("mIdSeq", "mIdSeq+1"),
        SIV("Shot", "id", "mIdSeq"),
        SIV("Shot", "x0", lane_var), SIV("Shot", "d0", d_var),
        SIV("Shot", "xl", "clamp(mPX+random(-42,42),64,356)"),
        SIV("Shot", "dl", f"max({dl},{d_var}+0.22)"),
        SIV("Shot", "fly", fly), SIV("Shot", "age", 0), SIV("Shot", "exploded", 0), SIV("Shot", "done", 0),
        SIV("Shot", "training", 0), SIV("Shot", "landed", 0), SIV("Shot", "d", d_var),
        # the warning on the road where it will land: read the shot's values, then create Warn
        SETV("wxl", "Shot.xl"), SETV("wdl", "Shot.dl"), SETV("wid", "Shot.id"),
        CREATE("Warn", "Actors", 0, 0), ANIM("Warn", "warn"),
        SIV("Warn", "owner", "wid"),
        SIV("Warn", "sx", "210+(wxl-210)*(148+90*pow(clamp(wdl,0,1),1.06))/148"),
        SIV("Warn", "sy", "319+441*pow(min(max(wdl,0),1.15),1.22)+100*min(wdl,0)"),
        SIV("Warn", "sc", "0.92*(1+0.6*max(clamp(wdl,-0.5,1.15),0)+1.5*min(clamp(wdl,-0.5,1.15),0))"),
    ]

def shot_events():
    """HTML L487-498: flight, landing and roll toward the car, explosion, lethal radius 64 px."""
    upd = gate()
    ev = []
    ev.append(G("Shot flight", [
        B(upd, [SIV("Shot", "age", "age+ddt")]),
        B(upd + [IV("Shot", "age", 5, "fly")], [SIV("Shot", "landed", 1)]),
        B(upd, [SIV("Shot", "d", "d0+(dl-d0)*min(1,age/fly)-0.26*max(0,age-fly)"),
                SIV("Shot", "dist", "abs(xl-mPX)"),
                SIV("Shot", "sx", "210+(x0+(xl-x0)*min(1,age/fly)-210)*(148+90*pow(clamp(d,0,1),1.06))/148"),
                SIV("Shot", "sy", "319+441*pow(min(max(d,0),1.15),1.22)+100*min(d,0)"
                                  "-(sin(3.14159*min(1,age/fly))*150+(1-min(1,age/fly))*24)*0.92*(1+0.6*max(clamp(d,-0.5,1.15),0)+1.5*min(clamp(d,-0.5,1.15),0))*(1-landed)"),
                SIV("Shot", "sc", "0.92*(1+0.6*max(clamp(d,-0.5,1.15),0)+1.5*min(clamp(d,-0.5,1.15),0))")]),
    ]))
    ev.append(G("Shot lethal check", [
        B(upd + [IV("Shot", "exploded", 0, 0), IV("Shot", "age", 5, "fly"), IV("Shot", "d", 3, 0.052),
                 IV("Shot", "dist", 2, 64)],
          [SETV("mDeathNow", 1)]),
    ]))
    ev.append(G("Shot explodes", [
        B(upd + [IV("Shot", "exploded", 0, 0), IV("Shot", "age", 5, "fly"), IV("Shot", "d", 3, 0.052)],
          [SETV("bx", "Shot.sx"), SETV("by", "Shot.sy"), SIV("Shot", "exploded", 1),
           CREATE("Fx", "Actors", 0, 0), ANIM("Fx", "blast"), SIV("Fx", "life", 0.66), SIV("Fx", "t", 0)]),
        B(upd + [IV("Shot", "exploded", 0, 1)], [DESTROY("Shot")]),
    ]))
    ev.append(G("Shot expires", [
        B(upd + [IV("Shot", "age", 4, "fly+4")], [DESTROY("Shot")]),
    ]))
    return ev

def pickup_events():
    """HTML L500-507 and spawnPickup L372-374. Coins come in groups of three; extra coins are created first."""
    gt = gate() + [CMPV("mWave", 2, 6)]
    ev = []
    ev.append(G("Pickup timer", [B(gt, [SETV("mPickupTimer", "mPickupTimer-ddt")])]))
    ev.append(G("Pickup lane", [B(gt + [CMPV("mPickupTimer", 3, 0)], [SETV("rPick", "random()"), SETV("rLane", "84+252*random()")])]))
    timer_ok = gt + [CMPV("mPickupTimer", 3, 0)]
    coin_group = [
        B(timer_ok + [CMPV("rPick", 5, 0.43)],
          [SETV("mIdSeq", "mIdSeq+1"), CREATE("Pickup", "Actors", 0, 0), ANIM("Pickup", "coin"),
           SIV("Pickup", "id", "mIdSeq"), SIV("Pickup", "progress", -0.12), SIV("Pickup", "duration", 2.25),
           SIV("Pickup", "amount", 25), SIV("Pickup", "lane", "clamp(rLane+random(-12,12),64,356)"),
           SIV("Pickup", "isCrate", 0), SIV("Pickup", "training", 0), SIV("Pickup", "collected", 0)]),
        B(timer_ok + [CMPV("rPick", 5, 0.43)],
          [SETV("mIdSeq", "mIdSeq+1"), CREATE("Pickup", "Actors", 0, 0), ANIM("Pickup", "coin"),
           SIV("Pickup", "id", "mIdSeq"), SIV("Pickup", "progress", -0.24), SIV("Pickup", "duration", 2.25),
           SIV("Pickup", "amount", 25), SIV("Pickup", "lane", "clamp(rLane+random(-12,12),64,356)"),
           SIV("Pickup", "isCrate", 0), SIV("Pickup", "training", 0), SIV("Pickup", "collected", 0)]),
        B(timer_ok + [CMPV("rPick", 5, 0.43)],
          [SETV("mIdSeq", "mIdSeq+1"), CREATE("Pickup", "Actors", 0, 0), ANIM("Pickup", "coin"),
           SIV("Pickup", "id", "mIdSeq"), SIV("Pickup", "progress", 0.02), SIV("Pickup", "duration", 2.25),
           SIV("Pickup", "amount", 25), SIV("Pickup", "lane", "rLane"),
           SIV("Pickup", "isCrate", 0), SIV("Pickup", "training", 0), SIV("Pickup", "collected", 0)]),
    ]
    crate = [
        B(timer_ok + [CMPV("rPick", 2, 0.43)],
          [SETV("mIdSeq", "mIdSeq+1"), CREATE("Pickup", "Actors", 0, 0), ANIM("Pickup", "crate"),
           SIV("Pickup", "id", "mIdSeq"), SIV("Pickup", "progress", 0.02), SIV("Pickup", "duration", 2.7),
           SIV("Pickup", "amount", 6), SIV("Pickup", "lane", "rLane"),
           SIV("Pickup", "isCrate", 1), SIV("Pickup", "training", 0), SIV("Pickup", "collected", 0)]),
    ]
    ev.append(G("Pickups spawn (coins first, then the main one)", coin_group + crate))
    ev.append(G("Pickup reset", [B(timer_ok, [SETV("mPickupTimer", "3+1.7*random()")])]))
    upd = gate()
    ev.append(G("Pickup movement", [
        B(upd, [SIV("Pickup", "prev", "progress"), SIV("Pickup", "progress", "progress+ddt/duration"),
                SIV("Pickup", "dist", "abs(lane-mPX)")]),
        B(upd, [SIV("Pickup", "sx", "210+(lane-210)*(148+90*pow(clamp(1-clamp(progress,0,1.15),0,1),1.06))/148"),
                SIV("Pickup", "sy", "319+441*pow(min(max(1-clamp(progress,0,1.15),0),1.15),1.22)+100*min(1-clamp(progress,0,1.15),0)"),
                SIV("Pickup", "sc", "0.92*(1+0.6*max(clamp(1-clamp(progress,0,1.15),-0.5,1.15),0)+1.5*min(clamp(1-clamp(progress,0,1.15),-0.5,1.15),0))")]),
    ]))
    coin_hit = upd + [IV("Pickup", "prev", 2, 0.95), IV("Pickup", "progress", 5, 0.95), IV("Pickup", "dist", 2, 58),
                      IV("Pickup", "isCrate", 0, 0)]
    # HTML takePickup L378: '+add COINS' (add = min(amount, bank left)) or 'BANK EMPTY' (.65 s); read before the loot update
    coin_text = '"+"&min(Pickup.amount,mBankBal-mBankLoot)&" COINS"'
    ev.append(G("Pickup coin toast", [
        B(coin_hit + [CMPX("mBankBal-mBankLoot", 4, 0)] + TOASTX("game", coin_text, 0.65)[0],
          TOASTX("game", coin_text, 0.65)[1]),
        B(coin_hit + [CMPX("mBankBal-mBankLoot", 3, 0)] + TOAST("game", "BANK EMPTY", 0.65)[0],
          TOAST("game", "BANK EMPTY", 0.65)[1]),
    ]))
    ev.append(G("Pickup collected", [
        B(upd + [IV("Pickup", "prev", 2, 0.95), IV("Pickup", "progress", 5, 0.95), IV("Pickup", "dist", 2, 58),
                 IV("Pickup", "isCrate", 0, 0)],
          [SETV("mBankLoot", "mBankLoot+min(Pickup.amount,mBankBal-mBankLoot)"), SETV("xp", "xp+1"),
           DESTROY("Pickup")]),
        B(upd + [IV("Pickup", "prev", 2, 0.95), IV("Pickup", "progress", 5, 0.95), IV("Pickup", "dist", 2, 73),
                 IV("Pickup", "isCrate", 0, 1)],
          [SETV("mWeaponBuff", 9), SETV("mBonusWeapon", "1+floor(random(0,3))"), SETV("mWeaponToast", 1),
           DESTROY("Pickup")]),
        B(upd + [IV("Pickup", "progress", 4, 1.06)], [DESTROY("Pickup")]),
    ]))
    # HTML takePickup L377: 'WEAPON: X!' (1.15 s). Bonus 1 bomb, 2 shot, 3 machine (same order as the HUD icons).
    weapon_toasts = []
    for k, name in [(1, "BOMB"), (2, "SHOT"), (3, "MACHINE")]:
        tc, ta = TOAST("game", f"WEAPON: {name}!", 1.15)
        weapon_toasts.append(B([TICK(), CMPV("mWeaponToast", 0, 1), CMPV("mBonusWeapon", 0, k)] + tc,
                               ta + [SETV("mWeaponToast", 0)]))
    ev.append(G("Pickup weapon toast", weapon_toasts))
    return ev

def kill_events():
    """HTML hurtEnemy L370: reward, xp, coin drop (26%), boss -> victory. Drops are separate events (one CREATE each)."""
    ev = []
    ev.append(G("Enemy killed", [
        B(gate() + [IV("Enemy", "hp", 3, 0), IV("Enemy", "training", 0, 0)],
          [SETV("mKillLoot", "mKillLoot+round((23+7*mLevel+3*mWave)*(1+0.2*own_luckyPet))"),
           SETV("xp", "xp+4"), SETV("kx", "Enemy.sx"), SETV("ky", "Enemy.sy"), SETV("kDrop", 1),
           SETV("rDrop", "random()"), DESTROY("Enemy")]),
    ]))
    ev.append(G("Enemy coin drop", [
        B(gate() + [CMPV("kDrop", 0, 1), CMPV("rDrop", 2, 0.26)],
          [SETV("mIdSeq", "mIdSeq+1"), CREATE("Pickup", "Actors", 0, 0), ANIM("Pickup", "coin"),
           SIV("Pickup", "id", "mIdSeq"), SIV("Pickup", "progress", 0.02), SIV("Pickup", "duration", 2.25),
           SIV("Pickup", "amount", 50), SIV("Pickup", "lane", "clamp(kx+random(-32,32),60,365)"),
           SIV("Pickup", "isCrate", 0), SIV("Pickup", "training", 0), SIV("Pickup", "collected", 0)]),
        B(gate() + [CMPV("kDrop", 0, 1)], [SETV("kDrop", 0)]),
    ]))
    ev.append(G("Boss killed", [
        B(gate() + [IV("Boss", "hp", 3, 0)],
          [SETV("mKillLoot", "mKillLoot+110+42*mLevel"), SETV("xp", "xp+30"), SETV("mEnded", 1), SETV("mBossRatio", 0),
           DESTROY("Boss")]),
    ]))
    return ev

def level_events():
    """HTML gainXp L385: while xp >= 60+20*plevel: xp -= need, plevel++, toast 'LEVEL n!  +2.5% POWER' (1.2 s).
    One level per tick is enough: a single xp gain is at most 30, and the next need is at least 80."""
    tc, ta = TOASTX("game", '"LEVEL "&plevel&"!  +2.5% POWER"', 1.2)
    return [G("Level up", [
        B([TICK(), CMPX("xp", 5, "60+20*plevel")] + tc,
          [SETV("xp", "xp-(60+20*plevel)"), SETV("plevel", "plevel+1"), SETV("needSave", 1)] + ta),
    ])]
