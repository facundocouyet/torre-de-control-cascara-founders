# Torre de control de Cáscara Founders

Este repo genera todo lo que Cáscara Founders publica: los documentos de cada founder, la torre de
control, las cuarenta cards con sus plantillas, el handoff para el equipo y el documento del rol.

## Cómo está armado

```
fichas/                 la fuente de verdad
  <slug>.json           una ficha por founder, 22 claves (esquema v2)
  inventario.json       las 40 cards: categoría, pasos, qué completa el founder, herramientas
  plantillas/*.json     la hoja que completa el founder para cada card
generador/              los scripts que convierten las fichas en HTML
sistema/                el rol de líder y las reglas de redacción
agente/                 el prompt de la tarea programada diaria
clientes/               los documentos generados, uno por founder
cartas/ plantillas/     las cards y sus hojas, generadas
index.html              la torre de control
```

## Los scripts

| Script | Qué hace | Salida |
|---|---|---|
| `build2.py` | Documentos de cliente desde `fichas/*.json` | `out2/<slug>.html` → se copia a `clientes/` |
| `build_cartas.py` | Las 40 cards | `cartas/` |
| `build_plantillas.py` | Las hojas del founder | `plantillas/` |
| `build_app.py` + `app_shell.py` | La torre de control | `index.html` |
| `build_cards.py` | El handoff de cards por dueño | `cards-por-dueno.html` |
| `build_rol.py` | El documento del rol | `rol-lider-founders.html` |
| `build_ally.py` | El handoff del equipo | `founders-handoff-aye.html` |
| `handicap.py` | Calcula los cinco ejes y el tramo | lo usan los builds |

`build_plantillas.py` exporta la paleta (INK, PAPER, GREY, LINE, DISP, SERIF) que reusan todos los demás.

## El esquema de una ficha

22 claves, en este orden: `slug`, `cliente`, `proyecto`, `modo` ("cierre" o "radiografia"),
`orientacion`, `arranque`, `etapa`, `metrica`, `titular`, `bajada`, `punto_a`, `recorrido`,
`lectura`, `respuestas`, `entregables`, `punto_b`, `roadmap`, `accionables`, `conclusion`,
`carta`, `abierto`, `handicap`.

El handicap se renderiza **solo cuando `modo` es "radiografia"**. En los informes de cierre no va,
porque esos son los que se le mandan al cliente.

## Reglas de redacción

Están completas en `sistema/brief-redaccion-v2.md`. Las que más se rompen:

- Se dice lo que la cosa es, directo. Nunca explicar algo anteponiendo lo que no es.
- Un solo cuello de botella por caso.
- Nada inventado: lo que la llamada no dijo va "(falta confirmar)".
- Sin ironía a costa del founder.
- Los paneles que se parten en dos no llevan "1 de 2".
- La autocrítica de Cáscara va en la versión interna, no en el documento del cliente.

## Cómo correr todo

```bash
cd generador
python3 build2.py && cp out2/*.html ../clientes/
python3 build_cartas.py && python3 build_plantillas.py
python3 build_app.py
```
