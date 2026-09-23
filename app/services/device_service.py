from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.device_model import Device


def obtener_todos(
    db: Session,
    device_type: str | None = None,
    is_available: bool | None = None,
    brand: str | None = None,
    search: str | None = None
):
    consulta = select(Device)

    if device_type is not None:
        consulta = consulta.where(
            Device.device_type == device_type
        )

    if is_available is not None:
        consulta = consulta.where(
            Device.is_available == is_available
        )

    if brand is not None:
        consulta = consulta.where(
            Device.brand == brand
        )

    if search is not None:
        termino = f"%{search}%"

        consulta = consulta.where(
            or_(
                Device.name.ilike(termino),
                Device.serial_number.ilike(termino),
                Device.device_type.ilike(termino),
                Device.brand.ilike(termino)
            )
        )

    consulta = consulta.order_by(Device.name.asc())

    return db.scalars(consulta).all()


def obtener_por_id(
    device_id: int,
    db: Session
):
    dispositivo = db.get(Device, device_id)

    if dispositivo is None:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado."
        )

    return dispositivo


def obtener_por_serial(
    serial_number: str,
    db: Session
):
    return db.scalar(
        select(Device).where(
            Device.serial_number == serial_number
        )
    )


def crear(
    datos,
    db: Session
):
    dispositivo_existente = obtener_por_serial(
        datos.serial_number,
        db
    )

    if dispositivo_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un dispositivo con ese número de serie."
        )

    nuevo_dispositivo = Device(
        name=datos.name,
        serial_number=datos.serial_number,
        device_type=datos.device_type,
        brand=datos.brand,
        is_available=datos.is_available
    )

    db.add(nuevo_dispositivo)
    db.commit()
    db.refresh(nuevo_dispositivo)

    return nuevo_dispositivo


def actualizar_completo(
    device_id: int,
    datos,
    db: Session
):
    dispositivo = obtener_por_id(
        device_id,
        db
    )

    dispositivo_existente = db.scalar(
        select(Device).where(
            Device.serial_number == datos.serial_number,
            Device.id != device_id
        )
    )

    if dispositivo_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un dispositivo con ese número de serie."
        )

    dispositivo.name = datos.name
    dispositivo.serial_number = datos.serial_number
    dispositivo.device_type = datos.device_type
    dispositivo.brand = datos.brand
    dispositivo.is_available = datos.is_available

    db.commit()
    db.refresh(dispositivo)

    return dispositivo


def actualizar_parcial(
    device_id: int,
    datos,
    db: Session
):
    dispositivo = obtener_por_id(
        device_id,
        db
    )

    cambios = datos.model_dump(
        exclude_unset=True
    )

    if not cambios:
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar."
        )

    if "serial_number" in cambios:
        dispositivo_existente = db.scalar(
            select(Device).where(
                Device.serial_number == cambios["serial_number"],
                Device.id != device_id
            )
        )

        if dispositivo_existente:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un dispositivo con ese número de serie."
            )

    for campo, valor in cambios.items():
        setattr(dispositivo, campo, valor)

    db.commit()
    db.refresh(dispositivo)

    return dispositivo


def eliminar(
    device_id: int,
    db: Session
):
    dispositivo = obtener_por_id(
        device_id,
        db
    )

    db.delete(dispositivo)
    db.commit()