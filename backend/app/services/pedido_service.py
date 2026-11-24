
from uuid import uuid4
from datetime import datetime

from app.services.carrito_service import CARRITOS
from app.data.catalogo_repuestos import CATALOGO_REPUESTOS
from app.services.paypal_service import crear_orden_paypal


# Almacenamiento temporal de pedidos
PEDIDOS = {}


def buscar_producto(repuesto_id):

    for producto in CATALOGO_REPUESTOS:
        if producto["id"] == repuesto_id:
            return producto

    return None


def preparar_datos_pedido(datos):

    carrito_id = datos.carrito_id

    if carrito_id not in CARRITOS:
        raise ValueError("El carrito no existe")

    carrito = CARRITOS[carrito_id]

    if not carrito:
        raise ValueError("El carrito está vacío")

    if datos.modalidad_entrega == "domicilio":
        if not datos.direccion or not datos.direccion.strip():
            raise ValueError("Debe ingresar la dirección de entrega")

    productos_pedido = []

    for item in carrito.values():

        producto = buscar_producto(item["repuesto_id"])

        if producto is None:
            raise ValueError(
                f"El producto {item['codigo']} ya no existe"
            )

        cantidad = item["cantidad"]

        if cantidad <= 0:
            raise ValueError("La cantidad del producto no es válida")

        if producto["existencia"] < cantidad:
            raise ValueError(
                f"Existencias insuficientes para {item['nombre']}"
            )

        precio = producto["precio"]
        subtotal = round(precio * cantidad, 2)

        productos_pedido.append({
            "repuesto_id": producto["id"],
            "codigo": producto["codigo"],
            "nombre": producto["nombre"],
            "precio_unitario": precio,
            "cantidad": cantidad,
            "subtotal": subtotal
        })

    total = round(
        sum(p["subtotal"] for p in productos_pedido),
        2
    )

    if total <= 0:
        raise ValueError("El total del pedido no es válido")

    return productos_pedido, total


def construir_pedido(datos, clerk_user_id, productos, total):

    pedido_id = "PED-" + uuid4().hex[:8].upper()
    fecha = datetime.now().isoformat()

    return {
        "pedido_id": pedido_id,
        "clerk_user_id": clerk_user_id,
        "carrito_id": datos.carrito_id,
        "fecha": fecha,
        "metodo_pago": datos.metodo_pago,
        "estado_pago": "pendiente",
        "cliente": {
            "nombre": datos.nombre_cliente,
            "celular": datos.celular,
            "documento": datos.documento
        },
        
"modalidad_entrega": datos.modalidad_entrega,

"direccion": (
    datos.direccion.strip()
    if datos.modalidad_entrega == "domicilio" and datos.direccion
    else None
),

"referencia": (
    datos.referencia.strip()
    if datos.modalidad_entrega == "domicilio" and datos.referencia
    else None
),

"latitud": (
    datos.latitud
    if datos.modalidad_entrega == "domicilio"
    else None
),
        "longitud": (
            datos.longitud
            if datos.modalidad_entrega == "domicilio"
            else None
        ),

        # Productos incluidos en el pedido
        "productos": productos,

        # Cantidad total de unidades
        "cantidad_total": sum(
            p["cantidad"] for p in productos
        ),

        "total": total,
        "estado": "pendiente",
        "historial": [
            {
                "estado": "pendiente",
                "fecha": fecha,
                "observacion": "Pedido registrado correctamente"
            }
        ]
    }


def validar_existencias_pedido(pedido):

    for item in pedido["productos"]:

        producto = buscar_producto(item["repuesto_id"])

        if producto is None:
            raise ValueError(
                f"El producto {item['codigo']} ya no existe"
            )

        if producto["existencia"] < item["cantidad"]:
            raise ValueError(
                f"Existencias insuficientes para {item['nombre']}"
            )

    return True

def finalizar_pedido(pedido):

    # Volver a validar existencias antes de descontarlas
    for item in pedido["productos"]:

        producto = buscar_producto(item["repuesto_id"])

        if producto is None:
            raise ValueError(
                f"El producto {item['codigo']} ya no existe"
            )

        if producto["existencia"] < item["cantidad"]:
            raise ValueError(
                f"Existencias insuficientes para {item['nombre']}"
            )

    # Descontar existencias después de validar todos los productos
    for item in pedido["productos"]:

        producto = buscar_producto(item["repuesto_id"])
        producto["existencia"] -= item["cantidad"]

    # Vaciar el carrito
    CARRITOS[pedido["carrito_id"]] = {}

    pedido["estado"] = "pendiente"

    pedido["historial"].append({
        "estado": "pendiente",
        "fecha": datetime.now().isoformat(),
        "observacion": "Pedido confirmado correctamente"
    })

    return pedido


def crear_pedido(datos, clerk_user_id):

    # Este proceso se conserva para pago en efectivo
    if datos.metodo_pago != "efectivo":
        raise ValueError(
            "Para pagar con tarjeta debe utilizar el proceso de PayPal"
        )

    productos, total = preparar_datos_pedido(datos)

    pedido = construir_pedido(
        datos,
        clerk_user_id,
        productos,
        total
    )

    pedido = finalizar_pedido(pedido)

    PEDIDOS[pedido["pedido_id"]] = pedido

    return pedido


def crear_pedido_tarjeta(datos, clerk_user_id):

    # Validar carrito y calcular total en el backend
    productos, total = preparar_datos_pedido(datos)

    pedido = construir_pedido(
        datos,
        clerk_user_id,
        productos,
        total
    )

    # Crear orden de PayPal con el total calculado en el servidor
    orden_paypal = crear_orden_paypal(
        total,
        pedido["pedido_id"]
    )

    pedido["paypal_order_id"] = orden_paypal["id"]
    pedido["estado"] = "pendiente_pago"

    pedido["historial"].append({
        "estado": "pendiente_pago",
        "fecha": datetime.now().isoformat(),
        "observacion": "Esperando confirmación del pago en PayPal"
    })

    # Todavía no se descuenta inventario ni se vacía el carrito
    PEDIDOS[pedido["pedido_id"]] = pedido

    return {
        "pedido_id": pedido["pedido_id"],
        "paypal_order_id": orden_paypal["id"],
        "total": total,
        "estado": "pendiente_pago"
    }


def confirmar_pago_tarjeta(pedido_id, clerk_user_id, captura):

    pedido = PEDIDOS.get(pedido_id)

    if pedido is None:
        raise KeyError("Pedido no encontrado")

    if pedido["clerk_user_id"] != clerk_user_id:
        raise KeyError("Pedido no encontrado")

    if pedido["estado"] != "pendiente_pago":
        raise ValueError("El pedido no está pendiente de pago")

    # Verificar que PayPal haya completado el pago
    if captura.get("status") != "COMPLETED":
        raise ValueError("PayPal no confirmó el pago")

    if captura.get("id") != pedido["paypal_order_id"]:
        raise ValueError("La orden de PayPal no coincide con el pedido")

    unidades = captura.get("purchase_units", [])

    if not unidades:
        raise ValueError("PayPal no devolvió información del pago")

    unidad = unidades[0]

    if unidad.get("reference_id") != pedido_id:
        raise ValueError("La referencia del pago no coincide")

    capturas = unidad.get("payments", {}).get("captures", [])

    if not capturas:
        raise ValueError("PayPal no devolvió la captura del pago")

    pago = capturas[0]

    if pago.get("status") != "COMPLETED":
        raise ValueError("La captura del pago no está completada")

    importe = pago.get("amount", {})

    if importe.get("currency_code") != "USD":
        raise ValueError("La moneda del pago no es válida")

    if importe.get("value") != f"{pedido['total']:.2f}":
        raise ValueError("El importe pagado no coincide con el pedido")

    # El pago está confirmado
    pedido["estado_pago"] = "aprobado"
    pedido["paypal_capture_id"] = pago.get("id")

    pedido["historial"].append({
        "estado": "pago_aprobado",
        "fecha": datetime.now().isoformat(),
        "observacion": "Pago confirmado correctamente por PayPal"
    })

    # Ahora sí se descuentan existencias y se vacía el carrito
    return finalizar_pedido(pedido)


def obtener_pedido(pedido_id):

    return PEDIDOS.get(pedido_id)


def actualizar_estado(pedido_id, nuevo_estado):

    pedido = PEDIDOS.get(pedido_id)

    if pedido is None:
        raise KeyError("Pedido no encontrado")

    estado_actual = pedido["estado"]

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
