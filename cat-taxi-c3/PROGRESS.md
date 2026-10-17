# PROGRESO — port de Cat Taxi v9 (HTML) a Construct 3 (r50600, plantilla portrait)

## Hecho
- render/: harness Chromium (usa el propio código del HTML) -> render/raw -> sprites/*.png + sprites/manifest.json (44 sprites)
  - render/build_harness.py, render/specs.py, render/capture.mjs, render/postprocess.py
  - gen/art_extra.py: botones, tarjetas, barras, velos, líneas (PIL, colores del HTML) -> 112 entradas en manifest
- gen/ev.py: helpers de eventos y registro USED (ids usados) para el ledger
- gen/cfg.py: bancos, armas, coches, premios, variables persistentes (57) y de ejecución (86)

## Decisiones de diseño
- Lógica en unidades HTML (420x746). Transformación a layout: X = 60 + x*6/7, Y = y*6/7, tamaños*6/7.
- Layout 480x640 (plantilla); fondos rellenados a 480 px (60 px a cada lado con el borde).
- Pantallas = layouts: Home(0) Map(1) Garage(2) Shop(3) Roulette(4) Game(5) Results(8) Settings(9).
  Pausa (6) y derrota (7) = capas dentro de Game. Popup = capa en Roulette y Settings.
- Variable `screen` con los mismos números que el HTML.
- Hoja de eventos común inyectada en cada layout (no hay includes): reloj, toast, guardado.
- Globales en "Event Home" (como Sound_ONOFF de la plantilla).
- Guardado: LocalStorage, una clave por campo (cat_taxi_v6_<campo>), escritura coalescida por needSave.
- Objetivos/mínimos/conteos: "Pick highest/lowest" sobre instancias filtradas (id NO verificado).
- Por instancia: objeto sin condición de objeto => acciones sobre todas las instancias (manual).
- Sistema: las acciones System no corren por instancia (manual) => agregados solo con pick lowest/highest.

## Diferencias conocidas (a documentar)
- Iris del túnel -> fundido a negro (no hay círculo).
- Fuente Arial en lugar de Comic Sans; emojis (🔒) pueden no verse.
- Dt por fotograma con tope 0.042 (HTML: paso fijo 1/60).
- Sin Tab/Enter de foco de teclado (accesibilidad).
- Partículas simplificadas (mismas formas básicas, sin la animación exacta).
- Toque: los botones disparan al pulsar (HTML: al soltar, cancelan si arrastras >9 px).
- Nubes del fondo estáticas (no se desplazan).

## Pendiente (en orden)
1. gen/objects.py: tipos de objeto (Sprite con animaciones, Text, plugins de plantilla) + índice.
2. gen/layouts.py: instancias de cada layout con coordenadas transformadas.
3. gen/sheet_common.py + sheet_home.py (globales, carga/guardado, inicio, mapa).
4. gen/sheet_game.py: núcleo (oleadas, enemigos, disparo, dinamita, pickups, túnel, jefe, victoria, derrota, pausa, tutorial guiado).
5. gen/sheet_menus.py: garaje, tienda, ruleta, ajustes, resultados.
6. gen/audio.py: WAV con numpy (beep y música) — al final.
7. gen/build.py: ensamblar .c3p; validar con c3source; pruebas negativas; ledger.

## ESTADO (actualizado)
- sprites/: 130 entradas en manifest (render/run_all.sh regenera TODO: harness -> capturas -> alfa -> PIL).
  Fondos opacos ampliados a 560 unidades HTML (padding con borde) para cubrir 480 px de layout.
- gen/objects.py: OBJECTS (Bg, Taxi[taxi,blue,mint,home], Enemy, Boss, Shot, Warn, Pickup, Fx, EnemyBar,
  Speed, Btn[colores], Card[colores], Shape[SHAPE_KEYS], Icon, Wheel, Logo, Cloud, Node, Roulette) + Txt/TxtHit + Keyboard.
  Todas las variables de instancia de id: 'id'. Txt tiene 'id'.
- gen/lay.py: Lay (capas, img/txt/btn/card/rect), coordenadas HTML -> layout (lx/ly, *6/7).
- gen/layouts_menu.py: build_home/map/results/garage/shop/roulette/settings (popups por capas PopCoin/PopGem/PopGun/PopWarn/PopNice/PopConfirm).
- gen/sheet_common.py: common(lname) = reloj (ddt, clock), toast (por id de Txt y Card), guardado (set-item), tecla M.
- gen/cfg.py: PERSIST (57), RUNTIME (incl. startReq/startGuide/startBank/awardNeeded/toastReq/...).
- gen/ids.py: nid(name) registro estable de ids.

## Convenciones de eventos (importante para la siguiente tanda)
- Botón: B([TOUCH('Btn','start'), IV('Btn','id',0,nid('btn.<pantalla>.<nombre>')), CMPV('popupOpen',0,0)], acciones)
- Texto dinámico: B([IV('Txt','id',0,nid('<nombre>'))], [A('set-text','Txt', text=expr)]).
  Cada texto distinto necesita su propio evento (la condición de id es por instancia).
- Cambio de grupo visual: LAYER_VIS(capa, 1/0) (una acción por capa).
- Arranque de misión: startReq=1, startGuide=g, startBank=b; Game on-start hace la inicialización.
- Toast desde cualquier evento: TOAST(lname, msg, dur) devuelve (condiciones extra, acciones).
- Sin ternarios ni comparaciones dentro de expresiones: se usan eventos por caso (ids no verificados en expresiones).

## Pendiente inmediato
1. gen/sheet_menus.py: Home (globales, carga LocalStorage, PLAY/HOW/Enter), Map (nodos, textos por banco, START), Results,
   Garage (pestañas, celdas, detalle arma/coche/tripulación, comprar/equipar), Shop (pestañas, 3 tarjetas), Roulette (giro,
   premios, popup), Settings (sonido, movimiento, tutorial, reset con popup de confirmación).
2. gen/sheet_game.py + layout Game (capas: Background, Road/Speed, Enemigos, Taxi, HUD, Flash, Iris (fundido), Guía, Pausa, Derrota, Toast).
3. gen/build.py: unir todo en el .c3p (plantilla + índices + usedAddons: Text, Keyboard?, Audio, LocalStorage).
4. Validar (verify.mjs + negtest2.mjs + ledger), luego audio (numpy).

## ESTADO 2 (menús listos en código; juego pendiente)
- gen/sheet_menus.py: home (load/click/Enter), map (nodos, textos banco, START), results, garage (pestañas, celdas,
  candados/checks, detalle arma). Pendiente en garage: textos y posiciones de botón de coche/tripulación (garage_labels parcial).
- gen/sheet_menus2.py: garage_actions (equip/comprar/mejorar arma, coches, tripulación VISIT SHOP).
- gen/sheet_menus3.py: popup (capas), roulette (etiqueta, giro, premio con bandera awardNeeded), salida.
  Pendiente: shop, settings.
- Diseño juego (sheet_game): usar el mapeo de máxima simplicidad:
  * groundY sin condicionales: 319 + 441*pow(min(max(d,0),1.15),1.22) + 100*min(d,0)
  * perspectiveScale sin condicionales: 0.92*(1 + 0.6*max(c,0) + 1.5*min(c,0)), c=clamp(d,-0.5,1.15)
  * roadHalfWidth(d) = 148 + 90*pow(clamp(d,0,1),1.06); laneAt = 210 + (lane-210)*roadHalfWidth/148
  * instancias por tipo: Enemy/Boss (d<0), Shot/Pickup (d>=0 casi siempre, pero shot puede ser <0 al inicio)
  * dodge: instancia 'roll' = random(0,1) al vencer dodgeCd; comparar roll < dodge
- Estado de pausa/derrota: screen 5 juego, 6 pausa (capa), 7 derrota (capa). Globals en Event Home.

## ESTADO 3 (juego, parte 1 lista: gen/sheet_game1.py)
- Plantilla de referencia confirmada: LocalStorage key entre comillas ('"clave"'), on-item-get + LocalStorage.ItemValue.
- Reglas para el resto del juego (gen/sheet_game2.py, pendiente):
  * Agregados: reset de flags por tick -> filtros -> PICK_LOWEST/PICK_HIGHEST (sub-evento) -> flags.
  * Contar instancias: expresión Enemy.Count (no System action).
  * Crear y luego fijar variables: primero SIV sobre el objeto existente (p.ej. fire), luego CREATE, luego SIV del nuevo.
  * Sin ternarios ni '=' dentro de expresiones: comparaciones como eventos (CMPV/IV).
  * Peligro (dynamite): Shot.dist = abs(xl-mPX) por tick; filtro dist<94, d>0.05; PICK_LOWEST(d).
  * Objetivo de disparo: Enemy.isTarget; boss primero; bomba: inAoe = abs(sx - tSX) < 75.
  * Explosión: exploded=1 + CREATE blast + DESTROY Shot; Warn se destruye por owner=Shot.id en el mismo evento.
- Pendiente tras parte 2: HUD/overlays (parte 3), layout Game, TxtHit (números de daño: diferido), guía (parte 3).

## ESTADO 4 (proyecto compila; validaciones pasan; quedan partes)
- Construcción: `python3 gen/build_v9.py` -> CatTaxi_v9_port.c3p (214 entradas, 8 layouts, 8 hojas).
- Validación: extraer a check9 (script inline en la sesión), `validator/verify9.mjs ../v9c3/check9` -> 0 issues,
  0 reference issues; `v9c3/check_idents.py check9` -> sólo nombres de enumeración (teclas, layouts, 'start').
- Correcciones aplicadas por chef-gotchas: layer visibility 'visible'/'invisible', animación entre comillas, capas entre comillas.
- Variables de evento: se declaran automáticamente en Event Home (lista impresa al construir). Nombres con '.' se excluyen.
- Conteo de instancias: compare-two-values con first-value/second-value (NOMBRES DE PARÁMETRO NO VERIFICADOS).
- Keyboard: plugin id 'Keyboard' NO VERIFICADO; claves como enumeración (NO VERIFICADO).

## PENDIENTE (en este orden)
1. gen/sheet_game5.py: guía (tutorial 4 fases, guideNewEnemy, pickups de entrenamiento, túnel de entrenamiento).
2. gen/sheet_game6.py: visuales: Taxi (pos LX/LY, angle, size), Enemy/Boss/Shot/Warn/Pickup (pos+size por animación),
   Speed (22 líneas), HUD (textos, barras, dial+aguja, AUTO, monedas), capa de tunel, boost, pausa/derrota textos,
   guía (textos por fase), cambio de fondo por tema, toasts del juego (TOAST), botones AUTO/pausa/continuar/rendirse.
3. gen/sheet_menus4.py: Shop (pestañas, 3 tarjetas por pestaña, comprar/equipar) y Settings (sonido, movimiento, tutorial,
   reset con popup de confirmación).
4. Garage: textos/posiciones de coche y tripulación (garage_labels parcial).
5. Audio (numpy): WAV de beep y música; Audio plugin 'play' NO VERIFICADO.
6. Ledger final (LEDGER9.md) a partir de USED y de los nombres no verificados; pruebas negativas; informe.
