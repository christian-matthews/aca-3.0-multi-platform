# 📅 Configuración de Calendly - ACA 3.0

## ¿Qué es Calendly?

Calendly es una plataforma de programación de reuniones que permite a los usuarios programar citas automáticamente sin necesidad de intercambiar correos electrónicos.

## 🚀 Ventajas de Calendly

- ✅ **Interfaz web integrada** - No necesita app adicional
- ✅ **Sincronización automática** con Google Calendar, Outlook, etc.
- ✅ **Personalización completa** de tipos de reuniones
- ✅ **API robusta** para integración
- ✅ **Notificaciones automáticas** por email y SMS
- ✅ **Analytics** de reuniones programadas

## 🔧 Configuración Paso a Paso

### **Paso 1: Crear cuenta en Calendly**

1. Ve a [calendly.com](https://calendly.com)
2. Haz clic en "Sign up for free"
3. Crea una cuenta con tu email
4. Completa el perfil básico

### **Paso 2: Configurar tipos de eventos**

1. **Crear tipos de reuniones:**
   - Consulta inicial (15 min)
   - Revisión de documentos (30 min)
   - Asesoría contable (45 min)
   - Planificación financiera (60 min)

2. **Configurar cada tipo:**
   - Nombre del evento
   - Duración
   - Descripción
   - Ubicación (Zoom, Google Meet, etc.)
   - Disponibilidad

### **Paso 3: Obtener API Key**

1. Ve a [Calendly Developer Portal](https://developer.calendly.com/)
2. Crea una cuenta de desarrollador
3. Ve a "API Keys"
4. Genera una nueva API Key
5. Copia la clave (empieza con `cal_`)

### **Paso 4: Configurar en el proyecto**

1. **Editar archivo `.env`:**
   ```bash
   CALENDLY_API_KEY=cal_your_api_key_here
   ```

2. **Verificar configuración:**
   ```bash
   python -c "from app.config import Config; print('✅ Calendly configurado') if Config.CALENDLY_API_KEY else print('❌ Falta CALENDLY_API_KEY')"
   ```

## 📋 Tipos de Eventos Recomendados

### **1. Consulta Inicial (15 min)**
- **Propósito:** Primera reunión con nuevos clientes
- **Duración:** 15 minutos
- **Descripción:** "Consulta inicial para conocer tus necesidades contables"
- **Ubicación:** Zoom

### **2. Revisión de Documentos (30 min)**
- **Propósito:** Revisar documentos y estados financieros
- **Duración:** 30 minutos
- **Descripción:** "Revisión de documentos contables y financieros"
- **Ubicación:** Google Meet

### **3. Asesoría Contable (45 min)**
- **Propósito:** Asesoría especializada en contabilidad
- **Duración:** 45 minutos
- **Descripción:** "Asesoría contable y fiscal personalizada"
- **Ubicación:** Zoom

### **4. Planificación Financiera (60 min)**
- **Propósito:** Planificación financiera y estratégica
- **Duración:** 60 minutos
- **Descripción:** "Planificación financiera y estratégica de tu empresa"
- **Ubicación:** Google Meet

## 🔗 Configuración de Enlaces

### **Enlaces de Programación**

Una vez configurados los tipos de eventos, puedes crear enlaces de programación:

```python
# Ejemplo de creación de enlace
link_data = await calendly_service.create_scheduling_link(
    name="Consulta ACA 3.0",
    event_type_uri="https://api.calendly.com/event_types/XXXXXXXX"
)
```

### **Webhooks (Opcional)**

Para recibir notificaciones cuando se programen eventos:

```python
# Crear webhook
webhook_data = await calendly_service.create_webhook_subscription(
    url="https://tu-app.com/webhook/calendly",
    events=["invitee.created", "invitee.canceled"]
)
```

## 📊 Funcionalidades Disponibles

### **En el Bot de Telegram:**

1. **Ver enlaces disponibles:**
   - Lista de tipos de reuniones
   - Enlaces directos para agendar

2. **Ver eventos programados:**
   - Próximas reuniones
   - Historial de eventos

3. **Cancelar eventos:**
   - Cancelar reuniones programadas
   - Notificar cambios

### **En la API:**

```python
# Obtener información del usuario
user_info = await calendly_service.get_user_info()

# Obtener tipos de eventos
event_types = await calendly_service.get_event_types()

# Obtener eventos programados
events = await calendly_service.get_scheduled_events()

# Cancelar evento
success = await calendly_service.cancel_event(event_uri, "Cliente canceló")
```

## 🎯 Configuración Avanzada

### **Sincronización con Calendarios**

1. **Google Calendar:**
   - Ve a Settings > Connected Calendars
   - Conecta tu cuenta de Google
   - Selecciona calendarios a sincronizar

2. **Outlook:**
   - Conecta tu cuenta de Microsoft
   - Sincroniza calendarios de Outlook

3. **iCal:**
   - Exporta eventos a calendarios locales

### **Personalización de Notificaciones**

1. **Email automático:**
   - Confirmación de cita
   - Recordatorio 24h antes
   - Recordatorio 1h antes

2. **SMS (Premium):**
   - Recordatorios por SMS
   - Confirmaciones por SMS

### **Analytics y Reportes**

1. **Métricas disponibles:**
   - Reuniones programadas
   - Tasa de cancelación
   - Tiempo promedio de reunión
   - Tipos de reuniones más populares

## 🐛 Troubleshooting

### **Error: "API Key inválida"**
```bash
# Verificar que la API Key esté correcta
echo $CALENDLY_API_KEY
```

### **Error: "No se pueden obtener enlaces"**
```bash
# Verificar permisos de la API Key
# Asegurarse de que tenga permisos de lectura
```

### **Error: "No se pueden crear eventos"**
```bash
# Verificar que los tipos de eventos estén configurados
# Asegurarse de que la API Key tenga permisos de escritura
```

## 📚 Recursos Adicionales

- [Calendly API Documentation](https://developer.calendly.com/api-docs/)
- [Calendly Help Center](https://help.calendly.com/)
- [Calendly Developer Portal](https://developer.calendly.com/)

## 🎉 ¡Listo!

Una vez configurado Calendly, los usuarios podrán:

1. **Ver enlaces de programación** en el bot
2. **Agendar reuniones** directamente
3. **Recibir confirmaciones** automáticas
4. **Sincronizar** con sus calendarios
5. **Recibir recordatorios** automáticos

¡El sistema de agendamiento estará completamente funcional! 