import asyncio
from datetime import date
from decimal import Decimal

import httpx
from sqlalchemy import select, func

from config import config
from database.models import Company, Asset, Role
from database.database import async_session_maker
from logger import logger

TICKERS_TO_SEED = ["AAPL", "GOOGL", "MSFT", "TSLA"]

FINNHUB_BASE_URL = "https://finnhub.io/api/v1"


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
    async with async_session_maker() as db:
        try:
            count = await db.scalar(select(func.count()).select_from(Role))
            if count > 0:
                logger.info("Database already seeded, skipping seeding.")
                return

            db.add_all([Role(name="users", permissions={}), Role(name="admin", permissions={})])

            async with httpx.AsyncClient() as client:
                for ticker in TICKERS_TO_SEED:
                    logger.info(f"Processing ticker: {ticker}")

                    profile_res = await client.get(
                        f"{FINNHUB_BASE_URL}/stock/profile2",
                        params={"symbol": ticker, "token": config.FINNHUB_API_KEY}
                    )
                    profile_res.raise_for_status()
                    company_data = profile_res.json()
                    if not company_data:
                        logger.warning(f"No company profile found for ticker {ticker}. Skipping.")
                        continue

                    quote_res = await client.get(
                        f"{FINNHUB_BASE_URL}/quote",
                        params={"symbol": ticker, "token": config.FINNHUB_API_KEY}
                    )
                    quote_res.raise_for_status()
                    quote_data = quote_res.json()

                    company = await create_company(db, company_data)
                    logger.info(f"Creating asset for {ticker}")
                    asset = Asset(
                        name=company_data.get("name", ticker),
                        company_id=company.id,
                        listed_year=date.fromisoformat(company_data.get("ipo")).year if company_data.get("ipo") else 0,
                        ticker=company_data.get("ticker", ticker),
                        description=f"Акции {company_data.get('name')}",
                        available_count=10000,
                        price=Decimal(str(quote_data.get("c", 0.0)))  # 'c' - current price
                    )
                    db.add(asset)

            await db.commit()
            logger.info("Database seeded successfully!")

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            await db.rollback()
        except Exception as e:
            logger.exception("Error seeding database")
            await db.rollback()
        finally:
            await db.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
