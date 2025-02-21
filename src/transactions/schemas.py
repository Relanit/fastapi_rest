from datetime import date, timedelta

from pydantic import BaseModel, field_validator, Field


class TransactionBase(BaseModel):
    user_id: int
    asset_id: int
    purchase_date: date | None = Field(default_factory=date.today)
    target_sell_date: date | None = Field(default_factory=lambda: date.today() + timedelta(days=30))
    amount: float

    @field_validator("user_id")
    def validate_user_id(cls, value: int) -> int:
        if value < 0:
            raise ValueError("ID пользователя должен быть неотрицательным.")
        return value

    @field_validator("asset_id")
    def validate_asset_id(cls, value: int) -> int:
        if value < 0:
            raise ValueError("ID актива должен быть неотрицательным.")
        return value

    @field_validator("purchase_date")
    def validate_purchase_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Дата покупки не может быть в будущем.")
        return value

    @field_validator("target_sell_date")
    def validate_target_sell_date(cls, value: date) -> date:
        if value <= date.today():
            raise ValueError("Целевая дата продажи должна быть в будущем.")
        return value

    @field_validator("amount")
    def validate_amount(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Сумма транзакции должна быть больше нуля.")
        return value


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    sell_date: date | None


class TransactionPatchUpdate(BaseModel):
    user_id: int | None = None
    asset_id: int | None = None
    purchase_date: date | None = None
    target_sell_date: date | None = None
    amount: float | None = None
    sell_date: date | None = None


class TransactionResponse(TransactionBase):
    id: int
    sell_date: date | None
