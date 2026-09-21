# Cómo trabajamos los dos sobre este repo

Facu tiene la torre de control. Teo tiene la app de clientes. Los dos leen
los mismos datos de clientes. Esto explica cómo se hace sin romper nada.

---

## La regla que evita el 90% de los problemas

**El HTML generado no se commitea.**

La torre no se escribe a mano: sale de correr los scripts de `generador/`
sobre los JSON de `fichas/` y `contenido/`. Antes esos HTML estaban en el
repo, y ahí está el problema: si los dos regeneramos y los dos commiteamos
un `index.html` de 220 KB, git no tiene forma de mergearlos y el push se
traba.

Ahora los genera GitHub en cada push y los publica solo. En el repo queda
la fuente —los JSON y los scripts—, que sí se mergea bien porque cada uno
toca líneas distintas.

---

## Quién toca qué

| Carpeta | Dueño | Qué es |
|---|---|---|
| `generador/` | Facu | Los scripts que arman la torre |
| `fichas/` | Facu | Una ficha por cliente, más el inventario de módulos |
| `contenido/` | Facu | Entregas, proceso, orientaciones |
| `clientes/`, `cartas/`, `index.html` | nadie | Generados. No se tocan a mano |
| `app-clientes/` | Teo | La app de clientes, entera |
| `assets/`, `construir.sh`, `.github/` | los dos | Se avisa antes de cambiarlos |

Mientras cada uno se quede en su columna, git no tiene nada que resolver.

---

## El día a día

**Facu**, que es el único que edita la torre, puede seguir trabajando
derecho sobre `main`:

    git pull --rebase        # siempre antes de empezar
    ...editar fichas y contenido...
    git add -A && git commit -m "..."
    git push

El `--rebase` es lo que evita los merges cruzados. Si alguna vez `git push`
dice que estás atrasado, es porque Teo subió algo: `git pull --rebase` y
volvé a pushear.

**Teo** trabaja en su propia rama y la mergea por pull request:

    git switch -c app-clientes        # la primera vez
    ...trabajar en app-clientes/...
    git add -A && git commit -m "..."
    git push -u origin app-clientes

Después, un pull request en GitHub. El robot arma el sitio y avisa si algo
se rompió antes de mergear.

---

## Cómo ver el sitio antes de subirlo

    ./construir.sh ver

Arma todo en `dist/` y lo sirve en http://localhost:8765. Es lo mismo que
va a hacer GitHub, así que si funciona acá funciona allá.

Para armar sin servir:

    ./construir.sh

---

## Cuando igual hay conflicto

Pasa si los dos editaron el mismo JSON. Es raro y se arregla a mano: el
archivo queda con las dos versiones marcadas, se elige y se sigue.

    git status                        # ver cuál es
    ...editar el archivo, borrar las marcas <<<< ==== >>>>...
    git add <archivo>
    git rebase --continue

Si te perdiste y querés volver al estado de antes:

    git rebase --abort

Nada se pierde: lo que ya estaba commiteado está a salvo.

---

## Lo que se publica y lo que no

El sitio que sale a internet tiene la torre, las cartas, los documentos de
clientes y la app de Teo en `/app`. **No** incluye `fichas/`, `contenido/`,
`generador/` ni `sistema/`: esos son fuente y se quedan en el repo.

Antes sí se publicaban, porque Pages subía la carpeta entera.

---

## Arnold

Es el panel de la derecha de la torre. Contesta con lo que está cargado:
los clientes, sus accionables, las cartas y las reglas del programa.

Se abre con el botón de abajo a la derecha, con la tecla `/`, o escribiendo
**hey arnold** en cualquier parte de la página. Se cierra con Escape.

Hoy Arnold busca, no piensa: repite lo que hay en la torre y, cuando no
está, lo dice en vez de inventarlo. Eso lo hace confiable para Aye.

Para que además piense, hay que poner a andar `arnold-backend/worker.js`
—una función chica que guarda la clave de Anthropic, porque en la página la
vería cualquiera— y pegar su URL en `generador/app_shell.py`, en la línea:

    var ARNOLD_API = '';

Con esa línea llena, cada pregunta se contesta primero con la torre y
después con el modelo, que recibe el estado de los clientes como contexto.
Las instrucciones para desplegarlo están arriba de todo en `worker.js`.
