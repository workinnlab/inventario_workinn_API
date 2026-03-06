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
    
    Debes especificar UNO de estos campos:
    - equipo_id
    - electronica_id
    - robot_id
    - material_id
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
    
    # Verificar que el prestatario existe
    prestatario = service.get_prestatario_by_id(supabase, prestamo.prestatario_id)
    if not prestatario:
        raise HTTPException(status_code=404, detail="Prestatario no encontrado")
    
    # Preparar datos para insertar
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
        prestamo = service.get_prestamo_by_id(supabase, prestamo_id)
        if not prestamo:
            raise HTTPException(status_code=404, detail="Préstamo no encontrado")

        # Los datos de Supabase son dicts, no objetos Pydantic
        if prestamo['estado'] != 'activo':
            raise HTTPException(status_code=400, detail="El préstamo no está activo")

        # Usar formato de fecha compatible con PostgreSQL
        from datetime import datetime, timezone
        fecha_devolucion = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

        return service.update_prestamo(
            supabase,
            prestamo_id,
            {
                "estado": "devuelto",
                "fecha_devolucion": fecha_devolucion
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al devolver: {str(e)}")


@router.delete("/prestamos/{prestamo_id}", tags=["Préstamos > Gestión"])
def eliminar_prestamo(prestamo_id: int, supabase: Client = Depends(get_supabase)):
    """Eliminar préstamo"""
    if not service.delete_prestamo(supabase, prestamo_id):
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return {"message": "Préstamo eliminado correctamente"}
