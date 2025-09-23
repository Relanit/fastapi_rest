from fastapi import APIRouter, Depends, Body
from fastapi import status, Request
from pydantic import condecimal

from limiter import limiter
from transactions.dependencies import TransactionServiceDep
from transactions.schemas import TransactionResponse
from users.auth import current_user_admin, current_user
from assets.dependencies import valid_asset_id, AssetServiceDep
from database.models import Asset, User
from assets.schemas import AssetCreate, AssetUpdate, AssetResponse, AssetPatchUpdate
from pagination import PaginatorDep

router = APIRouter(prefix="/assets", tags=["Asset"])


@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset: AssetCreate,
    service: AssetServiceDep,
    current_user_admin=Depends(current_user_admin),
):
    return await service.create(asset)


@router.get("/", response_model=list[AssetResponse], status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def get_assets(
    request: Request,
    pagination: PaginatorDep,
    service: AssetServiceDep,
    company_id: int | None = None,
):
    return await service.get_all(pagination.limit, pagination.skip, company_id)


@router.get("/{asset_id}", response_model=AssetResponse, status_code=status.HTTP_200_OK)
@limiter.limit("7/minute")
async def get_specific_asset(request: Request, asset: Asset = Depends(valid_asset_id)):
    return asset


@router.get("/search/", response_model=list[AssetResponse])
async def search_assets(search_query: str, service: AssetServiceDep):
    return await service.search_assets(search_query)


@router.post(
    "/{asset_id}/buy/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
async def buy_asset(
    request: Request,
    service: TransactionServiceDep,
    asset: Asset = Depends(valid_asset_id),
    amount: condecimal(gt=0, max_digits=20, decimal_places=10) = Body(...),
    current_user: User = Depends(current_user),
):
    return await service.create_buy(asset, amount, current_user)


@router.post(
    "/{asset_id}/sell/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def sell_asset(
    service: TransactionServiceDep,
    asset: Asset = Depends(valid_asset_id),
    amount: condecimal(gt=0, max_digits=20, decimal_places=10) = Body(...),
    current_user: User = Depends(current_user),
):
    return await service.create_sell(asset, amount, current_user)


@router.put("/{asset_id}", response_model=AssetResponse, status_code=status.HTTP_200_OK)
async def update_asset(
    updated_asset: AssetUpdate,
    service: AssetServiceDep,
    asset: Asset = Depends(valid_asset_id),
    current_user_admin=Depends(current_user_admin),
):
    return await service.update_full(asset, updated_asset)


@router.patch(
    "/{asset_id}", response_model=AssetResponse, status_code=status.HTTP_200_OK
)
async def partial_update_asset(
    asset_data: AssetPatchUpdate,
    service: AssetServiceDep,
    asset: Asset = Depends(valid_asset_id),
    current_user_admin=Depends(current_user_admin),
):
    return await service.update_partial(asset, asset_data)


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    service: AssetServiceDep,
    asset: Asset = Depends(valid_asset_id),
    current_user_admin=Depends(current_user_admin),
):
    await service.delete(asset)
