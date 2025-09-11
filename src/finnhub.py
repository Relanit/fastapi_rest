from decimal import Decimal
from typing import Any

import httpx

from logger import logger

FINNHUB_BASE_URL = "https://finnhub.io/api/v1"


class FinnhubService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Finnhub API key is required.")

        self._api_key = api_key
        self._client = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(params={"token": self._api_key})
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get_company_profile(self, ticker: str) -> dict[str, Any] | None:
        try:
            response = await self._client.get(f"{FINNHUB_BASE_URL}/stock/profile2", params={"symbol": ticker})
            response.raise_for_status()
            profile = response.json()
            return profile if profile else None
        except (httpx.HTTPStatusError, KeyError) as e:
            logger.info(f"Could not fetch profile for {ticker}: {e}")
            return None

    async def get_asset_price(self, ticker: str) -> Decimal | None:
        try:
            response = await self._client.get(f"{FINNHUB_BASE_URL}/quote", params={"symbol": ticker})
            response.raise_for_status()
            quote_data = response.json()
            price = Decimal(str(quote_data.get("c", "0.0")))
            return price if price > 0 else None
        except (httpx.HTTPStatusError, KeyError, ValueError) as e:
            logger.info(f"Could not fetch price for {ticker}: {e}")
            return None
