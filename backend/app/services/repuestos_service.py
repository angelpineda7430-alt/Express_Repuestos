
from app.data.catalogo_repuestos import CATALOGO_REPUESTOS


def listar_categorias():

    return [
        {"codigo": "MOTOR", "nombre": "Motor"},
        {"codigo": "FRENOS", "nombre": "Sistema de frenos"},
        {"codigo": "ELECTRICO", "nombre": "Sistema eléctrico"},
        {"codigo": "ENFRIAMIENTO", "nombre": "Sistema de enfriamiento"},
        {"codigo": "CARROCERIA", "nombre": "Carrocería"},
        {"codigo": "SUSPENSION", "nombre": "Suspensión"},
        {"codigo": "TRANSMISION", "nombre": "Transmisión"}
    ]


def obtener_repuestos(
    tipo=None,
    marca=None,
    modelo=None,
    anio=None,
    categoria=None,
    condicion=None
):

    resultado = CATALOGO_REPUESTOS.copy()

    if tipo:
        resultado = [
            r for r in resultado
            if r["tipo_vehiculo"] == tipo.lower()
        ]

    if marca:
        resultado = [
            r for r in resultado
            if r["marca_vehiculo"].lower() == marca.lower()
        ]

    if modelo:
        resultado = [
            r for r in resultado
            if r["modelo_vehiculo"].lower() == modelo.lower()
        ]

    if anio is not None:
        resultado = [
            r for r in resultado
            if r["anio_desde"] <= anio <= r["anio_hasta"]
        ]

    if categoria:
        resultado = [
            r for r in resultado
            if r["categoria"] == categoria.upper()
        ]

    if condicion:
        resultado = [
            r for r in resultado
            if r["condicion"] == condicion.lower()
        ]

    return resultado


def obtener_repuesto_por_id(repuesto_id):

    for repuesto in CATALOGO_REPUESTOS:

        if repuesto["id"] == repuesto_id:
            return repuesto

    return None
