#!/usr/bin/env python3
"""
✅ Verify Fixes - Verificar que las correcciones críticas se aplicaron correctamente
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

def verify_critical_fixes():
    """Verificar que todas las correcciones críticas se aplicaron"""
    print("\n" + "="*70)
    print("✅ VERIFICACIÓN DE CORRECCIONES CRÍTICAS - ACA 3.0")
    print("="*70)
    
    try:
        client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        
        # Verificar cada tabla crítica
        critical_checks = {
            'meses_reportes': {
                'should_exist': True,
                'should_have_data': True,
                'expected_count': 12,
                'required_columns': ['id', 'mes', 'nombre', 'activo', 'created_at']
            },
            'citas': {
                'should_exist': True,
                'should_have_data': False,
                'required_columns': ['id', 'empresa_id', 'created_at', 'activo']
            },
            'security_logs': {
                'should_exist': True,
                'should_have_data': False,
                'required_columns': ['id', 'created_at']
            },
            'archivos_reportes': {
                'should_exist': True,
                'should_have_data': False,
                'required_columns': ['id', 'empresa_id', 'created_at', 'activo']
            }
        }
        
        all_good = True
        results = {}
        
        for table_name, checks in critical_checks.items():
            print(f"\n🔍 Verificando: {table_name}")
            table_result = {'status': 'ok', 'issues': []}
            
            try:
                # Verificar existencia y obtener datos
                response = client.table(table_name).select("*").limit(3).execute()
                
                # Verificar estructura
                if response.data:
                    columns = list(response.data[0].keys())
                    table_result['columns'] = columns
                    
                    # Verificar columnas requeridas
                    missing_columns = [col for col in checks['required_columns'] if col not in columns]
                    if missing_columns:
                        table_result['status'] = 'error'
                        table_result['issues'].append(f"Columnas faltantes: {', '.join(missing_columns)}")
                        all_good = False
                        print(f"   ❌ Columnas faltantes: {', '.join(missing_columns)}")
                    else:
                        print(f"   ✅ Estructura correcta: {len(columns)} columnas")
                    
                    # Verificar datos si es necesario
                    if checks.get('should_have_data', False):
                        count_response = client.table(table_name).select("*", count="exact").limit(0).execute()
                        actual_count = count_response.count
                        expected_count = checks.get('expected_count', 1)
                        
                        if actual_count >= expected_count:
                            print(f"   ✅ Datos correctos: {actual_count} registros")
                        else:
                            table_result['status'] = 'warning'
                            table_result['issues'].append(f"Pocos registros: {actual_count}/{expected_count}")
                            print(f"   ⚠️  Pocos registros: {actual_count}/{expected_count}")
                    else:
                        print(f"   ⚪ Tabla vacía (normal)")
                
                else:
                    # Tabla existe pero está vacía - verificar si debe tener datos
                    if checks.get('should_have_data', False):
                        table_result['status'] = 'error'
                        table_result['issues'].append("Tabla vacía cuando debería tener datos")
                        all_good = False
                        print(f"   ❌ Tabla vacía cuando debería tener datos")
                    else:
                        print(f"   ✅ Tabla existe (vacía)")
                
            except Exception as e:
                if "does not exist" in str(e):
                    table_result['status'] = 'error'
                    table_result['issues'].append("Tabla no existe")
                    all_good = False
                    print(f"   ❌ Tabla no existe")
                else:
                    table_result['status'] = 'error'
                    table_result['issues'].append(f"Error: {str(e)[:50]}")
                    all_good = False
                    print(f"   ❌ Error: {str(e)[:50]}")
            
            results[table_name] = table_result
        
        # Resumen final
        print(f"\n📊 RESUMEN DE VERIFICACIÓN:")
        
        ok_tables = [name for name, result in results.items() if result['status'] == 'ok']
        warning_tables = [name for name, result in results.items() if result['status'] == 'warning']
        error_tables = [name for name, result in results.items() if result['status'] == 'error']
        
        print(f"   ✅ Correctas: {len(ok_tables)}")
        print(f"   ⚠️  Con advertencias: {len(warning_tables)}")
        print(f"   ❌ Con errores: {len(error_tables)}")
        
        if error_tables:
            print(f"\n❌ TABLAS CON ERRORES:")
            for table in error_tables:
                issues = results[table]['issues']
                print(f"   • {table}: {', '.join(issues)}")
        
        if warning_tables:
            print(f"\n⚠️  TABLAS CON ADVERTENCIAS:")
            for table in warning_tables:
                issues = results[table]['issues']
                print(f"   • {table}: {', '.join(issues)}")
        
        # Resultado final
        if all_good:
            print(f"\n🎉 ¡TODAS LAS CORRECCIONES SE APLICARON CORRECTAMENTE!")
            print(f"   🚀 Tu base de datos ahora está en excelente estado")
            print(f"   📊 Ejecuta: python check_database.py para ver la puntuación final")
        elif not error_tables:
            print(f"\n👍 CORRECCIONES APLICADAS CON ADVERTENCIAS MENORES")
            print(f"   🔧 Revisa las advertencias pero el sistema debería funcionar")
        else:
            print(f"\n🔧 ALGUNAS CORRECCIONES NECESITAN ATENCIÓN")
            print(f"   📋 Revisa los errores y re-ejecuta las correcciones necesarias")
        
        print("="*70)
        return len(error_tables) == 0
        
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {e}")
        print("\n💡 Posibles soluciones:")
        print("   • Verificar que las correcciones se ejecutaron en Supabase")
        print("   • Comprobar variables de entorno")
        print("   • Intentar ejecutar: python check_database.py")
        return False

if __name__ == "__main__":
    import sys
    success = verify_critical_fixes()
    sys.exit(0 if success else 1)