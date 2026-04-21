"""
Endpoints para gestión de movimientos (auditoría) usando Supabase
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from supabase import Client
from ....core.supabase_client import get_supabase
from ....core.auth import require_inventory
from ....schemas.auth import PerfilResponse
from ....schemas.inventory import MovimientoResponse, MovimientoCreate
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
def obtener_movimiento(
    movimiento_id: int,
    supabase: Client = Depends(get_supabase)
):
    """Obtener movimiento por ID"""
    movimiento = service.get_movimiento_by_id(supabase, movimiento_id)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return movimiento


@router.post("/movimientos", response_model=MovimientoResponse, tags=["Auditoría > Movimientos"])
def crear_movimiento(movimiento: MovimientoCreate):
    """
    Crear nuevo movimiento de auditoría - NO PERMITIDO

    Los movimientos son creados automáticamente por el sistema (triggers).
    Esta función está deshabilitada para mantener la integridad del historial.
    """
    raise HTTPException(
        status_code=403,
        detail="Los movimientos son creados automáticamente por el sistema. No puedes crear movimientos manualmente."
    )


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
