#!/bin/bash
# Ejecuta el filtrado de videos desde fuente_agente.json

# Cargar variables de entorno desde .env si existe
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "🎥 Iniciando filtrado de videos..."
echo "📄 Extrayendo objetos con 'file' que inicie con 'videos -'"
echo "🎯 Destino: salida/salida.videos.json"

# Crear directorio de salida si no existe
mkdir -p salida

echo "🐳 Ejecutando filtrado usando Docker..."

docker run -it \
  -v $(pwd):/app \
  -w /app \
  --rm \
  lector_gdrive \
  python -u lector_gdrive/filtrar_videos.py

# Capturar el código de salida del contenedor
EXIT_CODE=$?

echo ""
echo "📊 Resultado del filtrado:"

# Verificar que se creó el archivo de salida
if [ -f "salida/salida.videos.json" ]; then
    echo "✅ Archivo generado: salida/salida.videos.json"
    
    # Contar elementos en el archivo JSON si jq está disponible
    if command -v jq &> /dev/null; then
        VIDEO_COUNT=$(jq length salida/salida.videos.json 2>/dev/null || echo "?")
        echo "📊 Videos extraídos: $VIDEO_COUNT"
        
        # Mostrar algunos videos de muestra
        if [ "$VIDEO_COUNT" != "?" ] && [ "$VIDEO_COUNT" -gt "0" ]; then
            echo ""
            echo "🎥 Muestra de videos extraídos (primeros 3):"
            jq -r '.[0:3][] | .title // .file' salida/salida.videos.json 2>/dev/null | while read -r titulo; do
                # Truncar título si es muy largo
                if [ ${#titulo} -gt 70 ]; then
                    titulo_truncado="${titulo:0:70}..."
                else
                    titulo_truncado="$titulo"
                fi
                echo "   • $titulo_truncado"
            done 2>/dev/null
        fi
    else
        echo "⚠️  jq no está disponible para contar videos"
    fi
    
    FILE_SIZE=$(du -h salida/salida.videos.json 2>/dev/null | cut -f1 || echo "0B")
    echo "💾 Tamaño del archivo: $FILE_SIZE"
    
else
    echo "❌ Error: No se pudo generar el archivo de videos"
    EXIT_CODE=1
fi

# Verificar el código de salida del proceso
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "🎉 Filtrado de videos completado exitosamente"
else
    echo ""
    echo "❌ Error: El filtrado de videos falló"
    exit 1
fi
