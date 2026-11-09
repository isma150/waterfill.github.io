# Arena de pelea (versión optimizada para móvil)

Versión limpia y ligera del entorno del FBX original (`Entorno.fbx`), rehecha a partir de su geometría y textura, con la referencia de escenario de templo, plaza oscura y bordes de neón.

## Archivos

| Archivo | Contenido | Uso sugerido |
|---|---|---|
| `arena_combined.glb` | Escena completa: templo + suelo + neón (3 materiales) | Probar primero en Construct 3 |
| `temple.glb` | Templo, muros, escalinatas, árboles y faroles. Textura de color 1024 | Si C3 no admite varios materiales |
| `floor.glb` | Suelo nuevo de baldosas (36 × 36 unidades). Atlas 1024 | Idem |
| `neon.glb` | Tiras de neón emisivas, sin textura | Idem |
| `preview_con_luz.png` | Captura de referencia con iluminación | Revisión visual |
| `preview_sin_luz.png` | Captura sin iluminación (material plano) | Simula un render sin luces |

## Especificaciones

- Triángulos: templo 19 999 · suelo 162 · neón 36 · **total ≈ 20.2 k** (el FBX original tenía 99 543).
- Vértices del templo: 16 974.
- Texturas: una de 1024 × 1024 para el templo (color, JPEG embebido) y otra de 1024 × 1024 para el suelo (atlas 2 × 2 de 512 px). Ninguna supera 1080 px.
- Tamaños: `arena_combined.glb` ≈ 0,95 MB · `temple.glb` ≈ 0,88 MB · `floor.glb` ≈ 0,07 MB · `neon.glb` ≈ 2 KB.
- Origen en el centro del suelo, con la superficie del suelo en y = 0. El templo queda en el lado −X.
- Escala: la del FBX original, sin normalizar. Ajústala en el objeto 3D de Construct 3 si hace falta.

## Qué se hizo

1. Se eliminaron la cara inferior de la losa y la rampa descendente de la plaza original. La plaza en el FBX bajaba unas 20 unidades, así que se reconstruyó como suelo plano.
2. Se aplanaron las superficies casi planas (desviación < 0,12) y se quitaron islas de menos de 25 caras.
3. Decimación de 67 k a 20 k caras, con las normales cortadas a 35° para que muros y bordes sigan siendo nítidos.
4. UV nuevas (xatlas) y color horneado desde la textura original de 2048 px a 1024 px.
5. Suelo nuevo: rejilla de 9 × 9 baldosas con bordes biselados y resplandor verde en las filas de los bordes. Tiras de neón emisivas en los dos laterales y en la línea del muro.

## Limitaciones (importante)

- **No es AAA hecho a mano.** Es una versión limpia y optimizada del modelo original. El detalle fino de Tripo se pierde al decimar, y no hay normal map, ORM ni AO horneado para ahorrar memoria.
- El fondo con el skyline de la referencia no está modelado. En Construct 3 conviene resolverlo con una capa 2D o parallax.
- **Compatibilidad con Construct 3 no verificada.** No pude consultar la documentación oficial desde el entorno de trabajo. Antes de usarlo en el juego, comprueba si el objeto 3D Model admite iluminación y varios materiales. Si no, usa `temple.glb`, `floor.glb` y `neon.glb` por separado.
