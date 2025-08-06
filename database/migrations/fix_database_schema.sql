-- Fix para agregar campo comentarios a info_compania
-- Ejecutar en Supabase SQL Editor

-- Agregar columna comentarios a info_compania
ALTER TABLE info_compania 
ADD COLUMN IF NOT EXISTS comentarios TEXT;

-- Agregar comentario a la columna
COMMENT ON COLUMN info_compania.comentarios IS 'Comentarios y notas adicionales, incluye ID de Airtable para tracking';