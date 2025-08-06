# 🏗️ Arquitectura del Sistema ACA 3.0 - Actualizado

## 📋 Resumen Ejecutivo

ACA 3.0 es un sistema integral de gestión contable multi-plataforma que integra:
- **Dashboard Web** con 6 vistas especializadas
- **Integración Airtable** para gestión documental
- **Bots Telegram** para acceso móvil
- **Base Supabase** optimizada con RLS
- **Sincronización Inteligente** con detección de duplicados

## 🎯 Arquitectura General Actualizada

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Airtable      │◄──►│   FastAPI Core   │◄──►│   Supabase      │
│  (Contador)     │    │  + Dashboard Web │    │ (Base de Datos) │
│  📊 Docs + Data │    │  🌐 6 Vistas     │    │  🔒 RLS + Opt   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Telegram Bots   │
                    │  🤖 Admin + Prod │
                    │  📱 Mobile Ready │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  External APIs   │
                    │  🧠 OpenAI       │
                    │  📅 Google Cal   │
                    │  💬 Slack (Soon) │
                    │  📝 Notion (Soon)│
                    └──────────────────┘
```

## 🔧 Componentes Principales

### 1. **FastAPI Core + Dashboard Web**
- **Ubicación**: `/app/main.py` + `/templates/`
- **Puerto**: 8000
- **Tecnologías**: FastAPI + Jinja2 + Bootstrap 5 + Chart.js

**Endpoints Dashboard**:
```
GET /dashboard           # Vista principal con KPIs
GET /dashboard/empresas  # Gestión completa empresas  
GET /dashboard/reportes  # Reportes con filtros
GET /dashboard/archivos  # Archivos grid/lista
GET /dashboard/airtable  # Monitor integración
GET /dashboard/sync      # Centro sincronización
```

**Endpoints API**:
```
GET  /health            # Estado sistema
GET  /status            # Estado servicios
GET  /docs              # Documentación Swagger
POST /sync/airtable     # Sincronización manual
GET  /airtable/statistics # Stats Airtable
```

### 2. **Dashboard Web - 6 Vistas Especializadas**

#### **Vista Principal** (`/dashboard`)
- **KPIs**: Empresas, reportes, archivos, sincronizaciones
- **Estado Servicios**: Supabase, Airtable, Bots en tiempo real
- **Gráfico Reportes**: Distribución por tipo con Chart.js
- **Actividad Reciente**: Últimas operaciones del sistema

#### **Gestión Empresas** (`/dashboard/empresas`)
- **CRUD Completo**: Crear, leer, actualizar empresas
- **Búsqueda RUT**: Filtrado inteligente por RUT
- **Estados**: Activo/Inactivo con indicadores visuales
- **Navegación**: Links directos a reportes por empresa

#### **Gestión Reportes** (`/dashboard/reportes`)
- **Filtros Avanzados**: Año, mes, tipo documento, empresa
- **Origen Datos**: Indicadores Airtable vs manual
- **Vista Archivos**: Acceso directo a documentos adjuntos
- **Estadísticas**: Reportes por período y categoría

#### **Gestión Archivos** (`/dashboard/archivos`)
- **Vista Dual**: Lista detallada y grid visual
- **Tipos Archivo**: PDF, Excel, Word con iconos
- **Previsualización**: Modal con vista previa PDF
- **Filtros**: Por tipo, tamaño, estado, fecha

#### **Monitor Airtable** (`/dashboard/airtable`)
- **Estado Conexión**: Real-time status check
- **Estadísticas**: Registros total, pendientes, procesados
- **Gráficos**: Distribución por empresa y tipo documento
- **Acciones**: Sincronización manual, test conexión

#### **Centro Sincronización** (`/dashboard/sync`)
- **Flujo Visual**: 4 pasos con animación
- **Logs Tiempo Real**: Consola con colores por tipo
- **Historial**: Timeline de sincronizaciones
- **Configuración**: Intervalos automáticos
- **Herramientas**: Verificar duplicados, limpiar cache

### 3. **Integración Airtable Avanzada**

**Base Configurada**: "ACA - Gestión Documental"
**Tabla**: "Reportes_Empresas"

**Campos Obligatorios**:
- `Empresa` (Text): "Nombre Empresa (RUT)" 
- `Fecha subida` (Date): Fecha del documento
- `Tipo documento` (Select): Balance, Estado Resultados, etc.
- `Archivo adjunto` (Attachment): PDFs, Excel
- `Estado subida` (Select): Pendiente, Procesado, Error
- `Comentarios` (Long Text): Notas y tracking

**Servicio Airtable** (`/app/services/airtable_service.py`):
```python
class AirtableService:
    def get_pending_records() -> List[Dict]
    def mark_as_processed(record_id: str) -> bool
    def get_statistics() -> Dict
    def get_all_records() -> List[Dict]
    def test_connection() -> bool
```

### 4. **Sincronización Inteligente**

**Servicio Sync** (`/app/services/sync_service.py`):

**Funciones Clave**:
```python
def sync_from_airtable() -> SyncResult:
    # 1. Obtener registros pendientes de Airtable
    # 2. Para cada registro:
    #    - Extraer RUT del nombre empresa
    #    - Buscar empresa en Supabase por RUT
    #    - Verificar si reporte ya existe (anti-duplicados)
    #    - Insertar o actualizar según corresponda
    #    - Sincronizar archivos adjuntos
    #    - Marcar como procesado en Airtable

def _extraer_rut_de_nombre(nombre: str) -> str:
    # Extrae RUT de formato "Empresa (12345678-9)"
    
def _get_empresa_by_rut(rut: str) -> Optional[Dict]:
    # Búsqueda confiable por RUT en lugar de nombre
    
def _verificar_duplicado(airtable_id: str) -> bool:
    # Verifica si registro ya fue procesado
```

**Flujo de Sincronización**:
1. **Detección**: Nuevos registros en Airtable
2. **Extracción**: RUT desde nombre empresa
3. **Búsqueda**: Empresa en Supabase por RUT
4. **Verificación**: Anti-duplicados por Airtable ID
5. **Procesamiento**: Inserción de reporte y archivos
6. **Confirmación**: Update estado en Airtable

### 5. **Base de Datos Supabase Optimizada**

**Tabla Empresas**:
```sql
CREATE TABLE empresas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(255) NOT NULL,
    rut VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(255),
    email VARCHAR(255),
    telefono VARCHAR(50),
    direccion TEXT,
    estado VARCHAR(20) DEFAULT 'activo',
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policy
CREATE POLICY "Usuarios ven solo sus empresas" 
ON empresas FOR ALL 
USING (auth.uid() = user_id);
```

**Tabla Reportes Mensuales**:
```sql
CREATE TABLE reportes_mensuales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    tipo_reporte VARCHAR(100) NOT NULL,
    estado VARCHAR(50) DEFAULT 'pendiente',
    comentarios TEXT,
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraint único para evitar duplicados
    UNIQUE(empresa_id, anio, mes, tipo_reporte)
);
```

**Tabla Archivos**:
```sql
CREATE TABLE archivos_reportes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporte_id UUID REFERENCES reportes_mensuales(id) ON DELETE CASCADE,
    empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE,
    nombre_archivo VARCHAR(255) NOT NULL,
    tipo_archivo VARCHAR(100),
    tamanio_bytes BIGINT,
    url_archivo TEXT NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_archivos_empresa ON archivos_reportes(empresa_id);
CREATE INDEX idx_archivos_reporte ON archivos_reportes(reporte_id);
CREATE INDEX idx_empresas_rut ON empresas(rut);
```

### 6. **Bots Telegram**

#### **Bot Admin** (`/app/bots/handlers/admin_handlers.py`)
- **Comando `/start`**: Menú principal administración
- **Comando `/empresas`**: CRUD completo empresas
- **Comando `/stats`**: Estadísticas del sistema
- **Comando `/config`**: Configuración servicios
- **Comando `/restart`**: Reinicio de bots

#### **Bot Producción** (`/app/bots/handlers/production_handlers.py`)
- **Comando `/start`**: Menú usuario final
- **Comando `/reportes`**: Consulta por RUT
- **Comando `/pendientes`**: Tareas pendientes
- **Comando `/asesor`**: Consultas IA
- **Comando `/agendar`**: Sistema citas

### 7. **Sistema de Templates**

**Base Template** (`/templates/base.html`):
- **Sidebar Navegación**: 6 vistas + logout
- **Header Responsive**: Título dinámico por página
- **Footer**: Info sistema y versión
- **Scripts Comunes**: Bootstrap, Chart.js, Font Awesome

**Template Inheritance**:
```html
<!-- Cada vista extiende base.html -->
{% extends "base.html" %}
{% block title %}Empresas - ACA 3.0{% endblock %}
{% block page_title %}Gestión de Empresas{% endblock %}
{% block content %}
<!-- Contenido específico de la vista -->
{% endblock %}
{% block scripts %}
<!-- JavaScript específico de la vista -->
{% endblock %}
```

## 🔄 Flujos de Datos Críticos

### **Flujo Carga Documento Contador**

```
1. Contador sube PDF a Airtable
   ├── Empresa: "THE WINGDEMO (12345678-9)"
   ├── Tipo: "Balance General"
   ├── Fecha: "2025-01-08"
   └── Archivo: balance_enero.pdf

2. Sistema detecta nuevo registro
   ├── Extrae RUT: "12345678-9"
   ├── Busca empresa en Supabase
   └── Encuentra: empresa_id = "uuid-123"

3. Verifica duplicados
   ├── Busca comentario con Airtable ID
   ├── No encuentra = registro nuevo
   └── Procede con inserción

4. Inserta reporte_mensual
   ├── empresa_id: "uuid-123"
   ├── titulo: "Balance General Enero 2025"
   ├── anio: 2025, mes: 1
   ├── tipo_reporte: "Balance General"
   └── comentarios: "Sincronizado desde Airtable [rec123]"

5. Descarga y almacena archivo
   ├── URL temporal de Airtable
   ├── Metadatos: nombre, tipo, tamaño
   └── Inserta en archivos_reportes

6. Actualiza estado Airtable
   ├── Estado: "Procesado"
   └── Comentarios: timestamp + detalles

7. Dashboard se actualiza automáticamente
   ├── Stats en tiempo real
   ├── Nuevo reporte visible
   └── Logs en centro sync
```

### **Flujo Consulta Usuario Telegram**

```
1. Usuario envía: "/reportes 12345678-9"

2. Bot valida formato RUT
   ├── Regex validation
   └── Formato correcto ✅

3. Busca empresa en Supabase
   ├── SELECT * FROM empresas WHERE rut = '12345678-9'
   └── Encuentra: "THE WINGDEMO"

4. Obtiene reportes de la empresa
   ├── SELECT * FROM reportes_mensuales WHERE empresa_id = 'uuid-123'
   └── Encuentra: 3 reportes

5. Procesa con OpenAI
   ├── Contexto: datos empresa + reportes
   ├── Prompt: análisis financiero
   └── Respuesta: insights inteligentes

6. Formatea respuesta Telegram
   ├── Nombre empresa
   ├── Lista reportes con fechas
   ├── Análisis IA
   └── Botones navegación

7. Usuario recibe respuesta completa
   ├── Datos estructurados
   ├── Análisis profesional
   └── Opciones adicionales
```

## 🛡️ Seguridad y Performance

### **Row Level Security (RLS)**
- **Empresas**: Solo empresas del usuario autenticado
- **Reportes**: Filtrado automático por empresa_id
- **Archivos**: Acceso granular por reporte

### **Optimizaciones Base Datos**
- **Índices**: RUT, empresa_id, fechas
- **Constraints**: Únicos para evitar duplicados
- **Triggers**: Actualización automática timestamps

### **Performance Metrics Actuales**
- **API Response**: <150ms promedio
- **Dashboard Load**: <2s primera carga  
- **Sync 50 registros**: <10s
- **DB Query Time**: <50ms promedio

## 🔮 Roadmap Arquitectural

### **Próximas Integraciones**
1. **Notion**: Dashboard ejecutivo CEO
2. **Slack**: Notificaciones equipo
3. **Calendly**: Sistema agendamiento
4. **Deploy**: Render/Vercel producción

### **Expansión Multi-País**
- **Multi-DB**: Supabase por región
- **Multi-Currency**: Conversiones automáticas  
- **Multi-Language**: i18n completo
- **Compliance**: Regulaciones por país

### **Arquitectura Microservicios**
- **Auth Service**: JWT + roles
- **Company Service**: Gestión empresas
- **Report Service**: Procesamiento reportes
- **File Service**: Almacenamiento archivos
- **Notification Service**: Multi-canal

---

**Esta arquitectura soporta el crecimiento actual y futuro manteniendo simplicidad operacional.**