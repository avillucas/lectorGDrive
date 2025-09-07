import os
import json

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
    page_token = None
    while True:
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token
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
        page_token = results.get('nextPageToken', None)
        if not page_token:
            break
    if cache_file:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(files, f, ensure_ascii=False, indent=2)
        print(f"Resultados guardados en cache: {cache_file}")
    return files
