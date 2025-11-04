from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root_endpoint():
    r = client.get("/")
    assert r.status_code == 200

def test_health():
    r = client.get("/system/health")
    assert r.status_code == 200

def test_reward_admin_post():
    r = client.post("/admin/reward", json={"request_id": "r1", "outcome": "success"})
    assert r.status_code in (200, 201)

def test_logs_post():
    r = client.post("/admin/logs", json={"timestamp": "2025-01-01T00:00:00", "level": "INFO", "message": "test log"})
    assert r.status_code in (200, 201)