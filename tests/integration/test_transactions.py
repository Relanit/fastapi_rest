import json
from datetime import date, timedelta
from decimal import Decimal

import pytest
from httpx import AsyncClient
from fastapi import status

from utils import DecimalEncoder


@pytest.mark.dependency()
async def test_create_transaction(client: AsyncClient):
    data = {"amount": Decimal("1000.00")}
    json_data = json.dumps(data, cls=DecimalEncoder)
    response = await client.post("/balance/top-up", content=json_data)
    assert response.status_code == status.HTTP_200_OK

    transaction_data = {
        "user_id": 2,
        "asset_id": 1,
        "purchase_date": date.today().isoformat(),
        "target_sell_date": (date.today() + timedelta(days=30)).isoformat(),
        "amount": "60.00",
    }

    json_transaction = json.dumps(transaction_data, cls=DecimalEncoder)
    response = await client.post("/transactions/", content=json_transaction)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["user_id"] == transaction_data["user_id"]
    assert response.json()["asset_id"] == transaction_data["asset_id"]
    assert response.json()["purchase_date"] == transaction_data["purchase_date"]

    response_amount_decimal = Decimal(response.json()["amount"])
    transaction_amount_decimal = Decimal(transaction_data["amount"])
    assert response_amount_decimal == transaction_amount_decimal


async def test_get_all_transactions(admin_client: AsyncClient):
    response = await admin_client.get("/transactions/")
    assert response.status_code == status.HTTP_200_OK
    transactions = response.json()
    assert isinstance(transactions, list)

    for trx in transactions:
        assert "user_id" in trx
        assert "asset_id" in trx
        assert "purchase_date" in trx
        assert "target_sell_date" in trx
        assert "amount" in trx


@pytest.mark.dependency(depends=["test_create_transaction"])
async def test_get_specific_transaction(admin_client: AsyncClient):
    transaction_id = 1
    response = await admin_client.get(f"/transactions/{transaction_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == transaction_id


@pytest.mark.dependency(depends=["test_create_transaction"])
async def test_update_transaction(admin_client: AsyncClient):
    transaction_id = 1
    updated_data = {
        "user_id": 2,
        "asset_id": 1,
        "purchase_date": date.today().isoformat(),
        "target_sell_date": (date.today() + timedelta(days=45)).isoformat(),
        "sell_date": date.today().isoformat(),
        "amount": "150.00",
    }

    json_transaction = json.dumps(updated_data, cls=DecimalEncoder)
    response = await admin_client.put(f"/transactions/{transaction_id}", content=json_transaction)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["target_sell_date"] == updated_data["target_sell_date"]

    response_amount_decimal = Decimal(response.json()["amount"])
    updated_amount_decimal = Decimal(updated_data["amount"])
    assert response_amount_decimal == updated_amount_decimal


@pytest.mark.dependency(depends=["test_create_transaction"])
async def test_partial_update_transaction(admin_client: AsyncClient):
    transaction_id = 1
    partial_data = {
        "target_sell_date": (date.today() + timedelta(days=60)).isoformat(),
    }
    response = await admin_client.patch(f"/transactions/{transaction_id}", json=partial_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["target_sell_date"] == partial_data["target_sell_date"]


@pytest.mark.dependency(depends=["test_create_transaction"])
async def test_delete_transaction(admin_client: AsyncClient):
    transaction_id = 1
    response = await admin_client.delete(f"/transactions/{transaction_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = await admin_client.get(f"/transactions/{transaction_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
