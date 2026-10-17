"""Writes LEDGER9.md from used_aces.json (recorded by build_v9.py) with the evidence of each identifier."""
import json, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo folder (this file lives in tools/)
used = json.load(open(os.path.join(BASE, "used_aces.json"), encoding="utf-8"))
C3 = "CONFIRMADO (plantilla C3 r50600)"
DOC = "DOCUMENTADO (tercero, no export de C3)"
NV = "NO VERIFICADO"
EVIDENCE = {
 "condition|System|on-start-of-layout": ("Plantilla", C3),
 "condition|System|every-tick": ("Plantilla (chef lo usa en pruebas)", DOC),
 "condition|System|compare-eventvar": ("c3source EVENTVAR_REFERENCE_ACES", DOC),
 "condition|System|compare-two-values": ("chef recipe-reference (comparison entero 0..5)", "PARCIAL: id y codigos documentados; nombres first-value/second-value NO VERIFICADOS"),
 "condition|Touch|on-touched-object": ("Plantilla (object, type 'start')", C3),
 "condition|Touch|is-in-touch": ("ninguna", NV),
 "condition|Keyboard|is-key-down": ("liauw (on-key-pressed con key numerico); plugin Keyboard NO VERIFICADO", "PARCIAL: keyCode numerico documentado; plugin y accion NO VERIFICADOS"),
 "condition|Keyboard|on-key-pressed": ("liauw (on-key-pressed con key numerico, p.ej. 32, 38)", "PARCIAL: keyCode numerico documentado; plugin NO VERIFICADO"),
 "condition|System|trigger-once-while-true": ("Plantilla", C3),
 "action|System|go-to-layout": ("Plantilla (layout)", C3),
 "action|System|set-eventvar-value": ("Plantilla (variable, value)", C3),
 "action|System|set-layer-visible": ("Plantilla (layer, visibility 'visible'/'invisible')", C3),
 "action|System|wait": ("Plantilla (seconds, use-timescale booleano)", C3),
 "action|System|create-object": ("chef (template-name, create-hierarchy); object-to-create, layer, x, y NO VERIFICADOS", "PARCIAL"),
 "action|LocalStorage|set-item": ("Plantilla (key, value)", C3),
 "action|LocalStorage|get-item": ("Plantilla (key)", C3),
 "condition|LocalStorage|on-item-get": ("Plantilla (key) + LocalStorage.ItemValue", C3),
 "action|Audio|stop-all": ("Plantilla", C3),
 "action|Taxi|set-size": ("Plantilla (UI_Sprites set-size: width, height)", C3),
 "action|Taxi|set-position": ("fixture liauw (x, y); no export de C3", DOC),
 "action|Taxi|set-angle": ("ninguna (manual 'Set angle' sin id)", NV),
 "action|Taxi|set-animation": ("chef (animation entre comillas, validacion)", DOC),
 "action|Taxi|set-visible": ("liauw EXAMPLES: {\"visible\": true}; port: visibility 'visible'/'invisible' (chef gotcha 26 es de set-layer-visible)", "CONFLICTO: dos fuentes distintas, sin export de C3 que lo resuelva"),
 "action|Txt|set-text": ("ninguna (manual 'Set text' sin id)", NV),
 "action|Txt|set-position": ("fixture liauw (x, y)", DOC),
 "action|Txt|set-size": ("Plantilla (width, height)", C3),
 "action|Txt|destroy": ("liauw (destroy)", DOC),
 "action|Enemy|destroy": ("liauw (destroy)", DOC),
 "action|Shot|destroy": ("liauw (destroy)", DOC),
 "action|Warn|destroy": ("liauw (destroy)", DOC),
 "action|Pickup|destroy": ("liauw (destroy)", DOC),
 "action|Boss|destroy": ("liauw (destroy)", DOC),
 "action|Fx|destroy": ("liauw (destroy)", DOC),
 "action|Enemy|set-instvar-value": ("liauw (variable, value)", DOC),
 "action|Boss|set-instvar-value": ("liauw (variable, value)", DOC),
 "action|Shot|set-instvar-value": ("liauw (variable, value)", DOC),
 "action|Pickup|set-instvar-value": ("liauw (variable, value)", DOC),
 "action|Warn|set-instvar-value": ("liauw (variable, value)", DOC),
 "action|Fx|set-instvar-value": ("liauw (variable, value)", DOC),
 "action|Taxi|set-instvar-value": ("liauw (variable, value)", DOC),
 "condition|Enemy|compare-instance-variable": ("liauw (variable, comparison, value); liauw usa simbolos en comparison", "PARCIAL: comparison entero asumido"),
 "condition|Boss|pick-lowest-instvar": ("manual 'Pick highest/lowest' (sin id)", NV),
 "condition|Enemy|pick-lowest-instvar": ("manual 'Pick highest/lowest' (sin id)", NV),
 "condition|Shot|pick-lowest-instvar": ("manual 'Pick highest/lowest' (sin id)", NV),
 "condition|Pickup|pick-highest-instvar": ("manual 'Pick highest/lowest' (sin id)", NV),
}
def status(key):
    if key in EVIDENCE:
        return EVIDENCE[key]
    kind, obj, aid = key.split("|")
    if aid == "compare-instance-variable":
        return ("liauw (variable, comparison, value); liauw usa simbolos en comparison", "PARCIAL: comparison entero asumido")
    if aid == "set-animation":
        return ("chef (animation entre comillas)", DOC)
    return ("(sin fuente)", NV)
rows = []
nv = 0
for key in sorted(used, key=lambda k: (k.split("|")[0], k.split("|")[1], k.split("|")[2])):
    src, st = status(key)
    if "NO VERIFICADO" in st or "parcial" in st:
        nv += 1
    kind, obj, aid = key.split("|")
    params = ", ".join(sorted(used[key])) or "-"
    rows.append(f"| {kind} | {obj} | {aid} | {params} | {src} | {st} |")
out = ["# Trazabilidad de identificadores — CatTaxi v9 (port a Construct 3)", "",
       "Generado por `gen/build_v9.py` (registro USED). Estado: **confirmado** = aparece en plantilla, c3source, chef o liauw; "
       "**parcial** = el id tiene fuente pero algún parámetro no; **NO VERIFICADO** = no hay fuente en el paquete.", "",
       "| Tipo | Objeto | Identificador | Parámetros usados | Fuente | Estado |", "|---|---|---|---|---|---|"]
out += rows
out += ["", f"Total de identificadores distintos: {len(used)}. Con algo sin verificar (no verificado o parcial): {nv}.", "",
        "## Expresiones", "",
        "Funciones usadas: `min`, `max`, `abs`, `floor`, `ceil`, `round`, `clamp`, `pow`, `sin`, `atan2`, `sqrt`, `random`, `exp`. "
        "Concatenación con `&`. Variables `ddt` y `clock` son globales propias. Nada de ternarios ni comparaciones dentro de expresiones.", "",
        "## Esquemas no verificados (no son identificadores)", "",
        "- Propiedades de instancia Text (liauw DEFAULT_INSTANCE_PROPERTIES.Text).",
        "- Variables de instancia en objectType (`initialValue`, `desc`, `show`, `sid`): liauw solo muestra `name`, `type`, `desc`, `show`, `sid`.",
        "- Instancias de capa de la plantilla (TemplateSprite) copiadas tal cual; capa 'Template' como primera capa.",
        "- Hojas de eventos: formato del evento `variable` y `comment` copiado de la plantilla.",
        "- Plugin `Keyboard` (usedAddons y objectType con plugin-id 'Keyboard'): NO VERIFICADO.",
        "- Sonido: no implementado en esta versión (ver informe).", ""]
open(os.path.join(BASE, "LEDGER9.md"), "w", encoding="utf-8").write("\n".join(out))
print("rows", len(rows), "unverified-or-partial", nv)
