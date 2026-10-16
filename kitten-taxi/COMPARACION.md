# Kitten Taxi: comparación con el original y lista de fallos y faltas

Base revisada: `index.html` (Trayectorias v2 corregida, commit 85e7d04 y siguientes).
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
| R1 | Los bancos llevan nombres de personas reales (Bernard Arnault, S. Robson Walton, Alice Walton, Stefan Persson, Liliane Bettencourt) y el juego permite robarles. | [Cód] líneas `name:'…'` del array `BANKS` | Sustituir por nombres ficticios. Ya está publicado en la versión 4. |

---

## 3. Fallos (lo que existe pero funciona mal o no tiene efecto)

| # | Gravedad | Fallo | Evidencia | Original |
|---|---|---|---|---|
| F1 | Alta | **Las llaves no tienen función.** Se muestran como `k/4` en el mapa, pero nunca se ganan ni se gastan. | [Cód] `save.keys` solo se lee para mostrarlo. | [Obs] Las llaves son un recurso con "+" para comprar y tienen un temporizador m:ss junto a ellas. Su uso exacto no está claro. |
| F2 | Alta | **El saldo del banco no baja** con lo robado y no se guarda entre visitas. | [Cód] `BANKS` es constante; `missionVictory` no escribe el saldo. | [Obs] Saldo 150 → robado 138 → la siguiente visita muestra 12. Saldo 250 → robado 146 → 104. |
| F3 | Alta | **El nivel del banco no sube** al volver. Todos los bancos están fijos. | [Cód] `level:b.level` nunca cambia. | [Obs] El nivel sube cada visita: Level 2 → 3 → 4. |
| F4 | Alta | **Las oleadas duran ~11 s** y el temporizador **cuenta hacia arriba**. | [Cód] `waveDuration:10.7+b.level*.35`; `m.seconds` crece. | [Obs] 20–35 s por ola, con cuenta atrás de 2 decimales (18.86 → 17.86). |
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
