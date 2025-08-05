-- =====================================================
-- SCRIPT DE VERIFICACIÓN - ACA 3.0
-- =====================================================

-- Verificar que las tablas existen
SELECT 
    table_name,
    CASE 
        WHEN table_name IS NOT NULL THEN '✅ Existe'
        ELSE '❌ No existe'
    END as estado
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
    'empresas', 'usuarios', 'conversaciones', 'reportes', 
    'pendientes', 'cuentas_cobrar', 'cuentas_pagar', 
    'citas', 'security_logs'
)
ORDER BY table_name;

-- Verificar empresas creadas
SELECT 
    'Empresas' as tipo,
    COUNT(*) as total,
    STRING_AGG(nombre, ', ') as nombres
FROM empresas;

-- Verificar usuarios creados
SELECT 
    'Usuarios' as tipo,
    COUNT(*) as total,
    STRING_AGG(nombre, ', ') as nombres
FROM usuarios;

-- Verificar reportes creados
SELECT 
    'Reportes' as tipo,
    COUNT(*) as total,
    STRING_AGG(titulo, ', ') as titulos
FROM reportes;

-- Verificar pendientes creados
SELECT 
    'Pendientes' as tipo,
    COUNT(*) as total,
    STRING_AGG(titulo, ', ') as titulos
FROM pendientes;

-- Verificar cuentas por cobrar
SELECT 
    'Cuentas por Cobrar' as tipo,
    COUNT(*) as total,
    SUM(monto) as monto_total
FROM cuentas_cobrar;

-- Verificar cuentas por pagar
SELECT 
    'Cuentas por Pagar' as tipo,
    COUNT(*) as total,
    SUM(monto) as monto_total
FROM cuentas_pagar;

-- Verificar conversaciones
SELECT 
    'Conversaciones' as tipo,
    COUNT(*) as total
FROM conversaciones;

-- Verificar índices creados
SELECT 
    indexname,
    tablename,
    indexdef
FROM pg_indexes 
WHERE schemaname = 'public' 
AND indexname LIKE 'idx_%'
ORDER BY tablename, indexname;

-- Verificar políticas RLS
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

-- Verificar vistas creadas
SELECT 
    viewname,
    definition
FROM pg_views 
WHERE schemaname = 'public'
AND viewname IN ('resumen_cuentas', 'resumen_pendientes');

-- Resumen final
SELECT '🎉 Verificación completada - Revisa los resultados arriba' as mensaje; 