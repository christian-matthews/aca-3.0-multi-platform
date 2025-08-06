#!/usr/bin/env python3
"""
🔍 Script de verificación pre-deploy para ACA 3.0
Verifica que todos los componentes estén listos para deploy en Render
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_file_exists(filepath: str, required: bool = True) -> bool:
    """Verifica si un archivo existe"""
    exists = Path(filepath).exists()
    status = "✅" if exists else "❌"
    requirement = "(REQUERIDO)" if required else "(OPCIONAL)"
    print(f"{status} {filepath} {requirement}")
    return exists

def check_env_example() -> bool:
    """Verifica que env.example tenga todas las variables necesarias"""
    print("\n🔧 Verificando env.example...")
    
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY", 
        "TELEGRAM_BOT_TOKEN_ADMIN",
        "TELEGRAM_BOT_TOKEN_PROD",
        "OPENAI_API_KEY",
        "AIRTABLE_API_KEY",
        "AIRTABLE_BASE_ID",
        "AIRTABLE_TABLE_NAME",
        "AIRTABLE_VIEW_NAME"
    ]
    
    if not Path("env.example").exists():
        print("❌ env.example no existe")
        return False
    
    with open("env.example", "r") as f:
        content = f.read()
    
    missing_vars = []
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables faltantes en env.example: {missing_vars}")
        return False
    else:
        print("✅ Todas las variables requeridas están en env.example")
        return True

def check_dependencies() -> bool:
    """Verifica que todas las dependencias estén instaladas"""
    print("\n📦 Verificando dependencias...")
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "jinja2",
        "python-dotenv",
        "supabase",
        "python-telegram-bot",
        "openai",
        "pyairtable",
        "aiofiles"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            spec = importlib.util.find_spec(package.replace("-", "_"))
            if spec is None:
                missing_packages.append(package)
            else:
                print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n❌ Paquetes faltantes: {missing_packages}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    return True

def check_app_structure() -> bool:
    """Verifica estructura de la aplicación"""
    print("\n🏗️ Verificando estructura de la aplicación...")
    
    required_files = [
        ("app/__init__.py", True),
        ("app/main.py", True),
        ("app/config.py", True),
        ("app/bots/bot_manager.py", True),
        ("app/services/airtable_service.py", True),
        ("app/services/sync_service.py", True),
        ("app/database/supabase.py", True),
    ]
    
    required_dirs = [
        "templates",
        "static"
    ]
    
    all_good = True
    
    # Verificar archivos
    for filepath, required in required_files:
        if not check_file_exists(filepath, required):
            if required:
                all_good = False
    
    # Verificar directorios
    for dirname in required_dirs:
        exists = Path(dirname).is_dir()
        status = "✅" if exists else "❌"
        print(f"{status} {dirname}/ (DIRECTORIO)")
        if not exists:
            all_good = False
    
    return all_good

def check_deploy_files() -> bool:
    """Verifica archivos específicos para deploy"""
    print("\n🚀 Verificando archivos de deploy...")
    
    deploy_files = [
        ("Procfile", True),
        ("requirements.txt", True),
        ("runtime.txt", True),
        (".gitignore", True),
        ("render.yaml", False),
        ("DEPLOY_RENDER_GUIDE.md", False)
    ]
    
    all_good = True
    
    for filepath, required in deploy_files:
        if not check_file_exists(filepath, required):
            if required:
                all_good = False
    
    return all_good

def check_git_status() -> bool:
    """Verifica estado del repositorio git"""
    print("\n📝 Verificando estado Git...")
    
    try:
        # Verificar si es un repo git
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ No es un repositorio Git")
            return False
        
        # Verificar si hay cambios sin commit
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️ Hay cambios sin commit:")
            print(result.stdout)
            return False
        else:
            print("✅ Todos los cambios están committed")
        
        # Verificar remote origin
        result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Remote origin: {result.stdout.strip()}")
        else:
            print("❌ No hay remote origin configurado")
            return False
        
        return True
        
    except FileNotFoundError:
        print("❌ Git no está instalado o no disponible")
        return False

def run_basic_tests() -> bool:
    """Ejecuta tests básicos de la aplicación"""
    print("\n🧪 Ejecutando tests básicos...")
    
    try:
        # Test de importación principal
        import app.main
        print("✅ app.main se importa correctamente")
        
        # Test de configuración
        import app.config
        print("✅ app.config se importa correctamente")
        
        # Test de servicios
        import app.services.airtable_service
        import app.services.sync_service
        print("✅ Servicios se importan correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en tests básicos: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🔍 VERIFICACIÓN PRE-DEPLOY ACA 3.0")
    print("=" * 50)
    
    checks = [
        ("Estructura de la aplicación", check_app_structure),
        ("Archivos de deploy", check_deploy_files),
        ("Variables de entorno", check_env_example),
        ("Dependencias", check_dependencies),
        ("Estado Git", check_git_status),
        ("Tests básicos", run_basic_tests)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        try:
            if check_func():
                passed += 1
                print(f"✅ {check_name}: PASSED")
            else:
                print(f"❌ {check_name}: FAILED")
        except Exception as e:
            print(f"❌ {check_name}: ERROR - {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 RESUMEN: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("🎉 ¡LISTO PARA DEPLOY!")
        print("\n📋 NEXT STEPS:")
        print("1. Ve a https://render.com")
        print("2. Conecta tu repositorio GitHub")
        print("3. Configura las variables de entorno")
        print("4. Deploy!")
        return True
    else:
        print("⚠️ Hay problemas que resolver antes del deploy")
        print("\n💡 Revisa los errores arriba y corrígelos")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)