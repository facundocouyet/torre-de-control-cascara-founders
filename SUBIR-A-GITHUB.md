# Cómo subir esto a GitHub

El repo ya está armado y con el primer commit hecho. Falta crearlo en GitHub y empujarlo.

## 1. Crear el repositorio vacío

En https://github.com/new:

- **Repository name:** `torre-de-control-cascara-founders`
- **Description:** Torre de control de Cáscara Founders — la camada, el handicap del 1 al 100 y los documentos de cada founder.
- **Private**
- Dejar destildado "Add a README file", "Add .gitignore" y "Choose a license". El repo tiene que quedar vacío.

## 2. Empujar

Desde la carpeta que descomprimiste, en la terminal:

```bash
cd torre-de-control-cascara-founders
git remote add origin https://github.com/facundocouyet/torre-de-control-cascara-founders.git
git push -u origin main
```

## 3. Si querés que se vea como web (opcional)

En el repo, Settings → Pages → Source: Deploy from a branch → Branch `main`, carpeta `/ (root)`.
Queda publicado en `https://facundocouyet.github.io/torre-de-control-cascara-founders/`.
Ojo: con Pages, un repo privado necesita plan de equipo; si el repo es público, la torre de control
queda visible para cualquiera que tenga el link.

## Para que lo actualice yo desde acá

Una vez creado el repo, agregalo como fuente de esta sesión (en la configuración del proyecto,
donde se listan los repositorios autorizados). Con eso puedo empujar los cambios directamente y no
hace falta repetir estos pasos.
