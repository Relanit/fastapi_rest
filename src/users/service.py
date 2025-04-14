from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from database.models import Transaction, Asset, UserAsset


class UserService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_transactions(self, limit: int, skip: int, user_id: int):
        query = select(Transaction).limit(limit).offset(skip).where(Transaction.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_assets(self, limit: int, skip: int, user_id: int):
        query = select(UserAsset).limit(limit).offset(skip).where(UserAsset.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()
