#!/bin/bash
# Script maestro que ejecuta todo el pipeline de procesamiento en orden

set -e  # Salir si hay algún error

echo "🚀 INICIANDO PIPELINE COMPLETO DE PROCESAMIENTO"
echo "=============================================="
echo "📅 Fecha: $(date)"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging con timestamp
log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%H:%M:%S')] ERROR:${NC} $1"
}

warning() {
    echo -e "${YELLOW}[$(date +'%H:%M:%S')] WARNING:${NC} $1"
}

info() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')] INFO:${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "shell/run_pipeline_completo.sh" ]; then
    error "Debe ejecutar este script desde el directorio raíz del proyecto (/home/lucas/divit/lectorGDrive)"
    exit 1
fi

# Crear directorios necesarios
log "📁 Creando directorios necesarios..."
mkdir -p cache
mkdir -p salida
mkdir -p titulos

# Paso 1: Generar fuente_agente.json base
log "📋 PASO 1: Generando fuente_agente.json base"
echo "============================================"
if [ -x "shell/run_genera_fuente_agente.sh" ]; then
    ./shell/run_genera_fuente_agente.sh
    if [ $? -eq 0 ]; then
        log "✅ fuente_agente.json generado exitosamente"
    else
        error "❌ Falló la generación de fuente_agente.json"
        exit 1
    fi
else
    error "❌ No se encuentra shell/run_genera_fuente_agente.sh o no es ejecutable"
    exit 1
fi

echo ""

# Paso 2: Filtrar contemplaciones
log "📿 PASO 2: Filtrando contemplaciones"
echo "===================================="
if [ -x "shell/run_filtrar_contemplaciones.sh" ]; then
    ./shell/run_filtrar_contemplaciones.sh
    if [ $? -eq 0 ]; then
        log "✅ Contemplaciones filtradas exitosamente"
    else
        warning "⚠️  Error filtrando contemplaciones, continuando..."
    fi
else
    warning "⚠️  No se encuentra shell/run_filtrar_contemplaciones.sh"
fi

echo ""

# Paso 3: Corregir títulos de contemplaciones (si existe el archivo de títulos)
if [ -f "titulos/contemplaciones.json" ]; then
    log "🔧 PASO 3a: Corrigiendo títulos de contemplaciones"
    echo "==============================================="
    if [ -x "shell/run_corregir_titulos_contemplaciones.sh" ]; then
        ./shell/run_corregir_titulos_contemplaciones.sh
        if [ $? -eq 0 ]; then
            log "✅ Títulos de contemplaciones corregidos"
        else
            warning "⚠️  Error corrigiendo títulos de contemplaciones"
        fi
    else
        warning "⚠️  No se encuentra shell/run_corregir_titulos_contemplaciones.sh"
    fi
else
    info "ℹ️  No se encuentra titulos/contemplaciones.json, saltando corrección de títulos"
fi

echo ""

# Paso 4: Filtrar artículos (talleres)
log "📚 PASO 4: Filtrando artículos/talleres"
echo "======================================"
if [ -x "shell/run_filtrar_articulos.sh" ]; then
    ./shell/run_filtrar_articulos.sh
    if [ $? -eq 0 ]; then
        log "✅ Artículos/talleres filtrados exitosamente"
    else
        warning "⚠️  Error filtrando artículos, continuando..."
    fi
else
    warning "⚠️  No se encuentra shell/run_filtrar_articulos.sh"
fi

echo ""

# Paso 5: Corregir títulos de talleres (si existe el archivo de títulos)
if [ -f "titulos/ejercicios_espirituales.json" ]; then
    log "🔧 PASO 5a: Corrigiendo títulos de talleres"
    echo "=========================================="
    if [ -x "shell/run_corregir_titulos_talleres.sh" ]; then
        ./shell/run_corregir_titulos_talleres.sh
        if [ $? -eq 0 ]; then
            log "✅ Títulos de talleres corregidos"
        else
            warning "⚠️  Error corrigiendo títulos de talleres"
        fi
    else
        warning "⚠️  No se encuentra shell/run_corregir_titulos_talleres.sh"
    fi
else
    info "ℹ️  No se encuentra titulos/ejercicios_espirituales.json, saltando corrección de títulos"
fi

echo ""

# Paso 6: Filtrar audios (si existe el script)
if [ -x "shell/run_filtrar_audios.sh" ]; then
    log "🔊 PASO 6: Filtrando audios"
    echo "============================"
    ./shell/run_filtrar_audios.sh
    if [ $? -eq 0 ]; then
        log "✅ Audios filtrados exitosamente"
    else
        warning "⚠️  Error filtrando audios, continuando..."
    fi
else
    info "ℹ️  No se encuentra shell/run_filtrar_audios.sh, saltando filtrado de audios"
fi

echo ""

# Paso 7: Filtrar libros (si existe el script)
if [ -x "shell/run_filtrar_libros.sh" ]; then
    log "📖 PASO 7: Filtrando libros"
    echo "============================"
    ./shell/run_filtrar_libros.sh
    if [ $? -eq 0 ]; then
        log "✅ Libros filtrados exitosamente"
    else
        warning "⚠️  Error filtrando libros, continuando..."
    fi
else
    info "ℹ️  No se encuentra shell/run_filtrar_libros.sh, saltando filtrado de libros"
fi

echo ""

# Paso 8: Filtrar videos (si existe el script)
if [ -x "shell/run_filtrar_videos.sh" ]; then
    log "🎥 PASO 8: Filtrando videos"
    echo "============================"
    ./shell/run_filtrar_videos.sh
    if [ $? -eq 0 ]; then
        log "✅ Videos filtrados exitosamente"
    else
        warning "⚠️  Error filtrando videos, continuando..."
    fi
else
    info "ℹ️  No se encuentra shell/run_filtrar_videos.sh, saltando filtrado de videos"
fi

echo ""

# Paso 9: Unificar todos los archivos filtrados
log "🔗 PASO 9: Unificando todos los archivos filtrados"
echo "================================================="
if [ -x "shell/run_unificar_salidas.sh" ]; then
    ./shell/run_unificar_salidas.sh
    if [ $? -eq 0 ]; then
        log "✅ Archivos unificados exitosamente en fuente_agente_v2.json"
    else
        error "❌ Error unificando archivos"
        exit 1
    fi
else
    error "❌ No se encuentra shell/run_unificar_salidas.sh"
    exit 1
fi

echo ""

# Paso 10: Estadísticas finales y verificación
log "📊 PASO 10: Estadísticas finales y verificación"
echo "=============================================="

# Verificar archivos generados
info "📂 Archivos generados en el directorio salida/:"
if [ -d "salida" ]; then
    for archivo in salida/*.json; do
        if [ -f "$archivo" ]; then
            ELEMENTOS=""
            TAMAÑO=""
            
            if command -v jq &> /dev/null; then
                ELEMENTOS=$(jq length "$archivo" 2>/dev/null || echo "?")
            fi
            
            TAMAÑO=$(du -h "$archivo" 2>/dev/null | cut -f1 || echo "?")
            echo "   ✅ $(basename "$archivo"): $ELEMENTOS elementos ($TAMAÑO)"
        fi
    done
else
    warning "⚠️  No se encuentra el directorio salida/"
fi

echo ""

# Verificar archivos de salida específicos
info "🔍 Verificación de archivos específicos:"

# fuente_agente.json original
if [ -f "salida/fuente_agente.json" ]; then
    if command -v jq &> /dev/null; then
        ELEMENTOS_ORIGINAL=$(jq length salida/fuente_agente.json 2>/dev/null || echo "?")
    else
        ELEMENTOS_ORIGINAL="?"
    fi
    TAMAÑO_ORIGINAL=$(du -h salida/fuente_agente.json 2>/dev/null | cut -f1 || echo "?")
    echo "   📋 fuente_agente.json: $ELEMENTOS_ORIGINAL elementos ($TAMAÑO_ORIGINAL)"
else
    error "❌ No se encuentra salida/fuente_agente.json"
fi

# fuente_agente_v2.json unificado
if [ -f "salida/fuente_agente_v2.json" ]; then
    if command -v jq &> /dev/null; then
        ELEMENTOS_V2=$(jq length salida/fuente_agente_v2.json 2>/dev/null || echo "?")
    else
        ELEMENTOS_V2="?"
    fi
    TAMAÑO_V2=$(du -h salida/fuente_agente_v2.json 2>/dev/null | cut -f1 || echo "?")
    echo "   📋 fuente_agente_v2.json: $ELEMENTOS_V2 elementos ($TAMAÑO_V2)"
    
    # Comparar si ambos existen
    if [ "$ELEMENTOS_ORIGINAL" != "?" ] && [ "$ELEMENTOS_V2" != "?" ]; then
        if [ "$ELEMENTOS_ORIGINAL" = "$ELEMENTOS_V2" ]; then
            log "✅ Misma cantidad de elementos en ambas versiones"
        else
            DIFERENCIA=$((ELEMENTOS_V2 - ELEMENTOS_ORIGINAL))
            if [ $DIFERENCIA -gt 0 ]; then
                info "📈 fuente_agente_v2.json tiene $DIFERENCIA elementos adicionales"
            else
                warning "📉 fuente_agente_v2.json tiene ${DIFERENCIA#-} elementos menos"
            fi
        fi
    fi
else
    error "❌ No se encuentra salida/fuente_agente_v2.json"
fi

echo ""

# Verificar archivos filtrados individuales
info "📋 Archivos filtrados individuales:"
for tipo in contemplaciones talleres audios libros videos; do
    archivo="salida/salida.${tipo}.json"
    if [ -f "$archivo" ]; then
        if command -v jq &> /dev/null; then
            ELEMENTOS=$(jq length "$archivo" 2>/dev/null || echo "?")
        else
            ELEMENTOS="?"
        fi
        TAMAÑO=$(du -h "$archivo" 2>/dev/null | cut -f1 || echo "?")
        echo "   📄 salida.${tipo}.json: $ELEMENTOS elementos ($TAMAÑO)"
    else
        echo "   ❌ No se encuentra salida.${tipo}.json"
    fi
done

echo ""

# Tiempo total de ejecución
TIEMPO_TOTAL=$SECONDS
MINUTOS=$((TIEMPO_TOTAL / 60))
SEGUNDOS=$((TIEMPO_TOTAL % 60))

log "🎉 PIPELINE COMPLETO FINALIZADO"
echo "==============================="
echo "⏱️  Tiempo total: ${MINUTOS}m ${SEGUNDOS}s"
echo "📅 Finalizado: $(date)"
echo ""

if [ -f "salida/fuente_agente_v2.json" ]; then
    log "✅ Pipeline ejecutado exitosamente"
    echo "🔗 Archivo principal generado: salida/fuente_agente_v2.json"
    echo ""
    echo "📋 Próximos pasos sugeridos:"
    echo "   1. Revisar salida/fuente_agente_v2.json"
    echo "   2. Verificar que los títulos estén correctamente corregidos"
    echo "   3. Usar el archivo para tu aplicación final"
else
    error "❌ Pipeline completado con errores"
    echo "🔍 Revisa los mensajes de error anteriores"
    exit 1
fi
