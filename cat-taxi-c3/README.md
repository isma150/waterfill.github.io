# Cat Taxi v9 → Construct 3 (port en curso)

Port del juego HTML `CatTaxi_v9_Jugable` a Construct 3 (r50600, plantilla portrait), solo con hojas de eventos y sin JavaScript.
Objetivo actual: el mismo comportamiento que el HTML, incluidos sus bugs. Los cambios se harán después.

**Estado: NO probado en Construct 3.** En este entorno no hay editor ni runtime. Lo comprobado es:
- estructura del proyecto (`c3source` validateForEditor y detectReferenceIntegrity: 0 problemas);
- identificadores usados dentro de expresiones contra variables declaradas (`tools/check_idents.py`: 0 no declarados).

Los identificadores de acciones y condiciones están en `LEDGER9.md`. Solo algunos están confirmados con un export real de
Construct (la plantilla). El resto viene de documentación de terceros o no tiene fuente, y puede fallar al abrir el proyecto.

## Contenido
- `CatTaxi_v9_port.c3p` — proyecto generado (zip; nombres con `\` como la plantilla).
- `gen/` — generador en Python. `python3 gen/build_v9.py` reconstruye el `.c3p` desde cero.
- `render/` — pipeline de sprites: renderiza el HTML con Chromium y recupera el canal alfa. `render/run_all.sh`.
- `sprites/` — PNG y `manifest.json` generados.
- `template/` — plantilla de Construct 3 r50600 de la que se parte (extraída del `.c3p`).
- `source/cat_taxi_v9.html` — copia del HTML del usuario (referencia de comportamiento).
- `tools/` — validación: `verify9.mjs` (c3source), `check_idents.py`, `ledger9.py` (genera `LEDGER9.md`), `extract_check.py`.
- `LEDGER9.md` — trazabilidad de cada identificador: fuente y estado.
- `PLAN.md`, `PROGRESS.md` — diseño y estado de trabajo.

## Reconstruir y validar
```sh
python3 gen/build_v9.py                       # genera CatTaxi_v9_port.c3p y used_aces.json
python3 tools/ledger9.py                      # genera LEDGER9.md
python3 tools/extract_check.py CatTaxi_v9_port.c3p /tmp/check9
(cd tools && npm ci && node verify9.mjs /tmp/check9)
python3 tools/check_idents.py /tmp/check9
```
Requiere Python 3 con Pillow.
Para regenerar sprites hace falta Chromium (`PLAYWRIGHT_BROWSERS_PATH`) y `playwright-core`: `sh render/run_all.sh`.

## Diferencias conocidas frente al HTML
Lista completa y en orden en `PROGRESS.md`. Resumen:
- Sin audio (ni efectos ni música).
- Sin HP de enemigos, números de daño, partículas, destellos de disparo ni trazadores.
- Iris del túnel sustituido por fundido a negro. Sin opacidad en flashes, invulnerabilidad ni textos.
- Sin separadores de miles ni `toFixed(2)`.
- Botones disparan al pulsar (el HTML dispara al soltar, y cancela si arrastras más de 9 px).
- Sin navegación con Tab/Enter, y sin pausa automática al perder el foco.
- Dt por fotograma con tope 0.042 s (el HTML avanza a paso fijo 1/60).
- Sacudida de pantalla con scroll de la vista (no traslada el HUD).
