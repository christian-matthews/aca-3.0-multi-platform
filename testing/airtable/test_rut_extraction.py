#!/usr/bin/env python3
"""
🧪 Test de Extracción de RUT para Airtable
Verificar que el nuevo sistema de RUT funciona correctamente
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from app.services.sync_service import get_sync_service

def test_rut_extraction():
    print("🧪 Testing Extracción de RUT para ACA 3.0")
    print("=" * 50)
    
    sync_service = get_sync_service()
    
    # Casos de prueba
    test_cases = [
        "Empresa Ejemplo 2 Ltda. (98765432-1)",
        "THE WINGDEMO (12345678-9)", 
        "Empresa Ejemplo 3 EIRL (11223344-5)",
        "98765432-1",  # Solo RUT
        "12.345.678-9",  # RUT con puntos
        "Empresa Sin RUT",  # Sin RUT
        "Empresa Ejemplo 2 Ltda."  # Solo nombre
    ]
    
    print("\n🔍 Probando extracción de RUT:")
    for caso in test_cases:
        rut = sync_service._extraer_rut_de_nombre(caso)
        print(f"  Input: '{caso}'")
        print(f"  RUT extraído: {rut if rut else '❌ No encontrado'}")
        print()
    
    print("\n🏢 Probando búsqueda de empresas:")
    for caso in test_cases:
        empresa = sync_service._get_empresa_by_name(caso)
        if empresa:
            print(f"✅ '{caso}' → {empresa['nombre']} (RUT: {empresa['rut']})")
        else:
            print(f"❌ '{caso}' → No encontrada")
    
    print("\n🎯 Formato recomendado para Airtable:")
    print("  - Empresa Ejemplo 2 Ltda. (98765432-1)")
    print("  - Empresa Ejemplo 3 EIRL (11223344-5)")  
    print("  - THE WINGDEMO (12345678-9)")
    
    return True

if __name__ == "__main__":
    try:
        test_rut_extraction()
    except Exception as e:
        print(f"❌ Error en testing: {e}")
        sys.exit(1)