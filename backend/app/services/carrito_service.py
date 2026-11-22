
from app.data.catalogo_repuestos import CATALOGO_REPUESTOS


# Almacenamiento temporal de los carritos
CARRITOS = {}


def buscar_repuesto(repuesto_id):

    for repuesto in CATALOGO_REPUESTOS:

        if repuesto["id"] == repuesto_id:
            return repuesto

    return None


def obtener_carrito(carrito_id):

    if carrito_id not in CARRITOS:
        CARRITOS[carrito_id] = {}

    productos = list(CARRITOS[carrito_id].values())

    total = sum(
        producto["subtotal"] for producto in productos
    )

    cantidad_total = sum(
        producto["cantidad"] for producto in productos
    )

    return {
        "carrito_id": carrito_id,
        "productos": productos,
        "cantidad_productos": len(productos),
        "cantidad_total": cantidad_total,
        "total": round(total, 2)
    }


def agregar_producto(carrito_id, repuesto_id, cantidad):

    repuesto = buscar_repuesto(repuesto_id)

    if repuesto is None:
        raise KeyError("El repuesto solicitado no existe")

    if repuesto["existencia"] <= 0:
        raise ValueError("El repuesto no tiene existencias")

    if carrito_id not in CARRITOS:
        CARRITOS[carrito_id] = {}

    carrito = CARRITOS[carrito_id]

    cantidad_actual = 0

    if repuesto_id in carrito:
        cantidad_actual = carrito[repuesto_id]["cantidad"]

    nueva_cantidad = cantidad_actual + cantidad

    if nueva_cantidad > repuesto["existencia"]:
        raise ValueError(
            "La cantidad solicitada supera las existencias disponibles"
        )

    subtotal = nueva_cantidad * repuesto["precio"]

    carrito[repuesto_id] = {
        "repuesto_id": repuesto_id,
        "codigo": repuesto["codigo"],
        "nombre": repuesto["nombre"],
        "condicion": repuesto["condicion"],
        "precio_unitario": repuesto["precio"],
        "cantidad": nueva_cantidad,
        "subtotal": round(subtotal, 2),
        "imagen": repuesto["imagen"]
    }

    return obtener_carrito(carrito_id)


def actualizar_producto(carrito_id, repuesto_id, cantidad):

    if carrito_id not in CARRITOS:
        raise KeyError("El carrito no existe")

    carrito = CARRITOS[carrito_id]

    if repuesto_id not in carrito:
        raise KeyError("El producto no está en el carrito")

    repuesto = buscar_repuesto(repuesto_id)

    if repuesto is None:
        raise KeyError("El repuesto ya no existe")

    if cantidad > repuesto["existencia"]:
        raise ValueError("No hay suficientes existencias")

    carrito[repuesto_id]["cantidad"] = cantidad

    carrito[repuesto_id]["subtotal"] = round(
        carrito[repuesto_id]["precio_unitario"] * cantidad,
        2
    )

    return obtener_carrito(carrito_id)


def eliminar_producto(carrito_id, repuesto_id):

    if carrito_id not in CARRITOS:
        raise KeyError("El carrito no existe")

    carrito = CARRITOS[carrito_id]

    if repuesto_id not in carrito:
        raise KeyError("El producto no está en el carrito")

    del carrito[repuesto_id]

    return obtener_carrito(carrito_id)


def vaciar_carrito(carrito_id):

    if carrito_id not in CARRITOS:
        raise KeyError("El carrito no existe")

    CARRITOS[carrito_id] = {}

    return obtener_carrito(carrito_id)
