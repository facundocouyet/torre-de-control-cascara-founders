# -*- coding: utf-8 -*-
"""El ritmo de cada cliente: una alerta de seguimiento, no un juicio sobre el resultado.
Lo que logra o no logra el founder lo miden el puntaje y la lectura de la radiografía.

  verde     al día             contacto en los últimos 14 días y un próximo paso
                               (una reunión con fecha que todavía no pasó, o una carta abierta)
  amarillo  sin próximo paso   hay noticias, pero no hay reunión agendada ni carta abierta
  rojo      sin noticias       pasaron más de 14 días sin saber nada del cliente
  cierre    en cierre          está en sign off: no lleva ritmo

Los datos viven en contenido/seguimiento.json y se actualizan con cada ronda de novedades."""
import json, os, datetime

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOY = datetime.date.today()
DATOS = json.load(open(os.path.join(B, 'contenido', 'seguimiento.json'), encoding='utf-8'))
LIMITE = DATOS.get('dias_sin_noticias', 14)
SEG = DATOS['clientes']

TEXTO = {"verde": "al día", "amarillo": "sin próximo paso", "rojo": "sin noticias", "cierre": "en cierre"}
EXPLICA = {"verde": "Hubo contacto en los últimos %d días y tiene un próximo paso." % LIMITE,
           "amarillo": "Hay noticias, pero no hay reunión agendada ni carta abierta.",
           "rojo": "Pasaron más de %d días sin saber nada." % LIMITE,
           "cierre": "Está en sign off: no lleva ritmo."}

def _en_cierre():
    e = json.load(open(os.path.join(B, 'contenido', 'entregas.json'), encoding='utf-8'))
    return {f['slug'] for f in e['filas']
            if f.get('estado', '').lower().startswith(('sign off', 'upselling'))}
CIERRE = _en_cierre()

def _f(t): return datetime.date(*map(int, t.split('-'))) if t else None

def calcular(slug):
    s = SEG.get(slug) or {}
    u, p = _f(s.get('ultimo')), _f(s.get('proximo'))
    if slug in CIERRE: r = 'cierre'
    elif not u or (HOY - u).days > LIMITE: r = 'rojo'
    elif (p and p >= HOY) or s.get('carta'): r = 'verde'
    else: r = 'amarillo'
    return {"ritmo": r, "texto": TEXTO[r], "explica": EXPLICA[r],
            "ultimo": s.get('ultimo'), "que": s.get('que'), "hace": (HOY - u).days if u else None,
            "proximo": s.get('proximo'), "paso": s.get('paso'), "carta": s.get('carta')}

if __name__ == '__main__':
    import glob
    for g in sorted(glob.glob(os.path.join(B, 'fichas', '*.json'))):
        if os.path.basename(g) == 'inventario.json': continue
        slug = json.load(open(g, encoding='utf-8'))['slug']
        c = calcular(slug)
        print('%-22s %-17s %s' % (slug, c['texto'], c['hace']))
