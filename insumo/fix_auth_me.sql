-- ============================================================================
-- CORREGIR POLÍTICAS RLS PARA /auth/me
-- ============================================================================
-- Ejecutar en: Supabase Dashboard > SQL Editor
-- ============================================================================

-- 1. Verificar políticas actuales
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd
FROM pg_policies 
WHERE tablename = 'perfiles';

-- 2. Eliminar políticas existentes (si las hay)
DROP POLICY IF EXISTS "Usuarios ven su propio perfil" ON perfiles;
DROP POLICY IF EXISTS "Usuarios ven perfiles" ON perfiles;
DROP POLICY IF EXISTS "Admins ven todos los perfiles" ON perfiles;

-- 3. Crear política simplificada para SELECT
-- Permite que usuarios autenticados lean SU PROPIO perfil
CREATE POLICY "Usuarios pueden ver su propio perfil" ON perfiles
    FOR SELECT
    USING (auth.uid() = id);

-- 4. Política para que admins puedan ver TODOS los perfiles
CREATE POLICY "Admins pueden ver todos los perfiles" ON perfiles
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol = 'admin'
        )
    );

-- 5. Verificar que las políticas se crearon
SELECT 
    policyname,
    cmd,
    roles,
    qual IS NOT NULL as has_using,
    with_check IS NOT NULL as has_with_check
FROM pg_policies 
WHERE tablename = 'perfiles';

-- ============================================================================
-- PROBAR EL ENDPOINT /auth/me
-- ============================================================================
-- Después de ejecutar, espera 1 minuto y prueba:
-- curl https://inventario-workinn-api.onrender.com/api/v1/auth/me \
--   -H "Authorization: Bearer TU_TOKEN"
-- ============================================================================
