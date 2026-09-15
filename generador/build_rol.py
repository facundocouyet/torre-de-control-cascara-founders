# -*- coding: utf-8 -*-
"""El rol de líder de Cáscara Founders — proceso y ritmo."""
import os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # la raíz del repo
from _base import CSS, S, P, CITA, PASOS, MARCO, TABLA, BLOQ, CARRIL, META, esc

CSS += """
.sino{margin-top:30px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:#DBD7D2;border:1px solid #DBD7D2}
.sino > div{background:#ECEAE4;padding:24px 22px}
.sino .et{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85;margin-bottom:16px}
.sino ul{margin:0;padding:0;list-style:none}
.sino li{font-size:17px;line-height:1.5;padding:9px 0 9px 22px;position:relative;border-top:1px solid #DBD7D2}
.sino li:first-child{border-top:0}
.sino li:before{content:"";position:absolute;left:0;top:16px;width:8px;height:1.5px;background:#171717}
.sino li b{font-weight:800}
.ritmo{margin-top:28px}
.ritmo .r{display:grid;grid-template-columns:150px minmax(0,1fr);gap:28px;border-top:1px solid #DBD7D2;padding:20px 0}
.ritmo .r:first-child{border-top:2px solid #171717}
.ritmo .cu{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#171717;font-weight:800;padding-top:3px}
.ritmo .tx{font-size:18px;line-height:1.55;max-width:60ch}
.ritmo .tx b{font-weight:800}
@media (max-width:640px){ .sino{grid-template-columns:1fr} .ritmo .r{grid-template-columns:1fr;gap:8px} }
"""

def SINO(si, no, et_si="Es suyo", et_no="No es suyo"):
    a="".join(f'<li>{x}</li>' for x in si); b="".join(f'<li>{x}</li>' for x in no)
    return (f'<div class="sino"><div><div class="et">{et_si}</div><ul>{a}</ul></div>'
            f'<div><div class="et">{et_no}</div><ul>{b}</ul></div></div>')

def RITMO(xs):
    return '<div class="ritmo">' + "".join(
        f'<div class="r"><div class="cu">{c}</div><div class="tx">{t}</div></div>' for c,t in xs) + '</div>'

partes=[]

partes.append(S("00","Para qué es este documento",
  P("Cáscara Founders tiene cinco frentes y cinco personas. Este documento dice cuál es el tuyo: qué decidís vos, "
    "qué decide otro, con qué ritmo corre tu semana y qué parte de todo eso puede sostener un agente en vez de "
    "tu memoria.") +
  P("Está escrito para leerse una vez y después consultarse. El resto del proceso —las diez llamadas, las "
    "orientaciones, el puntaje, las grupales— vive en el documento de proceso; acá está solamente tu lugar adentro "
    "de ese proceso.","sub")))

partes.append(S("01","Qué decidís vos",
  P("Lo que tenés no es un frente: es <b>la responsabilidad de Cáscara Founders</b>. El programa responde a vos. "
    "Adentro de esa responsabilidad trabajás sobre la entrega del servicio y sobre la estructura, la capacidad y los "
    "números, y el resto tiene dueño propio: las decisiones que le corresponden a cada uno se toman ahí.") +
  SINO([
    "<b>La responsabilidad del programa.</b> Founders responde a vos: lo que promete, lo que entrega y qué pasa "
    "cuando algo se cae.",
    "<b>La forma de la oferta.</b> Qué incluye el día 90, qué queda afuera y cómo se entrega. El precio se define "
    "con Franco, que es el growth partner.",
    "<b>El criterio de admisión.</b> Las llamadas de venta las toma el departamento comercial; lo que vos fijás es "
    "el criterio con el que filtran, porque el founder al que no le va a salir se evita ahí y no adentro.",
    "<b>La orientación de cada founder</b> en la semana 3, y el cambio de orientación si el caso lo pide.",
    "<b>Qué módulos se desbloquean y cuándo.</b> Nadie avanza de bloque sin que vos lo apruebes en una llamada.",
    "<b>Cómo cierra cada founder:</b> sign off, renovación con módulo, o growth partner.",
    "<b>Los conflictos.</b> Todo lo que se traba entre un founder y el equipo termina en vos.",
  ],[
    "<b>Las llamadas de venta.</b> Las toma el departamento comercial. No las tomás vos ni las toma Teo.",
    "<b>El growth del founder.</b> Franco es growth partner de todo Cáscara y entra a Founders con ese rol: oferta, "
    "pricing, demanda y comercial son suyos de punta a punta, no una consulta puntual.",
    "<b>La narrativa, los ángulos y el calendario.</b> Fede y Juana.",
    "<b>Las llamadas de onboarding y de sign off.</b> Las hace Teo, incluso cuando el informe lo escribiste vos.",
    "<b>La satisfacción del founder.</b> Aye arma y sostiene el seguimiento: testimonios, formularios y el estado de "
    "cada persona. Teo le da el soporte operativo.",
    "<b>Los guiones.</b> Los escribe el founder. Cáscara deja el criterio y un ejemplo.",
  ]) +
  P("La regla que ordena las dos columnas: <b>Cáscara diseña el sistema y baja la estrategia, el founder ejecuta.</b> "
    "Cada vez que algo se corre de ese eje —producir contenido, operar una landing, entregar el servicio del "
    "cliente— es una señal de que la oferta necesita una aclaración, no de que hace falta más trabajo.","sub")))

partes.append(S("02","El ritmo",
  P("Founders se vende en evergreen, así que no hay una camada que arranca y termina junta: cada founder corre su "
    "propio reloj de noventa días desde el día que completa el onboarding. Tenés cinco de sus diez llamadas y sos el "
    "que escribe. El ritmo existe para que eso entre cuando hay veinte relojes distintos corriendo a la vez.") +
  RITMO([
    ("Cada mañana","El agente te deja tres cosas antes de que empieces: las llamadas de hoy con el link listo, los "
      "accionables que vencieron y quién quedó esperando algo tuyo. Nada más."),
    ("Lunes","El pulso: quién avanzó, quién está frenado, quién entra esta semana y quién llega al día 30, al 60 o al "
      "90. De ahí salen las llamadas que agendás y a quién le toca documento."),
    ("Martes a jueves","Tus uno a uno. Las grupales corren solas: martes con Teo, jueves con Juana, viernes con Fede. "
      "Entrás a una grupal cuando el caso lo pide, no por calendario."),
    ("Viernes","Escribís. Las radiografías del día 30 y los informes de cierre salen acá, con el material ya juntado "
      "por el barrido de la semana. Es el bloque que conviene no negociar."),
    ("Día 30","Primera radiografía y roadmap del mes siguiente. Cierra siempre con lo mismo: oferta construida, ICP "
      "identificado, ángulos de comunicación y profile funnel acomodado."),
    ("Día 60","Segunda radiografía. Mismo documento, un mes después: qué se movió contra lo que el roadmap decía, y "
      "el plan del último tramo."),
    ("Día 90","Informe de cierre, paquete de entregables y recomendación. Vos escribís, Teo presenta."),
    ("Cada tres meses","Se revisan los cortes del puntaje, el precio y la forma de la oferta con todos los founders "
      "activos a la vista. En evergreen no hay fin de camada, así que la revisión se agenda."),
  ])))

partes.append(S("03","Las llamadas que son tuyas",
  P("Cinco por founder, y cada una tiene un trabajo distinto. Saber cuál es evita que se conviertan en reuniones de "
    "actualización.") +
  TABLA(["Cuándo","Qué se resuelve","Con qué llega el founder"],[
   ["Semana 1","<b>Clarity Call.</b> Diagnóstico y cuello de botella. Sale la conclusión que va a Franco.",
    "Founder Insights y los formularios completos. Sin eso no hay llamada: el día 5 escala Teo, el día 7 se corre."],
   ["Semana 3","<b>Selección de foco.</b> Una sola orientación, con el puntaje adelante.",
    "El one-pager de oferta y el ICP que salieron de la llamada con Franco."],
   ["Día 30","<b>Primera radiografía y roadmap.</b> Qué salió, qué no, y el plan del mes que viene.",
    "Las cartas del primer bloque completadas."],
   ["Día 60","<b>Segunda radiografía.</b> Mismo documento un mes después: qué se movió contra el roadmap del día 30 "
    "y el plan del último tramo.",
    "Las cartas del segundo bloque y el proceso de entrega mapeado con horas reales."],
   ["Mes 3","<b>Ejecución sobre el foco.</b> La última corrección antes del cierre.",
    "Los números del tramo: piezas, conversaciones, ventas."],
  ]) +
  P("Son tres documentos en los noventa días y siempre el mismo formato: radiografía al día 30, radiografía al día 60 "
    "e informe de cierre al día 90. Las dos primeras las presentás vos en la llamada; el cierre lo escribís vos y lo "
    "presenta Teo.","sub") +
  P("El link lo manda el agente el día anterior por WhatsApp junto con la línea de con qué hay que llegar. Si el "
    "founder no llega con eso, la llamada se reagenda: es la misma regla que aplica a los documentos.","sub")))

partes.append(S("04","La torre de control",
  P("Es la página donde viven los founders activos: los veintidós casos ordenados por puntaje, el detalle de cada uno con su "
    "cuello de botella y sus accionables, el programa y el mapa de cartas. Arriba está siempre el que más atención "
    "necesita. Se actualiza sola todas las mañanas.") +
  BLOQ([
    ("Lo que se actualiza solo",
     "El barrido diario toma las llamadas nuevas de Fathom, agrega el hito al recorrido de cada ficha, ajusta "
     "únicamente lo que esa llamada cambió, recalcula el puntaje y vuelve a publicar la página y los documentos. "
     "También escribe el Update en la ficha de Cuentas en Notion."),
    ("Lo que depende de vos",
     "El puntaje lo calcula el sistema, pero los cortes y los anclajes los fijás vos. La orientación se propone "
     "desde el eje más bajo y la confirmás vos. El desbloqueo de módulos se marca en la llamada. Y lo que la llamada "
     "no dijo queda escrito como falta confirmar, en vez de completarse."),
    ("La fecha de inicio",
     "El reloj de los noventa días arranca el día que se completa el onboarding, o sea cuando Teo hace esa llamada. "
     "Esa fecha se carga en Cuentas en ese momento y es la que hace que el día 30, el 60 y el 90 se puedan anticipar "
     "en vez de descubrirse. Hoy falta en casi todas las fichas."),
  ])))

partes.append(S("05","Dónde trabaja cada uno",
  P("Cuatro superficies, y cada una tiene un dueño. Cuando algo vive en dos lugares, se desincroniza.") +
  TABLA(["Superficie","Para qué","Quién la mantiene"],[
   ["<b>Cuentas</b>, en Notion","La ficha de cada cliente: paso, fechas, Updates. Es la fuente de verdad del padrón.","Teo carga el alta y las fechas. El barrido escribe los Updates."],
   ["<b>La torre de control</b>","El estado de cada founder y los documentos. Es lo que mirás vos y lee el equipo.","El barrido diario. Vos confirmás orientación y desbloqueos."],
   ["<b>El OS del cliente</b>, en Notion","Lo que el founder abre: roadmap, formularios, materiales, cartas asignadas.","Aye, sobre el roadmap del servicio."],
   ["<b>El seguimiento de satisfacción</b>","Cómo va cada founder más allá del avance: testimonios, formularios de servicio y señales de que algo se está enfriando.","Aye lo arma y lo sostiene. Teo le da el soporte operativo."],
   ["<b>El grupo de WhatsApp</b>","El canal con el founder. También es insumo: es la fuente que más cambió un diagnóstico.","Teo y Aye. Se avisa al founder que queda registrado."],
  ]) +
  P("Aye trabaja sobre las tres últimas: el OS de cada cliente, el contacto y el seguimiento de satisfacción. Adentro "
    "de Founders le corresponde operaciones y productividad, que las cartas asignadas se completen, y la estructura "
    "de satisfacción persona por persona, que hasta hoy no tenía dueño.","sub")))

partes.append(S("06","Cómo se manda la documentación",
  P("Hay dos formas y conviene no mezclarlas.") +
  CARRIL([
    ("Al equipo","El handoff","Una página con los clientes, el accionable de cada uno y su documento con botón de "
      "descarga. Sale cuando hay un lote —un tramo, un grupo de informes, varios cierres juntos— y reemplaza al "
      "mensaje largo. Aye descarga, manda y coordina desde ahí."),
    ("Al founder","El documento solo","Su radiografía o su informe, sin contexto de los demás. En los que siguen en "
      "curso se manda antes de la llamada. En los cierres se muestra en la llamada y se manda después."),
  ]) +
  P("Los dos salen del mismo lugar, así que no hay que armarlos aparte: el handoff toma los documentos que ya generó "
    "el barrido. Lo que cambia es el envoltorio.","sub")))

partes.append(S("07","Cómo se presenta un informe",
  P("Un informe se lee en paneles, se scrollea hacia la derecha y se imprime a PDF desde el navegador. Doce paneles: "
    "dónde estás hoy, la lectura, lo que pasó, las respuestas, lo que te entregamos, la conclusión, a dónde vamos, el "
    "roadmap, los accionables y la carta final.") +
  PASOS([
    "<b>Un solo cuello de botella por caso.</b> Si hay dos, todavía no está leído.",
    "<b>Se dice lo que la cosa es, directo.</b> Nada de explicar algo anteponiendo lo que no es.",
    "<b>Cada founder queda ubicado en su etapa.</b> Uno que recién empieza y uno que cierra no leen lo mismo.",
    "<b>El puntaje queda adentro.</b> Va en las radiografías y sale de los informes de cierre, que son los que se "
    "mandan.",
    "<b>La autocrítica de Cáscara no va en el documento del cliente.</b> Lo que hay que corregir de nuestro lado va "
    "en la versión interna, separada.",
    "<b>Nada inventado.</b> Lo que la llamada no dijo se escribe como falta confirmar.",
  ]) +
  MARCO("La razón de ser del formato",
    "El informe existe para que el founder pueda ejecutar sin vos adelante. Por eso termina en accionables con "
    "fecha y en una carta, y no en un resumen de lo que hicimos.")))

partes.append(S("08","Procesos de la oferta de Founders",
  P("Hasta acá está lo que hace cada founder. Esto es lo otro: los procesos que hacen que la oferta funcione, que son "
    "de Cáscara y se repiten con cada founder que entra. Cada uno tiene un dueño, un disparador y algo que queda hecho. "
    "Cuando uno de estos falla, el síntoma aparece en un cliente y parece un problema de ese cliente.") +
  TABLA(["Proceso","Se dispara con","Qué queda hecho","Dueño"],[
   ["<b>Admisión</b>","La llamada de venta","La decisión de si entra o no, contra el criterio escrito. El founder al que no le va a salir se detecta acá y no adentro.","Departamento comercial, con el criterio de Facu"],
   ["<b>Alta en 48 horas</b>","La confirmación de pago","Contrato, ficha en Cuentas con fecha de inicio, OS del cliente, grupo de WhatsApp, acceso, y los formularios pedidos.","Teo"],
   ["<b>Formularios antes de la Clarity</b>","El alta","Founder Insights y los formularios completos. Día 5 se escala, día 7 se corre la llamada.","Teo"],
   ["<b>Asignación de cartas</b>","Cada 1:1 de Facu","El bloque siguiente desbloqueado y las cartas cargadas en el OS del cliente.","Facu asigna, Aye carga"],
   ["<b>Seguimiento de cartas</b>","La asignación","Cuáles se completaron y cuáles no. Es la medida real de avance del programa.","Aye"],
   ["<b>Barrido de llamadas</b>","Cada llamada grabada","El hito en la ficha, los accionables al día, el Update en Cuentas y la torre republicada.","El agente"],
   ["<b>Radiografía del día 30</b>","El día 30 de cada founder","El documento con el roadmap del mes siguiente y la orientación confirmada.","Facu escribe"],
   ["<b>Cierre del día 90</b>","El día 90","Informe de cierre, paquete de entregables, recomendación y la fecha hasta la que quedan las grupales.","Facu escribe, Teo presenta"],
   ["<b>Handoff al equipo</b>","Un lote de documentos listo","La página con cada cliente, su accionable y su documento descargable.","Facu arma, Aye ejecuta"],
   ["<b>Seguimiento de satisfacción</b>","El arranque del programa","Cómo va cada founder más allá del avance: formulario de servicio, señales tempranas y el estado de la relación.","Aye, con soporte operativo de Teo"],
   ["<b>Captura del caso</b>","Un cierre que salió bien","El testimonio y el caso documentado. Es lo que alimenta la venta, que en evergreen corre todo el tiempo.","Aye lo documenta, Teo lo pide en la llamada"],
   ["<b>Revisión de la oferta</b>","Cada tres meses","Los cortes del puntaje revisados, el precio con Franco y la forma de la oferta.","Facu"],
  ]) +
  P("Los dos que recién arrancan son el <b>seguimiento de cartas</b> y el <b>seguimiento de satisfacción</b>, los dos "
    "de Aye. Son los que más se notan cuando faltan: sin el primero el estado de cada founder hay que preguntarlo, y "
    "sin el segundo un founder se enfría sin que nadie lo vea hasta el cierre. Y como la venta es evergreen y corre "
    "todo el tiempo, la captura del caso deja de ser algo que se hace al final de un tramo y pasa a ser continua.","sub")))

partes.append(S("09","Qué hace el agente",
  P("Corre de lunes a viernes a las ocho y media, y es el mismo que ya venía haciendo el barrido de la torre. Ahora "
    "además te lleva el ritmo. La regla que sigue es la que vos pusiste: resuelve adentro del sistema y te deja "
    "tres líneas, sin dejarte trabajo para operar a mano.") +
  BLOQ([
    ("Todos los días, antes de que arranques",
     "Lee el calendario y Fathom. Te deja las llamadas de Founders de hoy con el link y la línea de con qué llega "
     "cada uno; los accionables que vencieron y de quién son; y quién quedó esperando algo tuyo hace más de tres "
     "días. Manda por WhatsApp el recordatorio de las llamadas del día siguiente con lo que hay que traer."),
    ("Después de cada llamada",
     "Corre el seguimiento: escribe el hito en la ficha, actualiza los accionables de los dos lados, deja el Update "
     "en Cuentas y prepara el mensaje corto para el grupo. Recalcula el puntaje y republica la torre."),
    ("Los lunes, además",
     "El pulso: quién avanzó y quién está frenado contra la semana anterior, quién entra esta semana y quién llega al día 30, al 60 o al "
     "día 90 en los próximos siete días, qué llamadas faltan agendar y qué documentos hay que escribir. Y una sola "
     "decisión, si la hay."),
    ("Lo que no hace",
     "No te deja borradores para que corrijas y mandes. No agenda nada sin pedirlo. No inventa lo que la llamada no "
     "dijo. Y no te avisa dos veces de lo mismo."),
  ])))

partes.append(S("10","Lo que todavía no tiene dueño",
  P("Tres cosas que hoy se resuelven sobre la marcha y convendría que dejen de hacerlo.") +
  PASOS([
    "<b>Las cartas de cada departamento.</b> Quedó acordado que cada dueño escribe las suyas. Hasta que exista una "
    "carta madre en blanco con las preguntas que cualquier carta responde, van a seguir saliendo de vos.",
    "<b>El set obligatorio del primer mes.</b> Hoy las cuarenta cartas parecen iguales. Marcar las cinco que son "
    "obligatorias convierte el catálogo en un programa.",
    "<b>La fecha de inicio cargada en el momento del onboarding.</b> Es el dato que permite anticipar el día 30, el "
    "60 y el 90 en vez de descubrirlos.",
    "<b>Las clases pregrabadas que acompañan la primera entrega de cards.</b> Un video por dueño —Franco, Facu, Fede "
    "y Teo— que sale apenas termina el onboarding, para que el founder llegue a la primera grupal sabiendo qué se "
    "trabaja ahí. Lo encara Aye con cada uno.",
  ])))

cuerpo="".join(partes)

HTML=f"""<title>El rol de líder de Founders</title>
<style>{CSS}</style>
<div class="hoja">
<div class="caja">Cáscara Founders · proceso interno</div>
<h1>El rol de líder<br>de Founders</h1>
<p class="bajada">Qué decidís vos, con qué ritmo corre la semana, dónde trabaja cada uno y qué parte de todo eso
sostiene un agente en vez de tu memoria.</p>
<div class="tira">
  <div><div class="et">Frentes propios</div><div class="tx">Entrega y estructura</div></div>
  <div><div class="et">Llamadas por founder</div><div class="tx">5 de 10</div></div>
  <div><div class="et">El agente corre</div><div class="tx">L a V, 8:30</div></div>
  <div><div class="et">Versión</div><div class="tx">15 de septiembre de 2026</div></div>
</div>
{cuerpo}
<div class="pie"><div><span class="sello">C</span></div>
<div>Cáscara Founders · el rol de líder</div></div>
</div>"""

open(os.path.join(RAIZ,'rol-lider-founders.html'),'w',encoding='utf-8').write(HTML)
print("ok",len(HTML))
