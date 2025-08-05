#!/usr/bin/env python3
"""
Script de prueba del sistema completo ACA 3.0
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_configuration():
    """Probar la configuración del sistema"""
    print("🔧 Probando configuración...")
    
    try:
        from app.config import Config
        Config.validate()
        print("✅ Configuración válida")
        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_supabase_connection():
    """Probar conexión a Supabase"""
    print("\n🗄️ Probando conexión a Supabase...")
    
    try:
        from app.database.supabase import supabase
        
        # Probar conexión básica
        result = supabase.table('empresas').select('*').limit(1).execute()
        print(f"✅ Conexión exitosa - Encontradas {len(result.data)} empresas")
        
        # Probar obtener empresas
        empresas = supabase.table('empresas').select('*').execute()
        print(f"📊 Total empresas en BD: {len(empresas.data)}")
        
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_sample_data():
    """Probar datos de ejemplo"""
    print("\n📋 Verificando datos de ejemplo...")
    
    try:
        from app.database.supabase import supabase
        
        # Verificar empresas
        empresas = supabase.table('empresas').select('*').execute()
        print(f"🏢 Empresas encontradas: {len(empresas.data)}")
        for empresa in empresas.data:
            print(f"   - {empresa['nombre']} (RUT: {empresa['rut']})")
        
        # Verificar usuarios
        usuarios = supabase.table('usuarios').select('*').execute()
        print(f"👥 Usuarios encontrados: {len(usuarios.data)}")
        for usuario in usuarios.data:
            print(f"   - {usuario['nombre']} (chat_id: {usuario['chat_id']})")
        
        # Verificar reportes
        reportes = supabase.table('reportes').select('*').execute()
        print(f"📊 Reportes encontrados: {len(reportes.data)}")
        for reporte in reportes.data:
            print(f"   - {reporte['titulo']}")
        
        # Verificar pendientes
        pendientes = supabase.table('pendientes').select('*').execute()
        print(f"⏳ Pendientes encontrados: {len(pendientes.data)}")
        for pendiente in pendientes.data:
            print(f"   - {pendiente['titulo']} ({pendiente['prioridad']})")
        
        # Verificar cuentas por cobrar
        cxc = supabase.table('cuentas_cobrar').select('*').execute()
        print(f"💰 Cuentas por cobrar: {len(cxc.data)}")
        total_cxc = sum(item['monto'] for item in cxc.data)
        print(f"   - Total: ${total_cxc:,.0f}")
        
        # Verificar cuentas por pagar
        cxp = supabase.table('cuentas_pagar').select('*').execute()
        print(f"💸 Cuentas por pagar: {len(cxp.data)}")
        total_cxp = sum(item['monto'] for item in cxp.data)
        print(f"   - Total: ${total_cxp:,.0f}")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando datos: {e}")
        return False

def test_user_validation():
    """Probar validación de usuarios"""
    print("\n🔐 Probando validación de usuarios...")
    
    try:
        from app.security.auth import security
        
        # Probar con chat_id de ejemplo
        test_chat_id = 123456789
        
        validation = security.validate_user(test_chat_id)
        if validation['valid']:
            print(f"✅ Usuario válido: {validation['user_data']['nombre']}")
            print(f"   Empresa: {validation['user_data']['empresa_nombre']}")
        else:
            print(f"❌ Usuario no válido: {validation['message']}")
        
        # Probar con chat_id inexistente
        invalid_chat_id = 999999999
        validation = security.validate_user(invalid_chat_id)
        if not validation['valid']:
            print(f"✅ Validación correcta para usuario inexistente")
        else:
            print(f"❌ Error: usuario inexistente fue validado")
        
        return True
    except Exception as e:
        print(f"❌ Error en validación: {e}")
        return False

def test_conversation_logging():
    """Probar logging de conversaciones"""
    print("\n💬 Probando logging de conversaciones...")
    
    try:
        from app.database.supabase import supabase
        
        test_chat_id = 123456789
        test_message = "Mensaje de prueba desde script"
        test_response = "Respuesta de prueba"
        
        # Obtener empresa_id real
        empresas = supabase.table('empresas').select('id').limit(1).execute()
        if empresas.data:
            empresa_id = empresas.data[0]['id']
            
            # Log de conversación
            supabase.log_conversation(
                chat_id=test_chat_id,
                empresa_id=empresa_id,
                mensaje=test_message,
                respuesta=test_response
            )
        else:
            print("⚠️ No hay empresas disponibles para el test")
            return False
        
        print("✅ Logging de conversación exitoso")
        return True
    except Exception as e:
        print(f"❌ Error en logging: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas del sistema ACA 3.0")
    print("=" * 50)
    
    tests = [
        ("Configuración", test_configuration),
        ("Conexión Supabase", test_supabase_connection),
        ("Datos de Ejemplo", test_sample_data),
        ("Validación de Usuarios", test_user_validation),
        ("Logging de Conversaciones", test_conversation_logging)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está listo.")
        return True
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 