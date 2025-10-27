#!/bin/bash
# Ejecuta el filtrado de libros desde fuente_agente.json

# Cargar variables de entorno desde .env si existe
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "📖 Iniciando filtrado de libros..."
echo "📄 Extrayendo objetos con 'file' que inicie con 'libros -'"
echo "🎯 Destino: salida/salida.libros.json"

# Crear directorio de salida si no existe
mkdir -p salida

echo "🐳 Ejecutando filtrado usando Docker..."

docker run -it \
  -v $(pwd):/app \
  -w /app \
  --rm \
  lector_gdrive \
  python -u lector_gdrive/filtrar_libros.py

# Capturar el código de salida del contenedor
EXIT_CODE=$?

echo ""
echo "📊 Resultado del filtrado:"

# Verificar que se creó el archivo de salida
if [ -f "salida/salida.libros.json" ]; then
    echo "✅ Archivo generado: salida/salida.libros.json"
    
    # Contar elementos en el archivo JSON si jq está disponible
    if command -v jq &> /dev/null; then
        LIBRO_COUNT=$(jq length salida/salida.libros.json 2>/dev/null || echo "?")
        echo "📊 Libros extraídos: $LIBRO_COUNT"
        
        # Mostrar algunos libros de muestra
        if [ "$LIBRO_COUNT" != "?" ] && [ "$LIBRO_COUNT" -gt "0" ]; then
            echo ""
            echo "📖 Muestra de libros extraídos (primeros 3):"
            jq -r '.[0:3][] | .title // .file' salida/salida.libros.json 2>/dev/null | while read -r titulo; do
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
        echo "⚠️  jq no está disponible para contar libros"
    fi
    
    FILE_SIZE=$(du -h salida/salida.libros.json 2>/dev/null | cut -f1 || echo "0B")
    echo "💾 Tamaño del archivo: $FILE_SIZE"
    
else
    echo "❌ Error: No se pudo generar el archivo de libros"
    EXIT_CODE=1
fi

# Verificar el código de salida del proceso
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "🎉 Filtrado de libros completado exitosamente"
else
    echo ""
    echo "❌ Error: El filtrado de libros falló"
    exit 1
fi