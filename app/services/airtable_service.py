"""
🗂️ Servicio de Airtable para ACA 3.0
Gestión documental integrada con Supabase
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pyairtable import Api
try:
    from pyairtable.exceptions import AirtableError
except ImportError:
    # Fallback si la clase no existe en esta versión
    class AirtableError(Exception):
        pass

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AirtableService:
    """
    Servicio para integración con Airtable
    Permite sincronización de documentos entre Airtable y Supabase
    """
    
    def __init__(self):
        """Inicializar servicio de Airtable"""
        from dotenv import load_dotenv
        load_dotenv()  # Asegurar que se cargan las variables
        
        self.api_key = os.getenv('AIRTABLE_API_KEY')
        self.base_id = os.getenv('AIRTABLE_BASE_ID')
        self.table_name = os.getenv('AIRTABLE_TABLE_NAME', 'ACA - Gestión Documental')
        self.view_name = os.getenv('AIRTABLE_VIEW_NAME', 'Grid view')
        
        # Debug: imprimir valores para verificar
        logger.info(f"🔍 Debug Airtable - API Key: {'✅ Configurado' if self.api_key else '❌ Faltante'}")
        logger.info(f"🔍 Debug Airtable - Base ID: {'✅ Configurado' if self.base_id else '❌ Faltante'}")
        logger.info(f"🔍 Debug Airtable - Table Name: {self.table_name}")
        
        if not self.api_key or not self.base_id:
            logger.warning("⚠️ Variables de Airtable no configuradas")
            self.enabled = False
            return
            
        try:
            self.api = Api(self.api_key)
            self.table = self.api.table(self.base_id, self.table_name)
            self.enabled = True
            logger.info("✅ Airtable configurado correctamente")
        except Exception as e:
            logger.error(f"❌ Error configurando Airtable: {e}")
            self.enabled = False
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Probar conexión con Airtable
        
        Returns:
            Dict con información de la conexión
        """
        if not self.enabled:
            return {
                "success": False,
                "message": "Airtable no está configurado",
                "configured": False
            }
        
        try:
            # Intentar obtener información de la tabla
            records = self.table.all(max_records=1)
            
            return {
                "success": True,
                "message": "Conexión exitosa con Airtable",
                "base_id": self.base_id,
                "table_name": self.table_name,
                "configured": True,
                "sample_records": len(records)
            }
        except AirtableError as e:
            logger.error(f"❌ Error de Airtable: {e}")
            return {
                "success": False,
                "message": f"Error de Airtable: {str(e)}",
                "configured": True
            }
        except Exception as e:
            logger.error(f"❌ Error general: {e}")
            return {
                "success": False,
                "message": f"Error general: {str(e)}",
                "configured": True
            }
    
    def get_all_records(self, empresa_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtener todos los registros de Airtable
        
        Args:
            empresa_filter: Filtrar por empresa específica
            
        Returns:
            Lista de registros
        """
        if not self.enabled:
            logger.warning("Airtable no está habilitado")
            return []
        
        try:
            if empresa_filter:
                # Filtrar por empresa
                formula = f"{{Empresa}} = '{empresa_filter}'"
                records = self.table.all(formula=formula)
            else:
                records = self.table.all()
            
            # Procesar registros para formato consistente
            processed_records = []
            for record in records:
                processed_record = {
                    'id': record['id'],
                    'fields': record['fields'],
                    'created_time': record.get('createdTime'),
                    'empresa': record['fields'].get('Empresa'),
                    'fecha_subida': record['fields'].get('Fecha subida'),
                    'tipo_documento': record['fields'].get('Tipo documento'),
                    'archivos': record['fields'].get('Archivo adjunto', []),
                    'estado': record['fields'].get('Estado subida', 'Pendiente'),
                    'comentarios': record['fields'].get('Comentarios', '')
                }
                processed_records.append(processed_record)
            
            logger.info(f"📊 Obtenidos {len(processed_records)} registros de Airtable")
            return processed_records
            
        except AirtableError as e:
            logger.error(f"❌ Error obteniendo registros: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Error general: {e}")
            return []
    
    def create_record(self, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Crear un nuevo registro en Airtable
        
        Args:
            fields: Campos del registro
            
        Returns:
            Registro creado o None si hay error
        """
        if not self.enabled:
            logger.warning("Airtable no está habilitado")
            return None
        
        try:
            # Agregar timestamp si no existe
            if 'Fecha subida' not in fields:
                fields['Fecha subida'] = datetime.now().isoformat()
            
            # Estado por defecto
            if 'Estado subida' not in fields:
                fields['Estado subida'] = 'Pendiente'
            
            record = self.table.create(fields)
            logger.info(f"✅ Registro creado en Airtable: {record['id']}")
            return record
            
        except AirtableError as e:
            logger.error(f"❌ Error creando registro: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error general: {e}")
            return None
    
    def update_record(self, record_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Actualizar un registro existente
        
        Args:
            record_id: ID del registro
            fields: Campos a actualizar
            
        Returns:
            Registro actualizado o None si hay error
        """
        if not self.enabled:
            logger.warning("Airtable no está habilitado")
            return None
        
        try:
            record = self.table.update(record_id, fields)
            logger.info(f"✅ Registro actualizado: {record_id}")
            return record
            
        except AirtableError as e:
            logger.error(f"❌ Error actualizando registro: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error general: {e}")
            return None
    
    def mark_as_processed(self, record_id: str, supabase_id: Optional[str] = None) -> bool:
        """
        Marcar registro como procesado
        
        Args:
            record_id: ID del registro en Airtable
            supabase_id: ID en Supabase para referencia
            
        Returns:
            True si se actualizó correctamente
        """
        # Formato de fecha compatible con Airtable (YYYY-MM-DD)
        fecha_procesado = datetime.now().strftime('%Y-%m-%d')
        
        fields = {
            'Estado subida': 'Procesado',
            'Fecha procesado': fecha_procesado
        }
        
        if supabase_id:
            fields['Supabase ID'] = supabase_id
        
        result = self.update_record(record_id, fields)
        return result is not None
    
    def get_pending_records(self) -> List[Dict[str, Any]]:
        """
        Obtener registros pendientes de procesar
        
        Returns:
            Lista de registros pendientes
        """
        if not self.enabled:
            return []
        
        try:
            # Filtrar por estado pendiente
            formula = "OR({Estado subida} = 'Pendiente', {Estado subida} = '')"
            records = self.table.all(formula=formula)
            
            processed_records = []
            for record in records:
                processed_record = {
                    'id': record['id'],
                    'fields': record['fields'],
                    'empresa': record['fields'].get('Empresa'),
                    'tipo_documento': record['fields'].get('Tipo documento'),
                    'archivos': record['fields'].get('Archivo adjunto', []),
                    'comentarios': record['fields'].get('Comentarios', '')
                }
                processed_records.append(processed_record)
            
            logger.info(f"📋 Encontrados {len(processed_records)} registros pendientes")
            return processed_records
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo registros pendientes: {e}")
            return []
    
    def get_records_by_empresa(self, empresa_name: str) -> List[Dict[str, Any]]:
        """
        Obtener registros de una empresa específica
        
        Args:
            empresa_name: Nombre de la empresa
            
        Returns:
            Lista de registros de la empresa
        """
        return self.get_all_records(empresa_filter=empresa_name)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de Airtable
        
        Returns:
            Diccionario con estadísticas
        """
        if not self.enabled:
            return {"enabled": False}
        
        try:
            all_records = self.get_all_records()
            pending_records = self.get_pending_records()
            
            # Contar por empresa
            empresas = {}
            for record in all_records:
                empresa = record.get('empresa', 'Sin empresa')
                empresas[empresa] = empresas.get(empresa, 0) + 1
            
            # Contar por tipo
            tipos = {}
            for record in all_records:
                tipo = record.get('tipo_documento', 'Sin tipo')
                tipos[tipo] = tipos.get(tipo, 0) + 1
            
            return {
                "enabled": True,
                "total_records": len(all_records),
                "pending_records": len(pending_records),
                "processed_records": len(all_records) - len(pending_records),
                "by_empresa": empresas,
                "by_tipo": tipos,
                "base_id": self.base_id,
                "table_name": self.table_name
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas: {e}")
            return {"enabled": True, "error": str(e)}

# Instancia global del servicio
airtable_service = AirtableService()

def get_airtable_service() -> AirtableService:
    """Obtener instancia del servicio de Airtable"""
    return airtable_service