# -*- coding: utf-8 -*-
import json, os

INK="#171717"; DEEP="#0A0A0C"; PAPER="#ECEAE4"; PAPER2="#FBFAF8"
GREY="#6A6A66"; LINE="#DBD7D2"; LINEINK="#3A3A40"; SOFT="#C9C7C3"
DISP='"Helvetica Neue", Helvetica, Arial, sans-serif'
SERIF='"Times New Roman", Georgia, serif'

def panel(num, total, sec, kicker, body, dark=False, foot="Qualita Studio · Cáscara Founders"):
    bg = INK if dark else PAPER
    fg = PAPER2 if dark else INK
    gr = "#8C8C90" if dark else GREY
    ln = LINEINK if dark else LINE
    boxb = "#8C8C90" if dark else "#9A968E"
    return f'''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <style>
    body {{ margin: 0; background: {bg}; color: {fg};
           font-family: {DISP}; -webkit-font-smoothing: antialiased; }}
    a {{ color: {fg}; }} a:hover {{ color: {gr}; }}
    .it {{ font-family: {SERIF}; font-style: italic; }}
    .num {{ font-weight: 800; letter-spacing: -0.045em; font-variant-numeric: tabular-nums; }}
  </style>
</helmet>
<div style="width: 1920px; height: 1080px; box-sizing: border-box; background: {bg}; display: flex; padding: 34px;">
  <div style="flex-grow: 1; display: flex; flex-direction: column; box-sizing: border-box; padding: 62px 88px 62px 88px; border: 1px solid {ln};">

    <div style="display: inline-flex; align-self: flex-start; border: 1px solid {boxb}; padding: 7px 14px; margin-bottom: 56px;">
      <span style="font-size: 17px; letter-spacing: 0.22em; text-transform: uppercase; color: {gr};">{kicker}</span>
    </div>

{body}

    <div style="margin-top: auto; padding-top: 48px; display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid {ln};">
      <span style="font-size: 19px; letter-spacing: 0.06em; color: {gr};">{foot}</span>
      <span style="font-size: 19px; letter-spacing: 0.06em; color: {gr};" class="num">{num} / {total}</span>
    </div>

  </div>
</div>
</x-dc>
</body>
</html>
'''

def H(txt, size=70, color=None, mb=0, lh=1.06):
    c = f"color: {color};" if color else ""
    return f'    <div style="font-size: {size}px; font-weight: 700; letter-spacing: -0.03em; line-height: {lh}; {c} margin-bottom: {mb}px; max-width: 1480px;">{txt}</div>\n'

def P(txt, size=25, color=None, mb=0, mw=1180, lh=1.5):
    c = f"color: {color};" if color else ""
    return f'    <div style="font-size: {size}px; line-height: {lh}; {c} margin-bottom: {mb}px; max-width: {mw}px;">{txt}</div>\n'

def COLS(items, gap=64, top=56, dark=False):
    gr = "#8C8C90" if dark else GREY
    ln = "#3A3A40" if dark else LINE
    cells=[]
    for label, head, txt in items:
        cells.append(f'''      <div style="display: flex; flex-direction: column; gap: 18px; border-top: 1px solid {ln}; padding-top: 22px;">
        <div style="font-size: 17px; letter-spacing: 0.2em; text-transform: uppercase; color: {gr};">{label}</div>
        <div style="font-size: 34px; font-weight: 700; letter-spacing: -0.02em; line-height: 1.16;">{head}</div>
        <div style="font-size: 23px; line-height: 1.5; color: {gr};">{txt}</div>
      </div>''')
    n=len(items)
    return f'''    <div style="display: grid; grid-template-columns: repeat({n}, minmax(0, 1fr)); gap: {gap}px; margin-top: {top}px;">
{chr(10).join(cells)}
    </div>
'''

def SPACER(h): return f'    <div style="height: {h}px;"></div>\n'

import glob, html as _h, re

SHELL_HEAD = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  html,body{margin:0;padding:0;background:#0A0A0C;height:100%;overflow:hidden;
            font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
  .it{font-family:"Times New Roman",Georgia,serif;font-style:italic}
  .num{font-weight:800;letter-spacing:-.045em;font-variant-numeric:tabular-nums}
  #deck{display:flex;height:100%;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;
        scroll-behavior:smooth;scrollbar-width:none;-ms-overflow-style:none}
  #deck::-webkit-scrollbar{display:none}
  .slot{flex:0 0 auto;scroll-snap-align:center;display:flex;align-items:center;
        justify-content:center;height:100%;overflow:hidden}
  .pnl{width:1920px;height:1080px;transform-origin:center center;flex:0 0 auto}
  #hint{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);font-size:12px;
        letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.45);
        background:rgba(0,0,0,.35);padding:7px 14px;pointer-events:none;transition:opacity .6s;z-index:9}
  #bar{position:fixed;left:0;bottom:0;height:2px;background:rgba(255,255,255,.55);width:0;
       transition:width .15s linear;z-index:10}
  @media print{
    html,body{overflow:visible;height:auto;background:#fff}
    #deck{display:block;overflow:visible;height:auto}
    .slot{display:block;height:auto;page-break-after:always;break-after:page}
    .pnl{transform:none!important;zoom:.52}
    #hint,#bar{display:none}
    @page{size:landscape;margin:0}
  }
</style>
</head>
<body>
<div id="deck">
'''

SHELL_TAIL = '''</div>
<div id="hint">Scrolleá hacia la derecha · o usá las flechas</div>
<div id="bar"></div>
<script>
(function(){
  var deck=document.getElementById('deck'),hint=document.getElementById('hint'),bar=document.getElementById('bar');
  var slots=[].slice.call(deck.querySelectorAll('.slot'));
  function shrink(){
    slots.forEach(function(sl){
      var f=sl.querySelector('.fitme'); if(!f||f.dataset.done) return;
      f.style.zoom=1;
      var over=f.scrollHeight/f.clientHeight;
      if(over>1.005){ f.style.zoom=Math.max(0.62,(1/over)*0.985); }
      f.dataset.done='1';
    });
  }
  function fit(){var vw=innerWidth,vh=innerHeight,s=Math.min(vw/1920,vh/1080);
    slots.forEach(function(sl){sl.querySelector('.pnl').style.transform='scale('+s+')';sl.style.width=(1920*s)+'px';});
    shrink();prog();}
  function prog(){var m=deck.scrollWidth-deck.clientWidth;bar.style.width=(m>0?(deck.scrollLeft/m*100):100)+'%';}
  var cur=0,busy=0;
  function go(d){busy=1;clearTimeout(go._t);go._t=setTimeout(function(){busy=0;},520);
    cur=Math.max(0,Math.min(slots.length-1,cur+d));
    deck.scrollTo({left:slots[cur].offsetLeft-(deck.clientWidth-slots[cur].offsetWidth)/2,behavior:'smooth'});}
  function sync(){if(busy)return;var w=slots[0]?slots[0].offsetWidth:1;
    cur=Math.max(0,Math.min(slots.length-1,Math.round(deck.scrollLeft/w)));}
  addEventListener('resize',fit);
  deck.addEventListener('scroll',function(){prog();sync();hint.style.opacity=0;});
  deck.addEventListener('wheel',function(e){if(Math.abs(e.deltaY)>Math.abs(e.deltaX)){deck.scrollLeft+=e.deltaY;e.preventDefault();}},{passive:false});
  document.addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){go(1);e.preventDefault();}
    if(e.key==='ArrowLeft'||e.key==='PageUp'){go(-1);e.preventDefault();}
    if(e.key==='Home'){cur=0;go(0);} if(e.key==='End'){cur=slots.length-1;go(0);}});
  setTimeout(function(){hint.style.opacity=0;},5000); fit();
})();
</script>
</body></html>
'''


FRAME_MARK = 'padding: 62px 88px 62px 88px; border: 1px solid'
def wrap_fit(p):
    if FRAME_MARK not in p: return p   # hojas sin marco, como la carta
    i = p.index(FRAME_MARK)
    j = p.index('">', i) + 2
    k = p.rindex('\n  </div>\n</div>\n</x-dc>')
    return (p[:j]
            + '\n<div class="fitme" style="display:flex;flex-direction:column;flex-grow:1;min-height:0;">'
            + p[j:k] + '</div>\n' + p[k:])

def compose(panels, title):
    out=[SHELL_HEAD.replace("__TITLE__", _h.escape(title))]
    for p in panels:
        p=wrap_fit(p)
        m=re.search(r'body \{[^}]*background:\s*([#\w]+);\s*color:\s*([#\w]+)', p)
        bg,fg=m.group(1),m.group(2)
        body=re.search(r'(<div style="width: 1920px;[\s\S]*?)\n</x-dc>', p).group(1)
        body=body.replace('<div style="width: 1920px;','<div class="pnl" style="width: 1920px;',1)
        out.append(f'<div class="slot" style="background:{bg};color:{fg};">\n{body}\n</div>\n')
    out.append(SHELL_TAIL)
    return "".join(out)

def esc(s): return _h.escape(str(s or ""))

def build(d):
    PN=[]
    modo = d["modo"]
    es_cierre = modo == "cierre"
    foot = f'{esc(d["proyecto"])} · Cáscara Founders'

    # 01 PORTADA
    b  = SPACER(110)
    b += f'    <div style="font-size: 26px; letter-spacing: 0.24em; text-transform: uppercase; color: #8C8C90; margin-bottom: 32px;">{"Informe de cierre" if es_cierre else "Radiografía y roadmap"}</div>\n'
    b += H(esc(d["cliente"]), 132, mb=22, lh=0.99)
    b += f'    <div style="font-size: 40px; line-height: 1.24; color: #C9C7C3; max-width: 1300px;">{esc(d["bajada"])}</div>\n'
    b += f'''    <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 60px; margin-top: 56px; max-width: 1560px;">
      <div style="border-top: 1px solid {LINEINK}; padding-top: 18px;"><div style="font-size: 16px; letter-spacing: 0.2em; text-transform: uppercase; color: #8C8C90; margin-bottom: 10px;">Proyecto</div><div style="font-size: 26px; color: {PAPER2};">{esc(d["proyecto"])}</div></div>
      <div style="border-top: 1px solid {LINEINK}; padding-top: 18px;"><div style="font-size: 16px; letter-spacing: 0.2em; text-transform: uppercase; color: #8C8C90; margin-bottom: 10px;">Arranque</div><div style="font-size: 26px; color: {PAPER2};">{esc(d["arranque"])}</div></div>
      <div style="border-top: 1px solid {LINEINK}; padding-top: 18px;"><div style="font-size: 16px; letter-spacing: 0.2em; text-transform: uppercase; color: #8C8C90; margin-bottom: 10px;">Orientación</div><div style="font-size: 26px; color: {PAPER2};">{esc(d["orientacion"])}</div></div>
    </div>
'''
    PN.append(("Cáscara Founders", b, True, "12 de septiembre de 2026 · borrador para revisar"))

    # 02 PUNTO A
    b  = H(esc(d["titular"]), 74, mb=34)
    b += P(f'La métrica que importa: {esc(d["metrica"])}', 26, GREY, mw=1420)
    b += COLS([(esc(x["label"]), esc(x["titulo"]), esc(x["texto"])) for x in d["punto_a"]])
    PN.append(("01 · Punto A", b, False, foot))

    # 03 QUE PASO
    rows=[]
    for x in d["que_paso"]:
        rows.append(f'''      <div style="display: grid; grid-template-columns: 250px minmax(0, 1fr); gap: 34px; padding: 20px 0; border-bottom: 1px solid {LINE}; align-items: start;">
        <div style="font-size: 19px; letter-spacing: 0.12em; text-transform: uppercase; color: {GREY}; padding-top: 5px;">{esc(x["cuando"])}</div>
        <div><div style="font-size: 28px; font-weight: 700; letter-spacing: -0.02em; line-height: 1.2; margin-bottom: 8px;">{esc(x["titulo"])}</div>
        <div style="font-size: 22px; line-height: 1.45; color: {GREY}; max-width: 1380px;">{esc(x["texto"])}</div></div>
      </div>''')
    # peso aproximado por entrada, para paginar
    W = [len(x["texto"]) + 3*len(x["titulo"]) + 260 for x in d["que_paso"]]
    LIM = 2700
    import math
    tot = sum(W)
    ng = max(1, math.ceil(tot / LIM))
    obj = tot / ng
    grupos=[]; cur=[]; acc=0
    for k,(r,w) in enumerate(zip(rows, W)):
        rest = len(rows) - k
        if cur and (acc + w/2 > obj) and rest >= (ng - len(grupos) - 1) + 1 and len(grupos) < ng-1:
            grupos.append(cur); cur=[]; acc=0
        cur.append(r); acc += w
    if cur: grupos.append(cur)
    for gi, g in enumerate(grupos):
        suf = "" if len(grupos) == 1 else f" ({gi+1} de {len(grupos)})"
        b  = H("Qué pasó hasta hoy" + suf, 66, mb=26)
        b += "    <div style=\"display: flex; flex-direction: column;\">\n" + "\n".join(g) + "\n    </div>\n"
        PN.append(("02 · El recorrido", b, False, foot))

    # 04 LECTURA
    L=d["lectura"]
    b  = SPACER(40)
    b += H(esc(L["titular"]), 96, mb=44, lh=1.04)
    cita = ""
    if L.get("cita"):
        cita = f'''      <div style="display: flex; flex-direction: column; gap: 14px;">
        <div class="it" style="font-size: 30px; line-height: 1.4; color: {PAPER2};">“{esc(L["cita"])}”</div>
        <div style="font-size: 20px; color: #8C8C90;">{esc(L.get("cita_autor",""))}</div>
      </div>'''
    else:
        cita = '<div></div>'
    b += f'''    <div style="display: grid; grid-template-columns: 1.15fr 1fr; gap: 76px; max-width: 1640px;">
      <div style="font-size: 27px; line-height: 1.5; color: #C9C7C3;">{esc(L["texto"])}</div>
{cita}
    </div>
'''
    b += f'''    <div style="display: inline-flex; align-self: flex-start; margin-top: 52px; border: 1px solid {PAPER2}; padding: 14px 26px; gap: 18px; align-items: baseline;">
      <span style="font-size: 17px; letter-spacing: 0.2em; text-transform: uppercase; color: #8C8C90;">Orientación</span>
      <span style="font-size: 30px; font-weight: 700; letter-spacing: -0.02em; color: {PAPER2};">{esc(d["orientacion"])}</span>
    </div>
'''
    PN.append(("03 · La lectura del caso", b, True, foot))

    # HANDICAP
    H_ = d.get("handicap")
    if H_:
        import handicap as _hk
        RC = {"verde":"#3F6B45","amarillo":"#8A6A2F","rojo":"#8C3A32"}
        cols=[]
        for _k, _nom, _desc in _hk.EJES:
            v = H_["ejes"][_k]
            flojo = _k in H_["eje_flojo"]
            barras = "".join('<div style="flex:1;height:10px;background:%s;"></div>' % (INK if i < v else "#D7D3CE") for i in range(4))
            cols.append('      <div style="border-top: 2px solid %s; padding-top: 18px;">\n'
              '        <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:14px;">\n'
              '          <div style="font-size: 17px; letter-spacing: 0.18em; text-transform: uppercase; color: %s;">%s</div>\n'
              '          <div class="num" style="font-size: 30px; color: %s;">%d</div>\n'
              '        </div>\n'
              '        <div style="display:flex;gap:4px;margin-bottom:14px;">%s</div>\n'
              '        <div style="font-size: 19px; line-height: 1.38; color: %s;">%s</div>\n'
              '      </div>' % (INK if flojo else LINE, INK if flojo else GREY, esc(_nom),
                                INK if flojo else GREY, v, barras, GREY, esc(_desc)))
        b  = H("Handicap", 66, mb=8)
        b += P("Cinco ejes de cero a cuatro sobre el estado del negocio. El eje más bajo es por donde se trabaja, y es el que marca la orientación.", 25, GREY, mb=40, mw=1500)
        b += '    <div style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 40px;">\n' + "\n".join(cols) + '\n    </div>\n'
        b += ('    <div style="display:flex;gap:56px;align-items:flex-start;margin-top:52px;border-top:1px solid %s;padding-top:30px;flex-wrap:wrap;">\n'
              '      <div><div style="font-size: 16px; letter-spacing: 0.2em; text-transform: uppercase; color: %s; margin-bottom: 8px;">Total</div>\n'
              '        <div class="num" style="font-size: 56px; line-height:1;">%d<span style="font-size:26px;color:%s;font-weight:400;letter-spacing:0;"> / 20</span></div></div>\n'
              '      <div><div style="font-size: 16px; letter-spacing: 0.2em; text-transform: uppercase; color: %s; margin-bottom: 8px;">Tramo</div>\n'
              '        <div style="font-size: 30px; font-weight: 700; letter-spacing: -0.02em;">%s</div></div>\n'
              '      <div><div style="font-size: 16px; letter-spacing: 0.2em; text-transform: uppercase; color: %s; margin-bottom: 8px;">Ritmo</div>\n'
              '        <div style="font-size: 30px; font-weight: 700; letter-spacing: -0.02em; color:%s;">%s</div>\n'
              '        <div style="font-size: 19px; color: %s; margin-top:4px;">%s</div></div>\n'
              '      <div style="flex:1;min-width:380px;"><div style="font-size: 16px; letter-spacing: 0.2em; text-transform: uppercase; color: %s; margin-bottom: 8px;">Por dónde se trabaja</div>\n'
              '        <div style="font-size: 23px; line-height:1.4;">%s</div></div>\n'
              '    </div>\n' % (LINE, GREY, H_["total"], GREY, GREY, esc(H_["tramo"]), GREY,
                                RC[H_["ritmo"]], esc(H_["ritmo"].capitalize()), GREY, esc(H_["ritmo_texto"]),
                                GREY, esc(H_["nota"])))
        PN.append(("04 · El handicap", b, False, foot))

    # 05 PUNTO B
    cells=[]
    for x in d["punto_b"]:
        cells.append(f'''      <div style="display: flex; flex-direction: column; gap: 18px; border-top: 2px solid {INK}; padding-top: 26px;">
        <div style="font-size: 19px; letter-spacing: 0.2em; text-transform: uppercase; color: {GREY};">{esc(x["fecha"])}</div>
        <div style="font-size: 50px; font-weight: 700; letter-spacing: -0.03em; line-height: 1.09;">{esc(x["titulo"])}</div>
        <div style="font-size: 23px; line-height: 1.5; color: {GREY};">{esc(x["texto"])}</div>
      </div>''')
    b  = H("Punto B", 70, mb=14)
    b += P("Dos hitos con fecha. Lo demás cuelga de estos dos." if not es_cierre else "Los dos hitos que quedan por delante, ya sin acompañamiento.", 26, GREY, mb=48)
    b += f'    <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 72px;">\n' + "\n".join(cells) + "\n    </div>\n"
    PN.append(("05 · Punto B", b, False, foot))

    # 06 ROADMAP
    hdr=f'''      <div style="font-size: 17px; letter-spacing: 0.2em; text-transform: uppercase; color: {GREY}; padding-bottom: 14px; border-bottom: 1px solid {INK};">Cuándo</div>
      <div style="font-size: 17px; letter-spacing: 0.2em; text-transform: uppercase; color: {GREY}; padding-bottom: 14px; border-bottom: 1px solid {INK};">Objetivo</div>
      <div style="font-size: 17px; letter-spacing: 0.2em; text-transform: uppercase; color: {GREY}; padding-bottom: 14px; border-bottom: 1px solid {INK};">Entregable</div>
      <div style="font-size: 17px; letter-spacing: 0.2em; text-transform: uppercase; color: {GREY}; padding-bottom: 14px; border-bottom: 1px solid {INK};">Quién</div>'''
    cells=[hdr]
    n=len(d["roadmap"]); fs = 22 if n<=6 else 20; pad = 16 if n<=6 else 13
    for x in d["roadmap"]:
        cells.append(f'''      <div style="font-size: {fs}px; font-weight: 700; padding: {pad}px 0; border-bottom: 1px solid {LINE};">{esc(x["cuando"])}</div>
      <div style="font-size: {fs}px; font-weight: 700; padding: {pad}px 22px {pad}px 0; border-bottom: 1px solid {LINE};">{esc(x["objetivo"])}</div>
      <div style="font-size: {fs-1}px; line-height: 1.42; color: {GREY}; padding: {pad}px 22px {pad}px 0; border-bottom: 1px solid {LINE};">{esc(x["entregable"])}</div>
      <div style="font-size: {fs-1}px; color: {GREY}; padding: {pad}px 0; border-bottom: 1px solid {LINE};">{esc(x["quien"])}</div>''')
    b  = H("El roadmap" if not es_cierre else "Los próximos 60 días", 66, mb=18)
    b += P("Hasta el 31 de octubre." if not es_cierre else "Lo que sigue, para ejecutar solo.", 25, GREY, mb=30)
    b += f'    <div style="display: grid; grid-template-columns: 240px 320px minmax(0, 1fr) 280px; gap: 0;">\n' + "\n".join(cells) + "\n    </div>\n"
    PN.append(("06 · El roadmap", b, False, foot))

    # 07 ACCIONABLES
    def ul(items):
        return ('<ul style="margin: 0; padding-left: 20px; font-size: 20px; line-height: 1.38; color: '
                + GREY + ';">' + "".join(f'<li style="margin-bottom: 6px;">{esc(x)}</li>' for x in items) + '</ul>')
    hdr=f'''      <div style="font-size: 17px; letter-spacing: 0.2em; text-transform: uppercase; color: {GREY}; padding-bottom: 14px; border-bottom: 1px solid {INK};">Cuándo</div>
      <div style="font-size: 17px; letter-spacing: 0.2em; text-transform: uppercase; color: {GREY}; padding-bottom: 14px; border-bottom: 1px solid {INK};">{esc(d["cliente"].split()[0])}</div>
      <div style="font-size: 17px; letter-spacing: 0.2em; text-transform: uppercase; color: {GREY}; padding-bottom: 14px; border-bottom: 1px solid {INK};">Cáscara</div>'''
    cells=[hdr]
    for x in d["accionables"]:
        cells.append(f'''      <div style="font-size: 22px; font-weight: 700; line-height: 1.2; padding: 16px 20px 16px 0; border-bottom: 1px solid {LINE};">{esc(x["cuando"])}</div>
      <div style="padding: 16px 28px 16px 0; border-bottom: 1px solid {LINE};">{ul(x["cliente"])}</div>
      <div style="padding: 16px 0; border-bottom: 1px solid {LINE};">{ul(x["cascara"])}</div>''')
    b  = H("Los accionables", 60, mb=14)
    b += P("Quién hace qué y cuándo.", 24, GREY, mb=26)
    b += f'    <div style="display: grid; grid-template-columns: 250px minmax(0, 1fr) minmax(0, 1fr); gap: 0;">\n' + "\n".join(cells) + "\n    </div>\n"
    if d.get("abierto"):
        b += f'    <div style="margin-top: 26px; border-left: 3px solid {INK}; padding-left: 22px; font-size: 22px; line-height: 1.4; max-width: 1560px;">{esc(d["abierto"])}</div>\n'
    PN.append(("07 · Los accionables", b, False, foot))

    # 08 PAQUETE
    items=d["paquete"]
    cols = 2 if len(items) <= 4 else 3
    cells="".join(f'''      <div style="border-top: 1px solid {LINE}; padding-top: 22px;">
        <div class="num" style="font-size: 34px; color: {GREY}; line-height: 1; margin-bottom: 14px;">{i+1:02d}</div>
        <div style="font-size: 24px; line-height: 1.42;">{esc(x)}</div>
      </div>''' for i,x in enumerate(items))
    b  = H("Qué se lleva" if es_cierre else "Qué entregamos", 70, mb=18)
    b += P("Todo esto queda hecho y aplicado a su caso, con sus palabras y sus decisiones adentro.", 26, GREY, mb=44, mw=1400)
    b += f'    <div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 52px;">\n{cells}\n    </div>\n'
    PN.append(("08 · El paquete", b, False, foot))

    # 09 CIERRE
    b  = SPACER(80)
    b += H(("Hasta acá llega el acompañamiento." if es_cierre else "Lo que viene."), 80, mb=44, lh=1.06)
    b += f'    <div style="font-size: 27px; line-height: 1.52; color: #C9C7C3; max-width: 1500px;">{esc(d["cierre"])}</div>\n'
    PN.append(("Cáscara Founders", b, True, "Borrador · revisar con Facu antes de enviar"))

    T = len(PN)
    return [panel(f"{i+1:02d}", f"{T:02d}", "", k, bb, dark=dk, foot=ft)
            for i,(k,bb,dk,ft) in enumerate(PN)]

os.makedirs("out", exist_ok=True)
fichas=sorted(glob.glob("fichas/*.json"))
idx=[]
for f in fichas:
    d=json.load(open(f,encoding="utf-8"))
    tit=f'{d["cliente"]} · {"Informe de cierre" if d["modo"]=="cierre" else "Radiografía y roadmap"}'
    open(f'out/{d["slug"]}.html',"w",encoding="utf-8").write(compose(build(d), tit))
    idx.append((d["slug"], d["cliente"], d["proyecto"], d["modo"], d["orientacion"], d["titular"], d.get("abierto","")))
print("documentos:", len(idx))
json.dump(idx, open("index.json","w"), ensure_ascii=False, indent=1)
