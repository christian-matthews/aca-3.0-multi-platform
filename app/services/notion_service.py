import requests
import json
from typing import Dict, List, Optional
from app.config import Config
import logging

logger = logging.getLogger(__name__)

class NotionService:
    """Servicio para integración con Notion API"""
    
    def __init__(self):
        self.token = Config.NOTION_TOKEN
        self.database_id = Config.NOTION_DATABASE_ID
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def test_connection(self) -> bool:
        """Probar conexión con Notion"""
        try:
            url = f"{self.base_url}/databases/{self.database_id}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                logger.info("✅ Conexión exitosa con Notion")
                return True
            else:
                logger.error(f"❌ Error conectando con Notion: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en conexión Notion: {e}")
            return False
    
    def add_empresa_row(self, empresa_data: Dict) -> bool:
        """Agregar una fila de empresa al database"""
        try:
            url = f"{self.base_url}/pages"
            
            data = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "Id_empresa": {
                        "rich_text": [{"text": {"content": empresa_data.get("id", "")}}]
                    },
                    "Empresa": {
                        "title": [{"text": {"content": empresa_data.get("nombre", "Sin nombre")}}]
                    },
                    "RUT": {
                        "rich_text": [{"text": {"content": empresa_data.get("rut", "")}}]
                    },
                    "Reportes": {
                        "number": empresa_data.get("reportes_count", 0)
                    },
                    "Último Reporte": {
                        "date": {"start": empresa_data.get("ultimo_reporte")} if empresa_data.get("ultimo_reporte") else None
                    },
                    "Estado": {
                        "select": {"name": "Activo" if empresa_data.get("activo") else "Inactivo"}
                    }
                }
            }
            
            response = requests.post(url, headers=self.headers, data=json.dumps(data))
            
            if response.status_code == 200:
                logger.info(f"✅ Empresa agregada a Notion: {empresa_data.get('nombre')}")
                return True
            else:
                logger.error(f"❌ Error agregando empresa: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error agregando empresa a Notion: {e}")
            return False
    
    def clear_database(self) -> bool:
        """Limpiar todas las filas del database"""
        try:
            # Obtener todas las páginas
            url = f"{self.base_url}/databases/{self.database_id}/query"
            response = requests.post(url, headers=self.headers)
            
            if response.status_code != 200:
                logger.error(f"❌ Error obteniendo páginas: {response.status_code}")
                return False
            
            pages = response.json().get("results", [])
            
            # Eliminar cada página
            for page in pages:
                page_id = page["id"]
                delete_url = f"{self.base_url}/pages/{page_id}"
                delete_data = {"archived": True}
                
                delete_response = requests.patch(
                    delete_url, 
                    headers=self.headers, 
                    data=json.dumps(delete_data)
                )
                
                if delete_response.status_code != 200:
                    logger.warning(f"⚠️ Error eliminando página {page_id}")
            
            logger.info("✅ Database limpiado")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error limpiando database: {e}")
            return False