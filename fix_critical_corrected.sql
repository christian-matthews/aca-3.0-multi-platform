-- 🔧 CORRECCIÓN OPTIMIZADA DE PROBLEMAS CRÍTICOS - ACA 3.0 (CORREGIDA)
-- ✅ Script seguro con verificaciones IF NOT EXISTS
-- 🐛 Error de ambigüedad corregido
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
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'citas' AND c.column_name = 'id') THEN
        ALTER TABLE citas ADD COLUMN id SERIAL PRIMARY KEY;
        RAISE NOTICE '✅ Agregada columna id a tabla citas';
    ELSE
        RAISE NOTICE '⚪ Columna id ya existe en tabla citas';
    END IF;
    
    -- Agregar empresa_id si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'citas' AND c.column_name = 'empresa_id') THEN
        -- Verificar tipo de dato de empresas.id para usar el tipo correcto
        IF EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'empresas' AND c.column_name = 'id' AND c.data_type = 'uuid') THEN
            ALTER TABLE citas ADD COLUMN empresa_id UUID REFERENCES empresas(id);
        ELSE
            ALTER TABLE citas ADD COLUMN empresa_id INTEGER REFERENCES empresas(id);
        END IF;
        RAISE NOTICE '✅ Agregada columna empresa_id a tabla citas';
    ELSE
        RAISE NOTICE '⚪ Columna empresa_id ya existe en tabla citas';
    END IF;
    
    -- Agregar created_at si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'citas' AND c.column_name = 'created_at') THEN
        ALTER TABLE citas ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
        RAISE NOTICE '✅ Agregada columna created_at a tabla citas';
    ELSE
        RAISE NOTICE '⚪ Columna created_at ya existe en tabla citas';
    END IF;
    
    -- Agregar activo si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'citas' AND c.column_name = 'activo') THEN
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
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'security_logs' AND c.column_name = 'id') THEN
        ALTER TABLE security_logs ADD COLUMN id SERIAL PRIMARY KEY;
        RAISE NOTICE '✅ Agregada columna id a tabla security_logs';
    ELSE
        RAISE NOTICE '⚪ Columna id ya existe en tabla security_logs';
    END IF;
    
    -- Agregar created_at si no existe (renombrar timestamp existente si es necesario)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'security_logs' AND c.column_name = 'created_at') THEN
        -- Si existe 'timestamp', renombrarlo a 'created_at'
        IF EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'security_logs' AND c.column_name = 'timestamp') THEN
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
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'archivos_reportes' AND c.column_name = 'id') THEN
        ALTER TABLE archivos_reportes ADD COLUMN id SERIAL PRIMARY KEY;
        RAISE NOTICE '✅ Agregada columna id a tabla archivos_reportes';
    ELSE
        RAISE NOTICE '⚪ Columna id ya existe en tabla archivos_reportes';
    END IF;
    
    -- Agregar empresa_id si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'archivos_reportes' AND c.column_name = 'empresa_id') THEN
        -- Verificar tipo de dato de empresas.id
        IF EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'empresas' AND c.column_name = 'id' AND c.data_type = 'uuid') THEN
            ALTER TABLE archivos_reportes ADD COLUMN empresa_id UUID REFERENCES empresas(id);
        ELSE
            ALTER TABLE archivos_reportes ADD COLUMN empresa_id INTEGER REFERENCES empresas(id);
        END IF;
        RAISE NOTICE '✅ Agregada columna empresa_id a tabla archivos_reportes';
    ELSE
        RAISE NOTICE '⚪ Columna empresa_id ya existe en tabla archivos_reportes';
    END IF;
    
    -- Agregar created_at si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'archivos_reportes' AND c.column_name = 'created_at') THEN
        ALTER TABLE archivos_reportes ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
        RAISE NOTICE '✅ Agregada columna created_at a tabla archivos_reportes';
    ELSE
        RAISE NOTICE '⚪ Columna created_at ya existe en tabla archivos_reportes';
    END IF;
    
    -- Agregar activo si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'archivos_reportes' AND c.column_name = 'activo') THEN
        ALTER TABLE archivos_reportes ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE '✅ Agregada columna activo a tabla archivos_reportes';
    ELSE
        RAISE NOTICE '⚪ Columna activo ya existe en tabla archivos_reportes';
    END IF;
END $$;

-- =====================================================================
-- 🎁 MEJORAS ADICIONALES (Opcional - Problemas Medios/Bajos)
-- =====================================================================

-- Agregar columna activo a otras tablas si no existe (CORREGIDO)
DO $$ 
DECLARE
    tabla_actual text;
BEGIN
    -- Procesar reportes
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'reportes' AND c.column_name = 'activo') THEN
        ALTER TABLE reportes ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE '✅ Agregada columna activo a tabla reportes';
    ELSE
        RAISE NOTICE '⚪ Columna activo ya existe en tabla reportes';
    END IF;
    
    -- Procesar pendientes
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'pendientes' AND c.column_name = 'activo') THEN
        ALTER TABLE pendientes ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE '✅ Agregada columna activo a tabla pendientes';
    ELSE
        RAISE NOTICE '⚪ Columna activo ya existe en tabla pendientes';
    END IF;
    
    -- Procesar cuentas_cobrar
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'cuentas_cobrar' AND c.column_name = 'activo') THEN
        ALTER TABLE cuentas_cobrar ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE '✅ Agregada columna activo a tabla cuentas_cobrar';
    ELSE
        RAISE NOTICE '⚪ Columna activo ya existe en tabla cuentas_cobrar';
    END IF;
    
    -- Procesar cuentas_pagar
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'cuentas_pagar' AND c.column_name = 'activo') THEN
        ALTER TABLE cuentas_pagar ADD COLUMN activo BOOLEAN DEFAULT true;
        RAISE NOTICE '✅ Agregada columna activo a tabla cuentas_pagar';
    ELSE
        RAISE NOTICE '⚪ Columna activo ya existe en tabla cuentas_pagar';
    END IF;
END $$;

-- Agregar columna updated_at donde falte (CORREGIDO)
DO $$ 
BEGIN
    -- Procesar reportes
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'reportes' AND c.column_name = 'updated_at') THEN
        ALTER TABLE reportes ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
        RAISE NOTICE '✅ Agregada columna updated_at a tabla reportes';
    ELSE
        RAISE NOTICE '⚪ Columna updated_at ya existe en tabla reportes';
    END IF;
    
    -- Procesar cuentas_cobrar
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'cuentas_cobrar' AND c.column_name = 'updated_at') THEN
        ALTER TABLE cuentas_cobrar ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
        RAISE NOTICE '✅ Agregada columna updated_at a tabla cuentas_cobrar';
    ELSE
        RAISE NOTICE '⚪ Columna updated_at ya existe en tabla cuentas_cobrar';
    END IF;
    
    -- Procesar cuentas_pagar
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'cuentas_pagar' AND c.column_name = 'updated_at') THEN
        ALTER TABLE cuentas_pagar ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
        RAISE NOTICE '✅ Agregada columna updated_at a tabla cuentas_pagar';
    ELSE
        RAISE NOTICE '⚪ Columna updated_at ya existe en tabla cuentas_pagar';
    END IF;
    
    -- Procesar archivos_reportes (si no se agregó antes)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = 'archivos_reportes' AND c.column_name = 'updated_at') THEN
        ALTER TABLE archivos_reportes ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
        RAISE NOTICE '✅ Agregada columna updated_at a tabla archivos_reportes';
    ELSE
        RAISE NOTICE '⚪ Columna updated_at ya existe en tabla archivos_reportes';
    END IF;
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

-- Aplicar triggers a tablas específicas (CORREGIDO)
DO $$
DECLARE
    tabla_actual text;
BEGIN
    -- Lista de tablas que deberían tener trigger de updated_at
    FOR tabla_actual IN 
        SELECT unnest(ARRAY['empresas', 'usuarios', 'reportes', 'cuentas_cobrar', 'cuentas_pagar', 'citas', 'archivos_reportes', 'meses_reportes'])
    LOOP
        -- Verificar si la tabla y columna existen
        IF EXISTS (SELECT 1 FROM information_schema.columns c
                   WHERE c.table_name = tabla_actual AND c.column_name = 'updated_at') THEN
            
            -- Eliminar trigger si existe
            EXECUTE format('DROP TRIGGER IF EXISTS update_%I_updated_at ON %I', tabla_actual, tabla_actual);
            
            -- Crear nuevo trigger
            EXECUTE format('CREATE TRIGGER update_%I_updated_at 
                           BEFORE UPDATE ON %I 
                           FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()', tabla_actual, tabla_actual);
            
            RAISE NOTICE '🔄 Trigger created for table: %', tabla_actual;
        END IF;
    END LOOP;
END $$;

-- =====================================================================
-- ✅ VERIFICACIONES FINALES
-- =====================================================================

-- Mostrar resumen de tablas
SELECT 
    t.table_name,
    (SELECT count(*) FROM information_schema.columns c WHERE c.table_name = t.table_name) as columns_count
FROM information_schema.tables t
WHERE t.table_schema = 'public' 
  AND t.table_type = 'BASE TABLE'
ORDER BY t.table_name;

-- Verificar estructura de tablas críticas corregidas
SELECT 
    c.table_name,
    c.column_name,
    c.data_type,
    c.is_nullable,
    CASE 
        WHEN c.column_default IS NOT NULL THEN 'YES'
        ELSE 'NO'
    END as has_default
FROM information_schema.columns c
WHERE c.table_schema = 'public' 
  AND c.table_name IN ('citas', 'security_logs', 'archivos_reportes', 'meses_reportes')
ORDER BY c.table_name, c.ordinal_position;

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