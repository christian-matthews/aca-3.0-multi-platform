# Esquema de Base de Datos - ACA 3.0

## Tablas Principales

### 1. **empresas**
Tabla principal para almacenar información de las empresas registradas.

```sql
CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    rut VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Campos:**
- `id`: Identificador único autoincremental
- `rut`: RUT de la empresa (único)
- `nombre`: Nombre de la empresa
- `activo`: Estado de la empresa (true/false)
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última actualización

### 2. **usuarios**
Tabla para almacenar usuarios registrados por empresa.

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL,
    empresa_id INTEGER REFERENCES empresas(id),
    nombre VARCHAR(255) NOT NULL,
    rol VARCHAR(50) DEFAULT 'user',
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Campos:**
- `id`: Identificador único autoincremental
- `chat_id`: ID del chat de Telegram (único)
- `empresa_id`: Referencia a la empresa
- `nombre`: Nombre del usuario
- `rol`: Rol del usuario (admin, user)
- `activo`: Estado del usuario
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última actualización

### 3. **conversaciones**
Tabla para registrar todas las conversaciones del sistema.

```sql
CREATE TABLE conversaciones (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    empresa_id INTEGER REFERENCES empresas(id),
    mensaje TEXT NOT NULL,
    respuesta TEXT,
    tipo VARCHAR(50) DEFAULT 'user',
    timestamp TIMESTAMP DEFAULT NOW()
);
```

**Campos:**
- `id`: Identificador único autoincremental
- `chat_id`: ID del chat de Telegram
- `empresa_id`: Referencia a la empresa
- `mensaje`: Mensaje del usuario
- `respuesta`: Respuesta del sistema
- `tipo`: Tipo de conversación (user, system, error)
- `timestamp`: Fecha y hora de la conversación

### 4. **reportes**
Tabla para almacenar reportes disponibles por empresa.

```sql
CREATE TABLE reportes (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES empresas(id),
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    url_pdf VARCHAR(500),
    tipo VARCHAR(50) DEFAULT 'general',
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Campos:**
- `id`: Identificador único autoincremental
- `empresa_id`: Referencia a la empresa
- `titulo`: Título del reporte
- `descripcion`: Descripción del reporte
- `url_pdf`: URL del archivo PDF
- `tipo`: Tipo de reporte (general, financiero, contable)
- `activo`: Estado del reporte
- `created_at`: Fecha de creación

### 5. **pendientes**
Tabla para almacenar tareas pendientes por empresa.

```sql
CREATE TABLE pendientes (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES empresas(id),
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50) DEFAULT 'general',
    fecha_limite DATE,
    prioridad VARCHAR(20) DEFAULT 'media',
    estado VARCHAR(20) DEFAULT 'pendiente',
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Campos:**
- `id`: Identificador único autoincremental
- `empresa_id`: Referencia a la empresa
- `titulo`: Título de la tarea
- `descripcion`: Descripción de la tarea
- `tipo`: Tipo de pendiente (contabilizacion, pago, cobro)
- `fecha_limite`: Fecha límite de la tarea
- `prioridad`: Prioridad (baja, media, alta)
- `estado`: Estado (pendiente, en_proceso, completado)
- `activo`: Estado del registro
- `created_at`: Fecha de creación

### 6. **cuentas_cobrar**
Tabla para almacenar cuentas por cobrar.

```sql
CREATE TABLE cuentas_cobrar (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES empresas(id),
    cliente VARCHAR(255) NOT NULL,
    monto DECIMAL(15,2) NOT NULL,
    fecha_emision DATE,
    fecha_vencimiento DATE,
    estado VARCHAR(20) DEFAULT 'pendiente',
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Campos:**
- `id`: Identificador único autoincremental
- `empresa_id`: Referencia a la empresa
- `cliente`: Nombre del cliente
- `monto`: Monto a cobrar
- `fecha_emision`: Fecha de emisión
- `fecha_vencimiento`: Fecha de vencimiento
- `estado`: Estado (pendiente, cobrado, vencido)
- `descripcion`: Descripción adicional
- `activo`: Estado del registro
- `created_at`: Fecha de creación

### 7. **cuentas_pagar**
Tabla para almacenar cuentas por pagar.

```sql
CREATE TABLE cuentas_pagar (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES empresas(id),
    proveedor VARCHAR(255) NOT NULL,
    monto DECIMAL(15,2) NOT NULL,
    fecha_emision DATE,
    fecha_vencimiento DATE,
    estado VARCHAR(20) DEFAULT 'pendiente',
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Campos:**
- `id`: Identificador único autoincremental
- `empresa_id`: Referencia a la empresa
- `proveedor`: Nombre del proveedor
- `monto`: Monto a pagar
- `fecha_emision`: Fecha de emisión
- `fecha_vencimiento`: Fecha de vencimiento
- `estado`: Estado (pendiente, pagado, vencido)
- `descripcion`: Descripción adicional
- `activo`: Estado del registro
- `created_at`: Fecha de creación

### 8. **citas**
Tabla para el sistema de agendamiento.

```sql
CREATE TABLE citas (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES empresas(id),
    usuario_id INTEGER REFERENCES usuarios(id),
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_inicio TIMESTAMP NOT NULL,
    fecha_fin TIMESTAMP NOT NULL,
    tipo VARCHAR(50) DEFAULT 'reunion',
    estado VARCHAR(20) DEFAULT 'programada',
    google_calendar_id VARCHAR(255),
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Campos:**
- `id`: Identificador único autoincremental
- `empresa_id`: Referencia a la empresa
- `usuario_id`: Referencia al usuario
- `titulo`: Título de la cita
- `descripcion`: Descripción de la cita
- `fecha_inicio`: Fecha y hora de inicio
- `fecha_fin`: Fecha y hora de fin
- `tipo`: Tipo de cita (reunion, llamada, evento)
- `estado`: Estado (programada, confirmada, cancelada)
- `google_calendar_id`: ID del evento en Google Calendar
- `activo`: Estado del registro
- `created_at`: Fecha de creación

### 9. **security_logs**
Tabla para registrar eventos de seguridad.

```sql
CREATE TABLE security_logs (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    details TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

**Campos:**
- `id`: Identificador único autoincremental
- `chat_id`: ID del chat de Telegram
- `event_type`: Tipo de evento de seguridad
- `details`: Detalles del evento
- `timestamp`: Fecha y hora del evento

## Índices Recomendados

```sql
-- Índices para optimizar consultas
CREATE INDEX idx_usuarios_chat_id ON usuarios(chat_id);
CREATE INDEX idx_usuarios_empresa_id ON usuarios(empresa_id);
CREATE INDEX idx_conversaciones_chat_id ON conversaciones(chat_id);
CREATE INDEX idx_conversaciones_empresa_id ON conversaciones(empresa_id);
CREATE INDEX idx_conversaciones_timestamp ON conversaciones(timestamp);
CREATE INDEX idx_empresas_rut ON empresas(rut);
CREATE INDEX idx_pendientes_empresa_id ON pendientes(empresa_id);
CREATE INDEX idx_pendientes_fecha_limite ON pendientes(fecha_limite);
CREATE INDEX idx_cxc_empresa_id ON cuentas_cobrar(empresa_id);
CREATE INDEX idx_cxp_empresa_id ON cuentas_pagar(empresa_id);
CREATE INDEX idx_citas_empresa_id ON citas(empresa_id);
CREATE INDEX idx_citas_fecha_inicio ON citas(fecha_inicio);
```

## Políticas de Seguridad (RLS)

```sql
-- Habilitar RLS en todas las tablas
ALTER TABLE empresas ENABLE ROW LEVEL SECURITY;
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE reportes ENABLE ROW LEVEL SECURITY;
ALTER TABLE pendientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE cuentas_cobrar ENABLE ROW LEVEL SECURITY;
ALTER TABLE cuentas_pagar ENABLE ROW LEVEL SECURITY;
ALTER TABLE citas ENABLE ROW LEVEL SECURITY;
ALTER TABLE security_logs ENABLE ROW LEVEL SECURITY;
```

## Triggers para Auditoría

```sql
-- Trigger para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar trigger a tablas relevantes
CREATE TRIGGER update_empresas_updated_at BEFORE UPDATE ON empresas FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_usuarios_updated_at BEFORE UPDATE ON usuarios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
``` 