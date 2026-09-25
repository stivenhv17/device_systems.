from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import (
    require_admin,
    require_admin_or_support
)
from app.dependencies.database_dependency import get_db
from app.models.user_model import User
from app.schemas.device_schema import (
    DeviceCreate,
    DevicePatch,
    DeviceResponse,
    DeviceUpdate
)
from app.services import device_service

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.get(
    "",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos",
    description="Obtiene todos los dispositivos y permite filtrarlos por tipo, disponibilidad, marca y búsqueda.",
    response_description="Lista de dispositivos registrados.",
    responses={
        200: {"description": "Dispositivos obtenidos correctamente."},
        422: {"description": "Parámetros de consulta inválidos."}
    }
)
def listar_dispositivos(
    device_type: str | None = Query(default=None),
    is_available: bool | None = Query(default=None),
    brand: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return device_service.obtener_todos(
        db,
        device_type=device_type,
        is_available=is_available,
        brand=brand,
        search=search
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Consultar dispositivo por ID",
    description="Obtiene un dispositivo específico utilizando su identificador.",
    response_description="Información del dispositivo solicitado.",
    responses={
        200: {"description": "Dispositivo encontrado correctamente."},
        404: {"description": "El dispositivo solicitado no existe."}
    }
)
def obtener_dispositivo(
    device_id: int,
    db: Session = Depends(get_db)
):
    return device_service.obtener_por_id(
        device_id,
        db
    )


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description="Registra un nuevo dispositivo validando que su número de serie no esté duplicado.",
    response_description="Dispositivo creado correctamente.",
    responses={
        201: {"description": "Dispositivo creado correctamente."},
        400: {"description": "El número de serie ya está registrado."},
        401: {"description": "Token inválido o no enviado."},
        403: {"description": "No tiene permisos para realizar esta operación."},
        422: {"description": "Los datos enviados no cumplen las validaciones."}
    }
)
def crear_dispositivo(
    datos: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    return device_service.crear(
        datos,
        db
    )


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo completo",
    description="Reemplaza todos los datos de un dispositivo existente.",
    response_description="Dispositivo actualizado correctamente.",
    responses={
        200: {"description": "Dispositivo actualizado correctamente."},
        400: {"description": "El número de serie ya está registrado."},
        401: {"description": "Token inválido o no enviado."},
        403: {"description": "No tiene permisos para realizar esta operación."},
        404: {"description": "El dispositivo solicitado no existe."},
        422: {"description": "Los datos enviados no cumplen las validaciones."}
    }
)
def actualizar_dispositivo(
    device_id: int,
    datos: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    return device_service.actualizar_completo(
        device_id,
        datos,
        db
    )


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo parcialmente",
    description="Modifica únicamente los campos enviados del dispositivo.",
    response_description="Dispositivo actualizado correctamente.",
    responses={
        200: {"description": "Dispositivo actualizado correctamente."},
        400: {"description": "La solicitud no contiene campos válidos o el número de serie ya está registrado."},
        404: {"description": "El dispositivo solicitado no existe."},
        422: {"description": "Los datos enviados no cumplen las validaciones."}
    }
)
def actualizar_dispositivo_parcial(
    device_id: int,
    datos: DevicePatch,
    db: Session = Depends(get_db)
):
    return device_service.actualizar_parcial(
        device_id,
        datos,
        db
    )


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo existente.",
    response_description="Dispositivo eliminado correctamente.",
    responses={
        204: {"description": "Dispositivo eliminado correctamente."},
        401: {"description": "Token inválido o no enviado."},
        403: {"description": "No tiene permisos para realizar esta operación."},
        404: {"description": "El dispositivo solicitado no existe."}
    }
)
def eliminar_dispositivo(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    device_service.eliminar(
        device_id,
        db
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )