-- ============================================================================
-- VERIFICAR Y CORREGIR POLÍTICAS RLS PARA TODAS LAS TABLAS
-- ============================================================================
-- Ejecutar en: Supabase Dashboard > SQL Editor
-- ============================================================================

-- 1. Verificar usuario actual y su rol
SELECT 
    u.id,
    u.email,
    u.raw_user_meta_data->>'nombre' as nombre,
    u.raw_user_meta_data->>'rol' as rol,
    p.rol as perfil_rol,
    p.activo
FROM auth.users u
LEFT JOIN perfiles p ON p.id = u.id
WHERE u.email = 'eduardopimienta@americana.edu.co';

-- 2. Verificar políticas actuales en todas las tablas
SELECT 
    tablename,
    policyname,
    cmd,
    roles,
    qual IS NOT NULL as has_using
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

-- ============================================================================
-- POLÍTICAS PARA EQUIPOS
-- ============================================================================

DROP POLICY IF EXISTS "equipos_select" ON equipos;
DROP POLICY IF EXISTS "equipos_insert" ON equipos;
DROP POLICY IF EXISTS "equipos_update" ON equipos;
DROP POLICY IF EXISTS "equipos_delete" ON equipos;

-- SELECT: Todos los autenticados pueden leer
CREATE POLICY "equipos_select" ON equipos
    FOR SELECT
    TO authenticated
    USING (true);

-- INSERT: Admin e inventory pueden crear
CREATE POLICY "equipos_insert" ON equipos
    FOR INSERT
    TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

-- UPDATE: Admin e inventory pueden editar
CREATE POLICY "equipos_update" ON equipos
    FOR UPDATE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

-- DELETE: Solo admin puede eliminar
CREATE POLICY "equipos_delete" ON equipos
    FOR DELETE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol = 'admin'
        )
    );

-- ============================================================================
-- POLÍTICAS PARA ELECTRONICA
-- ============================================================================

DROP POLICY IF EXISTS "electronica_select" ON electronica;
DROP POLICY IF EXISTS "electronica_insert" ON electronica;
DROP POLICY IF EXISTS "electronica_update" ON electronica;
DROP POLICY IF EXISTS "electronica_delete" ON electronica;

CREATE POLICY "electronica_select" ON electronica
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "electronica_insert" ON electronica
    FOR INSERT TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

CREATE POLICY "electronica_update" ON electronica
    FOR UPDATE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

CREATE POLICY "electronica_delete" ON electronica
    FOR DELETE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol = 'admin'
        )
    );

-- ============================================================================
-- POLÍTICAS PARA ROBOTS
-- ============================================================================

DROP POLICY IF EXISTS "robots_select" ON robots;
DROP POLICY IF EXISTS "robots_insert" ON robots;
DROP POLICY IF EXISTS "robots_update" ON robots;
DROP POLICY IF EXISTS "robots_delete" ON robots;

CREATE POLICY "robots_select" ON robots
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "robots_insert" ON robots
    FOR INSERT TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

CREATE POLICY "robots_update" ON robots
    FOR UPDATE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

CREATE POLICY "robots_delete" ON robots
    FOR DELETE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol = 'admin'
        )
    );

-- ============================================================================
-- POLÍTICAS PARA MATERIALES
-- ============================================================================

DROP POLICY IF EXISTS "materiales_select" ON materiales;
DROP POLICY IF EXISTS "materiales_insert" ON materiales;
DROP POLICY IF EXISTS "materiales_update" ON materiales;
DROP POLICY IF EXISTS "materiales_delete" ON materiales;

CREATE POLICY "materiales_select" ON materiales
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "materiales_insert" ON materiales
    FOR INSERT TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

CREATE POLICY "materiales_update" ON materiales
    FOR UPDATE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

CREATE POLICY "materiales_delete" ON materiales
    FOR DELETE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol = 'admin'
        )
    );

-- ============================================================================
-- POLÍTICAS PARA PRESTATARIOS
-- ============================================================================

DROP POLICY IF EXISTS "prestatarios_select" ON prestatarios;
DROP POLICY IF EXISTS "prestatarios_insert" ON prestatarios;
DROP POLICY IF EXISTS "prestatarios_update" ON prestatarios;
DROP POLICY IF EXISTS "prestatarios_delete" ON prestatarios;

CREATE POLICY "prestatarios_select" ON prestatarios
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "prestatarios_insert" ON prestatarios
    FOR INSERT TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

CREATE POLICY "prestatarios_update" ON prestatarios
    FOR UPDATE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

CREATE POLICY "prestatarios_delete" ON prestatarios
    FOR DELETE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

-- ============================================================================
-- POLÍTICAS PARA PRÉSTAMOS
-- ============================================================================

DROP POLICY IF EXISTS "prestamos_select" ON prestamos;
DROP POLICY IF EXISTS "prestamos_insert" ON prestamos;
DROP POLICY IF EXISTS "prestamos_update" ON prestamos;
DROP POLICY IF EXISTS "prestamos_delete" ON prestamos;

CREATE POLICY "prestamos_select" ON prestamos
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "prestamos_insert" ON prestamos
    FOR INSERT TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

CREATE POLICY "prestamos_update" ON prestamos
    FOR UPDATE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

CREATE POLICY "prestamos_delete" ON prestamos
    FOR DELETE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol = 'admin'
        )
    );

-- ============================================================================
-- POLÍTICAS PARA MOVIMIENTOS
-- ============================================================================

DROP POLICY IF EXISTS "movimientos_select" ON movimientos;
DROP POLICY IF EXISTS "movimientos_insert" ON movimientos;
DROP POLICY IF EXISTS "movimientos_update" ON movimientos;
DROP POLICY IF EXISTS "movimientos_delete" ON movimientos;

CREATE POLICY "movimientos_select" ON movimientos
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "movimientos_insert" ON movimientos
    FOR INSERT TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

CREATE POLICY "movimientos_update" ON movimientos
    FOR UPDATE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol IN ('admin', 'inventory')
        )
    );

CREATE POLICY "movimientos_delete" ON movimientos
    FOR DELETE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM perfiles p 
            WHERE p.id = auth.uid() AND p.rol = 'admin'
        )
    );

-- ============================================================================
-- POLÍTICAS PARA PERFILES
-- ============================================================================

DROP POLICY IF EXISTS "perfiles_select" ON perfiles;
DROP POLICY IF EXISTS "perfiles_insert" ON perfiles;
DROP POLICY IF EXISTS "perfiles_update" ON perfiles;

CREATE POLICY "perfiles_select" ON perfiles
    FOR SELECT TO authenticated
    USING (true);

CREATE POLICY "perfiles_insert" ON perfiles
    FOR INSERT TO authenticated
    WITH CHECK (true);

CREATE POLICY "perfiles_update" ON perfiles
    FOR UPDATE TO authenticated
    USING (auth.uid() = id);

-- ============================================================================
-- VERIFICACIÓN FINAL
-- ============================================================================

-- Mostrar todas las políticas creadas
SELECT 
    tablename,
    policyname,
    cmd,
    roles
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

-- ============================================================================
-- AHORA LAS OPERACIONES DEBERÍAN FUNCIONAR
-- ============================================================================
