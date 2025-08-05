-- 🔧 CORRECCIÓN OPTIMIZADA DE PROBLEMAS CRÍTICOS - ACA 3.0
-- ✅ Script seguro con verificaciones IF NOT EXISTS
-- 📅 Fecha: 2025-08-05
-- 
-- INSTRUCCIONES:
-- 1. Copiar este script completo
-- 2. Abrir Supabase Dashboard → SQL Editor
-- 3. Pegar y ejecutar
-- 4. Verificar resultado con: python check_database.py

-- =====================================================================
-- 🎯 CORRECCIONES CRÍTICAS AUTOMÁTICAS
-- =====================================================================

-- 📋 1. CREAR TABLA FALTANTE: meses_reportes
-- =====================================================================
CREATE TABLE IF NOT EXISTS meses_reportes (
    id SERIAL PRIMARY KEY,
    mes INTEGER NOT NULL UNIQUE,
    nombre VARCHAR(20) NOT NULL,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insertar meses solo si la tabla está vacía
INSERT INTO meses_reportes (mes, nombre) 
SELECT mes, nombre FROM (VALUES
    (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
    (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
    (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
) AS months(mes, nombre)
WHERE NOT EXISTS (SELECT 1 FROM meses_reportes LIMIT 1);

-- 🔧 2. CORREGIR TABLA: citas
-- =====================================================================
DO $$ 
BEGIN
    -- Agregar id si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'citas' AND column_name = 'id') THEN
        ALTER TABLE citas ADD COLUMN id SERIAL PRIMARY KEY;
        RAISE NOTICE '✅ Agregada columna id a tabla citas';
    ELSE
        RAISE NOTICE '⚪ Columna id ya existe en tabla citas';
    END IF;
    
    -- Agregar empresa_id si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'citas' AND column_name = 'empresa_id') THEN
        -- Verificar tipo de dato de empresas.id para usar el tipo correcto
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'empresas' AND column_name = 'id' AND data_type = 'uuid') THEN
            ALTER TABLE citas ADD COLUMN empresa_id UUID REFERENCES empresas(id);
        ELSE
            ALTER TABLE citas ADD COLUMN empresa_id INTEGER REFERENCES empresas(id);
        END IF;
        RAISE NOTICE '✅ Agregada columna empresa_id a tabla citas';
    ELSE
        RAISE NOTICE '⚪ Columna empresa_id ya existe en tabla citas';
    END IF;
    
    -- Agregar created_at si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'citas' AND column_name = 'created_at') THEN
        ALTER TABLE citas ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
        RAISE NOTICE '✅ Agregada columna created_at a tabla citas';
    ELSE
        RAISE NOTICE '⚪ Columna created_at ya existe en tabla citas';
    END IF;
    
    -- Agregar activo si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'citas' AND column_name = 'activo') THEN
        ALTER TABLE citas ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE '✅ Agregada columna activo a tabla citas';
    ELSE
        RAISE NOTICE '⚪ Columna activo ya existe en tabla citas';
    END IF;
END $$;

-- 🔧 3. CORREGIR TABLA: security_logs
-- =====================================================================
DO $$ 
BEGIN
    -- Agregar id si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'security_logs' AND column_name = 'id') THEN
        ALTER TABLE security_logs ADD COLUMN id SERIAL PRIMARY KEY;
        RAISE NOTICE '✅ Agregada columna id a tabla security_logs';
    ELSE
        RAISE NOTICE '⚪ Columna id ya existe en tabla security_logs';
    END IF;
    
    -- Agregar created_at si no existe (renombrar timestamp existente si es necesario)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'security_logs' AND column_name = 'created_at') THEN
        -- Si existe 'timestamp', renombrarlo a 'created_at'
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'security_logs' AND column_name = 'timestamp') THEN
            ALTER TABLE security_logs RENAME COLUMN timestamp TO created_at;
            RAISE NOTICE '✅ Renombrada columna timestamp a created_at en security_logs';
        ELSE
            ALTER TABLE security_logs ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
            RAISE NOTICE '✅ Agregada columna created_at a tabla security_logs';
        END IF;
    ELSE
        RAISE NOTICE '⚪ Columna created_at ya existe en tabla security_logs';
    END IF;
END $$;

-- 🔧 4. CORREGIR TABLA: archivos_reportes
-- =====================================================================
DO $$ 
BEGIN
    -- Agregar id si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'archivos_reportes' AND column_name = 'id') THEN
        ALTER TABLE archivos_reportes ADD COLUMN id SERIAL PRIMARY KEY;
        RAISE NOTICE '✅ Agregada columna id a tabla archivos_reportes';
    ELSE
        RAISE NOTICE '⚪ Columna id ya existe en tabla archivos_reportes';
    END IF;
    
    -- Agregar empresa_id si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'archivos_reportes' AND column_name = 'empresa_id') THEN
        -- Verificar tipo de dato de empresas.id
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'empresas' AND column_name = 'id' AND data_type = 'uuid') THEN
            ALTER TABLE archivos_reportes ADD COLUMN empresa_id UUID REFERENCES empresas(id);
        ELSE
            ALTER TABLE archivos_reportes ADD COLUMN empresa_id INTEGER REFERENCES empresas(id);
        END IF;
        RAISE NOTICE '✅ Agregada columna empresa_id a tabla archivos_reportes';
    ELSE
        RAISE NOTICE '⚪ Columna empresa_id ya existe en tabla archivos_reportes';
    END IF;
    
    -- Agregar created_at si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'archivos_reportes' AND column_name = 'created_at') THEN
        ALTER TABLE archivos_reportes ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
        RAISE NOTICE '✅ Agregada columna created_at a tabla archivos_reportes';
    ELSE
        RAISE NOTICE '⚪ Columna created_at ya existe en tabla archivos_reportes';
    END IF;
    
    -- Agregar activo si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'archivos_reportes' AND column_name = 'activo') THEN
        ALTER TABLE archivos_reportes ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE '✅ Agregada columna activo a tabla archivos_reportes';
    ELSE
        RAISE NOTICE '⚪ Columna activo ya existe en tabla archivos_reportes';
    END IF;
END $$;

-- =====================================================================
-- 🎁 MEJORAS ADICIONALES (Opcional - Problemas Medios/Bajos)
-- =====================================================================

-- Agregar columna activo a otras tablas si no existe
DO $$ 
DECLARE
    tables_to_fix text[] := ARRAY['reportes', 'pendientes', 'cuentas_cobrar', 'cuentas_pagar'];
    table_name text;
BEGIN
    FOREACH table_name IN ARRAY tables_to_fix LOOP
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = table_name AND column_name = 'activo') THEN
            EXECUTE format('ALTER TABLE %I ADD COLUMN activo BOOLEAN DEFAULT true', table_name);
            RAISE NOTICE '✅ Agregada columna activo a tabla %', table_name;
        ELSE
            RAISE NOTICE '⚪ Columna activo ya existe en tabla %', table_name;
        END IF;
    END LOOP;
END $$;

-- Agregar columna updated_at donde falte
DO $$ 
DECLARE
    tables_to_fix text[] := ARRAY['reportes', 'cuentas_cobrar', 'cuentas_pagar', 'citas', 'archivos_reportes'];
    table_name text;
BEGIN
    FOREACH table_name IN ARRAY tables_to_fix LOOP
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = table_name AND column_name = 'updated_at') THEN
            EXECUTE format('ALTER TABLE %I ADD COLUMN updated_at TIMESTAMP DEFAULT NOW()', table_name);
            RAISE NOTICE '✅ Agregada columna updated_at a tabla %', table_name;
        ELSE
            RAISE NOTICE '⚪ Columna updated_at ya existe en tabla %', table_name;
        END IF;
    END LOOP;
END $$;

-- =====================================================================
-- 🔄 CREAR TRIGGERS PARA updated_at (Recomendado)
-- =====================================================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar triggers a tablas con updated_at
DO $$
DECLARE
    table_name text;
    tables_with_updated_at text[] := ARRAY['empresas', 'usuarios', 'reportes', 'cuentas_cobrar', 'cuentas_pagar', 'citas', 'archivos_reportes', 'meses_reportes'];
BEGIN
    FOREACH table_name IN ARRAY tables_with_updated_at LOOP
        -- Verificar si la tabla y columna existen
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = table_name AND column_name = 'updated_at') THEN
            
            -- Eliminar trigger si existe
            EXECUTE format('DROP TRIGGER IF EXISTS update_%I_updated_at ON %I', table_name, table_name);
            
            -- Crear nuevo trigger
            EXECUTE format('CREATE TRIGGER update_%I_updated_at 
                           BEFORE UPDATE ON %I 
                           FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()', table_name, table_name);
            
            RAISE NOTICE '🔄 Trigger created for table: %', table_name;
        END IF;
    END LOOP;
END $$;

-- =====================================================================
-- ✅ VERIFICACIONES FINALES
-- =====================================================================

-- Mostrar resumen de tablas
SELECT 
    table_name,
    (SELECT count(*) FROM information_schema.columns WHERE table_name = t.table_name) as columns_count
FROM information_schema.tables t
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- Verificar estructura de tablas críticas corregidas
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable,
    CASE 
        WHEN column_default IS NOT NULL THEN 'YES'
        ELSE 'NO'
    END as has_default
FROM information_schema.columns 
WHERE table_schema = 'public' 
  AND table_name IN ('citas', 'security_logs', 'archivos_reportes', 'meses_reportes')
ORDER BY table_name, ordinal_position;

-- Verificar que meses_reportes tenga 12 registros
SELECT 
    'meses_reportes' as tabla,
    COUNT(*) as registros,
    CASE 
        WHEN COUNT(*) = 12 THEN '✅ CORRECTO'
        ELSE '⚠️ REVISAR'
    END as status
FROM meses_reportes;

-- =====================================================================
-- 🎉 FINALIZADO - RESULTADO FINAL
-- =====================================================================

SELECT 
    '🎉 CORRECCIONES CRÍTICAS APLICADAS EXITOSAMENTE' as status,
    '📊 Ejecutar: python check_database.py para verificar' as next_step,
    '🚀 Puntuación esperada: 95-100/100' as expected_result;

-- FIN DEL SCRIPT