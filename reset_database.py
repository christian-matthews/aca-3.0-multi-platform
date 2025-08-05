#!/usr/bin/env python3
"""
Script para borrar todos los datos de la base de datos ACA 3.0
⚠️ ADVERTENCIA: ESTO BORRARÁ TODOS LOS DATOS
"""

import sys
import os
from app.database.supabase import supabase

def confirm_reset():
    """Confirmar que el usuario quiere borrar todo"""
    print("⚠️  ADVERTENCIA: Esto borrará TODOS los datos de la base de datos")
    print("=" * 60)
    
    response = input("¿Estás seguro de que quieres continuar? (escribe 'SI' para confirmar): ")
    
    if response.upper() != 'SI':
        print("❌ Operación cancelada")
        return False
    
    # Doble confirmación
    response2 = input("¿Realmente estás seguro? Esto no se puede deshacer (escribe 'BORRAR'): ")
    
    if response2.upper() != 'BORRAR':
        print("❌ Operación cancelada")
        return False
    
    return True

def reset_database():
    """Borrar todos los datos de la base de datos"""
    print("🗑️ Iniciando borrado de base de datos...")
    
    try:
        # Lista de tablas en orden (respetando foreign keys)
        tables = [
            'security_logs',
            'citas', 
            'cuentas_pagar',
            'cuentas_cobrar',
            'pendientes',
            'reportes',
            'conversaciones',
            'usuarios',
            'empresas'
        ]
        
        deleted_count = 0
        
        for table in tables:
            try:
                # Obtener conteo antes de borrar
                count_result = supabase.table(table).select('id', count='exact').execute()
                count_before = len(count_result.data) if count_result.data else 0
                
                # Borrar todos los registros
                delete_result = supabase.table(table).delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
                
                print(f"✅ Tabla '{table}': {count_before} registros borrados")
                deleted_count += count_before
                
            except Exception as e:
                print(f"⚠️ Error borrando tabla '{table}': {e}")
        
        print(f"\n📊 Total de registros borrados: {deleted_count}")
        print("✅ Base de datos borrada exitosamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error borrando base de datos: {e}")
        return False

def verify_empty_database():
    """Verificar que la base de datos esté vacía"""
    print("\n🔍 Verificando que la base de datos esté vacía...")
    
    tables = [
        'empresas',
        'usuarios', 
        'conversaciones',
        'reportes',
        'pendientes',
        'cuentas_cobrar',
        'cuentas_pagar',
        'citas',
        'security_logs'
    ]
    
    total_records = 0
    
    for table in tables:
        try:
            result = supabase.table(table).select('id').limit(1).execute()
            count = len(result.data)
            total_records += count
            
            if count == 0:
                print(f"✅ Tabla '{table}': Vacía")
            else:
                print(f"⚠️ Tabla '{table}': {count} registros restantes")
                
        except Exception as e:
            print(f"❌ Error verificando tabla '{table}': {e}")
    
    if total_records == 0:
        print("\n🎉 ¡Base de datos completamente vacía!")
        return True
    else:
        print(f"\n⚠️ Aún quedan {total_records} registros en la base de datos")
        return False

def main():
    """Función principal"""
    print("🗑️ Script de Reset de Base de Datos ACA 3.0")
    print("=" * 50)
    
    # Confirmar operación
    if not confirm_reset():
        sys.exit(1)
    
    # Borrar base de datos
    if not reset_database():
        print("❌ Error durante el borrado")
        sys.exit(1)
    
    # Verificar que esté vacía
    if not verify_empty_database():
        print("⚠️ Algunos datos no se pudieron borrar")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Reset completado exitosamente")
    print("📝 Para recrear la base de datos, ejecuta:")
    print("   - El script SQL de docs/setup_database.md")
    print("   - O ejecuta: python test_database.py")

if __name__ == "__main__":
    main() 