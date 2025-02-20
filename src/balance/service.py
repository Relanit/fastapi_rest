from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from models import User
from database import get_async_session


class BalanceService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def top_up_balance(self, user: User, amount: float) -> User:
        user.balance += amount
        await self.session.merge(user)
        await self.session.commit()
        return user
