#!/bin/bash
# Empuja a GitHub los commits que quedaron sin subir en la torre de control.
# Lo corre launchd cada cinco minutos. No hace merge, no fuerza nada:
# si el remoto se adelantó, lo anota y se va.

REPO="$HOME/Documents/torre-de-control-cascara-founders"
LOG="$HOME/Library/Logs/torre-autopush.log"
GIT=/usr/bin/git

decir(){ echo "$(date '+%Y-%m-%d %H:%M') · $1" >> "$LOG"; }

[ -d "$REPO/.git" ] || { decir "no encuentro el repo en $REPO"; exit 0; }
cd "$REPO" || exit 0

# cuántos commits locales no están arriba, según lo último que sabemos del remoto
PEND=$("$GIT" rev-list --count @{u}..HEAD 2>/dev/null) || exit 0
[ "${PEND:-0}" -eq 0 ] && exit 0

decir "hay $PEND commit(s) sin subir, empujando"
SALIDA=$("$GIT" push origin main 2>&1)
if [ $? -eq 0 ]; then
  decir "listo: $PEND commit(s) arriba"
else
  decir "no pude empujar. $(echo "$SALIDA" | tail -2 | tr '\n' ' ')"
fi
