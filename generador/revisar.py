#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Revisa el sistema antes de publicar.

Busca la clase de error que ya nos pasó tres veces: un número o un documento
que se nombra en un lado y no existe en el otro. Corre solo, al final de
construir.sh, y si encuentra algo lo dice y corta el build.

    python3 generador/revisar.py
"""
import json, os, re, glob, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def R(*p): return os.path.join(RAIZ, *p)
def cargar(p): return json.load(open(R(p), encoding='utf-8'))

fallos, avisos = [], []
def mal(q): fallos.append(q)
def ojo(q): avisos.append(q)

NUM = {1:'una',2:'dos',3:'tres',4:'cuatro',5:'cinco',6:'seis',7:'siete',8:'ocho',
       9:'nueve',10:'diez',11:'once',12:'doce',13:'trece',14:'catorce',15:'quince'}
PALABRA = {v: k for k, v in NUM.items()}


def secciones_efectivas(pl, base):
    """Las secciones que termina teniendo una carta, variante incluida."""
    if pl.get('secciones'): return pl['secciones']
    return (list(pl.get('bloques_inicio') or []) + list((base or {}).get('secciones') or [])
            + list(pl.get('bloques_final') or []))


# ── 1. los números que se dicen contra los que hay ─────────────────────────
# "Son diez preguntas", "las nueve respuestas", "las ocho primeras"
# sólo las frases que hablan de la hoja entera. "las tres preguntas" adentro de
# una consigna habla de esa sección, no de la carta, y no se cuenta.
CUENTA = re.compile(r'\bson\s+(%s)\s+preguntas' % '|'.join(PALABRA), re.I)
# "las ocho primeras" sólo se valida cuando acompaña a un "Son N preguntas":
# suelto puede hablar de piezas, de semanas o de cualquier otra cosa.
PRIMERAS = re.compile(r'\blas\s+(%s)\s+primeras' % '|'.join(PALABRA), re.I)

def revisar_cartas():
    for f in sorted(glob.glob(R('fichas/plantillas/*.json'))):
        nom = os.path.basename(f)
        pl = json.load(open(f, encoding='utf-8'))
        base = None
        if '--' in nom:
            b = R('fichas/plantillas/%s.json' % pl['modulo'])
            base = json.load(open(b, encoding='utf-8')) if os.path.exists(b) else None
        secs = secciones_efectivas(pl, base)
        trabajo = sum(1 for s in secs if not s.get('nuestro'))

        txt = json.dumps(pl, ensure_ascii=False)
        declara = False
        for m in CUENTA.finditer(txt):
            declara = True
            dicho = PALABRA[m.group(1).lower()]
            if dicho != trabajo:
                mal('%s dice "%s" pero la carta tiene %d preguntas'
                    % (nom, m.group(0), trabajo))
        if declara:
            for m in PRIMERAS.finditer(txt):
                if PALABRA[m.group(1).lower()] > trabajo:
                    mal('%s dice "%s" y la carta tiene %d preguntas'
                        % (nom, m.group(0), trabajo))

        # claves de campo repetidas: pisan lo que el founder escribió
        vistos = {}
        for i, s in enumerate(secs):
            cid = s.get('cid', i)
            if s.get('nuestro') and not s.get('pregunta'): continue
            if cid in vistos:
                mal('%s: la sección "%s" comparte la clave s%s con "%s"'
                    % (nom, s.get('titulo'), cid, vistos[cid]))
            vistos[cid] = s.get('titulo')

        # una variante tiene que apuntar a un módulo que exista
        if '--' in nom and base is None and not pl.get('secciones'):
            ojo('%s no tiene preguntas: el módulo "%s" todavía no tiene hoja escrita, '
                'así que esa carta no se genera' % (nom, pl['modulo']))


# ── 2. lo que se nombra como entregable tiene que existir ──────────────────
def revisar_inventario():
    inv = cargar('fichas/inventario.json')
    for c in inv['categorias']:
        for m in c['modulos']:
            for campo in ('completar', 'herramientas'):
                for x in (m.get(campo) or []):
                    if re.search(r'formulario de (construcción de oferta|40 preguntas)', x, re.I):
                        mal('inventario · %s: nombra un formulario que no existe ("%s")' % (m['id'], x))
                    n = CUENTA.search(x)
                    if n:
                        mal('inventario · %s: fija un número de preguntas ("%s"), '
                            'que cambia con cada variante' % (m['id'], n.group(0)))


# ── 3. la torre no puede apuntar a documentos que no están ─────────────────
def revisar_entregas():
    d = cargar('contenido/entregas.json')
    for f in d['filas']:
        for k in ('doc',):
            v = f.get(k)
            if v and not os.path.exists(R('clientes', v)):
                mal('entregas · %s: el documento "%s" no está en clientes/' % (f['nombre'], v))
        # "Mandarle la carta X" tiene que tener su html armado para ese founder
        slug = f.get('slug')
        for a in (f.get('accionables') or []):
            if re.search(r'[Mm]andarle la carta', a) and slug:
                hay = glob.glob(R('cartas/para/%s-*.html' % slug))
                if not hay:
                    mal('entregas · %s: se le manda una carta pero no hay ninguna '
                        'escrita para ese slug' % f['nombre'])
                break


# ── 4. los recursos de la biblioteca: link o aviso de que falta ────────────
def revisar_materiales():
    m = cargar('contenido/materiales.json')
    for b in m['bloques']:
        for p in b['piezas']:
            if not p.get('url') and p.get('estado') == 'listo' and 'Notion' in (p.get('formatos') or []):
                ojo('materiales · "%s" dice listo y no tiene link' % p['titulo'])



# ── 5. las palabras que no son las nuestras ────────────────────────────────
# Los documentos se escriben leyendo llamadas de gente de España, Colombia,
# Uruguay y México, y sus palabras se filtran a un texto que tiene que sonar a
# Facu. No es gramática: es léxico y registro.
VOZ = [
    (r'\bm[óo]viles?\b', 'celular'), (r'\bordenador\w*', 'computadora'),
    (r'\bvosotros\b', 'ustedes'), (r'\bvuestr[oa]s?\b', 'su'),
    (r'\bcoger\b', 'agarrar'), (r'\bguay\b', 'buenísimo'),
    (r'\baqu[íi]\b', 'acá'), (r'\ball[íi]\b', 'allá'),
    (r'\bahora mismo\b', 'ahora'), (r'\bechar un vistazo\b', 'mirar'),
    (r'\bzumo\b', 'jugo'), (r'\bcurrar\b', 'laburar'),
    (r'\bt[ú]\b', 'vos'), (r'\bpuedes\b', 'podés'), (r'\btienes\b', 'tenés'),
    (r'\bquieres\b', 'querés'), (r'\bdebes\b', 'tenés que'),
    (r'\bhaces\b', 'hacés'), (r'\bsabes\b', 'sabés'), (r'\bvienes\b', 'venís'),
    (r'\bch[ée]vere\b', 'copado'), (r'\bahorita\b', 'ahora'),
    (r'\bplaticar\b', 'charlar'), (r'\bplatica\b', 'charla'),
    (r'siguiente nivel', 'sacar: es aspiracional'),
    (r'\bpotenciar\b', 'sacar: es corporativo'),
    (r'\bmaximizar\b', 'sacar: es corporativo'),
    (r'\bsinergia\w*', 'sacar: es corporativo'),
    (r'\bempoderar\w*', 'sacar: es corporativo'),
    (r'cabe destacar', 'sacar: es relleno'),
    (r'es importante destacar', 'sacar: es relleno'),
    (r'\bsumergi\w+', 'sacar: es relleno'),
]

def revisar_voz():
    import glob as _g
    archivos = sorted(_g.glob(R('fichas/plantillas/*.json'))) + sorted(_g.glob(R('contenido/*.json')))
    for f in archivos:
        if os.path.basename(f) == 'app-data.json': continue   # es generado
        s = open(f, encoding='utf-8').read()
        for pat, sug in VOZ:
            for m in re.finditer(pat, s):
                ctx = re.sub(r'\s+', ' ', s[max(0, m.start()-50):m.start()+50])
                ojo('%s dice "%s" (va "%s") · …%s…'
                    % (os.path.basename(f), m.group(0), sug, ctx))


# ── 6. contar módulos o cartas en el texto ─────────────────────────────────
# "los cuarenta módulos", "las 40 cartas": el número del catálogo queda viejo
# el día que se agrega uno y nadie se acuerda de tocarlo. La regla es no
# nombrarlo. Los números chicos son de los clientes (los nueve módulos de
# Cecilia) y esos se dejan pasar.
CANTIDAD = re.compile(
    r'\b(?:veinte|treinta|cuarenta|cincuenta|sesenta|setenta|[2-9]\d)\s+'
    r'(m[oó]dulos|cartas)\b', re.I)

def revisar_cuentas():
    import glob as _g
    archivos = (sorted(_g.glob(R('fichas/*.json'))) + sorted(_g.glob(R('contenido/*.json')))
                + sorted(_g.glob(R('generador/*.py'))))
    for f in archivos:
        base = os.path.basename(f)
        if base in ('app-data.json', 'revisar.py'): continue
        s = open(f, encoding='utf-8').read()
        for m in CANTIDAD.finditer(s):
            ctx = re.sub(r'\s+', ' ', s[max(0, m.start()-60):m.start()+60])
            mal('%s dice "%s": el número de módulos o cartas se queda viejo, '
                'escribilo sin contarlo · …%s…' % (base, m.group(0), ctx))


for fn in (revisar_cartas, revisar_inventario, revisar_entregas, revisar_materiales,
           revisar_voz, revisar_cuentas):
    try: fn()
    except Exception as e: mal('%s reventó: %s' % (fn.__name__, e))

for a in avisos: print('   ojo · %s' % a)
for f in fallos: print('   MAL  · %s' % f)
if fallos:
    print('\n   %d problema(s). No publiques así.' % len(fallos)); sys.exit(1)
print('   revisión: %d aviso(s), nada roto' % len(avisos))
