#!/usr/bin/env python3
"""
🔧 Fix Critical Issues - ACA 3.0
Script para corregir automáticamente los problemas críticos de la base de datos
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

class CriticalIssueFixer:
    """Clase para corregir problemas críticos de la base de datos"""
    
    def __init__(self):
        """Inicializar el corrector"""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Variables SUPABASE_URL y SUPABASE_KEY son requeridas")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        self.fixes_applied = []
        self.errors = []
    
    def print_header(self):
        """Imprimir encabezado"""
        print("\n" + "="*80)
        print("🔧 CORRECCIÓN DE PROBLEMAS CRÍTICOS - ACA 3.0")
        print("="*80)
    
    def check_table_structure(self, table_name: str) -> Dict[str, Any]:
        """Verificar estructura actual de una tabla"""
        try:
            # Obtener muestra de datos para analizar estructura
            response = self.client.table(table_name).select("*").limit(1).execute()
            
            if response.data:
                columns = list(response.data[0].keys())
                return {
                    'exists': True,
                    'has_data': True,
                    'columns': columns,
                    'has_id': 'id' in columns,
                    'has_empresa_id': 'empresa_id' in columns,
                    'has_created_at': 'created_at' in columns,
                    'has_activo': 'activo' in columns
                }
            else:
                # Tabla existe pero está vacía, intentar consulta para ver estructura
                try:
                    # Intentar insertar y hacer rollback para ver la estructura esperada
                    return {
                        'exists': True,
                        'has_data': False,
                        'columns': [],
                        'needs_structure_check': True
                    }
                except Exception:
                    return {'exists': True, 'has_data': False, 'unknown_structure': True}
        
        except Exception as e:
            if "does not exist" in str(e):
                return {'exists': False, 'error': str(e)}
            else:
                logger.error(f"Error verificando {table_name}: {e}")
                return {'exists': True, 'error': str(e)}
    
    def create_missing_table(self, table_name: str) -> bool:
        """Crear tabla faltante con estructura básica"""
        try:
            print(f"\n📋 Creando tabla faltante: {table_name}")
            
            # Definir estructuras para tablas específicas
            table_structures = {
                'meses_reportes': {
                    'id': 'SERIAL PRIMARY KEY',
                    'mes': 'INTEGER NOT NULL',
                    'nombre': 'VARCHAR(20) NOT NULL',
                    'activo': 'BOOLEAN DEFAULT true',
                    'created_at': 'TIMESTAMP DEFAULT NOW()',
                    'updated_at': 'TIMESTAMP DEFAULT NOW()'
                }
            }
            
            if table_name not in table_structures:
                print(f"⚠️  Estructura no definida para {table_name}, saltando...")
                return False
            
            structure = table_structures[table_name]
            
            # Construir SQL de creación
            columns_sql = []
            for col_name, col_def in structure.items():
                columns_sql.append(f"{col_name} {col_def}")
            
            create_sql = f"""
            CREATE TABLE {table_name} (
                {', '.join(columns_sql)}
            );
            """
            
            print(f"   📝 SQL: {create_sql.strip()}")
            print(f"   ⚠️  NOTA: Ejecutar manualmente en Supabase SQL Editor")
            
            # Para tablas como meses_reportes, agregar datos iniciales
            if table_name == 'meses_reportes':
                insert_sql = """
                INSERT INTO meses_reportes (mes, nombre) VALUES
                (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
                (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
                (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre');
                """
                print(f"   📝 Datos iniciales: {insert_sql.strip()}")
            
            self.fixes_applied.append({
                'type': 'create_table',
                'table': table_name,
                'status': 'sql_generated',
                'sql': create_sql.strip()
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Error creando tabla {table_name}: {e}")
            self.errors.append(f"Error creando {table_name}: {e}")
            return False
    
    def add_missing_columns(self, table_name: str, structure: Dict[str, Any]) -> bool:
        """Agregar columnas faltantes a una tabla"""
        try:
            fixes_needed = []
            
            # Verificar qué columnas faltan
            if not structure.get('has_id', False):
                fixes_needed.append({
                    'column': 'id',
                    'definition': 'SERIAL PRIMARY KEY',
                    'sql': f'ALTER TABLE {table_name} ADD COLUMN id SERIAL PRIMARY KEY;'
                })
            
            if not structure.get('has_empresa_id', False) and table_name not in ['empresas', 'security_logs', 'meses_reportes']:
                fixes_needed.append({
                    'column': 'empresa_id',
                    'definition': 'UUID REFERENCES empresas(id)',
                    'sql': f'ALTER TABLE {table_name} ADD COLUMN empresa_id UUID REFERENCES empresas(id);'
                })
            
            if not structure.get('has_created_at', False):
                fixes_needed.append({
                    'column': 'created_at',
                    'definition': 'TIMESTAMP DEFAULT NOW()',
                    'sql': f'ALTER TABLE {table_name} ADD COLUMN created_at TIMESTAMP DEFAULT NOW();'
                })
            
            if not structure.get('has_activo', False) and table_name not in ['conversaciones', 'security_logs']:
                fixes_needed.append({
                    'column': 'activo',
                    'definition': 'BOOLEAN DEFAULT true',
                    'sql': f'ALTER TABLE {table_name} ADD COLUMN activo BOOLEAN DEFAULT true;'
                })
            
            if fixes_needed:
                print(f"\n🔧 Corrigiendo tabla: {table_name}")
                for fix in fixes_needed:
                    print(f"   ➕ Agregando columna: {fix['column']}")
                    print(f"      📝 SQL: {fix['sql']}")
                    
                    self.fixes_applied.append({
                        'type': 'add_column',
                        'table': table_name,
                        'column': fix['column'],
                        'sql': fix['sql'],
                        'status': 'sql_generated'
                    })
                
                return True
            else:
                print(f"   ✅ {table_name}: No necesita correcciones")
                return True
                
        except Exception as e:
            logger.error(f"Error corrigiendo {table_name}: {e}")
            self.errors.append(f"Error corrigiendo {table_name}: {e}")
            return False
    
    def generate_complete_sql_script(self) -> str:
        """Generar script SQL completo con todas las correcciones"""
        sql_script = f"""-- 🔧 Script de Corrección de Problemas Críticos - ACA 3.0
-- Generado: {datetime.now().isoformat()}
-- 
-- INSTRUCCIONES:
-- 1. Abrir Supabase Dashboard
-- 2. Ir a SQL Editor
-- 3. Ejecutar este script completo
-- 4. Verificar que todas las operaciones fueron exitosas

-- =====================================================================
-- CORRECCIONES DE PROBLEMAS CRÍTICOS
-- =====================================================================

"""
        
        # Agrupar por tipo de operación
        creates = [f for f in self.fixes_applied if f['type'] == 'create_table']
        alters = [f for f in self.fixes_applied if f['type'] == 'add_column']
        
        if creates:
            sql_script += "-- ===== CREACIÓN DE TABLAS FALTANTES =====\n\n"
            for fix in creates:
                sql_script += f"-- Crear tabla: {fix['table']}\n"
                sql_script += fix['sql'] + "\n\n"
        
        if alters:
            sql_script += "-- ===== ADICIÓN DE COLUMNAS FALTANTES =====\n\n"
            
            # Agrupar por tabla
            tables = {}
            for fix in alters:
                if fix['table'] not in tables:
                    tables[fix['table']] = []
                tables[fix['table']].append(fix)
            
            for table_name, table_fixes in tables.items():
                sql_script += f"-- Corregir tabla: {table_name}\n"
                for fix in table_fixes:
                    sql_script += f"-- Agregar columna: {fix['column']}\n"
                    sql_script += fix['sql'] + "\n"
                sql_script += "\n"
        
        # Agregar verificaciones finales
        sql_script += """-- ===== VERIFICACIONES FINALES =====

-- Verificar que las tablas existen
SELECT table_name, table_type 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Verificar estructura de tablas críticas
SELECT table_name, column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_schema = 'public' 
  AND table_name IN ('citas', 'security_logs', 'archivos_reportes', 'meses_reportes')
ORDER BY table_name, ordinal_position;

-- ===== FINALIZADO =====
-- Ejecutar check_database.py para verificar que todos los problemas fueron corregidos
"""
        
        return sql_script
    
    def analyze_and_fix(self) -> Dict[str, Any]:
        """Analizar y generar correcciones para todos los problemas críticos"""
        print("\n🔍 Analizando problemas críticos...")
        
        # Tablas que necesitan revisión según el análisis anterior
        critical_tables = [
            'citas',           # Sin id, sin empresa_id
            'security_logs',   # Sin id
            'archivos_reportes', # Sin id, sin empresa_id
            'meses_reportes'   # No existe
        ]
        
        tables_processed = 0
        
        for table_name in critical_tables:
            print(f"\n📋 Analizando: {table_name}")
            
            structure = self.check_table_structure(table_name)
            
            if not structure.get('exists', False):
                print(f"   ❌ Tabla no existe")
                self.create_missing_table(table_name)
            else:
                print(f"   ✅ Tabla existe")
                if structure.get('has_data', False) or not structure.get('unknown_structure', False):
                    self.add_missing_columns(table_name, structure)
                else:
                    print(f"   ⚠️  Estructura desconocida, se necesita revisión manual")
            
            tables_processed += 1
        
        # Generar script SQL completo
        sql_script = self.generate_complete_sql_script()
        
        return {
            'tables_processed': tables_processed,
            'fixes_generated': len(self.fixes_applied),
            'errors': len(self.errors),
            'sql_script': sql_script
        }
    
    def save_sql_script(self, sql_script: str) -> str:
        """Guardar script SQL en archivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fix_critical_issues_{timestamp}.sql"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(sql_script)
        
        return filename
    
    def print_summary(self, result: Dict[str, Any]):
        """Imprimir resumen de las correcciones"""
        print(f"\n📊 RESUMEN DE CORRECCIONES:")
        print(f"   📋 Tablas procesadas: {result['tables_processed']}")
        print(f"   🔧 Correcciones generadas: {result['fixes_generated']}")
        print(f"   ❌ Errores encontrados: {result['errors']}")
        
        if self.fixes_applied:
            print(f"\n🔧 CORRECCIONES GENERADAS:")
            for fix in self.fixes_applied:
                if fix['type'] == 'create_table':
                    print(f"   📋 Crear tabla: {fix['table']}")
                elif fix['type'] == 'add_column':
                    print(f"   ➕ Agregar {fix['column']} a {fix['table']}")
        
        if self.errors:
            print(f"\n⚠️  ERRORES:")
            for error in self.errors:
                print(f"   ❌ {error}")


def main():
    """Función principal"""
    try:
        # Crear corrector
        fixer = CriticalIssueFixer()
        fixer.print_header()
        
        print("🎯 Este script identificará y generará correcciones para problemas críticos:")
        print("   • Tablas sin clave primaria (id)")
        print("   • Tablas sin empresa_id para aislamiento")
        print("   • Tablas faltantes")
        print("   • Columnas críticas faltantes")
        
        # Pedir confirmación
        confirm = input("\n¿Continuar con el análisis? (s/n): ").lower().strip()
        if confirm not in ['s', 'si', 'yes', 'y']:
            print("❌ Operación cancelada")
            return
        
        # Ejecutar análisis y generar correcciones
        result = fixer.analyze_and_fix()
        
        # Mostrar resumen
        fixer.print_summary(result)
        
        # Guardar script SQL
        if result['fixes_generated'] > 0:
            sql_filename = fixer.save_sql_script(result['sql_script'])
            print(f"\n💾 Script SQL guardado en: {sql_filename}")
            
            print(f"\n📋 PRÓXIMOS PASOS:")
            print(f"   1. 🌐 Abrir Supabase Dashboard")
            print(f"   2. 📝 Ir a SQL Editor")
            print(f"   3. 📄 Abrir el archivo: {sql_filename}")
            print(f"   4. ▶️  Ejecutar el script completo")
            print(f"   5. ✅ Verificar con: python check_database.py")
            
            # Mostrar vista previa del script
            print(f"\n👀 VISTA PREVIA DEL SCRIPT:")
            print("─" * 60)
            script_lines = result['sql_script'].split('\n')
            for i, line in enumerate(script_lines[:20]):  # Mostrar primeras 20 líneas
                print(line)
            if len(script_lines) > 20:
                print(f"... ({len(script_lines) - 20} líneas más)")
            print("─" * 60)
        else:
            print("\n🎉 ¡No se encontraron problemas críticos que corregir!")
            print("   Tu base de datos ya está en buen estado.")
        
        print("\n" + "="*80)
        return result['fixes_generated']
        
    except KeyboardInterrupt:
        print("\n\n👋 Operación cancelada por el usuario")
        return 0
    except Exception as e:
        logger.error(f"Error durante la corrección: {e}")
        print(f"\n❌ Error: {e}")
        print("\n💡 Posibles soluciones:")
        print("   • Verificar variables de entorno en .env")
        print("   • Comprobar permisos en Supabase")
        print("   • Validar conectividad a internet")
        return 0

if __name__ == "__main__":
    fixes_count = main()
    sys.exit(0 if fixes_count >= 0 else 1)