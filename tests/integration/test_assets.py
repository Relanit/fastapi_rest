import pytest
from httpx import AsyncClient

from fastapi import status


@pytest.mark.dependency()
async def test_create_asset(client: AsyncClient):
    asset_data = {
        "name": "Test Asset",
        "listed_year": 2022,
        "ticker": "TST",
        "description": "A test asset description.",
        "available_count": 100,
        "price": 50.5,
        "company_id": 1,
    }
    response = await client.post("/assets/", json=asset_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == asset_data["name"]
    assert data["company_id"] == asset_data["company_id"]

    asset_data = {
        "name": "Test Asset 2",
        "listed_year": 2022,
        "ticker": "TST2",
        "description": "Another test asset.",
        "available_count": 200,
        "price": 75.0,
        "company_id": 1,
    }
    await client.post("/assets/", json=asset_data)


async def test_create_asset_invalid_company(admin_client: AsyncClient):
    asset_data = {
        "name": "Invalid Asset",
        "listed_year": 2022,
        "ticker": "INV",
        "description": "Invalid asset for testing.",
        "available_count": 50,
        "price": 30.0,
        "company_id": 999,
    }
    response = await admin_client.post("/assets/", json=asset_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_assets(admin_client: AsyncClient):
    response = await admin_client.get("/assets/")
    assert response.status_code == status.HTTP_200_OK
    assets = response.json()
    assert isinstance(assets, list)
    for asset in assets:
        assert "ticker" in asset, f"Asset missing ticker: {asset}"
        assert "description" in asset, f"Asset missing description: {asset}"
        assert "available_count" in asset, f"Asset missing available_count: {asset}"
        assert "price" in asset, f"Asset missing price: {asset}"
        assert "company_id" in asset, f"Asset missing company_id: {asset}"


@pytest.mark.dependency(depends=["test_create_asset"])
async def test_get_assets_by_company(admin_client: AsyncClient):
    response = await admin_client.get("/assets/", params={"company_id": 1})
    assert response.status_code == status.HTTP_200_OK
    assets = response.json()
    for asset in assets:
        assert asset["company_id"] == 1


@pytest.mark.dependency(depends=["test_create_asset"])
async def test_get_specific_asset(admin_client: AsyncClient):
    response = await admin_client.get("/assets/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 1


@pytest.mark.dependency(depends=["test_create_asset"])
async def test_search_assets(admin_client: AsyncClient):
    response = await admin_client.get("/assets/search/?search_query=test asset")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "Test Asset"


@pytest.mark.dependency(depends=["test_create_asset"])
async def test_update_asset(admin_client: AsyncClient):
    updated_data = {
        "company_id": 1,
        "name": "Updated Test Asset",
        "listed_year": 2023,
        "ticker": "UPDT",
        "description": "Updated asset description.",
        "available_count": 150,
        "price": 60.0,
    }
    response = await admin_client.put("/assets/1", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == updated_data["name"]


@pytest.mark.dependency(depends=["test_create_asset"])
async def test_partial_update_asset(admin_client: AsyncClient):
    updated_data = {
        "name": "Partially Updated Asset",
    }
    response = await admin_client.patch("/assets/1", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == updated_data["name"]


@pytest.mark.dependency(depends=["test_create_asset"])
async def test_delete_asset(admin_client: AsyncClient):
    response = await admin_client.delete("/assets/2")
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_nonexistent_asset(admin_client: AsyncClient):
    response = await admin_client.delete("/assets/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
