"""Carta de módulo para un cliente que no es de Founders (p. ej. Cero).

Uso: python3 generador/carta_externa.py fichas/externos/<modulo>--<slug>.json
Sale a envios/<slug>/<modulo>.html, en plural (ustedes) y sin la marca Founders.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_cartas as B

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLURAL = [
    ("Esto lo escribimos para vos, sobre lo que venimos viendo en tu caso.",
     "Esto lo escribimos para ustedes, sobre lo que venimos viendo en su caso."),
    ("Por qué te toca ahora", "Por qué les toca ahora"),
    ("Qué tenés que hacer", "Qué tienen que hacer"),
    ("Lo que escribís se guarda solo en este navegador.", "Lo que escriban se guarda solo en este navegador."),
    ("Cáscara Founders · ", "Cáscara · "),
]

def main(ruta):
    pl = json.load(open(ruta, encoding='utf-8'))
    inv = json.load(open(os.path.join(RAIZ, 'fichas', 'inventario.json'), encoding='utf-8'))
    m, cat = next((dict(x), c["nombre"]) for c in inv["categorias"] for x in c["modulos"] if x["id"] == pl["modulo"])
    if pl.get("para_quien"): m["para_quien"] = pl["para_quien"]
    h = B.render(m, cat, pl, pl.get("bajada_envio"))
    quien = (pl.get("bajada_envio") or {}).get("founder", "")
    if quien:
        h = h.replace("Por qué esta carta, " + quien.split(" ")[0], "Por qué esta carta, " + quien)
        h = h.replace(" · carta de módulo · " + quien, " · " + pl.get("marca", pl["slug"].title()))
    for a, b in PLURAL: h = h.replace(a, b)
    sal = os.path.join(RAIZ, 'envios', pl["slug"], pl.get("archivo", pl["modulo"]) + '.html')
    os.makedirs(os.path.dirname(sal), exist_ok=True)
    open(sal, 'w', encoding='utf-8').write(h)
    print("carta:", os.path.relpath(sal, RAIZ))

if __name__ == "__main__":
    main(sys.argv[1])
