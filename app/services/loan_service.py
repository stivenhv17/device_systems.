from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.models.user_model import User
from app.schemas.loan_schema import ESTADOS_PRESTAMO


def validar_estado(status: str):
    if status not in ESTADOS_PRESTAMO:
        raise HTTPException(
            status_code=422,
            detail="El estado debe ser active, returned o overdue."
        )


def obtener_por_id(
    loan_id: int,
    db: Session
):
    prestamo = db.get(Loan, loan_id)

    if prestamo is None:
        raise HTTPException(
            status_code=404,
            detail="Préstamo no encontrado."
        )

    return prestamo


def obtener_todos(
    db: Session,
    status: str | None = None,
    user_email: str | None = None,
    device_type: str | None = None,
    loan_date_from: datetime | None = None,
    loan_date_to: datetime | None = None
):
    if status is not None:
        validar_estado(status)

    consulta = (
        select(Loan)
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
    )

    filtros = []

    if status is not None:
        filtros.append(Loan.status == status)

    if user_email is not None:
        filtros.append(User.email.ilike(f"%{user_email}%"))

    if device_type is not None:
        filtros.append(Device.device_type.ilike(f"%{device_type}%"))

    if loan_date_from is not None:
        filtros.append(Loan.loan_date >= loan_date_from)

    if loan_date_to is not None:
        filtros.append(Loan.loan_date <= loan_date_to)

    if filtros:
        consulta = consulta.where(and_(*filtros))

    consulta = consulta.order_by(Loan.loan_date.desc())

    return db.scalars(consulta).all()


def crear(
    datos,
    db: Session
):
    usuario = db.get(User, datos.user_id)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado."
        )

    dispositivo = db.get(Device, datos.device_id)

    if dispositivo is None:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado."
        )

    if not dispositivo.is_available:
        raise HTTPException(
            status_code=409,
            detail="El dispositivo no está disponible para préstamo."
        )

    nuevo_prestamo = Loan(
        user_id=datos.user_id,
        device_id=datos.device_id,
        loan_date=datetime.now(
            ZoneInfo("America/Bogota")
        ),
        status="active"
    )

    dispositivo.is_available = False

    db.add(nuevo_prestamo)
    db.commit()
    db.refresh(nuevo_prestamo)

    return nuevo_prestamo


def devolver(
    loan_id: int,
    db: Session
):
    prestamo = obtener_por_id(
        loan_id,
        db
    )

    if prestamo.status == "returned":
        raise HTTPException(
            status_code=409,
            detail="El préstamo ya fue devuelto."
        )

    dispositivo = db.get(
        Device,
        prestamo.device_id
    )

    prestamo.status = "returned"

    prestamo.return_date = datetime.now(
        ZoneInfo("America/Bogota")
    )

    if dispositivo is not None:
        dispositivo.is_available = True

    db.commit()
    db.refresh(prestamo)

    return prestamo


def obtener_detalles(
    db: Session
):
    consulta = (
        select(
            Loan.id,
            Loan.user_id,
            User.name.label("user_name"),
            User.email.label("user_email"),
            Loan.device_id,
            Device.name.label("device_name"),
            Device.serial_number,
            Device.device_type,
            Device.brand,
            Loan.loan_date,
            Loan.return_date,
            Loan.status
        )
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
        .order_by(Loan.loan_date.desc())
    )

    resultados = db.execute(consulta).mappings().all()

    return [
        dict(resultado)
        for resultado in resultados
    ]


def obtener_prestamos_usuario(
    user_id: int,
    db: Session
):
    usuario = db.get(
        User,
        user_id
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado."
        )

    consulta = (
        select(Loan)
        .join(User, Loan.user_id == User.id)
        .where(
            and_(
                User.id == user_id,
                Loan.user_id == user_id
            )
        )
        .order_by(
            Loan.loan_date.desc()
        )
    )

    return db.scalars(consulta).all()


def obtener_prestamos_dispositivo(
    device_id: int,
    db: Session
):
    dispositivo = db.get(
        Device,
        device_id
    )

    if dispositivo is None:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado."
        )

    consulta = (
        select(Loan)
        .join(Device, Loan.device_id == Device.id)
        .where(
            and_(
                Device.id == device_id,
                Loan.device_id == device_id
            )
        )
        .order_by(
            Loan.loan_date.desc()
        )
    )

    return db.scalars(consulta).all()