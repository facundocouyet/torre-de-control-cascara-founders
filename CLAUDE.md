# Contexto para Claude Code

Este repo es la **torre de control de Cáscara Founders**: el tablero interno con la camada de
clientes, el puntaje de cada uno y los documentos de founder. Leé `README.md` antes de tocar nada.

## Dónde vive

`https://github.com/facundocouyet/torre-de-control-cascara-founders`, público, cuenta
`facundocouyet`. GitHub Pages lo sirve desde `main` en
`https://facundocouyet.github.io/torre-de-control-cascara-founders/`, y `robots.txt` lo deja fuera
de los buscadores. El remoto `origin` ya está configurado y `main` sigue a `origin/main`.
Se mantiene actualizado desde Cowork, así que el repo tiene que estar entre las fuentes
autorizadas de la sesión de Cowork para que pueda empujar sin pasar por Code.

## Cómo se regenera todo

Python 3, sin dependencias. El orden importa.

```bash
python3 generador/build2.py      # documentos de cliente, desde fichas/  -> clientes/<slug>.html
python3 generador/build_app.py   # datos de la app, desde el registro    -> contenido/app-data.json
python3 generador/app_shell.py   # la app                                -> index.html
python3 generador/build_site.py  # la versión de scroll -> inicio.html, programa.html,
                                 #   materiales.html, clientes.html
```

Todas las rutas son relativas a la raíz del repo y los cuatro scripts corren desde cualquier
directorio. `contenido/app-data.json` es intermedio: lo escribe `build_app.py`, lo lee
`app_shell.py` y no se commitea.

`generador/build.py` es el generador v1, reemplazado por `build2.py`, que lo importa como
librería para los paneles y los colores. Su cuerpo está detrás de `if __name__ == "__main__"`:
importarlo no tiene que escribir nada.

`contenido/arranques.json` guarda la primera llamada de cada cliente, por slug. Es lo que antes
salía del campo `que_paso` de las fichas viejas, que no viajó con el repo. `dias.py` lo lee
después de `START`.

## Reglas que no se negocian

**El puntaje.** `generador/handicap.py` es la única fuente de verdad de los puntajes. Las fichas
y `contenido/panel-data.json` guardan una copia, y tanto `build_app.py` como `build_site.py` la
recalculan desde el registro, así que nunca edites un puntaje adentro de una ficha: se edita en
`handicap.py` y se regenera. En todo texto que se lea se dice puntaje, nunca handicap; el nombre
del archivo quedó por historia. Si la app y el sitio muestran números distintos, alguno dejó de
recalcular.

**La escritura.** Español rioplatense, directo, adulto. Se dice lo que la cosa es, sin anteponer lo
que no es: nada de "no es X, es Y". Nada aspiracional. Los documentos los lee el founder, con su
nombre en la portada, así que no hay ironía ni frases ingeniosas a costa de él.

**El diseño.** Monocromo. Tinta `#171717`, papel `#ECEAE4`, radio 0. El rojo `#FE1414` va racionado:
solo lo frenado, lo vencido y la habilidad que manda. Todo está comentado en `assets/founders.css`.

**Verificar antes de dar algo por hecho.** Cada documento son paneles de 1920×1080 fijos: si el
contenido crece, desborda en silencio. Después de tocar tamaños o textos hay que abrir los
diecinueve documentos en un navegador y chequear que ningún `.pnl` tenga `scrollHeight > 1080`.
Lo mismo con la app: no puede haber scroll horizontal ni a 1512px ni a 390px.

## Estado

Datos al 13 de septiembre de 2026. Veintiún clientes, diecinueve con documento. Los documentos son
primeras versiones y se revisan antes de mandarlos.
