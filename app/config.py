import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Configuration
    BOT_ADMIN_TOKEN = os.getenv("BOT_ADMIN_TOKEN")
    BOT_PRODUCTION_TOKEN = os.getenv("BOT_PRODUCTION_TOKEN")
    ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Calendly Configuration (opcional)
    CALENDLY_API_KEY = os.getenv("CALENDLY_API_KEY")
    
    # Google Calendar Configuration (opcional)
    GOOGLE_CALENDAR_CREDENTIALS_FILE = os.getenv("GOOGLE_CALENDAR_CREDENTIALS_FILE")
    
    # App Configuration
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    
    @classmethod
    def validate(cls):
        """Validar que todas las variables requeridas estén configuradas"""
        required_vars = [
            "BOT_ADMIN_TOKEN",
            "BOT_PRODUCTION_TOKEN", 
            "ADMIN_CHAT_ID",
            "SUPABASE_URL",
            "SUPABASE_KEY",
            "OPENAI_API_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Variables de entorno faltantes: {', '.join(missing_vars)}")
        
        return True 