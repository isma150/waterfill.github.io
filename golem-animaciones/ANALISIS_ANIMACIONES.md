# Animaciones del golem: análisis y nuevos clips

Este documento cubre el GLB `Golem_Piedra_Todas_Animaciones.glb` (modelo "Golem Shadow Clash"), la
comparación con las capturas de Hulk en Marvel Tokon y los clips nuevos generados.

Archivos de esta carpeta:

| Archivo | Qué es |
|---|---|
| `Golem_Piedra_Animaciones_v2.glb` | El GLB original con 3 clips nuevos añadidos. Mismos 23 clips, malla, esqueleto y texturas. |
| `generar_animaciones.py` | Generador de los clips nuevos. Solo necesita numpy. |
| `glb_lib.py` | Lectura, muestreo y escritura de clips en GLB. |
| `visor.html` | Reproductor de clips con three.js para comparar con el vídeo. |
| `capturas/` | Hojas de contacto de los clips y de la referencia mocap. |

---

## 1. Diagnóstico del GLB original (medido)

- **Modelo:** 1 malla de 10.638 triángulos, 2 materiales, 33 huesos Mixamo. La raíz `Golem_Rig`
  tiene una rotación de 90° en X. El golem mide unas 1,0 unidades de alto y está centrado en el origen.
- **23 clips, 84 canales cada uno** (28 huesos × translación, rotación y escala).

| Hallazgo | Dato medido | Por qué importa |
|---|---|---|
| Interpolación | **Los 23 clips usan `LINEAR` en todos sus canales** | Sin easing: los golpes arrancan y frenan a velocidad constante. Es la causa principal de que se vea mecánico. |
| Huesos que se mueven en los golpes | `Golpe01`–`Golpe10` y `Recibe*`: **12–14 huesos** | El cuerpo casi no participa. Las piernas apenas se mueven (`LeftLeg`/`RightLeg` ≈ 20–25°). |
| Huesos que se mueven en mocap | `Idle`, `Jump`, `Punch`, `Punch2`, `Run`, `Walking`: 25–28 huesos | Son los clips con más cuerpo. |
| Densidad de keyframes | Golpes: 20–42 por canal (≈30 fps). `Punch2`: 81. `Idle`: 201 | Suficiente para la forma, pero sin tiempos de aceleración. |
| Duplicados | `Punch` ≈ `Ascendente`: **81/84 canales idénticos**. `Punch2` ≈ `Gancho`: **81/84**. `Walking` ≈ `Retroceso`: 57/84 | Tres pares de clips con distinto nombre y casi el mismo movimiento. |
| Anticipación y pausa de impacto | No existen en ningún clip | Sin preparación ni pausa, el golpe no tiene peso. |
| Desplazamiento de raíz | Ningún clip mueve la cadera en horizontal de forma intencionada | El salto y el avance dependen del código del juego. |

Conclusión: el problema no es el formato ni el modelo, sino la **temporización** (sin easing, sin
anticipación, sin retraso entre cadenas) y el **peso corporal** (pocos huesos participan).

---

## 2. Qué se ve en las capturas de Hulk

Lo que aporta calidad en las capturas que compartiste:

1. **Preparación marcada:** el brazo se carga hacia atrás antes del golpe, con el torso girado.
2. **Golpe seco con sobrepaso y pausa:** el impacto es un instante de parada, con destello y líneas de velocidad.
3. **Peso:** en el salto con caída hay compresión al aterrizar y polvo en el suelo.
4. **Efectos y cámara:** destellos, polvo, temblor de cámara y el rival que sale despedido. Esto no está en el GLB.

Del punto 4 se deduce algo importante: buena parte de la sensación de calidad no se puede conseguir solo
con el GLB. Hay que añadirla en el motor del juego.

---

## 3. Clips nuevos

Los tres se generan a partir de un clip mocap del propio GLB, con el mismo proceso:

1. **Remapeo temporal** con curvas de easing por tramo (preparación `inout`, golpe `in`, recuperación `out`).
2. **Retraso por cadena:** antebrazo 2 fotogramas, cabeza 3, mano 4, columna 1. Así el movimiento
   se propaga desde el torso hacia fuera.
3. **Exageración del giro respecto al reposo** (ganancia por grupo) y **tope de ángulo** en cadera (40°),
   columna (35°), cabeza (25°) y hombros (30°). El tope evita las rotaciones imposibles del mocap.
4. **Peso corporal:** la cadera baja al cargar y comprime al aterrizar. El desplazamiento se aplica en el
   eje vertical del mundo (ver nota técnica abajo).
5. **Asentamiento:** tras el impacto, la pose vuelve a la postura `Idle` (no al reposo de la malla).

| Clip | Base | Duración | Impacto | Pausa de impacto (hit-stop) | Notas |
|---|---|---|---|---|---|
| `Golpe_Pesado_v2` | `Punch2` | 1,30 s | 0,58 s | 0,58–0,70 s | Brazo en arco (ver §4) |
| `Golpe_Recto_v2` | `Golpe02_Cruzado` | 1,25 s | 0,58 s | 0,58–0,70 s | Piernas con ganancia 1,5 |
| `Salto_Impacto_v2` | `Jump` | 1,70 s | 1,05 s | 1,05–1,15 s | Cadera +0,49 en el salto y −0,17 al aterrizar, respecto a Idle |

Los instantes de impacto y de pausa están en `extras` de cada animación (`impactos_s`, `hit_stop_s`).
three.js no expone esos `extras` en el clip: se leen de `gltf.parser.json.animations[i].extras`, como
hace `visor.html`. Los clips están en 60 fps, con interpolación `LINEAR` sobre claves densas (no se usa
`CUBICSPLINE`, para que se reproduzcan igual en cualquier motor).

**Nota técnica (corregida en esta versión):** `Golem_Rig` gira 90° en X, así que el eje Y local de la
cadera apunta al eje Z del mundo. La primera versión aplicaba la caída en ese eje y la movía hacia
delante y hacia atrás. Ahora el vector "arriba" del mundo se convierte al espacio local del hueso, y el
desplazamiento horizontal de la cadera es cero en todos los clips nuevos.

---

## 4. Lo que todavía no alcanza el nivel de Hulk

Esto es lo que veo en las hojas de `capturas/`, sin suavizar:

- **`Golpe_Pesado_v2`:** la preparación y la recuperación se leen bien. El golpe no: el brazo sigue el arco
  del mocap de `Punch2` (sube por encima de la cabeza y luego se abre hacia el lateral), así que parece un
  golpe de martillo o lateral, no el puñetazo recto de Hulk.
- **`Golpe_Recto_v2`:** mejor lectura que el anterior. El brazo sale de la guardia, hay zancada y vuelve a
  Idle. Aun así, el impacto se lee más como gancho o desplazamiento lateral que como un puñetazo recto
  hacia la cámara. Falta extensión del brazo hacia delante.
- **`Salto_Impacto_v2`:** se ve el agachado, el despegue, la suspensión y la caída, con una compresión
  clara en el aterrizaje (cadera −0,17 respecto a Idle). La altura del salto (+0,49, casi la mitad de
  la altura del golem) puede ser demasiado grande para lo que buscas. No hay desplazamiento de raíz: el
  golem sube y baja en el sitio.
- **Efectos, polvo, temblor de cámara y empuje del rival:** fuera del GLB, en el motor.
- **Verificación:** la comprobación visual se ha hecho con three.js r160 en Chromium sin GPU
  (SwiftShader). No se ha probado en el motor del juego.

---

## 5. Cómo regenerar

```bash
python3 generar_animaciones.py <entrada.glb> <salida.glb>
```

Los parámetros de cada clip están en `CLIPS` (tiempos, mapa temporal, peso, asentamiento, impactos y
ganancias por hueso con `gain_override`). Las ganancias, retrasos y topes por tipo de hueso están en
`GROUP_RULES`.

Verificaciones hechas sobre el GLB generado:
- la cabecera coincide con el tamaño del archivo;
- el buffer original es prefijo exacto del nuevo (los 23 clips originales no cambian);
- malla, esqueleto y nodos son idénticos al original;
- una copia de prueba de `Punch2` renderiza igual al original (diferencia máxima de 1/255 en 6 píxeles de 230.400);
- la posición en mundo de la cadera: desplazamiento horizontal 0 en todos los clips nuevos; la altura
  cambia como se describe en la tabla de §3;
- el visor llega al final del clip y vuelve a reproducirse (no se congela).

---

## 6. Lo que necesito para seguir

El vídeo original de Marvel Tokon. Con él voy a comparar, fotograma a fotograma:

- cuántos fotogramas dura la preparación y dónde está el impacto;
- cuánto se aleja el brazo y qué parte del cuerpo se mueve con él;
- cuánto tarda la recuperación en volver a la postura base;
- cuánto sube el salto y cuánto se hunde al aterrizar.

Con esos datos ajusto `CLIPS` y el golpe recto. Si me dices qué motor usa el juego (three.js u otro),
también puedo añadir los efectos de impacto como datos de animación.
