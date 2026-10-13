import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_suppliers(client: AsyncClient):
    response = await client.get("/api/v1/suppliers")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_supplier(client: AsyncClient):
    response = await client.post("/api/v1/suppliers", json={
        "name": "Apple",
        "phone_number": "+79991234567",
        "address": {
            "country": "Russia",
            "city": "Moscow",
            "street": "Tverskaya"
        }
    })

    assert response.status_code == 201

    response = await client.get("/api/v1/suppliers")

    assert response.status_code == 200
    suppliers = response.json()

    assert len(suppliers) == 1
    assert suppliers[0]["name"] == "Apple"


@pytest.mark.asyncio
async def test_get_supplier(client: AsyncClient):
    response = await client.post("/api/v1/suppliers", json={
        "name": "Apple",
        "phone_number": "+79991234567",
        "address": {
            "country": "Russia",
            "city": "Moscow",
            "street": "Tverskaya"
        }
    })

    response = await client.get("/api/v1/suppliers/1")

    assert response.status_code == 200
    suppliers = response.json()

    assert suppliers["name"] == "Apple"


@pytest.mark.asyncio
async def test_get_supplier_not_found(client: AsyncClient):
    response = await client.get("/api/v1/suppliers/1")

    assert response.status_code == 404
    assert response.json() == {'errors': 'Поставщика по id 1 не существует'}