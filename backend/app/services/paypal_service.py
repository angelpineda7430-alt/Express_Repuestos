
import os
import httpx

from fastapi import HTTPException


PAYPAL_BASE_URL = (
    "https://api-m.sandbox.paypal.com"
    if os.getenv("PAYPAL_MODE", "sandbox") == "sandbox"
    else "https://api-m.paypal.com"
)


def obtener_access_token():
    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise HTTPException(
            status_code=500,
            detail="Credenciales de PayPal no configuradas."
        )

    try:
        respuesta = httpx.post(
            f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            auth=(client_id, client_secret),
            data={"grant_type": "client_credentials"},
            headers={"Accept": "application/json"},
            timeout=30
        )

        respuesta.raise_for_status()

        return respuesta.json()["access_token"]

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="No fue posible conectar con PayPal."
        )


def crear_orden_paypal(total, pedido_id):

    token = obtener_access_token()

    try:
        respuesta = httpx.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "reference_id": pedido_id,
                        "description": f"Express Repuestos - {pedido_id}",
                        "amount": {
                            "currency_code": "USD",
                            "value": f"{total:.2f}"
                        }
                    }
                ]
            },
            timeout=30
        )

        respuesta.raise_for_status()

        return respuesta.json()

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="No fue posible crear la orden de PayPal."
        )


def capturar_orden_paypal(paypal_order_id):

    token = obtener_access_token()

    try:
        respuesta = httpx.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders/"
            f"{paypal_order_id}/capture",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={},
            timeout=30
        )

        respuesta.raise_for_status()

        return respuesta.json()

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="No fue posible capturar el pago en PayPal."
        )
