# REESCRITURA DE LOS DOCUMENTOS DE CÁSCARA FOUNDERS — v2

Estos documentos los lee el founder, no el equipo. Esa persona está en un proceso de
aprendizaje y de construcción de su negocio. Nos contratan para ser directos, y lo
somos: decimos el cuello de botella con nombre y apellido. Y lo decimos con respeto.

## LA REGLA DE REDACCIÓN QUE MANDA

**Nunca definas por la negativa.** Prohibido el patrón "no es X, es Y", "más que X es Y",
"el problema no es X". Decí directamente lo que es.

Mal: «No es conocimiento: le baja marketing a cinco infoproductores. No es producción:
tiene equipo. Es que nunca se puso el objetivo...»
Bien: «Sabe bajarle la estrategia a cinco infoproductores y tiene equipo para producir.
Lo que falta es el objetivo: que su marca personal sostenga una oferta propia.»

## SIN IRONÍA

Nada que suene a "sabés un montón para los demás y nada para vos". El titular de Aaron
decía «Le baja el marketing a cinco infoproductores y no se lo sabe bajar a sí mismo»:
eso es una chicana. Se cambia por algo que nombre el trabajo del tramo.
Los titulares describen el trabajo que viene, no el defecto de la persona.

## UBICAR AL FOUNDER EN SU ETAPA

Cada uno está en un momento distinto y el documento tiene que decirlo. Aaron recién
empieza: su documento le sirve a medida que avance esta primera etapa, con la llamada de
Franco y la de Facu ya hechas, y baja el objetivo del mes que viene. Otros están cerrando.
El proceso se repite: se marca un estado y desde ahí se evoluciona.

## VOZ

Español rioplatense, prosa, directo, adulto. Frases cortas. Sin tono aspiracional en el
cuerpo del documento. Prohibidas: "productivizar", "apalancar", "sinergia", "potenciar",
"llevar al siguiente nivel", "desbloquear tu potencial". Nada inventado: si un dato no
está, va "(falta confirmar)". Un solo cuello de botella por caso. Cáscara diseña y baja
la estrategia; el founder ejecuta. Los guiones los escribe el founder: Cáscara deja el
criterio y un ejemplo.

## EL ESQUEMA NUEVO

Claves, en este orden exacto:

`slug`, `cliente`, `proyecto`, `modo` ("cierre"|"radiografia"), `orientacion`, `arranque`,
`etapa`, `metrica`, `titular`, `bajada`, `punto_a`, `recorrido`, `lectura`, `respuestas`,
`entregables`, `punto_b`, `roadmap`, `accionables`, `conclusion`, `carta`, `abierto`

Lo que cambia respecto de la versión anterior:

**`etapa`** (nuevo, string): una frase que ubica al founder en el proceso. Ejemplo:
"Arranca el segundo mes: la oferta está definida y todavía no salió a probarse."

**`recorrido`** (reemplaza `que_paso`): deja de ser un repaso cronológico y pasa a ser una
**lectura de lo que pasó**. Forma:
```
{"titulo": "...", "texto": "prosa, 5 a 8 frases: qué se movió en estos días y qué significa",
 "hitos": [{"cuando": "17 jul", "que": "una línea, seis a doce palabras"}]}
```
Los hitos son referencia rápida, cortos y en minúscula. El texto es lo que el founder
realmente lee: qué cambió, qué quedó probado, qué se descartó.

**`respuestas`** (reemplaza `paquete`): los temas que quedaron **con una respuesta**
después de estas semanas. Forma: `[{"tema": "...", "respuesta": "una o dos frases"}]`.
Entre 5 y 9. Son conclusiones, decisiones tomadas y criterios que ya están definidos.
NO son entregables. "Documentar en lugar de crear" es una respuesta, no algo que se entrega.

**`entregables`** (nuevo): lo que Cáscara efectivamente le da o le va a dar: un formulario
para completar, un one-pager con la estructura, un módulo, una estrategia escrita, un
calendario, una plantilla. Forma: `[{"que": "...", "para": "qué hace el founder con eso"}]`.
Entre 2 y 5. Si algo lo completa el founder (como el pasaporte digital), se escribe así:
que = "El formulario del pasaporte digital", para = "Lo completa él y de ahí salen los
ángulos". Nunca digas que entregamos algo que en realidad es el founder quien lo llena.

**`conclusion`** (nuevo, string): la conclusión estratégica. Con todas las respuestas
arriba de la mesa, hacia dónde se direcciona el negocio. 4 a 6 frases, sin tono
aspiracional, concreta.

**`carta`** (reemplaza `cierre`, string): lo único del documento que puede levantar la
mirada. Se lee como una carta corta del mentor al founder: qué logró, qué lo espera, qué
lo va a hacer llegar. 4 a 7 frases. Cálida y cierta, sin promesas de resultado.
Se renderiza en cursiva.

El resto de las claves conservan su forma actual:
`punto_a` (3 bloques con label/titulo/texto), `lectura` (titular/texto/cita/cita_autor),
`punto_b` (2 bloques con fecha/titulo/texto), `roadmap` (4 a 7 pasos con
cuando/objetivo/entregable/quien), `accionables` (bloques con cuando/cliente[]/cascara[]),
`abierto` (string).
