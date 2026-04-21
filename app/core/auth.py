"""
Dependencias para autenticación y autorización
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from typing import Optional, List
from ..core.supabase_client import get_supabase
from ..schemas.auth import PerfilResponse

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: Client = Depends(get_supabase)
) -> PerfilResponse:
    """
    Dependencia para obtener el usuario autenticado
    
    Lanza HTTPException 401 si el token es inválido o expirado
    """
    try:
        token = credentials.credentials
        
        # Verificar token con Supabase
        user_response = supabase.auth.get_user(token)
        
        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Obtener perfil del usuario
        perfil = supabase.table("perfiles").select("*").eq("id", user_response.user.id).execute()
        
        if not perfil.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de usuario no encontrado"
            )
        
        user_data = perfil.data[0]
        
        if not user_data.get("activo", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        return PerfilResponse(**user_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error de autenticación: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_role(allowed_roles: List[str]):
    """
    Decorador para requerir roles específicos

    Uso:
        @router.get("/admin", dependencies=[Depends(require_role(["admin"]))])
        def endpoint_admin():
            ...
    """
    async def role_checker(
        current_user: PerfilResponse = Depends(get_current_user)
    ):
        if current_user.rol_id:
            rol_map = {1: "admin", 2: "inventory", 3: "viewer"}
            if rol_map.get(current_user.rol_id) not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Se requiere uno de los siguientes roles: {', '.join(allowed_roles)}"
                )
        elif current_user.rol.lower() not in [r.lower() for r in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los siguientes roles: {', '.join(allowed_roles)}"
            )
        return current_user

    return role_checker


# Dependencias pre-configuradas para roles comunes
require_admin = require_role(["admin"])
require_inventory = require_role(["admin", "inventory"])
require_auth = get_current_user  # Solo requiere estar autenticado
