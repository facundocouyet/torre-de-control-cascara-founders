# -*- coding: utf-8 -*-
"""Las cartas de módulo, como documento de scroll.

La carta es lo que el founder lee para accionar. Por eso tiene tres cosas y
nada más: el contexto de por qué le estamos dando esta carta, la explicación
de lo que tiene que hacer, y el checklist de entregables que se tacha.

Fuera quedaron, por decisión de Facu del 18/9: las herramientas, el estado
interno de la carta y el panel de "cómo trabajamos". El campo `evidencia` del
inventario tampoco entra: nombra a otros clientes de la cartera y este
documento lo lee el founder.

Si se le pasa una bajada personalizada (para quién va, por qué esa carta,
cuál es el objetivo y con qué cabeza encararla), entra debajo del encabezado.
La app la inserta sola: busca #deck y el primer .slot, que es el encabezado.
"""
import json, os, html as _h

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
.lista{margin-top:38px;border-top:1px solid #171717;padding-top:20px;display:flex;
  justify-content:space-between;gap:20px 30px;align-items:baseline;flex-wrap:wrap}
.lista .et{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85}
.lista .tx{font-size:17px;line-height:1.5;color:#6A6A66;max-width:58ch;margin-top:7px}
.avance{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#6A6A66;white-space:nowrap}

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

.entregables{margin-top:26px}
.cab{display:flex;justify-content:space-between;align-items:baseline;gap:20px;
  border-bottom:2px solid #171717;padding-bottom:12px}
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

.hoja-link{margin-top:22px;font-size:18px;line-height:1.55;color:#6A6A66;max-width:60ch}
.hoja-link a{color:#171717;text-decoration:underline;text-underline-offset:3px}

/* la bajada personalizada, cuando se prepara el envío desde la torre */
.bajada-bloque{margin-top:56px;border:1px solid #171717;padding:30px 28px;background:#FBFAF8}
.bajada-bloque .tt{font-size:26px;font-weight:800;letter-spacing:-.028em;line-height:1.2}
.bajada-bloque .sub{font-size:17px;line-height:1.5;color:#6A6A66;margin-top:10px;max-width:58ch}
.bajada-grilla{display:grid;gap:24px;margin-top:26px;grid-template-columns:1fr!important}
.bajada-grilla .k{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85;
  border-top:2px solid #171717;padding-top:14px}
.bajada-grilla .v{font-size:18.5px;line-height:1.55;margin-top:9px;max-width:58ch}

.pie{margin-top:86px;border-top:1px solid #171717;padding-top:22px;display:flex;
  justify-content:space-between;align-items:baseline;gap:20px;flex-wrap:wrap;
  font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6A6A66}
.sello{width:28px;height:28px;border:1.5px solid #171717;display:inline-flex;
  align-items:center;justify-content:center;font-size:13px;font-weight:800}

@media (max-width:640px){
  .hoja{padding:40px 20px 90px}
  .paso{grid-template-columns:38px minmax(0,1fr);gap:14px}
  .bajada-bloque{padding:22px 18px}
}
@media print{
  body{background:#fff}
  section{break-inside:avoid;margin-top:40px}
  .chk{cursor:default}
}
"""

JS = """
(function(){
  var K='cf-carta-'+(document.body.dataset.mod||'x');
  var st={}; try{ st=JSON.parse(localStorage.getItem(K)||'{}'); }catch(e){}
  function contar(){
    document.querySelectorAll('[data-cuenta]').forEach(function(c){
      var g=c.dataset.cuenta,t=0,h=0;
      document.querySelectorAll('.chk[data-g="'+g+'"]').forEach(function(el){t++; if(st[el.dataset.k])h++;});
      c.textContent=h+' de '+t;});
  }
  function pintar(){
    document.querySelectorAll('.chk').forEach(function(el){
      el.classList.toggle('done', !!st[el.dataset.k]);
      el.setAttribute('aria-checked', st[el.dataset.k]?'true':'false');});
    contar();
  }
  document.addEventListener('click',function(e){
    var el=e.target.closest && e.target.closest('.chk'); if(!el)return;
    st[el.dataset.k]=!st[el.dataset.k];
    try{ localStorage.setItem(K,JSON.stringify(st)); }catch(err){}
    pintar();});
  document.addEventListener('keydown',function(e){
    if(e.key!==' '&&e.key!=='Enter')return;
    var el=document.activeElement && document.activeElement.closest && document.activeElement.closest('.chk');
    if(!el)return; e.preventDefault(); el.click();});
  pintar();
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


def construir(m, categoria, bajada=None, hay_plantilla=False):
    pasos = m.get("pasos", []) or []
    comp  = m.get("completar", []) or []
    out = []

    # ---- encabezado. Es el primer .slot: la bajada personalizada entra justo abajo.
    out.append('<header class="slot">')
    out.append('  <div class="caja">Carta de módulo · %s</div>' % esc(categoria))
    out.append('  <h1>%s</h1>' % esc(m["nombre"]))
    out.append('  <p class="bajada">%s</p>' % esc(m.get("resultado", "")))
    out.append('  <div class="lista">')
    out.append('    <div><div class="et">Cuándo se asigna</div><div class="tx">%s</div></div>'
               % esc(m.get("para_quien", "")))
    if comp:
        out.append('    <span class="avance" data-cuenta="entregables">0 de %d</span>' % len(comp))
    out.append('  </div>')
    out.append('</header>')

    # ---- la bajada, cuando viene escrita desde el generador
    if bajada and (bajada.get("porque") or bajada.get("objetivo") or bajada.get("mindset")):
        quien = (bajada.get("founder") or "").split(" ")[0]
        out.append('<div class="bajada-bloque">')
        out.append('  <div class="tt">%s</div>' % esc("Por qué esta carta, " + quien if quien else "Por qué esta carta"))
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
                   'así que no conviene saltear ninguno aunque parezca obvio.</p>')
        out.append('  <div class="pasos">')
        for i, x in enumerate(pasos):
            out.append('    <div class="paso"><span class="p">%02d</span><span class="t">%s</span></div>'
                       % (i + 1, esc(x)))
        out.append('  </div>')
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
        out.append('    <div class="cab"><span class="et">Lo que tiene que existir</span>'
                   '<span class="avance" data-cuenta="entregables">0 de %d</span></div>' % len(comp))
        for i, x in enumerate(comp):
            out.append('    <div class="chk" role="checkbox" tabindex="0" aria-checked="false" '
                       'data-k="c%d" data-g="entregables">'
                       '<span class="box"><i></i></span>'
                       '<span class="t"><span class="txt">%s</span></span></div>' % (i, esc(x)))
        out.append('  </div>')
        if hay_plantilla:
            out.append('  <p class="hoja-link">La hoja donde se completa es la plantilla de este módulo: '
                       '<a href="../plantillas/%s.html">abrirla acá</a>.</p>' % esc(m["id"]))
        out.append('</section>')

    return "\n".join(out)


def render(m, categoria, bajada=None, hay_plantilla=False):
    quien = (bajada or {}).get("founder")
    tit = '%s · carta de módulo' % m["nombre"] + (' · %s' % quien if quien else '')
    cuerpo = construir(m, categoria, bajada, hay_plantilla)
    return ('<!doctype html>\n<html lang="es"><head>\n'
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '<title>%s</title>\n<style>%s</style>\n</head>\n'
            '<body data-mod="%s">\n<div class="hoja">\n<main id="deck">\n%s\n</main>\n'
            '<div class="pie"><div><span class="sello">C</span></div>'
            '<div>Cáscara Founders · %s</div></div>\n</div>\n%s\n<script>%s</script>\n'
            '</body></html>\n') % (esc(tit), CSS, esc(m["id"]), cuerpo, esc(categoria), TPL, JS)


if __name__ == "__main__":
    RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    inv = json.load(open(os.path.join(RAIZ, 'fichas', 'inventario.json'), encoding='utf-8'))
    os.makedirs(os.path.join(RAIZ, 'cartas'), exist_ok=True)
    n, indice = 0, []
    for c in inv["categorias"]:
        for m in c["modulos"]:
            hp = os.path.exists(os.path.join(RAIZ, 'fichas', 'plantillas', m["id"] + '.json'))
            open(os.path.join(RAIZ, 'cartas', '%s.html' % m["id"]), 'w', encoding='utf-8').write(
                render(m, c["nombre"], None, hp))
            indice.append({"id": m["id"], "categoria": c["nombre"], "nombre": m["nombre"]})
            n += 1
    json.dump(indice, open(os.path.join(RAIZ, 'cartas', 'indice.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print("cartas:", n)
