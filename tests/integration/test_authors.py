import pytest
from httpx import AsyncClient

from fastapi import status


@pytest.mark.dependency()
async def test_create_author(admin_client: AsyncClient):
    response = await admin_client.post(
        "/authors/", json={"name": "test author", "biography": "Test bio", "date_of_birth": "1990-01-01"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()

    response = await admin_client.post(
        "/authors/", json={"name": "test author 2", "biography": "Test bio", "date_of_birth": "1990-01-01"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()


async def test_create_author_with_invalid_date(admin_client: AsyncClient):
    response = await admin_client.post(
        "/authors/", json={"name": "test author invalid", "biography": "Test bio", "date_of_birth": "invalid-date"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


@pytest.mark.dependency(depends=["test_create_author"])
async def test_create_existing_author(admin_client: AsyncClient):
    response = await admin_client.post(
        "/authors/", json={"name": "test author", "biography": "Test bio", "date_of_birth": "1990-01-01"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["details"] == "Author already exists"


@pytest.mark.dependency(depends=["test_create_author"])
async def test_get_specific_author(admin_client: AsyncClient):
    response = await admin_client.get("/authors/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Test Author"


async def test_get_nonexistent_author(admin_client: AsyncClient):
    response = await admin_client.get("/authors/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.dependency(depends=["test_create_author"])
async def test_update_author(admin_client: AsyncClient):
    response = await admin_client.put(
        f"/authors/1",
        json={"name": "Updated Author", "biography": "Updated bio", "date_of_birth": "1990-01-01"},
    )
    assert response.status_code == status.HTTP_200_OK

    response = await admin_client.get("/authors/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Author"
    assert response.json()["biography"] == "Updated bio"


@pytest.mark.dependency(depends=["test_create_author"])
async def test_partial_update_author(admin_client: AsyncClient):
    response = await admin_client.patch(f"/authors/1", json={"biography": "New bio"})
    assert response.status_code == status.HTTP_200_OK

    response = await admin_client.get("/authors/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["biography"] == "New bio"


@pytest.mark.dependency(depends=["test_create_author"])
async def test_delete_author(client: AsyncClient):
    delete_response = await client.delete("/authors/2")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    get_response = await client.get("/authors/2")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.dependency(depends=["test_create_author"])
async def test_paginated_authors(admin_client: AsyncClient):
    await admin_client.post(
        "/authors/", json={"name": "test author 3", "biography": "bio", "date_of_birth": "1990-01-01"}
    )
    await admin_client.post(
        "/authors/", json={"name": "test author 4", "biography": "bio", "date_of_birth": "1990-01-01"}
    )

    response = await admin_client.get("/authors/?limit=1&skip=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

    response = await admin_client.get("/authors/?limit=1&skip=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
