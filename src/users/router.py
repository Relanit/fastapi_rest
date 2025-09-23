from fastapi import APIRouter, Depends, status, Request

from assets.schemas import AssetResponse
from limiter import limiter
from pagination import PaginatorDep
from transactions.schemas import TransactionResponse
from users.auth import current_user_admin
from users.dependencies import UserServiceDep

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/{user_id}/assets",
    response_model=list[AssetResponse],
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute")
async def get_assets(
    request: Request,
    pagination: PaginatorDep,
    service: UserServiceDep,
    user_id: int,
    current_user_admin=Depends(current_user_admin),
):
    return await service.get_assets(pagination.limit, pagination.skip, user_id)


@router.get(
    "/{user_id}/transactions",
    response_model=list[TransactionResponse],
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute")
async def get_transactions(
    request: Request,
    pagination: PaginatorDep,
    service: UserServiceDep,
    user_id: int,
    current_user_admin=Depends(current_user_admin),
):
    return await service.get_transactions(pagination.limit, pagination.skip, user_id)
