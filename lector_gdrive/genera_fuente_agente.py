import os
import json
import re

def generar_fuente_agente(cache_dir, output_dir):
    def quitar_extension(nombre):
        """Quita la extensión del archivo (todo lo que sigue al último punto)"""
        return nombre.rsplit('.', 1)[0]
    
    def corregir_ortografia(texto):
        """Correcciones ortográficas básicas manteniendo caracteres españoles"""
        correcciones = {
            # Correcciones comunes
            'cutura': 'cultura',
            'Cutura': 'Cultura',
            'antropologia': 'antropología',
            'Antropologia': 'Antropología',
            'politica': 'política',
            'Politica': 'Política',
            'filosofia': 'filosofía',
            'Filosofia': 'Filosofía',
            'teologia': 'teología',
            'Teologia': 'Teología',
            'ecclesiale': 'eclesial',
            'Ecclesiale': 'Eclesial',
            'pequenios': 'pequeños',
            'Pequenios': 'Pequeños',
            'povertà': 'pobreza',
            'Povertà': 'Pobreza',
            'fragilità': 'fragilidad',
            'Fragilità': 'Fragilidad',
            'spirituali': 'espirituales',
            'Spirituali': 'Espirituales',
            'misericorida': 'misericordia',
            'Misericorida': 'Misericordia',
            # Letras faltantes - acentos
            'corazn': 'corazón',
            'Corazn': 'Corazón',
            'CORAZ': 'Corazón',
            'razon': 'razón',
            'Razon': 'Razón',
            'oracion': 'oración',
            'Oracion': 'Oración',
            'pasion': 'pasión',
            'Pasion': 'Pasión',
            'vocacion': 'vocación',
            'Vocacion': 'Vocación',
            'creacion': 'creación',
            'Creacion': 'Creación',
            'salvacion': 'salvación',
            'Salvacion': 'Salvación',
            'resurreccion': 'resurrección',
            'Resurreccion': 'Resurrección',
            'contemplacion': 'contemplación',
            'Contemplacion': 'Contemplación',
            'meditacion': 'meditación',
            'Meditacion': 'Meditación',
            # Terminaciones -ciones por -ción
            'contemplacionesn': 'contemplaciones',
            'Contemplacionesn': 'Contemplaciones',
            'meditacionesn': 'meditaciones',
            'Meditacionesn': 'Meditaciones',
            # Mayúsculas específicas
            'BIBLIA': 'Biblia',
            'EJERCICIOS': 'Ejercicios',
            'TRIPTICO': 'Tríptico',
            'APARECIDA': 'Aparecida',
            'EVANGELII': 'Evangelii',
            'GAUDIUM': 'Gaudium',
            'FRUTOS': 'Frutos',
            'EUCARISTA': 'Eucaristía',
            'CHERNOBYL': 'Chernóbyl',
            'FRATELLANZA': 'Fratellanza',
            'SAGGEZZA': 'Saggezza',
            'LAETITIA': 'Laetitia',
            'AMORIS': 'Amoris',
            'MISERICORDIA': 'Misericordia',
            'MISERA': 'Misera',
            'CARTA': 'Carta',
            'ENCCLICA': 'Encíclica',
            'DILEXIT': 'Dilexit',
            'NOS': 'Nos',
            'SANTO': 'Santo',
            'PADRE': 'Padre',
            'FRANCISCO': 'Francisco',
            'AMOR': 'Amor',
            'HUMANO': 'Humano',
            'DIVINO': 'Divino'
        }
        
        # Aplicar correcciones palabra por palabra
        palabras = texto.split()
        palabras_corregidas = []
        
        for palabra in palabras:
            # Separar signos de puntuación
            inicio = ''
            final = ''
            palabra_limpia = palabra
            
            # Extraer signos del inicio
            while palabra_limpia and not palabra_limpia[0].isalnum():
                inicio += palabra_limpia[0]
                palabra_limpia = palabra_limpia[1:]
            
            # Extraer signos del final
            while palabra_limpia and not palabra_limpia[-1].isalnum():
                final = palabra_limpia[-1] + final
                palabra_limpia = palabra_limpia[:-1]
            
            # Aplicar corrección si existe
            if palabra_limpia in correcciones:
                palabra_corregida = correcciones[palabra_limpia]
            else:
                palabra_corregida = palabra_limpia
                
            # Correcciones de patrones específicos para palabras no encontradas
            if palabra_corregida:
                # Corregir terminaciones -ciones truncadas
                if palabra_corregida.endswith('cione') and not palabra_corregida.endswith('ciones'):
                    palabra_corregida += 's'
                elif palabra_corregida.endswith('cion') and not palabra_corregida.endswith('ción'):
                    palabra_corregida = palabra_corregida[:-4] + 'ción'
                elif palabra_corregida.endswith('ciones') and not palabra_corregida.endswith('ciones'):
                    palabra_corregida = palabra_corregida[:-7] + 'ciones'
            
            palabras_corregidas.append(inicio + palabra_corregida + final)
        
        return ' '.join(palabras_corregidas)
    
    def limpiar_titulo(nombre):
        """Limpia el título eliminando extensiones, números entre paréntesis y formatea con primera letra mayúscula"""
        # Quitar extensión
        titulo = nombre.rsplit('.', 1)[0]
        
        # Quitar números entre paréntesis como (1), (2), etc.
        titulo = re.sub(r'\(\d+\)', '', titulo)
        
        # Quitar fechas del principio (formato YYYY-MM-DD o DD-MM-YY, etc.)
        titulo = re.sub(r'^\d{4}-\d{2}-\d{2}_?', '', titulo)
        titulo = re.sub(r'^\d{2}-\d{2}-\d{2,4}_?', '', titulo)
        titulo = re.sub(r'^\d{2}_\d{2}_\d{2,4}_?', '', titulo)
        titulo = re.sub(r'^\d{4}_\d{2}_\d{2}_?', '', titulo)
        
        # Quitar extensiones adicionales que puedan haber quedado (.docx, .doc, .pdf, etc.)
        titulo = re.sub(r'\.(docx?|pdf|txt|dot)$', '', titulo, flags=re.IGNORECASE)
        
        # Reemplazar guiones y guiones bajos con espacios
        titulo = titulo.replace('-', ' ')
        titulo = titulo.replace('_', ' ')
        
        # Limpiar espacios extra
        titulo = ' '.join(titulo.split())
        
        # Si está todo en mayúsculas, convertir a formato título
        if titulo.isupper():
            titulo = titulo.title()
            # Corregir algunas palabras que quedan mal con title()
            titulo = titulo.replace('De La', 'de la')
            titulo = titulo.replace('De Los', 'de los')
            titulo = titulo.replace('Del', 'del')
            titulo = titulo.replace('En El', 'en el')
            titulo = titulo.replace('En La', 'en la')
            titulo = titulo.replace('Con El', 'con el')
            titulo = titulo.replace('Con La', 'con la')
            titulo = titulo.replace('Para El', 'para el')
            titulo = titulo.replace('Para La', 'para la')
            titulo = titulo.replace('Por El', 'por el')
            titulo = titulo.replace('Por La', 'por la')
            titulo = titulo.replace('Sobre El', 'sobre el')
            titulo = titulo.replace('Sobre La', 'sobre la')
            titulo = titulo.replace('Y El', 'y el')
            titulo = titulo.replace('Y La', 'y la')
        # Si no, solo capitalizar primera letra
        elif titulo:
            titulo = titulo[0].upper() + titulo[1:]
        
        # Aplicar corrección ortográfica
        titulo = corregir_ortografia(titulo)
        
        return titulo
    
    def obtener_directorio_y_nombre(nombre):
        """Extrae el directorio (parte antes del primer guion) y el nombre del archivo"""
        partes = nombre.split(' - ', 1)
        if len(partes) == 2:
            directorio = partes[0].strip()
            nombre_archivo = partes[1].strip()
            return directorio.lower(), nombre_archivo.lower()
        return "", nombre.lower()

    print("[3/3] Generando fuente_agente.json a partir de los caches...")
    with open(os.path.join(cache_dir, "cache_textuales.json"), "r", encoding="utf-8") as f:
        textuales_files = json.load(f)
    with open(os.path.join(cache_dir, "cache_buscador_fares.json"), "r", encoding="utf-8") as f:
        buscador_files = json.load(f)
    # Crear un índice de BUSCADOR FARES organizando por directorio/nombre
    buscador_dict = {}
    for bf in buscador_files:
        # Usar el path como directorio y el nombre sin extensión
        path = bf.get("path", "").lower()
        nombre = quitar_extension(bf["name"].lower())
        
        # Siempre indexar por nombre para búsqueda flexible
        if nombre not in buscador_dict:
            buscador_dict[nombre] = []
        buscador_dict[nombre].append(bf)
        print(f"Indexando en BUSCADOR por nombre: {nombre}")
        
        # Si hay path, crear índices adicionales por directorio
        if path:
            paths = path.split('/')
            for i in range(len(paths)):
                subpath = '/'.join(paths[0:i+1])
                key = f"{subpath}/{nombre}"
                if key not in buscador_dict:
                    buscador_dict[key] = []
                print(f"Indexando en BUSCADOR por ruta: {key}")
                buscador_dict[key].append(bf)

    resultado = []
    for tf in textuales_files:
        # Extraer directorio y nombre del archivo TEXTUAL
        directorio, nombre_completo = obtener_directorio_y_nombre(tf["name"])
        nombre_archivo = quitar_extension(nombre_completo)
        print(f"\nArchivo TEXTUALES: {tf['name']}")
        print(f"Directorio extraído: {directorio}")
        print(f"Nombre sin extensión: {nombre_archivo}")
        
        # Buscar primero por nombre completo sin directorio
        print(f"Buscando en BUSCADOR FARES por nombre: {nombre_archivo}")
        related_files = buscador_dict.get(nombre_archivo, [])
        
        # Si no se encuentra y hay directorio, intentar con el path completo
        if not related_files and directorio:
            clave_busqueda = f"{directorio}/{nombre_archivo}"
            print(f"Buscando en BUSCADOR FARES por directorio/nombre: {clave_busqueda}")
            related_files = buscador_dict.get(clave_busqueda, [])
        
        fila = {"file": tf["name"]}
        if related_files:
            # Solo tomamos el primer archivo relacionado
            rf = related_files[0]
            fila["link"] = f"https://drive.google.com/file/d/{rf['id']}/view?usp=drive_link"
            fila["title"] = limpiar_titulo(rf["name"])
            print(f"  Relacionado con: {rf['name']} | {fila['link']}")
        else:
            print("  No se encontró archivo relacionado en BUSCADOR FARES para este archivo.")
        resultado.append(fila)
    output_path = os.path.join(output_dir, "fuente_agente.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=4)
    print(f"Archivo {output_path} generado con {len(resultado)} elementos.")

if __name__ == "__main__":
    cache_dir = "cache"
    output_dir = "salida"
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    resultado = generar_fuente_agente(cache_dir, output_dir)
    if resultado is None:
        print("La ejecución se detuvo por un archivo no encontrado.")
