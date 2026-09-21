# -*- coding: utf-8 -*-
"""Correcciones de Facu sobre los accionables del 21/09."""
import io, json, sys
P = sys.argv[1]
d = json.load(io.open(P, encoding='utf-8'))
F = {f['nombre']: f for f in d['filas']}

def set_items(n, items):
    F[n]['accionables'] = items

# ── la regla: en los nueve sign off el informe no se manda ──
d['regla_signoff'][4] = ('<b>El documento no se manda: se presenta en la llamada.</b> En los nueve es igual. '
  'Se lo muestra Teo mientras se lo cuenta; mandarlo antes deja al founder sacando conclusiones solo.')

# ── Cecilia: el documento de sign off ya está hecho ──
set_items('Cecilia Belotti', [
 'Coordinar la llamada de cierre con Teo. Es lo único que hay que hacer con este caso.',
 'Preguntarle en qué quedó Tantasiña: la propuesta vence el <b>viernes 19</b> y el arranque propuesto es la '
 'semana del 22. Es el dato con el que Teo llega a la llamada.',
 'Teo marcó que a Ceci <b>no</b> le pide el formulario de feedback: su perfil no es el que nutre al programa.',
])

set_items('Antonio Mazzello', [
 'Coordinar el offboarding <b>con Teo</b> —esta llamada no la hace Facu— y avisarle que el informe es una '
 '<b>versión nueva</b>, distinta de la que se armó en septiembre.',
 'Antes de la llamada: responder el mensaje de Antonio que quedó sin contestar. Es lo primero.',
 'Confirmar con Teo hasta qué fecha exacta mantiene el acceso a las grupales.',
])

set_items('Manuel Bruzzone', [
 'Coordinar la llamada de sign off con Teo y decirle en el mismo mensaje hasta cuándo tiene las grupales.',
 'Preguntarle si la base de leads y las automatizaciones llegaron a implementarse: es el único dato que falta '
 'para cerrar el informe.',
])

# Andrea: sin nada de Franco ni de estar cruzada
set_items('Andrea Saturno', [
 'Ofrecerle el sprint hasta fin de septiembre: grupales más <b>una llamada extra con Facu</b>. Si la pide, '
 'coordinarla con Facu y agendarla.',
 'Pedirle la fecha del viaje y, con eso, la fecha de la primera Onfire Session.',
 'Coordinar el offboarding con Teo.',
 'De la grupal de procesos del 17/9 quedó el <b>mapa de check-ins</b> para el jueves 24: dónde se inserta cada '
 'uno, qué pregunta, para qué se usa y dónde cae el dato.',
])

# Lucca: sin llamada con Franco; el upsell lo hace Teo en el sign off
set_items('Lucca Sorgoni', [
 'Coordinar con Teo la llamada de sign off: ahí mismo Teo le hace el upselling.',
 'Capturar el testimonio en esa llamada.',
])
F['Lucca Sorgoni']['upselling'] = ('Sí. Es el único de los nueve, y lo hace Teo en la misma llamada de sign off. '
  'No hay llamada aparte con Franco.')

set_items('Sharon Palacio', [
 'Coordinar con Teo la llamada <b>en formato caso de éxito</b>, que es como se decidió cerrarla.',
 'Capturar el testimonio en esa misma llamada.',
 'Ofrecerle seguir entrando a las grupales como referente.',
 'Confirmar con Facu cuántas llamadas uno a uno quedan antes del cierre y agendarlas (falta confirmar).',
 'De la grupal de procesos del 17/9 quedó el <b>mapa de check-ins</b> para el jueves 24: dónde se inserta cada '
 'uno, qué pregunta, para qué se usa y dónde cae el dato.',
])

set_items('Scarlett Montilla', [
 'Agendar <b>una llamada más con Franco</b>: de ahí sale el precio de la mentoría, que es lo único que falta.',
 'Recién después de esa llamada, coordinar el offboarding con Teo.',
 '<b>El lanzamiento ya está bajado a 3 etapas</b>: workshop presencial en un mes, apertura de postulaciones a '
 'una mentoría grupal de 4 a 6 semanas, y uno a uno de validación. Está consiguiendo locación.',
 'Bajó el ritmo de publicación por el rebranding. La salida que le dio Juana es documentar el propio rebranding.',
 'De la grupal de procesos del 17/9 quedó el <b>mapa de check-ins</b> para el jueves 24: dónde se inserta cada '
 'uno, qué pregunta, para qué se usa y dónde cae el dato.',
])

set_items('Nicolás Lozada', [
 'Pedirle a Teo que hable con él <b>ahora</b>, antes de cualquier otra cosa.',
 'El sign off va <b>después</b> del sprint comercial, no antes. Agendarlo recién cuando el sprint termine: ahí '
 'Teo le presenta el informe, que incluye la mini orientación al lanzamiento y el sprint comercial.',
 '<b>Ya lanzó.</b> El 15/9 subió el primer video de contexto de la marca y arrancó a documentar 30 días; al '
 'cierre de esos treinta abre cupos de acompañamiento.',
])

set_items('Ayelén Cerqueira', [
 'Agendarle ella misma la reunión con <b>Franco</b>: es la que cierra la oferta, nombre y precio. Esa llamada la '
 'toma Franco siempre.',
 'Recién después de esa llamada, coordinar el offboarding con Teo.',
])

# ── Sofía: van las cartas ──
set_items('Sofía Galvis Montoya', [
 'Mandar la radiografía con el roadmap. <b>Va por el día 82 de los 90</b>, así que esto no se puede correr más.',
 'Mandarle las tres cartas: <b>Oferta</b>, <b>ICP y mecanismo</b> y <b>Ángulos de comunicación</b>. Las completa '
 'antes de la llamada con Franco y son lo que esa llamada usa.',
 'Agendar la llamada con <b>Franco</b>: ahí se define la oferta y la fecha del lanzamiento del programa de '
 'educación. Esta llamada es la de ella, no el sign off con Teo.',
 'Resolver el desfasaje de fechas: los 90 días caen alrededor del 20 de septiembre y en Cuentas tiene FINISH el '
 '31 de octubre. O el 31 se dice como extensión, o las dos fechas coinciden.',
])

# ── Bianca: el documento ya salió, queda el seguimiento ──
set_items('Bianca Antonini', [
 '<b>Los dos documentos ya se mandaron</b> —la radiografía y el de Eclipse y los anillos—. Hacerle el '
 'seguimiento hasta que devuelva: está pendiente su respuesta.',
 'Agendar la <b>1:1 de Franco con Bianca esta semana</b>: es donde se cierra el pricing del anillo llave.',
 'Pedirle a Teo los contenidos del Cowork editados para regalárselos.',
 'Pedirle a Bianca cuánta gente hay hoy en la comunidad de WhatsApp.',
 'Pasarle el ejemplo de la serie de contenido de Delfi Ferro.',
 'De la grupal de procesos del 17/9 quedó el <b>mapa de check-ins</b> para el jueves 24: dónde se inserta cada '
 'uno, qué pregunta, para qué se usa y dónde cae el dato.',
])

# ── Matías: la 1:1 del viernes 18 ya se hizo ──
set_items('Matías Morales', [
 '<b>La 1:1 con Facu ya se hizo el viernes 18.</b> Ahí Facu le presentó el análisis y le marcó el camino.',
 'Mandar la radiografía con el roadmap.',
 'Mandarle las dos cartas: <b>ICP y mecanismo</b> y <b>Ángulos de comunicación</b>.',
 'Pedirle <b>cuáles son los 2 clientes que cerró</b>, por qué montos y con qué alcance prometido: sin eso el '
 'roadmap de entrega no se puede cerrar.',
 'Agendar con Facu el roadmap de lanzamiento y con Teo el de entrega de servicio.',
 'Llega al <b>día 90 el 29 de septiembre</b> y en Cuentas tiene FINISH el 31/10. O el 31 se dice como extensión, '
 'o las dos fechas coinciden.',
])

# ── Sebastián: la 1:1 del 18 ya se hizo; van las dos cartas ──
set_items('Sebastián Martínez', [
 '<b>La 1:1 con Facu ya se hizo el viernes 18.</b> Ahí se armó el producto: onboarding, recorrido del cliente '
 'semana a semana, seguimiento y el resultado mínimo que el programa garantiza.',
 'Mandar la radiografía con el roadmap.',
 'Mandarle las dos cartas: <b>ICP y mecanismo</b> y <b>Ángulos de comunicación</b>. Van juntas y se devuelven '
 'completas antes de la llamada con Franco.',
 'Agendar la <b>segunda llamada con Franco para la semana del 29</b>: ahí se cierran la fecha de lanzamiento, el '
 'precio exacto y los entregables.',
 'Después de Franco va la llamada con Fede, que baja los ángulos al calendario de contenido.',
 '<b>La llamada con Franco del 16/9</b> dejó los parámetros: 8 semanas, 3 pilares, 12 a 15 cupos y precio de '
 'entrada entre 997 y 1.200 dólares.',
])

# ── Lucio: la 1:1 del 18 ya se hizo; la carta es Profile funnel ──
set_items('Lucio Labate', [
 '<b>La 1:1 con Facu ya se hizo el viernes 18.</b>',
 '<b>Escribirle por privado, no por el grupo: no le llegan los mensajes.</b> Es lo primero y lo bloquea todo lo '
 'demás.',
 'Mandar la radiografía con el roadmap.',
 'Mandarle la carta <b>Profile funnel</b>, con la lista de tareas del perfil de Instagram.',
 'Agendar la llamada con Franco para cerrar la oferta: la fecha era el 17 de septiembre y esa llamada no consta '
 'agendada.',
 'El foco del tramo es cerrar la oferta y sacar <b>un mínimo de 10 piezas</b>: con menos de diez no se evalúa '
 'nada.',
])

# ── Aaron: una sola línea de cartas, con las tres ──
set_items('Aaron Aiello', [
 'Mandar la radiografía con el roadmap.',
 'Mandarle las tres cartas: <b>Pasaporte digital</b>, <b>Ángulos de comunicación</b> y <b>Proceso de entrega '
 'repetible</b>. El pasaporte es el entregable distintivo del caso.',
 'Mandarle la plantilla del formulario de feedback para auditar a los clientes actuales.',
 'Coordinar con Fede el seguimiento de contenido, que acá va con Aaron como personaje.',
])

# ── Custom Lab: la llamada de Franco ya fue; ahora la 1:1 con Facu ──
set_items('Piero Medina y Juan — Custom Lab', [
 '<b>La llamada con Franco ya se hizo el 18/9.</b> De ahí salió la radiografía actualizada.',
 'Mandar la radiografía actualizada.',
 'Agendar la <b>1:1 con Facu para el 2 de octubre</b>: es el punto B del tramo.',
 'Cargar la ficha de la segunda persona y conseguir el apellido de Juan, que falta en la base.',
 'Preguntar cuánto pueden poner por mes en pauta y quién la opera.',
])

# ── Qualita: la 1:1 del 18 ya se hizo ──
set_items('Qualita Studio', [
 '<b>La 1:1 de Rafa con Facu ya se hizo el viernes 18.</b>',
 'Mandar los dos documentos: la radiografía y las cartas del tramo.',
 'Las cartas son los accionables que ejecutan antes de la próxima reunión.',
 'Avisar que el documento de Qualita tiene un panel que desborda y hay que rehacerlo antes de mandarlo.',
 'Borrar las dos fichas duplicadas de Rafael Lizarraga que quedaron en la base.',
])

json.dump(d, io.open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('filas:', len(d['filas']), '· accionables:', sum(len(f['accionables']) for f in d['filas']))
