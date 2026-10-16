/* Kitten Taxi: motor de la partida (lógica y dibujo del campo de juego). */
(() => {
'use strict';
const KT = window.KT;
const W = KT.W, H = KT.H, HZ = KT.HORIZON;
const CAR_Y = HZ;                 // el coche está en el horizonte
const WS = 0.29;                  // velocidad de acercamiento (profundidad/s)
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const rnd = (a, b) => a + Math.random() * (b - a);
const pick = a => a[Math.floor(Math.random() * a.length)];

// t = 0 en el coche (lejos), t = 1 en el borde inferior (cerca de la cámara)
KT.proj = (x, t) => {
  const hr = 95 + 190 * t;
  return { x: W / 2 + x * hr, y: HZ + (H - HZ) * t, s: 1 + 0.6 * t };
};
KT.carX = px => W / 2 + px * 95;

const SCALE = { taxi: 0.78, enemy: 0.66, boss: 0.62, coin: 0.6, gem: 0.6, bottle: 0.62, dumpster: 0.7, clay: 0.7, crate: 0.8, bullet: 0.9 };

// Tutorial de la primera ola (textos observados en el original)
const TUT = [
  { at: 0.6, text: 'Bank robber', pos: 'car' },
  { at: 3.0, text: 'Drive!', kind: 'drive' },
  { at: 6.2, text: 'Police', kind: 'label', target: 'enemy' },
  { at: 9.0, text: 'Dodge!', pos: 'car' },
  { at: 13.5, text: 'Auto attack when you go near an enemy', pos: 'car', wide: true },
  { at: 18.5, text: 'get a weapons', pos: 'car', spawn: 'crate' },
  { at: 22.5, text: 'get a Coin', pos: 'car', spawn: 'coins' },
];

KT.newRun = (bi, tutorial) => {
  const save = KT.save, st = KT.stats;
  const bank = save.banks[bi];
  if (bank.balance <= 0) bank.balance = KT.bankBase(bi);
  const golden = save.goldenKeys > 0;
  if (golden) { save.goldenKeys--; KT.persist(); }
  const hpMax = st.maxHp();
  return {
    bi, level: bank.level, bankLeft: bank.balance, golden, tutorial: !!tutorial,
    phase: 'tip', phaseT: 0, wave: 0, t: 0, playT: 0,
    px: 0, targetX: 0, auto: true,
    hp: hpMax, hpMax, hpBonus: 0, rateBonus: 1, magnetBonus: 0,
    slowT: 0, slowMul: 1, shake: 0, flash: 0,
    cd: 0, boostT: 0, boostId: null, bombs: save.owned.bomb ? 2 : 0,
    stolen: 0, destroyed: 0, gemsRun: 0,
    enemies: [], bullets: [], objs: [], fx: [], texts: [], warnings: [],
    bubble: null, tutQueue: [],
    tm: { coin: 0.8, crate: 6, bottle: 2.5, dump: 8, clay: 12 },
    spawnLeft: 0, spawnT: 0, remaining: 0, timeLeft: 0, waveTotal: 0,
    boss: false, bossDone: false, shieldLeft: 0,
    tallyLeft: 0, tallyStart: 0, tallyT: 0, levelUpText: '', prePause: 'play',
    introText: '', deadTitle: '', deadMsg: '',
  };
};

KT.startWave = (G, n) => {
  const d = G.level, boss = n === 6;
  G.wave = n;
  G.boss = boss;
  G.bossDone = false;
  G.waveTotal = boss ? 4 : 5 + n + d;
  G.spawnLeft = G.waveTotal;
  G.spawnT = 0.6;
  G.remaining = G.waveTotal + (boss ? 1 : 0);
  G.timeLeft = boss ? 45 : 24 + d * 1.5 + n * 1.2;
  G.shieldLeft = KT.save.shield;
  G.hp = Math.min(G.hpMax, G.hp + 12);
  if (KT.save.owned.bomb) G.bombs += 1;
  G.phase = 'intro';
  G.phaseT = boss ? 1.8 : 1.2;
  G.introText = boss ? 'BOSS' : 'OLA ' + n;
  G.playT = 0;
  G.tutQueue = (G.tutorial && n === 1) ? TUT.map(x => ({ ...x })) : [];
  G.bubble = null;
};

KT.spawnEnemy = G => {
  const d = G.level;
  const r = Math.random();
  let type;
  if (G.wave === 1) type = r < 0.8 ? 'police' : 'sedan';
  else type = r < 0.45 ? 'police' : r < 0.7 ? 'sedan' : 'van';
  const st = KT.ENEMY[type];
  const hp = st.hp * (1 + 0.25 * (d - 1));
  G.enemies.push({
    type, x: (Math.random() < 0.5 ? -1 : 1) * rnd(0.3, 0.85), t: 1.0, hp, maxHp: hp,
    reward: Math.round(st.reward * (1 + 0.1 * (d - 1))),
    fire: st.fire, fireT: rnd(1, 2.5), ram: st.ram, vt: st.vz,
    tStop: rnd(0.03, 0.08), state: 'approach', flash: 0, dead: false,
  });
};

KT.spawnBoss = G => {
  const d = G.level;
  const hp = 140 * (1 + 0.3 * (d - 1));
  G.enemies.push({
    type: 'boss', x: 0, t: 0.22, hp, maxHp: hp, reward: 300 * d,
    fire: 2.0, fireT: 1.5, ram: false, vt: 0, tStop: 0.22, state: 'hold', flash: 0, dead: false,
  });
};

/* ---------- proyectiles y disparos ---------- */
const fireAt = (G, e, off) => {
  const speed = WS * 3.0;
  const tt = Math.max(0.15, e.t / speed);
  const x0 = e.x + off;
  const vx = (G.px - x0) / tt * 0.7;
  G.bullets.push({ x: x0, t: e.t, vx, dmg: e.type === 'boss' ? 6 : 5, dead: false });
  G.warnings.push({ x: clamp(x0 + vx * tt, -0.9, 0.9), life: 0.6, t: 0 });
};

KT.hurt = (G, d) => {
  if (G.phase !== 'play') return;
  G.hp = Math.max(0, G.hp - d);
  G.shake = 0.35;
  G.flash = 0.3;
  if (G.hp <= 0) {
    G.phase = 'dead';
    G.deadTitle = '¡Te han parado!';
    G.deadMsg = 'Tu coche no aguanta más.';
  }
};

KT.boom = (G, x, t, size) => {
  G.fx.push({ k: 'burst', x, t, size, life: 0.5, age: 0 });
  G.fx.push({ k: 'smoke', x, t: Math.max(0, t - 0.02), size, life: 0.9, age: 0 });
};
KT.floatText = (G, sx, sy, text, color) => G.texts.push({ sx, sy, text, color, age: 0 });
KT.worldText = (G, x, t, text, color) => { const p = KT.proj(x, t); KT.floatText(G, p.x, p.y - 30, text, color); };

KT.hitEnemy = (G, e, dmg) => {
  if (e.dead) return;
  e.hp -= dmg;
  e.flash = 0.1;
  if (e.hp <= 0) {
    e.dead = true;
    G.remaining--;
    G.destroyed += e.reward;
    KT.boom(G, e.x, e.t, e.type === 'boss' ? 2.4 : 1);
    KT.worldText(G, e.x, e.t, '+' + e.reward, '#8a5a00');
    if (e.type === 'boss') G.bossDone = true;
  }
};

KT.useBomb = G => {
  if (!G || G.phase !== 'play' || G.bombs <= 0) return;
  let tgt = null, bd = 1e9;
  for (const e of G.enemies) if (!e.dead && e.t < bd && e.t > 0.05) { bd = e.t; tgt = e; }
  if (!tgt) return;
  G.bombs--;
  const x0 = tgt.x, t0 = tgt.t;
  for (const e of G.enemies) if (!e.dead && Math.abs(e.t - t0) <= 0.15 && Math.abs(e.x - x0) <= 0.35) KT.hitEnemy(G, e, KT.stats.bombDmg());
  KT.boom(G, x0, t0, 2.2);
};

const updWeapon = (G, dt) => {
  const id = G.boostId || KT.save.active;
  const w = KT.WEAPONS[id];
  G.cd -= dt;
  if (G.cd > 0) return;
  let tgt = null, bd = 1e9;
  for (const e of G.enemies) {
    if (e.dead || e.t > w.range || e.t < 0.03 || Math.abs(e.x - G.px) > w.lat) continue;
    if (e.t < bd) { bd = e.t; tgt = e; }
  }
  if (!tgt) { G.cd = 0; return; }
  G.cd = 1 / (KT.stats.weaponRate(id) * G.rateBonus);
  const pw = KT.stats.weaponPower(id);
  const from = { x: KT.carX(G.px), y: CAR_Y - 34 };
  const to = KT.proj(tgt.x, tgt.t);
  G.fx.push({ k: 'tracer', from, to, life: 0.08, age: 0, color: id === 'machine' ? '#5a5a5a' : KT.INK });
  if (id === 'shot') {
    for (const e of G.enemies) if (!e.dead && Math.abs(e.t - tgt.t) < 0.12 && Math.abs(e.x - tgt.x) < 0.22) KT.hitEnemy(G, e, pw * 2);
  } else {
    KT.hitEnemy(G, tgt, pw);
  }
};

/* ---------- actualización ---------- */
const updEnemy = (G, e, dt) => {
  e.flash = Math.max(0, e.flash - dt);
  if (e.type === 'boss') {
    e.x = Math.sin(G.t * 0.8) * 0.45;
    e.fireT -= dt;
    if (e.fireT <= 0) { e.fireT = e.fire; for (const o of [-0.25, 0, 0.25]) fireAt(G, e, o); }
    return;
  }
  if (e.state === 'approach') {
    e.t -= (WS * G.slowMul + e.vt) * dt;
    if (e.ram) e.x += clamp(G.px - e.x, -1, 1) * 0.35 * dt;
    if (!e.ram && e.t <= e.tStop) { e.t = e.tStop; e.state = 'hold'; }
  }
  e.x = clamp(e.x, -0.95, 0.95);
  if (e.fire > 0 && e.t > 0.02 && e.t < 0.9) {
    e.fireT -= dt;
    if (e.fireT <= 0) { e.fireT = e.fire; fireAt(G, e, 0); }
  }
  if (e.t <= 0.07 && Math.abs(e.x - G.px) < 0.2) {
    e.dead = true; G.remaining--; KT.boom(G, e.x, 0.05, 1); KT.hurt(G, 10);
  } else if (e.t < -0.05) {
    e.dead = true; G.remaining--;
  }
};

const updBullets = (G, dt) => {
  const speed = WS * 3.0;
  for (const b of G.bullets) {
    if (b.dead) continue;
    b.t -= speed * dt;
    b.x += b.vx * dt;
    if (b.t <= 0.07 && Math.abs(b.x - G.px) < 0.2) {
      b.dead = true;
      if (G.shieldLeft > 0) { G.shieldLeft--; KT.floatText(G, KT.carX(G.px), CAR_Y - 110, 'Bloqueado', '#2b6cb0'); }
      else KT.hurt(G, b.dmg);
    } else if (b.t < -0.05) b.dead = true;
  }
};

const updObjs = (G, dt) => {
  const mr = KT.stats.magnetR() + G.magnetBonus;
  for (const o of G.objs) {
    if (o.dead) continue;
    o.t -= WS * G.slowMul * dt;
    if ((o.kind === 'coin' || o.kind === 'gem') && o.t < 0.5 && Math.abs(o.x - G.px) < mr) {
      o.x += (G.px - o.x) * Math.min(1, dt * 6);
    }
    if (o.t <= 0.07 && Math.abs(o.x - G.px) < 0.24) {
      o.dead = true;
      if (o.kind === 'bottle') { KT.hurt(G, 6); slow(G, 0.6, 0.6); KT.worldText(G, o.x, 0.1, '¡Ay!', '#c0392b'); }
      else if (o.kind === 'dumpster') { KT.hurt(G, 12); KT.worldText(G, o.x, 0.1, '¡Choque!', '#c0392b'); }
      else if (o.kind === 'clay') { slow(G, 2.5, 0.5); KT.worldText(G, o.x, 0.1, 'Arcilla', '#3c8a3c'); }
      else collect(G, o);
    } else if (o.t < -0.05) o.dead = true;
  }
};

const slow = (G, sec, mul) => { G.slowT = Math.max(G.slowT, sec); G.slowMul = mul; };

const collect = (G, o) => {
  const sx = KT.carX(G.px), sy = CAR_Y - 80;
  if (o.kind === 'coin') {
    const left = G.bankLeft - G.stolen;
    const v = Math.min(KT.stats.coinValue() * (G.golden ? 2 : 1), Math.max(0, left));
    if (v > 0) { G.stolen += v; KT.floatText(G, sx, sy, '+' + v, '#8a5a00'); }
    else KT.floatText(G, sx, sy, 'Banco vacío', '#6d6a63');
  } else if (o.kind === 'gem') {
    G.gemsRun++;
    KT.floatText(G, sx, sy, '+1 gema', '#1a87b5');
  } else if (o.kind === 'crate') {
    const opts = ['shot', 'machine'].filter(id => KT.save.owned[id]);
    if (opts.length) { G.boostId = pick(opts); G.boostT = 10; KT.floatText(G, sx, sy, KT.WEAPONS[G.boostId].name + '!', '#1d1d1d'); }
    else if (KT.save.owned.bomb) { G.bombs++; KT.floatText(G, sx, sy, '+1 bomba', '#1d1d1d'); }
    else { G.destroyed += 20; KT.floatText(G, sx, sy, '+20', '#8a5a00'); }
  }
};

const spawnTick = (G, dt) => {
  const tm = G.tm;
  const add = (kind, x, t) => G.objs.push({ kind, x, t, dead: false });
  tm.coin -= dt;
  if (tm.coin <= 0) {
    tm.coin = rnd(1.5, 2.3);
    const x = rnd(-0.7, 0.7);
    if (Math.random() < 0.15) add('gem', x, 1.0);
    else for (let k = 0; k < 4; k++) add('coin', x, 1.0 - k * 0.07);
  }
  tm.crate -= dt;  if (tm.crate <= 0)  { tm.crate = rnd(9, 12); add('crate', rnd(-0.7, 0.7), 1.0); }
  tm.bottle -= dt; if (tm.bottle <= 0) { tm.bottle = rnd(2.6, 4); add('bottle', rnd(-0.8, 0.8), 1.0); }
  tm.dump -= dt;   if (tm.dump <= 0)   { tm.dump = rnd(10, 14); add('dumpster', rnd(-0.7, 0.7), 1.0); }
  tm.clay -= dt;   if (tm.clay <= 0)   { tm.clay = rnd(13, 18); add('clay', rnd(-0.7, 0.7), 1.0); }
  if (G.spawnLeft > 0) {
    G.spawnT -= dt;
    if (G.spawnT <= 0) {
      G.spawnT = Math.max(0.6, 1.2 - 0.05 * G.level);
      G.spawnLeft--;
      KT.spawnEnemy(G);
    }
  }
};

const runTutorial = G => {
  while (G.tutQueue.length && G.playT >= G.tutQueue[0].at) {
    const q = G.tutQueue.shift();
    if (q.spawn === 'crate') G.objs.push({ kind: 'crate', x: 0.35, t: 1.0, dead: false });
    if (q.spawn === 'coins') for (let k = 0; k < 4; k++) G.objs.push({ kind: 'coin', x: -0.35, t: 1.0 - k * 0.07, dead: false });
    G.bubble = { text: q.text, kind: q.kind || 'speech', pos: q.pos, target: q.target, wide: !!q.wide, age: 0, dur: 1.6 };
    return;
  }
};

const endWave = (G, bonus) => {
  G.enemies.length = 0;
  G.bullets.length = 0;
  G.phase = 'tally';
  G.tallyLeft = Math.max(0, bonus);
  G.tallyStart = G.tallyLeft;
  G.tallyT = 0.6;
};

const updTally = (G, dt) => {
  G.tallyT -= dt;
  if (G.tallyLeft > 0) {
    if (G.tallyT <= 0) {
      const step = Math.min(G.tallyLeft, 2);
      G.tallyLeft -= step;
      G.destroyed += step;
      G.tallyT = G.tallyLeft > 0 ? 0.035 : 0.7;
    }
  } else if (G.tallyT <= 0) {
    KT.startWave(G, G.wave + 1);
  }
};

KT.levelUp = G => {
  G.enemies.length = 0;
  G.bullets.length = 0;
  const k = pick(['rate', 'hp', 'magnet']);
  if (k === 'rate') { G.rateBonus *= 1.1; G.levelUpText = 'Firing rate Up'; }
  else if (k === 'hp') { G.hpBonus += 20; G.levelUpText = 'Loadage Up'; }
  else { G.magnetBonus += 0.05; G.levelUpText = 'Magnet Up'; }
  G.hpMax = KT.stats.maxHp() + G.hpBonus;
  G.hp = Math.min(G.hpMax, G.hp + 20);
  G.phase = 'levelUp';
  G.phaseT = 2.2;
};

KT.updateRun = (G, dt) => {
  G.t += dt;
  G.shake = Math.max(0, G.shake - dt * 2.5);
  G.flash = Math.max(0, G.flash - dt * 1.5);
  for (const f of G.fx) f.age += dt;
  G.fx = G.fx.filter(f => f.age < f.life);
  for (const tx of G.texts) tx.age += dt;
  G.texts = G.texts.filter(tx => tx.age < 0.9);
  for (const w of G.warnings) w.t += dt;
  G.warnings = G.warnings.filter(w => w.t < w.life);

  if (G.phase === 'intro') {
    G.phaseT -= dt;
    if (G.phaseT <= 0) {
      if (G.boss) KT.spawnBoss(G);
      G.phase = 'play';
    }
    return;
  }
  if (G.phase === 'tally') { updTally(G, dt); return; }
  if (G.phase === 'levelUp') {
    G.phaseT -= dt;
    if (G.phaseT <= 0) G.phase = 'done';
    return;
  }
  if (G.phase !== 'play') return;

  if (G.bubble) {                    // el tutorial pausa el mundo mientras hay burbuja
    G.bubble.age += dt;
    if (G.bubble.age >= G.bubble.dur) G.bubble = null;
    return;
  }
  G.playT += dt;
  if (G.tutQueue.length) runTutorial(G);
  if (G.bubble) return;

  G.timeLeft -= dt;
  if (G.slowT > 0) { G.slowT -= dt; if (G.slowT <= 0) G.slowMul = 1; }
  if (G.boostT > 0) { G.boostT -= dt; if (G.boostT <= 0) G.boostId = null; }

  if (KT.keys.ArrowLeft)  { G.auto = false; G.targetX -= dt * 1.6; }
  if (KT.keys.ArrowRight) { G.auto = false; G.targetX += dt * 1.6; }
  if (G.auto) autoSteer(G);
  G.targetX = clamp(G.targetX, -0.9, 0.9);
  G.px += (G.targetX - G.px) * Math.min(1, dt * (G.auto ? 5 : 12));

  spawnTick(G, dt);
  updObjs(G, dt);
  for (const e of G.enemies) if (!e.dead) updEnemy(G, e, dt);
  updBullets(G, dt);
  updWeapon(G, dt);
  if (G.phase !== 'play') return;

  G.enemies = G.enemies.filter(e => !e.dead);
  G.bullets = G.bullets.filter(b => !b.dead);
  G.objs = G.objs.filter(o => !o.dead);

  if (G.boss && G.bossDone) {
    KT.levelUp(G);
  } else if (G.spawnLeft <= 0 && G.remaining <= 0) {
    endWave(G, Math.floor(G.timeLeft) * 2);
  } else if (G.timeLeft <= 0) {
    if (G.boss) {
      G.phase = 'dead';
      G.deadTitle = 'Se acabó el tiempo';
      G.deadMsg = 'El jefe te ha ganado la carrera.';
    } else {
      endWave(G, 0);
    }
  }
};

const autoSteer = G => {
  let best = null, bd = 1e9;
  for (const e of G.enemies) if (!e.dead && e.t > 0.02 && e.t < bd) { bd = e.t; best = e; }
  if (!best) {
    for (const o of G.objs) {
      if (!o.dead && (o.kind === 'coin' || o.kind === 'gem' || o.kind === 'crate') && o.t < bd) { bd = o.t; best = o; }
    }
  }
  G.targetX = best ? clamp(best.x, -0.9, 0.9) : 0;
};

/* ---------- dibujo del campo ---------- */
const drawSpeed = (g, G) => {
  g.save();
  g.fillStyle = KT.INK;
  for (const L of KT.speedLines) {
    const u = ((L.p - G.t * 0.22) % 1 + 1) % 1;       // las líneas avanzan hacia el coche
    const t1 = u, t2 = Math.min(1, u + L.len);
    if (t2 <= t1) continue;
    const a = KT.proj(L.x, t1), b = KT.proj(L.x, t2);
    const wa = L.w * 1.6 * a.s, wb = L.w * 0.3 * b.s;
    g.globalAlpha = 0.35 + 0.5 * t1;
    g.beginPath();
    g.moveTo(a.x - wa / 2, a.y);
    g.lineTo(b.x - wb / 2, b.y);
    g.lineTo(b.x + wb / 2, b.y);
    g.lineTo(a.x + wa / 2, a.y);
    g.closePath();
    g.fill();
  }
  g.restore();
};

const drawLanes = g => {
  g.save();
  g.lineCap = 'round';
  const lanes = [[-0.42, -0.35], [0.4, 0.3], [-0.9, -0.5], [0.92, 0.55]];
  for (const [x0, c] of lanes) {
    const a = KT.proj(x0 * 0.6, 0.02), b = KT.proj(x0 + c * 0.35, 0.5), d = KT.proj(x0 + c, 1);
    g.strokeStyle = 'rgba(70,70,70,.55)';
    g.lineWidth = 3;
    g.beginPath(); g.moveTo(a.x, a.y); g.quadraticCurveTo(b.x, b.y, d.x, d.y); g.stroke();
    g.strokeStyle = 'rgba(40,40,40,.35)';
    g.lineWidth = 1.2;
    g.beginPath(); g.moveTo(a.x + 2, a.y); g.quadraticCurveTo(b.x + 3, b.y, d.x + 3, d.y); g.stroke();
  }
  g.restore();
};

const spriteFor = (o) => {
  const SP = KT.sprites;
  if (o.kind === 'coin') return [SP.coin, SCALE.coin];
  if (o.kind === 'gem') return [SP.gem, SCALE.gem];
  if (o.kind === 'crate') return [SP.crate, SCALE.crate];
  if (o.kind === 'bottle') return [SP.bottle, SCALE.bottle];
  if (o.kind === 'dumpster') return [SP.dumpster, SCALE.dumpster];
  if (o.kind === 'clay') return [SP.clay, SCALE.clay];
  return [null, 1];
};

const drawEnemy = (g, e, level) => {
  const p = KT.proj(e.x, e.t);
  const SP = KT.sprites;
  if (e.type === 'boss') {
    KT.drawSprite(g, level % 2 ? SP.bossBlue : SP.bossYellow, p.x, p.y, SCALE.boss * p.s);
    const w = 140 * p.s, y = p.y - 240 * SCALE.boss * p.s - 14;
    barHp(g, p.x, y, w, e.hp / e.maxHp);
    return;
  }
  const spr = e.type === 'van' ? SP.van : e.type === 'sedan' ? SP.sedan : SP.police;
  KT.drawSprite(g, spr, p.x, p.y, SCALE.enemy * p.s);
  if (e.flash > 0) {
    g.save(); g.globalAlpha = 0.5; g.fillStyle = '#ffffff';
    g.fillRect(p.x - 40 * p.s, p.y - 90 * p.s * SCALE.enemy * 1.4, 80 * p.s, 90 * p.s * SCALE.enemy * 1.4);
    g.restore();
  }
  if (e.hp < e.maxHp) barHp(g, p.x, p.y - spr.h * SCALE.enemy * p.s - 10, 60 * p.s, e.hp / e.maxHp);
};

const barHp = (g, x, y, w, frac) => {
  g.save();
  g.fillStyle = '#ffffff';
  g.fillRect(x - w / 2, y, w, 9);
  g.strokeStyle = KT.INK; g.lineWidth = 1.6; g.strokeRect(x - w / 2, y, w, 9);
  g.fillStyle = '#4caf32';
  g.fillRect(x - w / 2 + 1.5, y + 1.5, Math.max(0, (w - 3) * frac), 6);
  g.restore();
};

const drawBullet = (g, b) => {
  const p = KT.proj(b.x, b.t);
  KT.drawSprite(g, KT.sprites.bullet, p.x, p.y, SCALE.bullet * p.s);
};

const drawTaxi = (g, G) => {
  const x = KT.carX(G.px);
  const spr = G.golden ? KT.sprites.taxiGold : KT.sprites.taxi;
  KT.shadow(g, x, CAR_Y + 2, 56, 7);
  if (G.boostT > 0) {
    g.save(); g.globalAlpha = 0.35; g.fillStyle = '#ffffff';
    g.beginPath(); g.arc(x, CAR_Y - 40, 58, 0, Math.PI * 2); g.fill(); g.restore();
  }
  KT.drawSprite(g, spr, x, CAR_Y, SCALE.taxi);
  if (G.shieldLeft > 0) {
    g.save(); g.strokeStyle = '#2b6cb0'; g.lineWidth = 3; g.setLineDash([6, 5]);
    g.beginPath(); g.arc(x, CAR_Y - 40, 62, 0, Math.PI * 2); g.stroke(); g.restore();
  }
};

const drawWarnings = (g, G) => {
  for (const w of G.warnings) {
    const p = KT.proj(w.x, 0.14);
    const a = 1 - w.t / w.life;
    g.save(); g.globalAlpha = Math.max(0, a);
    KT.drawSprite(g, KT.sprites.warning, p.x, p.y, 0.9);
    g.restore();
  }
};

const drawFx = (g, G) => {
  for (const f of G.fx) {
    const k = f.age / f.life;
    if (f.k === 'tracer') {
      g.save(); g.globalAlpha = 1 - k; g.strokeStyle = f.color; g.lineWidth = 2.4; g.lineCap = 'round';
      g.beginPath(); g.moveTo(f.from.x, f.from.y); g.lineTo(f.to.x, f.to.y - 6); g.stroke(); g.restore();
    } else if (f.k === 'burst') {
      const p = KT.proj(f.x, f.t);
      g.save(); g.globalAlpha = 1 - k;
      KT.drawSprite(g, KT.sprites.burst, p.x, p.y, (0.5 + 0.7 * k) * f.size * p.s * 0.8);
      g.restore();
    } else if (f.k === 'smoke') {
      const p = KT.proj(f.x, f.t);
      g.save(); g.globalAlpha = 0.85 * (1 - k);
      KT.drawSprite(g, KT.sprites.smoke, p.x, p.y, (0.6 + 0.8 * k) * f.size * p.s * 0.8);
      g.restore();
    }
  }
};

const drawTexts = (g, G) => {
  g.save();
  g.textAlign = 'center';
  g.textBaseline = 'middle';
  for (const tx of G.texts) {
    const a = clamp(1 - tx.age / 0.9, 0, 1);
    const y = tx.sy - tx.age * 40;
    g.globalAlpha = a;
    g.font = '700 26px "Patrick Hand", "Comic Sans MS", cursive';
    g.lineWidth = 4; g.strokeStyle = 'rgba(255,255,255,.9)';
    g.strokeText(tx.text, tx.sx, y);
    g.fillStyle = tx.color;
    g.fillText(tx.text, tx.sx, y);
  }
  g.restore();
};

const drawBubble = (g, G) => {
  const b = G.bubble;
  if (!b) return;
  let ax = KT.carX(G.px), ay = CAR_Y - 110;
  if (b.target === 'enemy') {
    const e = G.enemies.find(en => !en.dead);
    if (e) { const p = KT.proj(e.x, e.t); ax = p.x; ay = p.y - 90; }
  }
  const lines = b.wide ? ['Auto attack when you', 'go near an enemy'] : [b.text];
  const size = b.kind === 'label' ? 22 : b.wide ? 22 : 30;
  g.save();
  g.font = `700 ${size}px "Patrick Hand", "Comic Sans MS", cursive`;
  const tw = Math.max(...lines.map(l => g.measureText(l).width));
  const bw = Math.max(110, tw + 34), bh = lines.length * size + (b.kind === 'drive' ? 64 : 22);
  const bx = clamp(ax - bw / 2, 8, W - bw - 8), by = ay - bh - 26;
  const pts = KT.rrPts(bx, by, bw, bh, 18, 6);
  // cola
  g.fillStyle = '#fffdf7';
  g.beginPath(); g.moveTo(ax - 12, by + bh - 2); g.lineTo(ax, ay - 6); g.lineTo(ax + 12, by + bh - 2); g.closePath(); g.fill();
  KT.shape(g, pts, '#fffdf7', 2.2, KT.rng(bx * 7 + by));
  if (b.kind === 'label') {
    // corchetes de objetivo alrededor del enemigo
    g.strokeStyle = '#e67e22'; g.lineWidth = 3;
    g.strokeRect(ax - 38, ay + 26, 76, 60);
  }
  lines.forEach((l, i) => KT.hand(g, l, bx + bw / 2, by + 16 + size / 2 + i * size, size, KT.INK, '700'));
  if (b.kind === 'drive') {
    g.strokeStyle = KT.INK; g.lineWidth = 3; g.lineCap = 'round';
    const cy = by + bh - 28;
    g.beginPath(); g.moveTo(bx + bw / 2 - 60, cy); g.lineTo(bx + bw / 2 + 60, cy); g.stroke();
    g.beginPath(); g.moveTo(bx + bw / 2 - 60, cy); g.lineTo(bx + bw / 2 - 48, cy - 9); g.moveTo(bx + bw / 2 - 60, cy); g.lineTo(bx + bw / 2 - 48, cy + 9); g.stroke();
    g.beginPath(); g.moveTo(bx + bw / 2 + 60, cy); g.lineTo(bx + bw / 2 + 48, cy - 9); g.moveTo(bx + bw / 2 + 60, cy); g.lineTo(bx + bw / 2 + 48, cy + 9); g.stroke();
  }
  g.restore();
};

/* Monedas, gemas, botellas... */
const drawObjects = (g, G) => {
  const items = [];
  for (const o of G.objs) if (!o.dead) items.push({ t: o.t, o });
  for (const e of G.enemies) if (!e.dead) items.push({ t: e.t, e });
  items.sort((a, b) => a.t - b.t);
  for (const it of items) {
    if (it.o) {
      const [spr, base] = spriteFor(it.o);
      const p = KT.proj(it.o.x, it.o.t);
      if (spr) KT.drawSprite(g, spr, p.x, p.y, base * p.s);
    } else {
      drawEnemy(g, it.e, G.level);
    }
  }
  for (const b of G.bullets) if (!b.dead) drawBullet(g, b);
};

KT.skies = {};
KT.skyFor = level => {
  const k = (level - 1) % KT.PALETTES.length;
  if (!KT.skies[k]) KT.skies[k] = KT.makeSky(KT.PALETTES[k], 100 + k * 17);
  return KT.skies[k];
};

KT.drawField = (g, G) => {
  g.save();
  if (G.shake > 0) g.translate((Math.random() - 0.5) * G.shake * 14, (Math.random() - 0.5) * G.shake * 14);
  g.fillStyle = '#f7f7f3';
  g.fillRect(-20, HZ - 1, W + 40, H - HZ + 40);
  g.drawImage(KT.skyFor(G.level), 0, 0, W, HZ + 6);
  drawSpeed(g, G);
  drawLanes(g);
  drawTaxi(g, G);
  drawObjects(g, G);
  drawWarnings(g, G);
  drawFx(g, G);
  drawTexts(g, G);
  g.restore();
};

/* HUD según la referencia: temporizador arriba centro, monedas bajo el horizonte, AUTO arriba izq. */
KT.drawHUD = (g, G) => {
  const font = '"Patrick Hand", "Comic Sans MS", cursive';
  g.save();
  // etiquetas arriba izquierda
  g.fillStyle = '#d7d7d7';
  g.fillRect(W * 0.03, H * 0.012, 74, 16);
  KT.hand(g, 'WAVE ' + (G.wave || 1), W * 0.03 + 37, H * 0.012 + 8, 13, '#444', '700');
  KT.hand(g, 'Level ' + G.level, W * 0.03 + 30, H * 0.045 + 8, 18, KT.INK, '700');
  // AUTO
  const ax = W * 0.135, ay = H * 0.13;
  g.beginPath(); g.arc(ax, ay, 19, 0, Math.PI * 2);
  g.fillStyle = '#ffffff'; g.fill();
  g.lineWidth = G.auto ? 4 : 1.5; g.strokeStyle = G.auto ? '#4caf32' : '#8a8a8a'; g.stroke();
  KT.hand(g, 'auto', ax, ay, 12, KT.INK, '700');
  // temporizador: entero grande y decimales pequeños
  const tl = Math.max(0, G.timeLeft);
  const ip = Math.floor(tl), dp = Math.floor((tl - ip) * 100);
  const bigTxt = G.boss ? 'JEFE' : String(ip);
  g.font = `700 52px ${font}`;
  const bw = g.measureText(bigTxt).width;
  g.textAlign = 'left'; g.textBaseline = 'middle'; g.fillStyle = KT.INK;
  const tx = W * 0.6 - (bw + (G.boss ? 0 : 30)) / 2;
  g.fillText(bigTxt, tx, H * 0.075);
  if (!G.boss) {
    g.font = `700 28px ${font}`;
    g.fillText('.' + String(dp).padStart(2, '0'), tx + bw + 2, H * 0.075 + 10);
  }
  // monedas de la partida, bajo el horizonte
  const cx = W * 0.45, cy = H * 0.545;
  KT.drawSprite(g, KT.sprites.coin, cx - 22, cy + 8, 0.55);
  g.textAlign = 'left';
  KT.hand(g, KT.fmt(G.stolen + G.destroyed), cx - 12, cy, 24, KT.INK, '700');
  g.textAlign = 'center';
  // pausa
  const px = W * 0.92, py = H * 0.034;
  KT.shape(g, KT.rrPts(px - 16, py - 14, 32, 28, 6), '#ffffff', 1.8, KT.rng(9));
  g.fillStyle = KT.INK;
  g.fillRect(px - 6, py - 7, 4.5, 14); g.fillRect(px + 2, py - 7, 4.5, 14);
  // carga/vida abajo izquierda
  const sx = W * 0.04, sy = H * 0.945;
  KT.drawSprite(g, KT.sprites.coin, sx + 10, sy + 8, 0.6);
  const frac = clamp(G.hp / G.hpMax, 0, 1);
  const bx = W * 0.10, bwid = W * 0.25;
  g.fillStyle = '#ffffff'; g.fillRect(bx, sy - 6, bwid, 13);
  g.strokeStyle = KT.INK; g.lineWidth = 1.6; g.strokeRect(bx, sy - 6, bwid, 13);
  g.fillStyle = '#f2b705'; g.fillRect(bx + 1.5, sy - 4.5, (bwid - 3) * frac, 10);
  KT.hand(g, String(Math.ceil(G.hp)), bx + bwid / 2, sy - 16, 15, KT.INK, '700');
  KT.hand(g, 'Lv', W * 0.05, sy + 18, 15, KT.INK, '700');
  // dial de bomba abajo centro
  const dx = W * 0.5, dy = H * 0.905;
  g.beginPath(); g.arc(dx, dy, 38, 0, Math.PI * 2);
  g.fillStyle = G.auto ? '#dcf2cc' : '#ffffff'; g.fill();
  g.lineWidth = 3; g.strokeStyle = KT.INK; g.stroke();
  g.fillStyle = KT.INK;
  g.beginPath(); g.ellipse(dx, dy - 2, 9, 11, 0, 0, Math.PI * 2); g.fill();
  g.fillRect(dx - 2, dy - 18, 4, 9);
  KT.hand(g, KT.save.owned.bomb ? String(G.bombs) : '–', dx, dy + 24, 20, KT.INK, '700');
  // refuerzo de arma
  if (G.boostT > 0 && G.boostId) KT.hand(g, KT.WEAPONS[G.boostId].name + ' ' + Math.ceil(G.boostT) + ' s', W / 2, H * 0.16, 22, KT.INK, '700');
  if (G.golden) KT.hand(g, 'COCHE DORADO', W / 2, H * 0.195, 17, '#8a5a00', '700');
  g.restore();
};

/* Pantallas de la partida: intro, fin de ola, jefe, subida de nivel. */
KT.drawRunOverlay = (g, G) => {
  const font = '"Patrick Hand", "Comic Sans MS", cursive';
  if (G.phase === 'intro' && G.boss) {
    g.fillStyle = '#111'; g.fillRect(0, 0, W, H);
    const cx = W / 2, cy = H / 2 - 40;
    g.strokeStyle = '#e9e9e9'; g.lineWidth = 3; g.lineCap = 'round';
    for (let i = 0; i < 28; i++) {
      const a = i / 28 * Math.PI * 2 + G.t * 0.6;
      g.beginPath(); g.moveTo(cx + Math.cos(a) * 80, cy + Math.sin(a) * 80); g.lineTo(cx + Math.cos(a) * 240, cy + Math.sin(a) * 240); g.stroke();
    }
    KT.hand(g, 'BOSS', cx, cy, 96, '#ffffff', '700');
    return;
  }
  if (G.phase === 'tally') {
    g.fillStyle = '#0d0d0d'; g.fillRect(0, 0, W, H);
    KT.hand(g, 'OLA ' + G.wave + (G.tallyStart > 0 ? ' superada' : ' terminada'), W / 2, H / 2 - 140, 26, '#ffffff', '700');
    KT.hand(g, String(Math.max(0, Math.ceil(G.tallyLeft))), W / 2, H / 2 - 20, 120, '#ffffff', '700');
    KT.hand(g, G.tallyStart > 0 ? 'Tiempo sobrante x 2 Bonus' : 'Sin bonus de tiempo', W / 2, H / 2 + 80, 28, '#cfcfcf', '700');
    return;
  }
  if (G.phase === 'intro') {
    g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(0, 0, W, H);
    KT.hand(g, G.introText, W / 2, H / 2 - 60, 74, '#ffffff', '700');
    return;
  }
  if (G.phase === 'levelUp') {
    g.fillStyle = 'rgba(0,0,0,.45)'; g.fillRect(0, 0, W, H);
    KT.hand(g, 'LEVEL ↑', W / 2, H / 2 - 40, 84, '#f2b705', '700');
    KT.hand(g, G.levelUpText, W / 2, H / 2 + 26, 32, '#ffffff', '700');
  }
  if (G.phase === 'dead' || G.phase === 'paused') {
    g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(0, 0, W, H);
  }
  void font;
};

KT.drawRunBubble = (g, G) => drawBubble(g, G);

KT.drawRun = (g, G) => {
  KT.drawField(g, G);
  KT.drawRunBubble(g, G);
  KT.drawHUD(g, G);
  KT.drawRunOverlay(g, G);
  if (G.flash > 0) {
    g.save(); g.globalAlpha = G.flash * 0.5; g.fillStyle = '#e0523b'; g.fillRect(0, 0, W, H); g.restore();
  }
};

KT.keys = {};
})();
