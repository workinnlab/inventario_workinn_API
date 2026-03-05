"""
Cliente de Supabase para la aplicación
Usa la API REST de Supabase en lugar de conexión directa a PostgreSQL
"""
from supabase import create_client, Client
from .config import settings
from functools import lru_cache


@lru_cache()
def get_supabase_client() -> Client:
    """
    Obtiene el cliente de Supabase (singleton con caché)
    
    Returns:
        Client: Cliente de Supabase configurado
    """
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY
    )


def get_supabase() -> Client:
    """
    Dependencia para obtener el cliente de Supabase
    Usar en endpoints como: supabase: Client = Depends(get_supabase)
    """
    return get_supabase_client()
