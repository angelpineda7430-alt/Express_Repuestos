
from pydantic import BaseModel, Field


class AgregarAlCarrito(BaseModel):
    repuesto_id: int = Field(gt=0)
    cantidad: int = Field(gt=0, le=50)


class ActualizarCantidad(BaseModel):
    cantidad: int = Field(gt=0, le=50)
