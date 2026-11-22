
from uuid import uuid4
from datetime import datetime

from app.services.carrito_service import CARRITOS
from app.data.catalogo_repuestos import CATALOGO_REPUESTOS


# Almacenamiento temporal de pedidos
PEDIDOS = {}


def buscar_producto(repuesto_id):

    for producto in CATALOGO_REPUESTOS:
        if producto["id"] == repuesto_id:
            return producto

    return None


def crear_pedido(datos):

    carrito_id = datos.carrito_id

    # Verificar que exista el carrito
    if carrito_id not in CARRITOS:
        raise ValueError("El carrito no existe")

    carrito = CARRITOS[carrito_id]

    if not carrito:
        raise ValueError("El carrito está vacío")

    # Validar dirección para entregas a domicilio
    if datos.modalidad_entrega == "domicilio":
        if not datos.direccion or not datos.direccion.strip():
            raise ValueError(
                "Debe ingresar la dirección de entrega"
            )

    # Validar todos los productos antes de modificar inventario
    productos_pedido = []

    for item in carrito.values():

        producto = buscar_producto(item["repuesto_id"])

        if producto is None:
            raise ValueError(
                f"El producto {item['codigo']} ya no existe"
            )

        if producto["existencia"] < item["cantidad"]:
            raise ValueError(
                f"Existencias insuficientes para {item['nombre']}"
            )

        productos_pedido.append({
            "repuesto_id": producto["id"],
            "codigo": producto["codigo"],
            "nombre": producto["nombre"],
            "precio_unitario": producto["precio"],
            "cantidad": item["cantidad"],
            "subtotal": item["subtotal"]
        })

    # Calcular total
    total = round(
        sum(p["subtotal"] for p in productos_pedido),
        2
    )

    # Generar identificador único
    pedido_id = "PED-" + uuid4().hex[:8].upper()

    # Determinar estado inicial
    estado = "pendiente"

    pedido = {
        "pedido_id": pedido_id,
        "fecha": datetime.now().isoformat(),
        "cliente": {
            "nombre": datos.nombre_cliente,
            "celular": datos.celular,
            "documento": datos.documento
        },
        "modalidad_entrega": datos.modalidad_entrega,
        "direccion": (
            datos.direccion.strip()
            if datos.modalidad_entrega == "domicilio"
            else None
        ),
        "productos": productos_pedido,
        "cantidad_total": sum(
            p["cantidad"] for p in productos_pedido
        ),
        "total": total,
        "estado": estado,
        "historial": [
            {
                "estado": estado,
                "fecha": datetime.now().isoformat(),
                "observacion": "Pedido registrado correctamente"
            }
        ]
    }

    # Descontar existencias después de validar todos los productos
    for item in productos_pedido:

        producto = buscar_producto(item["repuesto_id"])

        producto["existencia"] -= item["cantidad"]

    # Registrar pedido
    PEDIDOS[pedido_id] = pedido

    # Vaciar el carrito después de confirmar el pedido
    CARRITOS[carrito_id] = {}

    return pedido


def obtener_pedido(pedido_id):

    return PEDIDOS.get(pedido_id)


def actualizar_estado(pedido_id, nuevo_estado):

    pedido = PEDIDOS.get(pedido_id)

    if pedido is None:
        raise KeyError("Pedido no encontrado")

    estado_actual = pedido["estado"]

    # Definir transiciones permitidas
    transiciones = {
        "pendiente": ["preparado", "cancelado"],
        "preparado": [
            "listo_para_retiro",
            "despachado",
            "cancelado"
        ],
        "listo_para_retiro": ["entregado"],
        "despachado": ["en_camino"],
        "en_camino": ["entregado"]
    }

    permitidos = transiciones.get(estado_actual, [])

    if nuevo_estado not in permitidos:
        raise ValueError(
            f"No se puede cambiar de {estado_actual} a {nuevo_estado}"
        )

    # Si se cancela, devolver las existencias
    if nuevo_estado == "cancelado":

        for item in pedido["productos"]:

            producto = buscar_producto(item["repuesto_id"])

            if producto:
                producto["existencia"] += item["cantidad"]

    pedido["estado"] = nuevo_estado

    pedido["historial"].append({
        "estado": nuevo_estado,
        "fecha": datetime.now().isoformat(),
        "observacion": "Estado actualizado correctamente"
    })

    return pedido
