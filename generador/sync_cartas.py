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
  6. Las tareas salen de `tareas` (titulo, semana, frecuencia, descripcion) si el módulo o la versión
     las tiene; si no, de `completar`, todas en la semana 1 y únicas.
  7. `estado_galeria` (aprobada / rehacer / obsoleta) viaja con cada carta genérica.
  8. contenido/asignaciones.json → la carta activa (con `inicio`, el lunes de la semana 1) y la
     siguiente (fila con estado 'proxima') de cada cliente. Solo corre cuando ese archivo dice
     "activar": true. Si el cliente tiene versión propia de esa carta, se asigna la versión.

Las columnas extra (cliente_slug, variante_de, url) necesitan existir en `cartas`. Si Supabase las
rechaza, el script sube igual sin ellas y avisa qué columnas faltan agregar.
Sin dependencias: Python 3 pelado, como el resto del generador."""
import json, os, sys, glob, datetime, urllib.request, urllib.error, urllib.parse

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = "https://facundocouyet.github.io/torre-de-control-cascara-founders"
EXTRA = ("cliente_slug", "variante_de", "url", "estado_galeria")
TAREA_EXTRA = ("frecuencia", "descripcion")
FRECUENCIAS = ("unica", "diaria", "semanal", "mensual")
PROBAR = "--probar" in sys.argv or not (os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_KEY"))

def leer(p): return json.load(open(p, encoding="utf-8"))

def tareas_de(fuente, respaldo=None):
    """Las tareas de una carta: `tareas` con semana y frecuencia, o `completar` en la semana 1."""
    ts = fuente.get("tareas") or (respaldo or {}).get("tareas")
    if ts:
        out = []
        for i, t in enumerate(ts):
            f = (t.get("frecuencia") or "unica").lower()
            if f not in FRECUENCIAS:
                print("  ojo: frecuencia '%s' no válida en %s; va como unica" % (f, t.get("titulo"))); f = "unica"
            out.append({"orden": i + 1, "semana": int(t.get("semana") or 1), "titulo": t["titulo"],
                        "descripcion": t.get("descripcion", ""), "frecuencia": f})
        return out
    comp = fuente.get("completar") or (respaldo or {}).get("completar", [])
    return [{"orden": i + 1, "semana": 1, "titulo": t, "descripcion": "", "frecuencia": "unica"}
            for i, t in enumerate(comp)]

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
                "estado_galeria": m.get("estado_galeria") or "aprobada",
            })
            tareas[m["id"]] = tareas_de(m)
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
            "estado_galeria": v.get("estado_galeria") or "aprobada",
        })
        tareas[cod] = tareas_de(v, m)
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

def subir_tareas(filas):
    """Sube las tareas; si la base no tiene frecuencia o descripcion, reintenta sin esas columnas."""
    try:
        pedir("POST", "carta_tareas", filas); return []
    except RuntimeError as e:
        faltan = [c for c in TAREA_EXTRA if c in str(e)]
        if not faltan: raise
        pedir("POST", "carta_tareas", [{k: v for k, v in f.items() if k not in faltan} for f in filas])
        return faltan

def lunes_semana_1(a, x):
    """El lunes de la semana 1: el que diga el cliente, el del archivo, o el próximo lunes (hoy si es lunes)."""
    f = x.get("inicio") or a.get("inicio")
    if f: return f
    hoy = datetime.date.today()
    return (hoy + datetime.timedelta(days=(7 - hoy.weekday()) % 7)).isoformat()

def asignar(ids):
    """Carta activa y siguiente por cliente desde contenido/asignaciones.json. No corre hasta que diga activar.

    Lo que hace la base sola (Teo, 3/10): al insertar una activa crea las tareas del cliente desde
    carta_tareas (por eso asignada_por va null) y pasa la activa anterior a 'pausada'. Si la anterior
    se da por terminada, el archivo dice "anterior": "completada" (en el cliente o arriba de todo) y
    se marca así antes de insertar la nueva. La siguiente va como otra fila con estado 'proxima'."""
    p = os.path.join(B, "contenido", "asignaciones.json")
    if not os.path.exists(p): return
    a = leer(p)
    lista = a.get("clientes", {})
    if not a.get("activar"):
        print("→ asignaciones: %d clientes escritos, sin activar (\"activar\": false)" % len(lista))
        return
    col = a.get("columnas", {})
    c_cli, c_car, c_est = col.get("cliente", "cliente_id"), col.get("carta", "carta_id"), col.get("estado", "estado")
    c_ini, c_por = col.get("inicio", "inicio"), col.get("asignada_por", "asignada_por")
    activa, proxima, completada = col.get("activa", "activa"), col.get("proxima", "proxima"), col.get("completada", "completada")
    clientes = {c["slug"]: c["id"] for c in (pedir("GET", "clientes?select=id,slug") or []) if c.get("slug")}
    def carta_de(cod, slug):
        return ids.get("%s--%s" % (cod, slug)) or ids.get(cod)
    def filas(cid, estado):
        q = "asignaciones?%s=eq.%s&%s=eq.%s&select=id,%s" % (c_cli, urllib.parse.quote(str(cid)), c_est, estado, c_car)
        return pedir("GET", q) or []
    def borrar(fid):
        pedir("DELETE", "asignaciones?id=eq.%s" % urllib.parse.quote(str(fid)))
    hechas = sig = 0
    for slug, x in lista.items():
        if x.get("cerrar"):
            # sign off: la activa pasa a completada y se saca la próxima
            cid = clientes.get(slug)
            if cid:
                for v in filas(cid, activa):
                    pedir("PATCH", "asignaciones?id=eq.%s" % urllib.parse.quote(str(v["id"])), {c_est: completada})
                for v in filas(cid, proxima): borrar(v["id"])
                print("  cierra %s: activa a completada, sin próxima" % slug)
            continue
        cod = x.get("activa")
        if not cod: continue
        cid = clientes.get(slug)
        if not cid:
            print("  ojo: %s no está en clientes de la app; no se asigna" % slug); continue
        carta = carta_de(cod, slug)
        if not carta:
            print("  ojo: la carta %s no existe; %s queda sin asignar" % (cod, slug)); continue
        vigentes = filas(cid, activa)
        if not any(str(v.get(c_car)) == str(carta) for v in vigentes):
            if (x.get("anterior") or a.get("anterior")) == completada:
                for v in vigentes:
                    pedir("PATCH", "asignaciones?id=eq.%s" % urllib.parse.quote(str(v["id"])), {c_est: completada})
            # si la nueva activa estaba como próxima, esa fila se saca: la activa entra por insert
            for v in filas(cid, proxima):
                if str(v.get(c_car)) == str(carta): borrar(v["id"])
            pedir("POST", "asignaciones", {c_cli: cid, c_car: carta, c_est: activa,
                                           c_ini: lunes_semana_1(a, x), c_por: None})
            hechas += 1
        # la siguiente: una sola fila 'proxima' por cliente
        cod_s = x.get("siguiente")
        carta_s = carta_de(cod_s, slug) if cod_s else None
        if cod_s and not carta_s:
            print("  ojo: la carta siguiente %s no existe para %s" % (cod_s, slug))
        prox = filas(cid, proxima)
        if carta_s and any(str(v.get(c_car)) == str(carta_s) for v in prox): continue
        for v in prox: borrar(v["id"])
        if carta_s:
            pedir("POST", "asignaciones", {c_cli: cid, c_car: carta_s, c_est: proxima, c_por: None})
            sig += 1
    print("→ asignaciones: %d activas nuevas o cambiadas, %d siguientes" % (hechas, sig))

def main():
    cartas, tareas = filas_del_repo()
    gen = [c for c in cartas if not c["cliente_slug"]]
    ver = [c for c in cartas if c["cliente_slug"]]
    print("→ %d cartas genéricas y %d escritas para un cliente" % (len(gen), len(ver)))
    if PROBAR:
        from collections import Counter
        print("   niveles:", dict(Counter(c["nivel"] for c in gen)))
        for c in ver: print("   %-45s → %s" % (c["codigo"], c["cliente_slug"]))
        con_sem = sum(1 for ts in tareas.values() if any(t["semana"] > 1 or t["frecuencia"] != "unica" for t in ts))
        print("   cartas con tareas por semana o frecuencia:", con_sem)
        print("   estados de galería:", dict(Counter(c["estado_galeria"] for c in gen)))
        p = os.path.join(B, "contenido", "asignaciones.json")
        if os.path.exists(p):
            a = leer(p); cods = {c["codigo"] for c in cartas}
            for slug, x in a.get("clientes", {}).items():
                if x.get("cerrar"):
                    print("   cierra %-22s → activa a completada, sin próxima" % slug); continue
                cod = x.get("activa")
                if not cod: continue
                pars = x.get("en_paralelo") or []
                for par in ([pars] if isinstance(pars, str) else pars):
                    print("   en paralelo %-16s → %s (no entra a la app: va por su canal)" % (slug, par))
                usa = "%s--%s" % (cod, slug) if "%s--%s" % (cod, slug) in cods else cod
                sg = x.get("siguiente") or ""
                usa_s = ("%s--%s" % (sg, slug) if "%s--%s" % (sg, slug) in cods else sg) if sg else "-"
                print("   asigna %-22s → %s%s · desde %s · sigue %s%s" % (
                    slug, usa, "" if usa in cods else " (NO EXISTE)", lunes_semana_1(a, x),
                    usa_s, "" if (not sg or usa_s in cods) else " (NO EXISTE)"))
        print("   modo prueba: no se tocó Supabase (faltan SUPABASE_URL y SUPABASE_SERVICE_KEY, o se pidió --probar)")
        return
    filas, faltan = subir(cartas)
    ids = {f["codigo"]: f["id"] for f in filas}
    for cod, ts in tareas.items():
        cid = ids.get(cod)
        if not cid: continue
        pedir("DELETE", "carta_tareas?carta_id=eq.%s" % urllib.parse.quote(str(cid)))
        if ts:
            for c in subir_tareas([dict(t, carta_id=cid) for t in ts]):
                if c not in faltan: faltan.append(c)
    # lo que ya no está en el repo se oculta, nunca se borra
    en_base = pedir("GET", "cartas?origen=eq.repo&select=id,codigo,oculta") or []
    del_repo = {c["codigo"] for c in cartas}
    viejas = [c for c in en_base if c["codigo"] not in del_repo and not c["oculta"]]
    for c in viejas:
        pedir("PATCH", "cartas?id=eq.%s" % urllib.parse.quote(str(c["id"])), {"oculta": True})
    print("   subidas %d, tareas reemplazadas en %d, ocultadas %d" % (len(filas), len(tareas), len(viejas)))
    asignar(ids)
    if faltan:
        print("   OJO: la base no tiene las columnas %s. Subió igual sin ellas; hay que pedirle a Teo "
              "que las agregue." % ", ".join(faltan))

if __name__ == "__main__":
    main()
