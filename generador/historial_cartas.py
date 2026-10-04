#!/usr/bin/env python3
"""Arma fichas/plantillas/HISTORIAL.md: por cada carta genérica, cómo se usa, cómo se personaliza,
quién la tiene en versión propia y sus últimos cambios (del git log de la plantilla y de sus variantes).

Lo de uso y personalización vive en fichas/plantillas/_uso.json y se escribe a mano (Facu o el agente,
cuando Facu marca un criterio). Lo demás sale solo. Se corre en cada corrida, después de tocar cartas.
"""
import glob, json, os, subprocess
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PL = os.path.join(B, "fichas", "plantillas")

def log(paths, n=5):
    try:
        out = subprocess.run(["git", "-C", B, "log", "--format=%h|%ad|%s", "--date=short", "-n", str(n), "--"] + paths,
                             capture_output=True, text=True).stdout
    except Exception:
        return []
    return [l.split("|", 2) for l in out.strip().splitlines() if l.count("|") >= 2]

inv = json.load(open(os.path.join(B, "fichas", "inventario.json"), encoding="utf-8"))
uso = json.load(open(os.path.join(PL, "_uso.json"), encoding="utf-8")) if os.path.exists(os.path.join(PL, "_uso.json")) else {}
var = {}
for f in glob.glob(os.path.join(PL, "*--*.json")):
    mod, slug = os.path.basename(f)[:-5].split("--", 1)
    d = json.load(open(f, encoding="utf-8"))
    var.setdefault(mod, []).append((slug, "propia" if d.get("secciones") else "liviana", os.path.relpath(f, B)))

out = ["# Historial de las cartas", "",
       "> Se arma solo con `python3 generador/historial_cartas.py`. Lo de uso y personalización sale de `fichas/plantillas/_uso.json`.",
       "> Regla: la genérica es la base. La versión de cada founder es **liviana** (solo `bajada_envio`, `ajustes` por `cid` y bloques nuestros) y hereda todo lo demás, así un cambio en la genérica le llega a todos. Una versión **propia** (con `secciones`) solo cuando el formulario tiene que ser otro, y lleva `por_que_propia`.", ""]
for c in inv["categorias"]:
    for m in c["modulos"]:
        mid = m["id"]
        if not os.path.exists(os.path.join(PL, mid + ".json")): continue
        u = uso.get(mid, {})
        out += ["## %s · `%s`" % (m["nombre"], mid), ""]
        out.append("- **Cuándo va:** %s" % (u.get("cuando") or m.get("para_quien", "")))
        if u.get("personalizar"): out.append("- **Cómo se personaliza:** %s" % u["personalizar"])
        if u.get("ojo"): out.append("- **Ojo:** %s" % u["ojo"])
        vs = sorted(var.get(mid, []))
        if vs: out.append("- **Versiones:** " + ", ".join("%s (%s)" % (s, t) for s, t, _ in vs))
        paths = [os.path.join("fichas", "plantillas", mid + ".json")] + [p for _, _, p in vs]
        cambios = log(paths)
        if cambios:
            out.append("- **Últimos cambios:**")
            out += ["  - %s · %s (`%s`)" % (d, s, h) for h, d, s in cambios]
        out.append("")
open(os.path.join(PL, "HISTORIAL.md"), "w", encoding="utf-8").write("\n".join(out))
print("historial: %d cartas, %d versiones por founder" % (sum(1 for l in out if l.startswith("## ")), sum(len(v) for v in var.values())))
