from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator
)

from app.schemas.user_schema import ROLES_PERMITIDOS


class UserRegister(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = Field(default="user")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Stiven Hurtado",
                "email": "stiven@sena.edu.co",
                "password": "ClaveSegura1",
                "role": "user"
            }
        }
    )

    @field_validator("name")
    @classmethod
    def validar_nombre(cls, value: str) -> str:
        nombre = value.strip()
        if not nombre:
            raise ValueError("El nombre es obligatorio.")
        return nombre

    @field_validator("password")
    @classmethod
    def validar_password(cls, value: str) -> str:
        if " " in value:
            raise ValueError("La contraseña no puede contener espacios.")
        if len(value) < 8:
            raise ValueError("La contraseña debe tener mínimo 8 caracteres.")
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

    @field_validator("role")
    @classmethod
    def validar_rol(cls, value: str) -> str:
        if value not in ROLES_PERMITIDOS:
            raise ValueError(
                "El rol no está permitido. Use admin, support o user."
            )
        return value

    @model_validator(mode="after")
    def validar_datos_registro(self):
        if self.password.lower() == self.email.lower():
            raise ValueError(
                "La contraseña no puede ser igual al correo electrónico."
            )
        return self


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "stiven@sena.edu.co",
                "password": "ClaveSegura1"
            }
        }
    )


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "token_generado",
                "token_type": "bearer"
            }
        }
    )


class TokenData(BaseModel):
    email: EmailStr | None = None
    role: str | None = None

    model_config = ConfigDict(from_attributes=True)
