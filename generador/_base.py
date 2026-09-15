# -*- coding: utf-8 -*-
"""Devolución a Bianca: el documento de Eclipse y la comunidad de WhatsApp."""
import html as _h, io, sys
sys.path.insert(0,'/home/claude/founders')
from build_plantillas import INK, DEEP, PAPER, PAPER2, GREY, GREY2, LINE, ROJO, DISP, SERIF

def esc(s): return _h.escape(str(s or ""))

CSS = f"""
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:{PAPER};color:{INK};font-family:{DISP};
  font-size:18px;line-height:1.55;-webkit-font-smoothing:antialiased}}
.hoja{{max-width:880px;margin:0 auto;padding:64px 32px 110px}}
.caja{{display:inline-block;border:1px solid {GREY2};padding:6px 13px;font-size:10.5px;
  letter-spacing:.24em;text-transform:uppercase;color:{GREY}}}
h1{{font-size:clamp(38px,6vw,58px);font-weight:800;letter-spacing:-.038em;line-height:1.02;
  margin:28px 0 0;text-wrap:balance}}
.bajada{{font-size:21px;line-height:1.5;color:{GREY};margin:18px 0 0;max-width:60ch}}
.tira{{margin-top:38px;border-top:1px solid {INK};padding-top:20px;display:flex;
  gap:44px;flex-wrap:wrap}}
.tira div .et{{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:{GREY2}}}
.tira div .tx{{font-size:17px;color:{INK};margin-top:5px}}

section{{margin-top:64px}}
section .n{{font-size:11px;letter-spacing:.2em;color:{GREY2};font-variant-numeric:tabular-nums}}
section h2{{font-size:32px;font-weight:800;letter-spacing:-.03em;line-height:1.14;
  margin:10px 0 0;max-width:24ch}}
p{{font-size:19px;line-height:1.58;margin:18px 0 0;max-width:64ch}}
p.sub{{color:{GREY}}}
.cita{{margin-top:24px;border-left:2px solid {LINE};padding:4px 0 4px 20px}}
.cita .et{{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:{GREY2}}}
.cita .tx{{font-family:{SERIF};font-style:italic;font-size:19px;line-height:1.5;
  color:{GREY};margin-top:8px;max-width:62ch}}

.nums{{margin-top:30px;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:1px;background:{LINE};border:1px solid {LINE}}}
.nums div{{background:{PAPER};padding:20px 18px}}
.nums .v{{font-size:40px;font-weight:800;letter-spacing:-.04em;line-height:1;
  font-variant-numeric:tabular-nums}}
.nums .k{{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:{GREY};margin-top:10px}}

ol.pasos{{margin:26px 0 0;padding:0;list-style:none;counter-reset:p}}
ol.pasos li{{counter-increment:p;border-top:1px solid {LINE};padding:20px 0 20px 52px;
  position:relative;font-size:19px;line-height:1.55;max-width:66ch}}
ol.pasos li:before{{content:counter(p,decimal-leading-zero);position:absolute;left:0;top:22px;
  font-size:11px;letter-spacing:.16em;color:{GREY2};font-variant-numeric:tabular-nums}}
ol.pasos li b{{font-weight:800}}

.qa{{margin-top:26px}}
.qa .q{{border-top:1px solid {INK};padding-top:18px;margin-top:26px;font-size:21px;
  font-weight:800;letter-spacing:-.02em;max-width:52ch}}
.qa .a{{font-size:19px;line-height:1.58;color:{GREY};margin-top:12px;max-width:64ch}}
.qa .a b{{color:{INK};font-weight:800}}

.marco{{margin-top:30px;background:{DEEP};color:{PAPER2};padding:34px 32px}}
.marco .et{{font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:#8E8B85}}
.marco p{{color:{PAPER2};margin-top:14px}}
.marco b{{font-weight:800}}

.pie{{margin-top:90px;border-top:1px solid {INK};padding-top:22px;display:flex;
  justify-content:space-between;align-items:baseline;gap:20px;flex-wrap:wrap;
  font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:{GREY}}}
.sello{{width:30px;height:30px;border:1.5px solid {INK};display:inline-flex;
  align-items:center;justify-content:center;font-size:14px;font-weight:800}}

@media (max-width:640px){{
  .hoja{{padding:40px 20px 80px}} .tira{{gap:24px}}
  .nums .v{{font-size:32px}} ol.pasos li{{padding-left:40px}}
}}
@media print{{ body{{background:#fff}} section{{break-inside:avoid}} }}
"""

def S(n, t, cuerpo):
    return f'<section><div class="n">{n}</div><h2>{t}</h2>\n{cuerpo}\n</section>\n'

def P(t, cls=""):  return f'<p{" class=%s"%cls if cls else ""}>{t}</p>'
def CITA(et, t):   return f'<div class="cita"><div class="et">{et}</div><div class="tx">{t}</div></div>'
def NUMS(xs):      return '<div class="nums">' + "".join(
    f'<div><div class="v">{v}</div><div class="k">{k}</div></div>' for v,k in xs) + '</div>'
def PASOS(xs):     return '<ol class="pasos">' + "".join(f'<li>{x}</li>' for x in xs) + '</ol>'
def QA(xs):        return '<div class="qa">' + "".join(
    f'<div class="q">{q}</div><div class="a">{a}</div>' for q,a in xs) + '</div>'
def MARCO(et, t):  return f'<div class="marco"><div class="et">{et}</div><p>{t}</p></div>'


def TABLA(cols, filas):
    th = "".join(f'<th>{c}</th>' for c in cols)
    tr = "".join('<tr>'+''.join(f'<td>{c}</td>' for c in f)+'</tr>' for f in filas)
    return f'<div class="envoltorio"><table class="tb"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

CSS += """
.envoltorio{overflow-x:auto;margin-top:28px}
.tb{width:100%;border-collapse:collapse;font-size:17px;line-height:1.45}
.tb th{text-align:left;font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:#6A6A66;font-weight:400;padding:0 16px 12px 0;border-bottom:2px solid #171717;white-space:nowrap}
.tb td{padding:16px 16px 16px 0;border-bottom:1px solid #DBD7D2;vertical-align:top}
.tb td:first-child{white-space:nowrap;font-weight:800;font-variant-numeric:tabular-nums}
.tb b{font-weight:800}
@media (max-width:640px){ .tb{min-width:620px} }
"""

CSS += """
.meta{margin-top:26px;border-top:1px solid #171717;border-bottom:1px solid #DBD7D2;
  display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:#DBD7D2}
.meta > div{background:#ECEAE4;padding:16px 16px 16px 0}
.meta .et{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85}
.meta .tx{font-size:17px;line-height:1.4;margin-top:7px;max-width:30ch}
.bloq{margin-top:26px}
.bloq .q{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85;
  border-top:1px solid #DBD7D2;padding-top:16px;margin-top:22px}
.bloq .a{font-size:18.5px;line-height:1.58;margin-top:10px;max-width:64ch}
.bloq .a b{font-weight:800}
.carril{margin-top:30px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:#DBD7D2;border:1px solid #DBD7D2}
.carril > div{background:#ECEAE4;padding:22px 20px}
.carril .et{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8E8B85}
.carril .tt{font-size:22px;font-weight:800;letter-spacing:-.02em;margin-top:8px}
.carril .tx{font-size:17px;line-height:1.5;color:#6A6A66;margin-top:10px}
@media (max-width:640px){ .meta,.carril{grid-template-columns:1fr} .meta > div{padding-right:16px} }
"""

def META(qq, cuando, quien):
    return ('<div class="meta">'
            f'<div><div class="et">Qué queda hecho</div><div class="tx">{qq}</div></div>'
            f'<div><div class="et">Cuándo</div><div class="tx">{cuando}</div></div>'
            f'<div><div class="et">Quién</div><div class="tx">{quien}</div></div>'
            '</div>')

def BLOQ(xs):
    return '<div class="bloq">' + "".join(
        f'<div class="q">{q}</div><div class="a">{a}</div>' for q,a in xs) + '</div>'

def CARRIL(xs):
    return '<div class="carril">' + "".join(
        f'<div><div class="et">{e}</div><div class="tt">{t}</div><div class="tx">{x}</div></div>'
        for e,t,x in xs) + '</div>'
