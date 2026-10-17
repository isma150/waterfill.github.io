"""Game sheet, part 2: spawning, enemy and boss AI, dynamite throws.
HTML: enemySpawn 361-368, spawn cadence 454-463, AI 464-482, throwFromEnemy 380-382.
Engine rules used (see PROGRESS.md): System actions run once per event; CREATE makes one instance per event
and then the picked instance is the new one, so values are written to the new instance right after CREATE."""
from ev import *

def gate():
    """Normal combat only: in game, not paused, not in a tunnel, not in the guided tutorial."""
    return [TICK(), CMPV("screen", 0, 5), CMPV("paused", 0, 0), CMPV("mTunnel", 0, 0), CMPV("mGuide", 0, 0)]

def proj(obj, lane="lane", d="d"):
    """sx, sy, sc (HTML laneAt, groundY, perspectiveScale). Written without conditionals."""
    c = f"clamp({d},-0.5,1.15)"
    return [
        SIV(obj, "sx", f"210+({lane}-210)*(148+90*pow(clamp({d},0,1),1.06))/148"),
        SIV(obj, "sy", f"319+441*pow(min(max({d},0),1.15),1.22)+100*min({d},0)"),
        SIV(obj, "sc", f"0.92*(1+0.6*max({c},0)+1.5*min({c},0))"),
    ]

def enemy_ai_events():
    ev = []
    ev.append(G("Enemy projection", [B([TICK()], [SIV("Enemy", "dist", "abs(lane-mPX)")] + proj("Enemy"))]))
    ev.append(G("Enemy clocks", [
        B(gate(), [SIV("Enemy", "age", "age+ddt"), SIV("Enemy", "fire", "fire-ddt"),
                   SIV("Enemy", "dodgeCd", "dodgeCd-ddt")]),
    ]))
    # HTML L465: when the cooldown ends, a roll decides if the car moves away from the taxi
    ev.append(G("Enemy dodge", [
        B(gate() + [IV("Enemy", "dodgeCd", 3, 0), IV("Enemy", "d", 4, -0.22), IV("Enemy", "dist", 2, 130)],
          [SIV("Enemy", "dodgeCd", "0.9+0.6*random()-(mWave-1)*0.08"), SIV("Enemy", "roll", "random()"),
           SIV("Enemy", "dodgeNow", 1)]),
        B(gate() + [IV("Enemy", "dodgeNow", 0, 1), IV("Enemy", "roll", 2, "dodge"), IV("Enemy", "lane", 5, "mPX")],
          [SIV("Enemy", "laneFrom", "lane"), SIV("Enemy", "laneTo", "clamp(lane+55+25*random(),70,350)"),
           SIV("Enemy", "laneT", 0), SIV("Enemy", "laneDur", 0.45), SIV("Enemy", "dodgeNow", 0)]),
        B(gate() + [IV("Enemy", "dodgeNow", 0, 1), IV("Enemy", "roll", 2, "dodge"), IV("Enemy", "lane", 2, "mPX")],
          [SIV("Enemy", "laneFrom", "lane"), SIV("Enemy", "laneTo", "clamp(lane-55-25*random(),70,350)"),
           SIV("Enemy", "laneT", 0), SIV("Enemy", "laneDur", 0.45), SIV("Enemy", "dodgeNow", 0)]),
        B(gate() + [IV("Enemy", "dodgeNow", 0, 1)], [SIV("Enemy", "dodgeNow", 0)]),
    ]))
    # HTML L466: smoothstep lane motion
    ev.append(G("Enemy lane motion", [
        B(gate(), [SIV("Enemy", "laneT", "min(1,laneT+ddt/laneDur)"),
                   SIV("Enemy", "lane", "laneFrom+(laneTo-laneFrom)*(laneT*laneT*(3-2*laneT))")]),
    ]))
    # HTML L474-475 and L481: approach, arrive, hover-attack, never overtake
    ev.append(G("Enemy approach and attack", [
        B(gate() + [IV("Enemy", "state", 0, 0)], [SIV("Enemy", "d", "min(hoverD,d+ddt*vd)")]),
        B(gate() + [IV("Enemy", "state", 0, 0), IV("Enemy", "d", 5, "hoverD")],
          [SIV("Enemy", "state", 1), SIV("Enemy", "hold", 0)]),
        B(gate() + [IV("Enemy", "state", 0, 1)],
          [SIV("Enemy", "hold", "hold+ddt"), SIV("Enemy", "d", "clamp(hoverD+sin(age*1.3)*0.012,-0.13,-0.023)")]),
        B(gate(), [SIV("Enemy", "d", "min(d,-0.023)")]),
    ]))
    return ev

def boss_ai_events():
    ev = []
    ev.append(G("Boss projection", [
        B([TICK(), CMPV("mBossSpawned", 0, 1)], [SIV("Boss", "dist", "abs(lane-mPX)")] + proj("Boss")),
    ]))
    ev.append(G("Boss clocks and phase", [
        B(gate() + [CMPV("mBossSpawned", 0, 1)], [SIV("Boss", "age", "age+ddt"), SIV("Boss", "fire", "fire-ddt")]),
        B(gate() + [CMPV("mBossSpawned", 0, 1), IV("Boss", "hp", 4, "0.67*maxHp")], [SIV("Boss", "phase", 1)]),
        B(gate() + [CMPV("mBossSpawned", 0, 1), IV("Boss", "hp", 3, "0.67*maxHp"), IV("Boss", "hp", 4, "0.32*maxHp")],
          [SIV("Boss", "phase", 2)]),
        B(gate() + [CMPV("mBossSpawned", 0, 1), IV("Boss", "hp", 3, "0.32*maxHp")], [SIV("Boss", "phase", 3)]),
    ]))
    # HTML L467-473: the boss advances to its hover depth; afterwards it sways at its side (no lane change)
    ev.append(G("Boss motion", [
        B(gate() + [CMPV("mBossSpawned", 0, 1), IV("Boss", "state", 0, 0)],
          [SIV("Boss", "laneT", "min(1,laneT+ddt/laneDur)"),
           SIV("Boss", "lane", "laneFrom+(laneTo-laneFrom)*(laneT*laneT*(3-2*laneT))"),
           SIV("Boss", "d", "min(hoverD,d+ddt*vd)")]),
        B(gate() + [CMPV("mBossSpawned", 0, 1), IV("Boss", "state", 0, 0), IV("Boss", "d", 5, "hoverD")],
          [SIV("Boss", "state", 1)]),
        B(gate() + [CMPV("mBossSpawned", 0, 1), IV("Boss", "state", 0, 1), IV("Boss", "phase", 0, 1)],
          [SIV("Boss", "lane", "clamp(laneTo+sin(age*0.70)*35,75,345)")]),
        B(gate() + [CMPV("mBossSpawned", 0, 1), IV("Boss", "state", 0, 1), IV("Boss", "phase", 0, 2)],
          [SIV("Boss", "lane", "clamp(laneTo+sin(age*0.70)*55,75,345)")]),
        B(gate() + [CMPV("mBossSpawned", 0, 1), IV("Boss", "state", 0, 1), IV("Boss", "phase", 0, 3)],
          [SIV("Boss", "lane", "clamp(laneTo+sin(age*1.35)*55,75,345)")]),
    ]))
    return ev

def spawn_events():
    """HTML L454-463 and enemySpawn L361-368. The kind is chosen once per tick from rKind, with exclusive ranges."""
    spawn_ok = gate() + [CMPV("mWave", 2, 6), CMPV("mSpawnTimer", 3, 0), CMPV("mSpawned", 2, "mQuota"),
                         CMPV("Enemy.Count", 2, "mMaxAlive")]
    ev = [G("Spawn roll", [B([TICK()], [SETV("rKind", "random()"), SETV("rSide", "floor(random(0,2))*2-1")])])]
    ev.append(G("Spawn timer", [
        B(gate(), [SETV("mSpawnTimer", "mSpawnTimer-ddt")]),
    ]))
    # van: level >= 3 and roll < 0.13 ; ambulance: roll < 0.22 (not a van) ; police: the rest
    van = [CMPV("mLevel", 4, 2), CMPV("rKind", 2, 0.13)]
    ev.append(G("Spawn enemies (one per tick)", [
        B(spawn_ok + van, _create_enemy("van", "31")),
        B(spawn_ok + [CMPV("rKind", 2, 0.22), CMPV("mLevel", 2, 3)], _create_enemy("ambulance", "20")),
        B(spawn_ok + [CMPV("rKind", 2, 0.22), CMPV("mLevel", 5, 3), CMPV("rKind", 5, 0.13)], _create_enemy("ambulance", "20")),
        B(spawn_ok + [CMPV("rKind", 5, 0.22), CMPV("mLevel", 2, 3)], _create_enemy("police", "16")),
        B(spawn_ok + [CMPV("rKind", 5, 0.22), CMPV("mLevel", 5, 3)], _create_enemy("police", "16")),
    ]))
    # waves 6 escorts: one alive at a time, at most 3 (5 at level >= 4)
    boss_ok = gate() + [CMPV("mWave", 0, 6), CMPV("mBossSpawned", 0, 1), CMPV("mSpawnTimer", 3, 0),
                        CMPV("Enemy.Count", 0, 0)]
    ev.append(G("Boss escorts", [
        B(boss_ok + [CMPV("mBossAdds", 2, 3), CMPV("mLevel", 2, 4)], _escort()),
        B(boss_ok + [CMPV("mBossAdds", 2, 5), CMPV("mLevel", 5, 4)], _escort()),
    ]))
    return ev

KIND_NUM = {"police": 0, "ambulance": 1, "van": 2}

def _create_enemy(kind, hp_base):
    return [SETV("mIdSeq", "mIdSeq+1"), CREATE("Enemy", "Actors", 0, 0), ANIM("Enemy", kind),
            SIV("Enemy", "kind", KIND_NUM[kind])] + _enemy_init(hp_base) + [
        SETV("mSpawned", "mSpawned+1"), SETV("mSpawnTimer", "max(0.95,1.2+0.8*random()-mLevel*0.03)")]

def _escort():
    return [SETV("mIdSeq", "mIdSeq+1"), SETV("mBossAdds", "mBossAdds+1"), CREATE("Enemy", "Actors", 0, 0),
            ANIM("Enemy", "police"), SIV("Enemy", "kind", 0)] + _enemy_init("16") + [SETV("mSpawnTimer", "3.8+1.7*random()")]

def _enemy_init(hp_base):
    hp = f"{hp_base}+mLevel*4+(mWave-1)*4"
    return [
        SIV("Enemy", "id", "mIdSeq"),
        SIV("Enemy", "laneFrom", "210+random(-35,35)"),
        SIV("Enemy", "lane", "laneFrom"),
        SIV("Enemy", "laneTo", "210+rSide*(84+56*random())"),
        SIV("Enemy", "laneT", 0), SIV("Enemy", "laneDur", 0.9), SIV("Enemy", "dodge", 0.36),
        SIV("Enemy", "dodgeCd", "0.6+0.6*random()"), SIV("Enemy", "d", -0.45),
        SIV("Enemy", "vd", "0.23+0.09*random()"), SIV("Enemy", "hoverD", "-0.1+0.065*random()"),
        SIV("Enemy", "hp", hp), SIV("Enemy", "maxHp", hp),
        SIV("Enemy", "fire", "1.2+1.2*random()"), SIV("Enemy", "state", 0), SIV("Enemy", "training", 0),
        SIV("Enemy", "age", 0), SIV("Enemy", "dodgeNow", 0),
    ]

BOSS_KINDS = ["convoy", "armored", "green", "orange", "police"]

def boss_spawn_events():
    """HTML L454 and enemySpawn(true) L361-368: the boss appears in wave 6 when waveTime > 0.9.
    The truck depends on the bank (mBoss 0..4)."""
    arrive = [TICK(), CMPV("screen", 0, 5), CMPV("mTunnel", 0, 0), CMPV("mWave", 0, 6), CMPV("mBossSpawned", 0, 0),
              CMPV("mWaveTime", 4, 0.9)]
    return [G("Boss arrives", [
        B(arrive + [CMPV("mBoss", 0, k)], [SETV("mBossSpawned", 1), SETV("mIdSeq", "mIdSeq+1"),
                                            CREATE("Boss", "Actors", 0, 0), ANIM("Boss", kind)] + _boss_init())
        for k, kind in enumerate(BOSS_KINDS)
    ])]

def _boss_init():
    hp = "120+mLevel*47"
    return [
        SIV("Boss", "id", "mIdSeq"),
        SIV("Boss", "lane", "210+rSide*(100+18*random())"), SIV("Boss", "laneFrom", "lane"), SIV("Boss", "laneTo", "lane"),
        SIV("Boss", "laneT", 0), SIV("Boss", "laneDur", 0.9),
        SIV("Boss", "d", -0.45), SIV("Boss", "vd", 0.11), SIV("Boss", "hoverD", -0.055),
        SIV("Boss", "hp", hp), SIV("Boss", "maxHp", hp), SIV("Boss", "fire", "1.2+1.2*random()"),
        SIV("Boss", "phase", 1), SIV("Boss", "state", 0), SIV("Boss", "age", 0),
    ]
