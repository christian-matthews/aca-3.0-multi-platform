-- Script simplificado para configurar reportes por empresa
-- Ejecutar este script en Supabase SQL Editor

-- 1. Crear tabla de reportes mensuales
CREATE TABLE IF NOT EXISTS reportes_mensuales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL CHECK (mes >= 1 AND mes <= 12),
    tipo_reporte VARCHAR(50) NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    url_pdf VARCHAR(500),
    url_excel VARCHAR(500),
    comentarios TEXT,
    estado VARCHAR(20) DEFAULT 'borrador',
    creado_por UUID REFERENCES usuarios(id),
    creado_en TIMESTAMP DEFAULT NOW(),
    actualizado_en TIMESTAMP DEFAULT NOW(),
    UNIQUE(empresa_id, anio, mes, tipo_reporte)
);

-- 2. Crear tabla de archivos de reportes
CREATE TABLE IF NOT EXISTS archivos_reportes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporte_id UUID NOT NULL REFERENCES reportes_mensuales(id) ON DELETE CASCADE,
    nombre_archivo VARCHAR(200) NOT NULL,
    tipo_archivo VARCHAR(50) NOT NULL,
    url_archivo VARCHAR(500) NOT NULL,
    tamanio_bytes BIGINT,
    descripcion TEXT,
    subido_por UUID REFERENCES usuarios(id),
    subido_en TIMESTAMP DEFAULT NOW()
);

-- 3. Crear tabla de comentarios de reportes
CREATE TABLE IF NOT EXISTS comentarios_reportes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporte_id UUID NOT NULL REFERENCES reportes_mensuales(id) ON DELETE CASCADE,
    usuario_id UUID NOT NULL REFERENCES usuarios(id),
    comentario TEXT NOT NULL,
    tipo_comentario VARCHAR(50) DEFAULT 'general',
    creado_en TIMESTAMP DEFAULT NOW()
);

-- 4. Crear tabla de información de compañía
CREATE TABLE IF NOT EXISTS info_compania (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    categoria VARCHAR(50) NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    contenido TEXT,
    url_documento VARCHAR(500),
    estado VARCHAR(20) DEFAULT 'activo',
    creado_por UUID REFERENCES usuarios(id),
    creado_en TIMESTAMP DEFAULT NOW(),
    actualizado_en TIMESTAMP DEFAULT NOW()
);

-- 5. Crear tabla de archivos de información de compañía
CREATE TABLE IF NOT EXISTS archivos_info_compania (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    info_id UUID NOT NULL REFERENCES info_compania(id) ON DELETE CASCADE,
    nombre_archivo VARCHAR(200) NOT NULL,
    tipo_archivo VARCHAR(50) NOT NULL,
    url_archivo VARCHAR(500) NOT NULL,
    tamanio_bytes BIGINT,
    descripcion TEXT,
    subido_por UUID REFERENCES usuarios(id),
    subido_en TIMESTAMP DEFAULT NOW()
);

-- 6. Crear índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_reportes_empresa_anio_mes ON reportes_mensuales(empresa_id, anio, mes);
CREATE INDEX IF NOT EXISTS idx_archivos_reporte ON archivos_reportes(reporte_id);
CREATE INDEX IF NOT EXISTS idx_comentarios_reporte ON comentarios_reportes(reporte_id);
CREATE INDEX IF NOT EXISTS idx_info_compania_empresa_categoria ON info_compania(empresa_id, categoria);
CREATE INDEX IF NOT EXISTS idx_archivos_info ON archivos_info_compania(info_id);

-- 7. Habilitar RLS en todas las tablas
ALTER TABLE reportes_mensuales ENABLE ROW LEVEL SECURITY;
ALTER TABLE archivos_reportes ENABLE ROW LEVEL SECURITY;
ALTER TABLE comentarios_reportes ENABLE ROW LEVEL SECURITY;
ALTER TABLE info_compania ENABLE ROW LEVEL SECURITY;
ALTER TABLE archivos_info_compania ENABLE ROW LEVEL SECURITY;

-- 8. Crear políticas RLS básicas (sin dependencias complejas)
CREATE POLICY "Permitir acceso a reportes de la empresa" ON reportes_mensuales
    FOR ALL USING (true);

CREATE POLICY "Permitir acceso a archivos de reportes" ON archivos_reportes
    FOR ALL USING (true);

CREATE POLICY "Permitir acceso a comentarios de reportes" ON comentarios_reportes
    FOR ALL USING (true);

CREATE POLICY "Permitir acceso a información de compañía" ON info_compania
    FOR ALL USING (true);

CREATE POLICY "Permitir acceso a archivos de información" ON archivos_info_compania
    FOR ALL USING (true);

-- 9. Insertar datos de ejemplo básicos (solo si existe la empresa)
INSERT INTO reportes_mensuales (empresa_id, anio, mes, tipo_reporte, titulo, descripcion, comentarios, estado)
SELECT 
    e.id,
    2024,
    1,
    'balance',
    'Balance General Enero 2024',
    'Balance general al 31 de enero de 2024',
    'Crecimiento de activos del 15% respecto al mes anterior. Mejora en la liquidez.',
    'finalizado'
FROM empresas e
WHERE e.nombre = 'Empresa Ejemplo'
LIMIT 1;

INSERT INTO reportes_mensuales (empresa_id, anio, mes, tipo_reporte, titulo, descripcion, comentarios, estado)
SELECT 
    e.id,
    2024,
    2,
    'resultados',
    'Estado de Resultados Febrero 2024',
    'Estado de resultados del mes de febrero de 2024',
    'Incremento en ventas del 20%. Control de gastos operativos.',
    'finalizado'
FROM empresas e
WHERE e.nombre = 'Empresa Ejemplo'
LIMIT 1;

-- 10. Insertar información de compañía de ejemplo
INSERT INTO info_compania (empresa_id, categoria, titulo, descripcion, contenido, estado)
SELECT 
    e.id,
    'legal',
    'Estatutos de la Empresa',
    'Documentos legales de constitución',
    'Estatutos actualizados de la empresa con todas las modificaciones vigentes.',
    'activo'
FROM empresas e
WHERE e.nombre = 'Empresa Ejemplo'
LIMIT 1;

INSERT INTO info_compania (empresa_id, categoria, titulo, descripcion, contenido, estado)
SELECT 
    e.id,
    'financiera',
    'Estados Financieros 2024',
    'Estados financieros del año 2024',
    'Balance general, estado de resultados y flujo de caja del año 2024.',
    'activo'
FROM empresas e
WHERE e.nombre = 'Empresa Ejemplo'
LIMIT 1;

INSERT INTO info_compania (empresa_id, categoria, titulo, descripcion, contenido, estado)
SELECT 
    e.id,
    'tributaria',
    'Declaraciones de Impuestos 2024',
    'Declaraciones de impuestos del año 2024',
    'Todas las declaraciones de impuestos presentadas en 2024.',
    'activo'
FROM empresas e
WHERE e.nombre = 'Empresa Ejemplo'
LIMIT 1;

INSERT INTO info_compania (empresa_id, categoria, titulo, descripcion, contenido, estado)
SELECT 
    e.id,
    'carpeta',
    'Carpeta Tributaria Completa',
    'Documentos de respaldo tributario',
    'Documentos de constitución, registros contables y comprobantes de pago.',
    'activo'
FROM empresas e
WHERE e.nombre = 'Empresa Ejemplo'
LIMIT 1; 