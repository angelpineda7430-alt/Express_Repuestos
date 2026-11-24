
from fastapi import APIRouter, HTTPException, Depends

from app.auth import verificar_usuario
from app.models.pedido import CrearPedido, ActualizarEstadoPedido

from app.services.pedido_service import (
    crear_pedido,
    crear_pedido_tarjeta,
    confirmar_pago_tarjeta,
    validar_existencias_pedido,
    obtener_pedido,
    actualizar_estado
)

from app.services.paypal_service import capturar_orden_paypal


router = APIRouter(
    prefix="/pedidos",
    tags=["Gestión de pedidos"]
)


@router.post("/")
def registrar_pedido(
    datos: CrearPedido,
    clerk_user_id: str = Depends(verificar_usuario)
):
    try:
        return crear_pedido(datos, clerk_user_id)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/crear-pago")
def registrar_pedido_tarjeta(
    datos: CrearPedido,
    clerk_user_id: str = Depends(verificar_usuario)
):
    if datos.metodo_pago != "tarjeta":
        raise HTTPException(
            status_code=400,
            detail="Este proceso es exclusivo para pagos con tarjeta."
        )

    try:
        return crear_pedido_tarjeta(datos, clerk_user_id)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )



@router.post("/{pedido_id}/capturar-pago")
def confirmar_pago(
    pedido_id: str,
    clerk_user_id: str = Depends(verificar_usuario)
):
    pedido = obtener_pedido(pedido_id)

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    if pedido.get("clerk_user_id") != clerk_user_id:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    if pedido.get("estado") != "pendiente_pago":
        raise HTTPException(
            status_code=400,
            detail="El pedido no está pendiente de pago."
        )

    try:
        # Comprobar existencias antes de cobrar
        validar_existencias_pedido(pedido)

        # Capturar el pago utilizando el ID guardado por el backend
        captura = capturar_orden_paypal(
            pedido["paypal_order_id"]
        )

        # Verificar la respuesta y finalizar el pedido
        return confirmar_pago_tarjeta(
            pedido_id,
            clerk_user_id,
            captura
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )



@router.get("/{pedido_id}")
def consultar_pedido(
    pedido_id: str,
    clerk_user_id: str = Depends(verificar_usuario)
):
    pedido = obtener_pedido(pedido_id)

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    if pedido.get("clerk_user_id") != clerk_user_id:
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
