from fastapi import APIRouter, HTTPException, Query
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


usuarios = [
    {
        "id": 1,
        "name": "Carlos",
        "email": "carlos@example.com",
        "role": "admin",
        "is_active": True
    },
    {
        "id": 2,
        "name": "Laura",
        "email": "laura@example.com",
        "role": "support",
        "is_active": True
    },
    {
        "id": 3,
        "name": "Miguel",
        "email": "miguel@example.com",
        "role": "user",
        "is_active": False
    }
]


@router.get("/", response_model=list[UserResponse])
def listar_usuarios(
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None)
):
    resultado = usuarios

    if role is not None:
        resultado = [
            usuario for usuario in resultado
            if usuario["role"] == role
        ]

    if is_active is not None:
        resultado = [
            usuario for usuario in resultado
            if usuario["is_active"] == is_active
        ]

    return resultado


@router.get("/{user_id}", response_model=UserResponse)
def obtener_usuario(user_id: int):
    for usuario in usuarios:
        if usuario["id"] == user_id:
            return usuario

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado."
    )


@router.post("/", response_model=UserResponse, status_code=201)
def crear_usuario(usuario: UserCreate):

    for usuario_existente in usuarios:
        if usuario_existente["email"].lower() == usuario.email.lower():
            raise HTTPException(
                status_code=409,
                detail="Ya existe un usuario con ese correo."
            )

    nuevo_id = max(usuario["id"] for usuario in usuarios) + 1

    nuevo_usuario = {
        "id": nuevo_id,
        **usuario.model_dump()
    }

    usuarios.append(nuevo_usuario)

    return nuevo_usuario