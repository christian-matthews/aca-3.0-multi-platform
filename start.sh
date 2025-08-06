#!/bin/bash
# Script de inicio para ACA 3.0 - Sistema de Gestión Contable

echo "🚀 Iniciando ACA 3.0 - Sistema de Gestión Contable"
echo "=================================================="

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado"
    echo "📝 Ejecuta primero: python3 setup.py"
    exit 1
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Verificar configuración
if [ ! -f ".env" ]; then
    echo "❌ Archivo .env no encontrado"
    echo "📝 Copia env.example a .env y configúralo"
    exit 1
fi

# Verificar que las dependencias estén instaladas
echo "🔄 Verificando dependencias..."
python3 -c "import fastapi, supabase, pyairtable" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Instalando dependencias faltantes..."
    pip install -r requirements.txt
fi

# Mostrar información del sistema
echo ""
echo "📊 INFORMACIÓN DEL SISTEMA:"
echo "• Entorno virtual: ✅ Activado"
echo "• Configuración: ✅ .env encontrado"
echo "• Dependencias: ✅ Instaladas"
echo ""

# Iniciar servidor
echo "🌐 Iniciando servidor..."
echo "📍 Dashboard: http://localhost:8000/dashboard"
echo "📖 API Docs: http://localhost:8000/docs"
echo "❤️  Health: http://localhost:8000/health"
echo ""
echo "🛑 Presiona Ctrl+C para detener"
echo "=================================================="

python3 run.py