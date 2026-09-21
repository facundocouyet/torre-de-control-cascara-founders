# -*- coding: utf-8 -*-
"""Pasa a número las cantidades escritas con palabras, cuando llevan unidad o porcentaje.
   La prosa sin unidad queda como está: "las dos cosas", "un solo comentario"."""
import re, unicodedata

UNI = {'cero':0,'dos':2,'tres':3,'cuatro':4,'cinco':5,'seis':6,'siete':7,'ocho':8,'nueve':9,
       'diez':10,'once':11,'doce':12,'trece':13,'catorce':14,'quince':15,
       'dieciseis':16,'diecisiete':17,'dieciocho':18,'diecinueve':19,
       'veinte':20,'veintiuno':21,'veintidos':22,'veintitres':23,'veinticuatro':24,
       'veinticinco':25,'veintiseis':26,'veintisiete':27,'veintiocho':28,'veintinueve':29}
DEC = {'treinta':30,'cuarenta':40,'cincuenta':50,'sesenta':60,'setenta':70,'ochenta':80,'noventa':90}
CEN = {'cien':100,'ciento':100,'doscientos':200,'trescientos':300,'cuatrocientos':400,
       'quinientos':500,'seiscientos':600,'setecientos':700,'ochocientos':800,'novecientos':900}
TODAS = dict(UNI); TODAS.update(DEC); TODAS.update(CEN); TODAS['mil']=1000

def _n(w):
    return unicodedata.normalize('NFKD', w.lower()).encode('ascii','ignore').decode()

def _pal(d):  # alternativa de regex con acentos y sin acentos
    ac = {'dieciseis':'dieciséis','veintidos':'veintidós','veintitres':'veintitrés',
          'veintiseis':'veintiséis'}
    ws = list(d) + [ac[k] for k in d if k in ac]
    return "|".join(sorted(set(ws), key=len, reverse=True))

R_UNI, R_DEC, R_CEN = _pal(UNI), _pal(DEC), _pal(CEN)
# un número de 1 a 999: [centena] [decena [y unidad] | unidad]
CHICO = r"(?:(?:%s)(?:\s+(?:(?:%s)(?:\s+y\s+(?:%s))?|(?:%s)))?|(?:%s)(?:\s+y\s+(?:%s))?|(?:%s))" % (
    R_CEN, R_DEC, R_UNI, R_UNI, R_DEC, R_UNI, R_UNI)
# y con mil adentro: mil, tres mil, mil quinientos, dos mil quinientos
FRASE = r"(?:(?:%s)\s+)?mil(?:\s+%s)?|%s" % (CHICO, CHICO, CHICO)
FRASE = "(?:%s)" % FRASE

UNIDADES = ("minutos?|horas?|d[ií]as?|semanas?|meses|mes|a[nñ]os?|piezas?|videos?|reels?|"
            "posteos?|publicaciones?|cuentas?|clientes?|alumnos?|llamadas?|reuniones?|personas?|"
            "cupos?|d[oó]lares?|seguidores?|comentarios?|mensajes?|propuestas?|ventas?|leads?|"
            "m[oó]dulos?|sesiones?|guiones?|cartas?|entregas?|niveles?|campos?|formularios?|"
            "preguntas?|propiedades?|lugares?|conversaciones?|episodios?|invitados?|"
            "asistentes?|cohortes?|invitaciones?|encuentros?|bloques?|etapas?|pasos?|ejes|"
            "[aá]ngulos?|drops?|workshops?|talleres?|historias?|vistas?|respuestas?|testimonios?|"
            "casos?|pilares?|hojas?|ideas?|tareas?|canales?|clases?|grabaciones?|suscriptores?|"
            "millones?|mill[oó]n")

def _chico(p):
    if not p: return 0
    if len(p)==1: return TODAS.get(p[0])
    if p[0] in CEN:
        r=_chico(p[1:])
        return None if r is None else CEN[p[0]]+r
    if len(p)==3 and p[1]=='y' and p[0] in DEC and p[2] in UNI:
        return DEC[p[0]]+UNI[p[2]]
    return None

def valor(frase):
    p=[_n(x) for x in frase.split()]
    if not p: return None
    if 'mil' in p:
        i=p.index('mil')
        izq=_chico(p[:i]) if p[:i] else 1
        der=_chico(p[i+1:])
        if izq is None or der is None: return None
        return izq*1000+der
    return _chico(p)

def fmt(n):
    return f"{n:,}".replace(',', '.') if n>=1000 else str(n)

# para el guardia: también las formas femeninas y "un/una", que el parser no usa
GUARDIA = set(TODAS) | {'un','una','unos','unas','millon','millones',
    'doscientas','trescientas','cuatrocientas','quinientas','seiscientas',
    'setecientas','ochocientas','novecientas','veintiuna','treintaiuna'}

def _pegado(t,i):
    """True si justo antes del match hay otra palabra numérica."""
    ant=t[:i].rstrip()
    if re.search(r"[\d.]$", ant): return True
    m=re.search(r"([A-Za-zÁÉÍÓÚáéíóúñÑ]+)$", ant)
    return bool(m) and _n(m.group(1)) in GUARDIA

def convertir(t):
    if not isinstance(t,str) or not t: return t, []
    cambios=[]
    # 0) lo que ya venía en cifra con "mil" al lado: "50 mil" -> "50.000"
    def mil2(m):
        s=fmt(int(m.group(1))*1000)+' y '+fmt(int(m.group(2))*1000)
        cambios.append((m.group(0), s)); return s
    t = re.sub(r"\b(\d{1,3})\s+y\s+(\d{1,3})\s+mil\b", mil2, t)
    def mil1(m):
        s=fmt(int(m.group(1))*1000)
        cambios.append((m.group(0), s)); return s
    t = re.sub(r"\b(\d{1,3})\s+mil\b", mil1, t)
    def rango(m):
        if _pegado(t, m.start()): return m.group(0)
        a,b,sep = m.group('a'), m.group('b'), m.group('sep')
        if sep.lower()=='y' and valor(a+' y '+b) is not None: return m.group(0)
        va,vb = valor(a), valor(b)
        if va is None or vb is None: return m.group(0)
        s = m.group(0).replace(a, fmt(va), 1)
        s = s[::-1].replace(b[::-1], fmt(vb)[::-1], 1)[::-1]
        cambios.append((m.group(0), s)); return s
    t2 = re.sub(r"\b(?P<a>%s)\s+(?P<sep>y|a)\s+(?P<b>%s)\s+(?P<u>%s)\b" % (FRASE, FRASE, UNIDADES),
                rango, t, flags=re.I)
    t = t2
    def pc(m):
        if _pegado(t, m.start()): return m.group(0)
        v=valor(m.group('a'))
        if v is None: return m.group(0)
        s=fmt(v)+'%'; cambios.append((m.group(0), s)); return s
    t = re.sub(r"\b(?P<a>%s)\s+por\s+ciento\b" % FRASE, pc, t, flags=re.I)
    def cu(m):
        if _pegado(t, m.start()): return m.group(0)
        v=valor(m.group('a'))
        if v is None: return m.group(0)
        s=fmt(v)+' '+m.group('u'); cambios.append((m.group(0), s)); return s
    t = re.sub(r"\b(?P<a>%s)\s+(?P<u>%s)\b" % (FRASE, UNIDADES), cu, t, flags=re.I)
    return t, cambios
