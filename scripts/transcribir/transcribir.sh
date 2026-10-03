#!/usr/bin/env bash
# Transcribe audios en español. Funciona en la nube de Claude, donde Hugging Face está bloqueado:
# el modelo se instala desde npm (sts-whisper-small). Necesita node y ffmpeg.
# La primera vez instala ~300 MB en $STT_DIR (por defecto ~/.stt). Tarda ~1 minuto por minuto de audio.
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
export STT_DIR="${STT_DIR:-$HOME/.stt}"
mkdir -p "$STT_DIR"
if [ ! -d "$STT_DIR/node_modules/sts-whisper-small" ]; then
  (cd "$STT_DIR" && [ -f package.json ] || npm init -y >/dev/null)
  (cd "$STT_DIR" && npm install --ignore-scripts --silent sts-whisper-small @huggingface/transformers)
fi
ABS=(); for a in "$@"; do ABS+=("$(cd "$(dirname "$a")" && pwd)/$(basename "$a")"); done
cp "$AQUI/transcribir.mjs" "$STT_DIR/transcribir.mjs"
cd "$STT_DIR" && node transcribir.mjs "${ABS[@]}"
