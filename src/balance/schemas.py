from pydantic import field_validator, BaseModel


class TopUpBalanceRequest(BaseModel):
    amount: float

    @field_validator("amount")
    def amount_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Сумма должна быть положительной")
        return value
