#!/usr/bin/env python3
"""
Script para probar el acceso de administrador
"""

import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_admin_access():
    """Probar acceso de administrador"""
    print("🔐 Probando acceso de administrador...")
    
    try:
        from app.config import Config
        from app.security.auth import security
        
        # Mostrar configuración
        print(f"📋 Configuración:")
        print(f"   ADMIN_CHAT_ID: {Config.ADMIN_CHAT_ID}")
        print(f"   Tipo: {type(Config.ADMIN_CHAT_ID)}")
        
        # Probar con tu chat_id
        your_chat_id = Config.ADMIN_CHAT_ID
        is_admin = security.is_admin(your_chat_id)
        
        print(f"\n🔍 Resultado:")
        print(f"   Tu chat_id: {your_chat_id}")
        print(f"   ¿Es admin?: {'✅ Sí' if is_admin else '❌ No'}")
        
        # Mostrar lista de admins
        print(f"\n👥 Administradores configurados:")
        for admin_id in security.admin_chat_ids:
            print(f"   - {admin_id}")
        
        if is_admin:
            print("\n🎉 ¡Tienes acceso de administrador!")
            return True
        else:
            print("\n❌ No tienes acceso de administrador")
            print("💡 Verifica que tu ADMIN_CHAT_ID esté configurado correctamente")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_bot_admin():
    """Probar el bot de administración"""
    print("\n🤖 Probando bot de administración...")
    
    try:
        from app.bots.handlers.admin_handlers import AdminHandlers
        from app.config import Config
        
        # Simular un update de Telegram
        class MockUpdate:
            def __init__(self, chat_id):
                self.effective_chat = MockChat(chat_id)
                self.message = MockMessage()
                self.callback_query = MockCallbackQuery()
        
        class MockChat:
            def __init__(self, chat_id):
                self.id = chat_id
        
        class MockMessage:
            def __init__(self):
                pass
            async def reply_text(self, text):
                print(f"📱 Bot respondería: {text}")
        
        class MockCallbackQuery:
            def __init__(self):
                pass
            async def answer(self):
                pass
            async def edit_message_text(self, text):
                print(f"📱 Bot respondería: {text}")
        
        # Probar con tu chat_id
        mock_update = MockUpdate(Config.ADMIN_CHAT_ID)
        
        print(f"🧪 Simulando comando /start con chat_id: {Config.ADMIN_CHAT_ID}")
        
        # Simular el comando start
        try:
            await AdminHandlers.start_command(mock_update, None)
        except Exception as e:
            print(f"❌ Error en simulación: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando bot: {e}")
        return False

async def main():
    """Función principal"""
    print("🚀 Test de Acceso de Administrador")
    print("=" * 40)
    
    # Probar acceso
    if test_admin_access():
        print("\n✅ Acceso de administrador configurado correctamente")
        
        # Probar bot
        await test_bot_admin()
    else:
        print("\n❌ Problema con el acceso de administrador")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 