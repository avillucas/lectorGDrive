#!/bin/bash
# Ejecuta el script para actualizar títulos de libros desde libros.csv usando Docker

# Cargar variables de entorno desde .env si existe
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Permitir personalizar rutas por argumentos
FUENTE_PATH_ARG=""
OUTPUT_PATH_ARG=""

# Primer argumento: archivo fuente_agente.json
if [ ! -z "$1" ]; then
  FUENTE_PATH_ARG="--fuente_path $1"
fi

# Segundo argumento: archivo de salida
if [ ! -z "$2" ]; then
  OUTPUT_PATH_ARG="--output_path $2"
fi

echo "📚 Ejecutando actualización de títulos de libros desde CSV..."
echo "📁 Archivo CSV: titulos/libros.csv"

docker run -it \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd):/app \
  -w /app \
  lector_gdrive \
  python -u lector_gdrive/actualizar_titulos_libros.py $FUENTE_PATH_ARG $OUTPUT_PATH_ARG
