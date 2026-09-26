# Torre de control de Cáscara Founders

Este repo genera todo lo que Cáscara Founders publica: los documentos de cada founder, la torre de
control, las cuarenta cartas, el handoff para el equipo y el documento del rol.
Leé `README.md` antes de tocar nada.

## Dónde vive

`https://github.com/facundocouyet/torre-de-control-cascara-founders`, público, cuenta
`facundocouyet`. GitHub Pages lo sirve desde `main` en
`https://facundocouyet.github.io/torre-de-control-cascara-founders/`, y `robots.txt` lo deja fuera
de los buscadores. Se mantiene desde Cowork y desde la tarea programada de `agente/`, así que el
repo tiene que estar entre las fuentes autorizadas de esas sesiones para que puedan empujar.

## Cómo está armado

```
fichas/                 la fuente de verdad
  <slug>.json           una ficha por founder, 22 claves (esquema v2)
  inventario.json       las 40 cartas: categoría, pasos, qué completa el founder, herramientas
  plantillas/*.json     la hoja que completa el founder, que entra adentro de su carta
                        <modulo>--<slug>.json es la versión escrita para un founder
contenido/              lo que no es de un founder: panel, programa, materiales y arranques
generador/              los scripts que convierten las fichas en HTML
sistema/                el rol de líder y las reglas de redacción
agente/                 el prompt de la tarea programada diaria
cerebro/                la memoria escrita de Cáscara: registro, lo vigente por depto e índice
assets/                 founders.css, los logos y el favicon
clientes/               los documentos generados, uno por founder
cartas/                 las cuarenta cartas, generadas
  para/                 las escritas para un founder: <slug>-<modulo>.html
index.html              la torre de control
```

## Cómo se regenera todo

Python 3, sin dependencias. Todas las rutas son relativas a la raíz del repo y los scripts corren
desde cualquier directorio. Los cuatro primeros van en ese orden; el resto es independiente.

```bash
python3 generador/build2.py            # documentos de cliente, desde fichas/   -> clientes/<slug>.html
python3 generador/build_app.py         # datos de la app, desde el registro     -> contenido/app-data.json
python3 generador/app_shell.py         # la torre de control                    -> index.html
python3 generador/build_site.py        # la versión de scroll -> inicio.html, programa.html,
                                       #   materiales.html, clientes.html
python3 generador/build_cartas.py      # las cartas, desde fichas/inventario.json +
                                       #   fichas/plantillas/                  -> cartas/
python3 generador/build_cards.py       # el reparto de cartas por dueño         -> cards-por-dueno.html
python3 generador/build_rol.py         # el documento del rol                   -> rol-lider-founders.html
python3 generador/build_ally.py        # el handoff del equipo                  -> founders-handoff-aye.html
```

- `contenido/app-data.json` es intermedio: lo escribe `build_app.py`, lo lee `app_shell.py` y no se
  commitea.
- `fichas/` guarda también `inventario.json`. Los scripts que recorren las fichas de founder lo
  saltean; si agregás uno que las recorra, tiene que saltearlo también.
- `generador/build.py` es el generador v1. `build2.py` lo importa como librería para los paneles, los
  colores y el shell, así que su cuerpo va detrás de `if __name__ == "__main__"`. `build_cartas.py`
  dejó de importarlo el 18/9: las cartas pasaron a documento de scroll y se generan solas.
- `build_plantillas.py` dejó de generar el 21/9: la carta y la hoja son un solo documento vertical
  y las arma `build_cartas.py`. Queda como librería, porque exporta la paleta (INK, PAPER, GREY, LINE, DISP, SERIF) que reusan `_base.py`,
  `build_cards.py`, `build_rol.py` y `build_ally.py`.
- `contenido/arranques.json` guarda la primera llamada de cada cliente, por slug. `dias.py` lo lee
  después de `START`.
- `tablero.html` y `home-scroll.html` son páginas sueltas: no tienen generador y nada las linkea.

## El esquema de una ficha

22 claves, en este orden: `slug`, `cliente`, `proyecto`, `modo` ("cierre" o "radiografia"),
`orientacion`, `arranque`, `etapa`, `metrica`, `titular`, `bajada`, `punto_a`, `recorrido`,
`lectura`, `respuestas`, `entregables`, `punto_b`, `roadmap`, `accionables`, `conclusion`,
`carta`, `abierto`, `handicap`.

El puntaje se renderiza **solo cuando `modo` es "radiografia"**. En los informes de cierre no va,
porque esos son los que se le mandan al cliente.

## Reglas de redacción

Están completas en `sistema/brief-redaccion-v2.md`. Español rioplatense, directo, adulto, nada
aspiracional. Las que más se rompen:

- Se dice lo que la cosa es, directo. Nunca explicar algo anteponiendo lo que no es.
- Un solo cuello de botella por caso.
- Nada inventado: lo que la llamada no dijo va "(falta confirmar)".
- Sin ironía a costa del founder.
- Los paneles que se parten en dos no llevan "1 de 2".
- La autocrítica de Cáscara va en la versión interna, no en el documento del cliente.

## Reglas que no se negocian

**El puntaje.** `generador/handicap.py` es la única fuente de verdad de los puntajes. Las fichas y
`contenido/panel-data.json` guardan una copia: `build_app.py` y `build_site.py` recalculan desde el
registro, y `build2.py` lee la copia de la ficha. Nunca edites un puntaje adentro de una ficha: se
edita en `handicap.py`, se corre `python3 generador/handicap.py` parado en la raíz para actualizar
las copias, y se regenera. Si la app, el sitio y un documento muestran números distintos, alguna
copia quedó atrás.

**La palabra.** En todo texto que se lea se dice puntaje, nunca handicap. Quedaron con su nombre
el archivo `handicap.py`, la clave `handicap` de las fichas y el documento de anclajes del Project.

**El diseño.** Monocromo. Tinta `#171717`, papel `#ECEAE4`, radio 0. El rojo `#FE1414` va racionado:
solo lo frenado, lo vencido y la habilidad que manda. Todo está comentado en `assets/founders.css`.
Los logos están en `assets/`: `cascara-founders-blanco.png` con el menú abierto,
`founders-f-blanco.png` con el menú plegado y en el visor de cartas, y `favicon.png`. Salen de los
PNG de marca con el fondo pasado a transparente.

**Verificar antes de dar algo por hecho.** Los documentos de cliente son paneles de 1920×1080 fijos:
si el contenido crece, desborda en silencio. Después de tocar tamaños o textos hay que abrir en un
navegador lo que se tocó y chequear que ningún `.pnl` tenga `scrollHeight > 1080`. Las cartas son
documentos de scroll y no desbordan, pero se revisan igual a 1512 y a 390 de ancho. Lo mismo con la app: no puede haber scroll horizontal ni a 1512px ni a
390px.

## Estado

Datos al 14 de septiembre de 2026. Veintiún clientes, diecinueve con documento, cuarenta cartas, treinta y tres de
ellas con hoja para completar adentro. Los documentos son primeras versiones y se revisan antes de mandarlos.

## El cerebro

`cerebro/` es la memoria de Cáscara entera, no solo de Founders: qué se decidió, por qué, qué se
aprendió, cómo cambió la oferta y cómo evolucionó cada cliente. Leé `cerebro/README.md` antes de
escribir. Cuando en una conversación se decide algo con consecuencia, se registra en el momento
como una entrada en `cerebro/registro/AAAA/MM/`, y después se corre `python3 generador/cerebro.py`.
No va a `dist/`: es fuente, no sitio.
