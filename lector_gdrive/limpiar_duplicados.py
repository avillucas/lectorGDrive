import json
import os
from pathlib import Path
from collections import defaultdict

def detectar_y_limpiar_duplicados():
    """
    Detecta duplicados en fuente_agente.json basándose en el título,
    los guarda en un archivo separado y los elimina del original
    """
    
    # Rutas de archivos
    archivo_fuente = 'salida/fuente_agente.json'
    archivo_duplicados = 'salida/duplicados_eliminados.json'
    archivo_limpio = 'salida/fuente_agente_limpio.json'
    
    print("🧹 Detectando y eliminando duplicados...")
    print(f"📄 Archivo fuente: {archivo_fuente}")
    print(f"🗑️  Duplicados guardados en: {archivo_duplicados}")
    print(f"✨ Archivo limpio: {archivo_limpio}")
    
    # Verificar que existe el archivo fuente
    if not os.path.exists(archivo_fuente):
        print(f"❌ No se encuentra el archivo fuente: {archivo_fuente}")
        return False
    
    try:
        # Cargar datos del archivo fuente
        with open(archivo_fuente, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        print(f"📊 Total de objetos en archivo original: {len(datos)}")
        
        # Diccionarios para organizar los datos
        titulos_vistos = {}  # title -> primer objeto encontrado
        elementos_unicos = []
        elementos_duplicados = []
        
        # Procesar cada elemento
        for i, item in enumerate(datos):
            titulo = item.get('title', '').strip()
            
            if not titulo:
                # Si no tiene título, lo consideramos único (probablemente hay pocos casos)
                elementos_unicos.append(item)
                print(f"⚠️  Elemento {i+1} sin título, se mantiene como único")
                continue
            
            if titulo in titulos_vistos:
                # Es duplicado
                original = titulos_vistos[titulo]
                
                # Determinar cuál mantener (preferir el que tiene fecha en el nombre del archivo)
                nombre_archivo_original = original.get('file', '')
                nombre_archivo_actual = item.get('file', '')
                
                # Criterio: mantener el que tenga fecha en formato YYYY-MM-DD o DD-MM-YY
                tiene_fecha_original = any(char.isdigit() for char in nombre_archivo_original.split(' - ')[0] if ' - ' in nombre_archivo_original)
                tiene_fecha_actual = any(char.isdigit() for char in nombre_archivo_actual.split(' - ')[0] if ' - ' in nombre_archivo_actual)
                
                if tiene_fecha_actual and not tiene_fecha_original:
                    # El actual tiene fecha y el original no, reemplazar
                    elementos_duplicados.append({
                        "titulo_duplicado": titulo,
                        "elemento_eliminado": original,
                        "elemento_conservado": item,
                        "razon_eliminacion": "El original no tenía fecha, se conserva el que tiene fecha"
                    })
                    titulos_vistos[titulo] = item
                    # Remover el original de elementos_unicos si está ahí
                    elementos_unicos = [e for e in elementos_unicos if e.get('title') != titulo]
                    elementos_unicos.append(item)
                    
                elif tiene_fecha_original and not tiene_fecha_actual:
                    # El original tiene fecha y el actual no, mantener original
                    elementos_duplicados.append({
                        "titulo_duplicado": titulo,
                        "elemento_eliminado": item,
                        "elemento_conservado": original,
                        "razon_eliminacion": "El duplicado no tenía fecha, se conserva el original con fecha"
                    })
                    
                else:
                    # Ambos tienen fecha o ambos no tienen, mantener el primero encontrado
                    elementos_duplicados.append({
                        "titulo_duplicado": titulo,
                        "elemento_eliminado": item,
                        "elemento_conservado": original,
                        "razon_eliminacion": "Duplicado encontrado, se conserva el primer elemento"
                    })
                
                print(f"🔍 Duplicado detectado: '{titulo[:60]}...'")
                
            else:
                # Es único, guardarlo
                titulos_vistos[titulo] = item
                elementos_unicos.append(item)
        
        print(f"\n📊 Resumen de la limpieza:")
        print(f"   📁 Elementos originales: {len(datos)}")
        print(f"   ✅ Elementos únicos: {len(elementos_unicos)}")
        print(f"   🗑️  Elementos duplicados eliminados: {len(elementos_duplicados)}")
        
        # Crear directorio de salida si no existe
        Path(archivo_duplicados).parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar elementos duplicados
        with open(archivo_duplicados, 'w', encoding='utf-8') as f:
            json.dump({
                "resumen": {
                    "total_duplicados_eliminados": len(elementos_duplicados),
                    "fecha_limpieza": "2024-01-01",  # Puedes usar datetime si quieres la fecha real
                    "criterio_eliminacion": "Se mantiene el elemento con fecha en el nombre del archivo, o el primero encontrado en caso de empate"
                },
                "duplicados_eliminados": elementos_duplicados
            }, f, ensure_ascii=False, indent=2)
        
        # Guardar archivo limpio
        with open(archivo_limpio, 'w', encoding='utf-8') as f:
            json.dump(elementos_unicos, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Limpieza completada exitosamente")
        print(f"🗑️  Duplicados guardados en: {archivo_duplicados}")
        print(f"✨ Archivo limpio guardado en: {archivo_limpio}")
        
        # Mostrar algunos ejemplos de duplicados eliminados
        if elementos_duplicados:
            print(f"\n🔍 Ejemplos de duplicados eliminados:")
            for i, dup in enumerate(elementos_duplicados[:5], 1):
                titulo = dup["titulo_duplicado"][:50]
                razon = dup["razon_eliminacion"]
                print(f"  {i}. {titulo}...")
                print(f"     → {razon}")
            
            if len(elementos_duplicados) > 5:
                print(f"     ... y {len(elementos_duplicados) - 5} duplicados más")
        
        # Mostrar tamaño de los archivos generados
        if os.path.exists(archivo_limpio):
            file_size = os.path.getsize(archivo_limpio)
            file_size_mb = file_size / (1024 * 1024)
            print(f"💾 Tamaño del archivo limpio: {file_size_mb:.2f} MB")
        
        if os.path.exists(archivo_duplicados):
            file_size = os.path.getsize(archivo_duplicados)
            file_size_kb = file_size / 1024
            print(f"🗑️  Tamaño del archivo de duplicados: {file_size_kb:.1f} KB")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer el archivo JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🧹 Iniciando limpieza de duplicados en fuente_agente.json")
    
    exito = detectar_y_limpiar_duplicados()
    
    if exito:
        print("\n🎉 Limpieza de duplicados completada exitosamente!")
        print("\n📋 Próximos pasos:")
        print("   1. Revisar salida/fuente_agente_limpio.json")
        print("   2. Verificar salida/duplicados_eliminados.json")
        print("   3. Si todo está bien, reemplazar el archivo original")
    else:
        print("\n❌ La limpieza de duplicados falló")
        exit(1)

if __name__ == "__main__":
    main()
