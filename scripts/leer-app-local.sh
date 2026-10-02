#!/bin/bash
# Abre en la Mac lo que la Action "Leer la app" dejó cifrado en la rama app-datos.
# Necesita la clave en .app-datos-clave (la misma que el secret APP_DATOS_CLAVE de GitHub).
# Deja los JSON en _app/ (ignorado por git). No toca main ni la carpeta de trabajo.
set -e
cd "$(dirname "$0")/.."
[ -f .app-datos-clave ] || { echo "Falta .app-datos-clave"; exit 1; }
git fetch -q origin app-datos
rm -rf _app && mkdir -p _app
git show origin/app-datos:datos.tgz.enc > _app/datos.tgz.enc
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in _app/datos.tgz.enc -out _app/datos.tgz -pass file:.app-datos-clave
tar -xzf _app/datos.tgz -C _app && rm _app/datos.tgz _app/datos.tgz.enc
cat _app/app-datos/_resumen.json
