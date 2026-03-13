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


@lru_cache()
def get_supabase_admin_client() -> Client:
    """
    Obtiene el cliente de Supabase con service_role key (bypass RLS)
    Usar solo para operaciones de escritura en el backend
    """
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_KEY
    )


def get_supabase() -> Client:
    """
    Dependencia para obtener el cliente de Supabase
    Usar en endpoints como: supabase: Client = Depends(get_supabase)
    """
    return get_supabase_client()


def get_supabase_admin() -> Client:
    """
    Dependencia para obtener el cliente admin de Supabase (bypass RLS)
    Usar para operaciones de escritura que requieren permisos elevados
    """
    return get_supabase_admin_client()
