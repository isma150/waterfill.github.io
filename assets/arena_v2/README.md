# Arena de pelea · versión 2 (rehecha con geometría limpia)

Segunda versión del escenario. En lugar de decimar la malla generada por IA del FBX, reconstruí el escenario con geometría limpia y de bordes definidos, siguiendo las proporciones medidas del FBX y la referencia: cúpula escalonada tipo pagoda, muro con arcos enmarcados, pilastras, bonsáis y linternas sobre el muro, plaza oscura con bordes de neón verde.

**Aviso:** esta versión es más limpia que la v1, pero **no alcanza el acabado de la referencia**. Es un escenario estilizado hecho con primitivas. Para llegar a un acabado pulido hace falta trabajo de texturizado y sombreado, o un modelado final en Blender o ZBrush.

## Archivos

| Archivo | Contenido |
|---|---|
| `arena_combined.glb` | Escena completa con 6 materiales. Probar primero en Construct 3 |
| `struct.glb` | Estructura: cúpula, muros, pilares, planos (material oscuro) |
| `trim.glb` | Molduras, arcos enmarcados, escalinatas, cornisas (piedra clara) |
| `neon.glb` | Neón verde emisivo: puerta, pilares, anillos de la cúpula, suelo |
| `gold.glb` | Ventanas doradas emisivas de la cúpula |
| `foliage.glb` | Copas de los bonsáis |
| `floor.glb` | Suelo de baldosas con resplandor. Textura 1024 |
| `preview_vista_hero.png`, `preview_vista_lejana.png` | Capturas del escenario |

Las piezas comparten origen: si las usas por separado en Construct 3, colócalas con la misma posición, rotación y escala.

## Especificaciones

- Triángulos: 11 858 en total. Estructura, molduras, neón, ventanas, follaje y suelo por separado.
- Única textura: el suelo, de 1024 × 1024 en JPEG. El resto son colores sólidos y materiales emisivos, sin textura.
- glTF 2.0 básico, sin extensiones.
- Origen en el centro del suelo, con la superficie del suelo en y ≈ 0. El templo queda en el lado −X.

## Limitaciones

- Sin texturas de piedra, sin sombreado de oclusión ambiental ni normal maps. Los materiales son de color plano, así que el resultado depende mucho de la iluminación de Construct 3.
- Bonsáis simplificados como esferas, y linternas como conos y esferas.
- El fondo con el skyline de la referencia no está incluido.
- Compatibilidad con Construct 3 no verificada (ver la nota de la v1).
