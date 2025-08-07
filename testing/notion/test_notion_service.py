#!/usr/bin/env python3
"""
Test script para verificar integración con Notion
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.notion_service import NotionService
from app.database.supabase import supabase
import asyncio

def test_notion_connection():
    """Probar conexión con Notion"""
    print("🧪 Probando conexión con Notion...")
    
    notion = NotionService()
    
    if notion.test_connection():
        print("✅ Conexión exitosa con Notion")
        return True
    else:
        print("❌ Error en conexión con Notion")
        return False

def sync_empresas_to_notion():
    """Sincronizar empresas de Supabase a Notion"""
    print("🔄 Sincronizando empresas a Notion...")
    
    try:
        # Obtener empresas desde Supabase
        empresas_response = supabase.table('empresas').select('*').eq('activo', True).execute()
        empresas = empresas_response.data
        
        print(f"📊 Encontradas {len(empresas)} empresas activas")
        
        notion = NotionService()
        
        # Limpiar database primero
        print("🧹 Limpiando database de Notion...")
        notion.clear_database()
        
        # Agregar cada empresa
        for empresa in empresas:
            # Obtener conteo de reportes para esta empresa
            reportes_response = supabase.table('reportes_mensuales').select('id', count='exact').eq('empresa_id', empresa['id']).execute()
            reportes_count = reportes_response.count if hasattr(reportes_response, 'count') else 0
            
            # Obtener último reporte
            ultimo_reporte_response = supabase.table('reportes_mensuales').select('creado_en').eq('empresa_id', empresa['id']).order('creado_en', desc=True).limit(1).execute()
            ultimo_reporte = ultimo_reporte_response.data[0]['creado_en'][:10] if ultimo_reporte_response.data else None
            
            empresa_data = {
                "id": empresa['id'],
                "nombre": empresa['nombre'],
                "rut": empresa['rut'],
                "reportes_count": reportes_count,
                "ultimo_reporte": ultimo_reporte,
                "activo": empresa['activo']
            }
            
            if notion.add_empresa_row(empresa_data):
                print(f"✅ Empresa agregada: {empresa['nombre']}")
            else:
                print(f"❌ Error agregando: {empresa['nombre']}")
        
        print("🎉 Sincronización completada")
        
    except Exception as e:
        print(f"❌ Error en sincronización: {e}")

if __name__ == "__main__":
    print("🚀 Test de integración Notion")
    print("-" * 40)
    
    # Paso 1: Probar conexión
    if test_notion_connection():
        print()
        # Paso 2: Sincronizar datos
        sync_empresas_to_notion()
    else:
        print("❌ No se puede continuar sin conexión a Notion")
    
    print("-" * 40)
    print("✅ Test completado")