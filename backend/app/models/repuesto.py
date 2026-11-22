
from pydantic import BaseModel, Field
from typing import Literal


class Repuesto(BaseModel):

    id: int

    codigo: str

    nombre: str

    descripcion: str

    categoria: str

    condicion: Literal["nuevo", "usado"]

    precio: float = Field(gt=0)

    marca_vehiculo: str

    modelo_vehiculo: str

    tipo_vehiculo: str

    anio_desde: int

    anio_hasta: int

    existencia: int

    imagen: str
