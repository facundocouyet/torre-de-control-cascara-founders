# -*- coding: utf-8 -*-
"""Días con nosotros. START de Notion cuando existe; si no, la primera llamada registrada."""
import json, re, datetime
# el día de hoy, para que el conteo no quede clavado en una fecha vieja
HOY=datetime.date.today()
MES={'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,
     'agosto':8,'septiembre':9,'setiembre':9,'octubre':10,'noviembre':11,'diciembre':12}
# START cargado en la base Cuentas
START={"lucca-sorgoni":"2026-04-06","qualita":"2026-04-24","sebastian":"2026-09-01",
       "sharon-palacio":"2026-05-13","sol-boutmy":"2026-09-02","the-momentum-club":"2026-09-16"}

# Tramos frenados: no consumen días del programa, pero el cliente lleva más tiempo con nosotros.
# Qualita arrancó como Rafael Lizarraga el 24/04, se frenó en Mes 2 por viaje y retomó el 20/08.
PAUSA={"qualita":[("2026-06-12","2026-08-20")]}

def parse(t):
    t=t.lower()
    m=re.search(r'(\d{1,2})\s+de\s+([a-záé]+)\s+de\s+(\d{4})',t)
    if m and m.group(2) in MES:
        return datetime.date(int(m.group(3)),MES[m.group(2)],int(m.group(1)))
    m=re.search(r'\b([a-záé]+)\s+de\s+(\d{4})',t)
    if m and m.group(1) in MES:
        return datetime.date(int(m.group(2)),MES[m.group(1)],1)
    return None

def _fecha(t): return datetime.date(*map(int,t.split('-')))

def _frenado(slug):
    """Días que el cliente estuvo frenado y que no cuentan contra los noventa."""
    total=0; tramos=[]
    for a,b in PAUSA.get(slug,[]):
        ini,fin=_fecha(a),min(_fecha(b),HOY)
        if fin>ini:
            total+=(fin-ini).days
            tramos.append((ini.isoformat(),fin.isoformat()))
    return total,tramos

def _armar(d,fuente,slug):
    frena,tramos=_frenado(slug)
    corridos=max(1,(HOY-d).days+1)
    return {"d":max(1,corridos-frena),"desde":d.isoformat(),"fuente":fuente,
            "corridos":corridos,"frenado":frena,"tramos":tramos}

def calcular(slug, que_paso):
    if slug in START:
        return _armar(_fecha(START[slug]),"start",slug)
    fechas=[f for f in (parse(x['cuando']) for x in que_paso) if f]
    if fechas:
        return _armar(min(fechas),"llamada",slug)
    return {"d":None,"desde":None,"fuente":"falta","corridos":None,"frenado":0,"tramos":[]}
