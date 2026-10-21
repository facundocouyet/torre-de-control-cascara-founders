#!/usr/bin/env python3
"""Plazos de las cartas: cuánto dura cada una (en días hábiles) y cómo queda el roadmap de cada founder.

Regla (Facu, 21/10: la carta es cuestión de días; lo ideal son 2 o 3 cartas por semana):
  1. Duración en días hábiles según lo que hay que completar: 1 campo = 1 día, 2 o 3 = 2 días,
     4 o más (o más de 5 tareas) = 3 días. `PISO` fija a mano las que pidan otra cosa.
  2. Las tareas diarias o semanales son hábitos que siguen después de aprobada la carta:
     no estiran el deadline.
  3. La carta arranca un día hábil y su deadline es el último de sus días (ese día se manda a
     revisión). Revisión en el día: la siguiente arranca el día hábil después del deadline.
  4. Las en paralelo arrancan con la activa y no corren la fila.
  5. Ritmo objetivo: 2 a 3 cartas por semana. El resumen dice hasta cuándo alcanza la fila
     cargada y cuántas cartas faltan para cubrir hasta el día 90.

Se corre:  python3 generador/plazos.py          → escribe contenido/plazos.json y muestra el resumen
           python3 generador/plazos.py --probar  → solo muestra
"""
import json, os, sys, datetime as dt
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: json.load(open(os.path.join(B, *p), encoding="utf-8"))
HOY = dt.date.today()
# Facu, 21/10: días que fijó a mano. El 360 del negocio no es carta del founder: lo presenta Cáscara al cierre del mes 1.
PISO = {"auditoria-de-clientes": 3, "icp-mecanismo": 3, "one-sheeter-oferta": 3, "profile-funnel": 7,
        "angulos-desde-icp": 3, "calendario-contenido": 7}
FUERA = {"radiografia-360"}
RITMO = (2, 3)  # cartas por semana

inv = J("fichas", "inventario.json")
MOD = {m["id"]: m for c in inv["categorias"] for m in c["modulos"]}

def dias(cod):
    base = cod.split("--")[0]
    if cod in PISO: return PISO[cod]
    if base in PISO: return PISO[base]
    m = MOD.get(base, {})
    tareas = None
    p = os.path.join(B, "fichas", "plantillas", cod + ".json")
    if "--" in cod and os.path.exists(p):
        tareas = J("fichas", "plantillas", cod + ".json").get("tareas")
    tareas = tareas or m.get("tareas") or []
    n = len(m.get("completar") or [])
    if n >= 4 or len(tareas) > 5: return 3
    return 1 if n <= 1 else 2

def habil(d):
    while d.weekday() >= 5: d += dt.timedelta(days=1)
    return d
def sumar(d, n):  # n días hábiles después de d
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5: n -= 1
    return d
def habiles_entre(a, b):
    n, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        if d.weekday() < 5: n += 1
    return n
def f(d): return d.strftime("%d/%m")
def lista(v): return [v] if isinstance(v, str) else list(v or [])

app = {c["slug"]: c for c in J("contenido", "app-data.json")["clientes"]}
A = J("contenido", "asignaciones.json")["clientes"]

cartas = {}
for cid, m in MOD.items():
    if m.get("absorbida_en") or m.get("duplica") or cid in FUERA: continue
    cartas[cid] = {"nombre": m["nombre"], "nivel": m.get("nivel"), "dias": dias(cid)}

roadmaps = {}
for slug, a in A.items():
    if a.get("cerrar") or not a.get("activa"): continue
    c = app.get(slug, {})
    desde = c.get("desde") or a.get("inicio")   # sin ficha: la semana 1 de su primera carta (aprox. la Clarity Call)
    pausa = c.get("pausa") or 0
    fin90 = (dt.date.fromisoformat(desde) + dt.timedelta(days=89 + pausa)) if desde else None
    ini = habil(HOY)  # proyección desde hoy: la activa arranca hoy
    fila = [a["activa"]] + lista(a.get("siguiente")) + lista(a.get("despues"))
    out, cur = [], ini
    for i, cod in enumerate(fila):
        d = dias(cod); dead = sumar(cur, d - 1)
        out.append({"carta": cod, "estado": "activa" if i == 0 else "proxima", "dias": d,
                    "inicio": cur.isoformat(), "deadline": dead.isoformat()})
        cur = sumar(dead, 1)
    for cod in lista(a.get("en_paralelo")):
        d = dias(cod)
        out.append({"carta": cod, "estado": "paralelo", "dias": d, "inicio": ini.isoformat(),
                    "deadline": sumar(ini, d - 1).isoformat()})
    ultimo = max(dt.date.fromisoformat(x["deadline"]) for x in out)
    hab_rest = habiles_entre(HOY, fin90) if fin90 and fin90 > HOY else 0
    faltan = None
    if fin90 and fin90 > ultimo:
        sem = habiles_entre(ultimo, fin90) / 5
        faltan = (round(sem * RITMO[0]), round(sem * RITMO[1]))
    roadmaps[slug] = {"nombre": c.get("nombre", slug), "desde": desde, "dia": c.get("dia"),
                      "dia_90": fin90.isoformat() if fin90 else None,
                      "dias_restantes": (fin90 - HOY).days if fin90 else None, "habiles_restantes": hab_rest,
                      "fila_hasta": ultimo.isoformat(), "cartas_cargadas": len(out),
                      "faltan_cartas": faltan, "cartas": out}

tron = [x for x in inv["orden_sugerido"] if x in cartas and cartas[x]["nivel"] == "troncal"]
print("Troncales: %d cartas, %d días hábiles en fila (%s)" % (len(tron), sum(cartas[x]["dias"] for x in tron),
      ", ".join("%s %d" % (x, cartas[x]["dias"]) for x in tron)))
cnt = {}
for v in cartas.values(): cnt[v["dias"]] = cnt.get(v["dias"], 0) + 1
print("Cartas: %d · %s" % (len(cartas), " · ".join("%d de %d día(s)" % (cnt[k], k) for k in sorted(cnt))))
print()
for slug, r in sorted(roadmaps.items(), key=lambda kv: kv[1]["dias_restantes"] if kv[1]["dias_restantes"] is not None else 999):
    fz = r["faltan_cartas"]
    nota = ("pasó el día 90" if (r["dias_restantes"] or 0) < 0 else
            "faltan %d a %d cartas para llegar al día 90" % fz if fz else "la fila llega al día 90")
    print("%-22s quedan %-4s días (día 90 %s) · %d cartas cargadas, alcanzan hasta el %s · %s" % (
        slug, r["dias_restantes"], f(dt.date.fromisoformat(r["dia_90"])) if r["dia_90"] else "-",
        r["cartas_cargadas"], f(dt.date.fromisoformat(r["fila_hasta"])), nota))
    if "-v" in sys.argv:
        for x in r["cartas"]:
            print("     %-9s %-48s %d d  %s → %s" % (x["estado"], x["carta"], x["dias"],
                  f(dt.date.fromisoformat(x["inicio"])), f(dt.date.fromisoformat(x["deadline"]))))

if "--probar" not in sys.argv:
    json.dump({"actualizado": HOY.isoformat(), "regla": __doc__.strip().split("\n\n")[1], "ritmo_por_semana": RITMO,
               "cartas": cartas, "roadmaps": roadmaps},
              open(os.path.join(B, "contenido", "plazos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\nescrito contenido/plazos.json")
