-- ============================================================================
-- FIX: Agregar estado 'arreglado' a equipos
-- ============================================================================
-- Ejecutar en: Supabase Dashboard > SQL Editor
-- ============================================================================

-- 1. Actualizar el check constraint de la tabla equipos
ALTER TABLE equipos DROP CONSTRAINT IF EXISTS equipos_estado_check;

ALTER TABLE equipos ADD CONSTRAINT equipos_estado_check 
CHECK (estado IN ('disponible', 'en uso', 'prestado', 'mantenimiento', 'dañado', 'arreglado'));

-- 2. Actualizar equipos que estaban 'dañado' y ya fueron arreglados
-- (Opcional - el admin puede hacerlo manualmente)
-- UPDATE equipos SET estado = 'arreglado' WHERE estado = 'dañado' AND ...;

-- 3. Verificar que se actualizó
-- SELECT DISTINCT estado FROM equipos;

-- ============================================================================
