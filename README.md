# lector_gdrive

Librería en Python para leer los contenidos de un directorio en Google Drive usando la API oficial de Google.

## Instalación

1. Clona este repositorio y entra en la carpeta:
   ```bash
   git clone <url-del-repo>
   cd lectorGDrive
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso en Docker

1. Copia tu archivo de credenciales de Google (ver abajo) como `credentials.json` en la raíz del proyecto.
2. Construye la imagen:
   ```bash
   docker build -t lector_gdrive .
   ```
3. Ejecuta el contenedor:
   ```bash
   docker run --env-file .env -v $(pwd)/credentials.json:/app/credentials.json lector_gdrive
   ```

## Cómo obtener el archivo de credenciales de Google (Service Account)

1. Ve a [Google Cloud Console](https://console.cloud.google.com/).
2. Crea un nuevo proyecto o selecciona uno existente.
3. Ve a **APIs y servicios > Habilitar APIs y servicios** y busca "Google Drive API". Haz clic en "Habilitar".
4. Ve a **IAM y administración > Cuentas de servicio**.
5. Haz clic en "Crear cuenta de servicio".
6. Asigna un nombre y descripción. Haz clic en "Crear y continuar".
7. Asigna el rol "Editor" o "Lector" según lo que necesites. Haz clic en "Continuar" y luego en "Listo".
8. Haz clic en la cuenta de servicio creada y ve a la pestaña "Claves".
9. Haz clic en "Agregar clave" > "Crear nueva clave" > selecciona JSON y descarga el archivo. Renómbralo como `credentials.json` y colócalo en la raíz del proyecto.
10. Comparte la carpeta de Google Drive que quieras leer con el email de la cuenta de servicio (aparece en la consola de Google Cloud).

## Cómo compartir el directorio de Google Drive con la cuenta de servicio

Para que la aplicación pueda acceder a los archivos, debes compartir el directorio de Google Drive con la cuenta de servicio:

1. Ingresa a [Google Drive](https://drive.google.com/) con tu cuenta.
2. Busca la carpeta que deseas compartir.
3. Haz clic derecho sobre la carpeta y selecciona **Compartir**.
4. En el campo para añadir personas o grupos, ingresa el correo de la cuenta de servicio:
   ```
   lector-padre-farez@balmy-ground-471400-a8.iam.gserviceaccount.com
   ```
5. Asigna el permiso de **Lector** (o superior si necesitas modificar archivos).
6. Haz clic en **Enviar**.

Ahora la cuenta de servicio tendrá acceso a los archivos de esa carpeta y la aplicación podrá listarlos correctamente.

## Variables de entorno

Copia `.env.example` a `.env` y ajusta la ruta si es necesario:
```
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
```

## Ejemplo de uso
```python
from lector_gdrive import GDriveReader

reader = GDriveReader('/app/credentials.json')
folder_id = 'TU_FOLDER_ID'
archivos = reader.list_directory(folder_id)
for archivo in archivos:
    print(archivo)
```
