# Arquitectura del Sistema - ACA 3.0

## Visión General

El sistema ACA 3.0 es una aplicación de bots de Telegram que permite a las empresas acceder a información financiera y contable a través de una interfaz conversacional segura.

## Arquitectura General

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram      │    │   FastAPI       │    │   Supabase      │
│   Bots          │◄──►│   Application   │◄──►│   Database      │
│                 │    │                 │    │                 │
│ • BOT_ADMIN     │    │ • REST API      │    │ • PostgreSQL    │
│ • BOT_PRODUCTION│    │ • Webhooks      │    │ • Real-time     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   External      │
                       │   Services      │
                       │                 │
                       │ • OpenAI API    │
                       │ • Google Calendar│
                       └─────────────────┘
```

## Componentes Principales

### 1. **Bots de Telegram**

#### BOT_ADMIN
- **Propósito**: Gestión administrativa del sistema
- **Usuarios**: Solo el administrador principal
- **Funcionalidades**:
  - Crear nuevas empresas
  - Ver estadísticas del sistema
  - Gestionar usuarios
  - Monitorear actividad

#### BOT_PRODUCTION
- **Propósito**: Interfaz principal para usuarios empresariales
- **Usuarios**: Usuarios registrados por empresa
- **Funcionalidades**:
  - Reportes financieros
  - Pendientes y tareas
  - Cuentas por cobrar/pagar
  - Asesor IA
  - Sistema de agendamiento

### 2. **FastAPI Application**

#### Estructura Modular
```
app/
├── main.py              # Aplicación principal
├── config.py            # Configuración centralizada
├── database/            # Capa de datos
│   └── supabase.py      # Gestor de Supabase
├── bots/                # Lógica de bots
│   ├── bot_manager.py   # Gestor principal
│   └── handlers/        # Manejadores específicos
│       ├── admin_handlers.py
│       └── production_handlers.py
├── security/            # Seguridad
│   └── auth.py          # Autenticación y validación
├── services/            # Servicios externos
│   ├── openai_service.py
│   └── calendar_service.py
└── utils/               # Utilidades
    └── helpers.py       # Funciones auxiliares
```

#### Características
- **Async/Await**: Manejo asíncrono de operaciones
- **Dependency Injection**: Inyección de dependencias
- **Error Handling**: Manejo centralizado de errores
- **Logging**: Sistema de logs estructurado
- **CORS**: Configuración para desarrollo web

### 3. **Base de Datos (Supabase)**

#### Características
- **PostgreSQL**: Base de datos principal
- **Row Level Security**: Seguridad a nivel de fila
- **Real-time**: Actualizaciones en tiempo real
- **Backup Automático**: Copias de seguridad automáticas
- **Escalabilidad**: Infraestructura escalable

#### Tablas Principales
- `empresas`: Información de empresas
- `usuarios`: Usuarios registrados
- `conversaciones`: Historial de conversaciones
- `reportes`: Reportes disponibles
- `pendientes`: Tareas pendientes
- `cuentas_cobrar`: Cuentas por cobrar
- `cuentas_pagar`: Cuentas por pagar
- `citas`: Sistema de agendamiento
- `security_logs`: Logs de seguridad

### 4. **Servicios Externos**

#### OpenAI API
- **Propósito**: Asesoría inteligente
- **Integración**: Chat completions
- **Modelo**: GPT-3.5-turbo
- **Contexto**: Financiero y contable

#### Google Calendar API
- **Propósito**: Sistema de agendamiento
- **Integración**: OAuth 2.0
- **Funcionalidades**:
  - Crear eventos
  - Listar eventos
  - Actualizar eventos
  - Eliminar eventos

## Flujo de Datos

### 1. **Registro de Usuario**
```
Usuario → BOT_ADMIN → Validación → Crear Empresa → Crear Usuario → Confirmación
```

### 2. **Acceso a Sistema**
```
Usuario → BOT_PRODUCTION → Validación → Menú Principal → Funcionalidades
```

### 3. **Consulta de Datos**
```
Usuario → Bot → Validación → Supabase → Filtrado por Empresa → Respuesta
```

### 4. **Asesoría IA**
```
Usuario → Bot → OpenAI API → Contexto Empresa → Respuesta IA → Usuario
```

## Seguridad

### 1. **Validación de Usuarios**
- Verificación de chat_id en cada interacción
- Validación de empresa_id en todas las consultas
- Control de acceso basado en roles

### 2. **Aislamiento de Datos**
- Filtrado automático por empresa_id
- Row Level Security en Supabase
- Logs de auditoría completos

### 3. **Protección de APIs**
- Validación de tokens
- Rate limiting
- Sanitización de inputs

### 4. **Logging de Seguridad**
- Registro de todas las interacciones
- Eventos de seguridad
- Trazabilidad completa

## Patrones de Diseño

### 1. **Singleton Pattern**
- Configuración centralizada
- Conexiones de base de datos
- Gestores de servicios

### 2. **Factory Pattern**
- Creación de bots
- Inicialización de servicios
- Gestión de handlers

### 3. **Observer Pattern**
- Eventos de seguridad
- Logging automático
- Notificaciones

### 4. **Strategy Pattern**
- Diferentes tipos de validación
- Múltiples servicios de IA
- Varios proveedores de calendario

## Escalabilidad

### 1. **Horizontal**
- Múltiples instancias de FastAPI
- Load balancing
- Microservicios

### 2. **Vertical**
- Optimización de consultas
- Caching
- Compresión de datos

### 3. **Funcional**
- Módulos independientes
- Plugins de funcionalidad
- APIs extensibles

## Monitoreo y Logging

### 1. **Métricas**
- Uso de bots
- Tiempo de respuesta
- Errores por tipo
- Usuarios activos

### 2. **Logs**
- Aplicación: INFO, WARNING, ERROR
- Seguridad: Todos los eventos
- Base de datos: Consultas lentas
- APIs externas: Respuestas

### 3. **Alertas**
- Errores críticos
- Tiempo de respuesta alto
- Uso de recursos
- Intentos de acceso no autorizado

## Despliegue

### 1. **Desarrollo**
- Docker Compose
- Variables de entorno locales
- Hot reload

### 2. **Producción**
- Render (GitHub integration)
- Variables de entorno seguras
- SSL automático
- Auto-scaling

### 3. **CI/CD**
- GitHub Actions
- Tests automáticos
- Despliegue automático
- Rollback automático

## Consideraciones Técnicas

### 1. **Performance**
- Consultas optimizadas
- Índices de base de datos
- Caching de respuestas
- Compresión de datos

### 2. **Mantenibilidad**
- Código modular
- Documentación completa
- Tests unitarios
- Code reviews

### 3. **Disponibilidad**
- Health checks
- Auto-restart
- Backup automático
- Monitoring 24/7 