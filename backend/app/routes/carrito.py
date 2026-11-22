

from fastapi import APIRouter, HTTPException

from app.models.carrito import (
    AgregarAlCarrito,
    ActualizarCantidad
)

from app.services.carrito_service import (
    obtener_carrito,
    agregar_producto,
    actualizar_producto,
    eliminar_producto,
    vaciar_carrito
)


router = APIRouter(
    prefix="/carrito",
    tags=["Carrito de compras"]
)


@router.get("/{carrito_id}")
def consultar_carrito(carrito_id: str):

    return obtener_carrito(carrito_id)


@router.post("/{carrito_id}/items")
def agregar_item(
    carrito_id: str,
    datos: AgregarAlCarrito
):

    try:
        return agregar_producto(
            carrito_id,
            datos.repuesto_id,
            datos.cantidad
        )

    except KeyError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.patch("/{carrito_id}/items/{repuesto_id}")
def modificar_item(
    carrito_id: str,
    repuesto_id: int,
    datos: ActualizarCantidad
):

    try:
        return actualizar_producto(
            carrito_id,
            repuesto_id,
            datos.cantidad
        )

    except KeyError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.delete("/{carrito_id}/items/{repuesto_id}")
def quitar_item(carrito_id: str, repuesto_id: int):

    try:
        return eliminar_producto(
            carrito_id,
            repuesto_id
        )

    except KeyError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete("/{carrito_id}")
def limpiar_carrito(carrito_id: str):

    try:
        return vaciar_carrito(carrito_id)

    except KeyError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
