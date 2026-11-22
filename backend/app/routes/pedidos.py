
from fastapi import APIRouter, HTTPException

from app.models.pedido import (
    CrearPedido,
    ActualizarEstadoPedido
)

from app.services.pedido_service import (
    crear_pedido,
    obtener_pedido,
    actualizar_estado
)


router = APIRouter(
    prefix="/pedidos",
    tags=["Gestión de pedidos"]
)


@router.post("/")
def registrar_pedido(datos: CrearPedido):
    """
    Registra una compra y genera un número de pedido.
    """

    try:
        return crear_pedido(datos)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get("/{pedido_id}")
def consultar_pedido(pedido_id: str):
    """
    Consulta un pedido y su historial de seguimiento.
    """

    pedido = obtener_pedido(pedido_id)

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    return pedido


@router.patch("/{pedido_id}/estado")
def cambiar_estado_pedido(
    pedido_id: str,
    datos: ActualizarEstadoPedido
):
    """
    Actualiza el estado del pedido respetando
    las transiciones permitidas.
    """

    try:
        return actualizar_estado(
            pedido_id,
            datos.estado
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
