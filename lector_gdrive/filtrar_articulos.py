import json
import os
from pathlib import Path

def filtrar_articulos():
    """
    Filtra los artículos del archivo fuente_agente.json
    Busca objetos cuyo atributo 'file' inicie con 'articulos -'
    y los guarda en salida/salida.talleres.json
    """
    
    # Rutas de archivos
    archivo_fuente = 'salida/fuente_agente.json'
    archivo_salida = 'salida/salida.talleres.json'
    
    print("📚 Filtrando artículos...")
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
        
        # Filtrar artículos (objetos cuyo 'file' inicie con 'articulos -')
        articulos = []
        
        for item in datos:
            # Verificar que el objeto tenga el atributo 'file'
            if 'file' in item:
                file_name = item['file']
                
                # Buscar archivos que inicien con 'articulos -'
                if file_name.startswith('articulos -'):
                    articulos.append(item)
                    print(f"✅ Artículo encontrado: {file_name[:80]}...")
        
        print(f"\n📊 Resumen del filtrado:")
        print(f"   📁 Total objetos procesados: {len(datos)}")
        print(f"   📚 Artículos encontrados: {len(articulos)}")
        
        # Crear directorio de salida si no existe
        Path(archivo_salida).parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar los artículos filtrados
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(articulos, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Filtrado completado exitosamente")
        print(f"💾 Archivo guardado: {archivo_salida}")
        
        # Mostrar algunos artículos de ejemplo
        if articulos:
            print(f"\n📚 Ejemplos de artículos extraídos:")
            for i, articulo in enumerate(articulos[:5], 1):
                titulo = articulo.get('title', articulo.get('file', 'Sin título'))
                print(f"  {i}. {titulo[:70]}...")
            
            if len(articulos) > 5:
                print(f"  ... y {len(articulos) - 5} artículos más")
        
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
    print("🔄 Iniciando filtrado de artículos desde fuente_agente.json")
    
    exito = filtrar_articulos()
    
    if exito:
        print("\n🎉 Proceso completado exitosamente!")
    else:
        print("\n❌ El proceso falló")
        exit(1)

if __name__ == "__main__":
    main()
