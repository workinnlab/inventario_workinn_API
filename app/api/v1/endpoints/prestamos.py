"""
Endpoints para gestión de préstamos y prestatarios usando Supabase
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from supabase import Client
from ....core.supabase_client import get_supabase
from ....core.auth import require_inventory
from ....schemas.auth import PerfilResponse
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
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """Obtener lista de prestatarios - Solo inventory y admin"""
    return service.get_prestatarios(supabase, skip=skip, limit=limit, activo=activo)


@router.get("/prestatarios/{prestatario_id}", response_model=PrestatarioResponse, tags=["Préstamos > Prestatarios"])
def obtener_prestatario(
    prestatario_id: int,
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """Obtener prestatario por ID - Solo inventory y admin"""
    prestatario = service.get_prestatario_by_id(supabase, prestatario_id)
    if not prestatario:
        raise HTTPException(status_code=404, detail="Prestatario no encontrado")
    return prestatario


@router.post("/prestatarios", response_model=PrestatarioResponse, tags=["Préstamos > Prestatarios"])
def crear_prestatario(
    prestatario: PrestatarioCreate,
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """
    Crear nuevo prestatario - Solo inventory y admin

    VALIDACIONES:
    - Email válido (si se proporciona)
    - PR-06: Cédula única (si se proporciona)
    - PR-04: Teléfono formato válido (si se proporciona)
    """
    # VALIDACIÓN: Email válido (formato simple)
    if prestatario.email:
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, prestatario.email):
            raise HTTPException(
                status_code=400,
                detail=f"Email inválido: '{prestatario.email}'. Formato esperado: usuario@dominio.com"
            )

    # VALIDACIÓN PR-06: Cédula única (si se proporciona)
    if prestatario.cedula:
        prestatarios_con_cedula = supabase.table("prestatarios").select("*").eq("cedula", prestatario.cedula).execute()
        if prestatarios_con_cedula.data:
            raise HTTPException(
                status_code=400,
                detail=f"La cédula '{prestatario.cedula}' YA ESTÁ EN USO por otro prestatario"
            )

    # VALIDACIÓN PR-04: Teléfono formato válido (si se proporciona)
    if prestatario.telefono:
        import re
        # Formato: +57 300 123 4567 o 300 123 4567 o 3001234567
        phone_pattern = r'^(\+57\s?)?([0-9]{10}|[0-9]{3}\s?[0-9]{3}\s?[0-9]{4})$'
        if not re.match(phone_pattern, prestatario.telefono.replace(' ', '')):
            raise HTTPException(
                status_code=400,
                detail=f"Teléfono inválido: '{prestatario.telefono}'. Formato esperado: 3001234567 o +57 300 123 4567"
            )

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
def actualizar_prestatario(
    prestatario_id: int,
    prestatario: PrestatarioUpdate,
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """
    Actualizar prestatario - Solo inventory y admin

    VALIDACIONES:
    - Email válido (si se proporciona y se está actualizando)
    """
    update_data = prestatario.model_dump(exclude_unset=True)

    # VALIDACIÓN: Email válido (si se está actualizando)
    if 'email' in update_data and update_data['email']:
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, update_data['email']):
            raise HTTPException(
                status_code=400,
                detail=f"Email inválido: '{update_data['email']}'. Formato esperado: usuario@dominio.com"
            )

    updated = service.update_prestatario(supabase, prestatario_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Prestatario no encontrado")
    return updated


@router.delete("/prestatarios/{prestatario_id}", tags=["Préstamos > Prestatarios"])
def eliminar_prestatario(
    prestatario_id: int,
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """
    Eliminar prestatario (lógico: marca como inactivo) - Solo inventory y admin

    VALIDACIONES:
    - NO eliminar/inactivar si tiene préstamos activos
    """
    # VALIDACIÓN: Verificar si tiene préstamos activos
    prestamos_activos = supabase.table("prestamos").select("*").eq("prestatario_id", prestatario_id).eq("estado", "activo").execute()

    if prestamos_activos.data:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede inactivar: el prestatario tiene {len(prestamos_activos.data)} préstamo(s) activo(s). Primero deben ser devueltos."
        )

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
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """Obtener lista de préstamos - Solo inventory y admin"""
    return service.get_prestamos(supabase, skip=skip, limit=limit, estado=estado)


@router.get("/prestamos/activos", response_model=List[PrestamoResponse], tags=["Préstamos > Gestión"])
def listar_prestamos_activos(
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """
    Obtener préstamos activos - Solo inventory y admin

    NOTA: También incluye lógica para marcar automáticamente como 'vencidos'
    los préstamos que pasaron su fecha_limite

    RN-03: Retorna información de días restantes para alertas
    """
    # Primero, marcar como vencidos los que ya pasaron fecha_limite
    from datetime import datetime, timezone
    fecha_actual = datetime.now(timezone.utc)

    prestamos_activos = supabase.table("prestamos").select("*").eq("estado", "activo").execute()

    for prestamo in prestamos_activos.data:
        fecha_limite_str = prestamo.get('fecha_limite')
        if fecha_limite_str:
            # Parsear fecha_limite
            try:
                fecha_limite = datetime.fromisoformat(fecha_limite_str.replace('Z', '+00:00'))
                if fecha_limite < fecha_actual:
                    # Marcar como vencido
                    supabase.table("prestamos").update({"estado": "vencido"}).eq("id", prestamo['id']).execute()
            except Exception:
                pass  # Si no se puede parsear, continuar

    # Retornar préstamos activos
    return service.get_prestamos_activos(supabase)


@router.get("/prestamos/por-vencer", response_model=List[PrestamoResponse], tags=["Préstamos > Gestión"])
def listar_prestamos_por_vencer(
    dias: Optional[int] = Query(None, ge=1, description="Días para considerar como 'por vencer'"),
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """
    RN-03: Obtener préstamos que están por vencer en los próximos X días - Solo inventory y admin

    Si no se proporciona 'dias', usa la configuración global (default: 7)
    """
    from datetime import datetime, timezone, timedelta

    # Obtener configuración si no se proporciona dias
    if dias is None:
        config_response = supabase.table("configuracion_alertas").select("valor").eq("clave", "prestamo_por_vencer_dias").execute()
        dias = config_response.data[0]['valor'] if config_response.data else 7

    fecha_actual = datetime.now(timezone.utc)
    fecha_limite = fecha_actual + timedelta(days=dias)

    # Obtener préstamos activos
    prestamos_activos = supabase.table("prestamos").select("*").eq("estado", "activo").execute()

    # Filtrar los que vencen en los próximos X días
    prestamos_por_vencer = []
    for prestamo in prestamos_activos.data:
        fecha_limite_str = prestamo.get('fecha_limite')
        if fecha_limite_str:
            try:
                fecha_prestamo_limite = datetime.fromisoformat(fecha_limite_str.replace('Z', '+00:00'))
                if fecha_actual <= fecha_prestamo_limite <= fecha_limite:
                    prestamos_por_vencer.append(prestamo)
            except Exception:
                pass

    return prestamos_por_vencer


@router.get("/prestamos/{prestamo_id}", response_model=PrestamoResponse, tags=["Préstamos > Gestión"])
def obtener_prestamo(
    prestamo_id: int,
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """Obtener préstamo por ID - Solo inventory y admin"""
    prestamo = service.get_prestamo_by_id(supabase, prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo


@router.post("/prestamos", response_model=PrestamoResponse, tags=["Préstamos > Gestión"])
def crear_prestamo(
    prestamo: PrestamoCreate,
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """
    Crear nuevo préstamo - Solo inventory y admin

    VALIDACIONES:
    1. Verifica que el elemento NO esté ya prestado
    2. Verifica que el elemento NO esté dañado o en mantenimiento
    3. Verifica que el prestatario exista y esté activo
    4. Verifica que fecha_limite >= fecha_actual (si se proporciona)
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
    # VALIDACIÓN 0: fecha_limite >= fecha_actual
    # ========================================================================
    if prestamo.fecha_limite:
        try:
            from datetime import datetime, timezone, timedelta

            # Obtener fecha actual con timezone
            fecha_actual = datetime.now(timezone.utc)

            # Parsear la fecha_limite si es string
            if isinstance(prestamo.fecha_limite, str):
                # Reemplazar Z con +00:00 para fromisoformat
                fecha_str = prestamo.fecha_limite.replace('Z', '+00:00')
                fecha_limite_dt = datetime.fromisoformat(fecha_str)
            else:
                fecha_limite_dt = prestamo.fecha_limite

            # Asegurar que fecha_limite tenga timezone info
            if fecha_limite_dt.tzinfo is None:
                # Asumir UTC si no tiene timezone
                fecha_limite_dt = fecha_limite_dt.replace(tzinfo=timezone.utc)

            # Asegurar que fecha_actual tenga timezone info (ya lo tiene)
            if fecha_actual.tzinfo is None:
                fecha_actual = fecha_actual.replace(tzinfo=timezone.utc)

            if fecha_limite_dt < fecha_actual:
                raise HTTPException(
                    status_code=400,
                    detail="fecha_limite debe ser mayor o igual a la fecha actual"
                )

            # RN-02: Validar que fecha_limite no exceda el límite máximo de días
            LIMITE_DIAS_PRESTAMO = 30  # Máximo 30 días por préstamo
            fecha_maxima = fecha_actual + timedelta(days=LIMITE_DIAS_PRESTAMO)

            if fecha_limite_dt > fecha_maxima:
                raise HTTPException(
                    status_code=400,
                    detail=f"RN-02: fecha_limite no puede exceder {LIMITE_DIAS_PRESTAMO} días. Fecha máxima: {fecha_maxima.strftime('%Y-%m-%d')}"
                )
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ [DEBUG] Error validando fecha: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=400,
                detail=f"Error al validar fecha_limite: {str(e)}"
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
    # VALIDACIÓN 2B: Verificar stock disponible (para electrónica, robots, materiales)
    # ========================================================================
    if item_tipo == 'electronica':
        electronica = service.get_electronica_by_id(supabase, item_id)
        if not electronica:
            raise HTTPException(status_code=404, detail="Electrónica no encontrada")

        en_stock = electronica.get('en_stock', 0)
        if en_stock <= 0:
            raise HTTPException(
                status_code=400,
                detail=f"La electrónica con ID {item_id} NO TIENE STOCK disponible (en_stock={en_stock})"
            )

    elif item_tipo == 'robot':
        robot = service.get_robot_by_id(supabase, item_id)
        if not robot:
            raise HTTPException(status_code=404, detail="Robot no encontrado")

        disponible = robot.get('disponible', 0)
        if disponible <= 0:
            raise HTTPException(
                status_code=400,
                detail=f"El robot con ID {item_id} NO TIENE unidades disponibles (disponible={disponible})"
            )

    elif item_tipo == 'material':
        material = service.get_material_by_id(supabase, item_id)
        if not material:
            raise HTTPException(status_code=404, detail="Material no encontrado")

        en_stock = material.get('en_stock', 0)
        if en_stock <= 0:
            raise HTTPException(
                status_code=400,
                detail=f"El material con ID {item_id} NO TIENE stock disponible (en_stock={en_stock})"
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
    # VALIDACIÓN 4: RN-05 - No prestar si tiene préstamos vencidos
    # ========================================================================
    prestamos_vencidos = supabase.table("prestamos").select("*").eq("prestatario_id", prestamo.prestatario_id).eq("estado", "vencido").execute()

    if prestamos_vencidos.data:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede crear préstamo: el prestatario tiene {len(prestamos_vencidos.data)} préstamo(s) VENCIDO(S). Primero deben ser devueltos."
        )

    # ========================================================================
    # VALIDACIÓN 5: RN-01 - Límite de préstamos activos por prestatario
    # ========================================================================
    LIMITE_PRESTAMOS_ACTIVOS = 5  # Máximo 5 préstamos activos simultáneos
    prestamos_activos_prestatario = supabase.table("prestamos").select("*").eq("prestatario_id", prestamo.prestatario_id).eq("estado", "activo").execute()

    if len(prestamos_activos_prestatario.data) >= LIMITE_PRESTAMOS_ACTIVOS:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede crear préstamo: el prestatario ya tiene {LIMITE_PRESTAMOS_ACTIVOS} préstamos activos (límite alcanzado)."
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
        # VALIDACIÓN PS-13: Actualizar estado del equipo a 'prestado'
        supabase.table("equipos").update({"estado": "prestado"}).eq("id", item_id).execute()
    elif item_tipo == 'electronica':
        data["electronica_id"] = item_id
        # VALIDACIÓN EL-07: Restar del stock al prestar
        electronica = service.get_electronica_by_id(supabase, item_id)
        if electronica:
            nuevo_stock = max(0, electronica.get('en_stock', 0) - 1)
            supabase.table("electronica").update({"en_stock": nuevo_stock}).eq("id", item_id).execute()
    elif item_tipo == 'robot':
        data["robot_id"] = item_id
        # VALIDACIÓN RO-08: Mover de disponible a en_uso al prestar
        robot = service.get_robot_by_id(supabase, item_id)
        if robot:
            nuevo_disponible = max(0, robot.get('disponible', 0) - 1)
            nuevo_en_uso = robot.get('en_uso', 0) + 1
            supabase.table("robots").update({
                "disponible": nuevo_disponible,
                "en_uso": nuevo_en_uso
            }).eq("id", item_id).execute()
    elif item_tipo == 'material':
        data["material_id"] = item_id
        # Restar del stock al prestar
        material = service.get_material_by_id(supabase, item_id)
        if material:
            nuevo_stock = max(0, material.get('en_stock', 0) - 1)
            supabase.table("materiales").update({"en_stock": nuevo_stock}).eq("id", item_id).execute()

    return service.create_prestamo(supabase, data)


@router.put("/prestamos/{prestamo_id}", response_model=PrestamoResponse, tags=["Préstamos > Gestión"])
def actualizar_prestamo(
    prestamo_id: int,
    prestamo: PrestamoUpdate,
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """
    Actualizar préstamo - Solo inventory y admin

    VALIDACIONES:
    - PS-09: fecha_devolucion >= fecha_prestamo (si se proporciona)
    """
    update_data = prestamo.model_dump(exclude_unset=True)

    # PS-09: Validar que fecha_devolucion >= fecha_prestamo
    if 'fecha_devolucion' in update_data and update_data['fecha_devolucion']:
        # Obtener el préstamo para verificar fecha_prestamo
        prestamo_actual = service.get_prestamo_by_id(supabase, prestamo_id)
        if prestamo_actual:
            fecha_prestamo_str = prestamo_actual.get('fecha_prestamo')
            fecha_devolucion_str = update_data['fecha_devolucion']

            if fecha_prestamo_str and fecha_devolucion_str:
                from datetime import datetime
                try:
                    fecha_prestamo = datetime.fromisoformat(fecha_prestamo_str.replace('Z', '+00:00'))
                    fecha_devolucion = datetime.fromisoformat(fecha_devolucion_str.replace('Z', '+00:00'))

                    if fecha_devolucion < fecha_prestamo:
                        raise HTTPException(
                            status_code=400,
                            detail="PS-09: fecha_devolucion debe ser mayor o igual a fecha_prestamo"
                        )
                except ValueError:
                    pass  # Si no se puede parsear, continuar

    updated = service.update_prestamo(
        supabase,
        prestamo_id,
        update_data
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return updated


@router.post("/prestamos/{prestamo_id}/devolver", response_model=PrestamoResponse, tags=["Préstamos > Gestión"])
def devolver_prestamo(
    prestamo_id: int,
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """
    Marcar préstamo como devuelto

    VALIDACIONES:
    - Solo devolver si está 'activo' o 'vencido'
    - PS-14: Actualizar estado del equipo a 'disponible' al devolver
    - EL-08: Ajustar stock de electrónica al devolver
    - RO-09: Ajustar disponible/en_uso de robots al devolver
    """
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

        # ✅ Permitir 'activo' y 'vencido'
        if estado_actual not in ['activo', 'vencido']:
            raise HTTPException(
                status_code=400,
                detail=f"El préstamo no está activo o vencido (estado: {estado_actual})"
            )

        # Usar formato de fecha compatible con PostgreSQL
        from datetime import datetime, timezone
        fecha_devolucion = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        print(f"📅 Fecha devolución: {fecha_devolucion}")

        # ====================================================================
        # PS-14: Actualizar estado del equipo a 'disponible' al devolver
        # ====================================================================
        equipo_id = prestamo.get('equipo_id')
        if equipo_id:
            print(f"🔄 Actualizando equipo {equipo_id} a 'disponible'...")
            supabase.table("equipos").update({"estado": "disponible"}).eq("id", equipo_id).execute()

        # ====================================================================
        # EL-08: Ajustar stock de electrónica al devolver
        # ====================================================================
        electronica_id = prestamo.get('electronica_id')
        if electronica_id:
            electronica = service.get_electronica_by_id(supabase, electronica_id)
            if electronica:
                nuevo_stock = electronica.get('en_stock', 0) + 1
                print(f"🔄 Ajustando stock electrónica: {electronica.get('en_stock')} -> {nuevo_stock}")
                supabase.table("electronica").update({"en_stock": nuevo_stock}).eq("id", electronica_id).execute()

        # ====================================================================
        # RO-09: Ajustar disponible/en_uso de robots al devolver
        # ====================================================================
        robot_id = prestamo.get('robot_id')
        if robot_id:
            robot = service.get_robot_by_id(supabase, robot_id)
            if robot:
                nuevo_disponible = robot.get('disponible', 0) + 1
                nuevo_en_uso = max(0, robot.get('en_uso', 0) - 1)
                print(f"🔄 Ajustando robot: disponible {robot.get('disponible')} -> {nuevo_disponible}, en_uso {robot.get('en_uso')} -> {nuevo_en_uso}")
                supabase.table("robots").update({
                    "disponible": nuevo_disponible,
                    "en_uso": nuevo_en_uso
                }).eq("id", robot_id).execute()

        # ====================================================================
        # Ajustar stock de materiales al devolver
        # ====================================================================
        material_id = prestamo.get('material_id')
        if material_id:
            material = service.get_material_by_id(supabase, material_id)
            if material:
                nuevo_stock = material.get('en_stock', 0) + 1
                print(f"🔄 Ajustando stock material: {material.get('en_stock')} -> {nuevo_stock}")
                supabase.table("materiales").update({"en_stock": nuevo_stock}).eq("id", material_id).execute()

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
def eliminar_prestamo(
    prestamo_id: int,
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """
    Eliminar préstamo - Solo inventory y admin

    VALIDACIÓN:
    - NO permitir eliminar si está activo (debe estar devuelto primero)
    """
    # Obtener préstamo para verificar estado
    prestamo = service.get_prestamo_by_id(supabase, prestamo_id)

    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    # VALIDACIÓN: No eliminar si está activo
    if prestamo.get('estado') == 'activo':
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar un préstamo ACTIVO. Primero debe ser devuelto."
        )

    if not service.delete_prestamo(supabase, prestamo_id):
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    return {"message": "Préstamo eliminado correctamente"}
