# -*- coding: utf-8 -*-
import json, html as _h
def esc(s): return _h.escape(str(s or ""))
rows=json.load(open('panel-data.json',encoding='utf-8'))
import handicap as hk
EJES=[(k,n) for k,n,_ in hk.EJES]

con = [r for r in rows if r['handicap']]
prom = sum(r['handicap']['total'] for r in con)/len(con)
n_rojo = sum(1 for r in con if r['handicap']['ritmo']=='rojo')
n_amar = sum(1 for r in con if r['handicap']['ritmo']=='amarillo')
n_cierre = sum(1 for r in rows if r['modo']=='cierre')

# dueños de los accionables de Cáscara
DUENOS = ["Facu","Franco","Teo","Juana","Fede","Cáscara"]
tareas={d:[] for d in DUENOS}
for r in rows:
    for t in r['cascara']:
        d = next((x for x in DUENOS if t.startswith(x) or (" "+x+" ") in t), "Cáscara")
        tareas[d].append((r['cliente'], t))

def barras(h, key):
    v=h['ejes'][key]; flojo = key in h['eje_flojo']
    return "".join('<i class="s%s"></i>' % ("" if i<v else " o") for i in range(4)), v, flojo

def fila(r, i):
    h=r['handicap']
    if h:
        ejes="".join(
            '<span class="eje%s" title="%s: %d de 4"><b>%s</b><span class="bars">%s</span></span>' % (
              " f" if k in h['eje_flojo'] else "", esc(n), h['ejes'][k], esc(n[:3]),
              "".join('<i%s></i>' % ("" if j<h['ejes'][k] else ' class="o"') for j in range(4)))
            for k,n in EJES)
        tot='<span class="tot num">%d</span>' % h['total']
        tramo='<span class="tramo">%s</span>' % esc(h['tramo'])
        ritmo='<span class="ritmo %s">%s</span>' % (h['ritmo'], esc(h['ritmo']))
        nota=esc(h['nota'])
        sug = "/".join(h['sugiere'])
        choca = r['orientacion'] not in h['sugiere']
        disc = ('<p class="disc">El eje más flojo apunta a <b>%s</b> y la orientación asignada es <b>%s</b>. Vale revisarlo.</p>' % (esc(sug), esc(r['orientacion']))) if choca else ""
    else:
        ejes='<span class="sinh">sin handicap</span>'; tot=""; tramo=""; ritmo=""; nota=esc(r['cuello']); disc=""
    det=[]
    if r['metrica']: det.append('<div><h4>La métrica</h4><p>%s</p></div>' % esc(r['metrica']))
    if r['cliente_tareas']:
        det.append('<div><h4>Septiembre · lo que hace él o ella</h4><ul>%s</ul></div>'
                   % "".join('<li>%s</li>' % esc(x) for x in r['cliente_tareas']))
    if r['cascara']:
        det.append('<div><h4>Septiembre · lo que hace Cáscara</h4><ul>%s</ul></div>'
                   % "".join('<li>%s</li>' % esc(x) for x in r['cascara']))
    if r['abierto']: det.append('<div><h4>Sin definir</h4><p>%s</p></div>' % esc(r['abierto']))
    link = ('<a class="doc" href="%s">Abrir el documento</a>' % esc(r['doc'])) if r['doc'] else '<span class="doc off">Documento aparte</span>'
    return '''<article class="row" data-ori="%s" data-modo="%s" data-ritmo="%s" data-txt="%s">
  <button class="head" aria-expanded="false" aria-controls="d%d">
    <span class="who"><b>%s</b><small>%s</small></span>
    <span class="ejes">%s</span>
    <span class="meta">%s%s%s<span class="ori">%s</span></span>
  </button>
  <p class="nota">%s</p>
  <div class="det" id="d%d" hidden>
    %s
    <p class="tit">%s</p>
    %s
    <div class="grid">%s</div>
    <p class="last">Última llamada tomada: %s · %s</p>
  </div>
</article>''' % (esc(r['orientacion']), esc(r['modo']), (h['ritmo'] if h else 'na'),
      esc((r['cliente']+' '+r['proyecto']+' '+r['orientacion']).lower()), i,
      esc(r['cliente']), esc(r['proyecto']), ejes, tot, tramo, ritmo, esc(r['orientacion']),
      nota, i, disc, esc(r['titular']), link,
      "".join(det), esc(r['ultima']), link)

filas = "\n".join(fila(r,i) for i,r in enumerate(rows))

bloque_tareas = "".join(
  '<div class="duen"><h3>%s</h3><ul>%s</ul></div>' % (esc(d), "".join(
     '<li><b>%s</b> %s</li>' % (esc(c), esc(t)) for c,t in tareas[d]))
  for d in DUENOS if tareas[d])

leyenda = "".join('<li><b>%s</b> %s</li>' % (esc(n), esc(desc)) for k,n,desc in hk.EJES)

HTML = '''<title>Camada Cáscara Founders</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<style>
:root{
  --ground:#ECEAE4; --surf:#FBFAF8; --ink:#171717; --deep:#0A0A0C;
  --grey:#6A6A66; --line:#DBD7D2; --soft:#9A968E;
  --ok:#3F6B45; --warn:#8A6A2F; --bad:#8C3A32;
  --disp:"Helvetica Neue",Helvetica,Arial,sans-serif;
  --serif:"Times New Roman",Times,Georgia,serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --ground:#0F0F10; --surf:#17171A; --ink:#ECEAE4; --deep:#08080A;
  --grey:#8E8E92; --line:#2C2C31; --soft:#6E6E74;
  --ok:#7FAE86; --warn:#C7A25C; --bad:#D2776C;
}}
:root[data-theme="dark"]{
  --ground:#0F0F10; --surf:#17171A; --ink:#ECEAE4; --deep:#08080A;
  --grey:#8E8E92; --line:#2C2C31; --soft:#6E6E74;
  --ok:#7FAE86; --warn:#C7A25C; --bad:#D2776C;
}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font-family:var(--disp);
  line-height:1.55;-webkit-font-smoothing:antialiased}
.num{font-weight:800;letter-spacing:-.045em;font-variant-numeric:tabular-nums}
.wrap{max-width:1180px;margin:0 auto;padding-inline:20px;padding-block:0 72px}

/* masthead */
header{background:var(--deep);color:#ECEAE4;margin-bottom:0}
.mast{max-width:1180px;margin:0 auto;padding-inline:20px;padding-block:46px 40px}
.k{display:inline-block;border:1px solid #45454C;padding:5px 12px;font-size:10.5px;
  letter-spacing:.22em;text-transform:uppercase;color:#9A9AA2;margin-bottom:26px}
h1{font-size:clamp(34px,6.2vw,58px);font-weight:800;letter-spacing:-.035em;line-height:1;margin:0 0 16px;text-wrap:balance}
.sub{font-size:17px;color:#A8A8AE;max-width:62ch;margin:0}
.stats{display:flex;flex-wrap:wrap;gap:38px;margin-top:38px;border-top:1px solid #2A2A30;padding-top:26px}
.stat b{display:block;font-size:30px;line-height:1;color:#FBFAF8}
.stat span{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:#7A7A82}

/* controles */
.bar{position:sticky;top:0;z-index:5;background:var(--ground);border-bottom:1px solid var(--line);
  padding-block:14px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.bar input{font:inherit;font-size:14px;padding:7px 11px;border:1px solid var(--line);
  background:var(--surf);color:var(--ink);min-width:190px;flex:1}
.chip{font:inherit;font-size:11px;letter-spacing:.14em;text-transform:uppercase;padding:7px 12px;
  border:1px solid var(--line);background:transparent;color:var(--grey);cursor:pointer}
.chip[aria-pressed="true"]{background:var(--ink);color:var(--ground);border-color:var(--ink)}
.chip:focus-visible,.head:focus-visible,.doc:focus-visible{outline:2px solid var(--ink);outline-offset:2px}

/* filas */
h2{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--grey);font-weight:400;
  margin:54px 0 0;padding-bottom:12px;border-bottom:1px solid var(--ink)}
h2+.note{margin:14px 0 20px;font-size:15px;color:var(--grey);max-width:70ch}
.row{border-bottom:1px solid var(--line);padding-block:16px}
.row.hide{display:none}
.head{display:grid;grid-template-columns:minmax(0,1fr) 350px 268px;gap:24px;align-items:center;
  width:100%;background:none;border:0;padding:0;text-align:left;color:inherit;font:inherit;cursor:pointer}
.who b{display:block;font-size:19px;font-weight:700;letter-spacing:-.02em;line-height:1.2}
.who small{display:block;font-size:13px;color:var(--grey);margin-top:2px}
.ejes{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;justify-items:start}
.eje{display:flex;flex-direction:column;gap:5px}
.eje b{font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--soft);font-weight:400}
.eje.f b{color:var(--ink);font-weight:700}
.eje .bars{display:flex;gap:3px}
.eje i{display:block;width:12px;height:7px;background:var(--ink)}
.eje i.o{background:var(--line)}
.meta{display:flex;align-items:center;gap:16px;justify-content:flex-end}
.tot{font-size:26px;min-width:2.2ch;text-align:right}
.tramo{font-size:12px;color:var(--grey);white-space:nowrap;min-width:11ch}
.ritmo{font-size:10px;letter-spacing:.16em;text-transform:uppercase;padding:3px 9px;border:1px solid currentColor}
.ritmo.verde{color:var(--ok)} .ritmo.amarillo{color:var(--warn)} .ritmo.rojo{color:var(--bad)}
.ori{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--grey);
  border:1px solid var(--line);padding:3px 9px;white-space:nowrap}
.sinh{font-size:12px;color:var(--soft);font-style:italic;font-family:var(--serif)}
.nota{margin:10px 0 0;font-size:15px;color:var(--grey);max-width:92ch}
.det{margin-top:18px;background:var(--surf);border:1px solid var(--line);padding:22px 24px}
.det .tit{font-size:17px;margin:0 0 16px;max-width:74ch}
.det .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:24px;margin-top:18px}
.det h4{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--grey);font-weight:400;margin:0 0 8px}
.det p{margin:0;font-size:14.5px}
.det ul{margin:0;padding-left:17px} .det li{font-size:14.5px;margin-bottom:6px}
.disc{margin:0 0 14px;font-size:14px;color:var(--warn);border-left:2px solid var(--warn);padding-left:12px}
.last{margin-top:18px;font-size:12.5px;color:var(--soft);font-family:var(--serif);font-style:italic}
.doc{display:inline-block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;
  border:1px solid var(--ink);padding:7px 14px;text-decoration:none;color:var(--ink);margin-bottom:16px}
.doc:hover{background:var(--ink);color:var(--ground)}
.doc.off{border-color:var(--line);color:var(--soft)}

/* tareas y leyenda */
.duenos{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:26px;margin-top:22px}
.duen h3{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--grey);font-weight:400;
  margin:0 0 12px;padding-bottom:9px;border-bottom:1px solid var(--line)}
.duen ul{margin:0;padding-left:0;list-style:none}
.duen li{font-size:14px;margin-bottom:11px;padding-left:0}
.duen li b{display:block;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--soft);font-weight:400}
.ley{margin:22px 0 0;padding-left:0;list-style:none;display:grid;
  grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.ley li{font-size:14px;color:var(--grey)}
.ley b{display:block;font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink);font-weight:400;margin-bottom:3px}
footer{margin-top:60px;padding-top:20px;border-top:1px solid var(--line);font-size:12.5px;color:var(--grey);
  display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap}
@media (max-width:940px){
  .head{grid-template-columns:1fr;gap:12px}
  .ejes{max-width:340px}
  .meta{justify-content:flex-start;flex-wrap:wrap}
  .ejes{flex-wrap:wrap;gap:12px}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
</style>

<header><div class="mast">
  <div class="k">Cáscara Founders · panel interno</div>
  <h1>Camada Cáscara Founders</h1>
  <p class="sub">Los veintiún casos con su handicap, ordenados de menor a mayor: arriba está el que más atención necesita. Cada fila abre el documento completo del cliente.</p>
  <div class="stats">
    <div class="stat"><b class="num">__N__</b><span>Clientes</span></div>
    <div class="stat"><b class="num">__PROM__</b><span>Handicap promedio</span></div>
    <div class="stat"><b class="num">__ROJO__</b><span>Ritmo en rojo</span></div>
    <div class="stat"><b class="num">__AMAR__</b><span>Ritmo en amarillo</span></div>
    <div class="stat"><b class="num">__CIERRE__</b><span>En cierre</span></div>
  </div>
</div></header>

<div class="wrap">
  <div class="bar">
    <input id="q" type="search" placeholder="Buscar cliente o proyecto" aria-label="Buscar cliente o proyecto">
    <button class="chip" id="f-todos" data-f="todos" aria-pressed="true">Todos</button>
    <button class="chip" data-f="ori:Conseguir" aria-pressed="false">Conseguir</button>
    <button class="chip" data-f="ori:Sostener" aria-pressed="false">Sostener</button>
    <button class="chip" data-f="ori:Entregar" aria-pressed="false">Entregar</button>
    <button class="chip" data-f="modo:cierre" aria-pressed="false">En cierre</button>
    <button class="chip" data-f="ritmo:rojo" aria-pressed="false">Ritmo rojo</button>
    <button class="chip" data-f="ritmo:amarillo" aria-pressed="false">Ritmo amarillo</button>
  </div>

  <h2>Los veintiún casos</h2>
  <p class="note">Ordenados por handicap de menor a mayor. El eje en negrita es el más flojo y es por donde se trabaja. Tocá cualquier fila para ver la métrica, los accionables de septiembre y lo que queda sin definir.</p>
  <div id="lista">
__FILAS__
  </div>
  <p class="note" id="vacio" hidden>No hay ningún cliente con ese filtro.</p>

  <h2>Qué mide cada eje</h2>
  <p class="note">Cinco ejes de cero a cuatro sobre el estado del negocio, veinte en total. El ritmo va aparte: mide cómo viene ejecutando la persona, no cómo está el negocio.</p>
  <ul class="ley">__LEY__</ul>

  <h2>Lo que espera de Cáscara en septiembre</h2>
  <p class="note">Los accionables de nuestro lado, sacados de las fichas y agrupados por quién los tiene.</p>
  <div class="duenos">__TAREAS__</div>

  <footer><span>Cáscara Founders · panel interno para Facu y Teo</span><span>Actualizado el __FECHA__</span></footer>
</div>

<script>
(function(){
  var lista=document.getElementById('lista'), q=document.getElementById('q'),
      chips=[].slice.call(document.querySelectorAll('.chip')), vacio=document.getElementById('vacio');
  var filtro='todos';
  function aplica(){
    var t=(q.value||'').trim().toLowerCase(), n=0;
    [].forEach.call(lista.children,function(r){
      var ok=true;
      if(filtro!=='todos'){
        var p=filtro.split(':');
        ok = r.getAttribute('data-'+p[0])===p[1];
      }
      if(ok && t) ok = r.getAttribute('data-txt').indexOf(t)>-1;
      r.classList.toggle('hide',!ok); if(ok)n++;
    });
    vacio.hidden = n>0;
  }
  chips.forEach(function(c){c.addEventListener('click',function(){
    filtro=c.getAttribute('data-f');
    chips.forEach(function(o){o.setAttribute('aria-pressed', String(o===c));});
    aplica();
  });});
  q.addEventListener('input',aplica);
  lista.addEventListener('click',function(e){
    var b=e.target.closest('.head'); if(!b)return;
    var d=document.getElementById(b.getAttribute('aria-controls'));
    var abierto=b.getAttribute('aria-expanded')==='true';
    b.setAttribute('aria-expanded',String(!abierto)); d.hidden=abierto;
  });
})();
</script>'''

HTML = (HTML.replace('__FILAS__', filas).replace('__TAREAS__', bloque_tareas)
        .replace('__LEY__', leyenda).replace('__FECHA__', '12 de septiembre de 2026')
        .replace('__N__', str(len(rows))).replace('__PROM__', ('%.1f'%prom).replace('.',','))
        .replace('__ROJO__', str(n_rojo)).replace('__AMAR__', str(n_amar))
        .replace('__CIERRE__', str(n_cierre)))
open('panel.html','w',encoding='utf-8').write(HTML)
print('ok', len(HTML))
