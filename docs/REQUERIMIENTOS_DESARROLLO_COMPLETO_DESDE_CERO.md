# 🌍 REQUERIMIENTOS DESARROLLO COMPLETO DESDE CERO
## Sistema ACA 3.0 - Plataforma Contable Multi-Nacional

---

## 📋 RESUMEN EJECUTIVO

Este documento especifica **TODOS** los requerimientos técnicos y funcionales para desarrollar desde cero un sistema integral de gestión contable que opere simultáneamente en múltiples países, con soporte nativo para múltiples monedas e idiomas, y compliance total con regulaciones locales.

### 🎯 **Objetivo Principal**
Crear una plataforma completa que incluya:
- **Dashboard Web** administrativo completo
- **Aplicación Móvil** nativa (iOS/Android)
- **Bots Telegram** para acceso móvil
- **Integración Airtable** para gestión documental
- **Dashboard Notion** para ejecutivos
- **Notificaciones Slack** para equipos
- **Sistema Calendly** para agendamiento
- **Arquitectura Multi-País** escalable globalmente

---

## 🏗️ ARQUITECTURA GENERAL DEL SISTEMA

### **Vista de Alto Nivel**

```
                    ┌─────────────────────────────────────────┐
                    │           API GATEWAY GLOBAL            │
                    │    Authentication • Routing • RateLimit │
                    └─────────────────────────────────────────┘
                                        │
            ┌───────────────────────────┼───────────────────────────┐
            │                           │                           │
    ┌──────────────┐          ┌─────────────────┐          ┌──────────────┐
    │   REGIÓN      │          │   REGIÓN        │          │   REGIÓN     │
    │   CHILE       │          │   COLOMBIA      │          │   MÉXICO     │
    │              │          │                 │          │              │
    │ ┌──────────┐ │          │ ┌─────────────┐ │          │ ┌──────────┐ │
    │ │Supabase  │ │          │ │Supabase     │ │          │ │Supabase  │ │
    │ │Chile     │ │          │ │Colombia     │ │          │ │México    │ │
    │ └──────────┘ │          │ └─────────────┘ │          │ └──────────┘ │
    │ ┌──────────┐ │          │ ┌─────────────┐ │          │ ┌──────────┐ │
    │ │Airtable  │ │          │ │Airtable     │ │          │ │Airtable  │ │
    │ │CL        │ │          │ │CO           │ │          │ │MX        │ │
    │ └──────────┘ │          │ └─────────────┘ │          │ └──────────┘ │
    └──────────────┘          └─────────────────┘          └──────────────┘
            │                           │                           │
            └───────────────────────────┼───────────────────────────┘
                                        │
        ┌─────────────────────────────────────────────────────────┐
        │                  CAPA DE SERVICIOS                      │
        │                                                         │
        │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌──────────┐│
        │  │Dashboard  │ │Mobile App │ │Telegram   │ │External  ││
        │  │Web        │ │iOS/Android│ │Bots       │ │APIs      ││
        │  └───────────┘ └───────────┘ └───────────┘ └──────────┘│
        └─────────────────────────────────────────────────────────┘
```

### **Componentes Core a Desarrollar**

1. **API Gateway Central** - Ruteo y autenticación global
2. **Bases de Datos Regionales** - Supabase por país
3. **Dashboard Web Administrativo** - 6+ vistas especializadas
4. **Aplicación Móvil Nativa** - React Native
5. **Bots Telegram** - Admin y Producción
6. **Integración Airtable** - Gestión documental
7. **Sistema Notion** - Dashboard ejecutivo
8. **Notificaciones Slack** - Colaboración equipos
9. **Integración Calendly** - Agendamiento reuniones
10. **Servicios Especializados** - Monedas, i18n, Compliance

---

## 💻 DASHBOARD WEB ADMINISTRATIVO

### **Arquitectura Frontend**
- **Framework**: React.js 18+ con TypeScript
- **Estado**: Redux Toolkit + RTK Query
- **UI**: Material-UI v5 o Ant Design
- **Gráficos**: Chart.js + D3.js para visualizaciones avanzadas
- **Routing**: React Router v6
- **Forms**: React Hook Form + Yup validation

### **Vistas Requeridas (Mínimo 8 Páginas)**

#### **1. Dashboard Principal** (`/dashboard`)
```typescript
interface DashboardProps {
  kpis: {
    totalEmpresas: number;
    reportesMes: number;
    archivosPendientes: number;
    sincronizacionesHoy: number;
  };
  graficos: {
    reportesPorTipo: ChartData;
    ingresosPorMes: ChartData;
    distribucionPorPais: ChartData;
  };
  actividadReciente: Activity[];
  estadoServicios: ServiceStatus;
}

// Componentes requeridos:
- KPI Cards con animaciones
- Gráficos interactivos tiempo real
- Feed actividad con filtros
- Monitor estado servicios
- Alertas y notificaciones
```

#### **2. Gestión de Empresas** (`/empresas`)
```typescript
interface EmpresasPageProps {
  empresas: Empresa[];
  filtros: {
    pais: string;
    estado: 'activa' | 'inactiva';
    tamaño: 'pequeña' | 'mediana' | 'grande';
    sector: string;
  };
  acciones: {
    crear: (empresa: NuevaEmpresa) => Promise<void>;
    editar: (id: string, datos: Partial<Empresa>) => Promise<void>;
    eliminar: (id: string) => Promise<void>;
    exportar: (formato: 'csv' | 'excel') => Promise<Blob>;
  };
}

// Funcionalidades:
- Tabla responsive con ordenamiento
- Búsqueda avanzada por RUT/nombre
- Filtros múltiples combinables
- Modal creación/edición con validación
- Bulk actions para operaciones masivas
- Exportación datos con plantillas
```

#### **3. Gestión de Reportes** (`/reportes`)
```typescript
interface ReportesPageProps {
  reportes: ReporteFinanciero[];
  filtros: {
    empresa: string;
    tipoReporte: string;
    periodo: DateRange;
    estado: string;
    moneda: string;
  };
  estadisticas: {
    totalReportes: number;
    promedioTiempoRespuesta: number;
    tasaCompletitud: number;
  };
}

// Características:
- Vista lista/grid intercambiable
- Filtros avanzados por período/tipo
- Preview reportes en modal
- Comparación períodos
- Alertas reportes vencidos
- Integración con generador PDFs
```

#### **4. Gestión de Archivos** (`/archivos`)
```typescript
interface ArchivosPageProps {
  archivos: ArchivoDocumento[];
  configuracion: {
    tiposPermitidos: string[];
    tamañoMaximo: number;
    almacenamiento: StorageConfig;
  };
  acciones: {
    subir: (archivos: File[]) => Promise<UploadResult[]>;
    descargar: (id: string) => Promise<Blob>;
    eliminar: (ids: string[]) => Promise<void>;
    compartir: (id: string, permisos: SharePermissions) => Promise<string>;
  };
}

// Funcionalidades:
- Drag & drop upload con progress
- Previsualización archivos (PDF, imágenes)
- Organización por carpetas/tags
- Control versiones documentos
- Permisos granulares por archivo
- Integración antivirus/scanning
```

#### **5. Monitor Multi-País** (`/paises`)
```typescript
interface PaisesPageProps {
  paises: PaisConfiguracion[];
  metricas: {
    [paisCode: string]: {
      empresasActivas: number;
      reportesMes: number;
      ingresosTotales: MontoMoneda;
      compliance: ComplianceStatus;
    };
  };
  configuraciones: {
    monedas: ConfiguracionMoneda[];
    idiomas: ConfiguracionIdioma[];
    regulaciones: RegulacionPorPais[];
  };
}

// Características específicas:
- Mapa interactivo con métricas por país
- Switching contexto país en tiempo real
- Configuración regulaciones locales
- Monitor compliance automático
- Alertas regulatorias
```

#### **6. Centro de Sincronización** (`/sync`)
```typescript
interface SyncPageProps {
  estadoSincronizacion: {
    [servicio: string]: SyncStatus;
  };
  historial: SyncHistoryEntry[];
  configuracion: {
    intervalos: SyncInterval[];
    webhooks: WebhookConfig[];
    alertas: AlertConfig[];
  };
  metricas: {
    ultimaSync: DateTime;
    registrosProcesados: number;
    errores: SyncError[];
    performance: PerformanceMetrics;
  };
}

// Funcionalidades avanzadas:
- Logs tiempo real con WebSocket
- Control manual sync por servicio
- Configuración webhooks automáticos
- Dashboard performance métricas
- Alerting inteligente por umbrales
```

#### **7. Configuración Sistema** (`/config`)
```typescript
interface ConfigPageProps {
  configuraciones: {
    general: ConfigGeneral;
    usuarios: ConfigUsuarios;
    integraciones: ConfigIntegraciones;
    seguridad: ConfigSeguridad;
    backup: ConfigBackup;
  };
  permisos: PermisosUsuario;
}

// Secciones configuración:
- Configuración global sistema
- Gestión usuarios y roles
- API keys y integraciones
- Políticas seguridad
- Configuración backup/restore
```

#### **8. Analytics y Reportes** (`/analytics`)
```typescript
interface AnalyticsPageProps {
  dashboard: {
    metricas: MetricasNegocio;
    tendencias: TendenciasDatos;
    predicciones: PrediccionesIA;
  };
  reportesPersonalizados: {
    plantillas: PlantillaReporte[];
    generados: ReporteGenerado[];
  };
  exportacion: {
    formatos: FormatoExportacion[];
    programados: ExportacionProgramada[];
  };
}

// Características:
- Dashboard métricas negocio
- Constructor reportes personalizados
- Exportación automatizada
- Integración BI tools
- Alertas métricas críticas
```

### **Arquitectura Backend Dashboard**

#### **API REST Completa**
```python
# FastAPI con estructura modular
app/
├── main.py                    # Aplicación principal
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── empresas.py    # CRUD empresas
│   │   │   ├── reportes.py    # Gestión reportes
│   │   │   ├── archivos.py    # Gestión archivos
│   │   │   ├── usuarios.py    # Gestión usuarios
│   │   │   ├── sync.py        # Sincronización
│   │   │   └── analytics.py   # Analytics y métricas
│   │   └── api.py             # Router principal
│   └── deps.py                # Dependencias
├── core/
│   ├── config.py              # Configuración
│   ├── security.py            # Autenticación/autorización
│   └── database.py            # Conexiones DB
├── models/
│   ├── empresa.py             # Modelos Pydantic
│   ├── reporte.py
│   ├── archivo.py
│   └── usuario.py
├── services/
│   ├── empresa_service.py     # Lógica negocio
│   ├── reporte_service.py
│   ├── archivo_service.py
│   ├── sync_service.py
│   └── notification_service.py
└── utils/
    ├── validators.py          # Validaciones
    ├── formatters.py          # Formateo datos
    └── helpers.py             # Utilidades
```

#### **Endpoints API Completos**
```python
# Empresas
GET    /api/v1/empresas                    # Listar con filtros
POST   /api/v1/empresas                    # Crear empresa
GET    /api/v1/empresas/{id}               # Obtener por ID
PUT    /api/v1/empresas/{id}               # Actualizar
DELETE /api/v1/empresas/{id}               # Eliminar
GET    /api/v1/empresas/{id}/reportes      # Reportes de empresa
GET    /api/v1/empresas/search             # Búsqueda avanzada

# Reportes
GET    /api/v1/reportes                    # Listar con filtros
POST   /api/v1/reportes                    # Crear reporte
GET    /api/v1/reportes/{id}               # Obtener por ID
PUT    /api/v1/reportes/{id}               # Actualizar
DELETE /api/v1/reportes/{id}               # Eliminar
GET    /api/v1/reportes/{id}/archivos      # Archivos del reporte
POST   /api/v1/reportes/{id}/generate      # Generar PDF
GET    /api/v1/reportes/templates          # Plantillas disponibles

# Archivos
GET    /api/v1/archivos                    # Listar archivos
POST   /api/v1/archivos/upload             # Subir archivo
GET    /api/v1/archivos/{id}               # Obtener archivo
DELETE /api/v1/archivos/{id}               # Eliminar archivo
GET    /api/v1/archivos/{id}/download      # Descargar archivo
POST   /api/v1/archivos/{id}/share         # Compartir archivo
GET    /api/v1/archivos/{id}/preview       # Preview archivo

# Sincronización
GET    /api/v1/sync/status                 # Estado sincronización
POST   /api/v1/sync/trigger                # Triggear sync manual
GET    /api/v1/sync/history                # Historial sync
GET    /api/v1/sync/logs                   # Logs tiempo real
POST   /api/v1/sync/configure              # Configurar sync
GET    /api/v1/sync/metrics                # Métricas performance

# Analytics
GET    /api/v1/analytics/dashboard         # Métricas dashboard
GET    /api/v1/analytics/reports           # Reportes analytics
POST   /api/v1/analytics/custom            # Crear reporte custom
GET    /api/v1/analytics/export            # Exportar datos
GET    /api/v1/analytics/predictions       # Predicciones IA

# Multi-País
GET    /api/v1/countries                   # Listar países
GET    /api/v1/countries/{code}/config     # Config por país
PUT    /api/v1/countries/{code}/config     # Actualizar config
GET    /api/v1/countries/{code}/metrics    # Métricas por país
GET    /api/v1/currencies                  # Monedas soportadas
GET    /api/v1/currencies/rates            # Tipos cambio actuales
```

---

## 📱 APLICACIÓN MÓVIL NATIVA

### **Arquitectura Móvil**
- **Framework**: React Native 0.72+ con TypeScript
- **Estado**: Redux Toolkit + Redux Persist
- **Navegación**: React Navigation v6
- **UI**: React Native Elements + Styled Components
- **Offline**: Redux Offline + AsyncStorage
- **Push**: Firebase Cloud Messaging
- **Analytics**: Firebase Analytics + Crashlytics

### **Pantallas Principales (15+ Screens)**

#### **Autenticación y Onboarding**
```typescript
// 1. Splash Screen
interface SplashScreenProps {
  verificarAutenticacion: () => Promise<boolean>;
  cargarConfiguracionInicial: () => Promise<void>;
}

// 2. Login Screen
interface LoginScreenProps {
  autenticar: (credentials: LoginCredentials) => Promise<AuthResult>;
  loginBiometrico: () => Promise<AuthResult>;
  recuperarPassword: (email: string) => Promise<void>;
}

// 3. Onboarding Screens (3-4 pantallas)
interface OnboardingProps {
  pasos: OnboardingStep[];
  completarOnboarding: () => Promise<void>;
}

// 4. Selección País/Idioma
interface CountrySelectProps {
  paises: PaisDisponible[];
  idiomas: IdiomaDisponible[];
  configurarLocalizacion: (config: LocalizationConfig) => Promise<void>;
}
```

#### **Dashboard y Navegación**
```typescript
// 5. Dashboard Principal
interface MobileDashboardProps {
  resumen: {
    empresaActual: EmpresaResumen;
    reportesPendientes: number;
    notificacionesNuevas: number;
    proximasCitas: CitaProxima[];
  };
  accionesRapidas: AccionRapida[];
  widgets: DashboardWidget[];
}

// 6. Drawer Navigation
interface DrawerNavigationProps {
  usuario: UsuarioMovil;
  menuItems: MenuItem[];
  configuraciones: ConfiguracionMovil;
  logout: () => Promise<void>;
}
```

#### **Gestión Empresas Móvil**
```typescript
// 7. Lista Empresas
interface EmpresasListScreenProps {
  empresas: EmpresaMovil[];
  filtros: FiltrosMovil;
  busqueda: string;
  acciones: {
    buscar: (termino: string) => void;
    filtrar: (filtros: FiltrosMovil) => void;
    actualizar: () => Promise<void>;
  };
}

// 8. Detalle Empresa
interface EmpresaDetailScreenProps {
  empresa: EmpresaCompleta;
  reportesRecientes: ReporteResumen[];
  archivosRecientes: ArchivoResumen[];
  metricas: MetricasEmpresa;
  acciones: {
    editarEmpresa: () => void;
    verReportes: () => void;
    nuevaCita: () => void;
  };
}

// 9. Crear/Editar Empresa
interface EmpresaFormScreenProps {
  empresa?: EmpresaCompleta;
  validaciones: ValidacionesEmpresa;
  guardar: (datos: EmpresaDatos) => Promise<void>;
  campos: CampoFormulario[];
}
```

#### **Reportes Móvil**
```typescript
// 10. Lista Reportes
interface ReportesListScreenProps {
  reportes: ReporteMovil[];
  filtros: {
    empresa: string;
    tipo: string;
    periodo: DateRange;
    estado: string;
  };
  ordenamiento: OrdenamientoConfig;
}

// 11. Visor Reportes
interface ReporteViewerScreenProps {
  reporte: ReporteCompleto;
  archivos: ArchivoAdjunto[];
  acciones: {
    descargar: () => Promise<void>;
    compartir: () => Promise<void>;
    imprimir: () => Promise<void>;
  };
  navegacion: {
    anterior: ReporteResumen;
    siguiente: ReporteResumen;
  };
}

// 12. Generador Reportes
interface ReporteGeneratorScreenProps {
  plantillas: PlantillaReporte[];
  empresaSeleccionada: EmpresaResumen;
  parametros: ParametrosReporte;
  generar: (config: ConfigGeneracion) => Promise<ReporteGenerado>;
}
```

#### **Cámara y Documentos**
```typescript
// 13. Escáner Documentos
interface DocumentScannerProps {
  configuracion: {
    tiposDocumento: TipoDocumento[];
    calidad: CalidadEscaneo;
    formatoSalida: FormatoArchivo;
  };
  procesamiento: {
    ocr: boolean;
    mejoramiento: boolean;
    deteccionBordes: boolean;
  };
  resultado: DocumentoEscaneado;
}

// 14. Galería Documentos
interface DocumentGalleryProps {
  documentos: DocumentoMovil[];
  filtros: FiltrosDocumento;
  acciones: {
    ver: (id: string) => void;
    compartir: (ids: string[]) => Promise<void>;
    eliminar: (ids: string[]) => Promise<void>;
    sincronizar: () => Promise<void>;
  };
}
```

#### **Configuración y Perfil**
```typescript
// 15. Configuración App
interface SettingsScreenProps {
  configuraciones: {
    notificaciones: ConfigNotificaciones;
    seguridad: ConfigSeguridad;
    sincronizacion: ConfigSincronizacion;
    idioma: ConfigIdioma;
    tema: ConfigTema;
  };
  cuenta: {
    perfil: PerfilUsuario;
    suscripcion: SuscripcionInfo;
    dispositivos: DispositivoRegistrado[];
  };
}

// Pantallas adicionales especializadas:
// 16. Chat IA Assistant
// 17. Calendario/Citas
// 18. Notificaciones Center
// 19. Offline Manager
// 20. Help & Support
```

### **Funcionalidades Móvil Específicas**

#### **Capacidades Offline**
```typescript
interface OfflineCapabilities {
  almacenamientoLocal: {
    empresas: EmpresaLocal[];
    reportes: ReporteLocal[];
    archivos: ArchivoLocal[];
    configuracion: ConfigLocal;
  };
  sincronizacion: {
    cola: AccionPendiente[];
    conflictos: ConflictoSincronizacion[];
    resolucion: ResolucionConflicto[];
  };
  cache: {
    imagenes: CacheImagenes;
    documentos: CacheDocumentos;
    datos: CacheDatos;
  };
}
```

#### **Push Notifications**
```typescript
interface PushNotificationConfig {
  tipos: {
    reporteNuevo: NotificacionConfig;
    documentoSubido: NotificacionConfig;
    recordatorioCita: NotificacionConfig;
    alertaCompliance: NotificacionConfig;
    sincronizacionCompleta: NotificacionConfig;
  };
  programacion: {
    horarios: HorarioNotificacion[];
    timezone: string;
    frecuencia: FrecuenciaConfig;
  };
  personalizacion: {
    sonidos: SonidoNotificacion[];
    colores: ColorNotificacion[];
    vibration: VibracionPattern[];
  };
}
```

#### **Biometric Authentication**
```typescript
interface BiometricAuthConfig {
  tipos: ('fingerprint' | 'face' | 'voice')[];
  configuracion: {
    requerirBiometrico: boolean;
    fallbackPIN: boolean;
    timeout: number;
    maxIntentos: number;
  };
  seguridad: {
    encriptacionLocal: boolean;
    saltHash: string;
    keychain: KeychainConfig;
  };
}
```

---

## 🤖 BOTS TELEGRAM

### **Arquitectura Bots**
- **Framework**: python-telegram-bot v20+
- **Arquitectura**: Webhook + Async handlers
- **Base de Datos**: Shared con API principal
- **Estados**: Finite State Machine (FSM)
- **Cache**: Redis para session management

### **Bot Administración**

#### **Comandos Principales**
```python
# Comandos de gestión
/start          # Menú principal administración
/empresas       # Gestión CRUD empresas
/reportes       # Gestión reportes
/usuarios       # Gestión usuarios sistema
/config         # Configuración sistema
/stats          # Estadísticas y métricas
/backup         # Backup y restauración
/deploy         # Comandos deployment
/logs           # Ver logs sistema
/alerts         # Configurar alertas
/help           # Ayuda administrativa

# Comandos avanzados
/empresas_bulk     # Operaciones masivas empresas
/reportes_batch    # Procesamiento batch reportes
/sync_manual       # Sincronización manual
/cache_clear       # Limpiar cache sistema
/db_query          # Queries directas BD (restringido)
/system_status     # Estado completo sistema
/performance       # Métricas performance
```

#### **Handlers Especializados**
```python
class AdminHandlers:
    async def empresas_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestión completa empresas con sub-menús"""
        # Menú: Crear, Listar, Editar, Eliminar, Buscar
        
    async def reportes_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestión reportes con filtros avanzados"""
        # Filtros: Por empresa, período, tipo, estado
        
    async def usuarios_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestión usuarios y permisos"""
        # CRUD usuarios, roles, permisos por país
        
    async def sync_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Control sincronización avanzado"""
        # Manual trigger, configuración, logs, errores
        
    async def analytics_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Dashboard analytics en Telegram"""
        # KPIs, gráficos texto, trending, alertas
```

### **Bot Producción (Usuarios Finales)**

#### **Comandos Usuario**
```python
# Comandos básicos
/start          # Onboarding y configuración inicial
/perfil         # Configuración perfil usuario
/empresas       # Listar mis empresas
/reportes       # Consultar reportes por RUT
/documentos     # Gestión documentos
/citas          # Agendar/ver citas
/notificaciones # Configurar notificaciones
/ayuda          # Asistente IA y help
/soporte        # Contactar soporte técnico

# Comandos avanzados
/reportes_rut   # Consulta específica por RUT
/documentos_upload  # Subir documentos vía bot
/citas_proximas     # Próximas citas programadas
/alertas            # Alertas personalizadas
/favoritos          # Empresas/reportes favoritos
/exportar           # Exportar datos
/comparar           # Comparar períodos
```

#### **Conversational AI Integration**
```python
class AIAssistantHandlers:
    async def natural_query_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesamiento consultas lenguaje natural"""
        # OpenAI GPT-4 integration para queries complejas
        
    async def financial_analysis_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Análisis financiero automático"""
        # Análisis tendencias, predicciones, insights
        
    async def document_analysis_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Análisis automático documentos"""
        # OCR, extracción datos, categorización
        
    async def compliance_checker_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Verificación compliance automática"""
        # Check regulaciones por país, alertas vencimientos
```

### **Sistema de Estados (FSM)**
```python
class ConversationStates:
    # Estados empresas
    EMPRESAS_MENU = "empresas_menu"
    EMPRESAS_CREAR = "empresas_crear"
    EMPRESAS_EDITAR = "empresas_editar"
    EMPRESAS_BUSCAR = "empresas_buscar"
    
    # Estados reportes
    REPORTES_MENU = "reportes_menu"
    REPORTES_FILTRAR = "reportes_filtrar"
    REPORTES_GENERAR = "reportes_generar"
    
    # Estados documentos
    DOCUMENTOS_UPLOAD = "documentos_upload"
    DOCUMENTOS_CATEGORIZAR = "documentos_categorizar"
    
    # Estados citas
    CITAS_AGENDAR = "citas_agendar"
    CITAS_CONFIRMAR = "citas_confirmar"
    
    # Estados IA
    AI_CONVERSACION = "ai_conversacion"
    AI_ANALISIS = "ai_analisis"
```

---

## 🗄️ INTEGRACIÓN AIRTABLE

### **Configuración Multi-País**

#### **Estructura Bases por País**
```javascript
// Chile
{
  baseId: 'appChileContabilidad123',
  tableName: 'Reportes_Empresas_CL',
  fields: {
    'Empresa': 'singleLineText',
    'RUT': 'singleLineText',
    'Tipo_Documento': 'singleSelect',
    'Fecha_Subida': 'date',
    'Archivo_Adjunto': 'multipleAttachments',
    'Estado_Procesamiento': 'singleSelect',
    'Comentarios': 'longText',
    'Moneda': 'singleSelect',
    'Monto_Total': 'currency',
    'Periodo_Fiscal': 'singleLineText'
  },
  views: {
    'Pendientes_Procesamiento': 'Registros con estado Pendiente',
    'Por_Empresa': 'Agrupado por empresa',
    'Por_Periodo': 'Agrupado por período fiscal'
  }
}

// Colombia
{
  baseId: 'appColombiaContabilidad456',
  tableName: 'Reportes_Empresas_CO',
  fields: {
    'Empresa': 'singleLineText',
    'NIT': 'singleLineText',
    'Tipo_Documento': 'singleSelect',
    // ... campos similares adaptados a Colombia
  }
}

// México
{
  baseId: 'appMexicoContabilidad789',
  tableName: 'Reportes_Empresas_MX',
  fields: {
    'Empresa': 'singleLineText',
    'RFC': 'singleLineText',
    'Tipo_Documento': 'singleSelect',
    // ... campos similares adaptados a México
  }
}
```

#### **Servicio Airtable Multi-País**
```python
class AirtableMultiCountryService:
    def __init__(self):
        self.country_configs = {
            'CL': AirtableConfig(
                api_key=settings.AIRTABLE_CL_API_KEY,
                base_id=settings.AIRTABLE_CL_BASE_ID,
                table_name='Reportes_Empresas_CL'
            ),
            'CO': AirtableConfig(
                api_key=settings.AIRTABLE_CO_API_KEY,
                base_id=settings.AIRTABLE_CO_BASE_ID,
                table_name='Reportes_Empresas_CO'
            ),
            'MX': AirtableConfig(
                api_key=settings.AIRTABLE_MX_API_KEY,
                base_id=settings.AIRTABLE_MX_BASE_ID,
                table_name='Reportes_Empresas_MX'
            )
        }
    
    async def get_pending_records(self, country_code: str) -> List[Dict]:
        """Obtener registros pendientes por país"""
        config = self.country_configs[country_code]
        client = Airtable(config.base_id, config.table_name, config.api_key)
        
        formula = "AND({Estado_Procesamiento} = 'Pendiente', {Archivo_Adjunto} != '')"
        records = client.get_all(formula=formula)
        
        return [self._transform_record(record, country_code) for record in records]
    
    async def mark_as_processed(self, record_id: str, country_code: str, 
                              processing_details: Dict) -> bool:
        """Marcar registro como procesado"""
        config = self.country_configs[country_code]
        client = Airtable(config.base_id, config.table_name, config.api_key)
        
        update_data = {
            'Estado_Procesamiento': 'Procesado',
            'Fecha_Procesamiento': datetime.now().isoformat(),
            'Comentarios': f"Procesado automáticamente: {processing_details}"
        }
        
        return client.update(record_id, update_data)
    
    def _transform_record(self, record: Dict, country_code: str) -> Dict:
        """Transformar registro según configuración país"""
        transformers = {
            'CL': self._transform_chile_record,
            'CO': self._transform_colombia_record,
            'MX': self._transform_mexico_record
        }
        
        return transformers[country_code](record)
    
    def _extract_tax_id(self, empresa_name: str, country_code: str) -> str:
        """Extraer ID fiscal según país"""
        patterns = {
            'CL': r'\((\d{1,2}\.\d{3}\.\d{3}-[0-9K])\)',  # RUT Chile
            'CO': r'\((\d{8,10}-\d)\)',                    # NIT Colombia  
            'MX': r'\(([A-Z]{4}\d{6}[A-Z0-9]{3})\)'        # RFC México
        }
        
        pattern = patterns[country_code]
        match = re.search(pattern, empresa_name)
        return match.group(1) if match else None
```

### **Webhooks y Sincronización Tiempo Real**
```python
class AirtableWebhookHandler:
    async def handle_webhook(self, webhook_data: Dict) -> Dict:
        """Procesar webhook de Airtable"""
        country_code = self._extract_country_from_webhook(webhook_data)
        
        if webhook_data['actionMetadata']['source'] == 'client':
            # Cambio manual por usuario
            await self._process_manual_change(webhook_data, country_code)
        
        elif webhook_data['changedTablesById']:
            # Cambios en tabla
            await self._process_table_changes(webhook_data, country_code)
        
        return {'status': 'processed', 'country': country_code}
    
    async def _process_manual_change(self, data: Dict, country_code: str):
        """Procesar cambio manual en Airtable"""
        # Trigger sincronización inmediata
        sync_service = SyncService(country_code)
        await sync_service.sync_specific_records(data['changedRecordsById'])
    
    async def setup_webhooks_all_countries(self):
        """Configurar webhooks para todos los países"""
        for country_code in self.country_configs.keys():
            await self._setup_country_webhook(country_code)
```

---

## 📝 INTEGRACIÓN NOTION

### **Workspace Ejecutivo**

#### **Estructura Notion por País**
```javascript
// Workspace: "ACA Global Executive Dashboard"
{
  databases: {
    // Base principal por país
    [`Empresas_${country_code}`]: {
      properties: {
        'Nombre': 'title',
        'ID_Fiscal': 'rich_text',
        'Estado': 'select',
        'Ingresos_Anuales': 'number',
        'Moneda': 'select',
        'Sector': 'select',
        'Tamaño': 'select',
        'Última_Actualización': 'date',
        'Reportes_Pendientes': 'number',
        'Compliance_Score': 'number',
        'Tendencia_Ingresos': 'select'
      }
    },
    
    [`Dashboard_Ejecutivo_${country_code}`]: {
      properties: {
        'Mes': 'date',
        'KPI': 'select',
        'Valor': 'number',
        'Meta': 'number',
        'Variación': 'number',
        'Tendencia': 'select',
        'Comentarios': 'rich_text'
      }
    },
    
    [`Reportes_Mensuales_${country_code}`]: {
      properties: {
        'Empresa': 'relation', // Referencia a Empresas
        'Período': 'date',
        'Tipo_Reporte': 'select',
        'Estado': 'select',
        'Ingresos': 'number',
        'Gastos': 'number',
        'Utilidad': 'formula', // Ingresos - Gastos
        'Margin_%': 'formula',  // (Utilidad/Ingresos)*100
        'Archivos_Adjuntos': 'files'
      }
    }
  },
  
  pages: {
    [`Dashboard_CEO_${country_code}`]: {
      template: 'executive_dashboard',
      sections: [
        'KPIs_Principales',
        'Tendencias_Financieras', 
        'Top_Empresas_Clientes',
        'Alertas_Compliance',
        'Métricas_Operacionales'
      ]
    }
  }
}
```

#### **Templates Automáticos**
```python
class NotionTemplateService:
    async def create_monthly_executive_report(self, country_code: str, 
                                            month: datetime) -> str:
        """Crear reporte ejecutivo mensual automático"""
        
        # Obtener datos del mes
        monthly_data = await self._get_monthly_aggregated_data(country_code, month)
        
        # Template structure
        template = {
            'parent': {'database_id': self.databases[f'Reportes_Ejecutivos_{country_code}']},
            'properties': {
                'Título': {
                    'title': [{'text': {'content': f'Reporte Ejecutivo {month.strftime("%B %Y")}'}}]
                },
                'Período': {'date': {'start': month.isoformat()}},
                'País': {'select': {'name': country_code}},
                'Total_Ingresos': {'number': monthly_data['total_ingresos']},
                'Total_Empresas': {'number': monthly_data['total_empresas']},
                'Nuevas_Empresas': {'number': monthly_data['nuevas_empresas']},
                'Compliance_Score': {'number': monthly_data['compliance_average']}
            },
            'children': await self._build_executive_content(monthly_data, country_code)
        }
        
        page = await self.notion_client.pages.create(**template)
        return page['id']
    
    async def _build_executive_content(self, data: Dict, country_code: str) -> List[Dict]:
        """Construir contenido ejecutivo con bloques Notion"""
        content = []
        
        # KPIs Dashboard
        content.append({
            'object': 'block',
            'type': 'heading_1',
            'heading_1': {'rich_text': [{'text': {'content': '📊 KPIs Principales'}}]}
        })
        
        # Tabla KPIs
        kpis_table = await self._create_kpis_table(data)
        content.append(kpis_table)
        
        # Gráfico ingresos (embebido desde Chart.js API)
        content.append({
            'object': 'block', 
            'type': 'image',
            'image': {
                'type': 'external',
                'external': {'url': await self._generate_chart_url(data, 'ingresos')}
            }
        })
        
        # Top empresas
        content.append({
            'object': 'block',
            'type': 'heading_2', 
            'heading_2': {'rich_text': [{'text': {'content': '🏢 Top 10 Empresas'}}]}
        })
        
        top_empresas = await self._create_top_empresas_table(data)
        content.append(top_empresas)
        
        # Alertas compliance
        content.append({
            'object': 'block',
            'type': 'heading_2',
            'heading_2': {'rich_text': [{'text': {'content': '⚠️ Alertas Compliance'}}]}
        })
        
        alertas = await self._create_compliance_alerts(data, country_code)
        content.extend(alertas)
        
        return content
```

### **Sincronización Bidireccional**
```python
class NotionSyncService:
    async def sync_supabase_to_notion(self, country_code: str) -> SyncResult:
        """Sincronizar datos Supabase → Notion"""
        
        # Obtener datos Supabase
        empresas = await self.supabase_service.get_empresas_by_country(country_code)
        reportes = await self.supabase_service.get_reportes_by_country(country_code)
        
        # Sincronizar empresas
        empresas_synced = []
        for empresa in empresas:
            notion_page = await self._sync_empresa_to_notion(empresa, country_code)
            empresas_synced.append(notion_page)
        
        # Sincronizar reportes
        reportes_synced = []
        for reporte in reportes:
            notion_record = await self._sync_reporte_to_notion(reporte, country_code)
            reportes_synced.append(notion_record)
        
        # Actualizar dashboard ejecutivo
        await self._update_executive_dashboard(country_code)
        
        return SyncResult(
            empresas_synced=len(empresas_synced),
            reportes_synced=len(reportes_synced),
            errors=[],
            duration=time.time() - start_time
        )
    
    async def sync_notion_to_supabase(self, country_code: str) -> SyncResult:
        """Sincronizar cambios Notion → Supabase"""
        
        # Detectar cambios en Notion desde última sync
        last_sync = await self._get_last_sync_timestamp(country_code)
        changed_pages = await self.notion_client.search({
            'filter': {
                'and': [
                    {'property': 'object', 'value': 'page'},
                    {'timestamp': 'last_edited_time', 'last_edited_time': {'after': last_sync}}
                ]
            }
        })
        
        # Procesar cambios
        for page in changed_pages['results']:
            await self._process_notion_change(page, country_code)
        
        return SyncResult(pages_processed=len(changed_pages['results']))
```

---

## 💬 INTEGRACIÓN SLACK

### **Arquitectura Slack**

#### **Slack App Configuration**
```json
{
  "name": "ACA Contabilidad Assistant",
  "description": "Asistente contable multi-país con notificaciones automáticas",
  "scopes": [
    "channels:read",
    "channels:write", 
    "chat:write",
    "commands",
    "files:write",
    "reactions:read",
    "reactions:write",
    "users:read",
    "users:read.email",
    "workflow.steps:execute"
  ],
  "features": {
    "bot_user": true,
    "slash_commands": true,
    "event_subscriptions": true,
    "interactive_components": true,
    "workflow_steps": true
  }
}
```

#### **Canales Automáticos por País**
```python
class SlackChannelManager:
    async def setup_country_channels(self, country_code: str) -> Dict[str, str]:
        """Crear estructura canales por país"""
        
        channels = {}
        
        # Canal principal país
        main_channel = await self.slack_client.conversations_create(
            name=f"aca-{country_code.lower()}",
            is_private=False
        )
        channels['main'] = main_channel['channel']['id']
        
        # Canal notificaciones automáticas
        notifications_channel = await self.slack_client.conversations_create(
            name=f"aca-{country_code.lower()}-alerts",
            is_private=False,
            topic=f"Notificaciones automáticas ACA {country_code}"
        )
        channels['notifications'] = notifications_channel['channel']['id']
        
        # Canal reportes ejecutivos
        executive_channel = await self.slack_client.conversations_create(
            name=f"aca-{country_code.lower()}-executive", 
            is_private=True,
            topic=f"Reportes ejecutivos {country_code} - Solo leadership"
        )
        channels['executive'] = executive_channel['channel']['id']
        
        # Canal soporte técnico
        support_channel = await self.slack_client.conversations_create(
            name=f"aca-{country_code.lower()}-support",
            is_private=False,
            topic=f"Soporte técnico ACA {country_code}"
        )
        channels['support'] = support_channel['channel']['id']
        
        return channels
```

#### **Comandos Slash Específicos**
```python
class SlackCommands:
    @slash_command('/aca-status')
    async def status_command(self, ack, body, client):
        """Estado general del sistema"""
        await ack()
        
        country_code = await self._detect_user_country(body['user_id'])
        status = await self.system_service.get_system_status(country_code)
        
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"🔧 Estado ACA {country_code}"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Base Datos:* {status['database']}"},
                    {"type": "mrkdwn", "text": f"*Airtable:* {status['airtable']}"},
                    {"type": "mrkdwn", "text": f"*Bots:* {status['telegram_bots']}"},
                    {"type": "mrkdwn", "text": f"*Sync:* {status['last_sync']}"}
                ]
            }
        ]
        
        await client.chat_postMessage(
            channel=body['channel_id'],
            blocks=blocks,
            text=f"Estado ACA {country_code}"
        )
    
    @slash_command('/aca-empresas')
    async def empresas_command(self, ack, body, client):
        """Listar empresas con filtros"""
        await ack()
        
        # Parse parámetros: /aca-empresas activas sector:tecnologia
        params = self._parse_command_params(body['text'])
        country_code = await self._detect_user_country(body['user_id'])
        
        empresas = await self.empresa_service.get_empresas_filtered(
            country_code=country_code,
            **params
        )
        
        # Crear mensaje interactivo
        blocks = self._build_empresas_blocks(empresas[:10])  # Límite Slack
        
        await client.chat_postMessage(
            channel=body['channel_id'],
            blocks=blocks,
            text=f"Empresas en {country_code}"
        )
    
    @slash_command('/aca-sync')
    async def sync_command(self, ack, body, client):
        """Triggear sincronización manual"""
        await ack()
        
        country_code = await self._detect_user_country(body['user_id'])
        
        # Verificar permisos usuario
        if not await self._user_has_sync_permission(body['user_id'], country_code):
            await client.chat_postEphemeral(
                channel=body['channel_id'],
                user=body['user_id'],
                text="❌ No tienes permisos para ejecutar sincronización"
            )
            return
        
        # Iniciar sync asíncrona
        sync_task = await self.sync_service.start_manual_sync(country_code)
        
        await client.chat_postMessage(
            channel=body['channel_id'],
            text=f"🔄 Sincronización iniciada para {country_code} (ID: {sync_task.id})"
        )
    
    @slash_command('/aca-reporte')
    async def reporte_command(self, ack, body, client):
        """Generar reporte específico"""
        await ack()
        
        # Formato: /aca-reporte empresa:RUT_EMPRESA tipo:balance periodo:2025-01
        params = self._parse_command_params(body['text'])
        
        if 'empresa' not in params:
            await client.chat_postEphemeral(
                channel=body['channel_id'],
                user=body['user_id'],
                text="❌ Parámetro empresa (RUT) requerido"
            )
            return
        
        # Generar reporte
        reporte = await self.reporte_service.generate_report(**params)
        
        # Subir archivo a Slack
        file_upload = await client.files_upload_v2(
            channel=body['channel_id'],
            file=reporte['file_path'],
            title=reporte['title'],
            initial_comment=f"📊 Reporte generado: {reporte['title']}"
        )
```

#### **Notificaciones Automáticas**
```python
class SlackNotificationService:
    async def send_sync_completion_notification(self, country_code: str, 
                                              sync_result: SyncResult):
        """Notificar finalización sincronización"""
        
        channel_id = await self._get_notifications_channel(country_code)
        
        if sync_result.success:
            color = "good"
            icon = "✅"
            message = "Sincronización completada exitosamente"
        else:
            color = "danger" 
            icon = "❌"
            message = "Sincronización completada con errores"
        
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{icon} *{message}*\n*País:* {country_code}\n*Duración:* {sync_result.duration}s"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Registros procesados:* {sync_result.processed}"},
                    {"type": "mrkdwn", "text": f"*Errores:* {len(sync_result.errors)}"},
                    {"type": "mrkdwn", "text": f"*Empresas actualizadas:* {sync_result.empresas_updated}"},
                    {"type": "mrkdwn", "text": f"*Reportes nuevos:* {sync_result.reportes_created}"}
                ]
            }
        ]
        
        if sync_result.errors:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": f"*Errores encontrados:*\n```{chr(10).join(sync_result.errors[:5])}```"
                }
            })
        
        await self.slack_client.chat_postMessage(
            channel=channel_id,
            blocks=blocks,
            attachments=[{"color": color}]
        )
    
    async def send_compliance_alert(self, country_code: str, alert: ComplianceAlert):
        """Enviar alerta compliance"""
        
        channel_id = await self._get_notifications_channel(country_code)
        
        urgency_config = {
            'high': {'color': 'danger', 'icon': '🚨', 'mention': '<!channel>'},
            'medium': {'color': 'warning', 'icon': '⚠️', 'mention': ''},
            'low': {'color': 'good', 'icon': 'ℹ️', 'mention': ''}
        }
        
        config = urgency_config[alert.urgency]
        
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{config['icon']} *Alerta Compliance* {config['mention']}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*País:* {country_code}"},
                    {"type": "mrkdwn", "text": f"*Empresa:* {alert.empresa_name}"},
                    {"type": "mrkdwn", "text": f"*Tipo:* {alert.alert_type}"},
                    {"type": "mrkdwn", "text": f"*Vencimiento:* {alert.due_date}"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Descripción:*\n{alert.description}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Ver detalles"},
                        "action_id": f"compliance_details_{alert.id}",
                        "style": "primary"
                    },
                    {
                        "type": "button", 
                        "text": {"type": "plain_text", "text": "Marcar resuelto"},
                        "action_id": f"compliance_resolve_{alert.id}"
                    }
                ]
            }
        ]
        
        await self.slack_client.chat_postMessage(
            channel=channel_id,
            blocks=blocks,
            attachments=[{"color": config['color']}]
        )
```

---

## 📅 INTEGRACIÓN CALENDLY

### **Configuración Multi-País**

#### **Calendly Setup por País**
```python
class CalendlyMultiCountryService:
    def __init__(self):
        self.country_configs = {
            'CL': CalendlyConfig(
                api_key=settings.CALENDLY_CL_API_KEY,
                organization_uri=settings.CALENDLY_CL_ORG_URI,
                timezone='America/Santiago',
                event_types=['consultoria-contable-cl', 'revision-reportes-cl', 'planificacion-fiscal-cl']
            ),
            'CO': CalendlyConfig(
                api_key=settings.CALENDLY_CO_API_KEY,
                organization_uri=settings.CALENDLY_CO_ORG_URI,
                timezone='America/Bogota',
                event_types=['consultoria-contable-co', 'revision-reportes-co', 'planificacion-fiscal-co']
            ),
            'MX': CalendlyConfig(
                api_key=settings.CALENDLY_MX_API_KEY,
                organization_uri=settings.CALENDLY_MX_ORG_URI,
                timezone='America/Mexico_City',
                event_types=['consultoria-contable-mx', 'revision-reportes-mx', 'planificacion-fiscal-mx']
            )
        }
    
    async def get_available_slots(self, country_code: str, 
                                date_range: DateRange) -> List[AvailableSlot]:
        """Obtener slots disponibles por país"""
        config = self.country_configs[country_code]
        
        availability = await self.calendly_client.get_user_availability(
            user_uri=config.user_uri,
            start_time=date_range.start.isoformat(),
            end_time=date_range.end.isoformat()
        )
        
        slots = []
        for event_type in config.event_types:
            event_slots = await self._get_event_type_availability(
                event_type, availability, config.timezone
            )
            slots.extend(event_slots)
        
        return sorted(slots, key=lambda x: x.start_time)
    
    async def schedule_meeting(self, country_code: str, 
                             meeting_request: MeetingRequest) -> ScheduledMeeting:
        """Agendar reunión específica por país"""
        config = self.country_configs[country_code]
        
        # Validar disponibilidad
        is_available = await self._validate_slot_availability(
            config, meeting_request.start_time, meeting_request.duration
        )
        
        if not is_available:
            raise ValueError("Slot no disponible")
        
        # Crear invitación
        invitee_data = {
            'email': meeting_request.invitee_email,
            'name': meeting_request.invitee_name,
            'text_reminder_number': meeting_request.phone_number,
            'custom_answers': {
                'empresa_rut': meeting_request.empresa_rut,
                'tipo_consulta': meeting_request.consultation_type,
                'descripcion': meeting_request.description
            }
        }
        
        scheduled_event = await self.calendly_client.schedule_event(
            event_type_uri=f"{config.organization_uri}/event_types/{meeting_request.event_type}",
            start_time=meeting_request.start_time.isoformat(),
            invitee=invitee_data
        )
        
        # Sincronizar con Google Calendar
        if config.google_calendar_integration:
            await self._sync_to_google_calendar(scheduled_event, country_code)
        
        # Enviar notificación Telegram
        await self._send_telegram_confirmation(scheduled_event, country_code)
        
        return ScheduledMeeting(
            calendly_event_uri=scheduled_event['uri'],
            start_time=scheduled_event['start_time'],
            end_time=scheduled_event['end_time'],
            join_url=scheduled_event['location']['join_url'],
            country_code=country_code
        )
```

#### **Tipos de Reuniones por País**
```python
class MeetingTypesConfig:
    TYPES_BY_COUNTRY = {
        'CL': {
            'consultoria-contable-cl': {
                'name': 'Consultoría Contable Chile',
                'duration': 60,  # minutos
                'description': 'Asesoría contable y fiscal para empresas chilenas',
                'questions': [
                    {'name': 'empresa_rut', 'type': 'string', 'required': True},
                    {'name': 'sector_empresa', 'type': 'select', 'options': ['Tecnología', 'Retail', 'Servicios', 'Manufactura']},
                    {'name': 'tipo_consulta', 'type': 'select', 'options': ['Balance', 'Declaración Renta', 'Planificación Fiscal', 'Otro']},
                    {'name': 'urgencia', 'type': 'select', 'options': ['Alta', 'Media', 'Baja']}
                ],
                'calendar_integration': True,
                'reminder_settings': {
                    'email': [24, 2],  # horas antes
                    'sms': [2],        # horas antes
                    'telegram': [24, 4, 1]  # horas antes
                }
            },
            'revision-reportes-cl': {
                'name': 'Revisión Reportes Financieros',
                'duration': 45,
                'description': 'Revisión y análisis de reportes financieros mensuales',
                'questions': [
                    {'name': 'empresa_rut', 'type': 'string', 'required': True},
                    {'name': 'periodo_revision', 'type': 'string', 'required': True},
                    {'name': 'reportes_revisar', 'type': 'multiselect', 'options': ['Balance', 'Estado Resultados', 'Flujo Caja']},
                    {'name': 'documentos_adjuntos', 'type': 'boolean'}
                ]
            }
        },
        'CO': {
            'consultoria-contable-co': {
                'name': 'Consultoría Contable Colombia',
                'duration': 60,
                'description': 'Asesoría contable NIIF para empresas colombianas',
                'questions': [
                    {'name': 'empresa_nit', 'type': 'string', 'required': True},
                    {'name': 'regimen_tributario', 'type': 'select', 'options': ['Ordinario', 'Simplificado', 'Gran Contribuyente']},
                    {'name': 'tipo_consulta', 'type': 'select', 'options': ['Estados Financieros NIIF', 'Declaración Renta', 'IVA', 'Otro']}
                ]
            }
        },
        'MX': {
            'consultoria-contable-mx': {
                'name': 'Consultoría Contable México',
                'duration': 60,
                'description': 'Asesoría contable NIF para empresas mexicanas',
                'questions': [
                    {'name': 'empresa_rfc', 'type': 'string', 'required': True},
                    {'name': 'regimen_fiscal', 'type': 'select', 'options': ['General', 'Simplificado', 'RESICO']},
                    {'name': 'tipo_consulta', 'type': 'select', 'options': ['Estados Financieros NIF', 'Declaración Anual', 'CFDI', 'Otro']}
                ]
            }
        }
    }
```

#### **Integración Google Calendar**
```python
class GoogleCalendarIntegration:
    async def sync_calendly_to_google(self, calendly_event: Dict, 
                                    country_code: str) -> str:
        """Sincronizar evento Calendly → Google Calendar"""
        
        config = self.country_configs[country_code]
        calendar_service = await self._get_google_calendar_service(country_code)
        
        # Preparar evento Google Calendar
        google_event = {
            'summary': calendly_event['name'],
            'description': f"""
                Reunión agendada via Calendly
                
                Tipo: {calendly_event['event_type']}
                Empresa: {calendly_event['invitee']['custom_answers'].get('empresa_rut', 'N/A')}
                
                Detalles reunión:
                {calendly_event['invitee']['custom_answers'].get('descripcion', '')}
                
                Link Calendly: {calendly_event['uri']}
            """,
            'start': {
                'dateTime': calendly_event['start_time'],
                'timeZone': config.timezone
            },
            'end': {
                'dateTime': calendly_event['end_time'], 
                'timeZone': config.timezone
            },
            'attendees': [
                {'email': calendly_event['invitee']['email']},
                {'email': config.organizer_email}
            ],
            'conferenceData': {
                'createRequest': {
                    'requestId': f"calendly-{calendly_event['uuid']}",
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                }
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 24 horas
                    {'method': 'popup', 'minutes': 120},       # 2 horas
                    {'method': 'popup', 'minutes': 60}         # 1 hora
                ]
            }
        }
        
        # Crear evento
        created_event = calendar_service.events().insert(
            calendarId='primary',
            body=google_event,
            conferenceDataVersion=1
        ).execute()
        
        # Guardar mapping Calendly ↔ Google Calendar
        await self._save_calendar_mapping(
            calendly_uri=calendly_event['uri'],
            google_event_id=created_event['id'],
            country_code=country_code
        )
        
        return created_event['id']
```

#### **Recordatorios Telegram Automáticos**
```python
class CalendlyTelegramReminders:
    async def setup_meeting_reminders(self, scheduled_meeting: ScheduledMeeting,
                                    country_code: str):
        """Configurar recordatorios automáticos Telegram"""
        
        reminder_times = [
            (24, 'hours'),  # 24 horas antes
            (4, 'hours'),   # 4 horas antes  
            (1, 'hours'),   # 1 hora antes
            (15, 'minutes') # 15 minutos antes
        ]
        
        for time_value, time_unit in reminder_times:
            reminder_datetime = scheduled_meeting.start_time - timedelta(**{time_unit: time_value})
            
            # Programar tarea celery para recordatorio
            send_meeting_reminder.apply_async(
                args=[scheduled_meeting.id, country_code, time_value, time_unit],
                eta=reminder_datetime
            )
    
    @celery.task
    def send_meeting_reminder(meeting_id: str, country_code: str, 
                            time_value: int, time_unit: str):
        """Enviar recordatorio Telegram (tarea async)"""
        
        # Obtener detalles reunión
        meeting = get_meeting_details(meeting_id)
        
        # Obtener chat_id usuario Telegram
        user_telegram = get_user_telegram_by_email(meeting.invitee_email, country_code)
        
        if not user_telegram:
            return  # Usuario no tiene Telegram configurado
        
        # Mensaje personalizado según tiempo restante
        if time_unit == 'hours' and time_value == 24:
            message = f"""
🗓️ *Recordatorio: Reunión mañana*

📅 *Fecha:* {meeting.start_time.strftime('%d/%m/%Y')}
🕐 *Hora:* {meeting.start_time.strftime('%H:%M')}
📋 *Tipo:* {meeting.event_type}
🏢 *Empresa:* {meeting.empresa_name}

💬 *Link reunión:* {meeting.join_url}

¿Necesitas reagendar? Responde con /reagendar
            """
        elif time_unit == 'hours' and time_value == 4:
            message = f"""
⏰ *Tu reunión es en 4 horas*

🕐 *Hora:* {meeting.start_time.strftime('%H:%M')}
💬 *Link:* {meeting.join_url}

¿Todo listo? Responde ✅ para confirmar
            """
        elif time_unit == 'hours' and time_value == 1:
            message = f"""
🚨 *¡Reunión en 1 hora!*

💬 *Link:* {meeting.join_url}
📋 *Preparación sugerida:*
• Tener documentos listos
• Probar conexión
• Preparar preguntas

🔔 Recibirás otro recordatorio en 15 minutos
            """
        else:  # 15 minutos
            message = f"""
🔴 *¡Reunión en 15 minutos!*

💬 *UNIRSE AHORA:* {meeting.join_url}

*Tip:* Únete unos minutos antes para probar audio/video
            """
        
        # Enviar mensaje
        bot = get_telegram_bot(country_code)
        bot.send_message(
            chat_id=user_telegram.chat_id,
            text=message,
            parse_mode='Markdown',
            reply_markup=get_meeting_reminder_keyboard(meeting.id)
        )
```

---

## 🗃️ SISTEMA DE BASE DE DATOS MULTI-PAÍS

### **Arquitectura Base de Datos**

#### **Supabase Multi-Regional Setup**
```sql
-- CONFIGURACIÓN GLOBAL (Master Database)
CREATE SCHEMA global;

-- Tabla países y configuraciones
CREATE TABLE global.countries (
    code VARCHAR(2) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    currency_code VARCHAR(3) NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    language_code VARCHAR(5) NOT NULL,
    database_url TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla organizaciones globales  
CREATE TABLE global.organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    country_codes TEXT[] NOT NULL,
    subscription_type VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla usuarios globales
CREATE TABLE global.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    country_codes TEXT[] NOT NULL, -- Países a los que tiene acceso
    role VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla monedas y tipos de cambio
CREATE TABLE global.currencies (
    code VARCHAR(3) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    decimal_places INTEGER DEFAULT 2,
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE global.exchange_rates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    from_currency VARCHAR(3) REFERENCES global.currencies(code),
    to_currency VARCHAR(3) REFERENCES global.currencies(code),
    rate DECIMAL(15,6) NOT NULL,
    source VARCHAR(50) NOT NULL,
    valid_from TIMESTAMPTZ NOT NULL,
    valid_to TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(from_currency, to_currency, valid_from)
);

-- ESQUEMA POR PAÍS (Replicado en cada región)
CREATE SCHEMA country_{COUNTRY_CODE};

-- Empresas locales
CREATE TABLE country_{COUNTRY_CODE}.empresas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES global.organizations(id),
    nombre VARCHAR(255) NOT NULL,
    tax_id VARCHAR(50) UNIQUE NOT NULL, -- RUT/NIT/RFC según país
    razon_social VARCHAR(255),
    email VARCHAR(255),
    telefono VARCHAR(50),
    direccion TEXT,
    sector VARCHAR(100),
    tamaño VARCHAR(20) CHECK (tamaño IN ('pequeña', 'mediana', 'grande')),
    estado VARCHAR(20) DEFAULT 'activa' CHECK (estado IN ('activa', 'inactiva', 'suspendida')),
    currency_code VARCHAR(3) DEFAULT '{DEFAULT_CURRENCY}',
    
    -- Campos específicos por país
    configuracion_local JSONB DEFAULT '{}',
    
    -- Compliance tracking
    compliance_score INTEGER DEFAULT 0 CHECK (compliance_score >= 0 AND compliance_score <= 100),
    last_compliance_check TIMESTAMPTZ,
    
    -- Auditoría
    created_by UUID REFERENCES global.users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- RLS
    CONSTRAINT rls_empresa_organization CHECK (organization_id IS NOT NULL)
);

-- Reportes mensuales
CREATE TABLE country_{COUNTRY_CODE}.reportes_mensuales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id UUID REFERENCES country_{COUNTRY_CODE}.empresas(id) ON DELETE CASCADE,
    
    -- Información básica
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    tipo_reporte VARCHAR(100) NOT NULL,
    subtipo_reporte VARCHAR(100),
    
    -- Período fiscal
    anio INTEGER NOT NULL CHECK (anio >= 2020 AND anio <= 2030),
    mes INTEGER NOT NULL CHECK (mes >= 1 AND mes <= 12),
    trimestre INTEGER CHECK (trimestre >= 1 AND trimestre <= 4),
    
    -- Estado y procesamiento
    estado VARCHAR(50) DEFAULT 'borrador' CHECK (estado IN ('borrador', 'pendiente', 'en_revision', 'aprobado', 'rechazado', 'enviado')),
    
    -- Montos financieros (estructura JSONB para multi-moneda)
    montos JSONB DEFAULT '{}', 
    /* Estructura ejemplo:
    {
      "ingresos": {"amount": 50000000, "currency": "CLP", "usd_amount": 55555.56},
      "gastos": {"amount": 30000000, "currency": "CLP", "usd_amount": 33333.33},
      "utilidad": {"amount": 20000000, "currency": "CLP", "usd_amount": 22222.22}
    }
    */
    
    -- Compliance y regulaciones
    regulatory_info JSONB DEFAULT '{}',
    compliance_status VARCHAR(50) DEFAULT 'pending',
    
    -- Metadatos
    source_system VARCHAR(50) DEFAULT 'manual', -- manual, airtable, api
    external_id VARCHAR(255), -- ID en sistema origen (Airtable, etc.)
    comentarios TEXT,
    
    -- Auditoría
    created_by UUID REFERENCES global.users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints únicos
    UNIQUE(empresa_id, anio, mes, tipo_reporte, subtipo_reporte)
);

-- Archivos de reportes
CREATE TABLE country_{COUNTRY_CODE}.archivos_reportes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporte_id UUID REFERENCES country_{COUNTRY_CODE}.reportes_mensuales(id) ON DELETE CASCADE,
    empresa_id UUID REFERENCES country_{COUNTRY_CODE}.empresas(id) ON DELETE CASCADE,
    
    -- Información archivo
    nombre_archivo VARCHAR(255) NOT NULL,
    nombre_original VARCHAR(255),
    tipo_archivo VARCHAR(100),
    extension VARCHAR(10),
    tamaño_bytes BIGINT,
    checksum_md5 VARCHAR(32),
    
    -- URLs y almacenamiento
    url_archivo TEXT NOT NULL,
    url_thumbnail TEXT,
    storage_provider VARCHAR(50) DEFAULT 'supabase',
    storage_path TEXT,
    
    -- Metadatos
    descripcion TEXT,
    tags TEXT[],
    categoria VARCHAR(100),
    
    -- Procesamiento y OCR
    ocr_text TEXT,
    extracted_data JSONB DEFAULT '{}',
    processing_status VARCHAR(50) DEFAULT 'pending',
    
    -- Versionado
    version INTEGER DEFAULT 1,
    parent_file_id UUID REFERENCES country_{COUNTRY_CODE}.archivos_reportes(id),
    
    -- Estado
    activo BOOLEAN DEFAULT true,
    
    -- Seguridad y acceso
    access_level VARCHAR(20) DEFAULT 'private' CHECK (access_level IN ('public', 'organization', 'private')),
    
    -- Auditoría
    uploaded_by UUID REFERENCES global.users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Información adicional de empresas
CREATE TABLE country_{COUNTRY_CODE}.info_compania (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id UUID REFERENCES country_{COUNTRY_CODE}.empresas(id) ON DELETE CASCADE,
    
    -- Información financiera adicional
    ingresos_anuales_estimados DECIMAL(15,2),
    numero_empleados INTEGER,
    fecha_constitucion DATE,
    
    -- Información de contacto expandida
    representante_legal VARCHAR(255),
    contador_asignado VARCHAR(255),
    email_contador VARCHAR(255),
    telefono_contador VARCHAR(50),
    
    -- Configuración específica
    configuracion_reportes JSONB DEFAULT '{}',
    configuracion_notificaciones JSONB DEFAULT '{}',
    
    -- Compliance específico
    licencias_requeridas TEXT[],
    fechas_vencimiento_licencias JSONB DEFAULT '{}',
    
    -- Metadatos
    notas TEXT,
    ultima_revision TIMESTAMPTZ,
    
    -- Auditoría
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraint único
    UNIQUE(empresa_id)
);

-- Logs de sincronización
CREATE TABLE country_{COUNTRY_CODE}.sync_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Información de sincronización
    sync_type VARCHAR(50) NOT NULL, -- airtable, notion, slack, manual
    sync_direction VARCHAR(20) NOT NULL, -- inbound, outbound, bidirectional
    source_system VARCHAR(50) NOT NULL,
    target_system VARCHAR(50) NOT NULL,
    
    -- Timing
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    duration_seconds INTEGER,
    
    -- Resultados
    status VARCHAR(20) NOT NULL CHECK (status IN ('running', 'completed', 'failed', 'partial')),
    records_processed INTEGER DEFAULT 0,
    records_success INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    
    -- Detalles
    error_details JSONB DEFAULT '{}',
    sync_details JSONB DEFAULT '{}',
    
    -- Metadatos
    triggered_by UUID REFERENCES global.users(id),
    trigger_type VARCHAR(20) DEFAULT 'manual' CHECK (trigger_type IN ('manual', 'scheduled', 'webhook', 'api')),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ÍNDICES PARA PERFORMANCE
CREATE INDEX idx_empresas_tax_id ON country_{COUNTRY_CODE}.empresas(tax_id);
CREATE INDEX idx_empresas_organization ON country_{COUNTRY_CODE}.empresas(organization_id);
CREATE INDEX idx_empresas_estado ON country_{COUNTRY_CODE}.empresas(estado);

CREATE INDEX idx_reportes_empresa_periodo ON country_{COUNTRY_CODE}.reportes_mensuales(empresa_id, anio, mes);
CREATE INDEX idx_reportes_tipo ON country_{COUNTRY_CODE}.reportes_mensuales(tipo_reporte);
CREATE INDEX idx_reportes_estado ON country_{COUNTRY_CODE}.reportes_mensuales(estado);
CREATE INDEX idx_reportes_created ON country_{COUNTRY_CODE}.reportes_mensuales(created_at);

CREATE INDEX idx_archivos_reporte ON country_{COUNTRY_CODE}.archivos_reportes(reporte_id);
CREATE INDEX idx_archivos_empresa ON country_{COUNTRY_CODE}.archivos_reportes(empresa_id);
CREATE INDEX idx_archivos_tipo ON country_{COUNTRY_CODE}.archivos_reportes(tipo_archivo);
CREATE INDEX idx_archivos_activo ON country_{COUNTRY_CODE}.archivos_reportes(activo);

CREATE INDEX idx_sync_logs_type_status ON country_{COUNTRY_CODE}.sync_logs(sync_type, status);
CREATE INDEX idx_sync_logs_created ON country_{COUNTRY_CODE}.sync_logs(created_at);

-- RLS POLICIES
ALTER TABLE country_{COUNTRY_CODE}.empresas ENABLE ROW LEVEL SECURITY;
ALTER TABLE country_{COUNTRY_CODE}.reportes_mensuales ENABLE ROW LEVEL SECURITY;
ALTER TABLE country_{COUNTRY_CODE}.archivos_reportes ENABLE ROW LEVEL SECURITY;
ALTER TABLE country_{COUNTRY_CODE}.info_compania ENABLE ROW LEVEL SECURITY;

-- Política: Los usuarios solo ven empresas de su organización
CREATE POLICY "Usuarios ven empresas de su organización" 
ON country_{COUNTRY_CODE}.empresas FOR ALL 
USING (organization_id IN (
    SELECT organization_id 
    FROM global.user_organizations 
    WHERE user_id = auth.uid()
));

-- Política: Los reportes siguen la visibilidad de las empresas
CREATE POLICY "Usuarios ven reportes de sus empresas"
ON country_{COUNTRY_CODE}.reportes_mensuales FOR ALL
USING (empresa_id IN (
    SELECT id FROM country_{COUNTRY_CODE}.empresas 
    WHERE organization_id IN (
        SELECT organization_id 
        FROM global.user_organizations 
        WHERE user_id = auth.uid()
    )
));

-- TRIGGERS PARA AUDITORÍA
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_empresas_updated_at 
    BEFORE UPDATE ON country_{COUNTRY_CODE}.empresas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reportes_updated_at 
    BEFORE UPDATE ON country_{COUNTRY_CODE}.reportes_mensuales
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_archivos_updated_at 
    BEFORE UPDATE ON country_{COUNTRY_CODE}.archivos_reportes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### **Database Connection Manager**
```python
class MultiCountryDatabaseManager:
    def __init__(self):
        self.connections = {}
        self.global_connection = None
        
    async def initialize(self):
        """Inicializar conexiones a todas las bases regionales"""
        
        # Conexión global
        self.global_connection = create_supabase_client(
            settings.GLOBAL_SUPABASE_URL,
            settings.GLOBAL_SUPABASE_KEY
        )
        
        # Obtener configuración países activos
        countries = await self.global_connection.table('countries')\
            .select('*')\
            .eq('is_active', True)\
            .execute()
        
        # Crear conexiones por país
        for country in countries.data:
            self.connections[country['code']] = create_supabase_client(
                country['database_url'],
                country['service_role_key']
            )
    
    def get_connection(self, country_code: str):
        """Obtener conexión específica por país"""
        if country_code not in self.connections:
            raise ValueError(f"País {country_code} no configurado")
        return self.connections[country_code]
    
    def get_global_connection(self):
        """Obtener conexión global"""
        return self.global_connection
    
    async def execute_multi_country_query(self, query: str, 
                                        params: Dict, 
                                        country_codes: List[str] = None) -> Dict[str, Any]:
        """Ejecutar query en múltiples países"""
        
        if not country_codes:
            country_codes = list(self.connections.keys())
        
        results = {}
        
        for country_code in country_codes:
            try:
                connection = self.get_connection(country_code)
                result = await connection.rpc(query, params).execute()
                results[country_code] = result.data
            except Exception as e:
                results[country_code] = {'error': str(e)}
        
        return results
```

---

Este documento continúa siendo muy extenso. ¿Te gustaría que continúe con las siguientes secciones como:

- 💱 **Sistema Multi-Moneda Completo**
- 🌐 **Internacionalización (i18n) Detallada** 
- 🏛️ **Compliance por País**
- 🔐 **Sistema de Autenticación Global**
- 📊 **Analytics y Reportes**
- 🚀 **Plan de Implementación Detallado**
- 💰 **Presupuesto Completo**

O prefieres que me enfoque en alguna sección específica?