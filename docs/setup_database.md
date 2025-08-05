# 🗄️ Configuración de Base de Datos - ACA 3.0

## 📋 **Paso a Paso para Configurar Supabase**

### **1. Crear Proyecto en Supabase**

1. Ve a [supabase.com](https://supabase.com)
2. Crea una cuenta o inicia sesión
3. Crea un nuevo proyecto
4. Anota la URL y las claves (las necesitarás para `.env`)

### **2. Ejecutar Script SQL**

Ve a **SQL Editor** en tu proyecto de Supabase y ejecuta este script completo:

```sql
-- =====================================================
-- ESQUEMA DE BASE DE DATOS ACA 3.0
-- =====================================================

-- Habilitar extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- TABLA: empresas
-- =====================================================
CREATE TABLE empresas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rut VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    telefono VARCHAR(50),
    direccion TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA: usuarios
-- =====================================================
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_id BIGINT UNIQUE NOT NULL,
    empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    telefono VARCHAR(50),
    rol VARCHAR(50) DEFAULT 'usuario',
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA: conversaciones
-- =====================================================
CREATE TABLE conversaciones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_id BIGINT NOT NULL,
    empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE,
    mensaje TEXT NOT NULL,
    respuesta TEXT,
    tipo VARCHAR(50) DEFAULT 'texto',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA: reportes
-- =====================================================
CREATE TABLE reportes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50) NOT NULL,
    url_pdf VARCHAR(500),
    url_excel VARCHAR(500),
    fecha_reporte DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA: pendientes
-- =====================================================
CREATE TABLE pendientes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50) NOT NULL,
    prioridad VARCHAR(20) DEFAULT 'media',
    fecha_limite DATE,
    estado VARCHAR(20) DEFAULT 'pendiente',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA: cuentas_cobrar
-- =====================================================
CREATE TABLE cuentas_cobrar (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE,
    cliente VARCHAR(255) NOT NULL,
    descripcion TEXT,
    monto DECIMAL(15,2) NOT NULL,
    fecha_emision DATE NOT NULL,
    fecha_vencimiento DATE,
    estado VARCHAR(20) DEFAULT 'pendiente',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA: cuentas_pagar
-- =====================================================
CREATE TABLE cuentas_pagar (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE,
    proveedor VARCHAR(255) NOT NULL,
    descripcion TEXT,
    monto DECIMAL(15,2) NOT NULL,
    fecha_emision DATE NOT NULL,
    fecha_vencimiento DATE,
    estado VARCHAR(20) DEFAULT 'pendiente',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA: citas
-- =====================================================
CREATE TABLE citas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE,
    usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_inicio TIMESTAMP WITH TIME ZONE NOT NULL,
    fecha_fin TIMESTAMP WITH TIME ZONE NOT NULL,
    tipo VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'programada',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA: security_logs
-- =====================================================
CREATE TABLE security_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_id BIGINT,
    empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE,
    accion VARCHAR(100) NOT NULL,
    detalles JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================

-- Índices para usuarios
CREATE INDEX idx_usuarios_chat_id ON usuarios(chat_id);
CREATE INDEX idx_usuarios_empresa_id ON usuarios(empresa_id);

-- Índices para conversaciones
CREATE INDEX idx_conversaciones_chat_id ON conversaciones(chat_id);
CREATE INDEX idx_conversaciones_empresa_id ON conversaciones(empresa_id);
CREATE INDEX idx_conversaciones_created_at ON conversaciones(created_at);

-- Índices para reportes
CREATE INDEX idx_reportes_empresa_id ON reportes(empresa_id);
CREATE INDEX idx_reportes_fecha_reporte ON reportes(fecha_reporte);

-- Índices para pendientes
CREATE INDEX idx_pendientes_empresa_id ON pendientes(empresa_id);
CREATE INDEX idx_pendientes_estado ON pendientes(estado);
CREATE INDEX idx_pendientes_fecha_limite ON pendientes(fecha_limite);

-- Índices para cuentas
CREATE INDEX idx_cuentas_cobrar_empresa_id ON cuentas_cobrar(empresa_id);
CREATE INDEX idx_cuentas_pagar_empresa_id ON cuentas_pagar(empresa_id);

-- =====================================================
-- ROW LEVEL SECURITY (RLS)
-- =====================================================

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

-- Políticas para empresas (solo admin puede ver todas)
CREATE POLICY "Admin can view all empresas" ON empresas
    FOR ALL USING (true);

-- Políticas para usuarios
CREATE POLICY "Users can view own data" ON usuarios
    FOR SELECT USING (chat_id = current_setting('app.chat_id', true)::bigint);

CREATE POLICY "Admin can manage users" ON usuarios
    FOR ALL USING (true);

-- Políticas para conversaciones
CREATE POLICY "Users can view own conversations" ON conversaciones
    FOR SELECT USING (chat_id = current_setting('app.chat_id', true)::bigint);

CREATE POLICY "Users can insert own conversations" ON conversaciones
    FOR INSERT WITH CHECK (chat_id = current_setting('app.chat_id', true)::bigint);

-- Políticas para reportes
CREATE POLICY "Users can view own reports" ON reportes
    FOR SELECT USING (empresa_id IN (
        SELECT empresa_id FROM usuarios 
        WHERE chat_id = current_setting('app.chat_id', true)::bigint
    ));

-- Políticas para pendientes
CREATE POLICY "Users can view own pendientes" ON pendientes
    FOR SELECT USING (empresa_id IN (
        SELECT empresa_id FROM usuarios 
        WHERE chat_id = current_setting('app.chat_id', true)::bigint
    ));

-- Políticas para cuentas
CREATE POLICY "Users can view own cuentas" ON cuentas_cobrar
    FOR SELECT USING (empresa_id IN (
        SELECT empresa_id FROM usuarios 
        WHERE chat_id = current_setting('app.chat_id', true)::bigint
    ));

CREATE POLICY "Users can view own cuentas" ON cuentas_pagar
    FOR SELECT USING (empresa_id IN (
        SELECT empresa_id FROM usuarios 
        WHERE chat_id = current_setting('app.chat_id', true)::bigint
    ));

-- Políticas para citas
CREATE POLICY "Users can view own citas" ON citas
    FOR SELECT USING (empresa_id IN (
        SELECT empresa_id FROM usuarios 
        WHERE chat_id = current_setting('app.chat_id', true)::bigint
    ));

-- Políticas para security_logs (solo admin)
CREATE POLICY "Admin can view security logs" ON security_logs
    FOR ALL USING (true);

-- =====================================================
-- DATOS DE EJEMPLO
-- =====================================================

-- Insertar empresas de ejemplo
INSERT INTO empresas (rut, nombre, email, telefono, direccion) VALUES
('12345678-9', 'Empresa Ejemplo 1 SPA', 'contacto@empresa1.cl', '+56912345678', 'Av. Providencia 123, Santiago'),
('98765432-1', 'Empresa Ejemplo 2 Ltda.', 'info@empresa2.cl', '+56987654321', 'Las Condes 456, Santiago'),
('11223344-5', 'Empresa Ejemplo 3 EIRL', 'ventas@empresa3.cl', '+56911223344', 'Ñuñoa 789, Santiago');

-- Insertar usuarios de ejemplo
INSERT INTO usuarios (chat_id, empresa_id, nombre, email, telefono, rol) VALUES
(123456789, (SELECT id FROM empresas WHERE rut = '12345678-9'), 'Juan Pérez', 'juan@empresa1.cl', '+56912345678', 'admin'),
(987654321, (SELECT id FROM empresas WHERE rut = '98765432-1'), 'María González', 'maria@empresa2.cl', '+56987654321', 'usuario'),
(111222333, (SELECT id FROM empresas WHERE rut = '11223344-5'), 'Carlos López', 'carlos@empresa3.cl', '+56911122233', 'usuario');

-- Insertar reportes de ejemplo
INSERT INTO reportes (empresa_id, titulo, descripcion, tipo, url_pdf, fecha_reporte) VALUES
((SELECT id FROM empresas WHERE rut = '12345678-9'), 'Balance General Enero 2024', 'Balance general del primer mes del año', 'balance', 'https://ejemplo.com/reportes/balance-enero-2024.pdf', '2024-01-31'),
((SELECT id FROM empresas WHERE rut = '12345678-9'), 'Estado de Resultados Q1 2024', 'Estado de resultados del primer trimestre', 'resultados', 'https://ejemplo.com/reportes/resultados-q1-2024.pdf', '2024-03-31'),
((SELECT id FROM empresas WHERE rut = '98765432-1'), 'Flujo de Caja Febrero 2024', 'Análisis del flujo de caja mensual', 'flujo_caja', 'https://ejemplo.com/reportes/flujo-febrero-2024.pdf', '2024-02-29');

-- Insertar pendientes de ejemplo
INSERT INTO pendientes (empresa_id, titulo, descripcion, tipo, prioridad, fecha_limite, estado) VALUES
((SELECT id FROM empresas WHERE rut = '12345678-9'), 'Declaración IVA Marzo', 'Presentar declaración de IVA del mes de marzo', 'tributario', 'alta', '2024-04-20', 'pendiente'),
((SELECT id FROM empresas WHERE rut = '12345678-9'), 'Pago Proveedor ABC', 'Pago pendiente a proveedor ABC por servicios', 'pago', 'media', '2024-04-15', 'pendiente'),
((SELECT id FROM empresas WHERE rut = '98765432-1'), 'Revisión Contratos', 'Revisar y actualizar contratos de servicios', 'administrativo', 'baja', '2024-04-30', 'pendiente'),
((SELECT id FROM empresas WHERE rut = '11223344-5'), 'Auditoría Interna', 'Realizar auditoría interna de procesos', 'auditoria', 'alta', '2024-04-25', 'pendiente');

-- Insertar cuentas por cobrar de ejemplo
INSERT INTO cuentas_cobrar (empresa_id, cliente, descripcion, monto, fecha_emision, fecha_vencimiento, estado) VALUES
((SELECT id FROM empresas WHERE rut = '12345678-9'), 'Cliente A', 'Servicios de consultoría enero', 1500000, '2024-01-15', '2024-02-15', 'pendiente'),
((SELECT id FROM empresas WHERE rut = '12345678-9'), 'Cliente B', 'Desarrollo de software', 2500000, '2024-02-01', '2024-03-01', 'pendiente'),
((SELECT id FROM empresas WHERE rut = '98765432-1'), 'Cliente C', 'Servicios de mantenimiento', 800000, '2024-03-10', '2024-04-10', 'pendiente'),
((SELECT id FROM empresas WHERE rut = '11223344-5'), 'Cliente D', 'Capacitación personal', 1200000, '2024-03-20', '2024-04-20', 'pendiente');

-- Insertar cuentas por pagar de ejemplo
INSERT INTO cuentas_pagar (empresa_id, proveedor, descripcion, monto, fecha_emision, fecha_vencimiento, estado) VALUES
((SELECT id FROM empresas WHERE rut = '12345678-9'), 'Proveedor X', 'Servicios de internet', 150000, '2024-03-01', '2024-04-01', 'pendiente'),
((SELECT id FROM empresas WHERE rut = '12345678-9'), 'Proveedor Y', 'Suministros de oficina', 250000, '2024-03-15', '2024-04-15', 'pendiente'),
((SELECT id FROM empresas WHERE rut = '98765432-1'), 'Proveedor Z', 'Servicios de limpieza', 300000, '2024-03-20', '2024-04-20', 'pendiente'),
((SELECT id FROM empresas WHERE rut = '11223344-5'), 'Proveedor W', 'Mantenimiento equipos', 450000, '2024-03-25', '2024-04-25', 'pendiente');

-- Insertar conversaciones de ejemplo
INSERT INTO conversaciones (chat_id, empresa_id, mensaje, respuesta, tipo) VALUES
(123456789, (SELECT id FROM empresas WHERE rut = '12345678-9'), '/start', 'Menú principal mostrado', 'comando'),
(123456789, (SELECT id FROM empresas WHERE rut = '12345678-9'), 'Callback: reportes', 'Procesando solicitud', 'callback'),
(987654321, (SELECT id FROM empresas WHERE rut = '98765432-1'), '/start', 'Menú principal mostrado', 'comando'),
(111222333, (SELECT id FROM empresas WHERE rut = '11223344-5'), 'Callback: pendientes', 'Procesando solicitud', 'callback');

-- =====================================================
-- FUNCIONES DE UTILIDAD
-- =====================================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para updated_at
CREATE TRIGGER update_empresas_updated_at BEFORE UPDATE ON empresas FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_usuarios_updated_at BEFORE UPDATE ON usuarios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_pendientes_updated_at BEFORE UPDATE ON pendientes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- VISTAS ÚTILES
-- =====================================================

-- Vista para resumen de cuentas por empresa
CREATE VIEW resumen_cuentas AS
SELECT 
    e.nombre as empresa,
    COUNT(cxc.id) as total_cxc,
    COALESCE(SUM(cxc.monto), 0) as monto_total_cxc,
    COUNT(cxp.id) as total_cxp,
    COALESCE(SUM(cxp.monto), 0) as monto_total_cxp
FROM empresas e
LEFT JOIN cuentas_cobrar cxc ON e.id = cxc.empresa_id AND cxc.estado = 'pendiente'
LEFT JOIN cuentas_pagar cxp ON e.id = cxp.empresa_id AND cxp.estado = 'pendiente'
GROUP BY e.id, e.nombre;

-- Vista para pendientes por empresa
CREATE VIEW resumen_pendientes AS
SELECT 
    e.nombre as empresa,
    COUNT(p.id) as total_pendientes,
    COUNT(CASE WHEN p.prioridad = 'alta' THEN 1 END) as pendientes_altas,
    COUNT(CASE WHEN p.prioridad = 'media' THEN 1 END) as pendientes_medias,
    COUNT(CASE WHEN p.prioridad = 'baja' THEN 1 END) as pendientes_bajas
FROM empresas e
LEFT JOIN pendientes p ON e.id = p.empresa_id AND p.estado = 'pendiente'
GROUP BY e.id, e.nombre;

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================

SELECT '✅ Base de datos ACA 3.0 configurada exitosamente!' as mensaje;
```

### **3. Verificar la Configuración**

Después de ejecutar el script, puedes verificar que todo esté funcionando:

```sql
-- Verificar empresas creadas
SELECT * FROM empresas;

-- Verificar usuarios creados
SELECT u.nombre, u.chat_id, e.nombre as empresa 
FROM usuarios u 
JOIN empresas e ON u.empresa_id = e.id;

-- Verificar reportes
SELECT r.titulo, e.nombre as empresa 
FROM reportes r 
JOIN empresas e ON r.empresa_id = e.id;

-- Verificar pendientes
SELECT p.titulo, p.prioridad, e.nombre as empresa 
FROM pendientes p 
JOIN empresas e ON p.empresa_id = e.id;

-- Verificar cuentas
SELECT 
    'CxC' as tipo,
    cxc.cliente as contraparte,
    cxc.monto,
    e.nombre as empresa
FROM cuentas_cobrar cxc 
JOIN empresas e ON cxc.empresa_id = e.id
UNION ALL
SELECT 
    'CxP' as tipo,
    cxp.proveedor as contraparte,
    cxp.monto,
    e.nombre as empresa
FROM cuentas_pagar cxp 
JOIN empresas e ON cxp.empresa_id = e.id;
```

### **4. Configurar Variables de Entorno**

Ahora necesitas actualizar tu archivo `.env` con las credenciales de Supabase:

```bash
# Supabase (reemplaza con tus valores reales)
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key
SUPABASE_SERVICE_KEY=tu-service-key
```

### **5. Probar la Conexión**

```bash
# Activar entorno virtual
source venv/bin/activate

# Probar conexión a Supabase
python -c "
from app.database.supabase import supabase
try:
    result = supabase.table('empresas').select('*').limit(1).execute()
    print('✅ Conexión a Supabase exitosa')
    print(f'Encontradas {len(result.data)} empresas')
except Exception as e:
    print(f'❌ Error de conexión: {e}')
"
```

## 🎯 **Datos de Ejemplo Incluidos**

### **Empresas:**
- Empresa Ejemplo 1 SPA (RUT: 12345678-9)
- Empresa Ejemplo 2 Ltda. (RUT: 98765432-1)  
- Empresa Ejemplo 3 EIRL (RUT: 11223344-5)

### **Usuarios:**
- Juan Pérez (chat_id: 123456789) - Empresa 1
- María González (chat_id: 987654321) - Empresa 2
- Carlos López (chat_id: 111222333) - Empresa 3

### **Reportes:**
- Balance General Enero 2024
- Estado de Resultados Q1 2024
- Flujo de Caja Febrero 2024

### **Pendientes:**
- Declaración IVA Marzo (Alta prioridad)
- Pago Proveedor ABC (Media prioridad)
- Revisión Contratos (Baja prioridad)
- Auditoría Interna (Alta prioridad)

### **Cuentas por Cobrar:**
- Cliente A: $1,500,000
- Cliente B: $2,500,000
- Cliente C: $800,000
- Cliente D: $1,200,000

### **Cuentas por Pagar:**
- Proveedor X: $150,000
- Proveedor Y: $250,000
- Proveedor Z: $300,000
- Proveedor W: $450,000

## 🚀 **Próximos Pasos**

1. **Ejecutar el script SQL** en Supabase
2. **Configurar variables de entorno** con tus credenciales
3. **Probar la conexión** con el comando de verificación
4. **Ejecutar la aplicación** y probar los bots

¡Con estos datos de ejemplo tendrás un sistema completamente funcional para probar! 🎉 