#!/bin/bash
# Genera libros_corregidos.json corrigiendo títulos desde libros.csv usando Docker

# Cargar variables de entorno desde .env si existe
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "📚 Generando libros corregidos desde CSV..."
echo "📁 Archivo de entrada: salida/salida.libros.json"
echo "📁 Archivo CSV: titulos/libros.csv"
echo "📁 Archivo de salida: salida/libros_corregidos.json"

# Verificar que existen los archivos necesarios
if [ ! -f "salida/salida.libros.json" ]; then
    echo "❌ No se encuentra salida/salida.libros.json"
    echo "💡 Ejecuta primero el filtrado de libros"
    exit 1
fi

if [ ! -f "titulos/libros.csv" ]; then
    echo "❌ No se encuentra titulos/libros.csv"
    echo "💡 Asegúrate de tener el archivo CSV con los títulos correctos"
    exit 1
fi

echo "🐳 Ejecutando corrección de títulos usando Docker..."

# Ejecutar el script Python usando Docker
docker run -it \
  -v $(pwd):/app \
  -w /app \
  lector_gdrive \
  python -u lector_gdrive/generar_libros_corregidos.py

if [ $? -eq 0 ]; then
    echo "✅ Proceso completado exitosamente"
    echo "📁 Revisa el archivo: salida/libros_corregidos.json"
else
    echo "❌ Error en el proceso"
    exit 1
fi
