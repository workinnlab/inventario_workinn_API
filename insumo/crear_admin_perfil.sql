-- ============================================================================
-- CREAR PERFIL PARA EL ADMIN (eduardopimienta@americana.edu.co)
-- ============================================================================
-- Ejecutar en: Supabase Dashboard > SQL Editor
-- ============================================================================

-- Insertar/actualizar el perfil del admin
INSERT INTO perfiles (id, nombre, email, rol, activo)
SELECT 
    id,
    COALESCE(raw_user_meta_data->>'nombre', 'Eduardo Pimienta'),
    email,
    COALESCE(raw_user_meta_data->>'rol', 'admin'),
    true
FROM auth.users 
WHERE email = 'eduardopimienta@americana.edu.co'
ON CONFLICT (id) DO UPDATE SET
    nombre = EXCLUDED.nombre,
    email = EXCLUDED.email,
    rol = EXCLUDED.rol,
    activo = EXCLUDED.activo,
    updated_at = NOW();

-- Verificar que se creó
SELECT 
    id,
    nombre,
    email,
    rol,
    activo,
    created_at
FROM perfiles 
WHERE email = 'eduardopimienta@americana.edu.co';

-- ============================================================================
-- AHORA EL LOGIN DEBERÍA FUNCIONAR
-- ============================================================================
