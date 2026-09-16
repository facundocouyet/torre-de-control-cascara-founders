# Cómo se actualiza la torre

Un solo comando, desde `web/`:

```bash
python3 build_app.py && python3 app_shell.py
```

## Dónde se edita cada cosa

| Qué | Archivo |
|---|---|
| Los clientes: cuello, métrica, titular, etapa, roadmap, accionables | `founders/v2/fichas/<slug>.json` |
| Los documentos de cliente | `cd founders && python3 build2.py` → `out2/`, después copiar a `web/site/clientes/` |
| **Entregas** (el handoff: qué mandar y qué hacer con cada cliente) | `web/contenido/entregas.json` |
| El handicap | `founders/handicap.py` |
| El programa, el material y las cartas | `web/contenido/programa.json`, `materiales.json`, `founders/modulos/inventario.json` |

## Entregas

`contenido/entregas.json` es la fuente única. De ahí salen dos cosas:

- La sección **Entregas** de la torre (`python3 app_shell.py`).
- El documento suelto para Aye (`cd ally && python3 build_ally.py`).

Cada fila tiene: `slug`, `nombre`, `estado`, `proyecto`, `accionables`, `doc`, `docn`, `extra`, `nota`.
Para cambiar lo que hay que hacer con un cliente se edita su `accionables` y se corre el comando de arriba.
