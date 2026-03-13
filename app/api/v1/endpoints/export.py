"""
Endpoints para exportación y backup de datos - Inventario CIE

Permite exportar datos en formatos Excel, CSV, JSON para backup.
"""

from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from ....core.supabase_client import get_supabase
import json
from datetime import datetime

router = APIRouter()


@router.get("/export/json", tags=["Exportación > Backup"])
def export_json(supabase: Client = Depends(get_supabase)):
    """
    RN-10: Exportar todos los datos en formato JSON
    
    Útil para backup manual o migración
    """
    try:
        # Obtener todos los datos
        equipos = supabase.table("equipos").select("*").execute().data
        electronica = supabase.table("electronica").select("*").execute().data
        robots = supabase.table("robots").select("*").execute().data
        materiales = supabase.table("materiales").select("*").execute().data
        prestatarios = supabase.table("prestatarios").select("*").execute().data
        prestamos = supabase.table("prestamos").select("*").execute().data
        movimientos = supabase.table("movimientos").select("*").execute().data
        
        backup_data = {
            "export_date": datetime.now().isoformat(),
            "equipos": equipos,
            "electronica": electronica,
            "robots": robots,
            "materiales": materiales,
            "prestatarios": prestatarios,
            "prestamos": prestamos,
            "movimientos": movimientos
        }
        
        return backup_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al exportar: {str(e)}")


@router.get("/export/resumen", tags=["Exportación > Backup"])
def export_resumen(supabase: Client = Depends(get_supabase)):
    """
    RN-10: Exportar resumen del inventario
    
    Resumen estadístico para reporte rápido
    """
    try:
        equipos = supabase.table("equipos").select("*").execute().data
        electronica = supabase.table("electronica").select("*").execute().data
        robots = supabase.table("robots").select("*").execute().data
        materiales = supabase.table("materiales").select("*").execute().data
        prestamos = supabase.table("prestamos").select("*").execute().data
        
        resumen = {
            "export_date": datetime.now().isoformat(),
            "totales": {
                "equipos": len(equipos),
                "electronica": len(electronica),
                "robots": len(robots),
                "materiales": len(materiales),
                "prestamos_totales": len(prestamos),
                "prestamos_activos": len([p for p in prestamos if p.get('estado') == 'activo']),
                "prestamos_devueltos": len([p for p in prestamos if p.get('estado') == 'devuelto'])
            },
            "equipos_por_estado": {},
            "ultima_actualizacion": datetime.now().isoformat()
        }
        
        # Contar equipos por estado
        for equipo in equipos:
            estado = equipo.get('estado', 'desconocido')
            resumen["equipos_por_estado"][estado] = resumen["equipos_por_estado"].get(estado, 0) + 1
        
        return resumen
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al exportar resumen: {str(e)}")