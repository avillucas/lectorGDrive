#!/bin/bash
# Ejecuta la limpieza de duplicados en fuente_agente.json

# Cargar variables de entorno desde .env si existe
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "🧹 Iniciando limpieza de duplicados en fuente_agente.json..."
echo "🎯 Detectando elementos con títulos duplicados"
echo "📄 Guardando duplicados en: salida/duplicados_eliminados.json"
echo "✨ Generando archivo limpio: salida/fuente_agente_limpio.json"

# Crear directorio de salida si no existe
mkdir -p salida

# Verificar que existe el archivo fuente
if [ ! -f "salida/fuente_agente.json" ]; then
    echo "❌ No se encuentra salida/fuente_agente.json"
    echo "💡 Asegúrate de haber generado el archivo base primero:"
    echo "   ./shell/run_genera_fuente_agente.sh"
    exit 1
fi

echo ""
echo "📊 Estado actual del archivo:"
if command -v jq &> /dev/null; then
    ELEMENTOS_ORIGINAL=$(jq length salida/fuente_agente.json 2>/dev/null || echo "?")
    echo "   📄 Elementos en fuente_agente.json: $ELEMENTOS_ORIGINAL"
else
    echo "   ⚠️  jq no disponible para mostrar estadísticas"
fi

echo ""
echo "🐳 Ejecutando limpieza usando Docker..."

docker run -it \
  -v $(pwd):/app \
  -w /app \
  --rm \
  lector_gdrive \
  python -u lector_gdrive/limpiar_duplicados.py

# Capturar el código de salida del contenedor
EXIT_CODE=$?

echo ""
echo "📊 Resultado de la limpieza:"

# Verificar que se crearon los archivos
if [ -f "salida/fuente_agente_limpio.json" ] && [ -f "salida/duplicados_eliminados.json" ]; then
    echo "✅ Archivos generados exitosamente"
    
    # Contar elementos si jq está disponible
    if command -v jq &> /dev/null; then
        ELEMENTOS_LIMPIO=$(jq length salida/fuente_agente_limpio.json 2>/dev/null || echo "?")
        DUPLICADOS_ELIMINADOS=$(jq '.resumen.total_duplicados_eliminados' salida/duplicados_eliminados.json 2>/dev/null || echo "?")
        
        echo "📊 Elementos en archivo limpio: $ELEMENTOS_LIMPIO"
        echo "🗑️  Duplicados eliminados: $DUPLICADOS_ELIMINADOS"
        
        if [ "$ELEMENTOS_ORIGINAL" != "?" ] && [ "$ELEMENTOS_LIMPIO" != "?" ] && [ "$DUPLICADOS_ELIMINADOS" != "?" ]; then
            SUMA=$((ELEMENTOS_LIMPIO + DUPLICADOS_ELIMINADOS))
            if [ $SUMA -eq $ELEMENTOS_ORIGINAL ]; then
                echo "✅ Verificación correcta: $ELEMENTOS_LIMPIO + $DUPLICADOS_ELIMINADOS = $ELEMENTOS_ORIGINAL"
            else
                echo "⚠️  Discrepancia en números: $ELEMENTOS_LIMPIO + $DUPLICADOS_ELIMINADOS ≠ $ELEMENTOS_ORIGINAL"
            fi
        fi
        
        # Mostrar algunos ejemplos de duplicados
        echo ""
        echo "🔍 Ejemplos de duplicados eliminados:"
        jq -r '.duplicados_eliminados[0:3][] | "   • " + .titulo_duplicado[0:60] + "..."' salida/duplicados_eliminados.json 2>/dev/null || echo "   (no disponible sin jq)"
        
    else
        echo "⚠️  jq no está disponible para mostrar estadísticas detalladas"
    fi
    
    # Mostrar tamaños de archivos
    FILE_SIZE_LIMPIO=$(du -h salida/fuente_agente_limpio.json 2>/dev/null | cut -f1 || echo "?")
    FILE_SIZE_DUPLICADOS=$(du -h salida/duplicados_eliminados.json 2>/dev/null | cut -f1 || echo "?")
    echo "💾 Tamaño archivo limpio: $FILE_SIZE_LIMPIO"
    echo "🗑️  Tamaño archivo duplicados: $FILE_SIZE_DUPLICADOS"
    
else
    echo "❌ Error: No se pudieron generar los archivos de limpieza"
    EXIT_CODE=1
fi

# Verificar el código de salida del proceso
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "🎉 Limpieza de duplicados completada exitosamente"
    echo ""
    echo "📋 Próximos pasos:"
    echo "   1. Revisar: salida/fuente_agente_limpio.json"
    echo "   2. Verificar: salida/duplicados_eliminados.json"
    echo "   3. Si todo está correcto, hacer:"
    echo "      mv salida/fuente_agente.json salida/fuente_agente_backup.json"
    echo "      mv salida/fuente_agente_limpio.json salida/fuente_agente.json"
else
    echo ""
    echo "❌ Error: La limpieza de duplicados falló"
    exit 1
fi
