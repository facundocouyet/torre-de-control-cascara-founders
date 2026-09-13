# -*- coding: utf-8 -*-
"""App de Cáscara Founders. Escritorio primero, monocromo, rojo racionado."""
import json, os, collections, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import dias as DI
import handicap as HK   # el registro manda sobre cualquier copia guardada
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # la raíz del repo
panel=json.load(open(B+'/contenido/panel-data.json',encoding='utf-8'))
prog=json.load(open(B+'/contenido/programa.json',encoding='utf-8'))
mat=json.load(open(B+'/contenido/materiales.json',encoding='utf-8'))
# los módulos salen del inventario con las tres capas (pasos, qué completar, qué herramientas),
# que es lo que distingue un módulo de un SOP
inv=json.load(open(B+'/contenido/modulos-inventario.json',encoding='utf-8'))
import glob

FECHA="13 SEP 2026"
EJES=[("oferta","Oferta"),("contenido","Contenido"),("demanda","Demanda"),("venta","Venta"),("entrega","Entrega")]
DUENOS=["Facu","Franco","Teo","Juana","Fede"]
RITMO={"verde":"al día","amarillo":"a los tirones","rojo":"frenado"}
# escala del handicap: cada eje se muestra del 1 al 100, como las habilidades de un piloto
def cien(n): return n*20+10
COMO_SUBE={
 "oferta":"Sube cuando la oferta queda escrita con precio y avatar, y salta cuando alguien la compra a ese precio.",
 "contenido":"Sube cuando hay cadencia con ángulos definidos, y salta cuando la audiencia valida uno.",
 "demanda":"Sube cuando entran conversaciones sin empujar, y salta cuando hay un canal propio y medible.",
 "venta":"Sube cuando hay un proceso de cierre que se repite, y salta cuando el precio se sostiene sin negociar.",
 "entrega":"Sube cuando el proceso es repetible, y salta cuando además está delegado.",
}

# las fichas v2 mandan sobre el panel viejo: de ahí salen el cuello, el titular,
# la métrica y la etapa, ya escritos sin negaciones
V2={}
for g in glob.glob(B+'/fichas/*.json'):
    v=json.load(open(g,encoding='utf-8')); V2[v['slug']]=v

clientes=[]
for r in panel:
    v=V2.get(r['slug'])
    if v:
        r=dict(r)
        r['cuello']=(v.get('lectura') or {}).get('titular') or r['cuello']
        r['titular']=v.get('titular') or r['titular']
        r['metrica']=v.get('metrica') or r['metrica']
        r['etapa']=v.get('etapa','')
    h=HK.calcular(r['slug']) or r['handicap']
    dd=DI.calcular(r['slug'],[])
    clientes.append({
      "slug":r['slug'],"nombre":r['cliente'],"proyecto":r['proyecto'],
      "ori":r['orientacion'],"modo":r['modo'],"cuello":r['cuello'],
      "metrica":r['metrica'],"abierto":r['abierto'],"doc":r['doc'],
      "etapa":r.get('etapa',''),
      "ultima":r['ultima'],"titular":r['titular'],
      "ct":r['cliente_tareas'],"cas":r['cascara'],
      "dia":dd['d'],"desde":dd['desde'],"fuente":dd['fuente'],
      "h": None if not h else {"t":h['total'],"tr":h['tramo'],"ri":h['ritmo'],
             "rt":RITMO[h['ritmo']],
             "ej":[h['ejes'][k] for k,_ in EJES],
             "e1":[cien(h['ejes'][k]) for k,_ in EJES],
             "g":round(sum(cien(h['ejes'][k]) for k,_ in EJES)/5),
             "flo":[[k for k,_ in EJES].index(x) for x in h['eje_flojo']],
             "sube":COMO_SUBE.get(h['eje_flojo'][0],"") if h['eje_flojo'] else "",
             "nota":h['nota'],"sug":h['sugiere']}})

tareas=collections.OrderedDict((d,[]) for d in DUENOS); tareas["Equipo"]=[]
for c in clientes:
    for t in c['cas']:
        d=next((x for x in DUENOS if t.startswith(x)),"Equipo")
        tareas[d].append({"c":c['nombre'],"slug":c['slug'],"t":t})

DATA={"fecha":FECHA,"ejes":[n for _,n in EJES],
 "ejes_def":[{"n":x['nombre'],"q":x['que_mide']} for x in prog['handicap']['ejes']],
 "clientes":clientes,"tareas":[{"d":d,"items":v} for d,v in tareas.items() if v],
 "proceso":[{"n":x['n'],"c":x['cuando'],"t":x['titulo'],"x":x['texto']} for x in prog['proceso']],
 "orientaciones":[{"n":o['nombre'],"l":o['lider'],"x":o['texto'],"m":o['modulos']} for o in prog['orientaciones']],
 "grupales":[{"n":g['nombre'],"q":g['quien'],"c":g['cuando'],"x":g['texto']} for g in prog['grupales']],
 "mentores":[{"n":m['nombre'],"r":m['rol'],"si":m['que_traerle'],"no":m['que_no']} for m in prog['mentores']],
 "bloques":[{"n":b['nombre'],"piezas":[{"t":p['titulo'],"q":p['que_es'],"e":p.get('estado',''),
             "f":p.get('formatos',[]),"u":p.get('url','')} for p in b['piezas']]} for b in mat['bloques']],
 "modulos":[{"c":c['nombre'],"porque":c.get('porque',''),
     "items":[{"t":i['nombre'],"x":i['resultado'],"e":i.get('estado',''),
               "q":i.get('para_quien',''),
               "p":i.get('pasos',[]),"cc":i.get('completar',[]),"hh":i.get('herramientas',[])}
              for i in c['modulos']]} for c in inv['categorias']],
 "decisiones":[{"t":x['titulo'],"x":x['texto']} for x in mat['decisiones']],
 "falta":mat['falta']}
J=json.dumps(DATA,ensure_ascii=False,separators=(',',':'))
open(B+'/contenido/app-data.json','w',encoding='utf-8').write(J)
print("clientes:",len(clientes),"· datos:",len(J))
