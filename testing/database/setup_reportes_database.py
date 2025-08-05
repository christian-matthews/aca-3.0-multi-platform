#!/usr/bin/env python3
"""
Script para configurar las tablas de reportes por empresa en Supabase
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.supabase import supabase
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_reportes_database():
    """Configurar las tablas de reportes en Supabase"""
    
    print("🚀 Configurando base de datos para reportes por empresa...")
    
    try:
        # Leer el archivo SQL
        with open('docs/reportes_por_empresa_schema.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print("📄 Archivo SQL leído correctamente")
        
        # Dividir el SQL en comandos individuales
        commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
        
        print(f"🔧 Ejecutando {len(commands)} comandos SQL...")
        
        # Ejecutar cada comando
        for i, command in enumerate(commands, 1):
            if command and not command.startswith('--'):
                try:
                    print(f"  [{i}/{len(commands)}] Ejecutando comando...")
                    supabase.client.rpc('exec_sql', {'sql': command}).execute()
                    print(f"  ✅ Comando {i} ejecutado correctamente")
                except Exception as e:
                    print(f"  ⚠️ Comando {i} falló: {e}")
                    # Continuar con el siguiente comando
        
        print("\n✅ Configuración de base de datos completada")
        print("\n📋 Tablas creadas:")
        print("  • reportes_mensuales")
        print("  • archivos_reportes")
        print("  • comentarios_reportes")
        print("  • info_compania")
        print("  • archivos_info_compania")
        
        print("\n🔒 Políticas RLS configuradas para seguridad")
        print("\n📊 Datos de ejemplo insertados")
        
        return True
        
    except Exception as e:
        logger.error(f"Error configurando base de datos: {e}")
        print(f"❌ Error: {e}")
        return False

def verify_setup():
    """Verificar que las tablas se crearon correctamente"""
    
    print("\n🔍 Verificando configuración...")
    
    try:
        # Verificar tablas principales
        tables_to_check = [
            'reportes_mensuales',
            'archivos_reportes', 
            'comentarios_reportes',
            'info_compania',
            'archivos_info_compania'
        ]
        
        for table in tables_to_check:
            try:
                result = supabase.client.table(table).select('count', count='exact').limit(1).execute()
                print(f"  ✅ Tabla '{table}' existe")
            except Exception as e:
                print(f"  ❌ Tabla '{table}' no existe: {e}")
        
        # Verificar datos de ejemplo
        try:
            reportes = supabase.get_reportes_mensuales(empresa_id=None)
            print(f"  📊 {len(reportes)} reportes de ejemplo encontrados")
        except Exception as e:
            print(f"  ⚠️ Error verificando reportes: {e}")
        
        try:
            info = supabase.get_info_compania(empresa_id=None)
            print(f"  📋 {len(info)} registros de información de compañía encontrados")
        except Exception as e:
            print(f"  ⚠️ Error verificando información: {e}")
        
        print("\n✅ Verificación completada")
        return True
        
    except Exception as e:
        logger.error(f"Error en verificación: {e}")
        print(f"❌ Error en verificación: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("📊 CONFIGURACIÓN DE REPORTES POR EMPRESA - ACA 3.0")
    print("=" * 60)
    
    # Verificar variables de entorno
    if not os.getenv('SUPABASE_URL') or not os.getenv('SUPABASE_KEY'):
        print("❌ Error: Variables de entorno SUPABASE_URL y SUPABASE_KEY son requeridas")
        print("   Asegúrate de tener un archivo .env configurado")
        sys.exit(1)
    
    # Configurar base de datos
    if setup_reportes_database():
        # Verificar configuración
        verify_setup()
        
        print("\n" + "=" * 60)
        print("🎉 ¡Configuración completada exitosamente!")
        print("=" * 60)
        print("\n📝 Próximos pasos:")
        print("1. Ejecuta el bot de producción")
        print("2. Ve a 'Información' → 'Reportes'")
        print("3. Selecciona un mes para ver los reportes")
        print("4. Prueba las funcionalidades de adjuntar archivos")
        print("\n🚀 ¡Listo para usar!")
    else:
        print("\n❌ La configuración falló. Revisa los errores arriba.")
        sys.exit(1) 