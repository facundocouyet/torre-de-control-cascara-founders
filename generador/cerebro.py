# -*- coding: utf-8 -*-
"""El cerebro de Cáscara: valida el registro y arma lo que leen las máquinas.

Lee cerebro/registro/**/*.md (una entrada por archivo, con frontmatter) y escribe:
  cerebro/indice.json      todas las entradas con sus campos, para un agente, n8n o Supabase
  cerebro/lineas/<slug>.md la línea de tiempo de cada cliente o tema, en orden
  cerebro/RECIENTE.md      lo último por departamento y las preguntas abiertas

Si una entrada está mal, dice cuál y por qué, y no escribe nada. Python 3 pelado.
Uso: python3 generador/cerebro.py
"""
import glob, json, os, re, sys, datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CER = os.path.join(RAIZ, 'cerebro')

TIPOS = ["decision", "criterio", "aprendizaje", "oferta", "hito", "proceso", "metrica", "pregunta"]
DEPTOS = {"cascara": "Dirección", "founders": "Cáscara Founders", "b2c": "B2C · La Cáscara",
          "agencia": "Agencia", "marcas": "0800 · marcas", "alianzas": "Growth y alianzas",
          "equipo": "Equipo y estructura", "sistemas": "Sistemas y agentes"}
CERTEZAS = ["dicho", "visto", "propuesto"]
ESTADOS = ["vigente", "reemplazada", "cerrada"]
OBLIG = ["id", "fecha", "tipo", "depto", "sobre", "quien", "fuente", "certeza", "estado"]
LISTAS = ["sobre", "quien", "temas"]
DIAS_RECIENTE = 30


def leer(ruta):
    t = open(ruta, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', t, re.S)
    if not m:
        return None, "no tiene el bloque --- de arriba"
    meta = {}
    for linea in m.group(1).split('\n'):
        if not linea.strip():
            continue
        if ':' not in linea:
            return None, "la línea «%s» no es campo: valor" % linea
        k, v = linea.split(':', 1)
        k, v = k.strip(), v.strip()
        if k in LISTAS:
            v = [x.strip() for x in v.strip('[]').split(',') if x.strip()]
        meta[k] = v
    cuerpo = m.group(2).strip()
    tit = re.match(r'^#\s+(.+)$', cuerpo.split('\n')[0])
    if not tit:
        return None, "el cuerpo tiene que arrancar con «# el título»"
    meta['titulo'] = tit.group(1).strip()
    meta['cuerpo'] = '\n'.join(cuerpo.split('\n')[1:]).strip()
    meta['archivo'] = os.path.relpath(ruta, CER)
    return meta, None


def validar(ents):
    errores, ids = [], {}
    for e in ents:
        a = e['archivo']
        for k in OBLIG:
            if not e.get(k):
                errores.append("%s: falta «%s»" % (a, k))
        if e.get('tipo') and e['tipo'] not in TIPOS:
            errores.append("%s: el tipo «%s» no existe (%s)" % (a, e['tipo'], ', '.join(TIPOS)))
        if e.get('depto') and e['depto'] not in DEPTOS:
            errores.append("%s: el depto «%s» no existe (%s)" % (a, e['depto'], ', '.join(DEPTOS)))
        if e.get('certeza') and e['certeza'] not in CERTEZAS:
            errores.append("%s: la certeza «%s» no existe (%s)" % (a, e['certeza'], ', '.join(CERTEZAS)))
        if e.get('estado') and e['estado'] not in ESTADOS:
            errores.append("%s: el estado «%s» no existe (%s)" % (a, e['estado'], ', '.join(ESTADOS)))
        try:
            datetime.date.fromisoformat(e.get('fecha', ''))
        except ValueError:
            errores.append("%s: la fecha «%s» no es AAAA-MM-DD" % (a, e.get('fecha')))
        if e.get('id') and not os.path.basename(a).startswith(e['id']):
            errores.append("%s: el archivo tiene que llamarse como el id (%s.md)" % (a, e['id']))
        if e.get('id') in ids:
            errores.append("%s: el id «%s» ya está en %s" % (a, e['id'], ids[e['id']]))
        ids[e.get('id')] = a
        if e.get('tipo') == 'decision' and e.get('certeza') == 'propuesto':
            errores.append("%s: una propuesta no es una decisión (usá tipo pregunta)" % a)
    for e in ents:
        r = e.get('reemplaza')
        if r and r not in ids:
            errores.append("%s: reemplaza a «%s», que no existe" % (e['archivo'], r))
        if r and r in ids:
            vieja = [x for x in ents if x['id'] == r][0]
            if vieja.get('estado') != 'reemplazada':
                errores.append("%s: la reemplaza %s, así que tiene que decir estado: reemplazada"
                               % (vieja['archivo'], e['id']))
    return errores


def link(e, desde):
    return os.path.relpath(os.path.join(CER, e['archivo']), os.path.join(CER, desde))


def main():
    rutas = sorted(glob.glob(os.path.join(CER, 'registro', '**', '*.md'), recursive=True))
    ents, errores = [], []
    for r in rutas:
        e, err = leer(r)
        if err:
            errores.append("%s: %s" % (os.path.relpath(r, CER), err))
        else:
            ents.append(e)
    errores += validar(ents)
    if errores:
        print("cerebro: hay %d error(es), no se escribió nada" % len(errores))
        for x in errores:
            print("   ·", x)
        sys.exit(1)
    ents.sort(key=lambda e: (e['fecha'], e['id']))
    hasta = ents[-1]['fecha'] if ents else datetime.date.today().isoformat()

    # 1 · el índice, para máquinas
    json.dump({"hasta": hasta, "departamentos": DEPTOS, "tipos": TIPOS, "total": len(ents),
               "entradas": ents},
              open(os.path.join(CER, 'indice.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    # 2 · la línea de tiempo de cada cliente o tema
    os.makedirs(os.path.join(CER, 'lineas'), exist_ok=True)
    por = {}
    for e in ents:
        for s in e['sobre']:
            por.setdefault(s, []).append(e)
    for viejo in glob.glob(os.path.join(CER, 'lineas', '*.md')):
        if os.path.basename(viejo)[:-3] not in por:
            open(viejo, 'w').write('')   # se vacía; no se puede borrar desde todos lados
    for s, es in sorted(por.items()):
        h = ["# %s · línea de tiempo" % s, "",
             "Generado por `generador/cerebro.py` desde el registro. No se edita a mano.", ""]
        for e in es:
            marca = "" if e['estado'] == 'vigente' else " _(%s)_" % e['estado']
            h.append("- **%s** · %s · [%s](%s)%s" % (e['fecha'], e['tipo'], e['titulo'],
                                                   link(e, 'lineas'), marca))
        open(os.path.join(CER, 'lineas', s + '.md'), 'w', encoding='utf-8').write('\n'.join(h) + '\n')

    # 3 · lo reciente, para arrancar el día
    corte = (datetime.date.fromisoformat(hasta) - datetime.timedelta(days=DIAS_RECIENTE)).isoformat()
    h = ["# Lo reciente del cerebro", "",
         "Los últimos %d días hasta el %s, por departamento. Generado por `generador/cerebro.py`."
         % (DIAS_RECIENTE, hasta), ""]
    abiertas = [e for e in ents if e['tipo'] == 'pregunta' and e['estado'] == 'vigente']
    if abiertas:
        h += ["## Preguntas abiertas", ""]
        h += ["- %s · [%s](%s)" % (e['fecha'], e['titulo'], e['archivo']) for e in abiertas]
        h.append("")
    for d, nombre in DEPTOS.items():
        es = [e for e in ents if e['depto'] == d and e['fecha'] >= corte and e['tipo'] != 'pregunta']
        if not es:
            continue
        h += ["## %s" % nombre, ""]
        for e in reversed(es):
            marca = "" if e['estado'] == 'vigente' else " _(%s)_" % e['estado']
            h.append("- %s · %s · [%s](%s)%s" % (e['fecha'], e['tipo'], e['titulo'], e['archivo'], marca))
        h.append("")
    open(os.path.join(CER, 'RECIENTE.md'), 'w', encoding='utf-8').write('\n'.join(h))

    print("cerebro: %d entradas · %d líneas de tiempo · %d preguntas abiertas"
          % (len(ents), len(por), len(abiertas)))


if __name__ == "__main__":
    main()
