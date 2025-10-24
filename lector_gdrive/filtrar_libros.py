import json
import os
from pathlib import Path

def filtrar_libros():
    """
    Filtra objetos del archivo fuente_agente.json que tengan 'libros -' 
    al inicio del atributo 'file' y los guarda en salida.libros.json
    """
    # Rutas de archivos
    archivo_fuente = Path('salida/fuente_agente.json')
    archivo_salida = Path('salida/salida.libros.json')
    
    try:
        # Verificar que existe el archivo fuente
        if not archivo_fuente.exists():
            print(f"Error: No se encuentra el archivo {archivo_fuente}")
            return False
            
        # Leer el archivo fuente
        with open(archivo_fuente, 'r', encoding='utf-8') as f:
            datos_fuente = json.load(f)
        
        # Filtrar objetos que comienzan con "libros -"
        libros_filtrados = [
            item for item in datos_fuente 
            if item.get('file', '').startswith('libros -')
        ]
        
        # Crear directorio de salida si no existe
        archivo_salida.parent.mkdir(parents=True, exist_ok=True)
        
        # Escribir archivo de salida
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(libros_filtrados, f, ensure_ascii=False, indent=2)
        
        # Mostrar estadísticas
        print(f"✓ Proceso completado exitosamente")
        print(f"📁 Archivo origen: {archivo_fuente}")
        print(f"📁 Archivo destino: {archivo_salida}")
        print(f"📊 Total objetos originales: {len(datos_fuente)}")
        print(f"📊 Objetos filtrados (libros): {len(libros_filtrados)}")
        
        # Mostrar algunos ejemplos
        if libros_filtrados:
            print(f"\n📚 Primeros 3 libros encontrados:")
            for i, libro in enumerate(libros_filtrados[:3], 1):
                print(f"  {i}. {libro.get('title', libro.get('file', 'Sin título'))}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = filtrar_libros()
    exit(0 if success else 1)
