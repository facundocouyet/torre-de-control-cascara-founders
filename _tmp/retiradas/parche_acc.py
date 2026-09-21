# -*- coding: utf-8 -*-
"""Los accionables pasan a ser filas plegables y tildables, y la torre lleva
sello de cuándo se generó. Se corre una sola vez sobre app_shell.py."""
import io, re, sys, datetime

P = sys.argv[1]
src = io.open(P, encoding='utf-8').read()
orig = len(src)

# ─────────────────────────── 1. CSS nuevo ───────────────────────────
CSS_NUEVO = r'''
/* ---------- accionables: filas plegables y tildables ---------- */
.accbar{display:flex;gap:9px;align-items:center;flex-wrap:wrap;margin-top:28px}
.accbar .busq{position:relative;display:flex}
.accbar input[type=search]{appearance:none;-webkit-appearance:none;border:1px solid var(--tiza);
  background:var(--papel2);color:var(--tinta);font-family:var(--disp);font-size:14px;
  padding:10px 13px;min-width:250px;border-radius:0}
.accbar input[type=search]:focus{outline:none;border-color:var(--tinta)}
.accbar button{appearance:none;border:1px solid var(--tiza);background:transparent;color:var(--gris);
  font-family:var(--disp);font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;
  padding:11px 14px;cursor:pointer;transition:border-color .12s,color .12s}
.accbar button:hover{border-color:var(--tinta);color:var(--tinta)}
.accbar .cuenta{margin-left:auto;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--gris2);white-space:nowrap}
.accbar .cuenta b{color:var(--tinta);font-weight:700;font-variant-numeric:tabular-nums}
.accgr{margin-top:38px}
.accgr > .et{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--gris2);
  display:flex;justify-content:space-between;align-items:baseline;gap:14px;
  border-bottom:2px solid var(--tinta);padding-bottom:9px}
.accgr > .nota{font-size:15.5px;line-height:1.55;color:var(--gris);margin:16px 0 0;max-width:72ch}
details.acc{border-bottom:1px solid var(--tiza)}
details.acc > summary{list-style:none;cursor:pointer;display:grid;
  grid-template-columns:14px minmax(0,1fr) auto 52px 62px;gap:18px;align-items:center;
  padding:16px 6px 16px 0}
details.acc > summary::-webkit-details-marker{display:none}
details.acc > summary:hover{background:var(--papel2)}
details.acc.lista{display:none}
.acc .mr{width:8px;height:8px;border-right:1.5px solid var(--gris2);border-bottom:1.5px solid var(--gris2);
  transform:rotate(-45deg);margin-left:3px;transition:transform .15s}
details.acc[open] .mr{transform:rotate(45deg)}
.acc .tx{min-width:0}
.acc .nm{display:block;font-size:19px;font-weight:700;letter-spacing:-.022em;line-height:1.18}
.acc .sb{display:block;font-size:13.5px;color:var(--gris);margin-top:3px;line-height:1.4;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.acc .rt{font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--gris2);
  text-align:right;white-space:nowrap}
.acc .ct{text-align:right;font-variant-numeric:tabular-nums;font-size:12.5px;color:var(--gris2)}
.acc .ct b{font-size:20px;color:var(--tinta);font-weight:700;letter-spacing:-.03em}
.acc .ct.full b{color:var(--gris2)}
.acc .br{height:3px;background:var(--tiza)}
.acc .br i{display:block;height:100%;background:var(--tinta);transition:width .18s}
.acc .ct.full + .br i{background:var(--gris2)}
.acc .cu{padding:2px 0 28px 32px}
.acc .cu .pr{font-size:15.5px;color:var(--gris);max-width:70ch;line-height:1.5}
ul.tl{margin:15px 0 0;padding:0;list-style:none}
ul.tl li{padding:0}
ul.tl label{display:grid;grid-template-columns:16px minmax(0,1fr);gap:14px;align-items:start;
  padding:8px 0;cursor:pointer;font-size:16.5px;line-height:1.5;max-width:74ch}
ul.tl input{appearance:none;-webkit-appearance:none;width:15px;height:15px;border:1.5px solid var(--gris2);
  background:transparent;margin:4px 0 0;cursor:pointer;border-radius:0;position:relative}
ul.tl input:checked{background:var(--tinta);border-color:var(--tinta)}
ul.tl input:checked + span{color:var(--gris2);text-decoration:line-through;text-decoration-thickness:1px}
ul.tl input:checked + span b{color:var(--gris2);font-weight:400}
ul.tl label b{font-weight:700}
.acc .cu .bt{margin-top:18px;display:flex;gap:9px;flex-wrap:wrap}
.acc .cu .bt button{appearance:none;border:1px solid var(--tinta);background:transparent;color:var(--tinta);
  font-family:var(--disp);font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;
  padding:11px 15px;cursor:pointer}
.acc .cu .bt button:hover{background:var(--tinta);color:var(--papel)}
.acc .cu .bt button.ll{background:var(--tinta);color:var(--papel)}
.acc .cu .bt button.ll:hover{opacity:.86}
.acc .cu .sd{font-size:13.5px;color:var(--gris2);margin-top:16px;font-style:italic}
.acc .cu .ups{margin-top:18px;border:1px solid var(--tinta);padding:13px 16px;font-size:15.5px;line-height:1.5}
.acc .cu .ups .k{display:block;font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--gris2);margin-bottom:7px}
.accvacio{font-family:var(--edit);font-style:italic;font-size:17px;color:var(--gris2);margin-top:30px}
@media (max-width:860px){
  details.acc > summary{grid-template-columns:12px minmax(0,1fr) auto;gap:11px;padding:14px 0}
  .acc .br{display:none} .acc .rt{display:none} .acc .cu{padding-left:0}
  .accbar .cuenta{margin-left:0;width:100%}
  .accbar input[type=search]{min-width:0;flex:1}
}

/* ---------- el sello de cuándo se generó la torre ---------- */
.riel .sellob{margin-top:auto;padding:18px 22px 4px;border-top:1px solid rgba(236,234,228,.14);
  font-size:9px;letter-spacing:.16em;text-transform:uppercase;color:rgba(236,234,228,.38);line-height:1.7}
.riel .sellob b{display:block;font-weight:400;color:rgba(236,234,228,.8)}
body.plegado .riel .sellob{display:none}
'''

marca = "\n/* ---------- el visor de cartas ---------- */"
assert src.count(marca) == 1
src = src.replace(marca, CSS_NUEVO + marca)

# ─────────────────── 2. engFila fuera, builders nuevos ───────────────────
def bloque(desde, hasta, nuevo, src):
    i = src.index(desde)
    j = src.index(hasta, i)
    return src[:i] + nuevo + src[j:]

ENG_NUEVO = r'''/* el estado de los accionables vive en este navegador: qué está tildado y qué está abierto */
var KACC='cf-acc-hechos', KABR='cf-acc-abiertos';
function leerL(k){ try{ return JSON.parse(localStorage.getItem(k)||'{}') }catch(e){ return {} } }
function guardarL(k,o){ try{ localStorage.setItem(k,JSON.stringify(o)) }catch(e){} }
var HECHOS=leerL(KACC), ABIERTOS=leerL(KABR);

/* una fila plegada: el nombre, el rótulo y cuánto falta. Se abre y adentro está todo. */
function filaAcc(o){
  var n=o.items.length, li='', ok=0;
  o.items.forEach(function(t,i){
    var id=o.id+'#'+i, m=!!HECHOS[id]; if(m) ok++;
    li+='<li><label><input type="checkbox" data-id="'+id+'"'+(m?' checked':'')+'><span>'+t+'</span></label></li>';
  });
  var pc=n?Math.round(ok/n*100):0;
  return '<details class="acc" data-id="'+o.id+'" data-b="'+esc(o.busca||'')+'"'+(ABIERTOS[o.id]?' open':'')+'>'+
    '<summary><span class="mr"></span>'+
      '<span class="tx"><span class="nm">'+esc(o.nombre)+'</span>'+
        (o.sub?'<span class="sb">'+esc(o.sub)+'</span>':'')+'</span>'+
      '<span class="rt">'+esc(o.rotulo||'')+'</span>'+
      '<span class="ct'+(n&&ok===n?' full':'')+'"><b class="num">'+ok+'</b>/'+n+'</span>'+
      '<span class="br"><i style="width:'+pc+'%"></i></span>'+
    '</summary><div class="cu">'+(o.extra||'')+'<ul class="tl">'+li+'</ul>'+(o.pie||'')+'</div></details>';
}
function pendientes(l){
  var p=0; l.forEach(function(o){ o.items.forEach(function(_,i){ if(!HECHOS[o.id+'#'+i]) p++ }) }); return p;
}
function totalAcc(l){ var t=0; l.forEach(function(o){ t+=o.items.length }); return t; }
function bloqueAcc(rotulo, l, nota){
  if(!l.length) return '';
  return '<div class="accgr"><div class="et"><span>'+esc(rotulo)+'</span>'+
    '<span class="num">'+pendientes(l)+' de '+totalAcc(l)+'</span></div>'+
    (nota?'<p class="nota">'+nota+'</p>':'')+l.map(filaAcc).join('')+'</div>';
}
'''
src = bloque("function engFila(f){", "function verDoc(ruta,titulo,bajar){", ENG_NUEVO, src)

# ─────────────────── 3. los tres panes ───────────────────
PANES = r'''function datosEntrega(){
  var E=D.entregas;
  return E.filas.map(function(f){
    var nm=esc(f.nombre).replace(/'/g,"");
    var b='';
    if(f.doc){
      b='<div class="bt"><button class="ll" onclick="verDoc(\''+f.doc+'\',\''+nm+'\')">Ver el documento</button>'+
        '<button onclick="verDoc(\''+f.doc+'\',\''+nm+'\',1)">Descargar</button>';
      if(f.extra) b+='<button class="ll" onclick="verDoc(\''+f.extra[0]+'\',\''+esc(f.extra[2]).replace(/'/g,"")+'\')">'+esc(f.extra[2])+'</button>';
      b+='</div>';
    } else if(f.nota){ b='<div class="sd">'+f.nota+'</div>' }
    if(f.upselling) b+='<div class="ups"><span class="k">Upselling</span>'+f.upselling+'</div>';
    var c=f.slug?porSlug(f.slug):null;
    return {id:'e/'+(f.slug||f.nombre), nombre:f.nombre, rotulo:f.estado,
            sub:c&&c.cuello?c.cuello:'', extra:'<div class="pr">'+f.proyecto+'</div>'+radResumen(f),
            items:f.accionables, pie:b, sign:/Sign off|Upselling/.test(f.estado),
            busca:(f.nombre+' '+f.proyecto+' '+f.estado).toLowerCase()};
  });
}
function datosFounders(){
  var l=C.filter(function(c){return c.ct&&c.ct.length}); ordenar(l);
  return l.map(function(c){
    return {id:'f/'+c.slug, nombre:c.nombre, rotulo:c.ori+(c.modo==='cierre'?' · cierre':''),
            sub:c.metrica||'', extra:'', items:c.ct.map(esc), pie:'',
            busca:(c.nombre+' '+(c.metrica||'')+' '+c.ori).toLowerCase()};
  });
}
function datosCascara(){
  return D.tareas.map(function(t){
    return {id:'t/'+t.d, nombre:t.d, rotulo:'De este lado', sub:'', extra:'',
            items:t.items.map(function(i){return '<b>'+esc(i.c)+'</b> '+esc(i.t)}), pie:'',
            busca:(t.d+' '+t.items.map(function(i){return i.c+' '+i.t}).join(' ')).toLowerCase()};
  });
}

function paneEntrega(){
  var E=D.entregas, L=ACC.entrega;
  var sign=L.filter(function(o){return o.sign}), curso=L.filter(function(o){return !o.sign});
  var h='<p class="entrada" style="margin-top:32px">Lo que ejecuta Aye con cada cliente: el documento que le '+
    'corresponde, qué hay que hacer con él y qué coordinar. Se abre el cliente y adentro está su radiografía '+
    'y la lista para ir tildando.</p>';
  h+='<div class="regla">'+E.intro.map(function(x,i){
      return '<div><span class="k">'+('0'+(i+1)).slice(-2)+'</span>'+x+'</div>'}).join('')+'</div>';
  h+=barraAcc('entrega');
  h+=bloqueAcc('Sign off', sign, '<b>Cómo funciona un sign off.</b> '+E.regla_signoff.join(' '));
  h+=bloqueAcc('En curso', curso);
  h+='<div class="accgr"><div class="et"><span>Lo que falta cargar</span>'+
     '<span class="num">'+E.falta.length+'</span></div><ul class="check" style="margin-top:20px">'+
     E.falta.map(function(x){return '<li><span>'+x+'</span></li>'}).join('')+'</ul></div>';
  h+='<div class="accgr"><div class="et"><span>Lo que le toca a Aye</span>'+
     '<span class="num">'+E.aye.length+'</span></div><div class="aye">'+
     E.aye.map(function(x){return '<div class="q">'+esc(x[0])+'</div><div class="a">'+x[1]+'</div>'}).join('')+
     '</div></div>';
  h+='<div class="crit"><div class="k">Un solo criterio</div><p>'+E.criterio+'</p></div>';
  return h;
}
function paneFounders(){
  return '<p class="entrada" style="margin-top:32px">Lo que cada founder tiene que ejecutar. Sale del roadmap '+
    'de su propio documento, así que es lo mismo que él está leyendo.</p>'+
    barraAcc('founders')+bloqueAcc('Los founders', ACC.founders);
}
function paneCascara(){
  var conRep=C.filter(function(c){return c.rep&&c.rep.length});
  var h='<p class="entrada" style="margin-top:32px">Dos cosas distintas. Arriba, lo que alguien de Cáscara '+
    'todavía tiene que hacer y no está escrito adentro del documento del founder. Abajo, quién toma cada caso '+
    'en este tramo, que es un rótulo y se lee de un vistazo.</p>';
  h+=barraAcc('cascara')+bloqueAcc('Cada uno de nosotros', ACC.cascara);
  ordenar(conRep);
  h+='<div class="accgr"><div class="et"><span>Quién toma cada caso</span>'+
     '<span class="num">'+conRep.length+'</span></div><div class="eng" style="margin-top:0">';
  conRep.forEach(function(c){
    h+='<div class="f"><div class="top"><div class="nm">'+esc(c.nombre)+'</div>'+
       '<div class="es">'+esc(c.ori)+(c.modo==='cierre'?' · cierre':'')+'</div></div>'+
       '<ul class="rpt">'+c.rep.map(function(r){
          return '<li><b>'+esc(r[0])+'</b> <span>'+esc(r[1])+'</span></li>'}).join('')+'</ul></div>';});
  return h+'</div></div>';
}
'''
src = bloque("function paneEntrega(){", "var PANE_ACC='entrega';", PANES, src)

# ─────────────────── 4. la vista, con barra y contador ───────────────────
VISTA = r'''var PANE_ACC='entrega', ACC={};
function barraAcc(k){
  return '<div class="accbar" data-p="'+k+'">'+
    '<span class="busq"><input type="search" data-q="'+k+'" placeholder="Buscar" aria-label="Buscar"></span>'+
    '<button data-a="abrir">Abrir todo</button><button data-a="cerrar">Cerrar todo</button>'+
    '<span class="cuenta" data-c="'+k+'"></span></div>';
}
function vAccionables(){
  ACC={entrega:datosEntrega(), founders:datosFounders(), cascara:datosCascara()};
  var h='<div class="hoja">'+migas(['Accionables'])+encab('Accionables','Lo que hay que hacer','',
    'Se actualiza con los clientes');
  h+='<div class="conm" role="group" aria-label="Qué accionables">'+
    '<button data-p="entrega">Accionables CSM · <b data-p2="entrega">'+pendientes(ACC.entrega)+'</b></button>'+
    '<button data-p="founders">Cada founder · <b data-p2="founders">'+pendientes(ACC.founders)+'</b></button>'+
    '<button data-p="cascara">Adentro de Cáscara · <b data-p2="cascara">'+pendientes(ACC.cascara)+'</b></button></div>';
  h+='<div class="pane" id="p-entrega">'+paneEntrega()+'</div>'+
     '<div class="pane" id="p-founders">'+paneFounders()+'</div>'+
     '<div class="pane" id="p-cascara">'+paneCascara()+'</div>';
  h+='</div>';
  var V=$('#v-accionables');
  V.innerHTML=h;
  V.querySelectorAll('.conm button').forEach(function(b){
    b.addEventListener('click',function(){PANE_ACC=b.dataset.p;pintaAcc()})});
  /* tildar un accionable */
  V.addEventListener('change',function(e){
    var i=e.target; if(i.type!=='checkbox'||!i.dataset.id) return;
    if(i.checked) HECHOS[i.dataset.id]=1; else delete HECHOS[i.dataset.id];
    guardarL(KACC,HECHOS); contarAcc();
  });
  /* recordar qué quedó abierto */
  V.addEventListener('toggle',function(e){
    var d=e.target; if(!d.dataset||!d.classList.contains('acc')) return;
    if(d.open) ABIERTOS[d.dataset.id]=1; else delete ABIERTOS[d.dataset.id];
    guardarL(KABR,ABIERTOS);
  },true);
  /* abrir todo, cerrar todo y buscar */
  V.querySelectorAll('.accbar button').forEach(function(b){
    b.addEventListener('click',function(){
      var p=b.closest('.accbar').dataset.p, ab=b.dataset.a==='abrir';
      $('#p-'+p).querySelectorAll('details.acc').forEach(function(d){d.open=ab});
    })});
  V.querySelectorAll('.accbar input[type=search]').forEach(function(q){
    q.addEventListener('input',function(){
      var t=q.value.trim().toLowerCase();
      $('#p-'+q.dataset.q).querySelectorAll('details.acc').forEach(function(d){
        d.classList.toggle('lista', !!t && d.dataset.b.indexOf(t)<0)});
      var gr=$('#p-'+q.dataset.q).querySelectorAll('.accgr');
      gr.forEach(function(g){
        var det=g.querySelectorAll('details.acc');
        if(det.length) g.style.display=[].slice.call(det).some(function(d){return !d.classList.contains('lista')})?'':'none';
      });
    })});
  contarAcc(); pintaAcc();
}
/* el contador: lo que falta, arriba de cada pane y en los botones */
function contarAcc(){
  var V=$('#v-accionables'); if(!V) return;
  ['entrega','founders','cascara'].forEach(function(k){
    var l=ACC[k]||[], p=pendientes(l), t=totalAcc(l);
    var c=V.querySelector('[data-c="'+k+'"]');
    if(c) c.innerHTML='<b>'+p+'</b> sin hacer · '+(t-p)+' de '+t+' listos';
    var n=V.querySelector('[data-p2="'+k+'"]'); if(n) n.textContent=p;
    var g=V.querySelectorAll('#p-'+k+' .accgr > .et .num');
    var i=0;
    V.querySelectorAll('#p-'+k+' .accgr').forEach(function(gr){
      var det=gr.querySelectorAll('details.acc'); if(!det.length) return;
      var pp=0, tt=0;
      det.forEach(function(d){
        var ch=d.querySelectorAll('.tl input'); tt+=ch.length;
        ch.forEach(function(x){ if(!x.checked) pp++ });
        var ok=ch.length-[].slice.call(ch).filter(function(x){return !x.checked}).length;
        var ct=d.querySelector('.ct'), br=d.querySelector('.br i');
        if(ct){ ct.innerHTML='<b class="num">'+ok+'</b>/'+ch.length;
                ct.classList.toggle('full', ch.length>0&&ok===ch.length); }
        if(br) br.style.width=(ch.length?Math.round(ok/ch.length*100):0)+'%';
      });
      var et=gr.querySelector('.et .num'); if(et) et.textContent=pp+' de '+tt;
    });
  });
}
'''
src = bloque("var PANE_ACC='entrega';", "function pintaAcc(){", VISTA, src)

# ─────────────────── 5. el sello: cuándo se generó ───────────────────
hoy = datetime.datetime.utcnow() - datetime.timedelta(hours=3)   # Buenos Aires
ISO = hoy.strftime('%Y-%m-%dT%H:%M:00-03:00')
TXT = hoy.strftime('%d/%m/%Y · %H:%M')

SELLO_JS = r'''
/* ---------------- el sello: cuándo se generó esta torre ---------------- */
var SELLO={iso:'__ISO__', txt:'__TXT__'};
function haceCuanto(){
  var s=Math.max(0,(Date.now()-new Date(SELLO.iso).getTime())/1000);
  if(s<90) return 'recién';
  if(s<5400) return 'hace '+Math.max(1,Math.round(s/60))+' min';
  if(s<172800) return 'hace '+Math.round(s/3600)+' horas';
  return 'hace '+Math.round(s/86400)+' días';
}
function pintaSello(){
  var t=haceCuanto();
  document.querySelectorAll('[data-sello]').forEach(function(e){
    e.innerHTML='<b>Actualizada '+t+'</b>'+SELLO.txt;});
  var f=$('#fmov'); if(f) f.textContent='Actualizada '+t;
}
pintaSello(); setInterval(pintaSello,30000);
'''.replace('__ISO__', ISO).replace('__TXT__', TXT)

ancla = "$('#fmov').textContent=D.fecha;\n"
assert src.count(ancla) == 1
src = src.replace(ancla, SELLO_JS + "\n")

# el sello en el riel
riel = '  <nav role="tablist" aria-label="Secciones">{NAV}</nav>\n</aside>'
assert src.count(riel) == 1
src = src.replace(riel,
  '  <nav role="tablist" aria-label="Secciones">{NAV}</nav>\n'
  '  <div class="sellob" data-sello title="Cuándo se generó esta versión de la torre"></div>\n</aside>')

io.open(P, 'w', encoding='utf-8').write(src)
print('app_shell.py:', orig, '->', len(src), '· sello', TXT)
