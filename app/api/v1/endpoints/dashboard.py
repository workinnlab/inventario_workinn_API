"""
Endpoints para Dashboard y estadísticas - Inventario CIE

Proporciona datos para gráficas y dashboard del frontend.
"""

from fastapi import APIRouter, Depends, Query
from supabase import Client
from ....core.supabase_client import get_supabase
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter()


@router.get("/dashboard/resumen", tags=["Dashboard > Estadísticas"])
def dashboard_resumen(supabase: Client = Depends(get_supabase)):
    """
    RN-12: Resumen completo para dashboard
    
    Datos para gráficas y tarjetas de estadísticas
    """
    try:
        # Obtener todos los datos
        equipos = supabase.table("equipos").select("*").execute().data
        electronica = supabase.table("electronica").select("*").execute().data
        robots = supabase.table("robots").select("*").execute().data
        materiales = supabase.table("materiales").select("*").execute().data
        prestamos = supabase.table("prestamos").select("*").execute().data
        prestatarios = supabase.table("prestatarios").select("*").execute().data
        
        # Calcular estadísticas
        equipos_por_estado = {}
        for e in equipos:
            estado = e.get('estado', 'desconocido')
            equipos_por_estado[estado] = equipos_por_estado.get(estado, 0) + 1
        
        prestamos_por_estado = {}
        for p in prestamos:
            estado = p.get('estado', 'desconocido')
            prestamos_por_estado[estado] = prestamos_por_estado.get(estado, 0) + 1
        
        materiales_por_categoria = {}
        for m in materiales:
            cat = m.get('categoria', 'Otro')
            materiales_por_categoria[cat] = materiales_por_categoria.get(cat, 0) + 1
        
        # Calcular totales de stock
        total_electronica_stock = sum(e.get('en_stock', 0) for e in electronica)
        total_electronica_uso = sum(e.get('en_uso', 0) for e in electronica)
        
        total_robots_disponible = sum(r.get('disponible', 0) for r in robots)
        total_robots_uso = sum(r.get('en_uso', 0) for r in robots)
        
        total_materiales_stock = sum(m.get('en_stock', 0) for m in materiales)
        
        # Préstamos próximos a vencer (7 días)
        fecha_limite = datetime.now() + timedelta(days=7)
        prestamos_por_vencer = [
            p for p in prestamos 
            if p.get('estado') == 'activo' and p.get('fecha_limite')
        ]
        
        return {
            "fecha": datetime.now().isoformat(),
            "totales": {
                "equipos": len(equipos),
                "electronica": len(electronica),
                "robots": len(robots),
                "materiales": len(materiales),
                "prestatarios": len(prestatarios),
                "prestamos": len(prestamos)
            },
            "equipos": {
                "por_estado": equipos_por_estado,
                "disponibles": equipos_por_estado.get('disponible', 0),
                "en_uso": equipos_por_estado.get('en uso', 0),
                "prestados": equipos_por_estado.get('prestado', 0),
                "danados": equipos_por_estado.get('dañado', 0)
            },
            "electronica": {
                "total_stock": total_electronica_stock,
                "total_en_uso": total_electronica_uso
            },
            "robots": {
                "total_disponible": total_robots_disponible,
                "total_en_uso": total_robots_uso
            },
            "materiales": {
                "total_stock": total_materiales_stock,
                "por_categoria": materiales_por_categoria
            },
            "prestamos": {
                "por_estado": prestamos_por_estado,
                "activos": prestamos_por_estado.get('activo', 0),
                "devueltos": prestamos_por_estado.get('devuelto', 0),
                "vencidos": prestamos_por_estado.get('vencido', 0),
                "por_vencer_7_dias": len(prestamos_por_vencer)
            }
        }
        
    except Exception as e:
        from ....core.logging_config import log_error
        log_error("/dashboard/resumen", str(e))
        raise HTTPException(status_code=500, detail=f"Error al obtener dashboard: {str(e)}")


@router.get("/dashboard/movimientos-historial", tags=["Dashboard > Estadísticas"])
def dashboard_movimientos(
    dias: int = Query(30, ge=1, le=365, description="Días de historial"),
    supabase: Client = Depends(get_supabase)
):
    """
    RN-12: Historial de movimientos para gráficas
    
    Datos para gráfica de líneas de movimientos por día
    """
    try:
        movimientos = supabase.table("movimientos").select("*").execute().data
        
        # Filtrar por últimos X días
        fecha_limite = datetime.now() - timedelta(days=dias)
        movimientos_filtrados = []
        
        for m in movimientos:
            created_at = m.get('created_at')
            if created_at:
                try:
                    fecha = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    if fecha >= fecha_limite:
                        movimientos_filtrados.append(m)
                except:
                    pass
        
        # Agrupar por día y tipo
        movimientos_por_dia = {}
        movimientos_por_tipo = {}
        
        for m in movimientos_filtrados:
            fecha_str = m.get('created_at', '')[:10]  # YYYY-MM-DD
            tipo = m.get('tipo', 'desconocido')
            
            # Por día
            movimientos_por_dia[fecha_str] = movimientos_por_dia.get(fecha_str, 0) + 1
            
            # Por tipo
            movimientos_por_tipo[tipo] = movimientos_por_tipo.get(tipo, 0) + 1
        
        return {
            "dias": dias,
            "total_movimientos": len(movimientos_filtrados),
            "por_dia": movimientos_por_dia,
            "por_tipo": movimientos_por_tipo
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener historial: {str(e)}")


@router.get("/dashboard/top-prestatarios", tags=["Dashboard > Estadísticas"])
def dashboard_top_prestatarios(
    limite: int = Query(10, ge=1, le=100, description="Cantidad de prestatarios a retornar"),
    supabase: Client = Depends(get_supabase)
):
    """
    RN-12: Top prestatarios con más préstamos
    
    Datos para ranking o tabla
    """
    try:
        prestamos = supabase.table("prestamos").select("*").execute().data
        prestatarios = supabase.table("prestatarios").select("*").execute().data
        
        # Contar préstamos por prestatario
        prestamos_por_prestatario = {}
        for p in prestamos:
            prestatario_id = p.get('prestatario_id')
            prestamos_por_prestatario[prestatario_id] = prestamos_por_prestatario.get(prestatario_id, 0) + 1
        
        # Ordenar y obtener top
        top_ids = sorted(prestamos_por_prestatario.keys(), key=lambda x: prestamos_por_prestatario[x], reverse=True)[:limite]
        
        # Obtener datos de prestatarios
        top_prestatarios = []
        for prestatario_id in top_ids:
            prestatario_data = next((p for p in prestatarios if p['id'] == prestatario_id), None)
            if prestatario_data:
                top_prestatarios.append({
                    "id": prestatario_data['id'],
                    "nombre": prestatario_data['nombre'],
                    "dependencia": prestatario_data['dependencia'],
                    "total_prestamos": prestamos_por_prestatario[prestatario_id],
                    "activo": prestatario_data.get('activo', False)
                })
        
        return {
            "limite": limite,
            "prestatarios": top_prestatarios
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener top prestatarios: {str(e)}")