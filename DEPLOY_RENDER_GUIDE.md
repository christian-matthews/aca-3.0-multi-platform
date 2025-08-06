# 🚀 Guía Deploy ACA 3.0 en Render

## 📋 **PASO A PASO COMPLETO**

### **1. Preparación Completada ✅**
- [x] Código subido a GitHub: `https://github.com/christian-matthews/aca-3.0-multi-platform.git`
- [x] Procfile configurado
- [x] render.yaml con configuración
- [x] requirements.txt actualizado
- [x] runtime.txt especificando Python 3.9.6

---

## **2. 🔗 CONECTAR GITHUB A RENDER**

### **2.1. Crear cuenta Render**
1. Ve a: https://render.com
2. Crea cuenta o inicia sesión
3. Conecta tu cuenta GitHub

### **2.2. Crear nuevo Web Service**
1. Click **"New +"** → **"Web Service"**
2. Conecta GitHub repository: `christian-matthews/aca-3.0-multi-platform`
3. Selecciona **branch: main**

---

## **3. ⚙️ CONFIGURACIÓN WEB SERVICE**

### **3.1. Configuración Básica**
```
Name: aca-3-0-backend
Region: Oregon (US West)
Branch: main
Root Directory: (dejar vacío)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

### **3.2. Variables de Entorno Requeridas**
**⚠️ CRÍTICO: Configura estas variables antes del deploy**

#### **Variables de Base de Datos:**
```bash
# SUPABASE (Requerido)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

#### **Variables Telegram Bots:**
```bash
# TELEGRAM (Requerido)
TELEGRAM_BOT_TOKEN_ADMIN=your-admin-bot-token
TELEGRAM_BOT_TOKEN_PROD=your-production-bot-token
```

#### **Variables APIs Externas:**
```bash
# OPENAI (Requerido para IA)
OPENAI_API_KEY=your-openai-api-key

# AIRTABLE (Requerido para sincronización)
AIRTABLE_API_KEY=your-airtable-api-key
AIRTABLE_BASE_ID=your-base-id
AIRTABLE_TABLE_NAME=Reportes_Empresas_CL
AIRTABLE_VIEW_NAME=Pendientes

# GOOGLE CALENDAR (Opcional)
GOOGLE_CALENDAR_CREDENTIALS_FILE=/app/credentials/google_calendar.json

# CALENDLY (Opcional)
CALENDLY_API_TOKEN=your-calendly-token
```

#### **Variables de Configuración:**
```bash
# APLICACIÓN
DEBUG=false
PORT=10000
ENVIRONMENT=production

# SINCRONIZACIÓN
SYNC_INTERVAL_MINUTES=30
MAX_FILE_SIZE_MB=50
AUTO_SYNC_ENABLED=true
```

---

## **4. 🔐 CONFIGURAR VARIABLES EN RENDER**

### **4.1. En Render Dashboard:**
1. Ve a tu Web Service
2. Click **"Environment"** tab
3. Agrega cada variable una por una:
   - **Key**: Nombre variable (ej: `SUPABASE_URL`)
   - **Value**: Valor real (ej: `https://xxx.supabase.co`)
   - Click **"Add"**

### **4.2. Variables Críticas - NO FALLAR:**
```bash
✅ SUPABASE_URL
✅ SUPABASE_ANON_KEY
✅ TELEGRAM_BOT_TOKEN_ADMIN
✅ TELEGRAM_BOT_TOKEN_PROD
✅ OPENAI_API_KEY
✅ AIRTABLE_API_KEY
✅ AIRTABLE_BASE_ID
```

---

## **5. 🚀 DEPLOY**

### **5.1. Iniciar Deploy:**
1. Después de configurar variables
2. Click **"Create Web Service"**
3. Render automáticamente:
   - Clona el repositorio
   - Instala dependencias
   - Ejecuta el build
   - Inicia la aplicación

### **5.2. Monitorear Deploy:**
```bash
# Logs en tiempo real en Render
- Build logs: Instalación dependencias
- Runtime logs: Ejecución aplicación
- Error logs: Si hay problemas
```

---

## **6. 🔍 VERIFICAR FUNCIONAMIENTO**

### **6.1. URLs de tu aplicación:**
```bash
# Render te dará una URL como:
https://aca-3-0-backend.onrender.com

# Endpoints principales:
GET  /                    → Dashboard principal
GET  /health             → Health check
GET  /dashboard          → Dashboard web
POST /api/sync/airtable  → Sincronización manual
GET  /api/status         → Estado sistema
```

### **6.2. Tests rápidos:**
```bash
# 1. Health check
curl https://aca-3-0-backend.onrender.com/health

# 2. Dashboard
https://aca-3-0-backend.onrender.com/dashboard

# 3. API Status
curl https://aca-3-0-backend.onrender.com/api/status
```

---

## **7. 🐛 TROUBLESHOOTING**

### **7.1. Errores Comunes:**

#### **Error: "Application failed to start"**
```bash
Causa: Variables de entorno faltantes
Solución: Verificar todas las variables críticas
```

#### **Error: "ModuleNotFoundError"**
```bash
Causa: Dependencia faltante en requirements.txt
Solución: Verificar requirements.txt
```

#### **Error: "Database connection failed"**
```bash
Causa: SUPABASE_URL o SUPABASE_ANON_KEY incorrectos
Solución: Verificar credenciales Supabase
```

### **7.2. Logs de Debug:**
```bash
# En Render Dashboard:
1. Ve a "Logs" tab
2. Busca errores específicos
3. Verifica mensajes de inicio:
   - "🚀 Iniciando ACA 3.0..."
   - "✅ Configuración validada correctamente"
   - "🤖 Iniciando bots de Telegram..."
```

---

## **8. 🔄 REDEPLOY AUTOMÁTICO**

### **8.1. Auto-Deploy configurado:**
- Cualquier push a `main` → Redeploy automático
- Render detecta cambios
- Rebuild automático

### **8.2. Deploy manual:**
```bash
# En Render Dashboard:
1. Click "Manual Deploy"
2. Selecciona branch
3. Click "Deploy"
```

---

## **9. 📊 MONITOREO POST-DEPLOY**

### **9.1. Métricas importantes:**
```bash
- Response time
- Memory usage
- CPU usage
- Error rate
```

### **9.2. Health checks:**
```bash
# Render automáticamente hace health checks a:
GET /health

# Debe responder:
{"status": "healthy", "timestamp": "..."}
```

---

## **10. 🎯 NEXT STEPS**

### **10.1. Configuración adicional:**
- [ ] Custom domain (opcional)
- [ ] HTTPS certificate (automático)
- [ ] Database backups
- [ ] Monitoring alerts

### **10.2. Optimizaciones:**
- [ ] CDN para archivos estáticos
- [ ] Redis para cache (opcional)
- [ ] Background workers para tareas pesadas

---

## **🆘 SOPORTE RÁPIDO**

```bash
# Si algo falla:
1. Revisa logs en Render
2. Verifica variables de entorno
3. Comprueba GitHub repository
4. Test endpoints manualmente
```

**🎉 ¡Una vez configurado, tu aplicación ACA 3.0 estará disponible 24/7 en la nube!**