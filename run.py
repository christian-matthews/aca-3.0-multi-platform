#!/usr/bin/env python3
"""
Script de inicio para ACA 3.0
Ejecuta la aplicación con configuración de desarrollo
"""

import os
import sys
import logging
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

def setup_environment():
    """Configurar entorno de desarrollo"""
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Verificar archivo .env
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  Archivo .env no encontrado")
        print("📝 Copiando env.example a .env...")
        
        example_file = Path('env.example')
        if example_file.exists():
            import shutil
            shutil.copy('env.example', '.env')
            print("✅ Archivo .env creado. Por favor, edítalo con tus credenciales.")
            print("🔧 Variables requeridas:")
            print("   - BOT_ADMIN_TOKEN")
            print("   - BOT_PRODUCTION_TOKEN")
            print("   - ADMIN_CHAT_ID")
            print("   - SUPABASE_URL")
            print("   - SUPABASE_KEY")
            print("   - OPENAI_API_KEY")
            return False
        else:
            print("❌ Archivo env.example no encontrado")
            return False
    
    return True

def validate_config():
    """Validar configuración"""
    try:
        from app.config import Config
        Config.validate()
        print("✅ Configuración validada correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando ACA 3.0...")
    
    # Configurar entorno
    if not setup_environment():
        print("❌ Error configurando entorno")
        sys.exit(1)
    
    # Validar configuración
    if not validate_config():
        print("❌ Error validando configuración")
        sys.exit(1)
    
    print("✅ Entorno configurado correctamente")
    print("🤖 Iniciando bots de Telegram...")
    
    try:
        # Importar y ejecutar la aplicación
        from app.main import app
        import uvicorn
        
        print("🌐 Servidor web iniciado en http://localhost:8000")
        print("📊 Documentación API en http://localhost:8000/docs")
        print("🔍 Health check en http://localhost:8000/health")
        print("📱 Bots de Telegram iniciados")
        print("\n🛑 Presiona Ctrl+C para detener")
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 