
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator
)


ROLES_PERMITIDOS = {"admin", "support", "user"}


class UserCreate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    role: str
    is_active: bool = True

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Stiven Hurtado",
                "email": "stiven@sena.edu.co",
                "role": "user",
                "is_active": True
            }
        }
    }

class UserUpdate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    role: str
    is_active: bool


class UserPatch(BaseModel):
    name: str | None = Field(default=None, min_length=3)
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None

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