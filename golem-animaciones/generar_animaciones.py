"""Genera clips de animación nuevos para el golem de piedra y los añade a un GLB.

Uso:
    python3 generar_animaciones.py <entrada.glb> <salida.glb>

Cada clip nuevo se construye a partir de un clip mocap del propio GLB:
  1. Remapeo temporal con curvas de easing (preparación, golpe, impacto, recuperación).
  2. Retraso por cadena: antebrazo, mano y cabeza van 1-4 fotogramas detrás del brazo.
  3. Exageración del giro respecto al reposo, con tope de ángulo en cadera, columna y cabeza.
  4. Peso corporal: la cadera baja en la preparación y vuelve en el impacto.
  5. Postura de combate: los golpes v3 entran desde la postura y terminan en ella.

Clips generados:
  - Postura_Combate: bucle de 2 s (la primera y la última pose coinciden).
  - *_v2: primera versión (se conservan para comparar en el visor).
  - *_v3: tiempos medidos en el vídeo de referencia (preparación, pausa de impacto y
    recuperación completa), con `cancelable_s` para encadenar como en el combo.

Los 23 clips originales se mantienen intactos. Los impactos y las pausas van en `extras`.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_lib import Glb, Writer, qmul, qconj, qnorm, qslerp, sample_channel  # noqa: E402

FPS = 60
DT = 1.0 / FPS
BLEND_IN_S = 0.10          # 6 fotogramas: entrada desde la postura de combate
STANCE_PERIOD_S = 2.0      # duración del bucle Postura_Combate
STANCE_CROUCH = 0.5        # mezcla de piernas y cadera hacia la postura agachada (Jump t=0)
STANCE_DROP_M = -0.03      # la cadera baja 3 % de la altura en postura
STANCE_BREATH_DEG = 2.0    # respiración: giro de la columna


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


def hips_up_local(g):
    """Vector 'arriba' del mundo expresado en el espacio local de la cadera."""
    hips = g.index['mixamorig:Hips']
    return rotate_vec(qconj(parent_world_rot(g, hips)), np.array([0.0, 1.0, 0.0]))


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


def hips_translation_at(g, clip, t):
    samples, _ = g.sample_clip(clip)
    hips = g.index['mixamorig:Hips']
    ch = samples.get(hips, {})
    if 't' in ch:
        return sample_channel(ch['t'][0], ch['t'][1], np.array([t]))[0]
    return g.rest_trs(hips)[0]


def clamp_group_1d(g, node, q):
    """Aplica el tope de ángulo de su grupo a una rotación (4,) respecto al reposo."""
    max_deg = GROUP_RULES[group_of(g.names[node])]['max_deg']
    if max_deg is None:
        return q
    rest = g.rest_trs(node)[1]
    delta = qmul(qconj(rest), q)
    ang = np.degrees(angle_of(delta[None, :]))[0]
    if ang <= max_deg:
        return q
    return qnorm(qmul(rest, qpow_v(delta[None, :], max_deg / ang)[0]))


def stance_sources(g):
    """Poses de origen de la postura de combate: Idle (base), Punch2 t=0 (guardia de brazos),
    Jump t=0 (agachado para piernas y cadera) y la altura de cadera de Idle."""
    return {
        'base': pose_at(g, 'Idle', 0.0),
        'guard': pose_at(g, 'Punch2', 0.0),
        'crouch': pose_at(g, 'Jump', 0.0),
        'hips': hips_translation_at(g, 'Idle', 0.0),
    }


def stance_pose(g, src, t):
    """Postura de combate en el instante t. Devuelve ({node: (4,)}, cadera (3,))."""
    breath = np.radians(STANCE_BREATH_DEG) * np.sin(2 * np.pi * t / STANCE_PERIOD_S)
    breath_q = np.array([np.sin(breath / 2), 0.0, 0.0, np.cos(breath / 2)])
    rot = {}
    for node in g.joints:
        name = g.names[node]
        grp = group_of(name)
        if grp in ('arm', 'shoulder', 'forearm', 'hand'):
            q = src['guard'][node]
        elif grp in ('leg', 'hips'):
            q = qslerp(src['base'][node][None, :], src['crouch'][node][None, :], STANCE_CROUCH)[0]
            q = clamp_group_1d(g, node, q)
        else:
            q = src['base'][node]
        if name == 'mixamorig:Spine1':
            q = qnorm(qmul(q, breath_q))
        rot[node] = q
    hips = src['hips'] + STANCE_DROP_M * hips_up_local(g)
    return rot, hips


def build_stance_clip(g, src):
    """Postura_Combate: bucle exacto de STANCE_PERIOD_S (el último fotograma es el primero)."""
    grid = np.arange(0, STANCE_PERIOD_S + 1e-9, DT)
    frames = [stance_pose(g, src, t) for t in grid]
    rot = {n: np.stack([f[0][n] for f in frames]).astype(np.float32) for n in g.joints}
    hips = np.stack([f[1] for f in frames]).astype(np.float32)
    return grid, rot, {g.index['mixamorig:Hips']: hips}


def build_clip(g, spec, src):
    """Construye los tracks de un clip nuevo. Devuelve (grid, rot{node}, trn{node})."""
    src_samples, src_dur = g.sample_clip(spec['src'])
    total = spec['duration']
    grid = np.arange(0, total + 1e-9, DT)
    tmap = piecewise_map(spec['timeline'])
    settle = spec.get('settle')
    stance = spec.get('stance', False)
    lift_gain = spec.get('lift_gain', 1.0)
    if stance:
        stance_rot, stance_hips = stance_pose(g, src, 0.0)
        neutral = stance_rot
        hips_target = stance_hips
    else:
        neutral = pose_at(g, 'Idle', 0.0) if settle else None
        hips_target = None
    hips_anchor = src['hips']
    up_local = hips_up_local(g)

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
            # Asentamiento: la pose vuelve a la postura neutra tras el impacto.
            s0, s1 = settle
            b = ease('inout', (grid - s0) / (s1 - s0))
            q_out = qslerp(q_out, neutral[node][None, :].repeat(len(grid), 0), b[:, None])
        if stance:
            # Entrada: los primeros fotogramas parten exactamente de la postura de combate.
            w_in = ease('inout', grid / BLEND_IN_S)
            q_out = qslerp(np.tile(stance_rot[node], (len(grid), 1)), q_out, w_in[:, None])
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
            # Vertical del mundo convertido al espacio local (Golem_Rig gira 90° en X).
            # Sin desplazamiento horizontal: del mocap solo se conserva la altura.
            vertical = (base - hips_anchor[None, :]) @ up_local
            vertical = np.where(vertical > 0, vertical * lift_gain, vertical)
            trn_out = hips_anchor[None, :] + (vertical + dip)[:, None] * up_local[None, :]
            if stance:
                s0, s1 = settle
                b = ease('inout', (grid - s0) / (s1 - s0))
                trn_out = trn_out * (1 - b[:, None]) + hips_target[None, :] * b[:, None]
                w_in = ease('inout', grid / BLEND_IN_S)
                trn_out = hips_target[None, :] * (1 - w_in[:, None]) + trn_out * w_in[:, None]
            trn[node] = trn_out.astype(np.float32)
    return grid, rot, trn


# ---------- definición de los clips ----------
# Tiempos de v3 medidos en el vídeo de referencia (60 fps, contador de golpes como impacto):
#   puñetazo recto: preparación visible ~8-10 fotogramas, pausa de impacto ~4-5 fotogramas,
#   recuperación a la guardia ancha ~0,25 s. Se usa una preparación algo más larga para
#   que se lea a la velocidad del juego (la superposición amarilla oculta el inicio).
CLIPS = [
    {
        # v2: primer intento con preparación de 0,58 s. Se conserva para comparar.
        'name': 'Golpe_Pesado_v2',
        'src': 'Punch2',
        'duration': 1.30,
        'timeline': [
            (0.00, 0.00, 'inout'),
            (0.30, 0.45, 'inout'),
            (0.40, 0.58, 'in'),
            (0.50, 0.95, 'in'),
            (0.58, 1.20, 'out'),
            (0.70, 1.26, 'out'),
            (1.30, 2.05, 'out'),
        ],
        'dip': [(0.00, 0.0), (0.30, -0.035), (0.50, -0.012), (0.70, 0.0), (1.30, 0.0)],
        'settle': (0.70, 1.30),
        'extras': {'impactos_s': [0.58], 'hit_stop_s': [0.58, 0.70]},
    },
    {
        'name': 'Salto_Impacto_v2',
        'src': 'Jump',
        'duration': 1.70,
        'timeline': [
            (0.00, 0.00, 'inout'),
            (0.35, 0.20, 'in'),
            (0.50, 0.40, 'out'),
            (0.95, 0.72, 'lin'),
            (1.05, 0.90, 'in'),
            (1.15, 0.95, 'out'),
            (1.70, 1.00, 'out'),
        ],
        'dip': [(0.00, 0.0), (0.35, -0.06), (0.50, 0.05), (0.95, 0.05),
                (1.05, -0.10), (1.20, -0.03), (1.70, 0.0)],
        'settle': (1.15, 1.70),
        'extras': {'impactos_s': [1.05], 'hit_stop_s': [1.05, 1.15]},
    },
    {
        'name': 'Golpe_Recto_v2',
        'src': 'Golpe02_Cruzado',
        'duration': 1.25,
        'timeline': [
            (0.00, 0.00, 'inout'),
            (0.25, 0.15, 'inout'),
            (0.40, 0.30, 'in'),
            (0.50, 0.40, 'in'),
            (0.58, 0.60, 'out'),
            (0.70, 0.62, 'out'),
            (1.25, 1.20, 'out'),
        ],
        'dip': [(0.00, 0.0), (0.25, -0.03), (0.50, -0.01), (0.70, 0.0), (1.25, 0.0)],
        'settle': (0.70, 1.25),
        'gain_override': {
            'mixamorig:LeftUpLeg': 1.5, 'mixamorig:RightUpLeg': 1.5,
            'mixamorig:LeftLeg': 1.5, 'mixamorig:RightLeg': 1.5,
        },
        'extras': {'impactos_s': [0.58], 'hit_stop_s': [0.58, 0.70]},
    },
    {
        # v3: preparación corta desde la postura, impacto a 0,32 s, pausa de 5 fotogramas,
        # recuperación completa hasta la postura. Puede encadenarse desde 0,40 s.
        'name': 'Golpe_Recto_v3',
        'src': 'Golpe02_Cruzado',
        'duration': 1.20,
        'stance': True,
        'timeline': [
            (0.00, 0.00, 'inout'),
            (0.18, 0.22, 'inout'),   # preparación
            (0.26, 0.40, 'in'),      # avance
            (0.32, 0.60, 'out'),     # impacto
            (0.40, 0.62, 'out'),     # pausa de impacto (5 fotogramas)
            (1.20, 1.20, 'out'),     # recuperación completa
        ],
        'dip': [(0.00, 0.0), (0.18, -0.03), (0.32, -0.01), (0.45, 0.0), (1.20, 0.0)],
        'settle': (0.45, 1.10),
        'gain_override': {
            'mixamorig:LeftUpLeg': 1.5, 'mixamorig:RightUpLeg': 1.5,
            'mixamorig:LeftLeg': 1.5, 'mixamorig:RightLeg': 1.5,
        },
        'extras': {'impactos_s': [0.32], 'hit_stop_s': [0.32, 0.40], 'cancelable_s': 0.40},
    },
    {
        # v3: impacto a 0,40 s, pausa de 6 fotogramas, recuperación completa.
        'name': 'Golpe_Pesado_v3',
        'src': 'Punch2',
        'duration': 1.30,
        'stance': True,
        'timeline': [
            (0.00, 0.00, 'inout'),
            (0.14, 0.30, 'inout'),
            (0.24, 0.50, 'in'),
            (0.32, 0.80, 'in'),
            (0.40, 1.20, 'out'),     # impacto
            (0.50, 1.26, 'out'),     # pausa de impacto (6 fotogramas)
            (1.30, 2.05, 'out'),     # recuperación completa
        ],
        'dip': [(0.00, 0.0), (0.14, -0.03), (0.40, -0.01), (0.55, 0.0), (1.30, 0.0)],
        'settle': (0.55, 1.20),
        'extras': {'impactos_s': [0.40], 'hit_stop_s': [0.40, 0.50], 'cancelable_s': 0.50},
    },
    {
        # v3: salto con el mismo perfil temporal que v2, cadera con 1,25 de altura en el
        # vuelo (la referencia sube algo más de 0,6 veces la altura del personaje).
        'name': 'Salto_Impacto_v3',
        'src': 'Jump',
        'duration': 1.70,
        'stance': True,
        'lift_gain': 1.25,
        'timeline': [
            (0.00, 0.00, 'inout'),
            (0.35, 0.20, 'in'),
            (0.50, 0.40, 'out'),
            (0.95, 0.72, 'lin'),
            (1.05, 0.90, 'in'),
            (1.13, 0.95, 'out'),     # pausa de impacto (5 fotogramas)
            (1.70, 1.00, 'out'),
        ],
        'dip': [(0.00, 0.0), (0.35, -0.06), (0.50, 0.05), (0.95, 0.05),
                (1.05, -0.10), (1.20, -0.03), (1.70, 0.0)],
        'settle': (1.13, 1.70),
        'extras': {'impactos_s': [1.05], 'hit_stop_s': [1.05, 1.13], 'cancelable_s': 1.13},
    },
]


def main(src, out):
    g = Glb(src)
    w = Writer(g)
    sources = stance_sources(g)
    grid, rot, trn = build_stance_clip(g, sources)
    w.add_animation('Postura_Combate', grid, rot, trn,
                    extras={'bucle': True, 'duracion_s': STANCE_PERIOD_S})
    print(f"Postura_Combate: {len(grid)} fotogramas, bucle de {STANCE_PERIOD_S:.2f}s")
    for spec in CLIPS:
        grid, rot, trn = build_clip(g, spec, sources)
        w.add_animation(spec['name'], grid, rot, trn, extras=spec.get('extras'))
        print(f"{spec['name']}: {len(grid)} fotogramas, {spec['duration']:.2f}s")
    w.save(out)
    print('guardado', out)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
