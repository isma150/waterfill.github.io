# Arena de pelea (versión optimizada para móvil)

Versión limpia y ligera del entorno del FBX original (`Entorno.fbx`), rehecha a partir de su geometría y textura, siguiendo la referencia: templo con cúpula, plaza oscura y bordes de neón verde.

## Archivos

| Archivo | Contenido | Uso sugerido |
|---|---|---|
| `arena_combined.glb` | Escena completa: templo + suelo + neón (3 materiales) | Probar primero en Construct 3 |
| `temple.glb` | Templo, muros, escalinatas, árboles y faroles. Textura de color 1024 | Si C3 no admite varios materiales |
| `floor.glb` | Suelo nuevo de baldosas (36 × 100 unidades). Atlas 1024 | Idem |
| `neon.glb` | Tiras de neón emisivas, sin textura | Idem |
| `preview_con_luz.png` | Captura desde el lado lejano, con iluminación | Revisión visual |
| `preview_sin_luz.png` | Misma cámara, material plano sin luces | Simula un render sin iluminación |

**Importante:** los cuatro GLB comparten el mismo origen. Si usas las partes por separado en Construct 3, colócalas con la misma posición, rotación y escala.

## Especificaciones

- Triángulos: templo 19 999 · suelo 450 · neón 36 · **total ≈ 20,5 k** (el FBX original tenía 99 543).
- Vértices del templo: 16 974.
- Texturas: una de 1024 × 1024 para el templo (color, JPEG embebido) y otra de 1024 × 1024 para el suelo (atlas 2 × 2 de 512 px). Ninguna supera 1080 px.
- Tamaños: `arena_combined.glb` ≈ 0,95 MB · `temple.glb` ≈ 0,88 MB · `floor.glb` ≈ 0,07 MB · `neon.glb` ≈ 2 KB.
- glTF 2.0 básico, sin extensiones.
- Origen en el centro del suelo, con la superficie del suelo en y ≈ 0. El templo queda en el lado −X.
- Escala: la del FBX original, sin normalizar. Ajústala en el objeto 3D de Construct 3 si hace falta.

## Qué se hizo

1. Se eliminaron la cara inferior de la losa y la rampa descendente de la plaza original. La plaza del FBX bajaba unas 20 unidades, así que se reconstruyó como suelo plano.
2. Se aplanaron las superficies casi planas (desviación < 0,12) y se quitaron islas de menos de 25 caras.
3. Decimación de 67 k a 20 k caras, con normales cortadas a 35° para que muros y bordes sigan nítidos.
4. UV nuevas (xatlas) y color horneado desde la textura original de 2048 px a 1024 px.
5. Suelo nuevo: rejilla de 9 × 25 baldosas con bordes biselados y resplandor verde en las filas de los bordes. Tiras de neón emisivas en los dos laterales (z = ±50) y en la línea del muro, que cruza todo el ancho.

## Limitaciones (importante)

- **No es AAA hecho a mano.** Es una versión limpia y optimizada del modelo original. El detalle fino de Tripo se pierde al decimar, y no hay normal map, ORM ni AO horneado para ahorrar memoria.
- El fondo con el skyline de la referencia no está modelado. En Construct 3 conviene resolverlo con una capa 2D o parallax.
- **Compatibilidad con Construct 3 no verificada.** No pude leer la documentación oficial desde el entorno de trabajo (el acceso a construct.net fue bloqueado). No sé si el objeto 3D Model de C3 aplica iluminación, qué canales de material usa ni si admite varios materiales por GLB. Antes de usarlo en el juego, compruébalo con `arena_combined.glb`; si no funciona, usa las partes por separado.
