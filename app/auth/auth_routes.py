from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.auth import auth_service
from app.dependencies.auth_dependency import get_current_active_user
from app.dependencies.database_dependency import get_db
from app.middlewares.request_middleware import limiter
from app.models.user_model import User
from app.schemas.auth_schema import Token, UserLogin, UserRegister
from app.schemas.user_schema import UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description=(
        "Crea un usuario con contraseña segura. "
        "La contraseña se almacena únicamente como hash y nunca se retorna."
    ),
    response_description="Usuario registrado correctamente.",
    responses={
        201: {"description": "Usuario registrado correctamente."},
        400: {"description": "El correo electrónico ya está registrado."},
        422: {"description": "Los datos enviados no cumplen las validaciones."},
        429: {"description": "Se superó el límite de solicitudes."}
    }
)
@limiter.limit("3/minute")
def registrar(
    request: Request,
    datos: UserRegister,
    db: Session = Depends(get_db)
):
    return auth_service.registrar_usuario(datos, db)


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description=(
        "Autentica al usuario y genera un token JWT. "
        "Acepta JSON con email y password, o formulario OAuth2 "
        "con username (correo) y password."
    ),
    response_description="Token JWT generado.",
    responses={
        200: {"description": "Autenticación correcta."},
        401: {"description": "Correo o contraseña incorrectos."},
        403: {"description": "El usuario está inactivo."},
        422: {"description": "Los datos enviados no cumplen las validaciones."},
        429: {"description": "Se superó el límite de solicitudes."}
    }
)
@limiter.limit("5/minute")
async def login(
    request: Request,
    db: Session = Depends(get_db)
):
    content_type = request.headers.get("content-type", "")

    if "application/x-www-form-urlencoded" in content_type:
        form = await request.form()

        datos = UserLogin(
            email=str(form.get("username") or form.get("email") or ""),
            password=str(form.get("password") or "")
        )
    else:
        body = await request.json()

        datos = UserLogin(
            email=body.get("email", ""),
            password=body.get("password", "")
        )

    access_token = auth_service.autenticar_usuario(datos, db)

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Consultar usuario autenticado",
    description=(
        "Retorna los datos del usuario autenticado a partir del token "
        "enviado en Authorization: Bearer <token>. No incluye hashed_password."
    ),
    response_description="Datos del usuario autenticado.",
    responses={
        200: {"description": "Usuario autenticado obtenido correctamente."},
        401: {"description": "Token inválido o no enviado."},
        403: {"description": "El usuario está inactivo."}
    }
)
def leer_usuario_actual(
    current_user: User = Depends(get_current_active_user)
):
    return current_user