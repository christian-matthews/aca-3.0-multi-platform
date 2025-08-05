#!/bin/bash

# Script para activar el entorno virtual de ACA 3.0

echo "🚀 Activando entorno virtual para ACA 3.0..."

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado. Creando..."
    python3 -m venv venv
fi

# Activar el entorno virtual
source venv/bin/activate

# Verificar que está activado
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Entorno virtual activado: $VIRTUAL_ENV"
    echo "🐍 Python: $(which python)"
    echo "📦 Pip: $(which pip)"
    echo ""
    echo "📋 Comandos útiles:"
    echo "  • python run.py          - Ejecutar la aplicación"
    echo "  • python -m app.main     - Ejecutar directamente"
    echo "  • pip install -r requirements.txt - Instalar dependencias"
    echo "  • deactivate             - Desactivar entorno virtual"
    echo ""
    echo "🔧 Para configurar variables de entorno:"
    echo "  • Editar archivo .env con tus credenciales"
    echo ""
else
    echo "❌ Error activando el entorno virtual"
    exit 1
fi 