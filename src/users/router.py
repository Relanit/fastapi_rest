from fastapi import APIRouter, Depends, status

from assets.schemas import AssetResponse
from pagination import PaginatorDep
from transactions.schemas import TransactionResponse
from users.auth import current_user_admin
from users.dependencies import UserServiceDep

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}/assets", response_model=list[AssetResponse], status_code=status.HTTP_200_OK)
async def get_assets(
    pagination: PaginatorDep, service: UserServiceDep, user_id: int, current_user_admin=Depends(current_user_admin)
):
    return await service.get_assets(pagination.limit, pagination.skip, user_id)


@router.get("/{user_id}/transactions", response_model=list[TransactionResponse], status_code=status.HTTP_200_OK)
async def get_transactions(
    pagination: PaginatorDep, service: UserServiceDep, user_id: int, current_user_admin=Depends(current_user_admin)
):
    return await service.get_transactions(pagination.limit, pagination.skip, user_id)
