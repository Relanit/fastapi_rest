from fastapi import APIRouter, Depends, status
from .schemas import TopUpBalanceRequest
from models import User
from .dependencies import BalanceServiceDep
from auth.auth import current_user

router = APIRouter(prefix="/balance", tags=["Balance"])


@router.post("/top-up", status_code=status.HTTP_200_OK)
async def top_up_balance(
    top_up: TopUpBalanceRequest, service: BalanceServiceDep, current_user: User = Depends(current_user)
):
    updated_user = await service.top_up_balance(current_user, top_up.amount)
    return {"message": "Баланс успешно пополнен", "new_balance": updated_user.balance}
