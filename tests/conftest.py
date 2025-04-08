import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

@pytest_asyncio.fixture
async def get_access_token_for_test(client):
    form_data = {"username": "admin", "password": "secret"}
    response = await client.post("/token", data=form_data)
    return response.json()["access_token"]
