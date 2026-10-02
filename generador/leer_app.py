# -*- coding: utf-8 -*-
"""Baja lo que pasa en la app de clientes (Supabase) a archivos JSON, para que el Claude de Facu lo lea.

  python3 generador/leer_app.py salida/      con SUPABASE_URL y SUPABASE_SERVICE_KEY

Solo lee. Corre en la Action "Leer la app" y el resultado va a la rama `app-datos`, nunca a main.
Las tablas que no existen se saltean. La llave nunca sale de los secrets de GitHub.
Sin dependencias: Python 3 pelado, como el resto del generador."""
import json, os, sys, datetime, urllib.request, urllib.error

TABLAS = ["clientes", "asignaciones", "tareas", "sesiones", "grupales", "actividad", "cartas",
          "comentarios", "adjuntos", "respuestas", "feedback"]
# columnas pesadas o internas que no hacen falta para leer el estado
SACAR = {"cartas": ("pasos", "herramientas")}

def pedir(ruta):
    url = os.environ["SUPABASE_URL"].rstrip("/") + "/rest/v1/" + ruta
    k = os.environ["SUPABASE_SERVICE_KEY"]
    req = urllib.request.Request(url, headers={"apikey": k, "Authorization": "Bearer " + k})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode() or "[]")

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "app-datos"
    os.makedirs(out, exist_ok=True)
    resumen = {"leido": datetime.datetime.utcnow().isoformat() + "Z", "tablas": {}}
    for t in TABLAS:
        filas, desde = [], 0
        try:
            while True:
                lote = pedir("%s?select=*&limit=1000&offset=%d" % (t, desde))
                filas += lote
                if len(lote) < 1000: break
                desde += 1000
        except urllib.error.HTTPError as e:
            resumen["tablas"][t] = "no se pudo leer (%s)" % e.code
            continue
        for f in filas:
            for c in SACAR.get(t, ()): f.pop(c, None)
        json.dump(filas, open(os.path.join(out, t + ".json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1, default=str)
        resumen["tablas"][t] = len(filas)
    json.dump(resumen, open(os.path.join(out, "_resumen.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(json.dumps(resumen, ensure_ascii=False))

if __name__ == "__main__":
    main()
