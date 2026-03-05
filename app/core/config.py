"""
Configuración central de la aplicación
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno"""

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str  # anon/public key
    SUPABASE_SERVICE_KEY: str  # service_role key (más privilegiada)

    # JWT
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App
    APP_NAME: str = "Inventario CIE API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    @property
    def database_url(self) -> str:
        """URL de conexión a PostgreSQL (Supabase)"""
        # Extraer el host del URL de Supabase
        # https://xyzcompany.supabase.co -> xyzcompany.supabase.co
        host = self.SUPABASE_URL.replace("https://", "").rstrip("/")
        # Formato: postgresql://postgres:[SERVICE_ROLE_KEY]@[HOST]:[PORT]/postgres
        return f"postgresql://postgres:{self.SUPABASE_SERVICE_KEY}@{host}:5432/postgres"

    @property
    def supabase_rest_url(self) -> str:
        """URL base para la API REST de Supabase"""
        return f"{self.SUPABASE_URL}/rest/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Obtiene la configuración de la aplicación (singleton con caché)
    Returns:
        Settings: Configuración cargada
    """
    return Settings()


# Instancia global de configuración
settings = get_settings()
