# 30 · El mapa del cerebro, antes de pasarlo a n8n

> 26 de septiembre de 2026 · Paso 1 del plan "Plan para Facu · el cerebro en n8n" (Notion, Portal de clientes · Founders).
> Fuentes: el prompt que corre hoy (`sistema/23-prompt-agente-cascara.md` del Project), `agente/prompt-agente.md`, `CLAUDE.md`, `sistema/15-rol-lider-founders.md`, `sistema/20-tareas-programadas.md` y la última semana de la bitácora (`sistema/04-bitacora-automatizacion.md`, del 18 al 25/9). Las tablas de destino salen de la página "App · pantallas, datos y prompts de Lovable", sección Los datos. Suma lo que se decidió en la reunión de Facu con Teo del 26/9 (`sistema/27-reunion-teo-2026-09-26.md` del Project).

## Antes de leer: qué prompt corre de verdad

El agente que corre hoy es **"Cáscara Founders — el día y el pulso"**, de lunes a viernes a las 9:00, con el prompt del doc 23 del Project. Desde el 25/9 es el agente de **Cáscara entera** (Founders, B2C, B2B de agencia, 0800, growth y equipo) y además es el PM de Facu. Lo de Founders vive adentro de un "bloque puente" que está escrito para cortarse entero cuando exista un agente de Founders aparte.

`agente/prompt-agente.md` del repo es la versión anterior. Sigue diciendo 8:30, sigue mandando a republicar el handoff de Aye, que está discontinuado desde el 25/9, y no tiene ni Slack ni la ronda de PM. Hay que reemplazarlo por el doc 23 o borrarlo, para que nadie arme un flujo sobre un prompt que ya no corre.

**Lo que esto cambia en el plan:** n8n se lleva el bloque puente, que es la operación de Founders. La parte de Cáscara entera se queda en el Claude de Facu: el día de Facu, los lineamientos que bajan entre frentes, el contenido y las cuentas B2B, y la ronda de PM. Ninguna tabla de la app tiene dónde poner eso, y no hace falta: no es de un cliente de Founders.

---

## 1. Qué lee y con qué busca

| Fuente | Qué busca | Cómo |
|---|---|---|
| **Google Calendar** | El día de Facu: reuniones de hoy, declinadas y encimadas; las 1:1 de mañana para los recordatorios; las 1:1 que caen en día 30 o 90 | Eventos de hoy y de mañana. Es la primera fuente, siempre |
| **Fathom** | Llamadas nuevas desde la corrida anterior: 1:1 de Facu y de Franco, las tres grupales, onboardings y sign off de Teo, y las de equipo, porque "el hallazgo del día suele estar ahí" | Lista desde la última corrida; transcript completo de cada una que importa. Franco casi no graba: si falta una llamada suya, se dice |
| **Slack** | Todo lo que se movió: canales de cliente, de edición, `#admin-cascara`, `#llamadas-agendadas`, `#all-areas`, y los de servicio Founders que se mudan desde WhatsApp la semana del 28/9 | Búsqueda con `after:` en públicos y privados, con y sin bots; hilos con respuestas; archivos bajados y leídos, audios transcriptos |
| **Notion · Cuentas** | El padrón: Paso, START, FINISH, Updates y Correo. Filtro `Type = C. Founders` | `collection://1dc511e6-8cad-81be-8286-000b4e036742` |
| **Notion · Llamadas · Founders** | Qué entró por la automatización Fathom → Notion y qué quedó "Sin cliente" | `collection://e5581cbd-d498-44e4-b3d5-3e9d7443d0e8` |
| **Notion · calendarios de contenido** | Lo que sale hoy en Cáscara y en las cuentas B2B, y lo que está en riesgo | Direcciones en `sistema/26-pm-facu.md`, sección Fuentes |
| **Gmail** | Si algo prometido salió de verdad; cancelaciones (la de José David del 25/9 apareció acá) | Búsqueda por cliente y por fecha |
| **El repo** | Fichas, cartas, accionables, seguimiento; `CLAUDE.md` manda cómo se regenera | El clon de la Mac cuando está conectada; nunca uno nuevo de la nube |
| **El Project** | El criterio (docs 13, 15, 16, 03, 10, 14, 19), la libreta de PM (26) y la bitácora (04) | Se leen cuando hay que decidir algo; el 26 se lee siempre |
| **Facu** | Lo que no está en ninguna fuente: WhatsApp, lo que habló con Franco sin grabar, cómo sigue un cliente que no aparece | La ronda de preguntas numeradas; contesta en texto o audio |

**Fuentes que el plan de n8n todavía no toma:** Google Calendar (no hay flujo), Gmail (no hay flujo) y las respuestas de Facu a la ronda. Las tres alimentan hoy datos que la app necesita (la próxima sesión y las cancelaciones, sobre todo).

## 2. Qué produce y dónde lo deja

| Producción | Dónde queda hoy | Tabla de la app | Encaja |
|---|---|---|---|
| Hito de una llamada (`recorrido.hitos`) | Ficha `fichas/<slug>.json` | `actividad` (fuente `fathom`) y, si es 1:1, `sesiones` | Sí |
| Lectura del caso: `etapa`, `punto_a`, `lectura`, `titular`, `bajada`, `punto_b`, `roadmap`, `conclusion`, `carta`, `abierto` | Ficha | Ninguna: queda en la ficha y sale en `informes` como HTML | Sí, vía `informes` (paso 9) |
| Accionables del founder | Ficha (`accionables.cliente`) | `tareas` (por asignación y semana) | A medias: una tarea necesita asignación y semana, y muchos accionables no cuelgan de una carta |
| Accionables de Cáscara (`accionables.cascara`) y los del CSM (`contenido/entregas.json`) | Ficha y torre, sección Accionables CSM | **Ninguna** | No. No hay tabla de tareas del equipo |
| Puntaje y tramo | `generador/handicap.py` y copia en la ficha | **Ninguna** | No. Es interno y vive en la radiografía; si el admin lo tiene que mostrar, hace falta un campo |
| Ritmo (al día, sin próximo paso, sin noticias, en cierre) | `contenido/seguimiento.json`, calculado por `generador/seguimiento.py` | Se deriva de `actividad` (último contacto), `sesiones` (próxima) y `asignaciones` (carta abierta) | A medias: falta la próxima sesión (ver abajo) |
| Documentos del cliente (radiografía, informe de cierre) | `clientes/<slug>.html` | `informes` (publicado = false hasta que se revisa) | Sí (paso 9) |
| Cartas genéricas | `fichas/inventario.json` + `fichas/plantillas/<modulo>.json` → `cartas/` | `cartas` y `carta_tareas` (origen `repo`) | Sí (paso 3) |
| Cartas personalizadas | `fichas/plantillas/<modulo>--<slug>.json` → `cartas/para/<slug>-<modulo>.html` | **Ninguna** | No. `cartas` es la plantilla y `asignaciones` no guarda la versión del cliente |
| Estado de la carta del cliente (en revisión, aprobada, con feedback, se revisa en la llamada) | No existe todavía | `asignaciones.estado`, pero solo tiene `activa`, `completada`, `pausada` | No. Faltan los estados de revisión y el campo del feedback |
| Update en Cuentas (`DD/MM · Puntaje N/100, tramo, ritmo X…`) | Notion · Cuentas | `actividad` (fuente `agente`), y sigue en Notion | Sí |
| Lo mecánico de Notion: correos, llamadas sin relacionar, START propuesto | Notion | Queda en Notion; el paso 6 lo lee | Sí |
| Cliente nuevo detectado | Reporte | `clientes` (paso 8, desde el form de Airtable) | Sí |
| Prep de 1:1 en hitos | `clientes/prep-1a1-<fecha>-<nombre>.md` del Project | **Ninguna** | No. Podría ir a `informes` sin publicar o a `actividad` |
| Recordatorios de mañana | Reporte, para que Aye los mande | **Ninguna** (es un mensaje) | No hace falta tabla: va al canal `cf-` o a Aye por Slack |
| El reporte del día | Push, mail y la conversación de la corrida | Slack `founders-cerebro` (paso 7) | Sí, para la parte de Founders |
| Preguntas de PM y respuestas | `sistema/26-pm-facu.md` del Project | **Ninguna** | No, y se queda en el Claude de Facu |
| Lineamientos que bajan entre frentes | Docs del Project | **Ninguna** | No, y se queda en el Claude de Facu |
| La torre publicada | Artefacto `9PwwjoF73JbgCHwi51m18W` | El admin de la app la reemplaza | Sí, cuando el admin esté |
| Bitácora y `CAMBIOS.md` | Project y repo | **Ninguna** | Se quedan donde están |

## 3. Cuándo corre y cuánto tarda

| Tarea | Cuándo (ART) | Qué hace |
|---|---|---|
| Cáscara Founders — el día y el pulso | L a V, 9:00 | Todo lo de este mapa. Los lunes, además, el pulso y los hitos de día 30 y 90 |
| Revisión semanal | Viernes, 16:00 | Padrón, compromisos, skills; corrige Cuentas y Llamadas |
| Cierre del día | L a V, 20:00 | Página con el día que pasó y cómo arranca mañana; no escribe nada |
| Doctor Financiero | Todos los días, 9:00 | Personal, no toca Cáscara |

**Cuánto tarda:** la bitácora no registra la duración (falta confirmar). Lo que sí registra: una corrida con barrido cargado lee entre 7 y 13 llamadas y hasta cuatro transcripts completos, toca varias fichas, regenera, republica y escribe los Updates; una sin novedades se cierra en una línea. Hay días con segunda corrida cuando Facu contesta la ronda (25/9 a las 8:55 y a las 9:20).

**Cómo se ordenan los flujos de n8n contra esto:** Fathom 8:00, Slack 8:15, Notion 8:30 y el cerebro 9:00. Mientras corran los dos en paralelo (paso 10), la tarea de las 9:00 sigue haciendo el barrido completo y n8n solo escribe en la base.

## 4. En qué tabla va a vivir cada cosa, y lo que no tiene tabla

Resumen de la columna "Encaja" de arriba. Tienen tabla y el plan ya las cubre: hitos y sesiones, grupales, documentos, cartas genéricas, Updates, cliente nuevo y el reporte.

**No tienen tabla, y hay que decidir antes del paso 4:**

1. **Las cartas personalizadas.** Son el trabajo de consultor de Facu y hoy son 21. Propuesta: que `sync_cartas.py` las suba como filas de `cartas` con código `<modulo>--<slug>`, origen `repo`, ocultas en la galería y ligadas al cliente, y que al asignarlas la app use esa versión en vez de la genérica. Ojo: la versión de The Momentum Club usa el slug `momentum-club` y el cliente es `the-momentum-club`; hay que igualarlo antes de sincronizar.
2. **Los estados de revisión de la carta del cliente.** Sumar a `asignaciones.estado` los valores `en_revision`, `aprobada`, `con_feedback` y `se_revisa_en_llamada`, más un campo `feedback`. Y un flujo de n8n que avise al canal del CSM cuando el cliente la pasa a revisión.
3. **La próxima sesión.** El ritmo necesita saber si hay una reunión con fecha, y hoy eso sale del Calendar. La app no tiene tabla de sesiones futuras ni flujo que lea el Calendar. Opciones: un flujo de Calendar → `sesiones` con estado `agendada`, o que el cliente reserve desde los links de agenda y la app lo registre.
4. **Las tareas del equipo** (los accionables de Cáscara y los del CSM). Hoy viven en la torre. O se suma una tabla, o se cargan en `tareas` con un responsable del equipo.
5. **El puntaje.** Si el admin lo va a mostrar, un campo en `clientes`; si no, queda en la radiografía.

**Los nombres de los canales de Slack.** El plan dice `cf-` + slug de la ficha (`cf-sofia-galvis`) y en la reunión del 26/9 salió "el nombre de Notion". Tiene que ser uno solo y el mismo que `clientes.slug`, porque el flujo del paso 5 busca al cliente por ese slug.

**El ritmo nuevo.** La definición vigente (26/9): al día si hubo contacto en los últimos 14 días y hay un próximo paso; sin próximo paso si hay noticias pero ni reunión ni carta abierta; sin noticias si pasaron más de 14 días; en cierre para los sign off. El último contacto sale de `actividad`; el reporte del paso 7 tiene que usar esta misma definición y sumar un bloque de "sin noticias" y "sin próximo paso", para que la torre, el admin y el Slack digan lo mismo.

## 5. Qué es mecánico y qué necesita criterio

**Mecánico (n8n lo hace sin modelo o con un resumen corto):**
- Traer llamadas de Fathom, mensajes de Slack y cambios de Notion desde la última corrida.
- Identificar al cliente de cada cosa (por mail, nombre o slug del canal).
- Relacionar llamadas "Sin cliente", cargar correos faltantes, escribir el START propuesto.
- Guardar grupales con su grabación.
- Calcular días de programa, hitos de día 30, 60 y 90, y el ritmo.
- Detectar vencidos y quién espera algo hace más de 3 días.
- Dar de alta al cliente desde el form y crear su canal.
- Sincronizar las cartas del repo y subir los documentos generados.
- Avisar al canal del CSM cuando una carta pasa a revisión.

**Criterio (necesita el modelo y, en lo que toca al cliente, a Facu):**
- Leer una llamada y decidir qué cambia en el caso: cuello, etapa, lectura, punto B.
- Mover el puntaje y explicar por qué.
- Escribir el resumen de una sesión de cara al cliente.
- Decidir qué carta va y armar la versión para ese cliente. **Esto se queda en el Claude de Facu**: es su trabajo de consultor y es lo que la reunión del 26/9 dejó explícitamente de su lado. Aye, después, puede asignar desde la galería las que ya existen.
- Proponer tareas nuevas para la semana (el paso 7 las deja para aprobar, no las carga solas).
- Detectar que una decisión contradice un documento del Project y reescribirlo.
- La ronda de PM y los lineamientos entre frentes.

---

## Lo que sale de este mapa para el resto del plan

- **Paso 3:** sincronizar también las cartas personalizadas, no solo el inventario, e igualar el slug de Momentum.
- **Paso 4:** además de `sesiones` y `grupales`, que el flujo marque el último contacto del cliente en `actividad`, porque de ahí sale el ritmo.
- **Paso 5:** fijar el nombre de los canales antes de crearlos.
- **Paso 7:** el reporte usa la definición de ritmo de arriba, y el agente de n8n se queda solo con Founders; el de Cáscara entera sigue en el Claude de Facu.
- **Falta en el plan:** un flujo de Calendar para la próxima sesión, los estados de revisión de la carta con su aviso al CSM, y reemplazar `agente/prompt-agente.md` por el prompt que corre.
