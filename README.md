# 🚀 ACA 3.0 - Sistema de Gestión Contable Multi-Plataforma

Sistema integral de gestión contable con integración multi-plataforma que incluye Telegram, Airtable, Supabase y Dashboard Web.

## ✨ Características Principales

### 🤖 **Bots de Telegram**
- **Bot Admin**: Gestión administrativa y monitoreo del sistema
- **Bot Producción**: Acceso para usuarios finales y consultas

### 🌐 **Dashboard Web Completo**
- **Vista General**: Estadísticas y métricas en tiempo real
- **Gestión de Empresas**: CRUD completo de empresas
- **Reportes**: Visualización y gestión de reportes financieros
- **Archivos**: Gestión de documentos con vista previa
- **Airtable**: Monitoreo de integración y sincronización
- **Sincronización**: Centro de control para sync automático

### 📊 **Integraciones**
- **Airtable**: Gestión documental del contador
- **Supabase**: Base de datos principal con RLS
- **OpenAI**: Procesamiento inteligente de documentos
- **Google Calendar**: Agendamiento y recordatorios
- **Telegram**: Notificaciones y acceso móvil

### 🔄 **Sincronización Inteligente**
- Detección automática de duplicados
- Búsqueda por RUT para mayor confiabilidad
- Sincronización incremental
- URLs de archivos con renovación automática

### 📊 **Sistema de Logging Completo**
- Registro de todas las conversaciones de Telegram
- Detección de usuarios autorizados y no autorizados
- Dashboard de conversaciones en tiempo real
- Botones de contacto directo con @wingmanbod
- Analíticas de uso de bots

## 🚀 Instalación Rápida

### Opción 1: Setup Automático (Recomendado)
```bash
python3 setup.py
```

### Opción 2: Setup Manual
```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp env.example .env
# Editar .env con tus credenciales

# 4. Iniciar sistema
python3 run.py
```

## ⚙️ Configuración

### Variables de Entorno Requeridas

```bash
# Telegram Bots
BOT_ADMIN_TOKEN=tu_token_de_bot_admin
BOT_PRODUCTION_TOKEN=tu_token_de_bot_produccion
ADMIN_CHAT_ID=tu_chat_id_admin

# Supabase
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_key_de_supabase
SUPABASE_SERVICE_KEY=tu_service_key

# OpenAI
OPENAI_API_KEY=tu_api_key_de_openai

# Airtable
AIRTABLE_API_KEY=tu_api_key_de_airtable
AIRTABLE_BASE_ID=tu_base_id
AIRTABLE_TABLE_NAME=nombre_de_tu_tabla
AIRTABLE_VIEW_NAME=nombre_de_vista

# Configuración de App
ENVIRONMENT=development
DEBUG=true
```

### Configuración de Airtable

1. **Crear Base en Airtable**:
   - Crea una nueva base con el nombre "ACA - Gestión Documental"
   - Agrega una tabla llamada "Reportes_Empresas"

2. **Campos Requeridos**:
   - `Empresa` (Single line text)
   - `Fecha subida` (Date)
   - `Tipo documento` (Single select)
   - `Archivo adjunto` (Attachment)
   - `Comentarios` (Long text)
   - `Estado subida` (Single select): Pendiente, Procesado, Error

3. **Formato Recomendado para Empresa**:
   ```
   Nombre de Empresa (RUT)
   Ejemplo: THE WINGDEMO (12345678-9)
   ```

## 🌐 Uso del Sistema

### Iniciar el Sistema
```bash
# Usando script de inicio
./start.sh

# O manualmente
source venv/bin/activate
python3 run.py
```

### Acceder al Dashboard
- **Dashboard Principal**: http://localhost:8000/dashboard
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Endpoints Principales

#### API Core
- `GET /health` - Estado del sistema
- `GET /status` - Estado de servicios
- `GET /docs` - Documentación interactiva

#### Dashboard Web
- `GET /dashboard` - Vista principal
- `GET /dashboard/empresas` - Gestión de empresas
- `GET /dashboard/reportes` - Gestión de reportes
- `GET /dashboard/archivos` - Gestión de archivos
- `GET /dashboard/airtable` - Monitoreo de Airtable
- `GET /dashboard/sync` - Centro de sincronización

#### Airtable
- `GET /airtable/status` - Estado de conexión
- `GET /airtable/records` - Obtener registros
- `GET /airtable/statistics` - Estadísticas
- `GET /airtable/pending` - Registros pendientes

#### Sincronización
- `POST /sync/airtable` - Ejecutar sincronización manual
- `GET /sync/statistics` - Estadísticas de sincronización

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Airtable      │◄──►│   FastAPI Core   │◄──►│   Supabase      │
│  (Contador)     │    │                  │    │ (Base de Datos) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Dashboard Web   │
                    │     + Bots       │
                    │    Telegram      │
                    └──────────────────┘
```

### Flujo de Datos

1. **Entrada**: Contador sube documentos a Airtable
2. **Sincronización**: Sistema detecta nuevos registros
3. **Procesamiento**: Validación y detección de duplicados
4. **Almacenamiento**: Datos guardados en Supabase
5. **Acceso**: Dashboard web y bots Telegram para consultas

## 📊 Funcionalidades por Módulo

### 🗄️ Base de Datos (Supabase)
- Empresas con RLS por usuario
- Reportes mensuales categorizados
- Archivos con URLs seguras
- Información de compañía
- Logs de sincronización

### 📋 Gestión Documental (Airtable)
- Interface amigable para contadores
- Carga de archivos PDF/Excel
- Categorización automática
- Estado de procesamiento
- Comentarios y notas

### 🤖 Bots de Telegram
- Comandos administrativos
- Consultas de empresas y reportes
- Notificaciones en tiempo real
- Acceso móvil completo

### 🌐 Dashboard Web
- Estadísticas en tiempo real
- Gestión CRUD completa
- Visualizaciones con gráficos
- Sistema de filtros avanzado
- Sincronización manual/automática

## 🛠️ Desarrollo

### Estructura del Proyecto
```
aca_3/
├── app/
│   ├── bots/                 # Bots de Telegram
│   ├── database/             # Configuración Supabase
│   ├── security/             # Autenticación y autorización
│   ├── services/             # Servicios (Airtable, Sync, etc.)
│   ├── utils/                # Utilidades
│   ├── config.py             # Configuración global
│   └── main.py               # Aplicación FastAPI
├── templates/                # Plantillas HTML
├── static/                   # Archivos estáticos
├── testing/                  # Scripts de testing
├── docs/                     # Documentación
├── requirements.txt          # Dependencias Python
├── setup.py                  # Script de configuración
├── start.sh                  # Script de inicio
└── run.py                    # Punto de entrada
```

### Comandos de Desarrollo
```bash
# Activar entorno
source venv/bin/activate

# Instalar dependencias de desarrollo
pip install -r requirements.txt

# Ejecutar tests
python -m pytest testing/

# Verificar base de datos
python testing/database/quick_db_check.py

# Test de servicios
python testing/system/test_system.py
```

### Testing
```bash
# Test completo del sistema
python testing/system/test_system.py

# Test de Airtable
python testing/airtable/test_airtable_service.py

# Test de extracción de RUT
python testing/airtable/test_rut_extraction.py

# Verificación de base de datos
python testing/database/quick_db_check.py
```

## 🔧 Solución de Problemas

### Errores Comunes

#### 1. Error de Dependencias
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

#### 2. Error de Airtable
```bash
# Verificar credenciales en .env
AIRTABLE_API_KEY=tu_api_key_aqui
AIRTABLE_BASE_ID=tu_base_id_aqui
```

#### 3. Error de Supabase
```bash
# Verificar conexión
python testing/database/quick_db_check.py
```

#### 4. Error de Telegram
```bash
# Verificar tokens de bots
BOT_ADMIN_TOKEN=token_valido
BOT_PRODUCTION_TOKEN=token_valido
```

### Logs y Monitoreo
- Logs en tiempo real en `/dashboard/sync`
- Health check en `/health`
- Estadísticas en `/sync/statistics`

## 📈 Roadmap

### ✅ Completado
- [x] Integración Airtable completa
- [x] Dashboard web funcional
- [x] Bots de Telegram operativos
- [x] Sincronización por RUT
- [x] Sistema de duplicados
- [x] Interface responsive

### 🔄 En Desarrollo
- [ ] Notion para dashboard ejecutivo
- [ ] Slack para notificaciones
- [ ] Calendly para agendamiento
- [ ] Deploy automático
- [ ] Asesor IA avanzado

### 🚀 Próximas Funcionalidades
- [ ] App móvil nativa
- [ ] API pública con autenticación
- [ ] Reportes automatizados
- [ ] Integración con bancos
- [ ] Machine Learning para categorización

## 👥 Contribución

1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🆘 Soporte

- **Issues**: Crear issue en GitHub
- **Documentación**: Ver `/docs` para guías detalladas
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

**ACA 3.0** - Sistema de Gestión Contable Multi-Plataforma
Desarrollado con ❤️ para simplificar la gestión contable.