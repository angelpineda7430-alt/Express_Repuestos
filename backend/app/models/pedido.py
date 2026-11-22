
from typing import Literal, Optional
from pydantic import BaseModel, Field


class CrearPedido(BaseModel):

    carrito_id: str = Field(min_length=1, max_length=100)

    nombre_cliente: str = Field(min_length=3, max_length=120)

    celular: str = Field(min_length=8, max_length=20)

    documento: str = Field(min_length=5, max_length=30)

    modalidad_entrega: Literal["sucursal", "domicilio"]

    direccion: Optional[str] = Field(
        default=None,
        max_length=300
    )


class ActualizarEstadoPedido(BaseModel):

    estado: Literal[
        "preparado",
        "listo_para_retiro",
        "despachado",
        "en_camino",
        "entregado",
        "cancelado"
    ]
