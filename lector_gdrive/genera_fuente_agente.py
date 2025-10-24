import os
import json
import re

def generar_fuente_agente(cache_dir, output_dir):
    print("[3/3] Generando fuente_agente.json a partir de los caches...")
    
    # Cargar cache de textuales
    cache_textuales_path = os.path.join(cache_dir, "cache_textuales.json")
    cache_buscador_fares_path = os.path.join(cache_dir, "cache_buscador_fares.json")
    
    fuente_agente = []
    
    # Procesar cache textuales
    if os.path.exists(cache_textuales_path):
        with open(cache_textuales_path, 'r', encoding='utf-8') as f:
            textuales_data = json.load(f)
        
        for item in textuales_data:
            fuente_agente.append({
                "id": item["id"],
                "file": item["name"],
                "link": f"https://drive.google.com/file/d/{item['id']}/view",
                "title": item["name"].replace(".txt", "")
            })
        print(f"Agregados {len(textuales_data)} elementos de textuales")
    
    # Procesar cache buscador fares
    if os.path.exists(cache_buscador_fares_path):
        with open(cache_buscador_fares_path, 'r', encoding='utf-8') as f:
            buscador_fares_data = json.load(f)
        
        for item in buscador_fares_data:
            fuente_agente.append({
                "id": item["id"],
                "file": item["name"],
                "link": f"https://drive.google.com/file/d/{item['id']}/view",
                "title": item["name"].replace(".txt", "")
            })
        print(f"Agregados {len(buscador_fares_data)} elementos de buscador fares")
    
    # Guardar fuente_agente.json
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "fuente_agente.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(fuente_agente, f, ensure_ascii=False, indent=2)
    
    print(f"fuente_agente.json generado con {len(fuente_agente)} elementos en {output_path}")
    return fuente_agente

def verificar_correspondencia_textuales():
    """Verifica que cada objeto en cache_textuales.json tenga correspondencia en fuente_agente.json"""
    print("\n=== VERIFICACIÓN DE CORRESPONDENCIA TEXTUALES ===")
    
    cache_textuales_path = "cache/cache_textuales.json"
    fuente_agente_path = "salida/fuente_agente.json"
    
    # Verificar que existan los archivos
    if not os.path.exists(cache_textuales_path):
        print(f"❌ No se encuentra {cache_textuales_path}")
        return False
    
    if not os.path.exists(fuente_agente_path):
        print(f"❌ No se encuentra {fuente_agente_path}")
        return False
    
    # Cargar archivos
    with open(cache_textuales_path, 'r', encoding='utf-8') as f:
        textuales_data = json.load(f)
    
    with open(fuente_agente_path, 'r', encoding='utf-8') as f:
        fuente_agente_data = json.load(f)
    
    # Crear un índice de fuente_agente por id para búsqueda rápida
    fuente_agente_ids = {item["id"] for item in fuente_agente_data}
    
    print(f"📊 Objetos en cache_textuales.json: {len(textuales_data)}")
    print(f"📊 Objetos en fuente_agente.json: {len(fuente_agente_data)}")
    
    # Verificar correspondencias
    encontrados = 0
    no_encontrados = []
    
    for item in textuales_data:
        if item["id"] in fuente_agente_ids:
            encontrados += 1
        else:
            no_encontrados.append({
                "id": item["id"],
                "name": item["name"],
                "path": item.get("path", "")
            })
    
    print(f"\n✅ Encontrados: {encontrados}/{len(textuales_data)}")
    print(f"❌ No encontrados: {len(no_encontrados)}")
    
    if no_encontrados:
        print("\n🔍 Objetos de textuales NO encontrados en fuente_agente:")
        for item in no_encontrados[:10]:  # Mostrar solo los primeros 10
            print(f"   - {item['id']}: {item['name']}")
        if len(no_encontrados) > 10:
            print(f"   ... y {len(no_encontrados) - 10} más")
    
    # Estadísticas finales
    porcentaje = (encontrados / len(textuales_data)) * 100 if textuales_data else 0
    print(f"\n📈 Cobertura: {porcentaje:.1f}%")
    
    if porcentaje == 100:
        print("🎉 ¡Perfecta correspondencia! Todos los objetos de textuales están en fuente_agente")
        return True
    else:
        print("⚠️  Hay objetos de textuales que no están en fuente_agente")
        return False

def actualizar_titulos_desde_csvs(fuente_agente, titulos_dir="titulos"):
    """Actualiza los títulos en fuente_agente usando archivos CSV del directorio titulos"""
    from .actualiza_titulos_csv import actualizar_titulos_desde_csvs as actualizar
    return actualizar(fuente_agente, titulos_dir)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generar fuente_agente.json y verificar correspondencias')
    parser.add_argument('--verificar', action='store_true', help='Solo verificar correspondencia sin generar')
    parser.add_argument('--cache_dir', default='cache', help='Directorio de cache')
    parser.add_argument('--output_dir', default='salida', help='Directorio de salida')
    parser.add_argument('--actualizar_titulos', action='store_true', help='Actualizar títulos desde archivos CSV')
    parser.add_argument('--titulos_dir', default='titulos', help='Directorio con archivos CSV de títulos')
    
    args = parser.parse_args()
    
    if args.verificar:
        verificar_correspondencia_textuales()
    else:
        # Generar fuente_agente.json
        fuente_agente = generar_fuente_agente(args.cache_dir, args.output_dir)
        
        # Actualizar títulos si se solicita
        if args.actualizar_titulos:
            print("\n🔄 Actualizando títulos desde archivos CSV...")
            try:
                from actualiza_titulos_csv import actualizar_titulos_desde_csvs
                total_actualizados = actualizar_titulos_desde_csvs(fuente_agente, args.titulos_dir)
                
                if total_actualizados > 0:
                    # Guardar archivo actualizado
                    output_path = os.path.join(args.output_dir, "fuente_agente.json")
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(fuente_agente, f, ensure_ascii=False, indent=2)
                    print(f"✅ Títulos actualizados y guardados: {total_actualizados} cambios")
            except ImportError:
                print("⚠️  No se pudo importar el actualizador de títulos")
            except Exception as e:
                print(f"❌ Error actualizando títulos: {e}")
        
        # Verificar correspondencia después de generar
        verificar_correspondencia_textuales()
