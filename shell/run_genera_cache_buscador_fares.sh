#!/bin/bash
# Ejecuta el script para generar el cache de BUSCADOR FARES usando Docker

docker run -it \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd):/app \
  -w /app \
  lector_gdrive \
  python -u lector_gdrive/genera_cache_buscador_fares.py
