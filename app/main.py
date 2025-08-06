from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

from app.config import Config
from app.bots.bot_manager import bot_manager
from app.utils.helpers import setup_logging
from app.services.airtable_service import get_airtable_service
from app.services.sync_service import get_sync_service
from app.database.supabase import get_supabase_client

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="ACA 3.0 - Sistema de Gestión Contable",
    description="API para gestionar bots de Telegram con integración a Supabase y Airtable",
    version="3.0.0"
)

# Configurar plantillas y archivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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

# Endpoints de Airtable
@app.get("/airtable/status")
async def airtable_status():
    """Verificar estado de Airtable"""
    try:
        airtable_service = get_airtable_service()
        status = airtable_service.test_connection()
        return status
    except Exception as e:
        logger.error(f"Error verificando Airtable: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/airtable/records")
async def get_airtable_records(empresa: str = None):
    """Obtener registros de Airtable"""
    try:
        airtable_service = get_airtable_service()
        if empresa:
            records = airtable_service.get_records_by_empresa(empresa)
        else:
            records = airtable_service.get_all_records()
        return {"records": records, "count": len(records)}
    except Exception as e:
        logger.error(f"Error obteniendo registros: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/airtable/pending")
async def get_pending_records():
    """Obtener registros pendientes de procesar"""
    try:
        airtable_service = get_airtable_service()
        records = airtable_service.get_pending_records()
        return {"pending_records": records, "count": len(records)}
    except Exception as e:
        logger.error(f"Error obteniendo pendientes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/airtable/statistics")
async def get_airtable_statistics():
    """Obtener estadísticas de Airtable"""
    try:
        airtable_service = get_airtable_service()
        stats = airtable_service.get_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints de Sincronización
@app.post("/sync/airtable")
async def sync_from_airtable():
    """Sincronizar registros desde Airtable a Supabase"""
    try:
        sync_service = get_sync_service()
        result = sync_service.sync_from_airtable()
        return result
    except Exception as e:
        logger.error(f"Error en sincronización: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sync/statistics")
async def get_sync_statistics():
    """Obtener estadísticas de sincronización"""
    try:
        sync_service = get_sync_service()
        stats = sync_service.get_sync_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas de sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===================== DASHBOARD WEB ENDPOINTS =====================

async def get_dashboard_data() -> Dict[str, Any]:
    """Obtener todos los datos necesarios para el dashboard"""
    try:
        supabase = get_supabase_client()
        airtable = get_airtable_service()
        sync_service = get_sync_service()
        
        # Obtener estadísticas básicas
        empresas = supabase.table('empresas').select('id').execute()
        reportes = supabase.table('reportes_mensuales').select('id').execute()
        archivos = supabase.table('archivos_reportes').select('id').execute()
        
        # Estadísticas de Airtable
        airtable_stats = airtable.get_statistics() if airtable.enabled else {"total_records": 0}
        
        # Estado de sincronización
        sync_stats = sync_service.get_sync_statistics()
        
        # Datos para gráfico de reportes por tipo
        reportes_data = supabase.table('reportes_mensuales').select('tipo_reporte').execute()
        reportes_por_tipo = {}
        for reporte in reportes_data.data:
            tipo = reporte['tipo_reporte'] or 'Sin categoría'
            reportes_por_tipo[tipo] = reportes_por_tipo.get(tipo, 0) + 1
        
        # Actividad reciente (últimos reportes)
        reportes_recientes = supabase.table('reportes_mensuales').select('*').order('creado_en', desc=True).limit(5).execute()
        recent_activity = []
        for reporte in reportes_recientes.data:
            recent_activity.append({
                'title': reporte['titulo'] or 'Reporte sin título',
                'description': f"Tipo: {reporte['tipo_reporte']} - Empresa: {reporte['empresa_id'][:8]}...",
                'time': reporte['creado_en'][:10] if reporte['creado_en'] else 'Fecha desconocida',
                'icon': 'file-alt',
                'color': 'primary'
            })
        
        return {
            'stats': {
                'empresas': len(empresas.data),
                'reportes': len(reportes.data),
                'archivos': len(archivos.data),
                'airtable': airtable_stats.get('total_records', 0)
            },
            'sync_status': {
                'success': sync_stats.get('success', False),
                'processed': sync_stats.get('supabase', {}).get('reportes_mensuales', 0),
                'failed': 0,  # Placeholder
                'last_sync': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            'system_status': {
                'healthy': True,
                'supabase': True,
                'airtable': airtable.enabled,
                'telegram': True,  # Placeholder
                'api': True
            },
            'reportes_chart_data': {
                'labels': list(reportes_por_tipo.keys()),
                'data': list(reportes_por_tipo.values())
            },
            'recent_activity': recent_activity
        }
    except Exception as e:
        logger.error(f"Error obteniendo datos del dashboard: {e}")
        return {
            'stats': {'empresas': 0, 'reportes': 0, 'archivos': 0, 'airtable': 0},
            'sync_status': {'success': False, 'processed': 0, 'failed': 0, 'last_sync': 'Error'},
            'system_status': {'healthy': False, 'supabase': False, 'airtable': False, 'telegram': False, 'api': True},
            'reportes_chart_data': {'labels': [], 'data': []},
            'recent_activity': []
        }

@app.get("/", response_class=HTMLResponse)
async def redirect_to_dashboard():
    """Redirigir la raíz al dashboard"""
    return """
    <html>
        <head>
            <meta http-equiv="refresh" content="0; url=/dashboard">
        </head>
        <body>
            <p>Redirigiendo al dashboard...</p>
        </body>
    </html>
    """

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_main(request: Request):
    """Dashboard principal"""
    try:
        data = await get_dashboard_data()
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            **data
        })
    except Exception as e:
        logger.error(f"Error en dashboard principal: {e}")
        raise HTTPException(status_code=500, detail="Error cargando el dashboard")

@app.get("/dashboard/empresas", response_class=HTMLResponse)
async def dashboard_empresas(request: Request):
    """Vista de empresas"""
    try:
        supabase = get_supabase_client()
        empresas = supabase.table('empresas').select('*').execute()
        
        return templates.TemplateResponse("empresas.html", {
            "request": request,
            "empresas": empresas.data
        })
    except Exception as e:
        logger.error(f"Error en dashboard de empresas: {e}")
        raise HTTPException(status_code=500, detail="Error cargando empresas")

@app.get("/dashboard/reportes", response_class=HTMLResponse)
async def dashboard_reportes(request: Request):
    """Vista de reportes"""
    try:
        supabase = get_supabase_client()
        reportes = supabase.table('reportes_mensuales').select('*').order('creado_en', desc=True).execute()
        
        return templates.TemplateResponse("reportes.html", {
            "request": request,
            "reportes": reportes.data
        })
    except Exception as e:
        logger.error(f"Error en dashboard de reportes: {e}")
        raise HTTPException(status_code=500, detail="Error cargando reportes")

@app.get("/dashboard/archivos", response_class=HTMLResponse) 
async def dashboard_archivos(request: Request):
    """Vista de archivos"""
    try:
        supabase = get_supabase_client()
        archivos = supabase.table('archivos_reportes').select('*').order('created_at', desc=True).execute()
        
        return templates.TemplateResponse("archivos.html", {
            "request": request,
            "archivos": archivos.data
        })
    except Exception as e:
        logger.error(f"Error en dashboard de archivos: {e}")
        raise HTTPException(status_code=500, detail="Error cargando archivos")

@app.get("/dashboard/airtable", response_class=HTMLResponse)
async def dashboard_airtable(request: Request):
    """Vista de Airtable"""
    try:
        airtable = get_airtable_service()
        records = airtable.get_all_records() if airtable.enabled else []
        stats = airtable.get_statistics() if airtable.enabled else {}
        
        return templates.TemplateResponse("airtable.html", {
            "request": request,
            "records": records,
            "stats": stats,
            "enabled": airtable.enabled
        })
    except Exception as e:
        logger.error(f"Error en dashboard de Airtable: {e}")
        raise HTTPException(status_code=500, detail="Error cargando Airtable")

@app.get("/dashboard/sync", response_class=HTMLResponse)
async def dashboard_sync(request: Request):
    """Vista de sincronización"""
    try:
        sync_service = get_sync_service()
        stats = sync_service.get_sync_statistics()
        
        return templates.TemplateResponse("sync.html", {
            "request": request,
            "stats": stats
        })
    except Exception as e:
        logger.error(f"Error en dashboard de sincronización: {e}")
        raise HTTPException(status_code=500, detail="Error cargando sincronización")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=Config.DEBUG
    ) 