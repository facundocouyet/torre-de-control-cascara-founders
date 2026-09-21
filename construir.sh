#!/usr/bin/env bash
# Arma el sitio entero en dist/. Lo corre GitHub Actions en cada push,
# y lo podés correr vos para ver el resultado antes de subirlo.
#
#   ./construir.sh          arma todo
#   ./construir.sh ver      arma todo y lo abre en el navegador
#
# No necesita instalar nada: es Python 3 pelado.
set -euo pipefail
cd "$(dirname "$0")"

echo "→ la torre"
cd generador
for g in build2.py build_cartas.py build_cards.py build_rol.py build_ally.py build_app.py app_shell.py; do
  echo "   $g"
  python3 "$g" > /dev/null
done
cd ..

# la app de clientes de Teo, si ya tiene su propio build
if [ -x app-clientes/construir.sh ]; then
  echo "→ la app de clientes"
  ( cd app-clientes && ./construir.sh )
fi

echo "→ juntando todo en dist/"
mkdir -p dist
# todo lo que es sitio va a dist; lo que es fuente o privado se queda afuera
rsync -a --delete --quiet \
  --exclude '.git/' --exclude '.github/' --exclude 'dist/' \
  --exclude 'generador/' --exclude 'fichas/' --exclude 'contenido/' \
  --exclude 'sistema/' --exclude 'agente/' --exclude 'app-clientes/' \
  --exclude '_tmp/' --exclude '_locks_viejos/' --exclude 'site/' --exclude 'out/' \
  --exclude '__pycache__/' --exclude '.DS_Store' --exclude '*.py' --exclude '*.sh' \
  --exclude '*.md' --exclude 'LICENSE' \
  ./ dist/

# la app de clientes cuelga de /app
if [ -d app-clientes/dist ]; then
  mkdir -p dist/app && rsync -a --delete --quiet app-clientes/dist/ dist/app/
fi

echo "✓ listo: $(find dist -type f | wc -l | tr -d ' ') archivos en dist/"
if [ "${1:-}" = "ver" ]; then
  echo "→ sirviendo en http://localhost:8765 (Ctrl+C para cortar)"
  ( cd dist && python3 -m http.server 8765 )
fi
