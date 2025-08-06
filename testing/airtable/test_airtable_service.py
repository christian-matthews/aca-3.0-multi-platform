#!/usr/bin/env python3
"""
🧪 Script de Testing para Airtable Service
Verificar la integración con Airtable
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from app.services.airtable_service import get_airtable_service
# Comentamos sync_service por ahora para probar solo Airtable
# from app.services.sync_service import get_sync_service
import json

def main():
    print("🧪 Testing Airtable Service para ACA 3.0")
    print("=" * 50)
    
    # Test 1: Conexión básica
    print("\n1️⃣ Probando conexión con Airtable...")
    airtable_service = get_airtable_service()
    
    connection_result = airtable_service.test_connection()
    print(f"✅ Resultado: {json.dumps(connection_result, indent=2, ensure_ascii=False)}")
    
    if not connection_result.get('success'):
        print("❌ No se pudo conectar con Airtable")
        print("💡 Verifica que tengas configuradas las variables:")
        print("   - AIRTABLE_API_KEY")
        print("   - AIRTABLE_BASE_ID")
        print("   - AIRTABLE_TABLE_NAME")
        return False
    
    # Test 2: Obtener registros
    print("\n2️⃣ Obteniendo registros de Airtable...")
    records = airtable_service.get_all_records()
    print(f"📊 Total de registros: {len(records)}")
    
    if records:
        print("📋 Primer registro (ejemplo):")
        first_record = records[0]
        print(f"   ID: {first_record.get('id')}")
        print(f"   Empresa: {first_record.get('empresa')}")
        print(f"   Tipo: {first_record.get('tipo_documento')}")
        print(f"   Estado: {first_record.get('estado')}")
    
    # Test 3: Registros pendientes
    print("\n3️⃣ Obteniendo registros pendientes...")
    pending_records = airtable_service.get_pending_records()
    print(f"⏳ Registros pendientes: {len(pending_records)}")
    
    # Test 4: Estadísticas
    print("\n4️⃣ Obteniendo estadísticas...")
    stats = airtable_service.get_statistics()
    print(f"📈 Estadísticas: {json.dumps(stats, indent=2, ensure_ascii=False)}")
    
    # Test 5: Servicio de sincronización (comentado por ahora)
    print("\n5️⃣ Servicio de sincronización disponible cuando configures Airtable...")
    print("💡 Configura primero las credenciales de Airtable para probar la sincronización")
    
    print("\n🎉 Tests completados exitosamente!")
    print("\n📋 Próximos pasos:")
    print("1. Configurar tu base de Airtable con la estructura recomendada")
    print("2. Subir algunos documentos de prueba")
    print("3. Ejecutar sincronización: POST /sync/airtable")
    print("4. Verificar que los datos aparezcan en Supabase")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error en testing: {e}")
        sys.exit(1)