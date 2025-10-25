#!/bin/bash
# Ejecuta la corrección de títulos de contemplaciones

# Cargar variables de entorno desde .env si existe
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "🔧 Iniciando corrección de títulos de contemplaciones..."
echo "📄 Corrigiendo: salida/salida.contemplaciones.json"
echo "📚 Base de títulos: titulos/contemplaciones.json"

# Verificar que existan los archivos necesarios
if [ ! -f "salida/salida.contemplaciones.json" ]; then
    echo "❌ Error: No se encuentra salida/salida.contemplaciones.json"
    echo "💡 Ejecuta primero: ./shell/run_filtrar_contemplaciones.sh"
    exit 1
fi

if [ ! -f "titulos/contemplaciones.json" ]; then
    echo "❌ Error: No se encuentra titulos/contemplaciones.json"
    echo "💡 Verifica que el archivo de títulos exista"
    exit 1
fi

echo "🐳 Ejecutando corrección usando Docker..."

docker run -it \
  -v $(pwd):/app \
  -w /app \
  --rm \
  lector_gdrive \
  python -u lector_gdrive/corregir_titulos_contemplaciones.py

# Capturar el código de salida del contenedor
EXIT_CODE=$?

echo ""
echo "📊 Resultado de la corrección:"

# Verificar que se actualizó el archivo
if [ $EXIT_CODE -eq 0 ] && [ -f "salida/salida.contemplaciones.json" ]; then
    echo "✅ Archivo corregido: salida/salida.contemplaciones.json"
    
    # Contar elementos en el archivo JSON si jq está disponible
    if command -v jq &> /dev/null; then
        CONTEMPLACION_COUNT=$(jq length salida/salida.contemplaciones.json 2>/dev/null || echo "?")
        echo "📊 Contemplaciones procesadas: $CONTEMPLACION_COUNT"
        
        # Mostrar algunas contemplaciones corregidas de muestra
        if [ "$CONTEMPLACION_COUNT" != "?" ] && [ "$CONTEMPLACION_COUNT" -gt "0" ]; then
            echo ""
            echo "📿 Muestra de títulos corregidos (primeras 3):"
            jq -r '.[0:3][] | "• \(.title)"' salida/salida.contemplaciones.json 2>/dev/null | while read -r titulo; do
                echo "   $titulo"
            done 2>/dev/null
        fi
    else
        echo "⚠️  jq no está disponible para mostrar estadísticas"
    fi
    
    FILE_SIZE=$(du -h salida/salida.contemplaciones.json 2>/dev/null | cut -f1 || echo "0B")
    echo "💾 Tamaño del archivo: $FILE_SIZE"
    
else
    echo "❌ Error: No se pudo corregir el archivo de contemplaciones"
    EXIT_CODE=1
fi

# Verificar el código de salida del proceso
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "🎉 Corrección de títulos completada exitosamente"
else
    echo ""
    echo "❌ Error: La corrección de títulos falló"
    exit 1
fi
