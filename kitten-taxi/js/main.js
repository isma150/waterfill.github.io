/* Kitten Taxi: arranque, bucle principal, entrada y flujo entre pantallas. */
(() => {
'use strict';
const KT = window.KT;
const W = KT.W, H = KT.H;
const save = () => KT.save;

const canvas = document.getElementById('game');
const g = canvas.getContext('2d');
const DPR = Math.min(2, window.devicePixelRatio || 1);
canvas.width = W * DPR;
canvas.height = H * DPR;

KT.run = null;
KT.backTo = 'title';

/* ---------- flujo ---------- */
const lastUnlocked = () => {
  let idx = 0;
  KT.save.banks.forEach((b, i) => { if (b.unlocked) idx = i; });
  return idx;
};

const openMap = () => {
  KT.go('map', { sel: lastUnlocked() });
};

const startRun = bi => {
  if (!KT.save.banks[bi].unlocked) return;
  const tutorial = !KT.save.seenTutorial;
  KT.save.seenTutorial = true;
  KT.persist();
  KT.run = KT.newRun(bi, tutorial);
  KT.go('tip', { text: KT.TIPS[Math.floor(Math.random() * KT.TIPS.length)] });
};

const beginRun = () => {
  KT.scene = 'run';
  KT.startWave(KT.run, 1);
};

const finishRun = completed => {
  const G = KT.run;
  if (!G) return;
  const bank = KT.save.banks[G.bi];
  const total = G.stolen + G.destroyed;
  bank.balance = Math.max(0, bank.balance - G.stolen);
  if (G.stolen > 0 || completed) bank.level += 1;
  const perfect = completed && bank.balance === 0 ? Math.round(total * 0.2) : 0;
  if (completed) {
    bank.done = true;
    if (KT.save.banks[G.bi + 1]) KT.save.banks[G.bi + 1].unlocked = true;
  }
  KT.save.coins += total + perfect;
  KT.save.gems += G.gemsRun;
  KT.persist();
  KT.run = null;
  KT.go('result', {
    title: completed ? '¡Banco completado!' : 'Fin del robo',
    stolen: G.stolen, destroyed: G.destroyed, perfect, total: total + perfect,
    gems: G.gemsRun, bal: bank.balance, bi: G.bi,
  });
};

const continueRun = () => {
  const G = KT.run;
  if (!G || KT.save.gems < 1) return;
  KT.save.gems--;
  KT.persist();
  G.hp = Math.round(G.hpMax * 0.5);
  G.shells.length = 0;
  if (G.timeLeft <= 0) G.timeLeft = 15;
  G.phase = 'play';
};

const pauseRun = () => {
  const G = KT.run;
  if (!G || !['play', 'intro', 'tally', 'levelUp'].includes(G.phase)) return;
  G.prePause = G.phase;
  G.phase = 'paused';
};
const resumeRun = () => { if (KT.run && KT.run.phase === 'paused') KT.run.phase = KT.run.prePause || 'play'; };

/* ---------- acciones de la interfaz ---------- */
const buyWeapon = id => {
  const s = KT.save;
  if (id === 'bomb') {
    if (s.coins < KT.BOMB.price) return;
    s.coins -= KT.BOMB.price; s.owned.bomb = true;
  } else {
    if (s.coins < KT.WEAPONS[id].price) return;
    s.coins -= KT.WEAPONS[id].price; s.owned[id] = true;
  }
  KT.persist();
};
const upgradeWeapon = id => {
  const s = KT.save;
  const c = id === 'bomb' ? KT.costs.bomb() : KT.costs.weapon(id);
  if (s.coins < c) return;
  s.coins -= c;
  s.lvl[id]++;
  KT.persist();
};
const buyUpg = key => {
  const u = KT.UPG[key];
  if (KT.save.coins < u.cost()) return;
  KT.save.coins -= u.cost();
  u.apply();
  KT.persist();
};

const back = () => { if (KT.backTo === 'map') openMap(); else KT.go('title'); };

const action = a => {
  const [name, arg] = a.split(':');
  const sd = KT.sceneData;
  switch (name) {
    case 'play': openMap(); break;
    case 'shop': KT.backTo = 'title'; KT.go('shop', { sel: KT.save.active }); break;
    case 'wheel': KT.backTo = 'title'; KT.go('wheel', {}); break;
    case 'settings': KT.prevScene = KT.scene; KT.go('settings', { prev: KT.scene }); break;
    case 'nop': break;
    case 'pickBank': sd.sel = Number(arg); break;
    case 'mapBack': KT.go('title'); break;
    case 'start': startRun(sd.sel || 0); break;
    case 'mapShop': KT.backTo = 'map'; KT.go('shop', { sel: KT.save.active }); break;
    case 'selectWeapon':
      sd.sel = arg;
      if (KT.save.owned[arg]) { KT.save.active = arg; KT.persist(); }
      break;
    case 'upgrade': upgradeWeapon(arg); break;
    case 'unlock': buyWeapon(arg); sd.sel = arg; break;
    case 'list': KT.go('shopList', { tab: 'car' }); break;
    case 'listTab': KT.go('shopList', { tab: arg }); break;
    case 'tab': sd.tab = arg; break;
    case 'buyUpg': buyUpg(arg); break;
    case 'shopBack': KT.go('shop', { sel: KT.save.active }); break;
    case 'shopNext': openMap(); break;
    case 'spin': KT.spin(); break;
    case 'wheelBack': back(); break;
    case 'resultDone': openMap(); break;
    case 'set':
      if (arg === 'hs') sd.note = 'Aún sin puntuaciones guardadas';
      else if (arg === 'ach') sd.note = 'Sin logros en esta versión';
      else if (arg === 'snd') sd.note = 'Esta versión no tiene sonido';
      else if (arg === 'reset') {
        if (sd.confirm) { KT.resetSave(); KT.persist(); sd.confirm = false; sd.note = 'Progreso borrado'; }
        else { sd.confirm = true; }
      }
      break;
    case 'settingsClose': KT.go(sd.prev || 'title'); break;
    case 'tipDone': beginRun(); break;
    case 'resume': resumeRun(); break;
    case 'quit': finishRun(false); break;
    case 'continue': continueRun(); break;
    case 'giveUp': finishRun(false); break;
    default: break;
  }
  if (name !== 'set' && sd.confirm) sd.confirm = false;
};

/* ---------- superposiciones de la partida ---------- */
const drawRunPanels = gc => {
  const G = KT.run;
  KT.hits = [];
  if (G.phase === 'paused') {
    gc.fillStyle = 'rgba(0,0,0,.45)'; gc.fillRect(0, 0, W, H);
    KT.panel(gc, 60, 300, 270, 230, '#fffdf7', 18, 2.6);
    KT.hand(gc, 'Pausa', W / 2, 340, 40, KT.INK, '700');
    KT.btn(gc, { x: 90, y: 378, w: 210, h: 50, label: 'Seguir', style: 'go', size: 24, action: 'resume' });
    KT.btn(gc, { x: 90, y: 442, w: 210, h: 50, label: 'Abandonar el banco', style: 'warn', size: 19, action: 'quit' });
  } else if (G.phase === 'dead') {
    gc.fillStyle = 'rgba(0,0,0,.45)'; gc.fillRect(0, 0, W, H);
    KT.panel(gc, 40, 270, 310, 290, '#fffdf7', 18, 2.6);
    KT.hand(gc, G.deadTitle, W / 2, 312, 34, '#e0523b', '700');
    KT.hand(gc, G.deadMsg, W / 2, 352, 19, KT.INK, '400');
    const canContinue = KT.save.gems >= 1;
    KT.btn(gc, { x: 70, y: 392, w: 250, h: 50, label: 'Reintentar (1 gema)', style: 'go', size: 21, action: 'continue', disabled: !canContinue });
    KT.btn(gc, { x: 70, y: 456, w: 250, h: 50, label: 'Rendirse', style: 'plain', size: 21, action: 'giveUp' });
  }
};

/* ---------- entrada ---------- */
const toLogical = e => {
  const r = canvas.getBoundingClientRect();
  return { x: (e.clientX - r.left) / r.width * W, y: (e.clientY - r.top) / r.height * H };
};
const dist = (p, x, y) => Math.hypot(p.x - x, p.y - y);

let dragging = false;
canvas.addEventListener('pointerdown', e => {
  const p = toLogical(e);
  if (KT.scene === 'run' && KT.run) {
    const G = KT.run;
    if (G.phase === 'paused' || G.phase === 'dead') {
      const a = KT.uiTap(p.x, p.y);
      if (a) action(a);
      return;
    }
    if (G.phase === 'done') return;
    if (dist(p, W * 0.135, H * 0.13) < 28) { G.auto = !G.auto; return; }
    if (dist(p, W * 0.92, H * 0.034) < 26) { pauseRun(); return; }
    if (dist(p, W * 0.5, H * 0.905) < 42) { KT.useBomb(G); return; }
    if (G.auto) G.auto = false;
    dragging = true;
    G.targetX = Math.max(-0.9, Math.min(0.9, (p.x - W / 2) / 95));
    return;
  }
  if (KT.scene === 'tip') { action('tipDone'); return; }
  const a = KT.uiTap(p.x, p.y);
  if (a) action(a);
});
canvas.addEventListener('pointermove', e => {
  if (!dragging || !KT.run || KT.run.phase !== 'play') return;
  const p = toLogical(e);
  KT.run.targetX = Math.max(-0.9, Math.min(0.9, (p.x - W / 2) / 95));
});
const endDrag = () => { dragging = false; };
window.addEventListener('pointerup', endDrag);
window.addEventListener('pointercancel', endDrag);

window.addEventListener('keydown', e => {
  KT.keys[e.key] = true;
  if (KT.scene !== 'run' || !KT.run) return;
  const G = KT.run;
  if (e.key === 'a' || e.key === 'A') G.auto = !G.auto;
  else if (e.key === ' ') { e.preventDefault(); KT.useBomb(G); }
  else if (e.key === 'p' || e.key === 'P' || e.key === 'Escape') {
    if (G.phase === 'paused') resumeRun(); else pauseRun();
  }
});
window.addEventListener('keyup', e => { KT.keys[e.key] = false; });
document.addEventListener('visibilitychange', () => { if (document.hidden) pauseRun(); });

const fit = () => {
  const k = Math.min(window.innerWidth / W, window.innerHeight / H);
  document.documentElement.style.setProperty('--k', String(k));
};
window.addEventListener('resize', fit);
fit();

/* ---------- bucle ---------- */
let lastT = performance.now();
const frame = now => {
  const dt = Math.min(0.05, (now - lastT) / 1000);
  lastT = now;
  if (KT.scene === 'run' && KT.run) {
    if (KT.run.phase !== 'paused' && KT.run.phase !== 'dead') KT.updateRun(KT.run, dt);
    if (KT.run.phase === 'done') finishRun(true);
  }
  g.setTransform(DPR, 0, 0, DPR, 0, 0);
  if (KT.scene === 'run' && KT.run) {
    g.clearRect(0, 0, W, H);
    KT.drawRun(g, KT.run);
    drawRunPanels(g);
  } else {
    KT.drawScene(g);
  }
  requestAnimationFrame(frame);
};

KT.init().then(() => {
  KT.go('title');
  requestAnimationFrame(frame);
});

/* Gancho de solo lectura para pruebas automáticas */
window.KittenTaxi = {
  state() {
    const G = KT.run;
    return {
      app: KT.scene,
      run: G && {
        phase: G.phase, wave: G.wave, level: G.level, boss: G.boss, hp: Math.round(G.hp),
        timeLeft: +G.timeLeft.toFixed(2), stolen: G.stolen, destroyed: G.destroyed,
        enemies: G.enemies.filter(e => !e.dead).length, bombs: G.bombs, auto: G.auto,
        shells: G.shells.length, combo: G.combo, px: +G.px.toFixed(3), targetX: +G.targetX.toFixed(3), bubble: !!G.bubble, playT: +G.playT.toFixed(2),
      },
      coins: KT.save.coins,
      gems: KT.save.gems,
    };
  },
  startRun(i) { KT.go('map', { sel: i }); startRun(i); },
  press(key) { window.dispatchEvent(new KeyboardEvent('keydown', { key })); },
  action,
};
})();
