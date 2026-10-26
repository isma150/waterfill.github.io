"""Lectura, muestreo y escritura de clips en un GLB (glTF 2.0 binario).

Solo depende de numpy. El GLB original se conserva byte a byte: los clips nuevos
se añaden al final del buffer, con sus propios bufferViews y accessors.
"""
import json
import struct

import numpy as np

COMPONENT_FLOAT = 5126
TYPE_SIZES = {'SCALAR': 1, 'VEC3': 3, 'VEC4': 4}


class Glb:
    def __init__(self, path):
        with open(path, 'rb') as f:
            magic, version, _ = struct.unpack('<4sII', f.read(12))
            assert magic == b'glTF' and version == 2, 'no es un GLB 2.0'
            json_len, _ = struct.unpack('<I4s', f.read(8))
            self.gltf = json.loads(f.read(json_len).decode('utf-8'))
            bin_len, _ = struct.unpack('<I4s', f.read(8))
            self.bin = bytearray(f.read(bin_len))
        self.bin = self.bin[:self.gltf['buffers'][0]['byteLength']]
        self.names = [n.get('name') for n in self.gltf['nodes']]
        self.index = {n: i for i, n in enumerate(self.names)}
        self.parent = {}
        for i, n in enumerate(self.gltf['nodes']):
            for c in n.get('children', []):
                self.parent[c] = i
        self.joints = self.gltf['skins'][0]['joints']

    # ---------- lectura ----------
    def accessor(self, idx):
        a = self.gltf['accessors'][idx]
        bv = self.gltf['bufferViews'][a['bufferView']]
        off = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
        nc = TYPE_SIZES[a['type']]
        dt = {5126: np.float32, 5123: np.uint16, 5125: np.uint32, 5121: np.uint8}[a['componentType']]
        arr = np.frombuffer(bytes(self.bin), dtype=dt, count=a['count'] * nc, offset=off)
        return arr.reshape(a['count'], nc) if nc > 1 else arr.copy()

    def rest_trs(self, node):
        n = self.gltf['nodes'][node]
        t = np.array(n.get('translation', [0, 0, 0]), dtype=np.float64)
        r = np.array(n.get('rotation', [0, 0, 0, 1]), dtype=np.float64)
        s = np.array(n.get('scale', [1, 1, 1]), dtype=np.float64)
        return t, r, s

    def clip_names(self):
        return [a['name'] for a in self.gltf['animations']]

    def sample_clip(self, name):
        """Devuelve {node: {'t': (times, values), 'r': (times, values), 's': ...}} del clip."""
        anim = next(a for a in self.gltf['animations'] if a['name'] == name)
        out = {}
        for c in anim['channels']:
            s = anim['samplers'][c['sampler']]
            node = c['target']['node']
            path = c['target']['path']
            times = self.accessor(s['input']).ravel().astype(np.float64)
            vals = self.accessor(s['output']).astype(np.float64)
            out.setdefault(node, {})[path[0]] = (times, vals)
        return out, float(max(v[0][-1] for d in out.values() for v in d.values()))


# ---------- cuaterniones (xyzw, como glTF) ----------
def qnorm(q):
    return q / np.linalg.norm(q, axis=-1, keepdims=True)


def qmul(a, b):
    ax, ay, az, aw = np.moveaxis(a, -1, 0)
    bx, by, bz, bw = np.moveaxis(b, -1, 0)
    return np.stack([
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
        aw * bw - ax * bx - ay * by - az * bz,
    ], axis=-1)


def qconj(q):
    return q * np.array([-1, -1, -1, 1.0])


def qslerp(a, b, t):
    """Slerp con corrección de hemisferio (evita giros de 360 grados)."""
    a = qnorm(a)
    b = qnorm(b)
    dot = np.sum(a * b, axis=-1, keepdims=True)
    b = np.where(dot < 0, -b, b)
    dot = np.abs(dot).clip(-1, 1)
    theta = np.arccos(dot)
    sin_t = np.sin(theta)
    safe = sin_t > 1e-6
    wa = np.where(safe, np.sin((1 - t) * theta) / np.where(safe, sin_t, 1), 1 - t)
    wb = np.where(safe, np.sin(t * theta) / np.where(safe, sin_t, 1), t)
    return qnorm(wa * a + wb * b)


def qpow(q, k):
    """Escala el ángulo de una rotación por k (k=1.3 exagera un 30 %)."""
    q = qnorm(q)
    if q[3] < 0:
        q = -q
    w = np.clip(q[3], -1, 1)
    angle = 2 * np.arccos(w)
    s = np.sqrt(max(1 - w * w, 0.0))
    axis = q[:3] / s if s > 1e-8 else np.array([1.0, 0, 0])
    na = angle * k
    return np.concatenate([axis * np.sin(na / 2), [np.cos(na / 2)]])


def qdelta(rest, q):
    """Rotación relativa al reposo expresada en espacio local del hueso."""
    return qmul(qconj(rest), q)


# ---------- muestreo lineal de un canal ----------
def sample_channel(times, vals, t, rotation=False):
    """Muestrea un canal en un array de tiempos `t` (LINEAR; slerp para rotaciones)."""
    t = np.clip(np.asarray(t, dtype=np.float64), times[0], times[-1])
    i = np.clip(np.searchsorted(times, t, side='right') - 1, 0, len(times) - 2)
    t0, t1 = times[i], times[i + 1]
    dt = t1 - t0
    u = np.where(dt > 0, (t - t0) / np.where(dt > 0, dt, 1.0), 0.0)[:, None]
    if rotation:
        return qslerp(vals[i], vals[i + 1], u)
    return vals[i] * (1 - u) + vals[i + 1] * u


def bake_tracks(glb, samples, grid):
    """Remuestrea cada canal del clip a una malla temporal común (p. ej. 60 fps).

    Los canales de un mismo clip no siempre comparten malla de tiempos, así que se
    muestrean todos en `grid`. Los nodos sin canal usan su pose de reposo.
    Devuelve (rot {node: (N,4)}, trn {node: (N,3)}) como float32.
    """
    rot, trn = {}, {}
    for node in glb.joints:
        rest_t, rest_r, _ = glb.rest_trs(node)
        ch = samples.get(node, {})
        if 'r' in ch:
            rot[node] = sample_channel(ch['r'][0], ch['r'][1], grid, rotation=True).astype(np.float32)
        else:
            rot[node] = np.tile(rest_r, (len(grid), 1)).astype(np.float32)
        if 't' in ch:
            trn[node] = sample_channel(ch['t'][0], ch['t'][1], grid).astype(np.float32)
    return rot, trn


# ---------- escritura ----------
class Writer:
    """Añade accessors, bufferViews y animaciones a un Glb cargado."""

    def __init__(self, glb):
        self.glb = glb
        self.gltf = glb.gltf
        self.bin = bytearray(glb.bin)

    def _align(self):
        while len(self.bin) % 4:
            self.bin.append(0)

    def add_accessor(self, data, typ, minmax=False):
        data = np.ascontiguousarray(data, dtype=np.float32)
        self._align()
        off = len(self.bin)
        self.bin.extend(data.tobytes())
        bv_index = len(self.gltf['bufferViews'])
        self.gltf['bufferViews'].append({'buffer': 0, 'byteOffset': off, 'byteLength': data.nbytes})
        acc = {'bufferView': bv_index, 'componentType': COMPONENT_FLOAT,
               'count': int(data.shape[0]), 'type': typ}
        if minmax:
            flat = data.reshape(data.shape[0], -1)
            acc['min'] = [float(v) for v in flat.min(axis=0)]
            acc['max'] = [float(v) for v in flat.max(axis=0)]
        self.gltf['accessors'].append(acc)
        return len(self.gltf['accessors']) - 1

    def add_animation(self, name, times, rot_by_node, trans_by_node=None, extras=None):
        """rot_by_node: {node: (N,4) quat}; trans_by_node: {node: (N,3)}. Ambos con la misma malla de tiempos."""
        times = np.asarray(times, dtype=np.float32)
        t_acc = self.add_accessor(times.reshape(-1, 1), 'SCALAR', minmax=True)
        samplers, channels = [], []
        for node, q in sorted(rot_by_node.items()):
            out = self.add_accessor(q, 'VEC4')
            samplers.append({'input': t_acc, 'output': out, 'interpolation': 'LINEAR'})
            channels.append({'sampler': len(samplers) - 1, 'target': {'node': node, 'path': 'rotation'}})
        for node, tr in sorted((trans_by_node or {}).items()):
            out = self.add_accessor(tr, 'VEC3')
            samplers.append({'input': t_acc, 'output': out, 'interpolation': 'LINEAR'})
            channels.append({'sampler': len(samplers) - 1, 'target': {'node': node, 'path': 'translation'}})
        anim = {'name': name, 'samplers': samplers, 'channels': channels}
        if extras:
            anim['extras'] = extras
        self.gltf['animations'].append(anim)

    def save(self, path):
        self._align()
        self.gltf['buffers'][0]['byteLength'] = len(self.bin)
        js = json.dumps(self.gltf, separators=(',', ':')).encode('utf-8')
        while len(js) % 4:
            js += b' '
        bin_chunk = bytes(self.bin)
        total = 12 + 8 + len(js) + 8 + len(bin_chunk)
        with open(path, 'wb') as f:
            f.write(struct.pack('<4sII', b'glTF', 2, total))
            f.write(struct.pack('<I4s', len(js), b'JSON'))
            f.write(js)
            f.write(struct.pack('<I4s', len(bin_chunk), b'BIN\x00'))
            f.write(bin_chunk)
