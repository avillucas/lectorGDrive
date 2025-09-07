import os
import json

def generar_fuente_agente(cache_dir, output_dir):
    print("[3/3] Generando fuente_agente.json a partir de los caches...")
    with open(os.path.join(cache_dir, "cache_textuales.json"), "r", encoding="utf-8") as f:
        textuales_files = json.load(f)
    with open(os.path.join(cache_dir, "cache_buscador_fares.json"), "r", encoding="utf-8") as f:
        buscador_files = json.load(f)
    textuales_dict = {f["name"].lower(): f for f in textuales_files}
    resultado = []
    for f in buscador_files:
        titulo = f["name"]
        if f["path"]:
            titulo = f["path"].replace(os.sep, "_") + "_" + titulo
        print(f"Archivo a buscar: {titulo}")
        nombre_busqueda = f["name"].lower()
        print(f"Buscando en TEXTUALES por nombre: {nombre_busqueda}")
        related = textuales_dict.get(nombre_busqueda)
        if related:
            link = f"https://drive.google.com/file/d/{related['id']}/view?usp=drive_link"
            print(f"  Relacionado con: {related['name']} | {link}")
            resultado.append({
                "titulo": titulo,
                "link": link
            })
        else:
            print("  No se encontró archivo relacionado en TEXTUALES (esto es normal si no hay correspondencia, no es un error). No se agregará la clave 'link'.")
            resultado.append({
                "titulo": titulo
            })
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
