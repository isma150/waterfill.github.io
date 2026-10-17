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

---

## 9. Calibración con los vídeos

Recuento hecho con un agente por vídeo, con muestreo de 2 fps. Los tiempos y tallies son firmes (±0.5 s). Los números de enemigos son estimaciones (±1–2 por oleada). Parte 1: niveles 1 a 3. Parte 2: niveles 4 y 5.

### 9.1 Parte 1 (niveles 1 a 3)

| Oleada | Tiempo (s) | Cronómetro al inicio → al terminar | Enemigos (est.) | Pantalla vacía al terminar |
|---|---|---|---|---|
| L1 W1 | 88–90.5 | 15 → 12.9 | 2 | sí |
| L1 W2 | 99–101.5 | 20 → 17.7 | 2 | sí |
| L1 W3 | 107–113.5 | 25 → 19.3 | 4 | sí (probable) |
| L1 W4 | 119–126 | 30 → 23.2 | 3 | sí |
| L1 W5 | 132.5–137.5 | 35 → 30.4 | 3 | sí |
| L2 W1 | 273–284.5 | 15 → 3.7 | 4 | sí |
| L2 W2 | 287.5–299.5 | 20 → 8.9 | 4 | sí |
| L2 W3 | 303.5–312.5 | 25 → 16.7 | 3 | sí |
| L2 W4 | 317.5–327.5 | 30 → 20.8 | 3 | sí |
| L2 W5 | 333.5–344.5 | 35 → 24.1 | 3 | sí |
| L3-A W1 | 446–458 | 20 → 7.3 | 3 | incierto |
| L3-A W2 | 460–471.6 | 25 → 14.0 | 5 | no (1–2 furgonetas sobre el taxi) |
| L3-A W3 | 475–485.5 | 30 → 19.8 | 3 | sí |
| L3-A W4 | 490–496 | 35 → 28.4 | 3 | sí |
| L3-A W5 | 503–511.5 | 40 → 30.3 | 5 | sí |
| L3-B W1 | 678.7–686 | 15 → 8.7 | 3 | sí |
| L3-B W2 | 690–702 | 20 → 9.2 | 4 | sí |
| L3-B W3 | 705.5–716 | 25 → 16.0 | 4 | sí |
| L3-B W4 | 721–731 | 30 → 21.3 | 3 | sí |
| L3-B W5 | 736.5–744 | 35 → 28.5 | 3 | sí |

Conclusiones:
- **Duración de la oleada:** las oleadas son cortas. En L1 duran 2.5–7 s y en L2 y L3 entre 6 y 12 s. El enemigo cae rápido y la oleada acaba. Es el origen principal de la sensación de velocidad.
- **Cronómetro inicial:** 15, 20, 25, 30 y 35 s para las oleadas 1 a 5 (L3-A usa 20–40 s). La base usaba 22–29 s. Cambiado a `10 + 5·ola`.
- **Fin de ola:** 17 de las 20 oleadas con tiempo terminan con la pantalla vacía. La oleada acaba cuando cae el último enemigo, y el tiempo sobrante se convierte en el tally "xN Bonus". Ninguna oleada llegó a cero.
- **Enemigos por oleada:** entre 2 y 5, con una media de unos 3.5. Cuota provisional en la base: [3,4,4,3,4], con uno menos en nivel 1.
- **Lados:** llegan de ambos lados. Se quedan junto al taxi y a veces detrás o encima de él. No se ha visto ninguno pasar a través.
- **Esquive:** **no observado en la parte 1**. El único aviso es "Dodge!" del tutorial. Esto contradice la observación del usuario. Queda pendiente de verificar con la parte 2 y con un vistazo dirigido.
- **Dinamita:** cae delante del taxi. Aparece un triángulo rojo de aviso antes del impacto (281, 325, 469, 685, 697, 712–714 y 728 s, con muestreo ligero). El lanzamiento no se vio.
- **Barra inferior izquierda (corregido):** no es la vida del taxi. Es el progreso de nivel: estrella, «N Lv» y un porcentaje. Lo confirmé en las dos partes. Las cifras 38 → 21 que leí antes eran ese porcentaje, así que **el daño del original no está calibrado**. Su vida no aparece en el HUD.
- **Jefes:** L1 W6 (147–173 s, muere hacia 158 s), L2 W6 (355–381 s, camión azul), L3-A W6 (521–554 s, camión azul) y L3-B W6 (754–773 s o más, camión verde). Terminan en la pantalla de resultados.
- **Sin identificar:** resplandores amarillos sobre el taxi en 121–123, 484–485, 531–535 y 764–772 s.

Consecuencias para la base (aplicadas):
- Cronómetro `10 + 5·ola`.
- Cuota por oleada `[3,4,4,3,4]`, con uno menos en nivel 1.
- Aparición de enemigos cada 0.9–1.6 s, hasta 2 vivos en la oleada 1 y 3 después.
- Cadencia de disparo enemiga: vuelve a 3–4.2 s. El valor de 4.5–6.5 s que puse antes se basaba en la lectura errónea de la barra de nivel.

### 9.2 Parte 2 (niveles 4 y 5)

Cuatro partidas completas: A y B en nivel 4, C1 y C2 en nivel 5. Cada una con cinco oleadas y un jefe. Celda: ventana de juego en segundos · tally al terminar · enemigos estimados.

| Oleada | A (nivel 4) | B (nivel 4) | C1 (nivel 5) | C2 (nivel 5) |
|---|---|---|---|---|
| W1 | 70–81 · 8 · ~6 | 268–282 · 5 · ~4 | 423–434 · 7 · ~7 | 581–592 · 4 · ~5 |
| W2 | 84–103 · 5 · ~10 | 284–296 · 9 · ~8 | 438–451 · 10 · ~8 | 596–612 · 9 · ~9 |
| W3 | 106–116 · 18 · ~4 | 299–308 · 18 · ~3 | 455–464 · 20 · ~6 | 617–627 · 15 · ~5 |
| W4 | 121–138 · 17 · ~10 | 313–323 · 20 · ~6 | 470–483 · 20 · ~8 | 632–647 · 15 · ~9 |
| W5 | 142–151 · 30 · ~3 | 328–340 · 24 · ~4 | 489–498 · 28 · ~5 | 652–662 · 25 · ~6 |
| Jefe | 161–182 · muerto | 349–378 · derrota | 506–540 · muerto | 670–697 · muerto |

Conclusiones:
- **Todas las oleadas acaban al despejarse.** Quedan entre 5 y 30 s en el cronómetro y en ningún caso llega a cero.
- **Más enemigos que en niveles 1 a 3:** la media por oleada pasa de unas 3.5 a unas 6.3. Las oleadas pares (W2 y W4) son las más pobladas, con 8 a 10 enemigos.
- **Cronómetro:** la suma de ventana y tally da unos 18–19 s en W1 y 35–39 s en W5. Respecto al nivel 1 a 3, son unos 3 s más.
- **Tally:** cuenta atrás de unos 4 por segundo.
- **Jefe:** siguen llegando furgonetas normales durante la pelea. El jefe se mata con el disparo automático. No se puede contar cuántos golpes necesita.
- **Derrota:** solo en B, en el jefe. Un destello rojo a pantalla completa marca el golpe directo (376.8, 533.0 y 601.8 s).
- **Pausa del cronómetro:** 4.5 s congelados durante un golpe en C2 W2 (601.8–606.3 s). Solo se ha visto una vez; no está implementado.
- **Aviso de bomba:** un «!» rojo marca el punto de impacto antes de que caiga la bomba. Las bombas se lanzan desde el costado y desde lejos.

Consecuencias para la base (aplicadas):
- Cuota por oleada: niveles 1 a 3, `[3,4,4,3,4]` (uno menos en nivel 1). Niveles 4 y 5, `[6,9,5,8,5]`. Para niveles 6 o más no hay datos; se usa la de niveles 4 y 5.
- Cronómetro: `10 + 5·ola`, y 3 s más desde el nivel 4.
- Tally: cuenta atrás de unos 4 por segundo.
- Jefe: las furgonetas normales siguen llegando durante la pelea.

### 9.3 Conflictos sin resolver

- **«x2 Bonus»:** confirmado en la parte 1: aparece en 116–119 s y en 476–477 s («13 x2 Bonus», al final de la oleada de L3-A). El agente de la parte 2 no lo vio en seis momentos. El código sigue con ×2.
- **Esquive:** ni el agente de la parte 1 ni el de la parte 2 lo confirman. La parte 2 anota un posible cambio de lado en 4:32–4:34 de B W1, sin poder saber cuál de los dos coches se movió. El esquive se mantiene porque lo pediste, pero hay que confirmarlo en el vídeo.
- **Vida del taxi:** no se ve en el HUD. El daño por golpe de la base es provisional.
- **Dirección de lanzamiento:** la parte 2 confirma que las bombas caen delante del taxi. No se ha medido si el lanzamiento viene de detrás o del costado en cada caso.

---

## 10. Igualdad visual (revisión 3)

Medido sobre fotogramas de la parte 1 (720 × 1280) y sobre capturas de nuestra base (420 × 746). Las posiciones se dan como fracción de la altura o del ancho. Error de medida: ±0.01. Referencia limpia: fotograma 471 s (L3-A, oleada 3), con el taxi en el horizonte.

### 10.1 Medidas

| Elemento | Original | Nuestro | Diferencia |
|---|---|---|---|
| Horizonte (fin del cielo azul) | 0.445 de la altura | 0.429 | Cerca. Unos 12 px en nuestra escala. |
| Base del taxi (ruedas) | ~0.40, justo sobre el horizonte | 0.538, bajo el horizonte | **Nuestro taxi está unos 0.14 de pantalla más abajo.** |
| Ancho del taxi | 0.296 del ancho | 0.221 del ancho | **Nuestro taxi es un 34 % más pequeño.** |
| Posición lateral del taxi | Se mueve entre 0.50 y 0.85 | Centrado (0.50) | Nuestro taxi no se desplaza en la conducción normal. [?] |
| Ancho del enemigo frente al taxi | ~0.7 del taxi | ~0.7 del taxi | Coincide. |

### 10.2 Lo que no es igual

| # | Elemento | Original | Nuestro | Prioridad |
|---|---|---|---|---|
| V1 | Carretera | Suelo blanco con líneas de lápiz y arcos curvos. No hay bordillos. | Asfalto gris oscuro, bordillos y raya central recta. | Alta |
| V2 | Líneas de velocidad | Trazos radiales negros que cubren la carretera en tramos de velocidad. | Líneas finas y casi invisibles. | Alta |
| V3 | Dinamita | Se dibuja por encima del taxi cuando vuela. | Cuando viene de detrás (profundidad negativa) se dibuja antes que el coche, y el coche la tapa. Por eso se ve entera o solo un trozo. | **Alta (lo que señalas)** |
| V4 | Aviso de impacto | Triángulo rojo «!». | Elipse roja. | Media |
| V5 | Transición de fin de ola | Pantalla negra con un arco de luz azul y una silueta del taxi que entra. Luego la cuenta atrás y «x2 Bonus». | Pantalla negra con la cuenta atrás y un aviso encima («WEAPON: BOMB!»). **Falta el arco y la silueta.** Es el «túnel». | Alta |
| V6 | Banner de ola | Solo la etiqueta «WAVE N» arriba a la izquierda. | Banner grande «WAVE 1» y «BOSS WAVE!». | Media |
| V7 | Jefe | Camiones grandes (verde, azul, amarillo, gris-azul). Sin banner. Su vida aparece como barra verde sobre el propio vehículo. | Un bus marrón y un taxi. Barra de vida fija arriba y un toast «BOSS INCOMING!». | Alta (hay que dibujar los camiones) |
| V8 | Barra inferior izquierda | Estrella, «N Lv» y porcentaje de progreso (lo confirmé en las dos partes). | Icono de gato y «100 / 100» (vida). | Decisión tuya |
| V9 | Botón central | Icono de bomba con el número de bombas. | Un «!» gris. | Baja |
| V10 | Furgonetas de policía | Furgoneta blanca redondeada con luz en el techo. | Coche pequeño blanco y azul con cartel «POLICE». | Media |
| V11 | Cielo | Azul con nubes en los bancos de tema azul; blanco con edificios a lápiz en el de ciudad. | Gris con edificios. | Baja |
| V12 | Tamaño de las monedas y cajas | Monedas pequeñas, cajas verdes con «?». | Similar. | Baja |
| V13 | Humo de explosión | Nubes blancas grandes que tapan el coche. | Destellos pequeños. | Media |

### 10.3 Lo que sí coincide

- Los gatos en el parabrisas, con el coche de frente.
- Las etiquetas «WAVE» y «Level» arriba a la izquierda, el botón de pausa y el AUTO circular.
- El cronómetro grande arriba al centro.
- Las barras verdes de vida sobre los enemigos.
- Los corchetes naranjas sobre el enemigo bloqueado.

### 10.4 Decisiones que necesito de ti

1. **Carretera:** ¿la paso a suelo blanco con líneas de lápiz, como el original? Es el cambio visual más grande.
2. **Taxi:** para ponerlo a 0.40 de la altura (sobre el horizonte) y a 0.296 del ancho hay que cambiar la perspectiva. Los enemigos que vienen de detrás salen del horizonte, así que la banda de persecución cambia también.
3. **Dibujo de camiones del jefe:** hay que dibujarlos a mano en canvas. Es el trabajo de arte más grande.
4. **Barra inferior izquierda:** ¿la cambio a la barra de nivel del original, o mantengo la vida con gato?
5. **Transición de fin de ola:** ¿la hago como el arco y la silueta del original?

### 10.5 Estado tras implementar las decisiones

Aprobadas: 1 (carretera clara con líneas de lápiz que sigue leyéndose como carretera), 2 (taxi sobre el horizonte, con el tamaño del vídeo), 3 (camiones del jefe), 4 (barra de nivel como el original), 5 (transición de fin de ola con arco y silueta).

Hecho:
- **Taxi:** escala 0.92 (0.296 del ancho, como el original). La base está sobre el horizonte (0.45 de la altura). Los enemigos de detrás aparecen por encima del horizonte, en el cielo.
- **Carretera:** suelo claro, bordes a lápiz, marcas de carril grises y líneas radiales más densas en la conducción.
- **Enemigos:** furgoneta de policía blanca con luz en el techo, ambulancia con cruz roja y camiones del jefe por tipo (beige, azul, verde, amarillo con pala, gris-azul). El jefe aparece a un lado, no en el centro.
- **Dinamita:** se dibuja siempre por encima del taxi mientras vuela. El aviso de impacto es un triángulo rojo con «!».
- **Fin de ola:** pantalla negra con un arco de cielo azul que se abre, la silueta del taxi entrando y la cuenta atrás. Al final, «N x2 Bonus». Se oculta cualquier aviso que estuviera en pantalla.
- **HUD inferior izquierdo:** estrella, «N Lv», barra de progreso y porcentaje, como en el original. El progreso sube con las muertes (4 puntos, 30 en el jefe) y las monedas (1 punto). Cada nivel cuesta 60 + 20·nivel puntos. **Estos valores son provisionales**: el original no permite medirlos.
- **Vida:** como la barra inferior ya no es la vida, la vida se muestra con una barra verde sobre el taxi.
- **Banners:** se quitan «WAVE N» y «BOSS WAVE!» en el centro, la barra de jefe arriba y los avisos «BOSS INCOMING!» y «FINAL WAVE!». El original no los tiene.

No tocado (no aprobado): el botón central con «!» en vez del icono de bomba con su número (V9), el cielo de los bancos de ciudad (V11) y el humo de explosión (V13).

Pendiente de comprobar: si el jefe se ve bien en la pelea completa en el resto de temas, y si la barra de nivel debe tener valores parecidos a los del original.

### 10.6 Segunda ronda de pulido (prueba en móvil)

Tras la primera captura en un móvil:
- **Policía:** furgoneta vista de frente, como en el original (carrocería blanca redondeada, rejilla, faros y luz en el techo). La versión anterior se veía de lado y con ruedas grandes.
- **Dinamita:** sale a la altura del enemigo y sube más en el arco. Antes arrancaba casi a ras de suelo y el aviso triangular tapaba la vista.
- **Monedas:** unos 35 % más pequeñas, y el crecimiento de escala hacia la cámara es más suave. La moneda grande de la izquierda era un efecto de esa escala.
- **HUD inferior izquierdo:** sin solapamientos. El porcentaje ya no se pisa con el dial.
- **Transición:** un círculo de cielo se cierra sobre el taxi en 0.9 s, con el taxi en negro dentro; después va la cuenta atrás y «x2 Bonus».

Pendiente: las líneas radiales de la carretera siguen siendo finas y grises. El original usa trazos oscuros y densos. Si se quiere parecido, hay que rehacerlas como trazos afilados.
