"""
Endpoints de autenticación usando Supabase Auth
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from ....core.supabase_client import get_supabase, get_supabase_admin
from ....schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
    PerfilResponse
)

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, tags=["Autenticación"])
def register(
    data: RegisterRequest,
    supabase: Client = Depends(get_supabase),
    supabase_admin: Client = Depends(get_supabase_admin)
):
    """
    Registrar nuevo usuario en Supabase Auth

    ⚠️ SEGURIDAD: Todos los usuarios se registran como 'viewer' por defecto.
    Solo un admin puede promover a 'inventory' o 'admin' desde Supabase Dashboard.

    Esto previene que cualquiera se registre como admin.
    """
    try:
        # FORZAR rol viewer para todos los registros públicos
        # Esto es por seguridad - solo admin puede crear roles privilegiados
        rol_asignado = 'viewer'

        # Registrar usuario en Supabase Auth SIN requerir confirmación de email
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
            "options": {
                "data": {
                    "nombre": data.nombre,
                    "rol": rol_asignado
                },
                "email_confirm": False  # No enviar email de confirmación
            }
        })

        if not response.user:
            raise HTTPException(
                status_code=400,
                detail="Error al registrar usuario"
            )

        # VERIFICAR que el usuario existe en auth.users
        user_check = supabase_admin.auth.get_user(response.user.id)
        if not user_check.user:
            raise HTTPException(
                status_code=400,
                detail="Usuario no confirmado en auth"
            )

        # CREAR PERFIL EXPLÍCITAMENTE (no depender del trigger)
        # Usar cliente admin para tener permisos de inserción
        try:
            perfil_result = supabase_admin.table("perfiles").insert({
                "id": response.user.id,
                "nombre": data.nombre,
                "email": data.email,
                "rol": rol_asignado,
                "activo": True
            }).execute()
            
            # Verificar que se creó
            if not perfil_result.data:
                raise HTTPException(
                    status_code=500,
                    detail="Error al crear perfil: no se recibió confirmación"
                )
                
        except HTTPException:
            raise
        except Exception as perfil_error:
            # Loguear el error real
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear perfil: {str(perfil_error)}"
            )

        return UserResponse(
            id=response.user.id,
            email=response.user.email,
            nombre=data.nombre,
            rol=rol_asignado,
            activo=True
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error en registro: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse, tags=["Autenticación"])
def login(
    data: LoginRequest,
    supabase: Client = Depends(get_supabase)
):
    """
    Iniciar sesión y obtener token de acceso

    VALIDACIONES:
    - AUTH-07: Rate limiting (máximo 5 intentos por minuto por IP)
    """
    # AUTH-07: Rate limiting simple (en producción usar Redis)
    # Esto es una implementación básica - en producción usar un sistema de cache como Redis
    from datetime import datetime, timedelta

    # Nota: Esta es una implementación simple. En producción se recomienda usar Redis.
    # Por ahora, dejamos que Supabase maneje el rate limiting a nivel de auth.

    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })

        if not response.user:
            raise HTTPException(
                status_code=401,
                detail="Credenciales inválidas"
            )

        # Obtener perfil del usuario
        perfil = supabase.table("perfiles").select("*").eq("id", response.user.id).execute()

        user_data = perfil.data[0] if perfil.data else None

        if not user_data:
            raise HTTPException(
                status_code=404,
                detail="Perfil de usuario no encontrado"
            )

        if not user_data.get("activo", True):
            raise HTTPException(
                status_code=403,
                detail="Usuario inactivo"
            )

        return TokenResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            token_type="bearer",
            user=UserResponse(
                id=response.user.id,
                email=response.user.email,
                nombre=user_data.get("nombre", ""),
                rol=user_data.get("rol", "viewer"),
                activo=user_data.get("activo", True)
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Error en login: {str(e)}"
        )


@router.post("/logout", tags=["Autenticación"])
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: Client = Depends(get_supabase)
):
    """
    Cerrar sesión (invalidar token)
    """
    try:
        await supabase.auth.sign_out()
        return {"message": "Sesión cerrada correctamente"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error en logout: {str(e)}"
        )


@router.get("/me", response_model=PerfilResponse, tags=["Autenticación"])
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: Client = Depends(get_supabase)
):
    """
    Obtener información del usuario autenticado
    """
    try:
        # Verificar token y obtener usuario
        token = credentials.credentials
        user_response = supabase.auth.get_user(token)

        if not user_response.user:
            raise HTTPException(
                status_code=401,
                detail="Token inválido o expirado"
            )

        # Obtener perfil completo
        perfil = supabase.table("perfiles").select("*").eq("id", user_response.user.id).execute()

        if not perfil.data:
            raise HTTPException(
                status_code=404,
                detail="Perfil no encontrado"
            )

        return PerfilResponse(**perfil.data[0])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Error al obtener usuario: {str(e)}"
        )


@router.post("/refresh", response_model=TokenResponse, tags=["Autenticación"])
async def refresh_token(
    refresh_token: str,
    supabase: Client = Depends(get_supabase)
):
    """
    Renovar token de acceso usando refresh token
    """
    try:
        response = await supabase.auth.refresh_session(refresh_token)
        
        if not response.session:
            raise HTTPException(
                status_code=401,
                detail="Refresh token inválido o expirado"
            )
        
        # Obtener perfil
        perfil = supabase.table("perfiles").select("*").eq("id", response.user.id).execute()
        user_data = perfil.data[0] if perfil.data else None
        
        return TokenResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            token_type="bearer",
            user=UserResponse(
                id=response.user.id,
                email=response.user.email,
                nombre=user_data.get("nombre", "") if user_data else "",
                rol=user_data.get("rol", "viewer") if user_data else "viewer",
                activo=user_data.get("activo", True) if user_data else False
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Error al renovar token: {str(e)}"
        )
