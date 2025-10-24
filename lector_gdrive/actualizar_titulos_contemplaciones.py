#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys

def mejorar_titulos():
    """
    Mejora los títulos de fuente_agente.json usando los títulos de contemplaciones.json
    """
    print("Iniciando actualización de títulos...")
    
    try:
        # Rutas de los archivos
        fuente_agente_path = 'fuente_agente.json'
        contemplaciones_path = 'titulos/contemplaciones.json'
        
        # Verificar que los archivos existan
        if not os.path.exists(fuente_agente_path):
            print(f"❌ Error: No se encontró {fuente_agente_path}")
            return False
            
        if not os.path.exists(contemplaciones_path):
            print(f"❌ Error: No se encontró {contemplaciones_path}")
            return False
        
        # Cargar fuente_agente.json
        print("📄 Cargando fuente_agente.json...")
        with open(fuente_agente_path, 'r', encoding='utf-8') as f:
            fuente_agente = json.load(f)
        
        # Cargar contemplaciones.json
        print("📄 Cargando contemplaciones.json...")
        with open(contemplaciones_path, 'r', encoding='utf-8') as f:
            contemplaciones = json.load(f)
        
        # Crear mapeo de títulos de contemplaciones
        print("🔍 Creando mapeo de títulos...")
        contemplaciones_titles = {}
        if 'posts' in contemplaciones:
            for post in contemplaciones['posts']:
                if 'title' in post:
                    contemplaciones_titles[post['title'].lower().strip()] = post['title']
        
        print(f"📊 Se encontraron {len(contemplaciones_titles)} títulos en contemplaciones.json")
        
        # Actualizar títulos
        actualizaciones = 0
        print("🔄 Actualizando títulos...")
        
        for obj in fuente_agente:
            if obj.get('file', '').startswith('contemplaciones -'):
                titulo_actual = obj.get('title', '').strip()
                
                # Buscar coincidencia exacta primero
                titulo_mejorado = contemplaciones_titles.get(titulo_actual.lower())
                
                # Si no hay coincidencia exacta, buscar coincidencias parciales
                if not titulo_mejorado:
                    for contemp_title_lower, contemp_title_original in contemplaciones_titles.items():
                        if (titulo_actual.lower() in contemp_title_lower or 
                            contemp_title_lower in titulo_actual.lower()):
                            titulo_mejorado = contemp_title_original
                            break
                
                # Actualizar si se encontró una mejora
                if titulo_mejorado and titulo_mejorado != titulo_actual:
                    print(f"✏️  '{titulo_actual}' -> '{titulo_mejorado}'")
                    obj['title'] = titulo_mejorado
                    actualizaciones += 1
        
        # Guardar archivo actualizado
        print("💾 Guardando cambios...")
        with open(fuente_agente_path, 'w', encoding='utf-8') as f:
            json.dump(fuente_agente, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Proceso completado: {actualizaciones} títulos actualizados")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error al procesar JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    exito = mejorar_titulos()
    sys.exit(0 if exito else 1)
