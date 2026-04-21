"""
Schemas Pydantic para validación y serialización de datos
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# ============================================================================
# SCHEMAS BASE (Campos compartidos)
# ============================================================================

class EquipoBase(BaseModel):
    """Schema base para Equipo"""
    nombre: str
    marca: str
    codigo: str
    accesorios: Optional[str] = None
    serial: Optional[str] = None
    estado: Optional[str] = None


class EquipoCreate(EquipoBase):
    """Schema para crear un Equipo"""
    pass


class EquipoUpdate(BaseModel):
    """Schema para actualizar un Equipo (todos los campos opcionales)"""
    nombre: Optional[str] = None
    marca: Optional[str] = None
    codigo: Optional[str] = None
    accesorios: Optional[str] = None
    serial: Optional[str] = None
    estado: Optional[str] = None


class EquipoResponse(EquipoBase):
    """Schema para respuesta de Equipo"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime


# ============================================================================
# ELECTRONICA
# ============================================================================

class ElectronicaBase(BaseModel):
    """Schema base para Electrónica"""
    nombre: str
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    en_uso: int = 0
    en_stock: int = 0


class ElectronicaCreate(ElectronicaBase):
    """Schema para crear Electrónica"""
    pass


class ElectronicaUpdate(BaseModel):
    """Schema para actualizar Electrónica"""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    en_uso: Optional[int] = None
    en_stock: Optional[int] = None


class ElectronicaResponse(ElectronicaBase):
    """Schema para respuesta de Electrónica"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    total: int
    created_at: datetime
    updated_at: datetime


# ============================================================================
# ROBOTS
# ============================================================================

class RobotBase(BaseModel):
    """Schema base para Robot"""
    nombre: str
    fuera_de_servicio: int = 0
    en_uso: int = 0
    disponible: int = 0


class RobotCreate(RobotBase):
    """Schema para crear Robot"""
    pass


class RobotUpdate(BaseModel):
    """Schema para actualizar Robot"""
    nombre: Optional[str] = None
    fuera_de_servicio: Optional[int] = None
    en_uso: Optional[int] = None
    disponible: Optional[int] = None


class RobotResponse(RobotBase):
    """Schema para respuesta de Robot"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    total: int
    created_at: datetime
    updated_at: datetime


# ============================================================================
# MATERIALES
# ============================================================================

class MaterialBase(BaseModel):
    """Schema base para Material"""
    color: str
    cantidad: str
    categoria: Optional[str] = None
    usado: int = 0
    en_uso: int = 0
    en_stock: int = 0


class MaterialCreate(MaterialBase):
    """Schema para crear Material"""
    tipo_id: Optional[int] = None


class MaterialUpdate(BaseModel):
    """Schema para actualizar Material"""
    color: Optional[str] = None
    tipo_id: Optional[int] = None
    cantidad: Optional[str] = None
    categoria: Optional[str] = None
    usado: Optional[int] = None
    en_uso: Optional[int] = None
    en_stock: Optional[int] = None


class MaterialResponse(MaterialBase):
    """Schema para respuesta de Material"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    tipo_id: Optional[int]
    total: int
    created_at: datetime
    updated_at: datetime


class TipoMaterialBase(BaseModel):
    """Schema base para Tipo de Material"""
    nombre: str


class TipoMaterialCreate(TipoMaterialBase):
    """Schema para crear Tipo de Material"""
    pass


class TipoMaterialResponse(TipoMaterialBase):
    """Schema para respuesta de Tipo de Material"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int


# ============================================================================
# PRESTATARIOS
# ============================================================================

class PrestatarioBase(BaseModel):
    """Schema base para Prestatario"""
    nombre: str
    telefono: Optional[str] = None
    dependencia: str
    cedula: Optional[str] = None
    email: Optional[str] = None


class PrestatarioCreate(PrestatarioBase):
    """Schema para crear Prestatario"""
    pass


class PrestatarioUpdate(BaseModel):
    """Schema para actualizar Prestatario"""
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    dependencia: Optional[str] = None
    cedula: Optional[str] = None
    email: Optional[str] = None
    activo: Optional[bool] = None


class PrestatarioResponse(PrestatarioBase):
    """Schema para respuesta de Prestatario"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    activo: bool
    created_at: datetime
    updated_at: datetime


# ============================================================================
# PRESTAMOS
# ============================================================================

class PrestamoBase(BaseModel):
    """Schema base para Préstamo"""
    prestatario_id: int
    fecha_limite: Optional[datetime] = None
    estado: str = "activo"
    observaciones: Optional[str] = None


class PrestamoCreate(PrestamoBase):
    """Schema para crear Préstamo"""
    # Uno de estos campos debe tener valor
    equipo_id: Optional[int] = None
    electronica_id: Optional[int] = None
    robot_id: Optional[int] = None
    material_id: Optional[int] = None


class PrestamoUpdate(BaseModel):
    """Schema para actualizar Préstamo"""
    fecha_devolucion: Optional[datetime] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None


class PrestamoResponse(PrestamoBase):
    """Schema para respuesta de Préstamo"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    equipo_id: Optional[int]
    electronica_id: Optional[int]
    robot_id: Optional[int]
    material_id: Optional[int]
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime]
    created_at: datetime
    updated_at: datetime


# ============================================================================
# MOVIMIENTOS
# ============================================================================

class MovimientoBase(BaseModel):
    """Schema base para Movimiento"""
    tipo: str
    cantidad: int = 1
    descripcion: Optional[str] = None
    ubicacion_anterior: Optional[str] = None
    ubicacion_nueva: Optional[str] = None


class MovimientoCreate(MovimientoBase):
    """Schema para crear Movimiento"""
    # Uno de estos campos debe tener valor
    equipo_id: Optional[int] = None
    electronica_id: Optional[int] = None
    robot_id: Optional[int] = None
    material_id: Optional[int] = None
    prestamo_id: Optional[int] = None


class MovimientoResponse(MovimientoBase):
    """Schema para respuesta de Movimiento"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    equipo_id: Optional[int]
    electronica_id: Optional[int]
    robot_id: Optional[int]
    material_id: Optional[int]
    prestamo_id: Optional[int]
    usuario_id: Optional[str]
    usuario_nombre: Optional[str] = None
    created_at: datetime


# ============================================================================
# SCHEMAS PARA RESPUESTAS ANIDADAS
# ============================================================================

class PrestamoConDetallesResponse(PrestamoResponse):
    """Préstamo con información del item y prestatario"""
    prestatario: PrestatarioResponse
    item_nombre: Optional[str] = None
    item_tipo: Optional[str] = None


class MovimientoConDetallesResponse(MovimientoResponse):
    """Movimiento con información del item"""
    item_nombre: Optional[str] = None
    item_tipo: Optional[str] = None
