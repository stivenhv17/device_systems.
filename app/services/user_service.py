from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import ROLES_PERMITIDOS


def validar_rol(role: str):
    if role not in ROLES_PERMITIDOS:
        raise HTTPException(
            status_code=400,
            detail="El rol no está permitido."
        )


def obtener_todos(
    db: Session,
    role: str | None = None,
    is_active: bool | None = None,
    ordenar_por: str = "name"
):
    consulta = select(User)

    if role is not None:
        consulta = consulta.where(User.role == role)

    if is_active is not None:
        consulta = consulta.where(User.is_active == is_active)

    if ordenar_por == "created_at":
        consulta = consulta.order_by(User.created_at.desc())
    else:
        consulta = consulta.order_by(User.name.asc())

    return db.scalars(consulta).all()


def obtener_por_id(user_id: int, db: Session):
    usuario = db.get(User, user_id)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado."
        )

    return usuario


def obtener_por_email(email: str, db: Session):
    return db.scalar(
        select(User).where(User.email == email)
    )


def crear(usuario, db: Session):
    validar_rol(usuario.role)

    usuario_existente = obtener_por_email(usuario.email, db)

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario con ese correo."
        )

    nuevo_usuario = User(
        name=usuario.name,
        email=usuario.email,
        role=usuario.role,
        is_active=usuario.is_active
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


def actualizar_completo(
    user_id: int,
    datos,
    db: Session
):
    usuario = obtener_por_id(user_id, db)

    validar_rol(datos.role)

    usuario_existente = db.scalar(
        select(User).where(
            User.email == datos.email,
            User.id != user_id
        )
    )

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario con ese correo."
        )

    usuario.name = datos.name
    usuario.email = datos.email
    usuario.role = datos.role
    usuario.is_active = datos.is_active

    db.commit()
    db.refresh(usuario)

    return usuario


def actualizar_parcial(
    user_id: int,
    datos,
    db: Session
):
    usuario = obtener_por_id(user_id, db)

    cambios = datos.model_dump(exclude_unset=True)

    if not cambios:
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar."
        )

    if "role" in cambios:
        validar_rol(cambios["role"])

    if "email" in cambios:
        usuario_existente = db.scalar(
            select(User).where(
                User.email == cambios["email"],
                User.id != user_id
            )
        )

        if usuario_existente:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con ese correo."
            )

    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)

    return usuario


def eliminar(user_id: int, db: Session):
    usuario = obtener_por_id(user_id, db)

    db.delete(usuario)
    db.commit()