from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, conint, condecimal, field_validator


class TransactionBase(BaseModel):
    asset_id: conint(ge=0)
    amount: condecimal(gt=0, max_digits=20, decimal_places=10)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionPatchUpdate(BaseModel):
    user_id: int | None = None
    asset_id: int | None = None
    purchase_datetime: datetime | None = None
    amount: Decimal | None = None
    total_value: Decimal | None = None

    @field_validator("purchase_datetime")
    def check_purchase_datetime(cls, value: datetime) -> datetime | None:
        if value is None:
            return None

        if value > datetime.now(timezone.utc):
            raise ValueError("purchase_datetime не может быть в будущем")
        return value


class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    purchase_datetime: datetime
    total_value: Decimal
