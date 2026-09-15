from fastapi import HTTPException

from app.data.users_db import usuarios
from app.schemas.user_schema import ROLES_PERMITIDOS


def validar_rol(role: str):
    if role not in ROLES_PERMITIDOS:
        raise HTTPException(
            status_code=400,
            detail="El rol no está permitido."
        )


def obtener_todos():
    return usuarios


def obtener_por_id(user_id: int):
    for usuario in usuarios:
        if usuario["id"] == user_id:
            return usuario

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado."
    )


def crear(usuario):
    validar_rol(usuario.role)

    for usuario_existente in usuarios:
        if usuario_existente["email"].lower() == usuario.email.lower():
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con ese correo."
            )

    nuevo_id = max(usuario["id"] for usuario in usuarios) + 1

    nuevo_usuario = {
        "id": nuevo_id,
        **usuario.model_dump()
    }

    usuarios.append(nuevo_usuario)

    return nuevo_usuario


def actualizar_completo(user_id: int, datos):
    usuario = obtener_por_id(user_id)

    validar_rol(datos.role)

    for usuario_existente in usuarios:
        if (
            usuario_existente["email"].lower() == datos.email.lower()
            and usuario_existente["id"] != user_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con ese correo."
            )

    usuario.update(datos.model_dump())

    return usuario


def actualizar_parcial(user_id: int, datos):
    usuario = obtener_por_id(user_id)

    cambios = datos.model_dump(exclude_unset=True)

    if not cambios:
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar."
        )

    if "role" in cambios:
        validar_rol(cambios["role"])

    if "email" in cambios:
        for usuario_existente in usuarios:
            if (
                usuario_existente["email"].lower() == cambios["email"].lower()
                and usuario_existente["id"] != user_id
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe un usuario con ese correo."
                )

    usuario.update(cambios)

    return usuario


def eliminar(user_id: int):
    usuario = obtener_por_id(user_id)

    usuarios.remove(usuario)