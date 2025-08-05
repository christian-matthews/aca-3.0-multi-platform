from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from app.config import Config
from app.bots.handlers.admin_handlers import AdminHandlers
from app.bots.handlers.production_handlers import ProductionHandlers
import logging
import asyncio

logger = logging.getLogger(__name__)

class BotManager:
    """Gestor principal de bots de Telegram"""
    
    def __init__(self):
        self.admin_app = None
        self.production_app = None
    
    async def initialize_bots(self):
        """Inicializar ambos bots"""
        try:
            # Inicializar bot admin
            self.admin_app = Application.builder().token(Config.BOT_ADMIN_TOKEN).build()
            self._setup_admin_handlers()
            
            # Inicializar bot de producción
            self.production_app = Application.builder().token(Config.BOT_PRODUCTION_TOKEN).build()
            self._setup_production_handlers()
            
            logger.info("Bots inicializados correctamente")
            
        except Exception as e:
            logger.error(f"Error inicializando bots: {e}")
            raise
    
    def _setup_admin_handlers(self):
        """Configurar manejadores del bot admin"""
        # Comandos
        self.admin_app.add_handler(CommandHandler("start", AdminHandlers.start_command))
        self.admin_app.add_handler(CommandHandler("crear_empresa", AdminHandlers.crear_empresa_command))
        
        # Callbacks
        self.admin_app.add_handler(CallbackQueryHandler(AdminHandlers.handle_callback))
        
        # Mensajes de texto
        self.admin_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, AdminHandlers.start_command))
    
    def _setup_production_handlers(self):
        """Configurar manejadores del bot de producción"""
        # Comandos
        self.production_app.add_handler(CommandHandler("start", ProductionHandlers.start_command))
        
        # Callbacks
        self.production_app.add_handler(CallbackQueryHandler(ProductionHandlers.handle_callback))
        
        # Mensajes de texto
        self.production_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ProductionHandlers.handle_message))
    
    async def start_bots(self):
        """Iniciar ambos bots"""
        try:
            # Verificar que los bots estén inicializados
            if not self.admin_app or not self.production_app:
                await self.initialize_bots()
            
            # Inicializar y iniciar bot admin
            await self.admin_app.initialize()
            await self.admin_app.start()
            await self.admin_app.updater.start_polling(drop_pending_updates=True)
            
            # Inicializar y iniciar bot de producción
            await self.production_app.initialize()
            await self.production_app.start()
            await self.production_app.updater.start_polling(drop_pending_updates=True)
            
            logger.info("Bots iniciados y escuchando mensajes")
            
        except Exception as e:
            logger.error(f"Error iniciando bots: {e}")
            raise
    
    async def stop_bots(self):
        """Detener ambos bots"""
        try:
            if self.admin_app:
                await self.admin_app.updater.stop()
                await self.admin_app.stop()
                await self.admin_app.shutdown()
            
            if self.production_app:
                await self.production_app.updater.stop()
                await self.production_app.stop()
                await self.production_app.shutdown()
            
            logger.info("Bots detenidos correctamente")
            
        except Exception as e:
            logger.error(f"Error deteniendo bots: {e}")
    
    async def run_bots(self):
        """Ejecutar bots en modo continuo"""
        try:
            await self.initialize_bots()
            await self.start_bots()
            
            # Mantener los bots ejecutándose
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Recibida señal de interrupción, deteniendo bots...")
        except Exception as e:
            logger.error(f"Error ejecutando bots: {e}")
        finally:
            await self.stop_bots()

# Instancia global
bot_manager = BotManager() 