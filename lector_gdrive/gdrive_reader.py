"""
libreria para leer contenidos de un directorio en Google Drive usando la API oficial de Google.
"""
import os
from typing import List, Dict
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

import csv

class GDriveReader:
    def __init__(self, service_account_file: str):
        self.creds = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES)
        self.service = build('drive', 'v3', credentials=self.creds)

    def list_directory(self, folder_id: str) -> List[Dict]:
        """
        Lista los archivos y carpetas dentro de un directorio de Google Drive.
        :param folder_id: ID de la carpeta de Google Drive
        :return: Lista de diccionarios con información de los archivos/carpetas
        """
        query = f"'{folder_id}' in parents and trashed = false"
        results = self.service.files().list(
            q=query,
            fields="files(id, name, mimeType)"
        ).execute()
        return results.get('files', [])

    def export_directory_to_csv(self, folder_id: str, csv_path: str):
        """
        Exporta los archivos y carpetas de un directorio de Google Drive a un archivo CSV,
        incluyendo los enlaces para compartir.
        :param folder_id: ID de la carpeta de Google Drive
        :param csv_path: Ruta del archivo CSV de salida
        """
        files = self.list_directory(folder_id)
        files_sorted = sorted(files, key=lambda x: x['name'].lower())
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'name', 'mimeType', 'share_url'])
            for f in files_sorted:
                share_url = f"https://drive.google.com/file/d/{f['id']}/view" if f['mimeType'] != 'application/vnd.google-apps.folder' else f"https://drive.google.com/drive/folders/{f['id']}"
                writer.writerow([f['id'], f['name'], f['mimeType'], share_url])
