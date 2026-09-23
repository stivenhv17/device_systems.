from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    device_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("devices.id"),
        nullable=False
    )

    loan_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(
            ZoneInfo("America/Bogota")
        ),
        nullable=False
    )

    return_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active"
    )

    user = relationship(
        "User",
        back_populates="loans"
    )

    device = relationship(
        "Device",
        back_populates="loans"
    )