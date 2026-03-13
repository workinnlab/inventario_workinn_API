"""
Endpoints para gestión de inventario usando Supabase
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from supabase import Client
from ....core.supabase_client import get_supabase
from ....schemas.inventory import (
    EquipoCreate, EquipoResponse, EquipoUpdate,
    ElectronicaCreate, ElectronicaResponse, ElectronicaUpdate,
    RobotCreate, RobotResponse, RobotUpdate,
    MaterialCreate, MaterialResponse, MaterialUpdate,
    TipoMaterialResponse
)
from ....services import supabase_service as service


router = APIRouter()


# ============================================================================
# EQUIPOS
# ============================================================================

@router.get("/equipos", response_model=List[EquipoResponse], tags=["Inventario > Equipos"])
def listar_equipos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    supabase: Client = Depends(get_supabase)
):
    """Obtener lista de equipos"""
    return service.get_equipos(supabase, skip=skip, limit=limit)


@router.get("/equipos/{equipo_id}", response_model=EquipoResponse, tags=["Inventario > Equipos"])
def obtener_equipo(equipo_id: int, supabase: Client = Depends(get_supabase)):
    """Obtener equipo por ID"""
    equipo = service.get_equipo_by_id(supabase, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo


@router.get("/equipos/codigo/{codigo}", response_model=EquipoResponse, tags=["Inventario > Equipos"])
def obtener_equipo_por_codigo(codigo: str, supabase: Client = Depends(get_supabase)):
    """Obtener equipo por código (ej: PC-01)"""
    equipo = service.get_equipo_by_codigo(supabase, codigo)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo


@router.post("/equipos", response_model=EquipoResponse, tags=["Inventario > Equipos"])
def crear_equipo(equipo: EquipoCreate, supabase: Client = Depends(get_supabase)):
    """Crear un nuevo equipo"""
    # Verificar que el código no exista
    existing = service.get_equipo_by_codigo(supabase, equipo.codigo)
    if existing:
        raise HTTPException(status_code=400, detail="El código ya existe")
    
    return service.create_equipo(
        supabase,
        {
            "nombre": equipo.nombre,
            "marca": equipo.marca,
            "codigo": equipo.codigo,
            "accesorios": equipo.accesorios,
            "serial": equipo.serial,
            "estado": equipo.estado
        }
    )


@router.put("/equipos/{equipo_id}", response_model=EquipoResponse, tags=["Inventario > Equipos"])
def actualizar_equipo(equipo_id: int, equipo: EquipoUpdate, supabase: Client = Depends(get_supabase)):
    """
    Actualizar equipo

    VALIDACIONES:
    - NO cambiar a 'disponible' si tiene préstamos activos
    """
    update_data = equipo.model_dump(exclude_unset=True)

    # VALIDACIÓN: No cambiar a 'disponible' si tiene préstamos activos
    if 'estado' in update_data and update_data['estado'] == 'disponible':
        prestamos_activos = supabase.table("prestamos").select("*").eq("equipo_id", equipo_id).eq("estado", "activo").execute()

        if prestamos_activos.data:
            raise HTTPException(
                status_code=400,
                detail=f"No se puede cambiar a 'disponible': el equipo tiene {len(prestamos_activos.data)} préstamo(s) activo(s)"
            )

    updated = service.update_equipo(
        supabase,
        equipo_id,
        update_data
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return updated


@router.delete("/equipos/{equipo_id}", tags=["Inventario > Equipos"])
def eliminar_equipo(equipo_id: int, supabase: Client = Depends(get_supabase)):
    """
    Eliminar equipo

    VALIDACIONES:
    - NO eliminar si tiene préstamos activos
    """
    # VALIDACIÓN: Verificar si tiene préstamos activos
    prestamos_activos = supabase.table("prestamos").select("*").eq("equipo_id", equipo_id).eq("estado", "activo").execute()

    if prestamos_activos.data:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede eliminar: el equipo tiene {len(prestamos_activos.data)} préstamo(s) activo(s)"
        )

    if not service.delete_equipo(supabase, equipo_id):
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"message": "Equipo eliminado correctamente"}


# ============================================================================
# ELECTRÓNICA
# ============================================================================

@router.get("/electronica", response_model=List[ElectronicaResponse], tags=["Inventario > Electrónica"])
def listar_electronica(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    supabase: Client = Depends(get_supabase)
):
    """Obtener lista de electrónica"""
    return service.get_electronica(supabase, skip=skip, limit=limit)


@router.get("/electronica/{electronica_id}", response_model=ElectronicaResponse, tags=["Inventario > Electrónica"])
def obtener_electronica(electronica_id: int, supabase: Client = Depends(get_supabase)):
    """Obtener electrónica por ID"""
    item = service.get_electronica_by_id(supabase, electronica_id)
    if not item:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    return item


@router.post("/electronica", response_model=ElectronicaResponse, tags=["Inventario > Electrónica"])
def crear_electronica(electronica: ElectronicaCreate, supabase: Client = Depends(get_supabase)):
    """Crear nuevo elemento de electrónica"""
    return service.create_electronica(
        supabase,
        {
            "nombre": electronica.nombre,
            "descripcion": electronica.descripcion,
            "tipo": electronica.tipo,
            "en_uso": electronica.en_uso,
            "en_stock": electronica.en_stock
        }
    )


@router.put("/electronica/{electronica_id}", response_model=ElectronicaResponse, tags=["Inventario > Electrónica"])
def actualizar_electronica(electronica_id: int, electronica: ElectronicaUpdate, supabase: Client = Depends(get_supabase)):
    """Actualizar electrónica"""
    updated = service.update_electronica(
        supabase,
        electronica_id,
        electronica.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    return updated


@router.delete("/electronica/{electronica_id}", tags=["Inventario > Electrónica"])
def eliminar_electronica(electronica_id: int, supabase: Client = Depends(get_supabase)):
    """Eliminar electrónica"""
    if not service.delete_electronica(supabase, electronica_id):
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    return {"message": "Elemento eliminado correctamente"}


# ============================================================================
# ROBOTS
# ============================================================================

@router.get("/robots", response_model=List[RobotResponse], tags=["Inventario > Robots"])
def listar_robots(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    supabase: Client = Depends(get_supabase)
):
    """Obtener lista de robots"""
    return service.get_robots(supabase, skip=skip, limit=limit)


@router.get("/robots/{robot_id}", response_model=RobotResponse, tags=["Inventario > Robots"])
def obtener_robot(robot_id: int, supabase: Client = Depends(get_supabase)):
    """Obtener robot por ID"""
    item = service.get_robot_by_id(supabase, robot_id)
    if not item:
        raise HTTPException(status_code=404, detail="Robot no encontrado")
    return item


@router.post("/robots", response_model=RobotResponse, tags=["Inventario > Robots"])
def crear_robot(robot: RobotCreate, supabase: Client = Depends(get_supabase)):
    """Crear nuevo robot"""
    return service.create_robot(
        supabase,
        {
            "nombre": robot.nombre,
            "fuera_de_servicio": robot.fuera_de_servicio,
            "en_uso": robot.en_uso,
            "disponible": robot.disponible
        }
    )


@router.put("/robots/{robot_id}", response_model=RobotResponse, tags=["Inventario > Robots"])
def actualizar_robot(robot_id: int, robot: RobotUpdate, supabase: Client = Depends(get_supabase)):
    """Actualizar robot"""
    updated = service.update_robot(
        supabase,
        robot_id,
        robot.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Robot no encontrado")
    return updated


@router.delete("/robots/{robot_id}", tags=["Inventario > Robots"])
def eliminar_robot(robot_id: int, supabase: Client = Depends(get_supabase)):
    """Eliminar robot"""
    if not service.delete_robot(supabase, robot_id):
        raise HTTPException(status_code=404, detail="Robot no encontrado")
    return {"message": "Robot eliminado correctamente"}


# ============================================================================
# MATERIALES
# ============================================================================

@router.get("/materiales", response_model=List[MaterialResponse], tags=["Inventario > Materiales"])
def listar_materiales(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    supabase: Client = Depends(get_supabase)
):
    """Obtener lista de materiales"""
    return service.get_materiales(supabase, skip=skip, limit=limit)


@router.get("/materiales/{material_id}", response_model=MaterialResponse, tags=["Inventario > Materiales"])
def obtener_material(material_id: int, supabase: Client = Depends(get_supabase)):
    """Obtener material por ID"""
    item = service.get_material_by_id(supabase, material_id)
    if not item:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return item


@router.post("/materiales", response_model=MaterialResponse, tags=["Inventario > Materiales"])
def crear_material(material: MaterialCreate, supabase: Client = Depends(get_supabase)):
    """Crear nuevo material"""
    return service.create_material(
        supabase,
        {
            "color": material.color,
            "tipo_id": material.tipo_id,
            "cantidad": material.cantidad,
            "categoria": material.categoria,
            "usado": material.usado,
            "en_uso": material.en_uso,
            "en_stock": material.en_stock
        }
    )


@router.put("/materiales/{material_id}", response_model=MaterialResponse, tags=["Inventario > Materiales"])
def actualizar_material(material_id: int, material: MaterialUpdate, supabase: Client = Depends(get_supabase)):
    """
    Actualizar material

    VALIDACIONES:
    - NO permitir valores negativos (usado, en_uso, en_stock)
    """
    # VALIDACIÓN: No permitir valores negativos
    update_data = material.model_dump(exclude_unset=True)

    for campo in ['usado', 'en_uso', 'en_stock']:
        if campo in update_data and update_data[campo] < 0:
            raise HTTPException(
                status_code=400,
                detail=f"El campo '{campo}' no puede ser negativo. Valor actual: {update_data[campo]}"
            )

    updated = service.update_material(
        supabase,
        material_id,
        update_data
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return updated


@router.delete("/materiales/{material_id}", tags=["Inventario > Materiales"])
def eliminar_material(material_id: int, supabase: Client = Depends(get_supabase)):
    """Eliminar material"""
    if not service.delete_material(supabase, material_id):
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return {"message": "Material eliminado correctamente"}


# ============================================================================
# TIPOS DE MATERIALES
# ============================================================================

@router.get("/tipos-materiales", response_model=List[TipoMaterialResponse], tags=["Inventario > Materiales"])
def listar_tipos_materiales(supabase: Client = Depends(get_supabase)):
    """Obtener todos los tipos de materiales"""
    return service.get_tipos_materiales(supabase)
