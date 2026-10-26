# Animaciones del golem: análisis, referencia y clips v3

Este documento cubre el GLB `Golem_Piedra_Todas_Animaciones.glb` (modelo "Golem Shadow Clash"), la
comparación con el combo de Hulk en MARVEL Tokon y los clips generados.

Este repo es público: no contiene fotogramas ni vídeo del juego. Las comparaciones con el vídeo se han
hecho fuera del repo; aquí solo hay capturas del golem y cifras.

Archivos de esta carpeta:

| Archivo | Qué es |
|---|---|
| `Golem_Piedra_Animaciones_v3.glb` | GLB original + 7 clips nuevos (30 clips en total). Malla, esqueleto y los 23 originales sin cambios. |
| `generar_animaciones.py` | Generador de los clips nuevos. Solo necesita numpy. |
| `glb_lib.py` | Lectura, muestreo y escritura de clips en GLB. |
| `visor.html` | Reproductor de clips con three.js para revisar cada clip y su instante de impacto. |
| `capturas/` | Capturas solo del golem: postura de combate y los clips v3 alineados en el impacto. |

---

## 1. Diagnóstico del GLB original (medido)

- **Modelo:** 1 malla de 10.638 triángulos, 2 materiales, 33 huesos Mixamo. La raíz `Golem_Rig`
  tiene una rotación de 90° en X, así que el eje Y local de la cadera apunta al eje Z del mundo. El golem
  mide unas 1,0 unidades de alto y está centrado en el origen.
- **23 clips, 84 canales cada uno.**

| Hallazgo | Dato medido | Por qué importa |
|---|---|---|
| Interpolación | **Los 23 clips usan `LINEAR` en todos sus canales** | Sin easing: los golpes arrancan y frenan a velocidad constante. |
| Huesos que se mueven en los golpes | `Golpe01`–`Golpe10` y `Recibe*`: **12–14 huesos** | El cuerpo casi no participa. |
| Duplicados | `Punch` ≈ `Ascendente`: **81/84 canales idénticos**. `Punch2` ≈ `Gancho`: **81/84**. `Walking` ≈ `Retroceso`: 57/84 | Tres pares con distinto nombre y casi el mismo movimiento. |
| Postura entre golpes | Todos los clips terminan en `Idle` (erguido) | El golem nunca adopta la postura ancha de combate del vídeo. |

---

## 2. Lo que mide el vídeo de referencia

Método:
- **Impactos:** el contador de golpes ("13 Hits") está fijo abajo a la izquierda. Se recorta esa zona a
  60 fps y se marca cada cambio del número. Cada cambio es un golpe conectado, con precisión de ±1–2
  fotogramas porque el contador anima al cambiar.
- **Recortes alineados en el impacto:** 60 fps, de 30 fotogramas antes a 20 después.
- **Limitación:** el golpe alto (≈12,98 s) cae dentro de una escena de "super" en primer plano, con brillo
  dorado y cámara cercana. No se usa para medir temporización.

Cifras medidas:
- **Puñetazo recto (impacto en 10,12 s):** la preparación visible dura unos 8–10 fotogramas (≈0,15 s).
  Desde −30 fotogramas hay una superposición amarilla de energía que tapa el inicio, así que esta cifra
  es el mínimo visible. Pausa de impacto de unos 4–5 fotogramas (≈0,08 s), a ojo. Vuelve a la postura
  ancha hacia +10–12 fotogramas.
- **Salto con caída (impacto en 8,98 s):** Hulk ya está en el aire al empezar la ventana (−19 fotogramas),
  así que la subida no se mide. Polvo en el suelo desde el aterrizaje. Pausa de 3–6 fotogramas, a ojo.
  Postura ancha hacia +6–12 fotogramas.
- **Altura del salto:** estimada a ojo a partir de los píxeles de los pies y del cuerpo en dos fotogramas
  completos. Resultado: entre 0,6 y 0,9 veces la altura del personaje, con error de ±0,15.
- **Ritmo del combo:** el contador sube de 11 a 33 golpes en unos 17 s. Entre golpes de la ráfaga hay
  0,25–0,5 s, y los golpes pesados están cada ~1 s. Esas cifras son el tiempo entre cancelaciones, no la
  duración de cada animación: en un combo cada movimiento se encadena antes de terminar su recuperación.

---

## 3. Tabla de temporización: Hulk, v2 y v3

| Medida | Hulk (vídeo) | v2 | v3 |
|---|---|---|---|
| Recto: preparación hasta el impacto | ≈0,15 s visibles (8–10 f) | 0,58 s (35 f) | 0,32 s (19 f), con 6 f de entrada desde la postura |
| Recto: pausa de impacto | ≈0,08 s (4–5 f) | 0,12 s (7 f) | 0,08 s (5 f) |
| Recto: vuelta a la postura | ≈0,2 s (hasta +10–12 f) | 0,67 s hasta Idle | ≈0,7 s hasta la postura (recuperación completa) |
| Salto: impacto de aterrizaje | 8,98 s en el vídeo | 1,05 s | 1,05 s |
| Salto: pausa de aterrizaje | 3–6 f (a ojo) | 0,10 s | 0,08 s |
| Salto: altura de cadera en el aire | 0,6–0,9 × altura (a ojo, ±0,15) | +0,486 | **+0,595** |
| Salto: cadera al aterrizar | — | −0,165 | −0,165 |

Notas:
- `Golpe_Pesado` no tiene una referencia limpia en el vídeo (el golpe alto va en una escena de "super").
  Su v3 se ajusta igual que el recto: impacto a 0,40 s y pausa de 0,10 s.
- Las cifras de v3 son las del generador. Se han medido en los propios clips, no en el juego.

---

## 4. Clips generados

Los clips nuevos se construyen a partir de un clip mocap del propio GLB, con el mismo proceso:

1. **Remapeo temporal** con curvas de easing por tramo.
2. **Retraso por cadena:** antebrazo 2 fotogramas, cabeza 3, mano 4, columna 1.
3. **Exageración del giro respecto al reposo** y **tope de ángulo** en cadera (40°), columna (35°),
   cabeza (25°) y hombros (30°).
4. **Peso:** la cadera baja al cargar y comprime al aterrizar. El desplazamiento se aplica en el eje
   vertical del mundo, convertido al espacio local. No hay desplazamiento horizontal en ningún clip nuevo.
5. **Postura de combate** (`Postura_Combate`, bucle de 2 s):
   - brazos: pose de guardia de `Punch2` en t=0;
   - piernas y cadera: mezcla al 50 % hacia la postura agachada de `Jump` en t=0, con tope de 40° en cadera;
   - cadera 0,03 más baja;
   - respiración: columna ±2°.
   La primera y la última pose son iguales (diferencia medida: 0).
6. **Entrada y salida desde la postura:** los clips v3 empiezan exactamente en `Postura_Combate` (primeros
   6 fotogramas con mezcla suave) y acaban en ella. Diferencia medida en los fotogramas de inicio y fin: 0.
7. **Instantes en `extras`:** `impactos_s`, `hit_stop_s` y, en los v3, `cancelable_s`, el instante desde el
   que el motor puede encadenar otro movimiento. Se lee desde `gltf.parser.json.animations[i].extras`
   (three.js no expone los `extras` en el clip).

Los clips `_v2` se conservan para comparar en el visor. Los clips `_v3`:

| Clip | Base | Duración | Impacto | Pausa | Cancelable desde |
|---|---|---|---|---|---|
| `Golpe_Recto_v3` | `Golpe02_Cruzado` | 1,20 s | 0,32 s | 0,32–0,40 s | 0,40 s |
| `Golpe_Pesado_v3` | `Punch2` | 1,30 s | 0,40 s | 0,40–0,50 s | 0,50 s |
| `Salto_Impacto_v3` | `Jump` | 1,70 s | 1,05 s | 1,05–1,13 s | 1,13 s |

---

## 5. Lo que todavía no alcanza el nivel de Hulk

- **Postura:** en el vídeo la postura es más ancha y más baja. La de `Postura_Combate` solo baja y dobla
  un poco las rodillas. Es la diferencia más visible en las capturas.
- **Golpe recto:** el tiempo de preparación, el impacto y la pausa ya se parecen al vídeo. El brazo
  avanza, pero el golpe se lee más como gancho o zancada que como puñetazo recto de frente.
- **Golpe pesado:** el brazo sigue el arco del mocap de `Punch2` (sube por encima de la cabeza y se abre
  hacia el lateral). Se lee como golpe de martillo o lateral.
- **Salto:** la altura sube a 0,595, dentro del rango estimado del vídeo. No se puede validar la subida
  completa, porque en la ventana medida Hulk ya está en el aire. Faltaría una ventana más amplia.
- **Efectos:** destellos, polvo, temblor de cámara, pausa de impacto real en el juego y el empuje del
  rival están fuera del GLB. La superposición de energía del vídeo tapa la preparación de Hulk.
- **Verificación:** las capturas se han hecho con three.js r160 en Chromium sin GPU (SwiftShader). No se
  ha probado en el motor del juego.

---

## 6. Verificación

- Cabecera del GLB coherente con el tamaño del archivo.
- Los 23 clips originales en orden y con el buffer original como prefijo exacto.
- Malla, esqueleto y nodos idénticos al original.
- Los clips `_v2` son idénticos byte a byte a la versión anterior del commit `40b7bc3`.
- `Postura_Combate`: primer y último fotograma idénticos (diferencia 0 en todos los canales).
- Clips `_v3`: primer y último fotograma iguales a la postura (diferencia 0 en todos los canales).
- Visor: carga, muestra el impacto y la cancelación, y vuelve a reproducir al llegar al final del clip.

---

## 7. Cómo regenerar

```bash
python3 generar_animaciones.py <entrada.glb> <salida.glb>
```

Los parámetros de cada clip están en `CLIPS` (tiempos, mapa temporal, peso, asentamiento, impactos,
cancelación y ganancias por hueso con `gain_override`). La postura está en `stance_pose`, y las
ganancias, retrasos y topes por tipo de hueso, en `GROUP_RULES`.

---

## 8. Próximo paso

- Una ventana de vídeo más amplia para el salto (desde antes de despegar), para medir la subida completa.
- Un golpe recto de frente en el vídeo, sin superposición, para cerrar la forma del brazo.
- Una postura de combate más ancha, con las piernas abiertas, a partir del salto o de la postura medida.
