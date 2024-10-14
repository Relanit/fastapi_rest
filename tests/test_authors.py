from httpx import AsyncClient


async def test_add_specific_author(ac: AsyncClient):
    response = await ac.post(
        "/authors/", json={"id": 1, "name": "string", "biography": "string", "date_of_birth": "2024-10-14T17:32:48.186"}
    )

    assert response.status_code == 200


async def test_get_specific_author(ac: AsyncClient):
    response = await ac.get("/authors/", params={"name": "string"})

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 1
