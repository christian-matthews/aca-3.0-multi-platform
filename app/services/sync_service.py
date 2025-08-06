"""
🔄 Servicio de Sincronización ACA 3.0
Sincronización entre Airtable → Supabase
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from .airtable_service import get_airtable_service
from ..database.supabase import get_supabase_client

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SyncService:
    """
    Servicio de sincronización entre Airtable y Supabase
    """
    
    def __init__(self):
        """Inicializar servicio de sincronización"""
        self.airtable = get_airtable_service()
        self.supabase = get_supabase_client()
        
    def sync_from_airtable(self) -> Dict[str, Any]:
        """
        Sincronizar registros desde Airtable hacia Supabase
        
        Returns:
            Resultado de la sincronización
        """
        if not self.airtable.enabled:
            return {
                "success": False,
                "message": "Airtable no está configurado",
                "details": {}
            }
        
        try:
            # Obtener registros pendientes de Airtable
            pending_records = self.airtable.get_pending_records()
            
            if not pending_records:
                return {
                    "success": True,
                    "message": "No hay registros pendientes para sincronizar",
                    "details": {
                        "processed": 0,
                        "failed": 0,
                        "skipped": 0
                    }
                }
            
            results = {
                "processed": 0,
                "failed": 0,
                "skipped": 0,
                "errors": []
            }
            
            logger.info(f"🔄 Iniciando sincronización de {len(pending_records)} registros")
            
            for record in pending_records:
                try:
                    # Validar que el registro tenga empresa
                    empresa_name = record.get('empresa')
                    if not empresa_name:
                        logger.warning(f"⚠️ Registro {record['id']} sin empresa")
                        results["skipped"] += 1
                        continue
                    
                    # Limpiar espacios extra
                    empresa_name = empresa_name.strip() if isinstance(empresa_name, str) else empresa_name
                    
                    # Buscar empresa en Supabase (por RUT o nombre)
                    empresa = self._get_empresa_by_name(empresa_name)
                    if not empresa:
                        logger.warning(f"⚠️ Empresa '{empresa_name}' no encontrada en Supabase")
                        logger.info("💡 Asegúrate de que el RUT coincida o usa formato 'Nombre (RUT)'")
                        results["skipped"] += 1
                        continue
                    
                    # Procesar archivos si existen
                    archivos_info = []
                    archivos = record.get('archivos', [])
                    for archivo in archivos:
                        archivo_info = {
                            'nombre': archivo.get('filename'),
                            'url': archivo.get('url'),
                            'tipo': archivo.get('type'),
                            'tamaño': archivo.get('size'),
                            'airtable_id': archivo.get('id')
                        }
                        archivos_info.append(archivo_info)
                    
                    # Determinar tipo de documento y tabla destino
                    tipo_documento = record.get('tipo_documento', '')
                    if self._is_reporte_mensual(tipo_documento):
                        # Sincronizar como reporte mensual
                        supabase_id = self._sync_reporte_mensual(record, empresa['id'], archivos_info)
                    else:
                        # Sincronizar como información de compañía
                        supabase_id = self._sync_info_compania(record, empresa['id'], archivos_info)
                    
                    if supabase_id:
                        # Marcar como procesado en Airtable
                        self.airtable.mark_as_processed(record['id'], supabase_id)
                        results["processed"] += 1
                        logger.info(f"✅ Registro {record['id']} procesado exitosamente")
                    else:
                        results["failed"] += 1
                        logger.error(f"❌ Error procesando registro {record['id']}")
                
                except Exception as e:
                    results["failed"] += 1
                    error_msg = f"Error procesando registro {record['id']}: {str(e)}"
                    results["errors"].append(error_msg)
                    logger.error(f"❌ {error_msg}")
            
            # Log final
            logger.info(f"🎉 Sincronización completada: {results['processed']} procesados, {results['failed']} fallidos, {results['skipped']} omitidos")
            
            return {
                "success": True,
                "message": f"Sincronización completada: {results['processed']} registros procesados",
                "details": results
            }
            
        except Exception as e:
            error_msg = f"Error en sincronización: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return {
                "success": False,
                "message": error_msg,
                "details": {}
            }
    
    def _get_empresa_by_name(self, nombre: str) -> Optional[Dict[str, Any]]:
        """Buscar empresa por nombre o RUT en Supabase"""
        try:
            # Primero intentar extraer RUT del formato "Nombre (RUT)"
            rut = self._extraer_rut_de_nombre(nombre)
            
            if rut:
                # Buscar por RUT (más confiable)
                response = self.supabase.table('empresas').select('*').eq('rut', rut).execute()
                if response.data:
                    logger.info(f"✅ Empresa encontrada por RUT: {rut}")
                    return response.data[0]
            
            # Si no encuentra por RUT, buscar por nombre exacto
            response = self.supabase.table('empresas').select('*').eq('nombre', nombre).execute()
            if response.data:
                logger.info(f"✅ Empresa encontrada por nombre: {nombre}")
                return response.data[0]
                
            logger.warning(f"⚠️ Empresa no encontrada: {nombre}")
            return None
        except Exception as e:
            logger.error(f"Error buscando empresa {nombre}: {e}")
            return None
    
    def _extraer_rut_de_nombre(self, nombre: str) -> Optional[str]:
        """Extraer RUT del formato 'Nombre (RUT)' o devolver RUT directo"""
        import re
        
        # Patrón para RUT chileno: 12345678-9 o 12.345.678-9
        patron_rut = r'(\d{1,2}\.?\d{3}\.?\d{3}-[0-9kK])'
        
        # Buscar RUT en el texto
        match = re.search(patron_rut, nombre)
        if match:
            rut = match.group(1)
            # Normalizar RUT (quitar puntos)
            rut_normalizado = rut.replace('.', '')
            logger.info(f"🔍 RUT extraído: {rut_normalizado} de '{nombre}'")
            return rut_normalizado
        
        # Si no hay RUT en paréntesis, verificar si el nombre completo es un RUT
        if re.match(r'^\d{1,2}\.?\d{3}\.?\d{3}-[0-9kK]$', nombre.strip()):
            return nombre.replace('.', '')
        
        return None
    
    def _is_reporte_mensual(self, tipo_documento: str) -> bool:
        """Determinar si es un reporte mensual"""
        tipos_reporte = ['balance', 'resultados', 'flujo de caja', 'estados financieros']
        return any(tipo.lower() in tipo_documento.lower() for tipo in tipos_reporte)
    
    def _sync_reporte_mensual(self, record: Dict[str, Any], empresa_id: str, archivos: List[Dict]) -> Optional[str]:
        """Sincronizar como reporte mensual"""
        try:
            # Verificar si ya existe un reporte con este ID de Airtable
            airtable_id = record['id']
            existing_check = self.supabase.table('reportes_mensuales').select('id').like('comentarios', f'%{airtable_id}%').execute()
            
            if existing_check.data:
                logger.info(f"📋 Reporte {airtable_id} ya existe en Supabase, omitiendo...")
                return existing_check.data[0]['id']
            
            # Determinar año y mes actual si no se especifica
            fecha_actual = datetime.now()
            anio = fecha_actual.year
            mes = fecha_actual.month
            
            # Crear registro en reportes_mensuales
            reporte_data = {
                'empresa_id': empresa_id,
                'anio': anio,
                'mes': mes,
                'tipo_reporte': self._get_categoria_from_tipo(record.get('tipo_documento', '')),
                'titulo': record.get('tipo_documento', 'Documento'),
                'descripcion': record.get('comentarios', ''),
                'comentarios': f"Sincronizado desde Airtable ID: {airtable_id}",
                'estado': 'activo'
            }
            
            response = self.supabase.table('reportes_mensuales').insert(reporte_data).execute()
            if not response.data:
                return None
            
            reporte_id = response.data[0]['id']
            
            # Crear registros de archivos (solo si no existen)
            for archivo in archivos:
                # Verificar si el archivo ya existe
                existing_file = self.supabase.table('archivos_reportes').select('id').like('descripcion', f"%{archivo['airtable_id']}%").execute()
                
                if existing_file.data:
                    logger.info(f"📎 Archivo {archivo['nombre']} ya existe, omitiendo...")
                    continue
                
                archivo_data = {
                    'reporte_id': reporte_id,
                    'empresa_id': empresa_id,
                    'nombre_archivo': archivo['nombre'],
                    'url_archivo': archivo['url'],
                    'tipo_archivo': archivo['tipo'],
                    'tamanio_bytes': archivo['tamaño'],
                    'descripcion': f"Archivo de Airtable ID: {archivo['airtable_id']}",
                    'activo': True
                }
                
                self.supabase.table('archivos_reportes').insert(archivo_data).execute()
                logger.info(f"📎 Archivo {archivo['nombre']} sincronizado exitosamente")
            
            return reporte_id
            
        except Exception as e:
            logger.error(f"Error sincronizando reporte mensual: {e}")
            return None
    
    def _sync_info_compania(self, record: Dict[str, Any], empresa_id: str, archivos: List[Dict]) -> Optional[str]:
        """Sincronizar como información de compañía"""
        try:
            # Verificar si ya existe información con este ID de Airtable
            airtable_id = record['id']
            existing_check = self.supabase.table('info_compania').select('id').like('comentarios', f'%{airtable_id}%').execute()
            
            if existing_check.data:
                logger.info(f"📋 Info compañía {airtable_id} ya existe en Supabase, omitiendo...")
                return existing_check.data[0]['id']
            
            # Crear registro en info_compania
            info_data = {
                'empresa_id': empresa_id,
                'categoria': self._get_categoria_from_tipo(record.get('tipo_documento', '')),
                'titulo': record.get('tipo_documento', 'Documento'),
                'descripcion': record.get('comentarios', ''),
                'comentarios': f"Sincronizado desde Airtable ID: {airtable_id}",
                'estado': 'activo'
            }
            
            response = self.supabase.table('info_compania').insert(info_data).execute()
            if not response.data:
                return None
            
            info_id = response.data[0]['id']
            
            # Crear registros de archivos (solo si no existen)
            for archivo in archivos:
                # Verificar si el archivo ya existe
                existing_file = self.supabase.table('archivos_info_compania').select('id').like('descripcion', f"%{archivo['airtable_id']}%").execute()
                
                if existing_file.data:
                    logger.info(f"📎 Archivo {archivo['nombre']} ya existe, omitiendo...")
                    continue
                
                archivo_data = {
                    'info_id': info_id,
                    'empresa_id': empresa_id,
                    'nombre_archivo': archivo['nombre'],
                    'url_archivo': archivo['url'],
                    'tipo_archivo': archivo['tipo'],
                    'tamanio_bytes': archivo['tamaño'],
                    'descripcion': f"Archivo de Airtable ID: {archivo['airtable_id']}"
                }
                
                self.supabase.table('archivos_info_compania').insert(archivo_data).execute()
                logger.info(f"📎 Archivo {archivo['nombre']} sincronizado exitosamente")
            
            return info_id
            
        except Exception as e:
            logger.error(f"Error sincronizando info compañía: {e}")
            return None
    
    def _get_categoria_from_tipo(self, tipo_documento: str) -> str:
        """Determinar categoría específica basada en tipo de documento"""
        tipo_lower = tipo_documento.lower().strip()
        
        # Mapeo específico para evitar duplicados
        if 'balance general' in tipo_lower:
            return 'Balance General'
        elif 'estado de resultados' in tipo_lower:
            return 'Estado de Resultados' 
        elif 'flujo de caja' in tipo_lower:
            return 'Flujo de Caja'
        elif 'estado de situación' in tipo_lower:
            return 'Estado de Situación'
        elif 'balance' in tipo_lower:
            return 'Balance'
        elif 'resultados' in tipo_lower:
            return 'Resultados'
        elif 'flujo' in tipo_lower:
            return 'Flujo'
        elif any(word in tipo_lower for word in ['legal', 'contrato', 'escritura', 'registro']):
            return 'Legal'
        elif any(word in tipo_lower for word in ['tributario', 'impuesto', 'declaracion', 'renta']):
            return 'Tributaria'
        elif any(word in tipo_lower for word in ['carpeta', 'tributaria']):
            return 'Carpeta Tributaria'
        else:
            # Usar el tipo original si no coincide con ninguno
            return tipo_documento.strip() or 'General'
    
    def get_sync_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas de sincronización"""
        try:
            airtable_stats = self.airtable.get_statistics()
            
            # Contar registros en Supabase
            reportes_response = self.supabase.table('reportes_mensuales').select('*', count='exact').execute()
            info_response = self.supabase.table('info_compania').select('*', count='exact').execute()
            archivos_reportes_response = self.supabase.table('archivos_reportes').select('*', count='exact').execute()
            archivos_info_response = self.supabase.table('archivos_info_compania').select('*', count='exact').execute()
            
            return {
                "airtable": airtable_stats,
                "supabase": {
                    "reportes_mensuales": reportes_response.count if hasattr(reportes_response, 'count') else len(reportes_response.data),
                    "info_compania": info_response.count if hasattr(info_response, 'count') else len(info_response.data),
                    "archivos_reportes": archivos_reportes_response.count if hasattr(archivos_reportes_response, 'count') else len(archivos_reportes_response.data),
                    "archivos_info_compania": archivos_info_response.count if hasattr(archivos_info_response, 'count') else len(archivos_info_response.data)
                },
                "last_sync": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {"error": str(e)}

# Instancia global del servicio
sync_service = SyncService()

def get_sync_service() -> SyncService:
    """Obtener instancia del servicio de sincronización"""
    return sync_service