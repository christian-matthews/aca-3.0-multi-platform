import httpx
from app.config import Config
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class CalendlyService:
    """Servicio para interactuar con Calendly API"""
    
    def __init__(self):
        self.api_key = Config.CALENDLY_API_KEY
        self.base_url = "https://api.calendly.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def get_user_info(self) -> Dict:
        """Obtener información del usuario de Calendly"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/users/me",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error obteniendo información de usuario: {e}")
            return {}
    
    async def get_scheduling_links(self) -> List[Dict]:
        """Obtener enlaces de programación disponibles"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/scheduling_links",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json().get("collection", [])
        except Exception as e:
            logger.error(f"Error obteniendo enlaces de programación: {e}")
            return []
    
    async def create_scheduling_link(self, name: str, event_type_uri: str) -> Dict:
        """Crear un nuevo enlace de programación"""
        try:
            data = {
                "name": name,
                "event_type": event_type_uri,
                "max_event_count": 1
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/scheduling_links",
                    headers=self.headers,
                    json=data
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error creando enlace de programación: {e}")
            return {}
    
    async def get_event_types(self) -> List[Dict]:
        """Obtener tipos de eventos disponibles"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/event_types",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json().get("collection", [])
        except Exception as e:
            logger.error(f"Error obteniendo tipos de eventos: {e}")
            return []
    
    async def get_scheduled_events(self, start_time: datetime = None, end_time: datetime = None) -> List[Dict]:
        """Obtener eventos programados"""
        try:
            params = {}
            if start_time:
                params["min_start_time"] = start_time.isoformat()
            if end_time:
                params["max_start_time"] = end_time.isoformat()
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/scheduled_events",
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                return response.json().get("collection", [])
        except Exception as e:
            logger.error(f"Error obteniendo eventos programados: {e}")
            return []
    
    async def cancel_event(self, event_uri: str, reason: str = "") -> bool:
        """Cancelar un evento programado"""
        try:
            data = {"reason": reason} if reason else {}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{event_uri}/cancellation",
                    headers=self.headers,
                    json=data
                )
                response.raise_for_status()
                return True
        except Exception as e:
            logger.error(f"Error cancelando evento: {e}")
            return False
    
    async def get_webhook_subscriptions(self) -> List[Dict]:
        """Obtener suscripciones de webhook"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/webhook_subscriptions",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json().get("collection", [])
        except Exception as e:
            logger.error(f"Error obteniendo webhooks: {e}")
            return []
    
    async def create_webhook_subscription(self, url: str, events: List[str]) -> Dict:
        """Crear suscripción de webhook"""
        try:
            data = {
                "url": url,
                "events": events,
                "scope": "user"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/webhook_subscriptions",
                    headers=self.headers,
                    json=data
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error creando webhook: {e}")
            return {}

# Instancia global
calendly_service = CalendlyService() 