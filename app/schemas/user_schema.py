from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserCreate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool = True


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool