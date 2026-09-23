from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


ESTADOS_PRESTAMO = {
    "active",
    "returned",
    "overdue"
}


class LoanCreate(BaseModel):
    user_id: int = Field(gt=0)
    device_id: int = Field(gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "device_id": 1
            }
        }
    }


class LoanUpdate(BaseModel):
    status: str = Field(min_length=1, max_length=20)


class LoanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: datetime | None
    status: str


class LoanDetailResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    user_email: str

    device_id: int
    device_name: str
    serial_number: str
    device_type: str
    brand: str | None

    loan_date: datetime
    return_date: datetime | None
    status: str