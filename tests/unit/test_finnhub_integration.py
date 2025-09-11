import pytest
from decimal import Decimal

from finnhub import FinnhubService, FINNHUB_BASE_URL

pytestmark = pytest.mark.asyncio

MOCK_API_KEY = "test_api_key"
MOCK_AAPL_PROFILE = {"name": "Apple Inc", "ticker": "AAPL", "ipo": "1980-12-12"}
MOCK_AAPL_QUOTE = {"c": 175.50}


@pytest.fixture
async def finnhub_service():
    async with FinnhubService(api_key=MOCK_API_KEY) as service:
        yield service


async def test_get_company_profile_success(httpx_mock, finnhub_service):
    httpx_mock.add_response(
        method="GET", url=f"{FINNHUB_BASE_URL}/stock/profile2?symbol=AAPL&token={MOCK_API_KEY}", json=MOCK_AAPL_PROFILE
    )

    result = await finnhub_service.get_company_profile("AAPL")

    assert result is not None
    assert result["name"] == "Apple Inc"
    assert result["ticker"] == "AAPL"


async def test_get_company_profile_api_error(httpx_mock, finnhub_service):
    httpx_mock.add_response(
        method="GET", url=f"{FINNHUB_BASE_URL}/stock/profile2?symbol=FAIL&token={MOCK_API_KEY}", status_code=404
    )

    result = await finnhub_service.get_company_profile("FAIL")

    assert result is None


async def test_get_asset_price_success(httpx_mock, finnhub_service):
    httpx_mock.add_response(
        method="GET", url=f"{FINNHUB_BASE_URL}/quote?symbol=AAPL&token={MOCK_API_KEY}", json=MOCK_AAPL_QUOTE
    )

    result = await finnhub_service.get_asset_price("AAPL")

    assert result == Decimal("175.50")


async def test_get_asset_price_api_error(httpx_mock, finnhub_service):
    httpx_mock.add_response(
        method="GET", url=f"{FINNHUB_BASE_URL}/quote?symbol=FAIL&token={MOCK_API_KEY}", status_code=500
    )

    result = await finnhub_service.get_asset_price("FAIL")

    assert result is None
