# -*- coding: utf-8 -*-
"""Los accionables arrancan con un checklist simple; el detalle de cada caso
—documento, carta, seguimiento— queda abajo."""
import io, sys
P = sys.argv[1]
s = io.open(P, encoding='utf-8').read()

def bloque(desde, hasta, nuevo):
    global s
    i = s.index(desde); j = s.index(hasta, i)
    s = s[:i] + nuevo + s[j:]

# ───────────── el motor: estado, checklist y filas de detalle ─────────────
MOTOR = r'''/* el estado de los accionables vive en este navegador: qué está tildado y qué está abierto */
var KACC='cf-acc-hechos', KABR='cf-acc-abiertos';
function leerL(k){ try{ return JSON.parse(localStorage.getItem(k)||'{}') }catch(e){ return {} } }
function guardarL(k,o){ try{ localStorage.setItem(k,JSON.stringify(o)) }catch(e){} }
var HECHOS=leerL(KACC), ABIERTOS=leerL(KABR);

function pendientes(l){
  var p=0; l.forEach(function(o){ o.items.forEach(function(_,i){ if(!HECHOS[o.id+'#'+i]) p++ }) }); return p;
}
function totalAcc(l){ var t=0; l.forEach(function(o){ t+=o.items.length }); return t; }

/* el checklist: una línea por cosa, el nombre a la izquierda */
function checklist(l){
  var h='<div class="chk">';
  l.forEach(function(o){
    h+='<div class="chgr" data-b="'+esc(o.busca||'')+'"><div class="qn"><b>'+esc(o.nombre)+'</b>'+
       (o.rotulo?'<span>'+esc(o.rotulo)+'</span>':'')+'</div><ul>';
    o.items.forEach(function(t,i){
      var id=o.id+'#'+i;
      h+='<li><label><input type="checkbox" data-id="'+id+'"'+(HECHOS[id]?' checked':'')+
         '><span>'+t+'</span></label></li>';
    });
    h+='</ul></div>';
  });
  return h+'</div>';
}
function grupoChk(rotulo, l, antes){
  if(!l.length) return '';
  return '<div class="accgr" data-g><div class="et"><span>'+esc(rotulo)+'</span>'+
    '<span class="num">'+(totalAcc(l)-pendientes(l))+' de '+totalAcc(l)+' hechos</span></div>'+
    (antes||'')+checklist(l)+'</div>';
}

/* el detalle de un caso: la radiografía, el documento que sale y lo que haya que seguir */
function filaAcc(o){
  var n=o.items.length, ok=0;
  o.items.forEach(function(_,i){ if(HECHOS[o.id+'#'+i]) ok++ });
  return '<details class="acc" data-id="'+o.id+'" data-b="'+esc(o.busca||'')+'"'+(ABIERTOS[o.id]?' open':'')+'>'+
    '<summary><span class="mr"></span>'+
      '<span class="tx"><span class="nm">'+esc(o.nombre)+'</span>'+
        (o.sub?'<span class="sb">'+esc(o.sub)+'</span>':'')+'</span>'+
      '<span class="rt">'+esc(o.rotulo||'')+'</span>'+
      '<span class="ct'+(n&&ok===n?' full':'')+'"><b class="num">'+ok+'</b>/'+n+'</span>'+
      '<span class="br"><i style="width:'+(n?Math.round(ok/n*100):0)+'%"></i></span>'+
    '</summary><div class="cu">'+(o.extra||'')+(o.pie||'')+'</div></details>';
}
'''
bloque("/* el estado de los accionables vive", "function verDoc(ruta,titulo,bajar){", MOTOR)

# ───────────── los panes y la vista ─────────────
VISTA = r'''function datosEntrega(){
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
    return {id:'t/'+t.d, nombre:t.d, rotulo:'', sub:'', extra:'',
            items:t.items.map(function(i){return '<b>'+esc(i.c)+'</b> '+esc(i.t)}), pie:'',
            busca:(t.d+' '+t.items.map(function(i){return i.c+' '+i.t}).join(' ')).toLowerCase()};
  });
}

function paneEntrega(){
  var E=D.entregas, L=ACC.entrega;
  var sign=L.filter(function(o){return o.sign}), curso=L.filter(function(o){return !o.sign});
  var h='<p class="entrada" style="margin-top:32px">Lo que ejecuta Aye, en una sola lista. Abajo, caso por '+
    'caso, está el documento que sale para cada uno y lo que haya que seguir.</p>';
  h+=barraAcc('entrega');
  h+=grupoChk('Sign off', sign);
  h+=grupoChk('En curso', curso);
  h+='<div class="accgr"><div class="et"><span>Caso por caso</span>'+
     '<span class="num">'+L.length+' clientes</span></div>'+
     '<p class="nota">El documento que sale para cada uno, con qué se lo ubica y lo que quedó de antes. '+
     'Se abre el que haga falta.</p>'+L.map(filaAcc).join('')+'</div>';
  h+='<div class="accgr"><div class="et"><span>Cómo se trabaja</span><span class="num">El criterio</span></div>'+
     '<div class="regla" style="margin-top:20px">'+E.intro.map(function(x,i){
        return '<div><span class="k">'+('0'+(i+1)).slice(-2)+'</span>'+x+'</div>'}).join('')+'</div>'+
     '<div class="reg"><div class="k">Cómo funciona un sign off</div><ul>'+
     E.regla_signoff.map(function(x){return '<li>'+x+'</li>'}).join('')+'</ul></div>'+
     '<div class="reg"><div class="k">Lo que falta cargar</div><ul>'+
     E.falta.map(function(x){return '<li>'+x+'</li>'}).join('')+'</ul></div>'+
     '<div class="aye">'+E.aye.map(function(x){
        return '<div class="q">'+esc(x[0])+'</div><div class="a">'+x[1]+'</div>'}).join('')+'</div>'+
     '<div class="crit"><div class="k">Un solo criterio</div><p>'+E.criterio+'</p></div></div>';
  return h;
}
function paneFounders(){
  return '<p class="entrada" style="margin-top:32px">Lo que cada founder tiene que ejecutar. Sale del roadmap '+
    'de su propio documento, así que es lo mismo que él está leyendo.</p>'+
    barraAcc('founders')+grupoChk('Los founders', ACC.founders);
}
function paneCascara(){
  var conRep=C.filter(function(c){return c.rep&&c.rep.length});
  var h='<p class="entrada" style="margin-top:32px">Lo que alguien de Cáscara todavía tiene que hacer y no '+
    'está escrito adentro del documento del founder.</p>';
  h+=barraAcc('cascara')+grupoChk('Cada uno de nosotros', ACC.cascara);
  ordenar(conRep);
  h+='<div class="accgr"><div class="et"><span>Quién toma cada caso</span>'+
     '<span class="num">'+conRep.length+' clientes</span></div><div class="eng" style="margin-top:0">';
  conRep.forEach(function(c){
    h+='<div class="f"><div class="top"><div class="nm">'+esc(c.nombre)+'</div>'+
       '<div class="es">'+esc(c.ori)+(c.modo==='cierre'?' · cierre':'')+'</div></div>'+
       '<ul class="rpt">'+c.rep.map(function(r){
          return '<li><b>'+esc(r[0])+'</b> <span>'+esc(r[1])+'</span></li>'}).join('')+'</ul></div>';});
  return h+'</div></div>';
}

var PANE_ACC='entrega', ACC={};
function barraAcc(k){
  return '<div class="accbar" data-p="'+k+'">'+
    '<span class="busq"><input type="search" data-q="'+k+'" placeholder="Buscar" aria-label="Buscar"></span>'+
    '<button data-a="limpiar">Destildar todo</button>'+
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
  /* tildar: el checklist y el detalle del caso quedan iguales */
  V.addEventListener('change',function(e){
    var i=e.target; if(i.type!=='checkbox'||!i.dataset.id) return;
    var id=i.dataset.id;
    if(i.checked) HECHOS[id]=1; else delete HECHOS[id];
    guardarL(KACC,HECHOS);
    V.querySelectorAll('input[data-id="'+id+'"]').forEach(function(x){x.checked=i.checked});
    contarAcc();
  });
  /* recordar qué caso quedó abierto */
  V.addEventListener('toggle',function(e){
    var d=e.target; if(!d.classList||!d.classList.contains('acc')) return;
    if(d.open) ABIERTOS[d.dataset.id]=1; else delete ABIERTOS[d.dataset.id];
    guardarL(KABR,ABIERTOS);
  },true);
  /* destildar todo el pane */
  V.querySelectorAll('.accbar button').forEach(function(b){
    b.addEventListener('click',function(){
      var p=b.closest('.accbar').dataset.p;
      $('#p-'+p).querySelectorAll('input[data-id]').forEach(function(x){
        x.checked=false; delete HECHOS[x.dataset.id]});
      guardarL(KACC,HECHOS); contarAcc();
    })});
  /* buscar por cliente */
  V.querySelectorAll('.accbar input[type=search]').forEach(function(q){
    q.addEventListener('input',function(){
      var t=q.value.trim().toLowerCase(), P=$('#p-'+q.dataset.q);
      P.querySelectorAll('.chgr,details.acc').forEach(function(d){
        d.classList.toggle('lista', !!t && (d.dataset.b||'').indexOf(t)<0)});
      P.querySelectorAll('.accgr[data-g]').forEach(function(g){
        var fs=g.querySelectorAll('.chgr');
        g.style.display=[].slice.call(fs).some(function(d){return !d.classList.contains('lista')})?'':'none';
      });
    })});
  contarAcc(); pintaAcc();
}
/* el contador: lo que falta, arriba de cada pane, en los botones y en cada grupo */
function contarAcc(){
  var V=$('#v-accionables'); if(!V) return;
  ['entrega','founders','cascara'].forEach(function(k){
    var l=ACC[k]||[], p=pendientes(l), t=totalAcc(l);
    var c=V.querySelector('[data-c="'+k+'"]');
    if(c) c.innerHTML='<b>'+p+'</b> sin hacer · '+(t-p)+' de '+t+' listos';
    var n=V.querySelector('[data-p2="'+k+'"]'); if(n) n.textContent=p;
    V.querySelectorAll('#p-'+k+' .accgr[data-g]').forEach(function(gr){
      var ch=gr.querySelectorAll('.chk input'), ok=0;
      ch.forEach(function(x){ if(x.checked) ok++ });
      var et=gr.querySelector('.et .num');
      if(et) et.textContent=ok+' de '+ch.length+' hechos';
    });
    V.querySelectorAll('#p-'+k+' details.acc').forEach(function(d){
      var o=null; (ACC[k]||[]).forEach(function(x){ if(x.id===d.dataset.id) o=x });
      if(!o) return;
      var ok=0; o.items.forEach(function(_,i){ if(HECHOS[o.id+'#'+i]) ok++ });
      var ct=d.querySelector('.ct'), br=d.querySelector('.br i');
      if(ct){ ct.innerHTML='<b class="num">'+ok+'</b>/'+o.items.length;
              ct.classList.toggle('full', o.items.length>0&&ok===o.items.length); }
      if(br) br.style.width=(o.items.length?Math.round(ok/o.items.length*100):0)+'%';
    });
  });
}
'''
bloque("function datosEntrega(){", "function pintaAcc(){", VISTA)

# ───────────── el CSS del checklist ─────────────
CSS = r'''
.chk{margin-top:4px}
.chgr{display:grid;grid-template-columns:215px minmax(0,1fr);gap:24px;align-items:start;
  border-bottom:1px solid var(--tiza);padding:15px 0}
.chgr.lista{display:none}
.chgr .qn b{display:block;font-size:16.5px;font-weight:700;letter-spacing:-.018em;line-height:1.25;
  padding-top:7px}
.chgr .qn span{display:block;font-size:9px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--gris2);margin-top:5px}
.chgr ul{margin:0;padding:0;list-style:none}
.chgr li{padding:0}
'''
marca = "\n/* ---------- el sello de cuándo se generó la torre ---------- */"
assert s.count(marca) == 1
s = s.replace(marca, CSS + marca)

# el checklist usa las mismas casillas que la lista de la ficha
s = s.replace("ul.tl{margin:15px 0 0;padding:0;list-style:none}",
              "ul.tl{margin:15px 0 0;padding:0;list-style:none}")
s = s.replace("ul.tl label{", ".chgr label,ul.tl label{")
s = s.replace("ul.tl input{", ".chgr input,ul.tl input{")
s = s.replace("ul.tl input:checked{", ".chgr input:checked,ul.tl input:checked{")
s = s.replace("ul.tl input:checked + span{", ".chgr input:checked + span,ul.tl input:checked + span{")
s = s.replace("ul.tl input:checked + span b{", ".chgr input:checked + span b,ul.tl input:checked + span b{")
s = s.replace("ul.tl label b{", ".chgr label b,ul.tl label b{")

CSSM = r'''
@media (max-width:860px){
  .chgr{grid-template-columns:1fr;gap:4px}
  .chgr .qn b{padding-top:0}
}
'''
s = s.replace(marca, CSSM + marca)

io.open(P, 'w', encoding='utf-8').write(s)
print('ok', len(s))
