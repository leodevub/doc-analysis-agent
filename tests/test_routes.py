from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token():
    response = client.post("/token", data={
        "username": "admin",
        "password": "admin123"
    })
    return response.json()["access_token"]

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_login_success():
    response = client.post("/token", data={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    response = client.post("/token", data={
        "username": "admin",
        "password": "senhaerrada"
    })
    assert response.status_code == 401

def test_ask_without_token():
    response = client.post("/ask", params={"question": "teste"})
    assert response.status_code == 401

def test_ask_with_token():
    token = get_token()
    response = client.post(
        "/ask",
        params={"question": "o que é esmalte?"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "answer" in response.json()