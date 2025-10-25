import json
import os
from pathlib import Path

def filtrar_contemplaciones():
    """
    Filtra las contemplaciones del archivo fuente_agente.json
    Busca objetos cuyo atributo 'file' inicie con 'contemplaciones -'
    y los guarda en salida/salida.contemplaciones.json
    """
    
    # Rutas de archivos
    archivo_fuente = 'salida/fuente_agente.json'
    archivo_salida = 'salida/salida.contemplaciones.json'
    
    print("📿 Filtrando contemplaciones...")
    print(f"📄 Archivo fuente: {archivo_fuente}")
    print(f"💾 Archivo destino: {archivo_salida}")
    
    # Verificar que existe el archivo fuente
    if not os.path.exists(archivo_fuente):
        print(f"❌ No se encuentra el archivo fuente: {archivo_fuente}")
        return False
    
    try:
        # Cargar datos del archivo fuente
        with open(archivo_fuente, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        print(f"📊 Total de objetos en fuente_agente.json: {len(datos)}")
        
        # Filtrar contemplaciones (objetos cuyo 'file' inicie con 'contemplaciones -')
        contemplaciones = []
        
        for item in datos:
            # Verificar que el objeto tenga el atributo 'file'
            if 'file' in item:
                file_name = item['file']
                
                # Buscar archivos que inicien con 'contemplaciones -'
                if file_name.startswith('contemplaciones -'):
                    contemplaciones.append(item)
                    print(f"✅ Contemplación encontrada: {file_name[:80]}...")
        
        print(f"\n📊 Resumen del filtrado:")
        print(f"   📁 Total objetos procesados: {len(datos)}")
        print(f"   📿 Contemplaciones encontradas: {len(contemplaciones)}")
        
        # Crear directorio de salida si no existe
        Path(archivo_salida).parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar las contemplaciones filtradas
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(contemplaciones, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Filtrado completado exitosamente")
        print(f"💾 Archivo guardado: {archivo_salida}")
        
        # Mostrar algunas contemplaciones de ejemplo
        if contemplaciones:
            print(f"\n📿 Ejemplos de contemplaciones extraídas:")
            for i, contemp in enumerate(contemplaciones[:5], 1):
                titulo = contemp.get('title', contemp.get('file', 'Sin título'))
                print(f"  {i}. {titulo[:70]}...")
            
            if len(contemplaciones) > 5:
                print(f"  ... y {len(contemplaciones) - 5} contemplaciones más")
        
        # Mostrar tamaño del archivo generado
        if os.path.exists(archivo_salida):
            file_size = os.path.getsize(archivo_salida)
            file_size_kb = file_size / 1024
            print(f"💾 Tamaño del archivo generado: {file_size_kb:.1f} KB")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer el archivo JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🔄 Iniciando filtrado de contemplaciones desde fuente_agente.json")
    
    exito = filtrar_contemplaciones()
    
    if exito:
        print("\n🎉 Proceso completado exitosamente!")
    else:
        print("\n❌ El proceso falló")
        exit(1)

if __name__ == "__main__":
    main()
