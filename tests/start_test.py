import pytest
from httpx import AsyncClient
from app.main import app  # Import your FastAPI app

@pytest.mark.asyncio
async def test_login_for_access_token(client):
    form_data = {
        "username": "admin",
        "password": "secret",
    }
    response = await client.post("/token", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_create_qr_code_unauthorized(client):
    # Attempt to create a QR code without authentication
    qr_request = {
        "url": "https://example.com",
        "fill_color": "red",
        "back_color": "white",
        "size": 10,
    }
    response = await client.post("/qr-codes/", json=qr_request)
    assert response.status_code == 401  # Unauthorized

@pytest.mark.asyncio
async def test_create_and_delete_qr_code(client, get_access_token_for_test):
    token = get_access_token_for_test
    headers = {"Authorization": f"Bearer {token}"}

    # Create a QR code
    qr_request = {
        "url": "https://example.com",
        "fill_color": "red",
        "back_color": "white",
        "size": 10,
    }
    create_response = await client.post("/qr-codes/", json=qr_request, headers=headers)
    assert create_response.status_code in [201, 409]  # 201 = Created, 409 = Already exists

    # If it was newly created, try deleting it
    if create_response.status_code == 201:
        qr_code_url = create_response.json()["qr_code_url"]
        qr_filename = qr_code_url.split('/')[-1]
        delete_response = await client.delete(f"/qr-codes/{qr_filename}", headers=headers)
        assert delete_response.status_code == 204  # 204 = No Content 