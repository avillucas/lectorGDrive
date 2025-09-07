
import os
import sys
import json

# Permitir importar desde el directorio principal si se ejecuta desde shell/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lector_gdrive.gdrive_reader import GDriveReader
from genera_fuente_agente_utils import get_all_files

if __name__ == "__main__":
    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    reader = GDriveReader(creds_path)
    service = reader.service
    buscador_fares_id = "1SjN3b2k05l82akwH24kPZOuuG82g-yk1"
    print("[2/3] Obteniendo archivos de BUSCADOR FARES y generando cache...")
    files = get_all_files(service, buscador_fares_id, cache_file=os.path.join(cache_dir, "cache_buscador_fares.json"))
    print(f"[2/3] Archivos encontrados en BUSCADOR FARES: {len(files)}")
