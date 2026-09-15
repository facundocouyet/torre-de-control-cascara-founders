# Handoff para Claude Code

Pegá esto en Claude Code, parado en esta carpeta.

---

Necesito que subas este repo a GitHub y lo dejes andando. Se llama **torre de control de Cáscara
Founders** y genera los documentos de los clientes de la aceleradora, la torre de control y las
cuarenta cards del programa.

## Lo que hay que hacer

1. **Verificá que el repo esté sano.** Ya tiene historia de git y siete commits. Chequeá que el
   working tree esté limpio y que la rama sea `main`.

2. **Creá el repositorio en GitHub** con `gh repo create`:
   - Nombre: `torre-de-control-cascara-founders`
   - Privado
   - Descripción: "Torre de control de Cáscara Founders: las fichas de cada founder, el generador de
     documentos, las 40 cards y el rol de líder."
   - Sin README ni .gitignore automáticos: el repo ya los tiene.

3. **Empujá** y dejá `main` como rama por defecto.

4. **Corré los builds una vez** para confirmar que todo genera sin tocar nada:
   ```bash
   cd generador
   python3 build2.py          # 19 documentos de cliente en out2/
   python3 build_cartas.py    # 40 cards
   python3 build_plantillas.py
   python3 build_cards.py     # el handoff de cards por dueño
   python3 build_rol.py       # el documento del rol
   ```
   Si alguno falla por una ruta absoluta que apunta a `/home/claude/...`, arreglala para que use
   rutas relativas al repo y commiteá ese arreglo aparte, con el mensaje "Rutas relativas para que
   los builds corran fuera del contenedor". Es el único cambio de código que te pido.

5. **Decime el resultado**: la URL del repo, si los cinco builds corrieron, y qué rutas tuviste que
   arreglar.

## Contexto que te conviene leer antes

- `CLAUDE.md` — cómo está armado el repo, qué hace cada script y el esquema de las fichas.
- `sistema/15-rol-lider-founders.md` — el proceso del que sale todo esto.
- `agente/prompt-agente.md` — la tarea programada que va a clonar este repo todos los días. Es la
  razón por la que el repo tiene que existir en GitHub.

## Lo que NO quiero que hagas

- No reescribas los documentos de `clientes/` ni las fichas de `fichas/`: son contenido, no código.
- No cambies las reglas de redacción de `CLAUDE.md`.
- No hagas público el repo.
