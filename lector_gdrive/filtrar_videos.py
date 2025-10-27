import json
import csv
import os
from pathlib import Path
from difflib import SequenceMatcher

def similarity(a, b):
    """Calcula la similitud entre dos strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def limpiar_nombre_archivo(nombre):
    """Limpia el nombre del archivo para mejor comparación"""
    # Remover prefijo "videos - " y extensión ".txt"
    nombre = nombre.replace("videos - ", "").replace(".txt", "")
    # Convertir a minúsculas y limpiar espacios
    return nombre.lower().strip()

def limpiar_titulo_csv(titulo):
    """Limpia el título del CSV para mejor comparación"""
    return titulo.lower().strip()

def cargar_titulos_csv(csv_path):
    """Carga los títulos desde el archivo CSV"""
    titulos = []
    if not os.path.exists(csv_path):
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
                    
                    # Solo procesar filas que contengan 'video' en la primera columna
                    if categoria == 'video':
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

def filtrar_videos():
    """
    Filtra los videos del archivo fuente_agente.json
    Busca objetos cuyo atributo 'file' inicie con 'videos -'
    y los guarda en salida/salida.videos.json
    """
    
    # Rutas de archivos
    archivo_fuente = 'salida/fuente_agente.json'
    archivo_salida = 'salida/salida.videos.json'
    
    print("🎥 Filtrando videos...")
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
        
        # Filtrar videos (objetos cuyo 'file' inicie con 'videos -')
        videos = []
        
        for item in datos:
            # Verificar que el objeto tenga el atributo 'file'
            if 'file' in item:
                file_name = item['file']
                
                # Buscar archivos que inicien con 'videos -'
                if file_name.startswith('videos -'):
                    videos.append(item)
                    print(f"✅ Video encontrado: {file_name[:80]}...")
        
        print(f"\n📊 Resumen del filtrado:")
        print(f"   📁 Total objetos procesados: {len(datos)}")
        print(f"   🎥 Videos encontrados: {len(videos)}")
        
        # Crear directorio de salida si no existe
        Path(archivo_salida).parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar los videos filtrados
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(videos, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Filtrado completado exitosamente")
        print(f"💾 Archivo guardado: {archivo_salida}")
        
        # Mostrar algunos videos de ejemplo
        if videos:
            print(f"\n🎥 Ejemplos de videos extraídos:")
            for i, video in enumerate(videos[:5], 1):
                titulo = video.get('title', video.get('file', 'Sin título'))
                print(f"  {i}. {titulo[:70]}...")
            
            if len(videos) > 5:
                print(f"  ... y {len(videos) - 5} videos más")
        
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

def generar_videos_corregidos():
    """Genera el archivo salida.videos.json con títulos corregidos"""
    
    # Rutas de archivos
    archivo_entrada = 'salida/salida.videos.json'
    archivo_csv = 'titulos/videos.csv'
    archivo_salida = 'salida/salida.videos.json'
    
    print("\n🎥 Generando videos corregidos...")
    
    # Verificar que existe el archivo de entrada
    if not os.path.exists(archivo_entrada):
        print(f"❌ No se encuentra el archivo: {archivo_entrada}")
        return False
    
    # Cargar datos de entrada
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            videos_originales = json.load(f)
    except Exception as e:
        print(f"❌ Error cargando {archivo_entrada}: {e}")
        return False
    
    # Cargar títulos del CSV
    titulos_csv = cargar_titulos_csv(archivo_csv)
    if not titulos_csv:
        print("⚠️  No se encontraron títulos válidos en el CSV, usando títulos originales")
        # Si no hay CSV, simplemente copiar el archivo original
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                json.dump(videos_originales, f, ensure_ascii=False, indent=2)
            print(f"💾 Archivo copiado sin correcciones en: {archivo_salida}")
            return True
        except Exception as e:
            print(f"❌ Error guardando el archivo: {e}")
            return False
    
    print(f"📋 Se encontraron {len(titulos_csv)} títulos en el CSV")
    
    # Procesar cada video
    videos_corregidos = []
    actualizados = 0
    
    for video in videos_originales:
        nombre_archivo = video.get('file', '')
        
        # Encontrar el título más similar
        titulo_corregido, similitud = encontrar_titulo_mas_similar(nombre_archivo, titulos_csv)
        
        # Crear copia del objeto original
        video_corregido = dict(video)
        
        if titulo_corregido and similitud > 0.5:  # Umbral de similitud del 50%
            video_corregido['title'] = titulo_corregido
            actualizados += 1
            print(f"✅ Actualizado: '{limpiar_nombre_archivo(nombre_archivo)}' -> '{titulo_corregido}' (similitud: {similitud:.2f})")
        
        videos_corregidos.append(video_corregido)
    
    # Guardar archivo corregido
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(videos_corregidos, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎉 Corrección completada!")
        print(f"📊 Títulos actualizados: {actualizados}/{len(videos_corregidos)}")
        print(f"💾 Archivo guardado en: {archivo_salida}")
        return True
        
    except Exception as e:
        print(f"❌ Error guardando el archivo: {e}")
        return False

def main():
    """Función principal"""
    print("🔄 Iniciando filtrado de videos desde fuente_agente.json")
    
    exito = filtrar_videos()
    
    if exito:
        print("\n🎉 Proceso completado exitosamente!")
    else:
        print("\n❌ El proceso falló")
        exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Filtrar videos y corregir títulos')
    parser.add_argument('--solo-filtrar', action='store_true', help='Solo filtrar videos sin corregir títulos')
    parser.add_argument('--solo-corregir', action='store_true', help='Solo corregir títulos (requiere salida.videos.json)')
    
    args = parser.parse_args()
    
    if args.solo_corregir:
        generar_videos_corregidos()
    elif args.solo_filtrar:
        filtrar_videos()
    else:
        # Proceso completo: filtrar y luego corregir
        if filtrar_videos():
            generar_videos_corregidos()
