-- ============================================================================
-- CONFIGURACIÓN DE ALERTAS - Inventario CIE
-- ============================================================================
-- Ejecutar en: Supabase Dashboard > SQL Editor
-- ============================================================================

-- 1. Tabla de configuración de alertas
create table if not exists configuracion_alertas (
  id bigint primary key generated always as identity,
  clave text unique not null,
  valor int not null,
  descripcion text,
  updated_at timestamptz default now()
);

-- 2. Valores por defecto
insert into configuracion_alertas (clave, valor, descripcion) values
  ('stock_minimo_default', 5, 'Stock mínimo por defecto para materiales'),
  ('prestamo_por_vencer_dias', 7, 'Días para alerta de préstamo por vencer'),
  ('prestamo_limite_dias', 30, 'Límite de días para préstamo'),
  ('prestamos_maximos_por_usuario', 5, 'Máximo préstamos activos por usuario'),
  ('alertar_stock_bajo', 1, 'Activar/desactivar alertas de stock bajo (1=si, 0=no)'),
  ('alertar_prestamos_vencidos', 1, 'Activar/desactivar alertas de préstamos vencidos'),
  ('alertar_equipos_danados', 1, 'Activar/desactivar alertas de equipos dañados')
on conflict (clave) do nothing;

-- 3. Habilitar RLS
alter table configuracion_alertas enable row level security;

-- 4. Políticas RLS
-- Todos los autenticados pueden leer
create policy "configuracion_select" on configuracion_alertas
  for select
  to authenticated
  using (true);

-- Solo admin puede actualizar
create policy "configuracion_update" on configuracion_alertas
  for update
  to authenticated
  using (
    exists (
      select 1 from perfiles p
      where p.id = auth.uid() and p.rol = 'admin'
    )
  );

-- 5. Función para obtener configuración
create or replace function get_configuracion(clave_busqueda text)
returns int as $$
declare
  valor_resultado int;
begin
  select valor into valor_resultado
  from configuracion_alertas
  where clave = clave_busqueda;
  
  return coalesce(valor_resultado, 0);
end;
$$ language plpgsql security definer;

-- 6. Índices
create index idx_configuracion_clave on configuracion_alertas(clave);

-- ============================================================================
-- EJEMPLOS DE USO
-- ============================================================================

-- Obtener configuración
-- select * from configuracion_alertas;

-- Actualizar stock mínimo
-- update configuracion_alertas set valor = 10 where clave = 'stock_minimo_default';

-- Usar en endpoint
-- select get_configuracion('stock_minimo_default');

-- ============================================================================
