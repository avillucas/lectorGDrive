#!/bin/bash
# Ejecuta el script para filtrar objetos con prefijo "articulos en revistas -" desde fuente_agente.json usando Docker

# Cargar variables de entorno desde .env si existe
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "📄 Iniciando filtrado de artículos en revistas desde fuente_agente.json..."

# Verificar que existe el archivo fuente
if [ ! -f "salida/fuente_agente.json" ]; then
    echo "❌ Error: No se encuentra salida/fuente_agente.json"
    echo "   Ejecuta primero el script para generar fuente_agente.json"
    exit 1
fi

echo "🐳 Ejecutando filtrado usando Docker..."

docker run -it \
  -v $(pwd):/app \
  -w /app \
  lector_gdrive \
  python -u lector_gdrive/filtrar_audios.py

# Verificar que se creó el archivo de salida
if [ -f "salida/salida.audios.json" ]; then
    echo ""
    echo "✅ Filtrado completado exitosamente"
    echo "📄 Archivo generado: salida/salida.audios.json"
    
    # Mostrar información del archivo generado si jq está disponible
    if command -v jq &> /dev/null; then
        AUDIOS_COUNT=$(jq length salida/salida.audios.json 2>/dev/null || echo "?")
        echo "📊 Cantidad de audios procesados: $AUDIOS_COUNT"
    fi

    FILE_SIZE=$(du -h salida/salida.audios.json | cut -f1)
    echo "💾 Tamaño del archivo: $FILE_SIZE"
else
    echo "❌ Error: No se pudo generar el archivo de salida"
    exit 1
fi

echo ""
echo "🎉 Proceso finalizado"
