# 📋 PLAN INTEGRADO ACA 3.0: MULTI-PLATAFORMA COMPLETO

**Basado en Inspección Completa de Supabase realizada el 2025-08-05**  
**Actualizado con integración Airtable + Notion + Slack + Telegram**

---

## 🌟 VISIÓN GLOBAL ACTUALIZADA

### 🏗️ **ARQUITECTURA MULTI-PLATAFORMA**

```mermaid
flowchart TD
    A[Contador - Airtable] -->|Python Script| B[Supabase Central]
    B -->|Python Script| C[Dueño - Notion]
    B -->|Bot API| D[Telegram Bots]
    B -->|Slack API| E[Slack Notifications]
    B -->|FastAPI| F[Web Dashboard]
    
    subgraph "Usuarios Finales"
        G[Contadores] --> A
        H[Dueños Empresa] --> C
        I[Usuarios Móviles] --> D
        J[Equipos Trabajo] --> E
    end
```

### 🎭 **ROLES Y PLATAFORMAS**

| Usuario | Plataforma Principal | Funcionalidad |
|---------|---------------------|---------------|
| **Contador** | 📊 Airtable | Subir documentos, gestión archivos |
| **Dueño Empresa** | 📝 Notion | Dashboard ejecutivo, visualización |
| **Usuario Móvil** | 📱 Telegram | Consultas rápidas, notificaciones |
| **Equipo Trabajo** | 💬 Slack | Colaboración, notificaciones grupales |
| **Administrador** | 🌐 FastAPI Web | Gestión sistema, configuración |

---

## 📊 RESUMEN ESTADO ACTUAL

### ✅ **Lo que FUNCIONA perfectamente:**
- **Sistema base**: Bots Telegram + FastAPI + Supabase ✅
- **Tablas CORE con datos**: `empresas` (3 registros), `usuarios` (4 registros) ✅
- **Variables entorno**: `.env` configurado correctamente ✅
- **UI/UX**: Layout 2 columnas, navegación mejorada ✅

### 🟡 **Lo que necesita ATENCIÓN:**
- **12 tablas vacías**: Todas las tablas existen pero solo `empresas` y `usuarios` tienen datos
- **🚨 FALLA CRÍTICA**: `archivos_reportes` y `archivos_info_compania` sin `empresa_id` (riesgo seguridad)
- **Variables faltantes**: Airtable, Notion, Slack no están en `env.example`
- **Sin ORM**: No existe `models.py` con SQLModel
- **Sin migraciones**: No hay sistema Alembic
- **Sin sincronización**: Faltan scripts automáticos entre plataformas

---

## 🎯 FASES PRIORIZADAS

### **FASE 0 - CORRECCIONES CRÍTICAS DE SEGURIDAD** ⏱️ *1-2 horas* 🚨

#### 0.1 🔴 CRÍTICO: Corregir falla de seguridad en archivos
```sql
-- Agregar empresa_id a tablas de archivos
ALTER TABLE archivos_reportes 
ADD COLUMN empresa_id UUID REFERENCES empresas(id);

ALTER TABLE archivos_info_compania 
ADD COLUMN empresa_id UUID REFERENCES empresas(id);
```

#### 0.2 🔴 CRÍTICO: Actualizar políticas RLS
```sql
-- Crear políticas de seguridad para archivos
-- Asegurar aislamiento por empresa
```

#### 0.3 🔴 CRÍTICO: Actualizar métodos en código
- Modificar `app/database/supabase.py`
- Agregar validación de `empresa_id` en métodos de archivos
- Testing de seguridad

#### 0.4 🟡 Poblar tablas con datos de prueba
```sql
-- Agregar datos de ejemplo para testing:
-- reportes_mensuales, info_compania, pendientes
```

---

### **FASE 1 - BASE AIRTABLE + SANEAMIENTO** ⏱️ *3-4 horas*

#### 1.1 Actualizar `env.example` con TODAS las variables faltantes
```bash
# Telegram (existente)
BOT_ADMIN_TOKEN=your_admin_bot_token
BOT_PRODUCTION_TOKEN=your_production_bot_token
ADMIN_CHAT_ID=your_admin_chat_id

# Supabase (existente)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SUPABASE_SERVICE_KEY=your_service_key

# Slack (actualizado)
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token
SLACK_WORKSPACE_ID=your-workspace-id

# Airtable (NUEVO)
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=your_base_id
AIRTABLE_TABLE_NAME=ACA - Gestión Documental

# Notion (NUEVO)
NOTION_API_KEY=secret_your_notion_integration_key
NOTION_DATABASE_ID=your_main_database_id
NOTION_WORKSPACE_ID=your_workspace_id

# Sincronización (NUEVO)
SYNC_INTERVAL_MINUTES=30
ENABLE_AUTO_SYNC=true
FILE_STORAGE_MODE=url  # 'url' o 'local'
MAX_FILE_SIZE_MB=50

# Google Calendar (futuro)
GOOGLE_CALENDAR_CREDENTIALS_FILE=path/to/credentials.json
GOOGLE_CALENDAR_CALENDAR_ID=YOUR_CALENDAR_ID_HERE
```

#### 1.2 **NUEVO**: Configurar base Airtable "ACA - Gestión Documental"
```bash
# Crear base Airtable con columnas:
# - Empresa (Select)
# - Fecha subida (Date)
# - Tipo documento (Select: Balance, Resultados, Legal, etc.)
# - Archivo adjunto (Attachment)
# - Estado subida (Select: Pendiente, Procesado, Error)
# - Comentarios (Long text)
```

#### 1.3 **NUEVO**: Configurar permisos y acceso contador
- Invitar contador con acceso Editor a tabla específica
- Configurar vistas filtradas por empresa
- Crear formularios de subida simplificados

#### 1.4 Crear rama `future-features` y documentar tablas no utilizadas
```bash
git checkout -b future-features
# Documentar en docs/future_features.md las 4 tablas:
# - cuentas_cobrar, cuentas_pagar, citas, security_logs
```

#### 1.5 Crear archivo de disclaimers/checklist
- Actualizar `README.md` con sección "✅ CHECKLIST ANTES DE EJECUTAR"
- Variables obligatorias vs opcionales
- Dependencias del sistema

#### 1.6 Consolidar documentación
- Actualizar `docs/architecture.md` con arquitectura multi-plataforma
- Crear `docs/database_real_state.md` con estructura actual

---

### **FASE 2 - ORM + ESTRUCTURA NOTION** ⏱️ *4-6 horas*

#### 2.1 Crear `app/models.py` con SQLModel
```python
# Modelos para TODAS las tablas que realmente usamos:
# - Empresa, Usuario, Conversacion, ReporteMensual, InfoCompania
# - ArchivoReporte, ComentarioReporte, ArchivoInfoCompania
# - SyncLog, PlatformMapping (nuevas para sincronización)
```

#### 2.2 Instalar y configurar Alembic + nuevas dependencias
```bash
pip install alembic sqlmodel
# Airtable
pip install pyairtable
# Notion  
pip install notion-client
# Slack (actualizado)
pip install slack-sdk slack-bolt
# Automatización
pip install schedule asyncio-cron
# Monitoreo
pip install loguru prometheus-client
```

#### 2.3 **NUEVO**: Crear workspace Notion "ACA - Empresas"
```bash
# Crear estructura Notion:
# 1. Database principal "Empresas ACA"
# 2. Templates por empresa:
#    - Dashboard ejecutivo (KPIs, gráficos)
#    - Reportes mensuales (por año/mes)
#    - Información legal (documentos, contratos)
#    - Información financiera (balances, P&L)
#    - Información tributaria (declaraciones, retenciones)
```

#### 2.4 **NUEVO**: Configurar databases y templates Notion
- Database "Reportes Mensuales" con propiedades empresa, mes, año, tipo
- Database "Información Compañía" con categorías (Legal, Financiera, Tributaria)
- Template página empresa con secciones organizadas
- Vistas filtradas por empresa automáticas

#### 2.5 Primera migración - Estado actual
```bash
# Crear migración que refleje el estado ACTUAL de la BD
alembic revision --autogenerate -m "initial_database_state"
```

#### 2.6 Adaptar código existente para usar ORM
- Modificar `app/database/supabase.py` para usar modelos
- Actualizar handlers para usar ORM en lugar de queries directas

---

### **FASE 3 - AUTOMATIZACIONES PYTHON** ⏱️ *5-7 horas*

#### 3.1 **NUEVO**: Script Airtable → Supabase (`sync_airtable.py`)
```python
from pyairtable import Table
from supabase import create_client

class AirtableSync:
    def sync_to_supabase(self):
        # Leer registros de Airtable
        # Procesar archivos adjuntos (URL o descarga)
        # Insertar/actualizar en Supabase
        # Log de sincronización
```

#### 3.2 **NUEVO**: Script Supabase → Notion (`sync_notion.py`)
```python
from notion_client import Client
from supabase import create_client

class NotionSync:
    def sync_from_supabase(self):
        # Leer reportes e info de Supabase
        # Crear/actualizar páginas en Notion
        # Organizar por empresa y categoría
        # Mantener mapeo de IDs
```

#### 3.3 **NUEVO**: Gestión de archivos (URL vs Storage local)
```python
class FileManager:
    def handle_file_storage(self, file_url, mode='url'):
        if mode == 'url':
            # Solo guardar URL de Airtable
        elif mode == 'local':
            # Descargar y subir a Supabase Storage
```

#### 3.4 **NUEVO**: Cron jobs para sincronización automática
```python
import schedule
import asyncio

# Ejecutar cada 30 minutos
schedule.every(30).minutes.do(sync_complete_flow)

# Orquestador principal
async def sync_complete_flow():
    # 1. Airtable → Supabase
    # 2. Supabase → Notion  
    # 3. Notificaciones Slack/Telegram
    # 4. Log y monitoreo
```

#### 3.5 Optimización BD (índices, constraints)
```sql
-- Índices para performance:
CREATE INDEX idx_usuarios_chat_id ON usuarios(chat_id);
CREATE INDEX idx_usuarios_empresa_id ON usuarios(empresa_id);
CREATE INDEX idx_reportes_empresa_periodo ON reportes_mensuales(empresa_id, anio, mes);
CREATE INDEX idx_archivos_reporte_empresa ON archivos_reportes(empresa_id);
CREATE INDEX idx_platform_mappings_lookup ON platform_mappings(empresa_id, record_type);
```

#### 3.6 Testing de sincronización completa
- Testing Airtable → Supabase
- Testing Supabase → Notion
- Testing notificaciones automáticas
- Validación integridad datos

---

### **FASE 4 - INTEGRACIÓN SLACK + TELEGRAM** ⏱️ *4-5 horas*

#### 4.1 Configurar Slack App completa
```bash
# Crear app en Slack workspace
# Obtener tokens necesarios:
# - Bot User OAuth Token (xoxb-)
# - Signing Secret  
# - App Token (xapp-) para Socket Mode
# - Workspace ID para identificación
```

#### 4.2 Implementar SlackService completo
```python
# app/services/slack_service.py
class SlackService:
    def __init__(self):
        self.client = WebClient(token=Config.SLACK_BOT_TOKEN)
        self.enabled = True
    
    def send_message(self, channel, text):
        # Enviar mensajes a Slack
    
    def create_empresa_channel(self, empresa_name):
        # Crear canal dedicado por empresa
    
    def notify_new_report(self, empresa, reporte):
        # Notificación automática nuevos reportes
    
    def handle_bot_commands(self, command):
        # Manejar comandos desde Slack
```

#### 4.3 Integrar notificaciones automáticas
```python
# Notificaciones inteligentes:
# - Nuevo archivo subido en Airtable → Slack + Telegram
# - Reporte procesado en Notion → Slack + Telegram  
# - Error en sincronización → Slack admin
# - Alertas por empresa en canales dedicados
```

#### 4.4 Canales dedicados por empresa en Slack
```python
# Crear automáticamente:
# - #empresa-{nombre}-general
# - #empresa-{nombre}-reportes  
# - #empresa-{nombre}-alertas
# Invitar automáticamente usuarios según empresa_id
```

#### 4.5 Bot commands bidireccionales
```python
# Comandos disponibles en Slack:
# /aca-reportes {empresa} {mes}
# /aca-info {empresa} {categoria}
# /aca-status
# /aca-sync

# Mantener comandos Telegram existentes
# Sincronización de respuestas entre plataformas
```

#### 4.6 Mantener funcionalidad Telegram + testing
- Asegurar que Telegram sigue funcionando como antes
- Testing integración multi-plataforma
- Validación notificaciones cruzadas

### **FASE 5 - DASHBOARD WEB + ORQUESTACIÓN** ⏱️ *3-4 horas*

#### 5.1 Expandir FastAPI con endpoints multi-plataforma
```python
# Nuevos endpoints:
# /integrations/status - Estado todas las plataformas
# /integrations/airtable/sync - Forzar sync Airtable
# /integrations/notion/sync - Forzar sync Notion
# /integrations/slack/status - Estado Slack
# /sync/full - Sincronización completa manual
```

#### 5.2 Dashboard admin para gestión sincronizaciones
```html
# Dashboard web con:
# - Estado en tiempo real todas las integraciones
# - Logs de sincronización por plataforma
# - Botones sync manual por empresa
# - Métricas de archivos procesados
# - Alertas y errores centralizados
```

#### 5.3 Monitoreo estado todas las integraciones
```python
class IntegrationMonitor:
    def check_airtable_status(self):
        # Verificar conectividad y última sync
    
    def check_notion_status(self):
        # Verificar API y páginas actualizadas
    
    def check_slack_status(self):
        # Verificar bot online y canales
    
    def generate_health_report(self):
        # Reporte consolidado estado sistema
```

#### 5.4 Logs centralizados y alertas
```python
# Usar loguru para logs estructurados
# Alertas automáticas por email/Slack en errores
# Métricas Prometheus para monitoreo
# Dashboard Grafana (opcional)
```

#### 5.5 Documentación completa usuario final
- Guías para contadores (Airtable)
- Guías para dueños (Notion)
- Manual de comandos Slack/Telegram
- Troubleshooting común

---

## 🗄️ **ESTRUCTURA DE DATOS ACTUALIZADA**

### **Nuevas Tablas Requeridas**

```sql
-- Tabla para sincronizaciones multi-plataforma
CREATE TABLE sync_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sync_type VARCHAR(50) NOT NULL, -- 'airtable_supabase', 'supabase_notion'
    source_platform VARCHAR(20) NOT NULL,
    target_platform VARCHAR(20) NOT NULL,
    records_processed INTEGER DEFAULT 0,
    records_successful INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'running', -- 'running', 'completed', 'failed'
    error_details TEXT,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    created_by VARCHAR(100)
);

-- Tabla para mapeo de IDs entre plataformas
CREATE TABLE platform_mappings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id UUID REFERENCES empresas(id),
    airtable_record_id VARCHAR(100),
    notion_page_id VARCHAR(100),
    supabase_record_id UUID,
    record_type VARCHAR(50), -- 'reporte', 'archivo', 'info_compania'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🚨 DECISIONES CRÍTICAS ACTUALIZADAS

### **A) ¿Almacenamiento de archivos?**
**Opciones:**
1. **🟢 URL Reference** (Simple): Solo URLs de Airtable en Supabase
2. **🟡 Hybrid**: URLs + copia local en Supabase Storage  
3. **🔴 Full Local**: Descargar todo a Supabase Storage

### **B) ¿Frecuencia de sincronización?**
**Opciones:**
1. **🟢 Real-time**: Webhooks + triggers inmediatos
2. **🟡 Programada**: Cada 30 minutos (RECOMENDADO)
3. **🔴 Manual**: Solo cuando se ejecute script

### **C) ¿Prioridad de plataformas?**
**Opciones:**
1. **🟢 RECOMENDADO**: Airtable → Notion (core business)
2. **🟡 PARALELO**: Slack + Telegram (notificaciones)
3. **🔴 SECUENCIAL**: Una plataforma por vez

### **D) ¿Qué hacer con las tablas "futuras"?**
**Opciones:**
1. **🟢 RECOMENDADO**: Dejarlas pero marcarlas como "no implementadas" en docs
2. **🟡 ALTERNATIVA**: Crear migration para eliminarlas temporalmente
3. **🔴 NO RECOMENDADO**: Eliminarlas definitivamente

---

## ⚡ CRONOGRAMA INTEGRADO MULTI-PLATAFORMA

### **SEMANA 1: IMPLEMENTACIÓN COMPLETA**

| Día | Fases | Tiempo | Entregables Principales |
|-----|-------|--------|-------------------------|
| **Lunes** | ✅ FASE 0 + FASE 1 | 6h | Seguridad BD + Base Airtable + Env Variables |
| **Martes** | 🔄 FASE 2 | 6h | ORM SQLModel + Workspace Notion + Templates |
| **Miércoles** | 🔄 FASE 3.1-3.4 | 6h | Scripts Airtable→Supabase + Supabase→Notion |
| **Jueves** | 🔄 FASE 3.5-3.6 + FASE 4.1-4.3 | 6h | Automatización + Slack Service + Notificaciones |
| **Viernes** | 🔄 FASE 4.4-4.6 + FASE 5 | 6h | Slack completo + Dashboard + Testing final |

### **SEMANA 2: REFINAMIENTO (Opcional)**
- **Lunes**: Optimizaciones performance + Google Calendar
- **Martes**: Funcionalidades avanzadas Slack + Webhooks
- **Miércoles**: Deploy producción + Monitoreo
- **Jueves**: Documentación usuario + Training
- **Viernes**: Testing integral + Go Live

### **TIEMPO TOTAL ESTIMADO: 5-7 días hábiles**

---

## 📋 TODOs INTEGRADOS MULTI-PLATAFORMA

### **🚨 TODOs Críticos (FASE 0) - HOY**
- [ ] **🔴 CRÍTICO**: Agregar `empresa_id` a `archivos_reportes` y `archivos_info_compania` - Falla de seguridad
- [ ] **🟡 Datos**: Poblar tablas vacías con datos de prueba para testing funcional  
- [ ] **🔧 Código**: Actualizar métodos en `supabase.py` para validar `empresa_id` en archivos

### **📊 TODOs Airtable (FASE 1)**
- [ ] **🆕 Setup**: Crear base Airtable "ACA - Gestión Documental" con columnas estructuradas
- [ ] **👤 Permisos**: Configurar acceso contador con vistas filtradas por empresa
- [ ] **📝 Variables**: Actualizar env.example con tokens Airtable, Notion, Slack

### **📝 TODOs Notion (FASE 2)**
- [ ] **🆕 Workspace**: Crear workspace Notion "ACA - Empresas" con estructura organizada
- [ ] **📋 Templates**: Diseñar templates por empresa (Dashboard, Reportes, Legal, Financiera)
- [ ] **🗃️ Databases**: Configurar databases Notion con propiedades y vistas automáticas

### **🔄 TODOs Sincronización (FASE 3)**
- [ ] **📊→🗄️ Script**: Desarrollar sync_airtable.py (Airtable → Supabase)
- [ ] **🗄️→📝 Script**: Desarrollar sync_notion.py (Supabase → Notion)
- [ ] **📁 Archivos**: Implementar gestión archivos (URL vs Storage local)
- [ ] **⏰ Cron**: Configurar jobs automáticos cada 30 minutos
- [ ] **🔍 Logs**: Sistema logging para todas las sincronizaciones

### **💬 TODOs Slack + Telegram (FASE 4)**
- [ ] **🆕 App**: Configurar Slack App con todos los tokens necesarios
- [ ] **🤖 Service**: Implementar SlackService completo con notificaciones
- [ ] **🏢 Canales**: Crear canales automáticos por empresa
- [ ] **🔔 Notificaciones**: Integrar notificaciones Airtable→Slack+Telegram
- [ ] **📱 Commands**: Bot commands bidireccionales en ambas plataformas

### **🌐 TODOs Dashboard (FASE 5)**
- [ ] **🔗 Endpoints**: Expandir FastAPI con endpoints multi-plataforma
- [ ] **📊 Dashboard**: Panel admin para monitoreo todas las integraciones
- [ ] **📈 Monitoreo**: Sistema health check todas las plataformas
- [ ] **📖 Docs**: Documentación completa usuario final

### **🔵 TODOs Estructurales (FASE 1-2)**
- [ ] **🏗️ ORM**: Implementar SQLModel para todas las tablas
- [ ] **🔄 Migrations**: Sistema Alembic con migración inicial
- [ ] **📊 Índices**: Optimización BD para consultas multi-plataforma
- [ ] **🗃️ Nuevas Tablas**: sync_logs y platform_mappings

### **✅ TODOs Completados**
- [x] **🔍 Inspección**: Inspección completa de Supabase - Realizada exitosamente
- [x] **📋 Análisis**: Análisis BD vs MVP con identificación fallas críticas
- [x] **📝 Plan**: Plan integrado multi-plataforma completo documentado

---

## 🎪 PREGUNTAS CRÍTICAS MULTI-PLATAFORMA

### **🚨 INMEDIATAS - SEGURIDAD (Hoy)**
1. **🔴 ¿Empezamos YA con FASE 0 (correcciones críticas de seguridad) mientras configuras las otras plataformas?**
2. **📁 ¿Prefieres almacenar archivos por URL (simple) o copiar a Supabase Storage (seguro)?**

### **📊 AIRTABLE - CONTADOR**
3. **🏢 ¿Ya tienes cuenta Airtable o necesitas que te ayude a crearla?**
4. **👤 ¿El contador está listo para empezar a usar Airtable o necesita training?**
5. **📝 ¿Qué tipos de documentos maneja principalmente? (Balance, P&L, Legal, Tributario, etc.)**

### **📝 NOTION - DUEÑO EMPRESA**
6. **📋 ¿Tienes workspace Notion configurado o necesitas ayuda con setup inicial?**
7. **📊 ¿Qué KPIs/métricas son más importantes para el dashboard ejecutivo?**
8. **🎨 ¿Tienes preferencias de diseño/organización para las páginas Notion?**

### **💬 SLACK - EQUIPOS**
9. **🏢 ¿Ya tienes Slack workspace donde podemos integrar o creamos uno nuevo?**
10. **🔔 ¿Qué notificaciones son prioritarias?**
    - Nuevos reportes subidos
    - Errores de sincronización  
    - Alertas por empresa
    - Comandos de consulta

### **⏰ TIMING Y PRIORIDADES**
11. **📅 ¿El cronograma de 5-7 días te parece adecuado para esta integración completa?**
12. **🎯 ¿Qué plataforma es MÁS urgente implementar primero?**
    - Airtable (contador subir archivos)
    - Notion (dueño ver dashboard)
    - Slack (notificaciones equipo)
13. **🔄 ¿Prefieres sincronización cada 30 min (recomendado) o tiempo real (complejo)?**

### **🔧 TÉCNICAS**
14. **💻 ¿Quieres ver prototipos/demos antes de implementación completa?**
15. **📖 ¿Necesitas documentación técnica o solo guías de usuario?**

---

## 🎯 **FLUJO DE DECISIÓN RECOMENDADO**

### **OPCIÓN A - PARALELO (Más Eficiente)**
- **YO**: Empiezo FASE 0 (seguridad) + preparar estructura código
- **TÚ**: Configuras cuentas Airtable + Notion + Slack en paralelo  
- **LUEGO**: Integramos todo de forma coordinada

### **OPCIÓN B - SECUENCIAL (Más Seguro)**
- Primero definimos y configuramos todas las plataformas externas
- Luego ejecutamos implementación completa paso a paso

### **OPCIÓN C - GRADUAL (Más Controlado)**
- Empezamos solo con Airtable → Supabase
- Agregamos Notion cuando esté funcionando
- Finalmente integramos Slack + refinamientos

---

**🚀 ESTADO: PLAN MULTI-PLATAFORMA INTEGRADO COMPLETO**  
**📋 DOCUMENTACIÓN: Totalmente actualizada con nuevas integraciones**  
**⚡ LISTO: Para ejecutar en cuanto definas prioridades y configuraciones**  
**👨‍💻 ESPERANDO: Confirmación de enfoque y respuestas a preguntas críticas**