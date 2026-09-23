from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.loan_schema import (
    LoanCreate,
    LoanDetailResponse,
    LoanResponse
)
from app.services import loan_service


router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)

history_router = APIRouter(
    tags=["Loans"]
)


@router.get(
    "",
    response_model=list[LoanResponse],
    summary="Listar préstamos",
    description="Obtiene los préstamos y permite filtrarlos por estado, correo del usuario, tipo de dispositivo y rango de fechas.",
    response_description="Lista de préstamos que cumplen los filtros establecidos.",
    responses={
        200: {"description": "Préstamos obtenidos correctamente."},
        422: {"description": "Los parámetros de consulta no son válidos."}
    }
)
def listar_prestamos(
    status_value: str | None = Query(
        default=None,
        alias="status",
        pattern="^(active|returned|overdue)$",
        description="Estado del préstamo: active, returned o overdue."
    ),
    user_email: str | None = Query(
        default=None,
        description="Correo o parte del correo del usuario."
    ),
    device_type: str | None = Query(
        default=None,
        description="Tipo de dispositivo."
    ),
    loan_date_from: datetime | None = Query(
        default=None,
        description="Fecha inicial del préstamo."
    ),
    loan_date_to: datetime | None = Query(
        default=None,
        description="Fecha final del préstamo."
    ),
    db: Session = Depends(get_db)
):
    return loan_service.obtener_todos(
        db,
        status=status_value,
        user_email=user_email,
        device_type=device_type,
        loan_date_from=loan_date_from,
        loan_date_to=loan_date_to
    )


@router.get(
    "/details",
    response_model=list[LoanDetailResponse],
    summary="Listar detalles de préstamos",
    description="Obtiene los préstamos incluyendo información del usuario y del dispositivo mediante consultas JOIN.",
    response_description="Lista de préstamos con información relacionada del usuario y dispositivo.",
    responses={
        200: {"description": "Detalles de préstamos obtenidos correctamente."}
    }
)
def listar_detalles(
    db: Session = Depends(get_db)
):
    return loan_service.obtener_detalles(db)


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Consultar préstamo por ID",
    description="Obtiene un préstamo específico utilizando su identificador.",
    response_description="Información del préstamo solicitado.",
    responses={
        200: {"description": "Préstamo encontrado correctamente."},
        404: {"description": "El préstamo solicitado no existe."}
    }
)
def obtener_prestamo(
    loan_id: int,
    db: Session = Depends(get_db)
):
    return loan_service.obtener_por_id(
        loan_id,
        db
    )


@router.post(
    "",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Crea un préstamo verificando que el usuario y el dispositivo existan y que el dispositivo esté disponible.",
    response_description="Préstamo creado correctamente.",
    responses={
        201: {"description": "Préstamo creado correctamente."},
        404: {"description": "El usuario o dispositivo solicitado no existe."},
        409: {"description": "El dispositivo no está disponible para préstamo."},
        422: {"description": "Los datos enviados no cumplen las validaciones."}
    }
)
def crear_prestamo(
    datos: LoanCreate,
    db: Session = Depends(get_db)
):
    return loan_service.crear(
        datos,
        db
    )


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver dispositivo",
    description="Registra la devolución del dispositivo, actualiza la fecha de devolución y lo marca nuevamente como disponible.",
    response_description="Devolución registrada correctamente.",
    responses={
        200: {"description": "Dispositivo devuelto correctamente."},
        404: {"description": "El préstamo solicitado no existe."},
        409: {"description": "El préstamo ya fue devuelto."}
    }
)
def devolver_dispositivo(
    loan_id: int,
    db: Session = Depends(get_db)
):
    return loan_service.devolver(
        loan_id,
        db
    )


@history_router.get(
    "/users/{user_id}/loans",
    response_model=list[LoanResponse],
    summary="Consultar préstamos de un usuario",
    description="Obtiene el historial de préstamos asociados a un usuario.",
    response_description="Historial de préstamos del usuario.",
    responses={
        200: {"description": "Historial obtenido correctamente."},
        404: {"description": "El usuario solicitado no existe."}
    }
)
def prestamos_usuario(
    user_id: int,
    db: Session = Depends(get_db)
):
    return loan_service.obtener_prestamos_usuario(
        user_id,
        db
    )


@history_router.get(
    "/devices/{device_id}/loans",
    response_model=list[LoanResponse],
    summary="Consultar historial de dispositivo",
    description="Obtiene el historial de préstamos asociados a un dispositivo.",
    response_description="Historial de préstamos del dispositivo.",
    responses={
        200: {"description": "Historial obtenido correctamente."},
        404: {"description": "El dispositivo solicitado no existe."}
    }
)
def prestamos_dispositivo(
    device_id: int,
    db: Session = Depends(get_db)
):
    return loan_service.obtener_prestamos_dispositivo(
        device_id,
        db
    )