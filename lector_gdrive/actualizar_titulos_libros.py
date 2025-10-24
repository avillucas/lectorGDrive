import os
import json
import csv
import argparse

def cargar_fuente_agente(fuente_path):
    """Carga el archivo fuente_agente.json"""
    if not os.path.exists(fuente_path):
        print(f"❌ No se encuentra {fuente_path}")
        return None
    
    with open(fuente_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def cargar_titulos_libros(csv_path):
    """Carga títulos de libros desde el archivo CSV y crea un mapeo archivo -> título"""
    if not os.path.exists(csv_path):
        return {}
    
    mapeo_archivos_titulos = {}
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Saltar la primera fila si es un header
            next(reader, None)
            
            for row in reader:
                if len(row) >= 2:
                    categoria = row[0].strip().lower()
                    titulo = row[1].strip()
                    
                    # Solo procesar filas que contengan 'libro' en la primera columna
                    if categoria == 'libro':
                        # El título en la segunda columna es también el nombre del archivo
                        nombre_archivo = titulo
                        mapeo_archivos_titulos[nombre_archivo] = titulo
                        
    except Exception as e:
        print(f"⚠️  Error leyendo {csv_path}: {e}")
    
    return mapeo_archivos_titulos

def actualizar_titulos_libros(fuente_agente, csv_path):
    """Actualiza los títulos de libros en fuente_agente usando el archivo CSV"""
    
    mapeo_archivos_titulos = cargar_titulos_libros(csv_path)
    
    if not mapeo_archivos_titulos:
        print(f"⚠️  No se encontraron títulos de libros válidos en {csv_path}")
        return 0
    
    print(f"📚 Se encontraron {len(mapeo_archivos_titulos)} archivos de libros en el CSV")
    print(f"📋 Archivos encontrados: {list(mapeo_archivos_titulos.keys())[:5]}...")  # Mostrar solo los primeros 5
    
    total_actualizados = 0
    archivos_encontrados = 0
    archivos_no_encontrados = []
    
    for item in fuente_agente:
        nombre_archivo = item.get('file', '')
        
        # Buscar coincidencia exacta del nombre del archivo
        if nombre_archivo in mapeo_archivos_titulos:
            archivos_encontrados += 1
            titulo_nuevo = mapeo_archivos_titulos[nombre_archivo]
            titulo_anterior = item.get('title', '')
            
            if titulo_anterior != titulo_nuevo:
                # Crear una copia del item para verificar que solo cambia el title
                item_original = dict(item)
                
                # Solo modificar el campo 'title'
                item['title'] = titulo_nuevo
                
                # Verificar que solo cambió el title
                cambios = []
                for key in item:
                    if key != 'title' and item.get(key) != item_original.get(key):
                        cambios.append(key)
                
                if cambios:
                    print(f"⚠️  ADVERTENCIA: Se detectaron cambios inesperados en {cambios}")
                
                total_actualizados += 1
                print(f"✅ Actualizado libro: {nombre_archivo} -> {titulo_nuevo}")
            else:
                print(f"📋 Sin cambios: {nombre_archivo} (ya tenía el título correcto)")
        
        # Registrar archivos que podrían ser libros pero no están en el CSV
        elif any(keyword in nombre_archivo.lower() for keyword in ['pdf', 'docx', 'doc']) and len(nombre_archivo) > 10:
            archivos_no_encontrados.append(nombre_archivo)
    
    # Mostrar estadísticas
    print(f"\n📊 Estadísticas de libros:")
    print(f"   Archivos de libros encontrados en fuente_agente: {archivos_encontrados}")
    print(f"   Archivos de libros actualizados: {total_actualizados}")
    print(f"   Archivos CSV disponibles: {len(mapeo_archivos_titulos)}")
    
    if archivos_no_encontrados:
        print(f"   Posibles libros no encontrados en CSV: {len(archivos_no_encontrados)}")
        print(f"   Ejemplos: {archivos_no_encontrados[:3]}")
    
    print(f"   ✅ Solo se modificaron títulos de archivos de libros")
    
    return total_actualizados

def main():
    parser = argparse.ArgumentParser(description='Actualizar títulos de libros en fuente_agente.json desde libros.csv')
    parser.add_argument('--fuente_path', default='salida/fuente_agente.json', help='Ruta al archivo fuente_agente.json')
    parser.add_argument('--csv_path', default='titulos/libros.csv', help='Ruta al archivo CSV con títulos de libros')
    parser.add_argument('--output_path', help='Ruta de salida (por defecto sobrescribe el original)')
    
    args = parser.parse_args()
    
    print("🔄 Iniciando actualización de títulos de libros desde CSV...")
    print(f"📄 Archivo CSV: {args.csv_path}")
    
    # Cargar fuente_agente.json
    print("📄 Cargando fuente_agente.json...")
    fuente_agente = cargar_fuente_agente(args.fuente_path)
    
    if fuente_agente is None:
        return
    
    # Verificar que existe el archivo CSV
    if not os.path.exists(args.csv_path):
        print(f"❌ No se encuentra el archivo CSV: {args.csv_path}")
        return
    
    # Actualizar títulos de libros
    total_actualizados = actualizar_titulos_libros(fuente_agente, args.csv_path)
    
    if total_actualizados == 0:
        print("❌ No se actualizaron títulos de libros")
        return
    
    # Guardar archivo actualizado
    output_path = args.output_path or args.fuente_path
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(fuente_agente, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 Proceso completado: {total_actualizados} títulos de libros actualizados")
    print(f"📁 Archivo guardado en: {output_path}")

if __name__ == "__main__":
    main()
