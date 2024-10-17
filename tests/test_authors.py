from httpx import AsyncClient

from auth.models import User
from tests.conftest import GetAdminAsyncClient


async def test_create_author(get_admin_async_client: GetAdminAsyncClient):
    user = User(username="test", email="test", hashed_password="test", role_id=1)

    client = await get_admin_async_client(user)

    response = await client.post(
        "/authors/", json={"name": "string", "biography": "string", "date_of_birth": "2024-10-14T17:32:48.186"}
    )

    assert response.status_code == 200


async def test_get_specific_author(ac: AsyncClient):
    response = await ac.get("/authors/", params={"name": "string"})

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 1
