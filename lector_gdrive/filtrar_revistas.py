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
    # Remover prefijo "articulos en revistas - " y extensión ".txt"
    nombre = nombre.replace("articulos en revistas - ", "").replace(".txt", "")
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
            content = f.read().strip()
            if not content:
                print(f"❌ El archivo CSV está vacío: {csv_path}")
                return titulos
            
            # Resetear el archivo para leerlo con csv.reader
            f.seek(0)
            reader = csv.reader(f)
            
            print(f"🔍 Analizando archivo CSV: {csv_path}")
            
            # Leer todas las filas para debug
            all_rows = list(reader)
            print(f"📊 Total de filas en CSV: {len(all_rows)}")
            
            if not all_rows:
                print("❌ No hay filas en el CSV")
                return titulos
            
            # Mostrar las primeras filas para debug
            print("🔍 Primeras 3 filas del CSV:")
            for i, row in enumerate(all_rows[:3]):
                print(f"  Fila {i}: {row}")
            
            # Intentar diferentes estrategias de lectura
            for i, row in enumerate(all_rows):
                if not row:  # Saltar filas vacías
                    continue
                    
                # Estrategia 1: Si hay al menos 2 columnas, usar la segunda como título
                if len(row) >= 2:
                    categoria = row[0].strip().lower()
                    titulo = row[1].strip()
                    
                    # Buscar diferentes variaciones de "revista"
                    categorias_validas = ['revista', 'revistas', 'articulo', 'articulos', 'artículo', 'artículos']
                    
                    if any(cat in categoria for cat in categorias_validas) and titulo:
                        titulos.append(titulo)
                        print(f"✅ Título añadido: '{titulo}' (categoría: '{categoria}')")
                
                # Estrategia 2: Si solo hay una columna, usar como título directamente
                elif len(row) == 1 and row[0].strip():
                    titulo = row[0].strip()
                    # Verificar que no sea un header
                    if not titulo.lower().startswith(('categoria', 'tipo', 'title', 'titulo')):
                        titulos.append(titulo)
                        print(f"✅ Título añadido (columna única): '{titulo}'")
            
            print(f"📋 Total títulos cargados: {len(titulos)}")
            
            # Si no encontró títulos con las estrategias anteriores, intentar leer todo como títulos
            if not titulos and all_rows:
                print("⚠️  Intentando estrategia alternativa: leer todas las filas como títulos")
                for i, row in enumerate(all_rows):
                    if row and len(row) > 0:
                        # Tomar el último elemento no vacío de la fila
                        for col in reversed(row):
                            if col.strip():
                                titulo = col.strip()
                                if titulo and not titulo.lower().startswith(('categoria', 'tipo', 'title', 'titulo')):
                                    titulos.append(titulo)
                                    print(f"✅ Título añadido (alternativo): '{titulo}'")
                                break
                        
                        # Solo tomar los primeros 20 para evitar spam
                        if len(titulos) >= 20:
                            break
                            
    except Exception as e:
        print(f"❌ Error leyendo {csv_path}: {e}")
        import traceback
        traceback.print_exc()
    
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

def filtrar_revistas():
    """
    Filtra objetos del archivo fuente_agente.json que tengan 'articulos en revistas -' 
    al inicio del atributo 'file' y los guarda en salida.revistas.json
    """
    # Rutas de archivos
    archivo_fuente = Path('salida/fuente_agente.json')
    archivo_salida = Path('salida/salida.revistas.json')
    
    try:
        # Verificar que existe el archivo fuente
        if not archivo_fuente.exists():
            print(f"Error: No se encuentra el archivo {archivo_fuente}")
            return False
            
        # Leer el archivo fuente
        with open(archivo_fuente, 'r', encoding='utf-8') as f:
            datos_fuente = json.load(f)
        
        # Filtrar objetos que comienzan con "articulos en revistas -"
        revistas_filtradas = [
            item for item in datos_fuente 
            if item.get('file', '').startswith('articulos en revistas -')
        ]
        
        # Crear directorio de salida si no existe
        archivo_salida.parent.mkdir(parents=True, exist_ok=True)
        
        # Escribir archivo de salida
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(revistas_filtradas, f, ensure_ascii=False, indent=2)
        
        # Mostrar estadísticas
        print(f"✓ Proceso completado exitosamente")
        print(f"📁 Archivo origen: {archivo_fuente}")
        print(f"📁 Archivo destino: {archivo_salida}")
        print(f"📊 Total objetos originales: {len(datos_fuente)}")
        print(f"📊 Objetos filtrados (artículos en revistas): {len(revistas_filtradas)}")
        
        # Mostrar algunos ejemplos
        if revistas_filtradas:
            print(f"\n📄 Primeros 3 artículos en revistas encontrados:")
            for i, revista in enumerate(revistas_filtradas[:3], 1):
                print(f"  {i}. {revista.get('title', 'Sin título')}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error: El archivo JSON no es válido: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def generar_revistas_corregidas():
    """Genera el archivo salida.revistas.json con títulos corregidos"""
    
    # Rutas de archivos
    archivo_entrada = 'salida/salida.revistas.json'
    archivo_csv = 'titulos/revistas.csv'
    archivo_salida = 'salida/salida.revistas.json'
    
    print("\n📄 Generando artículos en revistas corregidos...")
    print(f"📄 Archivo CSV: {archivo_csv}")
    
    # Verificar que existe el archivo de entrada
    if not os.path.exists(archivo_entrada):
        print(f"❌ No se encuentra el archivo: {archivo_entrada}")
        return False
    
    # Cargar datos de entrada
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            revistas_originales = json.load(f)
    except Exception as e:
        print(f"❌ Error cargando {archivo_entrada}: {e}")
        return False
    
    print(f"📊 Artículos en revistas a procesar: {len(revistas_originales)}")
    
    # Cargar títulos del CSV
    titulos_csv = cargar_titulos_csv(archivo_csv)
    if not titulos_csv:
        print("⚠️  No se encontraron títulos válidos en el CSV, usando títulos originales")
        # Si no hay CSV, simplemente copiar el archivo original
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                json.dump(revistas_originales, f, ensure_ascii=False, indent=2)
            print(f"💾 Archivo copiado sin correcciones en: {archivo_salida}")
            return True
        except Exception as e:
            print(f"❌ Error guardando el archivo: {e}")
            return False
    
    print(f"📋 Se encontraron {len(titulos_csv)} títulos en el CSV")
    
    # Mostrar algunos títulos del CSV para debug
    print("🔍 Primeros 3 títulos del CSV:")
    for i, titulo in enumerate(titulos_csv[:3]):
        print(f"  {i+1}. {titulo[:80]}...")  # Limitar a 80 caracteres
    
    # Procesar cada artículo en revista
    revistas_corregidas = []
    actualizados = 0
    
    for revista in revistas_originales:
        nombre_archivo = revista.get('file', '')
        
        # Encontrar el título más similar
        titulo_corregido, similitud = encontrar_titulo_mas_similar(nombre_archivo, titulos_csv)
        
        # Crear copia del objeto original
        revista_corregida = dict(revista)
        
        if titulo_corregido and similitud > 0.3:  # Reducir umbral de similitud al 30%
            revista_corregida['title'] = titulo_corregido
            actualizados += 1
            print(f"✅ Actualizado: '{limpiar_nombre_archivo(nombre_archivo)[:50]}...' -> '{titulo_corregido[:50]}...' (similitud: {similitud:.2f})")
        else:
            if titulo_corregido:
                print(f"⚠️  Similitud baja ({similitud:.2f}): '{limpiar_nombre_archivo(nombre_archivo)[:40]}...' vs '{titulo_corregido[:40]}...'")
            else:
                print(f"❌ No se encontró título similar para: '{limpiar_nombre_archivo(nombre_archivo)[:50]}...'")
        
        revistas_corregidas.append(revista_corregida)
    
    # Guardar archivo corregido
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(revistas_corregidas, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎉 Corrección completada!")
        print(f"📊 Títulos actualizados: {actualizados}/{len(revistas_corregidas)}")
        print(f"💾 Archivo guardado en: {archivo_salida}")
        return True
        
    except Exception as e:
        print(f"❌ Error guardando el archivo: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Filtrar artículos en revistas y corregir títulos')
    parser.add_argument('--solo-filtrar', action='store_true', help='Solo filtrar artículos sin corregir títulos')
    parser.add_argument('--solo-corregir', action='store_true', help='Solo corregir títulos (requiere salida.revistas.json)')
    
    args = parser.parse_args()
    
    if args.solo_corregir:
        generar_revistas_corregidas()
    elif args.solo_filtrar:
        filtrar_revistas()
    else:
        # Proceso completo: filtrar y luego corregir
        if filtrar_revistas():
            generar_revistas_corregidas()
