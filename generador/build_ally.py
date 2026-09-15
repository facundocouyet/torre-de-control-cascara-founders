# -*- coding: utf-8 -*-
"""Handoff para Aye: repaso de clientes, accionables y documentos."""
import sys, io, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # la raíz del repo
from _base import CSS, S, P, CITA, PASOS, MARCO, TABLA, BLOQ, esc
from _base import INK, DEEP, PAPER, PAPER2, GREY, GREY2, LINE, ROJO, DISP, SERIF

CSS += """
.cli{margin-top:0}
.cli .fila{border-top:1px solid #DBD7D2;padding:26px 0}
.cli .fila:first-child{border-top:2px solid #171717}
.cli .top{display:flex;justify-content:space-between;align-items:baseline;gap:18px;flex-wrap:wrap}
.cli .nom{font-size:25px;font-weight:800;letter-spacing:-.028em;line-height:1.1}
.cli .est{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85;
  white-space:nowrap;font-variant-numeric:tabular-nums}
.cli .pro{font-size:16px;color:#6A6A66;margin-top:6px;max-width:64ch;line-height:1.45}
.cli .acc{margin:16px 0 0;padding:0;list-style:none}
.cli .acc li{font-size:17.5px;line-height:1.5;padding:7px 0 7px 26px;position:relative;max-width:64ch}
.cli .acc li:before{content:"";position:absolute;left:2px;top:15px;width:9px;height:1.5px;background:#171717}
.cli .acc li b{font-weight:800}
.cli .btns{margin-top:18px;display:flex;gap:10px;flex-wrap:wrap}
.boton{appearance:none;border:1px solid #171717;background:transparent;color:#171717;
  font-family:inherit;font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  padding:11px 17px;cursor:pointer;line-height:1}
.boton:hover{background:#171717;color:#ECEAE4}
.boton.lleno{background:#171717;color:#ECEAE4}
.boton.lleno:hover{background:#000}
.boton[disabled]{border-color:#DBD7D2;color:#8E8B85;cursor:default}
.boton[disabled]:hover{background:transparent;color:#8E8B85}
.sinDoc{font-size:14px;color:#8E8B85;margin-top:16px;font-style:italic;font-family:"Times New Roman",Georgia,serif}

#visor{position:fixed;inset:0;background:rgba(10,10,12,.93);z-index:90;display:none;
  flex-direction:column;padding:0}
#visor.on{display:flex}
#visor .barra{display:flex;justify-content:space-between;align-items:center;gap:16px;
  padding:14px 18px;color:#ECEAE4;flex-wrap:wrap}
#visor .tt{font-size:12px;letter-spacing:.16em;text-transform:uppercase}
#visor .ac{display:flex;gap:9px}
#visor .boton{border-color:#ECEAE4;color:#ECEAE4}
#visor .boton:hover{background:#ECEAE4;color:#171717}
#visor iframe{flex:1;width:100%;border:0;background:#0A0A0C}
@media (max-width:640px){ .cli .nom{font-size:21px} }
@media print{ #visor{display:none!important} .cli .btns{display:none} }
"""

def FILA(nom, est, pro, accs, doc=None, docn=None, extra=None, nota=None):
    b = ""
    if doc and doc.endswith(".pdf"):
        b = ('<div class="btns">'
             f'<button class="boton lleno" onclick="bajar(\'{doc}\',\'{docn}\')">Descargar el documento</button>'
             '</div><div class="sinDoc">Es un PDF: se descarga y se abre en el lector de siempre.</div>')
        li = "".join(f'<li>{a}</li>' for a in accs)
        return (f'<div class="fila"><div class="top"><div class="nom">{esc(nom)}</div>'
                f'<div class="est">{est}</div></div>'
                f'<div class="pro">{pro}</div><ul class="acc">{li}</ul>{b}</div>')
    if doc:
        b = ('<div class="btns">'
             f'<button class="boton lleno" onclick="ver(\'{doc}\',\'{esc(nom)}\')">Ver el documento</button>'
             f'<button class="boton" onclick="bajar(\'{doc}\',\'{docn}\')">Descargar</button>')
        if extra:
            d2,n2,t2 = extra
            b += (f'<button class="boton lleno" onclick="ver(\'{d2}\',\'{esc(t2)}\')">{esc(t2)}</button>'
                  f'<button class="boton" onclick="bajar(\'{d2}\',\'{n2}\')">Descargar</button>')
        b += '</div>'
    elif nota:
        b = f'<div class="sinDoc">{nota}</div>'
    li = "".join(f'<li>{a}</li>' for a in accs)
    return (f'<div class="fila"><div class="top"><div class="nom">{esc(nom)}</div>'
            f'<div class="est">{est}</div></div>'
            f'<div class="pro">{pro}</div><ul class="acc">{li}</ul>{b}</div>')

def LISTA(filas): return '<div class="cli">' + "".join(filas) + '</div>'

# ─────────────────────────────────────────────────────────── contenido

SIGNOFF = [
 FILA("Cecilia Belotti", "Sign off · cierra 16/09",
   "Connect Turismo. El programa giró de curso auto-servicio a mentoría híbrida uno a uno, y el paquete de cierre "
   "ya está armado con los cinco entregables.",
   ["Mandar el cierre de ciclo. Es un PDF de diecisiete páginas y trae adentro el paquete completo: "
    "auditoría de producto y Skool, estructura y copy de la landing, calendario repetible y el proceso de outreach en frío.",
    "Coordinar la llamada de cierre con Teo <b>antes del 16/09</b>, que es cuando se le cierra el grupo. "
    "Es la primera de las nueve, así que conviene sacar insights de esta.",
    "Confirmar con Facu si el copy de la landing sale antes de esa llamada o después.",
    "Teo marcó que a Ceci <b>no</b> le pide el formulario de feedback: su perfil no es el que nutre al programa."],
   "docs/ceci-cierre-de-ciclo.pdf", "ceci-cierre-de-ciclo.pdf"),

 FILA("Antonio Mazzello", "Sign off · cierra 30/09",
   "Marca personal — Banca Privada, Grupo IEB. El informe se reescribió entero: la marca pasa a apoyarse en un "
   "producto de IEB y no en su figura personal.",
   ["Mandar el informe de cierre. <b>Es una versión nueva</b>, distinta de la que se armó en septiembre.",
    "Coordinar el offboarding <b>con Teo</b>. Esta llamada no la hace Facu.",
    "Antes de la llamada: responder el mensaje de Antonio que quedó sin contestar. Es lo primero.",
    "Confirmar con Teo hasta qué fecha exacta mantiene el acceso a las grupales."],
   "docs/antonio-mazzello.html", "antonio-mazzello-cierre.html"),

 FILA("Manuel Bruzzone", "Sign off · cierra 30/09",
   "Team Bruzzone. El sistema está diseñado hasta el último detalle; lo que nunca arrancó es la rutina que lo hace funcionar.",
   ["Mandar el informe de cierre.",
    "Coordinar la llamada de sign off con Teo y decirle en el mismo mensaje hasta cuándo tiene las grupales.",
    "Preguntarle si la base de leads y las automatizaciones llegaron a implementarse: es el único dato que falta para cerrar el informe."],
   "docs/manu-bruzzone.html", "manu-bruzzone-cierre.html"),

 FILA("Andrea Saturno", "Sign off · cierra 30/09",
   "Candela, la agencia que lleva con Sophie. Sale con las Onfire Sessions armadas y sin fecha.",
   ["Mandar el informe de cierre.",
    "Ofrecerle el sprint hasta fin de septiembre: grupales más <b>una llamada extra con Facu</b>. Agendar esa llamada.",
    "Pedirle la fecha del viaje y, con eso, la fecha de la primera Onfire Session.",
    "Tener presente que está mezclada con Franco: acá se da un poco de más."],
   "docs/andrea-saturno.html", "andrea-saturno-cierre.html"),

 FILA("Lucca Sorgoni", "Upselling · cierra 30/09",
   "Su programa B2C, que ya le da diez mil dólares por mes, y su agencia de Airbnb, que sigue viviendo de referidos.",
   ["Mandar el informe de cierre.",
    "Coordinar con Teo la llamada: acá el sign off puede convertirse en upselling o en continuación.",
    "Coordinar con <b>Franco</b> el testimonio y los próximos pasos como growth partner."],
   "docs/lucca-sorgoni.html", "lucca-sorgoni-cierre.html"),

 FILA("Sharon Palacio", "Sign off · cierra 30/09",
   "Estrategia creativa, y Sharon Tatt como proyecto aparte. Consiguió los clientes y entrega bien; lo único que nunca arrancó es su propio contenido.",
   ["Mandar el informe de cierre.",
    "Coordinar con Teo la llamada <b>en formato caso de éxito</b>, que es como se decidió cerrarla.",
    "Capturar el testimonio en esa misma llamada.",
    "Ofrecerle seguir entrando a las grupales como referente."],
   "docs/sharon-palacio.html", "sharon-palacio-cierre.html"),

 FILA("Scarlett Montilla", "Sign off · cierra 30/09",
   "Mentoría de procesos. El proceso terminó en un pivote: de vender servicios técnicos de marketing a vender el proceso.",
   ["Mandar el informe de cierre.",
    "Agendar <b>una llamada más con Franco</b>: de ahí sale el precio de la mentoría, que es lo único que falta.",
    "Recién después de esa llamada, coordinar el offboarding con Teo.",
    "Recordarle que de su lado queda terminar el one-sheeter y el ICP."],
   "docs/scarlett-montilla.html", "scarlett-montilla-cierre.html"),

 FILA("Nicolás Lozada", "Sign off · cierra 30/09",
   "@fffbrands. Primer comprador del Founder System. El sistema quedó armado entero; lo único que falta es vender.",
   ["Mandar el informe, que incluye la mini orientación al lanzamiento y el sprint comercial.",
    "Pedirle a Teo que hable con él <b>ahora</b>, antes de cualquier otra cosa.",
    "El sign off va <b>después</b> del sprint comercial, no antes. Agendarlo recién cuando el sprint termine."],
   "docs/nicolas-lozada.html", "nicolas-lozada-cierre.html"),

 FILA("Ayelén Cerqueira", "Sign off · cierra 30/09",
   "Estrategia creativa para construir comunidades. Sigue adentro de Cáscara: su sign off es cerrar su propia oferta como Community Success Manager.",
   ["Mandar el informe de cierre.",
    "Coordinar con Facu y Teo la reunión donde se cierra la oferta: nombre y precio.",
    "El precio sale de la llamada con Franco. Agendarla."],
   "docs/ayelen-cerqueira.html", "ayelen-cerqueira-cierre.html"),
]

CURSO = [
 FILA("Sofía Galvis Montoya", "En curso · cierra 31/10",
   "Estrategia creativa y contenido, desde Colombia. Sacó a los clientes que la tenían de techo y facturó el doble; ahora le falta el producto que escala.",
   ["Mandar la radiografía con el roadmap.",
    "Agendar la llamada con <b>Franco</b> de esta semana: ahí se define la oferta y la fecha del lanzamiento del programa de educación."],
   "docs/sofia-galvis.html", "sofia-galvis-radiografia.html"),

 FILA("Bianca Antonini", "En curso · cierra 31/10",
   "Kie, marca de ropa. Contrató Founders para mejorar el contenido; el contenido ya está bien y lo que falta es un punto A y un punto B.",
   ["Mandar los dos documentos: la radiografía y el de Eclipse y los anillos.",
    "Agendar la <b>1:1 de Franco con Bianca esta semana</b>: es donde se cierra el pricing del anillo llave.",
    "Pedirle a Teo los contenidos del Cowork editados para regalárselos.",
    "Pedirle a Bianca cuánta gente hay hoy en la comunidad de WhatsApp."],
   "docs/bianca-antonini.html", "bianca-antonini-radiografia.html",
   extra=("docs/bianca-eclipse-y-anillos.html","bianca-eclipse-y-anillos.html","Eclipse y anillos")),

 FILA("Matías Morales", "En curso · cierra 31/10",
   "9669, estudio creativo. Le pusimos el precio al doble y vendió igual. Lo que falta no es vender: es tener con qué entregar.",
   ["Mandar la radiografía con el roadmap.",
    "Pedirle <b>cuáles son los dos clientes que cerró</b>, por qué montos y con qué alcance prometido: sin eso el roadmap de entrega no se puede cerrar.",
    "Agendar con Facu el roadmap de lanzamiento y con Teo el de entrega de servicio."],
   "docs/matias-morales.html", "matias-morales-radiografia.html"),

 FILA("Agostina Marchesini Merayo", "En curso · cierra 31/10",
   "Arquitecta, estudio propio y consultoría para arquitectos. Se destrabó con el contenido y sabe cuál es su cliente ideal; le falta la oferta.",
   ["Mandar la radiografía con el roadmap.",
    "<b>Agendar la llamada donde Facu le presenta el roadmap.</b> Es el accionable principal de este cliente.",
    "Preguntarle si toma el rol de project manager de contenido con Delfina y cuántas horas le come: compite directo con el lanzamiento de octubre."],
   "docs/agostina-marchesini.html", "agostina-marchesini-radiografia.html"),

 FILA("Lucio Labate", "En curso · cierra 31/10",
   "@luwel, marca personal de diseño. Instala IA en una empresa todos los días y no la vende.",
   ["Mandar la radiografía con el roadmap.",
    "El foco del tramo es cerrar la oferta y sacar <b>un mínimo de diez piezas</b>: con menos de diez no se evalúa nada.",
    "El precio final de la instalación y del acompañamiento se confirma con las primeras cinco llamadas."],
   "docs/lucio-labate.html", "lucio-labate-radiografia.html"),

 FILA("José David Fajardo Guaqueta", "En curso · cierra 31/10",
   "Marca personal y servicio de crecimiento para e-commerce, con el concepto Universo de Marca. Es el caso que siguió la secuencia y funcionó.",
   ["Mandar la radiografía con el roadmap.",
    "<b>Agendar la llamada con Franco</b>: quedó pendiente desde la semana del 1 de septiembre y todavía no tiene fecha.",
    "Empezar a documentarlo como caso de éxito: es uno de los cuatro que quedaron marcados."],
   "docs/jose-david-fajardo.html", "jose-david-fajardo-radiografia.html"),

 FILA("Aaron Aiello", "En curso · cierra 31/10",
   "Marca personal y nueva oferta B2C, con Cami en operaciones y métricas. Le baja el marketing a cinco infoproductores y no se lo sabe bajar a sí mismo.",
   ["Mandar la radiografía con el roadmap.",
    "Mandarle el <b>Pasaporte Digital</b>: es el accionable que quedó de Facu.",
    "Coordinar con Fede el seguimiento de contenido, que acá va con Aaron como personaje."],
   "docs/aaron-aiello.html", "aaron-aiello-radiografia.html"),

 FILA("Piero Medina y Juan — Custom Lab", "En curso · cierra 31/10",
   "Producción textil y merch. Piero lleva lo creativo y Juan lo comercial. El merch no es ropa: es el medio publicitario de otra marca.",
   ["Mandar la radiografía con el roadmap.",
    "Agendar la llamada con <b>Franco</b>; el roadmap y el punto B salen después de esa llamada.",
    "Cargar la ficha de la segunda persona y conseguir el apellido de Juan, que falta en la base.",
    "Preguntar cuánto pueden poner por mes en pauta y quién la opera."],
   "docs/custom-lab.html", "custom-lab-radiografia.html"),

 FILA("Sebastián Martínez", "En curso · cierra 31/10",
   "Marca personal y programa de marca personal para creativos, con Estudio Gama 21 como productora. Tiene el tráfico y los ángulos validados; nunca cobró la mentoría.",
   ["Mandar la radiografía con el roadmap.",
    "Pasarle a Franco las conclusiones de la Clarity Call y agendar la llamada.",
    "De ahí sale la <b>fecha de lanzamiento del programa</b>, que hoy no está."],
   "docs/sebastian.html", "sebastian-radiografia.html"),

 FILA("Sol Boutmy", "En curso · cierra 31/10",
   "Be Motion, agencia de contenido orgánico en Montevideo. Seis clientes fijos y las dos socias todavía editando.",
   ["Mandar la radiografía con el roadmap.",
    "<b>Agendar la primera llamada con Franco: todavía no la tuvo.</b> De ahí salen el nicho y el precio para poder venderse fuera de Uruguay."],
   "docs/sol-boutmy.html", "sol-boutmy-radiografia.html"),

 FILA("Lola Berutti", "En curso · cierra 31/10",
   "Workflow, programa y bolsa de Project Managers para agencias creativas. El programa está listo y la demanda ya está juntada.",
   ["Mandar la radiografía con el roadmap. Avisarle que se armó con material más acotado que el resto.",
    "<b>Agendar la llamada con Franco: todavía no la tuvo.</b> Ahí se define si sale como workshop o como bootcamp, y con qué fecha."],
   "docs/lola-berutti.html", "lola-berutti-radiografia.html"),

 FILA("Qualita Studio", "En curso · cierra 31/10",
   "Rafa Lizarraga. Estudio que estuvo frenado y retoma. Tiene la radiografía y además el paquete de cartas del tramo.",
   ["Mandar los dos documentos: la radiografía y las cartas del tramo.",
    "Las cartas son los accionables que ejecutan antes de la próxima reunión. Coordinar esa reunión.",
    "Borrar las dos fichas duplicadas de Rafael Lizarraga que quedaron en la base."],
   "docs/qualita.html", "qualita-radiografia.html",
   extra=("docs/qualita-cartas.html","qualita-cartas-del-tramo.html","Las cartas del tramo")),

 FILA("Iñaki Efe", "Etiqueta a corregir",
   "Viene bien, pero Facu lo considera Growth y no Founders. En la base está mal etiquetado.",
   ["Confirmar la etiqueta con Teo antes de mandarle nada: si es Growth, no entra en este circuito.",
    "Lo mismo con Daniela Aiello."],
   nota="Sin documento: no corresponde radiografía de Founders hasta confirmar la etiqueta."),
]

# ─────────────────────────────────────────────────────────── página

partes = []
partes.append(S("00","Qué es esta página",
  P("Acá está el repaso de los veintidós clientes de Founders con el documento que le corresponde a cada uno "
    "y lo que hay que hacer con él. Sale de la revisión del 2 de septiembre y está actualizada con todo lo que "
    "pasó hasta hoy: los uno a uno de Facu, las grupales de Juana y de Fede, y las llamadas de la semana pasada.") +
  P("Cada cliente tiene dos botones. <b>Ver el documento</b> lo abre acá adentro para leerlo. "
    "<b>Descargar</b> baja el archivo a la computadora: es un HTML que se abre en el navegador, se scrollea "
    "hacia la derecha en paneles y se imprime a PDF desde el mismo navegador. Ese archivo es el que se le manda al cliente.","sub") +
  P("El orden de trabajo cambia según el grupo. En los <b>sign off</b>, el documento se muestra en la llamada y se "
    "manda después: la llamada es de informe y de cierre, y el documento es lo que se presenta ahí. En los que siguen "
    "<b>en curso</b>, el documento se manda antes y la llamada se usa para decidir sobre lo que ya leyeron.","sub")))

partes.append(S("01","Cómo funciona un sign off",
  P("Nueve clientes están en sign off. La regla es la misma para todos y conviene tenerla clara antes de escribirle a nadie.") +
  PASOS([
    "<b>No hay más llamadas uno a uno.</b> Lo que queda es la llamada de cierre.",
    "<b>El acceso a las grupales se mantiene hasta una fecha definida</b>, que se le dice en el mismo mensaje. "
    "Ceci hasta el 16 de septiembre; el resto hasta el 30.",
    "<b>Facu desarrolla el informe, Teo hace la llamada de offboarding.</b> Los documentos de esta página son esos informes.",
    "<b>Se aclara de antemano de qué se trata la llamada.</b> Cuando coordinás, la persona tiene que saber que es una "
    "llamada de informe y de cierre del programa, no una llamada más.",
    "<b>El documento se muestra en la llamada y se manda después.</b> Teo lo presenta ahí.",
    "<b>Si alguien se queja, resuelve Teo</b> y decide sobre la marcha.",
  ]) +
  P("Estos nueve son los primeros que se offboardean, así que de estas llamadas hay que sacar insights: qué salió bien, "
    "qué no y por qué. Al cerrar se manda un formulario de feedback con lo positivo y lo negativo, pero solo a los "
    "perfiles que nutren al programa; no a todos. Eso lo decide Teo caso por caso.","sub") +
  P("Los trece que siguen en curso cierran el 31 de octubre. Septiembre es para dejar todo armado y octubre para ver "
    "la evolución.","sub")))

partes.append(S("02","Sign off — nueve clientes", LISTA(SIGNOFF)))
partes.append(S("03","En curso — trece clientes", LISTA(CURSO)))

partes.append(S("04","Lo que falta cargar",
  P("Tres cosas quedaron pendientes de la revisión y siguen pendientes.") +
  PASOS([
    "<b>Juanjo</b>, que viene de La Cáscara por upselling: falta crear la ficha. Recién entra, así que le corresponde "
    "el roadmap normal de los primeros noventa días y no una radiografía.",
    "<b>La segunda persona de Custom Lab</b>: falta la ficha y falta el apellido de Juan.",
    "<b>La fecha de inicio de casi todos.</b> Solo Sharon (13 de mayo), Lucca (6 de abril), Sebastián (1 de septiembre) "
    "y Sol (2 de septiembre) la tienen cargada. Sin esa fecha no se sabe en qué día del programa está cada uno.",
  ])))

partes.append(S("05","Lo que te toca a vos después de esto",
  P("De la revisión del 2 de septiembre y de la reunión del 14 con Facu, Juana y Teo quedaron estas cosas a tu nombre. "
    "Arrancan una vez que los documentos estén mandados.") +
  BLOQ([
    ("El acercamiento a los que se cierran",
     "Armar el proceso de cómo se contacta a cada uno de los nueve: qué se le dice, en qué orden y con cuánta "
     "anticipación, para que lleguen a la llamada sabiendo que es de cierre. Facu te pasa la lista."),
    ("El roadmap del servicio",
     "El recorrido general del programa por fechas: onboarding, Clarity Call con Facu, llamada con Franco, y las "
     "grupales de creatividad, contenido y operaciones desde la semana uno. Hoy existe pero no está a mano. "
     "Teo te pasa el brief."),
    ("El roadmap de cada cliente",
     "Cada cliente tiene que poder ver el suyo. Los trece documentos de la sección En curso ya tienen el roadmap "
     "escrito adentro: de ahí sale el individual, no hay que inventarlo."),
    ("Los kick-offs de las grupales",
     "Un video o documento por grupal — uno de Teo, uno de Juana, uno de Fede — que diga qué se trabaja ahí, con qué "
     "hay que llegar y por dónde empezar. Arregla la primera semana, que hoy es un cachetazo."),
    ("Operaciones y oferta",
     "Dentro de Founders, el frente que queda de tu lado es operaciones y productividad, y la oferta. El seguimiento y "
     "el control de las tarjetas asignadas también: que se completen es lo que hace que el cliente pueda decidir."),
  ])))

partes.append(MARCO("Un solo criterio",
  "Nadie llega a una llamada sin saber para qué es. En los cierres se dice que es de informe y de cierre, y el "
  "documento se presenta ahí. En los que siguen, el documento va antes y la llamada se usa para decidir sobre lo que "
  "ya leyeron."))

cuerpo = "".join(partes)

HTML = f"""<title>Handoff para Aye</title>
<style>{CSS}</style>
<div class="hoja">
<div class="caja">Cáscara Founders · para Aye</div>
<h1>Los veintidós clientes,<br>con su documento y su accionable</h1>
<p class="bajada">Repaso completo del programa: quién cierra, quién sigue, qué documento le corresponde a cada uno
y qué hay que hacer con él esta semana.</p>
<div class="tira">
  <div><div class="et">Sign off</div><div class="tx">9 clientes</div></div>
  <div><div class="et">En curso</div><div class="tx">13 clientes</div></div>
  <div><div class="et">Documentos</div><div class="tx">23 archivos</div></div>
  <div><div class="et">Fecha</div><div class="tx">15 de septiembre de 2026</div></div>
</div>
{cuerpo}
<div class="pie"><div><span class="sello">C</span></div>
<div>Cáscara Founders · repaso del 2 de septiembre, actualizado al 15</div></div>
</div>

<div id="visor" role="dialog" aria-modal="true">
  <div class="barra">
    <div class="tt" id="vt"></div>
    <div class="ac">
      <button class="boton" id="vd">Descargar</button>
      <button class="boton" onclick="cerrar()">Cerrar</button>
    </div>
  </div>
  <iframe id="vf" title="Documento"></iframe>
</div>

<script>
var VIS=document.getElementById('visor'),VF=document.getElementById('vf'),
    VT=document.getElementById('vt'),VD=document.getElementById('vd');
function ver(ruta,titulo){{
  VT.textContent=titulo; VF.src=ruta;
  VD.onclick=function(){{ bajar(ruta, ruta.split('/').pop()) }};
  VIS.classList.add('on'); document.body.style.overflow='hidden';
}}
function cerrar(){{ VIS.classList.remove('on'); VF.src='about:blank'; document.body.style.overflow=''; }}
document.addEventListener('keydown',function(e){{ if(e.key==='Escape') cerrar() }});
async function bajar(ruta,nombre){{
  try{{
    var r=await fetch(ruta); var t=await r.blob();
    var dl=await window.claude.use('downloads');
    if(!dl){{ alert('La descarga no está disponible en esta vista. Abrí el documento y guardalo desde el navegador.'); return }}
    await dl.save({{filename:nombre,data:t}});
  }}catch(e){{ alert('No se pudo descargar el archivo.') }}
}}
</script>"""

open(os.path.join(RAIZ,'founders-handoff-aye.html'),'w',encoding='utf-8').write(HTML)
print("ok", len(HTML))
