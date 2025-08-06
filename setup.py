#!/usr/bin/env python3
"""
Script de configuración automática para ACA 3.0
Instala dependencias y verifica la configuración del sistema
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_step(step_num, total_steps, description):
    """Imprimir paso actual"""
    print(f"\n{'='*60}")
    print(f"📋 PASO {step_num}/{total_steps}: {description}")
    print(f"{'='*60}")

def run_command(command, description, check=True):
    """Ejecutar comando con manejo de errores"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {description} completado")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False
    return True

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.9+")
        return False

def setup_virtual_environment():
    """Configurar entorno virtual"""
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("🔄 Creando entorno virtual...")
        if run_command("python3 -m venv venv", "Creación de entorno virtual"):
            print("✅ Entorno virtual creado")
        else:
            return False
    else:
        print("✅ Entorno virtual ya existe")
    
    return True

def install_dependencies():
    """Instalar dependencias"""
    activate_cmd = "source venv/bin/activate" if os.name != 'nt' else "venv\\Scripts\\activate"
    
    commands = [
        f"{activate_cmd} && pip install --upgrade pip",
        f"{activate_cmd} && pip install -r requirements.txt"
    ]
    
    for cmd in commands:
        if not run_command(cmd, "Instalación de dependencias"):
            return False
    
    return True

def verify_configuration():
    """Verificar configuración"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("⚠️  Archivo .env no encontrado")
        print("📝 Creando .env desde template...")
        
        if Path("env.example").exists():
            run_command("cp env.example .env", "Copia de archivo de configuración")
            print("✅ Archivo .env creado desde template")
            print("⚠️  IMPORTANTE: Configura las variables en .env antes de continuar")
        else:
            print("❌ Template env.example no encontrado")
            return False
    else:
        print("✅ Archivo .env encontrado")
    
    return True

def test_system_components():
    """Probar componentes del sistema"""
    activate_cmd = "source venv/bin/activate" if os.name != 'nt' else "venv\\Scripts\\activate"
    
    tests = [
        f"{activate_cmd} && python -c 'from app.main import app; print(\"✅ FastAPI importado correctamente\")'",
        f"{activate_cmd} && python -c 'from app.database.supabase import get_supabase_client; print(\"✅ Supabase configurado\")'",
        f"{activate_cmd} && python -c 'from app.services.airtable_service import get_airtable_service; print(\"✅ Airtable configurado\")'",
    ]
    
    for test in tests:
        if not run_command(test, "Prueba de componente", check=False):
            print("⚠️  Algunos componentes pueden requerir configuración adicional")
    
    return True

def create_startup_script():
    """Crear script de inicio"""
    startup_script = """#!/bin/bash
# Script de inicio para ACA 3.0

echo "🚀 Iniciando ACA 3.0..."

# Activar entorno virtual
source venv/bin/activate

# Verificar configuración
if [ ! -f ".env" ]; then
    echo "❌ Archivo .env no encontrado"
    echo "📝 Copia env.example a .env y configúralo"
    exit 1
fi

# Iniciar servidor
echo "🌐 Iniciando servidor en http://localhost:8000"
python3 run.py
"""

    with open("start.sh", "w") as f:
        f.write(startup_script)
    
    run_command("chmod +x start.sh", "Hacer ejecutable script de inicio")
    print("✅ Script de inicio creado: ./start.sh")

def show_completion_message():
    """Mostrar mensaje de finalización"""
    print(f"\n{'='*60}")
    print("🎉 CONFIGURACIÓN COMPLETADA")
    print(f"{'='*60}")
    print()
    print("📋 PRÓXIMOS PASOS:")
    print("1. 📝 Configura las variables en el archivo .env")
    print("2. 🚀 Ejecuta: ./start.sh (o python3 run.py)")
    print("3. 🌐 Abre: http://localhost:8000/dashboard")
    print()
    print("📊 FUNCIONALIDADES DISPONIBLES:")
    print("• 🤖 Bots de Telegram (Admin y Producción)")
    print("• 🌐 Dashboard Web completo")
    print("• 📊 Integración con Airtable")
    print("• 🗄️  Sincronización con Supabase")
    print("• 📈 Estadísticas en tiempo real")
    print("• 🔄 Sincronización automática")
    print()
    print("📖 DOCUMENTACIÓN:")
    print("• API Docs: http://localhost:8000/docs")
    print("• Health Check: http://localhost:8000/health")
    print("• Dashboard: http://localhost:8000/dashboard")
    print()
    print("🆘 SOPORTE:")
    print("• Revisa los logs en caso de errores")
    print("• Verifica la configuración en .env")
    print("• Comprueba la conectividad con Supabase y Airtable")
    print(f"{'='*60}")

def main():
    """Función principal"""
    print("🚀 CONFIGURACIÓN AUTOMÁTICA DE ACA 3.0")
    print("Sistema de Gestión Contable Multi-Plataforma")
    
    total_steps = 7
    
    # Paso 1: Verificar Python
    print_step(1, total_steps, "Verificar versión de Python")
    if not check_python_version():
        sys.exit(1)
    
    # Paso 2: Configurar entorno virtual
    print_step(2, total_steps, "Configurar entorno virtual")
    if not setup_virtual_environment():
        sys.exit(1)
    
    # Paso 3: Instalar dependencias
    print_step(3, total_steps, "Instalar dependencias")
    if not install_dependencies():
        sys.exit(1)
    
    # Paso 4: Verificar configuración
    print_step(4, total_steps, "Verificar configuración")
    if not verify_configuration():
        sys.exit(1)
    
    # Paso 5: Probar componentes
    print_step(5, total_steps, "Probar componentes del sistema")
    test_system_components()
    
    # Paso 6: Crear script de inicio
    print_step(6, total_steps, "Crear script de inicio")
    create_startup_script()
    
    # Paso 7: Finalización
    print_step(7, total_steps, "Finalización")
    show_completion_message()

if __name__ == "__main__":
    main()