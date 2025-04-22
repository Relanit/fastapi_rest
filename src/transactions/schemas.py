from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, conint, condecimal, field_validator

from database.models import TransactionType


class TransactionBase(BaseModel):
    asset_id: conint(ge=0)
    amount: condecimal(gt=0, max_digits=20, decimal_places=10)


class TransactionUpdate(TransactionBase):
    pass


class TransactionPatchUpdate(BaseModel):
    user_id: int | None = None
    asset_id: int | None = None
    transaction_datetime: datetime | None = None
    amount: Decimal | None = None
    total_value: Decimal | None = None

    @field_validator("transaction_datetime")
    def check_transaction_datetime(cls, value: datetime) -> datetime | None:
        if value is None:
            return None

        if value > datetime.now(timezone.utc):
            raise ValueError("transaction_datetime не может быть в будущем")
        return value


class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    type: TransactionType
    transaction_datetime: datetime
    total_value: Decimal
