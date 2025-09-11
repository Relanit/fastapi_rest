import asyncio

from celery import Celery
from celery.schedules import crontab
from sqlalchemy import select

import database
from database.database import setup_database, dispose_database_engine, _async_session_maker
from database.models import Asset
from config import config
from finnhub import FinnhubService
from logger import logger

celery = Celery("fastapi_rest", broker="redis://redis:5370/0", backend="redis://redis:5370/0")


@celery.task
def update_asset_prices():
    logger.info("Starting asset price update task.")
    asyncio.run(async_update_prices())


async def async_update_prices():
    database.database.setup_database()
    SessionMaker = database.database._async_session_maker

    if SessionMaker is None:
        logger.error("SessionMaker is None after setup_database. Aborting task.")
        return

    try:
        async with FinnhubService(api_key=config.FINNHUB_API_KEY) as finnhub:
            async with SessionMaker() as db:
                result = await db.execute(select(Asset))
                assets = result.scalars().all()

                for asset in assets:
                    try:
                        logger.info(f"Updating price for {asset.ticker}...")
                        new_price = await finnhub.get_asset_price(asset.ticker)

                        if new_price is not None:
                            asset.price = new_price
                            logger.info(f"Successfully updated {asset.ticker} price to {new_price}")
                        else:
                            logger.warning(f"Received invalid price for {asset.ticker}. Skipping update.")
                    except Exception as e:
                        logger.error(f"An error occurred while updating {asset.ticker}: {e}")

                await db.commit()
                logger.info("Asset price update task finished successfully.")

    except Exception as e:
        logger.error(f"A critical error occurred in async_update_prices: {e}")

    finally:
        logger.info("Disposing database engine for the task.")
        await dispose_database_engine()


celery.conf.beat_schedule = {
    "update-prices-every-5-minutes": {
        "task": "tasks.update_asset_prices",
        "schedule": crontab(minute="*/5"),
    },
}
celery.conf.timezone = "UTC"
