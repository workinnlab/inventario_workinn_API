"""
Endpoints para configuración de alertas - Inventario CIE

Permite configurar umbrales de alertas de forma dinámica.
"""

from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from ....core.supabase_client import get_supabase
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()


class ConfiguracionAlerta(BaseModel):
    id: int
    clave: str
    valor: int
    descripcion: Optional[str] = None


class ConfiguracionUpdate(BaseModel):
    valor: int


@router.get("/configuracion/alertas", response_model=List[ConfiguracionAlerta], tags=["Configuración > Alertas"])
def get_configuracion_alertas(supabase: Client = Depends(get_supabase)):
    """
    Obtener todas las configuraciones de alertas
    
    Retorna los umbrales configurados para:
    - stock_minimo_default: Stock mínimo para materiales
    - prestamo_por_vencer_dias: Días para alerta de préstamo por vencer
    - prestamo_limite_dias: Límite de días para préstamo
    - prestamos_maximos_por_usuario: Máximo préstamos por usuario
    - alertar_stock_bajo: Activar/desactivar alertas de stock
    - alertar_prestamos_vencidos: Activar/desactivar alertas de vencidos
    - alertar_equipos_danados: Activar/desactivar alertas de dañados
    """
    response = supabase.table("configuracion_alertas").select("*").execute()
    return response.data


@router.get("/configuracion/alertas/{clave}", response_model=ConfiguracionAlerta, tags=["Configuración > Alertas"])
def get_configuracion_alerta(clave: str, supabase: Client = Depends(get_supabase)):
    """
    Obtener una configuración específica por clave
    
    Ejemplos de claves:
    - stock_minimo_default
    - prestamo_por_vencer_dias
    - prestamo_limite_dias
    """
    response = supabase.table("configuracion_alertas").select("*").eq("clave", clave).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail=f"Configuración '{clave}' no encontrada")
    
    return response.data[0]


@router.put("/configuracion/alertas/{clave}", response_model=ConfiguracionAlerta, tags=["Configuración > Alertas"])
def update_configuracion_alerta(clave: str, data: ConfiguracionUpdate, supabase: Client = Depends(get_supabase)):
    """
    Actualizar una configuración específica
    
    Solo admins pueden actualizar configuraciones
    """
    # Verificar que existe
    response = supabase.table("configuracion_alertas").select("*").eq("clave", clave).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail=f"Configuración '{clave}' no encontrada")
    
    # Actualizar
    response = supabase.table("configuracion_alertas").update({"valor": data.valor}).eq("clave", clave).execute()
    
    return response.data[0]


@router.post("/configuracion/alertas", response_model=ConfiguracionAlerta, tags=["Configuración > Alertas"])
def create_configuracion_alerta(clave: str, valor: int, descripcion: Optional[str] = None, supabase: Client = Depends(get_supabase)):
    """
    Crear nueva configuración de alerta
    
    Solo admins pueden crear configuraciones
    """
    # Verificar que no existe
    response = supabase.table("configuracion_alertas").select("*").eq("clave", clave).execute()
    
    if response.data:
        raise HTTPException(status_code=400, detail=f"Configuración '{clave}' ya existe")
    
    # Crear
    response = supabase.table("configuracion_alertas").insert({
        "clave": clave,
        "valor": valor,
        "descripcion": descripcion
    }).execute()
    
    return response.data[0]