from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from typing import Sequence
from fastapi import Depends

from companies.exceptions import CompanyAlreadyExists
from database.models import Company
from .schemas import CompanyCreate, CompanyUpdate, CompanyPatchUpdate
from database.database import get_async_session


class CompanyService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def create(self, company: CompanyCreate) -> Company:
        company.name = company.name.title()
        existing_company = await self.get_by_name(company.name)
        if existing_company:
            raise CompanyAlreadyExists()
        stmt = insert(Company).values(**company.model_dump()).returning(Company)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_all(self, limit: int, skip: int) -> Sequence[Company]:
        query = select(Company).limit(limit).offset(skip)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, company_id: int) -> Company | None:
        query = select(Company).where(Company.id == company_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Company | None:
        query = select(Company).where(Company.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_full(self, company: Company, updated_company: CompanyUpdate) -> Company:
        for key, value in updated_company.model_dump(exclude_unset=True).items():
            setattr(company, key, value)
        merged_company = await self.session.merge(company)
        await self.session.commit()
        return merged_company

    async def update_partial(self, company: Company, update_data: CompanyPatchUpdate) -> Company:
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(company, key, value)
        self.session.add(company)
        await self.session.commit()
        return company

    async def delete(self, company: Company) -> None:
        await self.session.delete(company)
        await self.session.commit()
