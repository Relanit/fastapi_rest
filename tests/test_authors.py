from httpx import AsyncClient

from auth.models import User
from tests.conftest import GetAdminClient


async def test_create_author(get_admin_client: GetAdminClient):
    user = User(username="test", email="admin@test.com", hashed_password="test", role_id=2)
    client = await get_admin_client(user)

    response = await client.post(
        "/authors/", json={"name": "name", "biography": "bio", "date_of_birth": "2024-10-14T17:32:48.186"}
    )

    assert response.status_code == 201


async def test_get_specific_author(client: AsyncClient):
    response = await client.get("/authors/1")

    assert response.status_code == 200
    assert response.json()["name"] == "name"


async def test_update_author(get_admin_client: GetAdminClient):
    user = User(username="test", email="admin@test.com", hashed_password="test", role_id=2)
    client = await get_admin_client(user)

    response = await client.put(
        f"/authors/1",
        json={"name": "updated_name", "biography": "updated_bio", "date_of_birth": "2024-10-14T17:32:48.186"},
    )
    assert response.status_code == 200

    response = await client.get("/authors/1")
    assert response.status_code == 200
    assert response.json()["name"] == "updated_name"
    assert response.json()["biography"] == "updated_bio"


async def test_delete_author(get_admin_client: GetAdminClient):
    user = User(username="test", email="admin@test.com", hashed_password="test", role_id=2)
    client = await get_admin_client(user)

    delete_response = await client.delete("/authors/1")
    assert delete_response.status_code == 204

    get_response = await client.get("/authors/1")
    assert get_response.status_code == 404
