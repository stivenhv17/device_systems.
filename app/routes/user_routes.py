from fastapi import APIRouter, Depends, Query, Response, status

from app.dependencies.user_dependencies import get_user_or_404
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
    description="Obtiene todos los usuarios registrados y permite filtrarlos por rol y estado.",
    response_description="Lista de usuarios."
)
def listar_usuarios(
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None)
):
    usuarios = user_service.obtener_todos()

    if role is not None:
        usuarios = [
            usuario for usuario in usuarios
            if usuario["role"] == role
        ]

    if is_active is not None:
        usuarios = [
            usuario for usuario in usuarios
            if usuario["is_active"] == is_active
        ]

    return usuarios


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Consultar usuario por ID",
    description="Obtiene un usuario específico utilizando su identificador.",
    response_description="Información del usuario encontrado."
)
def obtener_usuario(
    usuario: dict = Depends(get_user_or_404)
):
    return usuario


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Registra un nuevo usuario validando sus datos y evitando correos duplicados.",
    response_description="Usuario creado correctamente."
)
def crear_usuario(usuario: UserCreate):
    return user_service.crear(usuario)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Reemplaza todos los datos de un usuario existente.",
    response_description="Usuario actualizado correctamente."
)
def actualizar_usuario(
    user_id: int,
    datos: UserUpdate,
    usuario: dict = Depends(get_user_or_404)
):
    return user_service.actualizar_completo(user_id, datos)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente",
    description="Modifica únicamente los campos enviados del usuario.",
    response_description="Usuario actualizado parcialmente."
)
def actualizar_usuario_parcial(
    user_id: int,
    datos: UserPatch,
    usuario: dict = Depends(get_user_or_404)
):
    return user_service.actualizar_parcial(user_id, datos)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario existente.",
    response_description="Usuario eliminado correctamente."
)
def eliminar_usuario(
    user_id: int,
    usuario: dict = Depends(get_user_or_404)
):
    user_service.eliminar(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)