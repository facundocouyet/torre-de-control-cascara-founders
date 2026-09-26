# El cerebro de Cáscara

Acá queda escrito lo que pasa en Cáscara: qué decidimos, por qué, qué aprendimos, cómo cambió la
oferta, cómo avanzó cada alumno y cada cliente, y qué criterio fuimos armando en el camino. Lo que
hoy vive en WhatsApp, en una llamada o en la cabeza de Facu se registra acá, ordenado, para que
mañana lo lea una persona nueva, un agente o un copiloto y pueda trabajar con el mismo contexto.

El objetivo final es el de Facu: **negocios autónomos.** Un negocio puede correr solo cuando lo que
sabe está escrito de una forma que otro pueda usar. Este es el lugar donde se escribe.

---

## Las tres capas

| Capa | Dónde | Qué es | Quién la toca |
|---|---|---|---|
| **1 · El registro** | `registro/AAAA/MM/` | Lo que pasó. Una entrada por hecho, con fecha y fuente. No se edita nunca: se agrega. | El agente todos los días, y cualquiera que decida algo |
| **2 · Lo vigente** | `departamentos/<depto>/README.md` | Cómo es cada departamento hoy: qué vende, cómo trabaja, qué criterio usa, qué quedó abierto. Se reescribe cuando el registro lo cambia. | El agente los lunes, destilando la semana |
| **3 · El índice** | `indice.json`, `personas/`, `RECIENTE.md` | Lo mismo, armado para una máquina: todas las entradas con sus datos, la línea de tiempo de cada cliente y lo último por departamento. | Nadie a mano: lo genera `generador/cerebro.py` |

El registro es la memoria. Lo vigente es lo que hay que saber para trabajar hoy. El índice es lo que
lee un agente, n8n o una base de datos sin tener que abrir archivo por archivo.

## Qué se registra

Una entrada es **un hecho que tiene consecuencia**. Si mañana alguien lo necesita para decidir,
se registra. Hay ocho tipos:

| Tipo | Cuándo | Ejemplo |
|---|---|---|
| `decision` | Se decidió algo que cambia cómo se trabaja o qué se hace | Agos lanza en noviembre con 2 lugares |
| `criterio` | Facu o el equipo definen cómo se piensa o se evalúa algo | "Frenado" es una alerta de seguimiento, no un juicio sobre el resultado |
| `aprendizaje` | Algo salió distinto de lo esperado y eso nos enseña | Los clientes de alcance claro son los que mejor pagan por hora |
| `oferta` | Cambia qué vendemos, a quién, cómo o a qué precio | Un producto nuevo, un precio nuevo, un módulo que se suma |
| `hito` | Un cliente o alumno llega a un punto que marca su evolución | Primera venta, lanzamiento, mandó un documento clave, cierre, abandono |
| `proceso` | Cambia cómo se hace algo de forma repetible | Los accionables se trabajan en la torre y no en el handoff |
| `metrica` | Aparece un número real que importa | Facturación de un lanzamiento, ventas de un bootcamp |
| `pregunta` | Algo quedó abierto y alguien tiene que decidirlo | ¿El inicio de la torre muestra de quién es la pelota? |

**No se registra:** tareas y recordatorios (van al tablero de Facu o a la torre), lo que ya está en
una ficha y no cambia nada, y charla sin decisión.

## Cómo se escribe una entrada

Un archivo por entrada en `registro/AAAA/MM/AAAA-MM-DD-<tema-corto>.md`, con la fecha en que pasó
(no la del día que se registra). Copiá `_plantilla.md`.

```markdown
---
id: 2026-09-24-agos-lanza-en-noviembre
fecha: 2026-09-24
tipo: decision
depto: founders
sobre: [agostina-marchesini]
quien: [facu, agostina-marchesini]
temas: [lanzamiento, oferta]
fuente: WhatsApp, grupo Agos x Cáscara Founders, 24/9
certeza: dicho
estado: vigente
---
# Agos lanza en noviembre con 2 lugares de prueba y relanza en febrero con 5

Qué pasó, en dos o tres líneas. Por qué. A quién le cambia qué.
Las frases que definen algo van textuales y entre comillas.
```

Las reglas:

1. **El título es la conclusión**, en una frase y en presente. Quien lee solo los títulos tiene que
   entender la historia.
2. **Una entrada, un hecho.** Si en una llamada se decidieron tres cosas, son tres entradas.
3. **Siempre la fuente, con fecha.** Llamada de Fathom con su link, grupo de WhatsApp, doc del
   Project, mensaje de Facu. Si la fuente ya tiene el detalle, se linkea y no se copia.
4. **La certeza, sin disfrazar.** `dicho`: lo dijo alguien, en una llamada o por escrito. `visto`:
   sale de un dato (Notion, Fathom, números, un documento del cliente). `propuesto`: lo propone el
   agente o alguien y nadie lo confirmó. Una propuesta nunca se registra como decisión.
5. **El pasado no se edita.** Si una decisión cambia, se escribe una entrada nueva con
   `reemplaza: <id viejo>` y a la vieja se le cambia solo `estado: reemplazada`. Así queda la
   historia de cómo evolucionó el criterio, que es lo que más vale.
6. **Corto.** Entre tres y diez líneas de cuerpo. Si hace falta más, va a un documento y la entrada
   lo linkea.
7. **Los nombres, como slugs.** Clientes con el slug de su ficha (`sol-boutmy`), el equipo por su
   nombre corto (`facu`, `fede`, `juana`, `teo`, `franco`, `aye`, `azu`, `lola`, `mati`,
   `segundo`, `mora`, `enzo`). Los clientes que no son de Founders, con un slug nuevo (`cero`).
8. **Nada de claves, contraseñas, datos de tarjetas ni documentos personales.**

## Los departamentos

| Slug | Departamento | Dueño |
|---|---|---|
| `cascara` | Dirección: visión, estrategia, ecosistema Disruptia, capital | Facu |
| `founders` | Cáscara Founders, la aceleradora de 90 días | Facu |
| `b2c` | La Cáscara, La Cascarita y el Founders Bootcamp | Teo |
| `agencia` | Las cuentas de contenido B2B y la fábrica de contenido | Fede y Juana |
| `marcas` | 0800, la unidad de marcas | Aldi |
| `alianzas` | Growth y alianzas: REIN, Cero, Delfi Ferro, Newro, F3 | Franco |
| `equipo` | Roles, acuerdos, contrataciones, capacidad | Facu y Teo |
| `sistemas` | Automatización, agentes, la torre, la app y el cerebro | Facu |

Cada uno tiene su `README.md` con lo vigente. Un departamento nuevo se suma acá y en
`generador/cerebro.py`.

## El ritmo

- **Todos los días**, el agente de la mañana registra lo que pasó el día anterior: decisiones de
  las llamadas, hitos de los clientes, lo que Facu contestó en el PM, números nuevos.
- **Los lunes**, destila la semana: lee las entradas nuevas y reescribe la sección "Lo vigente" de
  cada departamento que cambió. Si una entrada contradice lo vigente, gana la entrada más nueva y
  se dice en el reporte.
- **Cuando alguien decide algo en una conversación** (con Facu, en Cowork, en una llamada), se
  registra en el momento. No se espera al barrido.

## Cómo se regenera el índice

```bash
python3 generador/cerebro.py        # valida las entradas y escribe indice.json, personas/ y RECIENTE.md
```

También corre dentro de `./construir.sh`. Si una entrada tiene un campo mal, el script dice cuál y
no escribe nada.

## Para qué sirve después

- **Un agente nuevo** arranca leyendo `RECIENTE.md` y el README de su departamento, y busca en
  `indice.json` lo que necesite.
- **La base de datos del cerebro** (n8n + Supabase) importa `indice.json` tal cual: cada entrada es
  una fila con sus campos.
- **Un copiloto de un departamento** recibe su README y sus entradas como contexto fijo.
- **Un cliente nuevo** se entiende leyendo `personas/<slug>.md`: su historia en orden, desde el
  primer día.
