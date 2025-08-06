from supabase import create_client, Client
from app.config import Config
import logging

logger = logging.getLogger(__name__)

class SupabaseManager:
    _instance = None
    _client: Client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    
    @property
    def client(self) -> Client:
        return self._client
    
    def table(self, table_name: str):
        """Acceso directo a tablas"""
        return self._client.table(table_name)
    
    def get_user_by_chat_id(self, chat_id: int):
        """Obtener usuario por chat_id con validación de seguridad"""
        try:
            response = self._client.table('usuarios').select('*').eq('chat_id', chat_id).eq('activo', True).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error obteniendo usuario por chat_id {chat_id}: {e}")
            return None
    
    def log_conversation(self, chat_id: int, empresa_id: int, mensaje: str, respuesta: str, tipo: str = "user"):
        """Registrar conversación en la base de datos"""
        try:
            data = {
                'chat_id': chat_id,
                'empresa_id': empresa_id,
                'mensaje': mensaje,
                'respuesta': respuesta,
                'tipo': tipo
            }
            self._client.table('conversaciones').insert(data).execute()
        except Exception as e:
            logger.error(f"Error registrando conversación: {e}")
    
    def get_empresa_data(self, empresa_id: int, table_name: str):
        """Obtener datos de una empresa específica con validación de seguridad"""
        try:
            response = self._client.table(table_name).select('*').eq('empresa_id', empresa_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error obteniendo datos de {table_name} para empresa {empresa_id}: {e}")
            return []
    
    def create_empresa(self, rut: str, nombre: str, admin_chat_id: int):
        """Crear nueva empresa desde el bot admin"""
        try:
            # Crear empresa
            empresa_data = {
                'rut': rut,
                'nombre': nombre,
                'activo': True
            }
            empresa_response = self._client.table('empresas').insert(empresa_data).execute()
            
            if empresa_response.data:
                empresa_id = empresa_response.data[0]['id']
                
                # Crear usuario admin para la empresa
                usuario_data = {
                    'chat_id': admin_chat_id,
                    'empresa_id': empresa_id,
                    'nombre': 'Administrador',
                    'rol': 'admin',
                    'activo': True
                }
                self._client.table('usuarios').insert(usuario_data).execute()
                
                return empresa_id
            return None
        except Exception as e:
            logger.error(f"Error creando empresa: {e}")
            return None

    def get_reportes_mensuales(self, empresa_id, anio=None, mes=None):
        """Obtener reportes mensuales de una empresa"""
        try:
            query = self._client.table('reportes_mensuales').select('*').eq('empresa_id', empresa_id)
            
            if anio:
                query = query.eq('anio', anio)
            if mes:
                query = query.eq('mes', mes)
            
            result = query.order('anio', desc=True).order('mes', desc=True).execute()
            return result.data
        except Exception as e:
            logger.error(f"Error obteniendo reportes mensuales: {e}")
            return []
    
    def get_archivos_reporte(self, reporte_id):
        """Obtener archivos adjuntos de un reporte"""
        try:
            result = self._client.table('archivos_reportes').select('*').eq('reporte_id', reporte_id).execute()
            return result.data
        except Exception as e:
            logger.error(f"Error obteniendo archivos del reporte: {e}")
            return []
    
    def get_comentarios_reporte(self, reporte_id):
        """Obtener comentarios de un reporte"""
        try:
            result = self._client.table('comentarios_reportes').select('*').eq('reporte_id', reporte_id).execute()
            return result.data
        except Exception as e:
            logger.error(f"Error obteniendo comentarios del reporte: {e}")
            return []
    
    def get_info_compania(self, empresa_id, categoria=None):
        """Obtener información de compañía por categoría"""
        try:
            query = self._client.table('info_compania').select('*').eq('empresa_id', empresa_id).eq('estado', 'activo')
            
            if categoria:
                query = query.eq('categoria', categoria)
            
            result = query.execute()
            return result.data
        except Exception as e:
            logger.error(f"Error obteniendo información de compañía: {e}")
            return []
    
    def get_archivos_info_compania(self, info_id):
        """Obtener archivos adjuntos de información de compañía"""
        try:
            result = self._client.table('archivos_info_compania').select('*').eq('info_id', info_id).execute()
            return result.data
        except Exception as e:
            logger.error(f"Error obteniendo archivos de información: {e}")
            return []
    
    def crear_reporte_mensual(self, empresa_id, anio, mes, tipo_reporte, titulo, descripcion=None, comentarios=None):
        """Crear un nuevo reporte mensual"""
        try:
            data = {
                'empresa_id': empresa_id,
                'anio': anio,
                'mes': mes,
                'tipo_reporte': tipo_reporte,
                'titulo': titulo,
                'descripcion': descripcion,
                'comentarios': comentarios,
                'estado': 'borrador'
            }
            
            result = self._client.table('reportes_mensuales').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error creando reporte mensual: {e}")
            return None
    
    def agregar_archivo_reporte(self, reporte_id, nombre_archivo, tipo_archivo, url_archivo, descripcion=None):
        """Agregar archivo adjunto a un reporte"""
        try:
            data = {
                'reporte_id': reporte_id,
                'nombre_archivo': nombre_archivo,
                'tipo_archivo': tipo_archivo,
                'url_archivo': url_archivo,
                'descripcion': descripcion
            }
            
            result = self._client.table('archivos_reportes').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error agregando archivo al reporte: {e}")
            return None
    
    def agregar_comentario_reporte(self, reporte_id, usuario_id, comentario, tipo_comentario='general'):
        """Agregar comentario a un reporte"""
        try:
            data = {
                'reporte_id': reporte_id,
                'usuario_id': usuario_id,
                'comentario': comentario,
                'tipo_comentario': tipo_comentario
            }
            
            result = self._client.table('comentarios_reportes').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error agregando comentario al reporte: {e}")
            return None

# Instancia global
supabase = SupabaseManager()

def get_supabase_client() -> SupabaseManager:
    """Obtener instancia del cliente de Supabase"""
    return supabase 