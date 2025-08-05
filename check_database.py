#!/usr/bin/env python3
"""
✅ Check Database - ACA 3.0
Script simple para verificar rápidamente la consistencia de la base de datos
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv
from supabase import create_client, Client
import json

# Cargar variables de entorno
load_dotenv()

def print_header():
    """Imprimir encabezado del script"""
    print("\n" + "="*70)
    print("✅ VERIFICACIÓN RÁPIDA DE BASE DE DATOS - ACA 3.0")
    print("="*70)

def check_connection() -> Client:
    """Verificar conexión a Supabase"""
    print("\n🔌 Verificando conexión a Supabase...")
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Variables SUPABASE_URL y SUPABASE_KEY son requeridas")
        print("💡 Asegúrate de tener configurado el archivo .env")
        sys.exit(1)
    
    try:
        client = create_client(supabase_url, supabase_key)
        print(f"✅ Conectado a: {supabase_url.replace('https://', '').split('.')[0]}")
        return client
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        sys.exit(1)

def check_tables(client: Client) -> Dict[str, Any]:
    """Verificar todas las tablas del proyecto"""
    print("\n📋 Verificando tablas...")
    
    # Tablas esperadas en el proyecto ACA 3.0
    expected_tables = {
        'empresas': 'Información de empresas',
        'usuarios': 'Usuarios del sistema',
        'conversaciones': 'Historial de conversaciones',
        'reportes': 'Reportes disponibles',
        'pendientes': 'Tareas pendientes',
        'cuentas_cobrar': 'Cuentas por cobrar',
        'cuentas_pagar': 'Cuentas por pagar',
        'citas': 'Sistema de agendamiento',
        'security_logs': 'Logs de seguridad',
        'archivos_reportes': 'Archivos de reportes',
        'meses_reportes': 'Configuración de meses'
    }
    
    tables_status = {}
    
    for table_name, description in expected_tables.items():
        try:
            # Intentar consultar la tabla
            response = client.table(table_name).select("*", count="exact").limit(1).execute()
            
            tables_status[table_name] = {
                'exists': True,
                'count': response.count,
                'description': description,
                'accessible': True
            }
            
            status_icon = "✅" if response.count > 0 else "⚪"
            print(f"   {status_icon} {table_name:<18} | {response.count:>4} registros | {description}")
            
        except Exception as e:
            tables_status[table_name] = {
                'exists': False,
                'error': str(e),
                'description': description,
                'accessible': False
            }
            print(f"   ❌ {table_name:<18} | Error: {str(e)[:40]}...")
    
    return tables_status

def check_table_structure(client: Client, table_name: str) -> Dict[str, Any]:
    """Verificar estructura de una tabla específica"""
    try:
        # Obtener muestra de datos
        response = client.table(table_name).select("*").limit(3).execute()
        
        if not response.data:
            return {'columns': [], 'sample_count': 0}
        
        # Extraer columnas del primer registro
        sample_row = response.data[0]
        columns = []
        
        for col_name, col_value in sample_row.items():
            columns.append({
                'name': col_name,
                'type': type(col_value).__name__ if col_value is not None else 'NoneType',
                'sample': str(col_value)[:30] if col_value else 'NULL'
            })
        
        return {
            'columns': columns,
            'sample_count': len(response.data)
        }
        
    except Exception as e:
        return {'error': str(e)}

def analyze_consistency(tables_status: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analizar consistencia de las tablas"""
    print("\n🔍 Analizando consistencia...")
    
    issues = []
    existing_tables = [name for name, info in tables_status.items() if info.get('exists', False)]
    
    # Verificar tablas críticas
    critical_tables = ['empresas', 'usuarios']
    for table in critical_tables:
        if table not in existing_tables:
            issues.append({
                'type': 'critical',
                'message': f"Tabla crítica '{table}' no encontrada",
                'suggestion': f"Crear tabla {table} usando el script de setup"
            })
        elif tables_status[table]['count'] == 0:
            issues.append({
                'type': 'warning',
                'message': f"Tabla '{table}' está vacía",
                'suggestion': f"Poblar tabla {table} con datos iniciales"
            })
    
    # Verificar datos mínimos
    if 'empresas' in existing_tables and tables_status['empresas']['count'] == 0:
        issues.append({
            'type': 'warning',
            'message': "No hay empresas registradas",
            'suggestion': "Usar el bot admin para crear la primera empresa"
        })
    
    if 'usuarios' in existing_tables and tables_status['usuarios']['count'] == 0:
        issues.append({
            'type': 'warning',
            'message': "No hay usuarios registrados",
            'suggestion': "Los usuarios se crean automáticamente al crear empresas"
        })
    
    # Verificar proporciones lógicas
    if all(t in existing_tables for t in ['empresas', 'usuarios']):
        empresas_count = tables_status['empresas']['count']
        usuarios_count = tables_status['usuarios']['count']
        
        if empresas_count > 0 and usuarios_count == 0:
            issues.append({
                'type': 'error',
                'message': "Hay empresas pero no usuarios",
                'suggestion': "Verificar la creación de usuarios al crear empresas"
            })
        
        if usuarios_count > empresas_count * 10:
            issues.append({
                'type': 'info',
                'message': f"Muchos usuarios ({usuarios_count}) para pocas empresas ({empresas_count})",
                'suggestion': "Revisar si es la proporción esperada"
            })
    
    return issues

def generate_summary(tables_status: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generar resumen del análisis"""
    existing_tables = [name for name, info in tables_status.items() if info.get('exists', False)]
    total_records = sum(info.get('count', 0) for info in tables_status.values() if info.get('exists', False))
    
    critical_issues = [i for i in issues if i['type'] == 'critical']
    error_issues = [i for i in issues if i['type'] == 'error']
    warning_issues = [i for i in issues if i['type'] == 'warning']
    
    return {
        'timestamp': datetime.now().isoformat(),
        'tables_found': len(existing_tables),
        'tables_expected': len(tables_status),
        'total_records': total_records,
        'issues': {
            'critical': len(critical_issues),
            'errors': len(error_issues),
            'warnings': len(warning_issues),
            'total': len(issues)
        },
        'health_score': calculate_health_score(tables_status, issues)
    }

def calculate_health_score(tables_status: Dict[str, Any], issues: List[Dict[str, Any]]) -> int:
    """Calcular puntuación de salud de la base de datos (0-100)"""
    score = 100
    
    # Penalizar por tablas faltantes
    existing_tables = len([info for info in tables_status.values() if info.get('exists', False)])
    expected_tables = len(tables_status)
    table_score = (existing_tables / expected_tables) * 40
    
    # Penalizar por problemas
    for issue in issues:
        if issue['type'] == 'critical':
            score -= 25
        elif issue['type'] == 'error':
            score -= 15
        elif issue['type'] == 'warning':
            score -= 5
    
    # Bonificar por tener datos
    tables_with_data = len([info for info in tables_status.values() 
                           if info.get('exists', False) and info.get('count', 0) > 0])
    data_score = (tables_with_data / expected_tables) * 20
    
    final_score = int(table_score + data_score + max(0, score - 60))
    return max(0, min(100, final_score))

def print_issues(issues: List[Dict[str, Any]]):
    """Imprimir problemas encontrados"""
    if not issues:
        print("\n✅ No se encontraron problemas de consistencia")
        return
    
    print(f"\n⚠️  PROBLEMAS ENCONTRADOS ({len(issues)}):")
    
    for issue in issues:
        icon = {
            'critical': '🔴',
            'error': '🟠', 
            'warning': '🟡',
            'info': '🔵'
        }.get(issue['type'], '⚪')
        
        print(f"\n   {icon} {issue['type'].upper()}: {issue['message']}")
        print(f"      💡 {issue['suggestion']}")

def print_summary(summary: Dict[str, Any]):
    """Imprimir resumen final"""
    print(f"\n📊 RESUMEN DEL ANÁLISIS:")
    print(f"   🗂️  Tablas encontradas: {summary['tables_found']}/{summary['tables_expected']}")
    print(f"   📄 Total de registros: {summary['total_records']:,}")
    print(f"   ⚠️  Problemas totales: {summary['issues']['total']}")
    
    # Mostrar puntuación de salud
    health_score = summary['health_score']
    if health_score >= 90:
        health_icon = "💚"
        health_status = "EXCELENTE"
    elif health_score >= 75:
        health_icon = "💛"
        health_status = "BUENO"
    elif health_score >= 50:
        health_icon = "🧡"
        health_status = "REGULAR"
    else:
        health_icon = "❤️"
        health_status = "CRÍTICO"
    
    print(f"\n{health_icon} PUNTUACIÓN DE SALUD: {health_score}/100 ({health_status})")

def save_detailed_report(tables_status: Dict[str, Any], issues: List[Dict[str, Any]], 
                        summary: Dict[str, Any]) -> str:
    """Guardar reporte detallado en JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"database_check_report_{timestamp}.json"
    
    report = {
        'generated_at': summary['timestamp'],
        'summary': summary,
        'tables': tables_status,
        'issues': issues
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    
    return filename

def main():
    """Función principal"""
    print_header()
    
    try:
        # Verificar conexión
        client = check_connection()
        
        # Verificar tablas
        tables_status = check_tables(client)
        
        # Analizar consistencia
        issues = analyze_consistency(tables_status)
        
        # Generar resumen
        summary = generate_summary(tables_status, issues)
        
        # Mostrar problemas
        print_issues(issues)
        
        # Mostrar resumen
        print_summary(summary)
        
        # Guardar reporte detallado
        report_file = save_detailed_report(tables_status, issues, summary)
        print(f"\n💾 Reporte detallado guardado en: {report_file}")
        
        # Recomendaciones finales
        print(f"\n💡 PRÓXIMOS PASOS:")
        if summary['health_score'] >= 90:
            print("   ✅ La base de datos está en excelente estado")
            print("   🔄 Considera ejecutar este check periódicamente")
        elif summary['health_score'] >= 75:
            print("   👍 La base de datos está en buen estado")
            print("   🔧 Resolver los problemas menores cuando sea posible")
        else:
            print("   🚨 La base de datos necesita atención")
            print("   🔧 Resolver problemas críticos inmediatamente")
            print("   📖 Revisar documentación en docs/setup_database.md")
        
        print("\n" + "="*70)
        
        return summary['health_score']
        
    except KeyboardInterrupt:
        print("\n\n👋 Verificación cancelada por el usuario")
        return 0
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {e}")
        print("\n💡 Posibles soluciones:")
        print("   • Verificar variables de entorno en .env")
        print("   • Comprobar conexión a internet")
        print("   • Validar credenciales de Supabase")
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(0 if exit_code >= 50 else 1)