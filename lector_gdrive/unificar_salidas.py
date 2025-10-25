import json
import os
import glob
from pathlib import Path

def unificar_salidas():
    """
    Unifica todos los archivos salida/salida.*.json en un solo archivo
    salida/fuente_agente_v2.json y compara con fuente_agente.json
    """
    
    # Rutas de archivos
    patron_salidas = 'salida/salida.*.json'
    archivo_unificado = 'salida/fuente_agente_v2.json'
    archivo_original = 'salida/fuente_agente.json'
    
    print("🔗 Unificando archivos de salida...")
    print(f"📁 Patrón de búsqueda: {patron_salidas}")
    print(f"💾 Archivo destino: {archivo_unificado}")
    print(f"📊 Archivo para comparar: {archivo_original}")
    
    try:
        # Buscar todos los archivos que coincidan con el patrón
        archivos_salida = glob.glob(patron_salidas)
        
        if not archivos_salida:
            print(f"❌ No se encontraron archivos con el patrón: {patron_salidas}")
            return False
        
        print(f"\n📂 Archivos encontrados ({len(archivos_salida)}):")
        for archivo in sorted(archivos_salida):
            print(f"   • {archivo}")
        
        # Unificar contenidos
        contenido_unificado = []
        estadisticas = {}
        
        for archivo in sorted(archivos_salida):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                # Verificar que sea una lista
                if not isinstance(datos, list):
                    print(f"⚠️  {archivo} no contiene una lista, saltando...")
                    continue
                
                # Agregar al contenido unificado
                contenido_unificado.extend(datos)
                
                # Estadísticas por archivo
                nombre_archivo = os.path.basename(archivo)
                estadisticas[nombre_archivo] = len(datos)
                
                print(f"   ✅ {nombre_archivo}: {len(datos)} elementos")
                
            except json.JSONDecodeError as e:
                print(f"   ❌ Error JSON en {archivo}: {e}")
                continue
            except Exception as e:
                print(f"   ❌ Error leyendo {archivo}: {e}")
                continue
        
        # Crear directorio de salida si no existe
        Path(archivo_unificado).parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar archivo unificado
        with open(archivo_unificado, 'w', encoding='utf-8') as f:
            json.dump(contenido_unificado, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 Resumen de unificación:")
        print(f"   📁 Archivos procesados: {len(estadisticas)}")
        print(f"   📄 Total elementos unificados: {len(contenido_unificado)}")
        print(f"   💾 Archivo generado: {archivo_unificado}")
        
        # Mostrar estadísticas detalladas
        if estadisticas:
            print(f"\n📈 Desglose por archivo:")
            total_verificacion = 0
            for archivo, cantidad in estadisticas.items():
                porcentaje = (cantidad / len(contenido_unificado) * 100) if len(contenido_unificado) > 0 else 0
                print(f"   • {archivo}: {cantidad} elementos ({porcentaje:.1f}%)")
                total_verificacion += cantidad
            
            print(f"   📊 Total verificación: {total_verificacion}")
            if total_verificacion == len(contenido_unificado):
                print(f"   ✅ Verificación correcta")
            else:
                print(f"   ❌ Error en verificación")
        
        # Comparar con archivo original si existe
        if os.path.exists(archivo_original):
            print(f"\n🔍 Comparación con archivo original:")
            try:
                with open(archivo_original, 'r', encoding='utf-8') as f:
                    datos_originales = json.load(f)
                
                cantidad_original = len(datos_originales) if isinstance(datos_originales, list) else 0
                cantidad_nueva = len(contenido_unificado)
                diferencia = cantidad_nueva - cantidad_original
                
                print(f"   📊 Archivo original: {cantidad_original} elementos")
                print(f"   📊 Archivo nuevo: {cantidad_nueva} elementos")
                print(f"   📈 Diferencia: {diferencia:+d} elementos")
                
                if diferencia == 0:
                    print(f"   ✅ Misma cantidad de elementos")
                elif diferencia > 0:
                    print(f"   📈 {diferencia} elementos adicionales en la nueva versión")
                else:
                    print(f"   📉 {abs(diferencia)} elementos menos en la nueva versión")
                
                # Verificar porcentaje de coincidencia
                porcentaje_cambio = abs(diferencia) / cantidad_original * 100 if cantidad_original > 0 else 0
                print(f"   📊 Porcentaje de cambio: {porcentaje_cambio:.2f}%")
                
            except Exception as e:
                print(f"   ❌ Error comparando con archivo original: {e}")
        else:
            print(f"\n⚠️  Archivo original no encontrado: {archivo_original}")
        
        # Mostrar tamaño del archivo generado
        if os.path.exists(archivo_unificado):
            file_size = os.path.getsize(archivo_unificado)
            file_size_mb = file_size / (1024 * 1024)
            print(f"💾 Tamaño del archivo unificado: {file_size_mb:.2f} MB")
        
        # Mostrar algunos ejemplos del contenido unificado
        if contenido_unificado:
            print(f"\n📄 Muestra del contenido unificado (primeros 3 elementos):")
            for i, elemento in enumerate(contenido_unificado[:3], 1):
                titulo = elemento.get('title', elemento.get('file', 'Sin título'))[:60]
                tipo_archivo = elemento.get('file', '').split(' - ')[0] if ' - ' in elemento.get('file', '') else 'desconocido'
                print(f"   {i}. [{tipo_archivo}] {titulo}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🔄 Iniciando unificación de archivos de salida")
    
    exito = unificar_salidas()
    
    if exito:
        print("\n🎉 Unificación completada exitosamente!")
    else:
        print("\n❌ La unificación falló")
        exit(1)

if __name__ == "__main__":
    main()
