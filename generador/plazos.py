#!/usr/bin/env python3
"""Plazos de las cartas: cuánto dura cada una y cómo queda el roadmap de cada founder en sus 90 días.

Regla de duración (en semanas):
  1. Si la carta (o la versión del founder) tiene `tareas`, dura lo que marca la semana más alta.
  2. Si no, sale de lo que hay que completar: 1 campo = 1 semana, 2 o 3 = 2 semanas, 4 o más = 3.
  3. `PISO` fija a mano las que pidan otra cosa (vacío por ahora).
Cada carta arranca un lunes y su deadline es el viernes de su última semana (ese día se manda a
revisión). La revisión entra entre el viernes y el lunes: la siguiente arranca el lunes siguiente.
Las cartas en paralelo arrancan con la activa y no corren la fila.

Se corre:  python3 generador/plazos.py          → escribe contenido/plazos.json y muestra el resumen
           python3 generador/plazos.py --probar  → solo muestra
"""
import json, os, sys, datetime as dt
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: json.load(open(os.path.join(B, *p), encoding="utf-8"))
HOY = dt.date.today()
PISO = {}

inv = J("fichas", "inventario.json")
MOD = {m["id"]: m for c in inv["categorias"] for m in c["modulos"]}

def semanas(cod):
    base = cod.split("--")[0]
    m = MOD.get(base, {})
    tareas = None
    p = os.path.join(B, "fichas", "plantillas", cod + ".json")
    if "--" in cod and os.path.exists(p):
        tareas = J("fichas", "plantillas", cod + ".json").get("tareas")
    tareas = tareas or m.get("tareas")
    if cod in PISO: return PISO[cod], "a mano"
    if base in PISO: return PISO[base], "a mano"
    if tareas: return max(int(t.get("semana") or 1) for t in tareas), "tareas"
    n = len(m.get("completar") or [])
    return (1 if n <= 1 else 2 if n <= 3 else 3), "estimada"

def lunes(d): return d - dt.timedelta(days=d.weekday())
def f(d): return d.strftime("%d/%m")

app = {c["slug"]: c for c in J("contenido", "app-data.json")["clientes"]}
A = J("contenido", "asignaciones.json")["clientes"]

def lista(v): return [v] if isinstance(v, str) else list(v or [])

# 1. Duración de cada carta
cartas = {}
for cid, m in MOD.items():
    if m.get("absorbida_en") or m.get("duplica"): continue
    s, fuente = semanas(cid)
    cartas[cid] = {"nombre": m["nombre"], "nivel": m.get("nivel"), "semanas": s, "fuente": fuente}

# 2. Roadmap de cada founder
roadmaps = {}
for slug, a in A.items():
    if a.get("cerrar") or not a.get("activa"): continue
    c = app.get(slug, {})
    desde = c.get("desde") or a.get("inicio")   # sin ficha: la semana 1 de su primera carta (aprox. la Clarity Call)
    pausa = c.get("pausa") or 0
    fin90 = (dt.date.fromisoformat(desde) + dt.timedelta(days=89 + pausa)) if desde else None
    ini = lunes(dt.date.fromisoformat(a["inicio"])) if a.get("inicio") else lunes(HOY)
    fila = [a["activa"]] + lista(a.get("siguiente")) + lista(a.get("despues"))
    out = []
    cur = ini
    for i, cod in enumerate(fila):
        s, fu = semanas(cod)
        dead = cur + dt.timedelta(days=7 * (s - 1) + 4)
        out.append({"carta": cod, "estado": "activa" if i == 0 else "proxima", "semanas": s, "fuente": fu,
                    "inicio": cur.isoformat(), "deadline": dead.isoformat()})
        cur = cur + dt.timedelta(days=7 * s)
    for cod in lista(a.get("en_paralelo")):
        s, fu = semanas(cod)
        out.append({"carta": cod, "estado": "paralelo", "semanas": s, "fuente": fu, "inicio": ini.isoformat(),
                    "deadline": (ini + dt.timedelta(days=7 * (s - 1) + 4)).isoformat()})
    ultimo = max(dt.date.fromisoformat(x["deadline"]) for x in out)
    roadmaps[slug] = {"nombre": c.get("nombre", slug), "desde": desde, "dia": c.get("dia"),
                      "dia_90": fin90.isoformat() if fin90 else None,
                      "dias_restantes": (fin90 - HOY).days if fin90 else None,
                      "ultimo_deadline": ultimo.isoformat(),
                      "margen": (fin90 - ultimo).days if fin90 else None, "cartas": out}

# 3. Resumen
tron = [x for x in inv["orden_sugerido"] if x in cartas and cartas[x]["nivel"] == "troncal"]
print("Troncales en fila: %d semanas (%s)" % (sum(cartas[x]["semanas"] for x in tron),
      ", ".join("%s %d" % (x, cartas[x]["semanas"]) for x in tron)))
cnt = {}
for v in cartas.values(): cnt[v["fuente"]] = cnt.get(v["fuente"], 0) + 1
print("Cartas: %d · por tareas %d · estimadas %d" % (len(cartas), cnt.get("tareas", 0), cnt.get("estimada", 0)))
print()
for slug, r in sorted(roadmaps.items(), key=lambda kv: (kv[1]["margen"] is None, kv[1]["margen"] if kv[1]["margen"] is not None else 0)):
    m = r["margen"]
    estado = "sin fecha de inicio" if m is None else ("entra, sobran %d días" % m if m >= 0 else "SE PASA %d días" % -m)
    print("%-22s día %-4s quedan %-4s día 90 %-6s última entrega %-6s %s" % (
        slug, r["dia"] or "-", r["dias_restantes"] if r["dias_restantes"] is not None else "-",
        f(dt.date.fromisoformat(r["dia_90"])) if r["dia_90"] else "-", f(dt.date.fromisoformat(r["ultimo_deadline"])), estado))
    for x in r["cartas"]:
        print("     %-9s %-48s %d sem  %s → %s%s" % (x["estado"], x["carta"], x["semanas"], f(dt.date.fromisoformat(x["inicio"])),
              f(dt.date.fromisoformat(x["deadline"])), "" if x["fuente"] == "tareas" else "  (estimada)"))

if "--probar" not in sys.argv:
    json.dump({"actualizado": HOY.isoformat(), "regla": __doc__.strip().split("\n\n")[1], "cartas": cartas, "roadmaps": roadmaps},
              open(os.path.join(B, "contenido", "plazos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\nescrito contenido/plazos.json")
