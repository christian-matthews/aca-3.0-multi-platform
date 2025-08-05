import openai
from app.config import Config
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    """Servicio para interactuar con OpenAI"""
    
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    async def get_ai_response(self, user_message: str, context: str = "") -> str:
        """
        Obtener respuesta de OpenAI
        Args:
            user_message: Mensaje del usuario
            context: Contexto adicional (datos de la empresa, etc.)
        """
        try:
            system_prompt = (
                "Eres un asesor financiero y contable experto. "
                "Proporciona respuestas claras, precisas y útiles sobre temas financieros, "
                "contables y de gestión empresarial. "
                "Si no tienes suficiente información, indícalo claramente. "
                "Siempre responde en español."
            )
            
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            if context:
                messages.append({
                    "role": "system", 
                    "content": f"Contexto adicional: {context}"
                })
            
            messages.append({
                "role": "user", 
                "content": user_message
            })
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error obteniendo respuesta de OpenAI: {e}")
            return "Lo siento, no puedo procesar tu consulta en este momento. Intenta nuevamente más tarde."
    
    async def analyze_financial_data(self, data: dict) -> str:
        """
        Analizar datos financieros con IA
        Args:
            data: Diccionario con datos financieros
        """
        try:
            analysis_prompt = f"""
            Analiza los siguientes datos financieros y proporciona insights útiles:
            
            Datos: {data}
            
            Por favor proporciona:
            1. Resumen ejecutivo
            2. Tendencias identificadas
            3. Recomendaciones
            4. Alertas importantes
            """
            
            return await self.get_ai_response(analysis_prompt)
            
        except Exception as e:
            logger.error(f"Error analizando datos financieros: {e}")
            return "Error analizando los datos financieros."
    
    async def generate_report_suggestion(self, user_query: str, available_data: list) -> str:
        """
        Sugerir reportes basados en la consulta del usuario
        Args:
            user_query: Consulta del usuario
            available_data: Lista de datos disponibles
        """
        try:
            suggestion_prompt = f"""
            Basándote en la consulta del usuario: "{user_query}"
            
            Y los datos disponibles: {available_data}
            
            Sugiere qué reportes o análisis serían más útiles para responder esta consulta.
            Proporciona una explicación clara de por qué cada sugerencia es relevante.
            """
            
            return await self.get_ai_response(suggestion_prompt)
            
        except Exception as e:
            logger.error(f"Error generando sugerencias de reportes: {e}")
            return "No puedo generar sugerencias en este momento."

# Instancia global
openai_service = OpenAIService() 