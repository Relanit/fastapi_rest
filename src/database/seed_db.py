import asyncio
from datetime import date

from sqlalchemy import select, func

from database.models import Company, Asset, Role
from database.database import async_session_maker
from logger import logger


async def seed_database():
    async with async_session_maker() as db:
        try:
            count = await db.scalar(select(func.count()).select_from(Role))
            if count > 0:
                logger.info("Database already seeded, skipping seeding.")
                return

            db.add_all([Role(name="user", permissions={}), Role(name="admin", permissions={})])

            apple = Company(name="Apple", profile="Tech company...", foundation_date=date.fromisoformat("1976-04-01"))
            google = Company(
                name="Google", profile="Search engine...", foundation_date=date.fromisoformat("1998-09-04")
            )
            microsoft = Company(
                name="Microsoft", profile="Software company...", foundation_date=date.fromisoformat("1975-04-04")
            )
            tesla = Company(
                name="Tesla", profile="Electric vehicles...", foundation_date=date.fromisoformat("2003-07-01")
            )

            db.add_all([apple, google, microsoft, tesla])
            await db.commit()
            await db.refresh(apple)
            await db.refresh(google)
            await db.refresh(microsoft)
            await db.refresh(tesla)

            assets_data = [
                {
                    "name": "Apple акции",
                    "company_id": apple.id,
                    "listed_year": 1980,
                    "ticker": "AAPL",
                    "description": "Акции Apple Inc.",
                    "available_count": 1000,
                    "price": 150.0,
                },
                {
                    "name": "Google акции",
                    "company_id": google.id,
                    "listed_year": 2004,
                    "ticker": "GOOGL",
                    "description": "Акции Alphabet Inc.",
                    "available_count": 500,
                    "price": 2500.0,
                },
                {
                    "name": "Microsoft акции",
                    "company_id": microsoft.id,
                    "listed_year": 1986,
                    "ticker": "MSFT",
                    "description": "Акции Microsoft Corp.",
                    "available_count": 750,
                    "price": 300.0,
                },
                {
                    "name": "Tesla акции",
                    "company_id": tesla.id,
                    "listed_year": 2010,
                    "ticker": "TSLA",
                    "description": "Акции Tesla Inc.",
                    "available_count": 200,
                    "price": 700.0,
                },
                {
                    "name": "S&P 500 ETF",
                    "company_id": apple.id,
                    "listed_year": 1993,
                    "ticker": "SPY",
                    "description": "SPDR S&P 500 ETF Trust",
                    "available_count": 2000,
                    "price": 450.0,
                },  # ETF, для примера привязан к Apple, компанию можно сделать "Индексы" или "ETF провайдеры"
                {
                    "name": "Золото",
                    "company_id": google.id,
                    "listed_year": 0,
                    "ticker": "GOLD",
                    "description": "Золото (унция)",
                    "available_count": 5000,
                    "price": 1800.0,
                },  # Золото, для примера привязано к Google, компанию можно сделать "Сырьевые товары"
            ]

            for asset_data in assets_data:
                asset = Asset(**asset_data)
                db.add(asset)
            await db.commit()

            logger.info("Database seeded successfully!")

        except Exception as e:
            logger.info(f"Error seeding database: {e}")
            await db.rollback()
        finally:
            await db.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
