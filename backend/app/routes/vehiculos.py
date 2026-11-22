
from fastapi import APIRouter, HTTPException, Query

from app.services.catalogo_service import (
    obtener_tipos_vehiculos,
    obtener_marcas,
    obtener_modelos,
    obtener_anios
)

router = APIRouter(
    prefix="/vehiculos",
    tags=["Catálogo de vehículos"]
)


@router.get("/tipos")
def listar_tipos():
    """
    Lista los tipos de vehículos disponibles.
    """
    return obtener_tipos_vehiculos()


@router.get("/marcas")
def listar_marcas(
    tipo: str = Query(
        ...,
        description="Tipo de vehículo: automovil o motocicleta"
    )
):
    """
    Lista las marcas según el tipo de vehículo.
    """

    resultado = obtener_marcas(tipo.lower())

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Tipo de vehículo no encontrado"
        )

    return {
        "tipo": tipo.lower(),
        "total": len(resultado),
        "marcas": resultado
    }


@router.get("/modelos")
def listar_modelos(
    tipo: str = Query(...),
    marca: str = Query(...)
):
    """
    Lista los modelos correspondientes a una marca.
    """

    resultado = obtener_modelos(
        tipo.lower(),
        marca
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró la marca para ese tipo de vehículo"
        )

    return {
        "tipo": tipo.lower(),
        "marca": marca,
        "total": len(resultado),
        "modelos": resultado
    }


@router.get("/anios")
def listar_anios(
    tipo: str = Query(...),
    marca: str = Query(...),
    modelo: str = Query(...)
):
    """
    Lista los años disponibles para un modelo.
    """

    resultado = obtener_anios(
        tipo.lower(),
        marca,
        modelo
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el modelo solicitado"
        )

    return {
        "tipo": tipo.lower(),
        "marca": marca,
        "modelo": modelo,
        "total": len(resultado),
        "anios": resultado
    }
