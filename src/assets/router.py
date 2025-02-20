from fastapi import APIRouter, Depends
from fastapi import status

from auth.auth import current_user_admin
from assets.dependencies import valid_asset_id, AssetServiceDep
from models import Asset
from assets.schemas import AssetCreate, AssetUpdate, AssetResponse, AssetPatchUpdate
from pagination import PaginatorDep

router = APIRouter(prefix="/assets", tags=["Asset"])


@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset: AssetCreate,
    service: AssetServiceDep,
    current_user_admin=Depends(current_user_admin),
):
    created_asset = await service.create(asset)
    return created_asset


@router.get("/", response_model=list[AssetResponse], status_code=status.HTTP_200_OK)
async def get_assets(
    pagination: PaginatorDep,
    service: AssetServiceDep,
    company_id: int | None = None,
):
    assets = await service.get_all(pagination.limit, pagination.skip, company_id)
    return assets


@router.get("/{asset_id}", response_model=AssetResponse, status_code=status.HTTP_200_OK)
async def get_specific_asset(asset: Asset = Depends(valid_asset_id)):
    return asset


@router.get("/search/", response_model=list[AssetResponse])
async def search_assets(search_query: str, service: AssetServiceDep):
    assets = await service.search_assets(search_query)
    return assets


@router.put("/{asset_id}", response_model=AssetResponse, status_code=status.HTTP_200_OK)
async def update_asset(
    updated_asset: AssetUpdate,
    service: AssetServiceDep,
    asset: Asset = Depends(valid_asset_id),
    current_user_admin=Depends(current_user_admin),
):
    asset_updated = await service.update_full(asset, updated_asset)
    return asset_updated


@router.patch("/{asset_id}", response_model=AssetResponse, status_code=status.HTTP_200_OK)
async def partial_update_asset(
    asset_data: AssetPatchUpdate,
    service: AssetServiceDep,
    asset: Asset = Depends(valid_asset_id),
    current_user_admin=Depends(current_user_admin),
):
    updated_asset = await service.update_partial(asset, asset_data)
    return updated_asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    service: AssetServiceDep, asset: Asset = Depends(valid_asset_id), current_user_admin=Depends(current_user_admin)
):
    await service.delete(asset)
