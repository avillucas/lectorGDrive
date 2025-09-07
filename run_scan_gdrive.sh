#!/bin/bash
# Ejecuta el contenedor Docker para escanear un directorio de Google Drive y guardar el CSV en ./salida

docker run -it \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd)/salida:/app/salida \
  lector_gdrive \
  python scan_gdrive_console.py
