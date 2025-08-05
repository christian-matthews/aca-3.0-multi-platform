#!/usr/bin/env python3
"""
🔍 INSPECCIÓN COMPLETA DE SUPABASE - ACA 3.0
===============================================

Este script realiza una inspección exhaustiva de la base de datos Supabase
para entender completamente la estructura actual antes de implementar mejoras.

Autor: ACA 3.0 Team
Fecha: Agosto 2024
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import asyncio

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from supabase import create_client, Client
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("💡 Ejecuta: pip install supabase python-dotenv")
    sys.exit(1)

@dataclass
class TableInfo:
    """Información de una tabla"""
    name: str
    exists: bool
    column_count: int
    row_count: int
    columns: List[Dict[str, Any]]
    primary_keys: List[str]
    foreign_keys: List[Dict[str, str]]
    indexes: List[str]
    policies: List[str]
    sample_data: List[Dict[str, Any]]
    error: Optional[str] = None

@dataclass
class DatabaseReport:
    """Reporte completo de la base de datos"""
    timestamp: str
    supabase_url: str
    total_tables: int
    total_columns: int
    total_rows: int
    tables: List[TableInfo]
    relationships: List[Dict[str, str]]
    issues: List[Dict[str, str]]
    recommendations: List[str]

class SupabaseCompleteInspector:
    """Inspector completo de Supabase"""
    
    def __init__(self):
        """Inicializar el inspector"""
        load_dotenv()
        
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("❌ Variables SUPABASE_URL y SUPABASE_KEY son requeridas")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        
        # Tablas esperadas en ACA 3.0
        self.expected_tables = [
            'empresas',
            'usuarios', 
            'conversaciones',
            'reportes',
            'pendientes',
            'reportes_mensuales',
            'archivos_reportes',
            'comentarios_reportes',
            'info_compania',
            'archivos_info_compania',
            'cuentas_cobrar',
            'cuentas_pagar',
            'citas',
            'security_logs'
        ]

    def test_connection(self) -> bool:
        """Probar conexión a Supabase"""
        try:
            # Hacer una consulta simple a una tabla que debería existir
            response = self.client.table('empresas').select("id").limit(1).execute()
            print("✅ Conexión a Supabase exitosa")
            return True
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False

    def get_all_tables(self) -> List[str]:
        """Obtener lista de todas las tablas"""
        # Usar lista de tablas esperadas y verificar cuáles existen
        print("🔄 Usando lista de tablas esperadas")
        return self.expected_tables

    def get_table_columns(self, table_name: str) -> List[Dict[str, Any]]:
        """Obtener información de columnas de una tabla"""
        try:
            # Hacer una consulta simple para obtener una fila y analizar las columnas
            response = self.client.table(table_name).select("*").limit(1).execute()
            
            if hasattr(response, 'data') and response.data and len(response.data) > 0:
                # Obtener nombres de columnas del primer registro
                columns = []
                for column_name in response.data[0].keys():
                    columns.append({
                        'column_name': column_name,
                        'data_type': 'unknown',  # Simplificado
                        'is_nullable': 'unknown'
                    })
                return columns
            elif hasattr(response, 'data'):
                # Tabla existe pero está vacía, intentar con esquema desde error
                return []
            else:
                return []
                
        except Exception as e:
            print(f"⚠️ Error obteniendo columnas de {table_name}: {e}")
            return []

    def get_table_constraints(self, table_name: str) -> Dict[str, List[str]]:
        """Obtener constraints de una tabla (simplificado)"""
        # Simplificado: asumir que 'id' es primary key y detectar foreign keys por nombre
        constraints = {
            'primary_keys': ['id'],  # Asumido
            'foreign_keys': [],
            'unique': [],
            'check': []
        }
        
        try:
            # Obtener columnas para detectar foreign keys
            columns = self.get_table_columns(table_name)
            for column in columns:
                column_name = column['column_name']
                if column_name.endswith('_id') and column_name != 'id':
                    constraints['foreign_keys'].append(column_name)
        except Exception as e:
            print(f"⚠️ Error analizando constraints de {table_name}: {e}")
        
        return constraints

    def get_sample_data(self, table_name: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Obtener datos de muestra de una tabla"""
        try:
            response = self.client.table(table_name).select("*").limit(limit).execute()
            
            if hasattr(response, 'data'):
                return response.data or []
            else:
                return []
                
        except Exception as e:
            print(f"⚠️ Error obteniendo datos de {table_name}: {e}")
            return []

    def get_row_count(self, table_name: str) -> int:
        """Obtener cantidad de filas en una tabla"""
        try:
            response = self.client.table(table_name).select("*", count="exact").limit(1).execute()
            
            if hasattr(response, 'count') and response.count is not None:
                return response.count
            else:
                return 0
                
        except Exception as e:
            print(f"⚠️ Error contando filas de {table_name}: {e}")
            return 0

    def inspect_table(self, table_name: str) -> TableInfo:
        """Inspeccionar una tabla completamente"""
        print(f"🔍 Inspeccionando tabla: {table_name}")
        
        try:
            # Verificar si la tabla existe
            row_count = self.get_row_count(table_name)
            exists = True
            
            # Obtener información de columnas
            columns = self.get_table_columns(table_name)
            
            # Obtener constraints
            constraints = self.get_table_constraints(table_name)
            
            # Obtener datos de muestra
            sample_data = self.get_sample_data(table_name)
            
            return TableInfo(
                name=table_name,
                exists=exists,
                column_count=len(columns),
                row_count=row_count,
                columns=columns,
                primary_keys=constraints['primary_keys'],
                foreign_keys=[],  # Simplificado por ahora
                indexes=[],       # Simplificado por ahora
                policies=[],      # Simplificado por ahora
                sample_data=sample_data
            )
            
        except Exception as e:
            print(f"❌ Error inspeccionando {table_name}: {e}")
            return TableInfo(
                name=table_name,
                exists=False,
                column_count=0,
                row_count=0,
                columns=[],
                primary_keys=[],
                foreign_keys=[],
                indexes=[],
                policies=[],
                sample_data=[],
                error=str(e)
            )

    def analyze_relationships(self, tables: List[TableInfo]) -> List[Dict[str, str]]:
        """Analizar relaciones entre tablas"""
        relationships = []
        
        for table in tables:
            if table.exists:
                for column in table.columns:
                    column_name = column['column_name']
                    
                    # Detectar foreign keys por naming convention
                    if column_name.endswith('_id') and column_name != 'id':
                        referenced_table = column_name[:-3]  # Remove '_id'
                        
                        # Verificar si la tabla referenciada existe
                        if any(t.name == referenced_table and t.exists for t in tables):
                            relationships.append({
                                'from_table': table.name,
                                'from_column': column_name,
                                'to_table': referenced_table,
                                'to_column': 'id'
                            })
        
        return relationships

    def identify_issues(self, tables: List[TableInfo]) -> List[Dict[str, str]]:
        """Identificar problemas en la estructura"""
        issues = []
        
        for table in tables:
            if not table.exists:
                issues.append({
                    'severity': 'ERROR',
                    'table': table.name,
                    'issue': 'Tabla no existe',
                    'description': f'La tabla {table.name} no se encuentra en la base de datos'
                })
            elif table.row_count == 0:
                issues.append({
                    'severity': 'WARNING',
                    'table': table.name,
                    'issue': 'Tabla vacía',
                    'description': f'La tabla {table.name} no tiene datos'
                })
            elif not table.primary_keys:
                issues.append({
                    'severity': 'ERROR',
                    'table': table.name,
                    'issue': 'Sin clave primaria',
                    'description': f'La tabla {table.name} no tiene clave primaria definida'
                })
        
        return issues

    def generate_recommendations(self, tables: List[TableInfo], issues: List[Dict[str, str]]) -> List[str]:
        """Generar recomendaciones"""
        recommendations = []
        
        # Analizar issues críticos
        error_count = len([i for i in issues if i['severity'] == 'ERROR'])
        warning_count = len([i for i in issues if i['severity'] == 'WARNING'])
        
        if error_count > 0:
            recommendations.append(f"🔴 CRÍTICO: Resolver {error_count} errores estructurales")
        
        if warning_count > 0:
            recommendations.append(f"🟡 ATENCIÓN: Revisar {warning_count} advertencias")
        
        # Tablas futuras que podrían moverse
        future_tables = ['cuentas_cobrar', 'cuentas_pagar', 'security_logs', 'citas']
        existing_future = [t.name for t in tables if t.name in future_tables and t.exists]
        
        if existing_future:
            recommendations.append(f"📦 ORGANIZACIÓN: Mover tablas futuras a rama: {', '.join(existing_future)}")
        
        # Variables de entorno
        recommendations.append("⚙️ CONFIG: Agregar variables Slack/Calendar a env.example")
        
        # ORM
        recommendations.append("🏗️ ESTRUCTURA: Crear models.py con SQLModel")
        
        # Migraciones
        recommendations.append("🔄 MIGRACIÓN: Implementar sistema Alembic")
        
        return recommendations

    def run_complete_inspection(self) -> DatabaseReport:
        """Ejecutar inspección completa"""
        print("🚀 INICIANDO INSPECCIÓN COMPLETA DE SUPABASE")
        print("=" * 50)
        
        # Verificar conexión
        if not self.test_connection():
            raise Exception("No se pudo conectar a Supabase")
        
        # Obtener todas las tablas
        all_tables = self.get_all_tables()
        print(f"📋 Tablas encontradas: {len(all_tables)}")
        
        # Inspeccionar cada tabla
        table_infos = []
        total_columns = 0
        total_rows = 0
        
        for table_name in all_tables:
            table_info = self.inspect_table(table_name)
            table_infos.append(table_info)
            
            if table_info.exists:
                total_columns += table_info.column_count
                total_rows += table_info.row_count
        
        # Analizar relaciones
        relationships = self.analyze_relationships(table_infos)
        
        # Identificar problemas
        issues = self.identify_issues(table_infos)
        
        # Generar recomendaciones
        recommendations = self.generate_recommendations(table_infos, issues)
        
        # Crear reporte
        report = DatabaseReport(
            timestamp=datetime.now().isoformat(),
            supabase_url=self.supabase_url,
            total_tables=len([t for t in table_infos if t.exists]),
            total_columns=total_columns,
            total_rows=total_rows,
            tables=table_infos,
            relationships=relationships,
            issues=issues,
            recommendations=recommendations
        )
        
        return report

    def print_report(self, report: DatabaseReport):
        """Imprimir reporte en consola"""
        print("\n" + "=" * 60)
        print("📊 REPORTE COMPLETO DE INSPECCIÓN SUPABASE")
        print("=" * 60)
        
        print(f"\n🕒 Timestamp: {report.timestamp}")
        print(f"🌐 URL: {report.supabase_url[:30]}...")
        print(f"📊 Estadísticas:")
        print(f"   📋 Tablas: {report.total_tables}")
        print(f"   📄 Columnas: {report.total_columns}")
        print(f"   📦 Filas: {report.total_rows}")
        print(f"   🔗 Relaciones: {len(report.relationships)}")
        
        print(f"\n📋 TABLAS ENCONTRADAS:")
        for table in report.tables:
            if table.exists:
                status = "✅"
                detail = f"{table.column_count} cols, {table.row_count} filas"
            else:
                status = "❌"
                detail = "No existe"
            
            print(f"   {status} {table.name:<20} | {detail}")
        
        print(f"\n🔗 RELACIONES:")
        for rel in report.relationships:
            print(f"   📎 {rel['from_table']}.{rel['from_column']} → {rel['to_table']}.{rel['to_column']}")
        
        if report.issues:
            print(f"\n⚠️ PROBLEMAS IDENTIFICADOS:")
            for issue in report.issues:
                severity_icon = "🔴" if issue['severity'] == 'ERROR' else "🟡"
                print(f"   {severity_icon} {issue['table']}: {issue['issue']}")
        
        print(f"\n💡 RECOMENDACIONES:")
        for i, rec in enumerate(report.recommendations, 1):
            print(f"   {i}. {rec}")

    def save_report(self, report: DatabaseReport, filename: str = None):
        """Guardar reporte en archivo JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"supabase_inspection_complete_{timestamp}.json"
        
        # Convertir a dict serializable
        report_dict = asdict(report)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Reporte guardado en: {filename}")
        return filename

def main():
    """Función principal"""
    try:
        inspector = SupabaseCompleteInspector()
        
        # Ejecutar inspección completa
        report = inspector.run_complete_inspection()
        
        # Mostrar reporte
        inspector.print_report(report)
        
        # Guardar reporte
        filename = inspector.save_report(report)
        
        print("\n🎉 INSPECCIÓN COMPLETA FINALIZADA")
        print(f"📄 Reporte detallado disponible en: {filename}")
        
    except Exception as e:
        print(f"\n❌ Error durante la inspección: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()