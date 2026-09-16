# -*- coding: utf-8 -*-
"""Días con nosotros. START de Notion cuando existe; si no, la primera llamada registrada."""
import json, re, datetime
HOY=datetime.date(2026,9,12)
MES={'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,
     'agosto':8,'septiembre':9,'setiembre':9,'octubre':10,'noviembre':11,'diciembre':12}
# START cargado en la base Cuentas
START={"lucca-sorgoni":"2026-04-06","qualita":"2026-08-20","sebastian":"2026-09-01",
       "sharon-palacio":"2026-05-13","sol-boutmy":"2026-09-02"}

def parse(t):
    t=t.lower()
    m=re.search(r'(\d{1,2})\s+de\s+([a-záé]+)\s+de\s+(\d{4})',t)
    if m and m.group(2) in MES:
        return datetime.date(int(m.group(3)),MES[m.group(2)],int(m.group(1)))
    m=re.search(r'\b([a-záé]+)\s+de\s+(\d{4})',t)
    if m and m.group(1) in MES:
        return datetime.date(int(m.group(2)),MES[m.group(1)],1)
    return None

def calcular(slug, que_paso):
    if slug in START:
        d=datetime.date(*map(int,START[slug].split('-')))
        return {"d":(HOY-d).days,"desde":d.isoformat(),"fuente":"start"}
    fechas=[f for f in (parse(x['cuando']) for x in que_paso) if f]
    if fechas:
        d=min(fechas)
        return {"d":(HOY-d).days,"desde":d.isoformat(),"fuente":"llamada"}
    return {"d":None,"desde":None,"fuente":"falta"}
