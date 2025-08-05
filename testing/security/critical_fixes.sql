-- 🔧 CORRECCIONES CRÍTICAS PARA ACA 3.0
-- Ejecutar en Supabase SQL Editor
-- 
-- PROBLEMAS IDENTIFICADOS:
-- 1. Tablas sin clave primaria (id)
-- 2. Tablas sin empresa_id para aislamiento
-- 3. Tabla meses_reportes faltante
-- 4. Columnas de timestamp faltantes

-- =====================================================================
-- 1. CREAR TABLA FALTANTE: meses_reportes
-- =====================================================================

-- Verificar si la tabla existe
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'meses_reportes') THEN
        CREATE TABLE meses_reportes (
            id SERIAL PRIMARY KEY,
            mes INTEGER NOT NULL UNIQUE,
            nombre VARCHAR(20) NOT NULL,
            activo BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        
        -- Insertar datos de los meses
        INSERT INTO meses_reportes (mes, nombre) VALUES
            (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
            (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
            (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre');
        
        RAISE NOTICE 'Tabla meses_reportes creada con 12 registros';
    ELSE
        RAISE NOTICE 'Tabla meses_reportes ya existe';
    END IF;
END $$;

-- =====================================================================
-- 2. CORREGIR TABLA: citas
-- =====================================================================

-- Verificar estructura actual de citas
DO $$
BEGIN
    -- Agregar columna id si no existe
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'citas' AND column_name = 'id') THEN
        ALTER TABLE citas ADD COLUMN id SERIAL PRIMARY KEY;
        RAISE NOTICE 'Agregada columna id a tabla citas';
    END IF;
    
    -- Agregar empresa_id si no existe
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'citas' AND column_name = 'empresa_id') THEN
        ALTER TABLE citas ADD COLUMN empresa_id UUID REFERENCES empresas(id);
        RAISE NOTICE 'Agregada columna empresa_id a tabla citas';
    END IF;
    
    -- Agregar created_at si no existe
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'citas' AND column_name = 'created_at') THEN
        ALTER TABLE citas ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
        RAISE NOTICE 'Agregada columna created_at a tabla citas';
    END IF;
    
    -- Agregar updated_at si no existe
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'citas' AND column_name = 'updated_at') THEN
        ALTER TABLE citas ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
        RAISE NOTICE 'Agregada columna updated_at a tabla citas';
    END IF;
    
    -- Agregar activo si no existe
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'citas' AND column_name = 'activo') THEN
        ALTER TABLE citas ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE 'Agregada columna activo a tabla citas';
    END IF;
END $$;

-- =====================================================================
-- 3. CORREGIR TABLA: security_logs
-- =====================================================================

DO $$
BEGIN
    -- Agregar columna id si no existe
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'security_logs' AND column_name = 'id') THEN
        ALTER TABLE security_logs ADD COLUMN id SERIAL PRIMARY KEY;
        RAISE NOTICE 'Agregada columna id a tabla security_logs';
    END IF;
    
    -- NOTE: security_logs NO necesita empresa_id porque es global
END $$;

-- =====================================================================
-- 4. CORREGIR TABLA: archivos_reportes
-- =====================================================================

DO $$
BEGIN
    -- Agregar columna id si no existe
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'archivos_reportes' AND column_name = 'id') THEN
        ALTER TABLE archivos_reportes ADD COLUMN id SERIAL PRIMARY KEY;
        RAISE NOTICE 'Agregada columna id a tabla archivos_reportes';
    END IF;
    
    -- Agregar empresa_id si no existe
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'archivos_reportes' AND column_name = 'empresa_id') THEN
        ALTER TABLE archivos_reportes ADD COLUMN empresa_id UUID REFERENCES empresas(id);
        RAISE NOTICE 'Agregada columna empresa_id a tabla archivos_reportes';
    END IF;
    
    -- Agregar created_at si no existe
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'archivos_reportes' AND column_name = 'created_at') THEN
        ALTER TABLE archivos_reportes ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
        RAISE NOTICE 'Agregada columna created_at a tabla archivos_reportes';
    END IF;
    
    -- Agregar updated_at si no existe
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'archivos_reportes' AND column_name = 'updated_at') THEN
        ALTER TABLE archivos_reportes ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
        RAISE NOTICE 'Agregada columna updated_at a tabla archivos_reportes';
    END IF;
    
    -- Agregar activo si no existe
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'archivos_reportes' AND column_name = 'activo') THEN
        ALTER TABLE archivos_reportes ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE 'Agregada columna activo a tabla archivos_reportes';
    END IF;
END $$;

-- =====================================================================
-- 5. MEJORAR OTRAS TABLAS (Opcional - Problemas Medios)
-- =====================================================================

-- Agregar columna activo a reportes si no existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'reportes' AND column_name = 'activo') THEN
        ALTER TABLE reportes ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE 'Agregada columna activo a tabla reportes';
    END IF;
END $$;

-- Agregar columna activo a pendientes si no existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'pendientes' AND column_name = 'activo') THEN
        ALTER TABLE pendientes ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE 'Agregada columna activo a tabla pendientes';
    END IF;
END $$;

-- Agregar columna activo a cuentas_cobrar si no existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'cuentas_cobrar' AND column_name = 'activo') THEN
        ALTER TABLE cuentas_cobrar ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE 'Agregada columna activo a tabla cuentas_cobrar';
    END IF;
END $$;

-- Agregar columna activo a cuentas_pagar si no existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = 'cuentas_pagar' AND column_name = 'activo') THEN
        ALTER TABLE cuentas_pagar ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE 'Agregada columna activo a tabla cuentas_pagar';
    END IF;
END $$;

-- =====================================================================
-- 6. CREAR TRIGGERS PARA updated_at (Recomendado)
-- =====================================================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar trigger a tablas que tienen updated_at
DO $$
DECLARE
    t TEXT;
    tables_with_updated_at TEXT[] := ARRAY['empresas', 'usuarios', 'citas', 'archivos_reportes', 'meses_reportes'];
BEGIN
    FOREACH t IN ARRAY tables_with_updated_at
    LOOP
        -- Verificar si la tabla y columna existen
        IF EXISTS (SELECT FROM information_schema.columns 
                   WHERE table_name = t AND column_name = 'updated_at') THEN
            
            -- Eliminar trigger si existe
            EXECUTE format('DROP TRIGGER IF EXISTS update_%I_updated_at ON %I', t, t);
            
            -- Crear nuevo trigger
            EXECUTE format('CREATE TRIGGER update_%I_updated_at 
                           BEFORE UPDATE ON %I 
                           FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()', t, t);
            
            RAISE NOTICE 'Trigger created for table: %', t;
        END IF;
    END LOOP;
END $$;

-- =====================================================================
-- 7. VERIFICACIONES FINALES
-- =====================================================================

-- Mostrar estructura actualizada de tablas críticas
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_schema = 'public' 
  AND table_name IN ('citas', 'security_logs', 'archivos_reportes', 'meses_reportes')
ORDER BY table_name, ordinal_position;

-- Contar registros en todas las tablas
SELECT 
    schemaname,
    tablename,
    n_tup_ins as total_rows
FROM pg_stat_user_tables 
WHERE schemaname = 'public'
ORDER BY tablename;

-- =====================================================================
-- FINALIZADO
-- =====================================================================

SELECT 'Correcciones críticas aplicadas exitosamente' as status;

-- Ejecutar después: python check_database.py para verificar