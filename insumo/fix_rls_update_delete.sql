-- ============================================================================
-- FIX: Políticas RLS para UPDATE y DELETE en equipos
-- ============================================================================
-- Ejecutar en: Supabase Dashboard > SQL Editor
-- ============================================================================

-- 1. Política para UPDATE (editar equipos)
drop policy if exists "equipos_update" on equipos;

create policy "equipos_update" on equipos
  for update
  to authenticated
  using (true);

-- 2. Política para DELETE (eliminar equipos)
drop policy if exists "equipos_delete" on equipos;

create policy "equipos_delete" on equipos
  for delete
  to authenticated
  using (
    exists (
      select 1 from perfiles p
      where p.id = auth.uid() and p.rol = 'admin'
    )
  );

-- 3. Políticas para electrónica
drop policy if exists "electronica_update" on electronica;
drop policy if exists "electronica_delete" on electronica;

create policy "electronica_update" on electronica
  for update
  to authenticated
  using (true);

create policy "electronica_delete" on electronica
  for delete
  to authenticated
  using (
    exists (
      select 1 from perfiles p
      where p.id = auth.uid() and p.rol = 'admin'
    )
  );

-- 4. Políticas para robots
drop policy if exists "robots_update" on robots;
drop policy if exists "robots_delete" on robots;

create policy "robots_update" on robots
  for update
  to authenticated
  using (true);

create policy "robots_delete" on robots
  for delete
  to authenticated
  using (
    exists (
      select 1 from perfiles p
      where p.id = auth.uid() and p.rol = 'admin'
    )
  );

-- 5. Políticas para materiales
drop policy if exists "materiales_update" on materiales;
drop policy if exists "materiales_delete" on materiales;

create policy "materiales_update" on materiales
  for update
  to authenticated
  using (true);

create policy "materiales_delete" on materiales
  for delete
  to authenticated
  using (
    exists (
      select 1 from perfiles p
      where p.id = auth.uid() and p.rol = 'admin'
    )
  );

-- 6. Políticas para prestatarios
drop policy if exists "prestatarios_update" on prestatarios;
drop policy if exists "prestatarios_delete" on prestatarios;

create policy "prestatarios_update" on prestatarios
  for update
  to authenticated
  using (true);

create policy "prestatarios_delete" on prestatarios
  for delete
  to authenticated
  using (
    exists (
      select 1 from perfiles p
      where p.id = auth.uid() and p.rol = 'admin'
    )
  );

-- 7. Políticas para préstamos
drop policy if exists "prestamos_update" on prestamos;
drop policy if exists "prestamos_delete" on prestamos;

create policy "prestamos_update" on prestamos
  for update
  to authenticated
  using (true);

create policy "prestamos_delete" on prestamos
  for delete
  to authenticated
  using (
    exists (
      select 1 from perfiles p
      where p.id = auth.uid() and p.rol = 'admin'
    )
  );

-- ============================================================================
-- VERIFICAR POLÍTICAS
-- ============================================================================
-- SELECT tablename, policyname, cmd FROM pg_policies WHERE schemaname = 'public';
-- ============================================================================
