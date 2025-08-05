from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from app.config import Config
import os
import logging
from datetime import datetime, timedelta
import pickle

logger = logging.getLogger(__name__)

class GoogleCalendarService:
    """Servicio para interactuar con Google Calendar"""
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Autenticar con Google Calendar"""
        try:
            # El archivo token.pickle almacena los tokens de acceso y actualización del usuario
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.creds = pickle.load(token)
            
            # Si no hay credenciales válidas disponibles, deja que el usuario se autentique
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    if Config.GOOGLE_CALENDAR_CREDENTIALS_FILE and os.path.exists(Config.GOOGLE_CALENDAR_CREDENTIALS_FILE):
                        flow = InstalledAppFlow.from_client_secrets_file(
                            Config.GOOGLE_CALENDAR_CREDENTIALS_FILE, self.SCOPES)
                        self.creds = flow.run_local_server(port=0)
                    else:
                        logger.warning("Archivo de credenciales de Google Calendar no encontrado")
                        return
                
                # Guardar las credenciales para la próxima ejecución
                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.creds, token)
            
            self.service = build('calendar', 'v3', credentials=self.creds)
            logger.info("Autenticación con Google Calendar exitosa")
            
        except Exception as e:
            logger.error(f"Error autenticando con Google Calendar: {e}")
    
    async def create_event(self, summary: str, description: str, start_time: datetime, 
                          end_time: datetime, attendees: list = None) -> dict:
        """
        Crear un evento en Google Calendar
        Args:
            summary: Título del evento
            description: Descripción del evento
            start_time: Hora de inicio
            end_time: Hora de fin
            attendees: Lista de emails de asistentes
        """
        try:
            if not self.service:
                return {"success": False, "message": "Servicio de calendario no disponible"}
            
            event = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'America/Santiago',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'America/Santiago',
                },
            }
            
            if attendees:
                event['attendees'] = [{'email': email} for email in attendees]
            
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            
            return {
                "success": True,
                "message": "Evento creado exitosamente",
                "event_id": event['id'],
                "html_link": event['htmlLink']
            }
            
        except Exception as e:
            logger.error(f"Error creando evento: {e}")
            return {"success": False, "message": f"Error creando evento: {str(e)}"}
    
    async def get_events(self, start_date: datetime = None, end_date: datetime = None) -> list:
        """
        Obtener eventos del calendario
        Args:
            start_date: Fecha de inicio (por defecto hoy)
            end_date: Fecha de fin (por defecto en 7 días)
        """
        try:
            if not self.service:
                return []
            
            if not start_date:
                start_date = datetime.now()
            if not end_date:
                end_date = start_date + timedelta(days=7)
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=start_date.isoformat() + 'Z',
                timeMax=end_date.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                formatted_events.append({
                    'id': event['id'],
                    'summary': event.get('summary', 'Sin título'),
                    'description': event.get('description', ''),
                    'start': start,
                    'end': end,
                    'html_link': event.get('htmlLink', '')
                })
            
            return formatted_events
            
        except Exception as e:
            logger.error(f"Error obteniendo eventos: {e}")
            return []
    
    async def delete_event(self, event_id: str) -> dict:
        """
        Eliminar un evento
        Args:
            event_id: ID del evento a eliminar
        """
        try:
            if not self.service:
                return {"success": False, "message": "Servicio de calendario no disponible"}
            
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            
            return {"success": True, "message": "Evento eliminado exitosamente"}
            
        except Exception as e:
            logger.error(f"Error eliminando evento: {e}")
            return {"success": False, "message": f"Error eliminando evento: {str(e)}"}
    
    async def update_event(self, event_id: str, **kwargs) -> dict:
        """
        Actualizar un evento
        Args:
            event_id: ID del evento a actualizar
            **kwargs: Campos a actualizar
        """
        try:
            if not self.service:
                return {"success": False, "message": "Servicio de calendario no disponible"}
            
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
            
            # Actualizar campos proporcionados
            for key, value in kwargs.items():
                if key in ['summary', 'description', 'start', 'end']:
                    event[key] = value
            
            updated_event = self.service.events().update(
                calendarId='primary', eventId=event_id, body=event).execute()
            
            return {
                "success": True,
                "message": "Evento actualizado exitosamente",
                "event_id": updated_event['id']
            }
            
        except Exception as e:
            logger.error(f"Error actualizando evento: {e}")
            return {"success": False, "message": f"Error actualizando evento: {str(e)}"}

# Instancia global
calendar_service = GoogleCalendarService() 