from fastapi import APIRouter, Depends
from fastapi import status

from assets.schemas import UserAssetResponse
from database.models import User

from transactions.schemas import TransactionResponse
from users.auth import current_user
from pagination import PaginatorDep
from users.dependencies import UserServiceDep
from users.schemas import UserRead

router = APIRouter(prefix="/me", tags=["Current user"])


@router.get("/")
def get_current_user(user: User = Depends(current_user)):
    return UserRead(
        id=user.id,
        email=user.email,
        username=user.username,
        balance=user.balance,
        role_id=user.role_id,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        is_verified=user.is_verified,
    )


@router.get("/assets", response_model=list[UserAssetResponse], status_code=status.HTTP_200_OK)
async def get_assets(
    pagination: PaginatorDep,
    service: UserServiceDep,
    current_user: User = Depends(current_user),
):
    return await service.get_assets(pagination.limit, pagination.skip, current_user.id)


@router.get("/transactions", response_model=list[TransactionResponse], status_code=status.HTTP_200_OK)
async def get_transactions(
    pagination: PaginatorDep,
    service: UserServiceDep,
    current_user: User = Depends(current_user),
):
    return await service.get_transactions(pagination.limit, pagination.skip, current_user.id)
