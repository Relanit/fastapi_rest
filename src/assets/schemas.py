from datetime import date

from pydantic import BaseModel, field_validator


class AssetBase(BaseModel):
    company_id: int
    name: str
    listed_year: int
    ticker: str
    description: str | None = None
    available_count: int
    price: float

    @field_validator("company_id")
    def validate_company_id(cls, value: int) -> int:
        if value < 0:
            raise ValueError("ID компании должен быть неотрицательным.")
        return value

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not (1 < len(value) < 100):
            raise ValueError("Название актива должно содержать хотя бы 1 символ.")
        return value

    @field_validator("listed_year")
    def validate_listed_year(cls, value: int) -> int:
        current_year = date.today().year
        if value > current_year:
            raise ValueError("Год листинга не может быть в будущем.")
        return value

    @field_validator("available_count")
    def validate_available_count(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Количество доступных единиц должно быть неотрицательным.")
        return value

    @field_validator("price")
    def validate_price(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Цена должна быть положительной.")
        return value


class AssetCreate(AssetBase):
    pass


class AssetUpdate(AssetBase):
    pass


class AssetPatchUpdate(AssetBase):
    company_id: int | None = None
    name: str | None = None
    listed_year: int | None = None
    ticker: str | None = None
    description: str | None = None
    available_count: int | None = None
    price: float | None = None


class AssetResponse(AssetBase):
    id: int
