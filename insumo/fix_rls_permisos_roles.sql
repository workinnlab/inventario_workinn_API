-- ============================================================================
-- NUEVAS POLÍTICAS RLS - Sistema de Roles Inventory CIE
-- ============================================================================
-- Fecha: Abril 2026
-- Propósito: Implementar permisos por rol
--
-- RESUMEN DE PERMISOS:
-- | Recurso        | Viewer      | Inventory        | Admin             |
-- |--------------- |-------------|------------------|-------------------|
-- | Equipos        | LEER        | C, E, B          | TODO              |
-- | Electrónica    | LEER        | C, E, B          | TODO              |
-- | Robots         | LEER        | C, E, B          | TODO              |
-- | Materiales     | LEER        | C, E, B          | TODO              |
-- | Préstamos      | NADA        | C, E, B          | TODO              |
-- | Prestatarios   | NADA        | C, E, B          | TODO              |
-- | Movimientos    | NADA        | LEER             | TODO + Ver autor  |
--
-- ============================================================================

BEGIN;

-- ============================================================================
-- 1. PRÉSTAMOS - Viewer NO ve nada
-- ============================================================================

-- Eliminar política actual de viewer (permite leer todo)
DROP POLICY IF EXISTS "viewer_prestamos_read" ON prestamos;

-- Crear política NULL para viewer (no puede ver nada)
CREATE POLICY "viewer_prestamos_null" ON prestamos
  FOR SELECT
  USING (false);

-- Verificar que inventory tiene acceso total (ya existe)
-- CREATE POLICY "inventory_prestamos_all" ON prestamos
--   FOR ALL USING (get_user_role() = 'inventory')
--   WITH CHECK (get_user_role() = 'inventory');

-- Verificar que admin tiene acceso total (ya existe)
-- CREATE POLICY "admin_prestamos_all" ON prestamos
--   FOR ALL USING (get_user_role() = 'admin')
--   WITH CHECK (get_user_role() = 'admin');


-- ============================================================================
-- 2. PRESTATARIOS - Viewer NO ve nada
-- ============================================================================

-- Eliminar política actual de viewer (permite leer todo)
DROP POLICY IF EXISTS "viewer_prestatarios_read" ON prestatarios;

-- Crear política NULL para viewer (no puede ver nada)
CREATE POLICY "viewer_prestatarios_null" ON prestatarios
  FOR SELECT
  USING (false);

-- Verificar que inventory tiene acceso total (ya existe)
-- CREATE POLICY "inventory_prestatarios_all" ON prestatarios
--   FOR ALL USING (get_user_role() = 'inventory')
--   WITH CHECK (get_user_role() = 'inventory');


-- ============================================================================
-- 3. MOVIMIENTOS - Viewer NO ve nada, Inventory solo lee, Admin ve todo
-- ============================================================================

-- Eliminar política actual de viewer (permite leer)
DROP POLICY IF EXISTS "viewer_movimientos_read" ON movimientos;

-- Eliminar política de creación de inventory (el sistema crea los movimientos automáticamente)
DROP POLICY IF EXISTS "inventory_movimientos_create" ON movimientos;

-- Crear política NULL para viewer (no puede ver nada)
CREATE POLICY "viewer_movimientos_null" ON movimientos
  FOR SELECT
  USING (false);

-- Crear política para inventory: SOLO leer (el sistema crea automáticamente)
CREATE POLICY "inventory_movimientos_read" ON movimientos
  FOR SELECT
  USING (get_user_role() = 'inventory');

-- Admin ya tiene acceso total (ya existe)
-- CREATE POLICY "admin_movimientos_all" ON movimientos
--   FOR ALL USING (get_user_role() = 'admin')
--   WITH CHECK (get_user_role() = 'admin');


-- ============================================================================
-- 4. VERIFICAR QUE EQUIPOS, ELECTRÓNICA, ROBOTS, MATERIALES ESTÉN BIEN
-- ============================================================================

-- Equipos: Verificar viewer solo lee
-- Ya está: "viewer_equipos_read" usando (true)
-- Inventory y admin ya tienen políticas

-- Electrónica: Verificar viewer solo lee
-- Ya está: "viewer_electronica_read" usando (true)

-- Robots: Verificar viewer solo lee
-- Ya está: "viewer_robots_read" usando (true)

-- Materiales: Verificar viewer solo lee
-- Ya está: "viewer_materiales_read" usando (true)


-- ============================================================================
-- 5. CONFIGURACIÓN - Solo admin
-- ============================================================================

-- Verificar que viewer e inventory NO puedan ver configuración
-- (Ya debería estar implementado en schema_supabase.sql)


COMMIT;

-- ============================================================================
-- IMPORTANTE: ARQUITECTURA DE AUTENTICACIÓN
-- ============================================================================

-- NOTA: Para que estas políticas RLS funcionen correctamente,
-- el cliente de Supabase necesita usar el TOKEN del usuario, no la key pública (anon).

-- Actualmente los endpoints usan:
--   get_supabase_client() = create_client(url, SUPABASE_KEY)
-- donde SUPABASE_KEY es la key pública (anon).

-- Esto significa que RLS always will see "anon" como usuario, no el usuario real.

-- SOLUCIÓN NECESARIA EN PYTHON:
-- Opción 1: Modificar endpoints para aceitar el token y criar cliente con él
-- Opción 2: Usar middleware que extraiga el token del header Authorization

-- Ejemplo de cómo debería funcionar:
-- def get_supabase_with_token(token: str) -> Client:
--     return create_client(settings.SUPABASE_URL, token)

-- Y en el endpoint:
-- @router.get("/prestamos")
-- def listar_prestamos(
--     credentials: HTTPAuthorizationCredentials = Depends(security),
--     supabase: Client = Depends(lambda: get_supabase_with_token(credentials.credentials))
-- ):
--     ...
-- (Esto es un ejemplo, depende de la implementación)

-- HASTA QUE SE ARREGLE LA ARQUITECTURA:
-- Las políticas RLS below will NOT work as expected because auth.uid() siempre return null.
-- Instead you'll need to validar roles en Python.


-- ============================================================================
-- VERIFICACIÓN POST-EJECUCIÓN
-- ============================================================================

-- Ejecutar estas consultas para verificar:

-- Ver políticas actuales:
-- SELECT policyname, tablename, cmd, qual
-- FROM pg_policies
-- WHERE schemaname = 'public'
-- ORDER BY tablename, policyname;

-- Ver si auth.uid() está funcionando:
-- SELECT auth.uid();  -- Should return user ID when called via API with token
