# -*- coding: utf-8 -*-
"""Las cartas de módulo. Una por módulo, en la estética de los documentos.

Un módulo dice, además de cómo se hace algo, qué pasos seguir, qué hay que
completar y qué herramientas implementar. Esta carta es eso, en una hoja
que el founder puede leer y tachar.

Si se le pasa una bajada personalizada (para quién va, por qué esa carta,
cuál es el objetivo y con qué cabeza encararla), entra como segunda hoja.
"""
import json, os, math, html as _h
import build as B
import build2 as B2

INK,DEEP,PAPER,PAPER2 = B.INK,B.DEEP,B.PAPER,B.PAPER2
GREY,LINE,LINEINK,SOFT = B.GREY,B.LINE,B.LINEINK,B.SOFT
esc, H, P, ET, SP = B2.esc, B2.H, B2.P, B2.ET, B2.SP

EJE_NOMBRE = {"oferta":"Oferta","contenido":"Contenido","demanda":"Demanda",
              "venta":"Venta","entrega":"Entrega"}
ESTADO = {"escrito":"La carta ya está escrita",
          "parcial":"El criterio existe y se baja caso por caso",
          "falta":"Todavía sin escribir",
          "propuesta":"Propuesta, a confirmar el alcance"}


def _paginar(items, por_hoja):
    n = max(1, math.ceil(len(items)/por_hoja))
    base, resto = divmod(len(items), n)
    out, k = [], 0
    for i in range(n):
        c = base + (1 if i < resto else 0)
        out.append(items[k:k+c]); k += c
    return out


def construir(m, categoria, bajada=None):
    """m: el módulo del inventario. bajada: dict opcional con founder, porque, objetivo, mindset."""
    PN = []
    pie = f'{esc(categoria)} · Cáscara Founders'
    def add(k, b, dark=False, ft=None): PN.append((k, b, dark, ft or pie))

    # 01 · PORTADA
    b  = SP(96)
    b += f'    <div style="font-size:28px;letter-spacing:.24em;text-transform:uppercase;color:#8C8C90;margin-bottom:36px;">Carta de módulo</div>\n'
    b += H(esc(m["nombre"]), 96, PAPER2, mb=44, lh=1.0, mw=1560)
    b += f'    <div style="font-size:36px;line-height:1.42;color:#C9C7C3;max-width:1420px;">{esc(m["resultado"])}</div>\n'
    ejes = " · ".join(EJE_NOMBRE.get(e, e) for e in m.get("eje", []))
    if ejes:
        b += f'''    <div style="margin-top:70px;border-top:1px solid {LINEINK};padding-top:26px;max-width:1500px;">
      <div style="font-size:19px;letter-spacing:.2em;text-transform:uppercase;color:#8C8C90;margin-bottom:12px;">Qué habilidad mueve</div>
      <div style="font-size:30px;line-height:1.4;color:{PAPER2};">{esc(ejes)}</div>
    </div>\n'''
    add("Cáscara Founders", b, True, "Cáscara diseña, vos ejecutás")

    # 02 · LA BAJADA PERSONALIZADA
    if bajada and (bajada.get("porque") or bajada.get("objetivo") or bajada.get("mindset")):
        quien = bajada.get("founder") or ""
        b  = ""
        b += H(f"Por qué esta carta, {esc(quien)}" if quien else "Por qué esta carta", 76, mb=26)
        b += P("Esto lo escribimos para vos, sobre lo que venimos viendo en tu caso.", 28, GREY, mb=48, mw=1300)
        filas = ""
        for et, tx in (("Por qué te toca ahora", bajada.get("porque")),
                       ("El objetivo concreto", bajada.get("objetivo")),
                       ("Con qué cabeza encararla", bajada.get("mindset"))):
            if not tx: continue
            filas += f'''      <div style="border-top:2px solid {INK};padding-top:24px;">
        <div style="font-size:20px;letter-spacing:.18em;text-transform:uppercase;color:{GREY};margin-bottom:16px;">{et}</div>
        <div style="font-size:28px;line-height:1.46;">{esc(tx)}</div>
      </div>'''
        b += f'    <div style="display:grid;grid-template-columns:repeat({max(1,filas.count("border-top:2px"))},minmax(0,1fr));gap:64px;align-items:start;">\n{filas}\n    </div>\n'
        add("Tu bajada", b)

    # 03 · CUÁNDO SE ASIGNA
    b  = ""
    b += H("Cuándo se usa", 76, mb=26)
    b += P(esc(m.get("para_quien", "")), 32, None, mb=0, mw=1480, lh=1.46)
    est = ESTADO.get(m.get("estado", ""), "")
    if est:
        b += f'''    <div style="margin-top:64px;border-top:1px solid {LINE};padding-top:24px;max-width:1400px;">
      <div style="font-size:20px;letter-spacing:.18em;text-transform:uppercase;color:{GREY};margin-bottom:12px;">Estado de la carta</div>
      <div style="font-size:26px;line-height:1.45;color:{GREY};">{esc(est)}</div>
    </div>\n'''
    add("Cuándo se usa", b)

    # 04 · LOS PASOS
    pasos = m.get("pasos", [])
    for gi, grupo in enumerate(_paginar(pasos, 5)):
        base = sum(len(x) for x in _paginar(pasos, 5)[:gi])
        filas = "".join(f'''      <div style="display:grid;grid-template-columns:96px minmax(0,1fr);gap:34px;align-items:baseline;
           border-top:1px solid {LINE};padding:26px 0;">
        <span class="num" style="font-size:44px;color:{GREY};line-height:1;">{base+i+1:02d}</span>
        <span style="font-size:30px;line-height:1.42;">{esc(x)}</span>
      </div>''' for i, x in enumerate(grupo))
        b  = H("Los pasos", 76, mb=22)
        b += P("En este orden. Cada uno se apoya en el anterior.", 28, GREY, mb=40, mw=1300)
        b += f'    <div>\n{filas}\n    </div>\n'
        add("Los pasos", b)

    # 05 · QUÉ HAY QUE COMPLETAR, con checklist
    comp = m.get("completar", [])
    if comp:
        lis = ""
        for i, x in enumerate(comp):
            lis += f'''        <div class="chk" role="checkbox" tabindex="0" aria-checked="false" data-k="c{i}" data-g="completar"
             style="display:grid;grid-template-columns:34px minmax(0,1fr);gap:22px;padding:20px 0;border-top:1px solid {LINE};align-items:start;">
          <span class="box" style="width:26px;height:26px;border:2px solid {GREY};margin-top:6px;"><i></i></span>
          <span style="font-size:30px;line-height:1.42;"><span class="txt">{esc(x)}</span></span>
        </div>'''
        b  = H("Qué tenés que completar", 76, mb=22)
        b += P(f"La carta está hecha cuando {'estas dos cosas existen' if len(comp)==2 else ('esto existe' if len(comp)==1 else f'estas {len(comp)} cosas existen')}. Tocá cada una cuando la termines.", 28, GREY, mb=40, mw=1400)
        b += f'''    <div style="display:flex;justify-content:space-between;align-items:baseline;gap:20px;border-bottom:2px solid {INK};padding-bottom:14px;margin-bottom:6px;">
      <span style="font-size:21px;letter-spacing:.18em;text-transform:uppercase;color:{GREY};">Los entregables</span>
      <span class="num" data-cuenta="completar" style="font-size:24px;color:{GREY};">0 de {len(comp)}</span>
    </div>
{lis}\n'''
        add("Qué completar", b)

    # 06 · LAS HERRAMIENTAS
    herr = m.get("herramientas", [])
    if herr:
        filas = "".join(f'''      <div style="border-top:2px solid {INK};padding-top:22px;">
        <div style="font-size:28px;font-weight:700;letter-spacing:-.02em;line-height:1.25;">{esc(x)}</div>
      </div>''' for x in herr)
        cols = 2 if len(herr) > 2 else len(herr)
        b  = H("Qué herramientas implementar", 76, mb=22)
        b += P("Si alguna te falta, pedíla en el grupo antes de arrancar.", 28, GREY, mb=44, mw=1300)
        b += f'    <div style="display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:44px 64px;align-items:start;">\n{filas}\n    </div>\n'
        add("Las herramientas", b)

    # 07 · CIERRE
    b  = SP(80)
    b += f'    <div style="font-size:19px;letter-spacing:.22em;text-transform:uppercase;color:#8C8C90;margin-bottom:44px;">Cómo trabajamos</div>\n'
    b += f'''    <div class="it" style="font-size:44px;line-height:1.42;color:{PAPER2};max-width:1400px;">Cáscara baja la estructura, el criterio y un ejemplo de cada cosa. La ejecución es tuya, y es la parte que deja el resultado. Cuando termines esta carta, avisá en el grupo y sale la que sigue.</div>\n'''
    add("Cáscara Founders", b, True, "Avisá en el grupo cuando esté")

    T = len(PN)
    return [B.panel(f"{i+1:02d}", f"{T:02d}", "", k, bb, dark=dk, foot=ft)
            for i, (k, bb, dk, ft) in enumerate(PN)]


# La hoja de la bajada va desnuda: sin etiqueta, sin pie y sin número, así se puede
# insertar sin correr la numeración del resto. La app la clona y la completa.
TPL = f'''<template id="tpl-bajada">
<div class="slot" style="background:{PAPER};color:{INK};">
<div class="pnl" style="width:1920px;height:1080px;box-sizing:border-box;background:{PAPER};
     display:flex;flex-direction:column;justify-content:center;padding:120px 150px;">
  <div style="font-size:26px;letter-spacing:.22em;text-transform:uppercase;color:{GREY};margin-bottom:40px;">Tu bajada</div>
  <div data-b="titulo" style="font-size:82px;font-weight:800;letter-spacing:-.035em;line-height:1.02;margin-bottom:26px;max-width:1500px;"></div>
  <div style="font-size:30px;line-height:1.46;color:{GREY};max-width:1300px;margin-bottom:64px;">Esto lo escribimos para vos, sobre lo que venimos viendo en tu caso.</div>
  <div data-b="grilla" style="display:grid;gap:56px 64px;align-items:start;">
    <div data-b="fila-porque" style="border-top:2px solid {INK};padding-top:24px;">
      <div style="font-size:20px;letter-spacing:.18em;text-transform:uppercase;color:{GREY};margin-bottom:16px;">Por qué te toca ahora</div>
      <div data-b="porque" style="font-size:28px;line-height:1.46;"></div>
    </div>
    <div data-b="fila-objetivo" style="border-top:2px solid {INK};padding-top:24px;">
      <div style="font-size:20px;letter-spacing:.18em;text-transform:uppercase;color:{GREY};margin-bottom:16px;">El objetivo concreto</div>
      <div data-b="objetivo" style="font-size:28px;line-height:1.46;"></div>
    </div>
    <div data-b="fila-mindset" style="border-top:2px solid {INK};padding-top:24px;">
      <div style="font-size:20px;letter-spacing:.18em;text-transform:uppercase;color:{GREY};margin-bottom:16px;">Con qué cabeza encararla</div>
      <div data-b="mindset" style="font-size:28px;line-height:1.46;"></div>
    </div>
  </div>
</div>
</div>
</template>'''


def render(m, categoria, bajada=None):
    quien = (bajada or {}).get("founder")
    tit = f'{m["nombre"]} · carta de módulo' + (f' · {quien}' if quien else '')
    html = B2.compose(construir(m, categoria, bajada), tit)
    return html.replace('</body>', TPL + '\n</body>')


if __name__ == "__main__":
    inv = json.load(open('modulos/inventario.json', encoding='utf-8'))
    os.makedirs('cartas', exist_ok=True)
    n = 0
    indice = []
    for c in inv["categorias"]:
        for m in c["modulos"]:
            open(f'cartas/{m["id"]}.html', 'w', encoding='utf-8').write(render(m, c["nombre"]))
            indice.append({"id": m["id"], "categoria": c["nombre"], "nombre": m["nombre"]})
            n += 1
    json.dump(indice, open('cartas/indice.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print("cartas:", n)
