import asyncio
from decimal import Decimal
import httpx

from celery import Celery
from celery.schedules import crontab
from sqlalchemy import select

from database.database import async_session_maker
from database.models import Asset
from config import config
from logger import logger


celery = Celery("fastapi_rest", broker="redis://redis:5370/0", backend="redis://redis:5370/0")


FINNHUB_BASE_URL = "https://finnhub.io/api/v1"


@celery.task
def update_asset_prices():
    logger.info("Starting asset price update task.")
    asyncio.run(async_update_prices())


async def async_update_prices():
    async with async_session_maker() as db:
        try:
            result = await db.execute(select(Asset))
            assets = result.scalars().all()

            async with httpx.AsyncClient() as client:
                for asset in assets:
                    try:
                        logger.info(f"Updating price for {asset.ticker}...")
                        res = await client.get(
                            f"{FINNHUB_BASE_URL}/quote",
                            params={"symbol": asset.ticker, "token": config.FINNHUB_API_KEY},
                        )
                        res.raise_for_status()
                        quote_data = res.json()

                        new_price = Decimal(str(quote_data.get("c", 0.0)))

                        if new_price > 0:
                            asset.price = new_price
                            logger.info(f"Successfully updated {asset.ticker} price to {new_price}")
                        else:
                            logger.warning(f"Received invalid price for {asset.ticker}. Skipping update.")

                    except httpx.HTTPStatusError as e:
                        logger.error(f"Failed to fetch price for {asset.ticker}: {e.response.status_code}")
                    except Exception as e:
                        logger.error(f"An error occurred while updating {asset.ticker}: {e}")

            await db.commit()
            logger.info("Asset price update task finished successfully.")
        except Exception as e:
            logger.error(f"A critical error occurred in async_update_prices: {e}")
            await db.rollback()


celery.conf.beat_schedule = {
    "update-prices-every-5-minutes": {
        "task": "tasks.update_asset_prices",
        "schedule": crontab(minute="*/5"),
    },
}

celery.conf.timezone = "UTC"
