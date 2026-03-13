"""
Endpoints para gestión de préstamos y prestatarios usando Supabase
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from supabase import Client
from ....core.supabase_client import get_supabase
from ....schemas.inventory import (
    PrestatarioCreate, PrestatarioResponse, PrestatarioUpdate,
    PrestamoCreate, PrestamoResponse, PrestamoUpdate
)
from ....services import supabase_service as service


router = APIRouter()


# ============================================================================
# PRESTATARIOS
# ============================================================================

@router.get("/prestatarios", response_model=List[PrestatarioResponse], tags=["Préstamos > Prestatarios"])
def listar_prestatarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    activo: Optional[bool] = Query(True),
    supabase: Client = Depends(get_supabase)
):
    """Obtener lista de prestatarios"""
    return service.get_prestatarios(supabase, skip=skip, limit=limit, activo=activo)


@router.get("/prestatarios/{prestatario_id}", response_model=PrestatarioResponse, tags=["Préstamos > Prestatarios"])
def obtener_prestatario(prestatario_id: int, supabase: Client = Depends(get_supabase)):
    """Obtener prestatario por ID"""
    prestatario = service.get_prestatario_by_id(supabase, prestatario_id)
    if not prestatario:
        raise HTTPException(status_code=404, detail="Prestatario no encontrado")
    return prestatario


@router.post("/prestatarios", response_model=PrestatarioResponse, tags=["Préstamos > Prestatarios"])
def crear_prestatario(prestatario: PrestatarioCreate, supabase: Client = Depends(get_supabase)):
    """Crear nuevo prestatario"""
    return service.create_prestatario(
        supabase,
        {
            "nombre": prestatario.nombre,
            "dependencia": prestatario.dependencia,
            "telefono": prestatario.telefono,
            "cedula": prestatario.cedula,
            "email": prestatario.email
        }
    )


@router.put("/prestatarios/{prestatario_id}", response_model=PrestatarioResponse, tags=["Préstamos > Prestatarios"])
def actualizar_prestatario(prestatario_id: int, prestatario: PrestatarioUpdate, supabase: Client = Depends(get_supabase)):
    """Actualizar prestatario"""
    updated = service.update_prestatario(
        supabase,
        prestatario_id,
        prestatario.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Prestatario no encontrado")
    return updated


@router.delete("/prestatarios/{prestatario_id}", tags=["Préstamos > Prestatarios"])
def eliminar_prestatario(prestatario_id: int, supabase: Client = Depends(get_supabase)):
    """Eliminar prestatario (lógico: marca como inactivo)"""
    updated = service.update_prestatario(supabase, prestatario_id, {"activo": False})
    if not updated:
        raise HTTPException(status_code=404, detail="Prestatario no encontrado")
    return {"message": "Prestatario marcado como inactivo"}


# ============================================================================
# PRÉSTAMOS
# ============================================================================

@router.get("/prestamos", response_model=List[PrestamoResponse], tags=["Préstamos > Gestión"])
def listar_prestamos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    estado: Optional[str] = Query(None),
    supabase: Client = Depends(get_supabase)
):
    """Obtener lista de préstamos"""
    return service.get_prestamos(supabase, skip=skip, limit=limit, estado=estado)


@router.get("/prestamos/activos", response_model=List[PrestamoResponse], tags=["Préstamos > Gestión"])
def listar_prestamos_activos(supabase: Client = Depends(get_supabase)):
    """Obtener préstamos activos"""
    return service.get_prestamos_activos(supabase)


@router.get("/prestamos/{prestamo_id}", response_model=PrestamoResponse, tags=["Préstamos > Gestión"])
def obtener_prestamo(prestamo_id: int, supabase: Client = Depends(get_supabase)):
    """Obtener préstamo por ID"""
    prestamo = service.get_prestamo_by_id(supabase, prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo


@router.post("/prestamos", response_model=PrestamoResponse, tags=["Préstamos > Gestión"])
def crear_prestamo(prestamo: PrestamoCreate, supabase: Client = Depends(get_supabase)):
    """
    Crear nuevo préstamo

    VALIDACIONES:
    1. Verifica que el elemento NO esté ya prestado
    2. Verifica que el elemento NO esté dañado o en mantenimiento
    3. Verifica que el prestatario exista y esté activo
    """
    # Determinar qué tipo de item se está prestando
    item_id = None
    item_tipo = None

    if prestamo.equipo_id:
        item_id = prestamo.equipo_id
        item_tipo = 'equipo'
    elif prestamo.electronica_id:
        item_id = prestamo.electronica_id
        item_tipo = 'electronica'
    elif prestamo.robot_id:
        item_id = prestamo.robot_id
        item_tipo = 'robot'
    elif prestamo.material_id:
        item_id = prestamo.material_id
        item_tipo = 'material'
    else:
        raise HTTPException(
            status_code=400,
            detail="Debes especificar un item: equipo_id, electronica_id, robot_id o material_id"
        )

    # ========================================================================
    # VALIDACIÓN 1: Verificar que el elemento NO esté ya prestado
    # ========================================================================
    prestamos_activos = supabase.table("prestamos").select("*").eq("estado", "activo").execute()

    for p in prestamos_activos.data:
        if item_tipo == 'equipo' and p.get('equipo_id') == item_id:
            raise HTTPException(
                status_code=400,
                detail=f"El equipo con ID {item_id} YA ESTÁ PRESTADO. No se puede crear otro préstamo activo."
            )
        elif item_tipo == 'electronica' and p.get('electronica_id') == item_id:
            raise HTTPException(
                status_code=400,
                detail=f"El elemento de electrónica con ID {item_id} YA ESTÁ PRESTADO."
            )
        elif item_tipo == 'robot' and p.get('robot_id') == item_id:
            raise HTTPException(
                status_code=400,
                detail=f"El robot con ID {item_id} YA ESTÁ PRESTADO."
            )
        elif item_tipo == 'material' and p.get('material_id') == item_id:
            raise HTTPException(
                status_code=400,
                detail=f"El material con ID {item_id} YA ESTÁ PRESTADO."
            )

    # ========================================================================
    # VALIDACIÓN 2: Verificar estado del elemento (si es equipo)
    # ========================================================================
    if item_tipo == 'equipo':
        equipo = service.get_equipo_by_id(supabase, item_id)
        if not equipo:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")

        estado_equipo = equipo.get('estado', '')

        if estado_equipo == 'dañado':
            raise HTTPException(
                status_code=400,
                detail=f"El equipo con ID {item_id} está DAÑADO. No se puede prestar."
            )

        if estado_equipo == 'mantenimiento':
            raise HTTPException(
                status_code=400,
                detail=f"El equipo con ID {item_id} está en MANTENIMIENTO. No se puede prestar."
            )

    # ========================================================================
    # VALIDACIÓN 3: Verificar que el prestatario exista y esté activo
    # ========================================================================
    prestatario = service.get_prestatario_by_id(supabase, prestamo.prestatario_id)
    if not prestatario:
        raise HTTPException(status_code=404, detail="Prestatario no encontrado")

    if not prestatario.get('activo', False):
        raise HTTPException(
            status_code=400,
            detail=f"El prestatario con ID {prestamo.prestatario_id} está INACTIVO."
        )

    # ========================================================================
    # Crear préstamo (todas las validaciones pasaron)
    # ========================================================================
    data = {
        "prestatario_id": prestamo.prestatario_id,
        "estado": "activo",
        "observaciones": prestamo.observaciones
    }

    if prestamo.fecha_limite:
        data["fecha_limite"] = prestamo.fecha_limite.isoformat()

    # Agregar la FK correspondiente
    if item_tipo == 'equipo':
        data["equipo_id"] = item_id
    elif item_tipo == 'electronica':
        data["electronica_id"] = item_id
    elif item_tipo == 'robot':
        data["robot_id"] = item_id
    elif item_tipo == 'material':
        data["material_id"] = item_id

    return service.create_prestamo(supabase, data)


@router.put("/prestamos/{prestamo_id}", response_model=PrestamoResponse, tags=["Préstamos > Gestión"])
def actualizar_prestamo(prestamo_id: int, prestamo: PrestamoUpdate, supabase: Client = Depends(get_supabase)):
    """Actualizar préstamo (ej: marcar como devuelto)"""
    updated = service.update_prestamo(
        supabase,
        prestamo_id,
        prestamo.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return updated


@router.post("/prestamos/{prestamo_id}/devolver", response_model=PrestamoResponse, tags=["Préstamos > Gestión"])
def devolver_prestamo(prestamo_id: int, supabase: Client = Depends(get_supabase)):
    """Marcar préstamo como devuelto"""
    try:
        # Obtener préstamo
        print(f"🔍 Buscando préstamo ID={prestamo_id}")
        prestamo = service.get_prestamo_by_id(supabase, prestamo_id)
        print(f"📦 Préstamo encontrado: {prestamo}")

        if not prestamo:
            print(f"❌ Préstamo ID={prestamo_id} no encontrado")
            raise HTTPException(status_code=404, detail="Préstamo no encontrado")

        # Verificar estado (los datos de Supabase son dicts)
        estado_actual = prestamo.get('estado', '')
        print(f"📊 Estado actual: {estado_actual}")

        if estado_actual != 'activo':
            raise HTTPException(status_code=400, detail=f"El préstamo no está activo (estado: {estado_actual})")

        # Usar formato de fecha compatible con PostgreSQL
        from datetime import datetime, timezone
        fecha_devolucion = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        print(f"📅 Fecha devolución: {fecha_devolucion}")

        # Actualizar préstamo
        print(f"🔄 Actualizando préstamo ID={prestamo_id}...")
        updated = service.update_prestamo(
            supabase,
            prestamo_id,
            {
                "estado": "devuelto",
                "fecha_devolucion": fecha_devolucion
            }
        )
        print(f"✅ Resultado actualización: {updated}")

        if not updated:
            raise HTTPException(status_code=404, detail="No se pudo actualizar el préstamo")

        return updated

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Error al devolver: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ ERROR EN DEVOLVER: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.delete("/prestamos/{prestamo_id}", tags=["Préstamos > Gestión"])
def eliminar_prestamo(prestamo_id: int, supabase: Client = Depends(get_supabase)):
    """Eliminar préstamo"""
    if not service.delete_prestamo(supabase, prestamo_id):
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return {"message": "Préstamo eliminado correctamente"}
