from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, case, or_, func
from typing import Sequence
from fastapi import Depends

from assets.exceptions import AssetNotFound
from companies.exceptions import CompanyNotFound
from database.models import Asset, Company
from .schemas import AssetCreate, AssetUpdate, AssetPatchUpdate
from database.database import get_async_session


class AssetService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def valid_company_id(self, company_id: int) -> Company:
        result = await self.session.execute(select(Company).where(Company.id == company_id))
        if company := result.scalar_one_or_none():
            return company
        raise CompanyNotFound()

    async def create(self, asset: AssetCreate) -> Asset:
        await self.valid_company_id(asset.company_id)
        stmt = insert(Asset).values(**asset.model_dump()).returning(Asset)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_all(self, limit: int, skip: int, company_id: int | None) -> Sequence[Asset]:
        if company_id is not None:
            company = await self.valid_company_id(company_id)
            return company.assets[skip : skip + limit]
        query = select(Asset).limit(limit).offset(skip)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, asset_id: int) -> Asset:
        query = select(Asset).where(Asset.id == asset_id)
        result = await self.session.execute(query)
        asset = result.scalar_one_or_none()
        if asset is None:
            raise AssetNotFound()
        return asset

    async def search_assets(self, search_query: str) -> Sequence[Asset]:
        search_terms = search_query.split()
        name_conditions = [Asset.name.ilike(f"%{term}%") for term in search_terms]
        company_conditions = [Company.name.ilike(f"%{term}%") for term in search_terms]

        name_cases = [(Asset.name.ilike(f"%{term}%"), 1) for term in search_terms]
        company_cases = [(Company.name.ilike(f"%{term}%"), 1) for term in search_terms]
        name_match_score = case(*name_cases, else_=0)
        company_match_score = case(*company_cases, else_=0)

        query = (
            select(Asset)
            .join(Company)
            .filter(or_(*name_conditions, *company_conditions))
            .order_by((func.coalesce(name_match_score, 0) + func.coalesce(company_match_score, 0)).desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_full(self, asset: Asset, updated_asset: AssetUpdate) -> Asset:
        await self.valid_company_id(asset.company_id)
        for key, value in updated_asset.model_dump(exclude_unset=True).items():
            setattr(asset, key, value)
        merged_asset = await self.session.merge(asset)
        await self.session.commit()
        return merged_asset

    async def update_partial(self, asset: Asset, asset_data: AssetPatchUpdate) -> Asset:
        update_data = asset_data.model_dump(exclude_unset=True)
        if "company_id" in update_data:
            await self.valid_company_id(update_data["company_id"])
        for key, value in update_data.items():
            setattr(asset, key, value)
        self.session.add(asset)
        await self.session.commit()
        return asset

    async def delete(self, asset: Asset) -> None:
        await self.session.delete(asset)
        await self.session.commit()
