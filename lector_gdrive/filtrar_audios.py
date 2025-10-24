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
    # Remover prefijo "audios - " y extensión ".txt"
    nombre = nombre.replace("audios - ", "").replace(".txt", "")
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
                    
                    # Solo procesar filas que contengan 'audio' en la primera columna
                    if categoria == 'audio':
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

def filtrar_audios():
    """
    Filtra objetos del archivo fuente_agente.json que tengan 'audios -' 
    al inicio del atributo 'file' y los guarda en salida.audios.json
    """
    # Rutas de archivos
    archivo_fuente = Path('salida/fuente_agente.json')
    archivo_salida = Path('salida/salida.audios.json')
    
    try:
        # Verificar que existe el archivo fuente
        if not archivo_fuente.exists():
            print(f"Error: No se encuentra el archivo {archivo_fuente}")
            return False
            
        # Leer el archivo fuente
        with open(archivo_fuente, 'r', encoding='utf-8') as f:
            datos_fuente = json.load(f)
        
        # Filtrar objetos que comienzan con "audios -"
        audios_filtrados = [
            item for item in datos_fuente 
            if item.get('file', '').startswith('audios -')
        ]
        
        # Crear directorio de salida si no existe
        archivo_salida.parent.mkdir(parents=True, exist_ok=True)
        
        # Escribir archivo de salida
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(audios_filtrados, f, ensure_ascii=False, indent=2)
        
        # Mostrar estadísticas
        print(f"✓ Proceso completado exitosamente")
        print(f"📁 Archivo origen: {archivo_fuente}")
        print(f"📁 Archivo destino: {archivo_salida}")
        print(f"📊 Total objetos originales: {len(datos_fuente)}")
        print(f"📊 Objetos filtrados (audios): {len(audios_filtrados)}")
        
        # Mostrar algunos ejemplos
        if audios_filtrados:
            print(f"\n🎧 Primeros 3 audios encontrados:")
            for i, audio in enumerate(audios_filtrados[:3], 1):
                print(f"  {i}. {audio.get('title', 'Sin título')}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error: El archivo JSON no es válido: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def generar_audios_corregidos():
    """Genera el archivo salida.audios.json con títulos corregidos"""
    
    # Rutas de archivos
    archivo_entrada = 'salida/salida.audios.json'
    archivo_csv = 'titulos/audios.csv'
    archivo_salida = 'salida/salida.audios.json'
    
    print("\n🎧 Generando audios corregidos...")
    
    # Verificar que existe el archivo de entrada
    if not os.path.exists(archivo_entrada):
        print(f"❌ No se encuentra el archivo: {archivo_entrada}")
        return False
    
    # Cargar datos de entrada
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            audios_originales = json.load(f)
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
                json.dump(audios_originales, f, ensure_ascii=False, indent=2)
            print(f"💾 Archivo copiado sin correcciones en: {archivo_salida}")
            return True
        except Exception as e:
            print(f"❌ Error guardando el archivo: {e}")
            return False
    
    print(f"📋 Se encontraron {len(titulos_csv)} títulos en el CSV")
    
    # Procesar cada audio
    audios_corregidos = []
    actualizados = 0
    
    for audio in audios_originales:
        nombre_archivo = audio.get('file', '')
        
        # Encontrar el título más similar
        titulo_corregido, similitud = encontrar_titulo_mas_similar(nombre_archivo, titulos_csv)
        
        # Crear copia del objeto original
        audio_corregido = dict(audio)
        
        if titulo_corregido and similitud > 0.5:  # Umbral de similitud del 50%
            audio_corregido['title'] = titulo_corregido
            actualizados += 1
            print(f"✅ Actualizado: '{limpiar_nombre_archivo(nombre_archivo)}' -> '{titulo_corregido}' (similitud: {similitud:.2f})")
        
        audios_corregidos.append(audio_corregido)
    
    # Guardar archivo corregido
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(audios_corregidos, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎉 Corrección completada!")
        print(f"📊 Títulos actualizados: {actualizados}/{len(audios_corregidos)}")
        print(f"💾 Archivo guardado en: {archivo_salida}")
        return True
        
    except Exception as e:
        print(f"❌ Error guardando el archivo: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Filtrar audios y corregir títulos')
    parser.add_argument('--solo-filtrar', action='store_true', help='Solo filtrar audios sin corregir títulos')
    parser.add_argument('--solo-corregir', action='store_true', help='Solo corregir títulos (requiere salida.audios.json)')
    
    args = parser.parse_args()
    
    if args.solo_corregir:
        generar_audios_corregidos()
    elif args.solo_filtrar:
        filtrar_audios()
    else:
        # Proceso completo: filtrar y luego corregir
        if filtrar_audios():
            generar_audios_corregidos()
