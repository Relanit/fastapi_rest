from httpx import AsyncClient
from sqlalchemy import insert, select

from auth.models import Role
from tests.conftest import async_session_maker


async def test_add_role():
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


async def test_register(ac: AsyncClient):
    response = await ac.post(
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

    assert response.status_code == 201
