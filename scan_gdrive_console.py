import os
from lector_gdrive import GDriveReader

if __name__ == "__main__":
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    output_dir = "salida"
    os.makedirs(output_dir, exist_ok=True)

    folder_id = input("Ingrese el ID del directorio de Google Drive a escanear: ").strip()
    if not folder_id:
        print("Debe ingresar un ID de directorio válido.")
        exit(1)

    reader = GDriveReader(creds_path)
    output_csv = os.path.join(output_dir, f"listado_{folder_id}.csv")
    try:
        files = reader.list_directory(folder_id)
        print(f"Archivos encontrados: {len(files)}")
        if files:
            for f in files:
                share_url = f"https://drive.google.com/file/d/{f['id']}/view" if f['mimeType'] != 'application/vnd.google-apps.folder' else f"https://drive.google.com/drive/folders/{f['id']}"
                print(f"- {f['name']} | {share_url}")
        else:
            print("No se encontraron archivos en el directorio o no hay permisos de acceso.")
        reader.export_directory_to_csv(folder_id, output_csv)
        print(f"CSV generado en: {output_csv}")
    except Exception as e:
        print(f"Error al consultar la API de Google Drive: {e}")
