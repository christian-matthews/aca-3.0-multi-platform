# Variables de Entorno - ACA 3.0

## Configuración General

### Variables Requeridas

#### **Telegram Bots**
```bash
# Token del bot de administración
BOT_ADMIN_TOKEN=your_admin_bot_token_here

# Token del bot de producción
BOT_PRODUCTION_TOKEN=your_production_bot_token_here

# Chat ID del administrador principal
ADMIN_CHAT_ID=your_admin_chat_id_here
```

**Descripción:**
- `BOT_ADMIN_TOKEN`: Token obtenido de @BotFather para el bot de administración
- `BOT_PRODUCTION_TOKEN`: Token obtenido de @BotFather para el bot de producción
- `ADMIN_CHAT_ID`: ID del chat del administrador principal (solo este usuario puede usar el bot admin)

#### **Supabase Database**
```bash
# URL de tu proyecto Supabase
SUPABASE_URL=https://your-project.supabase.co

# Clave anónima de Supabase
SUPABASE_KEY=your_supabase_anon_key_here

# Clave de servicio de Supabase (opcional, para operaciones administrativas)
SUPABASE_SERVICE_KEY=your_supabase_service_key_here
```

**Descripción:**
- `SUPABASE_URL`: URL de tu proyecto Supabase
- `SUPABASE_KEY`: Clave anónima para operaciones normales
- `SUPABASE_SERVICE_KEY`: Clave de servicio para operaciones administrativas (opcional)

#### **OpenAI API**
```bash
# Clave de API de OpenAI
OPENAI_API_KEY=your_openai_api_key_here
```

**Descripción:**
- `OPENAI_API_KEY`: Clave de API de OpenAI para el asesor IA

### Variables Opcionales

#### **Google Calendar**
```bash
# Ruta al archivo de credenciales de Google Calendar
GOOGLE_CALENDAR_CREDENTIALS_FILE=path_to_credentials.json
```

**Descripción:**
- `GOOGLE_CALENDAR_CREDENTIALS_FILE`: Ruta al archivo JSON de credenciales de Google Calendar

#### **Configuración de la Aplicación**
```bash
# Entorno de ejecución
ENVIRONMENT=development

# Modo debug
DEBUG=true
```

**Descripción:**
- `ENVIRONMENT`: Entorno de ejecución (development, staging, production)
- `DEBUG`: Habilitar modo debug (true/false)

## Configuración por Entorno

### Desarrollo
```bash
ENVIRONMENT=development
DEBUG=true
```

### Producción
```bash
ENVIRONMENT=production
DEBUG=false
```

## Obtención de Variables

### 1. **Tokens de Telegram**

#### Crear Bots
1. Ir a [@BotFather](https://t.me/botfather) en Telegram
2. Enviar `/newbot`
3. Seguir las instrucciones para crear dos bots:
   - Bot de administración
   - Bot de producción
4. Guardar los tokens proporcionados

#### Obtener Chat ID
1. Enviar un mensaje a tu bot
2. Visitar: `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Buscar el `chat_id` en la respuesta

### 2. **Configuración de Supabase**

#### Crear Proyecto
1. Ir a [supabase.com](https://supabase.com)
2. Crear nuevo proyecto
3. Ir a Settings > API
4. Copiar URL y claves

#### Configurar Base de Datos
1. Ir a SQL Editor
2. Ejecutar el script de creación de tablas (ver `database_schema.md`)
3. Configurar Row Level Security

### 3. **OpenAI API**

#### Obtener API Key
1. Ir a [platform.openai.com](https://platform.openai.com)
2. Crear cuenta o iniciar sesión
3. Ir a API Keys
4. Crear nueva clave
5. Copiar la clave

### 4. **Google Calendar**

#### Configurar Credenciales
1. Ir a [Google Cloud Console](https://console.cloud.google.com)
2. Crear proyecto o seleccionar existente
3. Habilitar Google Calendar API
4. Crear credenciales OAuth 2.0
5. Descargar archivo JSON
6. Colocar en el proyecto

## Archivo .env

### Estructura Completa
```bash
# Telegram Bots
BOT_ADMIN_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
BOT_PRODUCTION_TOKEN=0987654321:ZYXwvuTSRqpONMlkjIHGfedCBA
ADMIN_CHAT_ID=123456789

# Supabase
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# OpenAI
OPENAI_API_KEY=sk-1234567890abcdefghijklmnopqrstuvwxyz

# Google Calendar
GOOGLE_CALENDAR_CREDENTIALS_FILE=./credentials.json

# App Configuration
ENVIRONMENT=development
DEBUG=true
```

### Validación de Variables

El sistema valida automáticamente que todas las variables requeridas estén configuradas al iniciar:

```python
# En app/config.py
@classmethod
def validate(cls):
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
```

## Seguridad

### Variables Sensibles
- **Nunca** committear archivos `.env` al repositorio
- Usar `.env.example` como plantilla
- Configurar variables en el servidor de producción
- Rotar tokens regularmente

### Buenas Prácticas
1. **Separación de entornos**: Diferentes configuraciones para dev/prod
2. **Validación**: Verificar variables al inicio
3. **Logging**: No loggear variables sensibles
4. **Backup**: Mantener copias seguras de configuraciones

## Despliegue

### Desarrollo Local
1. Copiar `env.example` a `.env`
2. Llenar con valores reales
3. Ejecutar aplicación

### Render (Producción)
1. Ir a Dashboard de Render
2. Seleccionar servicio
3. Ir a Environment
4. Agregar variables una por una

### Variables de Render
```bash
# Telegram
BOT_ADMIN_TOKEN
BOT_PRODUCTION_TOKEN
ADMIN_CHAT_ID

# Supabase
SUPABASE_URL
SUPABASE_KEY
SUPABASE_SERVICE_KEY

# OpenAI
OPENAI_API_KEY

# App
ENVIRONMENT=production
DEBUG=false
```

## Troubleshooting

### Variables Faltantes
```bash
Error: Variables de entorno faltantes: BOT_ADMIN_TOKEN, SUPABASE_URL
```
**Solución**: Verificar que todas las variables requeridas estén configuradas

### Tokens Inválidos
```bash
Error: Invalid token
```
**Solución**: Verificar tokens de Telegram en @BotFather

### Conexión a Supabase
```bash
Error: Connection to Supabase failed
```
**Solución**: Verificar URL y claves de Supabase

### OpenAI API
```bash
Error: OpenAI API key invalid
```
**Solución**: Verificar clave de API en OpenAI dashboard

## Monitoreo

### Health Check
```bash
curl https://your-app.onrender.com/health
```

### Status Check
```bash
curl https://your-app.onrender.com/status
```

### Logs
```bash
# Ver logs en Render
# Dashboard > Service > Logs
```

## Backup y Recuperación

### Configuración
1. Exportar variables de entorno
2. Guardar en lugar seguro
3. Documentar configuración

### Recuperación
1. Restaurar variables de entorno
2. Verificar conectividad
3. Probar funcionalidad básica 