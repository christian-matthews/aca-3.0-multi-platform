#!/usr/bin/env python3
"""
🔍 Database Inspector para ACA 3.0
Script para revisar todas las tablas en Supabase y analizar la consistencia de la estructura
"""

import os
import json
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

class DatabaseInspector:
    """Inspector de base de datos para analizar estructura y consistencia"""
    
    def __init__(self):
        """Inicializar el inspector con conexión a Supabase"""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Variables SUPABASE_URL y SUPABASE_KEY son requeridas")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        self.schema_info = {}
        self.consistency_issues = []
        
    def get_all_tables(self) -> List[Dict[str, Any]]:
        """Obtener lista de todas las tablas en el esquema público"""
        try:
            # Query para obtener información de tablas
            query = """
            SELECT 
                table_name,
                table_schema,
                table_type
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
            """
            
            response = self.client.rpc('get_tables_info', {}).execute()
            
            # Si el RPC no existe, usar query directo (necesita service key)
            if not response.data:
                # Intentar obtener tablas manualmente
                tables = []
                known_tables = [
                    'empresas', 'usuarios', 'conversaciones', 'reportes', 
                    'pendientes', 'cuentas_cobrar', 'cuentas_pagar', 
                    'citas', 'security_logs', 'archivos_reportes', 'meses_reportes'
                ]
                
                for table in known_tables:
                    try:
                        # Verificar si la tabla existe intentando una consulta
                        self.client.table(table).select("*").limit(1).execute()
                        tables.append({
                            'table_name': table,
                            'table_schema': 'public',
                            'table_type': 'BASE TABLE'
                        })
                    except Exception:
                        logger.warning(f"Tabla '{table}' no encontrada o sin acceso")
                
                return tables
            
            return response.data
            
        except Exception as e:
            logger.error(f"Error obteniendo tablas: {e}")
            return []
    
    def get_table_columns(self, table_name: str) -> List[Dict[str, Any]]:
        """Obtener información de columnas de una tabla específica"""
        try:
            # Intentar obtener información de columnas usando el client
            response = self.client.table(table_name).select("*").limit(1).execute()
            
            if response.data:
                # Si hay datos, extraer las columnas de la primera fila
                columns_info = []
                if response.data:
                    sample_row = response.data[0]
                    for column_name in sample_row.keys():
                        columns_info.append({
                            'column_name': column_name,
                            'data_type': type(sample_row[column_name]).__name__ if sample_row[column_name] is not None else 'unknown',
                            'is_nullable': True,  # Asumimos que es nullable por defecto
                            'column_default': None,
                            'table_name': table_name
                        })
                
                return columns_info
            else:
                # Tabla vacía, intentar obtener estructura de otra manera
                return []
                
        except Exception as e:
            logger.error(f"Error obteniendo columnas de {table_name}: {e}")
            return []
    
    def get_table_constraints(self, table_name: str) -> List[Dict[str, Any]]:
        """Obtener información de restricciones de una tabla"""
        try:
            # Para obtener restricciones, necesitaríamos acceso directo a information_schema
            # Por ahora, retornamos una lista vacía y recopilamos info básica
            return []
        except Exception as e:
            logger.error(f"Error obteniendo restricciones de {table_name}: {e}")
            return []
    
    def get_table_size_info(self, table_name: str) -> Dict[str, Any]:
        """Obtener información de tamaño y registros de una tabla"""
        try:
            # Contar registros
            response = self.client.table(table_name).select("*", count="exact").limit(0).execute()
            
            return {
                'row_count': response.count,
                'estimated_size': 'N/A'  # Necesitaría acceso a pg_stat para esto
            }
        except Exception as e:
            logger.error(f"Error obteniendo tamaño de {table_name}: {e}")
            return {'row_count': 0, 'estimated_size': 'Error'}
    
    def analyze_table_structure(self, table_name: str) -> Dict[str, Any]:
        """Analizar la estructura completa de una tabla"""
        logger.info(f"📋 Analizando tabla: {table_name}")
        
        # Obtener información básica
        columns = self.get_table_columns(table_name)
        constraints = self.get_table_constraints(table_name)
        size_info = self.get_table_size_info(table_name)
        
        # Analizar patrones comunes
        common_columns = ['id', 'created_at', 'updated_at', 'activo']
        missing_common = [col for col in common_columns if not any(c['column_name'] == col for c in columns)]
        
        return {
            'table_name': table_name,
            'columns': columns,
            'constraints': constraints,
            'size_info': size_info,
            'column_count': len(columns),
            'missing_common_columns': missing_common,
            'has_primary_key': any(c['column_name'] == 'id' for c in columns),
            'has_timestamps': any(c['column_name'] in ['created_at', 'updated_at'] for c in columns)
        }
    
    def check_naming_consistency(self, tables_info: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Verificar consistencia en nombres de tablas y columnas"""
        issues = []
        
        # Verificar convenciones de nombres de tablas
        for table_info in tables_info:
            table_name = table_info['table_name']
            
            # Verificar si usa plural (convención recomendada)
            if not table_name.endswith('s') and table_name not in ['security_logs']:
                issues.append({
                    'type': 'naming_convention',
                    'severity': 'low',
                    'table': table_name,
                    'issue': 'Tabla no usa nombre plural',
                    'suggestion': f'Considerar renombrar a {table_name}s'
                })
            
            # Verificar convenciones de columnas
            for column in table_info['columns']:
                col_name = column['column_name']
                
                # Verificar snake_case
                if col_name != col_name.lower() or ' ' in col_name:
                    issues.append({
                        'type': 'naming_convention',
                        'severity': 'medium',
                        'table': table_name,
                        'column': col_name,
                        'issue': 'Columna no usa snake_case',
                        'suggestion': 'Usar snake_case para nombres de columnas'
                    })
        
        return issues
    
    def check_structural_consistency(self, tables_info: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Verificar consistencia estructural entre tablas"""
        issues = []
        
        # Verificar que todas las tablas tengan ID
        for table_info in tables_info:
            if not table_info['has_primary_key']:
                issues.append({
                    'type': 'structure',
                    'severity': 'high',
                    'table': table_info['table_name'],
                    'issue': 'Tabla sin clave primaria (id)',
                    'suggestion': 'Agregar columna id como clave primaria'
                })
            
            # Verificar timestamps
            if not table_info['has_timestamps']:
                issues.append({
                    'type': 'structure',
                    'severity': 'medium',
                    'table': table_info['table_name'],
                    'issue': 'Tabla sin timestamps (created_at, updated_at)',
                    'suggestion': 'Agregar columnas de timestamp para auditoría'
                })
            
            # Verificar columnas empresa_id para aislamiento de datos
            if table_info['table_name'] not in ['empresas', 'security_logs']:
                has_empresa_id = any(c['column_name'] == 'empresa_id' for c in table_info['columns'])
                if not has_empresa_id:
                    issues.append({
                        'type': 'data_isolation',
                        'severity': 'high',
                        'table': table_info['table_name'],
                        'issue': 'Tabla sin empresa_id para aislamiento de datos',
                        'suggestion': 'Agregar empresa_id para seguridad por empresa'
                    })
        
        return issues
    
    def generate_report(self) -> Dict[str, Any]:
        """Generar reporte completo de la base de datos"""
        logger.info("🔍 Iniciando inspección completa de la base de datos...")
        
        # Obtener todas las tablas
        tables = self.get_all_tables()
        logger.info(f"📊 Encontradas {len(tables)} tablas")
        
        # Analizar cada tabla
        tables_analysis = []
        for table in tables:
            table_analysis = self.analyze_table_structure(table['table_name'])
            tables_analysis.append(table_analysis)
        
        # Verificar consistencia
        naming_issues = self.check_naming_consistency(tables_analysis)
        structural_issues = self.check_structural_consistency(tables_analysis)
        
        all_issues = naming_issues + structural_issues
        
        # Estadísticas generales
        total_columns = sum(t['column_count'] for t in tables_analysis)
        total_rows = sum(t['size_info']['row_count'] for t in tables_analysis)
        
        # Generar reporte
        report = {
            'generated_at': datetime.now().isoformat(),
            'database_url': self.supabase_url.replace('https://', '').split('.')[0],
            'summary': {
                'total_tables': len(tables),
                'total_columns': total_columns,
                'total_rows': total_rows,
                'total_issues': len(all_issues),
                'critical_issues': len([i for i in all_issues if i['severity'] == 'high']),
                'medium_issues': len([i for i in all_issues if i['severity'] == 'medium']),
                'low_issues': len([i for i in all_issues if i['severity'] == 'low'])
            },
            'tables': tables_analysis,
            'issues': all_issues,
            'recommendations': self.generate_recommendations(tables_analysis, all_issues)
        }
        
        return report
    
    def generate_recommendations(self, tables_analysis: List[Dict[str, Any]], issues: List[Dict[str, Any]]) -> List[str]:
        """Generar recomendaciones basadas en el análisis"""
        recommendations = []
        
        # Recomendaciones basadas en problemas encontrados
        critical_issues = [i for i in issues if i['severity'] == 'high']
        if critical_issues:
            recommendations.append("🔴 CRÍTICO: Resolver problemas de alta prioridad inmediatamente")
        
        # Verificar si hay tablas sin datos
        empty_tables = [t for t in tables_analysis if t['size_info']['row_count'] == 0]
        if empty_tables:
            recommendations.append(f"📋 Considerar poblar tablas vacías: {', '.join([t['table_name'] for t in empty_tables])}")
        
        # Verificar consistencia de estructura
        if any('empresa_id' in i.get('issue', '') for i in issues):
            recommendations.append("🔒 Implementar empresa_id en todas las tablas para aislamiento de datos")
        
        if any('timestamp' in i.get('issue', '') for i in issues):
            recommendations.append("⏰ Agregar timestamps (created_at, updated_at) para auditoría")
        
        # Recomendaciones generales
        recommendations.extend([
            "✅ Implementar Row Level Security (RLS) en todas las tablas",
            "📊 Crear índices en columnas empresa_id para optimizar consultas",
            "🔄 Configurar triggers para actualizar updated_at automáticamente",
            "🛡️ Revisar permisos y políticas de acceso regularmente"
        ])
        
        return recommendations
    
    def save_report(self, report: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Guardar reporte en archivo JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"database_inspection_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        return filename
    
    def print_summary(self, report: Dict[str, Any]):
        """Imprimir resumen del reporte en consola"""
        print("\n" + "="*80)
        print("🔍 REPORTE DE INSPECCIÓN DE BASE DE DATOS - ACA 3.0")
        print("="*80)
        
        summary = report['summary']
        print(f"\n📊 RESUMEN GENERAL:")
        print(f"   • Tablas encontradas: {summary['total_tables']}")
        print(f"   • Columnas totales: {summary['total_columns']}")
        print(f"   • Registros totales: {summary['total_rows']:,}")
        print(f"   • Problemas encontrados: {summary['total_issues']}")
        
        if summary['total_issues'] > 0:
            print(f"\n⚠️  PROBLEMAS POR SEVERIDAD:")
            print(f"   🔴 Críticos: {summary['critical_issues']}")
            print(f"   🟡 Medios: {summary['medium_issues']}")
            print(f"   🟢 Bajos: {summary['low_issues']}")
        
        print(f"\n📋 TABLAS ANALIZADAS:")
        for table in report['tables']:
            status = "✅" if table['size_info']['row_count'] > 0 else "⚪"
            print(f"   {status} {table['table_name']} - {table['column_count']} columnas, {table['size_info']['row_count']} registros")
        
        if report['issues']:
            print(f"\n🔍 PRINCIPALES PROBLEMAS:")
            for issue in report['issues'][:5]:  # Mostrar solo los primeros 5
                severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(issue['severity'], "⚪")
                print(f"   {severity_icon} {issue['table']}: {issue['issue']}")
            
            if len(report['issues']) > 5:
                print(f"   ... y {len(report['issues']) - 5} problemas más")
        
        print(f"\n💡 RECOMENDACIONES PRINCIPALES:")
        for i, recommendation in enumerate(report['recommendations'][:5], 1):
            print(f"   {i}. {recommendation}")
        
        print("\n" + "="*80)


def main():
    """Función principal para ejecutar la inspección"""
    try:
        print("🚀 Iniciando Database Inspector para ACA 3.0...")
        
        # Crear inspector
        inspector = DatabaseInspector()
        
        # Generar reporte
        report = inspector.generate_report()
        
        # Mostrar resumen en consola
        inspector.print_summary(report)
        
        # Guardar reporte completo
        filename = inspector.save_report(report)
        print(f"\n💾 Reporte completo guardado en: {filename}")
        
        # Conclusión
        if report['summary']['critical_issues'] > 0:
            print("\n🔴 ATENCIÓN: Se encontraron problemas críticos que requieren atención inmediata.")
        elif report['summary']['total_issues'] > 0:
            print("\n🟡 Se encontraron algunos problemas menores. Revisar reporte para detalles.")
        else:
            print("\n✅ ¡Excelente! La base de datos está bien estructurada y consistente.")
        
        return report
        
    except Exception as e:
        logger.error(f"Error durante la inspección: {e}")
        print(f"\n❌ Error: {e}")
        print("\n💡 Asegúrate de que:")
        print("   • Las variables SUPABASE_URL y SUPABASE_KEY estén configuradas")
        print("   • Tengas permisos de acceso a la base de datos")
        print("   • La conexión a internet esté funcionando")
        return None


if __name__ == "__main__":
    main()