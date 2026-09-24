# -*- coding: utf-8 -*-
"""Handoff de cards por dueño: Franco, Fede, Juana, Teo."""
import json, html as _h, os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # la raíz del repo
from build_plantillas import INK, DEEP, PAPER, PAPER2, GREY, GREY2, LINE, ROJO, DISP, SERIF
def esc(s): return _h.escape(str(s or ""))

inv=json.load(open(os.path.join(RAIZ,'fichas','inventario.json'),encoding='utf-8'))
MOD={}; CAT={}
for c in inv['categorias']:
    for m in c['modulos']:
        MOD[m['id']]=m; CAT[m['id']]=c['nombre']

DUENOS=[
 ("franco","Franco","Growth partner",
  "Oferta, pricing, demanda pagada y todo lo comercial. Sos el que convierte la estrategia en plata, "
  "así que son las que más se tocan cuando un founder no vende.",
  ["icp-mecanismo","one-sheeter-oferta","precio-escalera","cinco-llamadas-con-precio",
   "pipeline-7-campos","prospeccion-y-recontacto","llamada-de-venta","propuesta-comercial","setter-closer",
   "handraisers-historias","calendario-lanzamiento","webinar-de-venta"]),
 ("fede","Fede","Contenido y estrategia",
  "Perfil, ángulos, calendario y volumen. Son las que hacen que el founder tenga de dónde agarrarse "
  "para publicar sin improvisar cada semana.",
  ["profile-funnel","angulos-desde-icp","calendario-contenido","diez-piezas-y-lectura",
   "formato-barato","caso-documentado","capitalizar-evento"]),
 ("juana","Juana","Identidad y dirección creativa",
  "Quién es la marca y cómo se ve. Son pocas y son las que más se notan cuando están mal hechas, "
  "porque todo lo demás se apoya arriba.",
  ["pasaporte-digital","identidad-y-arco-narrativo","direccion-visual","narrativa-de-video"]),
 ("teo","Teo","Sistemas, herramientas y automatización",
  "Con qué se arma cada cosa y dónde vive el dato. Vos no decidís qué servicio da el founder: decidís "
  "cómo queda instrumentado para que se repita sin que él esté encima.",
  ["onboarding-y-roadmap-cliente","ciclo-y-continuidad","os-en-notion","arquitectura-comunidad",
   "base-de-datos-unica","captura-y-seguimiento","landing-que-convierte"]),
 ("facu","Facu","Negocio, estructura y números",
  "La mirada del negocio entero, la forma del servicio, el equipo y lo que dicen los números. Son las "
  "que decido yo y las que escribo yo.",
  ["radiografia-360","foco-y-ventana","sociedad-y-roles",
   "alcance-por-escrito","proceso-entrega-repetible","auditoria-del-programa",
   "contratar-primer-rol","delegar-produccion","cadencia-y-duenos",
   "diario-administrativo","dashboard-embudo","informes-con-ia"]),
]
FACU=[]

todas=[i for _,_,_,_,ids in DUENOS for i in ids]+FACU
falt=[k for k in MOD if k not in todas]
assert not falt, "sin dueño: %s"%falt
assert len(todas)==len(MOD), (len(todas),len(MOD))

def texto_card(mid):
    m=MOD[mid]
    L=[f"## {m['nombre']}  ({mid})",
       f"Categoría: {CAT[mid]}",
       f"Cuándo se asigna: {m['para_quien']}",
       f"Qué queda hecho: {m['resultado']}","","Pasos:"]
    L+= [f"  {i+1}. {p}" for i,p in enumerate(m['pasos'])]
    L+= ["","Qué completa el founder:"]+[f"  - {x}" for x in m['completar']]
    L+= ["","Herramientas:"]+[f"  - {x}" for x in m['herramientas']]
    if m.get('evidencia'): L+= ["",f"Casos de la camada: {m['evidencia']}"]
    return "\n".join(L)

def texto_set(nom,rol,ids):
    cab=(f"# Cards de Cáscara Founders · {nom} — {rol}\n\n"
      "Estas son las cards del programa que están a tu nombre. Necesito tu devolución sobre cada una:\n"
      "1. Si el momento en que se asigna está bien descripto.\n"
      "2. Si los pasos son los que vos darías, en ese orden.\n"
      "3. Si lo que se le pide completar al founder alcanza y no sobra.\n"
      "4. Si las herramientas son las que usamos hoy.\n"
      "5. Qué card falta que hoy resolvés a mano cada vez.\n\n"
      "Devolveme el texto corregido de las que cambien, con el mismo formato.\n\n"+"="*60+"\n")
    return cab+"\n\n".join(texto_card(i) for i in ids)

CSS=f"""
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:{PAPER};color:{INK};font-family:{DISP};font-size:18px;line-height:1.55;
 -webkit-font-smoothing:antialiased}}
.hoja{{max-width:1000px;margin:0 auto;padding:60px 32px 110px}}
.caja{{display:inline-block;border:1px solid {GREY2};padding:6px 13px;font-size:10.5px;
 letter-spacing:.24em;text-transform:uppercase;color:{GREY}}}
h1{{font-size:clamp(38px,6vw,62px);font-weight:800;letter-spacing:-.04em;line-height:1;margin:26px 0 0}}
.bajada{{font-size:21px;line-height:1.5;color:{GREY};margin:18px 0 0;max-width:58ch}}

.mosaico{{margin-top:50px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;
 background:{LINE};border:1px solid {LINE}}}
.tile:last-child{{grid-column:1/-1}}
.tile{{background:{PAPER2};padding:42px 34px 36px;text-align:left;border:0;cursor:pointer;
 font-family:inherit;color:inherit;display:block;width:100%;transition:background .12s}}
.tile:hover{{background:{INK};color:{PAPER2}}}
.tile:hover .rol,.tile:hover .cant,.tile:hover .tx{{color:#B8B5AF}}
.tile .nom{{font-size:clamp(34px,5vw,54px);font-weight:800;letter-spacing:-.04em;line-height:1}}
.tile .rol{{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:{GREY};margin-top:14px}}
.tile .cant{{font-size:15px;color:{GREY};margin-top:22px;font-variant-numeric:tabular-nums}}
.tile .tx{{font-size:16px;line-height:1.5;color:{GREY};margin-top:12px;max-width:34ch}}

.pie{{margin-top:70px;border-top:1px solid {INK};padding-top:22px;font-size:11px;
 letter-spacing:.14em;text-transform:uppercase;color:{GREY};display:flex;
 justify-content:space-between;gap:18px;flex-wrap:wrap}}
.mias{{margin-top:44px;border-top:1px solid {LINE};padding-top:22px;font-size:16px;color:{GREY};max-width:62ch}}

.vista{{display:none}} .vista.on{{display:block}}
.volver{{display:inline-flex;align-items:center;gap:12px;font-size:11px;letter-spacing:.18em;
 text-transform:uppercase;color:{GREY};border:0;background:none;cursor:pointer;font-family:inherit;padding:10px 0}}
.volver:hover{{color:{INK}}}
.volver i{{width:8px;height:8px;border-left:1.5px solid currentColor;border-bottom:1.5px solid currentColor;
 transform:rotate(45deg);display:block}}
.brief{{margin-top:28px;background:{DEEP};color:{PAPER2};padding:34px 30px}}
.brief .et{{font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:#8E8B85}}
.brief p{{margin:14px 0 0;font-size:18.5px;line-height:1.55;max-width:62ch;color:{PAPER2}}}
.brief ol{{margin:18px 0 0;padding-left:22px}}
.brief li{{font-size:18px;line-height:1.5;margin-bottom:9px;color:#D6D3CD}}
.brief li b{{color:{PAPER2};font-weight:800}}
.acc{{margin-top:26px;display:flex;gap:10px;flex-wrap:wrap}}
.boton{{appearance:none;border:1px solid {INK};background:transparent;color:{INK};font-family:inherit;
 font-size:11px;letter-spacing:.16em;text-transform:uppercase;padding:12px 18px;cursor:pointer;line-height:1}}
.boton:hover{{background:{INK};color:{PAPER}}}
.boton.lleno{{background:{INK};color:{PAPER}}} .boton.lleno:hover{{background:#000}}
.brief .boton{{border-color:{PAPER2};color:{PAPER2}}}
.brief .boton:hover{{background:{PAPER2};color:{INK}}}

.card{{margin-top:44px;border-top:2px solid {INK};padding-top:26px}}
.card .cab{{display:flex;justify-content:space-between;align-items:baseline;gap:18px;flex-wrap:wrap}}
.card .idx{{font-size:11px;letter-spacing:.2em;color:{GREY2};font-variant-numeric:tabular-nums}}
.card h2{{font-size:clamp(26px,3.4vw,38px);font-weight:800;letter-spacing:-.032em;line-height:1.1;
 margin:10px 0 0;max-width:24ch}}
.card .cat{{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:{GREY};white-space:nowrap}}
.card .cuando{{font-family:{SERIF};font-style:italic;font-size:19px;line-height:1.5;color:{GREY};
 margin-top:14px;max-width:62ch}}
.bloque{{margin-top:26px}}
.bloque .et{{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:{GREY2};
 border-top:1px solid {LINE};padding-top:14px}}
.bloque .res{{font-size:21px;line-height:1.45;margin-top:12px;max-width:56ch;font-weight:800;letter-spacing:-.018em}}
.bloque ol,.bloque ul{{margin:12px 0 0;padding-left:24px}}
.bloque li{{font-size:18px;line-height:1.52;margin-bottom:9px;max-width:60ch}}
.bloque .ev{{font-size:16.5px;line-height:1.5;color:{GREY};margin-top:12px;max-width:62ch}}
.dosc{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 44px}}

#txt{{position:fixed;inset:0;background:rgba(10,10,12,.94);z-index:90;display:none;
 flex-direction:column;padding:0}}
#txt.on{{display:flex}}
#txt .barra{{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:14px 18px;color:{PAPER2}}}
#txt .barra .t{{font-size:11px;letter-spacing:.16em;text-transform:uppercase}}
#txt .boton{{border-color:{PAPER2};color:{PAPER2}}}
#txt .boton:hover{{background:{PAPER2};color:{INK}}}
#txt textarea{{flex:1;width:100%;border:0;background:{PAPER2};color:{INK};font-family:ui-monospace,Menlo,monospace;
 font-size:13.5px;line-height:1.6;padding:22px;resize:none}}

@media (max-width:760px){{
 .hoja{{padding:40px 20px 80px}} .mosaico{{grid-template-columns:1fr}}
 .dosc{{grid-template-columns:1fr}} .tile{{padding:32px 24px}}
}}
@media print{{ .acc,.volver,#txt{{display:none!important}} .vista{{display:block!important}} }}
"""

def card_html(mid,i,n):
    m=MOD[mid]
    pq = esc(m['para_quien'].strip())
    pasos="".join(f'<li>{esc(p)}</li>' for p in m['pasos'])
    comp="".join(f'<li>{esc(x)}</li>' for x in m['completar'])
    herr="".join(f'<li>{esc(x)}</li>' for x in m['herramientas'])
    ev=f'<div class="bloque"><div class="et">Cómo se está usando hoy</div><div class="ev">{esc(m["evidencia"])}</div></div>' if m.get('evidencia') else ''
    return f'''<div class="card">
 <div class="cab"><span class="idx">{i:02d} / {n:02d}</span><span class="cat">{esc(CAT[mid])}</span></div>
 <h2>{esc(m['nombre'])}</h2>
 <div class="bloque" style="margin-top:18px"><div class="et" style="border:0;padding:0">Cuándo se asigna</div>
 <div class="cuando" style="margin-top:8px">{pq}</div></div>
 <div class="bloque"><div class="et">Qué queda hecho</div><div class="res">{esc(m['resultado'])}</div></div>
 <div class="bloque"><div class="et">Los pasos</div><ol>{pasos}</ol></div>
 <div class="dosc">
   <div class="bloque"><div class="et">Qué completa el founder</div><ul>{comp}</ul></div>
   <div class="bloque"><div class="et">Herramientas</div><ul>{herr}</ul></div>
 </div>
 {ev}
 <div class="acc"><button class="boton" onclick="unaSola('{mid}')">Copiar esta card</button></div>
</div>'''

TX={}
vistas=[]
for slug,nom,rol,intro,ids in DUENOS:
    n=len(ids)
    TX[slug]=texto_set(nom,rol,ids)
    cards="".join(card_html(m,i+1,n) for i,m in enumerate(ids))
    vistas.append(f'''<div class="vista" id="v-{slug}">
 <button class="volver" onclick="ir('home')"><i></i> Volver</button>
 <div class="caja" style="margin-top:18px">{esc(rol)}</div>
 <h1>{esc(nom)}</h1>
 <p class="bajada">{esc(intro)}</p>
 <div class="brief">
  <div class="et">{"Lo que reviso yo" if slug=="facu" else "Qué necesito de vos"}</div>
  <p>{"Estas son las mías. Las reviso con el mismo criterio que les pido a ustedes:" if slug=="facu" else "Pasale este set a tu Claude y revisalo card por card. Lo que busco es esto:"}</p>
  <ol>
   <li><b>El momento.</b> Si cuándo se asigna está bien descripto.</li>
   <li><b>Los pasos.</b> Si son los que vos darías, y en ese orden.</li>
   <li><b>Lo que completa el founder.</b> Si alcanza y si no sobra nada.</li>
   <li><b>Las herramientas.</b> Si son las que usamos hoy.</li>
   <li><b>Lo que falta.</b> Qué card no está y hoy resolvés a mano cada vez.</li>
  </ol>
  <p>{"El que quiera marcarme algo de estas, bienvenido." if slug=="facu" else "Devolveme el texto corregido de las que cambien, con el mismo formato."}</p>
  <div class="acc">
   <button class="boton" onclick="bajar('{slug}')">Descargar {"las" if slug=="facu" else "mis"} {n} cards</button>
   <button class="boton" onclick="verTexto('{slug}')">Ver el texto para copiar</button>
  </div>
 </div>
 {cards}
 <div class="pie"><div>Cáscara Founders · {esc(nom)} · {n} cards</div><div>15 de septiembre de 2026</div></div>
</div>''')

tiles="".join(f'''<button class="tile" onclick="ir('{slug}')">
 <div class="nom">{esc(nom)}</div><div class="rol">{esc(rol)}</div>
 <div class="cant">{len(ids)} cards</div><div class="tx">{esc(intro.split(".")[0])}.</div></button>'''
 for slug,nom,rol,intro,ids in DUENOS)

DATA=json.dumps(TX,ensure_ascii=False)
NOM=json.dumps({s:n for s,n,_,_,_ in DUENOS},ensure_ascii=False)
CARDS=json.dumps({k:texto_card(k) for k in MOD},ensure_ascii=False)

HTML=f"""<title>Las cards de Founders, por dueño</title>
<style>{CSS}</style>
<div class="hoja">
<div class="vista on" id="v-home">
 <div class="caja">Cáscara Founders · para revisar</div>
 <h1>Las cuarenta cards,<br>repartidas</h1>
 <p class="bajada">Cada card del programa quedó a nombre del que más sabe de eso. Entrá a la tuya, revisala con
 tu Claude y devolvémela corregida. Es lo que hace que dejen de salir de mi cabeza.</p>
 <div class="mosaico">{tiles}</div>
 <div class="mias"><b>El criterio del reparto:</b> el que decide qué se hace se queda con la card, y el que la
 instrumenta la recibe hecha. Por eso contratar a alguien o ponerle precio a la capacidad son mías aunque después
 las opere Teo, y armar el OS en Notion es de Teo aunque la decisión del proceso sea mía. Si alguna les parece que
 está en la columna equivocada, eso también es devolución.</div>
 <div class="pie"><div>Cáscara Founders · 40 cards</div><div>15 de septiembre de 2026</div></div>
</div>
{"".join(vistas)}
</div>

<div id="txt">
 <div class="barra"><span class="t" id="txt-t"></span>
  <span class="acc" style="margin:0">
   <button class="boton" onclick="copiarArea()">Copiar</button>
   <button class="boton" onclick="cerrarTexto()">Cerrar</button>
  </span></div>
 <textarea id="txt-a" spellcheck="false"></textarea>
</div>

<script>
var TX={DATA}, NOM={NOM}, CARDS={CARDS};
function ir(v){{
  document.querySelectorAll('.vista').forEach(function(e){{e.classList.remove('on')}});
  document.getElementById('v-'+v).classList.add('on');
  window.scrollTo(0,0);
}}
function verTexto(s){{
  document.getElementById('txt-t').textContent='Cards de '+NOM[s];
  var a=document.getElementById('txt-a'); a.value=TX[s];
  document.getElementById('txt').classList.add('on');
  setTimeout(function(){{a.focus();a.select()}},60);
}}
function unaSola(id){{
  document.getElementById('txt-t').textContent='Una card';
  var a=document.getElementById('txt-a'); a.value=CARDS[id];
  document.getElementById('txt').classList.add('on');
  setTimeout(function(){{a.focus();a.select()}},60);
}}
function cerrarTexto(){{ document.getElementById('txt').classList.remove('on') }}
function copiarArea(){{
  var a=document.getElementById('txt-a'); a.focus(); a.select();
  try{{ document.execCommand('copy') }}catch(e){{}}
}}
document.addEventListener('keydown',function(e){{ if(e.key==='Escape') cerrarTexto() }});
async function bajar(s){{
  try{{
    var dl=await window.claude.use('downloads');
    if(!dl){{ verTexto(s); return }}
    await dl.save({{filename:'cards-founders-'+s+'.md', data:TX[s]}});
  }}catch(e){{ verTexto(s) }}
}}
</script>"""

open(os.path.join(RAIZ,'cards-por-dueno.html'),'w',encoding='utf-8').write(HTML)
for s,n,_,_,ids in DUENOS: print(n, len(ids))
print("total", sum(len(x[4]) for x in DUENOS), "+ facu", len(FACU))
print("ok", len(HTML))
