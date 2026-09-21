# Qué carta de oferta corresponde

Antes de generar una carta de oferta hay que decidir cuál de las dos formas va, y eso
depende de dónde viene el founder. Generar la que no es cuesta una vuelta entera:
el founder contesta ocho preguntas que no aplican a su caso y la llamada con Franco
arranca de cero igual.

## La pregunta que decide

**¿Ya está vendiendo esto que estamos ordenando, o lo está por lanzar?**

No alcanza con mirar si factura. Un founder puede facturar mucho con un servicio y
estar armando un producto distinto: ahí lo que vende hoy es prueba de que sabe hacerlo,
no es el mercado del producto nuevo. Ese fue el caso de Sofía Galvis, y la primera
versión de su carta le preguntaba por los clientes de la agencia cuando el producto
nuevo es un programa de educación que esos clientes no compran.

## Forma A · Construcción — `one-sheeter-oferta`

Para el founder que **ya vende** y necesita ordenar lo que vende. Las preguntas lo
llevan a escribir la oferta: cliente ideal, promesa con número y plazo, cómo se mide,
paso a paso de la entrega, qué incluye y qué no, precio, y probarla en una conversación
real. Cáscara corrige, no redacta.

## Forma B · Discovery — variante `one-sheeter-oferta--<slug>`

Para el founder que **está por lanzar algo que todavía no existe**, o que redirecciona
su oferta hacia otro mercado. No se le puede pedir una promesa con número de algo que
nunca vendió. Las preguntas bajan materia prima: quién ya le pide, qué sabe hacer que
hoy no vende suelto, qué explica fácil, a quién ya le cambió algo, qué le van a
preguntar antes de comprar, dónde se traba la gente, qué no quiere sostener y contra
qué lo comparan. Franco escribe la oferta con eso en su llamada.

Cuando el producto todavía no existe, no se pregunta por horas medidas de entrega:
sería una estimación inventada. Eso se define con el formato, después.

## Lo que comparten las dos

Las dos abren con el bloque de NOVA y las dos cierran igual, con dos preguntas que el
founder contesta él:

- **Tu NOVA, en cuatro frases** — nicho, oferta, vehículo y atención, en borrador.
- **Tu one-sheeter, en una carilla** — las cinco partes del formato de Franco.

El one-sheeter lo arma el founder. Lo tosco se afila en la llamada; lo que llega en
blanco se improvisa.

## Cómo se genera

La variante vive en `fichas/plantillas/one-sheeter-oferta--<slug>.json` y hereda de la
genérica todo lo que no redefina. Si define `secciones`, reemplaza las de la genérica
por completo, que es el caso de las dos formas de arriba.

Cada sección puede fijar su clave de guardado con `cid`. Están fijadas: si hay que meter
un bloque nuevo en el medio de una carta ya enviada, lo escrito por el founder no se
mueve de lugar.

Casos vivos: Sofía Galvis (forma B, programa de educación), Matías Morales (forma B,
redirección a marcas personales).
