import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_admin_endpoint_without_auth():
    """Test that admin endpoints require authentication"""
    response = client.post("/admin/reward", json={
        "request_id": "test123",
        "outcome": "success"
    })
    assert response.status_code == 401

def test_admin_endpoint_with_invalid_auth():
    """Test that admin endpoints reject invalid API keys"""
    response = client.post("/admin/reward", 
                          json={
                              "request_id": "test123",
                              "outcome": "success"
                          },
                          headers={"X-API-Key": "invalid-key"})
    assert response.status_code == 401

def test_agent_endpoint_without_auth():
    """Test that agent endpoints require authentication"""
    response = client.post("/agent/", json={
        "team_id": "team123",
        "prompt": "Hello, world!"
    })
    assert response.status_code == 401

def test_public_endpoint_without_auth():
    """Test that public endpoints don't require authentication"""
    response = client.get("/system/health")
    assert response.status_code == 200

def test_cors_configuration():
    """Test that CORS is properly configured"""
    response = client.options("/system/health", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    })
    assert response.status_code == 200