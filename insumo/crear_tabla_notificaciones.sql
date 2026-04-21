-- ============================================================================
-- TABLA: notificaciones
-- ============================================================================
-- Sistema de notificaciones para admin e inventory
-- ============================================================================

create table if not exists notificaciones (
    id bigint primary key generated always as identity,
    tipo text not null,
    titulo text not null,
    mensaje text not null,
    leida boolean default false,
    url text,
    data jsonb,
    created_at timestamptz default now()
);

comment on table notificaciones is 'Sistema de notificaciones para admin e inventory';

comment on column notificaciones.tipo is 'Tipo: prestamo_creado, prestamo_vencer, prestamo_vencido, devolucion, stock_bajo';
comment on column notificaciones.titulo is 'Título corto de la notificación';
comment on column notificaciones.mensaje is 'Mensaje descriptivo';
comment on column notificaciones.leida is 'Si la notificación ha sido leída';
comment on column notificaciones.url is 'URL para navegar al hacer click';
comment on column notificaciones.data is 'Datos adicionales en formato JSON';