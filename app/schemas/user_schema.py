
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator
)


ROLES_PERMITIDOS = {"admin", "support", "user"}


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    role: str
    is_active: bool = True

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Stiven Hurtado",
                "email": "stiven@sena.edu.co",
                "password": "ClaveSegura1",
                "role": "user",
                "is_active": True
            }
        }
    )

    @field_validator("role")
    @classmethod
    def validar_rol(cls, value: str) -> str:
        if value not in ROLES_PERMITIDOS:
            raise ValueError(
                "El rol no está permitido. Use admin, support o user."
            )
        return value

    @field_validator("password")
    @classmethod
    def validar_password(cls, value: str) -> str:
        if " " in value:
            raise ValueError("La contraseña no puede contener espacios.")
        if not any(caracter.isupper() for caracter in value):
            raise ValueError(
                "La contraseña debe contener al menos una mayúscula."
            )
        if not any(caracter.islower() for caracter in value):
            raise ValueError(
                "La contraseña debe contener al menos una minúscula."
            )
        if not any(caracter.isdigit() for caracter in value):
            raise ValueError(
                "La contraseña debe contener al menos un número."
            )
        return value


class UserUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    role: str
    is_active: bool

    @field_validator("role")
    @classmethod
    def validar_rol(cls, value: str) -> str:
        if value not in ROLES_PERMITIDOS:
            raise ValueError(
                "El rol no está permitido. Use admin, support o user."
            )
        return value


class UserPatch(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None

    @field_validator("role")
    @classmethod
    def validar_rol(cls, value: str | None) -> str | None:
        if value is not None and value not in ROLES_PERMITIDOS:
            raise ValueError(
                "El rol no está permitido. Use admin, support o user."
            )
        return value

    @model_validator(mode="before")
    @classmethod
    def validar_campos_no_nulos(cls, datos):
        if isinstance(datos, dict):
            for campo, valor in datos.items():
                if campo in {
                    "name", "email", "role", "is_active"
                } and valor is None:
                    raise ValueError(
                        f"El campo '{campo}' no puede ser null."
                    )
        return datos


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
