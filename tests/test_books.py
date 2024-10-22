import pytest
from httpx import AsyncClient

from fastapi import status


@pytest.mark.dependency()
async def test_create_book(client: AsyncClient):
    book_data = {
        "title": "Test Book",
        "published_year": 2022,
        "isbn": "123-4567890123",
        "description": "A test book description.",
        "available_count": 10,
        "author_id": 1,
    }
    response = await client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["author_id"] == book_data["author_id"]


async def test_create_book_invalid_author(admin_client: AsyncClient):
    book_data = {
        "title": "Test Book",
        "published_year": 2022,
        "isbn": "123-4567890123",
        "description": "A test book description.",
        "available_count": 10,
        "author_id": 999,
    }
    response = await admin_client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_books(admin_client: AsyncClient):
    response = await admin_client.get("/books/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.dependency(depends=["test_create_book"])
async def test_get_books_by_author(admin_client: AsyncClient):
    response = await admin_client.get("/books/", params={"author_id": 1})
    assert response.status_code == status.HTTP_200_OK
    books = response.json()
    for book in books:
        assert book["author_id"] == 1


@pytest.mark.dependency(depends=["test_create_book"])
async def test_get_specific_book(admin_client: AsyncClient):
    response = await admin_client.get("/books/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 1


@pytest.mark.dependency(depends=["test_create_book"])
async def test_update_book(admin_client: AsyncClient):
    updated_data = {
        "title": "Updated Test Book",
        "published_year": 2023,
        "isbn": "987-6543210987",
        "description": "Updated description.",
        "available_count": 15,
    }
    response = await admin_client.put("/books/1", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == updated_data["title"]


@pytest.mark.dependency(depends=["test_create_book"])
async def test_partial_update_book(admin_client: AsyncClient):
    updated_data = {
        "title": "Partially Updated Test Book",
    }
    response = await admin_client.patch("/books/1", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == updated_data["title"]


@pytest.mark.dependency(depends=["test_create_book"])
async def test_delete_book(admin_client: AsyncClient):
    response = await admin_client.delete("/books/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_nonexistent_book(admin_client: AsyncClient):
    response = await admin_client.delete("/books/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
