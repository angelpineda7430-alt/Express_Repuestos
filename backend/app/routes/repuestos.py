
from fastapi import APIRouter, HTTPException, Query
from typing import Literal, Optional, List

from app.models.repuesto import Repuesto

from app.services.repuestos_service import (
    listar_categorias,
    obtener_repuestos,
    obtener_repuesto_por_id
)

router = APIRouter(
    prefix="/repuestos",
    tags=["Catálogo de repuestos"]
)


@router.get("/categorias")
def consultar_categorias():
    """
    Lista las categorías de repuestos disponibles.
    """
    return listar_categorias()


@router.get("/", response_model=List[Repuesto])
def consultar_repuestos(
    tipo: Optional[str] = Query(None),
    marca: Optional[str] = Query(None),
    modelo: Optional[str] = Query(None),
    anio: Optional[int] = Query(None, ge=1900, le=2100),
    categoria: Optional[str] = Query(None),
    condicion: Optional[
        Literal["nuevo", "usado"]
    ] = Query(None)
):
    """
    Consulta los repuestos aplicando filtros opcionales.
    """

    if tipo and tipo.lower() not in ["automovil", "motocicleta"]:
        raise HTTPException(
            status_code=400,
            detail="Tipo de vehículo inválido"
        )

    if anio is not None and not marca:
        raise HTTPException(
            status_code=400,
            detail="Debe especificar la marca cuando selecciona un año"
        )

    if modelo and not marca:
        raise HTTPException(
            status_code=400,
            detail="Debe especificar la marca cuando selecciona un modelo"
        )

    if marca and not tipo:
        raise HTTPException(
            status_code=400,
            detail="Debe especificar el tipo de vehículo cuando selecciona una marca"
        )

    resultado = obtener_repuestos(
        tipo=tipo,
        marca=marca,
        modelo=modelo,
        anio=anio,
        categoria=categoria,
        condicion=condicion
    )

    return resultado


@router.get("/{repuesto_id}", response_model=Repuesto)
def consultar_repuesto(repuesto_id: int):
    """
    Consulta las especificaciones de un repuesto específico.
    """

    repuesto = obtener_repuesto_por_id(repuesto_id)

    if repuesto is None:
        raise HTTPException(
            status_code=404,
            detail="Repuesto no encontrado"
        )

    return repuesto
