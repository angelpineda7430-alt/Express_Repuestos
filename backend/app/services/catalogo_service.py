
from app.data.catalogo import (
    CATALOGO_VEHICULOS,
    ANIOS_DISPONIBLES
)


def obtener_tipos_vehiculos():
    """
    Devuelve los tipos de vehículos disponibles.
    """
    return [
        {
            "codigo": "automovil",
            "nombre": "Automóvil"
        },
        {
            "codigo": "motocicleta",
            "nombre": "Motocicleta"
        }
    ]


def obtener_marcas(tipo):
    """
    Devuelve las marcas según el tipo de vehículo.
    """

    if tipo not in CATALOGO_VEHICULOS:
        return None

    return list(CATALOGO_VEHICULOS[tipo].keys())


def obtener_modelos(tipo, marca):
    """
    Devuelve los modelos de una marca específica.
    """

    if tipo not in CATALOGO_VEHICULOS:
        return None

    catalogo = CATALOGO_VEHICULOS[tipo]

    if marca not in catalogo:
        return None

    return catalogo[marca]


def obtener_anios(tipo, marca, modelo):
    """
    Verifica que el vehículo exista y devuelve
    los años disponibles para la selección.
    """

    modelos = obtener_modelos(tipo, marca)

    if modelos is None or modelo not in modelos:
        return None

    return ANIOS_DISPONIBLES
