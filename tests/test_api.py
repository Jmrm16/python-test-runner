from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_eval_api_endpoint():
    payload = {
        "code": "def square(n):\n    return n * n\n",
        "tests": "def test_square():\n    assert square(5) == 25\n",
        "timeout_seconds": 3.0,
    }
    resp = client.post("/api/v1/eval/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["passed"] is True
    assert data["timed_out"] is False
    assert data["duration_ms"] > 0
