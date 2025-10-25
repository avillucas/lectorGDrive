#!/bin/bash
# Ejecuta la corrección de títulos de talleres

# Cargar variables de entorno desde .env si existe
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "🔧 Iniciando corrección de títulos de talleres..."
echo "📄 Corrigiendo: salida/salida.talleres.json"
echo "📚 Base de títulos: titulos/ejercicios_espirituales.json"

# Verificar que existan los archivos necesarios
if [ ! -f "salida/salida.talleres.json" ]; then
    echo "❌ Error: No se encuentra salida/salida.talleres.json"
    echo "💡 Ejecuta primero: ./shell/run_filtrar_articulos.sh"
    exit 1
fi

if [ ! -f "titulos/ejercicios_espirituales.json" ]; then
    echo "❌ Error: No se encuentra titulos/ejercicios_espirituales.json"
    echo "💡 Verifica que el archivo de títulos de ejercicios espirituales exista"
    exit 1
fi

echo "🐳 Ejecutando corrección usando Docker..."

docker run -it \
  -v $(pwd):/app \
  -w /app \
  --rm \
  lector_gdrive \
  python -u lector_gdrive/corregir_titulos_talleres.py

# Capturar el código de salida del contenedor
EXIT_CODE=$?

echo ""
echo "📊 Resultado de la corrección:"

# Verificar que se actualizó el archivo
if [ $EXIT_CODE -eq 0 ] && [ -f "salida/salida.talleres.json" ]; then
    echo "✅ Archivo corregido: salida/salida.talleres.json"
    
    # Contar elementos en el archivo JSON si jq está disponible
    if command -v jq &> /dev/null; then
        TALLER_COUNT=$(jq length salida/salida.talleres.json 2>/dev/null || echo "?")
        echo "📊 Talleres procesados: $TALLER_COUNT"
        
        # Mostrar algunos talleres corregidos de muestra
        if [ "$TALLER_COUNT" != "?" ] && [ "$TALLER_COUNT" -gt "0" ]; then
            echo ""
            echo "📚 Muestra de títulos corregidos (primeros 3):"
            jq -r '.[0:3][] | "• \(.title)"' salida/salida.talleres.json 2>/dev/null | while read -r titulo; do
                echo "   $titulo"
            done 2>/dev/null
        fi
    else
        echo "⚠️  jq no está disponible para mostrar estadísticas"
    fi
    
    FILE_SIZE=$(du -h salida/salida.talleres.json 2>/dev/null | cut -f1 || echo "0B")
    echo "💾 Tamaño del archivo: $FILE_SIZE"
    
else
    echo "❌ Error: No se pudo corregir el archivo de talleres"
    EXIT_CODE=1
fi

# Verificar el código de salida del proceso
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "🎉 Corrección de títulos de talleres completada exitosamente"
else
    echo ""
    echo "❌ Error: La corrección de títulos de talleres falló"
    exit 1
fi
