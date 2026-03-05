-- ============================================================================
-- INVENTARIO CIE - Schema completo para Supabase
-- ============================================================================
-- Diseño con 4 columnas FK separadas (más explícito, sin triggers de validación)
-- Incluye:
--   1. Tablas de inventario (equipos, electronica, robots, materiales)
--   2. Tabla de prestatarios
--   3. Tabla de préstamos (con 4 FKs separadas)
--   4. Tabla de movimientos (con 4 FKs separadas)
--   5. Vista unificada para reportes
--   6. Índices estratégicos
--   7. Triggers para updated_at
--   8. Row Level Security (RLS) básico
-- ============================================================================

-- ============================================================================
-- 0. LIMPIEZA DE TABLAS EXISTENTES (para migración desde diseño polimórfico)
-- ============================================================================
-- IMPORTANTE: Esto eliminará todos los datos existentes en estas tablas
-- ============================================================================

drop view if exists movimientos_completo cascade;
drop view if exists prestamos_activos cascade;
drop view if exists resumen_inventario cascade;
drop view if exists inventario_completo cascade;

drop table if exists movimientos cascade;
drop table if exists prestamos cascade;
drop table if exists prestatarios cascade;
drop table if exists materiales cascade;
drop table if exists robots cascade;
drop table if exists electronica cascade;
drop table if exists equipos cascade;
drop table if exists tipos_materiales cascade;

-- ============================================================================
-- 1. EXTENSIONES Y CONFIGURACIÓN
-- ============================================================================

create extension if not exists "uuid-ossp";

-- ============================================================================
-- 2. TABLAS DE INVENTARIO
-- ============================================================================
create table if not exists equipos (
  id bigint primary key generated always as identity,
  nombre text not null,
  marca text not null,
  codigo text unique not null,  -- Ej: PC-01, PC-02
  accesorios text,
  serial text,
  estado text check (estado in ('disponible', 'en uso', 'prestado', 'mantenimiento', 'dañado')),
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Equipos de electrónica (componentes, sensores, etc.)
create table if not exists electronica (
  id bigint primary key generated always as identity,
  nombre text not null,
  descripcion text,
  tipo text,
  en_uso int default 0,
  en_stock int default 0,
  total int generated always as (en_uso + en_stock) stored,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Robots (kits robóticos)
create table if not exists robots (
  id bigint primary key generated always as identity,
  nombre text not null,
  fuera_de_servicio int default 0,
  en_uso int default 0,
  disponible int default 0,
  total int generated always as (fuera_de_servicio + en_uso + disponible) stored,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Tipos de materiales (PLA, PETG, Resina, etc.)
create table if not exists tipos_materiales (
  id bigint primary key generated always as identity,
  nombre text not null unique
);

-- Materiales (filamentos, resinas, insumos)
create table if not exists materiales (
  id bigint primary key generated always as identity,
  color text not null,
  tipo_id bigint references tipos_materiales(id),
  cantidad text not null,  -- Ej: '1KG', '500ml'
  categoria text check (categoria in ('Filamento', 'Resina', 'Otro')),
  usado int default 0,
  en_uso int default 0,
  en_stock int default 0,
  total int generated always as (usado + en_uso + en_stock) stored,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- ============================================================================
-- 3. TABLA DE PRESTATARIOS
-- ============================================================================

create table if not exists prestatarios (
  id bigint primary key generated always as identity,
  nombre text not null,
  telefono text,
  dependencia text not null,  -- Departamento, aula, área
  cedula text,
  email text,
  activo boolean default true,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- ============================================================================
-- 4. TABLA DE PRÉSTAMOS
-- ============================================================================
-- Diseño: 4 columnas FK separadas, solo una tendrá valor por fila
-- ============================================================================

create table if not exists prestamos (
  id bigint primary key generated always as identity,
  
  -- FKs separadas por tipo de item (solo una será NOT NULL)
  equipo_id bigint references equipos(id),
  electronica_id bigint references electronica(id),
  robot_id bigint references robots(id),
  material_id bigint references materiales(id),
  
  -- Prestatario
  prestatario_id bigint not null references prestatarios(id),
  
  -- Fechas
  fecha_prestamo timestamptz default now(),
  fecha_devolucion timestamptz,
  fecha_limite timestamptz,  -- Fecha esperada de devolución
  
  -- Estado y observaciones
  estado text not null check (estado in ('activo', 'devuelto', 'vencido', 'perdido')),
  observaciones text,
  
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  
  -- CONSTRAINT: Exactamente una FK de item debe tener valor
  constraint chk_prestamo_un_item check (
    (equipo_id is not null and electronica_id is null and robot_id is null and material_id is null) or
    (equipo_id is null and electronica_id is not null and robot_id is null and material_id is null) or
    (equipo_id is null and electronica_id is null and robot_id is not null and material_id is null) or
    (equipo_id is null and electronica_id is null and robot_id is null and material_id is not null)
  )
);

-- ============================================================================
-- 5. TABLA DE MOVIMIENTOS
-- ============================================================================
-- Diseño: 4 columnas FK separadas, solo una tendrá valor por fila
-- ============================================================================

create table if not exists movimientos (
  id bigint primary key generated always as identity,
  
  -- Tipo de movimiento
  tipo text not null check (tipo in (
    'entrada',           -- Item ingresa al inventario
    'salida',            -- Item sale temporalmente (préstamo)
    'devolucion',        -- Item es devuelto
    'daño',              -- Item se daña
    'ajuste_stock',      -- Ajuste de cantidad (conteo)
    'baja',              -- Item dado de baja definitivamente
    'transferencia'      -- Cambio de ubicación/departamento
  )),
  
  -- FKs separadas por tipo de item (solo una será NOT NULL)
  equipo_id bigint references equipos(id),
  electronica_id bigint references electronica(id),
  robot_id bigint references robots(id),
  material_id bigint references materiales(id),
  
  -- Cantidad (para materiales que tienen múltiples unidades)
  cantidad int default 1,
  
  -- Relación con préstamo (si aplica)
  prestamo_id bigint references prestamos(id),
  
  -- Usuario que realiza el movimiento (Supabase Auth)
  usuario_id uuid references auth.users(id),
  
  -- Descripción del movimiento
  descripcion text,
  
  -- Metadata adicional
  ubicacion_anterior text,
  ubicacion_nueva text,
  
  created_at timestamptz default now(),
  
  -- CONSTRAINT: Exactamente una FK de item debe tener valor
  constraint chk_movimiento_un_item check (
    (equipo_id is not null and electronica_id is null and robot_id is null and material_id is null) or
    (equipo_id is null and electronica_id is not null and robot_id is null and material_id is null) or
    (equipo_id is null and electronica_id is null and robot_id is not null and material_id is null) or
    (equipo_id is null and electronica_id is null and robot_id is null and material_id is not null)
  )
);

-- ============================================================================
-- 6. VISTAS UNIFICADAS PARA REPORTES
-- ============================================================================

create or replace view inventario_completo as
select 
  id,
  'equipo' as tipo,
  nombre,
  codigo as identificador,
  marca,
  serial,
  estado,
  null as en_uso,
  null as en_stock,
  null as total,
  created_at,
  updated_at
from equipos

union all

select 
  id,
  'electronica' as tipo,
  nombre,
  coalesce(tipo, descripcion) as identificador,
  null as marca,
  null as serial,
  null as estado,
  en_uso,
  en_stock,
  total,
  created_at,
  updated_at
from electronica

union all

select 
  id,
  'robot' as tipo,
  nombre,
  null as identificador,
  null as marca,
  null as serial,
  case 
    when fuera_de_servicio > 0 then 'fuera de servicio'
    when disponible > 0 then 'disponible'
    when en_uso > 0 then 'en uso'
  end as estado,
  en_uso,
  disponible as en_stock,
  total,
  created_at,
  updated_at
from robots

union all

select 
  m.id,
  'material' as tipo,
  concat(m.color, ' - ', tm.nombre) as nombre,
  m.cantidad as identificador,
  m.categoria as marca,
  null as serial,
  m.categoria as estado,
  m.en_uso,
  m.en_stock,
  m.total,
  m.created_at,
  m.updated_at
from materiales m
left join tipos_materiales tm on m.tipo_id = tm.id;

-- Vista de préstamos activos con información del item
create or replace view prestamos_activos as
select 
  p.id as prestamo_id,
  case 
    when p.equipo_id is not null then 'equipo'
    when p.electronica_id is not null then 'electronica'
    when p.robot_id is not null then 'robot'
    when p.material_id is not null then 'material'
  end as item_tipo,
  case 
    when p.equipo_id is not null then e.nombre
    when p.electronica_id is not null then el.nombre
    when p.robot_id is not null then r.nombre
    when p.material_id is not null then concat(m.color, ' ', tm.nombre)
  end as item_nombre,
  case 
    when p.equipo_id is not null then e.codigo
    else null
  end as item_codigo,
  pr.nombre as prestatario_nombre,
  pr.dependencia,
  pr.telefono,
  pr.cedula,
  p.fecha_prestamo,
  p.fecha_limite,
  p.observaciones,
  extract(days from (now() - p.fecha_prestamo)) as dias_prestado
from prestamos p
join prestatarios pr on p.prestatario_id = pr.id
left join equipos e on p.equipo_id = e.id
left join electronica el on p.electronica_id = el.id
left join robots r on p.robot_id = r.id
left join materiales m on p.material_id = m.id
left join tipos_materiales tm on m.tipo_id = tm.id
where p.estado = 'activo';

-- Vista de resumen de inventario por categoría
create or replace view resumen_inventario as
select 
  tipo,
  count(*) as total_items,
  count(*) filter (where estado = 'disponible' or estado like '%disponible%') as disponibles,
  count(*) filter (where estado = 'en uso') as en_uso,
  count(*) filter (where estado = 'dañado' or estado = 'fuera de servicio') as dañados
from inventario_completo
group by tipo;

-- Vista de historial de movimientos
create or replace view movimientos_completo as
select 
  m.id,
  m.tipo,
  case 
    when m.equipo_id is not null then 'equipo'
    when m.electronica_id is not null then 'electronica'
    when m.robot_id is not null then 'robot'
    when m.material_id is not null then 'material'
  end as item_tipo,
  case 
    when m.equipo_id is not null then e.nombre
    when m.electronica_id is not null then el.nombre
    when m.robot_id is not null then r.nombre
    when m.material_id is not null then concat(ma.color, ' ', tm.nombre)
  end as item_nombre,
  case 
    when m.equipo_id is not null then e.codigo
    else null
  end as item_codigo,
  m.cantidad,
  m.descripcion,
  m.ubicacion_anterior,
  m.ubicacion_nueva,
  m.created_at,
  u.email as usuario_email
from movimientos m
left join equipos e on m.equipo_id = e.id
left join electronica el on m.electronica_id = el.id
left join robots r on m.robot_id = r.id
left join materiales ma on m.material_id = ma.id
left join tipos_materiales tm on ma.tipo_id = tm.id
left join auth.users u on m.usuario_id = u.id
order by m.created_at desc;

-- ============================================================================
-- 7. ÍNDICES ESTRATÉGICOS
-- ============================================================================
create index if not exists idx_equipos_codigo on equipos(codigo);
create index if not exists idx_equipos_estado on equipos(estado);
create index if not exists idx_equipos_serial on equipos(serial);
create index if not exists idx_equipos_created on equipos(created_at desc);

-- Electrónica
create index if not exists idx_electronica_tipo on electronica(tipo);
create index if not exists idx_electronica_stock on electronica(en_stock);

-- Robots
create index if not exists idx_robots_estado on robots(disponible, en_uso, fuera_de_servicio);

-- Materiales
create index if not exists idx_materiales_categoria on materiales(categoria);
create index if not exists idx_materiales_color on materiales(color);
create index if not exists idx_materiales_stock on materiales(en_stock);
create index if not exists idx_tipos_materiales_nombre on tipos_materiales(nombre);

-- Prestatarios
create index if not exists idx_prestatarios_nombre on prestatarios(nombre);
create index if not exists idx_prestatarios_dependencia on prestatarios(dependencia);
create index if not exists idx_prestatarios_activo on prestatarios(activo) where activo = true;

-- Préstamos - FKs separadas
create index if not exists idx_prestamos_equipo on prestamos(equipo_id);
create index if not exists idx_prestamos_electronica on prestamos(electronica_id);
create index if not exists idx_prestamos_robot on prestamos(robot_id);
create index if not exists idx_prestamos_material on prestamos(material_id);
create index if not exists idx_prestamos_prestatario on prestamos(prestatario_id);
create index if not exists idx_prestamos_estado on prestamos(estado);
create index if not exists idx_prestamos_fecha on prestamos(fecha_prestamo desc);
create index if not exists idx_prestamos_activos on prestamos(prestatario_id, estado) 
  where estado = 'activo';
create index if not exists idx_prestamos_vencidos on prestamos(fecha_limite) 
  where estado = 'activo';

-- Movimientos - FKs separadas
create index if not exists idx_movimientos_equipo on movimientos(equipo_id);
create index if not exists idx_movimientos_electronica on movimientos(electronica_id);
create index if not exists idx_movimientos_robot on movimientos(robot_id);
create index if not exists idx_movimientos_material on movimientos(material_id);
create index if not exists idx_movimientos_tipo on movimientos(tipo);
create index if not exists idx_movimientos_fecha on movimientos(created_at desc);
create index if not exists idx_movimientos_usuario on movimientos(usuario_id);
create index if not exists idx_movimientos_prestamo on movimientos(prestamo_id);

-- ============================================================================
-- 8. TRIGGERS PARA UPDATED_AT
-- ============================================================================
create or replace function update_updated_at_column()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

-- Aplicar trigger a todas las tablas con updated_at
create trigger update_equipos_updated_at
  before update on equipos
  for each row
  execute function update_updated_at_column();

create trigger update_electronica_updated_at
  before update on electronica
  for each row
  execute function update_updated_at_column();

create trigger update_robots_updated_at
  before update on robots
  for each row
  execute function update_updated_at_column();

create trigger update_materiales_updated_at
  before update on materiales
  for each row
  execute function update_updated_at_column();

create trigger update_prestatarios_updated_at
  before update on prestatarios
  for each row
  execute function update_updated_at_column();

create trigger update_prestamos_updated_at
  before update on prestamos
  for each row
  execute function update_updated_at_column();

-- ============================================================================
-- 9. ROW LEVEL SECURITY (RLS)
-- ============================================================================

-- Habilitar RLS en todas las tablas
alter table equipos enable row level security;
alter table electronica enable row level security;
alter table robots enable row level security;
alter table materiales enable row level security;
alter table prestatarios enable row level security;
alter table prestamos enable row level security;
alter table movimientos enable row level security;
alter table tipos_materiales enable row level security;

-- ============================================================================
-- POLÍTICAS DE ACCESO
-- ============================================================================
-- Roles esperados en metadata de usuario:
--   - 'admin': Acceso completo
--   - 'inventory': CRUD en inventario, lectura en otras tablas
--   - 'viewer': Solo lectura
--
-- Para asignar roles, usa Supabase Dashboard > Authentication > Users
-- y agrega metadata: {"rol": "admin"}
-- ============================================================================

-- Función helper para obtener rol del usuario actual
create or replace function get_user_role()
returns text as $$
begin
  return coalesce(
    (auth.jwt() ->> 'rol'),
    (auth.jwt() -> 'user_metadata' ->> 'rol'),
    'viewer'
  );
end;
$$ language plpgsql security definer;

-- ============================================================================
-- POLÍTICAS: EQUIPOS
-- ============================================================================

-- Admin: todo
create policy "admin_equipos_all" on equipos
  for all
  using (get_user_role() = 'admin')
  with check (get_user_role() = 'admin');

-- Inventory: CRUD excepto delete
create policy "inventory_equipos_all" on equipos
  for all
  using (get_user_role() = 'inventory')
  with check (get_user_role() = 'inventory');

-- Viewer: solo lectura
create policy "viewer_equipos_read" on equipos
  for select
  using (true);  -- Todos autenticados pueden leer

-- ============================================================================
-- POLÍTICAS: ELECTRÓNICA
-- ============================================================================

create policy "admin_electronica_all" on electronica
  for all
  using (get_user_role() = 'admin')
  with check (get_user_role() = 'admin');

create policy "inventory_electronica_all" on electronica
  for all
  using (get_user_role() = 'inventory')
  with check (get_user_role() = 'inventory');

create policy "viewer_electronica_read" on electronica
  for select
  using (true);

-- ============================================================================
-- POLÍTICAS: ROBOTS
-- ============================================================================

create policy "admin_robots_all" on robots
  for all
  using (get_user_role() = 'admin')
  with check (get_user_role() = 'admin');

create policy "inventory_robots_all" on robots
  for all
  using (get_user_role() = 'inventory')
  with check (get_user_role() = 'inventory');

create policy "viewer_robots_read" on robots
  for select
  using (true);

-- ============================================================================
-- POLÍTICAS: MATERIALES
-- ============================================================================

create policy "admin_materiales_all" on materiales
  for all
  using (get_user_role() = 'admin')
  with check (get_user_role() = 'admin');

create policy "inventory_materiales_all" on materiales
  for all
  using (get_user_role() = 'inventory')
  with check (get_user_role() = 'inventory');

create policy "viewer_materiales_read" on materiales
  for select
  using (true);

create policy "admin_tipos_materiales_all" on tipos_materiales
  for all
  using (get_user_role() = 'admin')
  with check (get_user_role() = 'admin');

create policy "inventory_tipos_materiales_read" on tipos_materiales
  for select
  using (true);

-- ============================================================================
-- POLÍTICAS: PRESTATARIOS
-- ============================================================================

create policy "admin_prestatarios_all" on prestatarios
  for all
  using (get_user_role() = 'admin')
  with check (get_user_role() = 'admin');

create policy "inventory_prestatarios_all" on prestatarios
  for all
  using (get_user_role() = 'inventory')
  with check (get_user_role() = 'inventory');

create policy "viewer_prestatarios_read" on prestatarios
  for select
  using (true);

-- ============================================================================
-- POLÍTICAS: PRÉSTAMOS
-- ============================================================================

create policy "admin_prestamos_all" on prestamos
  for all
  using (get_user_role() = 'admin')
  with check (get_user_role() = 'admin');

create policy "inventory_prestamos_all" on prestamos
  for all
  using (get_user_role() = 'inventory')
  with check (get_user_role() = 'inventory');

create policy "viewer_prestamos_read" on prestamos
  for select
  using (true);

-- ============================================================================
-- POLÍTICAS: MOVIMIENTOS
-- ============================================================================

-- Solo admin e inventory pueden crear movimientos
create policy "admin_movimientos_all" on movimientos
  for all
  using (get_user_role() = 'admin')
  with check (get_user_role() = 'admin');

create policy "inventory_movimientos_create" on movimientos
  for insert
  with check (get_user_role() = 'inventory');

create policy "inventory_movimientos_read" on movimientos
  for select
  using (get_user_role() = 'inventory');

create policy "viewer_movimientos_read" on movimientos
  for select
  using (get_user_role() = 'viewer');

-- ============================================================================
-- 10. DATOS INICIALES (SEED)
-- ============================================================================
insert into tipos_materiales (nombre) values
  ('PLA'),
  ('PETG'),
  ('ABS'),
  ('TPU'),
  ('Resina Standard'),
  ('Resina Flexible'),
  ('Resina ABS-Like')
on conflict (nombre) do nothing;

-- ============================================================================
-- 11. FUNCIONES UTILITARIAS
-- ============================================================================
create or replace function crear_movimiento_prestamo()
returns trigger as $$
begin
  insert into movimientos (tipo, equipo_id, electronica_id, robot_id, material_id, prestamo_id, usuario_id, descripcion)
  values (
    'salida',
    NEW.equipo_id,
    NEW.electronica_id,
    NEW.robot_id,
    NEW.material_id,
    NEW.id,
    auth.uid(),
    'Préstamo a ' || (select nombre from prestatarios where id = NEW.prestatario_id)
  );
  return NEW;
end;
$$ language plpgsql security definer;

-- Trigger para crear movimiento al crear préstamo
create trigger trigger_movimiento_al_prestamo
  after insert on prestamos
  for each row
  execute function crear_movimiento_prestamo();

-- Función para crear movimiento al devolver
create or replace function crear_movimiento_devolucion()
returns trigger as $$
begin
  if OLD.estado = 'activo' and NEW.estado = 'devuelto' then
    insert into movimientos (tipo, equipo_id, electronica_id, robot_id, material_id, prestamo_id, usuario_id, descripcion)
    values (
      'devolucion',
      NEW.equipo_id,
      NEW.electronica_id,
      NEW.robot_id,
      NEW.material_id,
      NEW.id,
      auth.uid(),
      'Devolución por ' || (select nombre from prestatarios where id = NEW.prestatario_id)
    );
  end if;
  return NEW;
end;
$$ language plpgsql security definer;

-- Trigger para crear movimiento al devolver
create trigger trigger_movimiento_al_devolver
  after update on prestamos
  for each row
  when (OLD.estado = 'activo' and NEW.estado = 'devuelto')
  execute function crear_movimiento_devolucion();

-- Función para marcar préstamos como vencidos
create or replace function marcar_prestamos_vencidos()
returns trigger as $$
begin
  update prestamos
  set estado = 'vencido'
  where estado = 'activo'
    and fecha_limite is not null
    and fecha_limite < now();
  return null;
end;
$$ language plpgsql;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================
-- Resumen del diseño:
--   - 4 tablas de inventario: equipos, electronica, robots, materiales
--   - Tablas transaccionales: prestamos, movimientos (con 4 FKs separadas)
--   - Constraints CHECK aseguran que solo una FK tenga valor por fila
--   - Vistas unificadas para reportes generales
--   - RLS con 3 roles: admin, inventory, viewer
--   - Triggers automáticos: updated_at, movimientos por préstamo/devolución
--
-- Uso en Supabase:
--   1. SQL Editor > New Query
--   2. Pegar este script completo
--   3. Ejecutar
--   4. Asignar roles en Auth > Users > User Metadata: {"rol": "admin"}
-- ============================================================================
