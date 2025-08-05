from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import logging

from app.config import Config
from app.bots.bot_manager import bot_manager
from app.utils.helpers import setup_logging

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="ACA 3.0 - Sistema de Bots de Telegram",
    description="API para gestionar bots de Telegram con integración a Supabase",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    try:
        # Validar configuración
        Config.validate()
        logger.info("Configuración validada correctamente")
        
        # Inicializar bots
        await bot_manager.initialize_bots()
        logger.info("Bots inicializados correctamente")
        
        # Iniciar bots automáticamente
        await bot_manager.start_bots()
        logger.info("Bots iniciados y escuchando mensajes")
        
    except Exception as e:
        logger.error(f"Error en startup: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre de la aplicación"""
    try:
        await bot_manager.stop_bots()
        logger.info("Aplicación cerrada correctamente")
    except Exception as e:
        logger.error(f"Error en shutdown: {e}")

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "ACA 3.0 - Sistema de Bots de Telegram",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "bots": {
            "admin": "running" if bot_manager.admin_app and bot_manager.admin_app.updater.running else "initialized",
            "production": "running" if bot_manager.production_app and bot_manager.production_app.updater.running else "initialized"
        }
    }

@app.post("/start-bots")
async def start_bots():
    """Iniciar bots manualmente"""
    try:
        await bot_manager.start_bots()
        return {"message": "Bots iniciados correctamente"}
    except Exception as e:
        logger.error(f"Error iniciando bots: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop-bots")
async def stop_bots():
    """Detener bots manualmente"""
    try:
        await bot_manager.stop_bots()
        return {"message": "Bots detenidos correctamente"}
    except Exception as e:
        logger.error(f"Error deteniendo bots: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    """Obtener estado de los bots"""
    try:
        return {
            "admin_bot": "running" if bot_manager.admin_app else "stopped",
            "production_bot": "running" if bot_manager.production_app else "stopped",
            "config": {
                "environment": Config.ENVIRONMENT,
                "debug": Config.DEBUG
            }
        }
    except Exception as e:
        logger.error(f"Error obteniendo estado: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=Config.DEBUG
    ) 