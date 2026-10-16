# Kitten Taxi: comparación con el original y lista de fallos y faltas

Base revisada: `index.html` (commit fb38976; revisión inicial en 85e7d04). La segunda revisión, con las pistas de alcance y de altura, está en la sección 8.
Referencia: los dos vídeos de partida (parte 1 y 2). El material llega hasta la mitad del nivel 5 y no tiene créditos ni final.

Etiquetas: **[Obs]** visto en el vídeo · **[Cód]** verificado leyendo o buscando en el código · **[Prueba]** comprobado con pruebas automáticas.

---

## 1. Resumen

- La base funciona: sin errores de consola en todas las pantallas y en el recorrido completo (olas, jefe, victoria).
- Cubre bien el **flujo de menús** y la **estructura** (mapa, garaje, tienda, ruleta, resultados).
- Le faltan **casi todas las reglas de economía y progresión del original** (saldo que baja, nivel que sube, bonus por tiempo) y **los momentos de espectáculo** (burbujas de tutorial, pantalla de jefe, "LEVEL ↑").
- Hay **un riesgo que hay que corregir ya**: usa nombres de personas reales como objetivos de robo.

---

## 2. Riesgo crítico (corregir antes de compartir)

| # | Problema | Evidencia | Acción |
|---|---|---|---|
| R1 | Los primeros bancos llevan nombres de personas reales y el juego permite robarles. | [Cód] líneas `name:'…'` del array `BANKS` | Sustituidos por nombres ficticios (Banco Lunar, Banco Mirador, Banco del Puerto, Banco Solano, Banco Ceniza). |

---

## 3. Fallos (lo que existe pero funciona mal o no tiene efecto)

| # | Gravedad | Fallo | Evidencia | Original |
|---|---|---|---|---|
| F1 | Alta | **Las llaves no tienen función.** Se muestran como `k/4` en el mapa, pero nunca se ganan ni se gastan. | [Cód] `save.keys` solo se lee para mostrarlo. | [Obs] Las llaves son un recurso con "+" para comprar y tienen un temporizador m:ss junto a ellas. Su uso exacto no está claro. |
| F2 | Alta | **El saldo del banco no baja** con lo robado y no se guarda entre visitas. | [Cód] `BANKS` es constante; `missionVictory` no escribe el saldo. | [Obs] Saldo 150 → robado 138 → la siguiente visita muestra 12. Saldo 250 → robado 146 → 104. |
| F3 | Alta | **El nivel del banco no sube** al volver. Todos los bancos están fijos. | [Cód] `level:b.level` nunca cambia. | [Obs] El nivel sube cada visita: Level 2 → 3 → 4. |
| F4 | Corregido | ~~Las oleadas duraban ~11 s y el temporizador contaba hacia arriba.~~ Ahora: 22 + 1.5·nivel + 1.2·ola segundos, con cuenta atrás. | [Cód] `waveLength` (línea 204) | [Obs] 20–35 s por ola, con cuenta atrás de 2 decimales (18.86 → 17.86). |
| F5 | Media | **El modo automático muere en las olas 4 o 5** en las pruebas. | [Prueba] con el bot en modo automático. | [Obs] La partida dura seis olas y un jefe sin que el bot tenga que esquivar tanto. |
| F6 | Media | **La ruleta cobra 1 moneda en la primera tirada y luego 200.** | [Cód] `save.spinCount===0?1:200` | [Obs] 500 → 730 → 1000 monedas. |
| F7 | Media | **Se regalan gemas en el banco 0** si tienes menos de 10. | [Cód] `if(m.bankIdx===0&&save.gems<10)save.gems=10` | No aparece en el original. Parece un resto de pruebas. |
| F8 | Media | **Bonus perfecto del 15 %** sin recibir daño. El criterio del original sigue sin estar claro, y en todos los resultados que vi sale 0. | [Cód] `m.perfect=m.damageTaken===0?…` | [Obs] "Per-Fect Bonus (0/-)" con valor 0 en todos los resultados vistos. |
| F9 | Baja | **El botón inferior central muestra "!" y no un contador de bombas.** | [Cód] `ell(210,681…)` con `!` | [Obs] El dial muestra un icono de bomba y un número (0, 2, 3). |
| F10 | Baja | **Los iconos de la garaje y la tienda son emojis** (🔒, ✓, ◉, 🔒 en botones) y dependen de la fuente del sistema. | [Cód] `txt('🔒',…)`, `txt('✓',…)` | No aplica. |
| F11 | Baja | **La pestaña Coin/Key de la tienda no tiene contenido**: muestra "COMING SOON" y no hay nada que comprar. | [Cód] `lists[4]` con `locked:true`. | [Obs] Coin/Key/Jewelry existe en el original. |

---

## 4. Faltas (lo que el original tiene y la base no)

### 4.1 Momentos de espectáculo y tutorial

| # | Falta | Original | Estado en la base |
|---|---|---|---|
| M1 | **Burbujas de tutorial dentro de la primera ola**, que pausan la escena | [Obs] "Bank robber" (0:12), "Drive!" con flechas (0:14), "Police" con corchetes (0:22), "Dodge!" (0:24), "Auto attack when you go near an enemy" (0:36), "get a weapons" (0:48), "get a Coin" (0:58), "Good job! Eat this!" (1:04), "auto drive to touch off! touch to drive yourself!" (1:28), túnel con monedas dobles (1:30). Verificado: la escena no avanza mientras hay burbuja. | Falta. La base tiene un tutorial en 4 pantallas antes de jugar, pero nada dentro de la partida. |
| M2 | **Consejo de carga antes de cada banco** (calle BANK + texto) | [Obs] 4 consejos literales (sección 9 del ANALISIS). | Falta. |
| M3 | **Pantalla de jefe en negro con "BOSS" y destello radial** | [Obs] 2:20 en el nivel 1 y antes del jefe de cada nivel. | Falta. La base muestra un banner "BOSS WAVE!" sobre la escena. |
| M4 | **"LEVEL ↑" con una mejora** al vencer al jefe | [Obs] "Firing rate Up" tras varios niveles. | Falta. Victoria directa a resultados. |
| M5 | **Pantalla de fin de ola con cuenta atrás del tiempo sobrante** y "x 2 Bonus" | [Obs] 17 → 11 → 4 → 0 en negro. | Falta (ver F4). |
| M6 | **Coche dorado** con la llave dorada | [Obs] "If you use the golden key while playing. The golden car shows up on your game play." | Falta. Las llaves no tienen efecto (F1). |
| M7 | **Túnel**: monedas dobles si recoges todas | [Obs] Texto en el tutorial. | Falta. |
| M8 | **Arcilla verde que frena el coche** | [Obs] "Green clay bomb is to slow down my car." | Falta. |
| M9 | **Botellas rojas y contenedor verde** como obstáculos | [Obs] Botellas en carretera, contenedor verde. | Falta. La base usa dinamita y cajas. |
| M10 | **Gemas azules en la carretera** | [Obs] Gema azul recogible. | Falta. Solo hay monedas, salud y cajas. |
| M11 | **Corchetes naranjas sobre el enemigo bloqueado** | [Obs] "Police" con corchetes. | Falta. |
| M12 | **Pistas de la mejora "Firing rate Up"** y del nivel | [Obs] | Falta (ver M4). |

### 4.2 Economía y progresión

| # | Falta | Estado |
|---|---|---|
| M13 | Saldo del banco que baja y persiste (F2) | Falta |
| M14 | Nivel del banco que sube por visita (F3) | Falta |
| M15 | Llaves que se ganan y se gastan (F1) | Falta |
| M16 | Precio de la ruleta 500 → 730 → 1000 (F6) | Diferente |
| M17 | Dos menús de mejoras separados (mapa → garaje → tienda) | Coincide en lo esencial |

### 4.3 Menús y ajustes

| # | Falta | Original | Base |
|---|---|---|---|
| M18 | High Scores | [Obs] En Ajustes | Falta |
| M19 | Achievements | [Obs] En Ajustes | Falta |
| M20 | Facebook, Delete ID, copy ID | [Obs] En Ajustes | Falta a propósito (no se replica, correcto) |
| M21 | Pantalla de título con GameCenter / Guest | [Obs] | Diferente: título con PLAY y HOW TO PLAY |

### 4.4 Audio y arte

| # | Falta | Estado |
|---|---|---|
| M22 | Música y efectos de sonido reales | Falta. Solo pitidos sintéticos (WebAudio). |
| M23 | Trazo de lápiz con relleno a mano | Falta. Las formas son geométricas. |
| M24 | Mapa ilustrado con detalle | Diferente: patrón rayado y edificios abstractos. |
| M25 | Líneas de velocidad intensas | Parcial: hay una línea central y líneas laterales suaves. |

---

## 5. Lo que sí coincide con el original

- Conducción por arrastre y AUTO (con apagado al tocar).
- Disparo automático contra enemigos en rango.
- Seis oleadas con jefe en la sexta.
- Pausa y "Continue" por 1 gema al morir.
- Pantalla de resultados con "Coins stolen from bank", "Earn money by destroying", "Per-Fect Bonus" y "Total".
- Rueda de premios con monedas y gemas.
- Tienda con pestañas Car, Driver, Assist, Pet y Coin/Key.
- Mapa de bancos con popup de nivel y saldo, y pie con Back y Start.
- Armas Pistol, Bomb, Shot y Machine con mejoras.
- HUD: etiqueta WAVE, temporizador, AUTO, pausa, barra inferior izquierda y contador de monedas bajo el horizonte.
- Enemigos con barra de vida verde y números de daño.

---

## 6. Desviaciones deliberadas (confirmar si las quieres)

- **Carretera:** la base es asfalto gris oscuro con arcenes. El original es blanco con arcos de lápiz.
- **Enemigos:** la base usa policía, furgoneta blindada y ambulancia con aspecto de taxi. El original tiene policía, camión blanco, sedán azul y jefes de camión.
- **Bonus perfecto:** la base da el 15 % sin daño. El original no tiene un criterio conocido.
- **Progresión:** la base tiene 15 bancos. En el material del original se ven 6 o más, con el mapa de 15 posibles no confirmado.

---

## 7. Plan sugerido, por prioridad

**Prioridad 0 (antes de compartir):**
1. R1: sustituir los nombres de los bancos.
2. F1, F2, F3: llaves con función, saldo que baja y nivel que sube.

**Prioridad 1 (lo que más se nota al jugar):**
3. F4 y M5: oleadas de 20–35 s con cuenta atrás y bonus por tiempo sobrante.
4. M1: burbujas de tutorial en la primera ola.
5. M3 y M4: pantalla de jefe y "LEVEL ↑".
6. F5: equilibrio del modo automático.

**Prioridad 2:**
7. M2: consejo de carga antes de cada banco.
8. M6, M7, M8, M9, M10: coche dorado, túnel, arcilla, botellas y gemas.
9. F6, F7, F8: precios, gemas regaladas y criterio del bonus perfecto.

**Prioridad 3 (pulido):**
10. M22 a M25: sonido, arte a lápiz, mapa ilustrado y líneas de velocidad.
11. F9, F10, F11: contador de bombas, iconos sin emoji y pestaña Coin/Key.

---

## 8. Segunda revisión (commit fb38976)

Esta revisión responde a tres observaciones: el arma tiene demasiado alcance, solo debería disparar cuando el enemigo está a nuestra altura, y los coches nunca terminan de adelantarnos. Persiguen un poco por detrás, lanzan bombas, y solo se les dispara en contacto. Además, el juego transmite menos sensación de velocidad que el original. No se ha cambiado el código del juego; solo este documento.

Etiquetas igual que arriba. Medido a 4 fps (parte 1, 116–126 s). Esa resolución da una precisión de ±0.25 s.

### 8.1 Las observaciones y lo que se ve en el original

| # | Observación | Código (base) | Original |
|---|---|---|---|
| P1 | El arma tiene demasiado alcance | [Cód] El objetivo es válido con `d∈(-.42,.9)` (línea 257): de y≈344, justo bajo el horizonte, a y≈714, casi al borde inferior. Un enemigo queda en tiro unos 5 s. | [Obs] Los corchetes naranjas aparecen solo cuando el enemigo está pegado al taxi. |
| P2 | Solo debería disparar cuando la policía está a nuestra altura | [Cód] Los enemigos normales tienen `stopD:9` (línea 214): no se paran. Cruzan el coche y salen en d>1.12. | [Obs] La policía está a la altura del taxi, solapada con él, y cae 1–2 s después (parte 1, 120–122 s). En el tutorial (~0:31–0:35) ya lanza dinamita desde esa fila, hacia el taxi. |
| P3 | Solo disparamos en contacto | [Cód] El arma apunta a cualquier enemigo con `d∈(-.42,.9)` y lateral de 18–133 px (línea 257), o sea, a distancia. El choque también nos hace daño (línea 253). | [Obs] El corchete aparece justo antes del choque y la explosión coincide con el contacto. A 4 fps no veo disparos a distancia. La burbuja del tutorial dice "Auto attack when you go near an enemy": "near", no "from afar". |
| P4 | Los coches nunca terminan de adelantarnos | [Cód] Los enemigos se van: salen en d>1.12 (línea 254) y no hay nada que los retenga. | [Obs] Entre 120 y 139 s (oleadas 4 y 5, muestreo de 1 fps), van llegando uno tras otro a la altura del taxi, y ninguno se marcha antes de ser eliminado. |
| P5 | Sensación de velocidad más baja | [Cód] Las líneas laterales son finas y suaves (línea 140). No hay líneas radiales. Los enemigos avanzan unos 90–120 px/s por la mitad de la pantalla (estimado con `groundY` y `vd`). | [Obs] Líneas radiales oscuras que cubren la carretera durante la conducción (125 s y 121–122 s). Las cajas y las monedas pasan rápido. La velocidad exacta no está medida (ver nota). |

Nota sobre profundidad [?]: en 121, 122 y 134 s, la base de la policía está en la misma línea que la del taxi (unos 10 px de diferencia en la resolución de 1280 px). No veo un desfase claro hacia atrás; lo que sí veo es el solapamiento. Si tú lo ves "un poco detrás", probablemente sea ese solapamiento. La propuesta usa una banda de profundidad que cubre las dos lecturas.

Nota sobre velocidad [?]: no he podido medir la velocidad de la carretera en el original. Las líneas radiales se redibujan en cada fotograma, así que el desplazamiento entre fotogramas no sirve. Para medirla habría que seguir una caja o una moneda de un fotograma a otro.

### 8.2 Propuesta (no aplicada)

Corrijo lo que escribí antes: la policía no se aparca a distancia y luego muere. Se queda pegada al taxi y cae por contacto. Eso sustituye la fase de `hold` que propuse. Responde a P1–P4.

1. **Persecución**: el enemigo entra desde detrás y frena al acercarse (d de −0.45 a −0.06). Después se queda en esa banda mientras la carretera pasa, y no se marcha (cambia `stopD:9`).
2. **Zona de contacto**: el arma dispara solo cuando el enemigo está en contacto: d∈(−.08,.1) y lateral de unos 60 px (un ancho de coche). El número exacto lo ajusto con el bot.
3. **Corchetes** sobre el objetivo (M11).
4. **Tiempo de caída**: ya no hace falta un valor fijo. Con la pistola (unos 20 de daño por segundo) la policía de nivel 1 cae en ~1 s, en línea con el original (1–2 s).
5. **Choque**: en el original el choque elimina al enemigo. El daño que recibe el taxi en ese choque no lo he podido medir. Hoy recibe 6–11 por contacto (línea 253).
6. **Bombas**: lanzadas desde la banda de persecución, caen delante del taxi, como pediste. Hoy empiezan a lanzar en d>−.3 (N2). Lo mantengo, pero hay que equilibrarlo con el bot.
7. **Auto-steer**: hoy se pone a ±78 px del carril del enemigo más cercano con d>−.4 (línea 239). Con enemigos que persiguen, se pegará a ellos. Hay que probarlo con el bot.

Decisiones que necesito de ti:
- ¿El choque debe dañar al taxi, o solo al enemigo?
- ¿Cuántos enemigos por ola? (ver 8.3)
- ¿Lanzan solo desde detrás, o también desde el costado? En el tutorial se ve desde el costado.

### 8.3 Fin de ola anticipado (fallo de juego, no solo visual)

- [Obs] Ola 3 (parte 1, ~116–119 s): el cronómetro marca 19.6. La pantalla pasa a negro con "19 → 11 → 3" y aparece "19 x2 Bonus". Después empieza la ola 4. En la ola 4 el cronómetro estaba en 23.2 y la pantalla pasa a negro con "22 → 14 → 5". La ola termina con tiempo sobrante y ese tiempo se convierte en bonus.
- [Cód] Nuestra ola termina solo cuando se agota el tiempo (línea 243: `if(m.waveTime>=m.waveDuration)nextWave()`). Los enemigos se generan sin límite total, hasta 3 vivos a la vez. Acabar rápido no tiene premio.
- [?] No he verificado en el vídeo que la causa sea haber abatido a todos los enemigos. Es lo más probable, pero hace falta más vídeo para confirmarlo.
- Propuesta: cuota de enemigos por ola. Al llegar a cero, negro con cuenta atrás del tiempo sobrante y multiplicador ×2 (la fórmula exacta es [?]). Esto cubre M5.

### 8.4 Fallos nuevos

| # | Gravedad | Fallo | Evidencia |
|---|---|---|---|
| N1 | Alta | El jefe se aparca en el centro del carril (`210±30`, `stopD .02`), dentro de la zona de choque. Si conduces a menos de 42 px de él, recibes 11 de daño cada 1.3 s. A menos de 18 px no puedes dispararle. | [Cód] líneas 214, 253 y 257. [Prueba] pendiente. |
| N2 | Alta | Los enemigos empiezan a lanzar en d>−.3, cuando todavía están detrás del coche. Con P2–P4, el coche no puede responder hasta el contacto. Hay que equilibrarlo a la vez. | [Cód] línea 250. |

### 8.5 Estado de la lista anterior

| Elemento | Estado |
|---|---|
| Orientación (coche de frente, carretera hacia abajo) | Corregido en fb38976 |
| R1, nombres de bancos | Corregido |
| F4, duración de oleada | Corregido (ver sección 3) |
| M3, pantalla de jefe en negro | Falta. Solo hay un banner "BOSS WAVE!" (línea 283) y un toast "BOSS INCOMING!" (línea 215). |
| M4, "LEVEL ↑" con mejora | Parcial: aparece "LEVEL N COMPLETED" (línea 310), sin mejora. |
| M5, tally del tiempo sobrante | Falta (ver 8.3). |
| M11, corchetes sobre el objetivo | Falta (ver 8.2). |
| F1, llaves sin función | Sigue: solo se muestran (línea 171). |
| F2 y F3, saldo y nivel de banco | Siguen: `BANKS` es constante y la victoria solo guarda desbloqueo y banco seleccionado (línea 231). |
| F6, precio de la ruleta | Sigue (líneas 197 y 199). |
| F7, gemas regaladas en el banco 0 | Sigue (línea 231). |
| F8, bonus perfecto | Sigue (línea 231). |
| F9, botón central con "!" | Sigue (línea 282). |
| F5, modo automático | No medido en esta revisión. |
| F10 y F11 | Sin cambios. No los he vuelto a revisar. |
| M1, M6 a M10 (burbujas, dorado, túnel, arcilla, botellas, gemas en la carretera) | Siguen sin aparecer en el código (búsqueda de palabras clave). |

### 8.6 Plan propuesto, por orden

1. P1–P4 y M11 juntos: persecución en banda, zona de contacto y corchetes. Es el cambio principal.
2. P5: velocidad. Líneas radiales durante la conducción (M25), y subir el flujo de la carretera y de las cajas para que el movimiento se note más.
3. Fin de ola por cuota, con tally del tiempo sobrante (8.3 y M5).
4. Jefe: que no bloquee el centro ni la zona de choque (N1).
5. Equilibrio con el bot: N2 y F5.
6. Después: M1 burbujas, M3 pantalla de jefe y M4 "LEVEL ↑".
