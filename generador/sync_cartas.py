# -*- coding: utf-8 -*-
"""Sube las cartas del repo a la app de clientes (Supabase). El repo es la fuente: la app solo lee.

  python3 generador/sync_cartas.py            con SUPABASE_URL y SUPABASE_SERVICE_KEY: sincroniza
  python3 generador/sync_cartas.py --probar   sin tocar nada: muestra lo que haría

Qué hace:
  1. Cada módulo de fichas/inventario.json → una fila de `cartas` (upsert por `codigo`, origen 'repo').
     No manda `evidencia` ni `estado`, que son internos.
  2. Sus `carta_tareas` se reemplazan con los "completar" del módulo, en la semana 1.
  3. Cada carta escrita para un cliente (fichas/plantillas/<modulo>--<slug>.json) → otra fila de
     `cartas` con código <modulo>--<slug>, oculta en la galería y ligada a ese cliente, para que al
     asignarla la app use esa versión y no la genérica.
  4. Una carta de origen 'repo' que ya no está en el repo se marca oculta. No se borra nunca.
  5. Las cartas de origen 'app' no se tocan.

Las columnas extra (cliente_slug, variante_de, url) necesitan existir en `cartas`. Si Supabase las
rechaza, el script sube igual sin ellas y avisa qué columnas faltan agregar.
Sin dependencias: Python 3 pelado, como el resto del generador."""
import json, os, sys, glob, datetime, urllib.request, urllib.error, urllib.parse

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = "https://facundocouyet.github.io/torre-de-control-cascara-founders"
EXTRA = ("cliente_slug", "variante_de", "url")
PROBAR = "--probar" in sys.argv or not (os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_KEY"))

def leer(p): return json.load(open(p, encoding="utf-8"))

def filas_del_repo():
    inv = leer(os.path.join(B, "fichas", "inventario.json"))
    ahora = datetime.datetime.utcnow().isoformat() + "Z"
    cartas, tareas, base = [], {}, {}
    for cat in inv["categorias"]:
        for m in cat["modulos"]:
            base[m["id"]] = (m, cat["nombre"])
            cartas.append({
                "codigo": m["id"], "nombre": m["nombre"], "categoria": cat["nombre"],
                "nivel": m.get("nivel"), "para_quien": m.get("para_quien", ""),
                "resultado": m.get("resultado", ""), "pasos": m.get("pasos", []),
                "herramientas": m.get("herramientas", []), "origen": "repo", "oculta": False,
                "actualizada": ahora,
                "cliente_slug": None, "variante_de": None, "url": "%s/cartas/%s.html" % (PAGES, m["id"]),
            })
            tareas[m["id"]] = [{"orden": i + 1, "semana": 1, "titulo": t, "descripcion": ""}
                               for i, t in enumerate(m.get("completar", []))]
    # las cartas escritas para un cliente
    for f in sorted(glob.glob(os.path.join(B, "fichas", "plantillas", "*--*.json"))):
        v = leer(f)
        mod, slug = os.path.basename(f)[:-5].split("--", 1)
        if mod not in base:
            print("  ojo: %s es versión de un módulo que no está en el inventario" % os.path.basename(f)); continue
        m, cat = base[mod]
        cod = "%s--%s" % (mod, slug)
        cartas.append({
            "codigo": cod, "nombre": v.get("nombre") or m["nombre"], "categoria": cat,
            "nivel": m.get("nivel"), "para_quien": v.get("founder", ""),
            "resultado": v.get("bajada") or m.get("resultado", ""),
            "pasos": v.get("pasos") or m.get("pasos", []), "herramientas": m.get("herramientas", []),
            "origen": "repo", "oculta": True, "actualizada": ahora,
            "cliente_slug": slug, "variante_de": mod,
            "url": "%s/cartas/para/%s-%s.html" % (PAGES, slug, mod),
        })
        tareas[cod] = [{"orden": i + 1, "semana": 1, "titulo": t, "descripcion": ""}
                       for i, t in enumerate(v.get("completar") or m.get("completar", []))]
    return cartas, tareas

# ---------------- Supabase (PostgREST) ----------------
def pedir(metodo, ruta, cuerpo=None, prefer=None):
    url = os.environ["SUPABASE_URL"].rstrip("/") + "/rest/v1/" + ruta
    k = os.environ["SUPABASE_SERVICE_KEY"]
    h = {"apikey": k, "Authorization": "Bearer " + k, "Content-Type": "application/json"}
    if prefer: h["Prefer"] = prefer
    data = json.dumps(cuerpo).encode() if cuerpo is not None else None
    req = urllib.request.Request(url, data=data, headers=h, method=metodo)
    try:
        with urllib.request.urlopen(req) as r:
            t = r.read().decode()
            return json.loads(t) if t else None
    except urllib.error.HTTPError as e:
        raise RuntimeError("%s %s → %s %s" % (metodo, ruta, e.code, e.read().decode()[:400]))

def subir(cartas):
    try:
        return pedir("POST", "cartas?on_conflict=codigo", cartas,
                     "resolution=merge-duplicates,return=representation"), []
    except RuntimeError as e:
        if not any(c in str(e) for c in EXTRA): raise
        faltan = [c for c in EXTRA if c in str(e)] or list(EXTRA)
        sin = [{k: v for k, v in c.items() if k not in EXTRA} for c in cartas]
        return pedir("POST", "cartas?on_conflict=codigo", sin,
                     "resolution=merge-duplicates,return=representation"), faltan

def main():
    cartas, tareas = filas_del_repo()
    gen = [c for c in cartas if not c["cliente_slug"]]
    ver = [c for c in cartas if c["cliente_slug"]]
    print("→ %d cartas genéricas y %d escritas para un cliente" % (len(gen), len(ver)))
    if PROBAR:
        from collections import Counter
        print("   niveles:", dict(Counter(c["nivel"] for c in gen)))
        for c in ver: print("   %-45s → %s" % (c["codigo"], c["cliente_slug"]))
        print("   modo prueba: no se tocó Supabase (faltan SUPABASE_URL y SUPABASE_SERVICE_KEY, o se pidió --probar)")
        return
    filas, faltan = subir(cartas)
    ids = {f["codigo"]: f["id"] for f in filas}
    for cod, ts in tareas.items():
        cid = ids.get(cod)
        if not cid: continue
        pedir("DELETE", "carta_tareas?carta_id=eq.%s" % urllib.parse.quote(str(cid)))
        if ts: pedir("POST", "carta_tareas", [dict(t, carta_id=cid) for t in ts])
    # lo que ya no está en el repo se oculta, nunca se borra
    en_base = pedir("GET", "cartas?origen=eq.repo&select=id,codigo,oculta") or []
    del_repo = {c["codigo"] for c in cartas}
    viejas = [c for c in en_base if c["codigo"] not in del_repo and not c["oculta"]]
    for c in viejas:
        pedir("PATCH", "cartas?id=eq.%s" % urllib.parse.quote(str(c["id"])), {"oculta": True})
    print("   subidas %d, tareas reemplazadas en %d, ocultadas %d" % (len(filas), len(tareas), len(viejas)))
    if faltan:
        print("   OJO: la tabla cartas no tiene %s. Subió igual, pero las versiones de cada cliente "
              "no quedan ligadas hasta que Teo agregue esas columnas." % ", ".join(faltan))

if __name__ == "__main__":
    main()
