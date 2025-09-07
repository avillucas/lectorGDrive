import os
import json
from lector_gdrive import GDriveReader

def get_all_files(service, folder_id, parent_path="", cache_file=None):
    """
    Recorre recursivamente todos los archivos en un directorio de Google Drive.
    Devuelve una lista de diccionarios con 'id', 'name', 'mimeType', 'path'.
    Si cache_file está definido y existe, lee los resultados desde el cache.
    Asegura que se obtienen todos los archivos usando paginación.
    """
    if cache_file and os.path.exists(cache_file):
        print(f"Cargando resultados cacheados de {cache_file} ...")
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    files = []
    def generar_cache_textuales(service, textuales_id, cache_dir):
        print("[1/3] Obteniendo archivos de TEXTUALES y generando cache...")
        files = get_all_files(service, textuales_id, cache_file=os.path.join(cache_dir, "cache_textuales.json"))
        print(f"[1/3] Archivos encontrados en TEXTUALES: {len(files)}")
        return files

    def generar_cache_buscador_fares(service, buscador_fares_id, cache_dir):
        print("[2/3] Obteniendo archivos de BUSCADOR FARES y generando cache...")
        files = get_all_files(service, buscador_fares_id, cache_file=os.path.join(cache_dir, "cache_buscador_fares.json"))
        print(f"[2/3] Archivos encontrados en BUSCADOR FARES: {len(files)}")
        return files

    def generar_fuente_agente(cache_dir, output_dir):
        print("[3/3] Generando fuente_agente.json a partir de los caches...")
        with open(os.path.join(cache_dir, "cache_textuales.json"), "r", encoding="utf-8") as f:
            textuales_files = json.load(f)
        with open(os.path.join(cache_dir, "cache_buscador_fares.json"), "r", encoding="utf-8") as f:
            buscador_files = json.load(f)
        textuales_dict = {f["name"].lower(): f for f in textuales_files}
        resultado = []
        for f in buscador_files:
            # Concatenar nombre del archivo y subdirectorio
            titulo = f["name"]
            if f["path"]:
                titulo = f["path"].replace(os.sep, "_") + "_" + titulo
            print(f"Archivo a buscar: {titulo}")
            nombre_busqueda = f["name"].lower()
            print(f"Buscando en TEXTUALES por nombre: {nombre_busqueda}")
            related = textuales_dict.get(nombre_busqueda)
            if related:
                link = f"https://drive.google.com/file/d/{related['id']}/view?usp=drive_link"
                print(f"  Relacionado con: {related['name']} | {link}")
                resultado.append({
                    "titulo": titulo,
                    "link": link
                })
            else:
                print("  No se encontró archivo relacionado en TEXTUALES (esto es normal si no hay correspondencia, no es un error). No se agregará la clave 'link'.")
                resultado.append({
                    "titulo": titulo
                })
        output_path = os.path.join(output_dir, "fuente_agente.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=4)
        print(f"Archivo {output_path} generado con {len(resultado)} elementos.")


    if __name__ == "__main__":
        # Crear directorios de cache y salida si no existen
        cache_dir = "cache"
        output_dir = "salida"
        os.makedirs(cache_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
        reader = GDriveReader(creds_path)
        service = reader.service

        # IDs de los directorios
        buscador_fares_id = "1SjN3b2k05l82akwH24kPZOuuG82g-yk1"
        textuales_id = "1DnWDELBR8RniMk8VWM0yV7r8eA4l8Ei3"

        print("Selecciona una opción:")
        print("1. Generar/actualizar cache de TEXTUALES")
        print("2. Generar/actualizar cache de BUSCADOR FARES")
        print("3. Generar fuente_agente.json a partir de los caches")
        print("4. Ejecutar todo el proceso (1, 2 y 3)")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            generar_cache_textuales(service, textuales_id, cache_dir)
        elif opcion == "2":
            generar_cache_buscador_fares(service, buscador_fares_id, cache_dir)
        elif opcion == "3":
            generar_fuente_agente(cache_dir, output_dir)
        elif opcion == "4":
            generar_cache_textuales(service, textuales_id, cache_dir)
            generar_cache_buscador_fares(service, buscador_fares_id, cache_dir)
            generar_fuente_agente(cache_dir, output_dir)
        else:
            print("Opción no válida.")
