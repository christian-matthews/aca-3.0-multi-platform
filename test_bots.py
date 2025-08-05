#!/usr/bin/env python3
"""
Script para probar los bots de Telegram
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_bots():
    """Probar los bots de Telegram"""
    print("🤖 Probando bots de Telegram...")
    
    try:
        from app.bots.bot_manager import bot_manager
        
        # Inicializar bots
        print("🔧 Inicializando bots...")
        await bot_manager.initialize_bots()
        print("✅ Bots inicializados")
        
        # Iniciar bots
        print("🚀 Iniciando bots...")
        await bot_manager.start_bots()
        print("✅ Bots iniciados y escuchando")
        
        print("\n📱 Bots activos:")
        print("   - Bot Admin: @tu_bot_admin")
        print("   - Bot Producción: @tu_bot_produccion")
        print("\n💡 Envía /start a cualquiera de los bots para probarlos")
        print("🛑 Presiona Ctrl+C para detener")
        
        # Mantener ejecutándose
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 Deteniendo bots...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        try:
            await bot_manager.stop_bots()
            print("✅ Bots detenidos")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_bots()) 