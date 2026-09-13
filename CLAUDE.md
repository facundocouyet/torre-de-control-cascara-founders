# Contexto para Claude Code

Este repo es la **torre de control de Cáscara Founders**: el tablero interno con la camada de
clientes, el handicap de cada uno y los documentos de founder. Leé `README.md` antes de tocar nada.

## Lo primero que hay que hacer acá

Crear el repositorio en GitHub y empujar lo que ya está commiteado.

- Nombre: `torre-de-control-cascara-founders`
- Cuenta: `facundocouyet`
- Privado
- Vacío, sin README ni .gitignore de GitHub (este repo ya tiene los suyos)

La rama es `main` y ya tiene los commits hechos. Después de crearlo:

```bash
git remote add origin https://github.com/facundocouyet/torre-de-control-cascara-founders.git
git push -u origin main
```

## Cómo se regenera todo

Python 3, sin dependencias. El orden importa.

```bash
python3 generador/build2.py      # documentos de cliente, desde fichas/  -> out2/<slug>.html
python3 generador/build_app.py   # datos de la app                       -> contenido/app-data.json
python3 generador/app_shell.py   # la app                                -> index.html
python3 generador/build_site.py  # la versión estática de scroll
```

Las rutas de los scripts apuntan a la máquina donde se generaron (`/home/claude/...`). Si algo no
encuentra un archivo, ajustá la ruta al repo y dejá el cambio commiteado.

## Reglas que no se negocian

**El handicap.** `generador/handicap.py` es la única fuente de verdad de los puntajes. Las fichas
guardan una copia y `build_app.py` la recalcula desde el registro, así que nunca edites un puntaje
adentro de una ficha: se edita en `handicap.py` y se regenera.

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
