#!/bin/bash
# Ejecuta la unificación de archivos de salida

# Cargar variables de entorno desde .env si existe
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "🔗 Iniciando unificación de archivos de salida..."
echo "📁 Buscando archivos: salida/salida.*.json"
echo "💾 Archivo destino: salida/fuente_agente_v2.json"
echo "📊 Comparación con: salida/fuente_agente.json"

# Crear directorio de salida si no existe
mkdir -p salida

# Verificar que existan archivos de salida
if ls salida/salida.*.json 1> /dev/null 2>&1; then
    echo "✅ Archivos de salida encontrados:"
    for archivo in salida/salida.*.json; do
        if [ -f "$archivo" ]; then
            ELEMENTOS=$(jq length "$archivo" 2>/dev/null || echo "?")
            TAMAÑO=$(du -h "$archivo" 2>/dev/null | cut -f1 || echo "?")
            echo "   • $(basename "$archivo"): $ELEMENTOS elementos ($TAMAÑO)"
        fi
    done
else
    echo "❌ No se encontraron archivos salida/salida.*.json"
    echo "💡 Asegúrate de haber ejecutado los filtrados primero:"
    echo "   ./shell/run_filtrar_contemplaciones.sh"
    echo "   ./shell/run_filtrar_articulos.sh"
    echo "   etc."
    exit 1
fi

echo ""
echo "🐳 Ejecutando unificación usando Docker..."

docker run -it \
  -v $(pwd):/app \
  -w /app \
  --rm \
  lector_gdrive \
  python -u lector_gdrive/unificar_salidas.py

# Capturar el código de salida del contenedor
EXIT_CODE=$?

echo ""
echo "📊 Resultado de la unificación:"

# Verificar que se creó el archivo unificado
if [ -f "salida/fuente_agente_v2.json" ]; then
    echo "✅ Archivo unificado generado: salida/fuente_agente_v2.json"
    
    # Contar elementos si jq está disponible
    if command -v jq &> /dev/null; then
        ELEMENTOS_V2=$(jq length salida/fuente_agente_v2.json 2>/dev/null || echo "?")
        echo "📊 Elementos en fuente_agente_v2.json: $ELEMENTOS_V2"
        
        # Comparar con archivo original si existe
        if [ -f "salida/fuente_agente.json" ]; then
            ELEMENTOS_ORIGINAL=$(jq length salida/fuente_agente.json 2>/dev/null || echo "?")
            echo "📊 Elementos en fuente_agente.json: $ELEMENTOS_ORIGINAL"
            
            if [ "$ELEMENTOS_V2" != "?" ] && [ "$ELEMENTOS_ORIGINAL" != "?" ]; then
                DIFERENCIA=$((ELEMENTOS_V2 - ELEMENTOS_ORIGINAL))
                if [ $DIFERENCIA -eq 0 ]; then
                    echo "✅ Misma cantidad de elementos"
                elif [ $DIFERENCIA -gt 0 ]; then
                    echo "📈 +$DIFERENCIA elementos adicionales"
                else
                    echo "📉 $DIFERENCIA elementos menos"
                fi
            fi
        else
            echo "⚠️  Archivo fuente_agente.json no encontrado para comparar"
        fi
        
        # Mostrar distribución por tipo si es posible
        echo ""
        echo "📂 Distribución por tipo de contenido:"
        jq -r '.[] | .file' salida/fuente_agente_v2.json 2>/dev/null | \
        sed 's/ - .*//' | sort | uniq -c | sort -nr | head -10 | \
        while read count tipo; do
            echo "   • $tipo: $count elementos"
        done 2>/dev/null || echo "   (no disponible sin jq)"
        
    else
        echo "⚠️  jq no está disponible para mostrar estadísticas detalladas"
    fi
    
    FILE_SIZE=$(du -h salida/fuente_agente_v2.json 2>/dev/null | cut -f1 || echo "0B")
    echo "💾 Tamaño del archivo unificado: $FILE_SIZE"
    
else
    echo "❌ Error: No se pudo generar el archivo unificado"
    EXIT_CODE=1
fi

# Verificar el código de salida del proceso
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "🎉 Unificación completada exitosamente"
    echo "💡 Archivo generado: salida/fuente_agente_v2.json"
    echo "🔄 Este archivo contiene todos los elementos de los archivos salida/salida.*.json"
else
    echo ""
    echo "❌ Error: La unificación falló"
    exit 1
fi
