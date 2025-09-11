import asyncio
from datetime import date
from decimal import Decimal

import httpx
from sqlalchemy import select, func

from config import config
from database.database import setup_database, dispose_database_engine
from database.models import Company, Asset, Role
from finnhub import FinnhubService
from logger import logger

TICKERS_TO_SEED = ["AAPL", "GOOGL", "MSFT", "TSLA"]


async def create_company(db, company_data: dict) -> Company:
    company_name = company_data.get("name")
    logger.info(f"Creating new company: {company_name}")
    foundation_date = None
    if fd_str := company_data.get("ipo"):
        try:
            foundation_date = date.fromisoformat(fd_str)
        except (ValueError, TypeError):
            foundation_date = None

    instance = Company(
        name=company_name,
        profile=company_data.get("description", ""),
        foundation_date=foundation_date,
    )
    db.add(instance)
    await db.flush()
    await db.refresh(instance)
    return instance


async def seed_database():
    setup_database()
    from database.database import _async_session_maker as async_session_maker

    try:
        async with async_session_maker() as db:
            try:
                count = await db.scalar(select(func.count()).select_from(Role))
                if count > 0:
                    logger.info("Database already seeded, skipping seeding.")
                    return

                db.add_all([Role(name="users", permissions={}), Role(name="admin", permissions={})])

                async with FinnhubService(api_key=config.FINNHUB_API_KEY) as finnhub:
                    for ticker in TICKERS_TO_SEED:
                        logger.info(f"Processing ticker: {ticker}")

                        profile = await finnhub.get_company_profile(ticker)
                        if not profile:
                            logger.warning(f"No company profile found for ticker {ticker}. Skipping.")
                            continue

                        company = await create_company(db, profile)
                        initial_price = await finnhub.get_asset_price(ticker)
                        logger.info(f"Creating asset for {ticker}")
                        asset = Asset(
                            name=profile.get("name", ticker),
                            company_id=company.id,
                            listed_year=date.fromisoformat(profile.get("ipo")).year if profile.get("ipo") else 0,
                            ticker=profile.get("ticker", ticker),
                            description=f"Акции {profile.get('name')}",
                            available_count=10000,
                            price=initial_price or Decimal("0.0"),
                        )
                        db.add(asset)

                await db.commit()
                logger.info("Database seeded successfully!")

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                await db.rollback()
            except Exception as e:
                logger.exception("Error during database seeding logic")
                await db.rollback()

    finally:
        logger.info("Disposing database engine...")
        await dispose_database_engine()


if __name__ == "__main__":
    asyncio.run(seed_database())
