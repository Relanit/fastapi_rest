from datetime import date, timedelta

import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.dependency()
async def test_create_borrowing(admin_client: AsyncClient):
    borrow_data = {
        "user_id": 1,
        "book_id": 1,
        "borrow_date": date.today().isoformat(),
        "return_deadline": (date.today() + timedelta(days=30)).isoformat(),
    }

    response = await admin_client.post("/borrowings/", json=borrow_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["user_id"] == borrow_data["user_id"]
    assert response.json()["book_id"] == borrow_data["book_id"]
    assert response.json()["borrow_date"] == borrow_data["borrow_date"]


async def test_get_all_borrowings(admin_client: AsyncClient):
    response = await admin_client.get("/borrowings/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.dependency(depends=["test_create_borrowing"])
async def test_get_specific_borrowing(admin_client: AsyncClient):
    borrowing_id = 1
    response = await admin_client.get(f"/borrowings/{borrowing_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == borrowing_id


@pytest.mark.dependency(depends=["test_create_borrowing"])
async def test_update_borrowing(admin_client: AsyncClient):
    borrowing_id = 1
    updated_data = {
        "user_id": 1,
        "book_id": 1,
        "borrow_date": date.today().isoformat(),
        "return_deadline": (date.today() + timedelta(days=45)).isoformat(),
    }
    response = await admin_client.put(f"/borrowings/{borrowing_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["return_deadline"] == updated_data["return_deadline"]


@pytest.mark.dependency(depends=["test_create_borrowing"])
async def test_partial_update_borrowing(admin_client: AsyncClient):
    borrowing_id = 1
    partial_data = {
        "return_deadline": (date.today() + timedelta(days=60)).isoformat(),
    }
    response = await admin_client.patch(f"/borrowings/{borrowing_id}", json=partial_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["return_deadline"] == partial_data["return_deadline"]


@pytest.mark.dependency(depends=["test_create_borrowing"])
async def test_delete_borrowing(admin_client: AsyncClient):
    borrowing_id = 1
    response = await admin_client.delete(f"/borrowings/{borrowing_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = await admin_client.get(f"/borrowings/{borrowing_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
