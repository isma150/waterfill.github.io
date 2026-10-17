# Progreso del port Cat Taxi v9 → Construct 3

Objetivo del usuario: mismo comportamiento que el HTML v9 (incluidos sus bugs). Cambios después, por separado.
Estado: **no abierto en Construct 3**. Todo lo marcado como "comprobado" son validaciones estructurales.

## Comprobado
- `tools/verify9.mjs` (c3source): manifiesto OK, 0 problemas de referencia, 0 problemas de editor.
- `tools/check_idents.py`: 0 variables de instancia no declaradas. Solo quedan sin declarar los nombres de capas/layouts y
  valores de enumeración ('start', 'end', 'visible', 'invisible', nombres de layout). Prueba negativa: un identificador
  inventado se detecta.
- `tools/check_ids.py`: sids únicos, uids únicos (layouts + singleton), tipos de objeto usados y en usedAddons,
  singleglobal-inst de los plugins sin instancias. Prueba negativa: detecta defectos plantados.
- `tools/ledger9.py` -> `LEDGER9.md`: 88 identificadores de acción/condición; ver estado en el propio ledger.

## Error de apertura reportado (TypeError de projectResources.js al abrir)
Defectos reales encontrados y corregidos (no se ha confirmado que sean la causa del error):
- sids duplicados (9 000+ apariciones, 220 repetidos): condiciones y acciones reutilizadas entre eventos.
  Ahora `ev.B`/`ev.G` copian los elementos con sid nuevo. `tools/check_ids.py` lo comprueba.
- Objetos plugin sin instancia (Keyboard): faltaba `singleglobal-inst`. Ahora lo tiene (como Touch de la plantilla).
- uids de instancias singleton (Audio 10, Touch 11, LocalStorage 13) colisionaban con uids de los layouts.
  Los singleton usan 900001 en adelante.
- Pendiente de confirmar: los ids de "Pick highest/lowest" (`pick-lowest-instvar`, `pick-highest-instvar`) son
  inventados. El manual confirma que la función existe como condición con la opción "Pick all tied", pero no el id
  ni los parámetros. Hace falta un ejemplo exportado desde Construct 3.

## Hecho en la última tanda
- Teclado: `key` con códigos numéricos (77 M, 80 P, 27 Escape, 37/39 flechas, 65 A, 68 D, 13 Enter). Documentado por
  ejemplos de liauw; no hay export de C3 que lo confirme.
- Espera: `use-timescale` booleano (como en la plantilla).
- XP: subida de nivel (`gainXp`): nivel nuevo cuando xp >= 60+20·nivel, toast 'LEVEL n!  +2.5% POWER' (1.2 s).
  El daño ya usaba el nivel (min(0.3,(nivel-1)·0.025)).
- Toasts añadidos: '+n COINS' / 'BANK EMPTY' (monedas), 'WEAPON: X!' (cajón), 'Sound on/off' (tecla M),
  'Not enough coins for a spin' (ruleta), 'Bank is locked' (mapa), guiados: '¡DINAMITA!…', '¡CASI!…', '¡BIEN ESQUIVADO!',
  'ARMA CONSEGUIDA!', 'MONEDA CONSEGUIDA!', 'TUTORIAL SUPERADO · OLEADA 1'.
- Fin del tutorial: spawnTimer 1.0 y pickupTimer 3 (HTML `finishGuidedMission`); antes 0.75 y aleatorio.
- Sacudida de pantalla: `scroll-to-position` alrededor de 240/320 mientras `mShake > 0` y sin movimiento reducido.
  El HTML traslada todo el dibujo (incluido el HUD); aquí el scroll mueve las capas con paralaje.
- Ruta de trabajo: el generador ya no depende de rutas absolutas; todo es relativo a esta carpeta.

## Pendiente, en orden de riesgo
1. **Nunca abierto en Construct 3.** Primer paso para el usuario: abrir `CatTaxi_v9_port.c3p` y pasar los errores.
2. Identificadores sin fuente en un export de C3 (ver LEDGER9.md): `set-visible` (conflicto de parámetro),
   `set-text`, `set-angle`, `set-animation`, `create-object` (object-to-create/layer/x/y), `pick-lowest-instvar` /
   `pick-highest-instvar` (agregados de todo el juego), `is-in-touch`, plugin `Keyboard`, `compare-two-values` (nombres).
3. Audio: no implementado. Hace falta confirmar el esquema de sonidos (C3 espera WebM Opus / M4A) y el `play` de Audio.
   La plantilla solo usa `set-muted` y `stop-all`.
4. HP de enemigos (`EnemyBar`), números de daño (`TxtHit`), partículas (impacto, explosiones, monedas, trazador, destello
   de disparo, humo de dinamita). Los objetos existen; no se controlan.
5. Opacidad (flash, pulso de invulnerabilidad, textos del túnel y del impulso, líneas de velocidad). Sin `set-opacity` confirmado.
6. Iris del túnel: sustituido por fundido a negro.
7. Formato de números: sin separadores de miles (`toLocaleString('en-US')`) y sin `toFixed(2)` en la cuenta atrás.
8. Botones: disparan al pulsar; el HTML dispara al soltar y cancela si arrastras más de 9 px.
9. Teclado: sin Tab/Enter/Espacio de foco; sin pausa automática al perder el foco o al ocultarse la pestaña.
10. Nubes del fondo estáticas; dt por fotograma con tope 0.042 s (HTML: paso fijo 1/60).
11. Recogida de monedas: si dos monedas llegan en el mismo fotograma, solo cuenta la primera (HTML: una a una).
12. Muertes por dinamita, bancos agotados, ruleta y continuar: se conservan los bugs del HTML (ver análisis §17), sin cambios.
13. Código muerto del HTML que no se porta (no tiene efecto): tutorial por páginas, escudos, asistencia, vida, bloque de
    túnel de monedas, `shootAt` de bloque, `BLOCKED!` y `Shield unavailable` (botones bloqueados), `Healing disabled`
    (botón bloqueado), `+ HEALTH` (nunca aparece).
