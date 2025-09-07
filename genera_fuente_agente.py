import os
import json
from lector_gdrive import GDriveReader

def get_all_files(service, folder_id, parent_path=""):
    """
    Recorre recursivamente todos los archivos en un directorio de Google Drive.
    Devuelve una lista de diccionarios con 'id', 'name', 'mimeType', 'path'.
    """
    files = []
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="files(id, name, mimeType)"
    ).execute()
    for f in results.get('files', []):
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            files += get_all_files(service, f['id'], os.path.join(parent_path, f['name']))
        else:
            files.append({
                'id': f['id'],
                'name': f['name'],
                'path': parent_path
            })
    return files

if __name__ == "__main__":
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    reader = GDriveReader(creds_path)
    service = reader.service

    # IDs de los directorios
    buscador_fares_id = "1SjN3b2k05l82akwH24kPZOuuG82g-yk1"
    textuales_id = "1DnWDELBR8RniMk8VWM0yV7r8eA4l8Ei3"

    print("Obteniendo archivos de BUSCADOR FARES...")
    buscador_files = get_all_files(service, buscador_fares_id)
    print(f"Archivos encontrados en BUSCADOR FARES: {len(buscador_files)}")

    print("Obteniendo archivos de TEXTUALES...")
    textuales_files = get_all_files(service, textuales_id)
    print(f"Archivos encontrados en TEXTUALES: {len(textuales_files)}")

    # Crear un diccionario para buscar archivos en TEXTUALES por nombre
    textuales_dict = {}
    for f in textuales_files:
        key = f["name"].lower()
        textuales_dict[key] = f

    resultado = []

    for f in buscador_files:
        # Concatenar nombre del archivo y subdirectorio
        titulo = f["name"]
        if f["path"]:
            titulo = f["path"].replace(os.sep, "_") + "_" + titulo
        # Buscar archivo relacionado en TEXTUALES
        related = textuales_dict.get(f["name"].lower())
        print(f"Procesando: {titulo}")
        if related:
            link = f"https://drive.google.com/file/d/{related['id']}/view?usp=drive_link"
            print(f"  Relacionado con: {related['name']} | {link}")
            resultado.append({
                "titulo": titulo,
                "link": link
            })
        else:
            print("  No se encontró archivo relacionado en TEXTUALES.")
        input("Presiona Enter para continuar...")

    with open("fuente_agente.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=4)
    print(f"Archivo fuente_agente.json generado con {len(resultado)} elementos.")
