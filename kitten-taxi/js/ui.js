/* Kitten Taxi: pantallas de menú dibujadas en canvas, con zonas de toque. */
(() => {
'use strict';
const KT = window.KT;
const W = KT.W, H = KT.H, INK = KT.INK;
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);

KT.hits = [];
KT.scene = 'title';
KT.sceneData = {};
KT.go = (name, data) => { KT.scene = name; KT.sceneData = data || {}; };

const STYLE = {
  go:    { fill: '#4caf32', text: '#ffffff' },
  blue:  { fill: '#3aa0e8', text: '#ffffff' },
  red:   { fill: '#ef7b5f', text: '#ffffff' },
  grey:  { fill: '#8c8c8c', text: '#ffffff' },
  plain: { fill: '#fffdf7', text: INK },
  dark:  { fill: '#1d1d1d', text: '#ffffff' },
  paper: { fill: '#f1efe8', text: INK },
  warn:  { fill: '#e0523b', text: '#ffffff' },
};

/* Botón a lápiz con zona de toque. */
KT.btn = (g, o) => {
  const st = STYLE[o.style || 'plain'];
  const seed = Math.round(o.x * 13 + o.y * 7) || 1;
  KT.shape(g, KT.rrPts(o.x, o.y, o.w, o.h, o.r || 14, 5), o.disabled ? '#d9d9d9' : st.fill, 2.2, KT.rng(seed));
  const size = o.size || 22;
  KT.hand(g, o.label, o.x + o.w / 2, o.y + o.h / 2 + 1, size, o.disabled ? '#8a8a8a' : st.text, '700');
  if (!o.disabled && o.action) KT.hits.push({ x: o.x, y: o.y, w: o.w, h: o.h, action: o.action });
};

KT.panel = (g, x, y, w, h, fill = '#fffdf7', r = 16, lw = 2.4) => {
  KT.shape(g, KT.rrPts(x, y, w, h, r, 6), fill, lw, KT.rng(Math.round(x * 3 + y * 5 + w)));
};

KT.tap = (x, y, w, h, action) => KT.hits.push({ x, y, w, h, action });

/* ---------- iconos dibujados ---------- */
KT.icon = (g, kind, cx, cy, s = 1) => {
  g.save();
  g.translate(cx, cy);
  g.scale(s, s);
  const rnd = KT.rng(kind.length * 31 + 7);
  if (kind === 'pistol') {
    KT.shape(g, KT.rrPts(-26, -10, 40, 12, 4), '#4a4a4a', 1.8, rnd);
    KT.shape(g, KT.rrPts(-10, 2, 12, 16, 3), '#4a4a4a', 1.8, rnd);
    KT.shape(g, KT.rrPts(-26, -10, 20, 8, 3), '#7a7a7a', 1.2, rnd);
  } else if (kind === 'bomb') {
    KT.shape(g, KT.ellPts(0, 4, 17, 17, 26), '#3b3b3b', 2, rnd);
    g.strokeStyle = '#8a6a3a'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(8, -12); g.quadraticCurveTo(14, -24, 22, -20); g.stroke();
    g.fillStyle = '#ffb347'; g.beginPath(); g.arc(22, -20, 4, 0, Math.PI * 2); g.fill();
  } else if (kind === 'shot') {
    KT.shape(g, KT.rrPts(-30, -8, 56, 10, 4), '#4a4a4a', 1.8, rnd);
    KT.shape(g, KT.rrPts(-30, 2, 24, 12, 4), '#6b4a2b', 1.8, rnd);
    KT.shape(g, KT.rrPts(-6, 2, 10, 16, 3), '#4a4a4a', 1.8, rnd);
  } else if (kind === 'machine') {
    KT.shape(g, KT.rrPts(-26, -10, 52, 16, 4), '#4a4a4a', 1.8, rnd);
    KT.shape(g, KT.rrPts(-6, 6, 10, 18, 3), '#4a4a4a', 1.8, rnd);
    KT.shape(g, KT.rrPts(-30, -14, 20, 8, 3), '#7a7a7a', 1.2, rnd);
  } else if (kind === 'car') {
    KT.drawSprite(g, KT.sprites.taxi, 0, 20, 0.36);
  } else if (kind === 'driver') {
    KT.shape(g, KT.ellPts(0, -6, 14, 16, 22), '#ffffff', 1.8, rnd);
    KT.shape(g, KT.rrPts(-16, 12, 32, 16, 6), '#ffffff', 1.8, rnd);
    g.fillStyle = INK; g.beginPath(); g.arc(-5, -8, 2, 0, Math.PI * 2); g.arc(5, -8, 2, 0, Math.PI * 2); g.fill();
  } else if (kind === 'assist') {
    KT.shape(g, KT.ellPts(0, 2, 18, 14, 22), '#ffffff', 1.8, rnd);
    KT.shape(g, [[-14, -6], [-10, -22], [-2, -10]], '#ffffff', 1.8, rnd);
    KT.shape(g, [[14, -6], [10, -22], [2, -10]], '#ffffff', 1.8, rnd);
  } else if (kind === 'pet') {
    KT.shape(g, KT.ellPts(0, 4, 17, 13, 22), '#ffffff', 1.8, rnd);
    KT.shape(g, KT.ellPts(0, -10, 10, 9, 18), '#ffffff', 1.8, rnd);
  } else if (kind === 'lock') {
    KT.shape(g, KT.rrPts(-13, -2, 26, 22, 4), '#9a9a9a', 1.8, rnd);
    g.strokeStyle = '#9a9a9a'; g.lineWidth = 3.5;
    g.beginPath(); g.arc(0, -4, 9, Math.PI, 0); g.stroke();
  } else if (kind === 'coin') {
    KT.shape(g, KT.ellPts(0, 0, 14, 14, 24), '#f6c33b', 1.8, rnd);
  } else if (kind === 'gem') {
    KT.shape(g, [[0, -16], [12, -4], [0, 14], [-12, -4]], '#27b6e8', 1.8, rnd);
  } else if (kind === 'key') {
    g.strokeStyle = '#c9c9c9'; g.lineWidth = 3;
    g.beginPath(); g.arc(0, -8, 7, 0, Math.PI * 2); g.stroke();
    g.beginPath(); g.moveTo(0, -1); g.lineTo(0, 16); g.moveTo(0, 10); g.lineTo(5, 10); g.stroke();
  } else if (kind === 'check') {
    g.strokeStyle = '#2e8b2e'; g.lineWidth = 3.5; g.lineCap = 'round';
    g.beginPath(); g.moveTo(-8, 0); g.lineTo(-2, 7); g.lineTo(9, -8); g.stroke();
  }
  g.restore();
};

/* ---------- fondos cacheados ---------- */
KT.bg = {};

KT.bgStreet = () => {
  if (KT.bg.street) return KT.bg.street;
  const c = KT.canvas(W * KT.S, H * KT.S);
  const g = c.getContext('2d');
  g.setTransform(KT.S, 0, 0, KT.S, 0, 0);
  const rnd = KT.rng(5151);
  g.fillStyle = '#f2f3f5'; g.fillRect(0, 0, W, H);
  // edificios de los lados con ventanas
  const wall = (x0, w, col) => {
    g.fillStyle = col; g.fillRect(x0, 0, w, 600);
    KT.pencil(g, [[x0, 0], [x0, 600]], 2, rnd, false);
    for (let y = 18; y < 560; y += 30) for (let x = x0 + 10; x < x0 + w - 16; x += 26) {
      KT.shape(g, KT.rrPts(x, y, 14, 18, 2, 2), '#f9fbfc', 1.2, rnd);
    }
    KT.hatch(g, KT.rrPts(x0, 0, w, 600, 1, 1), 6, 1.0, 0.12);
  };
  wall(-8, 150, '#d8dde3');
  wall(252, 150, '#d2d8df');
  // calzada y aceras
  g.fillStyle = '#e9ebee';
  g.beginPath(); g.moveTo(0, 430); g.lineTo(W, 430); g.lineTo(W, H); g.lineTo(0, H); g.closePath(); g.fill();
  KT.pencil(g, [[0, 452], [W, 452]], 2, rnd, false);
  KT.pencil(g, [[0, 600], [W, 600]], 1.5, rnd, false);
  // letrero BANK vertical
  KT.shape(g, KT.rrPts(132, 150, 32, 230, 4), '#ffffff', 2.2, rnd);
  for (let i = 0; i < 4; i++) KT.hand(g, 'BANK'[i], 148, 170 + i * 42, 26, INK, '700');
  // papelera y coche lejano
  KT.shape(g, KT.rrPts(-6, 560, 62, 90, 6), '#bfc5cc', 2.2, rnd);
  KT.hatch(g, KT.rrPts(-6, 560, 62, 90, 6), 6, 0.7, 0.2);
  KT.shape(g, KT.rrPts(170, 412, 46, 22, 8), '#9aa3ad', 1.8, rnd);
  KT.bg.street = c;
  return c;
};

KT.bgMap = () => {
  if (KT.bg.map) return KT.bg.map;
  const c = KT.canvas(W * KT.S, H * KT.S);
  const g = c.getContext('2d');
  g.setTransform(KT.S, 0, 0, KT.S, 0, 0);
  const rnd = KT.rng(8080);
  g.fillStyle = '#f3e9d0'; g.fillRect(0, 0, W, H);
  // parques
  for (const [x, y, w, h] of [[20, 600, 150, 110], [250, 720, 130, 90], [290, 240, 80, 70]]) {
    KT.shape(g, KT.rrPts(x, y, w, h, 18, 6), '#9fcf8a', 1.8, rnd);
    for (let i = 0; i < 6; i++) KT.shape(g, KT.ellPts(x + 14 + rnd() * (w - 28), y + 14 + rnd() * (h - 28), 9, 9, 14), '#6ba85a', 1.2, rnd);
  }
  // manzanas de edificios
  for (let gy = 40; gy < 820; gy += 58) {
    for (let gx = 12; gx < 390; gx += 62) {
      if (rnd() < 0.2) continue;
      const bw = 44 + rnd() * 8, bh = 40 + rnd() * 8;
      KT.shape(g, KT.rrPts(gx, gy, bw, bh, 4, 3), '#d7cfbd', 1.8, rnd);
      KT.hatch(g, KT.rrPts(gx, gy, bw, bh, 4, 3), 7, 0.9, 0.12);
      KT.shape(g, [[gx - 3, gy], [gx + bw / 2, gy - 10], [gx + bw + 3, gy]], '#c9a27a', 1.6, rnd);
      g.fillStyle = 'rgba(255,255,255,.7)';
      for (let wx = gx + 6; wx < gx + bw - 8; wx += 12) g.fillRect(wx, gy + 8, 6, 8);
    }
  }
  // calles blancas con borde
  g.strokeStyle = '#ffffff'; g.lineWidth = 8; g.lineCap = 'round';
  for (let y = 100; y < 830; y += 116) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y + 8); g.stroke(); }
  KT.bg.map = c;
  return c;
};

KT.bgBeach = () => {
  if (KT.bg.beach) return KT.bg.beach;
  const c = KT.canvas(W * KT.S, 260 * KT.S);
  const g = c.getContext('2d');
  g.setTransform(KT.S, 0, 0, KT.S, 0, 0);
  const rnd = KT.rng(606);
  const sky = g.createLinearGradient(0, 0, 0, 120);
  sky.addColorStop(0, '#6cc2ee'); sky.addColorStop(1, '#bfe8fb');
  g.fillStyle = sky; g.fillRect(0, 0, W, 130);
  // mar
  g.fillStyle = '#3fb0d4'; g.fillRect(0, 96, W, 42);
  g.strokeStyle = '#ffffff'; g.lineWidth = 2;
  for (let x = 10; x < W; x += 34) { g.beginPath(); g.moveTo(x, 110 + (x % 3) * 4); g.quadraticCurveTo(x + 8, 104, x + 16, 110); g.stroke(); }
  // arena
  g.fillStyle = '#f5e2b2'; g.fillRect(0, 136, W, 124);
  KT.pencil(g, [[0, 136], [W, 136]], 2, rnd, false);
  // nubes
  g.fillStyle = 'rgba(255,255,255,.9)';
  for (const [x, y, r] of [[120, 36, 18], [140, 30, 22], [160, 40, 14], [300, 58, 14], [316, 52, 18]]) { g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill(); }
  // palmera
  g.strokeStyle = '#8a5a2b'; g.lineWidth = 8; g.lineCap = 'round';
  g.beginPath(); g.moveTo(58, 150); g.quadraticCurveTo(44, 110, 60, 70); g.stroke();
  for (let i = 0; i < 6; i++) {
    const a = -Math.PI / 2 + (i - 2.5) * 0.45;
    g.fillStyle = i % 2 ? '#4fa54a' : '#3d8c3a';
    g.beginPath(); g.ellipse(60 + Math.cos(a) * 26, 68 + Math.sin(a) * 14, 26, 8, a, 0, Math.PI * 2); g.fill();
  }
  // cabaña de paja
  KT.shape(g, [[296, 150], [336, 98], [380, 150]], '#d9a441', 2, rnd);
  KT.hatch(g, [[296, 150], [336, 98], [380, 150]], 5, 0.6, 0.3);
  g.fillStyle = '#8a5a2b'; g.fillRect(302, 150, 6, 30); g.fillRect(372, 150, 6, 30);
  // gatos
  for (const [x, y] of [[62, 210], [330, 206]]) {
    KT.shape(g, KT.ellPts(x, y, 18, 14, 22), '#ffffff', 1.8, rnd);
    KT.shape(g, [[x - 12, y - 8], [x - 10, y - 24], [x - 2, y - 12]], '#ffffff', 1.6, rnd);
    KT.shape(g, [[x + 12, y - 8], [x + 10, y - 24], [x + 2, y - 12]], '#ffffff', 1.6, rnd);
    g.fillStyle = INK; g.beginPath(); g.arc(x - 5, y - 2, 2, 0, Math.PI * 2); g.arc(x + 5, y - 2, 2, 0, Math.PI * 2); g.fill();
  }
  KT.bg.beach = c;
  return c;
};

/* ---------- utilidades de escena ---------- */
const coinRow = (g, x, y, n, gems, keys) => {
  KT.icon(g, 'coin', x + 10, y, 0.55);
  KT.hand(g, KT.fmt(n), x + 26, y, 20, INK, '700');
  g.textAlign = 'center';
  if (gems !== undefined) {
    KT.icon(g, 'gem', x + 120, y, 0.55);
    KT.hand(g, String(gems), x + 136, y, 20, INK, '700');
  }
  if (keys) for (let i = 0; i < 5; i++) KT.icon(g, 'key', x + 180 + i * 22, y, 0.5);
};

/* ---------- escena: título ---------- */
const drawTitle = g => {
  g.drawImage(KT.bgStreet(), 0, 0, W, H);
  // logo manuscrito arriba a la izquierda, como en el original
  g.save();
  g.translate(44, 150);
  g.rotate(-0.1);
  g.lineJoin = 'round';
  g.font = '700 104px "Patrick Hand", "Comic Sans MS", cursive';
  g.textAlign = 'left'; g.textBaseline = 'middle';
  g.lineWidth = 14; g.strokeStyle = '#ffffff'; g.strokeText('Kitten', 0, 0);
  g.fillStyle = INK; g.fillText('Kitten', 0, 0);
  g.font = '700 64px "Patrick Hand", "Comic Sans MS", cursive';
  g.lineWidth = 10; g.strokeText('Taxi', 150, 72); g.fillStyle = '#f2a33a'; g.fillText('Taxi', 150, 72);
  g.restore();
  KT.btn(g, { x: 40, y: 640, w: 100, h: 40, label: 'Tienda', style: 'plain', size: 18, action: 'shop' });
  KT.btn(g, { x: 150, y: 640, w: 100, h: 40, label: 'Rueda', style: 'plain', size: 18, action: 'wheel' });
  KT.btn(g, { x: 260, y: 640, w: 100, h: 40, label: 'Ajustes', style: 'grey', size: 17, action: 'settings' });
  KT.btn(g, { x: 60, y: 735, w: 150, h: 44, label: 'GameCenter', style: 'plain', size: 17, action: 'nop' });
  KT.btn(g, { x: 220, y: 735, w: 110, h: 44, label: 'Guest', style: 'go', size: 20, action: 'play' });
};

/* ---------- escena: consejo de carga (antes de cada banco) ---------- */
const drawTip = g => {
  g.drawImage(KT.bgStreet(), 0, 0, W, H);
  g.fillStyle = 'rgba(255,255,255,.7)'; g.fillRect(0, 760, W, 84);
  const d = KT.sceneData;
  KT.hand(g, d.text || '', W / 2, 785, 19, INK, '700');
  KT.hand(g, '· toca para empezar ·', W / 2, 820, 16, '#6d6a63', '400');
  KT.tap(0, 0, W, H, 'tipDone');
};

/* ---------- escena: mapa ---------- */
const MAP_NODES = [
  { x: 110, y: 520 }, { x: 275, y: 440 }, { x: 120, y: 360 },
  { x: 275, y: 280 }, { x: 120, y: 200 }, { x: 260, y: 130 },
];
KT.MAP_NODES = MAP_NODES;

const drawBankIcon = (g, x, y, locked, done, level) => {
  const rnd = KT.rng(Math.round(x * 3 + y));
  KT.shape(g, KT.rrPts(x - 24, y - 20, 48, 40, 5, 4), done ? '#f2c94c' : '#e7e1d2', 2.2, rnd);
  KT.shape(g, [[x - 28, y - 20], [x, y - 36], [x + 28, y - 20]], '#7b5e3c', 2, rnd);
  g.fillStyle = INK; g.fillRect(x - 6, y - 4, 12, 24);
  KT.hand(g, String(level), x, y + 30, 18, INK, '700');
  if (locked) {
    KT.shape(g, KT.rrPts(x - 12, y - 6, 24, 18, 4), '#555', 1.6, rnd);
    g.strokeStyle = '#555'; g.lineWidth = 3; g.beginPath(); g.arc(x, y - 8, 7, Math.PI, 0); g.stroke();
  }
};

const drawMap = g => {
  g.drawImage(KT.bgMap(), 0, 0, W, H);
  const save = KT.save;
  // ruta amarilla entre bancos
  g.save();
  g.lineCap = 'round'; g.lineJoin = 'round';
  const path = () => {
    g.beginPath();
    MAP_NODES.forEach((n, i) => (i ? g.lineTo(n.x, n.y) : g.moveTo(n.x, n.y)));
  };
  g.strokeStyle = INK; g.lineWidth = 17; path(); g.stroke();
  g.strokeStyle = '#f2c94c'; g.lineWidth = 12; path(); g.stroke();
  g.restore();
  g.save();
  KT.hand(g, 'Ranking Stage', 118, 690, 22, '#3f8a2d', '700');
  g.restore();
  MAP_NODES.forEach((n, i) => {
    const bk = save.banks[i];
    drawBankIcon(g, n.x, n.y, !bk.unlocked, bk.done, bk.level);
    if (bk.unlocked) KT.tap(n.x - 30, n.y - 36, 60, 76, 'pickBank:' + i);
  });
  // globo de información del banco seleccionado
  const sel = clamp(KT.sceneData.sel || 0, 0, MAP_NODES.length - 1);
  const n = MAP_NODES[sel], bk = save.banks[sel];
  const bx = clamp(n.x - 110, 14, W - 234), by = n.y - 150;
  KT.panel(g, bx, by, 220, 92, '#ffffff', 14, 2.2);
  g.save(); g.beginPath(); g.moveTo(n.x - 10, by + 90); g.lineTo(n.x, n.y - 44); g.lineTo(n.x + 10, by + 90); g.closePath(); g.fillStyle = '#ffffff'; g.fill(); g.restore();
  KT.hand(g, KT.BANKS[sel].name, bx + 110, by + 20, 19, INK, '700');
  KT.hand(g, 'Level ' + bk.level, bx + 50, by + 56, 17, INK, '400');
  KT.hand(g, 'Balances', bx + 160, by + 46, 15, INK, '400');
  KT.hand(g, KT.fmt(bk.balance), bx + 160, by + 66, 22, INK, '700');
  // pie
  g.fillStyle = '#ffffff'; g.fillRect(0, 760, W, 84);
  KT.btn(g, { x: 12, y: 782, w: 80, h: 42, label: 'Back', style: 'grey', size: 18, action: 'mapBack' });
  coinRow(g, 110, 803, save.coins, save.gems, true);
  KT.btn(g, { x: 298, y: 782, w: 80, h: 42, label: 'Start', style: bk.unlocked ? 'go' : 'grey', size: 18, action: 'start', disabled: !bk.unlocked });
  KT.btn(g, { x: 298, y: 660, w: 80, h: 36, label: 'Tienda', style: 'plain', size: 15, action: 'mapShop' });
};

/* ---------- escena: tienda (pantalla principal de ranuras) ---------- */
const SLOTS = [
  ['pistol', 'pistol'], ['bomb', 'bomb'], ['shot', 'shot'], ['machine', 'machine'],
  ['car', 'car'], ['driver', 'driver'], ['assist', 'assist'], ['pet', 'pet'],
  ['lock', 'lock'], ['lock', 'lock'], ['lock', 'lock'], ['lock', 'lock'],
];
KT.SLOTS = SLOTS;

const weaponUpgradeCost = id => (id === 'bomb' ? KT.costs.bomb() : KT.costs.weapon(id));
const weaponDisplay = id => {
  const sv = KT.save;
  if (id === 'bomb') return sv.owned.bomb ? { power: 'Daño ' + Math.round(KT.stats.bombDmg()), rate: '2 por ola' } : null;
  return sv.owned[id] ? { power: 'Power ' + KT.stats.weaponPower(id).toFixed(0), rate: 'shoot / 1 sec ' + KT.stats.weaponRate(id).toFixed(1) } : null;
};

const drawShop = g => {
  const save = KT.save;
  g.fillStyle = '#f4f4f0'; g.fillRect(0, 0, W, H);
  g.drawImage(KT.bgBeach(), 0, 0, W, 260);
  // engranaje, RATE y sobre
  KT.hits.push({ x: 4, y: 4, w: 46, h: 46, action: 'settings' });
  g.save(); g.fillStyle = '#8a8a8a'; g.beginPath(); g.arc(28, 28, 12, 0, Math.PI * 2); g.fill();
  g.fillStyle = '#ffffff'; g.beginPath(); g.arc(28, 28, 5, 0, Math.PI * 2); g.fill(); g.restore();
  KT.shape(g, KT.rrPts(150, 14, 90, 26, 13), '#ffffff', 1.8, KT.rng(3));
  KT.hand(g, 'RATE', 195, 27, 17, INK, '700');
  KT.shape(g, KT.rrPts(346, 16, 30, 22, 3), '#ffffff', 1.8, KT.rng(4));
  g.strokeStyle = INK; g.lineWidth = 1.6; g.beginPath(); g.moveTo(346, 17); g.lineTo(361, 29); g.lineTo(376, 17); g.stroke();
  // panel del arma seleccionada
  const sel = KT.sceneData.sel || 'pistol';
  const d = weaponDisplay(sel);
  KT.panel(g, 14, 262, 362, 78, '#ffffff', 16, 2.2);
  if (d) {
    KT.icon(g, sel, 58, 302, 0.9);
    KT.hand(g, KT.WEAPONS[sel] ? KT.WEAPONS[sel].name : KT.BOMB.name, 130, 284, 16, '#555', '400');
    KT.hand(g, d.power, 130, 306, 18, INK, '700');
    KT.hand(g, d.rate, 130, 328, 15, INK, '400');
    const price = weaponUpgradeCost(sel);
    KT.btn(g, { x: 268, y: 270, w: 100, h: 60, r: 10, label: 'Upgrade', style: 'blue', size: 17, action: 'upgrade:' + sel, disabled: !d || save.coins < price });
    KT.icon(g, 'coin', 292, 322, 0.5);
    KT.hand(g, KT.fmt(price), 306, 322, 15, '#fff', '700');
  } else {
    KT.hand(g, 'Desbloquear', 210, 300, 22, INK, '700');
    const price = sel === 'bomb' ? KT.BOMB.price : KT.WEAPONS[sel].price;
    KT.btn(g, { x: 258, y: 280, w: 110, h: 46, label: 'Buy ' + KT.fmt(price), style: 'go', size: 18, action: 'unlock:' + sel, disabled: save.coins < price });
  }
  // cuadrícula de ranuras
  SLOTS.forEach(([kind, id], i) => {
    const col = i % 4, row = Math.floor(i / 4);
    const x = 21 + col * 90, y = 364 + row * 90;
    const equipped = (id === save.active && save.owned[id]);
    KT.shape(g, KT.rrPts(x, y, 78, 78, 12, 5), '#ffffff', 2.2, KT.rng(i * 11 + 5));
    if (kind === 'lock') {
      KT.icon(g, 'lock', x + 39, y + 39, 1);
    } else if (id === 'pistol' || id === 'shot' || id === 'machine') {
      KT.icon(g, id, x + 39, y + 40, 0.9);
      if (!save.owned[id]) { KT.shape(g, KT.rrPts(x, y, 78, 78, 12, 5), 'rgba(255,255,255,.55)', 0, KT.rng(1)); KT.icon(g, 'lock', x + 39, y + 40, 0.8); }
      if (equipped) KT.icon(g, 'check', x + 66, y + 14, 0.8);
    } else {
      KT.icon(g, id, x + 39, y + 40, 0.9);
    }
    if (kind !== 'lock') {
      const action = (id === 'pistol' || id === 'shot' || id === 'machine' || id === 'bomb') ? 'selectWeapon:' + id
        : id === 'car' ? 'listTab:car' : id === 'driver' ? 'listTab:driver' : id === 'assist' ? 'listTab:assist' : 'listTab:pet';
      KT.tap(x, y, 78, 78, action);
    }
  });
  // SHOP, monedas y Next
  KT.btn(g, { x: 14, y: 690, w: 100, h: 48, label: 'SHOP', style: 'go', size: 22, action: 'list' });
  KT.btn(g, { x: 280, y: 690, w: 96, h: 48, label: 'Next', style: 'plain', size: 22, action: 'shopNext' });
  g.fillStyle = '#ffffff'; g.fillRect(0, 760, W, 84);
  coinRow(g, 110, 803, save.coins, save.gems, true);
};

/* ---------- escena: lista de tienda con pestañas ---------- */
const LIST_TABS = [['car', 'Car'], ['driver', 'Driver'], ['assist', 'Assist'], ['pet', 'Pet'], ['jewel', 'Coin Key Jewelry']];

const drawShopList = g => {
  const save = KT.save;
  g.fillStyle = '#f4f4f0'; g.fillRect(0, 0, W, H);
  const tab = KT.sceneData.tab || 'car';
  // pestañas
  LIST_TABS.forEach(([id, label], i) => {
    const x = 6 + i * 77, w = 74;
    KT.shape(g, KT.rrPts(x, 14, w, 42, 6, 4), tab === id ? '#f2c94c' : '#ffffff', 1.6, KT.rng(i + 90));
    KT.hand(g, label, x + w / 2, 35, id === 'jewel' ? 12 : 16, INK, '700');
    KT.tap(x, 14, w, 42, 'tab:' + id);
  });
  const rows = [];
  if (tab === 'car') {
    rows.push({ key: 'carHp', icon: 'car', name: 'Blindaje (Loadage)', desc: 'Vida máxima ' + KT.stats.maxHp() });
    rows.push({ key: 'magnet', icon: 'coin', name: 'Imán de monedas', desc: 'Radio ' + KT.stats.magnetR().toFixed(2) });
  } else if (tab === 'assist') {
    rows.push({ key: 'shield', icon: 'assist', name: 'Escudo', desc: save.shield + ' bloqueo(s) por ola' });
  } else if (tab === 'pet') {
    rows.push({ key: 'pet', icon: 'pet', name: 'Gato copiloto', desc: '+' + (KT.stats.coinValue() - 1) + ' moneda por recogida · +' + save.pet * 8 + ' % daño' });
  }
  if (!rows.length) {
    KT.hand(g, 'Sin artículos en esta versión', W / 2, 220, 22, '#6d6a63', '700');
  }
  rows.forEach((r, i) => {
    const y = 84 + i * 124;
    KT.panel(g, 14, y, 362, 110, '#ffffff', 14, 2);
    if (r.icon === 'car') KT.drawSprite(g, KT.sprites.taxi, 58, y + 86, 0.5);
    else KT.icon(g, r.icon, 58, y + 56, 1.1);
    KT.hand(g, r.name, 116, y + 30, 21, INK, '700');
    KT.hand(g, r.desc, 116, y + 56, 16, '#6d6a63', '400');
    const u = KT.UPG[r.key];
    const price = u.cost();
    KT.btn(g, { x: 262, y: y + 74, w: 104, h: 28, r: 8, label: 'Buy ' + KT.fmt(price), style: 'go', size: 15, action: 'buyUpg:' + r.key, disabled: save.coins < price });
  });
  KT.btn(g, { x: 12, y: 790, w: 100, h: 40, label: 'EXIT', style: 'grey', size: 20, action: 'shopBack' });
  coinRow(g, 150, 806, save.coins, save.gems, true);
};

/* ---------- escena: rueda ---------- */
KT.wheelRot = 0;
KT.spinning = false;
const drawWheel = g => {
  g.fillStyle = '#f8f7f2'; g.fillRect(0, 0, W, H);
  const cx = W / 2, cy = 258, R = 150, n = KT.PRIZES.length, seg = Math.PI * 2 / n;
  // soporte a lápiz
  KT.shape(g, [[cx - 40, cy + 120], [cx + 40, cy + 120], [cx + 70, cy + 230], [cx - 70, cy + 230]], '#ffffff', 0, KT.rng(3));
  KT.hatch(g, [[cx - 40, cy + 120], [cx + 40, cy + 120], [cx + 70, cy + 230], [cx - 70, cy + 230]], 5, 0.4, 0.45);
  KT.pencil(g, [[cx - 40, cy + 120], [cx - 70, cy + 230], [cx + 70, cy + 230], [cx + 40, cy + 120]], 2, KT.rng(4), true);
  KT.shape(g, KT.ellPts(cx, cy + 232, 90, 10, 26), '#e5e2d8', 1.6, KT.rng(5));
  // aro y segmentos
  KT.shape(g, KT.ellPts(cx, cy, R + 14, R + 14, 60), '#2a2a2a', 0, KT.rng(6));
  for (let i = 0; i < n; i++) {
    const a0 = KT.wheelRot + i * seg - Math.PI / 2, a1 = a0 + seg;
    g.beginPath(); g.moveTo(cx, cy); g.arc(cx, cy, R, a0, a1); g.closePath();
    g.fillStyle = '#fbfaf6'; g.fill();
    g.strokeStyle = INK; g.lineWidth = 2; g.stroke();
    const mid = a0 + seg / 2;
    const px = cx + Math.cos(mid) * (R - 46), py = cy + Math.sin(mid) * (R - 46);
    const p = KT.PRIZES[i];
    if (p.gems) {
      g.save(); g.translate(px, py); g.rotate(mid + Math.PI / 2); KT.icon(g, 'gem', 0, 0, 1.1); g.restore();
    } else if (p.key) {
      g.save(); g.translate(px, py); g.rotate(mid + Math.PI / 2); KT.icon(g, 'key', 0, 0, 1.2); g.restore();
    } else {
      g.save(); g.translate(px, py); g.rotate(mid + Math.PI / 2);
      g.fillStyle = '#f6c33b'; g.beginPath(); g.arc(0, 0, 26, 0, Math.PI * 2); g.fill();
      g.strokeStyle = INK; g.lineWidth = 2; g.stroke();
      KT.hand(g, p.t, 0, 1, 20, INK, '700');
      g.restore();
    }
  }
  // bombillas del aro
  for (let i = 0; i < 16; i++) {
    const a = i / 16 * Math.PI * 2;
    g.fillStyle = i % 2 ? '#f6c33b' : '#5ec24e';
    g.beginPath(); g.arc(cx + Math.cos(a) * (R + 14), cy + Math.sin(a) * (R + 14), 5, 0, Math.PI * 2); g.fill();
  }
  g.beginPath(); g.arc(cx, cy, 16, 0, Math.PI * 2); g.fillStyle = '#2a2a2a'; g.fill();
  // puntero rojo arriba
  KT.shape(g, [[cx - 14, cy - R - 26], [cx + 14, cy - R - 26], [cx, cy - R - 2]], '#e0523b', 2, KT.rng(7));
  // botones
  KT.btn(g, { x: 110, y: 560, w: 170, h: 46, label: 'SPIN', style: 'red', size: 26, action: 'spin', disabled: KT.spinning });
  KT.icon(g, 'coin', W / 2 - 14, 618, 0.5);
  KT.hand(g, KT.fmt(KT.costs.spin()), W / 2 + 2, 618, 17, INK, '700');
  KT.btn(g, { x: 14, y: 790, w: 84, h: 38, label: 'EXIT', style: 'grey', size: 18, action: 'wheelBack' });
  g.fillStyle = '#ffffff'; g.fillRect(0, 764, W, 80);
  coinRow(g, 120, 806, KT.save.coins, KT.save.gems, true);
  KT.hand(g, KT.sceneData.msg || '', W / 2, 740, 19, '#555', '700');
};

KT.spin = () => {
  if (KT.spinning) return;
  const cost = KT.costs.spin();
  if (KT.save.coins < cost) { KT.sceneData.msg = 'Te faltan monedas para girar.'; return; }
  KT.save.coins -= cost;
  KT.save.spins++;
  KT.persist();
  KT.spinning = true;
  KT.sceneData.msg = 'Girando…';
  const idx = Math.floor(Math.random() * KT.PRIZES.length);
  const seg = Math.PI * 2 / KT.PRIZES.length;
  const target = -(idx * seg + seg / 2);
  const start = KT.wheelRot;
  const base = start + Math.PI * 2 * (5 + Math.floor(Math.random() * 2));
  const delta = ((target - base) % (Math.PI * 2) + Math.PI * 4) % (Math.PI * 2);
  const end = base + delta;
  const t0 = performance.now(), dur = 3200;
  const step = now => {
    const k = Math.min(1, (now - t0) / dur);
    KT.wheelRot = start + (end - start) * (1 - Math.pow(1 - k, 3));
    if (k < 1) { requestAnimationFrame(step); return; }
    const p = KT.PRIZES[idx];
    KT.save.coins += p.coins || 0;
    KT.save.gems += p.gems || 0;
    if (p.key) KT.save.goldenKeys += p.key;
    KT.persist();
    KT.spinning = false;
    KT.sceneData.msg = '¡Premio: ' + (p.coins ? KT.fmt(p.coins) + ' monedas' : p.gems ? '1 gema' : 'llave dorada (coche dorado)') + '!';
  };
  requestAnimationFrame(step);
};

/* ---------- escena: resultados (fondo negro, filas a mano) ---------- */
const rowL = (g, label, y) => KT.hand(g, label, 46, y, 24, '#ffffff', '400');
const rowR = (g, value, y, size = 26) => {
  g.save();
  g.textAlign = 'right'; g.textBaseline = 'middle';
  g.font = `700 ${size}px "Patrick Hand", "Comic Sans MS", cursive`;
  g.fillStyle = '#ffffff';
  g.fillText(value, 344, y);
  g.restore();
};
const drawResult = g => {
  g.fillStyle = '#000000'; g.fillRect(0, 0, W, H);
  const d = KT.sceneData;
  KT.hand(g, d.title || '', W / 2, 150, 36, '#ffffff', '700');
  rowL(g, 'Coins stolen from bank', 250);
  rowR(g, KT.fmt(d.stolen), 250);
  rowL(g, 'Earn money by destroying', 302);
  rowR(g, KT.fmt(d.destroyed), 302);
  rowL(g, 'Per-Fect Bonus (0/-)', 354);
  rowR(g, d.perfect ? '+' + KT.fmt(d.perfect) : '0', 354);
  g.strokeStyle = '#ffffff'; g.lineWidth = 1.5; g.setLineDash([6, 5]);
  g.beginPath(); g.moveTo(46, 400); g.lineTo(344, 400); g.stroke(); g.setLineDash([]);
  rowL(g, 'Total', 436);
  rowR(g, KT.fmt(d.total), 436, 30);
  rowL(g, 'Gemas recogidas', 490);
  rowR(g, '+' + (d.gems || 0), 490, 22);
  rowL(g, 'Saldo restante del banco', 532);
  rowR(g, KT.fmt(d.bal || 0), 532, 22);
  KT.btn(g, { x: 95, y: 700, w: 200, h: 52, label: 'Volver al mapa', style: 'plain', size: 22, action: 'resultDone' });
};

/* ---------- escena: ajustes ---------- */
const drawSettings = g => {
  g.fillStyle = 'rgba(0,0,0,.35)'; g.fillRect(0, 0, W, H);
  KT.panel(g, 40, 180, 310, 470, '#fffdf7', 18, 2.6);
  KT.hand(g, 'Ajustes', W / 2, 220, 38, INK, '700');
  const items = [
    ['Mejores puntuaciones', 'hs'],
    ['Logros', 'ach'],
    ['Sonido (sin audio en esta versión)', 'snd'],
    ['Borrar progreso', 'reset'],
  ];
  items.forEach(([label, action], i) => {
    const y = 262 + i * 66;
    KT.btn(g, { x: 66, y, w: 258, h: 50, label: action === 'reset' && KT.sceneData.confirm ? '¿Seguro? Toca otra vez' : label, style: action === 'reset' ? 'warn' : 'plain', size: 17, action: 'set:' + action });
  });
  KT.btn(g, { x: 110, y: 560, w: 170, h: 46, label: 'Cerrar', style: 'dark', size: 22, action: 'settingsClose' });
  KT.hand(g, KT.sceneData.note || '', W / 2, 628, 17, '#555', '400');
};

/* ---------- despacho ---------- */
const renderScene = (g, name) => {
  switch (name) {
    case 'title': drawTitle(g); break;
    case 'tip': drawTip(g); break;
    case 'map': drawMap(g); break;
    case 'shop': drawShop(g); break;
    case 'shopList': drawShopList(g); break;
    case 'wheel': drawWheel(g); break;
    case 'result': drawResult(g); break;
    default: break;
  }
};

KT.drawScene = g => {
  KT.hits = [];
  g.save();
  g.clearRect(0, 0, W, H);
  if (KT.scene === 'settings') {
    renderScene(g, KT.sceneData.prev || 'title');
    drawSettings(g);
  } else {
    renderScene(g, KT.scene);
  }
  g.restore();
};

KT.uiTap = (x, y) => {
  for (let i = KT.hits.length - 1; i >= 0; i--) {
    const h = KT.hits[i];
    if (x >= h.x && x <= h.x + h.w && y >= h.y && y <= h.y + h.h) return h.action;
  }
  return null;
};
})();
