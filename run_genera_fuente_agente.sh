#!/bin/bash
# Ejecuta el script para generar fuente_agente.json usando Docker

docker run -it \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd):/app \
  lector_gdrive \
  python genera_fuente_agente.py
