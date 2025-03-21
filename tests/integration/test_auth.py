import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import insert, select

from database.models import Role
from conftest import async_session_maker


@pytest.mark.dependency()
async def test_add_roles():
    async with async_session_maker() as session:
        stmt = insert(Role).values(id=1, name="user", permissions=None)
        await session.execute(stmt)
        stmt = insert(Role).values(id=2, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        result = await session.execute(query)
        role = result.first()[0]
        expected_role = {"id": 1, "name": "user", "permissions": None}
        result_role = {"id": role.id, "name": role.name, "permissions": role.permissions}
        assert expected_role == result_role


@pytest.mark.dependency(depends=["test_add_roles"])
async def test_register(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "string",
            "role_id": 1,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


async def test_bad_registration(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": 123,
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": 123,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.dependency(depends=["test_register"])
async def test_login(client: AsyncClient):
    response = await client.post(
        "/auth/jwt/login",
        data={
            "username": "user@example.com",
            "password": "string",
        },
    )

    token = response.cookies.get("library")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    client.cookies.set("library", token)


@pytest.mark.dependency(depends=["test_register"])
async def test_bad_login(client: AsyncClient):
    response = await client.post(
        "/auth/jwt/login",
        data={
            "username": "user@example.com",
            "password": "invalid_password",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.dependency(depends=["test_login"])
async def test_logout(client: AsyncClient):
    response = await client.post("/auth/jwt/logout")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    client.cookies.delete("library")
