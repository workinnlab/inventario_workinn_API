"""
Schemas Pydantic para autenticación
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ============================================================================
# REQUESTS
# ============================================================================

class LoginRequest(BaseModel):
    """Schema para login"""
    email: EmailStr
    password: str = Field(..., min_length=6)


class RegisterRequest(BaseModel):
    """Schema para registro de usuario"""
    email: EmailStr
    password: str = Field(..., min_length=6, description="Mínimo 6 caracteres")
    nombre: str = Field(..., min_length=2)
    rol: Optional[str] = Field(None, pattern="^(admin|inventory|viewer)$")


class RefreshTokenRequest(BaseModel):
    """Schema para renovar token"""
    refresh_token: str


# ============================================================================
# RESPONSES
# ============================================================================

class UserResponse(BaseModel):
    """Información básica del usuario"""
    id: str
    email: str
    nombre: str
    rol: str
    activo: bool
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Respuesta de login con token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class PerfilResponse(BaseModel):
    """Perfil completo del usuario"""
    id: str
    nombre: str
    email: str
    rol: str
    activo: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
