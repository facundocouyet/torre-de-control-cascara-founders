# Torre de control · Cáscara Founders

El tablero interno de Cáscara Founders: los clientes de la camada, el handicap de cada uno,
los días de programa, los documentos completos y el material del programa.

Abrí `index.html` en el navegador y ya funciona. No necesita servidor ni build para verse.

---

## Qué hay adentro

| Carpeta | Qué es |
|---|---|
| `index.html` | La app. Cuatro vistas (Hoy, Clientes, Programa, Material), navegación con flechas y teclado, y el detalle de cada cliente. Es un solo archivo con los datos adentro. |
| `clientes/` | Los diecinueve documentos de founder, uno por cliente, más el repaso de la camada. Cada uno es un HTML autocontenido de paneles horizontales, con el checklist de accionables que se acuerda de lo tachado. |
| `assets/founders.css` | El design system escrito y comentado: tokens primero, componentes después. |
| `contenido/` | Los datos en JSON: `app-data.json` es lo que lee la app, y los otros tres son las fuentes desde las que se arma. |
| `fichas/` | Las diecinueve fichas de cliente, esquema de veintiún campos. Es la fuente de verdad de los documentos. |
| `generador/` | Los scripts de Python que producen todo lo anterior. |
| `inicio.html`, `clientes.html`, `programa.html`, `materiales.html` | La versión estática, de scroll, para compartir con quien no entra a la app. |

## Cómo se regenera

Necesita Python 3, sin dependencias externas.

```bash
# 1. los documentos de cliente, desde las fichas
python3 generador/build2.py          # escribe out2/<slug>.html

# 2. los datos de la app, desde las fichas y el registro de handicap
python3 generador/build_app.py       # escribe contenido/app-data.json

# 3. la app
python3 generador/app_shell.py       # escribe index.html

# 4. la versión estática
python3 generador/build_site.py
```

El orden importa: las fichas mandan sobre todo lo demás, y `handicap.py` manda sobre cualquier
puntaje guardado en una ficha.

## El handicap

Cinco habilidades —oferta, contenido, demanda, venta y entrega— que el founder mejora durante el
programa. Cada una se muestra del 1 al 100 y el general es el promedio de las cinco.

Adentro se puntúan con una escalera de cinco escalones, que es lo que permite anclar cada número a
una evidencia concreta: `0` no existe, `1` está en la cabeza, `2` hecho pero incompleto, `3` completo
y funcionando sin depender de la persona, `4` probado con un resultado real. La conversión es
`escalón × 20 + 10`, así que el piso es 10 y el techo 90.

Dos reglas que definen el puntaje:

1. **Se puntúa el negocio sobre el que corre el roadmap.** Un founder con dos negocios se lee por el
   que estamos trabajando. La capacidad que tiene en el otro va en la evidencia, no en la barra.
2. **Lo que está en la cabeza vale 1.** Lo que salió de la Clarity Call es evidencia de lo que el
   founder sabe, y la barra sube cuando algo queda escrito, publicado o cobrado.

Cuando varias habilidades empatan abajo, manda la que el roadmap trabaja primero. Eso se declara
a mano en `MANDA`, dentro de `generador/handicap.py`.

Los tramos: 10 a 38 Arranque · 42 a 50 En construcción · 54 a 62 Andando · 66 a 90 Listo para cerrar.

El **ritmo** va aparte y no puntúa el negocio: mide si la persona hace lo que le queda de cada
llamada. Verde al día, amarillo a los tirones, rojo frenado.

## El diseño

La piel viene de F3: tinta `#171717`, papel cálido `#ECEAE4`, la etiqueta encajonada y el radio 0.
La respiración viene de Cáscara: escala grande, aire y columnas anchas. Todo monocromo, con el rojo
`#FE1414` racionado para lo frenado y lo vencido. El sello de la marca es la caja con la F de
Founders, el mismo motivo que la etiqueta de los documentos.

## Cómo escribir acá adentro

Español rioplatense, directo, adulto. Nada aspiracional. La regla dura: se dice lo que la cosa es,
sin anteponer lo que no es. Y el documento lo lee el founder, con su nombre en la portada, así que
no hay ingenio a costa de él.

## Estado

Datos al 13 de septiembre de 2026. Veintiún clientes, diecinueve con documento.
Los documentos son primeras versiones y se revisan antes de mandarlos.
