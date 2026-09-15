from pydantic import BaseModel, EmailStr, Field


ROLES_PERMITIDOS = {"admin", "support", "user"}


class UserCreate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    role: str
    is_active: bool = True


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


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool