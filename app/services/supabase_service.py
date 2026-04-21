"""
Servicios para operaciones de inventario usando Supabase
"""
from supabase import Client
from typing import List, Optional, Dict, Any
from datetime import datetime


# ============================================================================
# EQUIPOS
# ============================================================================

def get_equipos(supabase: Client, skip: int = 0, limit: int = 100) -> List[Dict]:
    """Obtener lista de equipos"""
    response = supabase.table("equipos").select("*").range(skip, skip + limit - 1).execute()
    return response.data


def get_equipo_by_id(supabase: Client, equipo_id: int) -> Optional[Dict]:
    """Obtener equipo por ID"""
    response = supabase.table("equipos").select("*").eq("id", equipo_id).execute()
    return response.data[0] if response.data else None


def get_equipo_by_codigo(supabase: Client, codigo: str) -> Optional[Dict]:
    """Obtener equipo por código (ej: PC-01)"""
    response = supabase.table("equipos").select("*").eq("codigo", codigo).execute()
    return response.data[0] if response.data else None


def create_equipo(supabase: Client, data: Dict[str, Any]) -> Dict:
    """Crear un nuevo equipo"""
    response = supabase.table("equipos").insert(data).execute()
    return response.data[0] if response.data else None


def update_equipo(supabase: Client, equipo_id: int, data: Dict[str, Any]) -> Optional[Dict]:
    """Actualizar equipo"""
    response = supabase.table("equipos").update(data).eq("id", equipo_id).execute()
    return response.data[0] if response.data else None


def delete_equipo(supabase: Client, equipo_id: int) -> bool:
    """Eliminar equipo"""
    response = supabase.table("equipos").delete().eq("id", equipo_id).execute()
    return len(response.data) > 0


# ============================================================================
# ELECTRÓNICA
# ============================================================================

def get_electronica(supabase: Client, skip: int = 0, limit: int = 100) -> List[Dict]:
    """Obtener lista de electrónica"""
    response = supabase.table("electronica").select("*").range(skip, skip + limit - 1).execute()
    return response.data


def get_electronica_by_id(supabase: Client, electronica_id: int) -> Optional[Dict]:
    """Obtener electrónica por ID"""
    response = supabase.table("electronica").select("*").eq("id", electronica_id).execute()
    return response.data[0] if response.data else None


def create_electronica(supabase: Client, data: Dict[str, Any]) -> Dict:
    """Crear nuevo elemento de electrónica"""
    response = supabase.table("electronica").insert(data).execute()
    return response.data[0] if response.data else None


def update_electronica(supabase: Client, electronica_id: int, data: Dict[str, Any]) -> Optional[Dict]:
    """Actualizar electrónica"""
    response = supabase.table("electronica").update(data).eq("id", electronica_id).execute()
    return response.data[0] if response.data else None


def delete_electronica(supabase: Client, electronica_id: int) -> bool:
    """Eliminar electrónica"""
    response = supabase.table("electronica").delete().eq("id", electronica_id).execute()
    return len(response.data) > 0


# ============================================================================
# ROBOTS
# ============================================================================

def get_robots(supabase: Client, skip: int = 0, limit: int = 100) -> List[Dict]:
    """Obtener lista de robots"""
    response = supabase.table("robots").select("*").range(skip, skip + limit - 1).execute()
    return response.data


def get_robot_by_id(supabase: Client, robot_id: int) -> Optional[Dict]:
    """Obtener robot por ID"""
    response = supabase.table("robots").select("*").eq("id", robot_id).execute()
    return response.data[0] if response.data else None


def create_robot(supabase: Client, data: Dict[str, Any]) -> Dict:
    """Crear nuevo robot"""
    response = supabase.table("robots").insert(data).execute()
    return response.data[0] if response.data else None


def update_robot(supabase: Client, robot_id: int, data: Dict[str, Any]) -> Optional[Dict]:
    """Actualizar robot"""
    response = supabase.table("robots").update(data).eq("id", robot_id).execute()
    return response.data[0] if response.data else None


def delete_robot(supabase: Client, robot_id: int) -> bool:
    """Eliminar robot"""
    response = supabase.table("robots").delete().eq("id", robot_id).execute()
    return len(response.data) > 0


# ============================================================================
# MATERIALES
# ============================================================================

def get_materiales(supabase: Client, skip: int = 0, limit: int = 100) -> List[Dict]:
    """Obtener lista de materiales"""
    response = supabase.table("materiales").select("*").range(skip, skip + limit - 1).execute()
    return response.data


def get_material_by_id(supabase: Client, material_id: int) -> Optional[Dict]:
    """Obtener material por ID"""
    response = supabase.table("materiales").select("*").eq("id", material_id).execute()
    return response.data[0] if response.data else None


def create_material(supabase: Client, data: Dict[str, Any]) -> Dict:
    """Crear nuevo material"""
    response = supabase.table("materiales").insert(data).execute()
    return response.data[0] if response.data else None


def update_material(supabase: Client, material_id: int, data: Dict[str, Any]) -> Optional[Dict]:
    """Actualizar material"""
    response = supabase.table("materiales").update(data).eq("id", material_id).execute()
    return response.data[0] if response.data else None


def delete_material(supabase: Client, material_id: int) -> bool:
    """Eliminar material"""
    # En versiones recientes de postgrest-py (async), delete() retorna los datos afectados
    response = supabase.table("materiales").delete().eq("id", material_id).execute()
    return len(response.data) > 0


# ============================================================================
# TIPOS DE MATERIALES
# ============================================================================

def get_tipos_materiales(supabase: Client) -> List[Dict]:
    """Obtener todos los tipos de materiales"""
    response = supabase.table("tipos_materiales").select("*").execute()
    return response.data


def create_tipo_material(supabase: Client, nombre: str) -> Dict:
    """Crear tipo de material (si no existe)"""
    # Verificar si existe
    existing = supabase.table("tipos_materiales").select("*").eq("nombre", nombre).execute()
    if existing.data:
        return existing.data[0]
    
    response = supabase.table("tipos_materiales").insert({"nombre": nombre}).execute()
    return response.data[0] if response.data else None


# ============================================================================
# PRESTATARIOS
# ============================================================================

def get_prestatarios(supabase: Client, skip: int = 0, limit: int = 100, activo: bool = True) -> List[Dict]:
    """Obtener lista de prestatarios"""
    query = supabase.table("prestatarios").select("*")
    if activo is not None:
        query = query.eq("activo", activo)
    response = query.range(skip, skip + limit - 1).execute()
    return response.data


def get_prestatario_by_id(supabase: Client, prestatario_id: int) -> Optional[Dict]:
    """Obtener prestatario por ID"""
    response = supabase.table("prestatarios").select("*").eq("id", prestatario_id).execute()
    return response.data[0] if response.data else None


def create_prestatario(supabase: Client, data: Dict[str, Any]) -> Dict:
    """Crear nuevo prestatario"""
    response = supabase.table("prestatarios").insert(data).execute()
    return response.data[0] if response.data else None


def update_prestatario(supabase: Client, prestatario_id: int, data: Dict[str, Any]) -> Optional[Dict]:
    """Actualizar prestatario"""
    response = supabase.table("prestatarios").update(data).eq("id", prestatario_id).execute()
    return response.data[0] if response.data else None


def delete_prestatario(supabase: Client, prestatario_id: int) -> bool:
    """Eliminar prestatario (lógico: marca como inactivo)"""
    return update_prestatario(supabase, prestatario_id, {"activo": False})


# ============================================================================
# PRÉSTAMOS
# ============================================================================

def get_prestamos(supabase: Client, skip: int = 0, limit: int = 100, estado: str = None) -> List[Dict]:
    """Obtener lista de préstamos"""
    query = supabase.table("prestamos").select("*")
    if estado:
        query = query.eq("estado", estado)
    response = query.range(skip, skip + limit - 1).execute()
    return response.data


def get_prestamo_by_id(supabase: Client, prestamo_id: int) -> Optional[Dict]:
    """Obtener préstamo por ID"""
    response = supabase.table("prestamos").select("*").eq("id", prestamo_id).execute()
    return response.data[0] if response.data else None


def get_prestamos_activos(supabase: Client) -> List[Dict]:
    """Obtener préstamos activos"""
    response = supabase.table("prestamos").select("*").eq("estado", "activo").execute()
    return response.data


def create_prestamo(supabase: Client, data: Dict[str, Any]) -> Dict:
    """Crear nuevo préstamo"""
    response = supabase.table("prestamos").insert(data).execute()
    return response.data[0] if response.data else None


def update_prestamo(supabase: Client, prestamo_id: int, data: Dict[str, Any]) -> Optional[Dict]:
    """Actualizar préstamo"""
    response = supabase.table("prestamos").update(data).eq("id", prestamo_id).execute()
    return response.data[0] if response.data else None


def delete_prestamo(supabase: Client, prestamo_id: int) -> bool:
    """Eliminar préstamo"""
    response = supabase.table("prestamos").delete().eq("id", prestamo_id).execute()
    return len(response.data) > 0


# ============================================================================
# MOVIMIENTOS
# ============================================================================

def get_movimientos(supabase: Client, skip: int = 0, limit: int = 100, tipo: str = None) -> List[Dict]:
    """Obtener lista de movimientos"""
    query = supabase.table("movimientos").select("*").order("created_at", desc=True)
    if tipo:
        query = query.eq("tipo", tipo)
    response = query.range(skip, skip + limit - 1).execute()

    movimientos = response.data
    for mov in movimientos:
        if mov.get('usuario_id'):
            perfil = supabase.table("perfiles").select("nombre").eq("id", mov['usuario_id']).execute()
            if perfil.data:
                mov['usuario_nombre'] = perfil.data[0].get('nombre')

    return movimientos


def get_movimiento_by_id(supabase: Client, movimiento_id: int) -> Optional[Dict]:
    """Obtener movimiento por ID"""
    response = supabase.table("movimientos").select("*").eq("id", movimiento_id).execute()
    return response.data[0] if response.data else None


def create_movimiento(supabase: Client, data: Dict[str, Any]) -> Dict:
    """Crear nuevo movimiento"""
    response = supabase.table("movimientos").insert(data).execute()
    return response.data[0] if response.data else None

