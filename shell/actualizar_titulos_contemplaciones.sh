#!/bin/bash

# actualizar_titulos_contemplaciones.sh
# Script para actualizar títulos de contemplaciones

echo "=== Actualizando títulos de contemplaciones ==="
echo "Fecha y hora: $(date)"
echo "=========================================="

# Verificar que Python esté disponible
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no está instalado o no está disponible"
    exit 1
fi

# Obtener el directorio del script y navegar al directorio padre del proyecto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Directorio del proyecto: $PROJECT_DIR"
cd "$PROJECT_DIR"

# Verificar que existe el script de Python
if [ ! -f "actualizar_titulos_contemplaciones.py" ]; then
    echo "Error: No se encontró el archivo actualizar_titulos_contemplaciones.py en $PROJECT_DIR"
    echo "Archivos disponibles:"
    ls -la
    exit 1
fi

# Ejecutar el script de actualización de títulos
echo "Ejecutando actualización de títulos de contemplaciones..."

python3 actualizar_titulos_contemplaciones.py

# Verificar el código de salida
if [ $? -eq 0 ]; then
    echo "✅ Actualización de títulos completada exitosamente"
else
    echo "❌ Error durante la actualización de títulos"
    exit 1
fi

echo "=========================================="
echo "Proceso finalizado: $(date)"