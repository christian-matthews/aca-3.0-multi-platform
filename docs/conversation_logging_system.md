# 📊 Sistema de Logging de Conversaciones - ACA 3.0

## 🎯 Descripción General

El sistema de logging de conversaciones de ACA 3.0 captura y registra **todas** las interacciones con los bots de Telegram, incluyendo usuarios autorizados y no autorizados, proporcionando visibilidad completa del uso del sistema.

## 🔧 Componentes Implementados

### 1. **Base de Datos**
```sql
-- Tablas principales
- conversaciones: Registro de todas las conversaciones
- usuarios_detalle: Información completa de usuarios
- intentos_acceso_negado: Registro de accesos no autorizados
- bot_analytics: Métricas y estadísticas

-- Vistas
- vista_conversaciones_recientes: Conversaciones con información completa
- vista_usuarios_sin_acceso: Usuarios no autorizados
```

### 2. **Servicios Python**
- `ConversationLogger`: Servicio principal de logging
- `log_conversacion_simple()`: Función SQL para inserción eficiente
- Decoradores automáticos para handlers de bots

### 3. **Dashboard Web**
- `/dashboard/conversaciones`: Vista de todas las conversaciones
- `/dashboard/usuarios-no-autorizados`: Usuarios sin permisos
- APIs REST para consultas dinámicas

## 🚀 Características Principales

### ✅ **Logging Automático**
- **Usuarios autorizados**: Se registran automáticamente con empresa vinculada
- **Usuarios no autorizados**: Se capturan y almacenan para análisis
- **Decoradores**: `@log_production_conversation`, `@log_admin_conversation`
- **Sin impacto**: El logging no afecta la funcionalidad normal

### ✅ **Botones de Contacto Directo**
- **URL directa**: `https://t.me/wingmanbod`
- **Integración automática**: Aparece en mensajes de acceso denegado
- **UX mejorada**: Un clic para abrir chat directo

### ✅ **Datos Capturados**
```json
{
  "chat_id": 123456789,
  "user_id": 987654321,
  "usuario_nombre": "Juan Pérez",
  "usuario_username": "juanperez",
  "mensaje": "Texto del mensaje",
  "respuesta": "Respuesta del bot",
  "bot_tipo": "production|admin",
  "empresa_id": "uuid|null",
  "tiene_acceso": true|false,
  "timestamp": "2025-01-01T10:30:00Z"
}
```

## 📊 Dashboard de Conversaciones

### **Vista Principal**
- **Tabla dinámica**: Conversaciones en tiempo real
- **Filtros**: Por bot, usuario, fecha, estado
- **Búsqueda**: Por chat_id, mensaje, usuario
- **Auto-refresh**: Actualización automática cada 30 segundos

### **Información Mostrada**
- **Usuario**: Nombre completo y username
- **IDs**: Chat ID y User ID de Telegram
- **Empresa**: Empresa vinculada (si aplica)
- **Mensaje**: Texto enviado por el usuario
- **Respuesta**: Respuesta del bot
- **Estado**: Autorizado/No Autorizado
- **Timestamp**: Fecha y hora exacta

## 🔐 Usuarios No Autorizados

### **Detección Automática**
- Se detectan usuarios que intentan usar el bot sin permisos
- Se registra información completa para análisis
- Se envía mensaje explicativo con botón de contacto

### **Información Capturada**
- Datos de perfil de Telegram
- Historial de intentos
- Mensajes enviados
- Timestamp de cada intento

### **Acciones Disponibles**
- **Ver historial**: Conversaciones del usuario específico
- **Bloquear**: Marcar usuario como bloqueado
- **Contactar**: Información para seguimiento manual

## 🚀 APIs REST

### **Endpoints Principales**
```http
GET /api/conversations/recent?limit=50&bot_type=production
GET /api/conversations/unauthorized?days=7
GET /api/conversations/analytics?days=30
GET /api/conversations/user-history/{chat_id}
POST /api/conversations/block/{chat_id}
```

### **Parámetros Comunes**
- `limit`: Número de registros (1-200)
- `days`: Rango de días (1-365)
- `bot_type`: Filtro por tipo de bot
- `chat_id`: ID específico de usuario

## 🔄 Integración con Bots

### **Producción Bot**
```python
@log_production_conversation
async def handle_message(update, context):
    # Lógica del handler
    # El logging es automático
```

### **Admin Bot**
```python
@log_admin_conversation  
async def start_command(update, context):
    # Lógica del handler
    # El logging es automático
```

### **Acceso Denegado**
```python
@log_unauthorized_access()
async def _handle_unauthorized_user(update, context):
    # Se registra automáticamente
    # Se envía mensaje con botón de contacto
```

## 📈 Métricas y Analytics

### **Estadísticas Disponibles**
- **Conversaciones por día**: Tendencias de uso
- **Usuarios únicos**: Alcance del sistema  
- **Intentos no autorizados**: Seguridad
- **Distribución por bot**: Admin vs Producción
- **Empresas más activas**: Análisis de uso

### **Exportación de Datos**
- **CSV**: Para análisis externo
- **JSON**: Para integraciones
- **Dashboard**: Visualización en tiempo real

## 🛠️ Configuración

### **Variables de Entorno**
```env
SUPABASE_SERVICE_KEY=your_service_key  # Para bypass RLS
TELEGRAM_BOT_TOKEN_ADMIN=bot_token
TELEGRAM_BOT_TOKEN_PROD=bot_token
```

### **Base de Datos**
1. Ejecutar migraciones en `/database/migrations/`
2. Crear función `log_conversacion_simple()`
3. Configurar vistas para dashboard

## 🔒 Seguridad y Privacidad

### **Cumplimiento**
- **GDPR**: Datos mínimos necesarios
- **Telegram ToS**: Cumplimiento de términos
- **Anonimización**: Posible para análisis

### **Acceso a Datos**
- **Service Key**: Solo para logging automatizado
- **RLS**: Protección en consultas manuales
- **Logs**: Rotación automática configurada

## 📋 Próximas Mejoras

### **Funcionalidades Planificadas**
- [ ] Alertas automáticas por usuarios sospechosos
- [ ] Integración con Slack para notificaciones
- [ ] Machine Learning para detección de spam
- [ ] API webhooks para integraciones externas
- [ ] Dashboard móvil optimizado

### **Optimizaciones**
- [ ] Indexado avanzado para consultas rápidas
- [ ] Compresión de mensajes largos
- [ ] Archivado automático de conversaciones antiguas
- [ ] Cache Redis para métricas frecuentes

---

**📞 Soporte**: Para dudas sobre el sistema de logging, contactar a @wingmanbod

**🔗 Enlaces útiles**:
- Dashboard: `/dashboard/conversaciones`
- API Docs: `/docs#conversation-logs`
- Código fuente: `/app/services/conversation_logger.py`