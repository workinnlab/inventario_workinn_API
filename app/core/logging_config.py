"""
Logging personalizado para la API - Inventario CIE

Configura logging detallado para auditoría y debugging.
"""

import logging
import sys
from datetime import datetime
from typing import Optional

# Configurar formato de logs
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Crear logger principal
logger = logging.getLogger("inventario_cie")
logger.setLevel(logging.INFO)

# Handler para consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# Handler para archivo (opcional - solo en desarrollo)
try:
    file_handler = logging.FileHandler(f"logs/inventario_cie_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(file_handler)
except FileNotFoundError:
    pass  # Si no existe el directorio logs, solo usar consola

logger.addHandler(console_handler)

# Funciones helper para logging de auditoría
def log_audit(action: str, user_id: Optional[str], resource: str, resource_id: Optional[int], details: Optional[str] = None):
    """
    Registrar acción de auditoría
    
    Args:
        action: Tipo de acción (CREATE, UPDATE, DELETE, LOGIN, LOGOUT)
        user_id: ID del usuario que realiza la acción
        resource: Recurso afectado (equipos, prestamos, etc.)
        resource_id: ID del recurso
        details: Detalles adicionales
    """
    log_message = f"AUDIT: {action} on {resource}"
    if resource_id:
        log_message += f"#{resource_id}"
    if user_id:
        log_message += f" by user#{user_id}"
    if details:
        log_message += f" - {details}"
    
    logger.info(log_message)

def log_login(user_email: str, success: bool, ip_address: Optional[str] = None):
    """Registrar intento de login"""
    status = "SUCCESS" if success else "FAILED"
    message = f"AUDIT: LOGIN {status} for {user_email}"
    if ip_address:
        message += f" from {ip_address}"
    logger.info(message)

def log_error(endpoint: str, error: str, user_id: Optional[str] = None):
    """Registrar error"""
    message = f"ERROR: {endpoint}"
    if user_id:
        message += f" by user#{user_id}"
    message += f" - {error}"
    logger.error(message)

# Exportar logger
__all__ = ["logger", "log_audit", "log_login", "log_error"]
