-- Actualizar vista para AGREGAR user_id (sin cambiar columnas existentes)
CREATE OR REPLACE VIEW vista_conversaciones_recientes AS
SELECT 
    c.id,
    c.chat_id,
    c.usuario_nombre,
    c.usuario_username,
    COALESCE(e.nombre, 'Usuario No Registrado') as empresa_nombre,
    c.mensaje,
    c.respuesta,
    c.bot_tipo,
    c.created_at,
    CASE 
        WHEN c.empresa_id IS NOT NULL THEN 'Autorizado'
        ELSE 'No Autorizado'
    END as estado_usuario,
    ud.user_id  -- NUEVA COLUMNA AGREGADA AL FINAL
FROM conversaciones c
LEFT JOIN empresas e ON c.empresa_id = e.id
LEFT JOIN usuarios_detalle ud ON c.chat_id = ud.chat_id
ORDER BY c.created_at DESC
LIMIT 1000;
