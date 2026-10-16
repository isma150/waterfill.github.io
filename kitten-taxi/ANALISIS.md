# Kitten Taxi: análisis del juego

Fuente: dos vídeos de partida en vertical (parte 1: 12 min 53 s; parte 2: 12 min 12 s; 720×1280, 24 fps). El análisis se hizo con fotogramas muestreados (de 1 cada 2 s a 1 cada 15 s según el tramo) y con recortes a resolución completa para leer números y textos.

Cobertura: el material va desde la pantalla de título hasta la mitad del nivel 5 (la parte 2 termina en la tienda y el mapa). No aparecen créditos ni final, así que el final del juego no está documentado.

Convención de etiquetas:

- **[Obs]**: visto directamente en los vídeos.
- **[Inf]**: deducido de varias observaciones que cuadran entre sí.
- **[?]**: no determinado con este material.

---

## 1. Resumen

*Kitten Taxi* es un juego de móvil (vertical) de conducción y disparo automático con perspectiva pseudo-3D. Conduces un taxi con un gato al volante por una ciudad hacia un banco y eliminas a los coches que te persiguen (policías, furgonetas, sedanes) mientras robas dinero del banco. Cada banco se juega en **6 oleadas**; la sexta es un **jefe**. Entre bancos hay una rueda de premios tipo gacha, una tienda de mejoras y un mapa para elegir el siguiente banco.

Está hecho con un estilo de dibujo a lápiz (blanco y negro con acentos de color). La pantalla de título y los vídeos muestran "© Wonder People, 2014".

---

## 2. De principio a fin

| Fase | Qué ocurre | Tiempo en el vídeo (aprox.) |
|---|---|---|
| Título | Logo sobre una calle con un letrero de BANK. Botones de inicio de sesión: "GameCenter" y "Guest". | 0:00–0:11 [Obs] |
| Tutorial | Enseña en orden: "Drive!" (arrastre), "Dodge!" (esquivar proyectiles), "Auto attack when you go near an enemy", una caja "?" con arma, monedas ("get a Coin"), un disparo especial ("Good job! Eat this!") y la recompensa de tutorial (10 gemas). | 0:12–1:08 [Obs] |
| Mapa | Nodos de bancos con candados, popup con nombre, "Level" y "Balances". Pie: Back, monedas, gemas, llaves y Start. | 1:10 [Obs] |
| Consejo de carga | Pantalla de la calle BANK con un consejo antes de cada banco. | 1:24, y antes de cada nivel [Obs] |
| Nivel (banco) | Seis oleadas. La 6.ª es el jefe. | Nivel 1 empieza en 1:34 [Obs] |
| Fin de nivel | "LEVEL ↑" con una mejora ("Firing rate Up") y tabla de resultados. | Nivel 1 ≈ 2:55 [Obs] |
| Rueda SPIN | Gacha con monedas y gemas. | Tras cada nivel [Obs] |
| Tienda | Pestañas Car, Driver, Assist, Pet y Coin/Key/Jewelry. Mejoras de armas. | Tras cada nivel [Obs] |
| Mapa | Siguiente banco, con un nivel más alto. | Repetido [Obs] |
| Ajustes | Engranaje: contact, High Scores, Achievements, Sound Off, Official Facebook, Delete ID, copy ID. | Parte 2 [Obs] |

Cronología de los niveles, con anclas verificadas:

- Nivel 2 empieza hacia 4:35 (parte 1) [Obs].
- Nivel 3 empieza hacia 7:30 (parte 1, aprox.) [Obs].
- El jefe del nivel 3 aparece hacia 12:30 de la parte 1 y continúa al inicio de la parte 2 [Obs].
- Nivel 4 empieza hacia 1:10 de la parte 2 [Obs].
- Nivel 5 empieza hacia 6:30 de la parte 2 (aprox.) [Obs].
- La parte 2 termina con la tienda y el mapa tras el nivel 5 [Obs].

---

## 3. Pantallas y HUD (en partida)

| Elemento | Posición | Función |
|---|---|---|
| "WAVE n" / "Level n" | Arriba izquierda | Ola actual y nivel del banco [Obs] |
| Botón AUTO | Debajo, izquierda | Activa la conducción automática. Verde = activa. Texto en pantalla: "auto drive to touch off! touch to drive yourself!" [Obs] |
| Temporizador | Arriba centro | Cuenta atrás de la ola con 2 decimales [Obs] |
| Monedas de la partida | Centro, bajo el temporizador | Suma de lo robado y lo ganado en esta partida [Obs] |
| Pausa | Arriba derecha | [Obs] |
| Barra con icono de moneda y "Lv" | Abajo izquierda | Medidor con número que baja al recibir daño; [Inf] vida/carga del coche ("Loadage" en la tienda). Confirmado sólo por tendencia, [?] |
| Círculo con número | Abajo centro | Se pone verde con la conducción automática. Número 0, 2 o 3. [?] (probablemente munición o bombas) |

---

## 4. Conducción y control

- **Dirección**: arrastre horizontal. La pantalla "Drive!" muestra una flecha izquierda-derecha con un dedo [Obs].
- **Conducción automática**: el botón AUTO la activa y tocar la pantalla la apaga [Obs].
- **Apuntado**: el jugador no apunta. El disparo es automático cuando un enemigo entra en rango ("Auto attack when you go near an enemy") [Obs]. Los corchetes naranjas marcan al enemigo bloqueado [Obs].
- **Esquivar**: los enemigos disparan proyectiles rojos y hay obstáculos en carretera. Un triángulo rojo "!" avisa de un peligro en un carril [Obs].
- **Bomba**: el tutorial lanza un disparo especial, pero el control exacto de la bomba no se ve claramente. [?]

---

## 5. Armas y mejoras

- **Armas** en la pantalla de mejoras: Pistol, BOMB, Shot (escopeta) y Machine (ametralladora). Hay casillas con candado para las que faltan [Obs].
- **Estadísticas** visibles: "Power" y "shoot / 1 sec" [Obs].
- **Costes de mejora** observados: 500, 1000 y 1200 monedas [Obs].
- **Cajas "?"**: aparecen en la carretera y dan un arma o un premio temporal ("get a weapons") [Obs]. El efecto exacto de cada caja [?].
- **Clay bomb** (bomba de arcilla verde): frena el coche [Obs, consejo de carga].
- **Escopeta y granadas**: alcanzan a varios enemigos a la vez [Obs, consejo de carga].
- **Cadencia**: la mejora de fin de nivel "Firing rate Up" aumenta la velocidad de disparo [Obs].

---

## 6. Enemigos, peligros y objetos

| Elemento | Aspecto | Comportamiento observado |
|---|---|---|
| Policía | Coche azul y blanco con luces, etiquetado "Police" | Dispara proyectiles rojos hacia el taxi [Obs] |
| Sedán | Coche azul que aparece a partir del nivel 1–2 | Se acerca en carril; si choca, daña [Inf] |
| Furgoneta / camión blanco | Vehículo grande con barra de vida verde | Resiste varios impactos [Obs] |
| Jefe | Camión grande con barra verde superior. Azul en el nivel 3, amarillo tipo buldócer en los niveles 4–5 | Aparece en la ola 6 tras una pantalla "BOSS" [Obs] |
| Bala / proyectil | Cápsula roja que avanza hacia el taxi | Hay que esquivarla [Obs] |
| Botella roja | Objeto en carretera | Obstáculo [Obs] |
| Contenedor verde | Obstáculo en carretera | Obstáculo [Obs] |
| Caja de madera con "?" | Recogible en carretera | Da un arma o un premio [Obs] |
| Monedas amarillas | Aparecen al destruir enemigos y en carretera | Se recogen al pasar por encima [Obs] |
| Gema azul | Recogible en carretera | Gema de cambio [Obs] |
| Llave dorada | Consejo: "si usas la llave dorada… el coche dorado aparece en la partida" | Coche dorado durante la partida [Obs] |
| Túnel | Pantalla negra con cuenta atrás y texto "You will have double coins when you get all the coins from the tunnel!" | Doble de monedas si recoges todas [Obs] |

---

## 7. Oleadas, temporizador y jefe

- **6 oleadas por banco**. La 6.ª es el jefe [Obs].
- **Temporizador de ola**: cuenta atrás con 2 decimales. Baja 1 segundo por cada segundo real. Verificado con muestreo a 1 fotograma por segundo (18.86 → 17.86; 24.6 → 19.6) [Obs].
- **Valores iniciales observados**: entre unos 20 y 35 segundos [Obs].
- **Fin de ola con los enemigos derrotados**: pantalla negra con cuenta atrás del tiempo restante (17 → 11 → 4 → 0) y texto "N x 2 Bonus" [Obs].
- **Fórmula del bonus**: tiempo sobrante × 2 [Inf]. Hay un caso verificado: una ola con 3 segundos sobrantes mostró "3 x 2 Bonus".
- **Hipótesis sobre el fin de ola**: se termina antes del tiempo cuando se derrotan todos los enemigos. [Inf] (no está confirmado qué pasa si el tiempo llega a 0 con enemigos vivos).
- **Jefe**: antes de la ola 6 aparece una pantalla negra con "BOSS" y destellos radiales [Obs]. El jefe tiene barra de vida verde [Obs]. Si dispara, [?].
- **Derrota del jefe**: "LEVEL ↑" y una mejora, después la tabla de resultados [Obs].
- **Muerte**: popup "Continue" con coste de 1 gema, o "Give up" [Obs].

---

## 8. Economía

**Contadores.** El contador central es el dinero de la partida. La cartera (abajo) muestra monedas, gemas y llaves [Obs].

**Resultados de fin de nivel.** Hay cuatro líneas: "Coins stolen from bank", "Earn money by destroying", "Per-Fect Bonus (0/-)" y "Total" [Obs].

- La suma de robado + destruyendo coincide con el contador central. Ejemplo: 138 + 192 = 330, y el contador marcaba 330 en el jefe [Obs].
- En todos los resultados vistos, el bonus perfecto sale en 0. Su criterio exacto [?].

**Saldo del banco ("Balances").** Lo que se roba baja el saldo del banco. Tres casos cuadran [Obs + Inf]:

| Banco | Saldo antes | Robado | Saldo después (visto en el mapa) |
|---|---|---|---|
| Nivel 2 | 150 | 138 | 12 |
| Nivel 4 | 250 | 146 | 104 |
| Nivel 3 | 200 | 110 | 90 (nivel 4) |

El número "Level" del banco sube cada vez que lo robas [Obs].

**Pista del mapa**: "Make previous bank balance to 0" [Obs]. Si vaciar el banco anterior es requisito para desbloquear el siguiente, no está comprobado: el banco de nivel 2 quedó con 12 y el siguiente apareció disponible igualmente [?].

**Rueda SPIN.** El precio sube: 500, después 730 o 750, luego 1000 monedas [Obs]. Premios vistos: monedas (5, 10, 20, 50, 100, 500…), gemas y piezas de coche o arma [Obs].

**Precios vistos en la tienda** [Obs]:

| Ítem | Precio |
|---|---|
| Mejora de arma (nivel bajo) | 500 monedas |
| Mejora de arma (nivel medio) | 1000 monedas |
| Mejora de arma (nivel alto) | 1200 monedas |
| Coche "Shoot quickly" | 40 000 monedas |
| Coche con imán / bloqueo | 90 o 130 gemas |
| Asistente "Loadage +" | 5000 monedas |
| Asistente "Bomb Power +" | 9000 monedas |
| Mascota "extra coin +1" | 6000 monedas |
| Asistente "Shotgun speed +" | 30 gemas |

**Gemas.** Sirven para continuar tras morir y para comprar algunos coches y mejoras. Salen de recompensas (tutorial, rueda, recogibles). Probablemente se compran con dinero real [Inf]; no se replica aquí.

**Llaves.** Hay cuatro huecos con iconos de llave y un "+" para comprar [Obs]. Su uso exacto [?]. Hay una cuenta atrás m:ss junto a las llaves en la tienda y el mapa (por ejemplo 4:31 o 1:18) [Obs]. Probablemente es un tiempo de regeneración, pero no está comprobado [?].

**Categorías de la tienda** [Obs]: Car, Driver, Assist, Pet, Coin/Key/Jewelry. Solo se ven en detalle Car, Assist y Pet. La pestaña Driver y Coin/Key/Jewelry [?].

---

## 9. Progresión y bancos

- **Mapa**: un camino amarillo une los bancos. Los bloqueados llevan candado. Hay una zona "Ranking Stage" que no se explora en el vídeo [Obs].
- **Nombres de los bancos**: son nombres de personas reales (multimillonarios). **No se reproducen en la versión HTML.**
- **Saldos iniciales vistos**: 100 (nivel 1), 150 (nivel 2), 200 (nivel 3), 250 (nivel 4) [Obs].
- **Fondo por nivel**: nivel 1 calle gris y blanca; nivel 2 cielo azul; nivel 3 cielo azul con montañas; nivel 4 atardecer rosa-amarillo; nivel 5 cielo azul con montañas [Obs].
- **Consejos de carga** (textos literales en inglés del juego):
  1. "If you use the golden key while playing. The golden car shows up on your game play."
  2. "Green clay bomb is to slow down my car."
  3. "Upgrade a weapon to clear stages easily."
  4. "Grenades and shotguns are the weapons that can strike around."

---

## 10. Elementos externos (no replicados)

- Compra de gemas con dinero real.
- Popup pidiendo una reseña ("Will you please write a review?") con recompensa, y botón RATE.
- Inicio de sesión con GameCenter e identificador de invitado; Delete ID y copy ID.
- Enlace a Facebook y buzón de mensajes.
- Clasificaciones ("High Scores") y logros ("Achievements"): se ven en el menú, sin contenido verificado.

---

## 11. Lo que no se ve en el material

- Final del juego, créditos y niveles 6 en adelante.
- Criterio del bonus perfecto y de la mejora de fin de nivel (¿siempre cadencia o aleatoria?).
- Qué pasa al llegar el tiempo a 0 con enemigos vivos.
- Uso de las llaves y de la cuenta atrás.
- Efecto exacto del coche dorado (¿monedas ×2, invulnerabilidad?).
- Pestañas Driver y Coin/Key/Jewelry.
- Medidor inferior izquierdo y círculo inferior central (ver sección 3).

---

## 12. Versión HTML: qué incluye y qué cambia

Archivos: `kitten-taxi/index.html` más cinco scripts en `kitten-taxi/js/` (`art.js`, `state.js`, `game.js`, `ui.js`, `main.js`). Sin dependencias salvo la fuente de Google Fonts. Todo se dibuja en un único canvas 2D y escala a cualquier pantalla con proporción de móvil.

| Original | Versión HTML |
|---|---|
| Arte a lápiz de los vídeos | Dibujado en código, sin copiar sprites ni fotogramas |
| Nombres reales de los bancos | Nombres ficticios: Lunar, Mirador, del Puerto, Solano, Ceniza, Estrella |
| 3 tipos de enemigo y varios jefes | Policía, sedán, furgoneta y un jefe por nivel |
| 4 armas y muchas mejoras | Pistola, escopeta, ametralladora y bomba, con mejora de nivel |
| Gacha con muchos premios | Rueda con 8 premios; coste 500 monedas (sube 225 por giro, máximo 1500) |
| Tienda con gemas | Solo monedas. Las gemas se usan para continuar y salen de premios |
| Llaves con cuenta atrás | Sin cuenta atrás. Llave dorada = coche dorado en la siguiente partida |
| Sonido | Sin sonido en esta versión |
| Progreso en servidor | Progreso en `localStorage` (con try/catch) |

**Reglas de diseño que he elegido (no observadas en el original):**

- El robo: las monedas de carretera restan del saldo del banco y no pueden superarlo. Las monedas de enemigos cuentan como "ganado destruyendo".
- Bonus perfecto: +20 % del total si el saldo llega a 0 al terminar.
- Mejora al derrotar al jefe: aleatoria entre cadencia, blindaje o imán, válida solo en esa partida.
- Recuperación de 12 de vida al empezar cada ola.
- Un banco se desbloquea al completar (vencer al jefe) el anterior.
- El nivel del banco sube en cada visita, así que aumenta la dificultad.

**Controles**

- Móvil: arrastra para conducir; toca AUTO para la conducción automática (tocar la pantalla la apaga); el botón circular central lanza una bomba.
- Teclado: flechas izquierda/derecha para conducir; **A** conmuta AUTO; **espacio** bomba; **P** o **Esc** pausa.

**Pruebas realizadas** (navegador headless, 390×844):

- Menú, mapa, rueda (giro y premio), tienda (compra de mejora), arrastre manual, pausa y reanudación.
- Recorrido completo: olas 1–5, jefe en la ola 6, "LEVEL ↑", resultados, bonus y vuelta al mapa con el banco siguiente desbloqueado.
- Derrota sin gemas: el botón de reintentar queda deshabilitado; "Rendirse" lleva a "Fin del robo" y el banco siguiente sigue bloqueado.
- Consola: 0 errores en todas las pruebas.

**Límites**: no probado en un móvil real ni con audio; el equilibrio (dificultad, economía) es un primer ajuste y necesita partidas humanas.

---

## 13. Cómo se trabajó

1. Muestreo de los vídeos: contact sheets de 15 s para la visión general; 2 s para el tutorial; 1 s con recorte del HUD para verificar el temporizador; 5 s para el nivel 1; 8 s para el resto.
2. Notas de tiempos y hechos en un archivo de trabajo, con cada dato etiquetado como observado, inferido o no determinado.
3. Revisión del plan con un segundo modelo antes de escribir el juego.
4. Implementación y pruebas automáticas con Playwright (Chromium) sobre la versión final.

---

## 14. Cámara y HUD (versión 2)

La primera versión colocaba el coche abajo y el horizonte arriba. Está invertido respecto al original. Esta sección recoge la geometría verificada con tiras a 10 fps del tramo de combate (parte 1, 296 s).

**Cámara**
- El coche está en la franja alta de la pantalla, de cara a la cámara. Sus ruedas están en la línea del horizonte (≈ 44 % de la altura).
- La carretera queda bajo el horizonte y se abre hacia abajo. Los carriles son arcos curvos.
- Los objetos (enemigos, botellas, monedas, cajas) salen de la parte inferior y suben hacia el coche, encogiéndose al alejarse de la cámara. La botella roja sube por el lateral y pasa al nivel del coche [Obs].
- Los enemigos se aparcan a los lados del coche, a su misma altura, y disparan desde ahí [Obs: la policía del tutorial].
- Las burbujas del tutorial congelan la escena: no se mueve nada mientras hay burbuja [Obs].

**HUD (fracciones de la pantalla 390 × 844)**
- Arriba izquierda: etiqueta "WAVE n" en gris pequeño, "Level n" debajo, y el botón AUTO con anillo verde cuando está activo (≈ 0.135 W, 0.13 H).
- Arriba centro: temporizador con enteros grandes y decimales pequeños (≈ 0.6 W, 0.075 H).
- Bajo el horizonte, a la izquierda del centro: monedas de la partida (≈ 0.45 W, 0.545 H). No están bajo el temporizador.
- Arriba derecha: pausa.
- Abajo izquierda: icono de moneda, barra, número y "Lv".
- Abajo centro: dial circular con el icono de bomba y el contador. Se pone verde con la conducción automática.

**Limitaciones de la versión 2**
- El arte es procedural y está dibujado a mano con líneas de lápiz simuladas. No reproduce los trazos del original, que son dibujos a mano escaneados.
- Mapa, carretera y fondos son versiones simplificadas. La textura del papel es un grano uniforme.
- Sin sonido.

### 14.1 Combate (versión 3)

- **Bombas desde detrás:** los enemigos que pasan por los lados del coche se quedan detrás de él y lanzan bombas en arco que vienen de atrás hacia delante. La bomba cae sobre el sitio donde estabas al lanzarla, y aparece un círculo de aviso en el suelo. Hay que apartarse [Inf: tomado del comportamiento de la bomba en el original y del brief de la versión 3].
- **Arrastre:** funciona durante las burbujas del tutorial. La burbuja congela el mundo, pero el coche sigue respondiendo.
- **Combo:** tres o más eliminaciones seguidas en 2,5 s muestran "COMBO xN".
- **Impactos:** chispas al golpear, monedas que vuelan al contador al eliminar un enemigo y temblor de pantalla con cada explosión.
- **Automático:** esquiva las bombas que caen cerca del coche.
