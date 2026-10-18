# -*- coding: utf-8 -*-
"""Suma las cartas de operaciones al catálogo de la torre de control.

Se corre parado en la raíz del repo:  python3 sumar_operaciones.py
Lee operaciones/inventario-operaciones.json y operaciones/plantillas/*.json, y:
  - suma cada módulo a su categoría de fichas/inventario.json (si el id ya existe, lo reemplaza),
  - copia las plantillas a fichas/plantillas/,
  - agrega los ids nuevos al final de orden_sugerido.
No toca ninguna carta existente. Después: python3 generador/build_cartas.py
"""
import json, os, glob, shutil

RAIZ = os.path.dirname(os.path.abspath(__file__))
OPS = os.path.join(RAIZ, "operaciones")
inv_p = os.path.join(RAIZ, "fichas", "inventario.json")
inv = json.load(open(inv_p, encoding="utf-8"))
ops = json.load(open(os.path.join(OPS, "inventario-operaciones.json"), encoding="utf-8"))

cats = {c["nombre"]: c for c in inv["categorias"]}
nuevos = []
for bloque in ops["categorias"]:
    cat = cats.get(bloque["nombre"])
    if cat is None:
        cat = {"nombre": bloque["nombre"], "porque": bloque.get("porque", ""), "modulos": []}
        inv["categorias"].append(cat); cats[cat["nombre"]] = cat
    for m in bloque["modulos"]:
        cat["modulos"] = [x for x in cat["modulos"] if x["id"] != m["id"]] + [m]
        nuevos.append(m["id"])

orden = inv.get("orden_sugerido", [])
inv["orden_sugerido"] = orden + [i for i in nuevos if i not in orden]
open(inv_p, "w", encoding="utf-8").write(json.dumps(inv, ensure_ascii=False, indent=2) + "\n")

for f in glob.glob(os.path.join(OPS, "plantillas", "*.json")):
    shutil.copy(f, os.path.join(RAIZ, "fichas", "plantillas", os.path.basename(f)))

print("cartas de operaciones sumadas:", len(nuevos))
for i in nuevos: print("  ", i)
