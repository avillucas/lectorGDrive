#!/bin/bash
# Ejecuta el script para generar el cache de TEXTUALES usando Docker

docker run -it \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd):/app \
  -w /app \
  lector_gdrive \
  python -u genera_cache_textuales.py
