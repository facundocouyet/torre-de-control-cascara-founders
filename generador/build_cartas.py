# -*- coding: utf-8 -*-
"""La carta de módulo: un solo documento vertical.

Decisión de Facu del 21/9: la carta y la plantilla eran dos archivos para lo
mismo. Ahora es uno. El founder recibe una sola cosa, la lee de arriba abajo y
la completa en el mismo lugar donde dice qué hacer.

El orden del documento es el orden en que se trabaja:

  encabezado          qué resuelve, cuándo se asigna, cuándo está lista
  bajada              por qué te toca ahora (la escribe el mentor al mandarla)
  01 qué hacer        los pasos numerados del módulo
  02..N el trabajo    las secciones de la plantilla, con su consigna, su
                      ejemplo de la camada y el campo donde se escribe
  cierre              los entregables tachables

Los módulos sin plantilla salen igual, con el encabezado, los pasos y los
entregables. El campo `evidencia` del inventario queda afuera: nombra a otros
clientes de la cartera y este documento lo lee el founder.

La bajada personalizada la inserta la app: busca #deck y el primer .slot, que
es el encabezado.

Se regenera con:  python3 build_cartas.py
Fuentes: fichas/inventario.json y fichas/plantillas/<id>.json
"""
import json, os, glob, html as _h

INK="#171717"; DEEP="#0A0A0C"; PAPER="#ECEAE4"; PAPER2="#FBFAF8"
GREY="#6A6A66"; GREY2="#8E8B85"; LINE="#DBD7D2"
DISP='"Helvetica Now Display","Helvetica Neue",Helvetica,Arial,sans-serif'
SERIF='"Redaction 10","Redaction","Exposure","Times New Roman",Times,serif'

def esc(s): return _h.escape(str(s or ""))

CSS = """
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#ECEAE4;color:#171717;
  font-family:"Helvetica Now Display","Helvetica Neue",Helvetica,Arial,sans-serif;
  font-size:18px;line-height:1.55;-webkit-font-smoothing:antialiased}
.hoja{max-width:880px;margin:0 auto;padding:64px 32px 120px}
.caja{display:inline-block;border:1px solid #8E8B85;padding:6px 13px;font-size:10.5px;
  letter-spacing:.24em;text-transform:uppercase;color:#6A6A66}
h1{font-size:clamp(38px,6vw,58px);font-weight:800;letter-spacing:-.038em;line-height:1.02;
  margin:28px 0 0;text-wrap:balance}
.bajada{font-size:21px;line-height:1.5;color:#6A6A66;margin:18px 0 0;max-width:60ch}
.lista{margin-top:38px;border-top:1px solid #171717;padding-top:20px;display:grid;
  gap:22px 34px;grid-template-columns:1fr}
.lista .et{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85}
.lista .tx{font-size:17px;line-height:1.5;color:#6A6A66;max-width:58ch;margin-top:7px}
.avance{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#6A6A66;
  white-space:nowrap;margin-top:22px}

section{margin-top:62px}
section .n{font-size:11px;letter-spacing:.2em;color:#8E8B85;font-variant-numeric:tabular-nums}
section h2{font-size:29px;font-weight:800;letter-spacing:-.028em;line-height:1.18;
  margin:10px 0 0;max-width:26ch}
section .consigna{font-size:18.5px;line-height:1.55;color:#6A6A66;margin:14px 0 0;max-width:62ch}

.pasos{margin-top:26px}
.paso{display:grid;grid-template-columns:52px minmax(0,1fr);gap:22px;align-items:baseline;
  border-top:1px solid #DBD7D2;padding:20px 0}
.paso .p{font-size:20px;font-weight:800;letter-spacing:-.04em;color:#8E8B85;
  font-variant-numeric:tabular-nums;line-height:1.3}
.paso .t{font-size:19px;line-height:1.55;max-width:58ch}

.ejemplo{margin-top:22px;border-left:2px solid #DBD7D2;padding:4px 0 4px 20px}
.ejemplo .et{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85}
.ejemplo .tx{font-family:"Redaction 10","Redaction","Exposure","Times New Roman",Times,serif;
  font-style:italic;font-size:18px;line-height:1.5;color:#6A6A66;margin-top:8px;max-width:62ch}

.campo{margin-top:24px}
textarea,input[type=text]{width:100%;font:inherit;font-size:18px;line-height:1.55;color:#171717;
  background:#FBFAF8;border:1px solid #DBD7D2;padding:14px 16px;border-radius:0;
  transition:border-color .15s}
textarea{resize:vertical}
textarea:focus,input[type=text]:focus{outline:none;border-color:#171717}
.lin{display:grid;grid-template-columns:210px minmax(0,1fr);gap:14px 18px;align-items:center;
  border-top:1px solid #DBD7D2;padding:14px 0}
.lin .rot{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#6A6A66}
.tabla{width:100%;border-collapse:collapse;margin-top:6px}
.tabla th{text-align:left;font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:#6A6A66;font-weight:400;padding:0 10px 10px 0;border-bottom:2px solid #171717}
.tabla td{padding:0;border-bottom:1px solid #DBD7D2}
.tabla input{border:0;background:transparent;padding:12px 10px 12px 0}
.tabla input:focus{background:#FBFAF8}
.tabla td.rotfila{font-size:17px;font-weight:700;letter-spacing:-.01em;padding:12px 18px 12px 0;white-space:nowrap}
.envoltorio{overflow-x:auto}

/* lo que ponemos nosotros: texto escrito, no campo para completar */
.nuestro{margin-top:62px;border-left:3px solid #171717;padding:2px 0 2px 26px}
.nuestro .et{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85}
.nuestro h2{font-size:29px;font-weight:800;letter-spacing:-.028em;line-height:1.18;
  margin:10px 0 0;max-width:26ch}
.nuestro p{font-size:18.5px;line-height:1.55;margin:16px 0 0;max-width:62ch}
.nuestro .devuelta{margin-top:26px;border-top:1px solid #DBD7D2;padding-top:18px}
.nuestro .devuelta .k{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#6A6A66}

.entregables{margin-top:26px}
.cab{border-bottom:2px solid #171717;padding-bottom:12px}
.cab .et{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85}
.chk{display:grid;grid-template-columns:26px minmax(0,1fr);gap:18px;align-items:start;
  border-bottom:1px solid #DBD7D2;padding:18px 0;cursor:pointer}
.chk .box{position:relative;flex:0 0 auto;width:20px;height:20px;border:2px solid #6A6A66;margin-top:3px}
.chk .box i{position:absolute;left:4px;top:1px;width:8px;height:14px;
  border-right:3px solid #171717;border-bottom:3px solid #171717;
  transform:rotate(45deg) scale(0);transform-origin:center;
  transition:transform .16s cubic-bezier(.2,1.4,.4,1)}
.chk.done .box i{transform:rotate(45deg) scale(1)}
.chk .t{font-size:19px;line-height:1.55;max-width:58ch}
/* el fibrón pasa por el medio de la letra, y en cada línea del renglón */
.chk .txt{display:inline;background-repeat:no-repeat;background-position:0 center;background-size:0% 8px;
  background-image:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 10' preserveAspectRatio='none'%3E%3Cpath d='M0 4.2L6 .8L24 6L44 1.2L68 6.6L94 1.4L120 6.2L144 1L170 6.4L192 1.6L200 5L200 9.2L0 8.8Z' fill='%23171717'/%3E%3C/svg%3E");
  -webkit-box-decoration-break:clone;box-decoration-break:clone;
  transition:background-size .28s cubic-bezier(.3,.9,.3,1),color .2s}
.chk.done .txt{background-size:100% 8px;color:#8E8B85}
.chk:focus-visible{outline:1px solid #171717;outline-offset:4px}

/* la bajada personalizada, cuando se prepara el envío desde la torre */
.bajada-bloque{margin-top:56px;border:1px solid #171717;padding:30px 28px;background:#FBFAF8}
.bajada-bloque .tt{font-size:26px;font-weight:800;letter-spacing:-.028em;line-height:1.2}
.bajada-bloque .sub{font-size:17px;line-height:1.5;color:#6A6A66;margin-top:10px;max-width:58ch}
.bajada-grilla{display:grid;gap:24px;margin-top:26px;grid-template-columns:1fr!important}
.bajada-grilla .k{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85;
  border-top:2px solid #171717;padding-top:14px}
.bajada-grilla .v{font-size:18.5px;line-height:1.55;margin-top:9px;max-width:58ch}

.acc{position:sticky;bottom:0;background:#ECEAE4;border-top:1px solid #DBD7D2;
  padding:14px 0;margin-top:62px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.acc button{font:inherit;font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;
  border:1px solid #171717;background:transparent;color:#171717;padding:13px 18px;cursor:pointer}
.acc button.tinta{background:#171717;color:#ECEAE4}
.acc button:hover{background:#171717;color:#ECEAE4}
.acc button.tinta:hover{background:transparent;color:#171717}
.acc .dicho{font-family:"Redaction 10","Redaction","Exposure","Times New Roman",Times,serif;
  font-style:italic;font-size:15px;color:#6A6A66}

.pie{margin-top:48px;border-top:1px solid #171717;padding-top:22px;display:flex;
  justify-content:space-between;align-items:baseline;gap:20px;flex-wrap:wrap;
  font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6A6A66}
.sello{width:28px;height:28px;border:1.5px solid #171717;display:inline-flex;
  align-items:center;justify-content:center;font-size:13px;font-weight:800}

@media (max-width:640px){
  .hoja{padding:40px 20px 90px}
  .paso{grid-template-columns:38px minmax(0,1fr);gap:14px}
  .lin{grid-template-columns:1fr;gap:8px}
  .tabla{min-width:560px}
  .bajada-bloque{padding:22px 18px}
}
@media print{
  body{background:#fff}
  .acc{display:none}
  textarea,input{border-color:#bbb;background:#fff}
  section{break-inside:avoid;margin-top:40px}
  .chk{cursor:default}
}
"""

JS = """
(function(){
  var MOD=document.body.dataset.mod||'x';
  var KC='cf-carta-'+MOD, KP='cf-pl-'+MOD;

  /* ---- los entregables tachables ---- */
  var st={}; try{ st=JSON.parse(localStorage.getItem(KC)||'{}'); }catch(e){}
  function pintar(){
    document.querySelectorAll('.chk').forEach(function(el){
      el.classList.toggle('done', !!st[el.dataset.k]);
      el.setAttribute('aria-checked', st[el.dataset.k]?'true':'false');});
  }
  document.addEventListener('click',function(e){
    var el=e.target.closest && e.target.closest('.chk'); if(!el)return;
    st[el.dataset.k]=!st[el.dataset.k];
    try{ localStorage.setItem(KC,JSON.stringify(st)); }catch(err){}
    pintar();});
  document.addEventListener('keydown',function(e){
    if(e.key!==' '&&e.key!=='Enter')return;
    var el=document.activeElement && document.activeElement.closest && document.activeElement.closest('.chk');
    if(!el)return; e.preventDefault(); el.click();});
  pintar();

  /* ---- lo que se escribe en la hoja ---- */
  function todos(){return Array.prototype.slice.call(document.querySelectorAll('[data-c]'))}
  function auto(el){ if(el.tagName==='TEXTAREA'){ el.style.height='auto'; el.style.height=(el.scrollHeight+2)+'px'; } }
  function contar(){
    var s=document.querySelectorAll('section.trabajo'), n=0;
    s.forEach(function(sec){
      var lleno=false;
      sec.querySelectorAll('[data-c]').forEach(function(el){ if(el.value && el.value.trim()) lleno=true; });
      if(lleno) n++;
    });
    var a=document.querySelector('.avance');
    if(a) a.textContent = s.length ? (n+' de '+s.length+' empezadas') : '';
  }
  function guardar(){
    var v={}; todos().forEach(function(el){ if(el.value) v[el.dataset.c]=el.value; });
    try{localStorage.setItem(KP,JSON.stringify(v))}catch(e){}
    contar();
  }
  function cargar(){
    var v={}; try{v=JSON.parse(localStorage.getItem(KP)||'{}')}catch(e){}
    todos().forEach(function(el){ if(v[el.dataset.c]!=null) el.value=v[el.dataset.c]; auto(el); });
    contar();
  }
  document.addEventListener('input',function(e){
    if(!e.target.dataset || !e.target.dataset.c) return; auto(e.target); guardar();
  });
  var bl=document.querySelector('[data-a="limpiar"]');
  if(bl) bl.addEventListener('click',function(){
    if(!confirm('Esto borra todo lo que escribiste en esta carta. \\u00bfSeguimos?')) return;
    todos().forEach(function(el){el.value='';auto(el)}); guardar();
  });
  var bi=document.querySelector('[data-a="imprimir"]');
  if(bi) bi.addEventListener('click',function(){window.print()});
  var bd=document.querySelector('[data-a="bajar"]');
  if(bd) bd.addEventListener('click',async function(){
    todos().forEach(function(el){
      if(el.tagName==='TEXTAREA') el.textContent=el.value; else el.setAttribute('value',el.value||'');
    });
    var html='<!doctype html>\\n'+document.documentElement.outerHTML;
    var nom='carta-'+MOD+'.html';
    var dl=null; try{ dl=await claude.use('downloads'); }catch(e){}
    if(dl){ try{ await dl.save({filename:nom,data:html}); return; }catch(e){ if(e&&e.code==='declined')return; } }
    var a=document.createElement('a');
    a.href=URL.createObjectURL(new Blob([html],{type:'text/html'})); a.download=nom;
    document.body.appendChild(a); a.click(); a.remove();
  });
  cargar();
  window.addEventListener('resize',function(){todos().forEach(auto)});
})();
"""

TPL = '''<template id="tpl-bajada">
<div class="bajada-bloque">
  <div data-b="titulo" class="tt"></div>
  <div class="sub">Esto lo escribimos para vos, sobre lo que venimos viendo en tu caso.</div>
  <div data-b="grilla" class="bajada-grilla">
    <div data-b="fila-porque"><div class="k">Por qué te toca ahora</div><div data-b="porque" class="v"></div></div>
    <div data-b="fila-objetivo"><div class="k">El objetivo concreto</div><div data-b="objetivo" class="v"></div></div>
    <div data-b="fila-mindset"><div class="k">Con qué cabeza encararla</div><div data-b="mindset" class="v"></div></div>
  </div>
</div>
</template>'''


def _plural(n):
    if n == 1: return "La carta está hecha cuando esto existe."
    if n == 2: return "La carta está hecha cuando estas dos cosas existen."
    return "La carta está hecha cuando estas %d cosas existen." % n


def campo(sec, i):
    """El lugar donde se escribe: texto largo, líneas cortas o tabla."""
    tipo = sec.get("campo", "texto")
    if tipo == "lineas":
        filas = "".join(
            '      <div class="lin"><span class="rot">%s</span>'
            '<input type="text" data-c="s%dl%d" placeholder=""></div>\n' % (esc(r), i, j)
            for j, r in enumerate(sec.get("lineas", [])))
        return '    <div class="campo">\n%s    </div>\n' % filas
    if tipo == "tabla":
        cols = sec.get("columnas", [])
        rot  = sec.get("filas_rotulo") or []          # primera celda fija, cuando la fila ya tiene nombre
        th = "".join('<th>%s</th>' % esc(c) for c in cols)
        cuerpo = ""
        for f in range(max(sec.get("filas", 6), len(rot))):
            celdas = []
            for c in range(len(cols)):
                if c == 0 and f < len(rot) and rot[f]:
                    celdas.append('<td class="rotfila">%s</td>' % esc(rot[f]))
                else:
                    celdas.append('<td><input type="text" data-c="s%df%dc%d"></td>' % (i, f, c))
            cuerpo += '        <tr>%s</tr>\n' % "".join(celdas)
        return ('    <div class="campo envoltorio"><table class="tabla">\n'
                '      <thead><tr>%s</tr></thead>\n      <tbody>\n%s      </tbody>\n'
                '    </table></div>\n' % (th, cuerpo))
    alto = sec.get("alto", 4)
    ph = esc(sec.get("placeholder", ""))
    return ('    <div class="campo"><textarea data-c="s%d" rows="%d" '
            'placeholder="%s"></textarea></div>\n' % (i, alto, ph))


def construir(m, categoria, pl=None, bajada=None):
    # la variante de un founder puede pisar los pasos y los entregables del módulo
    pasos = (pl or {}).get("pasos") or m.get("pasos", []) or []
    comp  = (pl or {}).get("completar") or m.get("completar", []) or []
    secciones = (pl or {}).get("secciones", []) or []
    out = []

    # ---- encabezado. Es el primer .slot: la bajada personalizada entra justo abajo.
    out.append('<header class="slot">')
    out.append('  <div class="caja">Carta de módulo · %s</div>' % esc(categoria))
    out.append('  <h1>%s</h1>' % esc(m["nombre"]))
    out.append('  <p class="bajada">%s</p>' % esc((pl or {}).get("bajada") or m.get("resultado", "")))
    out.append('  <div class="lista">')
    out.append('    <div><div class="et">Cuándo se asigna</div><div class="tx">%s</div></div>'
               % esc(m.get("para_quien", "")))
    if (pl or {}).get("lista_cuando"):
        out.append('    <div><div class="et">Está lista cuando</div><div class="tx">%s</div></div>'
                   % esc(pl["lista_cuando"]))
    out.append('  </div>')
    trabajo = [x for x in secciones if not x.get("nuestro")]
    if trabajo:
        out.append('  <div class="avance">0 de %d empezadas</div>' % len(trabajo))
    out.append('</header>')

    # ---- la bajada, cuando viene escrita desde el generador
    if bajada and (bajada.get("porque") or bajada.get("objetivo") or bajada.get("mindset")):
        quien = (bajada.get("founder") or "").split(" ")[0]
        out.append('<div class="bajada-bloque">')
        out.append('  <div class="tt">%s</div>'
                   % esc("Por qué esta carta, " + quien if quien else "Por qué esta carta"))
        out.append('  <div class="sub">Esto lo escribimos para vos, sobre lo que venimos viendo en tu caso.</div>')
        out.append('  <div class="bajada-grilla">')
        for k, tx in (("Por qué te toca ahora", bajada.get("porque")),
                      ("El objetivo concreto", bajada.get("objetivo")),
                      ("Con qué cabeza encararla", bajada.get("mindset"))):
            if not tx: continue
            out.append('    <div><div class="k">%s</div><div class="v">%s</div></div>' % (esc(k), esc(tx)))
        out.append('  </div>')
        out.append('</div>')

    n = 0
    # ---- qué hacer
    if pasos:
        n += 1
        out.append('<section>')
        out.append('  <div class="n">%02d</div>' % n)
        out.append('  <h2>Qué tenés que hacer</h2>')
        out.append('  <p class="consigna">En este orden. Cada paso se apoya en el anterior, '
                   'así que no conviene saltear ninguno aunque parezca obvio. Abajo está la hoja '
                   'para resolverlos, uno por uno.</p>' if secciones else
                   '  <p class="consigna">En este orden. Cada paso se apoya en el anterior, '
                   'así que no conviene saltear ninguno aunque parezca obvio.</p>')
        out.append('  <div class="pasos">')
        for i, x in enumerate(pasos):
            out.append('    <div class="paso"><span class="p">%02d</span><span class="t">%s</span></div>'
                       % (i + 1, esc(x)))
        out.append('  </div>')
        out.append('</section>')

    # ---- la hoja: una sección por cosa que hay que resolver
    for i, s in enumerate(secciones):
        # los bloques que escribimos nosotros: no llevan número ni cuentan como trabajo
        if s.get("nuestro"):
            out.append('<div class="nuestro">')
            out.append('  <div class="et">Esto lo ponemos nosotros</div>')
            out.append('  <h2>%s</h2>' % esc(s["titulo"]))
            for par in (s.get("texto") or []):
                out.append('  <p>%s</p>' % esc(par))
            if s.get("pregunta"):
                out.append('  <div class="devuelta"><div class="k">%s</div>' % esc(s["pregunta"]))
                out.append('    <div class="campo"><textarea data-c="s%d" rows="3"></textarea></div>' % i)
                out.append('  </div>')
            out.append('</div>')
            continue
        n += 1
        out.append('<section class="trabajo">')
        out.append('  <div class="n">%02d</div>' % n)
        out.append('  <h2>%s</h2>' % esc(s["titulo"]))
        out.append('  <p class="consigna">%s</p>' % esc(s["consigna"]))
        ej = s.get("ejemplo") or {}
        if ej.get("texto"):
            quien = ('Cómo lo resolvió %s' % esc(ej["quien"])) if ej.get("quien") else 'Un ejemplo'
            out.append('  <div class="ejemplo"><div class="et">%s</div><div class="tx">%s</div></div>'
                       % (quien, esc(ej["texto"])))
        out.append(campo(s, i).rstrip('\n'))
        out.append('</section>')

    # ---- los entregables, tachables
    if comp:
        n += 1
        out.append('<section>')
        out.append('  <div class="n">%02d</div>' % n)
        out.append('  <h2>Los entregables</h2>')
        out.append('  <p class="consigna">%s Tocá cada uno cuando lo termines: queda tachado y se guarda '
                   'en este navegador.</p>' % _plural(len(comp)))
        out.append('  <div class="entregables">')
        out.append('    <div class="cab"><span class="et">Lo que tiene que existir</span></div>')
        for i, x in enumerate(comp):
            out.append('    <div class="chk" role="checkbox" tabindex="0" aria-checked="false" '
                       'data-k="c%d" data-g="entregables">'
                       '<span class="box"><i></i></span>'
                       '<span class="t"><span class="txt">%s</span></span></div>' % (i, esc(x)))
        out.append('  </div>')
        out.append('</section>')

    return "\n".join(out)


def render(m, categoria, pl=None, bajada=None):
    quien = (bajada or {}).get("founder")
    tit = '%s · carta de módulo' % m["nombre"] + (' · %s' % quien if quien else '')
    cuerpo = construir(m, categoria, pl, bajada)
    hay_campos = bool((pl or {}).get("secciones"))
    acciones = ''
    if hay_campos:
        acciones = ('<div class="acc">\n'
                    '  <button class="tinta" data-a="bajar">Descargar completada</button>\n'
                    '  <button data-a="imprimir">Imprimir</button>\n'
                    '  <button data-a="limpiar">Vaciar la hoja</button>\n'
                    '  <span class="dicho">Lo que escribís se guarda solo en este navegador.</span>\n'
                    '</div>\n')
    return ('<!doctype html>\n<html lang="es"><head>\n'
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '<title>%s</title>\n<style>%s</style>\n</head>\n'
            '<body data-mod="%s">\n<div class="hoja">\n<main id="deck">\n%s\n</main>\n%s'
            '<div class="pie"><div><span class="sello">C</span></div>'
            '<div>Cáscara Founders · %s</div></div>\n</div>\n%s\n<script>%s</script>\n'
            '</body></html>\n') % (esc(tit), CSS, esc(m["id"]), cuerpo, acciones,
                                   esc(categoria), TPL, JS)


def cargar_plantilla(raiz, mid):
    p = os.path.join(raiz, 'fichas', 'plantillas', mid + '.json')
    if not os.path.exists(p): return None
    return json.load(open(p, encoding='utf-8'))


def variantes(raiz):
    """Las cartas escritas para un founder en particular.

    Viven en fichas/plantillas/<modulo>--<slug>.json, con el mismo esquema que
    la plantilla del módulo y dos claves más: `slug` y `bajada_envio` (founder,
    porque, objetivo, mindset). Reemplazan a la plantilla genérica sólo en la
    copia de ese founder; el módulo queda igual para todos los demás.

    Salen a cartas/para/<slug>-<modulo>.html.
    """
    return sorted(glob.glob(os.path.join(raiz, 'fichas', 'plantillas', '*--*.json')))


if __name__ == "__main__":
    RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    inv = json.load(open(os.path.join(RAIZ, 'fichas', 'inventario.json'), encoding='utf-8'))
    os.makedirs(os.path.join(RAIZ, 'cartas'), exist_ok=True)
    n, con_hoja, indice = 0, 0, []
    for c in inv["categorias"]:
        for m in c["modulos"]:
            pl = cargar_plantilla(RAIZ, m["id"])
            if pl: con_hoja += 1
            open(os.path.join(RAIZ, 'cartas', '%s.html' % m["id"]), 'w', encoding='utf-8').write(
                render(m, c["nombre"], pl, None))
            indice.append({"id": m["id"], "categoria": c["nombre"], "nombre": m["nombre"],
                           "hoja": bool(pl)})
            n += 1
    json.dump(indice, open(os.path.join(RAIZ, 'cartas', 'indice.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    # las cartas escritas para un founder
    meta = {m["id"]: (m, c["nombre"]) for c in inv["categorias"] for m in c["modulos"]}
    v = 0
    if variantes(RAIZ):
        os.makedirs(os.path.join(RAIZ, 'cartas', 'para'), exist_ok=True)
    for f in variantes(RAIZ):
        pl = json.load(open(f, encoding='utf-8'))
        mid = pl["modulo"]
        if mid not in meta:
            print("m\u00f3dulo desconocido:", mid, "en", os.path.basename(f)); continue
        m, cat = meta[mid]
        slug = pl.get("slug") or os.path.basename(f).split('--')[1][:-5]
        open(os.path.join(RAIZ, 'cartas', 'para', '%s-%s.html' % (slug, mid)),
             'w', encoding='utf-8').write(render(m, cat, pl, pl.get("bajada_envio")))
        v += 1
    print("cartas:", n, "\u00b7 con hoja para completar:", con_hoja, "\u00b7 escritas para un founder:", v)
