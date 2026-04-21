  -- ============================================================================
  -- SCRIP SQL PARA EJECUTAR EN SUPABASE DASHBOARD > SQL EDITOR
  -- ============================================================================
  -- Fecha: Abril 2026
  -- Proposito: Aplicar politicas RLS para el sistema de roles
  --
  -- ============================================================================
  -- INSTRUCCIONES:
  -- 1. Ir a https://supabase.com/dashboard
  -- 2. Seleccionar el proyecto
  -- 3. Ir a SQL Editor
  -- 4. Copiar y ejecutar este script
  -- ===========================================================================
  -- ============================================================================
  -- 1. PRESTAMOS - Viewer NO ve nada
  -- ============================================================================

  -- Eliminar politica viewer actual (permite leer todo)
  DROP POLICY IF EXISTS "viewer_prestamos_read" ON prestamos;

  -- Crear politica NULL para viewer (no puede ver nada)
  CREATE POLICY "viewer_prestamos_null" ON prestamos
    FOR SELECT
    USING (false);

  -- Verificar que inventory tiene acceso total
  -- (Ya deberian existir, aqui las aseguramos)
  DROP POLICY IF EXISTS "inventory_prestamos_all" ON prestamos;
  CREATE POLICY "inventory_prestamos_all" ON prestamos
    FOR ALL
    USING (get_user_role() = 'inventory')
    WITH CHECK (get_user_role() = 'inventory');

  DROP POLICY IF EXISTS "admin_prestamos_all" ON prestamos;
  CREATE POLICY "admin_prestamos_all" ON prestamos
    FOR ALL
    USING (get_user_role() = 'admin')
    WITH CHECK (get_user_role() = 'admin');

  -- ============================================================================
  -- 2. PRESTATARIOS - Viewer NO ve nada
  -- ============================================================================

  -- Eliminar politica viewer actual
  DROP POLICY IF EXISTS "viewer_prestatarios_read" ON prestatarios;

  -- Crear politica NULL para viewer
  CREATE POLICY "viewer_prestatarios_null" ON prestatarios
    FOR SELECT
    USING (false);

  -- Verificar que inventory tiene acceso total
  DROP POLICY IF EXISTS "inventory_prestatarios_all" ON prestatarios;
  CREATE POLICY "inventory_prestatarios_all" ON prestatarios
    FOR ALL
    USING (get_user_role() = 'inventory')
    WITH CHECK (get_user_role() = 'inventory');

  DROP POLICY IF EXISTS "admin_prestatarios_all" ON prestatarios;
  CREATE POLICY "admin_prestatarios_all" ON prestatarios
    FOR ALL
    USING (get_user_role() = 'admin')
    WITH CHECK (get_user_role() = 'admin');

  -- ============================================================================
  -- 3. MOVIMIENTOS - Viewer NO ve nada, Inventory solo lee
  -- ============================================================================

  -- Eliminar politicas viewer e inventory create
  DROP POLICY IF EXISTS "viewer_movimientos_read" ON movimientos;
  DROP POLICY IF EXISTS "inventory_movimientos_create" ON movimientos;

  -- Crear politica NULL para viewer
  CREATE POLICY "viewer_movimientos_null" ON movimientos
    FOR SELECT
    USING (false);

  -- Crear politica para inventory: SOLO leer (el sistema crea automaticamente)
  DROP POLICY IF EXISTS "inventory_movimientos_read" ON movimientos;
  CREATE POLICY "inventory_movimientos_read" ON movimientos
    FOR SELECT
    USING (get_user_role() = 'inventory');

  -- Admin tiene acceso total (verificar)
  DROP POLICY IF EXISTS "admin_movimientos_all" ON movimientos;
  CREATE POLICY "admin_movimientos_all" ON movimientos
    FOR ALL
    USING (get_user_role() = 'admin')
    WITH CHECK (get_user_role() = 'admin');

  -- ============================================================================
  -- VERIFICACION
  -- ============================================================================

  -- Mostrar politicas aplicadas
  SELECT
    schemaname,
    tablename,
    policyname,
    cmd,
    qual,
    with_check
  FROM pg_policies
  WHERE schemaname = 'public'
  AND tablename IN ('prestamos', 'prestatarios', 'movimientos')
  ORDER BY tablename, policyname;

  -- ============================================================================
  -- FIN DEL SCRIPT
  -- ============================================================================
  -- Ejecutar todo el script en una sola捷
  -- Verificar que no hay errores