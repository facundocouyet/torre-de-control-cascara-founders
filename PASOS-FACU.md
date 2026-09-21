# Los tres pasos que tenés que hacer vos en GitHub

Cinco minutos, una sola vez. **El orden importa**: el paso 2 va antes de
pushear, así el sitio no se cae ni un minuto.

---

## 1. Sumar a Teo al repo

En https://github.com/facundocouyet/torre-de-control-cascara-founders
→ **Settings** → **Collaborators** → **Add people** → su usuario de GitHub
→ permiso **Write**.

Le llega una invitación por mail que tiene que aceptar.

Pasame su usuario y completo `.github/CODEOWNERS`, que es lo que hace que
GitHub le pida revisión automáticamente cuando alguien toca su carpeta.

---

## 2. Cambiar de dónde sale el sitio — ANTES de pushear

**Settings** → **Pages** → en *Source* cambiar
**Deploy from a branch** por **GitHub Actions**.

Hasta el primer build, GitHub sigue sirviendo la versión que ya está
publicada, así que no se cae nada.

Este paso va primero porque el repo ya no lleva el HTML adentro: lo arma
GitHub en cada push. Si pusheás con Pages todavía en modo rama, va a
intentar publicar un repo sin `index.html`.

---

## 3. Recién ahí, pushear

    cd ~/Documents/torre-de-control-cascara-founders
    git push

Andá a la pestaña **Actions** del repo: vas a ver correr *Publicar la
torre*. Tarda menos de un minuto. Cuando termina en verde, el sitio está
actualizado.

Si sale en rojo, abrí el paso que falló: dice exactamente qué se rompió y
el sitio anterior sigue online mientras tanto.

---

## 4. Proteger main (opcional, para después)

**Settings** → **Rules** → **Rulesets** → **New branch ruleset**,
apuntado a `main`:

- *Require a pull request before merging*, y en **Bypass list** agregá
  **Repository admin**. Así vos seguís pusheando derecho y Teo pasa por
  pull request.
- *Require status checks to pass* → elegí **construir**.

Es un cinturón de seguridad, no un requisito. Funciona igual sin esto.
