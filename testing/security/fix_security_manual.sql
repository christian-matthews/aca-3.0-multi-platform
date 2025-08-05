-- ===============================================
-- 🔴 CORRECCIÓN CRÍTICA DE SEGURIDAD ACA 3.0
-- ===============================================
-- 
-- EJECUTAR EN: Supabase Dashboard > SQL Editor
-- PROPÓSITO: Corregir falla crítica de seguridad
-- 
-- PROBLEMA: archivos_reportes y archivos_info_compania 
--           NO tienen empresa_id (riesgo seguridad)
-- 
-- SOLUCIÓN: Agregar empresa_id + RLS policies
-- ===============================================

-- Paso 1: Agregar empresa_id a archivos_reportes
-- ===============================================
DO $$ 
BEGIN
    -- Verificar si la columna ya existe
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'archivos_reportes' 
        AND column_name = 'empresa_id'
    ) THEN
        -- Agregar la columna
        ALTER TABLE archivos_reportes 
        ADD COLUMN empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE;
        
        RAISE NOTICE '✅ Columna empresa_id agregada a archivos_reportes';
    ELSE
        RAISE NOTICE '⚠️ Columna empresa_id ya existe en archivos_reportes';
    END IF;
END $$;

-- Paso 2: Agregar empresa_id a archivos_info_compania
-- ===================================================
DO $$ 
BEGIN
    -- Verificar si la columna ya existe
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'archivos_info_compania' 
        AND column_name = 'empresa_id'
    ) THEN
        -- Agregar la columna
        ALTER TABLE archivos_info_compania 
        ADD COLUMN empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE;
        
        RAISE NOTICE '✅ Columna empresa_id agregada a archivos_info_compania';
    ELSE
        RAISE NOTICE '⚠️ Columna empresa_id ya existe en archivos_info_compania';
    END IF;
END $$;

-- Paso 3: Actualizar registros existentes (si los hay)
-- ====================================================

-- Obtener el primer empresa_id disponible para registros huérfanos
DO $$
DECLARE
    default_empresa_id UUID;
BEGIN
    -- Obtener una empresa existente
    SELECT id INTO default_empresa_id 
    FROM empresas 
    LIMIT 1;
    
    IF default_empresa_id IS NOT NULL THEN
        -- Actualizar archivos_reportes huérfanos
        UPDATE archivos_reportes 
        SET empresa_id = default_empresa_id 
        WHERE empresa_id IS NULL;
        
        RAISE NOTICE '✅ Registros huérfanos en archivos_reportes actualizados';
        
        -- Actualizar archivos_info_compania huérfanos  
        UPDATE archivos_info_compania 
        SET empresa_id = default_empresa_id 
        WHERE empresa_id IS NULL;
        
        RAISE NOTICE '✅ Registros huérfanos en archivos_info_compania actualizados';
    ELSE
        RAISE NOTICE '⚠️ No hay empresas disponibles para actualizar registros';
    END IF;
END $$;

-- Paso 4: Habilitar Row Level Security (RLS)
-- ===========================================

-- Habilitar RLS en archivos_reportes
ALTER TABLE archivos_reportes ENABLE ROW LEVEL SECURITY;

-- Habilitar RLS en archivos_info_compania  
ALTER TABLE archivos_info_compania ENABLE ROW LEVEL SECURITY;

-- Paso 5: Crear políticas de seguridad
-- ====================================

-- Eliminar políticas existentes si existen
DROP POLICY IF EXISTS "archivos_reportes_empresa_policy" ON archivos_reportes;
DROP POLICY IF EXISTS "archivos_info_compania_empresa_policy" ON archivos_info_compania;

-- Política para archivos_reportes - solo acceso a archivos de su empresa
CREATE POLICY "archivos_reportes_empresa_policy" ON archivos_reportes
    FOR ALL USING (
        -- Permitir acceso si el usuario pertenece a la misma empresa
        empresa_id IN (
            SELECT empresa_id 
            FROM usuarios 
            WHERE chat_id = current_setting('app.current_user_chat_id')::BIGINT
        )
    );

-- Política para archivos_info_compania - solo acceso a archivos de su empresa
CREATE POLICY "archivos_info_compania_empresa_policy" ON archivos_info_compania
    FOR ALL USING (
        -- Permitir acceso si el usuario pertenece a la misma empresa
        empresa_id IN (
            SELECT empresa_id 
            FROM usuarios 
            WHERE chat_id = current_setting('app.current_user_chat_id')::BIGINT
        )
    );

-- Paso 6: Crear índices para performance
-- ======================================

-- Índice en archivos_reportes.empresa_id
CREATE INDEX IF NOT EXISTS idx_archivos_reportes_empresa_id 
ON archivos_reportes(empresa_id);

-- Índice en archivos_info_compania.empresa_id
CREATE INDEX IF NOT EXISTS idx_archivos_info_compania_empresa_id 
ON archivos_info_compania(empresa_id);

-- Paso 7: Verificación final
-- ==========================

-- Mostrar estructura actualizada de archivos_reportes
SELECT 
    'archivos_reportes' as tabla,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'archivos_reportes' 
ORDER BY ordinal_position;

-- Mostrar estructura actualizada de archivos_info_compania
SELECT 
    'archivos_info_compania' as tabla,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'archivos_info_compania' 
ORDER BY ordinal_position;

-- Verificar que RLS está habilitado
SELECT 
    schemaname, 
    tablename, 
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE tablename IN ('archivos_reportes', 'archivos_info_compania');

-- Verificar políticas creadas
SELECT 
    schemaname,
    tablename, 
    policyname,
    permissive,
    roles,
    cmd,
    qual
FROM pg_policies 
WHERE tablename IN ('archivos_reportes', 'archivos_info_compania');

-- ===============================================
-- 🎉 CORRECCIÓN COMPLETADA
-- ===============================================
-- 
-- ✅ FALLA CRÍTICA DE SEGURIDAD CORREGIDA
-- 
-- CAMBIOS REALIZADOS:
-- 1. ✅ empresa_id agregado a archivos_reportes
-- 2. ✅ empresa_id agregado a archivos_info_compania  
-- 3. ✅ RLS habilitado en ambas tablas
-- 4. ✅ Políticas de seguridad por empresa
-- 5. ✅ Índices para performance
-- 6. ✅ Registros existentes actualizados
-- 
-- SEGURIDAD IMPLEMENTADA:
-- - Aislamiento total por empresa
-- - Usuarios solo ven archivos de su empresa
-- - Prevención de acceso cruzado
-- 
-- ===============================================