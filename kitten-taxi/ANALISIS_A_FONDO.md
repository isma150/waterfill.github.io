# Kitten Taxi: análisis a fondo

Versión analizada: commit `94f5a67` (pulido visual tras la prueba en móvil).
Referencia: los dos vídeos de partida (parte 1, 773 s, y parte 2, 732 s), incluido el audio.
Documentos relacionados: `ANALISIS.md` (análisis original), `COMPARACION.md` (fallos y faltas, secciones 1 a 10).

Etiquetas: **[Obs]** visto en el vídeo · **[Med]** medido sobre fotogramas o capturas · **[Cód]** verificado en el código · **[Sim]** resultado de la simulación automática (no es un jugador humano) · **[?]** sin confirmar.

---

## 0. Resumen

- **El bucle de juego funciona de principio a fin**: conducir, perseguir, chocar, oleadas con cuenta atrás, fin de ola con tally, jefe, resultados y garaje. No hay errores de consola en las pruebas.
- **Lo visual ya se parece al original** en lo principal: el taxi sobre el horizonte, el horizonte, el HUD superior, la dinamita por encima del coche, la transición de fin de ola y las furgonetas de policía de frente.
- **Lo que más se nota que falta**, por orden:
  1. **El jefe no se puede ganar en la simulación automática.** Se queda fijo en un carril lateral, dispara cada 1.3 a 1.8 s y el automático nunca llega a chocar con él [Sim]. En el original los camiones se mueven y se balancean.
  2. **Economía sin consecuencias.** El saldo del banco no baja, el nivel del banco no sube, las llaves no sirven para nada y la ruleta cobra 1 y luego 200 monedas (original: 500, 730 y 1000) [Cód].
  3. **El tutorial dentro de la partida no existe** (burbujas de "Drive!", "Dodge!", "get a Coin"…) [Cód, Obs].
  4. **El túnel del tutorial** ("doble de monedas si recoges todas las del túnel") no tiene mecánica. Solo tenemos el arco de fin de ola y un ×2 [Obs].
  5. **Audio**: solo pitidos sintéticos. El vídeo tiene pista de audio, que no he podido analizar porque no puedo escucharla [Cód, Obs].
  6. **Tipografía**: usamos Comic Sans / Comic Neue. El original usa una letra a mano distinta [Cód, Obs].
  7. **Resto de la base**: el oscurecimiento "DARK PASSAGE" de la ola 4 no existe en el original [Obs, Cód].
- **Lo que ya no es un problema** (corregido en esta ronda): el orden de dibujo de la dinamita, la escala y la posición del taxi, el banner "BOSS WAVE", la barra de nivel inferior y la transición del fin de ola (ahora es un círculo que se cierra, como pediste).

---

## 1. Fuentes y método

- **Vídeos:** dos partes con cuatro partidas completas en la parte 2 (dos en nivel 4 y dos en nivel 5) y tres bancos de nivel 1 a 3 en la parte 1.
- **Recuento de oleadas:** dos agentes, uno por vídeo, con muestreo de 2 fps. Ventanas y tallies son firmes (±0.5 s). Los números de enemigos son estimaciones (±1–2 por oleada).
- **Medidas visuales:** fotogramas a 720 × 1280 del original y capturas a 420 × 746 de nuestra versión (Playwright, Chromium). Error de medida ±0.01 de la altura.
- **Simulación automática:** el gancho de pruebas `KittenTaxiQA` con el piloto automático. Sirve para detectar problemas de equilibrio, no para decidir la dificultad real con un jugador humano.
- **Límites:** no he podido escuchar el audio; la velocidad de la carretera del original no se puede medir con precisión, porque las líneas radiales se redibujan en cada fotograma; y la vida del taxi del original no aparece en el HUD.

---

## 2. Flujo de pantallas

| Pantalla | Original [Obs] | Nuestra base [Cód] | Estado |
|---|---|---|---|
| Título | Logo sobre una calle con letrero BANK; botones GameCenter y Guest (0:00–0:11). | Logo, PLAY y HOW TO PLAY. | Diferente a propósito (M21). |
| Tutorial | Burbujas dentro de la primera ola: "Bank robber", "Drive!", "Police", "Dodge!", "Auto attack when you go near an enemy", "get a weapons", "get a Coin", "Good job! Eat this!", "auto drive to touch off!", y el túnel (0:12–1:30). Se congela la escena mientras hay burbuja. | Cuatro pantallas de tutorial antes de jugar. Nada dentro de la partida. | **Falta** (M1). |
| Consejos de carga | Cuatro consejos antes de cada banco. | No existen. | **Falta** (M2). |
| Mapa | Nodos con candado, popup con nombre, Level y Balances. Pie con Back, monedas, gemas, llaves y Start. | Igual en lo visual. Saldo y nivel fijos. | Parcial (F2, F3). |
| Partida | WAVE, Level, cronómetro, AUTO, pausa, barra inferior con nivel, dial con bomba. | WAVE, Level, cronómetro, AUTO, pausa, barra de nivel (nueva), vida sobre el taxi, dial con "!". | Casi igual. Falta el icono de bomba (V9). |
| Fin de ola | Tally con cuenta atrás, arco de cielo, silueta del taxi entrando y "N x2 Bonus" [Obs, 472–477 s]. | Círculo que se cierra sobre el taxi, cuenta atrás y "N x2 Bonus". | Igual en la idea (decisión tuya). |
| Jefe | Camiones grandes; las furgonetas normales siguen llegando; sin banner ni barra en el HUD. | Camión de jefe fijo en un carril lateral; furgonetas normales; barra verde sobre el jefe. | Ver sección 4.3. |
| Resultados | "Coins stolen from bank", "Earn money by destroying", "Per-Fect Bonus", "Total" [Obs]. El bonus perfecto sale 0 en todas las partidas del original. | Los mismos rótulos. El bonus perfecto da el 15 % sin daño. | Diferencia en el bonus (F8). |
| Garaje, tienda, ruleta | Pestañas Car, Driver, Assist, Pet y Coin/Key con contenido. Ruleta: 500, 730, 1000. | Coin/Key en "COMING SOON". Ruleta: 1 y luego 200. | F6, F11. |
| Ajustes | High Scores, Achievements, Facebook, Delete ID, copiar ID. | Sonido y movimiento reducido. | M18 a M20. |

---

## 3. Visual

### 3.1 Medidas

| Elemento | Original [Med] | Nuestra base [Med] | Diferencia |
|---|---|---|---|
| Horizonte (fin del cielo) | 0.445 de la altura | ≈0.445 (332 px de 746) | Igual. |
| Base del taxi | ≈0.40 (sobre el horizonte) | ≈0.445 (sobre el horizonte) | **≈0.045 de altura (≈34 px) más abajo.** |
| Ancho del taxi | 0.296 del ancho | 0.296 (escala 0.92) | Igual. |
| Ancho de la furgoneta de policía | ≈0.7 del taxi | ≈0.7 del taxi | Igual. |
| Dinamita a distancia | ≈0.026 del ancho | ≈0.024 del ancho | Parecida. |
| Monedas en el carril | ≈0.025 del ancho | ≈0.037 del ancho | **Nuestras son ≈50 % más grandes.** |
| Camión de jefe | ≈0.34 del ancho | ≈0.32 del ancho | Parecido. |

### 3.2 Lo que no es igual

| # | Elemento | Original | Nuestra base | Prioridad |
|---|---|---|---|---|
| V1 | Carretera | Suelo blanco con líneas de lápiz y arcos. | Suelo gris claro con bordes oscuros y marcas grises. | Media (aprobada, pero las marcas son rectas). |
| V2 | Líneas de velocidad | Trazos negros, densos, que cubren la carretera en los tramos rápidos [Obs]. | Trazos grises finos y rectos. | **Alta** (se ven como palitos). |
| V3 | Monedas | Pequeñas (≈0.025). | Un 50 % más grandes. | Media. |
| V4 | Tipografía | Letra a mano (los números del cronómetro y los textos del tutorial). | Comic Sans MS / Comic Neue. | **Alta** (es lo primero que se ve). |
| V5 | Furgonetas normales | Furgoneta blanca redondeada con rejilla, faros y luz en el techo. | Igual, pero sin el detalle de la rejilla y con el texto "POLICE" quitado. | Baja. |
| V6 | Camiones del jefe | Verde, azul, amarillo con pala y gris-azul; se balancean y se ven de lado. | Un camión por tipo, sin balanceo, quieto. | **Alta** (ver 4.3). |
| V7 | Cielo | Azul con nubes en los bancos de tema azul; blanco con edificios a lápiz en la ciudad. | Gris claro con edificios. | Baja. |
| V8 | Humo de explosión | Nubes blancas grandes que tapan el coche. | Destellos pequeños. | Media. |
| V9 | Dial central | Icono de bomba con el número de bombas. | Un "!" gris. | Baja. |
| V10 | Barra inferior izquierda | Estrella, "N Lv" y porcentaje. | Igual (aprobada). | Hecho. |
| V11 | Base del taxi | Ligeramente sobre el horizonte. | Sobre el horizonte (≈34 px más abajo). | Baja. |
| V12 | Dinamita al lanzarse | Sale desde el coche enemigo y sube en arco. | Igual, desde la altura del enemigo. | Hecho. |

### 3.3 Lo que sí coincide

- Los gatos en el parabrisas, con el taxi de frente.
- El horizonte, las etiquetas WAVE y Level, el AUTO circular, la pausa y el cronómetro grande.
- Las barras verdes de vida sobre los enemigos y los corchetes naranjas de bloqueo.
- La dinamita por encima del coche mientras vuela, y el aviso de impacto como triángulo rojo.

---

## 4. Jugabilidad

### 4.1 Conducción y persecución

- **Original [Obs]:** los vehículos llegan de ambos lados, se quedan junto al taxi, a veces detrás o encima, y ninguno pasa a través. Se eliminan por contacto, a razón de uno cada 0.5 a 1.5 s en las oleadas ocupadas.
- **Base [Cód]:** igual desde la última ronda. Los enemigos se quedan a la altura del taxi, el arma solo dispara en contacto y el choque no daña al taxi.
- **Esquive:** implementado con probabilidad creciente por ola, pero **ni el agente de la parte 1 ni el de la parte 2 lo confirman en el vídeo** [Obs]. Lo dejé porque lo pediste; hay que decidir si se queda.

### 4.2 Oleadas y enemigos

| Dato | Original [Obs] | Base [Cód] | Estado |
|---|---|---|---|
| Enemigos por oleada, niveles 1 a 3 | 2 a 5 (media ≈3.5) | `[3,4,4,3,4]`, uno menos en nivel 1 | Ajustado. |
| Enemigos por oleada, niveles 4 y 5 | 3 a 10 (media ≈6.3) | `[6,9,5,8,5]` | Ajustado. Niveles 6 o más sin datos. |
| Duración de la ola (hasta despejar) | 2.5 a 7 s en nivel 1; 6 a 12 s en niveles 2 y 3; 9 a 19 s en 4 y 5. | Cronómetro `10 + 5·ola` (+3 desde nivel 4). | Ajustado. |
| Fin de ola | 17 de 20 oleadas con tiempo terminan vacías; ninguna llega a cero. | Termina al despejarse; si se agota el tiempo, sin bonus. | Igual. |
| Primera oleada | Sin cronómetro en el tutorial [Obs]. | Con cronómetro. | **Diferente** (M1). |
| Cadencia de disparo enemiga | No medida con fiabilidad. | 3 a 4.2 s por enemigo. | **Sin calibrar** (la estimación anterior se basaba en una lectura errónea). |
| Tipos | Policía, ambulancia, furgoneta blindada, camiones de jefe. | Policía, ambulancia, furgoneta blindada (nivel 3 en adelante) y jefe. | Parecido. |

### 4.3 Jefe

**Original [Obs]:** cuatro peleas en la parte 2. A (nivel 4) se gana en 21 s; C1 (nivel 5) en 34 s; C2 en 27 s; B se pierde en 29 s (Continue / Give up). Durante la pelea siguen llegando furgonetas normales. Los camiones están de lado, detrás y a un lado del taxi, se balancean y se solapan con él.

**Base [Cód, Sim]:**
- El jefe aparece en un carril lateral fijo (lane 98 o 322) y no cambia de posición durante la pelea.
- Dispara cada 1.3 a 1.8 s, con un 60 % de dinamita, y cada dinamita quita unos 14 de vida con el nivel 1.
- El piloto automático elige como objetivo al enemigo más cercano en lateral, y casi siempre son las furgonetas. Así el taxi nunca llega a chocar con el jefe.
- **En la simulación, el jefe deja al taxi en 0 de vida en 21 s, con 8 golpes** (registro del 80 s).

**Problemas que se deducen:**
1. Ritmo de disparo del jefe: demasiado alto para lo que el original permite.
2. Movimiento: no hay balanceo ni cambio de carril, así que el jefe es un objetivo estático.
3. Prioridad del automático: debería perseguir al jefe cuando está en pantalla, o al menos no dejarlo sin atacar.

### 4.4 Dinamita, golpes y vida

- **Original [Obs]:** la vida del taxi no aparece en el HUD. No he podido medir el daño por golpe. El flash rojo a pantalla completa marca los golpes directos (376.8, 533.0 y 601.8 s).
- **Base [Cód]:** vida de 100 (más el coche y las mejoras). Dinamita: 12 + 1.9·nivel. Disparo: 5 + 1.4·nivel. Escudo: hasta un 40 %. La vida se muestra sobre el taxi.
- **[?]** Los valores de daño son provisionales.

### 4.5 Ítems y pickups

| Elemento | Original [Obs] | Base | Estado |
|---|---|---|---|
| Monedas de la carretera | Sí. | Sí. | Igual. |
| Cajas con "?" (arma) | Sí. | Sí. | Igual. |
| Botella roja y contenedor verde | Sí. | No. | **Falta** (M9). |
| Gema azul en la carretera | Sí ("gema de cambio"). | No. | **Falta** (M10). |
| Arcilla verde que frena | Sí. | No. | **Falta** (M8). |
| Llave dorada y coche dorado | Sí: el consejo dice que la llave dorada hace aparecer el coche dorado en la partida. | Las llaves no tienen función. | **Falta** (M6, F1). |
| Túnel con monedas dobles | Sí, en el tutorial: "double coins when you get all the coins from the tunnel". | Solo el arco de fin de ola y un ×2. | **Falta la mecánica** (M7). |
| Sistema de nivel del jugador (barra inferior) | Sí: estrella, "N Lv" y porcentaje. | Sí, pero **no desbloquea nada** todavía. | **Incompleto**. |

### 4.6 Armas

- **Base [Cód]:** Pistol, Bomb, Shot, Machine. Cada una tiene una cadencia y un daño base. Se mejoran con monedas. Los disparos son instantáneos y se aplican solo en contacto.
- **Original [Obs]:** la mejora "Firing rate Up" aparece al vencer al jefe (M4); la base tiene un "LEVEL N COMPLETED" sin mejora.
- **Diferencia** en la bomba: el original la muestra como un icono con su número en el dial (V9). En la base no hay contador de bombas.

---

## 5. Progresión y economía

| # | Qué pasa en el original [Obs] | Qué pasa en la base [Cód] | Estado |
|---|---|---|---|
| F1 | Las llaves se ganan y se gastan, con un temporizador junto a ellas. | Solo se muestran (`save.keys`). | **Sin función.** |
| F2 | El saldo del banco baja con lo robado y se guarda entre visitas (150 → 12). | `BANKS` es constante; la victoria no guarda el saldo. | **Sin función.** |
| F3 | El nivel del banco sube en cada visita (2 → 3 → 4). | `level` fijo en `BANKS`. | **Sin función.** |
| F6 | Ruleta: 500, 730, 1000. | 1, luego 200. | **Diferente.** |
| F7 | No aparece. | Regala gemas en el banco 0 si tienes menos de 10. | Resto de pruebas. |
| F8 | Bonus perfecto siempre 0. | 15 % sin daño. | Diferente. |
| F11 | Coin/Key tiene contenido. | "COMING SOON". | **Falta**. |
| — | Tally "N x2 Bonus" al final de la ola [Obs]. | Igual; el multiplicador ×2 es una suposición [?]. | Parcial. |
| — | Coins stolen from bank, perfect bonus, total. | Igual. | Igual. |
| — | Nivel del jugador con porcentaje. | Barra nueva; los valores (4 por muerte, 30 por jefe, 1 por moneda, 60 + 20·nivel) son provisionales y no desbloquean nada. | **Provisional**. |

**Coherencia económica [Cód]:** las monedas de la base suben con los enemigos (23 + 7·nivel + 3·ola por enemigo; 110 + 42·nivel el jefe) y con las monedas de la carretera (25 por moneda, hasta el saldo del banco). Como el saldo no baja, cualquier banco se puede repetir hasta el infinito sin consecuencias.

---

## 6. Audio

- **Original [Obs]:** el vídeo tiene pista de audio. No la he podido analizar porque no puedo escucharla, así que no sé qué música ni qué efectos tiene.
- **Base [Cód]:** solo pitidos sintéticos (WebAudio) para disparo, golpe, moneda y clic. Sin música.
- **Propuesta:** música de fondo y efectos nuevos, no copiados del original. Hace falta decidir si se quiere música propia.

---

## 7. Técnico y código

- **Restos de la base:**
  - `DARK PASSAGE`: oscurece la pantalla y muestra el texto en la ola 4 durante 3 s. **No aparece en el original** (en la ola 4 de nivel 1, 119–126 s, la pantalla está clara) [Obs]. Debería quitarse.
  - Las pruebas no están en el repositorio; viven en `scratchpad`. Si el proyecto va a seguir, conviene llevarlas al repo.
- **Código sin uso:** `waveBanner` ya no se dibuja; `carEnemy` queda como alias. Hay que limpiar.
- **Nombre:** el `<title>` sigue diciendo "Trayectorias v2", un nombre de la base anterior.
- **Guardado:** versión 2 con migración por mezcla de valores por defecto. Los campos nuevos (`xp`, `plevel`) se añaden sin romper partidas anteriores [Cód].
- **Rendimiento:** no se ha medido. El dibujo es por fotograma sin caché; en móvil conviene perfilarlo [?].

---

## 8. Plan por prioridad

**P0 (lo que más se nota y bloquea):**
1. Jefe: ritmo de disparo, movimiento lateral con balanceo, y prioridad del automático para que lo persiga.
2. Tipografía: sustituir Comic Sans por una letra a mano más cercana al original.
3. Quitar "DARK PASSAGE".

**P1 (lo que hace que el juego sea el del original):**
4. Economía: saldo que baja, nivel del banco que sube por visita, llaves con función, precios de la ruleta.
5. Tutorial dentro de la primera ola (burbujas que congelan la escena).
6. Efecto del nivel del jugador (qué desbloquea) o quitarlo.
7. Audio propio: música de fondo y efectos.

**P2 (contenido):**
8. Coche dorado, túnel con monedas dobles, arcilla, botellas, gemas azules.
9. Bonus perfecto (criterio), contador de bombas en el dial, pestaña Coin/Key.

**P3 (pulido):**
10. Líneas de velocidad oscuras y densas, monedas al tamaño del original, cielo de los bancos de ciudad, humo de explosión, base del taxi 34 px más arriba.
11. Limpieza de código y tests dentro del repositorio.

---

## 9. Decisiones que necesito

1. **Jefe:** ¿bajo la cadencia y el daño, o dejo el jefe como está y mejoro el automático? Mi propuesta: las dos cosas, con el jefe moviéndose de lado.
2. **Economía:** ¿implemento el saldo que baja y el nivel que sube por visita? Es lo que más diferencia la progresión.
3. **Nivel del jugador:** ¿qué desbloquea? Si no hay respuesta, lo quito.
4. **Esquive:** ¿lo mantengo? Ningún vídeo lo confirma.
5. **Audio:** ¿música y efectos propios?
