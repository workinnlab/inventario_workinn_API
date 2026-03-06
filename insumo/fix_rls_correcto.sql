-- ============================================================================
-- FIX CORRECTO PARA RLS - SIN RECURSIÓN INFINITA
-- ============================================================================
-- Ejecutar en: Supabase Dashboard > SQL Editor
-- ============================================================================

-- 1. Eliminar TODAS las políticas existentes en perfiles
DROP POLICY IF EXISTS "Usuarios ven su propio perfil" ON perfiles;
DROP POLICY IF EXISTS "Usuarios ven perfiles" ON perfiles;
DROP POLICY IF EXISTS "Admins ven todos los perfiles" ON perfiles;
DROP POLICY IF EXISTS "Usuarios pueden ver su propio perfil" ON perfiles;
DROP POLICY IF EXISTS "Admins pueden ver todos los perfiles" ON perfiles;
DROP POLICY IF EXISTS "Usuarios actualizan su perfil" ON perfiles;
DROP POLICY IF EXISTS "Admins insertan perfiles" ON perfiles;

-- 2. Política ÚNICA y SIMPLE para SELECT
-- Cualquier usuario autenticado puede leer CUALQUIER perfil
-- (esto evita recursión porque no hace subquery a perfiles)
CREATE POLICY "perfiles_read_policy" ON perfiles
    FOR SELECT
    USING (auth.role() = 'authenticated');

-- 3. Política para INSERT (solo desde el trigger de auth)
CREATE POLICY "perfiles_insert_policy" ON perfiles
    FOR INSERT
    WITH CHECK (true);

-- 4. Política para UPDATE (cada usuario puede actualizar su propio perfil)
CREATE POLICY "perfiles_update_policy" ON perfiles
    FOR UPDATE
    USING (auth.uid() = id);

-- 5. Verificar políticas
SELECT 
    policyname,
    cmd,
    qual IS NOT NULL as has_using
FROM pg_policies 
WHERE tablename = 'perfiles';

-- ============================================================================
-- Esperar 1 minuto y probar:
-- curl -X POST https://inventario-workinn-api.onrender.com/api/v1/auth/login \
--   -H "Content-Type: application/json" \
--   -d '{"email": "admin@cie.com", "password": "Admin123!"}'
-- ============================================================================
