from datetime import date
from decimal import Decimal

from pydantic import BaseModel, condecimal, constr, conint


class AssetBase(BaseModel):
    company_id: conint(ge=0)
    name: constr(strip_whitespace=True, min_length=1, max_length=100)
    listed_year: conint(le=date.today().year)
    ticker: str
    description: str | None = None
    available_count: conint(ge=0)
    price: condecimal(gt=0, max_digits=30, decimal_places=20)


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
    price: Decimal | None = None


class AssetResponse(AssetBase):
    id: int


class UserAssetResponse(BaseModel):
    id: int
    user_id: int
    asset_id: int
    amount: Decimal
