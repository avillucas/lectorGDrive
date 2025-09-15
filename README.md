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

## Variables de entorno adicionales

Puedes definir los directorios de entrada para los archivos textuales y del buscador Fares usando las siguientes variables de entorno:

```
TEXTUALES_DIR=/ruta/a/textuales
BUSCADOR_FARES_DIR=/ruta/a/buscador_fares
```

Por ejemplo, puedes exportarlas antes de ejecutar los scripts:
```bash
export TEXTUALES_DIR="/home/usuario/textuales"
export BUSCADOR_FARES_DIR="/home/usuario/buscador_fares"
./shell/run_genera_cache_textuales.sh
./shell/run_genera_cache_buscador_fares.sh
```

O bien, pasarlas en línea:
```bash
TEXTUALES_DIR="/home/usuario/textuales" BUSCADOR_FARES_DIR="/home/usuario/buscador_fares" ./shell/run_genera_fuente_agente.sh
```

Los scripts del directorio `shell/` detectarán estas variables y las usarán como rutas de entrada para los procesos correspondientes.

## Ejemplo de uso
```python
from lector_gdrive import GDriveReader

reader = GDriveReader('/app/credentials.json')
folder_id = 'TU_FOLDER_ID'
archivos = reader.list_directory(folder_id)
for archivo in archivos:
    print(archivo)
```

## Ejecución de procesos desde Shell

En la raíz del proyecto encontrarás un directorio llamado `shell/` que contiene varios scripts para automatizar tareas. Para ejecutarlos, abre una terminal y navega a la carpeta raíz del proyecto.

### 1. Generar cache del buscador Fares
```bash
./shell/run_genera_cache_buscador_fares.sh
```
Genera el archivo de caché `cache/cache_buscador_fares.json` a partir de los datos fuente.

### 2. Generar cache textuales
```bash
./shell/run_genera_cache_textuales.sh
```
Genera el archivo de caché `cache/cache_textuales.json` a partir de los datos fuente.

### 3. Generar fuente agente final
```bash
./shell/run_genera_fuente_agente_final.sh
```
Genera el archivo final de fuente agente usando los caches previos.

### 4. Generar fuente agente (principal)
```bash
./shell/run_genera_fuente_agente.sh
```
Genera el archivo `salida/fuente_agente.json` combinando la información de los caches.

---

**Notas:**
- Asegúrate de tener permisos de ejecución sobre los scripts. Si no los tienes, puedes otorgarlos con:
  ```bash
  chmod +x shell/*.sh
  ```
- Ejecuta los scripts en el orden indicado para evitar errores por archivos de caché faltantes.
- Los resultados se almacenan en la carpeta `cache/` y `salida/`.
