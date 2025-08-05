# ACA 3.0 - Sistema de Bots de Telegram

Sistema de bots de Telegram para gestión empresarial con integración a Supabase y OpenAI.

## 🚀 Características

- **Dos Bots de Telegram**: Admin y Producción
- **Seguridad Robusta**: Validación de usuarios y aislamiento de datos
- **Base de Datos Supabase**: PostgreSQL con Row Level Security
- **Asesor IA**: Integración con OpenAI GPT-3.5
- **Sistema de Agendamiento**: En desarrollo futuro
- **Logging Completo**: Auditoría de todas las interacciones
- **Arquitectura Modular**: FastAPI con estructura escalable

## 📋 Requisitos

- Python 3.8+
- Cuenta de Supabase
- Tokens de bots de Telegram
- API Key de OpenAI

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd aca_3
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
cp env.example .env
# Editar .env con tus credenciales
```

### 4. Configurar base de datos
Ejecutar el script SQL en Supabase (ver `docs/setup_database.md`)

### 5. Ejecutar la aplicación
```bash
python -m app.main
```

## 🗄️ Configuración de Base de Datos

### **Paso 1: Crear Proyecto en Supabase**
1. Ve a [supabase.com](https://supabase.com)
2. Crea una cuenta o inicia sesión
3. Crea un nuevo proyecto
4. Anota la URL y las claves

### **Paso 2: Ejecutar Script SQL**
1. Ve a **SQL Editor** en tu proyecto de Supabase
2. Copia y ejecuta el script completo de `docs/setup_database.md`
3. El script creará todas las tablas y datos de ejemplo

### **Paso 3: Verificar Configuración**
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar script de pruebas
python test_database.py
```

### **Datos de Ejemplo Incluidos**
- **3 Empresas** con usuarios asociados
- **Reportes financieros** con enlaces PDF
- **Pendientes** con diferentes prioridades
- **Cuentas por cobrar y pagar** con montos reales
- **Conversaciones** de ejemplo

## 🔧 Configuración

### Variables de Entorno Requeridas

```bash
# Telegram Bots
BOT_ADMIN_TOKEN=your_admin_bot_token
BOT_PRODUCTION_TOKEN=your_production_bot_token
ADMIN_CHAT_ID=your_admin_chat_id

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# OpenAI
OPENAI_API_KEY=your_openai_api_key
```

### Variables Opcionales (Desarrollo Futuro)

```bash
# Calendly (para sistema de agendamiento)
CALENDLY_API_KEY=your_calendly_api_key

# Google Calendar (alternativa para agendamiento)
GOOGLE_CALENDAR_CREDENTIALS_FILE=path_to_credentials.json
```

Ver documentación completa en `docs/variables.md`

## 📚 Documentación

- [Configuración de Base de Datos](docs/setup_database.md)
- [Esquema de Base de Datos](docs/database_schema.md)
- [Arquitectura del Sistema](docs/architecture.md)
- [Variables de Entorno](docs/variables.md)
- [Estado Actual del Proyecto](docs/current_status.md)
- [Configuración de Calendly](docs/calendly_setup.md) *(Desarrollo futuro)*

## 🏗️ Estructura del Proyecto

```
aca_3/
├── app/
│   ├── main.py                 # Aplicación FastAPI
│   ├── config.py               # Configuración
│   ├── database/
│   │   └── supabase.py         # Gestor de Supabase
│   ├── bots/
│   │   ├── bot_manager.py      # Gestor de bots
│   │   └── handlers/           # Manejadores
│   ├── security/
│   │   └── auth.py             # Autenticación
│   ├── services/               # Servicios externos
│   │   ├── openai_service.py   # OpenAI
│   │   ├── calendly_service.py # Calendly (futuro)
│   │   └── calendar_service.py # Google Calendar (futuro)
│   └── utils/
│       └── helpers.py          # Utilidades
├── docs/                       # Documentación
├── test_database.py           # Script de pruebas
├── requirements.txt            # Dependencias
└── README.md                  # Este archivo
```

## 🤖 Funcionalidades

### Bot de Administración
- Crear nuevas empresas
- Ver estadísticas del sistema
- Gestionar usuarios
- Monitorear actividad

### Bot de Producción
- **Reportes**: Acceso a reportes financieros
- **Pendientes**: Gestión de tareas pendientes
- **CxC & CxP**: Cuentas por cobrar y pagar
- **Asesor IA**: Consultas inteligentes
- **Agendar**: Sistema de citas *(En desarrollo)*
- **Salir**: Cerrar sesión

## 🔒 Seguridad

- **Validación de Usuarios**: Verificación en cada interacción
- **Aislamiento de Datos**: Filtrado por empresa
- **Row Level Security**: En Supabase
- **Logging de Auditoría**: Todas las acciones registradas
- **Sanitización de Inputs**: Protección contra inyección

## 🚀 Despliegue

### Desarrollo Local
```bash
python -m app.main
```

### Render (Producción)
1. Conectar repositorio a Render
2. Configurar variables de entorno
3. Desplegar automáticamente

## 📊 Monitoreo

### Health Check
```bash
curl https://your-app.onrender.com/health
```

### Status
```bash
curl https://your-app.onrender.com/status
```

### Pruebas de Base de Datos
```bash
python test_database.py
```

## 🐛 Troubleshooting

### Variables Faltantes
```bash
Error: Variables de entorno faltantes
```
**Solución**: Verificar archivo `.env`

### Tokens Inválidos
```bash
Error: Invalid token
```
**Solución**: Verificar tokens en @BotFather

### Conexión a Supabase
```bash
Error: Connection failed
```
**Solución**: Verificar URL y claves de Supabase

### Base de Datos Vacía
```bash
Error: No data found
```
**Solución**: Ejecutar script SQL de `docs/setup_database.md`

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Crear issue en GitHub
- Contactar al administrador del sistema

## 🔄 Changelog

### v1.0.0
- Sistema base implementado
- Bots de Telegram funcionales
- Integración con Supabase
- Sistema de seguridad implementado
- Base de datos con datos de ejemplo
- Documentación completa
- Preparado para integración futura de calendario

## 🎯 Roadmap

- [ ] Implementación completa del Asesor IA
- [ ] Sistema de agendamiento (Calendly/Google Calendar)
- [ ] Dashboard web de administración
- [ ] Notificaciones push
- [ ] Integración con más APIs financieras
- [ ] Sistema de reportes automáticos
- [ ] Multiidioma
- [ ] App móvil nativa 