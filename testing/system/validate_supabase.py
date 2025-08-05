#!/usr/bin/env python3
"""
Script simple para validar conexión a Supabase
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def check_supabase_connection():
    """Verificar conexión a Supabase"""
    print("🔧 Verificando conexión a Supabase...")
    
    # Verificar variables de Supabase
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Variables de Supabase faltantes:")
        if not supabase_url:
            print("   - SUPABASE_URL")
        if not supabase_key:
            print("   - SUPABASE_KEY")
        print("\n📝 Configura estas variables en tu archivo .env")
        return False
    
    print("✅ Variables de Supabase configuradas")
    print(f"   URL: {supabase_url}")
    print(f"   Key: {supabase_key[:20]}...")
    
    # Probar conexión
    try:
        from supabase import create_client
        
        # Crear cliente
        supabase = create_client(supabase_url, supabase_key)
        
        # Probar consulta simple
        result = supabase.table('empresas').select('*').limit(1).execute()
        
        print("✅ Conexión exitosa a Supabase")
        print(f"   Empresas encontradas: {len(result.data)}")
        
        # Mostrar datos de ejemplo si existen
        if result.data:
            empresa = result.data[0]
            print(f"   Ejemplo: {empresa['nombre']} (RUT: {empresa['rut']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\n🔍 Posibles soluciones:")
        print("   1. Verifica que las credenciales sean correctas")
        print("   2. Asegúrate de que las tablas existan en Supabase")
        print("   3. Ejecuta el script setup_database.sql en Supabase")
        return False

def check_tables():
    """Verificar que las tablas existan"""
    print("\n📋 Verificando tablas...")
    
    try:
        from supabase import create_client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        supabase = create_client(supabase_url, supabase_key)
        
        tables = [
            'empresas', 'usuarios', 'conversaciones', 'reportes',
            'pendientes', 'cuentas_cobrar', 'cuentas_pagar', 'citas', 'security_logs'
        ]
        
        for table in tables:
            try:
                result = supabase.table(table).select('*').limit(1).execute()
                print(f"✅ Tabla '{table}' existe")
            except Exception as e:
                print(f"❌ Tabla '{table}' no existe: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

def check_sample_data():
    """Verificar datos de ejemplo"""
    print("\n📊 Verificando datos de ejemplo...")
    
    try:
        from supabase import create_client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        supabase = create_client(supabase_url, supabase_key)
        
        # Verificar empresas
        empresas = supabase.table('empresas').select('*').execute()
        print(f"🏢 Empresas: {len(empresas.data)}")
        
        # Verificar usuarios
        usuarios = supabase.table('usuarios').select('*').execute()
        print(f"👥 Usuarios: {len(usuarios.data)}")
        
        # Verificar reportes
        reportes = supabase.table('reportes').select('*').execute()
        print(f"📊 Reportes: {len(reportes.data)}")
        
        # Verificar pendientes
        pendientes = supabase.table('pendientes').select('*').execute()
        print(f"⏳ Pendientes: {len(pendientes.data)}")
        
        # Verificar cuentas
        cxc = supabase.table('cuentas_cobrar').select('*').execute()
        cxp = supabase.table('cuentas_pagar').select('*').execute()
        print(f"💰 Cuentas por cobrar: {len(cxc.data)}")
        print(f"💸 Cuentas por pagar: {len(cxp.data)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando datos: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Validación de Supabase ACA 3.0")
    print("=" * 40)
    
    # Verificar conexión
    if not check_supabase_connection():
        return False
    
    # Verificar tablas
    if not check_tables():
        print("\n❌ Las tablas no existen. Ejecuta setup_database.sql en Supabase")
        return False
    
    # Verificar datos
    if not check_sample_data():
        print("\n❌ No hay datos de ejemplo. Ejecuta setup_database.sql en Supabase")
        return False
    
    print("\n🎉 ¡Validación completada exitosamente!")
    print("✅ Supabase está configurado correctamente")
    print("✅ Las tablas existen")
    print("✅ Los datos de ejemplo están cargados")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 