/* Kitten Taxi: arte procedural. Sprites a lápiz pre-renderizados y fondos. */
(() => {
'use strict';
const KT = (window.KT = window.KT || {});

KT.INK = '#2b2b2b';
KT.W = 390;
KT.H = 844;
KT.HORIZON = 372;          // línea de las ruedas del coche = horizonte
KT.S = 2;                  // supersampling de los sprites

KT.rng = seed => {
  let s = (seed >>> 0) || 2463534242;
  return () => {
    s ^= s << 13; s >>>= 0;
    s ^= s >>> 17;
    s ^= s << 5; s >>>= 0;
    return s / 4294967296;
  };
};

KT.canvas = (w, h) => {
  const c = document.createElement('canvas');
  c.width = Math.max(1, Math.ceil(w));
  c.height = Math.max(1, Math.ceil(h));
  return c;
};

/* ---------- formas ---------- */
KT.rrPts = (x, y, w, h, r, n = 6) => {
  const pts = [];
  const corners = [
    [x + w - r, y + r, -Math.PI / 2, 0],
    [x + w - r, y + h - r, 0, Math.PI / 2],
    [x + r, y + h - r, Math.PI / 2, Math.PI],
    [x + r, y + r, Math.PI, Math.PI * 1.5],
  ];
  for (const [cx, cy, a0, a1] of corners) {
    for (let i = 0; i <= n; i++) {
      const a = a0 + (a1 - a0) * i / n;
      pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
    }
  }
  return pts;
};
KT.ellPts = (cx, cy, rx, ry, n = 36) => {
  const p = [];
  for (let i = 0; i < n; i++) {
    const a = i / n * Math.PI * 2;
    p.push([cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]);
  }
  return p;
};
KT.pathPts = (g, pts) => {
  g.beginPath();
  pts.forEach(([x, y], i) => (i ? g.lineTo(x, y) : g.moveTo(x, y)));
};

/* Trazo a lápiz: dos pasadas con desviación fija (rnd sólo al generar el sprite). */
KT.pencil = (g, pts, lw, rnd, closed = false, color = KT.INK) => {
  const n = pts.length;
  g.save();
  g.strokeStyle = color;
  g.lineCap = 'round';
  g.lineJoin = 'round';
  for (let pass = 0; pass < 2; pass++) {
    g.globalAlpha = pass ? 0.45 : 0.95;
    g.lineWidth = pass ? lw * 0.55 : lw;
    g.beginPath();
    const last = closed ? n : n - 1;
    for (let i = 0; i <= last; i++) {
      const [x, y] = pts[i % n];
      const jx = x + (rnd() - 0.5) * lw * 0.9;
      const jy = y + (rnd() - 0.5) * lw * 0.9;
      if (i) g.lineTo(jx, jy); else g.moveTo(jx, jy);
    }
    g.stroke();
  }
  g.restore();
};

/* Relleno + contorno a lápiz. */
KT.shape = (g, pts, fill, lw, rnd) => {
  KT.pathPts(g, pts);
  g.closePath();
  if (fill) { g.fillStyle = fill; g.fill(); }
  if (lw) KT.pencil(g, pts, lw, rnd, true);
};

/* Sombreado con líneas diagonales recortado a la forma. */
KT.hatch = (g, pts, gap = 4, angle = -0.8, alpha = 0.3, color = KT.INK) => {
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const [x, y] of pts) {
    x0 = Math.min(x0, x); y0 = Math.min(y0, y);
    x1 = Math.max(x1, x); y1 = Math.max(y1, y);
  }
  g.save();
  KT.pathPts(g, pts);
  g.closePath();
  g.clip();
  g.strokeStyle = color;
  g.globalAlpha = alpha;
  g.lineWidth = 1;
  const dx = Math.cos(angle), dy = Math.sin(angle);
  const px = -dy, py = dx;
  const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  const d = Math.hypot(x1 - x0, y1 - y0);
  g.beginPath();
  for (let t = -d; t <= d; t += gap) {
    const ox = cx + px * t, oy = cy + py * t;
    g.moveTo(ox - dx * d, oy - dy * d);
    g.lineTo(ox + dx * d, oy + dy * d);
  }
  g.stroke();
  g.restore();
};

/* Texto manuscrito centrado. */
KT.hand = (g, text, x, y, size, color = KT.INK, weight = '') => {
  g.font = `${weight} ${size}px "Patrick Hand", "Comic Sans MS", cursive`.trim();
  g.fillStyle = color;
  g.textAlign = 'center';
  g.textBaseline = 'middle';
  g.fillText(text, x, y);
};

/* ---------- sprites ---------- */
KT.makeSprite = (w, h, seed, draw) => {
  const S = KT.S;
  const c = KT.canvas(w * S, h * S);
  const g = c.getContext('2d');
  // origen en el centro inferior del sprite
  g.setTransform(S, 0, 0, S, (w / 2) * S, h * S);
  draw(g, KT.rng(seed), w, h);
  return { c, w, h, ox: w / 2, oy: h };
};
// dibuja con el punto de anclaje (centro inferior) en x,y
KT.drawSprite = (g, spr, x, y, s = 1, alpha = 1) => {
  if (alpha < 1) g.globalAlpha = alpha;
  g.drawImage(spr.c, x - spr.ox * s, y - spr.oy * s, spr.w * s, spr.h * s);
  if (alpha < 1) g.globalAlpha = 1;
};

const wheel = (g, rnd, x, y, r) => {
  KT.shape(g, KT.ellPts(x, y, r, r, 20), '#2f2f2f', 2, rnd);
  KT.shape(g, KT.ellPts(x, y, r * 0.42, r * 0.42, 14), '#c9c9c9', 1.2, rnd);
};

const catHead = (g, rnd, x, y, s) => {
  // cabeza de gato asomando por el techo
  const ear = (sx) => [[x + sx * 14 * s, y - 8 * s], [x + sx * 20 * s, y - 30 * s], [x + sx * 3 * s, y - 16 * s]];
  KT.shape(g, ear(-1), '#ffffff', 2, rnd);
  KT.shape(g, ear(1), '#ffffff', 2, rnd);
  KT.shape(g, KT.ellPts(x, y, 20 * s, 17 * s, 26), '#ffffff', 2.2, rnd);
  g.fillStyle = KT.INK;
  g.beginPath(); g.arc(x - 7 * s, y - 2 * s, 2.2 * s, 0, Math.PI * 2); g.fill();
  g.beginPath(); g.arc(x + 7 * s, y - 2 * s, 2.2 * s, 0, Math.PI * 2); g.fill();
  g.fillStyle = '#f08a9b';
  g.beginPath(); g.arc(x, y + 4 * s, 2 * s, 0, Math.PI * 2); g.fill();
  g.strokeStyle = KT.INK; g.lineWidth = 0.9;
  g.beginPath();
  g.moveTo(x - 10 * s, y + 4 * s); g.lineTo(x - 20 * s, y + 2 * s);
  g.moveTo(x - 10 * s, y + 7 * s); g.lineTo(x - 20 * s, y + 9 * s);
  g.moveTo(x + 10 * s, y + 4 * s); g.lineTo(x + 20 * s, y + 2 * s);
  g.moveTo(x + 10 * s, y + 7 * s); g.lineTo(x + 20 * s, y + 9 * s);
  g.stroke();
};

const carBody = (g, rnd, col, w, bodyTop, cabinW, cabinH, glass) => {
  // carrocería, cabina y ventanas de un coche visto de frente
  const half = w / 2;
  KT.shape(g, KT.rrPts(-half, bodyTop, w, 40, 12), col, 2.6, rnd);
  KT.hatch(g, KT.rrPts(-half + 4, bodyTop + 26, w - 8, 12, 6), 4, -0.6, 0.25);
  KT.shape(g, KT.rrPts(-cabinW / 2, bodyTop - cabinH + 8, cabinW, cabinH, 12), col, 2.2, rnd);
  KT.shape(g, KT.rrPts(-cabinW / 2 + 9, bodyTop - cabinH + 16, cabinW - 18, cabinH - 20, 7), glass, 1.6, rnd);
  // reflejo
  g.save(); g.globalAlpha = 0.5; g.strokeStyle = '#ffffff'; g.lineWidth = 2;
  g.beginPath(); g.moveTo(-cabinW / 2 + 16, bodyTop - cabinH + 22); g.lineTo(-cabinW / 2 + 28, bodyTop - cabinH + 32); g.stroke(); g.restore();
  // paragolpes y faros
  KT.shape(g, KT.rrPts(-half - 2, bodyTop + 34, w + 4, 6, 3), '#3a3a3a', 1.6, rnd);
};

KT.buildSprites = () => {
  const SP = (KT.sprites = {});

  // Taxi amarillo visto de frente, con el gato asomado por el techo
  const taxi = (name, col, seed) => SP[name] = KT.makeSprite(170, 124, seed, (g, rnd) => {
    KT.shadow(g, 0, -4, 80, 9);
    carBody(g, rnd, col, 140, -54, 96, 40, '#9fd0ee');
    // letrero de taxi
    KT.shape(g, KT.rrPts(-14, -100, 28, 9, 2), '#fff3b0', 1.4, rnd);
    catHead(g, rnd, 0, -88, 1.05);
    // ruedas
    wheel(g, rnd, -46, -12, 13);
    wheel(g, rnd, 46, -12, 13);
    // luces delanteras
    g.fillStyle = '#fff6c4';
    g.beginPath(); g.ellipse(-57, -34, 6, 4, 0, 0, Math.PI * 2); g.fill();
    g.beginPath(); g.ellipse(57, -34, 6, 4, 0, 0, Math.PI * 2); g.fill();
  });
  taxi('taxi', '#f3b72a', 11);
  taxi('taxiGold', '#ffd84a', 12);

  SP.police = KT.makeSprite(150, 118, 21, (g, rnd) => {
    KT.shadow(g, 0, -4, 74, 9);
    carBody(g, rnd, '#3b6fd0', 124, -50, 84, 36, '#22324f');
    // franja blanca y placa
    KT.shape(g, KT.rrPts(-62, -30, 124, 8, 3), '#f4f4f4', 1.2, rnd);
    // barra de luces
    KT.shape(g, KT.rrPts(-18, -72, 36, 13, 4), '#ffffff', 1.4, rnd);
    g.fillStyle = '#e0523b'; g.fillRect(-16, -69, 15, 7);
    g.fillStyle = '#2b6cb0'; g.fillRect(1, -69, 15, 7);
    wheel(g, rnd, -40, -10, 12);
    wheel(g, rnd, 40, -10, 12);
  });

  SP.sedan = KT.makeSprite(150, 110, 31, (g, rnd) => {
    KT.shadow(g, 0, -4, 74, 8);
    carBody(g, rnd, '#7aa5e0', 128, -44, 84, 30, '#cfe6f8');
    wheel(g, rnd, -42, -10, 12);
    wheel(g, rnd, 42, -10, 12);
    g.fillStyle = '#fff1a8';
    g.beginPath(); g.ellipse(-52, -26, 5, 3.5, 0, 0, Math.PI * 2); g.fill();
    g.beginPath(); g.ellipse(52, -26, 5, 3.5, 0, 0, Math.PI * 2); g.fill();
  });

  SP.van = KT.makeSprite(160, 176, 41, (g, rnd) => {
    KT.shadow(g, 0, -4, 80, 10);
    KT.shape(g, KT.rrPts(-64, -162, 128, 140, 8), '#f7f7f2', 2.6, rnd);
    KT.hatch(g, KT.rrPts(-60, -90, 120, 60, 6), 4, -0.6, 0.18);
    KT.shape(g, KT.rrPts(-48, -150, 96, 46, 6), '#a9d3ec', 1.8, rnd);
    KT.shape(g, KT.rrPts(-64, -92, 128, 9, 2), '#e0523b', 1.4, rnd);
    KT.shape(g, KT.rrPts(-40, -60, 80, 28, 4), '#dfe6ea', 1.4, rnd);
    wheel(g, rnd, -48, -12, 14);
    wheel(g, rnd, 48, -12, 14);
  });

  SP.bossBlue = KT.makeSprite(300, 250, 51, (g, rnd) => {
    KT.shadow(g, 0, -4, 128, 13);
    KT.shape(g, KT.rrPts(-120, -190, 240, 164, 12), '#3b78c0', 3, rnd);
    KT.hatch(g, KT.rrPts(-118, -120, 236, 90, 10), 5, -0.6, 0.22);
    KT.shape(g, KT.rrPts(-112, -236, 224, 52, 10), '#f7f7f2', 2.6, rnd);
    KT.shape(g, KT.rrPts(-70, -226, 140, 26, 6), '#a9d3ec', 1.8, rnd);
    // torreta y cañón
    KT.shape(g, KT.ellPts(0, -246, 26, 10, 18), '#cfd6dc', 2, rnd);
    KT.shape(g, KT.rrPts(-14, -300 + 60, 28, 14, 3), '#2f2f2f', 2, rnd);
    wheel(g, rnd, -100, -18, 26);
    wheel(g, rnd, 100, -18, 26);
    wheel(g, rnd, -40, -18, 22);
    wheel(g, rnd, 40, -18, 22);
  });

  SP.bossYellow = KT.makeSprite(300, 250, 61, (g, rnd) => {
    KT.shadow(g, 0, -4, 136, 13);
    KT.shape(g, KT.rrPts(-136, -62, 272, 42, 8), '#5c5c5c', 2.6, rnd);   // pala
    KT.hatch(g, KT.rrPts(-132, -58, 264, 36, 6), 5, 0.6, 0.35);
    KT.shape(g, KT.rrPts(-120, -196, 240, 140, 12), '#e9b53c', 3, rnd);
    KT.hatch(g, KT.rrPts(-116, -150, 232, 80, 10), 5, -0.6, 0.2);
    KT.shape(g, KT.rrPts(-76, -236, 152, 64, 10), '#f4e4a8', 2.4, rnd);
    KT.shape(g, KT.rrPts(-60, -226, 120, 22, 6), '#a9d3ec', 1.8, rnd);
    wheel(g, rnd, -110, -24, 26);
    wheel(g, rnd, 110, -24, 26);
  });

  SP.bottle = KT.makeSprite(26, 60, 71, (g, rnd) => {
    KT.shape(g, KT.rrPts(-7, -40, 14, 40, 5), '#d2432c', 1.8, rnd);
    KT.shape(g, KT.rrPts(-3.5, -52, 7, 14, 2), '#b53a24', 1.4, rnd);
    g.fillStyle = 'rgba(255,255,255,.55)';
    g.fillRect(-4, -34, 2.4, 20);
  });

  SP.dumpster = KT.makeSprite(96, 84, 81, (g, rnd) => {
    KT.shadow(g, 0, -2, 46, 6);
    KT.shape(g, KT.rrPts(-42, -64, 84, 62, 4), '#4f9d5a', 2.2, rnd);
    KT.hatch(g, KT.rrPts(-40, -40, 80, 36, 3), 5, 0.5, 0.25);
    KT.shape(g, KT.rrPts(-46, -74, 92, 11, 3), '#3a7d45', 2, rnd);
  });

  SP.clay = KT.makeSprite(60, 60, 91, (g, rnd) => {
    KT.shape(g, KT.ellPts(0, -26, 24, 20, 30), '#8fd16b', 2, rnd);
    g.fillStyle = '#6bb84a';
    g.beginPath(); g.ellipse(-9, -10, 4, 7, 0, 0, Math.PI * 2); g.fill();
    g.beginPath(); g.ellipse(10, -8, 3.5, 6, 0, 0, Math.PI * 2); g.fill();
    g.fillStyle = 'rgba(255,255,255,.6)';
    g.beginPath(); g.ellipse(-8, -32, 4, 2.5, -0.5, 0, Math.PI * 2); g.fill();
  });

  SP.crate = KT.makeSprite(84, 80, 101, (g, rnd) => {
    KT.shadow(g, 0, -2, 40, 6);
    KT.shape(g, KT.rrPts(-38, -70, 76, 70, 4), '#c9925a', 2.4, rnd);
    g.save(); g.globalAlpha = 0.45; g.strokeStyle = KT.INK; g.lineWidth = 1.4;
    g.beginPath(); g.moveTo(-36, -68); g.lineTo(36, -2); g.moveTo(36, -68); g.lineTo(-36, -2); g.stroke();
    g.restore();
    KT.hand(g, '?', 0, -36, 40, KT.INK, 'bold');
  });

  SP.coin = KT.makeSprite(34, 34, 111, (g, rnd) => {
    KT.shape(g, KT.ellPts(0, -17, 14, 14, 28), '#f6c33b', 1.8, rnd);
    g.strokeStyle = '#c98a0c'; g.lineWidth = 1.6;
    g.beginPath(); g.arc(0, -17, 8, 0, Math.PI * 2); g.stroke();
    g.fillStyle = 'rgba(255,255,255,.7)';
    g.beginPath(); g.ellipse(-5, -23, 3, 1.8, -0.6, 0, Math.PI * 2); g.fill();
  });

  SP.gem = KT.makeSprite(34, 34, 121, (g, rnd) => {
    KT.shape(g, [[0, -32], [13, -20], [0, -2], [-13, -20]], '#27b6e8', 1.8, rnd);
    KT.shape(g, [[-13, -20], [0, -20], [0, -2]], '#7fd9f5', 0, rnd);
    g.fillStyle = 'rgba(255,255,255,.8)';
    g.beginPath(); g.ellipse(-4, -26, 2.5, 1.5, -0.5, 0, Math.PI * 2); g.fill();
  });

  SP.bullet = KT.makeSprite(22, 14, 131, (g, rnd) => {
    KT.shape(g, KT.rrPts(-10, -9, 20, 8, 4), '#d2432c', 1.4, rnd);
    g.fillStyle = '#ffd6c8';
    g.beginPath(); g.arc(6, -5, 1.6, 0, Math.PI * 2); g.fill();
  });

  SP.warning = KT.makeSprite(46, 42, 141, (g, rnd) => {
    KT.shape(g, [[0, -40], [22, -2], [-22, -2]], '#e0523b', 2, rnd);
    KT.hand(g, '!', 0, -17, 30, '#ffffff', 'bold');
  });

  SP.burst = KT.makeSprite(170, 170, 151, (g, rnd) => {
    const pts = [];
    for (let i = 0; i < 28; i++) {
      const a = i / 28 * Math.PI * 2;
      const r = i % 2 ? 40 + rnd() * 14 : 78 + rnd() * 14;
      pts.push([Math.cos(a) * r, -85 + Math.sin(a) * r]);
    }
    KT.shape(g, pts, '#ffe16b', 2.2, rnd);
    KT.shape(g, KT.ellPts(0, -85, 26, 22, 20), '#fff7c9', 0, rnd);
  });

  SP.shell = KT.makeSprite(34, 34, 171, (g, rnd) => {
    KT.shape(g, KT.ellPts(0, -17, 13, 13, 26), '#2f2f2f', 2, rnd);
    g.fillStyle = 'rgba(255,255,255,.35)';
    g.beginPath(); g.ellipse(-4, -22, 3, 2, -0.6, 0, Math.PI * 2); g.fill();
    g.strokeStyle = '#b08a4a'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(5, -27); g.quadraticCurveTo(9, -34, 13, -31); g.stroke();
    g.fillStyle = '#ffd24a';
    g.beginPath(); g.arc(13, -31, 3, 0, Math.PI * 2); g.fill();
  });
  SP.smoke = KT.makeSprite(170, 120, 161, (g, rnd) => {
    for (const [x, y, r] of [[-40, -40, 34], [0, -54, 42], [42, -40, 34], [-22, -22, 26], [26, -22, 26]]) {
      KT.shape(g, KT.ellPts(x, y, r, r * 0.85, 22), '#ffffff', 1.6, rnd);
    }
    g.fillStyle = 'rgba(180,180,180,.35)';
    g.beginPath(); g.ellipse(10, -14, 60, 12, 0, 0, Math.PI * 2); g.fill();
  });
};

KT.shadow = (g, x, y, rx, ry) => {
  g.save();
  g.fillStyle = 'rgba(0,0,0,.16)';
  g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2); g.fill();
  g.restore();
};

/* ---------- fondos del cielo (por nivel) ---------- */
KT.PALETTES = [
  { top: '#e4e7ea', bot: '#f8f9fa', far: '#b7bec6', kind: 'city',   sun: false },
  { top: '#56a7e4', bot: '#e3f2fb', far: '#ffffff', kind: 'clouds', sun: false },
  { top: '#4a9bd9', bot: '#e0f1fb', far: '#5b8fb5', kind: 'mount',  sun: false },
  { top: '#f0a07c', bot: '#fbe2c8', far: '#c8687f', kind: 'mount',  sun: true  },
  { top: '#5aaee8', bot: '#e6f5ff', far: '#4a85ad', kind: 'mount',  sun: false },
  { top: '#b9a6e6', bot: '#f2ecff', far: '#7a68b8', kind: 'city',   sun: false },
];

KT.makeSky = (pal, seed) => {
  const W = KT.W, Hh = KT.HORIZON + 6;
  const c = KT.canvas(W * KT.S, Hh * KT.S);
  const g = c.getContext('2d');
  g.setTransform(KT.S, 0, 0, KT.S, 0, 0);
  const rnd = KT.rng(seed);
  const gr = g.createLinearGradient(0, 0, 0, KT.HORIZON);
  gr.addColorStop(0, pal.top);
  gr.addColorStop(1, pal.bot);
  g.fillStyle = gr;
  g.fillRect(0, 0, W, Hh);
  if (pal.sun) {
    g.fillStyle = 'rgba(255,236,190,.9)';
    g.beginPath(); g.arc(W * 0.7, 150, 46, 0, Math.PI * 2); g.fill();
  }
  // nubes acuarela
  if (pal.kind === 'clouds' || pal.kind === 'mount') {
    for (let i = 0; i < 9; i++) {
      const x = rnd() * W, y = 40 + rnd() * 170, r = 30 + rnd() * 36;
      const cg = g.createRadialGradient(x, y, 2, x, y, r);
      cg.addColorStop(0, 'rgba(255,255,255,.95)');
      cg.addColorStop(1, 'rgba(255,255,255,0)');
      g.fillStyle = cg;
      g.beginPath(); g.ellipse(x, y, r * 1.5, r * 0.7, 0, 0, Math.PI * 2); g.fill();
    }
  }
  if (pal.kind === 'city') {
    for (let i = 0; i < 13; i++) {
      const x = i * 32 - 6 + rnd() * 6, w = 24 + rnd() * 18, h = 70 + rnd() * 120;
      g.fillStyle = pal.far;
      g.fillRect(x, KT.HORIZON - h, w, h);
      KT.pencil(g, KT.rrPts(x, KT.HORIZON - h, w, h, 1, 1), 1.4, rnd, true, '#6b737c');
      g.fillStyle = 'rgba(255,255,255,.55)';
      for (let wy = KT.HORIZON - h + 10; wy < KT.HORIZON - 8; wy += 14) {
        for (let wx = x + 5; wx < x + w - 6; wx += 9) g.fillRect(wx, wy, 4, 5);
      }
    }
  } else {
    // montañas con picos
    g.fillStyle = pal.far;
    g.beginPath();
    g.moveTo(-10, KT.HORIZON);
    for (let x = -10; x <= W + 10; x += 40) {
      g.lineTo(x + 20, KT.HORIZON - 40 - rnd() * 90);
      g.lineTo(x + 40, KT.HORIZON - 10 - rnd() * 20);
    }
    g.lineTo(W + 10, KT.HORIZON);
    g.closePath();
    g.fill();
  }
  // línea del horizonte, a lápiz
  KT.pencil(g, [[-4, KT.HORIZON], [W + 4, KT.HORIZON]], 2, rnd, false);
  return c;
};

/* Textura de grano de papel (una sola vez). */
KT.makeGrain = () => {
  const c = KT.canvas(160, 160);
  const g = c.getContext('2d');
  const id = g.createImageData(160, 160);
  const rnd = KT.rng(777);
  for (let i = 0; i < id.data.length; i += 4) {
    const v = 200 + rnd() * 55;
    id.data[i] = id.data[i + 1] = id.data[i + 2] = v;
    id.data[i + 3] = 40 + rnd() * 30;
  }
  g.putImageData(id, 0, 0);
  return c;
};

/* Líneas de velocidad: cuadriláteros afilados desde el horizonte hacia abajo. */
KT.speedLines = (() => {
  const rnd = KT.rng(4242);
  const arr = [];
  for (let i = 0; i < 46; i++) {
    arr.push({ x: (rnd() < 0.5 ? -1 : 1) * (0.25 + rnd() * 1.45), p: rnd(), len: 0.22 + rnd() * 0.45, w: 0.8 + rnd() * 2.2 });
  }
  return arr;
})();

KT.init = async () => {
  try { await document.fonts.load('40px "Patrick Hand"'); } catch (e) { /* sin fuente: se usa la de respaldo */ }
  KT.grain = KT.makeGrain();
  KT.buildSprites();
};
})();
