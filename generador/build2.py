# -*- coding: utf-8 -*-
"""Documentos de cliente v2: estructura nueva, tipografía más grande, checklist y línea de tiempo."""
import json, os, glob, re, html as _h
import build as B

RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # la raíz del repo

INK,DEEP,PAPER,PAPER2 = B.INK,B.DEEP,B.PAPER,B.PAPER2
GREY,LINE,LINEINK,SOFT = B.GREY,B.LINE,B.LINEINK,B.SOFT
ROJO="#FE1414"
def esc(s): return _h.escape(str(s or ""))

# --- escala 0-4 → 1-100, estilo Fórmula 1 -------------------------------
EJES=[("oferta","Oferta"),("contenido","Contenido"),("demanda","Demanda"),("venta","Venta"),("entrega","Entrega")]
COMO_SUBE={
 "oferta":"Sube cuando la oferta queda escrita con precio y avatar, y salta cuando alguien la compra a ese precio.",
 "contenido":"Sube cuando hay cadencia con ángulos definidos, y salta cuando la audiencia valida uno.",
 "demanda":"Sube cuando entran conversaciones sin empujar, y salta cuando hay un canal propio y medible.",
 "venta":"Sube cuando hay un proceso de cierre que se repite, y salta cuando el precio se sostiene sin negociar.",
 "entrega":"Sube cuando el proceso es repetible, y salta cuando además está delegado.",
}
def cien(n): return n*20+10

# el shell sale de build.py. Antes se leía de un archivo suelto en /tmp de la máquina donde
# se generó; el módulo ya lo tiene y da el mismo resultado, verificado contra clientes/.
SHELL_HEAD, SHELL_TAIL = B.SHELL_HEAD, B.SHELL_TAIL

# checklist con memoria + fibrón
EXTRA = '''
<style>
  .chk{cursor:pointer;position:relative}
  .chk .box{position:relative;flex:0 0 auto}
  .chk .box i{position:absolute;left:6px;top:2px;width:10px;height:19px;
    border-right:4px solid ''' + INK + ''';border-bottom:4px solid ''' + INK + ''';
    transform:rotate(45deg) scale(0);transform-origin:center;transition:transform .16s cubic-bezier(.2,1.4,.4,1)}
  .chk.done .box i{transform:rotate(45deg) scale(1)}
  /* el fibrón pasa por el medio de la letra, y en cada línea del renglón */
  .chk .txt{display:inline;background-image:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 10' preserveAspectRatio='none'%3E%3Cpath d='M0 4.2L6 .8L24 6L44 1.2L68 6.6L94 1.4L120 6.2L144 1L170 6.4L192 1.6L200 5L200 9.2L0 8.8Z' fill='%23171717'/%3E%3C/svg%3E");
    background-repeat:no-repeat;background-position:0 center;background-size:0% 9px;
    -webkit-box-decoration-break:clone;box-decoration-break:clone;
    transition:background-size .28s cubic-bezier(.3,.9,.3,1),opacity .2s}
  .chk.done .txt{background-size:100% 9px}
  .chk.done .txt{color:#8E8B85}
</style>
<script>
(function(){
  var K='cf-chk-'+(document.title||'doc').replace(/[^a-z0-9]/gi,'').slice(0,40);
  var st={}; try{ st=JSON.parse(localStorage.getItem(K)||'{}'); }catch(e){}
  function pintar(){ document.querySelectorAll('.chk').forEach(function(el){
    el.classList.toggle('done', !!st[el.dataset.k]);
    el.setAttribute('aria-checked', st[el.dataset.k]?'true':'false'); }); contar(); }
  function contar(){ document.querySelectorAll('[data-cuenta]').forEach(function(c){
    var g=c.dataset.cuenta, t=0,h=0;
    document.querySelectorAll('.chk[data-g="'+g+'"]').forEach(function(el){t++; if(st[el.dataset.k])h++;});
    c.textContent=h+' de '+t; }); }
  document.addEventListener('click',function(e){
    var el=e.target.closest('.chk'); if(!el)return;
    st[el.dataset.k]=!st[el.dataset.k];
    try{ localStorage.setItem(K,JSON.stringify(st)); }catch(err){}
    pintar(); });
  document.addEventListener('keydown',function(e){
    if(e.key!==' '&&e.key!=='Enter')return;
    var el=document.activeElement && document.activeElement.closest && document.activeElement.closest('.chk');
    if(!el)return; e.preventDefault(); el.click(); });
  pintar();
})();
</script>
'''
SHELL_TAIL = SHELL_TAIL.replace('</body>', EXTRA + '</body>')

def compose(panels, title):
    out=[SHELL_HEAD.replace("__TITLE__", esc(title))]
    for p in panels:
        p=B.wrap_fit(p)
        m=re.search(r'body \{[^}]*background:\s*([#\w]+);\s*color:\s*([#\w]+)', p)
        bg,fg=m.group(1),m.group(2)
        body=re.search(r'(<div style="width: 1920px;[\s\S]*?)\n</x-dc>', p).group(1)
        body=body.replace('<div style="width: 1920px;','<div class="pnl" style="width: 1920px;',1)
        out.append(f'<div class="slot" style="background:{bg};color:{fg};">\n{body}\n</div>\n')
    out.append(SHELL_TAIL)
    return "".join(out)

# --- helpers de tipografía, más grandes ---------------------------------
def H(t,s=84,c=None,mb=0,lh=1.02,mw=1560):
    cc=f"color:{c};" if c else ""
    return f'    <div style="font-size:{s}px;font-weight:800;letter-spacing:-.035em;line-height:{lh};{cc}margin-bottom:{mb}px;max-width:{mw}px;">{t}</div>\n'
def P(t,s=30,c=None,mb=0,mw=1300,lh=1.48):
    cc=f"color:{c};" if c else ""
    return f'    <div style="font-size:{s}px;line-height:{lh};{cc}margin-bottom:{mb}px;max-width:{mw}px;">{t}</div>\n'
def ET(t,c=None,mb=22):
    return f'    <div style="font-size:19px;letter-spacing:.22em;text-transform:uppercase;color:{c or GREY};margin-bottom:{mb}px;">{t}</div>\n'
def SP(h): return f'    <div style="height:{h}px;"></div>\n'

# ========================= LOS PANELES =========================

class B2:
    """La carta va en una hoja aparte: sin etiqueta, sin pie, sin número y sin marco.
    Papel, tinta y cursiva, con el párrafo solo en el centro."""
    @staticmethod
    def carta(texto):
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
    body {{ margin: 0; background: {PAPER}; color: {INK};
           font-family: {B.DISP}; -webkit-font-smoothing: antialiased; }}
    .it {{ font-family: {B.SERIF}; font-style: italic; }}
  </style>
</helmet>
<div style="width: 1920px; height: 1080px; box-sizing: border-box; background: {PAPER};
            display: flex; align-items: center; justify-content: center; padding: 120px 200px;">
  <div class="it" style="font-size: 43px; line-height: 1.5; color: {INK}; max-width: 1240px;">{texto}</div>
</div>
</x-dc>
</body>
</html>'''

def build(d):
    PN=[]
    cierre = d["modo"]=="cierre"
    foot = f'{esc(d["proyecto"])} · Cáscara Founders'
    H_=d.get("handicap")

    def add(k,b,dark=False,ft=None): PN.append((k,b,dark,ft or foot))

    # 01 · PORTADA
    b  = SP(96)
    b += f'    <div style="font-size:28px;letter-spacing:.24em;text-transform:uppercase;color:#8C8C90;margin-bottom:36px;">{"Informe de cierre" if cierre else "Radiografía y roadmap"}</div>\n'
    b += H(esc(d["cliente"]),146,mb=28,lh=.96,mw=1700)
    b += f'    <div style="font-size:44px;line-height:1.22;color:#C9C7C3;max-width:1420px;">{esc(d["bajada"])}</div>\n'
    b += f'''    <div style="margin-top:72px;border-top:1px solid {LINEINK};padding-top:26px;max-width:1500px;">
      <div style="font-size:17px;letter-spacing:.2em;text-transform:uppercase;color:#8C8C90;margin-bottom:12px;">En qué etapa estás</div>
      <div style="font-size:30px;line-height:1.4;color:{PAPER2};">{esc(d.get("etapa",""))}</div>
    </div>\n'''
    add("Cáscara Founders",b,True,"13 de septiembre de 2026")

    # 02 · DÓNDE ESTÁS HOY
    b  = ""
    b += H(esc(d["titular"]),76,mb=34,mw=1580)
    b += P(f'La métrica que importa: {esc(d["metrica"])}',28,GREY,mw=1500)
    cols="".join(f'''      <div style="border-top:2px solid {INK};padding-top:26px;">
        <div style="font-size:17px;letter-spacing:.2em;text-transform:uppercase;color:{GREY};margin-bottom:16px;">{esc(x["label"])}</div>
        <div style="font-size:32px;font-weight:700;letter-spacing:-.022em;line-height:1.2;margin-bottom:16px;">{esc(x["titulo"])}</div>
        <div style="font-size:28px;line-height:1.48;color:{GREY};">{esc(x["texto"])}</div>
      </div>''' for x in d["punto_a"])
    b += f'    <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:64px;margin-top:62px;">\n{cols}\n    </div>\n'
    add("01 · Dónde estás hoy",b)

    # 03 · LA LECTURA
    L=d["lectura"]
    b  = SP(48)+H(esc(L["titular"]),98,mb=48,lh=1.02,mw=1620)
    cita=f'''      <div style="display:flex;flex-direction:column;gap:16px;">
        <div class="it" style="font-size:34px;line-height:1.38;color:{PAPER2};">“{esc(L.get("cita",""))}”</div>
        <div style="font-size:22px;color:#8C8C90;">{esc(L.get("cita_autor",""))}</div>
      </div>''' if L.get("cita") else '<div></div>'
    b += f'''    <div style="display:grid;grid-template-columns:1.2fr 1fr;gap:80px;max-width:1680px;">
      <div style="font-size:31px;line-height:1.48;color:#C9C7C3;">{esc(L["texto"])}</div>
{cita}
    </div>\n'''
    b += f'''    <div style="display:inline-flex;align-self:flex-start;margin-top:58px;border:1px solid {PAPER2};padding:16px 30px;gap:20px;align-items:baseline;">
      <span style="font-size:18px;letter-spacing:.2em;text-transform:uppercase;color:#8C8C90;">Orientación</span>
      <span style="font-size:34px;font-weight:800;letter-spacing:-.02em;color:{PAPER2};">{esc(d["orientacion"])}</span>
    </div>\n'''
    add("02 · La lectura",b,True)

    # 04 · EL HANDICAP, escala 1-100
    if H_:
        gen=round(sum(cien(v) for v in [H_["ejes"][k] for k,_ in EJES])/5)
        filas=""
        for k,nom in EJES:
            v=cien(H_["ejes"][k]); flojo = k in H_["eje_flojo"]
            filas+=f'''      <div style="display:grid;grid-template-columns:250px 96px minmax(0,1fr);gap:30px;align-items:center;
           border-top:1px solid {INK if flojo else LINE};padding:22px 0;">
        <span style="font-size:22px;letter-spacing:.14em;text-transform:uppercase;color:{INK if flojo else GREY};font-weight:{700 if flojo else 400};">{esc(nom)}</span>
        <span class="num" style="font-size:38px;text-align:right;">{v}</span>
        <span style="display:block;height:12px;background:{LINE};"><span style="display:block;height:100%;width:{v}%;background:{INK};"></span></span>
      </div>'''
        b  = ""
        b += H("Tus cinco habilidades, de 1 a 100",76,mb=26)
        vals=[H_["ejes"][k] for k,_ in EJES]
        empate = vals.count(min(vals))>1
        sub = ("Cada una sube cuando pasa algo concreto en tu negocio. Hoy hay varias empatadas abajo, "
               "y manda la que el roadmap trabaja primero."
               if empate else
               "Cada una sube cuando pasa algo concreto en tu negocio. La más baja es por donde conviene "
               "empezar, porque es la que frena a las otras cuatro.")
        b += P(sub,28,GREY,mb=44,mw=1440)
        b += f'    <div style="display:grid;grid-template-columns:1.6fr .8fr;gap:72px;align-items:start;">\n      <div>\n{filas}\n      </div>\n'
        floj = H_["eje_flojo"][0]
        nomfloj = dict(EJES)[floj]
        b += f'''      <div style="border-top:2px solid {INK};padding-top:26px;">
        <div style="font-size:17px;letter-spacing:.2em;text-transform:uppercase;color:{GREY};margin-bottom:14px;">General</div>
        <div class="num" style="font-size:104px;line-height:.86;">{gen}</div>
        <div style="font-size:22px;color:{GREY};margin-top:14px;">{esc(H_["tramo"])}</div>
        <div style="margin-top:34px;border-top:1px solid {LINE};padding-top:22px;">
          <div style="font-size:17px;letter-spacing:.2em;text-transform:uppercase;color:{GREY};margin-bottom:12px;">Cómo sube {esc(nomfloj).lower()}</div>
          <div style="font-size:28px;line-height:1.46;">{esc(COMO_SUBE.get(floj,""))}</div>
        </div>
      </div>\n    </div>\n'''
        add("03 · El handicap",b)

    # 05 · LO QUE PASÓ
    R=d.get("recorrido") or {}
    if R:
        hitos="".join(f'''        <div style="display:grid;grid-template-columns:190px minmax(0,1fr);gap:24px;padding:15px 0;border-top:1px solid {LINE};">
          <span style="font-size:21px;letter-spacing:.1em;text-transform:uppercase;color:{GREY};">{esc(x["cuando"])}</span>
          <span style="font-size:28px;line-height:1.4;">{esc(x["que"])}</span>
        </div>''' for x in R.get("hitos",[]))
        b  = ""
        b += H(esc(R.get("titulo","")),72,mb=40,mw=1500)
        b += f'''    <div style="display:grid;grid-template-columns:1.15fr 1fr;gap:76px;align-items:start;">
      <div style="font-size:29px;line-height:1.5;">{esc(R.get("texto",""))}</div>
      <div>
        <div style="font-size:17px;letter-spacing:.2em;text-transform:uppercase;color:{GREY};margin-bottom:8px;">Los hitos</div>
{hitos}
      </div>
    </div>\n'''
        add("04 · Lo que pasó",b)

    # 06 · LAS RESPUESTAS
    RS=d.get("respuestas") or []
    if RS:
        cells="".join(f'''      <div style="border-top:1px solid {LINE};padding-top:22px;">
        <div class="num" style="font-size:30px;color:{GREY};line-height:1;margin-bottom:14px;">{i+1:02d}</div>
        <div style="font-size:27px;font-weight:700;letter-spacing:-.02em;line-height:1.22;margin-bottom:12px;">{esc(x["tema"])}</div>
        <div style="font-size:28px;line-height:1.46;color:{GREY};">{esc(x["respuesta"])}</div>
      </div>''' for i,x in enumerate(RS))
        cols = 2 if len(RS)<=4 else 3
        b  = ""
        b += H("Los temas que ya quedaron resueltos",72,mb=22)
        b += P("Cada uno se discutió y tiene una respuesta. De acá sale el roadmap.",28,GREY,mb=48,mw=1300)
        b += f'    <div style="display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:56px;">\n{cells}\n    </div>\n'
        add("05 · Las respuestas",b)

    # 07 · LO QUE TE ENTREGAMOS
    EN=d.get("entregables") or []
    if EN:
        filas="".join(f'''      <div style="display:grid;grid-template-columns:1fr 1fr;gap:56px;border-top:1px solid {LINE};padding:26px 0;align-items:start;">
        <div style="font-size:29px;font-weight:700;letter-spacing:-.02em;line-height:1.25;">{esc(x["que"])}</div>
        <div style="font-size:28px;line-height:1.46;color:{GREY};">{esc(x["para"])}</div>
      </div>''' for x in EN)
        b  = ""
        b += H("Lo que sale de Cáscara hacia tu negocio",72,mb=22)
        b += P("A la izquierda lo que te damos. A la derecha lo que hacés con eso.",28,GREY,mb=42,mw=1300)
        b += f'    <div>\n{filas}\n    </div>\n'
        add("06 · Lo que te entregamos",b)

    # 08 · CONCLUSIÓN ESTRATÉGICA
    if d.get("conclusion"):
        parrafos=[x.strip() for x in d["conclusion"].split("\n\n") if x.strip()]
        bloques=[]; cur=[]; peso=0
        for x in parrafos:
            pe=len(x)
            if cur and peso+pe>1150: bloques.append(cur); cur=[]; peso=0
            cur.append(x); peso+=pe
        if cur: bloques.append(cur)
        ultimo=len(bloques)-1
        for bi,bl in enumerate(bloques):
            b  = SP(40)
            b += H("Hacia dónde va el negocio",84,mb=44,mw=1500)
            for x in bl:
                b += P(esc(x),33,"#C9C7C3",mw=1520,lh=1.5,mb=32)
            if bi==ultimo and d.get("abierto"):
                b += f'''    <div style="margin-top:26px;border-top:1px solid {LINEINK};padding-top:24px;max-width:1400px;">
      <div style="font-size:19px;letter-spacing:.2em;text-transform:uppercase;color:#8C8C90;margin-bottom:12px;">Lo que queda sin definir</div>
      <div style="font-size:28px;line-height:1.46;color:#C9C7C3;">{esc(d["abierto"])}</div>
    </div>\n'''
            add("07 · La conclusión",b,True)

    # 09 · A DÓNDE VAMOS
    cells="".join(f'''      <div style="border-top:2px solid {INK};padding-top:26px;">
        <div style="font-size:19px;letter-spacing:.2em;text-transform:uppercase;color:{GREY};margin-bottom:14px;">{esc(x["fecha"])}</div>
        <div style="font-size:38px;font-weight:800;letter-spacing:-.026em;line-height:1.14;margin-bottom:18px;">{esc(x["titulo"])}</div>
        <div style="font-size:28px;line-height:1.48;color:{GREY};">{esc(x["texto"])}</div>
      </div>''' for x in d["punto_b"])
    b  = ""
    b += H("El objetivo del tramo",76,mb=48)
    b += f'    <div style="display:grid;grid-template-columns:1fr 1fr;gap:72px;">\n{cells}\n    </div>\n'
    add("08 · A dónde vamos",b)

    # 10 · EL ROADMAP, línea de tiempo horizontal
    RM=d["roadmap"]
    def paso(x): return f'''      <div style="position:relative;padding-top:52px;">
        <div style="position:absolute;top:-8px;left:0;width:17px;height:17px;background:{INK};"></div>
        <div style="font-size:20px;letter-spacing:.14em;text-transform:uppercase;color:{GREY};margin-bottom:14px;">{esc(x["cuando"])}</div>
        <div style="font-size:30px;font-weight:700;letter-spacing:-.02em;line-height:1.2;margin-bottom:14px;">{esc(x["objetivo"])}</div>
        <div style="font-size:28px;line-height:1.46;color:{GREY};margin-bottom:18px;">{esc(x["entregable"])}</div>
        <div style="font-size:20px;letter-spacing:.08em;text-transform:uppercase;color:{GREY};">{esc(x["quien"])}</div>
      </div>'''
    import math
    ng=max(1,math.ceil(len(RM)/3))
    base,resto=divmod(len(RM),ng)
    tramos=[]; k=0
    for gi in range(ng):
        c=base+(1 if gi<resto else 0); tramos.append(RM[k:k+c]); k+=c
    for gi,tr in enumerate(tramos):
        b  = ""
        b += H("La línea de tiempo",76,mb=22)
        b += P("De izquierda a derecha, en el orden en que pasa." if gi==0 else "Sigue de donde quedó la hoja anterior.",28,GREY,mb=52,mw=1200)
        b += f'''    <div style="position:relative;">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{INK};"></div>
      <div style="display:grid;grid-template-columns:repeat({len(tr)},minmax(0,1fr));gap:56px;">
{"".join(paso(x) for x in tr)}
      </div>
    </div>\n'''
        add("09 · El roadmap",b)

    # 11 · LOS ACCIONABLES, checklist
    AC=d["accionables"]
    BQ=[]
    ci=0
    for bl in AC:
        for lado,tit in (("cliente","Lo hacés vos"),("cascara","Lo hace Cáscara")):
            items=bl.get(lado) or []
            if not items: continue
            g=f'{esc(bl["cuando"])}-{lado}'.replace(' ','_')
            lis=""
            for x in items:
                ci+=1
                lis+=f'''          <div class="chk" role="checkbox" tabindex="0" aria-checked="false" data-k="k{ci}" data-g="{g}"
               style="display:grid;grid-template-columns:34px minmax(0,1fr);gap:20px;padding:16px 0;border-top:1px solid {LINE};align-items:start;">
            <span class="box" style="width:26px;height:26px;border:2px solid {GREY};margin-top:5px;"><i></i></span>
            <span style="font-size:29px;line-height:1.44;"><span class="txt">{esc(x)}</span></span>
          </div>'''
            BQ.append((f'''      <div>
        <div style="display:flex;justify-content:space-between;align-items:baseline;gap:20px;border-bottom:2px solid {INK};padding-bottom:12px;margin-bottom:6px;">
          <span style="font-size:21px;letter-spacing:.18em;text-transform:uppercase;color:{GREY};">{esc(bl["cuando"])} · {tit}</span>
          <span class="num" data-cuenta="{g}" style="font-size:24px;color:{GREY};">0 de {len(items)}</span>
        </div>
{lis}
      </div>''', len(items)+2))
    grupos=[]; cur=[]; peso=0
    for bq,p in BQ:
        if cur and peso+p>26: grupos.append(cur); cur=[]; peso=0
        cur.append(bq); peso+=p
    if cur: grupos.append(cur)
    for gi,g in enumerate(grupos):
        b  = H("Los accionables",76,mb=22)
        b += P("Tocá cada uno cuando lo termines. El documento se acuerda de lo que ya tachaste.",28,GREY,mb=44,mw=1400)
        cols = 1 if len(g)==1 else 2
        b += f'    <div style="display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:56px 72px;align-items:start;">\n' + "\n".join(g) + '\n    </div>\n'
        add("10 · Los accionables",b)

    # 12 · LA CARTA — hoja desnuda: solo el párrafo, centrado
    PN.append(("carta",esc(d.get("carta","")),False,None))

    T=len(PN)-1   # la carta no lleva número
    out=[]; i=0
    for k,bb,dk,ft in PN:
        if k=="carta":
            out.append(B2.carta(bb)); continue
        i+=1
        out.append(B.panel(f"{i:02d}",f"{T:02d}","",k,bb,dark=dk,foot=ft))
    return out

if __name__=="__main__":
    salida=os.path.join(RAIZ,"clientes")
    os.makedirs(salida,exist_ok=True)
    n=0
    for f in sorted(glob.glob(os.path.join(RAIZ,"fichas","*.json"))):
        d=json.load(open(f,encoding="utf-8"))
        tit=f'{d["cliente"]} · {"Informe de cierre" if d["modo"]=="cierre" else "Radiografía y roadmap"}'
        open(os.path.join(salida,f'{d["slug"]}.html'),"w",encoding="utf-8").write(compose(build(d),tit))
        n+=1
    print("documentos v2:",n)
