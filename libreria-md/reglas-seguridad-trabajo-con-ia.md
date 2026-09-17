# Cinco reglas de seguridad para trabajar con IA

Estas reglas forman un marco sencillo y memorable para trabajar con inteligencia artificial sin dejar que la inferencia, la sobreoptimización, la prisa, el código o los datos externos, o un problema más grande de lo previsto, nos metan por caminos que no queremos.

Las 5 no son una lista suelta: siguen el orden natural de cualquier trabajo — **qué hacer con los huecos de la especificación (1) → qué tamaño le doy a la solución (2) → qué entra desde fuera (3) → si de verdad conozco lo que tengo delante antes de actuar (4) → y si a mitad de camino descubro que el problema era más grande de lo que pensaba, decirlo de inmediato (5)**.

Ninguna de las 5 es infalible por sí sola. Reducen el espacio de error; no lo eliminan. Al final de cada una se anota, con honestidad, dónde sigue teniendo grietas.

---

## El test de reversibilidad (concepto compartido por las Reglas 1 y 4)

Antes de decidir si algo se pregunta o se decide solo, y antes de actuar, se aplica la misma pregunta:

> **¿Deshacer esto es gratis y rápido, o cuesta caro, tiempo o confianza recuperarlo?**

- **Reversible y barato de deshacer** → el listón de certeza puede ser más bajo.
- **No reversible, o costoso de deshacer** → el listón sube: no basta con "parece razonable", hace falta certeza real o aprobación explícita.

Este test se define una sola vez aquí porque aparece en dos momentos distintos del trabajo: al decidir si se puede rellenar un hueco de información (Regla 1) y al decidir si se puede actuar ya o hace falta más certeza (Regla 4).

---

## 1. Regla Jurassic Park

### Idea
Si falta una parte de la especificación, no se rellena por cuenta propia cuando lo que falta es un hecho, un dato o una decisión que compromete el resultado.

### ¿Por qué este nombre?
En la película, resucitan dinosaurios rellenando los huecos del ADN incompleto con genes de rana — y ese relleno "razonable" es exactamente lo que sale mal.

### Regla
Distingue siempre entre dos tipos de hueco:

- **Hecho, dato, cita, cifra, alcance o decisión que aplica el test de reversibilidad como "no reversible"** → nunca se infiere. Se pregunta antes de continuar, diciendo qué falta, qué se inferiría si se aprobara, y por qué.
- **Detalle de ejecución reversible** (estilo, formato, nombres, redacción, orden visual) → se decide sin preguntar, pero **se informa** de la decisión tomada, para que se pueda corregir sin coste si no gusta.

Ante la duda de en qué categoría cae algo, trátalo como del primer tipo y pregunta. Es más barato preguntar de más que deshacer una cadena de decisiones construida sobre un supuesto no confirmado.

### Frase corta
**No rellenes ADN crítico con rana. Los detalles del parque, decóralos tú — pero avisa qué has puesto.**

### Qué evita
- decisiones inventadas;
- arquitectura basada en supuestos;
- comportamientos no pedidos;
- desviaciones que aparecen varios pasos después;
- trabajo construido sobre información que nunca fue confirmada;
- y, al mismo tiempo, la fricción de preguntar por cada micro-decisión sin importancia.

### Dónde tiene grietas
Distinguir "hecho crítico" de "detalle de ejecución" exige criterio, y ese criterio puede fallar — la propia regla no puede trazar esa línea por ti en cada caso. Ante la duda, la regla obliga a preguntar, lo cual reduce el riesgo pero no lo hace desaparecer.

---

## 2. Regla de las Termópilas

### Idea
No emplees más recursos, capas, herramientas ni complejidad de los necesarios para el objetivo — y esto aplica tanto a la arquitectura técnica como al alcance del propio proyecto.

### ¿Por qué este nombre?
300 espartanos defendieron un paso tan estrecho que un ejército enorme no podía desplegar su tamaño — la fuerza de más no sirve si el problema no la necesita.

### Regla
Si una solución simple cubre el problema, no añadas arquitectura, dependencias, automatizaciones, agentes, comprobaciones o capas extra "por si acaso". Una tarea hace una cosa, no varias a la vez "ya que estamos". Antes de escalar la solución o el alcance, demuestra que la versión más pequeña es insuficiente.

**Con prisa:** se recorta el alcance (menos funciones, menos objetivos a la vez), nunca se recorta el rigor (verificación, pruebas, las otras cuatro reglas). Ir rápido nunca es excusa para saltarse una comprobación — es excusa para hacer menos cosas, bien hechas.

### Frase corta
**No metas al ejército persa en un paso estrecho.**

### Qué evita
- sobreoptimización;
- soluciones y proyectos sobredimensionados;
- dependencias innecesarias;
- arquitecturas demasiado complejas;
- que la prisa se convierta en excusa para bajar la guardia en vez de para hacer menos cosas.

### Dónde tiene grietas
"Demostrar que la versión pequeña es insuficiente" también exige criterio: sin un caso de prueba real contra el que medir, "insuficiente" puede convertirse en una opinión disfrazada de conclusión técnica.

---

## 3. Regla del Caballo de Troya

### Idea
No incorpores al proyecto nada externo —código, dependencias, datos, fuentes de información, afirmaciones de terceros— sin verificación proporcional a lo que hay en juego si resulta falso.

### ¿Por qué este nombre?
Los troyanos metieron dentro de su ciudad algo que parecía un regalo, sin comprobar qué llevaba dentro de verdad.

### Regla
1. Antes de integrar algo externo: identifica de dónde viene, qué dice o qué hace, y qué pasa si resulta erróneo.
2. **El nivel de verificación es proporcional al riesgo**, no siempre el máximo posible: un dato de contexto menor se puede usar marcado como "sin verificar, fuente X" y seguir; algo de lo que depende una decisión importante no se usa hasta que la verificación sea real.
3. **La verificación se documenta con su método y su fecha**, no solo como una etiqueta "✓ verificado". Un "✓" sin decir cómo se comprobó es indistinguible de una suposición con más confianza de la que merece.
4. Cuando la verificación es imposible en el momento, no se trata como "verificado a medias": se marca explícitamente como **no verificable**, y se dice qué se necesitaría para verificarlo si algún día se puede.

### Frase corta
**No metas dentro de la ciudad algo que no sabes quién ha construido — y aunque lo sepas, apunta cómo lo comprobaste.**

### Qué evita
- código y datos inseguros o falsos;
- dependencias dudosas;
- comportamiento oculto;
- afirmaciones que se dan por buenas solo porque "suenan razonables";
- verificaciones superficiales disfrazadas de certeza absoluta.

### Dónde tiene grietas
La verificación misma puede fallar: una fuente puede estar desactualizada, un método de comprobación puede tener puntos ciegos, o quien verifica puede cometer el mismo error que la regla intenta evitar. Esta regla reduce el riesgo, no lo elimina. Tampoco cubre la manipulación deliberada — una fuente que parece fiable pero está diseñada para engañar necesitaría una sexta cautela distinta, que queda fuera de estas 5.

---

## 4. Regla de Gallipoli

### Idea
No actúes con un plan que da por sentado lo que tienes delante — el objetivo declarado no vale nada si el terreno real, el problema real o la complejidad real no se han comprobado antes de lanzar la operación.

### ¿Por qué este nombre?
Los Aliados desembarcaron en 1915 dando por hecho que conocían el terreno y la fuerza del enemigo. La mala información y la falta de reconocimiento previo costaron una de las derrotas más caras de la Primera Guerra Mundial: tenían un objetivo claro y una orden clara, y aun así se equivocaron por no conocer de verdad lo que tenían delante.

### Regla
1. Antes de actuar, ten claro no solo *qué* objetivo persigues, sino si de verdad conoces lo que vas a encontrar: la complejidad real del problema, no la que se supone desde fuera. Si no lo sabes con precisión, no actúes todavía.
2. Aplica el **test de reversibilidad**: si la acción no es reversible o es costosa de deshacer, el listón de certeza sobre "conozco de verdad lo que tengo delante" sube todavía más — no basta con "creo que es lo correcto".
3. **El objetivo declarado antes de actuar no es prueba de nada por sí solo.** Después de actuar, se confirma que el resultado real coincide con lo esperado — no se da por bueno solo porque el plan sonaba razonable sobre el papel.

### Frase corta
**No desembarques sin conocer al enemigo.**

### Qué evita
- planes que asumen un problema más simple del que es en realidad;
- confiar en la inteligencia de partida sin comprobarla sobre el terreno;
- pérdidas (tiempo, trabajo, confianza) que se podrían haber evitado con un reconocimiento previo;
- planes que se dan por cumplidos sin comprobar el resultado real.

### Dónde tiene grietas
A veces no hay forma de "conocer el terreno" del todo sin desembarcar primero — hay problemas que solo se revelan actuando, y esta regla no distingue bien ese caso: puede paralizar la exploración legítima donde actuar con incertidumbre es el método correcto (prototipos, pruebas de descarte). Reduce el riesgo de sobreconfianza, pero no elimina la incertidumbre real de enfrentarse a algo nuevo. Y "comprobar el resultado real" exige que exista una forma objetiva de comparar; en decisiones subjetivas, esa comprobación vuelve a depender del criterio humano.

---

## 5. Regla del Tiburón (Jaws)

### Idea
Cuando en mitad del trabajo se descubre que el problema es más grande, más complejo o más arriesgado de lo que se pensaba al empezar, se dice de inmediato — no se sigue remando con el plan original esperando que alcance.

### ¿Por qué este nombre?
Brody sale al mar pensando que el barco que llevan basta para el trabajo. Cuando ve al tiburón de cerca, entiende que se han quedado cortos — y lo dice en voz alta en vez de seguir remando con lo que tienen: "vamos a necesitar un barco más grande".

### Regla
En cuanto se detecte que el enfoque, el alcance o los recursos con los que se empezó no van a bastar —un error que revela más problema del esperado, una inferencia que se coló sin querer, un resultado que no cuadra, una tarea que resulta mucho más compleja de lo estimado— se declara explícitamente, sin suavizarlo y sin intentar arreglarlo en silencio con el mismo enfoque que ya no alcanza. Se dice qué se ha descubierto, por qué cambia la situación, y qué hace falta ahora: más tiempo, más alcance, otra vía, o aprobación de nuevo.

### Frase corta
**Vamos a necesitar un barco más grande.**

### Qué evita
- seguir remando con un plan que ya se sabe insuficiente;
- minimizar o esconder que el problema es mayor de lo estimado al principio;
- descubrirlo demasiado tarde, cuando ya no queda margen para cambiar de barco;
- fallos acumulados por no parar a tiempo a decirlo.

### Dónde tiene grietas
Hace falta darse cuenta primero — si el problema no se detecta, la regla no se activa sola, no sustituye estar atento. Y, como a Brody, admitirlo delante de todos cuesta: la regla exige valentía para decirlo, no solo saberlo.

Un fallo declarado a tiempo es barato de corregir. Un fallo escondido, aunque sea con buena intención, es mucho más caro cuando aparece — porque para entonces ya hay trabajo construido encima.

---

## Resumen

**Jurassic Park** → No inventes lo que falta; lo importante se pregunta, lo reversible se decide y se avisa.

**Termópilas** → No sobredimensiones la solución ni el proyecto; con prisa, recorta alcance, no rigor.

**Caballo de Troya** → No integres nada externo sin verificarlo en proporción a lo que arriesgas, y deja constancia de cómo lo comprobaste.

**Gallipoli** → No actúes dando por hecho que conoces el problema; comprueba el terreno real antes de comprometerte, y el resultado real después.

**Tiburón (Jaws)** → Si el problema resulta más grande de lo esperado, se dice de inmediato: hace falta un barco más grande.

---

## Principio común

Las cinco reglas, en orden, son las cinco fases de cualquier trabajo: **qué hago con los huecos → qué tamaño le doy a la solución → qué dejo entrar desde fuera → si de verdad conozco el problema antes de actuar → y si a mitad de camino resulta más grande, decirlo**. Buscan lo mismo:

> **Reducir el espacio de error antes de ejecutar — y declarar con honestidad cuando el problema resulta más grande de lo previsto.**

La IA puede inferir, proponer, optimizar y acelerar muchísimo el trabajo, pero cuanto más crítico sea el cambio, menos espacio debe existir para decisiones no confirmadas. Ninguna de estas reglas es infalible: cada una reduce un tipo de riesgo concreto, ninguna lo elimina del todo, y sus propios límites quedan anotados a propósito en vez de escondidos — por la misma razón que existe la Regla del Tiburón.

La prioridad no es parecer inteligente ni hacer más cosas.

La prioridad es trabajar con criterio, trazabilidad y fiabilidad.
