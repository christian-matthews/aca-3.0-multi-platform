-- =====================================================
-- SCRIPT PARA BORRAR COMPLETAMENTE LA BASE DE DATOS
-- ⚠️ ADVERTENCIA: ESTO BORRARÁ TODOS LOS DATOS
-- =====================================================

-- Deshabilitar triggers temporalmente
SET session_replication_role = replica;

-- =====================================================
-- BORRAR TODAS LAS TABLAS
-- =====================================================

-- Borrar tablas en orden (respetando foreign keys)
DROP TABLE IF EXISTS security_logs CASCADE;
DROP TABLE IF EXISTS citas CASCADE;
DROP TABLE IF EXISTS cuentas_pagar CASCADE;
DROP TABLE IF EXISTS cuentas_cobrar CASCADE;
DROP TABLE IF EXISTS pendientes CASCADE;
DROP TABLE IF EXISTS reportes CASCADE;
DROP TABLE IF EXISTS conversaciones CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS empresas CASCADE;

-- =====================================================
-- BORRAR VISTAS
-- =====================================================

DROP VIEW IF EXISTS resumen_cuentas CASCADE;
DROP VIEW IF EXISTS resumen_pendientes CASCADE;

-- =====================================================
-- BORRAR FUNCIONES
-- =====================================================

DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- =====================================================
-- BORRAR EXTENSIONES (opcional)
-- =====================================================

-- DROP EXTENSION IF EXISTS "uuid-ossp";

-- =====================================================
-- REHABILITAR TRIGGERS
-- =====================================================

SET session_replication_role = DEFAULT;

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================

SELECT '🗑️ Base de datos ACA 3.0 borrada completamente!' as mensaje;
SELECT '📝 Para recrear la base de datos, ejecuta el script de docs/setup_database.md' as instruccion; 