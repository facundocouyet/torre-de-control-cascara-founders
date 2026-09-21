# La app de clientes

Acá va la app que ven los clientes. Es de Teo.

## Qué podés tocar libremente

Todo lo que esté adentro de esta carpeta. Nadie más la toca, así que no
hay forma de que se pise con la torre de control.

## De dónde sacás los datos

Los clientes y su estado viven en la raíz del repo y son la misma fuente
que usa la torre. No los copies ni los dupliques: leelos de ahí.

    ../fichas/*.json            una ficha por cliente
    ../fichas/inventario.json   el catálogo de módulos y cartas
    ../contenido/*.json         entregas, proceso, orientaciones

El esquema de una ficha son 22 claves y está descrito en
`../sistema/` y en el generador `../generador/build2.py`, que es el que
las lee hoy.

Si necesitás que una ficha tenga un campo nuevo, pedíselo a Facu antes de
agregarlo: ese archivo lo escribe él y un campo inventado de un lado se
pierde la próxima vez que lo regenere.

## Cómo se publica

Si ponés acá un `construir.sh` ejecutable que deje su salida en
`app-clientes/dist/`, el build de la raíz lo corre solo y publica el
resultado en `/app` del sitio.

    app-clientes/construir.sh   →   app-clientes/dist/   →   <sitio>/app/

Mientras no exista ese archivo, el build de la raíz lo saltea sin quejarse,
así que podés empezar cuando quieras.

## Lo único que no se hace

No se commitea nada generado. Si tu build produce HTML, JS o CSS armado,
va a `app-clientes/dist/`, que está ignorado. Lo que se versiona es el
código que lo produce.
