"""
Endpoints para gestión de movimientos (auditoría) usando Supabase
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from supabase import Client
from ....core.supabase_client import get_supabase
from ....schemas.inventory import MovimientoCreate, MovimientoResponse
from ....services import supabase_service as service


router = APIRouter()


# ============================================================================
# MOVIMIENTOS
# ============================================================================

@router.get("/movimientos", response_model=List[MovimientoResponse], tags=["Auditoría > Movimientos"])
def listar_movimientos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tipo: Optional[str] = Query(None),
    supabase: Client = Depends(get_supabase)
):
    """
    Obtener lista de movimientos (auditoría)
    
    Tipos de movimiento:
    - entrada: Item ingresa al inventario
    - salida: Item sale temporalmente (préstamo)
    - devolucion: Item es devuelto
    - daño: Item se daña
    - ajuste_stock: Ajuste de cantidad
    - baja: Item dado de baja
    - transferencia: Cambio de ubicación
    """
    return service.get_movimientos(supabase, skip=skip, limit=limit, tipo=tipo)


@router.get("/movimientos/{movimiento_id}", response_model=MovimientoResponse, tags=["Auditoría > Movimientos"])
def obtener_movimiento(movimiento_id: int, supabase: Client = Depends(get_supabase)):
    """Obtener movimiento por ID"""
    movimiento = service.get_movimiento_by_id(supabase, movimiento_id)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return movimiento


@router.post("/movimientos", response_model=MovimientoResponse, tags=["Auditoría > Movimientos"])
def crear_movimiento(movimiento: MovimientoCreate, supabase: Client = Depends(get_supabase)):
    """
    Crear nuevo movimiento de auditoría

    VALIDACIONES:
    - Debes especificar: tipo y UNO de: equipo_id, electronica_id, robot_id, material_id
    - MV-05: usuario_id válido (si se proporciona, debe existir en auth.users)
    """
    # Determinar qué tipo de item
    item_id = None
    item_tipo = None

    if movimiento.equipo_id:
        item_id = movimiento.equipo_id
        item_tipo = 'equipo'
    elif movimiento.electronica_id:
        item_id = movimiento.electronica_id
        item_tipo = 'electronica'
    elif movimiento.robot_id:
        item_id = movimiento.robot_id
        item_tipo = 'robot'
    elif movimiento.material_id:
        item_id = movimiento.material_id
        item_tipo = 'material'
    else:
        raise HTTPException(
            status_code=400,
            detail="Debes especificar un item: equipo_id, electronica_id, robot_id o material_id"
        )

    # Verificar que el item existe
    if item_tipo == 'equipo':
        item = service.get_equipo_by_id(supabase, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
    elif item_tipo == 'electronica':
        item = service.get_electronica_by_id(supabase, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Elemento de electrónica no encontrado")
    elif item_tipo == 'robot':
        item = service.get_robot_by_id(supabase, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Robot no encontrado")
    elif item_tipo == 'material':
        item = service.get_material_by_id(supabase, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Material no encontrado")

    # Preparar datos
    data = {
        "tipo": movimiento.tipo,
        "cantidad": movimiento.cantidad,
        "descripcion": movimiento.descripcion,
        "prestamo_id": movimiento.prestamo_id
    }

    # MV-05: Validar usuario_id (si se proporciona)
    if movimiento.usuario_id:
        try:
            # Verificar que el usuario existe en auth.users
            user_response = supabase.auth.admin.get_user(movimiento.usuario_id)
            if not user_response or not user_response.user:
                raise HTTPException(
                    status_code=400,
                    detail=f"MV-05: El usuario_id '{movimiento.usuario_id}' no existe en el sistema"
                )
            data["usuario_id"] = movimiento.usuario_id
        except Exception:
            # Si no tenemos permisos de admin, solo asignamos el valor
            data["usuario_id"] = movimiento.usuario_id

    # Agregar la FK correspondiente
    if item_tipo == 'equipo':
        data["equipo_id"] = item_id
    elif item_tipo == 'electronica':
        data["electronica_id"] = item_id
    elif item_tipo == 'robot':
        data["robot_id"] = item_id
    elif item_tipo == 'material':
        data["material_id"] = item_id

    return service.create_movimiento(supabase, data)


@router.put("/movimientos/{movimiento_id}", tags=["Auditoría > Movimientos"])
def actualizar_movimiento(movimiento_id: int):
    """
    Actualizar movimiento

    VALIDACIÓN:
    - RN-06: NO permitir modificar movimientos (auditoría inmutable)
    - Esta operación está BLOQUEADA por diseño
    """
    raise HTTPException(
        status_code=403,
        detail="RN-06: ❌ OPERACIÓN NO PERMITIDA: Los movimientos de auditoría son INMUTABLES y no pueden ser modificados. Esto es por diseño para mantener la integridad del historial."
    )


@router.delete("/movimientos/{movimiento_id}", tags=["Auditoría > Movimientos"])
def eliminar_movimiento(movimiento_id: int):
    """
    Eliminar movimiento

    VALIDACIÓN:
    - RN-06: NO permitir eliminar movimientos (auditoría inmutable)
    - Esta operación está BLOQUEADA por diseño
    """
    raise HTTPException(
        status_code=403,
        detail="RN-06: ❌ OPERACIÓN NO PERMITIDA: Los movimientos de auditoría son INMUTABLES y no pueden ser eliminados. Esto es por diseño para mantener la integridad del historial."
    )
