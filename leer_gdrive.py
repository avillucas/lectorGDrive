import os
from lector_gdrive import GDriveReader

if __name__ == "__main__":
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    folder_id = os.environ.get("GDRIVE_FOLDER_ID")
    if not folder_id:
        raise ValueError("La variable de entorno GDRIVE_FOLDER_ID no está definida.")
    reader = GDriveReader(creds_path)
    archivos = reader.list_directory(folder_id)
    for archivo in archivos:
        print(archivo)
