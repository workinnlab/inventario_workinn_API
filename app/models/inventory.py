"""
Modelos SQLAlchemy para las tablas de la base de datos
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class Equipo(Base):
    """Modelo para la tabla 'equipos'"""
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)
    marca = Column(Text, nullable=False)
    codigo = Column(Text, unique=True, nullable=False, index=True)
    accesorios = Column(Text)
    serial = Column(Text)
    estado = Column(Text, check_constraint="estado IN ('disponible', 'en uso', 'prestado', 'mantenimiento', 'dañado', 'arreglado')")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    prestamos = relationship("Prestamo", back_populates="equipo", cascade="all, delete-orphan")
    movimientos = relationship("Movimiento", back_populates="equipo", cascade="all, delete-orphan")


class Electronica(Base):
    """Modelo para la tabla 'electronica'"""
    __tablename__ = "electronica"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)
    descripcion = Column(Text)
    tipo = Column(Text)
    en_uso = Column(Integer, default=0)
    en_stock = Column(Integer, default=0)
    total = Column(Integer)  # Columna generada
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    prestamos = relationship("Prestamo", back_populates="electronica", cascade="all, delete-orphan")
    movimientos = relationship("Movimiento", back_populates="electronica", cascade="all, delete-orphan")


class Robot(Base):
    """Modelo para la tabla 'robots'"""
    __tablename__ = "robots"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)
    fuera_de_servicio = Column(Integer, default=0)
    en_uso = Column(Integer, default=0)
    disponible = Column(Integer, default=0)
    total = Column(Integer)  # Columna generada
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    prestamos = relationship("Prestamo", back_populates="robot", cascade="all, delete-orphan")
    movimientos = relationship("Movimiento", back_populates="robot", cascade="all, delete-orphan")


class TipoMaterial(Base):
    """Modelo para la tabla 'tipos_materiales'"""
    __tablename__ = "tipos_materiales"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False, unique=True)
    
    # Relaciones
    materiales = relationship("Material", back_populates="tipo")


class Material(Base):
    """Modelo para la tabla 'materiales'"""
    __tablename__ = "materiales"
    
    id = Column(Integer, primary_key=True, index=True)
    color = Column(Text, nullable=False)
    tipo_id = Column(Integer, ForeignKey("tipos_materiales.id"))
    cantidad = Column(Text, nullable=False)
    categoria = Column(Text)
    usado = Column(Integer, default=0)
    en_uso = Column(Integer, default=0)
    en_stock = Column(Integer, default=0)
    total = Column(Integer)  # Columna generada
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    tipo = relationship("TipoMaterial", back_populates="materiales")
    prestamos = relationship("Prestamo", back_populates="material", cascade="all, delete-orphan")
    movimientos = relationship("Movimiento", back_populates="material", cascade="all, delete-orphan")


class Prestatario(Base):
    """Modelo para la tabla 'prestatarios'"""
    __tablename__ = "prestatarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)
    telefono = Column(Text)
    dependencia = Column(Text, nullable=False)
    cedula = Column(Text)
    email = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    prestamos = relationship("Prestamo", back_populates="prestatario", cascade="all, delete-orphan")


class Prestamo(Base):
    """Modelo para la tabla 'prestamos'"""
    __tablename__ = "prestamos"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # FKs polimórficas (4 columnas separadas)
    equipo_id = Column(Integer, ForeignKey("equipos.id"))
    electronica_id = Column(Integer, ForeignKey("electronica.id"))
    robot_id = Column(Integer, ForeignKey("robots.id"))
    material_id = Column(Integer, ForeignKey("materiales.id"))
    
    # Prestatario
    prestatario_id = Column(Integer, ForeignKey("prestatarios.id"), nullable=False)
    
    # Fechas
    fecha_prestamo = Column(DateTime(timezone=True), server_default=func.now())
    fecha_devolucion = Column(DateTime(timezone=True))
    fecha_limite = Column(DateTime(timezone=True))
    
    # Estado
    estado = Column(Text, nullable=False)
    observaciones = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    equipo = relationship("Equipo", back_populates="prestamos")
    electronica = relationship("Electronica", back_populates="prestamos")
    robot = relationship("Robot", back_populates="prestamos")
    material = relationship("Material", back_populates="prestamos")
    prestatario = relationship("Prestatario", back_populates="prestamos")
    movimientos = relationship("Movimiento", back_populates="prestamo", cascade="all, delete-orphan")


class Movimiento(Base):
    """Modelo para la tabla 'movimientos'"""
    __tablename__ = "movimientos"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Tipo de movimiento
    tipo = Column(Text, nullable=False)
    
    # FKs polimórficas (4 columnas separadas)
    equipo_id = Column(Integer, ForeignKey("equipos.id"))
    electronica_id = Column(Integer, ForeignKey("electronica.id"))
    robot_id = Column(Integer, ForeignKey("robots.id"))
    material_id = Column(Integer, ForeignKey("materiales.id"))
    
    # Cantidad
    cantidad = Column(Integer, default=1)
    
    # Relación con préstamo
    prestamo_id = Column(Integer, ForeignKey("prestamos.id"))
    
    # Usuario (Supabase Auth)
    usuario_id = Column(Text)  # UUID como string
    
    # Descripción
    descripcion = Column(Text)
    
    # Metadata
    ubicacion_anterior = Column(Text)
    ubicacion_nueva = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    equipo = relationship("Equipo", back_populates="movimientos")
    electronica = relationship("Electronica", back_populates="movimientos")
    robot = relationship("Robot", back_populates="movimientos")
    material = relationship("Material", back_populates="movimientos")
    prestamo = relationship("Prestamo", back_populates="movimientos")
