"""
Endpoints para gestión de notificaciones - Inventario CIE

Sistema de notificaciones para admin e inventory.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from supabase import Client
from ....core.supabase_client import get_supabase
from ....core.auth import require_inventory
from ....schemas.auth import PerfilResponse
from ....services import supabase_service as service
from datetime import datetime, timedelta


router = APIRouter()


@router.get("/notificaciones", tags=["Notificaciones"])
def listar_notificaciones(
    skip: int = 0,
    limit: int = 100,
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """
    Obtener lista de notificaciones
    """
    return service.get_notificaciones(supabase, skip=skip, limit=limit)


@router.get("/notificaciones/pendientes", tags=["Notificaciones"])
def listar_notificaciones_pendientes(
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """
    Obtener notificaciones no leídas y generar alertas automáticas si no existen

    Este endpoint:
    1. Retorna notificaciones no leídas existentes
    2. Revisa préstamos por vencer y crea notificación si no existe
    3. Revisa stock bajo y crea notificación si no existe
    """
    from datetime import timezone

    notificaciones = service.get_notificaciones_pendientes(supabase)

    fecha_actual = datetime.now(timezone.utc)

    prestamos = supabase.table("prestamos").select("*").execute().data

    prestamos_por_vencer = []
    prestamos_vencidos = []

    for prestamo in prestamos:
        if prestamo.get('estado') == 'activo' and prestamo.get('fecha_limite'):
            try:
                fecha_limite = datetime.fromisoformat(prestamo.get('fecha_limite').replace('Z', '+00:00'))
                dias_restantes = (fecha_limite - fecha_actual).days

                if 0 <= dias_restantes <= 7:
                    prestamos_por_vencer.append({
                        'id': prestamo.get('id'),
                        'dias': dias_restantes,
                        'prestamo': prestamo
                    })
                elif dias_restantes < 0:
                    prestamos_vencidos.append({
                        'id': prestamo.get('id'),
                        'dias': abs(dias_restantes),
                        'prestamo': prestamo
                    })
            except:
                pass

    if prestamos_por_vencer:
        existente = supabase.table("notificaciones").select("id").eq("tipo", "prestamo_vencer").eq("leida", False).execute()
        if not existente.data:
            service.crear_notificacion(
                supabase=supabase,
                tipo="prestamo_vencer",
                titulo="Préstamos por vencer",
                mensaje=f"Hay {len(prestamos_por_vencer)} préstamo(s) por vencer en los próximos 7 días",
                url="/prestamos"
            )

    if prestamos_vencidos:
        existente = supabase.table("notificaciones").select("id").eq("tipo", "prestamo_vencido").eq("leida", False).execute()
        if not existente.data:
            service.crear_notificacion(
                supabase=supabase,
                tipo="prestamo_vencido",
                titulo="Préstamos vencidos",
                mensaje=f"Hay {len(prestamos_vencidos)} préstamo(s) vencidos que requieren atención",
                url="/prestamos"
            )

    materiales = supabase.table("materiales").select("*").execute().data
    config_response = supabase.table("configuracion_alertas").select("valor").eq("clave", "stock_minimo_default").execute()
    stock_minimo = config_response.data[0]['valor'] if config_response.data else 5

    materiales_bajo_stock = [m for m in materiales if m.get('en_stock', 0) <= stock_minimo]

    if materiales_bajo_stock:
        existente = supabase.table("notificaciones").select("id").eq("tipo", "stock_bajo").eq("leida", False).execute()
        if not existente.data:
            service.crear_notificacion(
                supabase=supabase,
                tipo="stock_bajo",
                titulo="Stock bajo",
                mensaje=f"Hay {len(materiales_bajo_stock)} material(es) con stock bajo (≤{stock_minimo})",
                url="/materiales"
            )

    return service.get_notificaciones_pendientes(supabase)


@router.put("/notificaciones/{notificacion_id}/leer", tags=["Notificaciones"])
def marcar_leida(
    notificacion_id: int,
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """Marcar notificación como leída"""
    updated = service.marcar_notificacion_leida(supabase, notificacion_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return updated


@router.put("/notificaciones/leer-todas", tags=["Notificaciones"])
def marcar_todas_leidas(
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """Marcar todas las notificaciones como leídas"""
    count = service.marcar_todas_leidas(supabase)
    return {"message": f"Se marcaron {count} notificaciones como leídas"}


@router.delete("/notificaciones/{notificacion_id}", tags=["Notificaciones"])
def eliminar_notificacion(
    notificacion_id: int,
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """Eliminar una notificación"""
    if not service.eliminar_notificacion(supabase, notificacion_id):
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return {"message": "Notificación eliminada"}


@router.delete("/notificaciones", tags=["Notificaciones"])
def eliminar_leidas(
    current_user: PerfilResponse = Depends(require_inventory),
    supabase: Client = Depends(get_supabase)
):
    """Eliminar todas las notificaciones leídas"""
    count = service.eliminar_notificaciones_leidas(supabase)
    return {"message": f"Se eliminaron {count} notificaciones leídas"}
