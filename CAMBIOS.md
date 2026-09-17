# Cambios

Lo que se tocó cada día, en criollo. Lo más nuevo arriba. Se lee antes de hacer el push
para saber qué estás subiendo, sin abrir los archivos.

---

## 17 de septiembre de 2026 · las cifras

**Las cantidades ahora van en número, en los veinte documentos y en la torre.** 40 minutos en vez
de cuarenta minutos, 70% en vez de setenta por ciento, 20 a 30 cuentas, 1.000 dólares, 90 días.
Son 598 reemplazos.

- **La prosa sin unidad queda en letra.** "Las dos cosas difíciles", "un solo comentario en
  contra": ahí el número no es un dato, es una manera de hablar.
- **Se arreglaron de paso dos que estaban a mano y quedaban mezcladas**: en el caso de Antonio,
  "50 mil" y "entre 50 y 60 mil" pasaron a 50.000 y a entre 50.000 y 60.000.
- **El agente escribe así de ahora en más**: la regla está en su prompt.
- Las cuatro páginas de scroll (Inicio, Clientes, Programa, Materiales) se regeneraron con lo
  mismo.

---

## 17 de septiembre de 2026 · tarde

Segunda pasada por lo mismo: el reparto interno salió de tres informes más.

- **Antonio.** La conclusión cerraba diciendo que la fecha de las grupales la fija Teo en el
  sign-off, y "Lo que queda sin definir" repetía lo mismo. Ahora la conclusión termina en el
  negocio y lo único sin definir es qué responde la dirección de marketing de IEB. El
  entregable dice "El acceso a las llamadas grupales", sin la fecha que dependa de nadie.
- **Nico.** Igual: la conclusión decía "el frente que queda abierto es de nuestro lado" y
  seguía con quién define qué. Eso vive en la torre, no en su informe.
- **Lucca.** Salió de "Sin definir" si hubo llamadas que no quedaron registradas en Fathom, y
  del recorrido quién agenda la llamada de cierre.
- **Nada se perdió:** los tres frentes internos siguen en la torre, en el campo "Sin definir"
  de cada cliente, que es interno.

---

## 17 de septiembre de 2026

Lo operativo nuestro salió de los documentos que lee el cliente.

- **El caso de Ceci.** Su informe decía que entró al circuito de cierre, que el documento de sign-off
  estaba vacío y lo completa Facu, que el encaje no era este, y que Aye coordina la llamada con Teo.
  Todo eso es operación nuestra y ahora vive donde corresponde, en los accionables CSM.
- **Lo mismo en otros seis.** Andrea, Manu, Sharon, Nico, Scarlett y Lucca tenían hitos escritos en
  lenguaje interno ("entra al circuito de cierre", "teo plantea el sign-off y facu coincide",
  "sin oferta nueva"). Quedaron en criollo y de cara al founder.
- **La fecha que depende de la agenda de Teo salió de "Sin definir"** en los cuatro casos donde
  estaba. Es una tarea nuestra, no una incógnita del caso.
- **El agente tiene la regla nueva.** El circuito de cierre, quién completa el sign-off, de quién
  depende la agenda, si hay oferta nueva y el juicio sobre el encaje van a `entregas.json`, nunca a
  `etapa`, `abierto`, `recorrido.texto` ni `recorrido.hitos`.
- **El generador:** cuando un caso no tiene hitos, el panel deja de mostrar el rótulo "Los hitos"
  vacío y el texto toma todo el ancho.

---

## 17 de septiembre de 2026 · el repo ya se construye solo, y el barrido del 16

Dos cosas. La primera es que el repo, tal como está en GitHub, no se podía regenerar desde
una clonación limpia: los scripts tenían rutas de cuatro carpetas de sesiones viejas
metidas adentro. Eso está arreglado. La segunda es el barrido de las llamadas del 16, que
fue un día cargado.

- **Los nueve builds corren desde cero.** Antes fallaban siete de nueve. `build.py` ejecutaba
  el generador v1 al ser importado, y eso volteaba a `build2.py` y a `build_cartas.py`; ahora
  su cuerpo está detrás de `if __name__ == "__main__"`, que es lo que el propio CLAUDE.md pedía.
  `build_app.py`, `app_shell.py` y `build_site.py` buscaban `contenido/` adentro de `generador/`.
  Y había rutas absolutas a `/home/claude/web`, `/home/claude/founders`, `/home/claude/qualita`,
  `/home/claude/ally` y hasta un `/tmp/claude-0/shell.txt`. Todas salen ahora de la raíz del repo.
- **`build2.py` leía `v2/fichas/` y escribía en `out2/`**, carpetas que en este repo no existen.
  Ahora lee `fichas/` y escribe en `clientes/`, que es lo que dice CLAUDE.md. Por eso hasta hoy
  no regeneraba ningún documento. `app_shell.py` escribía `site/app.html` y ahora escribe
  `index.html`, que es la torre.
- **La fecha del tablero estaba clavada en "16 SEP 2026".** Sale del día en que corre el build,
  como ya pasaba con los días de programa.
- **Seba Martínez es lo que más cambió.** El 16 tuvo la llamada con Franco y salió con la oferta
  parametrizada: ocho semanas, tres pilares, doce a quince cupos, entrada de 997 a 1.200 dólares.
  Lo que queda abierto es el producto, y eso se arma en su 1:1 del viernes 18 a las 9:30.
- **Lucio Labate pasa a frenado, y por un motivo que se arregla.** No le llegan los mensajes del
  grupo. El contacto pasa a privado y lo toma Aye.
- **Quince fichas con el hito del 16 adentro.** De la grupal de Juana salieron Nico, Aaron,
  Bianca, Scarlett, Custom Lab, Lola y Seba; de la revisión del servicio, los ocho que cierran
  más Sofía y Lucio.
- **El handoff de Aye dejó de mandar a agendar llamadas que ya pasaron.** Se reescribieron los
  accionables de Seba, Sofía, Lucio, Lucca, Cecilia, Nico, Lola, Scarlett y Qualita.
- Catorce Updates escritos en Cuentas, y la ficha de Israel Barranco pasó a On Going como
  The Momentum Club, con START el 16/09.

**Para mirar antes de subir:** los arreglos del generador, que son nueve archivos de `generador/`
y es lo más sensible de esta tanda — conviene correr los nueve builds una vez en tu clon y ver que
den lo mismo. Y el documento de Seba, que es con el que entrás a la llamada de mañana.

---

## 16 de septiembre de 2026 · noche · los accionables

Los accionables de nuestro lado estaban mezclando cinco cosas distintas. Quedaron repartidos
en tres lugares y de 68 líneas pasaron a 8.

- **Accionables CSM.** Lo que antes se llamaba "la entrega" es la lista de Aye: el documento
  que le corresponde a cada cliente, qué hacer con él y qué coordinar. Ahí entraron 18
  líneas que figuraban como tareas de Facu y son operativas: agendar, mandar una carta,
  mandarle a Franco el resumen antes de su llamada.
- **Arriba de cada cliente, el resumen de su radiografía.** El cuello, la métrica y en qué
  día está, para ubicarse sin abrir el documento. Va en la torre y en el documento de Aye.
- **Quién toma cada caso.** "Franco define la oferta", "Juana toma la narrativa", "grupales
  martes, jueves y viernes" dejó de ser checklist: es un rótulo, aparece en la ficha de cada
  cliente y junto en la sección Adentro de Cáscara.
- **Salió todo lo que ya está escrito en el documento del founder.** Los ángulos de
  comunicación, el bloque del profile funnel, el roadmap con punto de llegada: eso es el
  contenido del informe.
- **Salieron los traspasos de contexto a Franco.** En vez de pasarle transcripts, queda un
  mensaje corto antes de su llamada. El paso siguiente es la tabla de llamadas con su link
  adentro de cada cliente, que todavía falta.
- **Quedaron marcadas tres excepciones declaradas**, que van contra el criterio done with
  you y se sostienen igual: la pauta y los guiones de Custom Lab, y las automatizaciones de
  mail y la edición de regalo de Bianca.
- Cecilia: se corrigió el cuello, que estaba escrito explicando lo que no es.

---

## 16 de septiembre de 2026 · noche

- **Iñaki Efe sale de Founders.** Es cliente de 0800, así que no va en el circuito: se fue del
  handoff y de los accionables. En la lista de limpieza de Notion queda la línea para sacarle
  la etiqueta de Founders en la base.

---

## 16 de septiembre de 2026 · tarde

Entró un cliente nuevo y Qualita quedó contada como corresponde.

- **The Momentum Club es cliente desde hoy.** Israel Barranco y Natalia Zabaleta arrancaron
  el 16 de septiembre. Están completando los Founder Insights y después va la Clarity Call,
  que Aye puede coordinar. Ya aparece en la torre, en los accionables y en el handoff: son
  veintidós clientes.
- **Qualita se cuenta desde abril, no desde agosto.** El caso arrancó el 24 de abril como
  Rafael Lizarraga, se frenó por viaje y retomó el 20 de agosto. El freno no consume días
  del programa, así que ahora la ficha dice lo que pasó: lleva 146 días con nosotros y va
  por el día 77 de los noventa. (El 12 de junio como fecha de corte del freno sale de la
  última actualización cargada en Notion: falta confirmar.)
- **El contador dejó de estar clavado.** Estaba fijo en el 12 de septiembre, así que todos
  los clientes venían cuatro días atrasados y el que entraba hoy daba negativo.
- **Se fue "handicap" y "camada" de las páginas de scroll.** Inicio, Clientes, Programa y
  Materiales decían handicap promedio y "la camada": ahora dicen puntaje y clientes.

---

## 16 de septiembre de 2026

La torre se reordenó entera y Cecilia quedó con su informe de cierre.

- **La torre cambió de secciones.** Eran cinco y ahora son cuatro: **Home** dejó de listar
  clientes y es una portada de tres tarjetas; **Clientes** quedó igual; **Accionables** es
  nueva y junta tres cosas en un conmutador —la entrega de cada documento, lo que ejecuta
  cada founder y lo que queda de nuestro lado—; **Biblioteca** junta lo que antes eran
  Programa y Material.
- **Se puede volver siempre.** Arriba de cada pantalla hay migas (Home / Clientes / Fulano)
  y en el celular la flecha de atrás ahora aparece en todos lados.
- **Cecilia Belotti tiene informe de cierre.** Reemplaza al PDF de agosto: suma el giro al
  workshop del 13/08 y la propuesta de Tantasiña. Su fecha de inicio quedó en el 23 de marzo,
  así que va por el día 173 y no por el 10.
- **Los accionables de Cáscara salieron de los documentos de cliente.** Ahora cada informe
  muestra solo lo que hace el founder. Lo nuestro vive en la torre. Se regeneraron los veinte.
- **Se fue la palabra camada.** Founders es evergreen: en todo texto dice clientes. También
  se corrigieron los datos que hablaban de cupos cerrados.
- **La reunión que cierra una oferta la toma Franco, siempre.** Estaba escrito como
  "coordinar con Facu y Teo" en el caso de Aye.
- **Entró lo de la llamada con Aye:** a Ceci no se le manda el documento, lo presenta Teo;
  los grupos de WhatsApp de los que cierran se cierran; el seguimiento de accionables va por
  el grupo mientras está abierto; y el upselling es solo Lucca, con Sharon condicionada a que
  lance su B2C.
- **Arreglos.** El visor de documentos tapaba la app entera con un panel vacío fuera de
  Claude. Y los botones de descargar ahora funcionan también en la web, no solo adentro del
  artifact.
- **Quedó escrito, sin activar,** un auto-push para la Mac en `scripts/`. Está apagado a
  propósito: el push se sigue haciendo a mano.

**Para mirar antes de subir:** la sección Accionables, que es la que más cambió, y el
informe de Cecilia, que es documento nuevo.
