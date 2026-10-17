"""Data taken from the HTML v9 (line numbers in comments). Logic values stay in HTML units (420x746)."""
# ---- coordinate transform: HTML (420x746) -> Construct layout (480x640, playable area x 60..420)
K = 6 / 7
def LX(x):
    return f"(60+({x})*0.857142857)"
def LY(y):
    return f"(({y})*0.857142857)"
def LS(s):
    return f"(({s})*0.857142857)"
def lx(x):   # numeric version for static placement
    return 60 + x * K
def ly(y):
    return y * K

# ---- banks (L22-38): name, level, balance, theme index, boss index
THEMES = ["city", "blue", "mountain", "sunset", "rose"]          # L57
BOSSES = ["convoy", "armored", "green", "orange", "police"]
BANKS = [
    ("Banco Lunar", 1, 100, "city", "convoy"), ("Banco Mirador", 2, 150, "blue", "armored"),
    ("Banco del Puerto", 3, 200, "mountain", "green"), ("Banco Solano", 4, 250, "sunset", "orange"),
    ("Banco Ceniza", 5, 300, "rose", "police"), ("City Reserve", 6, 360, "blue", "armored"),
    ("Marble Finance", 7, 430, "mountain", "green"), ("Grand National", 8, 520, "sunset", "orange"),
    ("Harbor Vault", 9, 650, "city", "convoy"), ("Goldstone Bank", 10, 770, "rose", "police"),
    ("West Savings", 11, 900, "blue", "armored"), ("Northern Trust", 12, 1100, "mountain", "green"),
    ("Tower Bank", 13, 1250, "sunset", "orange"), ("Diamond Credit", 14, 1500, "rose", "police"),
    ("Central Bank", 15, 2000, "city", "convoy"),
]
# ---- weapons (L39): id, name, base, rate, price
WEAPONS = [("pistol", "Pistol", 3, 6.8, 500), ("bomb", "Bomb", 12, 1.1, 1400),
           ("shot", "Shot", 4, 3.2, 2200), ("machine", "Machine", 2.5, 11.2, 4000)]
# ---- cars (L40): id, name, hp, price
CARS = [("taxi", "Yellow Taxi", 100, 0), ("blue", "Blue Roadster", 125, 40000), ("mint", "Mint Racer", 150, 90000)]
# ---- prizes (L347)
PRIZES = [("coins", 50), ("coins", 90), ("coins", 150), ("gems", 1), ("coins", 250), ("weapon", 1), ("coins", 400), ("gems", 2)]
WHEEL_LABELS = ["50", "90", "150", "1", "250", "?", "400", "2"]

# ---- persistent fields (L42 DEFAULT). ledger/clears are dropped: they never change behaviour (ids are unique).
PERSIST = [
    ("coins", 800), ("gems", 10), ("keys", 4), ("unlocked", 0), ("selectedBank", 0),
    ("weapon", 0), ("car", 0), ("upg_pistol", 0), ("upg_bomb", 0), ("upg_shot", 0), ("upg_machine", 0),
    ("upg_car", 0), ("upg_block", 0),
    ("own_bomb", 0), ("own_shot", 0), ("own_machine", 0), ("own_blue", 0), ("own_mint", 0),
    ("own_speedDriver", 0), ("own_medicCat", 0), ("own_luckyPet", 0),
    ("sound", 1), ("reducedMotion", 0), ("seenTutorial", 0), ("spinCount", 0), ("xp", 0), ("plevel", 1),
] + [(f"bank{i}_bal", b[2]) for i, b in enumerate(BANKS)] + [(f"bank{i}_lvl", b[1]) for i, b in enumerate(BANKS)]
PERSIST_KEY_PREFIX = "cat_taxi_v6_"

# ---- non-persistent globals (initial values from the HTML states, L19, L56, mission L358)
RUNTIME = [
    ("screen", 0), ("prevScreen", 2), ("gearTab", 0), ("shopTab", 0), ("selectedItem", 0),
    ("popupOpen", 0), ("popupKind", 0), ("popupConfirm", 0), ("paused", 0),
    ("clock", 0), ("ddt", 0), ("needSave", 0), ("toastUntil", 0), ("toastOn", 0),
    ("spinActive", 0), ("spinT", 0), ("spinTurns", 5), ("spinDesired", 0), ("spinPhase", 0), ("spinCost", 0), ("popTitle", 0), ("popMsg", 0), ("popAmount", 0), ("spinFrom", 0), ("spinTo", 0), ("spinAngle", 0), ("spinOutcome", 0),
    ("spinAwarded", 0), ("selectedBankRun", 0),
    ("mActive", 0), ("mBank", 0), ("mLevel", 1), ("mTheme", 0), ("mWave", 1), ("mWaveTime", 0), ("mWaveDur", 15),
    ("mSeconds", 0), ("mSpawned", 0), ("mQuota", 3), ("mMaxAlive", 2), ("mBossAdds", 0), ("mBossSpawned", 0),
    ("mSpawnTimer", 0.65), ("mPickupTimer", 3), ("mBulletTimer", 0), ("mKillLoot", 0), ("mBankLoot", 0),
    ("mWeaponBuff", 0), ("mBonusWeapon", 0), ("mFlash", 0), ("mShake", 0), ("mWaveBanner", 0),
    ("mPX", 210), ("mTarget", 210), ("mVX", 0), ("mHP", 100), ("mMaxHP", 100), ("mInv", 0), ("mAuto", 0),
    ("mMoved", 0), ("mDeathReason", 0), ("mTouchUI", 0), ("mTouching", 0),
    ("mGuide", 0), ("mGuideStage", 0), ("mGuideTime", 0), ("mGuideReady", 0), ("mGuideLeft", 0),
    ("mGuideRight", 0), ("mGuideHit", 0), ("mGuideAvoided", 0), ("mGuideCrate", 0), ("mGuideCoin", 0),
    ("mGuideRetry", 0), ("mGuideWait", 0), ("mGuideShotMade", 0),
    ("mTunnel", 0), ("mTunnelT", 0), ("mTunnelL", 0), ("mTunnelLeft", 0), ("mTunnelTrain", 0),
    ("mBonusV", 0), ("mBonusT", 0), ("mEnded", 0),
    ("mIdSeq", 0), ("bestId", 0), ("bestVal", 0), ("lockId", 0), ("bossTarget", 0), ("targetLane", 0), ("targetX", 0),
    ("aliveCount", 0), ("guideCount", 0), ("soundToast", 0), ("mWeaponToast", 0), ("mSpawnFix", 0),
    ("loadStarted", 0), ("startReq", 0), ("startGuide", 0), ("startBank", 0), ("awardNeeded", 0),
    ("toastReq", 0), ("toastDur", 2), ("pendingToast", 0), ("startToast", 0), ("mBossRatio", 0), ("mGuideSpawned", 0), ("mEndTunnel", 0), ("mDeathNow", 0), ("mSetupWave", 0), ("mWeapon", 0), ("mRate", 1.1), ("mDmg", 0), ("mHit", 0), ("mBase", 0), ("mBankBal", 0), ("mRemain", 0), ("mReward", 0), ("mPerfect", 0), ("mBoss", 0), ("mEndNow", 0), ("pOld", 0), ("thLane", 0), ("thD", 0), ("tSX", 0), ("tAny", 0), ("tBoss", 0), ("tAny", 0), ("aDanger", 0), ("aPrize", 0), ("aBoss", 0), ("aEnemy", 0), ("aLock", 0), ("dangerXl", 0), ("prizeX", 0), ("bossLane", 0), ("enemyLane", 0), ("bossNow", 0), ("bx", 0), ("by", 0), ("kx", 0), ("ky", 0), ("kDrop", 0), ("rDrop", 0), ("rKind", 0), ("rSide", 1), ("rLane", 0), ("rPick", 0), ("rThrow", 0), ("wxl", 0), ("wdl", 0), ("wid", 0), ("popKind", 0), ("nodeOn", 0), ("keyLast", 0),
]
