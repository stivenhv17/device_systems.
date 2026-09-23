from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.user_schema import (
    UserCreate,
    UserPatch,
    UserResponse,
    UserUpdate
)
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Obtiene todos los usuarios y permite filtrarlos por rol, estado y orden.",
    response_description="Lista de usuarios registrados.",
    responses={
        200: {"description": "Usuarios obtenidos correctamente."},
        422: {"description": "Parámetros de consulta inválidos."}
    }
)
def listar_usuarios(
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    ordenar_por: str = Query(
        default="name",
        pattern="^(name|created_at)$"
    ),
    db: Session = Depends(get_db)
):
    return user_service.obtener_todos(
        db,
        role=role,
        is_active=is_active,
        ordenar_por=ordenar_por
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Consultar usuario por ID",
    description="Obtiene un usuario específico utilizando su identificador.",
    response_description="Información del usuario solicitado.",
    responses={
        200: {"description": "Usuario encontrado correctamente."},
        404: {"description": "El usuario solicitado no existe."}
    }
)
def obtener_usuario(
    user_id: int,
    db: Session = Depends(get_db)
):
    return user_service.obtener_por_id(user_id, db)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Registra un nuevo usuario validando sus datos y evitando correos duplicados.",
    response_description="Usuario creado correctamente.",
    responses={
        201: {"description": "Usuario creado correctamente."},
        400: {"description": "El correo electrónico ya está registrado."},
        422: {"description": "Los datos enviados no cumplen las validaciones."}
    }
)
def crear_usuario(
    usuario: UserCreate,
    db: Session = Depends(get_db)
):
    return user_service.crear(usuario, db)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Reemplaza todos los datos de un usuario existente.",
    response_description="Usuario actualizado correctamente.",
    responses={
        200: {"description": "Usuario actualizado correctamente."},
        404: {"description": "El usuario solicitado no existe."},
        400: {"description": "El correo electrónico ya está registrado."},
        422: {"description": "Los datos enviados no cumplen las validaciones."}
    }
)
def actualizar_usuario(
    user_id: int,
    datos: UserUpdate,
    db: Session = Depends(get_db)
):
    return user_service.actualizar_completo(
        user_id,
        datos,
        db
    )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente",
    description="Modifica únicamente los campos enviados del usuario.",
    response_description="Usuario actualizado correctamente.",
    responses={
        200: {"description": "Usuario actualizado correctamente."},
        400: {"description": "La solicitud no contiene campos válidos para actualizar."},
        404: {"description": "El usuario solicitado no existe."},
        422: {"description": "Los datos enviados no cumplen las validaciones."}
    }
)
def actualizar_usuario_parcial(
    user_id: int,
    datos: UserPatch,
    db: Session = Depends(get_db)
):
    return user_service.actualizar_parcial(
        user_id,
        datos,
        db
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario existente.",
    response_description="Usuario eliminado correctamente.",
    responses={
        204: {"description": "Usuario eliminado correctamente."},
        404: {"description": "El usuario solicitado no existe."}
    }
)
def eliminar_usuario(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_service.eliminar(user_id, db)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )