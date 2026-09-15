# Cómo subir y actualizar este repo

## La primera vez

Crear el repo vacío en https://github.com/new:

- **Nombre:** `torre-de-control-cascara-founders`
- **Privado**
- Sin README, sin .gitignore, sin licencia. Tiene que quedar vacío.

Después, desde esta carpeta:

```bash
git remote add origin https://github.com/facundocouyet/torre-de-control-cascara-founders.git
git push -u origin main
```

Si pide autenticación, `gh auth login` primero.

## De ahí en adelante

```bash
git add -A && git commit -m "<qué cambió>" && git push
```

## Por qué importa

La tarea programada diaria de Founders clona este repo para actualizar las fichas y republicar la
torre. Mientras el repo no exista en GitHub, esa tarea no puede correr sola y los scripts tienen
que vivir adentro del prompt.
