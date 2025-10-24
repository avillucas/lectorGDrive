import json
import csv
import os
from difflib import SequenceMatcher

def similarity(a, b):
    """Calcula la similitud entre dos strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def limpiar_nombre_archivo(nombre):
    """Limpia el nombre del archivo para mejor comparación"""
    # Remover prefijo "libros - " y extensión ".txt"
    nombre = nombre.replace("libros - ", "").replace(".txt", "")
    # Convertir a minúsculas y limpiar espacios
    return nombre.lower().strip()

def limpiar_titulo_csv(titulo):
    """Limpia el título del CSV para mejor comparación"""
    return titulo.lower().strip()

def cargar_titulos_csv(csv_path):
    """Carga los títulos desde el archivo CSV"""
    titulos = []
    if not os.path.exists(csv_path):
        print(f"❌ No se encuentra el archivo CSV: {csv_path}")
        return titulos
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Saltar header si existe
            next(reader, None)
            
            for row in reader:
                if len(row) >= 2:
                    categoria = row[0].strip().lower()
                    titulo = row[1].strip()
                    
                    # Solo procesar filas que contengan 'libro' en la primera columna
                    if categoria == 'libro':
                        titulos.append(titulo)
                        
    except Exception as e:
        print(f"⚠️  Error leyendo {csv_path}: {e}")
    
    return titulos

def encontrar_titulo_mas_similar(nombre_archivo, titulos_csv):
    """Encuentra el título más similar del CSV para un nombre de archivo dado"""
    nombre_limpio = limpiar_nombre_archivo(nombre_archivo)
    
    mejor_similitud = 0
    mejor_titulo = None
    
    for titulo in titulos_csv:
        titulo_limpio = limpiar_titulo_csv(titulo)
        similitud = similarity(nombre_limpio, titulo_limpio)
        
        if similitud > mejor_similitud:
            mejor_similitud = similitud
            mejor_titulo = titulo
    
    return mejor_titulo, mejor_similitud

def generar_libros_corregidos():
    """Genera el archivo libros_corregidos.json con títulos corregidos"""
    
    # Rutas de archivos
    archivo_entrada = 'salida/salida.libros.json'
    archivo_csv = 'titulos/libros.csv'
    archivo_salida = 'salida/libros_corregidos.json'
    
    print("📚 Generando libros corregidos...")
    print(f"📄 Archivo de entrada: {archivo_entrada}")
    print(f"📄 Archivo CSV: {archivo_csv}")
    print(f"💾 Archivo de salida: {archivo_salida}")
    
    # Verificar que existe el archivo de entrada
    if not os.path.exists(archivo_entrada):
        print(f"❌ No se encuentra el archivo: {archivo_entrada}")
        return
    
    # Cargar datos de entrada
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            libros_originales = json.load(f)
    except Exception as e:
        print(f"❌ Error cargando {archivo_entrada}: {e}")
        return
    
    # Cargar títulos del CSV
    titulos_csv = cargar_titulos_csv(archivo_csv)
    if not titulos_csv:
        print("❌ No se encontraron títulos válidos en el CSV")
        return
    
    print(f"📋 Se encontraron {len(titulos_csv)} títulos en el CSV")
    print(f"📋 Se encontraron {len(libros_originales)} libros en el archivo original")
    
    # Procesar cada libro
    libros_corregidos = []
    actualizados = 0
    no_encontrados = 0
    
    for libro in libros_originales:
        nombre_archivo = libro.get('file', '')
        titulo_original = libro.get('title', '')
        
        # Encontrar el título más similar
        titulo_corregido, similitud = encontrar_titulo_mas_similar(nombre_archivo, titulos_csv)
        
        # Crear copia del objeto original
        libro_corregido = dict(libro)
        
        if titulo_corregido and similitud > 0.5:  # Umbral de similitud del 50%
            libro_corregido['title'] = titulo_corregido
            actualizados += 1
            print(f"✅ Actualizado: '{limpiar_nombre_archivo(nombre_archivo)}' -> '{titulo_corregido}' (similitud: {similitud:.2f})")
        else:
            no_encontrados += 1
            print(f"⚠️  Sin coincidencia suficiente para: '{nombre_archivo}' (mejor similitud: {similitud:.2f})")
        
        libros_corregidos.append(libro_corregido)
    
    # Guardar archivo corregido
    try:
        os.makedirs('salida', exist_ok=True)
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(libros_corregidos, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎉 Proceso completado exitosamente!")
        print(f"📊 Estadísticas:")
        print(f"   Total de libros procesados: {len(libros_corregidos)}")
        print(f"   Títulos actualizados: {actualizados}")
        print(f"   Sin actualizar: {no_encontrados}")
        print(f"💾 Archivo guardado en: {archivo_salida}")
        
    except Exception as e:
        print(f"❌ Error guardando el archivo: {e}")

if __name__ == "__main__":
    generar_libros_corregidos()
