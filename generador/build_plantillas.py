# -*- coding: utf-8 -*-
"""Las plantillas: la hoja donde el founder completa lo que la carta le pide.

La carta dice qué hacer. La plantilla es donde se hace. Por eso va como
documento de scroll y no como paneles: se escribe adentro, se guarda solo
en el navegador y se puede descargar terminada o imprimir.

Cada plantilla sale de un JSON en fichas/plantillas/<id>.json con este esquema:

{
 "modulo": "one-sheeter-oferta",
 "titulo": "La hoja de tu oferta",
 "bajada": "Una frase sobre qué se resuelve completando esto.",
 "lista_cuando": "Qué tiene que ser cierto para darla por terminada.",
 "secciones": [
   {"titulo": "...", "consigna": "...",
    "ejemplo": {"quien": "Matías Morales", "texto": "..."},
    "campo": "texto" | "lineas" | "tabla",
    "alto": 5,                                  # solo texto: renglones
    "lineas": ["Rótulo de cada línea", ...],    # solo lineas
    "columnas": ["Cliente", "Qué compró", ...], # solo tabla
    "filas": 6}                                 # solo tabla
 ]
}
"""
import json, os, glob, html as _h

INK="#171717"; DEEP="#0A0A0C"; PAPER="#ECEAE4"; PAPER2="#FBFAF8"
GREY="#6A6A66"; GREY2="#8E8B85"; LINE="#DBD7D2"; ROJO="#FE1414"
DISP='"Helvetica Now Display","Helvetica Neue",Helvetica,Arial,sans-serif'
SERIF='"Redaction 10","Redaction","Exposure","Times New Roman",Times,serif'

def esc(s): return _h.escape(str(s or ""))

CSS = f"""
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:{PAPER};color:{INK};font-family:{DISP};
  font-size:18px;line-height:1.55;-webkit-font-smoothing:antialiased}}
.hoja{{max-width:880px;margin:0 auto;padding:64px 32px 120px}}
.caja{{display:inline-block;border:1px solid {GREY2};padding:6px 13px;font-size:10.5px;
  letter-spacing:.24em;text-transform:uppercase;color:{GREY}}}
h1{{font-size:clamp(38px,6vw,58px);font-weight:800;letter-spacing:-.038em;line-height:1.02;
  margin:28px 0 0;text-wrap:balance}}
.bajada{{font-size:21px;line-height:1.5;color:{GREY};margin:18px 0 0;max-width:60ch}}
.lista{{margin-top:38px;border-top:1px solid {INK};padding-top:20px;display:flex;
  justify-content:space-between;gap:20px;align-items:baseline;flex-wrap:wrap}}
.lista .et{{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:{GREY2}}}
.lista .tx{{font-size:17px;color:{GREY};max-width:60ch}}
.avance{{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:{GREY};white-space:nowrap}}

section{{margin-top:62px}}
section .n{{font-size:11px;letter-spacing:.2em;color:{GREY2};font-variant-numeric:tabular-nums}}
section h2{{font-size:29px;font-weight:800;letter-spacing:-.028em;line-height:1.18;
  margin:10px 0 0;max-width:26ch}}
section .consigna{{font-size:18.5px;line-height:1.55;color:{GREY};margin:14px 0 0;max-width:62ch}}
.ejemplo{{margin-top:22px;border-left:2px solid {LINE};padding:4px 0 4px 20px}}
.ejemplo .et{{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:{GREY2}}}
.ejemplo .tx{{font-family:{SERIF};font-style:italic;font-size:18px;line-height:1.5;
  color:{GREY};margin-top:8px;max-width:62ch}}

.campo{{margin-top:24px}}
textarea,input[type=text]{{width:100%;font:inherit;font-size:18px;line-height:1.55;color:{INK};
  background:{PAPER2};border:1px solid {LINE};padding:14px 16px;border-radius:0;
  transition:border-color .15s}}
textarea{{resize:vertical}}
textarea:focus,input[type=text]:focus{{outline:none;border-color:{INK}}}
.lin{{display:grid;grid-template-columns:210px minmax(0,1fr);gap:14px 18px;align-items:center;
  border-top:1px solid {LINE};padding:14px 0}}
.lin .rot{{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:{GREY}}}
.tabla{{width:100%;border-collapse:collapse;margin-top:6px}}
.tabla th{{text-align:left;font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:{GREY};font-weight:400;padding:0 10px 10px 0;border-bottom:2px solid {INK}}}
.tabla td{{padding:0;border-bottom:1px solid {LINE}}}
.tabla input{{border:0;background:transparent;padding:12px 10px 12px 0}}
.tabla input:focus{{background:{PAPER2}}}
.envoltorio{{overflow-x:auto}}

.pie{{margin-top:86px;border-top:1px solid {INK};padding-top:22px;display:flex;
  justify-content:space-between;align-items:baseline;gap:20px;flex-wrap:wrap;
  font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:{GREY}}}
.acc{{position:sticky;bottom:0;background:{PAPER};border-top:1px solid {LINE};
  padding:14px 0;margin-top:48px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}}
.acc button{{font:inherit;font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;
  border:1px solid {INK};background:transparent;color:{INK};padding:13px 18px;cursor:pointer}}
.acc button.tinta{{background:{INK};color:{PAPER}}}
.acc button:hover{{background:{INK};color:{PAPER}}}
.acc button.tinta:hover{{background:transparent;color:{INK}}}
.acc .dicho{{font-family:{SERIF};font-style:italic;font-size:15px;color:{GREY}}}

@media (max-width:640px){{
  .hoja{{padding:40px 20px 90px}} .lin{{grid-template-columns:1fr;gap:8px}}
  .tabla{{min-width:560px}}
}}
@media print{{
  .acc{{display:none}} body{{background:#fff}}
  textarea,input{{border-color:#bbb;background:#fff}}
  section{{break-inside:avoid;margin-top:40px}}
}}
"""

JS = """
(function(){
  var K='cf-pl-'+document.body.dataset.mod;
  function todos(){return Array.prototype.slice.call(document.querySelectorAll('[data-c]'))}
  function cargar(){
    var v={}; try{v=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
    todos().forEach(function(el){ if(v[el.dataset.c]!=null) el.value=v[el.dataset.c]; auto(el); });
    contar();
  }
  function guardar(){
    var v={}; todos().forEach(function(el){ if(el.value) v[el.dataset.c]=el.value; });
    try{localStorage.setItem(K,JSON.stringify(v))}catch(e){}
    contar();
  }
  function auto(el){ if(el.tagName==='TEXTAREA'){ el.style.height='auto'; el.style.height=(el.scrollHeight+2)+'px'; } }
  function contar(){
    var s=document.querySelectorAll('section'), n=0;
    s.forEach(function(sec){
      var c=sec.querySelectorAll('[data-c]'), lleno=false;
      c.forEach(function(el){ if(el.value && el.value.trim()) lleno=true; });
      if(lleno) n++;
    });
    var a=document.querySelector('.avance');
    if(a) a.textContent = n+' de '+s.length+' empezadas';
  }
  document.addEventListener('input',function(e){
    if(!e.target.dataset || !e.target.dataset.c) return; auto(e.target); guardar();
  });
  var bl=document.querySelector('[data-a="limpiar"]');
  if(bl) bl.addEventListener('click',function(){
    if(!confirm('Esto borra todo lo que escribiste en esta hoja. ¿Seguimos?')) return;
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
    var nom='plantilla-'+document.body.dataset.mod+'.html';
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

def campo(sec, i):
    tipo = sec.get("campo", "texto")
    if tipo == "lineas":
        filas = "".join(
            f'''      <div class="lin"><span class="rot">{esc(r)}</span>'''
            f'''<input type="text" data-c="s{i}l{j}" placeholder=""></div>'''
            for j, r in enumerate(sec.get("lineas", [])))
        return f'    <div class="campo">\n{filas}\n    </div>\n'
    if tipo == "tabla":
        cols = sec.get("columnas", [])
        th = "".join(f'<th>{esc(c)}</th>' for c in cols)
        cuerpo = ""
        for f in range(sec.get("filas", 6)):
            tds = "".join(f'<td><input type="text" data-c="s{i}f{f}c{c}"></td>' for c in range(len(cols)))
            cuerpo += f'        <tr>{tds}</tr>\n'
        return (f'    <div class="campo envoltorio"><table class="tabla">\n'
                f'      <thead><tr>{th}</tr></thead>\n      <tbody>\n{cuerpo}      </tbody>\n'
                f'    </table></div>\n')
    alto = sec.get("alto", 4)
    ph = esc(sec.get("placeholder", ""))
    return (f'    <div class="campo"><textarea data-c="s{i}" rows="{alto}" '
            f'placeholder="{ph}"></textarea></div>\n')


def render(pl, modulo_nombre, categoria):
    secs = ""
    for i, s in enumerate(pl["secciones"]):
        ej = s.get("ejemplo") or {}
        bloque_ej = ""
        if ej.get("texto"):
            quien = f'Cómo lo resolvió {esc(ej["quien"])}' if ej.get("quien") else "Un ejemplo"
            bloque_ej = (f'    <div class="ejemplo"><div class="et">{quien}</div>'
                         f'<div class="tx">{esc(ej["texto"])}</div></div>\n')
        secs += (f'  <section>\n    <div class="n">{i+1:02d}</div>\n'
                 f'    <h2>{esc(s["titulo"])}</h2>\n'
                 f'    <p class="consigna">{esc(s["consigna"])}</p>\n'
                 f'{bloque_ej}{campo(s, i)}  </section>\n')

    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(pl["titulo"])} · plantilla de Cáscara Founders</title>
<style>{CSS}</style>
</head>
<body data-mod="{esc(pl["modulo"])}">
<div class="hoja">
  <span class="caja">Plantilla · {esc(categoria)}</span>
  <h1>{esc(pl["titulo"])}</h1>
  <p class="bajada">{esc(pl["bajada"])}</p>
  <div class="lista">
    <div><div class="et">Está lista cuando</div><div class="tx">{esc(pl["lista_cuando"])}</div></div>
    <div class="avance">0 de {len(pl["secciones"])} empezadas</div>
  </div>

{secs}
  <div class="acc">
    <button class="tinta" data-a="bajar">Descargar completada</button>
    <button data-a="imprimir">Imprimir</button>
    <button data-a="limpiar">Vaciar la hoja</button>
    <span class="dicho">Lo que escribís se guarda solo en este navegador.</span>
  </div>

  <div class="pie">
    <span>{esc(modulo_nombre)} · Cáscara Founders</span>
    <span>Cáscara diseña, vos ejecutás</span>
  </div>
</div>
<script>{JS}</script>
</body>
</html>'''


if __name__ == "__main__":
    RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # la raíz del repo
    inv = json.load(open(os.path.join(RAIZ, 'fichas', 'inventario.json'), encoding='utf-8'))
    meta = {}
    for c in inv["categorias"]:
        for m in c["modulos"]:
            meta[m["id"]] = (m["nombre"], c["nombre"])
    os.makedirs(os.path.join(RAIZ, 'plantillas'), exist_ok=True)
    n = 0
    for f in sorted(glob.glob(os.path.join(RAIZ, 'fichas', 'plantillas', '*.json'))):
        pl = json.load(open(f, encoding='utf-8'))
        mid = pl["modulo"]
        if mid not in meta:
            print("módulo desconocido:", mid); continue
        nom, cat = meta[mid]
        open(os.path.join(RAIZ, 'plantillas', f'{mid}.html'), 'w', encoding='utf-8').write(render(pl, nom, cat))
        n += 1
    print("plantillas:", n)
