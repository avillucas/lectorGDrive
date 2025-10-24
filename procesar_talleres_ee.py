import json
import os
import shutil
from pathlib import Path

def leer_listado_ee():
    """Lee el archivo listadoee.txt y extrae los nombres de archivos."""
    listado_path = Path("pdfs/listadoee.txt")
    nombres_archivos = []
    
    if listado_path.exists():
        with open(listado_path, 'r', encoding='utf-8') as f:
            for linea in f:
                nombre = linea.strip()
                if nombre and not nombre.startswith('#'):  # Ignorar líneas vacías y comentarios
                    nombres_archivos.append(nombre)
        print(f"✓ Leídos {len(nombres_archivos)} nombres de archivo desde {listado_path}")
    else:
        print(f"✗ Archivo {listado_path} no encontrado")
    
    return nombres_archivos

def buscar_objetos_en_fuente_agente(nombres_archivos):
    """Busca objetos en fuente_agente.json que coincidan con los nombres de archivos."""
    fuente_path = Path("salida/fuente_agente.json")
    objetos_encontrados = []
    
    if not fuente_path.exists():
        print(f"✗ Archivo {fuente_path} no encontrado")
        return objetos_encontrados
    
    try:
        with open(fuente_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Cargado archivo JSON con {len(data)} elementos")
    except json.JSONDecodeError as e:
        print(f"✗ Error al leer JSON: {e}")
        return objetos_encontrados
    
    for nombre_archivo in nombres_archivos:
        # Buscar con diferentes patrones posibles
        patrones_busqueda = [
            f"{nombre_archivo}"
        ]
        
        encontrado = False
        for patron in patrones_busqueda:
            for obj in data:
                if obj.get("file") == patron and obj.get("link"):
                    objetos_encontrados.append({
                        "nombre_original": nombre_archivo,
                        "file": obj["file"],
                        "link": obj["link"],
                        "title": obj.get("title", "Sin título")
                    })
                    print(f"✓ Encontrado: {patron}")
                    encontrado = True
                    break
            if encontrado:
                break
        
        if not encontrado:
            print(f"✗ No encontrado: {nombre_archivo}")
    
    return objetos_encontrados

def crear_directorios():
    """Crea los directorios necesarios si no existen."""
    directorios = ["talleres", "articulos", "salida"]
    for directorio in directorios:
        Path(directorio).mkdir(exist_ok=True)
    print(f"✓ Directorios verificados: {', '.join(directorios)}")

def mover_archivos(objetos_encontrados):
    """Mueve los archivos del directorio articulos al directorio talleres."""
    articulos_dir = Path("articulos")
    talleres_dir = Path("talleres")
    
    archivos_movidos = []
    archivos_no_encontrados = []
    
    if not articulos_dir.exists():
        print(f"⚠ Directorio {articulos_dir} no existe, creándolo...")
        articulos_dir.mkdir(exist_ok=True)
    
    for obj in objetos_encontrados:
        archivo_origen = articulos_dir / obj["file"]
        archivo_destino = talleres_dir / obj["file"]
        
        if archivo_origen.exists():
            try:
                # Crear directorio destino si no existe
                archivo_destino.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(archivo_origen), str(archivo_destino))
                archivos_movidos.append({
                    "archivo": obj["file"],
                    "link": obj["link"],
                    "title": obj["title"],
                    "nombre_original": obj["nombre_original"]
                })
                print(f"✓ Movido: {obj['file']}")
            except Exception as e:
                print(f"✗ Error moviendo {obj['file']}: {e}")
        else:
            archivos_no_encontrados.append({
                "archivo": obj["file"],
                "nombre_original": obj["nombre_original"],
                "link": obj["link"]
            })
            print(f"✗ Archivo no encontrado físicamente: {obj['file']}")
    
    return archivos_movidos, archivos_no_encontrados

def guardar_reporte(objetos_encontrados, archivos_movidos, archivos_no_encontrados):
    """Guarda un reporte detallado del procesamiento."""
    reporte = {
        "resumen": {
            "objetos_encontrados_en_json": len(objetos_encontrados),
            "archivos_movidos_exitosamente": len(archivos_movidos),
            "archivos_no_encontrados_fisicamente": len(archivos_no_encontrados),
            "fecha_procesamiento": str(Path().resolve()),
            "directorio_trabajo": str(Path().resolve())
        },
        "links_google_drive": [obj["link"] for obj in objetos_encontrados],
        "archivos_procesados": {
            "movidos_exitosamente": archivos_movidos,
            "no_encontrados_fisicamente": archivos_no_encontrados
        },
        "objetos_completos": objetos_encontrados
    }
    
    # Guardar reporte en JSON
    reporte_path = Path("reporte_talleres_ee.json")
    with open(reporte_path, 'w', encoding='utf-8') as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
    
    # Guardar lista de links en archivo separado
    links_path = Path("links_google_drive.txt")
    with open(links_path, 'w', encoding='utf-8') as f:
        f.write("# Links de Google Drive extraídos\n")
        f.write(f"# Total: {len(objetos_encontrados)} links\n\n")
        for obj in objetos_encontrados:
            f.write(f"# {obj['title']}\n")
            f.write(f"{obj['link']}\n\n")
    
    print(f"\n{'='*60}")
    print(f"               REPORTE FINAL")
    print(f"{'='*60}")
    print(f"Objetos encontrados en JSON:       {reporte['resumen']['objetos_encontrados_en_json']}")
    print(f"Archivos movidos exitosamente:     {reporte['resumen']['archivos_movidos_exitosamente']}")
    print(f"Archivos no encontrados:           {reporte['resumen']['archivos_no_encontrados_fisicamente']}")
    print(f"")
    print(f"Archivos generados:")
    print(f"  - {reporte_path}")
    print(f"  - {links_path}")
    print(f"{'='*60}")

def main():
    """Función principal que ejecuta todo el proceso."""
    print("="*80)
    print("        PROCESAMIENTO DE TALLERES DE EJERCICIOS ESPIRITUALES")
    print("="*80)
    
    # 0. Crear directorios necesarios
    print("\n📁 Verificando directorios...")
    crear_directorios()
    
    # 1. Leer listado de nombres de archivos
    print("\n📋 1. Leyendo listadoee.txt...")
    nombres_archivos = leer_listado_ee()
    
    if not nombres_archivos:
        print("⚠ No se encontraron nombres de archivos para procesar")
        return
    
    # 2. Buscar objetos correspondientes en fuente_agente.json
    print(f"\n🔍 2. Buscando objetos en fuente_agente.json...")
    objetos_encontrados = buscar_objetos_en_fuente_agente(nombres_archivos)
    
    # 3. Mostrar links encontrados
    print(f"\n🔗 3. Links de Google Drive extraídos: {len(objetos_encontrados)}")
    for i, obj in enumerate(objetos_encontrados, 1):
        print(f"   {i:2d}. {obj['title']}")
        print(f"       {obj['link']}")
    
    # 4. Mover archivos del directorio articulos al directorio talleres
    print(f"\n📁 4. Moviendo archivos de articulos/ a talleres/...")
    archivos_movidos, archivos_no_encontrados = mover_archivos(objetos_encontrados)
    
    # 5. Guardar reporte
    print(f"\n📊 5. Generando reporte...")
    guardar_reporte(objetos_encontrados, archivos_movidos, archivos_no_encontrados)

if __name__ == "__main__":
    main()
