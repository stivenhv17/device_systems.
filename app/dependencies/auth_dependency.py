from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.security import decode_access_token
from app.dependencies.database_dependency import get_db
from app.models.user_model import User
from app.schemas.auth_schema import TokenData
from app.services import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o no enviado.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        role = payload.get("role")

        if email is None:
            raise credenciales_invalidas

        token_data = TokenData(email=email, role=role)
    except ValueError:
        raise credenciales_invalidas from None

    usuario = user_service.obtener_por_email(token_data.email, db)

    if usuario is None:
        raise credenciales_invalidas

    return usuario


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está inactivo."
        )

    return current_user


def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para realizar esta operación."
        )

    return current_user


def require_admin_or_support(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role not in {"admin", "support"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para realizar esta operación."
        )

    return current_user
