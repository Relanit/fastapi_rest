import json
from decimal import Decimal

import pytest
from httpx import AsyncClient
from fastapi import status

from utils import DecimalEncoder


@pytest.mark.dependency()
async def test_create_transaction_buy(client: AsyncClient):
    json_data = json.dumps({"amount": Decimal("1000.00")}, cls=DecimalEncoder)
    response = await client.post("/balance/top-up", content=json_data)
    assert response.status_code == status.HTTP_200_OK

    transaction_data = {"amount": 2.0}
    response = await client.post("/assets/1/buy/", json=transaction_data["amount"])

    assert response.status_code == status.HTTP_201_CREATED
    response = await client.get("/me/assets")
    assert len(response.json()) == 1
    assert Decimal(response.json()[0]["amount"]) == Decimal(transaction_data["amount"])


async def test_get_all_transactions(admin_client: AsyncClient):
    response = await admin_client.get("/transactions/")
    assert response.status_code == status.HTTP_200_OK
    transactions = response.json()
    assert isinstance(transactions, list)

    for trx in transactions:
        assert "user_id" in trx
        assert "asset_id" in trx
        assert "transaction_datetime" in trx
        assert "amount" in trx


@pytest.mark.dependency(depends=["test_create_transaction_buy"])
async def test_get_specific_transaction(admin_client: AsyncClient):
    transaction_id = 1
    response = await admin_client.get(f"/transactions/{transaction_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == transaction_id


@pytest.mark.dependency(depends=["test_create_transaction_buy"])
async def test_update_transaction(admin_client: AsyncClient):
    transaction_id = 1
    updated_data = {
        "user_id": 2,
        "asset_id": 1,
        "amount": "150.00",
    }

    json_transaction = json.dumps(updated_data, cls=DecimalEncoder)
    response = await admin_client.put(f"/transactions/{transaction_id}", content=json_transaction)
    assert response.status_code == status.HTTP_200_OK

    response_amount_decimal = Decimal(response.json()["amount"])
    updated_amount_decimal = Decimal(updated_data["amount"])
    assert response_amount_decimal == updated_amount_decimal


@pytest.mark.dependency(depends=["test_create_transaction_buy"])
async def test_partial_update_transaction(admin_client: AsyncClient):
    transaction_id = 1
    partial_data = {"amount": "120.00"}

    json_transaction = json.dumps(partial_data, cls=DecimalEncoder)
    response = await admin_client.patch(f"/transactions/{transaction_id}", content=json_transaction)
    assert response.status_code == status.HTTP_200_OK

    response_amount_decimal = Decimal(response.json()["amount"])
    updated_amount_decimal = Decimal(partial_data["amount"])
    assert response_amount_decimal == updated_amount_decimal


@pytest.mark.dependency(depends=["test_create_transaction_buy"])
async def test_delete_transaction(admin_client: AsyncClient):
    transaction_id = 1
    response = await admin_client.delete(f"/transactions/{transaction_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = await admin_client.get(f"/transactions/{transaction_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.dependency(depends=["test_create_transaction_buy"])
async def test_create_transaction_sell(client: AsyncClient):
    transaction_data = {"amount": 2.0}
    response = await client.post("/assets/1/sell/", json=transaction_data["amount"])

    assert response.status_code == status.HTTP_201_CREATED
    response = await client.get("/me/assets")
    assert len(response.json()) == 0
