"""
Módulo de autenticación y seguridad para ACA 3.0
"""

import logging
from app.database.supabase import supabase

logger = logging.getLogger(__name__)

class SecurityManager:
    """Gestor de seguridad y autenticación"""
    
    def __init__(self):
        # Chat IDs de administradores - usar el ADMIN_CHAT_ID de la configuración
        from app.config import Config
        self.admin_chat_ids = [Config.ADMIN_CHAT_ID] if Config.ADMIN_CHAT_ID else [123456789]
    
    def validate_user(self, chat_id: int):
        """Validar usuario y obtener sus datos"""
        try:
            user = supabase.get_user_by_chat_id(chat_id)
            
            if not user:
                return {
                    'valid': False,
                    'message': "❌ Usuario no registrado. Contacta al administrador para registrarte."
                }
            
            # Obtener datos de la empresa
            empresa = supabase.client.table('empresas').select('*').eq('id', user['empresa_id']).execute()
            
            if not empresa.data:
                return {
                    'valid': False,
                    'message': "❌ Empresa no encontrada. Contacta al administrador."
                }
            
            empresa_data = empresa.data[0]
            
            return {
                'valid': True,
                'user_data': {
                    'id': user['id'],
                    'chat_id': user['chat_id'],
                    'nombre': user['nombre'],
                    'rol': user['rol'],
                    'empresa_id': user['empresa_id'],
                    'empresa_nombre': empresa_data['nombre'],
                    'empresa_rut': empresa_data['rut']
                }
            }
            
        except Exception as e:
            logger.error(f"Error validando usuario {chat_id}: {e}")
            return {
                'valid': False,
                'message': "❌ Error de validación. Intenta nuevamente."
            }
    
    def is_admin(self, chat_id: int):
        """Verificar si el usuario es administrador"""
        return chat_id in self.admin_chat_ids
    
    def log_security_event(self, chat_id: int, event_type: str, description: str):
        """Registrar evento de seguridad"""
        try:
            data = {
                'chat_id': chat_id,
                'event_type': event_type,
                'description': description,
                'timestamp': 'now()'
            }
            supabase.client.table('security_logs').insert(data).execute()
        except Exception as e:
            logger.error(f"Error registrando evento de seguridad: {e}")

# Instancia global
security = SecurityManager() 