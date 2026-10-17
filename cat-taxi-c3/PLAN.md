# Plan: Cat Taxi v9 (HTML) -> Construct 3 (r50600, portrait template, event sheets only)

Objetivo (pedido del usuario): mismo comportamiento que el HTML v9, incluidos sus bugs actuales.
Cambios posteriores se harán por separado. Sin JavaScript.

## Arte
- Harness Chromium (playwright-core, /opt/pw-browsers/chromium) carga una copia del HTML con
  `window.__api` exponiendo las funciones de dibujo. Se renderiza cada sprite sobre fondo negro y blanco
  y se recupera alfa por diferencia (a = 1 - (Cw - Cb)/255).
- Fondos estáticos por tema (drawBackdrop con drive=false). Nubes, líneas de velocidad y
  iris del túnel: objetos propios (iris sustituido por fundido, documentado como diferencia).
- Botones y tarjetas: sprite estirado por color (esquinas ligeramente distorsionadas, documentado).
- Textos: objetos Text (fuente Arial, documentado).

## Audio
- WAV generados con numpy replicando beep() y musicTick() del HTML. Música en bucle de 8 s.

## Pantallas (layouts)
Home, Map, Garage, Shop, Roulette, Settings, Game (incluye tutorial guiado, túnel, pausa y derrota
como capas), Results. Toast en cada layout. Popup en Roulette y Settings.
Variable global `screen` (0 home,1 map,2 garage,3 shop,4 roulette,5 game,6 pause,7 defeat,8 results,9 settings)
para compuertas de lógica.

## Estado
- Globales en la hoja Event Home (como la plantilla con Sound_ONOFF).
- Guardado: LocalStorage con una clave por campo (prefijo cat_taxi_v6_). Carga en on-start con on-item-get.

## Lógica por instancia
- Patrón: objeto + compare-instance-variable (siempre verdadero, p.ej. alive=1) + acciones con expresiones.
- Búsquedas (objetivo más cercano, peligro, premio, cerrojo): agregados globales con
  set-eventvar-value(min/ternario) dentro de un bucle por instancia.
- Sin colisiones de motor: las recogidas y explosiones son por posición/progreso, como en el HTML.

## Tiempo
- dt por fotograma con tope 0.042 (min(dt,0.042)). El HTML usa paso fijo 1/60: diferencia menor, documentada.

## Verificación
- c3source validateForEditor + detectReferenceIntegrity + pruebas negativas.
- chef: revisión de índices/archivos sueltos.
- Ledger con cada identificador y su estado (confirmado / sin verificar).
- Sin ejecutar en Construct 3: no hay editor ni runtime.
