from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_analyze_validation_error():
    response = client.post("/analyze", json={})
    assert response.status_code == 422
