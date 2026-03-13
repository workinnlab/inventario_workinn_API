"""
Inventario CIE API - FastAPI
API para gestión de inventario del CIE usando Supabase
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.v1.endpoints import inventory, prestamos, movimientos, auth, export, dashboard

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para gestión de inventario del CIE",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
# En producción, especificar los orígenes permitidos
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir routers de la API
# Los tags se definen en cada endpoint, no aquí
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(inventory.router, prefix="/api/v1")
app.include_router(prestamos.router, prefix="/api/v1")
app.include_router(movimientos.router, prefix="/api/v1")
app.include_router(export.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")


@app.get("/")
def root():
    """Endpoint raíz - Información de la API"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Endpoint de verificación de salud"""
    return {"status": "healthy"}


# Para producción (Render usa la variable $PORT)
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.DEBUG
    )
