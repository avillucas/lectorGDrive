import os
import json

def generar_fuente_agente(cache_dir, output_dir):
    print("[3/3] Generando fuente_agente.json a partir de los caches...")
    with open(os.path.join(cache_dir, "cache_textuales.json"), "r", encoding="utf-8") as f:
        textuales_files = json.load(f)
    with open(os.path.join(cache_dir, "cache_buscador_fares.json"), "r", encoding="utf-8") as f:
        buscador_files = json.load(f)
    # Usar tanto nombre como path para la búsqueda en textuales
    textuales_dict = {}
    for tf in textuales_files:
        key = tf["name"].lower()
        if tf.get("path"):
            key = tf["path"].replace(os.sep, "_").lower() + "_" + key
        textuales_dict[key] = tf

    resultado = []
    for f in buscador_files:
        # Construir el título y la clave de búsqueda igual que en textuales
        titulo = f["name"]
        if f["path"]:
            #titulo = f["path"].replace(os.sep, "_") + "_" + titulo
            titulo = f["path"].replace(os.sep, "-") 
        print(f"Archivo a buscar: {titulo}")
        # Tomar solo la parte después del primer guion
        path = ''
        nombre_buscador = f["name"].lower()
        if '-' in nombre_buscador:
            nombre_busqueda = nombre_buscador.split('-', 1)[1].strip()
        else:
            nombre_busqueda = nombre_buscador
        # Incluir path en la clave de búsqueda si existe
        if f.get("path"):
            clave_busqueda = f["path"].replace(os.sep, "_").lower() + "_" + nombre_busqueda
        else:
            clave_busqueda = nombre_busqueda
        print(f"Buscando en TEXTUALES por clave: {clave_busqueda}")
        related = textuales_dict.get(clave_busqueda)
        fila = {"titulo": titulo}
        if related:
            fila["link"] = f"https://drive.google.com/file/d/{related['id']}/view?usp=drive_link"
            print(f"  Relacionado con: {related['name']} | {fila['link']}")
        else:
            print("  No se encontró archivo relacionado en TEXTUALES (esto es normal si no hay correspondencia, no es un error). No se agregará la clave 'link'.")
        resultado.append(fila)
    output_path = os.path.join(output_dir, "fuente_agente.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=4)
    print(f"Archivo {output_path} generado con {len(resultado)} elementos.")

if __name__ == "__main__":
    cache_dir = "cache"
    output_dir = "salida"
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    generar_fuente_agente(cache_dir, output_dir)
