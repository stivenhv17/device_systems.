from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import (
    create_access_token,
    get_password_hash,
    verify_password
)
from app.models.user_model import User
from app.schemas.auth_schema import UserLogin, UserRegister
from app.services import user_service


def registrar_usuario(datos: UserRegister, db: Session) -> User:
    usuario_existente = user_service.obtener_por_email(datos.email, db)

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese correo."
        )

    nuevo_usuario = User(
        name=datos.name,
        email=datos.email,
        hashed_password=get_password_hash(datos.password),
        role=datos.role,
        is_active=True
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


def autenticar_usuario(datos: UserLogin, db: Session) -> str:
    usuario = user_service.obtener_por_email(datos.email, db)

    if usuario is None or not verify_password(
        datos.password,
        usuario.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not usuario.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está inactivo."
        )

    return create_access_token(
        data={
            "sub": usuario.email,
            "role": usuario.role
        }
    )
