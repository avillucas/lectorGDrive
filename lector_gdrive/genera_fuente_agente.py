import os
import json

def generar_fuente_agente(cache_dir, output_dir):
    def quitar_extension(nombre):
        """Quita la extensión del archivo (todo lo que sigue al último punto)"""
        return nombre.rsplit('.', 1)[0]
    
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
