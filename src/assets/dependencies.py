from typing import Annotated

from fastapi import Depends

from assets.exceptions import AssetNotFound
from models import Asset
from assets.service import AssetService

AssetServiceDep = Annotated[AssetService, Depends(AssetService)]


async def valid_asset_id(asset_id: int, service: AssetServiceDep) -> Asset:
    asset = await service.get_by_id(asset_id)
    if not asset:
        raise AssetNotFound()
    return asset
