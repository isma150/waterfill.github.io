# Trazabilidad de identificadores — CatTaxi v9 (port a Construct 3)

Generado por `gen/build_v9.py` (registro USED). Estado: **confirmado** = aparece en plantilla, c3source, chef o liauw; **parcial** = el id tiene fuente pero algún parámetro no; **NO VERIFICADO** = no hay fuente en el paquete.

| Tipo | Objeto | Identificador | Parámetros usados | Fuente | Estado |
|---|---|---|---|---|---|
| action | Bg | set-animation | animation | chef (animation entre comillas) | DOCUMENTADO (tercero, no export de C3) |
| action | Boss | destroy | - | liauw (destroy) | DOCUMENTADO (tercero, no export de C3) |
| action | Boss | set-animation | animation | chef (animation entre comillas) | DOCUMENTADO (tercero, no export de C3) |
| action | Boss | set-instvar-value | value, variable | liauw (variable, value) | DOCUMENTADO (tercero, no export de C3) |
| action | Boss | set-position | x, y | (sin fuente) | NO VERIFICADO |
| action | Boss | set-size | height, width | (sin fuente) | NO VERIFICADO |
| action | Btn | set-animation | animation | chef (animation entre comillas) | DOCUMENTADO (tercero, no export de C3) |
| action | Btn | set-position | x, y | (sin fuente) | NO VERIFICADO |
| action | Btn | set-size | height, width | (sin fuente) | NO VERIFICADO |
| action | Btn | set-visible | visibility | (sin fuente) | NO VERIFICADO |
| action | Card | set-position | x, y | (sin fuente) | NO VERIFICADO |
| action | Card | set-visible | visibility | (sin fuente) | NO VERIFICADO |
| action | Enemy | destroy | - | liauw (destroy) | DOCUMENTADO (tercero, no export de C3) |
| action | Enemy | set-animation | animation | chef (animation entre comillas) | DOCUMENTADO (tercero, no export de C3) |
| action | Enemy | set-instvar-value | value, variable | liauw (variable, value) | DOCUMENTADO (tercero, no export de C3) |
| action | Enemy | set-position | x, y | (sin fuente) | NO VERIFICADO |
| action | Enemy | set-size | height, width | (sin fuente) | NO VERIFICADO |
| action | Fx | set-animation | animation | chef (animation entre comillas) | DOCUMENTADO (tercero, no export de C3) |
| action | Fx | set-instvar-value | value, variable | liauw (variable, value) | DOCUMENTADO (tercero, no export de C3) |
| action | Icon | set-animation | animation | chef (animation entre comillas) | DOCUMENTADO (tercero, no export de C3) |
| action | Icon | set-position | x, y | (sin fuente) | NO VERIFICADO |
| action | Icon | set-visible | visibility | (sin fuente) | NO VERIFICADO |
| action | LocalStorage | get-item | key | Plantilla (key) | CONFIRMADO (plantilla C3 r50600) |
| action | LocalStorage | set-item | key, value | Plantilla (key, value) | CONFIRMADO (plantilla C3 r50600) |
| action | Needle | set-angle | angle | (sin fuente) | NO VERIFICADO |
| action | Node | set-animation | animation | chef (animation entre comillas) | DOCUMENTADO (tercero, no export de C3) |
| action | Pickup | destroy | - | liauw (destroy) | DOCUMENTADO (tercero, no export de C3) |
| action | Pickup | set-animation | animation | chef (animation entre comillas) | DOCUMENTADO (tercero, no export de C3) |
| action | Pickup | set-instvar-value | value, variable | liauw (variable, value) | DOCUMENTADO (tercero, no export de C3) |
| action | Pickup | set-position | x, y | (sin fuente) | NO VERIFICADO |
| action | Pickup | set-size | height, width | (sin fuente) | NO VERIFICADO |
| action | Shape | set-animation | animation | chef (animation entre comillas) | DOCUMENTADO (tercero, no export de C3) |
| action | Shape | set-position | x, y | (sin fuente) | NO VERIFICADO |
| action | Shape | set-size | height, width | (sin fuente) | NO VERIFICADO |
| action | Shape | set-visible | visibility | (sin fuente) | NO VERIFICADO |
| action | Shot | destroy | - | liauw (destroy) | DOCUMENTADO (tercero, no export de C3) |
| action | Shot | set-angle | angle | (sin fuente) | NO VERIFICADO |
| action | Shot | set-animation | animation | chef (animation entre comillas) | DOCUMENTADO (tercero, no export de C3) |
| action | Shot | set-instvar-value | value, variable | liauw (variable, value) | DOCUMENTADO (tercero, no export de C3) |
| action | Shot | set-position | x, y | (sin fuente) | NO VERIFICADO |
| action | Shot | set-size | height, width | (sin fuente) | NO VERIFICADO |
| action | Speed | set-angle | angle | (sin fuente) | NO VERIFICADO |
| action | Speed | set-position | x, y | (sin fuente) | NO VERIFICADO |
| action | Speed | set-size | height, width | (sin fuente) | NO VERIFICADO |
| action | System | create-object | create-hierarchy, layer, object-to-create, template-name, x, y | chef (template-name, create-hierarchy); object-to-create, layer, x, y NO VERIFICADOS | PARCIAL |
| action | System | go-to-layout | layout | Plantilla (layout) | CONFIRMADO (plantilla C3 r50600) |
| action | System | scroll-to-position | x, y | Plantilla (x, y) | CONFIRMADO (plantilla C3 r50600) |
| action | System | set-eventvar-value | value, variable | Plantilla (variable, value) | CONFIRMADO (plantilla C3 r50600) |
| action | System | set-layer-visible | layer, visibility | Plantilla (layer, visibility 'visible'/'invisible') | CONFIRMADO (plantilla C3 r50600) |
| action | Taxi | set-angle | angle | ninguna (manual 'Set angle' sin id) | NO VERIFICADO |
| action | Taxi | set-animation | animation | chef (animation entre comillas, validacion) | DOCUMENTADO (tercero, no export de C3) |
| action | Taxi | set-position | x, y | fixture liauw (x, y); no export de C3 | DOCUMENTADO (tercero, no export de C3) |
| action | Taxi | set-size | height, width | Plantilla (UI_Sprites set-size: width, height) | CONFIRMADO (plantilla C3 r50600) |
| action | Taxi | set-visible | visibility | liauw EXAMPLES: {"visible": true}; port: visibility 'visible'/'invisible' (chef gotcha 26 es de set-layer-visible) | CONFLICTO: dos fuentes distintas, sin export de C3 que lo resuelva |
| action | Txt | set-position | x, y | fixture liauw (x, y) | DOCUMENTADO (tercero, no export de C3) |
| action | Txt | set-size | height, width | Plantilla (width, height) | CONFIRMADO (plantilla C3 r50600) |
| action | Txt | set-text | text | ninguna (manual 'Set text' sin id) | NO VERIFICADO |
| action | Txt | set-visible | visibility | (sin fuente) | NO VERIFICADO |
| action | Warn | destroy | - | liauw (destroy) | DOCUMENTADO (tercero, no export de C3) |
| action | Warn | set-animation | animation | chef (animation entre comillas) | DOCUMENTADO (tercero, no export de C3) |
| action | Warn | set-instvar-value | value, variable | liauw (variable, value) | DOCUMENTADO (tercero, no export de C3) |
| action | Warn | set-position | x, y | (sin fuente) | NO VERIFICADO |
| action | Warn | set-size | height, width | (sin fuente) | NO VERIFICADO |
| action | Wheel | set-angle | angle | (sin fuente) | NO VERIFICADO |
| condition | Boss | compare-instance-variable | comparison, value, variable | liauw (variable, comparison, value); liauw usa simbolos en comparison | PARCIAL: comparison entero asumido |
| condition | Btn | compare-instance-variable | comparison, value, variable | liauw (variable, comparison, value); liauw usa simbolos en comparison | PARCIAL: comparison entero asumido |
| condition | Card | compare-instance-variable | comparison, value, variable | liauw (variable, comparison, value); liauw usa simbolos en comparison | PARCIAL: comparison entero asumido |
| condition | Enemy | compare-instance-variable | comparison, value, variable | liauw (variable, comparison, value); liauw usa simbolos en comparison | PARCIAL: comparison entero asumido |
| condition | Enemy | pick-lowest-instvar | variable | manual 'Pick highest/lowest' (sin id) | NO VERIFICADO |
| condition | Icon | compare-instance-variable | comparison, value, variable | liauw (variable, comparison, value); liauw usa simbolos en comparison | PARCIAL: comparison entero asumido |
| condition | Keyboard | is-key-down | key | liauw (on-key-pressed con key numerico); plugin Keyboard NO VERIFICADO | PARCIAL: keyCode numerico documentado; plugin y accion NO VERIFICADOS |
| condition | Keyboard | on-key-pressed | key | liauw (on-key-pressed con key numerico, p.ej. 32, 38) | PARCIAL: keyCode numerico documentado; plugin NO VERIFICADO |
| condition | LocalStorage | on-item-get | key | Plantilla (key) + LocalStorage.ItemValue | CONFIRMADO (plantilla C3 r50600) |
| condition | Node | compare-instance-variable | comparison, value, variable | liauw (variable, comparison, value); liauw usa simbolos en comparison | PARCIAL: comparison entero asumido |
| condition | Pickup | compare-instance-variable | comparison, value, variable | liauw (variable, comparison, value); liauw usa simbolos en comparison | PARCIAL: comparison entero asumido |
| condition | Pickup | pick-highest-instvar | variable | manual 'Pick highest/lowest' (sin id) | NO VERIFICADO |
| condition | Shape | compare-instance-variable | comparison, value, variable | liauw (variable, comparison, value); liauw usa simbolos en comparison | PARCIAL: comparison entero asumido |
| condition | Shot | compare-instance-variable | comparison, value, variable | liauw (variable, comparison, value); liauw usa simbolos en comparison | PARCIAL: comparison entero asumido |
| condition | Shot | pick-lowest-instvar | variable | manual 'Pick highest/lowest' (sin id) | NO VERIFICADO |
| condition | System | compare-eventvar | comparison, value, variable | c3source EVENTVAR_REFERENCE_ACES | DOCUMENTADO (tercero, no export de C3) |
| condition | System | compare-two-values | comparison, first-value, second-value | chef recipe-reference (comparison entero 0..5) | PARCIAL: id y codigos documentados; nombres first-value/second-value NO VERIFICADOS |
| condition | System | every-tick | - | Plantilla (chef lo usa en pruebas) | DOCUMENTADO (tercero, no export de C3) |
| condition | System | on-start-of-layout | - | Plantilla | CONFIRMADO (plantilla C3 r50600) |
| condition | Taxi | compare-instance-variable | comparison, value, variable | liauw (variable, comparison, value); liauw usa simbolos en comparison | PARCIAL: comparison entero asumido |
| condition | Touch | is-in-touch | - | ninguna | NO VERIFICADO |
| condition | Touch | on-touched-object | object, type | Plantilla (object, type 'start') | CONFIRMADO (plantilla C3 r50600) |
| condition | Txt | compare-instance-variable | comparison, value, variable | liauw (variable, comparison, value); liauw usa simbolos en comparison | PARCIAL: comparison entero asumido |
| condition | Wheel | compare-instance-variable | comparison, value, variable | liauw (variable, comparison, value); liauw usa simbolos en comparison | PARCIAL: comparison entero asumido |

Total de identificadores distintos: 88. Con algo sin verificar (no verificado o parcial): 36.

## Expresiones

Funciones usadas: `min`, `max`, `abs`, `floor`, `ceil`, `round`, `clamp`, `pow`, `sin`, `atan2`, `sqrt`, `random`, `exp`. Concatenación con `&`. Variables `ddt` y `clock` son globales propias. Nada de ternarios ni comparaciones dentro de expresiones.

## Esquemas no verificados (no son identificadores)

- Propiedades de instancia Text (liauw DEFAULT_INSTANCE_PROPERTIES.Text).
- Variables de instancia en objectType (`initialValue`, `desc`, `show`, `sid`): liauw solo muestra `name`, `type`, `desc`, `show`, `sid`.
- Instancias de capa de la plantilla (TemplateSprite) copiadas tal cual; capa 'Template' como primera capa.
- Hojas de eventos: formato del evento `variable` y `comment` copiado de la plantilla.
- Plugin `Keyboard` (usedAddons y objectType con plugin-id 'Keyboard'): NO VERIFICADO.
- Teclas: el parametro key de Keyboard usa codigos numericos (keyCode: 13, 27, 37, 39, 65, 68, 77, 80); documentado por ejemplos de liauw, NO por un export de C3.
- Sonido: no implementado en esta versión (ver informe).
