# -*- coding: utf-8 -*-
"""Los SOPs de Founders: documentos para leer y aplicar, sin nada que completar.

Reorganización de Facu del 21/10: en fichas/inventario.json cada módulo tiene
`tipo`. Los de tipo "sop" no se completan: se estudian y se aplican, y van
pegados a una carta (`va_con` = id de la carta, "arranque", o nada).

Este script publica cada SOP como documento de lectura en cartas/sop/<id>.html,
con la misma estética que las cartas de build_cartas.py, y arma el índice en
cartas/sop/index.html (cada carta con sus SOPs abajo, y aparte los del arranque
y los sueltos).

De dónde sale el contenido de cada SOP, en este orden:
  1. un .md de fichas/sops/ con `reemplaza: <id>` en el frontmatter
  2. fichas/sops/<id>.md
  3. la plantilla fichas/plantillas/<id>.json (era una carta: sus campos se
     muestran como pasos para aplicar, sin inputs ni guardado)
Los .md de fichas/sops/ que no tienen módulo en el inventario se publican
igual: son los SOPs nuevos. Frontmatter: nombre, va_con, reemplaza (y,
opcionales, bajada, cuando, lista_cuando).

Se regenera con:  python3 generador/build_sops.py   (después de build_cartas.py)
"""
import os, re, sys, json, glob

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
from build_cartas import CSS as CSS_CARTAS, esc   # sin efectos: el build va bajo __main__

CSS = CSS_CARTAS + """
.arriba{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
.arriba a{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:#6A6A66;text-decoration:none;
  border-bottom:1px solid #DBD7D2;padding-bottom:2px}
.arriba a:hover{color:#171717;border-color:#171717}
.vacon a{color:#171717;text-decoration:none;border-bottom:1px solid #171717}
.btn-pdf{margin-top:30px;font:inherit;font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;
  border:1px solid #171717;background:#171717;color:#ECEAE4;padding:13px 18px;cursor:pointer}
.btn-pdf:hover{background:transparent;color:#171717}
.escribir{margin-top:24px;background:#FBFAF8;border:1px solid #DBD7D2;padding:18px 20px}
.escribir .et{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85}
.escribir .tx{font-size:17px;line-height:1.5;color:#6A6A66;margin-top:8px;max-width:60ch}
.escribir ul{margin:10px 0 0;padding:0;list-style:none}
.escribir li{font-size:17.5px;line-height:1.45;border-top:1px solid #DBD7D2;padding:10px 0}
.escribir li:first-child{border-top:0}
.nuestro .devuelta .q{font-family:"Redaction 10","Redaction","Exposure","Times New Roman",Times,serif;
  font-style:italic;font-size:18px;line-height:1.5;color:#6A6A66;margin-top:8px;max-width:62ch}
.md ul,.md ol{margin:14px 0 0;padding-left:1.3em;max-width:62ch}
.md li{font-size:18.5px;line-height:1.55;margin-top:6px}
.md h3{font-size:21px;font-weight:800;letter-spacing:-.02em;margin:28px 0 0}
.md blockquote{margin:18px 0 0;border-left:2px solid #DBD7D2;padding:4px 0 4px 20px;
  font-family:"Redaction 10","Redaction","Exposure","Times New Roman",Times,serif;font-style:italic;color:#6A6A66}
.md code{font-size:.9em;background:#FBFAF8;border:1px solid #DBD7D2;padding:1px 5px}
.md a,.nuestro p a{color:#171717}
.md hr{border:0;border-top:1px solid #DBD7D2;margin:30px 0 0}

/* el índice */
.cat{margin-top:56px}
.cat>.et{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85;
  border-bottom:2px solid #171717;padding-bottom:12px}
.carta{border-bottom:1px solid #DBD7D2;padding:20px 0}
.carta .nom{font-size:21px;font-weight:800;letter-spacing:-.02em;line-height:1.25}
.carta .nom a{color:#171717;text-decoration:none}
.carta .nom a:hover{text-decoration:underline}
.carta ul{margin:12px 0 0;padding:0;list-style:none}
.carta li{display:grid;grid-template-columns:44px minmax(0,1fr);gap:10px;align-items:baseline;padding:6px 0}
.carta li .k{font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;color:#8E8B85}
.carta li a{font-size:17.5px;color:#171717;text-decoration:none;border-bottom:1px solid #DBD7D2}
.carta li a:hover{border-color:#171717}
.carta li .falta{font-size:17.5px;color:#8E8B85}
.carta .nada{font-size:15px;color:#8E8B85;margin-top:8px}

@media (max-width:640px){
  .escribir{padding:14px 16px}
}
@media print{
  @page{margin:16mm 14mm}
  html,body{background:#fff!important}
  body{font-size:11.5pt}
  .hoja{max-width:none;padding:0}
  .btn-pdf,.arriba a,.no-print{display:none!important}
  h1{font-size:30pt;margin-top:14px}
  .bajada{font-size:13pt}
  section,.nuestro{margin-top:28px;break-inside:auto}
  section h2,.nuestro h2{font-size:17pt;break-after:avoid}
  .paso,.escribir,.ejemplo,.escribir li{break-inside:avoid}
  .escribir{background:#fff}
  .vacon a{border:0}
  .pie{margin-top:30px}
}
"""

JS = """document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('[data-a="pdf"]'); if(b) window.print();});"""


# ---------------------------------------------------------------- markdown
def frontmatter(txt):
    meta = {}
    if txt.startswith('---'):
        partes = txt.split('\n')
        for k in range(1, len(partes)):
            if partes[k].strip() == '---':
                for l in partes[1:k]:
                    if ':' in l and not l.lstrip().startswith('#'):
                        a, b = l.split(':', 1)
                        b = b.strip().strip('"').strip("'")
                        meta[a.strip()] = None if b.lower() in ('', 'null', 'none', '~') else b
                txt = '\n'.join(partes[k + 1:])
                break
    return meta, txt


def inline(s):
    s = esc(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', s)
    s = re.sub(r'(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])', r'<i>\1</i>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', s)
    return s


def md_bloques(txt):
    """Markdown chico, sin dependencias: párrafos, ###, listas, citas, ---,
    y HTML suelto (una línea que empieza con <) que pasa tal cual."""
    out, par, lista, tipo_l = [], [], [], None
    def cerrar():
        nonlocal par, lista, tipo_l
        if par: out.append('<p>%s</p>' % inline(' '.join(par))); par = []
        if lista:
            out.append('<%s>%s</%s>' % (tipo_l, ''.join('<li>%s</li>' % inline(x) for x in lista), tipo_l))
            lista, tipo_l = [], None
    for l in txt.split('\n'):
        s = l.strip()
        if not s: cerrar(); continue
        if s.startswith('<'): cerrar(); out.append(l); continue
        if re.match(r'^(-{3,}|\*{3,})$', s): cerrar(); out.append('<hr>'); continue
        m = re.match(r'^#{3,6}\s+(.*)', s)
        if m: cerrar(); out.append('<h3>%s</h3>' % inline(m.group(1))); continue
        if s.startswith('>'): cerrar(); out.append('<blockquote>%s</blockquote>' % inline(s.lstrip('> '))); continue
        m = re.match(r'^[-*+]\s+(.*)', s) or re.match(r'^\d+[.)]\s+(.*)', s)
        if m:
            t = 'ul' if re.match(r'^[-*+]', s) else 'ol'
            if par: cerrar()
            if tipo_l and tipo_l != t: cerrar()
            tipo_l = t; lista.append(m.group(1)); continue
        if lista and l.startswith((' ', '\t')): lista[-1] += ' ' + s; continue
        if lista: cerrar()
        par.append(s)
    cerrar()
    return out


def md_doc(txt):
    """Devuelve (titulo h1 o None, bloques sueltos del principio, [(h2, bloques)])."""
    h1, intro, secs, cur = None, [], [], None
    for l in txt.split('\n'):
        m = re.match(r'^#\s+(.*)', l.strip())
        if m and h1 is None and not secs and not ''.join(intro).strip():
            h1 = m.group(1).strip(); continue
        m = re.match(r'^##\s+(.*)', l.strip())
        if m:
            cur = [m.group(1).strip(), []]; secs.append(cur); continue
        (cur[1] if cur else intro).append(l)
    return h1, md_bloques('\n'.join(intro)), [(t, md_bloques('\n'.join(b))) for t, b in secs]


# ---------------------------------------------------------------- de carta a lectura
def lo_que_se_escribe(s):
    tipo = s.get("campo", "texto")
    if tipo == "tabla":
        cols = s.get("columnas") or []
        rot = [r for r in (s.get("filas_rotulo") or []) if r]
        h = ('<div class="escribir"><div class="et">Lo que hay que escribir</div>'
             '<div class="tx">Una tabla con estas columnas%s.</div><ul>%s</ul>'
             % (', una fila por cada cosa' if not rot else '', ''.join('<li>%s</li>' % esc(c) for c in cols)))
        if rot:
            h += ('<div class="tx" style="margin-top:14px">Una fila para cada una de estas:</div><ul>%s</ul>'
                  % ''.join('<li>%s</li>' % esc(r) for r in rot))
        return h + '</div>'
    if tipo == "lineas":
        return ('<div class="escribir"><div class="et">Lo que hay que escribir</div><ul>%s</ul></div>'
                % ''.join('<li>%s</li>' % esc(r) for r in (s.get("lineas") or [])))
    ph = s.get("placeholder")
    return ('<div class="escribir"><div class="et">Lo que hay que escribir</div>'
            '<div class="tx">%s</div></div>'
            % (esc(ph) if ph else 'Un texto corto con tu respuesta, en tus palabras.'))


def cuerpo_plantilla(m, pl):
    out, n = [], 0
    pasos = (m or {}).get("pasos") or []
    if pasos:
        n += 1
        out.append('<section>\n  <div class="n">%02d</div>\n  <h2>Cómo se aplica</h2>' % n)
        out.append('  <p class="consigna">En este orden. Abajo está cada parte explicada.</p>')
        out.append('  <div class="pasos">')
        for i, x in enumerate(pasos):
            out.append('    <div class="paso"><span class="p">%02d</span><span class="t">%s</span></div>'
                       % (i + 1, esc(x)))
        out.append('  </div>\n</section>')
    for s in (pl or {}).get("secciones") or []:
        if s.get("nuestro"):
            out.append('<div class="nuestro">')
            out.append('  <h2>%s</h2>' % esc(s.get("titulo")))
            for par in (s.get("texto") or []):
                out.append('  <p>%s</p>' % par)          # texto nuestro: el HTML va
            if s.get("figura"):
                out.append(s["figura"])
            if s.get("pregunta"):
                out.append('  <div class="devuelta"><div class="k">Para pensar</div>'
                           '<div class="q">%s</div></div>' % esc(s["pregunta"]))
            out.append('</div>')
            continue
        n += 1
        out.append('<section>\n  <div class="n">%02d</div>' % n)
        out.append('  <h2>%s</h2>' % esc(s.get("titulo")))
        if s.get("consigna"):
            out.append('  <p class="consigna">%s</p>' % s["consigna"])
        ej = s.get("ejemplo") or {}
        if ej.get("texto"):
            quien = ('Cómo lo resolvió %s' % esc(ej["quien"])) if ej.get("quien") else 'Un ejemplo'
            out.append('  <div class="ejemplo"><div class="et">%s</div><div class="tx">%s</div></div>'
                       % (quien, esc(ej["texto"])))
        out.append('  ' + lo_que_se_escribe(s))
        out.append('</section>')
    return "\n".join(out)


def cuerpo_md(intro, secs):
    out = []
    if intro:
        out.append('<div class="md" style="margin-top:46px">\n%s\n</div>' % '\n'.join(intro))
    for t, b in secs:
        out.append('<div class="nuestro md">\n  <h2>%s</h2>\n%s\n</div>' % (inline(t), '\n'.join(b)))
    return "\n".join(out)


# ---------------------------------------------------------------- página
def pagina(titulo, cuerpo, pie):
    return ('<!doctype html>\n<html lang="es"><head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n<div class="hoja">\n<main>\n%s\n</main>\n'
            '<div class="pie"><div><span class="sello">C</span></div><div>Cáscara Founders · %s</div></div>\n'
            '</div>\n<script>%s</script>\n</body></html>\n') % (esc(titulo), CSS, cuerpo, esc(pie), JS)


def va_con_html(vc, cartas, prefijo='../'):
    if not vc:
        return 'ninguna carta en particular, se usa suelto'
    if vc == 'arranque':
        return 'el arranque del programa'
    if vc in cartas:
        return '<a href="%s%s.html">%s</a>' % (prefijo, esc(vc), esc(cartas[vc]["nombre"]))
    return esc(vc)


def render_sop(sop, cartas):
    m, pl = sop.get("modulo"), sop.get("plantilla")
    out = ['<header>']
    out.append('  <div class="arriba"><div class="caja">SOP%s</div><a href="index.html">Todos los SOPs</a></div>'
               % (' · ' + esc(sop["categoria"]) if sop.get("categoria") else ''))
    out.append('  <h1>%s</h1>' % esc(sop["nombre"]))
    if sop.get("bajada"):
        out.append('  <p class="bajada">%s</p>' % sop["bajada"])
    out.append('  <div class="lista">')
    out.append('    <div class="vacon"><div class="et">Va con</div><div class="tx">%s</div></div>'
               % va_con_html(sop.get("va_con"), cartas))
    if sop.get("cuando"):
        out.append('    <div><div class="et">Cuándo se usa</div><div class="tx">%s</div></div>' % esc(sop["cuando"]))
    if sop.get("lista_cuando"):
        out.append('    <div><div class="et">Está aplicado cuando</div><div class="tx">%s</div></div>'
                   % esc(sop["lista_cuando"]))
    out.append('  </div>')
    out.append('  <button class="btn-pdf" data-a="pdf">Descargar PDF</button>')
    out.append('</header>')
    if sop.get("md") is not None:
        out.append(cuerpo_md(*sop["md"]))
    else:
        out.append(cuerpo_plantilla(m, pl))
    return pagina('%s · SOP' % sop["nombre"], "\n".join(out), sop.get("categoria") or 'SOP')


def render_indice(sops, inv, cartas):
    out = ['<header>', '  <div class="caja">SOPs · Cáscara Founders</div>',
           '  <h1>Los SOPs, carta por carta</h1>',
           '  <p class="bajada">Cada SOP se lee y se aplica: no hay nada para completar. '
           'Sale junto con la carta que tiene arriba.</p>', '</header>']
    por_carta = {}
    for s in sops.values():
        if s.get("va_con") in cartas:
            por_carta.setdefault(s["va_con"], [])
    por_escribir = {}
    for x in inv.get("sops_por_escribir") or []:
        if x.get("id") not in sops:
            por_escribir.setdefault(x.get("va_con") or '', []).append(x)

    def item(sid):
        s = sops[sid]
        return '<li><span class="k">SOP</span><a href="%s.html">%s</a></li>' % (esc(sid), esc(s["nombre"]))
    def falta(x):
        return '<li><span class="k">Falta</span><span class="falta">%s · por escribir</span></li>' % esc(x.get("nombre"))

    for c in inv["categorias"]:
        cs = [m for m in c["modulos"] if m.get("tipo") == "carta"]
        if not cs: continue
        out.append('<div class="cat"><div class="et">%s</div>' % esc(c["nombre"]))
        for m in cs:
            ids = [x for x in (m.get("sops") or []) if x in sops]
            ids += sorted((k for k, s in sops.items() if s.get("va_con") == m["id"] and k not in ids),
                          key=lambda k: sops[k]["nombre"])
            faltan = por_escribir.get(m["id"], [])
            out.append('  <div class="carta"><div class="nom"><a href="../%s.html">%s</a></div>'
                       % (esc(m["id"]), esc(m["nombre"])))
            if ids or faltan:
                out.append('    <ul>%s%s</ul>' % (''.join(item(k) for k in ids), ''.join(falta(x) for x in faltan)))
            else:
                out.append('    <div class="nada">Sin SOPs por ahora.</div>')
            out.append('  </div>')
        out.append('</div>')

    for titulo, filtro, clave in (("Arranque del programa", lambda v: v == 'arranque', 'arranque'),
                                  ("Sueltos", lambda v: v != 'arranque' and v not in cartas, '')):
        ids = sorted((k for k, s in sops.items() if filtro(s.get("va_con"))), key=lambda k: sops[k]["nombre"])
        faltan = por_escribir.get(clave, [])
        if clave == '':
            faltan = faltan + [x for v, xs in por_escribir.items() if v not in ('', 'arranque') and v not in cartas for x in xs]
        if not ids and not faltan: continue
        out.append('<div class="cat"><div class="et">%s</div><div class="carta"><ul>%s%s</ul></div></div>'
                   % (titulo, ''.join(item(k) for k in ids), ''.join(falta(x) for x in faltan)))
    return pagina('SOPs · Cáscara Founders', "\n".join(out), 'SOPs')


# ---------------------------------------------------------------- armado
def juntar(raiz):
    inv = json.load(open(os.path.join(raiz, 'fichas', 'inventario.json'), encoding='utf-8'))
    mods = {m["id"]: (m, c["nombre"]) for c in inv["categorias"] for m in c["modulos"]}
    cartas = {k: m for k, (m, _) in mods.items() if m.get("tipo") == "carta"}
    # a qué carta va pegado cada SOP: su va_con, o la carta que lo lista en `sops`
    listado = {}
    for k, m in cartas.items():
        for s in m.get("sops") or []:
            listado.setdefault(s, k)
    pendientes = {x["id"]: x for x in inv.get("sops_por_escribir") or [] if x.get("id")}

    # los .md: con reemplaza pisan a ese id; si no, valen por el nombre del archivo
    mds = {}
    for f in sorted(glob.glob(os.path.join(raiz, 'fichas', 'sops', '*.md'))):
        meta, txt = frontmatter(open(f, encoding='utf-8').read())
        sid = meta.get("reemplaza") or os.path.splitext(os.path.basename(f))[0]
        if sid in mds and not meta.get("reemplaza"):
            continue                    # ya lo pisó otro .md con reemplaza
        mds[sid] = (meta, txt, f)

    sops = {}
    ids = [k for k, (m, _) in mods.items() if m.get("tipo") == "sop"]
    ids += [k for k in mds if k not in ids]
    for sid in ids:
        m, cat = mods.get(sid, (None, None))
        meta, txt, _ = mds.get(sid, ({}, None, None))
        pend = pendientes.get(sid) or {}
        vc = (m or {}).get("va_con") or listado.get(sid) or meta.get("va_con") or pend.get("va_con")
        if cat is None and vc in cartas:
            cat = mods[vc][1]
        s = {"id": sid, "modulo": m, "va_con": vc, "categoria": cat}
        if txt is not None:
            h1, intro, secs = md_doc(txt)
            s["nombre"] = (m or {}).get("nombre") or meta.get("nombre") or pend.get("nombre") or h1 or sid
            s["md"] = (intro, secs)
            s["bajada"] = esc(meta.get("bajada")) if meta.get("bajada") else esc((m or {}).get("resultado"))
            s["cuando"] = meta.get("cuando") or (m or {}).get("para_quien")
            s["lista_cuando"] = meta.get("lista_cuando")
            s["fuente"] = "md"
        else:
            p = os.path.join(raiz, 'fichas', 'plantillas', sid + '.json')
            pl = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None
            s["plantilla"] = pl
            s["nombre"] = (m or {}).get("nombre") or (pl or {}).get("titulo") or sid
            s["bajada"] = (pl or {}).get("bajada") or esc((m or {}).get("resultado"))
            s["cuando"] = (m or {}).get("para_quien")
            s["lista_cuando"] = (pl or {}).get("lista_cuando")
            s["fuente"] = "plantilla" if pl else "inventario"
        sops[sid] = s
    return inv, cartas, sops


if __name__ == "__main__":
    inv, cartas, sops = juntar(RAIZ)
    dest = os.path.join(RAIZ, 'cartas', 'sop')
    os.makedirs(dest, exist_ok=True)
    cuenta = {}
    for sid, s in sops.items():
        open(os.path.join(dest, sid + '.html'), 'w', encoding='utf-8').write(render_sop(s, cartas))
        cuenta[s["fuente"]] = cuenta.get(s["fuente"], 0) + 1
    open(os.path.join(dest, 'index.html'), 'w', encoding='utf-8').write(render_indice(sops, inv, cartas))
    print("sops:", len(sops), "·", " · ".join("%s %d" % kv for kv in sorted(cuenta.items())))
