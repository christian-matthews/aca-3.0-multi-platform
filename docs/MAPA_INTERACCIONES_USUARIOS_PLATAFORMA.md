# 👥 MAPA DE INTERACCIONES USUARIOS - PLATAFORMA ACA 3.0

## 📋 RESUMEN EJECUTIVO

Este documento mapea **cómo cada tipo de usuario interactúa** con la plataforma ACA 3.0, mostrando el flujo **Frontend → Backend → Base de Datos** y las **estructuras coherentes** entre funcionalidades y permisos de usuarios.

---

## 🎭 TIPOS DE USUARIOS Y ROLES

### **Matriz de Usuarios**

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│   USUARIO TIPO  │   PLATAFORMA    │   PERMISOS      │   OBJETIVO      │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ 🏢 EMPRESA      │ 📱 Telegram     │ 👁️ Solo Lectura │ Consultar datos │
│ (Dueño/Gerente) │ 🌐 Dashboard    │ 📊 Ver reportes │ Tomar decisiones│
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ 📊 CONTADOR     │ 📋 Airtable     │ ✏️ Crear/Editar │ Gestionar docs  │
│ (Externo)       │ 💬 Slack        │ 📤 Subir docs   │ Reportar avances│
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ ⚙️ ADMIN        │ 🌐 Dashboard    │ 🔧 Control Total│ Administrar     │
│ (Tú)            │ 📱 Telegram     │ 👥 Gest. Users  │ Monitorear todo │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

---

## 🏢 USUARIO EMPRESA (Dueño/Gerente)

### **🎯 Objetivos del Usuario Empresa**
- Consultar estado financiero de su empresa
- Ver reportes mensuales y análisis
- Recibir alertas y notificaciones
- Agendar reuniones contables

### **📱 Interacción via Telegram Bot**

```
EMPRESA (Telegram) → BOT PRODUCCIÓN → API BACKEND → SUPABASE
                                                        ↓
                    ← RESPUESTA ←    CONSULTA    ← [empresas]
                                                   [reportes_mensuales]
                                                   [archivos_reportes]
```

#### **Flujo de Consulta por RUT**
```
Usuario escribe: "/reportes 12345678-9"
        ↓
Bot valida formato RUT
        ↓
API busca en: empresas WHERE rut = '12345678-9'
        ↓
Si existe empresa → busca en: reportes_mensuales WHERE empresa_id = 'uuid'
        ↓
Formatea respuesta con IA (OpenAI)
        ↓
Envía respuesta estructurada al usuario
```

#### **Comandos Disponibles para Empresa**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│    COMANDO      │    FUNCIÓN      │  TABLA CONSULTA │   PERMISOS      │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ /reportes RUT   │ Ver reportes    │ reportes_       │ 👁️ Solo lectura │
│                 │ por empresa     │ mensuales       │ (su empresa)    │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ /documentos     │ Listar archivos │ archivos_       │ 👁️ Solo lectura │
│                 │ adjuntos        │ reportes        │ (su empresa)    │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ /estado         │ Estado empresa  │ empresas +      │ 👁️ Solo lectura │
│                 │ completo        │ info_compania   │ (su empresa)    │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ /alertas        │ Notificaciones  │ configuración   │ ✏️ Sus alertas  │
│                 │ personalizadas  │ personal        │ únicamente      │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### **🌐 Interacción via Dashboard Web**

```
EMPRESA (Browser) → DASHBOARD WEB → API ENDPOINTS → SUPABASE
                                                       ↓
                   ← VISTA HTML ←   JSON RESPONSE  ← CONSULTA DB
```

#### **Dashboard Empresarial (Vista Limitada)**
```
┌─────────────────────────────────────────────────────────────┐
│                    🏢 MI EMPRESA                            │
├─────────────────┬─────────────────┬─────────────────────────┤
│   📊 KPIs       │   📈 Gráficos   │     📋 Reportes         │
│                 │                 │                         │
│ • Ingresos Mes  │ • Tendencia     │ • Balance Actual        │
│ • Gastos Mes    │ • Comparativa   │ • Estado Resultados     │
│ • Utilidad      │ • Proyección    │ • Flujo Caja           │
│ • Compliance    │                 │ • Reportes Pendientes   │
├─────────────────┴─────────────────┼─────────────────────────┤
│           📎 DOCUMENTOS           │    🗓️ PRÓXIMAS CITAS    │
│                                   │                         │
│ • Facturas Pendientes            │ • Reunión Contador       │
│ • Documentos Tributarios         │ • Revisión Mensual       │
│ • Certificados                   │ • Declaración Anual      │
└───────────────────────────────────┴─────────────────────────┘
```

#### **Permisos Empresa en Dashboard**
```
✅ PUEDE VER:
   - Sus propios reportes financieros
   - Archivos de su empresa únicamente  
   - Estadísticas de su empresa
   - Cronograma de citas agendadas

❌ NO PUEDE VER:
   - Datos de otras empresas
   - Panel administrativo
   - Configuración del sistema
   - Información de otros usuarios

✅ PUEDE HACER:
   - Descargar sus reportes
   - Agendar citas
   - Configurar notificaciones personales
   - Exportar sus datos

❌ NO PUEDE HACER:
   - Subir documentos (es rol del contador)
   - Editar datos financieros
   - Crear/eliminar reportes
   - Acceso configuración sistema
```

---

## 📊 CONTADOR EXTERNO

### **🎯 Objetivos del Contador**
- Subir documentos contables de múltiples empresas
- Categorizar y organizar información financiera
- Monitorear estado de procesamiento
- Colaborar con el equipo via notificaciones

### **📋 Interacción via Airtable**

```
CONTADOR → AIRTABLE → WEBHOOK → SYNC SERVICE → SUPABASE
                                                    ↓
           ← STATUS UPDATE ←  PROCESAMIENTO  ← VALIDACIÓN
```

#### **Base Airtable para Contador**
```
┌─────────────────────────────────────────────────────────────┐
│                    📋 AIRTABLE BASE                         │
│                "ACA - Gestión Documental"                   │
├─────────────────┬─────────────────┬─────────────────────────┤
│     CAMPO       │      TIPO       │       PROPÓSITO         │
├─────────────────┼─────────────────┼─────────────────────────┤
│ Empresa         │ Text            │ "Nombre (RUT)"          │
│ Fecha Subida    │ Date            │ Fecha documento         │
│ Tipo Documento  │ Select          │ Balance/Estado/Flujo    │
│ Archivo Adjunto │ Attachment      │ PDF/Excel del reporte   │
│ Estado Subida   │ Select          │ Pendiente→Procesado     │
│ Comentarios     │ Long Text       │ Notas del contador      │
│ Moneda          │ Select          │ CLP/COP/MXN/USD         │
│ Período Fiscal  │ Text            │ 2025-01, 2025-Q1       │
└─────────────────┴─────────────────┴─────────────────────────┘
```

#### **Flujo Trabajo Contador**
```
1. CONTADOR RECIBE DOCUMENTOS (email/físico)
                ↓
2. ABRE AIRTABLE → Vista "Pendientes de Subida"
                ↓
3. LLENA FORMULARIO:
   - Selecciona Empresa de lista
   - Elige Tipo Documento  
   - Arrastra archivo PDF/Excel
   - Agrega comentarios
                ↓
4. PRESIONA "SAVE" → Estado: "Pendiente"
                ↓
5. SISTEMA ACA DETECTA → Webhook triggered
                ↓
6. SYNC SERVICE PROCESA:
   - Extrae RUT del nombre empresa
   - Busca empresa en Supabase
   - Crea reporte_mensual
   - Adjunta archivo
                ↓
7. ACTUALIZA AIRTABLE → Estado: "Procesado"
                ↓
8. CONTADOR VE CONFIRMACIÓN → Puede procesar siguiente
```

#### **Vistas Airtable Organizadas**
```
📋 VISTA "Por Procesar"
   ├── Estado = "Pendiente"
   ├── Ordenado por Fecha Subida
   └── Filtro: Archivo adjunto ≠ vacío

📊 VISTA "Por Empresa"  
   ├── Agrupado por Empresa
   ├── Suma de documentos por empresa
   └── Colores por estado

📅 VISTA "Por Período"
   ├── Agrupado por Período Fiscal
   ├── Ordenado por fecha descendente
   └── Vista calendario

✅ VISTA "Procesados"
   ├── Estado = "Procesado"
   ├── Últimos 30 días
   └── Para verificación
```

### **💬 Interacción via Slack**

```
CONTADOR → SLACK CHANNEL → BOT NOTIFICATION → TEAM UPDATES
                                                    ↓
           ← CONFIRMACIÓN ←   AUTO RESPONSE    ← SYNC STATUS
```

#### **Canales Slack para Contador**
```
📢 #aca-uploads
   • Notificaciones automáticas cuando sube documentos
   • Confirmaciones de procesamiento exitoso
   • Alertas si hay errores en documentos
   
👥 #aca-team
   • Colaboración con equipo interno
   • Consultas sobre empresas específicas
   • Coordinación deadlines
   
⚠️ #aca-alerts
   • Alertas compliance vencimientos
   • Documentos faltantes por empresa
   • Recordatorios fechas límite
```

#### **Permisos Contador**
```
✅ PUEDE HACER:
   - Subir documentos múltiples empresas
   - Categorizar tipos de reportes
   - Ver estado procesamiento
   - Recibir notificaciones progreso
   - Colaborar via Slack channels

❌ NO PUEDE HACER:
   - Editar datos financieros en Supabase
   - Acceso dashboard administrativo
   - Ver información otras empresas detallada
   - Modificar configuración sistema

📊 VE EN AIRTABLE:
   - Lista todas las empresas asignadas
   - Histórico documentos subidos
   - Estados de procesamiento
   - Comentarios y feedback sistema

🚫 NO VE:
   - Dashboard financiero completo
   - Información confidencial empresas
   - Configuraciones técnicas
   - Datos de facturación/pagos
```

---

## ⚙️ ADMINISTRADOR (Tú)

### **🎯 Objetivos del Administrador**
- Control total del sistema y usuarios
- Monitoreo en tiempo real
- Configuración y mantenimiento
- Gestión de múltiples países/empresas

### **🌐 Dashboard Administrativo Completo**

```
ADMIN → DASHBOARD FULL → API ADMIN → TODAS LAS TABLAS
                                              ↓
       ← CONTROL TOTAL ← CRUD OPERATIONS ← WRITE ACCESS
```

#### **Vista Dashboard Admin**
```
┌─────────────────────────────────────────────────────────────┐
│                    ⚙️ PANEL ADMINISTRADOR                   │
├─────────────────┬─────────────────┬─────────────────────────┤
│   🌍 GLOBAL     │   📊 ANALYTICS  │     🔧 CONFIGURACIÓN    │
│                 │                 │                         │
│ • 3 Países      │ • 45 Empresas   │ • Usuarios & Roles      │
│ • 127 Empresas  │ • 234 Reportes  │ • Integraciones APIs    │
│ • 15 Contadores │ • 89% Uptime    │ • Backup & Security     │
│ • 5 Admins      │ • 2.3s Avg      │ • Compliance Rules      │
├─────────────────┼─────────────────┼─────────────────────────┤
│   🔄 SYNC       │   ⚠️ ALERTAS    │     👥 GESTIÓN USERS    │
│                 │                 │                         │
│ • Airtable ✅   │ • 3 Pendientes  │ • Crear nuevos usuarios │
│ • Notion ✅     │ • 1 Crítica     │ • Asignar permisos      │
│ • Slack ✅      │ • 0 Errores     │ • Monitorear actividad  │
│ • Calendly ✅   │                 │ • Gestionar empresas    │
└─────────────────┴─────────────────┴─────────────────────────┘
```

#### **Vistas Administrativas Especializadas**

**1. 🏢 Gestión Empresas**
```
┌─────────────────────────────────────────────────────────────┐
│  EMPRESA         │ PAÍS │ ESTADO │ REPORTES │ CONTADOR      │
├─────────────────────────────────────────────────────────────┤
│ 🇨🇱 Empresa A    │  CL  │   ✅   │   12/12  │ Contador 1    │
│ 🇨🇴 Empresa B    │  CO  │   ⚠️   │   10/12  │ Contador 2    │
│ 🇲🇽 Empresa C    │  MX  │   ✅   │   12/12  │ Contador 1    │
│ 🇨🇱 Empresa D    │  CL  │   ❌   │    8/12  │ Sin asignar   │
└─────────────────────────────────────────────────────────────┘
```

**2. 📊 Centro de Sincronización**
```
┌─────────────────────────────────────────────────────────────┐
│ SERVICIO   │ ÚLTIMA SYNC │ ESTADO │ REGISTROS │ ERRORES      │
├─────────────────────────────────────────────────────────────┤
│ Airtable   │ 10:30 AM    │   ✅   │    15     │      0       │
│ Notion     │ 10:25 AM    │   ✅   │     8     │      0       │
│ Slack      │ 10:32 AM    │   ✅   │     3     │      0       │
│ Calendly   │ 10:15 AM    │   ⚠️   │     2     │      1       │
└─────────────────────────────────────────────────────────────┘
```

**3. 👥 Gestión Usuarios**
```
┌─────────────────────────────────────────────────────────────┐
│ USUARIO        │ ROL       │ PAÍSES │ ÚLTIMO ACCESO │ ESTADO │
├─────────────────────────────────────────────────────────────┤
│ admin@aca.com  │ Admin     │ CL,CO,MX│ 10:45 AM     │   ✅   │
│ cont1@ext.com  │ Contador  │ CL,CO   │ 09:30 AM     │   ✅   │
│ cont2@ext.com  │ Contador  │ MX      │ 08:15 AM     │   ✅   │
│ emp1@email.com │ Empresa   │ CL      │ Ayer         │   ✅   │
└─────────────────────────────────────────────────────────────┘
```

### **📱 Bot Telegram Admin**

```
ADMIN → TELEGRAM BOT → API PRIVILEGIADA → TODAS LAS TABLAS
                                              ↓
       ← RESPUESTA COMPLETA ← DATOS ADMIN ← FULL ACCESS
```

#### **Comandos Admin Telegram**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│    COMANDO      │    FUNCIÓN      │  ACCESO DATOS   │   PERMISOS      │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ /stats          │ Estadísticas    │ TODAS las       │ 👁️ Lectura     │
│                 │ globales        │ tablas          │ total           │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ /empresas       │ CRUD empresas   │ empresas +      │ ✏️ Crear/Editar │
│                 │ completo        │ info_compania   │ /Eliminar       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ /sync           │ Control sync    │ sync_logs +     │ 🔄 Triggear     │
│                 │ manual          │ configuración   │ manualmente     │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ /users          │ Gestión         │ users +         │ 👥 Crear/Editar │
│                 │ usuarios        │ permissions     │ permisos        │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ /backup         │ Backup/Restore  │ TODAS           │ 💾 Backup       │
│                 │ sistema         │                 │ completo        │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

#### **Permisos Totales Administrador**
```
🌍 ACCESO GLOBAL:
   ✅ Todas las empresas de todos los países
   ✅ Todos los reportes y archivos
   ✅ Configuración completa del sistema
   ✅ Gestión usuarios y permisos
   ✅ Logs y auditoría completa

🔧 OPERACIONES ADMINISTRATIVAS:
   ✅ Crear/Editar/Eliminar empresas
   ✅ Asignar contadores a empresas
   ✅ Configurar reglas de compliance
   ✅ Gestionar integraciones (APIs)
   ✅ Backup y restauración

📊 MONITOREO AVANZADO:
   ✅ Métricas en tiempo real
   ✅ Alertas y notificaciones sistema
   ✅ Performance y estadísticas
   ✅ Análisis financiero global
   ✅ Reportes ejecutivos automáticos
```

---

## 🗄️ ESTRUCTURA BASE DE DATOS Y COHERENCIA

### **Mapa Relacional Supabase**

```
                    ┌─────────────────┐
                    │   GLOBAL        │
                    │                 │
              ┌─────┤  organizations  ├─────┐
              │     │  users          │     │
              │     │  countries      │     │
              │     └─────────────────┘     │
              │                             │
              ▼                             ▼
    ┌─────────────────┐           ┌─────────────────┐
    │   CHILE (CL)    │           │  COLOMBIA (CO)  │
    │                 │           │                 │
    │  ┌─────────────┐│           │ ┌─────────────┐ │
    │  │  empresas   ││           │ │  empresas   │ │
    │  └─────┬───────┘│           │ └─────┬───────┘ │
    │        │        │           │       │         │
    │  ┌─────▼───────┐│           │ ┌─────▼───────┐ │
    │  │ reportes_   ││           │ │ reportes_   │ │
    │  │ mensuales   ││           │ │ mensuales   │ │
    │  └─────┬───────┘│           │ └─────┬───────┘ │
    │        │        │           │       │         │
    │  ┌─────▼───────┐│           │ ┌─────▼───────┐ │
    │  │ archivos_   ││           │ │ archivos_   │ │
    │  │ reportes    ││           │ │ reportes    │ │
    │  └─────────────┘│           │ └─────────────┘ │
    └─────────────────┘           └─────────────────┘
```

### **Mapa Relacional Airtable**

```
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │  AIRTABLE CL    │    │  AIRTABLE CO    │    │  AIRTABLE MX    │
    │                 │    │                 │    │                 │
    │ Reportes_       │    │ Reportes_       │    │ Reportes_       │
    │ Empresas_CL     │    │ Empresas_CO     │    │ Empresas_MX     │
    │                 │    │                 │    │                 │
    │ Campos:         │    │ Campos:         │    │ Campos:         │
    │ • Empresa (RUT) │    │ • Empresa (NIT) │    │ • Empresa (RFC) │
    │ • Tipo Doc      │    │ • Tipo Doc      │    │ • Tipo Doc      │
    │ • Archivo PDF   │    │ • Archivo PDF   │    │ • Archivo PDF   │
    │ • Estado        │    │ • Estado        │    │ • Estado        │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    │
                              ┌─────▼─────┐
                              │SYNC ENGINE│
                              │           │
                              │ • Extract │
                              │ • Validate│
                              │ • Load    │
                              └───────────┘
```

### **Flujo Coherencia Datos**

```
CONTADOR AIRTABLE → WEBHOOK → SYNC SERVICE → VALIDACIÓN → SUPABASE
                                                              ↓
                                                         RLS CHECK
                                                              ↓
                                                    USUARIO VE DATOS
```

#### **Matriz Permisos por Tabla**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│     TABLA       │   EMPRESA       │   CONTADOR      │   ADMIN         │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ empresas        │ 👁️ Solo su     │ 👁️ Solo las    │ 🔧 Todas +     │
│                 │ empresa         │ asignadas       │ CRUD completo   │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ reportes_       │ 👁️ Solo sus    │ ❌ No acceso    │ 🔧 Todos +     │
│ mensuales       │ reportes        │ directo         │ CRUD completo   │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ archivos_       │ 👁️ Solo sus    │ ❌ No acceso    │ 🔧 Todos +     │
│ reportes        │ archivos        │ directo         │ CRUD completo   │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ info_compania   │ 👁️ Solo su     │ ❌ No acceso    │ 🔧 Toda +      │
│                 │ info            │                 │ CRUD completo   │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ AIRTABLE        │ ❌ Sin acceso   │ ✏️ Crear/Editar│ 👁️ Solo       │
│ (todas bases)   │                 │ documentos      │ monitoreo       │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

---

## 🔄 FLUJOS DE TRABAJO COMPLETOS

### **Flujo 1: Contador Sube Documento**

```
1. 📊 CONTADOR (Airtable)
   ├── Recibe documentos empresa
   ├── Abre base Airtable país correspondiente
   ├── Llena formulario: Empresa, Tipo, Archivo
   └── Guarda registro → Estado: "Pendiente"

2. 🔄 SISTEMA ACA (Automático)
   ├── Detecta nuevo registro via webhook
   ├── Extrae RUT/NIT/RFC del nombre empresa
   ├── Busca empresa en Supabase país
   ├── Valida formato y datos
   └── Procesa documento → Estado: "Procesado"

3. 🏢 EMPRESA (Usuario Final)
   ├── Recibe notificación Telegram
   ├── Consulta "/reportes RUT" 
   ├── Ve nuevo reporte disponible
   └── Puede descargar/analizar

4. ⚙️ ADMIN (Supervisión)
   ├── Ve estadísticas en dashboard
   ├── Monitorea logs de sync
   ├── Valida que proceso funcionó
   └── Puede intervenir si hay errores
```

### **Flujo 2: Empresa Consulta Sus Datos**

```
1. 🏢 EMPRESA (Telegram/Dashboard)
   ├── Inicia sesión o envía comando
   ├── Sistema identifica su empresa por RUT
   ├── RLS filtra automáticamente sus datos
   └── Ve solo información de su empresa

2. 🗄️ BASE DE DATOS (Filtrado RLS)
   ├── Query: WHERE empresa_id = 'su_uuid'
   ├── Solo retorna datos autorizados
   ├── Oculta información otras empresas
   └── Respeta permisos de lectura

3. 📊 PRESENTACIÓN (Frontend)
   ├── Formatea datos según país
   ├── Convierte monedas si necesario
   ├── Aplica idioma del usuario
   └── Muestra interfaz personalizada
```

### **Flujo 3: Admin Gestiona Sistema**

```
1. ⚙️ ADMIN (Dashboard/Telegram)
   ├── Acceso completo sin restricciones
   ├── Ve todas las empresas/países
   ├── Puede modificar cualquier dato
   └── Controla configuración global

2. 🔧 OPERACIONES ADMIN
   ├── Crear nuevas empresas
   ├── Asignar contadores a empresas
   ├── Configurar reglas compliance
   ├── Triggear sincronizaciones manuales
   ├── Gestionar usuarios y permisos
   └── Monitorear health del sistema

3. 📈 MONITOREO CONTINUO
   ├── Dashboard tiempo real
   ├── Alertas automáticas
   ├── Logs detallados
   ├── Métricas performance
   └── Reportes ejecutivos
```

---

## 🎯 COHERENCIA FUNCIONAL

### **Validación de Coherencia**

#### **1. Acceso por Empresa ✅**
```
Empresa consulta → RUT validado → Solo sus datos → Respuesta filtrada
```

#### **2. Contador Especializado ✅**
```
Contador → Airtable asignado → Empresas específicas → Sync automático
```

#### **3. Admin Total ✅**
```
Admin → Sin restricciones → Todas las empresas → Control completo
```

#### **4. Separación por País ✅**
```
Cada país → Base datos separada → Regulaciones específicas → Compliance local
```

### **Matriz de Verificación**

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│   FUNCIONALIDAD │   COHERENTE?    │   USUARIO TIPO  │   VALIDACIÓN    │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Consulta datos  │        ✅       │ Empresa         │ RLS + RUT match │
│ Subida docs     │        ✅       │ Contador        │ Airtable + Sync │
│ Gestión total   │        ✅       │ Admin           │ Sin restricción │
│ Multi-país      │        ✅       │ Todos           │ DB separadas    │
│ Compliance      │        ✅       │ Sistema         │ Reglas por país │
│ Notificaciones  │        ✅       │ Todos           │ Canal apropiado │
│ Backup/Restore  │        ✅       │ Solo Admin      │ Acceso total    │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

---

## 📊 RESUMEN VISUAL FINAL

### **Ecosystem Overview**

```
                    👥 USUARIOS
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    🏢 EMPRESA      📊 CONTADOR     ⚙️ ADMIN
        │               │               │
        │               │               │
    📱 Telegram     📋 Airtable    🌐 Dashboard
    🌐 Dashboard    💬 Slack       📱 Telegram
        │               │               │
        └───────────────┼───────────────┘
                        │
                    🔄 API LAYER
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    🗄️ SUPABASE    📊 ANALYTICS   🔧 CONFIG
   (Por País)      (Tiempo Real)   (Global)
        │               │               │
    🇨🇱 Chile       📈 Gráficos    ⚙️ Settings
    🇨🇴 Colombia    📊 KPIs        👥 Users  
    🇲🇽 México      📋 Reports     🔐 Security
```

### **Flujo de Valor**

```
📊 CONTADOR → 📋 AIRTABLE → 🔄 SYNC → 🗄️ SUPABASE → 🏢 EMPRESA
   (Input)      (Staging)    (Process)  (Storage)    (Output)
      ↓            ↓            ↓          ↓           ↓
   Documentos   Categoriza   Valida     Almacena    Consulta
   Originales   y Organiza   Datos      Seguro      Resultados
```

---

## 🗄️ ESTRUCTURAS DETALLADAS DE BASES DE DATOS

### **SUPABASE - Esquema Global**

#### **Tabla: global.countries**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│     CAMPO       │      TIPO       │     FORMATO     │       USO       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ code            │ VARCHAR(2)      │ 'CL','CO','MX'  │ Código ISO país │
│ name            │ VARCHAR(100)    │ 'Chile'         │ Nombre completo │
│ region          │ VARCHAR(50)     │ 'South America' │ Región geográf. │
│ currency_code   │ VARCHAR(3)      │ 'CLP','COP'     │ Moneda default  │
│ timezone        │ VARCHAR(50)     │ 'America/Santgo'│ Zona horaria    │
│ language_code   │ VARCHAR(5)      │ 'es_CL'         │ Idioma default  │
│ database_url    │ TEXT            │ URL Supabase    │ DB regional     │
│ is_active       │ BOOLEAN         │ true/false      │ País habilitado │
│ created_at      │ TIMESTAMPTZ     │ ISO 8601        │ Auditoría       │
│ updated_at      │ TIMESTAMPTZ     │ ISO 8601        │ Última modific. │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

CONSTRAINTS:
• PRIMARY KEY: code
• UNIQUE: name, database_url
• CHECK: code IN ('CL','CO','MX','PE','UY','AR')
```

#### **Tabla: global.users**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│     CAMPO       │      TIPO       │     FORMATO     │       USO       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ id              │ UUID            │ gen_random_uuid │ ID único global │
│ email           │ VARCHAR(255)    │ user@domain.com │ Login principal │
│ password_hash   │ TEXT            │ bcrypt hash     │ Auth segura     │
│ full_name       │ VARCHAR(255)    │ 'Juan Pérez'    │ Nombre completo │
│ country_codes   │ TEXT[]          │ ['CL','CO']     │ Países acceso   │
│ role            │ VARCHAR(50)     │ 'admin','user'  │ Rol principal   │
│ phone           │ VARCHAR(20)     │ '+56912345678'  │ Contacto móvil  │
│ telegram_chat_id│ BIGINT          │ 123456789       │ ID chat Telegram│
│ is_active       │ BOOLEAN         │ true/false      │ Usuario activo  │
│ last_login      │ TIMESTAMPTZ     │ ISO 8601        │ Último acceso   │
│ created_at      │ TIMESTAMPTZ     │ ISO 8601        │ Fecha registro  │
│ updated_at      │ TIMESTAMPTZ     │ ISO 8601        │ Última modific. │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

CONSTRAINTS:
• PRIMARY KEY: id
• UNIQUE: email, telegram_chat_id
• CHECK: role IN ('admin','contador','empresa','readonly')
• CHECK: array_length(country_codes, 1) >= 1
```

#### **Tabla: global.currencies**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│     CAMPO       │      TIPO       │     FORMATO     │       USO       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ code            │ VARCHAR(3)      │ 'CLP','USD'     │ Código ISO      │
│ name            │ VARCHAR(100)    │ 'Peso Chileno'  │ Nombre moneda   │
│ symbol          │ VARCHAR(10)     │ '$','$CLP'      │ Símbolo display │
│ decimal_places  │ INTEGER         │ 0,2             │ Decimales mostrar│
│ is_active       │ BOOLEAN         │ true/false      │ Moneda activa   │
│ created_at      │ TIMESTAMPTZ     │ ISO 8601        │ Auditoría       │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

CONSTRAINTS:
• PRIMARY KEY: code
• CHECK: decimal_places >= 0 AND decimal_places <= 4
```

#### **Tabla: global.exchange_rates**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│     CAMPO       │      TIPO       │     FORMATO     │       USO       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ id              │ UUID            │ gen_random_uuid │ ID único        │
│ from_currency   │ VARCHAR(3)      │ 'CLP'           │ Moneda origen   │
│ to_currency     │ VARCHAR(3)      │ 'USD'           │ Moneda destino  │
│ rate            │ DECIMAL(15,6)   │ 900.000000      │ Tipo cambio     │
│ source          │ VARCHAR(50)     │ 'banco_central' │ Fuente del rate │
│ valid_from      │ TIMESTAMPTZ     │ ISO 8601        │ Válido desde    │
│ valid_to        │ TIMESTAMPTZ     │ ISO 8601        │ Válido hasta    │
│ created_at      │ TIMESTAMPTZ     │ ISO 8601        │ Fecha creación  │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

CONSTRAINTS:
• PRIMARY KEY: id
• FOREIGN KEY: from_currency → currencies(code)
• FOREIGN KEY: to_currency → currencies(code)
• UNIQUE: (from_currency, to_currency, valid_from)
• CHECK: rate > 0
```

### **SUPABASE - Esquema por País (country_CL, country_CO, etc.)**

#### **Tabla: country_{CODE}.empresas**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│     CAMPO       │      TIPO       │     FORMATO     │       USO       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ id              │ UUID            │ gen_random_uuid │ ID único empresa│
│ organization_id │ UUID            │ FK global       │ Organización    │
│ nombre          │ VARCHAR(255)    │ 'Empresa Demo'  │ Nombre comercial│
│ tax_id          │ VARCHAR(50)     │ '12345678-9'    │ RUT/NIT/RFC     │
│ razon_social    │ VARCHAR(255)    │ 'Empresa Demo SA'│ Razón social   │
│ email           │ VARCHAR(255)    │ admin@emp.com   │ Email principal │
│ telefono        │ VARCHAR(50)     │ '+56912345678'  │ Teléfono        │
│ direccion       │ TEXT            │ 'Av. Principal' │ Dirección física│
│ sector          │ VARCHAR(100)    │ 'Tecnología'    │ Sector económico│
│ tamaño          │ VARCHAR(20)     │ 'mediana'       │ Tamaño empresa  │
│ estado          │ VARCHAR(20)     │ 'activa'        │ Estado operativo│
│ currency_code   │ VARCHAR(3)      │ 'CLP'           │ Moneda principal│
│ configuracion_  │ JSONB           │ JSON config     │ Config específica│
│ local           │                 │                 │                 │
│ compliance_score│ INTEGER         │ 0-100           │ Score compliance│
│ last_compliance │ TIMESTAMPTZ     │ ISO 8601        │ Última revisión │
│ _check          │                 │                 │                 │
│ created_by      │ UUID            │ FK global.users │ Usuario creador │
│ created_at      │ TIMESTAMPTZ     │ ISO 8601        │ Fecha creación  │
│ updated_at      │ TIMESTAMPTZ     │ ISO 8601        │ Última modific. │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

CONSTRAINTS:
• PRIMARY KEY: id
• UNIQUE: tax_id (por país)
• FOREIGN KEY: organization_id → global.organizations(id)
• FOREIGN KEY: created_by → global.users(id)
• CHECK: tamaño IN ('pequeña','mediana','grande')
• CHECK: estado IN ('activa','inactiva','suspendida')
• CHECK: compliance_score >= 0 AND compliance_score <= 100

RLS POLICY: WHERE organization_id IN (SELECT org_id FROM user_orgs WHERE user_id = auth.uid())
```

#### **Tabla: country_{CODE}.reportes_mensuales**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│     CAMPO       │      TIPO       │     FORMATO     │       USO       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ id              │ UUID            │ gen_random_uuid │ ID único reporte│
│ empresa_id      │ UUID            │ FK empresas     │ Empresa dueña   │
│ titulo          │ VARCHAR(255)    │ 'Balance Enero' │ Título reporte  │
│ descripcion     │ TEXT            │ 'Descripción...'│ Desc. detallada │
│ tipo_reporte    │ VARCHAR(100)    │ 'Balance General'│ Tipo documento  │
│ subtipo_reporte │ VARCHAR(100)    │ 'Mensual'       │ Subtipo específ.│
│ anio            │ INTEGER         │ 2025            │ Año fiscal      │
│ mes             │ INTEGER         │ 1-12            │ Mes fiscal      │
│ trimestre       │ INTEGER         │ 1-4             │ Trimestre fiscal│
│ estado          │ VARCHAR(50)     │ 'aprobado'      │ Estado proceso  │
│ montos          │ JSONB           │ JSON amounts    │ Montos financ.  │
│ regulatory_info │ JSONB           │ JSON regulatory │ Info compliance │
│ compliance_     │ VARCHAR(50)     │ 'compliant'     │ Estado complianc│
│ status          │                 │                 │                 │
│ source_system   │ VARCHAR(50)     │ 'airtable'      │ Sistema origen  │
│ external_id     │ VARCHAR(255)    │ 'rec123456'     │ ID sistema orig.│
│ comentarios     │ TEXT            │ 'Comentarios...'│ Notas adicional.│
│ created_by      │ UUID            │ FK global.users │ Usuario creador │
│ created_at      │ TIMESTAMPTZ     │ ISO 8601        │ Fecha creación  │
│ updated_at      │ TIMESTAMPTZ     │ ISO 8601        │ Última modific. │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

ESTRUCTURA JSONB 'montos':
{
  "ingresos": {
    "amount": 50000000,
    "currency": "CLP", 
    "usd_amount": 55555.56,
    "exchange_rate": 900.0,
    "rate_date": "2025-01-08"
  },
  "gastos": {
    "amount": 30000000,
    "currency": "CLP",
    "usd_amount": 33333.33
  },
  "utilidad": {
    "amount": 20000000,
    "currency": "CLP", 
    "usd_amount": 22222.22
  }
}

CONSTRAINTS:
• PRIMARY KEY: id
• FOREIGN KEY: empresa_id → empresas(id) ON DELETE CASCADE
• FOREIGN KEY: created_by → global.users(id)
• UNIQUE: (empresa_id, anio, mes, tipo_reporte, subtipo_reporte)
• CHECK: anio >= 2020 AND anio <= 2030
• CHECK: mes >= 1 AND mes <= 12
• CHECK: trimestre >= 1 AND trimestre <= 4
• CHECK: estado IN ('borrador','pendiente','en_revision','aprobado','rechazado','enviado')

RLS POLICY: WHERE empresa_id IN (SELECT id FROM empresas WHERE organization_id IN (...))
```

#### **Tabla: country_{CODE}.archivos_reportes**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│     CAMPO       │      TIPO       │     FORMATO     │       USO       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ id              │ UUID            │ gen_random_uuid │ ID único archivo│
│ reporte_id      │ UUID            │ FK reportes     │ Reporte asociado│
│ empresa_id      │ UUID            │ FK empresas     │ Empresa dueña   │
│ nombre_archivo  │ VARCHAR(255)    │ 'balance.pdf'   │ Nombre mostrar  │
│ nombre_original │ VARCHAR(255)    │ 'Balance Ene.pdf'│ Nombre original │
│ tipo_archivo    │ VARCHAR(100)    │ 'application/pdf'│ MIME type      │
│ extension       │ VARCHAR(10)     │ '.pdf'          │ Extensión       │
│ tamaño_bytes    │ BIGINT          │ 1048576         │ Tamaño en bytes │
│ checksum_md5    │ VARCHAR(32)     │ 'abc123...'     │ Hash integridad │
│ url_archivo     │ TEXT            │ 'https://...'   │ URL descarga    │
│ url_thumbnail   │ TEXT            │ 'https://...'   │ URL thumbnail   │
│ storage_provider│ VARCHAR(50)     │ 'supabase'      │ Proveedor almac.│
│ storage_path    │ TEXT            │ '/uploads/...'  │ Path interno    │
│ descripcion     │ TEXT            │ 'Balance mensual'│ Descripción    │
│ tags            │ TEXT[]          │ ['balance','ene']│ Tags búsqueda  │
│ categoria       │ VARCHAR(100)    │ 'Financiero'    │ Categoría doc   │
│ ocr_text        │ TEXT            │ 'Texto OCR...'  │ Texto extraído  │
│ extracted_data  │ JSONB           │ JSON data       │ Datos extraídos │
│ processing_     │ VARCHAR(50)     │ 'completed'     │ Estado proceso  │
│ status          │                 │                 │                 │
│ version         │ INTEGER         │ 1               │ Versión archivo │
│ parent_file_id  │ UUID            │ FK self         │ Archivo padre   │
│ activo          │ BOOLEAN         │ true/false      │ Archivo activo  │
│ access_level    │ VARCHAR(20)     │ 'private'       │ Nivel acceso    │
│ uploaded_by     │ UUID            │ FK global.users │ Usuario subida  │
│ created_at      │ TIMESTAMPTZ     │ ISO 8601        │ Fecha creación  │
│ updated_at      │ TIMESTAMPTZ     │ ISO 8601        │ Última modific. │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

ESTRUCTURA JSONB 'extracted_data':
{
  "total_ingresos": 50000000,
  "total_gastos": 30000000,
  "fecha_documento": "2025-01-31",
  "numero_documento": "001-2025",
  "entidades_detectadas": ["Cliente A", "Proveedor B"],
  "moneda_detectada": "CLP",
  "confianza_ocr": 0.95
}

CONSTRAINTS:
• PRIMARY KEY: id
• FOREIGN KEY: reporte_id → reportes_mensuales(id) ON DELETE CASCADE
• FOREIGN KEY: empresa_id → empresas(id) ON DELETE CASCADE
• FOREIGN KEY: parent_file_id → archivos_reportes(id)
• FOREIGN KEY: uploaded_by → global.users(id)
• CHECK: tamaño_bytes > 0
• CHECK: version >= 1
• CHECK: access_level IN ('public','organization','private')
• CHECK: processing_status IN ('pending','processing','completed','failed')

RLS POLICY: WHERE empresa_id IN (SELECT id FROM empresas WHERE organization_id IN (...))
```

#### **Tabla: country_{CODE}.info_compania**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│     CAMPO       │      TIPO       │     FORMATO     │       USO       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ id              │ UUID            │ gen_random_uuid │ ID único        │
│ empresa_id      │ UUID            │ FK empresas     │ Empresa (1:1)   │
│ ingresos_anuales│ DECIMAL(15,2)   │ 500000000.00    │ Ingresos estimad│
│ _estimados      │                 │                 │                 │
│ numero_empleados│ INTEGER         │ 50              │ Cantidad emplead│
│ fecha_          │ DATE            │ '2020-01-15'    │ Fecha fundación │
│ constitucion    │                 │                 │                 │
│ representante_  │ VARCHAR(255)    │ 'Juan Pérez'    │ Rep. legal      │
│ legal           │                 │                 │                 │
│ contador_       │ VARCHAR(255)    │ 'María García'  │ Contador asignad│
│ asignado        │                 │                 │                 │
│ email_contador  │ VARCHAR(255)    │ 'cont@ext.com'  │ Email contador  │
│ telefono_       │ VARCHAR(50)     │ '+56987654321'  │ Tel. contador   │
│ contador        │                 │                 │                 │
│ configuracion_  │ JSONB           │ JSON config     │ Config reportes │
│ reportes        │                 │                 │                 │
│ configuracion_  │ JSONB           │ JSON config     │ Config notific. │
│ notificaciones  │                 │                 │                 │
│ licencias_      │ TEXT[]          │ ['lic1','lic2'] │ Licencias req.  │
│ requeridas      │                 │                 │                 │
│ fechas_         │ JSONB           │ JSON dates      │ Vencimientos    │
│ vencimiento_    │                 │                 │                 │
│ licencias       │                 │                 │                 │
│ notas           │ TEXT            │ 'Notas varias'  │ Notas adicional.│
│ ultima_revision │ TIMESTAMPTZ     │ ISO 8601        │ Última revisión │
│ created_at      │ TIMESTAMPTZ     │ ISO 8601        │ Fecha creación  │
│ updated_at      │ TIMESTAMPTZ     │ ISO 8601        │ Última modific. │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

ESTRUCTURA JSONB 'configuracion_reportes':
{
  "frecuencia_reportes": "mensual",
  "tipos_requeridos": ["balance", "estado_resultados"],
  "formato_preferido": "pdf",
  "idioma": "es_CL",
  "moneda_reporte": "CLP",
  "incluir_comparativos": true,
  "envio_automatico": true,
  "destinatarios": ["admin@empresa.com"]
}

ESTRUCTURA JSONB 'fechas_vencimiento_licencias':
{
  "licencia_municipal": "2025-12-31",
  "patente_comercial": "2025-06-30", 
  "certificado_bomberos": "2025-09-15",
  "revision_tecnica": "2025-03-20"
}

CONSTRAINTS:
• PRIMARY KEY: id
• FOREIGN KEY: empresa_id → empresas(id) ON DELETE CASCADE
• UNIQUE: empresa_id (relación 1:1)
• CHECK: numero_empleados >= 0
• CHECK: ingresos_anuales_estimados >= 0

RLS POLICY: WHERE empresa_id IN (SELECT id FROM empresas WHERE organization_id IN (...))
```

#### **Tabla: country_{CODE}.sync_logs**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│     CAMPO       │      TIPO       │     FORMATO     │       USO       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ id              │ UUID            │ gen_random_uuid │ ID único log    │
│ sync_type       │ VARCHAR(50)     │ 'airtable'      │ Tipo sync       │
│ sync_direction  │ VARCHAR(20)     │ 'inbound'       │ Dirección sync  │
│ source_system   │ VARCHAR(50)     │ 'airtable'      │ Sistema origen  │
│ target_system   │ VARCHAR(50)     │ 'supabase'      │ Sistema destino │
│ started_at      │ TIMESTAMPTZ     │ ISO 8601        │ Inicio proceso  │
│ completed_at    │ TIMESTAMPTZ     │ ISO 8601        │ Fin proceso     │
│ duration_seconds│ INTEGER         │ 45              │ Duración total  │
│ status          │ VARCHAR(20)     │ 'completed'     │ Estado final    │
│ records_        │ INTEGER         │ 15              │ Total procesados│
│ processed       │                 │                 │                 │
│ records_success │ INTEGER         │ 14              │ Exitosos        │
│ records_failed  │ INTEGER         │ 1               │ Fallidos        │
│ error_details   │ JSONB           │ JSON errors     │ Detalles errores│
│ sync_details    │ JSONB           │ JSON details    │ Detalles sync   │
│ triggered_by    │ UUID            │ FK global.users │ Usuario trigger │
│ trigger_type    │ VARCHAR(20)     │ 'manual'        │ Tipo trigger    │
│ created_at      │ TIMESTAMPTZ     │ ISO 8601        │ Fecha creación  │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

ESTRUCTURA JSONB 'error_details':
{
  "errors": [
    {
      "record_id": "rec123456",
      "error_type": "validation_error",
      "message": "RUT inválido",
      "field": "empresa",
      "timestamp": "2025-01-08T10:30:00Z"
    }
  ],
  "summary": {
    "validation_errors": 1,
    "connection_errors": 0,
    "permission_errors": 0
  }
}

ESTRUCTURA JSONB 'sync_details':
{
  "source_config": {
    "base_id": "app123456",
    "table": "Reportes_Empresas_CL",
    "view": "Pendientes"
  },
  "processing_stats": {
    "empresas_created": 2,
    "reportes_created": 12,
    "archivos_uploaded": 18,
    "duplicates_skipped": 3
  },
  "performance": {
    "avg_record_time": 3.2,
    "api_calls_made": 45,
    "data_transferred_mb": 15.7
  }
}

CONSTRAINTS:
• PRIMARY KEY: id
• FOREIGN KEY: triggered_by → global.users(id)
• CHECK: status IN ('running','completed','failed','partial')
• CHECK: sync_direction IN ('inbound','outbound','bidirectional')
• CHECK: trigger_type IN ('manual','scheduled','webhook','api')
• CHECK: records_processed >= 0
• CHECK: records_success >= 0
• CHECK: records_failed >= 0
• CHECK: records_success + records_failed <= records_processed
```

### **AIRTABLE - Estructuras por País**

#### **Base Chile: "ACA_Contabilidad_CL"**
#### **Tabla: "Reportes_Empresas_CL"**

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│     CAMPO       │   TIPO AIRTABLE │     FORMATO     │       USO       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Empresa         │ Single line text│ 'Empresa (RUT)' │ Nombre + RUT    │
│ RUT             │ Single line text│ '12345678-9'    │ RUT separado    │
│ Fecha_Subida    │ Date            │ '2025-01-08'    │ Fecha documento │
│ Tipo_Documento  │ Single select   │ Options below   │ Tipo reporte    │
│ Subtipo_Doc     │ Single select   │ Options below   │ Subtipo específ.│
│ Archivo_Adjunto │ Multiple attach │ PDF/Excel files │ Documentos      │
│ Estado_Subida   │ Single select   │ 'Pendiente'     │ Estado proceso  │
│ Comentarios     │ Long text       │ Free text       │ Notas contador  │
│ Moneda          │ Single select   │ 'CLP'           │ Moneda document │
│ Monto_Total     │ Currency        │ $50.000.000    │ Monto principal │
│ Periodo_Fiscal  │ Single line text│ '2025-01'       │ Período fiscal  │
│ Urgencia        │ Single select   │ 'Media'         │ Prioridad       │
│ Contador_Asig   │ Single select   │ 'María García'  │ Contador respons│
│ Fecha_Proceso   │ Date            │ Auto-filled     │ Fecha procesado │
│ ID_Supabase     │ Single line text│ Auto-filled     │ ID generado     │
│ Error_Message   │ Long text       │ Auto-filled     │ Errores sync    │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

OPCIONES 'Tipo_Documento' (Chile):
• Balance General
• Estado de Resultados
• Estado de Situación Financiera
• Flujo de Caja
• Estado de Cambios en el Patrimonio
• Notas a los Estados Financieros
• Declaración de Renta
• Formulario 29 (IVA)
• Libro de Compras y Ventas
• Carpeta Tributaria

OPCIONES 'Subtipo_Doc':
• Mensual
• Trimestral
• Semestral
• Anual
• Extraordinario

OPCIONES 'Estado_Subida':
• ⏳ Pendiente
• 🔄 Procesando
• ✅ Procesado
• ❌ Error
• ⚠️ Requiere Atención

OPCIONES 'Urgencia':
• 🔴 Alta
• 🟡 Media  
• 🟢 Baja

OPCIONES 'Contador_Asig':
• María García (Contador Senior)
• Carlos López (Contador Junior)
• Ana Martínez (Especialista Tributario)
• External Contador (Por definir)
```

#### **Base Colombia: "ACA_Contabilidad_CO"**
#### **Tabla: "Reportes_Empresas_CO"**

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│     CAMPO       │   TIPO AIRTABLE │     FORMATO     │       USO       │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Empresa         │ Single line text│ 'Empresa (NIT)' │ Nombre + NIT    │
│ NIT             │ Single line text│ '900123456-1'   │ NIT separado    │
│ Regimen_Tributario│Single select   │ Options below   │ Régimen fiscal  │
│ Tipo_Documento  │ Single select   │ Options below   │ Tipo reporte    │
│ [... otros campos similares ...]     │                 │                 │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

OPCIONES 'Tipo_Documento' (Colombia):
• Estados Financieros NIIF
• Balance General NIIF
• Estado de Resultados NIIF
• Estado de Flujos de Efectivo
• Estado de Cambios en el Patrimonio
• Declaración de Renta Jurídicas
• Declaración Bimestral IVA
• Información Exógena
• Medios Magnéticos

OPCIONES 'Regimen_Tributario':
• Ordinario
• Simplificado
• Gran Contribuyente
• Entidad sin Ánimo de Lucro
```

#### **Base México: "ACA_Contabilidad_MX"**
#### **Tabla: "Reportes_Empresas_MX"**

```
OPCIONES 'Tipo_Documento' (México):
• Estados Financieros NIF
• Balance General NIF
• Estado de Resultados NIF
• Estado de Flujos de Efectivo
• Declaración Anual Personas Morales
• Declaración Mensual IVA
• CFDI (Facturación Electrónica)
• Contabilidad Electrónica
• DIOT (Información de Operaciones con Terceros)

OPCIONES 'Regimen_Fiscal':
• General de Ley Personas Morales
• Régimen Simplificado de Confianza (RESICO)
• Personas Morales con Fines No Lucrativos
```

### **VALIDACIÓN DE CONSISTENCIA**

#### **Matriz de Consistencia Supabase ↔ Airtable**

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│   AIRTABLE      │    SUPABASE     │   VALIDACIÓN    │   COHERENCIA    │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Empresa (RUT)   │ empresas.tax_id │ Extrae RUT      │ ✅ Match       │
│                 │ empresas.nombre │ Extrae nombre   │                 │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Tipo_Documento  │ reportes.       │ Mapeo directo   │ ✅ Coherente   │
│                 │ tipo_reporte    │                 │                 │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Archivo_Adjunto │ archivos_       │ URL temporal    │ ⚠️ Requiere    │
│                 │ reportes.url    │ → permanente    │ renovación      │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Estado_Subida   │ reportes.estado │ Mapeo estados   │ ✅ Sincronizado│
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Monto_Total     │ reportes.montos │ JSON structure  │ ✅ Multi-moneda│
│                 │ (JSONB)         │                 │                 │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Periodo_Fiscal  │ reportes.anio   │ Split YYYY-MM   │ ✅ Parseado    │
│                 │ reportes.mes    │                 │                 │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

#### **Validación Integridad Referencial**

```
1. EMPRESA EXISTE:
   Airtable.Empresa → Extrae RUT → Busca en empresas.tax_id
   Si NO existe → Crea nueva empresa automáticamente
   Si existe → Usa empresa_id existente

2. UNICIDAD REPORTES:
   Check UNIQUE(empresa_id, anio, mes, tipo_reporte, subtipo_reporte)
   Si existe → Actualiza datos
   Si NO existe → Crea nuevo reporte

3. ARCHIVOS VÁLIDOS:
   Valida extensión permitida (.pdf, .xlsx, .docx)
   Valida tamaño máximo (50MB)
   Genera checksum MD5 para integridad
   URL temporal → URL permanente en Supabase Storage

4. COMPLIANCE POR PAÍS:
   Chile: Valida RUT formato XX.XXX.XXX-X
   Colombia: Valida NIT formato XXXXXXXXX-X  
   México: Valida RFC formato XAXX010101000
```

#### **Mapeo de Estados**

```
AIRTABLE → SUPABASE:
• "⏳ Pendiente" → "pendiente"
• "🔄 Procesando" → "en_revision"  
• "✅ Procesado" → "aprobado"
• "❌ Error" → "rechazado"
• "⚠️ Requiere Atención" → "borrador"

SUPABASE → FRONTEND:
• "pendiente" → 🟡 "Pendiente de Revisión"
• "en_revision" → 🔵 "En Proceso"  
• "aprobado" → 🟢 "Completado"
• "rechazado" → 🔴 "Requiere Corrección"
• "borrador" → ⚪ "Borrador"
```

---

**🎯 Este documento asegura que cada usuario tiene acceso exacto a lo que necesita, con coherencia total entre funcionalidades, permisos y estructura de datos.**