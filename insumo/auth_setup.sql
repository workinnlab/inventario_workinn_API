-- ============================================================================
-- CONFIGURACIÓN DE AUTENTICACIÓN - SUPABASE
-- ============================================================================
-- Ejecutar este script en: Supabase Dashboard > SQL Editor
-- ============================================================================

-- 1. Tabla de perfiles vinculada a auth.users
create table if not exists perfiles (
  id uuid primary key references auth.users(id) on delete cascade,
  nombre text not null,
  email text unique not null,
  rol text not null default 'viewer' check (rol in ('admin', 'inventory', 'viewer')),
  activo boolean default true,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Habilitar RLS
alter table perfiles enable row level security;

-- 2. Función para crear perfil automáticamente al registrar usuario
create or replace function crear_perfil_automatico()
returns trigger as $$
begin
  insert into perfiles (id, nombre, email, rol)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'nombre', split_part(new.email, '@', 1)),
    new.email,
    coalesce(new.raw_user_meta_data->>'rol', 'viewer')
  );
  return new;
end;
$$ language plpgsql security definer;

-- 3. Trigger para crear perfil al registrar usuario
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row
  execute function crear_perfil_automatico();

-- 4. Políticas RLS para perfiles
drop policy if exists "Usuarios ven su propio perfil" on perfiles;
create policy "Usuarios ven su propio perfil" on perfiles
  for select using (auth.uid() = id);

drop policy if exists "Admins ven todos los perfiles" on perfiles;
create policy "Admins ven todos los perfiles" on perfiles
  for select using (
    exists (select 1 from perfiles where id = auth.uid() and rol = 'admin')
  );

drop policy if exists "Usuarios actualizan su perfil" on perfiles;
create policy "Usuarios actualizan su perfil" on perfiles
  for update using (auth.uid() = id);

-- ============================================================================
-- VERIFICACIÓN
-- ============================================================================
-- Después de ejecutar, verifica que el trigger existe:
-- SELECT * FROM pg_trigger WHERE tgname = 'on_auth_user_created';
-- ============================================================================
