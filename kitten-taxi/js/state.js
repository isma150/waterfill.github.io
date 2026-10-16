/* Kitten Taxi: constantes, guardado y estadísticas compartidas. */
(() => {
'use strict';
const KT = window.KT;

KT.SAVE_KEY = 'kitten-taxi-html-v2';

KT.BANKS = [
  { name: 'Banco Lunar' },
  { name: 'Banco Mirador' },
  { name: 'Banco del Puerto' },
  { name: 'Banco Solano' },
  { name: 'Banco Ceniza' },
  { name: 'Banco Estrella' },
];
KT.bankBase = i => 100 + 50 * i;

KT.WEAPONS = {
  pistol:  { name: 'Pistola',       rate: 4.0, dmg: 3,   range: 0.45, lat: 0.5,  price: 0 },
  shot:    { name: 'Escopeta',      rate: 1.1, dmg: 2,   range: 0.3, lat: 0.45, price: 1500 },
  machine: { name: 'Ametralladora', rate: 9.0, dmg: 1.2, range: 0.5, lat: 0.55, price: 3000 },
};
KT.BOMB = { name: 'Bomba de arcilla', price: 800, dmg: 14, lvlBonus: 0.3 };

KT.ENEMY = {
  police: { hp: 10, vz: 0.05, reward: 10, fire: 2.4, ram: false },
  sedan:  { hp: 8,  vz: 0.15, reward: 12, fire: 0,   ram: true },
  van:    { hp: 22, vz: 0.03, reward: 22, fire: 2.8, ram: false },
};

KT.PRIZES = [
  { t: '50',           coins: 50 },
  { t: '100',          coins: 100 },
  { t: 'Gema',         gems: 1 },
  { t: '200',          coins: 200 },
  { t: 'Llave dorada', key: 1 },
  { t: '500',          coins: 500 },
  { t: 'Gema',         gems: 1 },
  { t: '30',           coins: 30 },
];

KT.TIPS = [
  'If you use the golden key while playing. The golden car shows up on your game play.',
  'Green clay bomb is to slow down my car.',
  'Upgrade a weapon to clear stages easily.',
  'Grenades and shotguns are the weapons that can strike around.',
];

KT.fmt = n => Math.round(n).toLocaleString('es-ES');

KT.defaultSave = () => ({
  coins: 300, gems: 2, goldenKeys: 0, spins: 0,
  owned: { pistol: true, shot: false, machine: false, bomb: false },
  lvl: { pistol: 1, shot: 1, machine: 1, bomb: 1 },
  active: 'pistol',
  carHp: 1, magnet: 1, shield: 0, pet: 0,
  seenTutorial: false,
  banks: KT.BANKS.map((b, i) => ({ level: 1, balance: KT.bankBase(i), unlocked: i === 0, done: false })),
});

KT.loadSave = () => {
  const d = KT.defaultSave();
  try {
    const s = JSON.parse(localStorage.getItem(KT.SAVE_KEY) || 'null');
    if (s && typeof s === 'object') {
      Object.assign(d, s);
      d.owned = Object.assign(KT.defaultSave().owned, s.owned || {});
      d.lvl = Object.assign(KT.defaultSave().lvl, s.lvl || {});
      if (!Array.isArray(s.banks) || s.banks.length !== KT.BANKS.length) d.banks = KT.defaultSave().banks;
    }
  } catch (e) { /* sin almacenamiento: partida nueva */ }
  return d;
};
KT.save = KT.loadSave();
KT.persist = () => {
  try { localStorage.setItem(KT.SAVE_KEY, JSON.stringify(KT.save)); } catch (e) { /* ignorar */ }
};
KT.resetSave = () => {
  try { localStorage.removeItem(KT.SAVE_KEY); } catch (e) { /* ignorar */ }
  KT.save = KT.defaultSave();
};

/* Estadísticas derivadas de la mejora actual. */
KT.stats = {
  maxHp: () => 50 + 30 * (KT.save.carHp - 1),
  magnetR: () => 0.2 + 0.08 * (KT.save.magnet - 1),
  weaponPower: id => KT.WEAPONS[id].dmg * (1 + 0.25 * (KT.save.lvl[id] - 1)) * (1 + 0.08 * KT.save.pet),
  weaponRate: id => KT.WEAPONS[id].rate * (1 + 0.1 * (KT.save.lvl[id] - 1)),
  bombDmg: () => KT.BOMB.dmg * (1 + KT.BOMB.lvlBonus * (KT.save.lvl.bomb - 1)),
  coinValue: () => 1 + KT.save.pet,
};

KT.costs = {
  weapon: id => Math.round(500 * Math.pow(KT.save.lvl[id], 1.25)),
  bomb: () => Math.round(500 * Math.pow(KT.save.lvl.bomb, 1.25)),
  spin: () => Math.min(1500, 500 + 225 * KT.save.spins),
};

KT.UPG = {
  carHp:  { name: 'Blindaje (Loadage)', cost: () => Math.round(400 * Math.pow(KT.save.carHp, 1.2)), apply: () => { KT.save.carHp++; } },
  magnet: { name: 'Imán de monedas',    cost: () => 300 * KT.save.magnet, apply: () => { KT.save.magnet++; } },
  shield: { name: 'Escudo',             cost: () => 500 * (KT.save.shield + 1), apply: () => { KT.save.shield++; } },
  pet:    { name: 'Gato copiloto',      cost: () => 600 * (KT.save.pet + 1), apply: () => { KT.save.pet++; } },
};
})();
