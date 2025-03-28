from datetime import date, timedelta
from decimal import Decimal

from pydantic import BaseModel, Field, conint, condecimal


class TransactionBase(BaseModel):
    user_id: conint(ge=0)
    asset_id: conint(ge=0)
    purchase_date: date = Field(default_factory=date.today, le=date.today())
    target_sell_date: date = Field(default_factory=lambda: date.today() + timedelta(days=30), gt=date.today())
    amount: condecimal(gt=0, max_digits=10, decimal_places=2)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    sell_date: date | None


class TransactionPatchUpdate(BaseModel):
    user_id: int | None = None
    asset_id: int | None = None
    purchase_date: date | None = None
    target_sell_date: date | None = None
    amount: Decimal | None = None
    sell_date: date | None = None


class TransactionResponse(TransactionBase):
    id: int
    sell_date: date | None
