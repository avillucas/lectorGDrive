#!/bin/bash
# Ejecuta el script para generar el cache de BUSCADOR FARES usando Docker

# Cargar variables de entorno desde .env si existe
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Permite definir el directorio de buscador fares por variable de entorno
BUSCADOR_FARES_DIR_ARG="15dAh7wicfRDK_3kjN7-O74ouSmw7NDtI"
if [ ! -z "$BUSCADOR_FARES_DIR" ]; then
  BUSCADOR_FARES_DIR_ARG="--buscador_fares_dir $BUSCADOR_FARES_DIR"
fi

docker run -it \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  -e BUSCADOR_FARES_DIR="$BUSCADOR_FARES_DIR" \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd):/app \
  -w /app \
  lector_gdrive \
  python -u lector_gdrive/genera_cache_buscador_fares.py $BUSCADOR_FARES_DIR_ARG
