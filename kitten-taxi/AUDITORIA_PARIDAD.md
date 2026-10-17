# Kitten Taxi: auditoría de paridad con el original

Versión auditada: commit `94f5a67` (y `19b2e1b` / `8d42dcd` para la documentación).
Referencia: los dos vídeos de partida (parte 1, 773 s, con audio; parte 2, 732 s, con audio) y las capturas de las pantallas del original.
Complementa a `ANALISIS_A_FONDO.md`, que queda como resumen. Este documento es la lista de trabajo.

Etiquetas de evidencia: **[Obs]** visto en el vídeo · **[Med]** medido sobre fotogramas o capturas · **[Cód]** verificado en el código · **[Sim]** simulación automática (no es un jugador humano) · **[Dev]** pendiente de dispositivo real · **[?]** sin confirmar.

Severidad: **S0** bloquea la paridad o la experiencia · **S1** se nota de inmediato y rompe la sensación del original · **S2** degrada o falta · **S3** pulido.

---

## 0. Veredicto

**No está lista para afirmar paridad con el original.** El bucle de juego funciona de principio a fin, y en la conducción y en el HUD ya nos acercamos. Pero estos cuatro puntos no se cumplen:

1. **El túnel no es parte del juego.** En el original el taxi entra en un túnel dentro de la escena de conducción: los bordes se oscurecen, al fondo hay una luz, el cronómetro sigue corriendo y hay monedas en el carril que duplican el premio si las recoges todas. Nuestra versión lo hace como una pantalla negra aparte, sin conducción [Obs, Cód]. Es el fallo más visible para alguien que conozca el original.
2. **El jefe no se puede ganar con el piloto automático** [Sim], y es estático: no se balancea ni cambia de carril, mientras que en el original se mueve, se solapa con el taxi y lo rodea.
3. **El lenguaje gráfico es otro.** El original es un boceto a lápiz sobre papel blanco, con trama de sombreado y trazos irregulares. El nuestro es vector limpio con relleno pastel. La mezcla de colores también es distinta: en la escena de referencia la carretera ocupa el 56 % de la pantalla en gris, frente al 28 % del original [Med].
4. **La economía no tiene consecuencias.** El saldo del banco no baja, el nivel no sube, las llaves no sirven, y la ruleta cobra 1 y luego 200 [Cód].

Hay cosas que ya están bien: el taxi sobre el horizonte, la dinamita por encima del coche, las furgonetas de frente, el HUD superior, el contraste del texto y la pausa al ocultar la pestaña [Med, Cód].

---

## 1. Método

- **Vídeo:** fotogramas dispersos y muestras densas (2 y 4 fps) de las dos partes, con recuento de enemigos por oleada hecho por dos agentes independientes. Las ventanas de tiempo y los tallies son firmes (±0.5 s); los enemigos, estimados (±1–2).
- **Imagen:** comparación lado a lado de las mismas pantallas, a la misma altura, y de los mismos estados de juego (misma fase de la ola, mismo tema de banco cuando es posible).
- **Métricas:** proporción de píxeles por color, contraste WCAG de los textos del HUD, tamaño de los objetivos táctiles, y tasa de fotogramas.
- **Código:** lectura de las funciones implicadas y búsqueda de restos de la base.
- **Simulación:** piloto automático con el gancho de pruebas; sirve para equilibrio, no para dificultad real.
- **Límites:** no he escuchado el audio del original; no tengo un dispositivo real (todas las medidas de rendimiento son de Chromium headless); las pantallas de pausa, resultados y ajustes no se han recapturado en esta ronda.

---

## 2. Métricas

| Métrica | Original | Nuestra versión | Lectura |
|---|---|---|---|
| Carretera en gris (escena de conducción, mismo momento) | 28 % | 56 % | **Nuestra carretera es el doble de gris** [Med] |
| Blanco casi puro (escena) | 25 % | 32 % | Más blanco en nuestra escena [Med] |
| Cielo azul (escena azul) | 29 % | — | Comparar en el mismo tema de banco [Med, pendiente] |
| Trama de sombreado y líneas oscuras | Alta (trazos negros radiales) | Baja (trazos grises finos) | **Diferente** (ART-02) [Obs, Med] |
| Contraste "1 Lv" sobre carretera | — | 7.4 : 1 | Pasa (WCAG AA = 4.5 : 1) [Cód] |
| Contraste "WAVE" sobre etiqueta | — | 9.8 : 1 | Pasa [Cód] |
| Contraste barra de vida | — | 8.6 : 1 | Pasa [Cód] |
| Tamaño del botón GARAGE / SPIN / SHOP | — | 42 px de alto | **Por debajo de 44 px** (Apple HIG) [Cód] |
| Tamaño del botón HOW TO PLAY | — | 41 px de alto | **Por debajo de 44 px** [Cód] |
| Tamaño del botón de pausa | — | 39 × 39 px | **Por debajo de 44 px** [Cód] |
| Tamaño del botón PLAY | — | 272 × 60 px | Pasa [Cód] |
| Tasa de fotogramas (headless) | — | 60 fps (16.7 ms) | Pasa en headless; **falta medir en dispositivo** [Dev] |
| Pausa al ocultar la pestaña | — | Sí (`visibilitychange` y `blur`) | Pasa [Cód] |

---

## 3. Hallazgos

Cada hallazgo tiene un ID estable, una gravedad, la evidencia y un criterio de aceptación verificable.

### 3.1 Arte y estilo (ART)

| ID | Sev. | Hallazgo | Evidencia | Criterio de aceptación |
|---|---|---|---|---|
| ART-01 | **S0** | El estilo gráfico no es el del original. El original es un boceto a lápiz sobre papel blanco; el nuestro, vector limpio con relleno pastel y contorno uniforme. | Comparación lado a lado (escena, taxi, furgonetas, HUD) [Obs, Med] | Trazo con variación de grosor, relleno con trama de sombreado y fondo de papel, sin cambiar la geometría. |
| ART-02 | **S1** | Las líneas de velocidad son finas, grises y rectas. El original tiene trazos negros densos y radiales que cubren la carretera en los tramos rápidos. | [Obs: 60 s, 125 s, 121–122 s] [Med] | Trazos radiales negros, afilados, con densidad y opacidad parecidas en la conducción rápida; apagables con movimiento reducido. |
| ART-03 | **S1** | Tipografía: Comic Sans MS / Comic Neue. El original usa una letra a mano. | [Cód] `txt()` usa `'Comic Sans MS','Comic Neue',cursive`; [Obs] letra a mano en cronómetro y tutorial | Una fuente manuscrita libre, incluida en el proyecto, o rasterizada. Sin depender de la fuente del sistema. |
| ART-04 | **S2** | La carretera es gris claro con bordes oscuros. El original es blanco con arcos curvos a lápiz; las marcas de carril son curvas, no rectas. | [Med] 28 % gris frente a 56 % | Carretera mayoritariamente blanca, con arcos de lápiz que converjan al horizonte. Sigue leyéndose como carretera (decisión aprobada). |
| ART-05 | **S2** | Tienda: las tarjetas no tienen letra de rareza (S, A, B), ni imagen de vehículo, ni "Buy @ precio" con icono de moneda o gema. | [Obs: 260 s] [Cód] | Tarjetas con rareza, imagen y precio con icono. |
| ART-06 | **S2** | Mapa: el original tiene calles con retícula, edificios con candado, un parque ("Ranking Stage") y una ruta amarilla gruesa. El nuestro es más abstracto. | [Obs: 80 s] [Cód] | Mapa con edificios con candado, parque, retícula de calles y ruta amarilla. El usuario ha dicho que el mapa del original "mola más"; lo interpreto como que el original es más detallado [?]. |
| ART-07 | **S2** | Explosiones: nubes de humo blancas y grandes que tapan el coche. Las nuestras son destellos pequeños. | [Obs: 121–122 s] [Med] | Humo de sprite con tamaño ≈ ancho del coche, con tres o cuatro fases. |
| ART-08 | **S3** | Monedas: nuestras son ≈50 % más grandes que las del original (≈0.037 frente a ≈0.025 del ancho). | [Med] | Radio reducido hasta ≈0.025 del ancho a la altura del coche. |
| ART-09 | **S3** | Cielo: los bancos de ciudad tienen cielo claro y edificios grises; el original tiene edificios a lápiz sobre fondo blanco. | [Obs] | Edificios a lápiz, con trama. |
| ART-10 | **S3** | El título y el pie de la pantalla de inicio dicen "HTML5 · Depth & thrown items edition" (texto interno). | [Cód] | Pie con la versión pública, o nada. |

### 3.2 Escena y cámara (SCN)

| ID | Sev. | Hallazgo | Evidencia | Criterio de aceptación |
|---|---|---|---|---|
| SCN-01 | **S3** | La base del taxi está ≈34 px (≈0.045 de la altura) por debajo del original. | [Med]: original 0.40, nuestro 0.445 | Base del taxi a 0.40 de la altura, con la perspectiva ajustada. |
| SCN-02 | **S2** | Las marcas de carril son rectas y con guiones; el original tiene arcos de lápiz. | [Obs, Med] | Marcas curvas que sigan la perspectiva. |
| SCN-03 | **S2** | El taxi casi no se desplaza lateralmente en la conducción normal; el original se mueve entre 0.50 y 0.85 del ancho. | [Med] | Rango lateral parecido en la conducción manual. [?] |
| SCN-04 | **S2** | Los enemigos aparecen en el cielo, por encima del horizonte, y bajan hacia el coche. En el original aparecen en el carril, a los lados del taxi, a su altura. | [Obs: 121–134 s] [Cód] | Entrada por el lateral, a la altura del coche. [?] Revisar con la vista del original. |

### 3.3 Enemigos y jefe (ENE, BOS)

| ID | Sev. | Hallazgo | Evidencia | Criterio de aceptación |
|---|---|---|---|---|
| BOS-01 | **S0** | El jefe no se gana con el piloto automático. En la simulación, el taxi llega a 0 de vida en 21 s con 8 golpes, sin conseguir chocar con el jefe. | [Sim] registro del jefe: lane 98, hp 167 → 2 en 21 s | El piloto automático gana el jefe en al menos 9 de cada 10 simulaciones, con la vida por encima de 0. |
| BOS-02 | **S1** | El jefe está fijo en un carril lateral (lane 98 o 322) y no cambia de posición. El original se mueve, se balancea y se solapa con el taxi. | [Obs: 161–182, 349–378, 506–540, 670–697 s] [Cód] | Movimiento lateral con balanceo, cambio de carril cada 3–4 s y solapamiento con el taxi. |
| BOS-03 | **S1** | Cadencia del jefe: dispara cada 1.3–1.8 s, con un 60 % de dinamita de unos 14 de daño. La cadencia del jefe del original no se ha medido. | [Cód] `rnd(1.3,1.8)`, `e.kind==='boss'?.6` [Obs: aviso de bomba en 360, 511 y 600 s] | Cadencia de disparo del jefe ≈ una por cada 3–4 s, con dinamita en un 40 % de los casos. [?] |
| BOS-04 | **S2** | El piloto automático elige como objetivo al enemigo más cercano en lateral, así que casi siempre son las furgonetas. | [Cód] `m.enemies.filter(e=>...).sort(...)` | Prioridad al jefe cuando está en pantalla, o al menos alternancia. |
| BOS-05 | **S2** | Las furgonetas normales siguen llegando durante la pelea. | [Obs] [Cód] (implementado) | Igual. Pasa. |
| ENE-01 | **S2** | El esquive de los enemigos está implementado, pero **ningún agente lo confirma en el vídeo** (partes 1 y 2). | [Obs] [Cód] | Decisión tuya: mantener con probabilidad baja, o quitar. |
| ENE-02 | **S2** | Cadencia de disparo de los enemigos normales: 3 a 4.2 s, sin calibrar. La calibración anterior se basaba en una lectura errónea de la barra de nivel. | [Cód] | Calibrar con conteo de aparición de dinamita en vídeo. |
| ENE-03 | **S3** | Las furgonetas de policía de frente son correctas. La ambulancia usa el mismo modelo con cruz roja, y la furgoneta blindada usa el mismo modelo con color azul, pero lleva la barra de luces de policía. | [Cód] `policeVan` (`amb` y `kind==='van'`) | Modelos propios para la ambulancia y la furgoneta blindada, sin luces de policía en la blindada. |

### 3.4 Túnel y fin de ola (TUN)

Esta sección corrige lo que dije antes. **El túnel no es un tally separado: es una parte de la conducción.**

| ID | Sev. | Hallazgo | Evidencia | Criterio de aceptación |
|---|---|---|---|---|
| TUN-01 | **S0** | El túnel no está en la escena de juego. Nuestro fin de ola es una pantalla negra con un círculo y la cuenta atrás, sin conducción. | [Obs: 88–100 s, muestra densa a 4 fps] [Cód] `drawTally` | Al despejar la ola con tiempo sobrante, el taxi entra en un túnel dentro de la misma escena: el carril y el coche siguen visibles, los bordes se oscurecen, al fondo hay una luz, y el cronómetro cuenta hacia abajo mientras el jugador conduce. |
| TUN-02 | **S0** | En el original hay monedas en el carril del túnel. El texto del tutorial dice «double coins when you get all the coins from the tunnel». Nosotros no tenemos ninguna mecánica de monedas en el túnel. | [Obs: texto en el tutorial, 92–95 s] | Monedas en el carril durante el túnel; si el jugador recoge todas, el premio es el doble. |
| TUN-03 | **S1** | La cuenta atrás del túnel en el original baja de unos 12 a 0 en unos 3 s (cuatro por segundo), y después aparece "N x2 Bonus". | [Obs: 92–100 s] [Med] | Cuenta atrás en la escena, y el bonus aparece al final del túnel. |
| TUN-04 | **S2** | La luz del fondo del túnel en el original es un disco claro, no un arco con cielo azul. Nuestro círculo tiene cielo azul y suelo gris. | [Obs] [Cód] | Disco de luz al fondo, con las paredes negras en perspectiva. |
| TUN-05 | **S2** | El "DARK PASSAGE" de la base oscurece la pantalla en la ola 4 durante 3 s y muestra el texto. No existe en el original. | [Obs: ola 4 de nivel 1, 119–126 s: pantalla clara] [Cód] | Eliminar el oscurecimiento y el texto. |

### 3.5 Ítems, recolección y armas (ITM, CMB)

| ID | Sev. | Hallazgo | Evidencia | Criterio de aceptación |
|---|---|---|---|---|
| ITM-01 | **S2** | Faltan las botellas rojas y el contenedor verde, la gema azul de cambio y la arcilla verde que frena. | [Obs] [Cód] (no existen) | Cada ítem con su efecto. |
| ITM-02 | **S2** | Las llaves no tienen función. La llave dorada debería hacer aparecer el coche dorado en la partida. | [Obs: consejo en el banco] [Cód] | Llave con uso y coche dorado. |
| CMB-01 | **S2** | Un golpe directo del enemigo en el original muestra un destello rojo a pantalla completa (376.8, 533.0 y 601.8 s). Nuestro flash existe pero no se ha comparado. | [Obs] [Cód] `m.flash` | Destello equivalente, apagable con movimiento reducido. [Dev] |
| CMB-02 | **S2** | La dinamita tiene el aviso triangular y el arco. Pendiente: el sonido y la duración del aviso en el original. | [Obs] | Pendiente. [?] |
| CMB-03 | **S3** | Los disparos del taxi son líneas instantáneas. El original no tiene disparos visibles a distancia; el disparo está en contacto. | [Obs] [Cód] | Igual. Pasa. |

### 3.6 Economía y progresión (ECO)

| ID | Sev. | Hallazgo | Evidencia | Criterio de aceptación |
|---|---|---|---|---|
| ECO-01 | **S0** | El saldo del banco no baja al robarlo y no se guarda entre visitas. El original: 150 → 12 en la siguiente visita. | [Cód] `BANKS` constante; `missionVictory` no escribe el saldo. [Obs] | El saldo baja con lo robado y persiste entre partidas. |
| ECO-02 | **S1** | El nivel del banco no sube por visita. El original: 2 → 3 → 4. | [Cód] `level` fijo. [Obs] | El nivel sube en cada visita, con un tope. |
| ECO-03 | **S1** | Las llaves no se ganan ni se gastan. | [Cód] `save.keys` solo se muestra. | Llaves con ganancia y gasto. |
| ECO-04 | **S1** | Ruleta: la primera tirada cuesta 1 y las siguientes 200. El original: 500, 730, 1000. | [Cód] `save.spinCount===0?1:200`. [Obs] | Precios 500, 730, 1000 y el máximo después. |
| ECO-05 | **S2** | Tienda Coin/Key sin contenido ("COMING SOON"). | [Cód] `locked:true`. [Obs] | Contenido mínimo o pestaña oculta. |
| ECO-06 | **S2** | El bonus perfecto da el 15 % sin daño. En el original sale 0 en todas las partidas. | [Cód] `m.perfect`. [Obs] | Criterio igual al original, o desactivado. |
| ECO-07 | **S2** | La barra de nivel del jugador muestra progreso pero no desbloquea nada. Los valores (4 por muerte, 30 por jefe, 1 por moneda, 60 + 20·nivel) son provisionales. | [Cód] `gainXp` | Efecto definido o barra oculta. |
| ECO-08 | **S3** | Se regalan gemas en el banco 0 si tienes menos de 10. | [Cód] `if(m.bankIdx===0&&save.gems<10)`. | Eliminar. |

### 3.7 Pantallas y navegación (NAV)

| ID | Sev. | Hallazgo | Evidencia | Criterio de aceptación |
|---|---|---|---|---|
| NAV-01 | **S1** | Faltan las burbujas de tutorial dentro de la primera ola ("Drive!", "Dodge!", "Auto attack when you go near an enemy", "get a Coin"…), que congelan la escena. | [Obs: 0:12–1:30] [Cód] | Burbujas en la primera ola, con la escena congelada. |
| NAV-02 | **S2** | Faltan los consejos de carga antes de cada banco (calle BANK con texto). | [Obs: 4 consejos] [Cód] | Pantalla de consejo antes de cada banco, con el texto del original. |
| NAV-03 | **S2** | Faltan los avisos de valoración de la app, que el original muestra. | [Obs: 260 s] | No replicar; decisión tuya. |
| NAV-04 | **S2** | Ajustes sin High Scores ni Achievements. | [Obs] [Cód] | Decisión tuya. |
| NAV-05 | **S3** | Título sin GameCenter ni Guest (decisión deliberada). | [Obs] [Cód] | Igual. Pasa como decisión. |
| NAV-06 | **S2** | Mapa: el original permite ver el saldo y el nivel en el popup; el nuestro también, pero sin los candados ni el parque. | [Obs: 80 s] [Cód] | Ver ART-06. |

### 3.8 HUD, accesibilidad y táctil (HUD, A11Y)

| ID | Sev. | Hallazgo | Evidencia | Criterio de aceptación |
|---|---|---|---|---|
| HUD-01 | **S2** | Los botones GARAGE, SPIN, SHOP y HOW TO PLAY miden 41–42 px de alto; la pausa, 39 px. Por debajo de 44 px. | [Cód] `button('GARAGE',…,42)`, `iconBtn('Ⅱ',…,39)` | Objetivos táctiles de al menos 44 × 44 px. |
| HUD-02 | **S2** | Textos en el HUD con contraste suficiente. | [Med] 7.4–9.8 : 1 | Pasa. |
| A11Y-01 | **S2** | Movimiento reducido: el temblor de cámara y el destello respetan la opción; las líneas de velocidad y el parpadeo del radar no. [?] | [Cód] `save.reducedMotion` | Que la opción apague todo el movimiento de fondo. |
| A11Y-02 | **S3** | El canvas tiene `aria-label`, pero no hay controles accesibles fuera de él. | [Cód] | Descripciones para lectores de pantalla en los menús. [Dev] |

### 3.9 Audio (AUD)

| ID | Sev. | Hallazgo | Evidencia | Criterio de aceptación |
|---|---|---|---|---|
| AUD-01 | **S1** | Sin música. Solo pitidos sintéticos (WebAudio) para disparo, golpe, moneda y clic. | [Cód] `beep()` | Música de fondo y efectos propios. |
| AUD-02 | **S1** | El vídeo tiene pista de audio y no la he podido analizar: no sé qué música ni qué efectos tiene el original. | [Obs] | Análisis con una herramienta de audio, o con un oyente. [Dev] |
| AUD-03 | **S3** | Hay interruptor de sonido en Ajustes. | [Cód] | Pasa. |

### 3.10 Técnico y código (TEC)

| ID | Sev. | Hallazgo | Evidencia | Criterio de aceptación |
|---|---|---|---|---|
| TEC-01 | **S2** | Las pruebas viven en `scratchpad` y no están en el repositorio. | [Cód] | Pruebas en el repositorio, o un script `npm test`. |
| TEC-02 | **S2** | Rendimiento sin medir en dispositivo. Headless: 60 fps. | [Med] [Dev] | Medir en un móvil de gama media: 60 fps en la escena de conducción con seis enemigos. |
| TEC-03 | **S3** | Código sin uso: `waveBanner` ya no se dibuja; `carEnemy` es un alias. | [Cód] | Eliminar. |
| TEC-04 | **S3** | `<title>` dice "Trayectorias v2". | [Cód] | "Kitten Taxi". |
| TEC-05 | **S2** | Persistencia solo en localStorage, sin copia en la nube ni exportación. | [Cód] | Decisión tuya. |
| TEC-06 | **S2** | Nombre "Kitten Taxi", igual que el original. Un remake con el mismo nombre puede tener problemas de marca. | [Obs] [Cód] | Revisión legal y, si procede, un nombre distinto. Decisión tuya. |

---

## 4. Matriz de paridad (estimación)

Porcentajes orientativos. Son juicios, no medidas.

| Área | Paridad estimada | Motivo principal |
|---|---|---|
| Conducción y persecución | 70 % | Bucle correcto; falta el esquive confirmado, y el jefe. |
| Enemigos y oleadas | 75 % | Cuotas y tiempos calibrados; cadencia sin calibrar. |
| Jefe | 35 % | Estático, cadencia alta, automático incapaz. |
| Túnel y fin de ola | 15 % | Fuera de la escena; sin monedas. |
| Ítems y armas | 40 % | Faltan botellas, arcilla, gema, coche dorado. |
| Economía y progresión | 25 % | Saldo, nivel y llaves sin efecto. |
| Visual (estilo) | 35 % | Vector frente a boceto a lápiz. |
| Visual (escena y medidas) | 80 % | Taxi, horizonte, dinamita, HUD. |
| Pantallas y flujo | 55 % | Faltan burbujas, consejos y detalles de mapa y tienda. |
| Audio | 5 % | Sin música ni efectos propios. |
| Accesibilidad y táctil | 60 % | Botones por debajo de 44 px. |

---

## 5. Plan

**Fase 1: lo que más se nota (S0 y S1 de la escena).**
- BOS-01, BOS-02, BOS-03: jefe con movimiento, cadencia y automático.
- TUN-01, TUN-02, TUN-03: túnel dentro de la escena, con monedas y cuenta atrás.
- TUN-05: quitar el oscurecimiento "DARK PASSAGE".
- ART-03: tipografía manuscrita.
- HUD-01: objetivos táctiles de 44 px.

**Fase 2: estilo.**
- ART-01, ART-02, ART-04, ART-07: trazo a lápiz, trama, carretera clara con arcos, humo.
- SCN-01, SCN-02: base del taxi y marcas de carril.

**Fase 3: economía y progresión.**
- ECO-01 a ECO-04: saldo, nivel, llaves y ruleta.
- ECO-07: efecto del nivel del jugador.

**Fase 4: pantallas.**
- NAV-01, NAV-02: burbujas de tutorial y consejos de carga.
- ART-05, ART-06: tienda con rareza y mapa con candados, parque y retícula.

**Fase 5: contenido y audio.**
- ITM-01, ITM-02: botellas, arcilla, gema, coche dorado.
- AUD-01: música y efectos propios.

**Fase 6: técnico y legal.**
- TEC-01 a TEC-06, A11Y-01, A11Y-02.
- TEC-02: medir en dispositivo.

---

## 6. Decisiones que necesito

1. **Jefe:** ¿bajo la cadencia y el daño, lo muevo de lado con balanceo, y mejoro el automático? Mi propuesta: las tres.
2. **Túnel:** ¿lo implemento dentro de la escena, con monedas y cuenta atrás, como el original? Mi propuesta: sí.
3. **Estilo:** ¿paso al trazo a lápiz? Es el cambio más grande y el que más tiempo lleva. Mi propuesta: sí, por fases.
4. **Economía:** ¿saldo que baja y nivel que sube por visita?
5. **Nivel del jugador:** ¿qué desbloquea? Si no hay respuesta, lo quito.
6. **Esquive:** ningún vídeo lo confirma. ¿Lo mantengo o lo quito?
7. **Valoración de la app:** ¿la replicamos? Mi propuesta: no.
8. **Nombre y marca:** ¿mantenemos "Kitten Taxi"? Recomiendo revisión legal.
9. **Audio:** ¿música y efectos propios?
10. **Idioma:** la UI está en inglés, como el original. ¿Se queda así?
