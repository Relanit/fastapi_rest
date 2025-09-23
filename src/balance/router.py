from fastapi import APIRouter, Depends, status
from fastapi import Request

from limiter import limiter
from .schemas import TopUpBalanceRequest
from database.models import User
from .dependencies import BalanceServiceDep
from users.auth import current_user

router = APIRouter(prefix="/balance", tags=["Balance"])


@router.post("/top-up", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def top_up_balance(
    request: Request,
    top_up: TopUpBalanceRequest,
    service: BalanceServiceDep,
    current_user: User = Depends(current_user),
):
    updated_user = await service.top_up_balance(current_user, top_up.amount)
    return {"message": "Баланс успешно пополнен", "new_balance": updated_user.balance}
