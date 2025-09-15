#!/bin/bash
# Ejecuta el script para generar el cache de TEXTUALES usando Docker

# Cargar variables de entorno desde .env si existe
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Permite definir el directorio de textuales por variable de entorno
TEXTUALES_DIR_ARG=""
if [ ! -z "$TEXTUALES_DIR" ]; then
  TEXTUALES_DIR_ARG="--textuales_dir $TEXTUALES_DIR"
fi

docker run -it \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  -e TEXTUALES_DIR="$TEXTUALES_DIR" \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd):/app \
  -w /app \
  lector_gdrive \
  python -u lector_gdrive/genera_cache_textuales.py $TEXTUALES_DIR_ARG
