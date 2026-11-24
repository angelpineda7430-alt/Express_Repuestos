
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import HTTPException, Request

from clerk_backend_api.security import authenticate_request
from clerk_backend_api.security.types import AuthenticateRequestOptions


# Cargar las variables del archivo backend/.env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def verificar_usuario(request: Request) -> str:
    """
    Verifica el token de sesión de Clerk.
    Retorna el identificador del usuario autenticado.
    """

    secret_key = os.getenv("CLERK_SECRET_KEY")
    jwt_key = os.getenv("CLERK_JWT_KEY")

    authorized_parties = [
        origen.strip()
        for origen in os.getenv(
            "CLERK_AUTHORIZED_PARTIES", ""
        ).split(",")
        if origen.strip()
    ]

    if not secret_key or not jwt_key:
        raise HTTPException(
            status_code=500,
            detail="La configuración de Clerk está incompleta."
        )

    if not authorized_parties:
        raise HTTPException(
            status_code=500,
            detail="No se configuraron los orígenes autorizados."
        )

    try:
        estado = authenticate_request(
            request,
            AuthenticateRequestOptions(
                secret_key=secret_key,
                jwt_key=jwt_key,
                authorized_parties=authorized_parties,
                accepts_token=["session_token"]
            )
        )

        if not estado.is_signed_in:
            raise HTTPException(
                status_code=401,
                detail="Debes iniciar sesión para continuar."
            )

        return estado.payload["sub"]

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token de autenticación inválido o vencido."
        )
