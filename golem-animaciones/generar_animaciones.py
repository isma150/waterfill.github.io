"""Genera clips de animación nuevos para el golem de piedra y los añade a un GLB.

Uso:
    python3 generar_animaciones.py <entrada.glb> <salida.glb>

Cada clip nuevo se construye a partir de un clip mocap del propio GLB:
  1. Remapeo temporal con curvas de easing (preparación, golpe, impacto, recuperación).
  2. Retraso por cadena: antebrazo, mano y cabeza van 2-4 fotogramas detrás del brazo.
  3. Exageración del giro respecto al reposo, con tope de ángulo en cadera, columna y cabeza.
  4. Peso corporal: la cadera baja en la preparación y vuelve en el impacto.
Los 23 clips originales se mantienen intactos. Los clips nuevos llevan en `extras`
los instantes de impacto, para que el motor dispare el hit-stop y los efectos.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_lib import Glb, Writer, qmul, qconj, qnorm, qslerp, sample_channel  # noqa: E402

FPS = 60
DT = 1.0 / FPS


# ---------- utilidades ----------
def qpow_v(q, k):
    """Versión vectorizada de glb_lib.qpow: k escalar o array (N,)."""
    q = qnorm(q)
    q = np.where(q[:, 3:4] < 0, -q, q)
    w = np.clip(q[:, 3], -1, 1)
    angle = 2 * np.arccos(w)
    s = np.sqrt(np.maximum(1 - w * w, 0.0))
    safe = s > 1e-8
    axis = np.where(safe[:, None], q[:, :3] / np.maximum(s, 1e-8)[:, None], np.array([1.0, 0, 0]))
    na = angle * k
    return np.concatenate([axis * np.sin(na / 2)[:, None], np.cos(na / 2)[:, None]], axis=1)


def angle_of(q):
    return 2 * np.arccos(np.clip(np.abs(q[:, 3]), 0, 1))


def ease(kind, u):
    u = np.clip(u, 0, 1)
    if kind == 'in':        # arranca lento, acaba rápido (golpe)
        return u * u
    if kind == 'out':       # arranca rápido, frena (recuperación)
        return 1 - (1 - u) * (1 - u)
    if kind == 'inout':     # suave en ambos extremos (preparación)
        return u * u * (3 - 2 * u)
    return u                # lineal


def piecewise_map(keys):
    """keys: lista de (t_salida, t_fuente, easing) del segmento que empieza en esa clave.

    Devuelve una función t_salida -> t_fuente, monótona, con easing por segmento.
    """
    def f(t):
        t = np.asarray(t, dtype=np.float64)
        out = np.empty_like(t)
        for i in range(len(keys) - 1):
            t0, s0, kind = keys[i]
            t1, s1, _ = keys[i + 1]
            m = (t >= t0) & (t <= t1)
            if t1 > t0:
                out[m] = s0 + (s1 - s0) * ease(kind, (t[m] - t0) / (t1 - t0))
        out[t < keys[0][0]] = keys[0][1]
        out[t > keys[-1][0]] = keys[-1][1]
        return out
    return f


def group_of(name):
    n = name.replace('mixamorig:', '')
    if n in ('Hips',):
        return 'hips'
    if n.startswith('Spine'):
        return 'spine'
    if n.startswith('Neck') or n.startswith('Head'):
        return 'head'
    if 'Shoulder' in n:
        return 'shoulder'
    if 'ForeArm' in n:
        return 'forearm'
    if 'Hand' in n:
        return 'hand'
    if 'Arm' in n:
        return 'arm'
    return 'leg'


# Ganancias, retrasos (fotogramas a 60 fps) y topes de ángulo por grupo de hueso.
GROUP_RULES = {
    'arm':      {'gain': 1.0,  'lag': 0, 'max_deg': None},
    'shoulder': {'gain': 1.0,  'lag': 1, 'max_deg': 30},
    'forearm':  {'gain': 1.0,  'lag': 2, 'max_deg': None},
    'hand':     {'gain': 1.0,  'lag': 4, 'max_deg': None},
    'spine':    {'gain': 1.0,  'lag': 1, 'max_deg': 35},
    'hips':     {'gain': 1.0,  'lag': 0, 'max_deg': 40},
    'head':     {'gain': 1.0,  'lag': 3, 'max_deg': 25},
    'leg':      {'gain': 1.0,  'lag': 0, 'max_deg': None},
}


def rotate_vec(q, v):
    """Aplica el cuaternión q (xyzw) al vector v."""
    return qmul(qmul(q, np.concatenate([v, [0.0]])), qconj(q))[:3]


def parent_world_rot(g, node):
    """Rotación en reposo del padre en espacio de mundo (producto de los ancestros)."""
    chain = []
    p = g.parent.get(node)
    while p is not None:
        chain.append(p)
        p = g.parent.get(p)
    w = np.array([0.0, 0.0, 0.0, 1.0])
    for a in reversed(chain):
        w = qmul(w, g.rest_trs(a)[1])
    return w


def pose_at(g, clip, t):
    """Rotación local de cada hueso en el instante t de un clip existente: {node: (4,)}."""
    samples, _ = g.sample_clip(clip)
    pose = {}
    for node in g.joints:
        ch = samples.get(node, {})
        if 'r' in ch:
            pose[node] = sample_channel(ch['r'][0], ch['r'][1], np.array([t]), rotation=True)[0]
        else:
            pose[node] = g.rest_trs(node)[1]
    return pose


def build_clip(g, spec):
    """Construye los tracks de un clip nuevo. Devuelve (grid, rot{node}, trn{node})."""
    src_samples, src_dur = g.sample_clip(spec['src'])
    total = spec['duration']
    grid = np.arange(0, total + 1e-9, DT)
    tmap = piecewise_map(spec['timeline'])
    settle = spec.get('settle')
    neutral = pose_at(g, spec.get('settle_clip', 'Idle'), 0.0) if settle else None
    # Ancla de la cadera: posición neutra de Idle (t=0). Es la postura que usan los clips.
    idle_samples, _ = g.sample_clip('Idle')
    idle_hips = idle_samples[g.index['mixamorig:Hips']]['t']
    hips_anchor = sample_channel(idle_hips[0], idle_hips[1], np.array([0.0]))[0]

    rot, trn = {}, {}
    for node in g.joints:
        name = g.names[node]
        rules = GROUP_RULES[group_of(name)]
        rest_t, rest_r, _ = g.rest_trs(node)
        lag = rules['lag'] * DT
        src_t = tmap(np.maximum(grid - lag, 0))
        ch = src_samples.get(node, {})
        if 'r' in ch:
            q_src = sample_channel(ch['r'][0], ch['r'][1], src_t, rotation=True)
        else:
            q_src = np.tile(rest_r, (len(grid), 1))
        # Delta respecto al reposo en espacio local del hueso.
        delta = qmul(qconj(rest_r)[None, :].repeat(len(grid), 0), q_src)
        gain = spec.get('gain_override', {}).get(name, rules['gain'])
        delta = qpow_v(delta, gain)
        if rules['max_deg'] is not None:
            ang = np.degrees(angle_of(delta))
            k = np.minimum(1.0, rules['max_deg'] / np.maximum(ang, 1e-6))
            delta = qpow_v(delta, k)
        q_out = qnorm(qmul(rest_r[None, :].repeat(len(grid), 0), delta))
        if settle:
            # Asentamiento: la pose vuelve a la postura neutra (Idle, t=0) tras el impacto.
            s0, s1 = settle
            b = ease('inout', (grid - s0) / (s1 - s0))
            q_out = qslerp(q_out, neutral[node][None, :].repeat(len(grid), 0), b[:, None])
        # Continuidad de hemisferio para que no haya giros de 360 grados.
        for i in range(1, len(q_out)):
            if np.dot(q_out[i], q_out[i - 1]) < 0:
                q_out[i] = -q_out[i]
        rot[node] = q_out.astype(np.float32)

        if name == 'mixamorig:Hips':
            dip = piecewise_map([(t, v, 'lin') for t, v in spec['dip']])(grid)
            base = rest_t[None, :] + np.zeros((len(grid), 3))
            if 't' in ch:
                base = sample_channel(ch['t'][0], ch['t'][1], src_t)
            # `dip` va en el eje Y del mundo. Golem_Rig gira 90° en X, así que el eje Y
            # local de la cadera apunta al Z del mundo: el vector se convierte al espacio local.
            up_local = rotate_vec(qconj(parent_world_rot(g, node)), np.array([0.0, 1.0, 0.0]))
            # Sin desplazamiento horizontal: del mocap solo se conserva la altura de la cadera.
            vertical = (base - hips_anchor[None, :]) @ up_local
            trn[node] = (hips_anchor[None, :] + (vertical + dip)[:, None] * up_local[None, :]).astype(np.float32)
    return grid, rot, trn


# ---------- definición de los clips ----------
CLIPS = [
    {
        # Golpe pesado con preparación: base Punch2, pausa en el impacto y recuperación suave.
        'name': 'Golpe_Pesado_v2',
        'src': 'Punch2',
        'duration': 1.30,
        # (t_salida, t_fuente, easing del tramo que sale de esta clave)
        'timeline': [
            (0.00, 0.00, 'inout'),
            (0.30, 0.45, 'inout'),   # preparación: el brazo se carga hacia atrás
            (0.40, 0.58, 'in'),      # última fase de carga
            (0.50, 0.95, 'in'),      # aceleración del golpe
            (0.58, 1.20, 'out'),     # impacto
            (0.70, 1.26, 'out'),     # pausa de impacto (hit-stop visual)
            (1.30, 2.05, 'out'),     # recuperación
        ],
        # Peso: la cadera baja al cargar y sube en el golpe.
        'dip': [(0.00, 0.0), (0.30, -0.035), (0.50, -0.012), (0.70, 0.0), (1.30, 0.0)],
        'settle': (0.70, 1.30),  # vuelve a la postura Idle después del impacto
        'extras': {'impactos_s': [0.58], 'hit_stop_s': [0.58, 0.70]},
    },
    {
        # Salto con caída: agachado, despegue, suspensión, caída rápida y aterrizaje
        # con compresión de cadera. Base: Jump (mocap del propio GLB).
        'name': 'Salto_Impacto_v2',
        'src': 'Jump',
        'duration': 1.70,
        'timeline': [
            (0.00, 0.00, 'inout'),   # agachado (preparación)
            (0.35, 0.20, 'in'),      # despegue
            (0.50, 0.40, 'out'),     # suspensión en el aire
            (0.95, 0.72, 'lin'),     # inicio de la caída
            (1.05, 0.90, 'in'),      # aterrizaje: impacto
            (1.15, 0.95, 'out'),     # pausa de impacto
            (1.70, 1.00, 'out'),     # fin
        ],
        'dip': [(0.00, 0.0), (0.35, -0.06), (0.50, 0.05), (0.95, 0.05),
                (1.05, -0.10), (1.20, -0.03), (1.70, 0.0)],
        'settle': (1.15, 1.70),
        'extras': {'impactos_s': [1.05], 'hit_stop_s': [1.05, 1.15]},
    },
    {
        # Puñetazo recto: base Golpe02_Cruzado (el brazo avanza en línea recta).
        # Las piernas casi no se mueven en ese clip, así que se exagera su ganancia.
        'name': 'Golpe_Recto_v2',
        'src': 'Golpe02_Cruzado',
        'duration': 1.25,
        'timeline': [
            (0.00, 0.00, 'inout'),   # preparación
            (0.25, 0.15, 'inout'),   # carga del brazo
            (0.40, 0.30, 'in'),      # inicio del avance
            (0.50, 0.40, 'in'),      # aceleración del golpe
            (0.58, 0.60, 'out'),     # impacto
            (0.70, 0.62, 'out'),     # pausa de impacto (hit-stop visual)
            (1.25, 1.20, 'out'),     # recuperación
        ],
        'dip': [(0.00, 0.0), (0.25, -0.03), (0.50, -0.01), (0.70, 0.0), (1.25, 0.0)],
        'settle': (0.70, 1.25),
        'gain_override': {
            'mixamorig:LeftUpLeg': 1.5, 'mixamorig:RightUpLeg': 1.5,
            'mixamorig:LeftLeg': 1.5, 'mixamorig:RightLeg': 1.5,
        },
        'extras': {'impactos_s': [0.58], 'hit_stop_s': [0.58, 0.70]},
    },
]


def main(src, out):
    g = Glb(src)
    w = Writer(g)
    for spec in CLIPS:
        grid, rot, trn = build_clip(g, spec)
        w.add_animation(spec['name'], grid, rot, trn, extras=spec.get('extras'))
        print(f"{spec['name']}: {len(grid)} fotogramas, {spec['duration']:.2f}s")
    w.save(out)
    print('guardado', out)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
