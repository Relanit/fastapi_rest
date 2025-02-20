import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.dependency()
async def test_create_company(admin_client: AsyncClient):
    response = await admin_client.post(
        "/companies/", json={"name": "test company", "profile": "Tech industry leader", "foundation_date": "1990-01-01"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()

    response = await admin_client.post(
        "/companies/", json={"name": "test company 2", "profile": "Finance leader", "foundation_date": "1985-05-15"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()


async def test_create_company_with_invalid_date(admin_client: AsyncClient):
    response = await admin_client.post(
        "/companies/",
        json={"name": "test company invalid", "profile": "Invalid test", "foundation_date": "invalid-date"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


@pytest.mark.dependency(depends=["test_create_company"])
async def test_create_existing_company(admin_client: AsyncClient):
    response = await admin_client.post(
        "/companies/", json={"name": "test company", "profile": "Tech industry leader", "foundation_date": "1990-01-01"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["details"] == "Company already exists"


@pytest.mark.dependency(depends=["test_create_company"])
async def test_get_specific_company(admin_client: AsyncClient):
    response = await admin_client.get("/companies/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Test Company"


async def test_get_nonexistent_company(admin_client: AsyncClient):
    response = await admin_client.get("/companies/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.dependency(depends=["test_create_company"])
async def test_update_company(admin_client: AsyncClient):
    response = await admin_client.put(
        f"/companies/1",
        json={"name": "Updated Company", "profile": "Updated profile", "foundation_date": "1990-01-01"},
    )
    assert response.status_code == status.HTTP_200_OK
    response = await admin_client.get("/companies/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Company"
    assert response.json()["profile"] == "Updated profile"


@pytest.mark.dependency(depends=["test_create_company"])
async def test_partial_update_company(admin_client: AsyncClient):
    response = await admin_client.patch(f"/companies/1", json={"profile": "New profile"})
    assert response.status_code == status.HTTP_200_OK
    response = await admin_client.get("/companies/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["profile"] == "New profile"


@pytest.mark.dependency(depends=["test_create_company"])
async def test_delete_company(client: AsyncClient):
    delete_response = await client.delete("/companies/2")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    get_response = await client.get("/companies/2")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.dependency(depends=["test_create_company"])
async def test_paginated_companies(admin_client: AsyncClient):
    await admin_client.post(
        "/companies/", json={"name": "test company 3", "profile": "bio", "foundation_date": "1990-01-01"}
    )
    await admin_client.post(
        "/companies/", json={"name": "test company 4", "profile": "bio", "foundation_date": "1990-01-01"}
    )
    response = await admin_client.get("/companies/?limit=1&skip=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

    response = await admin_client.get("/companies/?limit=1&skip=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
