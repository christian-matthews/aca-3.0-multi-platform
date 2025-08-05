#!/usr/bin/env python3
"""
Prueba rápida de conexión a Supabase
"""

import os
from dotenv import load_dotenv

load_dotenv()

def quick_test():
    """Prueba rápida de conexión"""
    print("🔍 Prueba rápida de Supabase...")
    
    # Verificar variables
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or url == "your_supabase_url_here":
        print("❌ SUPABASE_URL no configurada")
        return False
    
    if not key or key == "your_supabase_anon_key_here":
        print("❌ SUPABASE_KEY no configurada")
        return False
    
    print(f"✅ URL: {url}")
    print(f"✅ Key: {key[:20]}...")
    
    # Probar conexión
    try:
        from supabase import create_client
        supabase = create_client(url, key)
        
        # Consulta simple
        result = supabase.table('empresas').select('*').limit(1).execute()
        print(f"✅ Conexión exitosa - {len(result.data)} empresas")
        
        if result.data:
            empresa = result.data[0]
            print(f"   📋 Ejemplo: {empresa['nombre']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    print(f"\n{'🎉 Éxito' if success else '❌ Falló'}") 