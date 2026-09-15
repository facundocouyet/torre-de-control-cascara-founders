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

