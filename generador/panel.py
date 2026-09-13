# -*- coding: utf-8 -*-
import json, glob, html as _h, re, datetime
def esc(s): return _h.escape(str(s or ""))

FECHA = "12 de septiembre de 2026"
rows=[]
for f in sorted(glob.glob('fichas/*.json')):
    d=json.load(open(f,encoding='utf-8'))
    h=d.get('handicap')
    # accionables de Cáscara del tramo de septiembre
    casc=[]; cli=[]
    for a in d.get('accionables',[]):
        if a.get('cuando','').lower().startswith('sept'):
            casc = a.get('cascara',[]); cli = a.get('cliente',[])
    rows.append({
      "slug": d['slug'], "cliente": d['cliente'], "proyecto": d['proyecto'],
      "modo": d['modo'], "orientacion": d['orientacion'], "metrica": d['metrica'],
      "titular": d['titular'], "cuello": d['lectura']['titular'],
      "abierto": d.get('abierto',''), "doc": d['slug']+'.html',
      "handicap": h, "cascara": casc, "cliente_tareas": cli,
      "ultima": d['que_paso'][-1]['cuando'],
    })

import handicap as hk
rows.append({
  "slug":"qualita","cliente":"Qualita Studio · Rafa Lizarraga",
  "proyecto":"Qualita Studio — estudio de diseño y el programa con Digital House",
  "modo":"radiografia","orientacion":"Sostener",
  "metrica":"Leads que entran por el canal propio del método, para poder elegir mejor y subir el ticket.",
  "titular":"El método ya existe y está probado. Lo que falta es el canal propio que lo comunique.",
  "cuello":"El canal propio de venta del mecanismo todavía no está formado.",
  "abierto":"Cuánto dura el programa con Digital House, que es lo que destraba la decisión del downsell (falta confirmar).",
  "doc":"qualita.html","handicap":hk.calcular("qualita"),
  "cascara":[],"cliente_tareas":[],"ultima":"11 de septiembre de 2026"})

rows.append({
  "slug":"cecilia-belotti","cliente":"Cecilia Belotti","proyecto":"Consultoría de turismo — propuesta para Tantasiña",
  "modo":"cierre","orientacion":"Conseguir","metrica":"(documento hecho aparte)",
  "titular":"Sign off en curso. Le quedó revisar el copy de la landing y la propuesta para Olga.",
  "cuello":"(sin handicap: el caso se trabajó aparte y no hay datos suficientes para puntuarlo)",
  "abierto":"","doc":"","handicap":None,"cascara":[],"cliente_tareas":[],
  "ultima":"2 de septiembre de 2026"})

orden = {"Arranque":0,"En construcción":1,"Andando":2,"Listo para cerrar":3}
rows.sort(key=lambda r: (r['handicap']['total'] if r['handicap'] else 99, r['cliente']))
json.dump(rows, open('panel-data.json','w',encoding='utf-8'), ensure_ascii=False)
print("filas:", len(rows))
