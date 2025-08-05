#!/usr/bin/env python3
"""
⚡ Quick DB Check - Verificación súper rápida de base de datos ACA 3.0
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

def quick_check():
    """Verificación ultra rápida en una línea"""
    try:
        client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        
        # Verificar tablas críticas
        empresas = client.table('empresas').select("*", count="exact").limit(0).execute().count
        usuarios = client.table('usuarios').select("*", count="exact").limit(0).execute().count
        
        # Calcular estado
        if empresas > 0 and usuarios > 0:
            status = "✅ OK"
            color = "\033[92m"  # Verde
        elif empresas > 0:
            status = "⚠️ PARTIAL"
            color = "\033[93m"  # Amarillo
        else:
            status = "❌ EMPTY"
            color = "\033[91m"  # Rojo
        
        reset = "\033[0m"  # Reset color
        
        print(f"{color}[ACA 3.0 DB] {status} - Empresas: {empresas}, Usuarios: {usuarios}{reset}")
        return empresas > 0 and usuarios > 0
        
    except Exception as e:
        print(f"\033[91m[ACA 3.0 DB] ❌ ERROR - {str(e)[:50]}...\033[0m")
        return False

if __name__ == "__main__":
    import sys
    sys.exit(0 if quick_check() else 1)