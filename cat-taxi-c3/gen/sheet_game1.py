"""Game sheet, part 1: mission start, per-wave setup, player movement, wave timeline, tunnel, victory, defeat, pause.
HTML lines: startMission 357, updateMission 440-463, nextWave 383, endWave 386, tunnel 395-407, missionVictory 409,
damagePlayer 369, exitMission 85, enterPause/leavePause 83-84, playerMove 444-453."""
from ev import *
from ids import nid
from cfg import BANKS, THEMES, BOSSES

TAU = "6.283185307"
QUOTA_LO = {1: 3, 2: 4, 3: 4, 4: 3, 5: 4}     # level < 4   (HTML waveQuota, L356)
QUOTA_HI = {1: 6, 2: 9, 3: 5, 4: 8, 5: 5}     # level >= 4

def wave_setup_events():
    """Runs once when mSetupWave=1 (set by run start, nextWave). Quota, wave length, max alive, timers."""
    gate = [CMPV("mSetupWave", 0, 1)]
    ev = []
    for w in range(1, 6):
        ev.append(B(gate + [CMPV("mWave", 0, w), CMPV("mLevel", 2, 4), CMPV("mLevel", 1, 1)], [SETV("mQuota", QUOTA_LO[w] - 1)]))
        ev.append(B(gate + [CMPV("mWave", 0, w), CMPV("mLevel", 2, 4), CMPV("mLevel", 0, 1)], [SETV("mQuota", QUOTA_LO[w])]))
        ev.append(B(gate + [CMPV("mWave", 0, w), CMPV("mLevel", 5, 4)], [SETV("mQuota", QUOTA_HI[w])]))
    ev.append(B(gate + [CMPV("mWave", 0, 6)], [SETV("mQuota", 0)]))
    ev.append(B(gate + [CMPV("mLevel", 5, 4)], [SETV("mWaveDur", "10+5*mWave+3")]))
    ev.append(B(gate + [CMPV("mLevel", 2, 4)], [SETV("mWaveDur", "10+5*mWave")]))
    ev.append(B(gate + [CMPV("mWave", 0, 6)], [SETV("mMaxAlive", 1)]))
    ev.append(B(gate + [CMPV("mWave", 5, 2), CMPV("mWave", 3, 5)], [SETV("mMaxAlive", 3)]))   # waves 2..5
    ev.append(B(gate + [CMPV("mWave", 0, 1)], [SETV("mMaxAlive", 2)]))
    ev.append(B(gate, [SETV("mSetupWave", 0), SETV("mSpawned", 0), SETV("mBossAdds", 0), SETV("mWaveTime", 0),
                       SETV("mBossSpawned", 0), SETV("mBulletTimer", 0), SETV("mSpawnTimer", 0.75),
                       SETV("mPickupTimer", "3+2*random()")]))
    return ev

def bank_start_events():
    """startMission (HTML L357): level, theme, boss and balance of the chosen bank."""
    ev = []
    for k, (name, lvl, bal, theme, boss) in enumerate(BANKS):
        ev.append(B([CMPV("startReq", 0, 1), CMPV("startBank", 0, k)], [
            SETV("mBank", k), SETV("mLevel", f"bank{k}_lvl"), SETV("mBankBal", f"bank{k}_bal"),
            SETV("mTheme", THEMES.index(theme)), SETV("mBoss", BOSSES.index(boss))]))
    return ev

def run_init_actions(guide):
    """Initial values of one run (HTML startMission object literal, L358)."""
    return [
        SETV("startReq", 0), SETV("mActive", 1), SETV("mWave", 1), SETV("mWaveTime", 0), SETV("mSeconds", 0),
        SETV("mSpawned", 0), SETV("mBossAdds", 0), SETV("mBossSpawned", 0), SETV("mSpawnTimer", 0.65),
        SETV("mPickupTimer", 3), SETV("mBulletTimer", 0), SETV("mKillLoot", 0), SETV("mBankLoot", 0),
        SETV("mWeaponBuff", 0), SETV("mBonusWeapon", 0), SETV("mFlash", 0), SETV("mShake", 0),
        SETV("mPX", 210), SETV("mTarget", 210), SETV("mVX", 0), SETV("mInv", 0), SETV("mAuto", 0),
        SETV("mMaxHP", "100+25*car+upg_car*15"), SETV("mHP", "100+25*car+upg_car*15"),
        SETV("mTunnel", 0), SETV("mBonusV", 0), SETV("mEnded", 0), SETV("mDeathReason", 0),
        SETV("mGuide", guide), SETV("mGuideStage", 0), SETV("mGuideTime", 0), SETV("mGuideReady", 0),
        SETV("mGuideLeft", 0), SETV("mGuideRight", 0), SETV("mGuideHit", 0), SETV("mGuideAvoided", 0),
        SETV("mGuideCrate", 0), SETV("mGuideCoin", 0), SETV("mGuideRetry", 0), SETV("mGuideWait", 0),
        SETV("mGuideShotMade", 0), SETV("mSetupWave", 1), SETV("screen", 5), SETV("paused", 0),
        SETV("needSave", 0), SETV("popupOpen", 0), SETV("startToast", 0 if guide else 1),
    ]

def start_events():
    return [
        G("Run start: guided tutorial", [
            B([START(), CMPV("startReq", 0, 1), CMPV("startGuide", 0, 1)], run_init_actions(1) + [SETV("startGuide", 0)]),
        ]),
        G("Run start: normal", [
            B([START(), CMPV("startReq", 0, 1), CMPV("startGuide", 0, 0)], run_init_actions(0) + [SETV("startGuide", 0)]),
        ]),
        G("Run start: bank data", bank_start_events()),
    ]

def player_move_events():
    """HTML L444-453: keyboard/touch targets, lerp and clamp, lateral speed."""
    steer = [
        B([TICK(), CMPV("screen", 0, 5), CMPV("paused", 0, 0), CMPV("mTunnel", 0, 0), CMPV("mTouchUI", 0, 0),
           C("is-in-touch", "Touch")],
          [SETV("mAuto", 0), SETV("mTarget", "clamp((Touch.X-60)*1.1666667,64,356)")]),
        B([TICK(), CMPV("screen", 0, 5), CMPV("paused", 0, 0), CMPV("mTunnel", 0, 0),
           C("is-key-down", "Keyboard", key="37")],
          [SETV("mAuto", 0), SETV("mTarget", "clamp(mTarget-330*ddt,64,356)")]),
        B([TICK(), CMPV("screen", 0, 5), CMPV("paused", 0, 0), CMPV("mTunnel", 0, 0),
           C("is-key-down", "Keyboard", key="65")],
          [SETV("mAuto", 0), SETV("mTarget", "clamp(mTarget-330*ddt,64,356)")]),
        B([TICK(), CMPV("screen", 0, 5), CMPV("paused", 0, 0), CMPV("mTunnel", 0, 0),
           C("is-key-down", "Keyboard", key="39")],
          [SETV("mAuto", 0), SETV("mTarget", "clamp(mTarget+330*ddt,64,356)")]),
        B([TICK(), CMPV("screen", 0, 5), CMPV("paused", 0, 0), CMPV("mTunnel", 0, 0),
           C("is-key-down", "Keyboard", key="68")],
          [SETV("mAuto", 0), SETV("mTarget", "clamp(mTarget+330*ddt,64,356)")]),
    ]
    physics = [
        B([TICK(), CMPV("screen", 0, 5), CMPV("paused", 0, 0), CMPV("mTunnel", 0, 0)], [
            SETV("pOld", "mPX"),
            SETV("mPX", f"clamp(mPX+(mTarget-mPX)*(1-exp(-ddt*(9+2.25*own_speedDriver))),42,378)"),
            SETV("mVX", "mVX+(clamp((mPX-pOld)/max(0.002,ddt),-450,450)-mVX)*(1-exp(-ddt*10))"),
        ]),
    ]
    return [G("Steering (keyboard and touch)", steer), G("Player physics", physics)]

def timers_events():
    """HTML L443: seconds, wave clock, banners, flash, shake, invulnerability, weapon buff, bonus text."""
    gate = [TICK(), CMPV("screen", 0, 5), CMPV("paused", 0, 0), CMPV("mTunnel", 0, 0), CMPV("mGuide", 0, 0)]
    return [G("Timers", [
        B(gate, [SETV("mSeconds", "mSeconds+ddt"), SETV("mWaveTime", "mWaveTime+ddt"),
                 SETV("mFlash", "max(0,mFlash-ddt)"), SETV("mShake", "max(0,mShake-ddt*14)"),
                 SETV("mInv", "max(0,mInv-ddt)"), SETV("mWeaponBuff", "max(0,mWeaponBuff-ddt)")]),
        B([TICK(), CMPV("screen", 0, 5), CMPV("paused", 0, 0)], [SETV("mBonusT", "mBonusT+ddt")]),
        B([TICK(), CMPV("mBonusT", 4, 1.6)], [SETV("mBonusV", 0)]),
    ])]

def boss_spawn_events():
    """HTML L454: the boss appears in wave 6 once waveTime > 0.9."""
    return [G("Boss arrives", [
        B([TICK(), CMPV("screen", 0, 5), CMPV("mTunnel", 0, 0), CMPV("mWave", 0, 6), CMPV("mBossSpawned", 0, 0),
           CMPV("mWaveTime", 4, 0.9)],
          [SETV("mBossSpawned", 1), SETV("mBossAdds", "mBossAdds"), SETV("bossNow", 1)]),
    ])]

def wave_end_events():
    """HTML L462: wave ends when quota is spent, every enemy is dead and waveTime >= min(11, 8+level*0.35)."""
    return [G("Wave end", [
        B([TICK(), CMPV("screen", 0, 5), CMPV("mTunnel", 0, 0), CMPV("mWave", 2, 6), CMPV("mSpawned", 5, "mQuota"),
           CMPV("Enemy.Count", 0, 0), CMPV("mWaveTime", 5, "min(11,8+mLevel*0.35)")],
          [SETV("mEndNow", 1)]),
        B([TICK(), CMPV("mEndNow", 0, 1)], [SETV("mEndNow", 0), SETV("mTunnel", 1), SETV("mTunnelT", 0),
           SETV("mTunnelL", "round(max(0,mWaveDur-mWaveTime))"), SETV("mTunnelLeft", "round(max(0,mWaveDur-mWaveTime))"),
           SETV("mShake", 0), SETV("mTunnelTrain", 0)]),
    ])]

def tunnel_events():
    """HTML L395-407: the tunnel is a pause in the run; bonus = remaining seconds x2 kill money."""
    return [G("Tunnel", [
        B([TICK(), CMPV("mTunnel", 0, 1), CMPV("screen", 0, 5)],
          [SETV("mTunnelT", "mTunnelT+ddt"), SETV("mTunnelLeft", "max(0,mTunnelL*(1-mTunnelT/2.75))")]),
        B([TICK(), CMPV("mTunnel", 0, 1), CMPV("mTunnelT", 5, 2.75)], [SETV("mTunnel", 0), SETV("mEndTunnel", 1)]),
        # endTunnel: money bonus (killLoot += L*2), bonus text, next wave
        B([TICK(), CMPV("mEndTunnel", 0, 1), CMPV("mTunnelTrain", 0, 0)], [
            SETV("mEndTunnel", 0), SETV("mKillLoot", "mKillLoot+mTunnelL*2"), SETV("mBonusV", "mTunnelL*2"),
            SETV("mBonusT", 0), SETV("mWave", "min(6,mWave+1)"), SETV("mSetupWave", 1), SETV("mWaveTime", 0),
            SETV("mPickupTimer", "3+2*random()")]),
    ])]

def victory_defeat_events():
    """missionVictory (L409) and damagePlayer lethal (L369). Victory only from the boss death (hurt events)."""
    ev = [G("Victory (boss defeated)", [
        B([TICK(), CMPV("mEnded", 0, 1)], [SETV("mEnded", 2), SETV("mPerfect", 0),
           SETV("mReward", "mBankLoot+mKillLoot"), SETV("mRemain", "mBankBal-mBankLoot"),
           SETV("coins", "coins+mBankLoot+mKillLoot"), SETV("needSave", 1), SETV("screen", 8), GOTO("Results")]),
    ])]
    ev.append(G("Victory: bank state", bank_end_events()))
    ev.append(G("Defeat: explosion inside the lethal radius", [
        B([TICK(), CMPV("screen", 0, 5), CMPV("mTunnel", 0, 0), CMPV("mDeathNow", 0, 1)],
          [SETV("mHP", 0), SETV("mDeathReason", 1), SETV("screen", 7), SETV("paused", 1), SETV("mDeathNow", 0),
           LAYER_VIS("Defeat", 1)]),
    ]))
    return ev

def bank_end_events():
    """missionVictory bank update: remain = balance - bankLoot; level+1 when empty; next bank unlocked."""
    ev = []
    for k in range(len(BANKS)):
        base = [CMPV("mEnded", 0, 2), CMPV("mBank", 0, k)]
        ev.append(B(base + [CMPV("mRemain", 4, 0)], [SETV(f"bank{k}_bal", "mRemain"), SETV("selectedBank", k)]))
        ev.append(B(base + [CMPV("mRemain", 3, 0)], [SETV(f"bank{k}_bal", 0), SETV(f"bank{k}_lvl", f"min(100,bank{k}_lvl+1)"),
                                                     SETV("unlocked", f"max(unlocked,{min(14, k + 1)})"),
                                                     SETV("selectedBank", f"max(selectedBank,{min(14, k + 1)})")]))
    ev.append(B([CMPV("mEnded", 0, 2), CMPV("mBank", 0, 0), CMPV("gems", 2, 10)], [SETV("gems", 10)]))
    return ev

def pause_exit_events():
    """HTML L83-85 and the keyboard pause (P / Escape)."""
    return [G("Pause and exit", [
        B([C("on-key-pressed", "Keyboard", key="80"), CMPV("screen", 0, 5)], [SETV("screen", 6), SETV("paused", 1), LAYER_VIS("Pause", 1)]),
        B([C("on-key-pressed", "Keyboard", key="27"), CMPV("screen", 0, 5)], [SETV("screen", 6), SETV("paused", 1), LAYER_VIS("Pause", 1)]),
        B([C("on-key-pressed", "Keyboard", key="80"), CMPV("screen", 0, 6)], [SETV("screen", 5), SETV("paused", 0), LAYER_VIS("Pause", 0)]),
        B([C("on-key-pressed", "Keyboard", key="27"), CMPV("screen", 0, 6)], [SETV("screen", 5), SETV("paused", 0), LAYER_VIS("Pause", 0)]),
        click_game("game.resume", [SETV("screen", 5), SETV("paused", 0), LAYER_VIS("Pause", 0)], [CMPV("screen", 0, 6)]),
        click_game("game.quit", [SETV("screen", 1), SETV("paused", 0), SETV("mActive", 0), SETV("needSave", 1),
                                 LAYER_VIS("Pause", 0), GOTO("Map")], [CMPV("screen", 0, 6)]),
        click_game("game.continue", [SETV("gems", "gems-1"), SETV("mHP", "ceil(mMaxHP*0.5)"),
                                     SETV("mInv", 2), SETV("screen", 5), SETV("paused", 0), SETV("mDeathReason", 0),
                                     SETV("needSave", 1), LAYER_VIS("Defeat", 0), DESTROY("Shot")],
                   [CMPV("screen", 0, 7), CMPV("gems", 5, 1)]),
        click_game("game.giveup", [SETV("screen", 1), SETV("paused", 0), SETV("mActive", 0), SETV("needSave", 1),
                                   LAYER_VIS("Defeat", 0), GOTO("Map")], [CMPV("screen", 0, 7)]),
    ])]

def click_game(name, acts, extra=()):
    return B([TOUCH("Btn", "start"), IV("Btn", "id", 0, nid("btn." + name))] + list(extra), acts)
