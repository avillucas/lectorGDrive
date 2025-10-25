import json
import os
from pathlib import Path
import re
from difflib import SequenceMatcher

def limpiar_nombre_archivo(nombre_archivo):
    """Limpia el nombre del archivo para extraer información relevante"""
    # Remover extensión
    nombre = nombre_archivo.replace('.txt', '')
    
    # Remover prefijo "articulos - "
    if nombre.startswith('articulos - '):
        nombre = nombre[len('articulos - '):]
    
    # Convertir guiones bajos en espacios
    nombre = nombre.replace('_', ' ')
    
    # Remover números al final que parecen códigos
    nombre = re.sub(r'_\d+$', '', nombre)
    
    return nombre.strip()

def extraer_palabras_clave(texto):
    """Extrae palabras clave relevantes para la comparación"""
    # Normalizar texto
    texto = texto.lower()
    
    # Palabras comunes de ejercicios espirituales a mantener
    palabras_espirituales = [
        'ejercicios', 'espirituales', 'ignacio', 'loyola', 'jesus', 'cristo', 'dios',
        'contemplacion', 'meditacion', 'oracion', 'discernimiento', 'consolacion',
        'desolacion', 'eleccion', 'principio', 'fundamento', 'reino', 'banderas',
        'binarios', 'humildad', 'pasion', 'resurreccion', 'amor', 'servicio',
        'alabar', 'reverenciar', 'servir', 'señor', 'creador', 'salvation',
        'pecado', 'gracia', 'libertad', 'voluntad', 'misericordia', 'cruz'
    ]
    
    # Extraer palabras significativas
    palabras = re.findall(r'\b\w+\b', texto)
    
    # Filtrar palabras muy cortas o números solos
    palabras_filtradas = []
    for palabra in palabras:
        if len(palabra) > 2 or palabra.isdigit():
            palabras_filtradas.append(palabra)
    
    return ' '.join(palabras_filtradas)

def calcular_similitud(texto1, texto2):
    """Calcula la similitud entre dos textos"""
    # Limpiar y normalizar ambos textos
    t1 = extraer_palabras_clave(texto1)
    t2 = extraer_palabras_clave(texto2)
    
    # Usar SequenceMatcher para calcular similitud
    return SequenceMatcher(None, t1, t2).ratio()

def encontrar_titulo_mas_similar(nombre_archivo, titulos_ejercicios):
    """Encuentra el título más similar en la base de ejercicios espirituales"""
    nombre_limpio = limpiar_nombre_archivo(nombre_archivo)
    
    mejor_titulo = None
    mejor_similitud = 0.0
    
    for ejercicio in titulos_ejercicios:
        titulo = ejercicio.get('titulo', '')
        
        # Calcular similitud
        similitud = calcular_similitud(nombre_limpio, titulo)
        
        if similitud > mejor_similitud:
            mejor_similitud = similitud
            mejor_titulo = titulo
    
    return mejor_titulo, mejor_similitud

def corregir_titulos_talleres():
    """
    Corrige los títulos en salida.talleres.json usando 
    los títulos de titulos/ejercicios_espirituales.json por similitud
    """
    
    # Rutas de archivos
    archivo_salida = 'salida/salida.talleres.json'
    archivo_titulos = 'titulos/ejercicios_espirituales.json'
    
    print("🔧 Corrigiendo títulos de talleres...")
    print(f"📄 Archivo a corregir: {archivo_salida}")
    print(f"📚 Base de títulos: {archivo_titulos}")
    
    # Verificar que existan los archivos
    if not os.path.exists(archivo_salida):
        print(f"❌ No se encuentra el archivo: {archivo_salida}")
        return False
    
    if not os.path.exists(archivo_titulos):
        print(f"❌ No se encuentra el archivo: {archivo_titulos}")
        return False
    
    try:
        # Cargar talleres a corregir
        with open(archivo_salida, 'r', encoding='utf-8') as f:
            talleres = json.load(f)
        
        print(f"📊 Talleres a procesar: {len(talleres)}")
        
        # Cargar base de títulos de ejercicios espirituales
        with open(archivo_titulos, 'r', encoding='utf-8') as f:
            titulos_base = json.load(f)
        
        print(f"📚 Títulos en la base: {len(titulos_base)}")
        
        # Procesar cada taller
        talleres_corregidos = []
        actualizados = 0
        no_encontrados = 0
        
        for i, taller in enumerate(talleres):
            nombre_archivo = taller.get('file', '')
            titulo_original = taller.get('title', '')
            
            # Buscar título más similar
            titulo_corregido, similitud = encontrar_titulo_mas_similar(nombre_archivo, titulos_base)
            
            # Crear copia del objeto
            taller_corregido = dict(taller)
            
            if titulo_corregido and similitud > 0.3:  # Umbral de 30% (más bajo para artículos)
                taller_corregido['title'] = titulo_corregido
                actualizados += 1
                
                if i < 5:  # Mostrar los primeros 5 para debug
                    print(f"✅ Actualizado: '{limpiar_nombre_archivo(nombre_archivo)}'")
                    print(f"   Original: '{titulo_original}'")
                    print(f"   Nuevo: '{titulo_corregido}' (similitud: {similitud:.2f})")
                    print()
            else:
                no_encontrados += 1
                if i < 3:  # Mostrar los primeros 3 no encontrados
                    print(f"❌ No encontrado: '{limpiar_nombre_archivo(nombre_archivo)}'")
                    print(f"   Mejor match: '{titulo_corregido}' (similitud: {similitud:.2f})")
                    print()
            
            talleres_corregidos.append(taller_corregido)
        
        # Guardar archivo corregido
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(talleres_corregidos, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎉 Corrección completada!")
        print(f"📊 Total talleres: {len(talleres_corregidos)}")
        print(f"✅ Títulos actualizados: {actualizados}")
        print(f"❌ No encontrados: {no_encontrados}")
        print(f"📈 Porcentaje de éxito: {(actualizados/len(talleres)*100):.1f}%")
        print(f"💾 Archivo guardado en: {archivo_salida}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer archivos JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🔄 Iniciando corrección de títulos de talleres")
    
    exito = corregir_titulos_talleres()
    
    if exito:
        print("\n🎉 Proceso completado exitosamente!")
    else:
        print("\n❌ El proceso falló")
        exit(1)

if __name__ == "__main__":
    main()
