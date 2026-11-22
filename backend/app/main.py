


from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION
)

from app.routes.vehiculos import router as vehiculos_router
from app.routes.repuestos import router as repuestos_router
from app.routes.carrito import router as carrito_router
from app.routes.pedidos import router as pedidos_router

# Crear aplicación FastAPI
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION
)


# Directorio principal del proyecto
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Directorio de fotografías
IMAGES_DIR = PROJECT_ROOT / "frontend" / "images"


# Publicar fotografías del catálogo
app.mount(
    "/images",
    StaticFiles(directory=str(IMAGES_DIR), check_dir=False),
    name="images"
)

# Publicar la tienda web
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app.mount(
    "/tienda",
    StaticFiles(
        directory=str(FRONTEND_DIR),
        html=True,
        check_dir=False
    ),
    name="tienda"
)

# Registrar rutas de vehículos
app.include_router(
    vehiculos_router,
    prefix="/api/v1"
)


# Registrar rutas de repuestos
app.include_router(
    repuestos_router,
    prefix="/api/v1"
)

app.include_router(
    carrito_router,
    prefix="/api/v1"
)

app.include_router(
    pedidos_router,
    prefix="/api/v1"
)

# Endpoint principal
@app.get("/")
def inicio():
    return {
        "empresa": APP_NAME,
        "mensaje": "Bienvenido a Express Repuestos",
        "estado": "API funcionando correctamente"
    }


# Endpoint de estado
@app.get("/api/v1/estado")
def verificar_estado():
    return {
        "estado": "Activo",
        "servicio": APP_NAME,
        "version": APP_VERSION
    }
