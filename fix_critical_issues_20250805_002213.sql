-- 🔧 Script de Corrección de Problemas Críticos - ACA 3.0
-- Generado: 2025-08-05T00:22:13.370523
-- 
-- INSTRUCCIONES:
-- 1. Abrir Supabase Dashboard
-- 2. Ir a SQL Editor
-- 3. Ejecutar este script completo
-- 4. Verificar que todas las operaciones fueron exitosas

-- =====================================================================
-- CORRECCIONES DE PROBLEMAS CRÍTICOS
-- =====================================================================

-- ===== CREACIÓN DE TABLAS FALTANTES =====

-- Crear tabla: meses_reportes
CREATE TABLE meses_reportes (
                id SERIAL PRIMARY KEY, mes INTEGER NOT NULL, nombre VARCHAR(20) NOT NULL, activo BOOLEAN DEFAULT true, created_at TIMESTAMP DEFAULT NOW(), updated_at TIMESTAMP DEFAULT NOW()
            );

-- ===== ADICIÓN DE COLUMNAS FALTANTES =====

-- Corregir tabla: citas
-- Agregar columna: id
ALTER TABLE citas ADD COLUMN id SERIAL PRIMARY KEY;
-- Agregar columna: empresa_id
ALTER TABLE citas ADD COLUMN empresa_id UUID REFERENCES empresas(id);
-- Agregar columna: created_at
ALTER TABLE citas ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
-- Agregar columna: activo
ALTER TABLE citas ADD COLUMN activo BOOLEAN DEFAULT true;

-- Corregir tabla: security_logs
-- Agregar columna: id
ALTER TABLE security_logs ADD COLUMN id SERIAL PRIMARY KEY;
-- Agregar columna: created_at
ALTER TABLE security_logs ADD COLUMN created_at TIMESTAMP DEFAULT NOW();

-- Corregir tabla: archivos_reportes
-- Agregar columna: id
ALTER TABLE archivos_reportes ADD COLUMN id SERIAL PRIMARY KEY;
-- Agregar columna: empresa_id
ALTER TABLE archivos_reportes ADD COLUMN empresa_id UUID REFERENCES empresas(id);
-- Agregar columna: created_at
ALTER TABLE archivos_reportes ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
-- Agregar columna: activo
ALTER TABLE archivos_reportes ADD COLUMN activo BOOLEAN DEFAULT true;

-- ===== VERIFICACIONES FINALES =====

-- Verificar que las tablas existen
SELECT table_name, table_type 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Verificar estructura de tablas críticas
SELECT table_name, column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_schema = 'public' 
  AND table_name IN ('citas', 'security_logs', 'archivos_reportes', 'meses_reportes')
ORDER BY table_name, ordinal_position;

-- ===== FINALIZADO =====
-- Ejecutar check_database.py para verificar que todos los problemas fueron corregidos
