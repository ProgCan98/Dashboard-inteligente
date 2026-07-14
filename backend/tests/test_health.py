from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_upload_invalid_extension():
    files = {"file": ("archivo.txt", b"hola", "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400