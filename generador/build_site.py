# -*- coding: utf-8 -*-
"""Genera el sitio de Cáscara Founders. Sin dependencias: python3 build_site.py"""
import json, html as _h, os, shutil, sys, glob
def e(s): return _h.escape(str(s or ""))
BASE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(BASE,'site')
FECHA="12 de septiembre de 2026"

NAV=[("index.html","El tablero"),("programa.html","El programa"),
     ("materiales.html","Los materiales"),("clientes.html","Los clientes")]

def pagina(archivo, titulo, cuerpo, raiz="."):
    nav="".join('<a href="%s/%s"%s>%s</a>' % (raiz,u," aria-current=\"page\"" if u==archivo else "",e(t))
                for u,t in NAV)
    return f'''<!doctype html>
<html lang="es"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)} · Cáscara Founders</title>
<meta name="description" content="Tablero de control de Cáscara Founders: el programa, los materiales y los clientes.">
<link rel="stylesheet" href="{raiz}/assets/founders.css">
</head><body>
<header class="topbar"><div class="wrap">
  <a class="marca" href="{raiz}/index.html"><b>Cáscara Founders</b><span>Tablero</span></a>
  <nav class="nav" aria-label="Secciones">{nav}</nav>
</div></header>
{cuerpo}
<div class="wrap"><footer class="pie">
  <span>Cáscara Founders · Cáscara Collective</span>
  <span>Actualizado el {FECHA}</span>
</footer></div>
</body></html>'''

def masthead(kicker, titulo, bajada, cifras=None, display=False):
    c=""
    if cifras:
        c='<div class="cifras">'+"".join(
          '<div class="cifra"><b>%s</b><span>%s</span></div>'%(e(v),e(k)) for v,k in cifras)+'</div>'
    return f'''<section class="masthead"><div class="wrap">
  <span class="kicker">{e(kicker)}</span>
  <h1 class="{'display' if display else ''}">{e(titulo)}</h1>
  <p class="bajada">{e(bajada)}</p>
  {c}
</div></section>'''

# ---------------------------------------------------------------- TABLERO
def build_index(panel):
    con=[r for r in panel if r['handicap']]
    prom=sum(r['handicap']['total'] for r in con)/len(con)
    rojo=[r for r in con if r['handicap']['ritmo']=='rojo']
    amar=[r for r in con if r['handicap']['ritmo']=='amarillo']
    cierre=[r for r in panel if r['modo']=='cierre']
    atencion=sorted(con,key=lambda r:r['handicap']['total'])[:5]

    zonas=[
      ("01","El programa","programa.html",
       "Qué es Cáscara Founders, cómo corre el proceso de noventa días, las tres orientaciones y qué se le lleva a cada mentor. Es lo que se le muestra a alguien que entra, sea del equipo o cliente."),
      ("02","Los materiales","materiales.html",
       "La biblioteca entera: la oferta y lo comercial, los documentos de cliente, los contratos y los procesos internos. Con los módulos por categoría y lo que todavía falta escribir."),
      ("03","Los clientes","clientes.html",
       "Los veintiún casos con su handicap, ordenados por quién necesita más atención. Cada fila abre el documento completo del founder."),
    ]
    zh="".join(f'''<a class="card" href="{u}" style="text-decoration:none;display:block">
      <span class="label">{n}</span>
      <h2 class="mt2">{e(t)}</h2>
      <p class="texto mt3" style="color:var(--grey)">{e(d)}</p>
      <span class="btn chico mt4">Entrar</span>
    </a>''' for n,t,u,d in zonas)

    def mini(r):
        h=r['handicap']
        barras="".join('<span class="eje %s"><span class="nombre">%s</span><span class="barras">%s</span></span>'%(
            "flojo" if k in h['eje_flojo'] else "", e(n[:3]),
            "".join('<i%s></i>'%("" if j<h['ejes'][k] else ' class="vacia"') for j in range(4)))
            for k,n in [("oferta","Oferta"),("contenido","Contenido"),("demanda","Demanda"),
                        ("venta","Venta"),("entrega","Entrega")])
        rc={"verde":"ok","amarillo":"warn","rojo":"bad"}[h['ritmo']]
        doc = f'clientes/{r["slug"]}.html' if r['doc'] else 'clientes.html'
        return f'''<a class="fila" href="{doc}" style="text-decoration:none;display:grid;
      grid-template-columns:minmax(0,1fr) 350px 150px;gap:var(--s3);align-items:center">
      <span><b style="font-size:var(--t-h3);font-weight:700;letter-spacing:-.02em">{e(r['cliente'])}</b>
        <span class="small" style="display:block">{e(r['cuello'])}</span></span>
      <span class="ejes">{barras}</span>
      <span style="display:flex;align-items:center;gap:14px">
        <span class="num" style="font-size:24px">{h['total']}</span>
        <span class="chip {rc}">{e(h['ritmo'])}</span></span>
    </a>'''

    cuerpo = masthead("Cáscara Founders · tablero de control",
      "Todo Cáscara Founders, en un solo lugar",
      "El programa, los materiales y los clientes. Se actualiza solo todas las mañanas con lo que salió de las llamadas del día anterior.",
      [(str(len(panel)),"Clientes"),("%.1f"%prom,"Handicap promedio"),
       (str(len(cierre)),"En cierre"),(str(len(rojo)),"Ritmo en rojo")], display=True)

    cuerpo += f'''<section class="zona"><div class="wrap">
  <h2 class="seccion">Las tres zonas</h2>
  <div class="cols cols-3 mt4">{zh}</div>
</div></section>

<section class="zona"><div class="wrap">
  <h2 class="seccion">Quién necesita atención esta semana</h2>
  <p class="small mt3" style="max-width:70ch">Los cinco handicaps más bajos de la camada. El eje en negrita es el más flojo y es por donde se trabaja.</p>
  <div class="mt4">{"".join(mini(r) for r in atencion)}</div>
  <a class="btn mt4" href="clientes.html">Ver los veintiuno</a>
</div></section>

<section class="zona"><div class="wrap">
  <h2 class="seccion">Cómo se mantiene</h2>
  <div class="cols cols-3 mt4">
    <div class="dato"><span class="label">Todas las mañanas</span>
      <p class="texto mt2">Una tarea barre las llamadas nuevas de Fathom, actualiza la ficha de cada cliente que aparece, recalcula el handicap si algún eje se movió y vuelve a publicar. Si no hubo llamadas nuevas, no toca nada.</p></div>
    <div class="dato"><span class="label">Dónde vive el dato</span>
      <p class="texto mt2">Las fichas de los clientes están en el Project de Cáscara, en un solo JSON. Los estados y las fechas viven en la base Cuentas de Notion. El sitio se genera desde ahí, no al revés.</p></div>
    <div class="dato"><span class="label">Quién lo toca</span>
      <p class="texto mt2">Facu desarrolla los informes y los cierres. Teo hace las llamadas de sign-off y los onboardings. El sitio se regenera con un comando y se sube como archivos estáticos.</p></div>
  </div>
</div></section>'''
    return pagina("index.html","El tablero",cuerpo)

# ---------------------------------------------------------------- PROGRAMA
def build_programa(d):
    c = masthead(d['kicker'], d['titulo'], d['bajada'])

    q=d['que_es']
    c += f'''<section class="zona"><div class="wrap">
  <h2 class="seccion">{e(q['titulo'])}</h2>
  <p class="texto mt4" style="font-size:clamp(17px,1.9vw,21px);line-height:1.55">{e(q['texto'])}</p>
</div></section>'''

    c += '<section class="zona"><div class="wrap"><h2 class="seccion">Para quién es</h2><div class="cols cols-3 mt4">'
    c += "".join(f'<div class="dato"><h3>{e(x["titulo"])}</h3><p class="texto mt2" style="color:var(--grey)">{e(x["texto"])}</p></div>' for x in d['para_quien'])
    c += '</div></div></section>'

    pasos="".join(f'''<div class="fila" style="display:grid;grid-template-columns:64px 190px minmax(0,1fr);gap:var(--s3);align-items:start">
      <span class="num" style="font-size:26px;color:var(--grey)">{e(x['n'])}</span>
      <span class="label" style="padding-top:6px">{e(x['cuando'])}</span>
      <span><b style="font-size:var(--t-h3);font-weight:700;letter-spacing:-.02em;display:block">{e(x['titulo'])}</b>
        <span class="texto small mt2" style="display:block;font-size:var(--t-body)">{e(x['texto'])}</span></span>
    </div>''' for x in d['proceso'])
    c += f'''<section class="zona"><div class="wrap">
  <h2 class="seccion">El proceso, paso por paso</h2>
  <div class="mt4">{pasos}</div>
</div></section>'''

    ori="".join(f'''<div class="card">
      <span class="label">Orientación</span>
      <h2 class="mt2">{e(o['nombre'])}</h2>
      <p class="small mt2">Lo lidera {e(o['lider'])}</p>
      <p class="texto mt3" style="color:var(--grey)">{e(o['texto'])}</p>
      <p class="nota mt3">Se elige cuando {e(o['cuando_se_elige'])}</p>
      <ul class="mt3" style="padding-left:18px;margin:0">{"".join('<li class="small" style="margin-bottom:6px">%s</li>'%e(m) for m in o['modulos'])}</ul>
    </div>''' for o in d['orientaciones'])
    c += f'''<section class="zona tinta"><div class="wrap">
  <h2 class="seccion">Las tres orientaciones</h2>
  <p class="bajada mt3">Terminado el primer mes se elige una sola. No son caminos exactos: son conjuntos de módulos, y el cliente tiene que saber en cuál está.</p>
  <div class="cols cols-3 mt5">{ori}</div>
</div></section>'''

    men="".join(f'''<div class="fila">
      <div style="display:flex;justify-content:space-between;gap:var(--s3);flex-wrap:wrap;align-items:baseline">
        <h3>{e(m['nombre'])}</h3><span class="chip">{e(m['rol'])}</span></div>
      <div class="cols cols-2 mt3">
        <div class="dato"><span class="label">Qué traerle</span><p class="texto mt2">{e(m['que_traerle'])}</p></div>
        <div class="dato"><span class="label">Qué no</span><p class="texto mt2" style="color:var(--grey)">{e(m['que_no'])}</p></div>
      </div>
    </div>''' for m in d['mentores'])
    c += f'''<section class="zona"><div class="wrap">
  <h2 class="seccion">Los mentores y qué se le lleva a cada uno</h2>
  <div class="mt4">{men}</div>
</div></section>'''

    gr="".join(f'''<div class="dato"><span class="label">{e(g['cuando'])}</span>
      <h3 class="mt2">{e(g['nombre'])}</h3>
      <p class="small" style="margin-top:4px">{e(g['quien'])}</p>
      <p class="texto mt2" style="color:var(--grey)">{e(g['texto'])}</p></div>''' for g in d['grupales'])
    c += f'''<section class="zona"><div class="wrap">
  <h2 class="seccion">Las grupales</h2>
  <div class="cols cols-4 mt4">{gr}</div>
</div></section>'''

    h=d['handicap']
    ejes="".join(f'''<div class="dato"><span class="label">{e(x['nombre'])}</span>
      <p class="texto mt2" style="color:var(--grey)">{e(x['que_mide'])}</p></div>''' for x in h['ejes'])
    tr="".join('<span class="chip">%s</span>'%e(t) for t in h['tramos'])
    c += f'''<section class="zona"><div class="wrap">
  <h2 class="seccion">El handicap</h2>
  <p class="bajada mt3">{e(h['texto'])}</p>
  <div class="cols cols-5 mt5" style="grid-template-columns:repeat(auto-fit,minmax(190px,1fr))">{ejes}</div>
  <div class="mt5" style="display:flex;gap:var(--s4);flex-wrap:wrap;align-items:flex-start">
    <div><span class="label">Tramos</span><div class="mt2" style="display:flex;gap:8px;flex-wrap:wrap">{tr}</div></div>
    <div style="flex:1;min-width:300px"><span class="label">El ritmo va aparte</span>
      <p class="texto mt2">{e(h['ritmo'])}</p></div>
  </div>
</div></section>'''

    g=d['graduacion']
    pr="".join('<li class="texto" style="margin-bottom:12px">%s</li>'%e(p) for p in d['principios'])
    c += f'''<section class="zona tinta"><div class="wrap">
  <div class="cols cols-2" style="gap:var(--s6)">
    <div><h2 class="seccion">{e(g['titulo'])}</h2>
      <p class="texto mt4">{e(g['texto'])}</p></div>
    <div><h2 class="seccion">Los principios</h2>
      <ol class="mt4" style="padding-left:20px;margin:0">{pr}</ol></div>
  </div>
</div></section>'''
    return pagina("programa.html","El programa",c)

# ---------------------------------------------------------------- MATERIALES
def build_materiales(d):
    c = masthead(d['kicker'], d['titulo'], d['bajada'])
    EST={"listo":"ok","en borrador":"warn","falta escribir":"bad"}
    for b in d['bloques']:
        piezas="".join(f'''<div class="fila">
          <div style="display:flex;justify-content:space-between;gap:var(--s3);flex-wrap:wrap;align-items:baseline">
            <h3>{e(p['titulo'])}</h3>
            <span class="chip {EST.get(p.get('estado'),'')}">{e(p.get('estado',''))}</span></div>
          <p class="texto mt2" style="color:var(--grey)">{e(p['que_es'])}</p>
          {('<div class="mt3" style="display:flex;gap:8px;flex-wrap:wrap">' + "".join('<a class="btn chico" href="%s">%s</a>'%(e(p['url']),e(f)) for f in p.get('formatos',[])) + '</div>') if p.get('url') else ('<p class="nota mt2">%s</p>'%" · ".join(e(f) for f in p.get('formatos',[])) if p.get('formatos') else '')}
        </div>''' for p in b['piezas'])
        c += f'''<section class="zona"><div class="wrap">
  <h2 class="seccion">{e(b['nombre'])}</h2>
  <p class="bajada mt3">{e(b['texto'])}</p>
  <div class="mt4">{piezas}</div>
</div></section>'''

    mods=""
    for m in d['modulos']:
        items="".join(f'''<div class="dato">
          <div style="display:flex;justify-content:space-between;gap:12px;align-items:baseline">
            <b style="font-size:var(--t-small);font-weight:700">{e(i['titulo'])}</b>
            <span class="chip {EST.get(i.get('estado'),'')}">{e(i.get('estado',''))}</span></div>
          <p class="small mt2">{e(i['texto'])}</p></div>''' for i in m['items'])
        mods += f'''<div class="mt5"><h3 class="label" style="color:var(--ink)">{e(m['categoria'])}</h3>
          <div class="cols cols-3 mt3">{items}</div></div>'''
    c += f'''<section class="zona tinta"><div class="wrap">
  <h2 class="seccion">Los módulos</h2>
  <p class="bajada mt3">Se asignan y se desbloquean según la orientación de cada cliente. De ahí sale el estado sin tener que preguntarlo.</p>
  {mods}
</div></section>'''

    dec="".join(f'<li class="texto" style="margin-bottom:16px"><b>{e(x["titulo"])}.</b> {e(x["texto"])}</li>' for x in d['decisiones'])
    falta="".join(f'<li class="texto small" style="margin-bottom:10px">{e(x)}</li>' for x in d['falta'])
    c += f'''<section class="zona"><div class="wrap">
  <div class="cols cols-2" style="gap:var(--s6)">
    <div><h2 class="seccion">Decisiones ya tomadas</h2><ol class="mt4" style="padding-left:20px;margin:0">{dec}</ol></div>
    <div><h2 class="seccion">Lo que falta escribir</h2><ul class="mt4" style="padding-left:20px;margin:0">{falta}</ul></div>
  </div>
</div></section>'''
    return pagina("materiales.html","Los materiales",c)

# ---------------------------------------------------------------- CLIENTES
def build_clientes(panel):
    con=[r for r in panel if r['handicap']]
    prom=sum(r['handicap']['total'] for r in con)/len(con)
    cierre=[r for r in panel if r['modo']=='cierre']
    rojo=[r for r in con if r['handicap']['ritmo']=='rojo']
    EJES=[("oferta","Oferta"),("contenido","Contenido"),("demanda","Demanda"),("venta","Venta"),("entrega","Entrega")]
    RC={"verde":"ok","amarillo":"warn","rojo":"bad"}

    def fila(r,i):
        h=r['handicap']
        if h:
            barras="".join('<span class="eje %s" title="%s: %d de 4"><span class="nombre">%s</span><span class="barras">%s</span></span>'%(
                "flojo" if k in h['eje_flojo'] else "", e(n), h['ejes'][k], e(n[:3]),
                "".join('<i%s></i>'%("" if j<h['ejes'][k] else ' class="vacia"') for j in range(4))) for k,n in EJES)
            meta=f'''<span class="num" style="font-size:24px">{h['total']}</span>
              <span class="small" style="min-width:11ch">{e(h['tramo'])}</span>
              <span class="chip {RC[h['ritmo']]}">{e(h['ritmo'])}</span>'''
            nota=e(h['nota'])
            disc = ('<p class="texto mt3" style="color:var(--warn);border-left:2px solid var(--warn);padding-left:12px;font-size:var(--t-small)">El eje más flojo apunta a <b>%s</b> y la orientación asignada es <b>%s</b>. Vale revisarlo.</p>'
                    % (e("/".join(h['sugiere'])), e(r['orientacion']))) if r['orientacion'] not in h['sugiere'] else ''
        else:
            barras='<span class="nota">Sin handicap</span>'; meta=''; nota=e(r['cuello']); disc=''
        det=[]
        if r['metrica']: det.append('<div class="dato"><span class="label">La métrica</span><p class="texto mt2">%s</p></div>'%e(r['metrica']))
        if r['cliente_tareas']: det.append('<div class="dato"><span class="label">Septiembre · lo que hace él o ella</span><ul class="mt2" style="padding-left:18px;margin:0">%s</ul></div>'%"".join('<li class="small" style="margin-bottom:6px">%s</li>'%e(x) for x in r['cliente_tareas']))
        if r['cascara']: det.append('<div class="dato"><span class="label">Septiembre · lo que hace Cáscara</span><ul class="mt2" style="padding-left:18px;margin:0">%s</ul></div>'%"".join('<li class="small" style="margin-bottom:6px">%s</li>'%e(x) for x in r['cascara']))
        if r['abierto']: det.append('<div class="dato"><span class="label">Sin definir</span><p class="texto mt2">%s</p></div>'%e(r['abierto']))
        link=('<a class="btn chico" href="clientes/%s">Abrir el documento</a>'%e(r['doc'])) if r['doc'] else '<span class="nota">Documento aparte</span>'
        return f'''<article class="fila" data-ori="{e(r['orientacion'])}" data-modo="{e(r['modo'])}" data-ritmo="{h['ritmo'] if h else 'na'}" data-txt="{e((r['cliente']+' '+r['proyecto']+' '+r['orientacion']).lower())}">
      <button class="head" aria-expanded="false" aria-controls="d{i}" style="display:grid;grid-template-columns:minmax(0,1fr) 350px 268px;gap:var(--s3);align-items:center;width:100%;background:none;border:0;padding:0;text-align:left;color:inherit;font:inherit;cursor:pointer">
        <span><b style="display:block;font-size:var(--t-h3);font-weight:700;letter-spacing:-.02em">{e(r['cliente'])}</b>
          <span class="small" style="display:block">{e(r['proyecto'])}</span></span>
        <span class="ejes">{barras}</span>
        <span style="display:flex;align-items:center;gap:14px;justify-content:flex-end">{meta}<span class="chip">{e(r['orientacion'])}</span></span>
      </button>
      <p class="texto mt2" style="color:var(--grey)">{nota}</p>
      <div class="card mt3" id="d{i}" hidden>
        {disc}{link}
        <p class="texto mt3">{e(r['titular'])}</p>
        <div class="cols cols-2 mt4">{"".join(det)}</div>
        <p class="nota mt4">Última llamada tomada: {e(r['ultima'])}</p>
      </div>
    </article>'''

    filas="\n".join(fila(r,i) for i,r in enumerate(panel))
    c = masthead("Los clientes","La camada, de menor a mayor handicap",
      "Arriba está quien más atención necesita. El eje en negrita es el más flojo y es por donde se trabaja. Tocá cualquier fila para ver la métrica, los accionables de septiembre y lo que queda sin definir.",
      [(str(len(panel)),"Clientes"),("%.1f"%prom,"Handicap promedio"),
       (str(len(cierre)),"En cierre"),(str(len(rojo)),"Ritmo en rojo")])
    c += f'''<div class="wrap">
  <div class="mt5" style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;position:sticky;top:56px;z-index:10;background:var(--paper);padding-block:14px;border-bottom:1px solid var(--line)">
    <input id="q" type="search" placeholder="Buscar cliente o proyecto" aria-label="Buscar cliente o proyecto" style="flex:1;min-width:190px">
    <button class="chip" data-f="todos" aria-pressed="true" style="cursor:pointer">Todos</button>
    <button class="chip" data-f="ori:Conseguir" aria-pressed="false" style="cursor:pointer">Conseguir</button>
    <button class="chip" data-f="ori:Sostener" aria-pressed="false" style="cursor:pointer">Sostener</button>
    <button class="chip" data-f="ori:Entregar" aria-pressed="false" style="cursor:pointer">Entregar</button>
    <button class="chip" data-f="modo:cierre" aria-pressed="false" style="cursor:pointer">En cierre</button>
    <button class="chip" data-f="ritmo:rojo" aria-pressed="false" style="cursor:pointer">Ritmo rojo</button>
  </div>
  <div id="lista" class="mt4">{filas}</div>
  <p class="small mt4" id="vacio" hidden>No hay ningún cliente con ese filtro.</p>
</div>
<style>
  #lista .head[aria-pressed]{{}}
  .fila.oculta{{display:none}}
  .chip[aria-pressed="true"]{{background:var(--ink);color:var(--paper);border-color:var(--ink)}}
  @media (max-width:940px){{
    #lista .head{{grid-template-columns:1fr!important;gap:12px!important}}
    #lista .head > span:last-child{{justify-content:flex-start!important;flex-wrap:wrap}}
  }}
</style>
<script>
(function(){{
  var lista=document.getElementById('lista'),q=document.getElementById('q'),vacio=document.getElementById('vacio'),
      chips=[].slice.call(document.querySelectorAll('.chip[data-f]')),filtro='todos';
  function aplica(){{
    var t=(q.value||'').trim().toLowerCase(),n=0;
    [].forEach.call(lista.children,function(r){{
      var ok=true;
      if(filtro!=='todos'){{var p=filtro.split(':');ok=r.getAttribute('data-'+p[0])===p[1];}}
      if(ok&&t) ok=r.getAttribute('data-txt').indexOf(t)>-1;
      r.classList.toggle('oculta',!ok); if(ok)n++;
    }});
    vacio.hidden=n>0;
  }}
  chips.forEach(function(c){{c.addEventListener('click',function(){{
    filtro=c.getAttribute('data-f');
    chips.forEach(function(o){{o.setAttribute('aria-pressed',String(o===c));}});
    aplica();
  }});}});
  q.addEventListener('input',aplica);
  lista.addEventListener('click',function(ev){{
    var b=ev.target.closest('.head'); if(!b)return;
    var d=document.getElementById(b.getAttribute('aria-controls'));
    var ab=b.getAttribute('aria-expanded')==='true';
    b.setAttribute('aria-expanded',String(!ab)); d.hidden=ab;
  }});
}})();
</script>'''
    return pagina("clientes.html","Los clientes",c)

# ---------------------------------------------------------------- MAIN
if __name__=="__main__":
    panel=json.load(open(os.path.join(BASE,'contenido','panel-data.json'),encoding='utf-8'))
    prog=json.load(open(os.path.join(BASE,'contenido','programa.json'),encoding='utf-8'))
    mat=json.load(open(os.path.join(BASE,'contenido','materiales.json'),encoding='utf-8'))
    os.makedirs(os.path.join(OUT,'clientes'),exist_ok=True)
    os.makedirs(os.path.join(OUT,'assets'),exist_ok=True)
    shutil.copy(os.path.join(BASE,'assets','founders.css'), os.path.join(OUT,'assets','founders.css'))
    open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(build_index(panel))
    open(os.path.join(OUT,'programa.html'),'w',encoding='utf-8').write(build_programa(prog))
    open(os.path.join(OUT,'materiales.html'),'w',encoding='utf-8').write(build_materiales(mat))
    open(os.path.join(OUT,'clientes.html'),'w',encoding='utf-8').write(build_clientes(panel))
    docs=os.path.join(BASE,'contenido','docs')
    n=0
    for f in glob.glob(os.path.join(docs,'*.html')):
        shutil.copy(f, os.path.join(OUT,'clientes',os.path.basename(f))); n+=1
    print("páginas: 4 · documentos de cliente:", n)
