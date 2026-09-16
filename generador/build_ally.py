# -*- coding: utf-8 -*-
"""Handoff para Aye: repaso de clientes, accionables y documentos."""
import sys, io, os
sys.path.insert(0,'/home/claude/qualita')
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

import json as _json
# la fuente única del handoff: se edita en web/contenido/entregas.json y sale acá y en la torre
ENT = _json.load(open('/home/claude/web/contenido/entregas.json', encoding='utf-8'))

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

def _fila(f):
    doc = ('docs/'+f['doc']) if f.get('doc') else None
    ex  = f.get('extra')
    if ex: ex = ['docs/'+ex[0], ex[1], ex[2]]
    return FILA(f['nombre'], f['estado'], f['proyecto'], f['accionables'],
                doc, f.get('docn'), ex, f.get('nota'))

_S = [f for f in ENT['filas'] if ('Sign off' in f['estado'] or 'Upselling' in f['estado'])]
_C = [f for f in ENT['filas'] if f not in _S]
SIGNOFF = [_fila(f) for f in _S]
CURSO   = [_fila(f) for f in _C]

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
  P("La regla es la misma para todos y conviene tenerla clara antes de escribirle a nadie.") +
  PASOS(ENT["regla_signoff"]) +
  P("Estos son los primeros que se offboardean, así que de estas llamadas hay que sacar insights: qué salió bien, "
    "qué no y por qué. Al cerrar se manda un formulario de feedback, pero solo a los perfiles que nutren al "
    "programa. Eso lo decide Teo caso por caso.","sub") +
  P("Los que siguen en curso cierran el 31 de octubre. Septiembre es para dejar todo armado y octubre para ver "
    "la evolución.","sub")))

partes.append(S("02","Sign off — %d clientes" % len(SIGNOFF), LISTA(SIGNOFF)))
partes.append(S("03","En curso — %d clientes" % len(CURSO), LISTA(CURSO)))

partes.append(S("04","Lo que falta cargar",
  P("Lo que quedó pendiente de la revisión y sigue pendiente.") + PASOS(ENT["falta"])))

partes.append(S("05","Lo que te toca a vos después de esto",
  P("Lo que quedó a tu nombre. Arranca una vez que los documentos estén mandados.") +
  BLOQ([tuple(x) for x in ENT["aye"]])))

partes.append(MARCO("Un solo criterio", ENT["criterio"]))

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

open('/home/claude/ally/founders-handoff-aye.html','w',encoding='utf-8').write(HTML)
print("ok", len(HTML))
